import subprocess, sys, json, os

def test_cli_help():
    proc = subprocess.run([sys.executable, "helpdesk.py", "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "Helpdesk CLI" in proc.stdout