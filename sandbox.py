
from pprint import pprint

import pandas as pd

from fantraxAPI import *

secrets = load_secrets()

with open("playerIDs.json", "w") as fjson:
    json.dump(fetch_playerIDs(), fjson, indent=4)

playerADP = fetch_playerADP()
leagueList = fetch_leagueList()

for leagueData in leagueList["leagues"]:
    leagueName = leagueData["leagueName"]
    leagueSport = leagueData["sport"]
    leagueId = leagueData["leagueId"]
    print(f"\n{leagueName} in {leagueSport} ({leagueId})")
    leagueInfo = fetch_leagueInfo(leagueId)
    draftResults = fetch_draftResults(leagueId)
    teamRosters = fetch_teamRosters(leagueId)
    leagueStandings = fetch_leagueStandings(leagueId)

# # see https://stackoverflow.com/questions/13575090/construct-pandas-dataframe-from-items-in-nested-dictionary
# # to do this better
# playerIDs = pd.DataFrame(fetch_playerIDs())
# print(playerIDs)


