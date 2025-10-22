# Xavier Scott — GitHub Portfolio

Welcome! This repo showcases a few small, real-world projects that reflect my day-to-day strengths: technical support engineering, tooling, and clean customer-facing UX.

**GitHub:** https://github.com/xavierdscott01

## Projects

1. **Helpdesk CLI (Python)** — Swiss-army knife for support engineers: ping, DNS lookup, HTTP check, and port scan.  
   Path: `projects/helpdesk-cli`

2. **Uptime Monitor (Node.js)** — Checks critical endpoints on an interval and records availability.  
   Path: `projects/uptime-monitor`

3. **Support Ticket Dashboard (HTML/JS)** — Lightweight, static dashboard to slice & filter tickets quickly.  
   Path: `projects/support-ticket-dashboard`

> CI is wired for Python & Node samples via GitHub Actions.

---

## Quickstart

### 1) Helpdesk CLI (Python)
```bash
cd projects/helpdesk-cli
python3 -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python helpdesk.py --help
python helpdesk.py ping --host example.com
python helpdesk.py dns --host example.com
python helpdesk.py http --url https://example.com
python helpdesk.py port-scan --host localhost --ports 22,80,443
pytest -q
```

### 2) Uptime Monitor (Node.js)
```bash
cd projects/uptime-monitor
npm install
node index.js                 # one-off run
npm run watch                 # run on an interval
```

### 3) Support Ticket Dashboard (HTML/JS)
```bash
cd projects/support-ticket-dashboard
# Open index.html in your browser (no build step needed).
```

---

## CI (GitHub Actions)
- **Python**: Lints & runs tests for Helpdesk CLI on push/PR.
- **Node**: Installs & lints Uptime Monitor.
See `.github/workflows/`.

---

## Repo setup

```bash
git init
git add .
git commit -m "feat: initial portfolio"
git branch -M main
git remote add origin git@github.com:xavierdscott01/github-portfolio.git
git push -u origin main
```

> Update the remote URL if you choose a different repo name.

## License
MIT — feel free to fork and adapt.