# vapi/phonelocfinder.py
"""
Phone location / carrier helper for Vector.
- Uses `phonenumbers` (Google lib) to parse/validate, get country, carrier, and timezones.
- Optionally, if NUMVERIFY_KEY (or other API) is provided, will call that API for extra info.
"""

import os
import re
import requests

import phonenumbers
from phonenumbers import geocoder, carrier, timezone

# Optional external API (NumVerify or similar) - set env var NUMVERIFY_KEY for more details
NUMVERIFY_KEY = os.environ.get("NUMVERIFY_KEY", None)
NUMVERIFY_URL = "http://apilayer.net/api/validate"  # example for numverify (http) - change if needed

def _normalize_phone(candidate: str) -> str:
    """Quick normalize: remove common separators but keep leading + if present."""
    if not candidate:
        return ""
    candidate = candidate.strip()
    # keep plus and digits only
    s = re.sub(r"[^\d+]", "", candidate)
    # if it starts with 00 convert to +
    if s.startswith("00"):
        s = "+" + s[2:]
    return s

def lookup_phone(raw_phone: str, default_region: str = None) -> dict:
    """
    Parse and enrich a phone number string.

    Args:
      raw_phone: raw string scraped from a profile or bio
      default_region: optional two-letter region (e.g., "US", "IN") to help parse local numbers

    Returns:
      dict with keys: normalized, valid, possible, e164, country, country_code,
                      carrier, timezones (list), location (geocoder description),
                      numverify (dict or None), error (if any)
    """
    out = {
        "normalized": None,
        "valid": False,
        "possible": False,
        "e164": None,
        "country": None,
        "country_code": None,
        "carrier": None,
        "timezones": [],
        "location": None,
        "numverify": None,
        "error": None
    }

    if not raw_phone:
        out["error"] = "empty input"
        return out

    s = _normalize_phone(raw_phone)
    out["normalized"] = s

    try:
        # If starts with + parse internationally; otherwise use default_region if provided
        if s.startswith("+"):
            pn = phonenumbers.parse(s, None)
        else:
            # If user gave a numeric local number and default_region is provided, use it.
            if default_region:
                pn = phonenumbers.parse(s, default_region)
            else:
                # fallback: try parsing as international anyway
                pn = phonenumbers.parse(s, None)

        out["possible"] = phonenumbers.is_possible_number(pn)
        out["valid"] = phonenumbers.is_valid_number(pn)
        out["e164"] = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
        out["country_code"] = pn.country_code
        out["country"] = phonenumbers.region_code_for_number(pn)  # e.g. 'US', 'IN'
        # human-readable location (e.g., "New York" or "Delhi")
        try:
            out["location"] = geocoder.description_for_number(pn, "en")
        except Exception:
            out["location"] = None

        # carrier (e.g., "Verizon")
        try:
            out["carrier"] = carrier.name_for_number(pn, "en")
        except Exception:
            out["carrier"] = None

        # timezones list
        try:
            out["timezones"] = timezone.time_zones_for_number(pn)
        except Exception:
            out["timezones"] = []

    except phonenumbers.NumberParseException as e:
        out["error"] = f"parse_error: {e}"
        return out
    except Exception as e:
        out["error"] = f"unexpected_error: {e}"
        return out

    # Optional: enrich with external API (NumVerify) if key provided
    if NUMVERIFY_KEY:
        try:
            params = {"access_key": NUMVERIFY_KEY, "number": out["e164"] or s}
            r = requests.get(NUMVERIFY_URL, params=params, timeout=10)
            if r.status_code == 200:
                out["numverify"] = r.json()
            else:
                out["numverify"] = {"error": f"http_{r.status_code}", "text": r.text}
        except Exception as e:
            out["numverify"] = {"error": f"exception_{e}"}

    return out


# small CLI for quick tests
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        phone = sys.argv[1]
    else:
        phone = input("Phone to lookup: ").strip()
    res = lookup_phone(phone)
    import json
    print(json.dumps(res, indent=2))
