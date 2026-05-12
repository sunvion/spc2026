from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://books.toscrape.com/')

    books = page.locator('strong.sa_text_strong')
    print(books.count())