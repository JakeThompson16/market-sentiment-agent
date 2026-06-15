
from concurrent.futures import ThreadPoolExecutor
import yfinance as yf
from config import RELEVANT_TICKERS

def fetch_yfinance_stock_sentiment(ticker:str) -> dict:
    """ Source recent articles about a stock """
    ticker = ticker.strip().upper()
    stock = yf.Ticker(ticker)

    new_list = stock.news

    articles = [
        {
            "title": item['content'].get('title'),
            "publisher": item['content'].get('provider', {}),
            "link": item['content']['thumbnail'].get('originalUrl'),
            "summary": item['content'].get('summary'),
            "published_at": item['content'].get('pubDate')
        }
        for item in new_list
    ]

    return {
        "ticker": ticker.upper(),
        "articles": articles
    }

def fetch_yfinance_market_sentiment(tickers:list[str]=RELEVANT_TICKERS) -> dict:
    """ Returns a dict of articles """

    # run requests in parallel with max 5 threads
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_yfinance_stock_sentiment, tickers)

    return {
        res["ticker"]: res["articles"] for res in results
    }

