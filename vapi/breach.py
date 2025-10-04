# vapi/breach.py
import os
import json
import requests
import time
from bs4 import BeautifulSoup
from prettytable import PrettyTable

from vapi.poor import color
from vapi.error import exp

# paths to save (unchanged)
SAVEN = "./vapi/save/nick.txt"
SAVEE = "./vapi/save/email.txt"

# Try to load API key from environment first, then config.json (if present)
def _load_leakcheck_key():
    key = os.environ.get("LEAKCHECK_KEY")
    if key:
        return key

    cfg_path = os.path.join(os.getcwd(), "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
                return cfg.get("leakcheck_key") or cfg.get("hibp_key") or None
        except Exception:
            return None
    return None

LEAKCHECK_KEY = _load_leakcheck_key()

def _build_url(query):
    """
    Build the leakcheck API URL.
    If a key is available, use it; otherwise try public endpoint (may fail).
    """
    # Prefer environment/config key — do not hardcode keys in repo
    if LEAKCHECK_KEY:
        return f"https://leakcheck.net/api/public?key={LEAKCHECK_KEY}&check={query}"
    # If no key, fall back to the same endpoint without a key (may be rate-limited or blocked)
    return f"https://leakcheck.net/api/public?check={query}"

def breach_nickname(nickname):
    """Return a list of leak source names for the nickname or 'false' on failure."""
    try:
        url = _build_url(nickname)
        resp = requests.get(url, timeout=12)
        resp.raise_for_status()
        data_nc = resp.json()
    except Exception as e:
        # Return False (string) to preserve earlier behavior but log the error
        print(f"[!] breach_nickname error: {e}")
        return "false"

    leaks = []
    if data_nc.get('success') is True:
        sources = data_nc.get('sources', [])
        for s in sources:
            leaks.append(s.get("name", "unknown"))
    else:
        return "false"

    return leaks

def _print_table(rows):
    t = PrettyTable()
    t.field_names = ["Breach Name", "Date", "Include"]
    for r in rows:
        t.add_row(r)
    print(t)

def run(email, nick):
    """
    Run breach checks for provided email and/or nick.
    Prints table of findings and returns a dict with structured results.
    """
    time.sleep(1)
    print(f"""
{color.CGREEN}[//]{color.CWHITE} This action will search the following informations below in {color.CWHITE2}breached databases{color.CWHITE}...
{color.CGREEN}[{time.strftime("%X")}] {color.CWHITE}Email Adress : {color.CWHITE}[{color.CWHITE2}{email}{color.CWHITE}]
{color.CGREEN}[{time.strftime("%X")}] {color.CWHITE}Username     : {color.CWHITE}[{color.CWHITE2}{nick}{color.CWHITE}]
""")

    results = {
        "email": {"found": False, "count": 0, "passwords": 0, "sources": []},
        "nick": {"found": False, "count": 0, "passwords": 0, "sources": []},
        "errors": []
    }

    try:
        rows = []

        # EMAIL
        if email:
            try:
                url_e = _build_url(email)
                r = requests.get(url_e, timeout=12)
                r.raise_for_status()
                data_em = r.json()
            except Exception as e:
                err = f"Email lookup failed: {e}"
                print(f"[!] {err}")
                results["errors"].append(err)
                data_em = {}

            if data_em.get('success') is True:
                found = data_em.get('found', 0)
                passwords = data_em.get('passwords', 0)
                sources = data_em.get('sources', [])
                results["email"].update({
                    "found": True,
                    "count": found,
                    "passwords": passwords,
                    "sources": sources
                })
                print(f"{color.CBLUE}[*]{color.CWHITE} Found {color.CWHITE2}{found}{color.CWHITE} data leaks for {color.CWHITE2}{email}{color.CWHITE} with {color.CWHITE2}{passwords}{color.CWHITE} passwords!")
                for s in sources:
                    rows.append([s.get("name", "unknown"), s.get("date", "N/A"), email])
            else:
                print(f"[{color.CRED}!{color.CWHITE}] Not found any {color.CWHITE2}leak{color.CWHITE} for [{color.CWHITE2}{email}{color.CWHITE}]!")

        # NICKNAME
        if nick:
            try:
                url_n = _build_url(nick)
                r2 = requests.get(url_n, timeout=12)
                r2.raise_for_status()
                data_nc = r2.json()
            except Exception as e:
                err = f"Nickname lookup failed: {e}"
                print(f"[!] {err}")
                results["errors"].append(err)
                data_nc = {}

            if data_nc.get('success') is True:
                found = data_nc.get('found', 0)
                passwords = data_nc.get('passwords', 0)
                sources = data_nc.get('sources', [])
                results["nick"].update({
                    "found": True,
                    "count": found,
                    "passwords": passwords,
                    "sources": sources
                })
                print(f"{color.CBLUE}[*]{color.CWHITE} Found {color.CWHITE2}{found}{color.CWHITE} data leaks for {color.CWHITE2}{nick}{color.CWHITE} with {color.CWHITE2}{passwords}{color.CWHITE} passwords!")
                for s in sources:
                    rows.append([s.get("name", "unknown"), s.get("date", "N/A"), nick])
            else:
                print(f"[{color.CRED}!{color.CWHITE}] Not found any {color.CWHITE2}leak{color.CWHITE} for [{color.CWHITE2}{nick}{color.CWHITE}]!")

        # Print table if rows exist
        if rows:
            _print_table(rows)

    except Exception as e:
        # Catch-all to avoid silent failures; log error
        err = f"Unexpected error in breach.run: {e}"
        print(f"[!] {err}")
        results["errors"].append(err)

    return results
