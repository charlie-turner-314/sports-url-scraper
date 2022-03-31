

from scraping.parser import htmlSoup


def add_betright_urls(schedule, leagues, driver):
    for league in leagues:
        if league == "nba":
            add_nba_games(schedule, driver)
        elif league == "nbl":
            add_nbl_games(schedule, driver)


def add_nba_games(schedule, driver):
    br_base = "https://www.betright.com.au"
    br_url = "https://www.betright.com.au/sports/Basketball/United-States-of-America/NBA/54"
    scrape_basketball_fixtures(br_url, br_base, schedule, driver)


def add_nbl_games(schedule, driver):
    br_base = "https://www.betright.com.au"
    br_url = "https://www.betright.com.au/sports/Basketball/Australia/NBL/110"
    scrape_basketball_fixtures(br_url, br_base, schedule, driver)


def scrape_basketball_fixtures(link, base, schedule, driver):
    driver.get(link)
    page = driver.page_source
    soup = htmlSoup(page)
    matches = soup.find_all('section', class_="push--bottom")
    br_links = [match.a['href'] for match in matches]

    for game in schedule:
        for link in br_links:
            if game["home"].split(" ")[-1].lower() in link.lower() and game["away"].split(" ")[-1].lower() in link.lower():
                game['urls'].append({
                    "bookie": "betright",
                    "urls": [
                        base + link,
                        base + link[:-1] + "G239/",
                        base + link[:-1] + "G52/"
                    ]
                })
                print("Betright URL - Home: " + game['home'])
