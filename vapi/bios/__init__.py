import re

def biose(bio, w):
    locations = [
        'Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa',
        'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda',
        'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan',
        'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
        'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia',
        # … (you can keep the full country list from before if needed)
    ]
    emails = ["@outlook", "@gmail", "@hotmail", "@yahoo"]
    websites = [".to", ".edu", ".lnk", ".com", ".az", ".tr", ".blogspot.", "wix.", ".org", ".net", ".info", ".io", ".me"]

    # Normalize bio to a single string
    if isinstance(bio, list):
        bio_text = " ".join(bio)
    else:
        bio_text = str(bio)
    bio_lower = bio_text.lower()

    if w == "loc":
        for loc in locations:
            if loc.lower() in bio_lower:
                return loc

    elif w == "mail":
        for m in emails:
            if m in bio_text:
                return m

    elif w == "site":
        for s in websites:
            if s in bio_text:
                return s

    elif w == "phone_num":
        # Look for 7+ digit sequences that could be a phone number
        match = re.search(r"\d{7,}", bio_text)
        if match:
            return match.group()
        return "invalid"

    return None
