import requests
from lxml import html
# import lxml as LX

page_data = requests.get('https://store.steampowered.com/explore/new/')
doc = html.fromstring(page_data.content)
# doc = LX.html.fromstring(page_data.content)



print(doc)