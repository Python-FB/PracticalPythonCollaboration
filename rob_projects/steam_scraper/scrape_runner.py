from scrape import SteamScraper
import json
from datetime import datetime
scraper = SteamScraper()

scraper.retrieve()
scraper.parse()

with open('current_games.json') as previous:
    previous_games = json.loads(previous.read())

for title in previous_games:
    print(title['title'])

for result in scraper.parsed_results:
    print(result['title'])

for prev in previous_games:
    for curr in scraper.current_games:
        pass
        # TODO: include logic that will check for the game in the previous games