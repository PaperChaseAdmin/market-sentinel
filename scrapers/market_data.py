"""
Market data via Yahoo Finance — macro indicators + most active stocks.
All data from yfinance (no API key needed).
"""
import yfinance as yf

MACRO_TICKERS = ["^TNX", "DX-Y.NYB", "GC=F", "CL=F"]
MACRO_NAMES = {"^TNX": "10Y Treasury Yield", "DX-Y.NYB": "US Dollar Index",
               "GC=F": "Gold", "CL=F": "Crude Oil"}

WATCHLIST = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "AMD",
             "PLTR", "COIN", "JPM", "BAC", "V", "MA", "SPY", "QQQ"]


def fetch_macro_indicators() -> list[dict]:
    """Fetch macro indicators one by one via yfinance."""
    results = []
    for ticker, name in MACRO_NAMES.items():
        try:
            s = yf.Ticker(ticker)
            hist = s.history(period="5d")
            if hist.empty or len(hist) < 2:
                continue
            closes = hist["Close"]
            prev, curr = float(closes.iloc[-2]), float(closes.iloc[-1])
            change = round((curr - prev) / prev * 100, 2)
            results.append({
                "symbol": ticker, "name": name,
                "value": round(curr, 2), "change_24h": change,
            })
        except Exception as e:
            print(f"  [macro] {ticker}: {e}")
    return results


def fetch_most_active() -> list[dict]:
    """Fetch most active stocks by volume."""
    active = []
    for sym in WATCHLIST:
        try:
            s = yf.Ticker(sym)
            hist = s.history(period="5d")
            if hist.empty or len(hist) < 2:
                continue
            closes = hist["Close"]
            volumes = hist["Volume"]
            vol = int(volumes.iloc[-1])
            prev, curr = float(closes.iloc[-2]), float(closes.iloc[-1])
            chg = round((curr - prev) / prev * 100, 2)
            active.append({
                "symbol": sym, "volume": vol,
                "price_usd": round(curr, 2), "change_24h": chg,
            })
        except Exception:
            pass
    active.sort(key=lambda x: x["volume"], reverse=True)
    return active[:10]
