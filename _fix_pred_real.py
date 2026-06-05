#!/usr/bin/env python3
"""Rewrite Market Sentinel prediction to use localStorage-persisted real data."""
path = "/mnt/c/Hermes/market-sentinel/index.html"
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Find old renderPrediction function
start = c.find('// ── Render Predictions (CLEAN VISUAL: S&P 500 + NASDAQ) ─────────────────')
end = c.find('\n// Initial load')

old_func = c[start:end]
print(f"Old function: {len(old_func)} bytes")

new_func = r'''// ── Render Predictions (localStorage-persisted: S&P 500 + NASDAQ) ─────
function renderPrediction(stocks) {
  document.getElementById('predictions-loading').style.display = 'none';
  document.getElementById('predictions-content').style.display = 'block';

  if (!stocks || !stocks.indices) {
    document.getElementById('prediction-big-cards').innerHTML = '<div style="color:var(--tv-text-2);padding:12px 0;text-align:center;grid-column:1/-1">No index data available</div>';
    return;
  }

  const idx = stocks.indices;
  const today = new Date().toISOString().split('T')[0];

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
        : (key === 'sp500' ? 'S&P 500 fell -' : 'NASDAQ fell -') + pct.toFixed(2) + '% today — bearish momentum likely to continue'
    };
  }

  // ── Render BIG prediction cards (S&P 500 + NASDAQ) ──
  const focus = ['sp500', 'nasdaq'];
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

  // ── Save today's predictions to localStorage ──
  function saveTodaysPrediction() {
    let history = JSON.parse(localStorage.getItem('sentinel_predictions') || '[]');
    // Clear anything from before today (fresh start)
    history = history.filter(h => h.date >= today);
    
    // Don't save duplicate for today
    if (history.length > 0 && history[0].date === today) return;
    
    const entry = {
      date: today,
      indices: {}
    };
    focus.forEach(k => {
      const p = predict(k);
      if (p) {
        entry.indices[k] = {
          label: p.label,
          predicted: p.direction,    // 'UP' or 'DOWN'
          actual: null,              // unknown until tomorrow
          correct: null
        };
      }
    });
    
    history.unshift(entry);
    // Keep max 15
    history = history.slice(0, 15);
    localStorage.setItem('sentinel_predictions', JSON.stringify(history));
  }
  saveTodaysPrediction();

  // ── Check & update yesterday's predictions ──
  function resolveYesterdaysPredictions() {
    let history = JSON.parse(localStorage.getItem('sentinel_predictions') || '[]');
    let changed = false;
    
    for (let i = 0; i < history.length; i++) {
      const entry = history[i];
      if (entry.date === today) continue; // skip today (not resolved yet)
      
      for (const k of focus) {
        const rec = entry.indices[k];
        if (!rec || rec.correct !== null) continue; // already resolved
        
        // Get today's actual direction for this index
        const d = idx[k];
        if (!d) continue;
        const actualUp = (d.change_24h || 0) > 0;
        rec.actual = actualUp ? 'UP' : 'DOWN';
        rec.correct = rec.predicted === rec.actual;
        changed = true;
      }
    }
    
    if (changed) {
      localStorage.setItem('sentinel_predictions', JSON.stringify(history));
    }
  }
  resolveYesterdaysPredictions();

  // ── Render 10-day track record (from localStorage) ──
  const history = JSON.parse(localStorage.getItem('sentinel_predictions') || '[]');
  const recent = history.slice(0, 10); // max 10 days

  function dayRow(entry, key) {
    const rec = entry.indices[key];
    if (!rec) return '';
    const predictedUp = rec.predicted === 'UP';
    const hasResult = rec.correct !== null;
    const correct = rec.correct;
    
    return '<div style="display:grid;grid-template-columns:60px 1fr 1fr 55px;gap:4px;align-items:center;padding:5px 8px;border-radius:var(--tv-radius-sm);font-size:11px;background:' +
      (hasResult ? (correct ? 'rgba(8,153,129,0.06)' : 'rgba(242,54,69,0.06)') : 'var(--tv-surface-2)') +
      ';margin-bottom:2px;border:1px solid var(--tv-border)">' +
      '<span style="color:var(--tv-text-3);font-weight:600;font-size:10px">' + entry.date.slice(5) + '</span>' +
      '<span style="font-weight:600;color:' + (predictedUp ? '#089981' : '#f23645') + '">Pred: ' + rec.predicted + '</span>' +
      (hasResult
        ? '<span style="font-weight:600;color:' + (correct ? '#089981' : '#f23645') + '">Act: ' + rec.actual + '</span>'
        : '<span style="color:var(--tv-text-3);font-size:10px">⏳ Pending</span>') +
      (hasResult
        ? (correct ? '<span style="color:#089981;font-size:13px;text-align:right">✅</span>' : '<span style="color:#f23645;font-size:13px;text-align:right">❌</span>')
        : '<span style="color:var(--tv-text-3);text-align:right;font-size:11px">⏳</span>') +
    '</div>';
  }

  function calcAcc(entries, key) {
    const resolved = entries.filter(e => e.indices[key] && e.indices[key].correct !== null);
    const correct = resolved.filter(e => e.indices[key].correct).length;
    return { correct, total: resolved.length, pct: resolved.length > 0 ? Math.round(correct / resolved.length * 100) : 0 };
  }

  const spAcc = calcAcc(recent, 'sp500');
  const ndAcc = calcAcc(recent, 'nasdaq');

  const hasSpData = recent.some(e => e.indices.sp500);
  const hasNdData = recent.some(e => e.indices.nasdaq);

  document.getElementById('prediction-10day').innerHTML =
    hasSpData || hasNdData
    ? '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' +
        '<div>' +
          '<div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--tv-text-2);margin-bottom:6px">S&P 500</div>' +
          '<div style="display:flex;flex-direction:column;gap:0">' +
            recent.map(e => dayRow(e, 'sp500')).join('') +
          '</div>' +
        '</div>' +
        '<div>' +
          '<div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--tv-text-2);margin-bottom:6px">NASDAQ</div>' +
          '<div style="display:flex;flex-direction:column;gap:0">' +
            recent.map(e => dayRow(e, 'nasdaq')).join('') +
          '</div>' +
        '</div>' +
      '</div>'
    : '<div style="color:var(--tv-text-2);padding:12px 0;text-align:center;font-size:13px">📡 No prediction history yet — tracking starts today. Check back tomorrow to see accuracy.</div>';

  // ── Render accuracy overview ──
  function accCard(label, acc) {
    if (acc.total === 0) return '';
    const pct = acc.pct;
    const color = pct >= 60 ? '#089981' : pct >= 40 ? '#ff9800' : '#f23645';
    return '<div style="background:var(--tv-surface-2);border:1px solid var(--tv-border);border-radius:var(--tv-radius-sm);padding:12px 16px;text-align:center">' +
      '<div style="font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--tv-text-2);margin-bottom:4px">' + label + '</div>' +
      '<div style="font-size:28px;font-weight:800;color:' + color + ';font-family:var(--tv-mono)">' + pct + '%</div>' +
      '<div style="font-size:11px;color:var(--tv-text-2);margin-top:2px">' + acc.correct + '/' + acc.total + ' correct</div>' +
    '</div>';
  }

  document.getElementById('prediction-stats').innerHTML =
    (spAcc.total > 0 || ndAcc.total > 0)
    ? '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">' +
        accCard('S&P 500 Accuracy', spAcc) +
        accCard('NASDAQ Accuracy', ndAcc) +
      '</div>'
    : '<div style="color:var(--tv-text-2);padding:8px;text-align:center;font-size:12px">Accuracy data will appear after at least one resolved prediction</div>';
}'''

c = c[:start] + new_func + c[end:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Done! Replaced renderPrediction with localStorage version")
