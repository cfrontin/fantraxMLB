from pprint import pprint

import pandas as pd

from baseballprospectus import append_fantraxIDs, load_baseballprospectus_data
from utils import *
from fantraxAPI import *

secrets = load_secrets()

dump_to_json("playerIDs.json", fetch_playerIDs())

playerADP = fetch_playerADP()
leagueList = fetch_leagueList()

for leagueData in leagueList["leagues"]:
    leagueName = leagueData["leagueName"]
    leagueSport = leagueData["sport"]
    leagueId = leagueData["leagueId"]
    print(f"\n{leagueName} in {leagueSport} ({leagueId})")
    leagueInfo = fetch_leagueInfo(leagueId)
    dump_to_json(f"{leagueName.replace(' ', '_')}_info.json", leagueInfo)
    draftResults = fetch_draftResults(leagueId)
    dump_to_json(f"{leagueName.replace(' ', '_')}_draft.json", draftResults)
    teamRosters = fetch_teamRosters(leagueId)
    leagueStandings = fetch_leagueStandings(leagueId)

# get the map of player IDs
df_idmap = load_playerIDMap()

# get BP/PECOTA predictions, map to points projections
df_pecota_hitting, df_pecota_pitching = load_baseballprospectus_data(50)
df_pecota_hitting = append_fantraxIDs(df_pecota_hitting, df_idmap)
df_pecota_pitching = append_fantraxIDs(df_pecota_pitching, df_idmap)

# df_pecota_hitting.join(df_datamap, on=["mlbid", ""])

print()
print(
    df_pecota_hitting[["name", "bpid", "fantraxid", "warp"]].sort_values(
        "warp", ascending=False
    )
)
print()
print(
    df_pecota_pitching[["name", "bpid", "fantraxid", "warp"]].sort_values(
        "warp", ascending=False
    )
)

# get current stats from somewhere, map to points projections
# ###
