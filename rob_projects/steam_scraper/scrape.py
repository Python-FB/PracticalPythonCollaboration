import requests
import lxml.html
import json

class SteamScraper():
    def __init__(self, url='https://store.steampowered.com/explore/new/') -> None:
        self.url = url
        self.parsed_results = {}
        self.request_results = self.retrieve()
        self.parsed_results = None

    def __str__(self) -> str:
        return f"I'm a scraper: {self.url}"

    def retrieve(self):
        page_data = requests.get(self.url)
        page = lxml.html.fromstring(page_data.content)
        return page.xpath('//div[@id="tab_newreleases_content"]')[0]

    def parse(self):

        def remove_unicode(title):
            title = title.encode('ascii', 'ignore')
            title = title.decode()
            return title
        try:
            titles = self.request_results.xpath('.//div[@class="tab_item_name"]/text()')
            titles = [remove_unicode(title) for title in titles]
            prices = self.request_results.xpath('.//div[@class="discount_final_price"]/text()')
            tags = []
            for tag in self.request_results.xpath('.//div[@class="tab_item_top_tags"]'):
                tags.append(tag.text_content().split(', '))
            platform_divs = self.request_results.xpath('.//div[@class="tab_item_details"]')
            total_platforms = []
            counter = 0
            for game in platform_divs:
                temp = game.xpath('.//span[contains(@class, "platform_img")]')
                platforms = []
                for platform in temp:
                    holder = platform.get('class').split(' ')[-1]
                    if holder != 'hmd_separator':
                        platforms.append(holder)

                total_platforms.append(platforms)
                counter += 1
            output = []
            headers = ['title', 'price', 'tags', 'platforms']
            counter = 0
            for info in zip(titles, prices, tags, total_platforms):
                resp = {}
                for i in range(0,4):
                    resp[headers[i]] = info[i]
                output.append(resp)
                counter += 1
            self.parsed_results = output
        except Exception as exc:
            raise exc

    def write_results(self, file_name='current_games.json'):
        if self.parsed_results is not None:
            with open(file_name, 'w') as game_file:
                json.dump(self.parsed_results, game_file)

# scraper = SteamScraper()
# print(scraper)
# scraper.retrieve()
# scraper.parse()
# scraper.write_results()