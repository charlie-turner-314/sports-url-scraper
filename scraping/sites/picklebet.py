from time import sleep

from scraping.parser import htmlSoup


def add_picklebet_urls(schedule, leagues, driver):
    for league in leagues:
        if league == "nba":
            add_nba_games(schedule, driver)
        elif league == "nbl":
            add_nbl_games(schedule, driver)


def add_nba_games(schedule, driver):
    pickle_url = "https://picklebet.com/sports/basketball/betting?any=&page=1&tab=next&tour=nba-21-22"
    pickle_base = "https://picklebet.com"
    scrape_fixtures(
        pickle_url, pickle_base, schedule, driver)


def add_nbl_games(schedule, driver):
    pickle_url = "https://picklebet.com/sports/basketball/betting?any=&page=1&tab=next&tour=nbl"
    pickle_base = "https://picklebet.com"
    scrape_fixtures(
        pickle_url, pickle_base, schedule, driver)


def scrape_fixtures(url, base_url, schedule, driver):
    driver.get(url)
    sleep(2)
    page = driver.page_source
    soup = htmlSoup(page)
    matches = soup.select("[class*='MatchRow-module--match--']")
    links = [[
            [competitor.text.split(
                " ")[-1] for competitor in match.select("[class*='Outcome-module--name--']")],
        match.a["href"] if match.a and match.a['href'] else "NO LINK"
    ] for match in matches]
    if len(links) < 1 or len(links[0]) < 2 or len(links[0][0]) < 2:
        return
    for game in schedule:
        for link in links:
            if (link[0][0] in game['home'] and link[0][1] in game['away']) or (link[0][0] in game['away'] and link[0][1] in game['home']):
                game['urls'].append(
                    {"bookie": "picklebet", "urls": [base_url + link[1]]})
                print("Pickle URL - Home: " + game['home'])


if __name__ == "__main__":
    day = input("Day: ")
    month = input("Month: ")
    year = input("Year: ")
