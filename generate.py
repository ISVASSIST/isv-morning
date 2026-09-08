#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 09 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 9 Sep (BOM Melbourne forecast issued 4:20pm Tue 8 Sep)
    "{{WEATHER_1}}": "WED 9 SEP · ⛅ Partly cloudy, light winds · 8–16°C",
    "{{WEATHER_2}}": "THU 10 SEP · 🌧️ Cloudy, high chance of showers (higher near the Dandenongs) · 9–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 11 SEP · ⛅ Partly cloudy, showers more likely later, northerly change · 9–17°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 12 SEP · 🌤️ Mostly sunny, medium chance of a shower, northerly 15–25km/h · 10–19°C",
    "{{WEATHER_5}}": "SUN 13 SEP · 🌧️ Cloudy, high chance of showers, wind swinging SW · 10–15°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Melbourne — today is the calmest, driest day of the run, with showers returning Thursday and building into a damp weekend.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 STRAIT OF HORMUZ · IRAN CLAIMS DOWNED US DRONE, CAPTURED NAVY SUBMERSIBLE",
    "{{WORLD_1_HEADLINE}}": "Iran Says It Shot Down a US MQ-1 Drone and Captured a US Navy Underwater Vehicle Near the Strait of Hormuz",
    "{{WORLD_1_SUMMARY}}": "Iran's military claims its air defences downed a US MQ-1 drone over the country's southeast, while separately the IRGC Navy says it seized an American-built unmanned underwater vehicle near the strait's entrance — both claims unconfirmed by Washington. It's the latest move in a months-long tanker war that has already cut Hormuz shipping traffic to its lowest level since May, with roughly a fifth of the world's oil still needing to pass through that gap.",
    "{{WORLD_1_URL}}": "https://www.middleeastmonitor.com/20260908-us-mq-1-drone-downed-by-iran-over-strait-of-hormuz/",

    "{{WORLD_2_FLAG}}": "🇸🇦 SAUDI ARABIA · HOUTHI MISSILES AND DRONES HIT OIL FACILITIES, WOUND 70+",
    "{{WORLD_2_HEADLINE}}": "Houthi Missile and Drone Barrage Wounds More Than 70 in Saudi Arabia, Ignites Fires at Oil Facilities",
    "{{WORLD_2_SUMMARY}}": "Yemen's Iran-backed Houthi rebels fired dozens of ballistic missiles and drones at oil, economic and air-force targets in southern Saudi Arabia on Tuesday, wounding more than 70 people and sparking fires, with the Saudi-led coalition vowing to retaliate \"with utmost resolve\". It's the sharpest escalation yet in a conflict that shattered a four-year Yemen truce, and one more reason the region's oil-price risk isn't fading soon.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/09/08/g-s1-142296/houthi-attacks-saudi-arabia",

    # Economics
    "{{ECON_1_FLAG}}": "📉 MARKETS · WESTPAC BECOMES LAST BIG FOUR BANK TO TIP A HIKE",
    "{{ECON_1_HEADLINE}}": "Westpac Joins Every Other Big Four Bank in Predicting an RBA Rate Hike, ASX Falls to a Six-Week Low",
    "{{ECON_1_SUMMARY}}": "Westpac has dropped its long-held \"hold\" call and now expects the RBA to lift the cash rate to 4.60% in November, meaning all four major banks now agree a hike is coming — the only argument left is timing, between the 29 September meeting (NAB, Deutsche Bank, UBS, Morgan Stanley) and November (ANZ, CBA, Westpac). The ASX closed at a six-week low on the news, but the direction of travel on borrowing costs is no longer in doubt.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-08/asx-markets-business-live-news-september-8-2026/107127114",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE PRICES HOLD NEAR MULTI-MONTH HIGHS",
    "{{ECON_2_HEADLINE}}": "Melbourne Bowser Prices Sit Near Multi-Month Highs — Unleaded Averaging 205c/L, Diesel 252c/L",
    "{{ECON_2_SUMMARY}}": "With Brent crude still elevated on the Hormuz and Houthi escalations, Melbourne's average unleaded price is running around 204.9c/L and diesel around 252.2c/L, though the cheapest sites are still 15–20c/L below that average. Same advice as it's been for months — shop between servos on the day rather than banking on a discount cycle that keeps getting interrupted by the Middle East.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💳 SMB AI · PAYMENTS \"SUPER AGENT\" GOES FULLY LIVE FOR SMALL BUSINESS BACK OFFICE",
    "{{TECH_1_HEADLINE}}": "Payments Platform Cashfree Takes Its AI \"Super Agent\" Out of Beta — Automating Reconciliation and Dispute Handling for Small Businesses",
    "{{TECH_1_SUMMARY}}": "Cashfree's Relay AI agent has moved from merchant beta to general availability, automatically matching payments, chasing reconciliation gaps and handling dispute paperwork that used to eat a rainy afternoon in the office. It's a sign of where practical business AI is actually landing in 2026 — not flashy, just quietly removing an admin job nobody wanted to do.",
    "{{TECH_1_URL}}": "https://thepaypers.com/payments/news/cashfree-payments-launches-relay-to-automate-payment-tasks",

    "{{TECH_2_FLAG}}": "📱 CONSUMER AI · BAIDU UNVEILS NEXT-GEN XIAODU SMART HOME HARDWARE",
    "{{TECH_2_HEADLINE}}": "Baidu Unveils New Xiaodu Smart Displays, Speakers and Cameras With an Upgraded AI Assistant",
    "{{TECH_2_SUMMARY}}": "Baidu used a dedicated product event to launch a refreshed Xiaodu hardware line-up — smart displays, speakers and home cameras — built around an upgraded Super Xiaodu assistant, including a second-generation AI monitoring agent embedded directly in the cameras. Another sign the assistant living in the loungeroom speaker keeps getting smarter, whether anyone asked for it or not.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🚶 PHYSICAL AI · A HUMANOID ROBOT WALKED ITSELF OFF THE PRODUCTION LINE",
    "{{ROBOT_1_HEADLINE}}": "XPeng's IRON Humanoid Robot Becomes the First to Autonomously Walk Off Its Own Production Line",
    "{{ROBOT_1_SUMMARY}}": "At a newly commissioned Guangzhou facility, XPeng says its IRON humanoid — built with over 80% automation and automotive-grade quality control shared with its EV lines — walked off the assembly line under its own power, with no human assistance or remote control, a world-first the company is calling proof mass production is within reach by year's end. Deployment starts in XPeng's own showrooms before any outside customer gets one in 2027.",
    "{{ROBOT_1_URL}}": "https://cleantechnica.com/2026/09/08/xpeng-iron-autonomously-walks-off-production-line/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Border Force Seizes 1.7 Million Illegal Cigarettes and Thousands of Vapes in WA and NT Blitz",
    "{{AUS_1_SUMMARY}}": "A six-day joint operation across Perth, Margaret River, Darwin and Katherine uncovered more than 1.7 million illicit cigarettes, 500kg of loose-leaf tobacco and over 9,500 vapes — a haul worth more than $800,000 at street value and nearly $4 million in dodged tax. Authorities have applied to shut 15 retail outlets as a result.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-08/wa-nt-illegal-cigarettes-tobacco-vapes-raids-police-border-force/107127594",

    "{{AUS_2_HEADLINE}}": "Australia and Solomon Islands Strike In-Principle Deal on New Bilateral Security and Development Treaty",
    "{{AUS_2_SUMMARY}}": "Canberra and Honiara have reached an in-principle agreement on a new treaty, with Australia offering close to $1 billion in funding over coming years — the latest move in a four-year push to rebuild Pacific ties after Solomon Islands' 2022 security pact with China rattled Canberra.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Reservoirs Spilling After Heavy Rain — Lake Eppalock Overflows, Three More Storages Above 90%",
    "{{VIC_1_SUMMARY}}": "Goulburn Murray Water says Lake Eppalock is now spilling around 300 megalitres a day after filling over the weekend, while Tullaroop Reservoir has been spilling for weeks and Cairn Curran and Laanecoorie both sit above 90% capacity — a solid water-security position heading into a wetter-than-usual spring.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ PHYSICS · EINSTEIN'S GRAVITY CONFIRMED IN THE QUANTUM WORLD FOR THE FIRST TIME",
    "{{SCI_1_HEADLINE}}": "Physicists Directly Observe Einstein's Gravity Acting on a Falling Quantum Object for the First Time",
    "{{SCI_1_SUMMARY}}": "An international team including Nobel laureate Sir Roger Penrose has measured a distinctive quantum-property change in atoms as they fall under gravity — exactly the effect predicted when Einstein's equivalence principle is applied to quantum matter. It doesn't unify gravity with quantum mechanics, but it's the first time the two have been tested together this directly, and the technique opens the door to heavier test objects like nanodiamonds.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Your Ute Doesn't Send a Text Before It Breaks Down — AI-Powered Predictive Maintenance Just Got Cheap Enough for a One-Truck Business",
    "{{INSIGHT_BODY}}": "With fuel sitting near multi-month highs and every major bank now tipping an RBA rate hike before year's end, an unplanned breakdown costs more than it used to — in tow bills, missed jobs, and finance repayments that don't pause for a blown radiator hose. A $50–$150 OBD-II dongle paired with a phone app now runs the same kind of predictive-maintenance AI once reserved for national fleets, quietly watching engine data in the background and flagging a failing part weeks before it strands you on Peninsula Link. For a one-ute or one-compressor operation, that's the difference between a scheduled Tuesday service and a Thursday tow truck eating into next week's margin.",

    # Fun facts
    "{{FACT_1}}": "The modern oil industry traces back to a 21-metre well Edwin Drake struck at Titusville, Pennsylvania, in 1859 — the world's first commercial oil well, drilled almost by accident after his backers had nearly pulled the funding, and the reason a tanker skirmish near the Strait of Hormuz today still moves the price at an Australian bowser.",
    "{{FACT_2}}": "Detroit engineer Charles Brady King patented a pneumatic hammer in 1890 — years before he became known as a car-making pioneer — and used the proceeds from selling the patent rights to help fund the build of the first petrol-powered automobile driven on Detroit's streets, in 1896.",
    "{{FACT_3}}": "The humble wooden shipping pallet was standardised by the US military during WWII to speed loading onto ships and aircraft, and the idea stuck so well that an estimated two billion of them are now in circulation in the US alone — more pallets than there are people in North and South America combined.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the NBN and data cabling technician never lose an argument with a client about slow Wi-Fi?",
    "{{JOKE_PUNCHLINE}}": "He just pulled out the signal tester and let the numbers do the talking.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The elevator to success is out of order. You'll have to use the stairs, one step at a time.\"",
    "{{CLOSING_ATTR}}": "— Joe Girard",
    "{{CLOSING_MESSAGE}}": "Wednesday should be the calmest, driest day of the run around Carrum Downs, with a cooler change and returning showers arriving Thursday — so if there's outdoor work or coatings prep needing a dry window, today's the one to use. Worth also keeping an eye on the Brent number this week; every fresh flare-up near Hormuz has a habit of turning up at the local bowser about a fortnight later.",
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
