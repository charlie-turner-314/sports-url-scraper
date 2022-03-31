from datetime import datetime, timedelta
from os import environ

from dotenv import load_dotenv

from database.connection import connect_mongo
from database.queries import insert_games
from schedules.basketball.nba import get_NBA_schedule
from schedules.basketball.nbl import get_NBL_schedule
from scraping.sites.betright import add_betright_urls
from scraping.sites.ladbrokes import add_ladbrokes_urls
from scraping.sites.picklebet import add_picklebet_urls
from scraping.sites.pointsbet import add_pointsbet_urls
from scraping.sites.sportsbet import add_sb_urls
from scraping.sites.tab import add_tab_urls
from scraping.webdriver import selenium_driver_config

# Any environment variables
load_dotenv()


def add_urls(schedule, leagues, driver):
    add_picklebet_urls(schedule, leagues, driver)
    add_tab_urls(schedule, leagues, driver)
    add_sb_urls(schedule, leagues)
    add_betright_urls(schedule, leagues, driver)
    add_ladbrokes_urls(schedule, leagues)
    add_pointsbet_urls(schedule, leagues)


def main():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    all_games = []
    # Get Schedules
    try:
        all_games.extend(get_NBA_schedule(today.year, today.month, today.day))
        all_games.extend(get_NBA_schedule(today.year, yesterday.month, yesterday.day))
        all_games.extend(get_NBA_schedule(tomorrow.year, tomorrow.month, tomorrow.day))
    except:
        print("Could not add all nba games")
    try:
        all_games.extend(get_NBL_schedule(today.year, today.month, today.day))
        all_games.extend(get_NBL_schedule(tomorrow.year, tomorrow.month, tomorrow.day))
    except:
        print("Could not add all NBL games")
    # Populate with urls
    driver = selenium_driver_config()
    add_urls(all_games, ['nbl', 'nba'], driver)
    driver.close()
    mongoDB = connect_mongo(
        environ.get("DB_URI"))
    insert_games(all_games, mongoDB)
    return print("Done")


if __name__ == "__main__":
    main()
