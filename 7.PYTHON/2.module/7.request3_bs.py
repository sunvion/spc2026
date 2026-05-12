import requests
from bs4 import BeautifulSoup

url = 'https://www.example.com'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup)

title = soup.find('title')
print(title)

headings = soup.find_all('h1')
print(headings)

divs = soup.find_all('div')
print(divs)

for elem in divs:
    link = elem.p # 요소 중에 a 태그를 가진 게 있나?
    if link:
        href = link.get('class')
        print('별점: ', href)