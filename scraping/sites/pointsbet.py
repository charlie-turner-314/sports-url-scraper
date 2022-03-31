import json
import random

import requests
from schedules.basketball.nbl import get_NBL_schedule

from ..headers import user_agents


def add_pointsbet_urls(schedule, leagues):
    for league in leagues:
        if league == "nba":
            add_games(schedule, 7176)
        elif league == "nbl":
            add_games(schedule, 7172)


def add_games(schedule, competitionId):
    pb_base = "https://pointsbet.com.au/sports/basketball/NBA/"
    data = requests.get("https://api.pointsbet.com/api/v2/competitions/{}/events/featured?includeLive=false&page=1".format(competitionId), headers={
        "referer": "https://pointsbet.com.au/", "user-agent": random.choice(user_agents)})
    try:
        eventsjson = json.loads(data.text)
    except:
        print("Could not get json from pointsbet data:")
        print(data)
        return
    pointsbet_games = []
    for event in eventsjson['events']:
        pointsbet_games.append(
            {
                'key': event['key'],
                'home': event['homeTeam'],
                'away': event['awayTeam'],
            }
        )
    for event in pointsbet_games:
        for game in schedule:
            if game['home'].split(" ")[-1].lower() in event['home'].lower() and game['away'].split(" ")[-1].lower() in event['away'].lower():
                game['urls'].append(
                    {'bookie': 'pointsbet', 'urls': [pb_base + event['key']]})
                print("Pointsbet URL - Home: " + game['home'])


if __name__ == "__main__":
    day = input("Day: ")
    month = input("Month: ")
    year = input("Year: ")
    schedule = get_NBL_schedule(year, month, day)
    add_pointsbet_urls(schedule, ['nbl'])
    print(schedule)
