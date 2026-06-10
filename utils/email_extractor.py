import re


# Scan raw text or HTML to find and return unique valid email addresses.
def extract_emails(text: str) -> list[str]:
    """
    Extract unique email addresses from raw HTML/text content.
    Filters out common false positives from CDN paths and schema references.
    """
    pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    found = re.findall(pattern, text)
    seen = set()
    unique = []
    for e in found:
        e_lower = e.lower()
        if e_lower not in seen:
            seen.add(e_lower)
            unique.append(e)

    # Filter common false positives
    false_positive_fragments = [
        "example", "sentry", "wix", "schema", "sampleemail",
        "domain.com", "email.com", "yoursite", "yourdomain",
        "test@", "noreply", "no-reply",
    ]
    filtered = [
        e for e in unique
        if not any(fp in e.lower() for fp in false_positive_fragments)
    ]
    return filtered
