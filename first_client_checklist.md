# First Client Checklist — Hazem Mrad
**Goal:** Go from built project → first paying client  
**Timeline:** 3 days max if you follow this daily

---

## STEP 1 — Clean Code + README + Push to GitHub
**Time needed: 2–3 hours**

### 1.1 Clean your code
- [ ] Delete any print statements used for debugging
- [ ] Add a comment above every function explaining what it does (one line is enough)
- [ ] Make sure `main.py` runs with zero errors end to end
- [ ] Delete any unused imports
- [ ] Rename any variables like `x`, `temp`, `data2` to something readable
- [ ] Put your niche and location as input prompts, NOT hardcoded strings

### 1.2 Write your README.md
Copy this structure exactly into your README.md file:

```markdown
# Lead Intel Pipeline 🔍

> Drop in a niche + city → get back 50 enriched, ready-to-contact business leads in minutes.

## What it does
1. Scrapes Google Maps for businesses matching your niche + location
2. Visits each website to extract emails, tech stack, and company info
3. Exports a clean CSV ready for outreach

## Output example
| business_name | email | tech_stack | google_rating | has_chatbot |
|---|---|---|---|---|
| Acme Agency | hello@acme.co | WordPress | 4.7 | false |
| Nova Digital | team@nova.io | Shopify | 4.2 | true |

## Setup
```bash
git clone https://github.com/hazemmrad17/lead-intel-pipeline
cd lead-intel-pipeline
pip install -r requirements.txt
python main.py
```

## Built with
Python · Selenium · BeautifulSoup · Pandas

## Author
Hazem Mrad — AI & Data Engineer  
[Portfolio](https://hazemmrad-io.vercel.app) · [LinkedIn](https://linkedin.com/in/hazem-mrad)
```

### 1.3 Push to GitHub
Run these commands in your terminal one by one:

```bash
# 1. Go to github.com → New Repository
# Name it: lead-intel-pipeline
# Set it to PUBLIC
# Do NOT initialize with README (you already have one)

# 2. In your project folder:
git init
git add .
git commit -m "Initial commit: lead enrichment pipeline with scraper + enricher"
git branch -M main
git remote add origin https://github.com/hazemmrad17/lead-intel-pipeline.git
git push -u origin main
```

- [ ] Repo is live at github.com/hazemmrad17/lead-intel-pipeline
- [ ] README renders correctly on the repo homepage
- [ ] All files are visible (scraper/, utils/, main.py, requirements.txt)

---

## STEP 2 — Record the Loom Demo
**Time needed: 1 hour (including re-records)**

### 2.1 Setup before recording
- [ ] Go to loom.com → sign up free
- [ ] Download Loom desktop app
- [ ] Set recording to: Screen + Camera (small bubble, bottom right)
- [ ] Open your terminal, VS Code, and a blank Excel/CSV viewer
- [ ] Run the pipeline once BEFORE recording so you know it works
- [ ] Save the output CSV from that test run — use it as backup if live run is slow

### 2.2 The exact script (90 seconds)

**0:00 – 0:08** — Don't say hi. Start with the hook:
> "This pipeline takes a niche and a city — and gives you back 50 enriched leads in under 5 minutes."

**0:08 – 0:20** — Show terminal, type:
```bash
python main.py
```
Enter niche: `digital marketing agency`  
Enter location: `Manchester`

**0:20 – 0:50** — Let it run. While it runs, narrate:
> "It's hitting Google Maps, pulling listings, then visiting each website to grab emails, detect their tech stack, check for chatbots..."

**0:50 – 1:10** — Open leads.csv. Zoom in. Point at columns:
> "Every row has the business name, their email, what platform they're built on, their Google rating, and whether they already have a chatbot or not."

**1:10 – 1:25** — Zoom into ONE specific row. Read it out:
> "This one — 4.8 stars, WordPress site, no chatbot, email right there. That's a warm lead."

**1:25 – 1:30** — End with:
> "Custom niche, any city, clean output. I build these for specific industries on request."

### 2.3 After recording
- [ ] Trim start/end silence in Loom editor
- [ ] Copy the Loom share link
- [ ] Paste it in your GitHub README under a "## Demo" section
- [ ] Also save the link somewhere — you'll use it in every outreach message

---

## STEP 3 — Update Upwork Profile
**Time needed: 30 minutes**

### 3.1 Title
Delete whatever is there. Replace with exactly:
```
AI Engineer | RAG Pipelines · Web Scraping · Lead Enrichment · Python
```

### 3.2 Overview — first 2 lines (most important, shows before "more")
```
I build data extraction and lead enrichment pipelines in Python — scraping 
static and dynamic pages, enriching with website signals, and delivering 
clean structured output ready for action.
```

