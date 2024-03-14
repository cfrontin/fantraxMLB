import os

import json
import requests

def load_secrets():
  fn_secrets = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "fantrax.secrets",
  )
  with open(fn_secrets, "r") as fsecrets:
    secrets = json.load(fsecrets)
  return secrets

def dump_to_json(fn_json, data):
  with open(fn_json, "w") as f_json:
    json.dump(data, f_json, indent=4)

def rest_request(
  url,
  body,
  note="",
  headers={"Content-Type":"application/json"},
):
  response = requests.post(
    url,
    data=json.dumps(body),
    headers=headers,
  )
  print(f"{note}status code:", response.status_code)
  return response.json()

def fetch_playerIDs(
    sport="MLB",
    # secrets=load_secrets(),
):
  url_playerIDs = f"https://www.fantrax.com/fxea/general/getPlayerIds"
  body_playerIDs = {
    "sport":sport,
  }
  result = rest_request(
    url_playerIDs,
    body_playerIDs,
    note="requesting player IDs. ",
  )

  return result

def fetch_playerADP(
    position=None,
    showAllPositions=True,
    start=None,
    limit=None,
    sport="MLB",
    # secrets=load_secrets(),
):
  url_playerADP = "https://www.fantrax.com/fxea/general/getAdp"
  body_playerADP = {
    "sport":sport,
    "position":position,
    "showAllPositions":showAllPositions,
    "start":start,
    "limit":limit,
  }
  to_pop = []
  for k, v in body_playerADP.items():
    if v is None:
      to_pop.append(k)
  [body_playerADP.pop(k) for k in to_pop]
  playerADPs = rest_request(
    url_playerADP,
    body_playerADP,
    note="requesting player ADP. ",
  )
  return playerADPs

def fetch_leagueList(
  secrets=load_secrets(),
):
  url_leagueList = "https://www.fantrax.com/fxea/general/getLeagues"
  body_leagueList = {
    "userSecretId":secrets["secret_id"],
  }
  leagueList = rest_request(
    url_leagueList,
    body_leagueList,
    note="requesting league list. ",
  )
  return leagueList

def fetch_leagueInfo(
    leagueId,
    secrets=load_secrets(),
):
  url_leagueInfo = f"https://www.fantrax.com/fxea/general/getLeagueInfo?leagueId={leagueId}"
  body_leagueInfo = {
    # "leagueId":secrets["league_id"],
  }
  leagueInfo = rest_request(
    url_leagueInfo,
    body_leagueInfo,
    note="requesting league info. ",
  )
  return leagueInfo

def fetch_draftResults(
    leagueId,
    secrets=load_secrets(),
):
  url_draftResults = f"https://www.fantrax.com/fxea/general/getDraftResults?leagueId={leagueId}"
  body_draftResults = {
    # "leagueId":secrets["league_id"],
  }
  draftResults = rest_request(
    url_draftResults,
    body_draftResults,
    note="requesting draft results. ",
  )
  return draftResults

def fetch_teamRosters(
    leagueId,
    secrets=load_secrets(),
):
  url_teamRosters = f"https://www.fantrax.com/fxea/general/getTeamRosters?leagueId={leagueId}"
  body_teamRosters = {
    # "leagueId":secrets["league_id"],
  }
  teamRosters = rest_request(
    url_teamRosters,
    body_teamRosters,
    note="requesting team rosters. ",
  )
  return teamRosters

def fetch_leagueStandings(
    leagueId,
    secrets=load_secrets(),
):
  url_leagueStandings = f"https://www.fantrax.com/fxea/general/getLeagueStandings?leagueId={leagueId}"
  body_leagueStandings = {
    # "leagueId":secrets["league_id"],
  }
  leagueStandings = rest_request(
    url_leagueStandings,
    body_leagueStandings,
    note="requesting league standings. ",
  )
  return leagueStandings

