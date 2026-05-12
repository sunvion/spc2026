# 1. books.toscrape.com 에 접속해서 페이지를 받아온다.
# 2. DOM 을 bs4로 구성한다.
# 3. 첫 페이지의 도서명, 평점, 가격을 받아온다.
# 4. CSV파일로 저장한다.

import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup)

title = soup.find_all('h3')
# print(headings)

star = soup.select('p[class^="star-rating"]')
print(star)

# for elem in title:
#     link = elem.a
#     if link:
#         a = link.get('title')
#         print('제목: ', title)