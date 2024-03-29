from baseballprospectus import append_fantraxIDs, merge_hittingpitching
from baseballprospectus import load_baseballprospectus_data
from baseballprospectus import append_fantrax_scoring

from utils import *
from fantraxAPI import *


def load_war_room_data(percentile=50):

    # get the map of player IDs
    df_idmap = load_playerIDMap()

    # get BP/PECOTA predictions, map to points projections
    df_pecota_hitting, df_pecota_pitching = load_baseballprospectus_data(percentile)

    # append fantrax info to BP dataframes
    df_pecota_hitting = append_fantraxIDs(df_pecota_hitting, df_idmap)
    df_pecota_pitching = append_fantraxIDs(df_pecota_pitching, df_idmap)
    df_pecota_hitting = append_fantrax_scoring(df_pecota_hitting, pitching=False)
    df_pecota_pitching = append_fantrax_scoring(df_pecota_pitching, pitching=True)

    # merge hitting and pitching
    df_pecota_all = merge_hittingpitching(
        df_pecota_hitting, df_pecota_pitching, has_fantrax=True
    )

    # return the results
    return df_idmap, df_pecota_hitting, df_pecota_pitching, df_pecota_all


def load_draft(df_merge=None, debug=False):
    draft = fetch_draftResults()
    df_teams = pd.DataFrame(fetch_leagueInfo()["teamInfo"]).T
    df_teams.rename(
        columns={"id": "teamId", "name": "teamName", "division": "teamDiv"},
        inplace=True,
    )

    df_draft_in = (
        pd.DataFrame(draft["draftPicks"])
        .sort_values(["round", "pick"])
        .reset_index(drop=True)
    )
    if debug:
        assert df_merge is not None
        df_merge = df_merge.sort_values("warp", ascending=False)
        df_draft_in.loc[:20, ("playerId",)] = df_merge.fantraxid[:20]
    df_draft_in = df_draft_in.dropna()
    df_draft_in = df_draft_in.merge(df_teams, on="teamId", how="left")
    df_draft_out = df_draft_in.copy()
    df_merge_out = df_merge.copy()

    if df_merge is not None:
        df_draft_out = df_draft_out.merge(
            df_merge, left_on="playerId", right_on="fantraxid"
        )
        df_merge_out = df_merge_out.merge(
            df_draft_in, left_on="fantraxid", right_on="playerId", how="left"
        )
        df_merge_out.sort_values("fpts", ascending=False, inplace=True)
        df_merge_out["teamName"] = df_merge_out.teamName.replace(pd.NA, "undrafted")

    return df_draft_out, df_merge_out
