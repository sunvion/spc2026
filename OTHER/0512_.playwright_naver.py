from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 크롬을 실행한다.
    browser = p.chromium.launch(headless=False)
    
    # 빈 페이지를 띄운다.
    page = browser.new_page()

    # 원하는 사이트로 가게 한다.
    page.goto('https://news.naver.com/section/105')

    news_list = page.locator('div.sa_text')
    # print(news_list.count())

    # 뉴스 제목 크롤링하기
    for i in range(news_list.count()):
        news = news_list.nth(i)

        title = news.locator('strong.sa_text_strong').inner_text()
        print(title)

        link = news.locator('a').first.get_attribute('href')
        print(link)

        