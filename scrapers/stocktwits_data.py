"""
StockTwits public API — no authentication required.
Provides trending symbols and user-labelled bullish/bearish sentiment.
API docs: https://api.stocktwits.com/developers/docs
"""
import requests, time

HEADERS = {"User-Agent": "MarketSentinel/1.0 (read-only)"}
BASE    = "https://api.stocktwits.com/api/2"

CRYPTO_SYMBOLS = ["BTC.X", "ETH.X", "SOL.X", "XRP.X", "BNB.X", "DOGE.X"]
STOCK_SYMBOLS  = ["NVDA", "TSLA", "AAPL", "MSFT", "AMD", "META", "AMZN"]


def _get(path: str) -> dict | None:
    try:
        r = requests.get(f"{BASE}{path}", headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  [StockTwits] {path} failed: {e}")
        return None


def fetch_trending() -> list[dict]:
    """All trending symbols on StockTwits right now."""
    data = _get("/trending/symbols.json")
    if not data:
        return []
    return [
        {
            "symbol":          s["symbol"],
            "name":            s.get("title", ""),
            "watchlist_count": s.get("watchlist_count", 0),
        }
        for s in data.get("symbols", [])[:20]
    ]


def fetch_symbol_sentiment(symbol: str) -> dict:
    """Recent messages for a symbol with Bullish/Bearish user labels."""
    data = _get(f"/streams/symbol/{symbol}.json")
    if not data:
        return {}
    messages = data.get("messages", [])
    bullish, bearish = 0, 0
    for m in messages:
        senti = (m.get("entities") or {}).get("sentiment") or {}
        basic = senti.get("basic", "")
        if basic == "Bullish":
            bullish += 1
        elif basic == "Bearish":
            bearish += 1
    labeled = bullish + bearish
    return {
        "symbol":       symbol.replace(".X", ""),
        "messages":     len(messages),
        "bullish":      bullish,
        "bearish":      bearish,
        "bullish_pct":  round(bullish / labeled * 100) if labeled else 50,
        "labeled":      labeled,
    }


def _sentiment_for_symbols(symbols: list[str]) -> list[dict]:
    results = []
    for sym in symbols:
        s = fetch_symbol_sentiment(sym)
        if s and s.get("messages", 0) > 0:
            results.append(s)
        time.sleep(0.25)   # gentle rate limiting
    return results


def fetch_crypto_stocktwits() -> dict:
    print("  [StockTwits] fetching crypto data…")
    trending = fetch_trending()
    # Separate crypto (ends in .X) vs stocks
    crypto_trending = [t for t in trending if t["symbol"].endswith(".X")][:8]
    sentiments = _sentiment_for_symbols(CRYPTO_SYMBOLS[:4])
    return {
        "trending":   crypto_trending,
        "sentiments": sentiments,
    }


def fetch_stock_stocktwits() -> dict:
    print("  [StockTwits] fetching stock data…")
    trending = fetch_trending()
    stock_trending = [t for t in trending if not t["symbol"].endswith(".X")][:8]
    sentiments = _sentiment_for_symbols(STOCK_SYMBOLS[:4])
    return {
        "trending":   stock_trending,
        "sentiments": sentiments,
    }
