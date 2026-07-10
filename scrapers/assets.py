# Asset keyword lookup tables for mention detection
# SPOT ASSETS ONLY — no leveraged/futures/margin products

CRYPTO_ASSETS = {
    "BTC":  ["bitcoin", "btc", "$btc"],
    "ETH":  ["ethereum", "eth", "$eth", "ether"],
    "SOL":  ["solana", "sol", "$sol"],
    "BNB":  ["binance coin", "bnb", "$bnb"],
    "XRP":  ["xrp", "ripple", "$xrp"],
    "ADA":  ["cardano", "ada", "$ada"],
    "DOGE": ["dogecoin", "doge", "$doge"],
    "AVAX": ["avalanche", "avax", "$avax"],
    "LINK": ["chainlink", "link", "$link"],
    "TON":  ["toncoin", "ton", "$ton"],
    "DOT":  ["polkadot", "dot", "$dot"],
    "MATIC":["polygon", "matic", "$matic"],
    "UNI":  ["uniswap", "uni", "$uni"],
    "LTC":  ["litecoin", "ltc", "$ltc"],
    "ATOM": ["cosmos", "atom", "$atom"],
}

STOCK_ASSETS = {
    "NVDA": ["nvda", "nvidia", "$nvda"],
    "TSLA": ["tsla", "tesla", "$tsla"],
    "AAPL": ["aapl", "apple", "$aapl"],
    "MSFT": ["msft", "microsoft", "$msft"],
    "GOOGL":["googl", "google", "alphabet", "$googl"],
    "AMZN": ["amzn", "amazon", "$amzn"],
    "META": ["meta", "facebook", "$meta"],
    "AMD":  ["amd", "$amd"],
    "PLTR": ["pltr", "palantir", "$pltr"],
    "GME":  ["gme", "gamestop", "$gme"],
    "AMC":  ["amc", "$amc"],
    "MSTR": ["mstr", "microstrategy", "$mstr"],
    "COIN": ["coinbase", "$coin"],
    "SPY":  ["spy", "s&p 500", "s&p500", "sp500"],
    "QQQ":  ["qqq", "nasdaq", "$qqq"],
}

BULLISH_WORDS = [
    # Price action
    "surge", "rally", "soar", "jump", "gain", "rise", "bull", "moon",
    "pump", "breakout", "ath", "record high", "upside", "buy", "long",
    "accumulate", "bottom", "rebound", "recovery", "outperform", "beat",
    "strong", "positive", "growth", "boost", "spike",
    "skyrocket", "explode", "pop", "blast off", "rip", "run", "running",
    "climb", "climbing", "advance", "advancing", "uptick", "upswing",
    "uptrend", "upward", "upwards", "momentum", "bull run", "bullish",
    "all-time high", "fresh high", "new high", "multi-year high",
    "golden cross", "breakout", "break above", "break through",
    "support holding", "hold support", "bounce", "bouncing",

    # Financial performance
    "profit", "revenue", "earnings", "beat estimates", "guidance raise",
    "upgrade", "upgraded", "dividend", "buyback", "share buyback",
    "oversold", "value", "bargain", "undervalued", "cheap",
    "catalyst", "tailwind", "green", "in the green", "profitable",
    "profitability", "margin expansion", "margin improvement",
    "operating leverage", "cost cutting", "efficiency", "synergy",
    "growth story", "growth trajectory", "top line", "bottom line",

    # Sentiment / outlook
    "confident", "confidence", "optimism", "optimistic", "hopeful",
    "promising", "bright", "outlook", "robust", "resilient", "resilience",
    "solid", "healthy", "expansion", "expanding", "accelerate",
    "accelerating", "booming", "boom", "thriving", "flourishing",
    "prosper", "prosperous", "lucrative", "fruitful", "favorable",
    "favourable", "encouraging", "encouraged", "upbeat", "bull case",

    # Competitive position
    "market leader", "sector leader", "best-in-class", "industry leader",
    "market share", "competitive advantage", "moat", "economic moat",
    "pricing power", "first mover", "early mover", "dominant",
    "dominate", "domination", "leadership", "frontrunner",

    # Technical / market structure
    "higher high", "higher low", "resistance broken", "resistance break",
    "volume surge", "accumulation", "bullish divergence",
    "trend reversal", "reversal", "oversold bounce",
    "support bounce", "bull flag", "ascending triangle",
    "cup and handle", "double bottom", "rounding bottom",
    "w bottom", "breakaway gap", "runaway gap",

    # Macro / economic
    "rate cut", "rate drop", "easing", "stimulus", "quantitative easing",
    "liquidity", "influx", "inflow", "capital inflow",
    "foreign investment", "fdi", "infrastructure spending",
    "tax cut", "deregulation", "dovish", "soft landing",
    "goldilocks", "recovery", "rebound", "expansionary",

    # M&A / corporate
    "acquisition", "merger", "takeover", "buyout", "ipo", "listing",
    "spin off", "spin-off", "partnership", "joint venture",
    "strategic alliance", "collaboration", "contract award",
    "government contract", "patent approval", "fda approval",

    # Crypto-specific
    "halving", "deflationary", "staking", "yield", "adoption",
    "institutional", "etf", "etf approval", "layer 2", "scaling",
    "mainnet", "upgrade", "token burn", "supply squeeze", "burn",
    "web3", "defi", "liquidity pool", "yield farming", "airdrop",
    "bull market", "alt season", "flippening", "proof of reserve",
    "transparent", "self custody", "regulation clarity",

    # General positive
    "accelerate", "advance", "appreciate", "boom", "build",
    "climb", "expand", "flourish", "improve", "increase",
    "innovate", "innovation", "launch", "lead", "progress",
    "rally", "recover", "strengthen", "succeed", "success",
    "successful", "win", "winner", "winning", "breakthrough",
    "upgrade", "upside", "upswing", "uptick",
]

