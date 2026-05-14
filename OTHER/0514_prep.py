from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://makemyproject.net/shop/')
    page.wait_for_selector('div.card')
    data = page.locator('div.card')
    # print(data.count())

    # 이동할 공고 목록 관리
    links = []

    # # 공고 크롤링하기
    for i in range(data.count()):
        news = data.nth(i)

        title = news.locator('a').first.inner_text()
        # print(title)
        price = news.locator('strong').inner_text()
        # print(price)

        link = 'https://makemyproject.net/shop/'+news.locator('a').first.get_attribute('href')
        print(f'{i+1}. {title}\n   {price}\n   {link}')
        
        links.append({
            "title": title,
            "price": price,
            "href": link
        })

    for news in links:
        print("-"*60)
        print("상품명: ", news["title"])
        print(news["price"])
        print("링크: ", news["href"])

        # 게시물로 이동
        page.goto(news['href'])

    #     # 스킬 추출
    #     # locator = (
    #     #     page.get_by_text("스킬")
    #     #     .locator("xpath=following-sibling::span[1]")
    #     # )
        
    #     # locator.wait_for()

    #     # content = locator.inner_text().strip() if locator.count() > 0 else None

    #     # print(content)
        
    #     try:
    #         locator = (
    #             page.get_by_text("스킬")
    #             .locator("xpath=following-sibling::span[1]")
    #         )

    #         locator.wait_for(timeout=500)

    #         content = locator.inner_text().strip()
    #         content = content if content else None

    #     except:
    #         content = None

    #     print(content)

    #====================
    # 선택한 곳에 있는 내용 확인
    # cards = page.locator('div.card')

    # first = cards.nth(0)

    # print(first.inner_html())
    # #=====================
    # with page.expect_navigation() as nav:
    # card.click()

    # print(page.url)