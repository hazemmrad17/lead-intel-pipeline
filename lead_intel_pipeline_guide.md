# Lead Intel Pipeline — Full Build Guide
**Project:** `lead-intel-pipeline` | Author: Hazem Mrad  
**Goal:** Input a niche + location → output 50 enriched, ready-to-contact business leads as CSV

---

## Project Structure

```
lead-intel-pipeline/
├── main.py                  # Entry point
├── scraper/
│   ├── __init__.py
│   ├── maps_scraper.py      # Step 1: Google Maps scraping
│   └── site_enricher.py     # Step 2: Website enrichment
├── utils/
│   ├── __init__.py
│   ├── email_extractor.py   # Regex email finder
│   └── tech_detector.py     # Tech stack detection
├── output/
│   └── leads.csv            # Final output
├── requirements.txt
└── README.md
```

---

## Agent Prompt Pipeline (Step by Step)

### PROMPT 1 — Scraper Agent
**Purpose:** Get raw business listings from Google Maps

```
You are a web scraping agent. Your job is to extract business listings from Google Maps.

Given:
- niche: "{niche}" (e.g. "digital marketing agency")
- location: "{location}" (e.g. "London, UK")

Your task:
1. Navigate to https://www.google.com/maps/search/{niche}+in+{location}
2. Scroll down to load at least 20 results
3. For each result, extract:
   - business_name (string)
   - address (string)
   - phone (string or null)
   - website_url (string or null)
   - google_rating (float or null)
   - review_count (int or null)

Return a JSON array. Each object must have all 6 fields.
If a field is unavailable, return null — never skip the field.
Do not return duplicates.
```

---

### PROMPT 2 — Enrichment Agent
**Purpose:** Visit each business website and extract useful signals

```
You are a website enrichment agent. You will be given a business website URL.

Your task is to visit the homepage and extract the following:
1. meta_description: The <meta name="description"> content tag value
2. emails: All email addresses found on the page (regex: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})
3. tech_stack: Detect technology signals from the HTML source:
   - Check for "wp-content" → WordPress
   - Check for "Shopify.theme" → Shopify
   - Check for "__next" or "_next/static" → Next.js
   - Check for "cdn.webflow.com" → Webflow
   - Check for "squarespace" → Squarespace
   - If none found → "Unknown"
4. has_chatbot: true if you detect Intercom, Drift, Crisp, Tidio, or similar chat widgets
5. social_links: Extract href values for linkedin.com, twitter.com, instagram.com if present

Return a single flat JSON object with these 5 fields.
If the site fails to load or blocks the request, return {"error": "unreachable"}.
```

---

### PROMPT 3 — Scoring Agent
**Purpose:** Rank leads by how "warm" they are (likely to need your service)

```
You are a lead scoring agent. You will receive an enriched business profile.

Score the lead from 1–10 based on these signals:
- Has a website: +2
- Has an email: +2
- Has a Google rating >= 4.0: +1
- Has 50+ reviews: +1
- Tech stack is WordPress or Webflow (easy to pitch AI add-ons): +1
- Has NO chatbot (opportunity to sell one): +1
- Has LinkedIn presence: +1
- meta_description mentions "growing", "scale", "clients", "leads": +1

Return a JSON object:
{
  "score": <int 1-10>,
  "reason": "<one sentence explaining the top signal>"
}

Be strict. A score of 7+ means strong lead. Below 5 means skip.
```

---

### PROMPT 4 — Outreach Personalization Agent
**Purpose:** Generate a cold outreach message per lead

```
You are a cold outreach copywriter. Write a short, personalized first message to a business owner.

You will receive:
- business_name
- niche
- meta_description
- tech_stack
- has_chatbot (bool)
- score_reason

Rules:
- Maximum 4 sentences
- Do NOT use "I hope this message finds you well"
- Do NOT mention your agency name or pricing
- Reference ONE specific detail from their profile (meta_description or tech_stack)
- End with a single soft question (not "Are you interested?")
- Tone: direct, peer-to-peer, not salesy

Return only the message text, no labels or JSON.
```

---

## Python Implementation

### requirements.txt
```
selenium==4.18.1
beautifulsoup4==4.12.3
requests==2.31.0
pandas==2.2.1
webdriver-manager==4.0.1
python-dotenv==1.0.1
```

### main.py
```python
import pandas as pd
from scraper.maps_scraper import scrape_google_maps
from scraper.site_enricher import enrich_leads
from utils.email_extractor import extract_emails
from utils.tech_detector import detect_tech

def run_pipeline(niche: str, location: str, max_leads: int = 50):
    print(f"[1/3] Scraping Google Maps for '{niche}' in '{location}'...")
    raw_leads = scrape_google_maps(niche, location, max_leads)
    print(f"  → Found {len(raw_leads)} raw listings")

    print("[2/3] Enriching each lead from their website...")
    enriched = enrich_leads(raw_leads)
    print(f"  → Enriched {len(enriched)} leads")

    print("[3/3] Exporting to CSV...")
    df = pd.DataFrame(enriched)
    df.to_csv("output/leads.csv", index=False)
    print(f"  → Saved to output/leads.csv")
    return df

if __name__ == "__main__":
    niche = input("Enter niche (e.g. 'digital marketing agency'): ")
    location = input("Enter location (e.g. 'London'): ")
    df = run_pipeline(niche, location)
    print(df[["business_name", "email", "tech_stack", "score"]].head(10))
```

### scraper/maps_scraper.py
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import urllib.parse

