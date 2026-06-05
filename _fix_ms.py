#!/usr/bin/env python3
"""Fix Market Sentinel subtitle"""
with open("/mnt/c/Hermes/market-sentinel/index.html") as f:
    c = f.read()

c = c.replace(
    'Crowd sentiment dashboard \u00b7 <span id="tabIndicator">Crypto</span>',
    '<span class="live"></span> Switch tabs: Crypto prices \u00b7 Stock indices \u00b7 ETF outlooks \u00b7 Next-day predictions')

# Also add .live class styling if not present (used by countdown dot)
if ".live{" not in c:
    c = c.replace(
        "@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}",
        "@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}\n.live{display:inline-block;width:7px;height:7px;background:var(--tv-green);border-radius:50%;animation:blink 2s infinite;margin-right:5px}")

with open("/mnt/c/Hermes/market-sentinel/index.html", "w") as f:
    f.write(c)
print("Market Sentinel subtitle fixed ✅")
