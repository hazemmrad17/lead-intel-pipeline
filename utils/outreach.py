"""
Outreach Generator — Rule-based implementation of Outreach Personalization Agent (Prompt 4).

Generates a short, personalized cold outreach message per lead.
Template is kept generic so the user can customise the service being pitched.

Rules (from guide):
  - Max 4 sentences
  - No "I hope this message finds you well"
  - No agency name or pricing
  - References ONE specific detail from the lead's profile
  - Ends with a soft question (not "Are you interested?")
  - Tone: direct, peer-to-peer, not salesy
"""


# Generate a personalized cold outreach message for a single lead.
def generate_outreach(lead: dict) -> str:
    """
    Generate a personalised cold outreach message for a single lead.

    Args:
        lead: enriched lead dict with keys business_name, tech_stack,
              has_chatbot, meta_description, score_reason, niche.

    Returns:
        str: The outreach message (plain text, 3-4 sentences).
    """
    name = lead.get("business_name", "there")
    tech = lead.get("tech_stack", "Unknown")
    has_chatbot = lead.get("has_chatbot", False)
    meta = lead.get("meta_description") or ""
    niche = lead.get("niche", "your industry")

    # Pick the strongest personalisation hook
    hook = _build_hook(tech, has_chatbot, meta, niche)

    # Build the message
    opener = f"Came across {name} while looking into {niche} businesses — {hook}."
    body = _build_body(tech, has_chatbot)
    cta = _build_cta(tech, has_chatbot)

    return f"{opener} {body} {cta}"


# ── Internal helpers ──────────────────────────────────────────────────────────

# Build the personalization hook based on metadata, tech stack, or general impression.
def _build_hook(tech: str, has_chatbot: bool, meta: str, niche: str) -> str:
    """Select the most specific detail to reference in the opener."""
    if meta and len(meta) > 20:
        # Trim to ~60 chars for the message
        snippet = meta[:60].rstrip() + ("…" if len(meta) > 60 else "")
        return f"noticed your positioning around \"{snippet}\""
    if tech not in ("Unknown", "Unreachable"):
        return f"noticed you're running on {tech}"
    return "impressed by what you've built"


# Build the body paragraph focusing on chatbot opportunity or site optimization.
def _build_body(tech: str, has_chatbot: bool) -> str:
    """Return the value-prop sentence based on tech + chatbot status."""
    if not has_chatbot:
        return (
            "Most businesses in this space are leaving leads on the table "
            "without an automated way to qualify visitors in real time."
        )
    if tech in ("WordPress", "Webflow"):
        return (
            f"There are a few quick wins specific to {tech} sites that tend "
            "to move the needle on conversions without a full rebuild."
        )
    return (
        "A lot of similar businesses are finding small automation changes "
        "drive outsized results on their existing setup."
    )


# Generate a soft call-to-action question specific to the lead's tech stack.
def _build_cta(tech: str, has_chatbot: bool) -> str:
    """Return a soft, open-ended closing question."""
    if not has_chatbot:
        return "Would it be worth a quick chat to see if there's a fit for your team?"
    if tech in ("WordPress", "Webflow"):
        return "Would you be open to a 15-minute look at what's working for similar sites?"
    return "Is this something you've been exploring, or is it off the table for now?"
