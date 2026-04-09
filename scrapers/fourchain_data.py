"""
4chan /biz/ board — fully public API, no auth, no rate limits.
Key crypto community with surprisingly strong sentiment signal.
API: https://github.com/4chan/4chan-API
"""
import requests, re
from collections import Counter

HEADERS = {"User-Agent": "MarketSentinel/1.0 (read-only)"}

CRYPTO_KEYWORDS = {
    "BTC":  ["btc", "bitcoin", "sats"],
    "ETH":  ["eth", "ethereum", "ether"],
    "SOL":  ["sol", "solana"],
    "XRP":  ["xrp", "ripple"],
    "DOGE": ["doge", "dogecoin"],
    "BNB":  ["bnb", "binance"],
    "AVAX": ["avax", "avalanche"],
}

BULLISH_WORDS = [
    "moon", "pump", "buy", "bullish", "long", "ath", "breakout",
    "green", "accumulate", "hodl", "hold", "wagmi", "gm", "🚀",
]
BEARISH_WORDS = [
    "dump", "crash", "sell", "bearish", "short", "rug", "dead",
    "rekt", "scam", "ngmi", "bear", "correction", "capitulate",
]


def fetch_biz_sentiment() -> dict:
    print("  [4chan /biz/] fetching catalog…")
    try:
        r = requests.get(
            "https://a.4cdn.org/biz/catalog.json",
            headers=HEADERS, timeout=14,
        )
        r.raise_for_status()
        pages = r.json()

        threads, all_text_parts = [], []
        for page in pages:
            for t in page.get("threads", []):
                text = f"{t.get('sub','') or ''} {t.get('com','') or ''}".lower()
                # strip HTML tags from com field
                text = re.sub(r"<[^>]+>", " ", text)
                threads.append({
                    "text":    text,
                    "replies": t.get("replies", 0),
                })
                all_text_parts.append(text)

        all_text = " ".join(all_text_parts)

        # Crypto mention counts
        mentions = Counter()
        for sym, kws in CRYPTO_KEYWORDS.items():
            for kw in kws:
                mentions[sym] += len(re.findall(r"\b" + re.escape(kw) + r"\b", all_text))

        # Sentiment keyword counts
        bull = sum(all_text.count(w) for w in BULLISH_WORDS)
        bear = sum(all_text.count(w) for w in BEARISH_WORDS)
        total = bull + bear or 1

        active = sum(1 for t in threads if t["replies"] >= 5)
        top = mentions.most_common(3)

        return {
            "thread_count":   len(threads),
            "active_threads": active,
            "mentions":       dict(top),
            "bullish_hits":   bull,
            "bearish_hits":   bear,
            "bullish_pct":    round(bull / total * 100),
            "top_coin":       top[0][0] if top else "BTC",
        }

    except Exception as e:
        print(f"  [4chan /biz/] failed: {e}")
        return {}
