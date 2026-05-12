from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.jobkorea.co.kr/Search/?stext=%EA%B0%9C%EB%B0%9C&tabType=recruit')

    job = page.locator('div.w-full')
    # print(job.count())

    # 이동할 공고 목록 관리
    links = []

    # 공고 크롤링하기
    for i in range(job.count()):
        news = job.nth(i)

        title = news.locator('span.truncate').first.inner_text()
        print(title)

        # link = news.locator('a').first.get_attribute('href')
        # print(f'{i+1}. {title}\n   {link}')
        
    #     links.append({
    #         "title": title,
    #         "href": link
    #     })

    # for news in links:
    #     print("-"*60)
    #     print("제목: ", news["title"])
    #     print("링크: ", news["href"])

    #     # 게시물로 이동
    #     page.goto(news['href'])

    #     # 본문 추출
    #     content = page.locator("#dic_area").inner_text().strip()
    #     print("본문: ", content)