### 3.3 Overview — full bio (paste this, edit where marked)
```
I'm an AI & Data Science engineering student at ESPRIT (Tunisia) specializing 
in building real data pipelines — not no-code wrappers.

What I deliver:
→ Web scraping pipelines (Selenium + BeautifulSoup, static & dynamic pages)
→ Lead enrichment systems (emails, tech stack detection, scoring)
→ RAG pipelines (LangChain + ChromaDB/Neo4j for AI knowledge bases)
→ REST API integrations and JSON/XML data processing

Recent work:
- Built a GraphRAG data pipeline for Vital Laboratoire (pharma company) — 
  scraped unstructured web content, cleaned and pushed into Neo4j for an 
  AI knowledge base
- Built data collection pipelines feeding a real-time YOLO computer vision 
  model for an AI sports management platform (Top 10, ESPRIT 2025)
- Built a lead enrichment pipeline that scrapes Google Maps + enriches each 
  result with email, tech stack, and chatbot detection [GitHub: link here]

I work fast, document my code, and communicate clearly.
Fixed-price projects delivered in 5–7 days.
```

### 3.4 Skills to add
Add ALL of these as skills tags:
```
Python, Web Scraping, Selenium, BeautifulSoup, Data Pipeline, 
LangChain, RAG, Neo4j, REST API, JSON, Pandas, Data Extraction,
Lead Generation, Data Cleaning, ChromaDB
```

### 3.5 Rate
- [ ] Set hourly rate to $20–25/hr minimum
- [ ] Do NOT go lower — it signals low quality, not affordability

### 3.6 Portfolio section
- [ ] Add your GitHub repo link as a portfolio item
- [ ] Title it: "Lead Enrichment Pipeline — Google Maps + Website Enricher"
- [ ] Paste your Loom link in the description

---

## STEP 4 — Send 10 Outreach Messages
**Time needed: 1–2 hours**

### 4.1 Where to find leads to message

**On Reddit (free, high intent):**
- Go to r/LangChain, r/datasets, r/MachineLearning, r/webdev
- Search: "scraping help", "lead generation", "data pipeline", "RAG"
- Filter by: New (last month)
- Look for posts where someone is struggling with a problem you solved

**On X/Twitter:**
Search these exact phrases:
```
"need help with scraping"
"web scraping problem"
"lead generation python"
"RAG pipeline help"
"data pipeline freelancer"
```

**On IndieHackers (indiehackers.com):**
- Go to "Ask IH" section
- Search "data", "scraping", "leads", "pipeline"
- People here have money and real problems

**On Upwork (proactive):**
- Search: "web scraping", "lead enrichment", "data pipeline", "RAG"
- Filter: Posted last 7 days, Budget $200+
- Apply to 5 jobs minimum daily

---

### 4.2 The outreach message template

**For Reddit/IndieHackers (comment on their post first, then DM):**
```
Hey [name] — I saw your post about [specific problem they mentioned].

I actually built something that solves exactly this — a pipeline that 
[one sentence describing what it does relevant to their problem].

Here's a 90-second demo: [your Loom link]
And the code: [your GitHub link]

Happy to build a custom version for your use case if it looks useful — 
what's your data source / target niche?
```

**For X/Twitter DM:**
```
Hey — saw your tweet about [problem].

Built something relevant last week — [one line description].
Demo: [Loom link]

Would a custom version be useful for what you're working on?
```

**For Upwork proposal (CRITICAL — first 2 lines are everything):**
```
I built exactly this last week — here's it running live: [Loom link]

[Then 2-3 lines addressing their specific job post requirements]

I can deliver this in 5 days. Fixed price, clean documented code.
Happy to jump on a quick call to scope it out.
```

---

### 4.3 Tracking your outreach
Keep a simple spreadsheet with these columns:

| Date | Platform | Name/Handle | Message Sent | Response | Follow Up |
|------|----------|-------------|--------------|----------|-----------|

- [ ] Send 10 messages today
- [ ] Follow up on non-responses after 3 days (one time only)
- [ ] If someone responds with interest → jump on a 20-min call, don't negotiate over chat

---

## Daily Routine Until First Client

**Every morning:**
1. Check responses to yesterday's outreach (15 min)
2. Apply to 3–5 new Upwork jobs (30 min)
3. Find and message 3 new leads on Reddit/X/IH (30 min)

**Every 2 days:**
- Post on LinkedIn or X: one short update about what you built or learned
  (builds visibility passively while you outreach actively)

---

## Pricing Reference

| Service | Price |
|---------|-------|
| Basic scraper (1 source, CSV output) | $150–250 |
| Lead enrichment pipeline (like this project) | $300–500 |
| RAG pipeline (scraping + vector store + Q&A) | $500–900 |
| Full system (scraping + RAG + simple UI) | $800–1500 |
| Hourly consulting/debugging | $20–30/hr |

**Rule:** Never quote lower than these. If they push back on price, explain the time saved, not the hours you spent.

---

## First Client Red Flags (avoid these people)

- "Can you do a test task first for free?"
- "Budget is $50 but it's simple"
- "I need this by tomorrow"
- "Can you just teach me how to do it?"
- Vague brief with no real data source mentioned

**Green flags (say yes fast):**
- They describe a specific problem with a specific data source
- They mention they've tried and failed themselves
- Budget is mentioned upfront ($200+)
- They ask about timeline, not price
