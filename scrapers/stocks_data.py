"""
Stock prices and market indices via yfinance — no API key required.
SPOT / long-only assets only. No futures, options, or leveraged ETFs.
"""
import yfinance as yf

WATCHLIST = ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "AMD", "PLTR", "COIN"]
INDICES   = ["^GSPC", "^IXIC", "^DJI", "^VIX"]  # S&P500, Nasdaq, Dow, VIX

# Macro indicators: 10yr yield, USD index, gold, crude oil
MACRO_TICKERS = ["^TNX", "DX-Y.NYB", "GC=F", "CL=F"]
MACRO_NAMES   = {"^TNX": "10Y Treasury Yield", "DX-Y.NYB": "US Dollar Index",
                 "GC=F": "Gold", "CL=F": "Crude Oil"}


def fetch_stock_prices(symbols: list[str] = None) -> list[dict]:
    tickers = symbols or WATCHLIST
    results = []
    try:
        data = yf.download(tickers, period="2d", auto_adjust=True, progress=False)
        closes = data["Close"]
        for sym in tickers:
            try:
                vals = closes[sym].dropna()
                if len(vals) < 2:
                    continue
                prev, curr = float(vals.iloc[-2]), float(vals.iloc[-1])
                change = round((curr - prev) / prev * 100, 2)
                results.append({
                    "symbol":     sym,
                    "price_usd":  round(curr, 2),
                    "change_24h": change,
                })
            except Exception:
                pass
    except Exception as e:
        print(f"  [yfinance stocks] failed: {e}")
    return results

def fetch_market_indices() -> dict:
    result = {"sp500": None, "nasdaq": None, "dow": None, "vix": None}
    try:
        data = yf.download(INDICES, period="2d", auto_adjust=True, progress=False)
        closes = data["Close"]
        mapping = {"^GSPC": "sp500", "^IXIC": "nasdaq", "^DJI": "dow", "^VIX": "vix"}
        for ticker, key in mapping.items():
            try:
                vals = closes[ticker].dropna()
                if len(vals) < 2:
                    continue
                prev, curr = float(vals.iloc[-2]), float(vals.iloc[-1])
                change = round((curr - prev) / prev * 100, 2)
                result[key] = {"value": round(curr, 2), "change_24h": change}
            except Exception:
                pass
    except Exception as e:
        print(f"  [yfinance indices] failed: {e}")
    return result

def market_mood_score(indices: dict) -> float:
    """Derive a simple market mood -1 to +1 from index changes."""
    scores = []
    for key, val in indices.items():
        if not val:
            continue
        chg = val["change_24h"]
        if key == "vix":
            scores.append(max(-1.0, min(1.0, -chg / 5)))
        else:
            scores.append(max(-1.0, min(1.0, chg / 2)))
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 3)


def fetch_macro_indicators() -> list[dict]:
    """Fetch macro indicators: 10yr yield, DXY, gold, crude oil via yfinance."""
    results = []
    try:
        data = yf.download(MACRO_TICKERS, period="2d", auto_adjust=True, progress=False)
        closes = data["Close"]
        for ticker, name in MACRO_NAMES.items():
            try:
                vals = closes[ticker].dropna()
                if len(vals) < 2:
                    continue
                prev, curr = float(vals.iloc[-2]), float(vals.iloc[-1])
                change = round((curr - prev) / prev * 100, 2)
                results.append({
                    "symbol": ticker,
                    "name": name,
                    "value": round(curr, 2),
                    "change_24h": change,
                })
            except Exception:
                pass
    except Exception as e:
        print(f"  [yfinance macro] failed: {e}")
    return results


def fetch_most_active() -> list[dict]:
    """Fetch Yahoo Finance most active stocks (popularity proxy)."""
    try:
        data = yf.download(WATCHLIST, period="2d", auto_adjust=True, progress=False)
        closes = data["Close"]
        volumes = data["Volume"]
        active = []
        for sym in WATCHLIST:
            try:
                v = volumes[sym].dropna()
                c = closes[sym].dropna()
                if len(v) < 1 or len(c) < 2:
                    continue
                vol = int(v.iloc[-1])
                prev, curr = float(c.iloc[-2]), float(c.iloc[-1])
                chg = round((curr - prev) / prev * 100, 2)
                active.append({
                    "symbol": sym,
                    "volume": vol,
                    "price_usd": round(curr, 2),
                    "change_24h": chg,
                })
            except Exception:
                pass
        active.sort(key=lambda x: x["volume"], reverse=True)
        return active[:10]
    except Exception as e:
        print(f"  [yfinance most active] {e}")
        return []
