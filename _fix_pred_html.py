#!/usr/bin/env python3
"""Replace Market Sentinel predictions section with cleaner visual."""
import re

path = "/mnt/c/Hermes/market-sentinel/index.html"
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Find the Predictions section
start = c.find('<!-- PREDICTIONS -->')
end = c.find('</div>\n\n<script>')

old_section = c[start:end]
print(f"Predictions section: {len(old_section)} bytes")

new_section = '''<!-- PREDICTIONS -->
  <div class="section" id="tab-predictions">
    <div class="loading" id="predictions-loading"><div class="spinner"></div>Analyzing prediction data&hellip;</div>
    <div id="predictions-content" style="display:none">

      <!-- BIG NEXT-DAY CARDS: S&P 500 + NASDAQ -->
      <div class="section-title" style="margin-bottom:8px;font-size:13px">NEXT SESSION FORECAST</div>
      <div id="prediction-big-cards" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:20px">
        <div style="color:var(--tv-text-2);padding:12px 0;text-align:center;grid-column:1/-1">Loading forecast data...</div>
      </div>

      <!-- 10-DAY TRACK RECORD -->
      <div class="section-title" style="margin-bottom:8px;font-size:13px">10-DAY PREDICTION TRACK RECORD</div>
      <div id="prediction-10day" style="margin-bottom:20px">
        <div style="color:var(--tv-text-2);padding:12px 0;text-align:center">Loading track record...</div>
      </div>

      <!-- ACCURACY OVERVIEW -->
      <div class="section-title" style="margin-bottom:8px;font-size:13px">ACCURACY BY INDEX</div>
      <div id="prediction-stats" style="margin-bottom:20px">
        <div style="color:var(--tv-text-2);padding:12px 0;text-align:center">Loading accuracy data...</div>
      </div>

      <div class="disclaimer"><strong>&#9888;&#65039; Not Financial Advice.</strong> Predictions are algorithmic direction signals based on market momentum and index trends. Past performance does not guarantee future results.</div>
    </div>
  </div>'''

c = c[:start] + new_section + c[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Predictions HTML replaced!")