BEARISH_WORDS = [
    # Price action
    "crash", "drop", "fall", "dump", "bear", "down", "sell", "decline",
    "collapse", "fear", "panic", "loss", "short", "correction", "plunge",
    "tumble", "sink", "weak", "negative", "risk", "warning", "miss",
    "underperform", "recession", "inflation", "selloff",
    "downtrend", "bearish", "dead cat bounce", "capitulation",
    "bloodbath", "massacre", "rout", "wipeout", "carnage",
    "meltdown", "melt up", "blow off top", "top signal",
    "lower high", "lower low", "support broken", "breakdown",
    "break below", "bear flag", "descending triangle", "death cross",
    "double top", "head and shoulders", "rising wedge",
    "exhaustion gap", "breakaway gap down",
    "plummet", "plunging", "tanking", "tanked", "nosedive",
    "freefall", "slump", "sliding", "slide", "slipping",

    # Financial distress
    "loss", "lost", "deficit", "debt", "default", "bankruptcy",
    "insolvent", "insolvency", "liquidation", "foreclosure",
    "impairment", "writedown", "write-off", "downgrade",
    "cut", "slash", "reduce", "reduction", "layoff", "layoffs",
    "firing", "furlough", "unemployment", "jobless", "job cuts",
    "stagnant", "stagnation", "contraction", "shrinking",
    "dwindling", "fading", "waning", "deteriorate", "deteriorating",
    "eroding", "erosion", "bleeding", "bleed", "burn rate",

    # Fear / uncertainty
    "fear", "panic", "uncertainty", "uncertain", "volatile",
    "volatility", "turmoil", "chaos", "crisis", "crises",
    "bubble", "burst", "implosion", "calamity", "disaster",
    "catastrophic", "catastrophe", "meltdown", "rout", "severe",
    "extreme", "dire", "grave", "grim", "bleak", "gloomy",
    "pessimistic", "pessimism", "doubtful", "dubious",
    "unstable", "shaky", "fragile", "precarious", "vulnerable",
    "risky", "risk-off", "risk aversion", "flight to safety",
    "safe haven", "haven", "hedge",

    # Economic / macro
    "recession", "depression", "stagflation", "inflation",
    "deflation", "hyperinflation", "interest rate hike",
    "rate hike", "rate increase", "tightening", "taper",
    "quantitative tightening", "credit crunch", "liquidity crisis",
    "banking crisis", "debt ceiling", "government shutdown",
    "shutdown", "default risk", "sovereign debt", "contagion",
    "spiral", "downward spiral", "vicious cycle", "doom loop",
    "economic slowdown", "slowdown", "cooling", "cool off",
    "slowing growth", "peak", "peaked", "plateau",

    # Warning / negative sentiment
    "warning", "caution", "cautionary", "careful", "concern",
    "concerned", "concerning", "troubling", "alarming",
    "worrisome", "worry", "worried", "dismal", "dismal",
    "unfavorable", "unfavourable", "adverse", "headwind",
    "overvalued", "expensive", "frothy", "froth",
    "speculation", "speculative", "mania", "irrational exuberance",
    "overbought", "overheated", "overheating",

    # Distribution / technical breakdown
    "distribution", "distribution day", "divergence",
    "bearish divergence", "resistance holding", "rejection",
    "failed breakout", "fakeout", "false breakout", "trap",
    "bull trap", "liquidity grab", "stop hunt", "stop loss",
    "distribution", "churning", "topping", "top pattern",

    # Corporate / sector
    "antitrust", "monopoly", "regulatory", "regulation",
    "compliance", "sanction", "penalty", "fine", "lawsuit",
    "investigation", "probe", "subpoena", "indictment",
    "settlement", "consent decree", "recall", "product recall",
    "supply chain", "disruption", "shortage", "bottleneck",
    "tariff", "trade war", "protectionism", "embargo",

    # Crypto-specific
    "rug pull", "scam", "hack", "exploit", "bridge attack",
    "smart contract bug", "token dump", "supply unlock",
    "validator slashing", "regulation", "ban", "crackdown",
    "sec", "lawsuit", "enforcement", "cease and desist",
    "delist", "delisting", "depeg", "de-pegging", "stablecoin",
    "bank run", "withdrawal halt", "pause withdrawals",
    "insolvent", "frozen assets", "freeze", "blacklist",

    # General negative
    "abandon", "bankrupt", "collapse", "cut", "damage",
    "decay", "decline", "decrease", "deflate", "depreciate",
    "destroy", "deteriorate", "diminish", "dip", "disaster",
    "drop", "dwindle", "fade", "fail", "failure", "falter",
    "fall", "hurt", "impair", "jeopardize", "lose", "loser",
    "plummet", "plunge", "reduce", "shrink", "slash", "slip",
    "slump", "suffer", "suspension", "suspend", "weaken",
    "weakening", "worsen", "worsening", "wrong",
]
