# Detect the CMS or web framework used by a website from its HTML source.
def detect_tech(html: str) -> str:
    """
    Detect CMS / framework from HTML source signals.
    Returns the first match found, or 'Unknown'.
    """
    checks = {
        "WordPress":   ["wp-content", "wp-includes", "wp-json"],
        "Shopify":     ["shopify.theme", "cdn.shopify.com", "shopify.com/s/files"],
        "Next.js":     ["__next", "_next/static", "__NEXT_DATA__"],
        "Webflow":     ["cdn.webflow.com", "webflow.com/css"],
        "Squarespace": ["squarespace.com", "static1.squarespace", "squarespace-cdn"],
        "Wix":         ["wix.com", "wixstatic.com", "wix-code"],
        "Framer":      ["framer.com", "framerusercontent.com"],
        "Ghost":       ["ghost.org", "ghost/content"],
    }
    html_lower = html.lower()
    for tech, signals in checks.items():
        if any(s in html_lower for s in signals):
            return tech
    return "Unknown"
