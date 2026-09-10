#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 11 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 11 Sep (BOM Melbourne-area forecast)
    "{{WEATHER_1}}": "FRI 11 SEP · 🌫️ Morning fog then sunny, light winds · 8–17°C",
    "{{WEATHER_2}}": "SAT 12 SEP · 🌤️ Morning fog then mostly sunny, winds turning northerly · 7–18°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SUN 13 SEP · ⛅ Mostly sunny, slight shower chance late, northerly 20–30km/h · 10–22°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 14 SEP · ☀️ Mostly sunny, light winds turning northerly 15–20km/h · 12–24°C",
    "{{WEATHER_5}}": "TUE 15 SEP · 🌦️ Cooler change, shower or two, northerly ahead of front · 13–19°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — fog clears to fine, sunny days Friday and Saturday, then a warm northerly build lifts the top into the low-to-mid 20s by Sunday and Monday ahead of a cooler, shower-bearing change forecast for Tuesday.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 VIENNA · IAEA BOARD REFERS IRAN TO UN SECURITY COUNCIL FOR FIRST TIME IN 20 YEARS",
    "{{WORLD_1_HEADLINE}}": "UN Nuclear Watchdog Refers Iran to the Security Council for the First Time in Two Decades",
    "{{WORLD_1_SUMMARY}}": "The IAEA's 35-member board voted 23-3 on Wednesday to report Iran to the UN Security Council over its refusal to let inspectors access nuclear sites hit in last year's Israeli-US strikes, in a resolution put forward by the US, UK, France and Germany. China, Russia and Niger opposed the move and eight countries abstained; Iran's allies retain a Security Council veto so sanctions are unlikely, but it marks the most serious diplomatic escalation since the 12-day war.",
    "{{WORLD_1_URL}}": "https://www.washingtonpost.com/world/2026/09/09/un-iran-atomic-watchdog-security-council/ca13d9b0-ac6b-11f1-b498-8697f35a6743_story.html",

    "{{WORLD_2_FLAG}}": "🇧🇩 COX'S BAZAR · POLICE BUST MAJOR CHINESE-RUN CYBER FRAUD NETWORK",
    "{{WORLD_2_HEADLINE}}": "Bangladesh Police Raid Hotel Cyber-Fraud Compound, Arrest Six Chinese and Taiwanese Nationals",
    "{{WORLD_2_SUMMARY}}": "A raid on a Cox's Bazar hotel uncovered what investigators believe is one of Bangladesh's largest organised cyber-fraud operations, seizing close to 2,000 iPhones and a facility built to run hundreds of fake online identities. Six suspects were charged and jailed, but police believe 250 to 300 more Chinese and Taiwanese nationals tied to the network remain at large, underscoring how Southeast Asia's scam-compound crisis is spreading into new countries.",
    "{{WORLD_2_URL}}": "https://ianslive.in/arrest-of-chinese-taiwanese-nationals-exposes-major-transnational-cybercrime-networks-in-bangladesh--20260910200752",

    # Economics
    "{{ECON_1_FLAG}}": "📈 INTEREST RATES · MARKETS NOW PRICE AN 80% CHANCE OF A SEPTEMBER RATE HIKE",
    "{{ECON_1_HEADLINE}}": "Traders Push Odds of a September 29 RBA Rate Rise to Near 80% as Inflation Runs Hot",
    "{{ECON_1_SUMMARY}}": "Futures markets are now pricing an 80% chance the RBA lifts the cash rate 25 basis points to 4.6% at its 29 September meeting — up from just 17% before July's hotter-than-expected inflation print, after June-quarter GDP growth also beat forecasts. NAB was first to call the hike outright; a rise would add roughly $76 a month to repayments on a $600,000 variable loan, and typically flows through fast to business overdraft and equipment-finance rates too.",
    "{{ECON_1_URL}}": "https://ts2.tech/en/rba-rate-hike-odds-near-80-the-asx-200-barely-blinked/",

    "{{ECON_2_FLAG}}": "⛽ FUEL · BRENT TOPS $100 A BARREL FOR THE FIRST TIME SINCE MAY",
    "{{ECON_2_HEADLINE}}": "Brent Crude Breaks Back Above $100 a Barrel on Middle East Tanker Strikes, Melbourne Pump Prices Stay Elevated",
    "{{ECON_2_SUMMARY}}": "Brent closed above US$100 a barrel on Wednesday for the first time since May after the latest round of tanker strikes in the Gulf of Oman, and Melbourne unleaded is still averaging around 205c/L with diesel from about 237c/L at the cheapest sites. With business conditions already negative for the first time since the pandemic, fuel remains the single biggest cost pressure small operators are naming survey after survey.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📱 CONSUMER TECH · APPLE'S FIRST 2-NANOMETRE IPHONE CHIP LANDS",
    "{{TECH_1_HEADLINE}}": "Apple Unveils iPhone 18 Pro Lineup With Its First 2-Nanometre Chip, Promising Big Speed and Battery Gains",
    "{{TECH_1_SUMMARY}}": "Apple's Wednesday keynote introduced the iPhone 18 Pro, Pro Max and a new foldable model, all built around the A20 Pro — Apple's first smartphone chip made on a 2-nanometre process, with a 32-core Neural Engine, up to 40% faster graphics and roughly 20% faster CPU performance than last year's chip. For a business running everything from quoting apps to job photos off a phone all day, it's a genuine on-device AI and battery-life upgrade, not just a spec bump.",
    "{{TECH_1_URL}}": "https://www.tomshardware.com/pc-components/cpus/apple-a20-pro-powers-iphone-18-pro-the-companys-first-2-nanometer-smartphone-chip",

    "{{TECH_2_FLAG}}": "📊 SMB MARKETING · GOOGLE ADS ADDS PLAIN-ENGLISH AI DASHBOARDS",
    "{{TECH_2_HEADLINE}}": "Google Ads Rolls Out AI Dashboards That Build a Performance Report From a Typed Question",
    "{{TECH_2_SUMMARY}}": "Google Ads has begun rolling out AI Dashboards that turn a plain-English request — 'which campaigns drove calls this month' — straight into a visual report, alongside a new Local Customer Optimisation toggle aimed at nearby, in-market customers. For an owner managing their own account between jobs, it trims a fiddly reporting task down to one typed sentence.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 WAREHOUSE AUTOMATION · HAI ROBOTICS TO DEPLOY 1,500 RACK-CLIMBING ROBOTS IN EUROPE",
    "{{ROBOT_1_HEADLINE}}": "Hai Robotics Wins Deal for the World's Largest Rack-Climbing Warehouse Robot Deployment",
    "{{ROBOT_1_SUMMARY}}": "Hai Robotics will install more than 1,500 of its HaiPick Climb robots at a European fashion retailer's new fulfilment centre, handling over 24,000 totes an hour — the largest deployment of rack-climbing warehouse robots built to date. It's another sign that the robotics investment happening in big-box logistics right now is aimed squarely at the same throughput and labour-cost problems any warehouse or yard operation would recognise.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/09/09/hai-robotics-to-install-1500-rack-climbing-robots-at-european-fulfillment-center/104691/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Greens Split Over Forest Carbon Credits as Senate Passes Scheme Tied to Koala National Park",
    "{{AUS_1_SUMMARY}}": "Three Greens senators crossed the floor to back a Coalition motion against letting states earn carbon credits for protecting native forest instead of logging it, defying former leaders Bob Brown and Christine Milne — but the government held the numbers 34-27 with support from seven other Greens and key crossbenchers. The scheme underpins funding for the proposed 476,000-hectare Great Koala National Park on the NSW mid-north coast.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-10/federal-politics-live-blog-grants/107135214",

    "{{AUS_2_HEADLINE}}": "One Nation Cartoon Calling Liberal MP Andrew Hastie a 'Traitor' Draws Cross-Party Backlash",
    "{{AUS_2_SUMMARY}}": "Independent senator Jacqui Lambie joined Coalition MPs Angus Taylor and Matt Canavan in calling on Pauline Hanson to pull down a One Nation cartoon video branding Liberal frontbencher and veteran Andrew Hastie a 'traitor', in an unusually broad show of cross-party solidarity.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Australia's First-Ever NFL Regular-Season Game Kicks Off at the MCG This Morning",
    "{{VIC_1_SUMMARY}}": "The San Francisco 49ers face the LA Rams at the MCG at 10:35am today in Australia's first regular-season NFL game, after the 49ers' 200-strong travelling party landed on a 15-hour charter flight and spent the week acclimatising in Melbourne. A sold-out crowd is expected, so inner-city traffic and public transport around the ground will be heavier than usual through the morning.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 MATERIALS SCIENCE · YEAST AND MARTIAN DUST COULD ONE DAY BUILD HOUSES ON MARS",
    "{{SCI_1_HEADLINE}}": "Scientists Develop a Yeast-and-Gelatin 'Living Concrete' Recipe for 3D-Printing Houses on Mars",
    "{{SCI_1_SUMMARY}}": "Researchers have built a Mars-ready building material by combining crushed Martian-analogue rock with gelatin and engineered yeast coated in mussel-inspired sticky proteins, extruding it through a 3D-printer nozzle into sub-zero, low-pressure conditions where it sets almost instantly. Once dried, the material is as strong as low-grade concrete, and — unlike concrete — it can be broken down and reprinted, giving future astronauts a renewable building supply they can keep reusing rather than shipping fresh material from Earth each time.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Rates Are Poised to Rise Again — How AI Can Help You Build a Cost-Escalation Clause Into Every Quote",
    "{{INSIGHT_BODY}}": "With markets now pricing an 80% chance of a rate rise this month and fuel still climbing, a fixed-price quote signed today can be underwater by the time you're actually on site in six weeks — yet most small operators still write quotes the same way they did when costs were flat. A general-purpose AI tool can turn your standard quote template into one with a clear, plain-English cost-escalation clause tied to a public index — fuel, materials or the RBA cash rate itself — and even draft the client-facing explanation so it doesn't read as a red flag. It's a five-minute fix that protects margin on every job that runs long, without you having to chase a variation later and risk the relationship over it.",

    # Fun facts
    "{{FACT_1}}": "The @ symbol in every email address predates computers by centuries — it shows up in a Bulgarian monk's 1345 manuscript as shorthand for the Latin word 'at', and centuries later Ray Tomlinson picked it for the first-ever email address in 1971 mainly because it was one of the few keys on his keyboard that never appeared in a person's name.",
    "{{FACT_2}}": "The Mars building material researchers unveiled this week hardens almost instantly because it's extruded into an environment so cold and low-pressure that the water inside skips straight from ice to vapour — a process called sublimation — without ever passing through a liquid stage.",
    "{{FACT_3}}": "Geologists have a nickname for the billion-odd years between 1.8 billion and 800 million years ago: the 'Boring Billion' — a stretch when Earth's climate, ocean chemistry and evolutionary pace stayed so eerily stable that scientists still can't fully explain why complex life seemed to hit pause for so long.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the termite inspector's small business partner ask him to look over the books as well as the roof?",
    "{{JOKE_PUNCHLINE}}": "He'd already proven he could spot exactly what was quietly eating into the numbers.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"If I have seen further, it is by standing on the shoulders of giants.\"",
    "{{CLOSING_ATTR}}": "— Isaac Newton",
    "{{CLOSING_MESSAGE}}": "It's a big Friday for Melbourne — kick-off for Australia's first-ever NFL regular season game is 10:35am at the MCG, so expect heavier traffic and transport around the city through the morning if you've got jobs that way. Weather-wise, this morning's fog should clear to a fine, sunny afternoon around Carrum Downs, and Friday and Saturday look like the pick of the week for outdoor work before it warms up and turns showery again by Tuesday. Worth keeping half an eye on the bowser and the cash rate too — Brent's back above US$100 a barrel and markets are now pricing an 80% chance of a rate rise this month, so it's a good week to get ahead on quoting rather than behind.",
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
