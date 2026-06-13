"""
Google Trends — search interest for stock tickers (free, no API key).
Uses pytrends library to fetch real-time search interest data.
"""
from pytrends.request import TrendReq

# Stock tickers to track for search interest
TRACK_TICKERS = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META",
                 "AMD", "PLTR", "COIN", "JPM", "BAC", "V", "SPY", "QQQ",
                 "BTC", "ETH", "XRP", "SOL", "DOGE"]

# Crypto keywords for broader search interest
CRYPTO_KEYWORDS = ["Bitcoin", "Ethereum", "Solana", "crypto"]


def fetch_stock_trends() -> list[dict]:
    """Fetch Google Trends interest scores for tracked stock tickers."""
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=10)
        # Process in batches of 5 (Google Trends limit)
        all_results = []
        for i in range(0, len(TRACK_TICKERS), 5):
            batch = TRACK_TICKERS[i:i+5]
            try:
                pytrends.build_payload(kw_list=batch, cat=0, timeframe='now 1-d', geo='US')
                data = pytrends.interest_over_time()
                if not data.empty:
                    latest = data.iloc[-1]
                    for ticker in batch:
                        if ticker in latest and not latest.get('isPartial', False):
                            all_results.append({
                                "symbol": ticker,
                                "interest_score": int(latest[ticker]),
                                "timestamp": str(data.index[-1]),
                            })
            except Exception as e:
                print(f"  [pytrends] batch {batch}: {e}")
        all_results.sort(key=lambda x: x["interest_score"], reverse=True)
        return all_results
    except Exception as e:
        print(f"  [pytrends] {e}")
        return []


def fetch_crypto_trends() -> list[dict]:
    """Fetch Google Trends interest for crypto keywords."""
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=10)
        pytrends.build_payload(kw_list=CRYPTO_KEYWORDS, cat=0, timeframe='now 1-d', geo='')
        data = pytrends.interest_over_time()
        if data.empty:
            return []
        latest = data.iloc[-1]
        return [
            {"keyword": kw, "interest_score": int(latest[kw])}
            for kw in CRYPTO_KEYWORDS if kw in latest
        ]
    except Exception as e:
        print(f"  [pytrends crypto] {e}")
        return []


def fetch_trending_queries(symbol: str = "NVDA") -> list[dict]:
    """Get related trending queries for a symbol (what people also search)."""
    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=10)
        pytrends.build_payload(kw_list=[symbol], cat=0, timeframe='now 7-d', geo='US')
        related = pytrends.related_queries()
        result = {}
        if related and symbol in related:
            r = related[symbol]
            if r.get('rising') is not None:
                result['rising'] = r['rising'].head(5).to_dict('records')
            if r.get('top') is not None:
                result['top'] = r['top'].head(5).to_dict('records')
        return [{"symbol": symbol, "related": result}] if result else []
    except Exception as e:
        print(f"  [pytrends related] {e}")
        return []
