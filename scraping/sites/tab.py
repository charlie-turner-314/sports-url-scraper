

from scraping.parser import htmlSoup
from selenium import webdriver


def add_tab_urls(schedule, leagues, driver):
    for league in leagues:
        if league == "nba":
            add_nba_games(schedule, driver)
        elif league == "nbl":
            add_nbl_games(schedule, driver)


def add_nba_games(schedule, driver):
    tab_base = "https://www.tab.com.au"
    tab_url = "https://www.tab.com.au/sports/betting/Basketball/competitions/NBA"
    scrape_fixtures(tab_url, tab_base, schedule, driver, 'nba')


def add_nbl_games(schedule, driver):
    tab_base = "https://www.tab.com.au"
    tab_url = "https://www.tab.com.au/sports/betting/Basketball/competitions/NBL"
    scrape_fixtures(tab_url, tab_base, schedule, driver, 'nbl')


def scrape_fixtures(url, base, schedule, driver: webdriver.Chrome, intent: str):
    driver.get(url)
    page = driver.page_source
    if(intent.upper() not in driver.current_url):
        return
    soup = htmlSoup(page)
    matches = soup.select("a[class='match-name']")
    for game in schedule:
        for el in matches:
            competitors = el['data-id'].split(" v ")
            for competitor in competitors:
                if competitor == "South East Melb":
                    competitor = "SE Melbourne"
                elif competitor == "LA Lakers":
                    competitor = "Lakers"
                elif competitor == "LA Clippers":
                    competitor = "Clippers"
            if((competitors[0].lower() in game['home'].lower() and competitors[1].lower() in game['away'].lower()) or
                    (competitors[0].lower() in game['away'].lower() and competitors[1].lower() in game['home'].lower())):
                game['urls'].append(
                    {"bookie": "tab", "urls": [base + el['href']]})
                print("TAB URL - Home: " + game['home'])
