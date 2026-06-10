"""
Lead Scorer — Rule-based implementation of the Scoring Agent (Prompt 3).

Scoring rubric (max 10 points):
  +2  Has a website
  +2  Has an email
  +1  Google rating >= 4.0
  +1  Has 50+ reviews
  +1  Tech stack is WordPress or Webflow (easy to pitch AI add-ons)
  +1  Has NO chatbot (opportunity to sell one)
  +1  Has LinkedIn presence
  +1  meta_description mentions growth/scale keywords
"""


GROWTH_KEYWORDS = {"growing", "scale", "clients", "leads", "growth", "expand", "revenue"}
PITCHABLE_STACKS = {"WordPress", "Webflow"}


# Score a business lead out of 10 based on predefined quality signals.
def score_lead(lead: dict) -> dict:
    """
    Score a single enriched lead.

    Returns:
        dict with keys:
            score (int 1–10)
            score_reason (str)
    """
    points = 0
    signals: list[str] = []

    # +2 Has a website
    if lead.get("website_url"):
        points += 2
        signals.append("has website")

    # +2 Has an email
    if lead.get("email"):
        points += 2
        signals.append("has email")

    # +1 Google rating >= 4.0
    rating = lead.get("google_rating")
    if rating and float(rating) >= 4.0:
        points += 1
        signals.append(f"rated {rating}★")

    # +1 Has 50+ reviews
    reviews = lead.get("review_count")
    if reviews and int(reviews) >= 50:
        points += 1
        signals.append(f"{reviews} reviews")

    # +1 Pitchable tech stack
    tech = lead.get("tech_stack", "")
    if tech in PITCHABLE_STACKS:
        points += 1
        signals.append(f"runs {tech}")

    # +1 No chatbot (opportunity)
    if not lead.get("has_chatbot", True):
        points += 1
        signals.append("no chatbot (opportunity)")

    # +1 Has LinkedIn
    social = lead.get("social_links", "")
    if social and "linkedin" in str(social).lower():
        points += 1
        signals.append("LinkedIn present")

    # +1 Growth keywords in meta description
    meta = (lead.get("meta_description") or "").lower()
    if any(kw in meta for kw in GROWTH_KEYWORDS):
        points += 1
        signals.append("growth-focused description")

    # Clamp to 1–10
    score = max(1, min(10, points))

    # Build reason from top signals
    if signals:
        reason = f"Strong signals: {', '.join(signals[:3])}."
    else:
        reason = "Minimal online presence detected."

    return {"score": score, "score_reason": reason}
