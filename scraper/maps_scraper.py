"""
Google Maps scraper — Step 1 of the Lead Intel Pipeline.

Two-phase approach for reliability:
  Phase 1: Scroll the search results feed to collect individual place page URLs
            (uses the stable `a.hfpxzc` card-link selector)
  Phase 2: Visit each place URL and extract full details from the detail panel
            (uses stable data-item-id selectors, not brittle list-view classes)

Why two-phase?
  Google changes the list-view CSS class names constantly.
  Individual place pages have semantic data-item-id attributes that rarely change.
"""

import re
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# ── Driver setup ──────────────────────────────────────────────────────────────

# Initialize a headless Chrome driver with anti-bot options.
def _build_driver() -> webdriver.Chrome:
    """Initialise a headless Chrome driver with anti-bot flags."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


# ── Public API ────────────────────────────────────────────────────────────────

# Search Google Maps for businesses matching a niche and location, and extract raw details.
def scrape_google_maps(niche: str, location: str, max_leads: int = 50) -> list[dict]:
    """
    Scrape Google Maps for businesses matching `niche` in `location`.

    Returns:
        List of dicts with keys:
            business_name, address, phone, website_url,
            google_rating, review_count
    """
    query = urllib.parse.quote_plus(f"{niche} in {location}")
    search_url = f"https://www.google.com/maps/search/{query}"

    driver = _build_driver()
    leads: list[dict] = []

    try:
        # ── Phase 1: collect place page URLs ──────────────────────────────
        print(f"  -> Collecting place URLs from search results...")
        place_urls = _collect_place_urls(driver, search_url, max_leads)

        if not place_urls:
            print("  [!] No place URLs found - Google may be showing a CAPTCHA.")
            return leads

        print(f"  -> Found {len(place_urls)} places. Fetching details...\n")

        # ── Phase 2: visit each place page ────────────────────────────────
        seen: set[str] = set()
        for i, url in enumerate(place_urls, 1):
            print(f"    [{i}/{len(place_urls)}] Scraping place page...")
            lead = _scrape_place_page(driver, url)
            if lead and lead["business_name"] and lead["business_name"] not in seen:
                seen.add(lead["business_name"])
                leads.append(lead)
            time.sleep(0.8)   # polite delay between place pages

    finally:
        driver.quit()

    return leads


# ── Phase 1: collect URLs ─────────────────────────────────────────────────────

# Scroll the Google Maps search results feed to collect individual place page URLs.
def _collect_place_urls(driver: webdriver.Chrome, search_url: str, max_count: int) -> list[str]:
    """
    Scroll the Maps search results feed and collect individual place page URLs.
    Uses `a.hfpxzc` — the stable card-link selector in Google Maps.
    """
    driver.get(search_url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
        )
    except Exception:
        return []

    urls: list[str] = []
    seen_urls: set[str] = set()
    scrollable = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")

    for _ in range(20):  # up to 20 scroll attempts
        driver.execute_script("arguments[0].scrollTop += 1200", scrollable)
        time.sleep(1.8)

        # Collect hrefs from card links
        for card in driver.find_elements(By.CSS_SELECTOR, "a.hfpxzc"):
            href = card.get_attribute("href")
            if href and "/maps/place/" in href and href not in seen_urls:
                seen_urls.add(href)
                urls.append(href)

        if len(urls) >= max_count:
            break

        # End-of-results sentinel
        end_els = driver.find_elements(
            By.XPATH, "//*[contains(text(), \"You've reached the end\")]"
        )
        if end_els:
            break

    return urls[:max_count]


# ── Phase 2: scrape individual place page ────────────────────────────────────

# Visit an individual Google Maps place page and extract structured details from its UI.
def _scrape_place_page(driver: webdriver.Chrome, url: str) -> dict | None:
    """
    Visit a Google Maps place URL and extract structured business data.

    Relies on semantic data-item-id attributes which are much more stable
    than the list-view CSS classes that change with every Maps UI update.
    """
    try:
        driver.get(url)

        # Wait for the place heading to appear
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        time.sleep(1.5)  # let secondary content (website btn etc.) render

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ── Name ──────────────────────────────────────────────────────────
        name_el = soup.select_one("h1.DUwDvf") or soup.select_one("h1")
        name = name_el.get_text(strip=True) if name_el else None
        if not name:
            return None

        # ── Website ───────────────────────────────────────────────────────
        # data-item-id="authority" is on the website anchor in the detail panel
        website_el = soup.select_one("a[data-item-id='authority']")
        website_url = website_el.get("href") if website_el else None

        # ── Rating ────────────────────────────────────────────────────────
        rating = None
        # aria-hidden span inside the F7nice rating block
        rating_el = soup.select_one("div.F7nice span[aria-hidden='true']")
        if rating_el:
            try:
                rating = float(rating_el.get_text(strip=True).replace(",", "."))
            except ValueError:
                pass

        # ── Review count ──────────────────────────────────────────────────
        review_count = None
        reviews_el = soup.find(
            "span", attrs={"aria-label": re.compile(r"\d+.*avis|review", re.I)}
        )
        if reviews_el:
            m = re.search(r"[\d\s,]+", reviews_el.get("aria-label", ""))
            if m:
                try:
                    review_count = int(m.group().replace(",", "").replace(" ", ""))
                except ValueError:
                    pass

        # ── Phone ─────────────────────────────────────────────────────────
        phone = None
        phone_btn = soup.select_one("button[data-item-id*='phone:tel']")
        if phone_btn:
            phone_div = phone_btn.select_one("div.rogA2c") or phone_btn
            phone = phone_div.get_text(strip=True) or None

        # ── Address ───────────────────────────────────────────────────────
        address = None
        addr_btn = soup.select_one("button[data-item-id='address']")
        if addr_btn:
            address = addr_btn.get_text(strip=True) or None

        return {
            "business_name": name,
            "address":       address,
            "phone":         phone,
            "website_url":   website_url,
            "google_rating": rating,
            "review_count":  review_count,
        }

    except Exception:
        return None
