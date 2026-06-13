"""
StockTwits — social sentiment for stocks (free, no API key).
Replaces Reddit as the primary social data source.
"""
import requests
from collections import Counter

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
STOCKTWITS_API = "https://api.stocktwits.com/api/2"

# Fallback: scrape StockTwits trending page as alternative
STOCKTWITS_FALLBACK = "https://stocktwits.com/trending.json"


def fetch_trending_symbols(limit: int = 15) -> list[dict]:
    """Get trending symbols on StockTwits right now."""
    # Try API first, then fallback
    for url in [f"{STOCKTWITS_API}/trending/symbols.json", STOCKTWITS_FALLBACK]:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.raise_for_status()
            data = r.json()
            symbols = data.get("symbols", [])
            if symbols:
                return [
                    {"symbol": s["symbol"], "title": s.get("title", s["symbol"]), "watchlist_count": s.get("watchlist_count", 0)}
                    for s in symbols[:limit]
                ]
        except Exception as e:
            print(f"  [StockTwits] {url.split('/')[-1]}: {e}")
            continue
    return []


def fetch_symbol_sentiment(symbol: str) -> dict:
    """Get recent messages for a symbol, return sentiment breakdown."""
    try:
        r = requests.get(
            f"{STOCKTWITS_API}/streams/symbol/{symbol}.json",
            params={"limit": 30},
            headers=HEADERS, timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        messages = data.get("messages", [])
        bullish = sum(1 for m in messages if m.get("entities", {}).get("sentiment", {}).get("basic") == "Bullish")
        bearish = sum(1 for m in messages if m.get("entities", {}).get("sentiment", {}).get("basic") == "Bearish")
        total = len(messages)
        return {
            "symbol": symbol,
            "messages_24h": data.get("symbol", {}).get("watchlist_count", total),
            "recent_messages": total,
            "bullish": bullish,
            "bearish": bearish,
            "sentiment_score": round((bullish - bearish) / max(total, 1), 3),
        }
    except Exception as e:
        print(f"  [StockTwits {symbol}] {e}")
        return {"symbol": symbol, "messages_24h": 0, "recent_messages": 0, "bullish": 0, "bearish": 0, "sentiment_score": 0}


def fetch_stock_sentiment() -> dict:
    """Main entry point: trending symbols + sentiment for top ones."""
    print("  Fetching StockTwits trending...")
    trending = fetch_trending_symbols(15)
    if not trending:
        return {"trending": [], "sentiment": []}

    # Get detailed sentiment for top 10
    top_symbols = [s["symbol"] for s in trending[:10]]
    sentiment_data = [fetch_symbol_sentiment(sym) for sym in top_symbols]

    return {
        "trending": trending,
        "sentiment": sentiment_data,
        "summary": _generate_summary(sentiment_data),
    }


def _generate_summary(sentiment: list[dict]) -> str:
    """Brief summary of overall sentiment."""
    if not sentiment:
        return "No StockTwits data"
    bullish = sum(s["bullish"] for s in sentiment)
    bearish = sum(s["bearish"] for s in sentiment)
    total = sum(s["recent_messages"] for s in sentiment)
    if total == 0:
        return "No recent messages on StockTwits"
    ratio = round((bullish - bearish) / total * 100, 1)
    if ratio > 10:
        return f"Bullish divergence ({ratio}% net bullish) across {len(sentiment)} trending stocks"
    elif ratio < -10:
        return f"Bearish divergence ({abs(ratio)}% net bearish) across {len(sentiment)} trending stocks"
    return f"Mixed sentiment ({ratio}% net) across {len(sentiment)} trending stocks"