def scrape_google_maps(niche: str, location: str, max_leads: int = 50) -> list[dict]:
    query = urllib.parse.quote(f"{niche} in {location}")
    url = f"https://www.google.com/maps/search/{query}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(url)
    time.sleep(3)

    leads = []
    seen = set()

    # Scroll to load more results
    scrollable = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
    for _ in range(10):
        driver.execute_script("arguments[0].scrollTop += 1000", scrollable)
        time.sleep(1.5)
        if len(leads) >= max_leads:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = soup.select("div.Nv2PK")

    for r in results[:max_leads]:
        try:
            name = r.select_one("div.qBF1Pd").text.strip() if r.select_one("div.qBF1Pd") else None
            if not name or name in seen:
                continue
            seen.add(name)

            rating_el = r.select_one("span.MW4etd")
            reviews_el = r.select_one("span.UY7F9")
            website_el = r.select_one("a[data-value='Website']")
            address_el = r.select_one("div.W4Efsd span:last-child")

            leads.append({
                "business_name": name,
                "address": address_el.text.strip() if address_el else None,
                "phone": None,  # Requires clicking each card — add as enhancement
                "website_url": website_el["href"] if website_el else None,
                "google_rating": float(rating_el.text) if rating_el else None,
                "review_count": int(reviews_el.text.replace("(","").replace(")","").replace(",","")) if reviews_el else None,
            })
        except Exception as e:
            continue

    driver.quit()
    return leads
```

### scraper/site_enricher.py
```python
import requests
from bs4 import BeautifulSoup
from utils.email_extractor import extract_emails
from utils.tech_detector import detect_tech
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def enrich_single(lead: dict) -> dict:
    url = lead.get("website_url")
    if not url:
        lead.update({"email": None, "meta_description": None, "tech_stack": "Unknown", "has_chatbot": False})
        return lead

    try:
        resp = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        html = resp.text.lower()

        meta = soup.find("meta", attrs={"name": "description"})
        emails = extract_emails(resp.text)
        tech = detect_tech(html)
        chatbot = any(x in html for x in ["intercom", "drift.com", "crisp.chat", "tidio", "tawk.to"])

        lead.update({
            "email": emails[0] if emails else None,
            "meta_description": meta["content"] if meta else None,
            "tech_stack": tech,
            "has_chatbot": chatbot,
        })
    except Exception:
        lead.update({"email": None, "meta_description": None, "tech_stack": "Unreachable", "has_chatbot": False})

    return lead

def enrich_leads(leads: list[dict]) -> list[dict]:
    enriched = []
    for i, lead in enumerate(leads):
        print(f"  Enriching {i+1}/{len(leads)}: {lead['business_name']}")
        enriched.append(enrich_single(lead))
        time.sleep(1)  # polite delay
    return enriched
```

### utils/email_extractor.py
```python
import re

def extract_emails(text: str) -> list[str]:
    pattern = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    emails = list(set(re.findall(pattern, text)))
    # Filter out common false positives
    filtered = [e for e in emails if not any(x in e for x in ["example", "sentry", "wix", "schema"])]
    return filtered
```

### utils/tech_detector.py
```python
def detect_tech(html: str) -> str:
    checks = {
        "WordPress": ["wp-content", "wp-includes"],
        "Shopify": ["shopify.theme", "cdn.shopify.com"],
        "Next.js": ["__next", "_next/static"],
        "Webflow": ["cdn.webflow.com", "webflow.com"],
        "Squarespace": ["squarespace.com", "static1.squarespace"],
        "Wix": ["wix.com", "wixstatic.com"],
    }
    for tech, signals in checks.items():
        if any(s in html for s in signals):
            return tech
    return "Unknown"
```

---

## README.md Template

```markdown
# Lead Intel Pipeline

A Python pipeline that takes a niche + location and returns enriched, 
ready-to-contact business leads as a structured CSV.

## What it does
1. Scrapes Google Maps for businesses matching your niche + location
2. Visits each business website to extract emails, tech stack, and meta info
3. Exports a clean CSV ready for outreach

## Output columns
| Column | Description |
|--------|-------------|
| business_name | Company name |
| website_url | Homepage URL |
| email | First email found on site |
| google_rating | Google Maps rating |
| review_count | Number of reviews |
| tech_stack | Detected CMS/framework |
| has_chatbot | Whether a chat widget was found |
| meta_description | Site's SEO description |

## Usage
pip install -r requirements.txt
python main.py

## Demo
[Link to Loom video]

## Built with
Python · Selenium · BeautifulSoup · Pandas
```

---

## Loom Demo Script (90 seconds)

```
0:00 - 0:10  | Show terminal. Type: python main.py
0:10 - 0:20  | Enter niche: "digital marketing agency", location: "Manchester"
0:20 - 0:50  | Let it run. Show scrolling enrichment logs in terminal
0:50 - 1:10  | Open leads.csv in VS Code or Excel — show the columns
1:10 - 1:25  | Zoom into one row: name, email, tech stack, rating
1:25 - 1:30  | Say: "Custom niche, any city, delivered in minutes."
```

---

## Day-by-Day Build Schedule

| Day | Task | Done when... |
|-----|------|-------------|
| Day 1 AM | Set up project structure + maps_scraper.py | Terminal prints 20 raw business names |
| Day 1 PM | Add site_enricher.py + utils | Each lead has email + tech_stack populated |
| Day 2 AM | Wire main.py + test full pipeline end to end | CSV exports with all columns filled |
| Day 2 PM | Clean code, write README, push to GitHub (public) | Repo is live and readable |
| Day 3 | Record Loom demo + start outreach | Video is live, 10 DMs sent |
```
