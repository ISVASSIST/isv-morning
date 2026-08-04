#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 05 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 05 Aug (BOM)
    "{{WEATHER_1}}": "WED 05 · 🌧️ Showers, most likely SE suburbs · 7–15°C",
    "{{WEATHER_2}}": "THU 06 · 🌦️ Shower or two, easing chance · 7–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 07 · ⛅ Partly cloudy, drier stretch begins · 7–15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 08 · ⛅ Shower or two later in the day · 8–17°C",
    "{{WEATHER_5}}": "SUN 09 · 🌧️ Windy, wettest day of the run · 9–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings current for Melbourne / Carrum Downs",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷🇶🇦 IRAN · QATARI-MEDIATED DRAFT DEAL REPORTEDLY 'IN VERY PROGRESSIVE STAGES' TO END THE US-IRAN WAR",
    "{{WORLD_1_HEADLINE}}": "A Qatari-Mediated Draft Deal Is Reportedly 'In Very Progressive Stages' to End the US-Iran War",
    "{{WORLD_1_SUMMARY}}": "Draft agreements are said to be circulating via Qatari mediation aimed at ending the 2026 US-Iran conflict, with Trump reportedly speaking directly with Qatar's emir, though no formal US-Iran talks are yet confirmed. Iran is separately working to establish a controlled safe shipping corridor through the Strait of Hormuz — worth watching given how directly that strait affects global oil and freight costs.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/08/04/world/live-news/iran-war-trump",

    "{{WORLD_2_FLAG}}": "🇷🇺🇺🇦 UKRAINE · NINE KILLED AS RUSSIA AND UKRAINE TRADE ESCALATING LONG-RANGE STRIKES",
    "{{WORLD_2_HEADLINE}}": "Nine Killed as Russia and Ukraine Trade Escalating Long-Range Missile and Drone Strikes",
    "{{WORLD_2_SUMMARY}}": "At least nine people died — five in Russia, four in Ukraine — in a fresh round of long-range strikes, including a Ukrainian drone hit on a warehouse in the Moscow region. There's no sign of a resolution, and the escalation keeps regional energy and shipping risk elevated for anyone watching fuel costs.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/8/4/nine-killed-in-escalating-long-range-strikes-between-russia-and-ukraine",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺⛽ FUEL · TEMPORARY EXCISE CUT HAS ENDED, PUMP PRICES ALREADY CLIMBING",
    "{{ECON_1_HEADLINE}}": "The Temporary Fuel Excise Cut Has Ended, and Pump Prices Are Already Climbing",
    "{{ECON_1_SUMMARY}}": "The government's 16-cent-a-litre fuel excise relief expired on 2 August, with the excise back to 53.7 cents a litre plus indexation from 3 August — the ACCC says it's watching retailers closely for any extra padding on top of the legitimate rise. Victoria's still the cheapest state at the pump, but worth comparing a couple of servos near your sites this week rather than assuming yesterday's cheapest is still today's.",
    "{{ECON_1_URL}}": "https://theconversation.com/australias-fuel-discount-is-ending-what-does-this-mean-for-petrol-prices-288279",

    "{{ECON_2_FLAG}}": "🇦🇺📋 TAX · SMALL BUSINESS LOBBY WANTS LOSS CARRY-BACK RELIEF EXTENDED TO TRUSTS AND SOLE TRADERS",
    "{{ECON_2_HEADLINE}}": "Small Business Lobby COSBOA Wants Loss Carry-Back Tax Relief Extended to Trusts and Sole Traders",
    "{{ECON_2_SUMMARY}}": "COSBOA has told a Senate committee the government's proposed loss carry-back reform shouldn't be limited to companies — it should cover trusts, partnerships and sole traders too, the structures most small trades businesses actually use. Worth watching if you don't operate as a company, since as drafted you'd miss a tax break your incorporated competitors could claim.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 OPENAI · PASSES 1 BILLION ACTIVE USERS, CUTS ITS CHEAPEST MODEL'S PRICE BY 80%",
    "{{TECH_1_HEADLINE}}": "OpenAI Passes 1 Billion Active Users and Cuts Its Cheapest AI Model's Price by 80%",
    "{{TECH_1_SUMMARY}}": "OpenAI says its models now serve more than a billion active users and over 2 million businesses, and it's just cut API pricing on its cheapest model by 80% and its mid-tier model by 20%. The trend keeps holding — the AI tools worth trialling in your business keep getting cheaper to run, not more expensive.",
    "{{TECH_1_URL}}": "https://www.ghacks.net/2026/08/04/openai-reaches-one-billion-active-users-and-cuts-gpt-5-6-luna-and-terra-prices-by-up-to-80/",

    "{{TECH_2_FLAG}}": "🌐 AI TRANSLATION · TOOLS ARE NOW HIGHLY FLUENT, BUT RESEARCHERS WARN TONE STILL GETS LOST",
    "{{TECH_2_HEADLINE}}": "AI Translation Tools Are Getting Remarkably Fluent — But Researchers Warn Tone and Nuance Still Slip Through",
    "{{TECH_2_SUMMARY}}": "University of Essex researchers note today's AI speech and text translators are now highly accurate on the words themselves, but still miss hesitation, tone and ambiguity that carry real meaning in a conversation. Handy to keep in mind if you're using a translation app with a client or crew member on site rather than trusting it word for word.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳🦾 ROBOTICS · HUMANOID ROBOT MAKER UNITREE OPENS BOOK-BUILDING TODAY FOR ITS SHANGHAI IPO",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robot Maker Unitree Opens Book-Building Today for a Shanghai IPO Valuing It at ¥42 Billion",
    "{{ROBOT_1_SUMMARY}}": "Unitree — the world's top-shipping humanoid robot maker in 2025 — opened institutional book-building today for its Shanghai STAR Market listing, aiming to raise about ¥4.2 billion at a ¥42 billion valuation floor, with public subscription due 10 August. It's a sign the humanoid robotics sector is shifting from prototype hype into real, capital-market-priced mass production.",
    "{{ROBOT_1_URL}}": "https://www.yuantalks.com/unitree-robotics-launches-star-market-ipo-bookbuilding-on-august-5/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Royal Commission Into Antisemitism Hears Evidence on Sydney Opera House and NSW Parliament Protests",
    "{{AUS_1_SUMMARY}}": "The Royal Commission on Antisemitism and Social Cohesion held a Sydney hearing block examining policing and conduct at protests outside the Opera House and NSW Parliament, part of its wider inquiry following the Bondi Beach terror attack.",
    "{{AUS_1_URL}}": "https://asc.royalcommission.gov.au/hearings",

    "{{AUS_2_HEADLINE}}": "Household Spending Beat Forecasts in June, Rising 0.8% on Stronger Car Sales and Recreation",
    "{{AUS_2_SUMMARY}}": "The ABS Monthly Household Spending Indicator showed spending up 0.8% in June, well ahead of the 0.2% expected, driven by new vehicle sales and recreation — a sign the economy isn't slowing as fast as hoped, with the RBA's next rate call due 10–11 August.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "New Premier Ben Carroll Unveils His Cabinet and Flags a Royal Commission Into the Construction Sector",
    "{{VIC_1_SUMMARY}}": "Following Jacinta Allan's resignation, new Premier Ben Carroll has named a reshuffled Cabinet — including a new Minister for AI and Digital Economy — and says his first act will be calling a royal commission into the construction sector, complete with a special prosecutor, to examine cost blowouts and dodgy practices industry-wide.",

    # Science
    "{{SCI_1_FLAG}}": "⚡ ENERGY · GERMAN ENGINEERS RUN A COMPRESSORLESS HYDROGEN TURBINE ON CONTROLLED EXPLOSIONS",
    "{{SCI_1_HEADLINE}}": "German Engineers Just Ran a Hydrogen Turbine With No Compressor at All — Using Controlled Detonations Instead",
    "{{SCI_1_SUMMARY}}": "Researchers at Germany's Karlsruhe Institute of Technology generated electricity for a record 303 seconds from a hydrogen turbine that skips the compressor entirely — the part that normally eats about half a gas turbine's power — using detonation waves travelling faster than sound to do the compressing instead. A neat reminder that some of the biggest efficiency gains in industrial equipment still come from removing a part, not adding one.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Victoria Just Called a Construction Royal Commission — Is Your Paper Trail Ready for More Scrutiny?",
    "{{INSIGHT_BODY}}": "New Premier Ben Carroll's first act was to call a royal commission into the construction sector, with a special prosecutor to examine cost blowouts and dodgy practices industry-wide. For a small subcontractor like Industrial Services Victoria, that kind of scrutiny usually rolls downhill — head contractors start demanding cleaner paper trails, more detailed sign-offs, and better evidence that work was done to spec and on time. An AI tool that logs site photos, timestamps and job notes as you go turns what used to be a scramble through old text messages into a ready-made file if a job is ever questioned — cheap insurance against a much bigger headache.",

    # Fun facts
    "{{FACT_1}}": "The Bluetooth logo isn't a random symbol — it's a bind rune combining the initials of Harald 'Bluetooth' Gormsson, the 10th-century Danish king who united Denmark and Norway, written in the Younger Futhark runic alphabet. Engineers named the wireless standard after him because, like the king, it was meant to unite different systems under one connection.",
    "{{FACT_2}}": "The rotary lawnmower was invented in a suburban Sydney garden shed in 1952, when Mervyn Victor Richardson built the first Victa mower using a war-surplus aircraft fuel tank as the cutting deck. It went on to become the world's biggest-selling lawnmower brand, exported to more than 30 countries.",
    "{{FACT_3}}": "The Chiko Roll was invented in Bendigo, Victoria, in 1951 by Frank McEncroe, who wanted a footy-crowd snack that could be eaten one-handed with no plate or cutlery. It was originally called the 'Chicken Roll' despite containing no chicken at all, and was renamed Chiko Roll before it hit the shelves.",

    # Joke
    "{{JOKE_SETUP}}": "A skip bin hire operator was asked how he always knew exactly which size bin a job needed before he'd even seen the site.",
    "{{JOKE_PUNCHLINE}}": "He said years on the job taught him one rule — customers always underestimate by exactly one size, every time.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Don't watch the clock; do what it does. Keep going.\"",
    "{{CLOSING_ATTR}}": "— Sam Levenson",
    "{{CLOSING_MESSAGE}}": "It's a showery start to Wednesday in Carrum Downs, with the wettest stretch easing off by Friday's partly cloudy break before rain returns for the weekend. The fuel excise increase is now fully baked into prices at the bowser, so budget for it on your next fill — and if you're running anything other than a company structure, keep an eye on the loss carry-back tax debate in Canberra this week, since it could decide whether you get the same relief your incorporated competitors do.",
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
