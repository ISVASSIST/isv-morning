#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 23 October 2026',
'{{WEATHER_1}}': 'FRI 23 OCT · ☀️ Warm and mostly sunny, small afternoon shower chance · ~29°C',
'{{WEATHER_2}}': 'SAT 24 OCT · 🌧️ Showers, possible afternoon thunderstorm',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SUN 25 OCT · 🌧️ Cooler, showers likely, solid rain possible · ~17°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'MON 26 OCT · 🌥️ Cool and showery',
'{{WEATHER_5}}': 'TUE 27 OCT · 🌥️ Cool, showers possible',
'{{WEATHER_ALERT}}': "Today is the last warm, mostly dry day: about 29°C with only a slight chance of a shower. A cool, wet change arrives Saturday, with a possible afternoon thunderstorm, and Sunday looks cooler and showery. Showery conditions may linger into early November. Forecasts vary between sources and I couldn't confirm Carrum Downs figures for Monday and Tuesday, so check BoM before committing to outdoor or coating jobs.",
'{{WORLD_1_FLAG}}': '🌍 IRAN WAR',
'{{WORLD_1_HEADLINE}}': "US Pulls Diplomats From Saudi Arabia as It Reportedly Readies Iran Strikes After the Midterms",
'{{WORLD_1_SUMMARY}}': "CNBC, 22 October: the State Department ordered diplomats out of Saudi Arabia, citing rising attacks by Iran-aligned Houthis. Other reports say Trump has said the US won't attack Iran before the 3 November midterms, and Iran says the Strait of Hormuz stays closed until its conditions are met. Fuel stays exposed either way.",
'{{WORLD_1_URL}}': 'https://www.cnbc.com/2026/10/22/us-iran-trump-hormuz-.html',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': "Iran Says Seven Vessels Hit Near Hormuz and Warns of a Wider Response Against US Bases; Trump Denies Talks Are Happening",
'{{WORLD_2_SUMMARY}}': "NewsNation reports Iran's Revolutionary Guard says seven vessels were damaged near the Strait, while CENTCOM says most Iranian attacks on shipping fail. Qatar says indirect US-Iran engagement continues despite Washington's denials. Accounts conflict, so treat claims from each side with caution.",
'{{WORLD_2_URL}}': 'https://www.newsnationnow.com/world/us-iran-war-strait-of-hormuz-oil-tankers/',
'{{ECON_1_FLAG}}': '📈 ASX · MARKETS',
'{{ECON_1_HEADLINE}}': 'ASX 200 Slides 0.43% to 8,793 as Nick Scali Profit Warning Flags a Consumer Slowdown; Mining and Energy Stocks Sold Off',
'{{ECON_1_SUMMARY}}': "Market Index's Thursday wrap says the furniture retailer's downgrade hit consumer stocks, with the Aussie dollar around 70 US cents. A weak jobs print also featured. A cooling consumer is worth watching if your customers are households or retailers.",
'{{ECON_1_URL}}': 'https://www.marketindex.com.au/news/evening-wrap-asx-200-slides-as-nck-profit-warning-flags-major-consumer',
'{{ECON_2_FLAG}}': '⛽ FUEL · OIL',
'{{ECON_2_HEADLINE}}': 'Oil Hovers Near Five-Month Highs Around US$110 a Barrel After Deadly Attacks on a Saudi Oil Field and Airport',
'{{ECON_2_SUMMARY}}': "ABC's 22 October markets blog has oil near five-month highs. Government figures put capital-city retail diesel around $2.79 a litre as of 14 October, and the ACCC said diesel eased slightly in its 16 October update. Diesel lags crude, so verify current bowser prices before quoting.",
'{{TECH_1_FLAG}}': '🤖 AI · ASSISTANTS',
'{{TECH_1_HEADLINE}}': "Anthropic Launches Claude Duet, a Proactive AI Agent for Professionals and Small Business Owners",
'{{TECH_1_SUMMARY}}': "SiliconANGLE, 22 October: a research-preview standalone app for Pro and Max subscribers that sends a short morning brief of the most important items across connected apps and flags only messages needing attention. Handy for a busy owner on the tools, but connect only what you need and keep banking out.",
'{{TECH_1_URL}}': 'https://siliconangle.com/2026/10/22/anthropic-introduces-claude-duet-a-proactive-ai-agent-for-professionals/',
'{{TECH_2_FLAG}}': '⚖️ AI · PROFESSIONAL SERVICES',
'{{TECH_2_HEADLINE}}': "Legal AI Startup Legora Raises US$550M at an US$8.8B Valuation",
'{{TECH_2_SUMMARY}}': "SiliconANGLE, 21 October. Heavy investment is pouring into AI for contracts, compliance and document review. For a small trades business, contract and tender review is a likely next practical use as these tools get cheaper.",
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS · WAREHOUSE',
'{{ROBOT_1_HEADLINE}}': "Signode Expands Its Autonomous Mobile Robot Line for End-of-Line and Warehouse Automation",
'{{ROBOT_1_SUMMARY}}': "Robotics Tomorrow, 22 October: the packaging company's expanded AMR range is aimed at moving palletised loads through manufacturing and warehouse sites. Not humanoids, but practical wheeled automation like this is where factory robotics is spreading fastest.",
'{{ROBOT_1_URL}}': 'https://www.roboticstomorrow.com/news/2026/10/22/signode-expands-autonomous-mobile-robot-portfolio-to-advance-end-of-line-and-warehouse-automation/27289',
'{{AUS_1_HEADLINE}}': "Helen Haines Remains in Critical Condition Three Days After the Wangaratta Car Attack",
'{{AUS_1_SUMMARY}}': "ABC, 22 October: the Indi MP, 65, lost both legs and remains critical, with her husband calling her a fighter. Accused driver Brendan Nugent, 43, has appeared in court on five charges. More than a dozen Victorian politicians told the ABC they have reported threats to MPs, families and volunteers.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-22/helen-haines-three-days-since-attack/107297946',
'{{AUS_2_HEADLINE}}': "Nick Scali Profit Warning Rattles Consumer Stocks as ASX Closes Lower",
'{{AUS_2_SUMMARY}}': "The furniture retailer's downgrade, reported in Thursday's market wraps, led a sell-off in consumer discretionary names. It adds to signs of household spending pulling back as interest rates and fuel costs bite.",
'{{VIC_1_HEADLINE}}': "Victorian MPs Call for an Election Campaign Security Boost After the Haines Attack",
'{{VIC_1_SUMMARY}}': "ABC, 21 October: Premier Ben Carroll will meet the electoral commissioner on security ahead of the 28 November state election. No similar offence to the federal one exists for state MPs, and some politicians want one.",
'{{SCI_1_FLAG}}': '☄️ GEOLOGY',
'{{SCI_1_HEADLINE}}': "Mystery of the Silverpit Crater Solved: A 160-Metre Object Struck the North Sea Seabed",
'{{SCI_1_SUMMARY}}': "ScienceDaily, 21 October: scientists have confirmed the crater, buried about 700 metres beneath the North Sea seabed, was created by an impact, settling a long-running debate over whether it was an impact or a salt-related collapse.",
'{{INSIGHT_TITLE}}': 'Start With a Morning Brief: Let AI Triage Your Inbox Before You Hit the Tools',
'{{INSIGHT_BODY}}': "New proactive assistants like Anthropic's Claude Duet are aimed at owners who spend all day on site and come home to a flooded inbox. The idea is a short morning summary of what matters across your email and calendar, with only the messages that need you flagged. For a small trades business the easy win is quote requests, supplier confirmations and overdue invoices not slipping through. Start read-only: connect email and calendar, not banking or accounting, and treat the brief as a prompt to check the original message, especially before you commit to prices or dates.",
'{{FACT_1}}': "The Silverpit Crater lies about 700 metres beneath the North Sea seabed and has now been confirmed as an impact crater from an object roughly 160 metres wide.",
'{{FACT_2}}': "Lake Hillier on Middle Island off Western Australia is naturally bubblegum pink and stays pink even when the water is scooped into a container.",
'{{FACT_3}}': "Australia is about 4,000 kilometres wide east to west, wider than the Moon's 3,474-kilometre diameter.",
'{{JOKE_SETUP}}': "Why did the chippie bring a pencil to the weekend barbecue?",
'{{JOKE_PUNCHLINE}}': '"To mark the occasion."',
'{{CLOSING_QUOTE}}': '"Success is neither magical nor mysterious. Success is the natural consequence of consistently applying the basic fundamentals."',
'{{CLOSING_ATTR}}': '— Jim Rohn',
'{{CLOSING_MESSAGE}}': "It's Friday, and the last warm, mostly dry day before a cool, wet change on Saturday. Get any outdoor work finished and covered today, and use the showery weekend to catch up on quotes and invoices.",
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
