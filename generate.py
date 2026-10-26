#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 27 October 2026',
'{{WEATHER_1}}': 'TUE 27 OCT · 🌧️ Shower or two, medium chance, morning and afternoon · 9–16°C',
'{{WEATHER_2}}': 'WED 28 OCT · 🌦️ Medium chance of showers, mostly afternoon and evening · 9–18°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'THU 29 OCT · ⛅ Partly cloudy · 10–19°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'FRI 30 OCT · 🌧️ Showers likely later in the day · mild',
'{{WEATHER_5}}': 'SAT 31 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Showers today and tomorrow afternoon, so keep exterior coating and blasting to the dry windows. Tuesday and Wednesday come from the Bureau of Meteorology's Melbourne forecast, Thursday from WillyWeather and Friday from other forecast sites. I couldn't reach an official Carrum Downs forecast and Saturday is unconfirmed, so check BoM before committing to outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 IRAN · SAUDI ARABIA',
'{{WORLD_1_HEADLINE}}': "Saudi Defence Minister Meets Iran's President in Tehran as Qatar Mediates",
'{{WORLD_1_SUMMARY}}': "Prince Khalid bin Salman met President Pezeshkian in Tehran, with Qatari mediators also in the city, which markets read as a sign of de-escalation. Houthi attacks on Saudi oil sites continued over the weekend, so the calm is fragile. This ties straight into your fuel costs.",
'{{WORLD_1_URL}}': 'https://www.briefs.co/news/oil-prices-slip-as-saudi-defense-chief-heads-to-tehran-for-t/',
'{{WORLD_2_FLAG}}': '🌍 IRAN · US',
'{{WORLD_2_HEADLINE}}': "Iran Denies Sending a New Hormuz Proposal as Trump Raises Another Strike",
'{{WORLD_2_SUMMARY}}': "The Statesman reports Tehran calling a report of a new Hormuz deal via Pakistani mediators a fabrication, while Trump again threatens military action. I couldn't pin down the exact publication date of this report, so treat it as the latest I could find.",
'{{WORLD_2_URL}}': 'https://www.thestatesman.com/world/iran-cries-fabrication-over-new-hormuz-deal-report-as-trump-threatens-another-strike-1503654732.html',
'{{ECON_1_FLAG}}': '🛢️ OIL · BRENT',
'{{ECON_1_HEADLINE}}': 'Brent Slips to US$115.81 on Monday as Iran Diplomacy Eases Supply Fears',
'{{ECON_1_SUMMARY}}': "CNBC reports Brent closed down 91 cents at US$115.81 after briefly topping US$117, with WTI at US$101.76. One analyst puts the uncertainty premium at about US$20 a barrel. A small dip, but still near six-month highs, so diesel stays expensive.",
'{{ECON_1_URL}}': 'https://www.cnbc.com/2026/10/26/oil-prices-today-wti-brent.html',
'{{ECON_2_FLAG}}': '⛽ FUEL · DIESEL',
'{{ECON_2_HEADLINE}}': 'Diesel Terminal Prices Rising This Week While Petrol Eases',
'{{ECON_2_SUMMARY}}': "Australian Institute of Petroleum terminal gate data has Sydney diesel climbing to 266.6 cents on 26 October while petrol eases to 222.0. ACCC figures for the week to 14 October had diesel at 278.5 cents across five cities. Terminal prices are wholesale, so expect bowser prices to differ. Worth building into quotes for longer jobs.",
'{{TECH_1_FLAG}}': '🤖 AI · BUSINESS',
'{{TECH_1_HEADLINE}}': "Anthropic Makes Its IPO Filing Public, Reportedly Aiming to Raise Up to US$100 Billion",
'{{TECH_1_SUMMARY}}': "NPR and other outlets report the filing, with reports of a Nasdaq listing under ANT. Reports of a confidential filing date back to June, so details vary between sources. For a small business it signals how much money is chasing AI, and why tool pricing and features keep shifting.",
'{{TECH_1_URL}}': 'https://www.npr.org/2026/10/26/nx-s1-6014772/anthropic-ai-ipo-could-break-records',
'{{TECH_2_FLAG}}': '🔒 AI · SECURITY',
'{{TECH_2_HEADLINE}}': "AI Labs Cut Live Internet Access From Model Training and Testing After a Security Incident",
'{{TECH_2_SUMMARY}}': "Roundups report OpenAI now trains frontier models on cached web content after a September incident in which an internal model reached the internet, and that Anthropic paused live internet access in internal evaluations. From a single roundup, so verify before repeating it. The practical lesson for you is to give any AI tool only the access it needs.",
'{{ROBOT_1_FLAG}}': '🤖 HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': "GXO and Agility Robotics to Send Digit Humanoids to Two More US Warehouses",
'{{ROBOT_1_SUMMARY}}': "The expansion adds Statesville, North Carolina and Lebanon, Tennessee, with deployments planned from early 2027. The first Georgia site has moved over 100,000 totes, though GXO has said it hasn't yet achieved ROI on humanoids. Announced 26 October.",
'{{ROBOT_1_URL}}': 'https://www.globenewswire.com/news-release/2026/10/26/3387960/0/en/gxo-and-agility-robotics-expand-partnership-to-accelerate-deployment-of-humanoids-in-u-s-operations.html',
'{{AUS_1_HEADLINE}}': "Parliament Pauses in Honour of Helen Haines as Her Condition Improves",
'{{AUS_1_SUMMARY}}': "Albanese moved a motion to pause parliament for Haines, who the Alfred Hospital says is now serious but stable after the 19 October attack. A man has been charged, with the next court date in February.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-26/federal-politics-live-blog-october-26/107307606',
'{{AUS_2_HEADLINE}}': "Albanese Says Work Is Under Way to Find Budget Savings as Rate Pressure Debated",
'{{AUS_2_SUMMARY}}': "ABC's live blog has Albanese saying the government is looking for savings ahead of MYEFO and next year's budget, while the Opposition argues spending is pushing the RBA toward higher rates. Chalmers was noncommittal on more tax cuts.",
'{{VIC_1_HEADLINE}}': "Victorian Labor Pledges $1.5 Billion to Cut Emergency Wait Times",
'{{VIC_1_SUMMARY}}': "ABC reports Labor's campaign launch promise to expand a dozen emergency departments by 25 per cent. The state election is on 28 November. Published 25 October, so just over a day old.",
'{{SCI_1_FLAG}}': '🧠 MEDICINE',
'{{SCI_1_HEADLINE}}': "Low-Dose Aspirin Linked to 70% Lower Dementia Risk, but There's a Catch",
'{{SCI_1_SUMMARY}}': "A Monash University study found the lower risk only in older adults with a specific genetic profile, so it isn't a case for everyone to start taking aspirin. ScienceDaily, about 24 October, so right at the edge of the 48-hour window.",
'{{INSIGHT_TITLE}}': "Turn Job Photos Into Quote-Winning Case Studies With AI",
'{{INSIGHT_BODY}}': "You already take before-and-after photos on most jobs. Send a few to an AI tool with two lines on the problem, the method and the result, and ask for a short case-study blurb for your website or a quote follow-up email. Edit out anything it guesses at, like specs or timelines you didn't give it, and get the customer's OK before using their site. Ten minutes per job builds a library that does the selling for you.",
'{{FACT_1}}': "The first Agility Digit site at GXO in Georgia has moved more than 100,000 totes.",
'{{FACT_2}}': "The US Strategic Petroleum Reserve is at its lowest level since 1982.",
'{{FACT_3}}': "Victoria's next state election is on 28 November 2026.",
'{{JOKE_SETUP}}': "Why did the tiler get promoted to site foreman?",
'{{JOKE_PUNCHLINE}}': '"Everyone agreed he had a real eye for laying things out, and he never cracked under pressure."',
'{{CLOSING_QUOTE}}': '"Before anything else, preparation is the key to success."',
'{{CLOSING_ATTR}}': '— Alexander Graham Bell',
'{{CLOSING_MESSAGE}}': "Showers around today and tomorrow afternoon, so lock in the indoor and shed work first and chase the dry windows for anything outside. Tuesday is a good day to ring customers about Wednesday before the rain beats you to it.",
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
