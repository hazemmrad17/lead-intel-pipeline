"""
Lead Intel Pipeline — Entry Point

Usage:
    python main.py

You will be prompted for:
    - niche    : e.g. "digital marketing agency"
    - location : e.g. "London, UK"

Output:
    output/leads.csv   — enriched, scored, outreach-ready lead list
"""

import os
import sys

# Force UTF-8 on Windows terminals that default to cp1252.
# errors='replace' means Arabic/special chars print as '?' instead of crashing.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd

from scraper.maps_scraper import scrape_google_maps
from scraper.site_enricher import enrich_leads
from utils.scorer import score_lead
from utils.outreach import generate_outreach


OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "leads.csv")


def run_pipeline(niche: str, location: str, max_leads: int = 50) -> pd.DataFrame:
    """
    Execute the full 4-step lead generation pipeline.

    Steps:
        1. Scrape Google Maps → raw listings
        2. Enrich each lead from its website
        3. Score every lead (1–10)
        4. Generate outreach message per lead

    Returns:
        DataFrame of enriched, scored leads.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Step 1: Scrape ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  LEAD INTEL PIPELINE")
    print(f"  Niche: {niche!r}  |  Location: {location!r}")
    print(f"{'='*60}\n")

    print(f"[1/4] Scraping Google Maps...")
    raw_leads = scrape_google_maps(niche, location, max_leads)

    if not raw_leads:
        print("\n[!] No leads scraped. Google Maps may have returned no results,")
        print("    or a CAPTCHA blocked the request. Try a broader niche/location.\n")
        sys.exit(1)

    print(f"  -> Found {len(raw_leads)} raw listings\n")

    # Attach niche to each lead so the outreach generator can reference it
    for lead in raw_leads:
        lead["niche"] = niche

    # ── Step 2: Enrich ────────────────────────────────────────────────────────
    print(f"[2/4] Enriching leads from their websites...")
    enriched = enrich_leads(raw_leads)
    print(f"  -> Enriched {len(enriched)} leads\n")

    # ── Step 3: Score ─────────────────────────────────────────────────────────
    print(f"[3/4] Scoring leads...")
    for lead in enriched:
        result = score_lead(lead)
        lead["score"] = result["score"]
        lead["score_reason"] = result["score_reason"]

    # Sort by score descending so CSV is immediately actionable
    enriched.sort(key=lambda lead: lead.get("score", 0), reverse=True)
    print(f"  -> Scored {len(enriched)} leads\n")

    # ── Step 4: Outreach ──────────────────────────────────────────────────────
    print(f"[4/4] Generating outreach messages...")
    for lead in enriched:
        lead["outreach_message"] = generate_outreach(lead)
    print(f"  -> Generated {len(enriched)} messages\n")

    # ── Export ────────────────────────────────────────────────────────────────
    column_order = [
        "business_name",
        "address",
        "phone",
        "website_url",
        "google_rating",
        "review_count",
        "email",
        "meta_description",
        "tech_stack",
        "has_chatbot",
        "social_links",
        "score",
        "score_reason",
        "outreach_message",
        "niche",
    ]
    df = pd.DataFrame(enriched)

    # Only keep columns that actually exist (guard against partial data)
    final_cols = [c for c in column_order if c in df.columns]
    df = df[final_cols]

    try:
        df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        actual_output = OUTPUT_FILE
    except PermissionError:
        import time
        actual_output = OUTPUT_FILE.replace(".csv", f"_{int(time.time())}.csv")
        df.to_csv(actual_output, index=False, encoding="utf-8-sig")
        print(f"\n[!] Permission denied for {OUTPUT_FILE} (file might be open).")
        print(f"    Saved to alternative file instead: {actual_output}\n")

    print(f"{'='*60}")
    print(f"  [OK] Saved {len(df)} leads -> {actual_output}")
    print(f"{'='*60}\n")

    return df


def _print_summary(df: pd.DataFrame) -> None:
    """Print a quick summary table of the top 10 leads."""
    print("TOP 10 LEADS (by score):\n")
    summary_cols = ["business_name", "email", "tech_stack", "score"]
    available = [c for c in summary_cols if c in df.columns]
    print(df[available].head(10).to_string(index=False))
    print()

    strong = df[df["score"] >= 7] if "score" in df.columns else pd.DataFrame()
    print(f"  [HOT] Strong leads (score >= 7): {len(strong)}")
    print(f"  [EMAIL] Leads with email:        {df['email'].notna().sum()}")
    print(f"  [WEB]   Leads with website:      {df['website_url'].notna().sum()}")
    print()


if __name__ == "__main__":
    print("\n Lead Intel Pipeline\n")
    niche    = input("Enter niche    (e.g. 'digital marketing agency'): ").strip()
    location = input("Enter location (e.g. 'London, UK')              : ").strip()

    if not niche or not location:
        print("Error: niche and location are required.")
        sys.exit(1)

    df = run_pipeline(niche, location)
    _print_summary(df)
