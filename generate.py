#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 22 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 22 May (BOM forecast)
    "{{WEATHER_1}}": "FRI 22 · 🌧 Showers likely · 14°C",
    "{{WEATHER_2}}": "SAT 23 · ⛅ Partly cloudy · 15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SUN 24 · ☁ Overcast · 13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 25 · ☀ Clearing · 14°C",
    "{{WEATHER_5}}": "TUE 26 · ⛅ Mild · 13°C",
    "{{WEATHER_ALERT}}": "☔ SHOWERS LIKELY TODAY",

    # World
    "{{WORLD_1_FLAG}}": "🕊️ IRAN · PEACE TALKS",
    "{{WORLD_1_HEADLINE}}": "Trump Declares Iran War 'In Its Final Stages' as US Tables New Peace Proposal",
    "{{WORLD_1_SUMMARY}}": "US President Donald Trump declared Thursday that the conflict with Iran is 'in its final stages' as the US tables its latest diplomatic proposal. Secretary of State Marco Rubio is leading negotiations, with the White House framing the offer as a final opportunity to resolve the conflict before further escalation. Iran is reportedly divided at the highest levels over whether to accept terms — which would include reopening the Strait of Hormuz to international shipping and sanctions relief in exchange for binding commitments on the nuclear programme. For Australian businesses, the critical metric is whether those 230 tankers trapped in the Gulf can move again. Every week they can't, global oil markets stay elevated and Australian diesel costs remain under pressure.",
    "{{WORLD_1_URL}}": "https://www.cbsnews.com/live-updates/iran-war-trump-us-latest-peace-proposal/",

    "{{WORLD_2_FLAG}}": "⚽ FOOTBALL · ENGLAND",
    "{{WORLD_2_HEADLINE}}": "Arsenal Win the Premier League After 22-Year Wait — Manchester City Draw Gifts Gunners the Title",
    "{{WORLD_2_SUMMARY}}": "Arsenal Football Club has won the Premier League title for the first time since 2004, ending a 22-year drought after Manchester City drew with Bournemouth on the final day of the season. Celebrations erupted across north London as one of English football's most-talked-about waits came to a close. The Premier League attracts around 3 billion viewers globally each season, with a large and passionate Australian audience. For context: in 2004, the iPhone didn't exist, YouTube hadn't launched, and ISV was a very different business. Twenty-two years is a long time — and a decent reminder that persistence and staying in the game eventually pays off.",
    "{{WORLD_2_URL}}": "https://www.bbc.com/sport/football/premier-league",

    # Economics
    "{{ECON_1_FLAG}}": "📈 INTEREST RATES · RBA",
    "{{ECON_1_HEADLINE}}": "RBA Lifts Cash Rate to 4.35% — Third Straight Hike This Year Puts Australian SMEs on Defensive Footing",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank of Australia raised its cash rate by 25 basis points to 4.35% this month — fully unwinding last year's easing cycle in just three meetings. Voted 8-1, the decision reflects higher-than-expected inflation, now running at 5.0% in Q2 2026, driven partly by Strait of Hormuz fuel price impacts and stubborn domestic demand. Analysis from Inside Small Business estimates the full rate cycle is quietly costing a typical SME turning over $2 million an extra $29,000 to $43,000 this year alone — enough to wipe out a junior hire. CBA economists expect rates on hold for the rest of 2026, but Westpac is forecasting two more hikes in June and August, pushing the cash rate to 4.85%. Variable-rate borrowings and asset finance costs are not coming down any time soon.",
    "{{ECON_1_URL}}": "https://insidesmallbusiness.com.au/management/government-policies/smes-on-a-defensive-footing-after-third-rba-rate-hike-this-year",

    "{{ECON_2_FLAG}}": "🏠 FEDERAL BUDGET · PROPERTY",
    "{{ECON_2_HEADLINE}}": "Federal Budget Scraps Negative Gearing for New Investment Properties From This Week — What It Means for Trades",
    "{{ECON_2_SUMMARY}}": "The 2026-27 Federal Budget abolished negative gearing for investment properties purchased after 12 May 2026, replacing the 50% capital gains tax discount with a 30% minimum tax on inflation-adjusted gains for properties held after 1 July 2027. New dwellings are exempt — a deliberate carrot for apartment construction. The Budget also downgrades Australia's economic growth forecast to 1.75% in 2026-27 and officially upgrades Q2 2026 inflation to 5.0%. For trades businesses working in residential construction and renovation, the combination of higher borrowing costs, cooling property investor confidence, and tightening demand could reduce the volume of fit-out, coating, and maintenance work flowing through in the second half of the year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🚀 SPACEX · IPO",
    "{{TECH_1_HEADLINE}}": "SpaceX Files $80 Billion IPO — Largest in History, Revealing AI Losses, Rocket Losses, and Starlink Profits",
    "{{TECH_1_SUMMARY}}": "SpaceX filed its S-1 IPO prospectus with the SEC on Wednesday, targeting an $80 billion raise at a $1.7 trillion valuation — which would make it the largest initial public offering in history. The filing laid bare the company's real financial structure for the first time: only Starlink turns a profit ($1.2B operating profit in Q1), while the rocket launch business lost $662M and the AI division (the merged xAI entity) burned through $2.5B. OpenAI is expected to file its own IPO in September at a $1 trillion valuation. Together, these two filings represent the largest-ever market test of whether investors believe AI and space infrastructure is worth trillions — before most of the underlying businesses have turned a profit.",
    "{{TECH_1_URL}}": "https://siliconangle.com/2026/05/20/spacex-releases-ipo-filing-openai-reportedly-prepares-september-listing/",

    "{{TECH_2_FLAG}}": "🟢 NVIDIA · EARNINGS",
    "{{TECH_2_HEADLINE}}": "Nvidia Reports Record $81.6 Billion Quarter — AI Chip Demand Up 85%, Market Barely Flinches",
    "{{TECH_2_SUMMARY}}": "Nvidia's Q1 fiscal 2027 results landed Wednesday with revenue of $81.6 billion — up 85% year-on-year and 20% on the prior quarter — and data centre revenue hitting $75.2 billion, up 92%. The company also boosted its quarterly dividend 25-fold and authorised another $80 billion in buybacks. Remarkably, the stock barely moved — expectations had simply grown as large as the numbers themselves. For anyone running AI tools in their business, Nvidia's numbers confirm the infrastructure behind AI is expanding at pace. The models being built on top of it are getting more capable, cheaper to run, and faster to access every quarter.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 BOSTON DYNAMICS · FACTORY",
    "{{ROBOT_1_HEADLINE}}": "Atlas Humanoid Robot Enters Hyundai Factories — Boston Dynamics Reveals How It Learned to Lift 100-Pound Loads",
    "{{ROBOT_1_SUMMARY}}": "Boston Dynamics has published new technical detail on how its Atlas humanoid mastered handling 100-pound (45kg) loads with factory-floor precision — a critical industrial capability milestone. Production units are now shipping to Hyundai's Robotics Metaplant Application Center in Savannah, Georgia, with Hyundai Motor Group planning a new robotics factory capable of producing 30,000 Atlas units per year. Every 2026 Atlas allocation is already spoken for. At 56 degrees of freedom, 50kg lift capacity, water resistance, and operation in conditions from -20°C to 40°C, Atlas is transitioning from research platform to production infrastructure. For industrial services businesses, the question is no longer whether humanoid robots are real — it's whether you understand what maintaining and servicing them will require.",
    "{{ROBOT_1_URL}}": "https://newatlas.com/ai-humanoids/boston-dynamics-production-atlas-hyundai/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australian House Prices Fall in Most Capitals After Third RBA Hike — But One State Keeps Charging Ahead",
    "{{AUS_1_SUMMARY}}": "Australian property prices are beginning to slide in most capital cities following the RBA's third consecutive rate hike this year. Sydney and Melbourne have recorded modest quarterly falls, while Brisbane has also slowed. Adelaide continues to outperform, buoyed by infrastructure spending and migration patterns. For trades businesses dependent on the residential construction and renovation pipeline in Melbourne, softening prices signal reduced investor activity — particularly as the new Federal Budget rules for negative gearing shift the calculus for property investors buying after 12 May.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/house-prices-are-falling-in-some-places-but-one-state-keeps-charging-ahead/520q3zwnc",

    "{{AUS_2_HEADLINE}}": "Australia on Track for 380,000-Home Shortfall by 2030 as Rate Hikes and Costs Stall New Builds",
    "{{AUS_2_SUMMARY}}": "The Urban Development Institute of Australia has warned Australia is tracking toward a shortfall of 380,000 new dwellings by 2030, with new housing production now forecast to drop 11% in 2026 as elevated construction costs, persistent labour shortages, and three straight rate hikes choke new housing starts. For trades businesses, the near-term read is mixed: new-build pipelines are contracting, but existing stock always needs maintenance, protective coatings, and remediation — demand that doesn't disappear with a slower property market.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Suburban Rail Loop Tunnelling Begins — Eight Giant Boring Machines Start Carving 26km Under Melbourne",
    "{{VIC_1_SUMMARY}}": "Tunnelling has officially commenced on the Suburban Rail Loop East — Victoria's landmark $34 billion first-stage infrastructure project. Eight tunnel boring machines, each named after groundbreaking Victorian women and powered by 100% renewable electricity, are launching from Clarinda and Burwood to bore 26 kilometres of twin tunnels up to 60 metres below the surface. The route connects Cheltenham to Box Hill via Clayton, Monash, Glen Waverley and Burwood — with trains running from 2035. For south-east Melbourne trades businesses including those in Carrum Downs, the SRL will eventually reshape the entire region's accessibility. For contractors, it signals sustained government infrastructure spending physically underway beneath the city.",

    # Science
    "{{SCI_1_FLAG}}": "⚡ PLANETARY SCIENCE",
    "{{SCI_1_HEADLINE}}": "Jupiter's Lightning Storms May Be 100 Times More Powerful Than Earth's — and Could Help Explain Life",
    "{{SCI_1_SUMMARY}}": "Using data from NASA's Juno spacecraft, scientists have confirmed that lightning strikes on Jupiter can pack up to 100 times more energy than Earth's most powerful bolts — with extreme cases potentially 10,000 times more energetic. Individual Jovian bolts carry up to 10 trillion joules (equivalent to 2,400 tonnes of TNT), compared to roughly 1 billion joules for a typical Earth strike. Jupiter's towering storm systems — some 100 kilometres tall — build enormous electrical charges before erupting in flashes that dwarf anything in our atmosphere. Beyond the spectacle, researchers note that such extreme lightning may be capable of triggering the complex chemical reactions thought necessary to initiate life on worlds with the right atmospheric chemistry. Published in ScienceDaily, 20 May 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Every Completed Job Is a Case Study Waiting to Be Written — AI Does It in 60 Seconds",
    "{{INSIGHT_BODY}}": "Most trades businesses finish a job, send the invoice, and move on — leaving a story untold. Every completed job contains the building blocks of genuinely compelling marketing: the client's problem, the solution you delivered, the measurable outcome, and the conditions you worked in. That's a case study, a Google review request, a portfolio entry, and a LinkedIn post rolled into one. The problem is writing it all up takes time most operators simply don't have at the end of a long day on site. AI solves that. Drop your end-of-job notes, a photo description, and the job scope into Claude or ChatGPT and ask it to produce: (1) a one-paragraph case study for your website, (2) a text message to the client requesting a Google review, and (3) a 150-word LinkedIn post with a before-and-after frame. Done in under two minutes. For a business like ISV — where every job involves technical prep work, measurable surface profile outcomes, and visible transformations — this kind of documented content is genuinely compelling to prospective clients searching for evidence of quality. The businesses winning work in 2026 aren't necessarily cheaper or faster. They're better documented.",

    # Fun Facts
    "{{FACT_1}}": "The first commercial hard disk drive — the IBM 350, released in 1956 — weighed an entire tonne, required a forklift to install, stored just five megabytes of data, and cost the equivalent of roughly $300,000 per year to lease in today's money. A modern 4TB portable hard drive stores 800,000 times more data for around $100 and fits in a jacket pocket. The entire progression happened in 70 years.",

    "{{FACT_2}}": "The Scoville scale — used to rank the heat of chillies — was invented by American pharmacist Wilbur Scoville in 1912, using a panel of human tasters who drank progressively diluted pepper extract until they could no longer detect the burn. Pure capsaicin rates 16 million Scoville Heat Units (SHU). Law enforcement pepper spray runs 2 to 5 million SHU — hotter than virtually any natural chilli most people will ever encounter, including the Carolina Reaper at around 1.6 million SHU.",

    "{{FACT_3}}": "Volcanic lightning — sometimes called a 'dirty thunderstorm' — occurs when ash particles collide and generate massive static charges inside eruption columns, producing lightning bolts that crackle through clouds of volcanic debris kilometres above the ground. It has been photographed at Mount Pinatubo (1991), Eyjafjallajokull (2010), and Taal Volcano (2020), with some eruptions generating thousands of bolts per hour before the ash cloud even reaches populated areas below.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the steel fabricator always win every argument on site?",
    "{{JOKE_PUNCHLINE}}": "He had an iron-clad case.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Either you run the day or the day runs you.”",
    "{{CLOSING_ATTR}}": "— Jim Rohn",
    "{{CLOSING_MESSAGE}}": "Friday morning in Carrum Downs — showers expected through the day at around 14°C, so plan outdoor work around the weather and move any exposed gear under cover between jobs. This week delivered a dense stack of economic signals: the RBA is now at 4.35% after three straight hikes, the Federal Budget scrapped negative gearing from this week, inflation is officially at 5%, and the housing construction pipeline is contracting. For a trades business, that means the maintenance and protective coatings market holds up better than new builds — existing stock always needs work regardless of what investors are doing. It's Friday: a good day to spend 15 minutes documenting this week's completed jobs before the weekend wipes the details. Photos, scope, outcome. That's tomorrow's case study. Have a strong end to the week, Liall.",
}

with open("template.html", "r", encoding="utf-8") as f:
    html = f.read()

for placeholder, value in replacements.items():
    html = html.replace(placeholder, value)

remaining = re.findall(r"\{\{[A-Z_0-9]+\}\}", html)
if remaining:
    print(f"WARNING: Unreplaced placeholders: {remaining}")
else:
    print("All placeholders replaced successfully.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html written successfully.")
