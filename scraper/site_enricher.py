"""
Site Enricher — Step 2 of the Lead Intel Pipeline.

Visits each business website and extracts:
  - email          : first email found on the page
  - meta_description: <meta name="description"> content
  - tech_stack     : CMS/framework detected from HTML signals
  - has_chatbot    : whether a live chat widget is present
  - social_links   : LinkedIn, Twitter/X, Instagram URLs
"""

import time

import requests
from bs4 import BeautifulSoup

from utils.email_extractor import extract_emails
from utils.tech_detector import detect_tech


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}

CHATBOT_SIGNALS = [
    "intercom", "drift.com", "crisp.chat", "tidio",
    "tawk.to", "freshchat", "hubspot-messages",
    "livechat", "zendesk.com/embeddable",
]

SOCIAL_DOMAINS = ["linkedin.com", "twitter.com", "x.com", "instagram.com", "facebook.com"]


# Visit the website of a single business lead and extract contact and technology details.
def enrich_single(lead: dict) -> dict:
    """
    Enrich one lead by fetching its website.

    Modifies the `lead` dict in-place and also returns it.
    """
    url = lead.get("website_url")
    if not url:
        lead.update({
            "email": None,
            "meta_description": None,
            "tech_stack": "Unknown",
            "has_chatbot": False,
            "social_links": None,
        })
        return lead

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        resp.raise_for_status()

        html_raw = resp.text
        html_lower = html_raw.lower()
        soup = BeautifulSoup(html_raw, "html.parser")

        # ── Email ──────────────────────────────────────────────────────────
        emails = extract_emails(html_raw)

        # ── Meta description ───────────────────────────────────────────────
        meta_tag = soup.find("meta", attrs={"name": "description"})
        meta_desc = meta_tag.get("content", "").strip() if meta_tag else None

        # ── Tech stack ─────────────────────────────────────────────────────
        tech = detect_tech(html_lower)

        # ── Chatbot ────────────────────────────────────────────────────────
        has_chatbot = any(signal in html_lower for signal in CHATBOT_SIGNALS)

        # ── Social links ───────────────────────────────────────────────────
        social_links = _extract_social_links(soup)

        lead.update({
            "email":            emails[0] if emails else None,
            "meta_description": meta_desc,
            "tech_stack":       tech,
            "has_chatbot":      has_chatbot,
            "social_links":     ", ".join(social_links) if social_links else None,
        })

    except requests.exceptions.Timeout:
        _mark_unreachable(lead, "timeout")
    except requests.exceptions.SSLError:
        _mark_unreachable(lead, "ssl_error")
    except requests.exceptions.ConnectionError:
        _mark_unreachable(lead, "connection_error")
    except Exception:
        _mark_unreachable(lead, "error")

    return lead


# Iterate through a list of leads and enrich each one from their website, printing progress.
def enrich_leads(leads: list[dict]) -> list[dict]:
    """
    Enrich all leads, printing progress.
    Applies a 1-second polite delay between requests.
    """
    enriched = []
    total = len(leads)
    for i, lead in enumerate(leads, start=1):
        name = lead.get("business_name", "Unknown")
        print(f"  [{i}/{total}] Enriching: {name}")
        enriched.append(enrich_single(lead))
        time.sleep(1)
    return enriched


# ── Helpers ───────────────────────────────────────────────────────────────────

# Extract social media profile links (LinkedIn, Twitter, Facebook, etc.) from the website HTML.
def _extract_social_links(soup: BeautifulSoup) -> list[str]:
    """Return a list of social profile URLs found in anchor tags."""
    links = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if any(domain in href for domain in SOCIAL_DOMAINS):
            if href not in seen:
                seen.add(href)
                links.append(href)
    return links


# Populate empty fields for unreachable websites with fallback values and indicate failure.
def _mark_unreachable(lead: dict, reason: str = "error") -> None:
    lead.update({
        "email":            None,
        "meta_description": None,
        "tech_stack":       "Unreachable",
        "has_chatbot":      False,
        "social_links":     None,
    })
