import requests
# from lxml import html as HTML
# from lxml.etree import HTMLParser
import lxml.html
# import lxml
import json

page_data = requests.get('https://store.steampowered.com/explore/new/')
# page = HTML.fromstring(page_data.content, parser=HTMLParser(encoding='utf8'))
page = lxml.html.fromstring(page_data.content)
# page = lxml.etree._Element(page)
new_games = page.xpath('//div[@id="tab_newreleases_content"]')[0]

titles = new_games.xpath('.//div[@class="tab_item_name"]/text()')

def remove_unicode(title):
    title = title.encode('ascii', 'ignore')
    title = title.decode()
    return title

titles = [remove_unicode(title) for title in titles]

prices = new_games.xpath('.//div[@class="discount_final_price"]/text()')

tags = []
for tag in new_games.xpath('.//div[@class="tab_item_top_tags"]'):
    tags.append(tag.text_content())
tags = [tag.split(', ') for tag in tags]

platform_divs = new_games.xpath('.//div[@class="tab_item_details"]')
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

output = {}
headers = ['title', 'price', 'tags', 'platforms']
counter = 0
for info in zip(titles, prices, tags, total_platforms):
    resp = {}
    for i in range(1,4):
        resp[headers[i]] = info[i]
    output[info[0]] = resp
    counter += 1

with open('current_games.json', 'w') as game_file:
    json.dump(output, game_file)
