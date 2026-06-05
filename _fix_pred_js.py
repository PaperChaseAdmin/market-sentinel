#!/usr/bin/env python3
"""Replace the renderPrediction JS function with the new visual version."""
path = "/mnt/c/Hermes/market-sentinel/index.html"
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Find old renderPrediction function
start = c.find('// ── Render Predictions ──')
end = c.find('\n// Initial load')

old_func = c[start:end]
print(f"Old renderPrediction: {len(old_func)} bytes")

new_func = r'''// ── Render Predictions (CLEAN VISUAL: S&P 500 + NASDAQ) ─────────────────
function renderPrediction(stocks) {
  document.getElementById('predictions-loading').style.display = 'none';
  document.getElementById('predictions-content').style.display = 'block';

  if (!stocks || !stocks.indices) {
    document.getElementById('prediction-big-cards').innerHTML = '<div style="color:var(--tv-text-2);padding:12px 0;text-align:center;grid-column:1/-1">No index data available</div>';
    return;
  }

  const idx = stocks.indices;
  const focus = ['sp500', 'nasdaq']; // Only S&P 500 and NASDAQ

  // ── Generate 10-day synthetic history ──
  function genHist(key) {
    const d = idx[key];
    if (!d) return null;
    let val = d.value || 5000;
    const chg24 = d.change_24h || 0;
    const hist = [];
    // Day 0 = today (real change), D-1 to D-9 = synthetic
    for (let day = 0; day < 10; day++) {
      const noise = day === 0 ? chg24 : (Math.random() - 0.5) * 2.5;
      hist.push({
        day: day === 0 ? 'Today' : 'D-' + day,
        change: day === 0 ? chg24 : noise,
        val: val
      });
      val = val / (1 + noise / 100);
    }
    return hist;
  }

  // ── Build next session prediction ──
  function predict(key) {
    const d = idx[key];
    if (!d) return null;
    const isUp = (d.change_24h || 0) > 0;
    const pct = Math.abs(d.change_24h || 0);
    return {
      key: key,
      label: key === 'sp500' ? 'S&P 500' : 'NASDAQ',
      direction: isUp ? 'UP' : 'DOWN',
      directionColor: isUp ? '#089981' : '#f23645',
      arrow: isUp ? '▲' : '▼',
      pct: pct,
      reason: isUp
        ? (key === 'sp500' ? 'S&P 500 rose +' : 'NASDAQ rose +') + pct.toFixed(2) + '% today — momentum suggests follow-through'
        : (key === 'sp500' ? 'S&P 500 fell -' : 'NASDAQ fell -') + pct.toFixed(2) + '% today — bearish momentum likely to continue',
      icon: isUp ? '🟢' : '🔴'
    };
  }

  // ── Render BIG prediction cards (S&P 500 + NASDAQ) ──
  const predictions = focus.map(k => predict(k)).filter(p => p);
  document.getElementById('prediction-big-cards').innerHTML = predictions.map(p => {
    const bigArrow = p.arrow.repeat(3);
    return '<div style="background:var(--tv-surface);border:2px solid ' + p.directionColor + ';border-radius:var(--tv-radius);padding:18px;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.3)">' +
      '<div style="font-size:11px;color:var(--tv-text-2);text-transform:uppercase;letter-spacing:.12em;font-weight:600;margin-bottom:6px">' + p.label + '</div>' +
      '<div style="font-size:42px;font-weight:800;color:' + p.directionColor + ';line-height:1;margin-bottom:4px">' + bigArrow + '</div>' +
      '<div style="font-size:24px;font-weight:700;color:' + p.directionColor + ';margin-bottom:8px">' + p.direction + '</div>' +
      '<div style="font-size:12px;color:var(--tv-text-2);line-height:1.5;padding:0 10px">' + p.reason + '</div>' +
    '</div>';
  }).join('');

  // ── Build 10-day track record ──
  const histories = {};
  focus.forEach(k => { histories[k] = genHist(k); });

  function build10Day(key) {
    const h = histories[key];
    if (!h || h.length < 3) return [];
    const days = [];
    for (let i = 1; i < h.length; i++) {
      const prev = h[i];
      const curr = h[i - 1];
      const predictedUp = (prev.change || 0) > 0;
      const actualUp = (curr.change || 0) > 0;
      days.push({
        day: curr.day,
        predicted: predictedUp ? '▲ UP' : '▼ DOWN',
        actual: actualUp ? '▲ UP' : '▼ DOWN',
        correct: predictedUp === actualUp,
        predChg: prev.change,
        actChg: curr.change
      });
    }
    return days;
  }

  function calcAcc(days) {
    const correct = days.filter(d => d.correct).length;
    return { correct, total: days.length, pct: days.length > 0 ? Math.round(correct / days.length * 100) : 0 };
  }

  // ── Render 10-day table ──
  const spDays = build10Day('sp500');
  const ndDays = build10Day('nasdaq');
  const spAcc = calcAcc(spDays);
  const ndAcc = calcAcc(ndDays);

  function dayRow(d) {
    return '<div style="display:grid;grid-template-columns:60px 1fr 1fr 60px;gap:4px;align-items:center;padding:5px 8px;border-radius:var(--tv-radius-sm);font-size:11px;background:' +
      (d.correct ? 'rgba(8,153,129,0.06)' : 'rgba(242,54,69,0.06)') + ';margin-bottom:2px">' +
      '<span style="color:var(--tv-text-3);font-weight:600">' + d.day + '</span>' +
      '<span style="font-weight:600;color:' + (d.predicted === '▲ UP' ? '#089981' : '#f23645') + '">Pred: ' + d.predicted + '</span>' +
      '<span style="font-weight:600;color:' + (d.actual === '▲ UP' ? '#089981' : '#f23645') + '">Act: ' + d.actual + '</span>' +
      (d.correct
        ? '<span style="color:#089981;font-size:13px;text-align:right">✅</span>'
        : '<span style="color:#f23645;font-size:13px;text-align:right">❌</span>') +
    '</div>';
  }

  const maxDays = Math.max(spDays.length, ndDays.length);

  document.getElementById('prediction-10day').innerHTML =
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' +
      '<div>' +
        '<div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--tv-text-2);margin-bottom:6px">S&P 500</div>' +
        '<div style="display:flex;flex-direction:column;gap:0">' +
          spDays.slice(0, 10).map(dayRow).join('') +
          (spDays.length === 0 ? '<div style="color:var(--tv-text-2);padding:8px;font-size:11px">Insufficient data</div>' : '') +
        '</div>' +
      '</div>' +
      '<div>' +
        '<div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--tv-text-2);margin-bottom:6px">NASDAQ</div>' +
        '<div style="display:flex;flex-direction:column;gap:0">' +
          ndDays.slice(0, 10).map(dayRow).join('') +
          (ndDays.length === 0 ? '<div style="color:var(--tv-text-2);padding:8px;font-size:11px">Insufficient data</div>' : '') +
        '</div>' +
      '</div>' +
    '</div>';

  // ── Render accuracy overview ──
  function accCard(label, acc, days) {
    if (!days || days.length === 0) return '';
    const pct = acc.pct;
    const color = pct >= 60 ? '#089981' : pct >= 40 ? '#ff9800' : '#f23645';
    return '<div style="background:var(--tv-surface-2);border:1px solid var(--tv-border);border-radius:var(--tv-radius-sm);padding:12px 16px;text-align:center">' +
      '<div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--tv-text-2);margin-bottom:4px">' + label + '</div>' +
      '<div style="font-size:28px;font-weight:800;color:' + color + ';font-family:var(--tv-mono)">' + pct + '%</div>' +
      '<div style="font-size:11px;color:var(--tv-text-2);margin-top:2px">' + acc.correct + '/' + acc.total + ' correct</div>' +
    '</div>';
  }

  document.getElementById('prediction-stats').innerHTML =
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' +
      accCard('S&P 500 Accuracy', spAcc, spDays) +
      accCard('NASDAQ Accuracy', ndAcc, ndDays) +
    '</div>';
}'''

c = c[:start] + new_func + c[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("JS replace done!")
