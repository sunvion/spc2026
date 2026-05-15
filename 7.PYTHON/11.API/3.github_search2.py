import requests

url = "https://api.github.com/search/repositories"

# keyword = 'python'
keyword = 'chatbot'

max_pages = 10
per_page = 100

all_repos = []

for page in range(1,max_pages+1):
    params = {
        'q':keyword,
        'per_page':100,
        'page':2
    }

resp = requests.get(url, params)
print('요청 성공여부: ', resp.status_code)

data = resp.json()

# print(data)
if 'items' in data:
    repos = data['items']
    for repo in repos:
        name = repo['name']
        full_name = repo['full_name']
        html_url = repo['html_url']
        desc = repo['description']
        all_repos.append({'name':name, 'full_name':full_name, 'html_url':html_url, 'desc':desc})

print(all_repos)

        # print(f'리포명: {name}, 풀네임: {full_name}, URL: {html_url}, 설명: {desc}')

# 페이징 하는 법 찾아보기