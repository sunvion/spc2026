from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://news.naver.com/section/105')

    news_list = page.locator('div.sa_text')
    # print(news_list.count())

    # 이동할 뉴스 목록 관리
    links = []

    # 뉴스 제목 크롤링하기
    for i in range(news_list.count()):
        news = news_list.nth(i)

        title = news.locator('strong.sa_text_strong').inner_text()
        # print(title)

        link = news.locator('a').first.get_attribute('href')
        print(f'{i+1}. {title}\n   {link}')