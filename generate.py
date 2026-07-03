#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 04 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 4 Jul
    "{{WEATHER_1}}": "SAT 4 · 🌧 Showers · 8–15°C",
    "{{WEATHER_2}}": "SUN 5 · ☁️ Cloudy · 9–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 6 · ☀️ Sunny, frosty start · 3–15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "TUE 7 · ⛅ Mostly sunny · 5–14°C",
    "{{WEATHER_5}}": "WED 8 · ⛅ Partly cloudy · 6–14°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS EASING TODAY · DIESEL & PETROL RISING AS FUEL EXCISE DISCOUNT HALVES",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 IRAN · KHAMENEI FUNERAL · WEEK OF MOURNING BEGINS",
    "{{WORLD_1_HEADLINE}}": "Iran Begins a Week of Funeral Ceremonies for Slain Supreme Leader Khamenei",
    "{{WORLD_1_SUMMARY}}": "Ayatollah Ali Khamenei's body lay in state in Tehran on Friday as officials, clerics and foreign dignitaries from more than 50 delegations paid their respects, opening a mourning period expected to run through July 9 across Iran and Iraq. Khamenei was killed alongside family members in the opening strikes of the US-Israeli attack on Tehran in February; Tehran's mayor has said turnout at this weekend's viewings, followed by Monday's funeral procession, could reach 20 million people. It's a moment likely to shape Middle East diplomacy for months, with US-Iran talks in Doha paused around the ceremonies.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/7/3/iran-begins-week-of-funeral-ceremonies-for-slain-supreme-leader-khamenei",

    "{{WORLD_2_FLAG}}": "🇫🇷 SOUTHERN FRANCE · WILDFIRES · THOUSANDS EVACUATED",
    "{{WORLD_2_HEADLINE}}": "Wildfires Scorch Southern France as Record Heatwave and Drought Fuel the Blazes",
    "{{WORLD_2_SUMMARY}}": "Multiple fires are burning across southern France, with the largest blaze near the Spanish border in the Aude and Hérault regions having scorched around 900 hectares and prompting roughly 800 firefighters and 150 vehicles to be deployed. Nearly 5,000 people have been evacuated from coastal campsites as wind gusts up to 70km/h hamper containment, following an 11-day record-breaking heatwave through June. A reminder of how fast a dry, hot run of weeks turns into an emergency — a pattern playing out across southern Europe this northern summer.",
    "{{WORLD_2_URL}}": "https://www.manilatimes.net/2026/07/03/world/wildfires-scorch-southern-france-as-heat-and-drought-fuel-blazes/2377748",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL PRICES · ACCC · EXCISE DISCOUNT HALVED",
    "{{ECON_1_HEADLINE}}": "Petrol and Diesel Prices Jump as the Fuel Excise Discount Halves From July 1",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly monitoring shows average retail petrol across the five largest capital cities rose to 158.1 cents a litre on July 1 (from 151.5c the day before), while diesel jumped to 179.1 cents a litre (from 173.5c) — the direct result of the temporary 32-cent fuel excise cut being halved to 16 cents from July 1, a measure due to run until August 2. Worth checking against whatever number you last quoted a job's fuel cost on, since the increase is landing in real time this week.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/media-release/accc-to-monitor-fuel-prices-and-market-behaviour-as-fuel-excise-is-partly-restored",

    "{{ECON_2_FLAG}}": "🛒 ACCC · RETAIL · SUPERMARKET PRICE-GOUGING NOW ILLEGAL",
    "{{ECON_2_HEADLINE}}": "World-First Law Banning Supermarket Price Gouging Takes Effect, Coles and Woolworths in the Crosshairs",
    "{{ECON_2_SUMMARY}}": "From this month, Australia's new Food and Grocery Code amendments make it illegal for 'very large retailers' — in practice just Coles and Woolworths, the only two chains turning over more than $30 billion — to charge prices the ACCC deems excessive relative to supply cost plus a reasonable margin, with penalties up to $10 million or 10% of annual turnover per breach. It won't move the needle on trade material costs directly, but it's the clearest sign yet regulators are willing to intervene on pricing power — worth watching if it extends to other sectors down the track.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 MICROSOFT · ENTERPRISE AI · $2.5B FRONTIER COMPANY",
    "{{TECH_1_HEADLINE}}": "Microsoft Launches $2.5 Billion 'Frontier Company' to Embed AI Engineers Inside Client Businesses",
    "{{TECH_1_SUMMARY}}": "Microsoft announced a new $2.5 billion business unit this week, Microsoft Frontier Company, that will place around 6,000 AI and industry experts directly inside customer organisations — from LSEG to Unilever — to help them design, deploy and continually improve AI systems tied to measurable business outcomes. It's the clearest sign yet that the big platforms see 'someone helps you actually use the AI' as the next competitive battleground, not just better models — a service tier way beyond small-business budgets today, but a hint at where AI support is heading.",
    "{{TECH_1_URL}}": "https://blogs.microsoft.com/blog/2026/07/02/microsoft-frontier-company-ai-engineering-that-amplifies-and-protects-your-intelligence/",

    "{{TECH_2_FLAG}}": "🤖 AMAZON · ENTERPRISE AI · $1B FORWARD-DEPLOYED ENGINEERS",
    "{{TECH_2_HEADLINE}}": "Amazon Joins the AI Deployment Arms Race With Its Own $1 Billion Engineer Unit",
    "{{TECH_2_SUMMARY}}": "Days before Microsoft's move, AWS committed $1 billion to its own new Forward Deployed Engineering unit, embedding pods of five or six engineers with clients including the NBA, NFL and Southwest Airlines to get agentic AI systems live in roughly 45-day cycles. Between Amazon, Microsoft, OpenAI and Anthropic all standing up near-identical units within weeks of each other, the message from the top of the industry is unmistakable: knowing which AI tool exists isn't the bottleneck anymore, getting it actually working inside a real business is.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · UBTECH · MASS-PRODUCED HUMANOID LAUNCHED",
    "{{ROBOT_1_HEADLINE}}": "UBTECH Launches the World's First Mass-Produced Full-Size 'Ultra-Bionic' Humanoid Robot",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics maker UBTECH unveiled its UWORLD U1 series this week — three models starting from roughly 119,800 RMB (around AUD $25,000), with 88 degrees of freedom and a biomimetic 'spine' letting it replicate about 90% of human movement. Orders have already passed 13,000 units ahead of first deliveries in September, positioning it as the first humanoid robot line built for genuine mass production rather than a one-off demo unit — another marker of how fast the hardware side of this industry is scaling, even if the price tag keeps it firmly in factory and research territory for now.",
    "{{ROBOT_1_URL}}": "https://www.prnewswire.com/news-releases/ubtech-launches-uworld-u1-the-worlds-first-full-size-mass-produced-ultra-bionic-humanoid-robot-302815285.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "World-First Supermarket Price-Gouging Ban Takes Effect, Coles and Woolworths Face $10M Fines",
    "{{AUS_1_SUMMARY}}": "Australia became the first country to outlaw supermarket price gouging this month, with new ACCC-enforced rules targeting Coles and Woolworths specifically — the only two retailers turning over more than $30 billion a year — with fines up to $10 million per breach. Ironically, the government's own report last year found no clear evidence of gouging by the pair, but the law is now live regardless.",
    "{{AUS_1_URL}}": "https://ministers.treasury.gov.au/ministers/andrew-leigh-2025/media-releases/price-gouging-large-supermarkets-illegal-1-july-2026",

    "{{AUS_2_HEADLINE}}": "Australia Commits $2 Million in Emergency Aid to Venezuela's Earthquake Recovery",
    "{{AUS_2_SUMMARY}}": "Foreign Minister Penny Wong announced $2 million in humanitarian funding this week for communities hit by the magnitude 7.2 and 7.5 earthquakes that struck west of Caracas on June 24, joining the US, UK and EU in funding emergency food, shelter and water for the roughly two million Venezuelans now in need.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Minor Flooding Continues Across North-East Victoria After Heavy Rain, Murray and Goulburn Rivers Affected",
    "{{VIC_1_SUMMARY}}": "The Bureau of Meteorology's flood watch remains current for parts of north-east and central Victoria, with minor flood warnings in place for the Murray River upstream of Lake Hume, the Mitta Mitta and the Goulburn — a reminder that while Carrum Downs copes with the usual winter showers, some regional Victorian communities are dealing with a fair bit more this week.",

    # Science
    "{{SCI_1_FLAG}}": "🌞 SPACE WEATHER · SOLAR STORM · AURORA CHANCE THIS WEEKEND",
    "{{SCI_1_HEADLINE}}": "The Sun Fired Off 10 Flares in 24 Hours — And the Resulting Storm Could Bring Aurora This Weekend",
    "{{SCI_1_SUMMARY}}": "A powerful X1.1 solar flare on June 30 sent a coronal mass ejection toward Earth, with forecasters expecting G1–G2 geomagnetic storm conditions (a chance of G3) to peak overnight into Sunday — strong enough that the Aurora Australis has a real shot at being visible from parts of southern Victoria and the Mornington Peninsula if skies clear after today's showers. Worth a look outside after dark this weekend if you're up; solar activity is still ramping up toward the peak of the current 11-year solar cycle.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Payday Super Has Landed — Is Your Payroll Actually Ready?",
    "{{INSIGHT_BODY}}": "From this month, employers are legally required to pay superannuation at the same time as wages instead of quarterly — a rule called Payday Super — with the ATO able to hit late payments with a new, tougher penalty regime from day one. For a small trades business running payroll off a spreadsheet or last year's habits, that's a real trap: miss the same-day super transfer even once by accident and the penalty regime doesn't care that it was an oversight. A genuinely useful move this week: ask your bookkeeping software (or an AI assistant reading your payroll process) to confirm super is actually configured to run automatically alongside every pay cycle, not just at quarter's end like it always has. Fifteen minutes checking now is considerably cheaper than an ATO penalty notice later.",

    # Fun Facts
    "{{FACT_1}}": "The first chatbot, ELIZA, was built in 1966 by MIT's Joseph Weizenbaum to simulate a psychotherapist by simply rephrasing whatever the user typed as a question — some early users still insisted they were talking to something that truly understood them, a reaction Weizenbaum found so unsettling he later became one of AI's most prominent critics.",

    "{{FACT_2}}": "Victoria's Ninety Mile Beach in Gippsland runs for approximately 151 kilometres without a single break, making it one of the longest continuous, uninterrupted beaches on Earth — roughly the driving distance from Carrum Downs to Wilsons Promontory in one unbroken stretch of sand.",

    "{{FACT_3}}": "The humble spirit level — a sealed glass tube with liquid and an air bubble — was invented in 1661 by French scientist Melchisédech Thévenot, and the basic design hasn't meaningfully changed in the 364 years since; it still outperforms most digital levels for a fast, no-battery sanity check on site.",

    # Joke
    "{{JOKE_SETUP}}": "Why is a chimney sweep never short on work during a Melbourne winter?",
    "{{JOKE_PUNCHLINE}}": "Because every homeowner who ignored their flue all summer suddenly remembers it exists on the first freezing morning in July.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Fall seven times, stand up eight.”",
    "{{CLOSING_ATTR}}": "— Japanese Proverb",
    "{{CLOSING_MESSAGE}}": "It's Saturday, and today's showers should ease into a cloudy but calmer Sunday before Monday brings a frosty, sunny start to the week — good timing if there's outdoor prep work on the list. Keep an eye out after dark this weekend too, with a decent chance of the Aurora Australis putting on a show over the Mornington Peninsula if the sky clears. And if you've got staff on the books, it's worth a five-minute check that your payroll is actually running Payday Super correctly now that it's live — better to catch it yourself than have the ATO catch it for you.",
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
