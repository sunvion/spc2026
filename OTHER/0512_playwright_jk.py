from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://www.jobkorea.co.kr/Search/?stext=%EA%B0%9C%EB%B0%9C&tabType=recruit')

    job = page.locator('div.flex.w-full.gap-5.p-7')
    # print(job.count())

    # 이동할 공고 목록 관리
    links = []

    # 공고 크롤링하기
    for i in range(job.count()):
        news = job.nth(i)

        title = news.locator('span.truncate').first.inner_text()
        # print(title)

        link = news.locator('a').first.get_attribute('href')
        print(f'{i+1}. {title}\n   {link}')
        
        links.append({
            "title": title,
            "href": link
        })

    for news in links:
        print("-"*60)
        print("제목: ", news["title"])
        print("링크: ", news["href"])

        # 게시물로 이동
        page.goto(news['href'])

        # 스킬 추출
        # locator = (
        #     page.get_by_text("스킬")
        #     .locator("xpath=following-sibling::span[1]")
        # )
        
        # locator.wait_for()

        # content = locator.inner_text().strip() if locator.count() > 0 else None

        # print(content)
        
        try:
            locator = (
                page.get_by_text("스킬")
                .locator("xpath=following-sibling::span[1]")
            )

            locator.wait_for(timeout=500)

            content = locator.inner_text().strip()
            content = content if content else None

        except:
            content = None

        print(content)