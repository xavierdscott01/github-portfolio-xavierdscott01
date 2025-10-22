# Helpdesk CLI (Python)

A compact toolkit for support engineers.

## Commands
- `ping` — host reachability (best-effort cross‑platform wrapper)
- `dns` — DNS A/AAAA resolution
- `http` — HTTP GET status & latency
- `port-scan` — quick TCP port scan

## Run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python helpdesk.py --help
```