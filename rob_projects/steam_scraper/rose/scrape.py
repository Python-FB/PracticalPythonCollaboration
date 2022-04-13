import requests
import lxml.html
from pprint import pprint

html = requests.get('https://editorial.rottentomatoes.com/guide/popular-movies/')
doc = lxml.html.fromstring(html.content)
popular_movies = doc.xpath('//div[@class="row countdown-item"]')

movie_indexes = []
movie_names = []
movie_years = []
movie_scores = []
movie_directors = []

for movie in popular_movies:
    movie_indexes.append(movie.xpath('.//div[@class="countdown-index"]/text()'))
    movie_names.append(movie.xpath('.//h2/a/text()'))
    print(type(movie.xpath('.//h2/a/text()')[0]))
    movie_years.append(movie.xpath('.//span[contains(@class, "subtle start-year")]/text()')[0].strip('()'))
    movie_scores.append(movie.xpath('.//span[contains(@class, "tMeterScore")]/text()'))
    movie_directors.append(movie.xpath('.//div[@class="info director"]/a/text()'))

output = []
for info in zip(movie_indexes, movie_names, movie_years, movie_scores, movie_directors):
    # print(info)
    final_dict = {}
    final_dict['movie_index'] = info[0]
    final_dict['movie_name'] = info[1]
    final_dict['movie_year'] = info[2]
    final_dict['movie_score'] = info[3]
    final_dict['movie_director'] = info[4]
    output.append(final_dict)

pprint(output)
