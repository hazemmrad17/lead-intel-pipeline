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
