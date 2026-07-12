#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 13 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 13 Jul (BOM)
    "{{WEATHER_1}}": "MON 13 · 🌧️ Showers, windy NW'ly · 10–14°C",
    "{{WEATHER_2}}": "TUE 14 · 🌦️ Showers, breezy · 9–13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 15 · ⛅ Partly cloudy, isolated shower · 7–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "THU 16 · ❄️ Patchy frost, mostly dry · 6–15°C",
    "{{WEATHER_5}}": "FRI 17 · ❄️ Patchy frost, mostly dry · 6–13°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERY START TO THE WEEK · FROST RETURNS THU–FRI MORNINGS",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷🇶🇦 IRAN · GULF · MISSILE STRIKES ESCALATE ACROSS FOUR NATIONS",
    "{{WORLD_1_HEADLINE}}": "Iran Launches Missile and Drone Attacks on Qatar, UAE, Bahrain and Kuwait After Fresh US Strikes",
    "{{WORLD_1_SUMMARY}}": "Iran unleashed simultaneous missile and drone attacks across the Gulf early Sunday, targeting the US Al-Udeid airbase in Qatar along with sites in the UAE, Bahrain and Kuwait, hours after Washington carried out a third round of strikes on Iranian targets over the Strait of Hormuz shipping attacks. Qatari air defences intercepted multiple ballistic missiles over Doha, while the UAE and Bahrain both activated air defence systems — a sharp escalation that puts the region's fragile ceasefire efforts back to square one heading into the new week.",
    "{{WORLD_1_URL}}": "https://www.euronews.com/2026/07/12/iran-launches-attacks-on-qatar-uae-bahrain-kuwait-following-us-strikes",

    "{{WORLD_2_FLAG}}": "🇶🇦 QATAR · TRIBUTE · TRANSFORMATIVE FORMER RULER DIES",
    "{{WORLD_2_HEADLINE}}": "Qatar's Former Emir Sheikh Hamad bin Khalifa Al Thani Dies at 74",
    "{{WORLD_2_SUMMARY}}": "Sheikh Hamad, who ruled Qatar from 1995 to 2013 and founded Al Jazeera, has died, with the government declaring four days of national mourning. He's widely credited with transforming Qatar from a small Gulf state into a major diplomatic and economic power — a legacy looming large as the region faces one of its most dangerous weeks of the year.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/7/12/former-emir-of-qatar-sheikh-hamad-bin-khalifa-al-thani-dies-at-74",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · ACCC · BOWSER PRICES CLIMBING AGAIN",
    "{{ECON_1_HEADLINE}}": "ACCC's Latest Weekly Report Confirms Petrol and Diesel Keep Climbing as Excise Relief Halves",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly fuel monitoring update shows capital city petrol and diesel prices continuing to rise since the fuel excise cut was halved from 32c to 16c a litre on 1 July, with the discount disappearing altogether from 2 August. With Middle East tensions also pushing crude prices up, it's worth locking a fuel surcharge into quotes now rather than absorbing it on jobs already priced.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🏦 RBA WATCH · CASH RATE HELD AT 4.35% · FUEL-DRIVEN INFLATION FLAGGED",
    "{{ECON_2_HEADLINE}}": "RBA Holds Cash Rate at 4.35%, Warns Higher Fuel Prices Are Feeding Through to Inflation",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank held the cash rate steady this month after three rises since the start of the year, but flagged that higher oil prices — driven by the Middle East conflict — are adding directly to inflation and starting to show up in the price of other goods and services. For anyone with equipment finance or a variable business loan, it's a signal that relief on borrowing costs is still a way off.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🖥️ MICROSOFT · TEAMS · AI OPT-OUT ADDED AFTER BACKLASH",
    "{{TECH_1_HEADLINE}}": "Microsoft Lets Teams Meeting Hosts Switch AI Features Off Live, After User Backlash",
    "{{TECH_1_SUMMARY}}": "Microsoft has added a toggle letting meeting organisers turn Copilot's AI note-taking and summary features on or off mid-meeting, responding to complaints about aggressive default rollouts. Meanwhile Google Ads cost-per-click has jumped 15% year-on-year, squeezing small business marketing budgets and making organic channels — reviews, referrals, local search — worth doubling down on.",
    "{{TECH_1_URL}}": "https://www.forbes.com/sites/quickerbettertech/2026/07/12/small-business-technology-news-roundup-microsoft-makes-a-major-ai-u-turn/",

    "{{TECH_2_FLAG}}": "⚖️ AI INDUSTRY · APPLE V OPENAI · TRADE SECRETS LAWSUIT",
    "{{TECH_2_HEADLINE}}": "Apple Sues OpenAI Over Alleged Trade Secret Theft and Staff Poaching",
    "{{TECH_2_SUMMARY}}": "Apple has filed suit in a California federal court alleging OpenAI ran a coordinated campaign to poach hardware and silicon staff and lift confidential technology — a reminder that the AI vendor landscape is more litigious and less settled than it looks from the outside, worth keeping in mind before locking a business into any single AI platform long-term.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 ROBOTICS · SIMULATION · TRAINING ROBOTS BEFORE THEY HIT THE FLOOR",
    "{{ROBOT_1_HEADLINE}}": "Robotics Teams Are Using \"Virtual Gyms\" to Train Warehouse Robots Before Deployment",
    "{{ROBOT_1_SUMMARY}}": "Robotics engineers, including in a Toyota Material Handling Europe case study, are increasingly using high-fidelity simulation environments — \"virtual gyms\" — to train forklift and warehouse robots' perception and decision-making before they ever touch a real floor, cutting the costly, risky trial-and-error that used to happen live. It's the same logic worth applying to any new piece of automation or software before it goes anywhere near a real job.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/why-robotics-teams-need-virtual-gyms-before-deployment/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Union Blames Telstra's Offshoring Push for Nationwide Network Outage",
    "{{AUS_1_SUMMARY}}": "The Communications Workers Union says last week's Telstra outage — which knocked out mobile, data and some Triple Zero calls nationally and halted V/Line's entire regional train network — is a direct result of the telco shifting hundreds of technical roles to Indian firm Infosys since February. Telstra maintains the cause was a software fault in its network timing servers unrelated to workforce changes, but the stoush is a live reminder to have a backup plan for whenever your main carrier goes down.",
    "{{AUS_1_URL}}": "https://www.theaustraliatoday.com.au/utterly-shameful-union-blames-telstra-workforce-cuts-for-nationwide-outage/",

    "{{AUS_2_HEADLINE}}": "NAB Survey: Business Confidence and Conditions Fall Further in Q2 as Middle East and Policy Uncertainty Bite",
    "{{AUS_2_SUMMARY}}": "NAB's latest quarterly business survey shows both conditions and confidence weakening further in Q2, with more businesses citing geopolitical uncertainty and federal policy as headwinds, and wage costs still the single biggest issue firms report. A reminder that even with a solid job book, plenty of similar-sized operators are feeling the same cost and confidence squeeze right now.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Logs Its Coldest Week of 2026 as a Wetter Change Arrives",
    "{{VIC_1_SUMMARY}}": "Melbourne recorded mornings as low as 3.2°C last week, with fog refusing to lift until early afternoon on some days — the city's coldest stretch so far in 2026 — before the cold front now moving through brings the shower and wind risk we're tracking today and tomorrow. Worth timing any outdoor coating work around the drier, frostier stretch forecast from Thursday.",

    # Science
    "{{SCI_1_FLAG}}": "🕳️ PHYSICS · BLACK HOLES · 50-YEAR-OLD THEORY DEMONSTRATED IN THE LAB",
    "{{SCI_1_HEADLINE}}": "Physicists Recreate Black-Hole Energy Extraction in a Tabletop Lab Experiment",
    "{{SCI_1_SUMMARY}}": "Researchers at CUNY's Advanced Science Research Center built a stationary device using synthetic ultrafast rotation to physically demonstrate the Penrose process — a 50-year-old thought experiment for pulling energy out of a spinning black hole — turning pure theory into a lab result for the first time, with possible spin-off uses in optics and quantum communications.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Get Ahead of the Silica Dust Crackdown",
    "{{INSIGHT_BODY}}": "WorkSafe Victoria is tightening its approach to respirable crystalline silica — while the legal exposure standard sits at 0.05 mg/m³, inspectors are increasingly benchmarking against the stricter 0.02 mg/m³ target as Victoria prepares to formally adopt the new national Workplace Exposure Standard from December 2026. For a business built on abrasive blasting, that means health monitoring records, baseline assessments and re-testing schedules for every exposed worker need to be watertight well before the transition lands. AI-assisted document tools can quietly do the heavy lifting here — auto-organising monitoring results, flagging workers due for re-testing, and building a clean, timestamped compliance trail — so if WorkSafe comes knocking, the evidence is already assembled rather than scrambled together after the fact.",

    # Fun Facts
    "{{FACT_1}}": "Between April 2025 and March 2026, the international Ocean Census initiative identified 1,121 new marine species — a 54% jump on the previous year — across 13 expeditions in 85 countries. Strikingly, 728 of those were found not on a new dive but by researchers finally identifying specimens that had been sitting unexamined in museum archives for years.",

    "{{FACT_2}}": "The oldest known stone tools, unearthed at the Lomekwi 3 site in Kenya, date back 3.3 million years — older than the genus Homo itself, meaning some pre-human ancestor was deliberately shaping tools long before our own species existed.",

    "{{FACT_3}}": "The teabag is usually credited to New York tea merchant Thomas Sullivan, who around 1908 mailed loose-tea samples in small silk pouches that customers started dunking straight into the pot. But two women, Roberta Lawson and Mary McLaren, had already patented a near-identical tea leaf holder back in 1901 — they just never got it into mass production before Sullivan's version took the credit.",

    # Joke
    "{{JOKE_SETUP}}": "How can you tell if you've found a good tax accountant?",
    "{{JOKE_PUNCHLINE}}": "They've got a loophole named after them.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"You don't have to be great to start, but you have to start to be great.\"",
    "{{CLOSING_ATTR}}": "— Zig Ziglar",
    "{{CLOSING_MESSAGE}}": "It's a wet, blustery start to the week in Carrum Downs with showers moving through today and tomorrow, so it's more of an indoor prep and paperwork day than one for outdoor coating work — school holidays wrap up today too, with kids back in the classroom this morning. Keep an eye on the news out of the Gulf as the week unfolds, and if you need a distraction tonight, Spain and France face off in Tuesday's World Cup semi-final.",
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
