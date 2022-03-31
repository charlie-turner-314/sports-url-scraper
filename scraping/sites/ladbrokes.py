import json
import random

import requests
from schedules.basketball.nba import get_NBA_schedule
from schedules.basketball.nbl import get_NBL_schedule

from ..headers import user_agents


def add_ladbrokes_urls(schedule, leagues):
    scrape_fixtures(schedule, leagues)


def scrape_fixtures(schedule, leagues):
    league_base_urls = {
        'nbl': "https://www.ladbrokes.com.au/sports/basketball/australia/australian-nbl",
        'nba': "https://www.ladbrokes.com.au/sports/basketball/usa/nba"
    }
    data = requests.get("https://api.ladbrokes.com.au/v2/sport/event-request?category_ids=%5B%223c34d075-dc14-436d-bfc4-9272a49c2b39%22%5D&include_any_team_vs_any_team_events=true",
                        headers={"referer": "https://www.ladbrokes.com.au/", "user-agent": random.choice(user_agents)})
    try:
        dataJson = json.loads(data.text)
    except:
        print("Could not get json from ladbrokes data:")
        print(data)
        return
    events = dataJson['events']
    ladbrokes_games = []
    for eventId in events:
        event = events[eventId]
        full_league_name = events[eventId]['competition']['name']
        league = ('nbl' if full_league_name ==
                  "Australian NBL" else full_league_name.lower()).strip()
        if league in leagues:
            ladbrokes_games.append({
                'name': event['name'],
                'key': eventId,
                'slug': event['slug'],
                'base': league_base_urls[league] if league in league_base_urls.keys() else " "
            })
    for game in schedule:
        for lb_game in ladbrokes_games:
            if game['home'].split(" ")[-1].lower() in lb_game['name'].lower() and game['away'].split(" ")[-1].lower() in lb_game['name'].lower():
                game['urls'].append({
                    'bookie': 'ladbrokes',
                    'urls': [lb_game['base'] + "/" + lb_game['slug'] + "/" + lb_game['key']]
                })
                print("Ladbrokes URL - Home: " + game['home'])


if __name__ == "__main__":
    day = input("Day: ")
    month = input("Month: ")
    year = input("Year: ")
    schedule = get_NBA_schedule(year, month, day)
    add_ladbrokes_urls(schedule, ['nba'])
    print(schedule)
