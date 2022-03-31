import dateutil.parser
import requests

"""Get NBA Schedule From SportRadar API"""


def get_NBA_schedule(year, month, day):
    api_key = "z9259s3ab22u98xt6ekphfnf"
    nba_url = "https://api.sportradar.us/nba/trial/v7/en/games/{year}/{month}/{day}/schedule.json?api_key={key}".format(
        year=year, month=month, day=day, key=api_key)
    data_raw = requests.get(nba_url)
    if not data_raw:
        return []
    data_json = data_raw.json()
    nba_games = []
    for game in data_json['games']:
        gameId = game["id"]
        sport = "basketball"
        league = "NBA"
        home = game["home"]["name"]  # Orlando Magic
        away = game["away"]["name"]  # Detroit Pistons
        gameTime = game["scheduled"]
        nba_games.append({
            "gameId": gameId,
            "sport": sport,
            "league": league,
            "home": home,
            "away": away,
            "gameTime": dateutil.parser.isoparse(gameTime),
            "urls": [
                {"bookie": "bet365", "urls": ["https://bet365.com.au"]},
                {"bookie": "topsport", "urls": [
                    "https://www.topsport.com.au/PlayerBets"]}
            ]})
    return nba_games


"""Debug If Running as Main"""
if __name__ == "__main__":
    day = input("Day: ")
    month = input("Month: ")
    year = input("Year: ")
    print(get_NBA_schedule(year, month, day))
