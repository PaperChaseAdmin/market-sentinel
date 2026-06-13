"""
Market data via Yahoo Finance — macro indicators, most active stocks, market breadth.
All data from yfinance (no API key needed, works on GH Actions when batch downloaded).
"""
import yfinance as yf

# Macro tickers: 10yr yield, US Dollar Index, Gold, Crude Oil
MACRO_TICKERS = ["^TNX", "DX-Y.NYB", "GC=F", "CL=F"]
MACRO_NAMES = {"^TNX": "10Y Treasury Yield", "DX-Y.NYB": "US Dollar Index",
               "GC=F": "Gold", "CL=F": "Crude Oil"}

# Stock watchlist for "most active" / volume ranking
WATCHLIST = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "AMD", "PLTR", "COIN",
             "JPM", "BAC", "WFC", "GS", "V", "MA", "SPY", "QQQ", "IWM", "DIA"]


def fetch_macro_indicators() -> list[dict]:
    """Fetch macro indicators via batch yfinance download."""
    try:
        data = yf.download(MACRO_TICKERS, period="2d", auto_adjust=True, progress=False, group_by="ticker")
        if data.empty:
            return []
        results = []
        for ticker in MACRO_TICKERS:
            try:
                if ticker in data.columns.levels[0]:
                    df = data[ticker]
                else:
                    continue
                vals = df["Close"].dropna()
                if len(vals) < 2:
                    continue
                prev, curr = float(vals.iloc[-2]), float(vals.iloc[-1])
                change = round((curr - prev) / prev * 100, 2)
                results.append({
                    "symbol": ticker,
                    "name": MACRO_NAMES.get(ticker, ticker),
                    "value": round(curr, 2),
                    "change_24h": change,
                })
            except Exception:
                pass
        return results
    except Exception as e:
        print(f"  [yfinance macro] {e}")
        return []


def fetch_most_active() -> list[dict]:
    """Fetch most active stocks by volume via batch yfinance."""
    try:
        data = yf.download(WATCHLIST, period="2d", auto_adjust=True, progress=False, group_by="ticker")
        if data.empty:
            return []
        active = []
        for sym in WATCHLIST:
            try:
                if sym in data.columns.levels[0]:
                    df = data[sym]
                else:
                    continue
                closes = df["Close"].dropna()
                volumes = df["Volume"].dropna()
                if len(closes) < 2 or len(volumes) < 1:
                    continue
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
    except Exception as e:
        print(f"  [yfinance most active] {e}")
        return []
