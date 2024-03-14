
from pprint import pprint

import pandas as pd

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

# # see https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary
# # to do this better
# playerIDs = pd.DataFrame(fetch_playerIDs())
# print(playerIDs)


