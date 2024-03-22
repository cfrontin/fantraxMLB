from utils import load_secrets, rest_request


def fetch_playerIDs(
    sport="MLB",
    # secrets=load_secrets(),
):
    url_playerIDs = f"https://www.fantrax.com/fxea/general/getPlayerIds"
    body_playerIDs = {
        "sport": sport,
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
        "sport": sport,
        "position": position,
        "showAllPositions": showAllPositions,
        "start": start,
        "limit": limit,
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
        "userSecretId": secrets["secret_id"],
    }
    leagueList = rest_request(
        url_leagueList,
        body_leagueList,
        note="requesting league list. ",
    )
    return leagueList


def fetch_leagueInfo(
    leagueId=None,
    secrets=load_secrets(),
):
    if leagueId is None:
        leagueId=secrets["league_id"]

    url_leagueInfo = (
        f"https://www.fantrax.com/fxea/general/getLeagueInfo?leagueId={leagueId}"
    )
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
    leagueId=None,
    secrets=load_secrets(),
):
    if leagueId is None: leagueId = secrets["league_id"]

    url_draftResults = (
        f"https://www.fantrax.com/fxea/general/getDraftResults?leagueId={leagueId}"
    )
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
    leagueId=None,
    secrets=load_secrets(),
):
    if leagueId is None: leagueId = secrets["league_id"]

    url_teamRosters = (
        f"https://www.fantrax.com/fxea/general/getTeamRosters?leagueId={leagueId}"
    )
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
    leagueId=None,
    secrets=load_secrets(),
):
    if leagueId is None: leagueId = secrets["league_id"]

    url_leagueStandings = (
        f"https://www.fantrax.com/fxea/general/getLeagueStandings?leagueId={leagueId}"
    )
    body_leagueStandings = {
        # "leagueId":secrets["league_id"],
    }
    leagueStandings = rest_request(
        url_leagueStandings,
        body_leagueStandings,
        note="requesting league standings. ",
    )
    return leagueStandings
