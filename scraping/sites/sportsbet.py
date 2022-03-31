import requests
from scraping.parser import htmlSoup

from ..headers import headers


def add_sb_urls(schedule, leagues):
    for league in leagues:
        if league == "nba":
            add_nba_games(schedule)
        elif league == "nbl":
            add_nbl_games(schedule)


def add_nba_games(schedule):
    sb_url = "https://www.sportsbet.com.au/betting/basketball-us/nba"
    sb_base = "https://www.sportsbet.com.au"
    link_match = "/betting/basketball-us/nba/"
    scrape_fixture(sb_url, sb_base, link_match, schedule)


def add_nbl_games(schedule):
    sb_url = "https://www.sportsbet.com.au/betting/basketball-aus-other/australian-nbl"
    sb_base = "https://www.sportsbet.com.au"
    link_match = "/betting/basketball-aus-other/australian-nbl/"
    schedule_with_links = scrape_fixture(sb_url, sb_base, link_match, schedule)
    return schedule_with_links


def scrape_fixture(link, sb_base, link_match, schedule):
    data = requests.get(link, headers=headers)
    page = data.text
    soup = htmlSoup(page)
    linksoup = soup.select("a[href*='{}']".format(link_match))
    sb_links = [link['href'] for link in linksoup]
    for game in schedule:
        for link in sb_links:
            if game["home"].lower().split(" ")[-1] in link and game["away"].lower().split(" ")[-1] in link:
                game["urls"].append(
                    {"bookie": "sportsbet", "urls": [sb_base+link]})
                print("Sportsbet URL - Home: " + game['home'])
