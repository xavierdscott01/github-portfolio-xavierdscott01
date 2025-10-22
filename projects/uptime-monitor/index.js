import fs from 'fs';
import axios from 'axios';

const cfg = JSON.parse(fs.readFileSync(new URL('./config.json', import.meta.url)));
const resultsPath = new URL('./results.json', import.meta.url);

async function check(url) {
  const t0 = Date.now();
  try {
    const res = await axios.get(url, { timeout: cfg.timeoutMs });
    return { url, ok: res.status < 400, status: res.status, ms: Date.now() - t0 };
  } catch (err) {
    return { url, ok: false, status: err.response?.status || 'ERR', ms: Date.now() - t0, error: err.message };
  }
}

async function runOnce() {
  const timestamp = new Date().toISOString();
  const checks = await Promise.all(cfg.targets.map(check));
  const record = { timestamp, checks };
  let history = [];
  try { history = JSON.parse(fs.readFileSync(resultsPath)); } catch {}
  history.push(record);
  fs.writeFileSync(resultsPath, JSON.stringify(history.slice(-cfg.historyLimit), null, 2));
  console.log(`[${timestamp}]`, checks.map(c => `${c.url} ${c.ok?'OK':'DOWN'} (${c.ms}ms)`).join(' | '));
}

if (process.argv.includes('--watch')) {
  await runOnce();
  setInterval(runOnce, cfg.intervalMs);
} else {
  await runOnce();
}