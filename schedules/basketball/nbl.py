
import dateutil.parser
import requests

"""Get NBA Schedule From SportRadar API"""


def get_NBL_schedule(year, month, day):
    api_key = "b2cw3vh9s9vz5srr3xnkwkka"
    nba_url = "https://api.sportradar.us/basketball-t1/en/tournaments/sr:tournament:1524/schedule.json?api_key={key}".format(
        key=api_key)
    data_raw = requests.get(nba_url)
    data_json = data_raw.json()
    nbl_games = []
    for game in data_json['sport_events']:
        gameTime = game["scheduled"]
        gameDateTime = dateutil.parser.isoparse(gameTime)
        # If its on the day that we give
        if(game['status'] != "cancelled"):
            if gameDateTime.year == int(year) and gameDateTime.month == int(month) and (gameDateTime.day == int(day) or gameDateTime.day == int(day)+1):
                # Process and add to the array of games
                gameId = game["id"]
                sport = "basketball"
                league = "NBL"
                home = game["competitors"][0]['name']  # Tasmanian Jackjumpers
                away = game["competitors"][1]['name']  # Brisbane Bullets
                nbl_games.append({
                    "gameId": gameId,
                    "sport": sport,
                    "league": league,
                    "home": home,
                    "away": away,
                    "gameTime": gameDateTime,
                    "urls": [
                        {"bookie": "bet365", "urls": [
                            "https://bet365.com.au"]},
                        {"bookie": "topsport", "urls": [
                            "https://www.topsport.com.au/PlayerBets"]}
                    ]})
    return nbl_games


"""Debug If Running as Main"""
if __name__ == "__main__":
    day = input("Day: ")
    month = input("Month: ")
    year = input("Year: ")
    print(get_NBL_schedule(year, month, day))
