# 툴들 추가
# 1. 네이버 뉴스를 가져온다.
# 2. 구글 검색으로 기업 개요/최근 정보를 조회한다.
# 3. 환율을 조회한다.
# 4. 주가를 조회한다.
from playwright.sync_api import sync_playwright
import requests
import yfinance as yf

def get_news():
    news_text = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://news.naver.com/section/105")

        headlines = page.locator(
            ".section_article.as_headline a.sa_text_title"
        )

        links = []

        for i in range(headlines.count()):
            news = headlines.nth(i)

            links.append({
                "title": news.inner_text().strip(),
                "href": news.get_attribute("href")
            })

        # 상위 5개만
        for news in links[:5]:
            page.goto(news["href"])

            content = page.locator("#dic_area").inner_text().strip()

            news_text += f"""
제목: {news['title']}

본문:
{content}

{'=' * 50}
"""

        browser.close()

    return news_text

def get_company_info(company):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        query = f"{company} 기업 개요 최근 뉴스"

        page.goto(
            f"https://www.google.com/search?q={query}"
        )

        search_results = page.locator("h3")

        result_text = ""

        for i in range(min(5, search_results.count())):
            result_text += (
                search_results.nth(i)
                .inner_text()
                + "\n"
            )

        browser.close()

    return result_text

def get_exchange_rate():
    """open.er-api.com에서 USD 대비 KRW(원화) 환율을 가져오는 함수"""
    url = "https://open.er-api.com/v6/latest/USD"

    try:
        # API 호출 및 JSON 데이터 파싱
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        data = response.json()

        # 데이터가 정상적으로 받아와졌는지 확인 (result가 success인지)
        if data.get("result") == "success":
            # rates 딕셔너리에서 KRW 값 추출
            krw_rate = data["rates"]["KRW"]
            return krw_rate
        else:
            print("API로부터 데이터를 가져오는 데 실패했습니다.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"네트워크 오류가 발생했습니다: {e}")
        return None

def get_stock_price(ticker):
    """ yfinance로 다양한 기업의 주가를 가져온다. 애플('APPL')과 삼성전자('005930.KS')의 주가 데이터를 가져온다."""
    # pip install yfinance
    data = yf.Ticker(ticker).history(period="1d")

    if data.empty:
        return "주가 정보를 찾을 수 없습니다."

    close_price = data["Close"].iloc[-1]

    return f"{ticker} 종가: {close_price:.2f}"

TOOLS = [get_news, get_company_info, get_exchange_rate, get_stock_price]