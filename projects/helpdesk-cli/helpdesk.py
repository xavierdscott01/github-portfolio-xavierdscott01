#!/usr/bin/env python3
import argparse, socket, time, subprocess, sys
from urllib.parse import urlparse
import requests
from rich import print
from rich.table import Table

def ping(host: str, count: int = 1, timeout: int = 2):
    # Cross-platform ping (best effort)
    flag = "-n" if sys.platform.startswith("win") else "-c"
    cmd = ["ping", flag, str(count), "-W" if not sys.platform.startswith("win") else "-w", str(timeout), host]
    start = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        rtt = (time.time() - start) * 1000
        ok = proc.returncode == 0
        return {"ok": ok, "ms": round(rtt, 2), "output": proc.stdout or proc.stderr}
    except Exception as e:
        return {"ok": False, "ms": None, "output": str(e)}

def dns_lookup(host: str):
    try:
        infos = socket.getaddrinfo(host, None)
        addrs = sorted({item[4][0] for item in infos})
        return {"ok": True, "addresses": addrs}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def http_check(url: str, timeout: int = 5):
    try:
        r = requests.get(url, timeout=timeout)
        return {"ok": r.ok, "status": r.status_code, "elapsed_ms": int(r.elapsed.total_seconds() * 1000)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def port_scan(host: str, ports: list[int], timeout: float = 0.5):
    result = []
    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((host, p))
            result.append({"port": p, "open": True})
        except Exception:
            result.append({"port": p, "open": False})
        finally:
            s.close()
    return result

def render_table(title, rows, headers):
    table = Table(title=title)
    for h in headers:
        table.add_column(h)
    for r in rows:
        table.add_row(*[str(x) for x in r])
    print(table)

def main():
    parser = argparse.ArgumentParser(description="Helpdesk CLI — quick diagnostics for support engineers")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sp_ping = sub.add_parser("ping", help="Ping a host")
    sp_ping.add_argument("--host", required=True)
    sp_ping.add_argument("--count", type=int, default=1)
    sp_ping.add_argument("--timeout", type=int, default=2)

    sp_dns = sub.add_parser("dns", help="DNS lookup for a host")
    sp_dns.add_argument("--host", required=True)

    sp_http = sub.add_parser("http", help="HTTP GET check")
    sp_http.add_argument("--url", required=True)
    sp_http.add_argument("--timeout", type=int, default=5)

    sp_scan = sub.add_parser("port-scan", help="Scan a comma-separated list of ports")
    sp_scan.add_argument("--host", required=True)
    sp_scan.add_argument("--ports", required=True, help="e.g., 22,80,443")
    args = parser.parse_args()

    if args.cmd == "ping":
        res = ping(args.host, count=args.count, timeout=args.timeout)
        render_table("Ping Result", [[args.host, res["ok"], res["ms"]]], ["Host", "Reachable", "RTT (ms)"])
        if not res["ok"]:
            print(f"[red]{res['output']}[/red]")
    elif args.cmd == "dns":
        res = dns_lookup(args.host)
        rows = [[i+1, a] for i, a in enumerate(res.get("addresses", []))]
        if rows:
            render_table(f"DNS Records for {args.host}", rows, ["#", "Address"])
        else:
            print(f"[red]{res.get('error','No records found')}[/red]")
    elif args.cmd == "http":
        res = http_check(args.url, timeout=args.timeout)
        if res.get("ok"):
            render_table("HTTP Check", [[args.url, res["status"], res["elapsed_ms"]]], ["URL", "Status", "Latency (ms)"])
        else:
            print(f"[red]{res.get('error','Unknown HTTP error')}[/red]")
    elif args.cmd == "port-scan":
        ports = [int(p.strip()) for p in args.ports.split(",") if p.strip()]
        res = port_scan(args.host, ports)
        rows = [[r["port"], "open" if r["open"] else "closed"] for r in res]
        render_table(f"Port Scan — {args.host}", rows, ["Port", "State"])

if __name__ == "__main__":
    main()