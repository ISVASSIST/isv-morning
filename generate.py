#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 03 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 3 Sep (BOM)
    "{{WEATHER_1}}": "THU 3 SEP · 🌤️ Slight chance of a shower, breezy nor'wester easing later · 9–15°C",
    "{{WEATHER_2}}": "FRI 4 SEP · 🌦️ Partly cloudy, medium chance of a shower in the early morning · 6–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 5 SEP · 🌧️ Cloudy, high chance of showers in the afternoon and evening · 7–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 6 SEP · ☀️ Mostly sunny, breezy nor'wester, moderate UV · 9–18°C",
    "{{WEATHER_5}}": "MON 7 SEP · 🌧️ Very high chance of rain, strong northerly winds · 11–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula. A showery, blustery spell builds through the weekend before a wetter, windier start to next week.",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 KYIV · PUTIN AND ZELENSKYY TRADE THREATS AS STRIKES ESCALATE",
    "{{WORLD_1_HEADLINE}}": "Putin and Zelenskyy Trade Threats as Russia Fires Missiles and Drones at Kyiv and Mykolaiv",
    "{{WORLD_1_SUMMARY}}": "Russia launched Iskander missiles and 174 drones at Ukraine overnight into Tuesday, striking a Kyiv university during class hours and damaging homes and cars in Mykolaiv, while Ukraine's forces hit drone control centres and troop concentrations; Putin and Zelenskyy then traded threats over next steps, with Zelenskyy warning that Russian airspace is unsafe for foreign flights given Ukraine's long-range drone strikes.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/9/2/putin-and-zelenskyy-issue-threats-as-strikes-rock-ukraine-russia",

    "{{WORLD_2_FLAG}}": "🇺🇸 WASHINGTON · HOUSE AVERTS SHUTDOWN WITH FUNDING PUSHED TO DECEMBER",
    "{{WORLD_2_HEADLINE}}": "US House Passes Stopgap Funding Bill, Averting a Government Shutdown Ahead of the Midterms",
    "{{WORLD_2_SUMMARY}}": "The US House voted 370-48 on Tuesday to fund the federal government through 11 December, an unusually early resolution that avoids a shutdown before the November midterms and pushes the next spending fight into the new year; the bill also delays a contentious overhaul of federal grant rules until the same date and now heads to the president's desk.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/09/01/nx-s1-5951536/house-government-funding-vote-midterms",

    # Economics
    "{{ECON_1_FLAG}}": "📉 ASX · MARKET SLIPS AS OIL JUMPS AND RATE-HIKE TALK BUILDS",
    "{{ECON_1_HEADLINE}}": "ASX Falls Almost 1% as Oil Hits a Two-Month High and Strong GDP Growth Fuels RBA Rate-Hike Bets",
    "{{ECON_1_SUMMARY}}": "The ASX 200 closed down 37.5 points (-0.41%) at 9,038.50 on Tuesday after June-quarter GDP came in stronger than expected, pushing traders' odds of a September RBA rate hike to around 70% — a mood echoed on Wall Street, where the Dow, S&P 500 and Nasdaq all fell overnight on the same rate-hike jitters.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-02/asx-markets-business-live-news/107105482",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE BOWSERS SIT MID-CYCLE, PATTERN STILL DISRUPTED",
    "{{ECON_2_HEADLINE}}": "Melbourne Fuel Holds Near 200c/L, With the Usual Price Cycle Still Disrupted by Middle East Tensions",
    "{{ECON_2_SUMMARY}}": "Melbourne's 14-day average unleaded price sits around 199.8–203c/L, with the cheapest sites near 186–187.5c/L in the outer suburbs and diesel averaging around 234.5c/L in Preston — but the usual predictable price cycle that normally lets drivers time a cheap fill has barely run in Sydney, Melbourne, Brisbane or Adelaide since the Middle East conflict began in late February, making bowser prices harder to plan around than usual.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🏥 AI IN HEALTHCARE · CHATGPT NOW PLUGS INTO EPIC PATIENT RECORDS",
    "{{TECH_1_HEADLINE}}": "OpenAI Adds Epic Health Record Integration to ChatGPT, Giving Clinicians Read-Only Patient Data Access",
    "{{TECH_1_SUMMARY}}": "OpenAI announced healthcare organisations can now connect their Epic electronic health record systems to ChatGPT for Healthcare, alongside a new plugin linking to nine official datasets including PubMed and CMS Coverage; UCSF Health is piloting it, with physicians rating 99.1% of nearly 4,400 evaluated responses as safe — a sign of how fast AI is being wired into serious, high-stakes systems, not just chatbots.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/09/01/chatgpt-health-adds-epic-integration-for-clinicians-to-import-patient-data/",

    "{{TECH_2_FLAG}}": "🔐 AI SECURITY · OPENAI'S NEWEST MODEL CROSSES A 'CRITICAL' CYBER THRESHOLD",
    "{{TECH_2_HEADLINE}}": "OpenAI Says Its Astra Model Is the First to Cross a 'Critical' Cybersecurity Capability Threshold",
    "{{TECH_2_SUMMARY}}": "OpenAI confirmed its Astra model scored a perfect result on ExploitBench and autonomously found two real zero-day vulnerabilities in testing, making it the first model to cross the 'Critical' cybersecurity bar in the company's own risk framework — access to its sharpest capabilities is being tightly restricted to vetted testers for now, but it's an early signal that AI-assisted hacking tools are getting genuinely capable, not just theoretical.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 DEXTEROUS AI · A WEARABLE DEVICE THAT TEACHES ROBOTS TO USE THEIR HANDS",
    "{{ROBOT_1_HEADLINE}}": "Chinese Robotics Firm X Square Robot Unveils TwinDEX, a Wearable Rig for Training Robot Hands",
    "{{ROBOT_1_SUMMARY}}": "X Square Robot this week introduced TwinDEX, a matched pair of three-finger, nine-degree-of-freedom devices — one worn by a human to collect fine hand-manipulation data, the other fitted to a robot as its end effector — aimed at making dexterous tasks like picking, sorting and assembly far cheaper to teach robots without needing expensive robot hardware for every hour of training data.",
    "{{ROBOT_1_URL}}": "https://www.prnewswire.com/news-releases/twindex-introduces-a-scalable-path-from-robot-free-data-collection-to-real-world-dexterous-manipulation-302867559.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "UN Report Warns 1.5°C Warming Threshold Likely to Be Breached, as Albanese Defends Pre-COP Talks in Fiji",
    "{{AUS_1_SUMMARY}}": "A new UN report warns the world is on track to breach the 1.5°C warming benchmark within five years and is unlikely to hold warming below 1.8°C, landing as Prime Minister Anthony Albanese defended Australia's role co-hosting Pacific pre-COP talks in Fiji and Tuvalu ahead of COP31, which Australia will help lead as President of Negotiations in Antalya, Türkiye, this November.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-02/global-warming-breach-likely-as-albanese-defends-pre-cop-meeting/107108178",

    "{{AUS_2_HEADLINE}}": "Hundreds of AI-Issued Seatbelt Fines Dropped in WA After Police Couldn't Prove Drivers Knew",
    "{{AUS_2_SUMMARY}}": "WA Police have overturned about 5,700 of the 81,412 seatbelt infringements issued by AI-assisted road safety cameras since last October, after prosecutors accepted 'reasonable defences' from drivers fined for passengers — including children and neurodivergent people — wearing seatbelts incorrectly; detected infractions are still down 76% year-on-year even as the fine-dropping continues.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "North Melbourne and Coach Alastair Clarkson Part Ways After Four Seasons",
    "{{VIC_1_SUMMARY}}": "North Melbourne says 'gaping holes' in Alastair Clarkson's game plan led the club to end his tenure early despite a contract through 2027, with president Dr Sonja Hood saying Clarkson remained well liked by players but the list needed a fresh voice — the Kangaroos finished 14th with nine wins this year, their best season under him since 2019.",

    # Science
    "{{SCI_1_FLAG}}": "🍵 HEALTHY AGEING · TEA LINKED TO STRONGER BONES IN OLDER WOMEN",
    "{{SCI_1_HEADLINE}}": "Flinders University Study of Nearly 10,000 Women Finds Tea Drinking Linked to Higher Hip Bone Density",
    "{{SCI_1_SUMMARY}}": "Tracking almost 10,000 women aged 65 and over for a decade, Flinders University researchers found regular tea drinkers had slightly higher hip bone mineral density, an important marker for osteoporosis risk; moderate coffee didn't appear harmful, but drinking more than five cups a day was linked to lower bone density — the study was published in the journal Nutrients.",

    # Business insight
    "{{INSIGHT_TITLE}}": "OpenAI's Newest Model Can Now Find Real Software Flaws On Its Own — Here's What That Means for Your Basic Cyber Hygiene",
    "{{INSIGHT_BODY}}": "OpenAI confirmed this week that its Astra model is the first to cross what it calls a 'Critical' cybersecurity threshold, scoring a perfect result on a benchmark for turning known flaws into working exploits and independently discovering two real zero-day vulnerabilities in testing. Access to its sharpest capabilities is being kept tightly restricted for now, but the direction is clear: tools that once needed a skilled human hacker are becoming more automatable every year. A small trades business isn't the target of a nation-state, but it is exactly the kind of soft, under-patched target automated scanning tools sweep up along the way. The unglamorous basics — unique passwords on your invoicing and banking logins, software updates you've been putting off, and a phone-call habit before paying any changed bank details — are cheap insurance against a threat that's only getting more automated.",

    # Fun facts
    "{{FACT_1}}": "The Allen key (hex key) was patented in 1910 by Connecticut toolmaker William G. Allen, whose Allen Manufacturing Company held exclusive rights to the hexagonal socket screw system for years before rival tool makers could legally copy it.",
    "{{FACT_2}}": "The give-way-to-the-right roundabout rule now standard from Melbourne to London wasn't obvious until British transport researcher Frank Blackmore tested it in the 1960s — his UK Road Research Laboratory studies found it cut collisions so sharply that the design was exported worldwide within a decade.",
    "{{FACT_3}}": "The lamington — Australia's chocolate-and-coconut sponge square — is said to owe its existence to Queensland Governor Lord Lamington's household around 1900, after a cook dipped day-old sponge cake in chocolate and rolled it in coconut to stretch it for unexpected guests.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the gas fitter's small business never run out of work?",
    "{{JOKE_PUNCHLINE}}": "Because he always left every job airtight — literally and financially.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Success is the sum of small efforts, repeated day in and day out.\"",
    "{{CLOSING_ATTR}}": "— Robert Collier",
    "{{CLOSING_MESSAGE}}": "It's Thursday in Carrum Downs, with just a slight chance of a shower this morning before a breezy nor'wester takes over — a decent window to get outdoor jobs sorted before the wetter, blustery stretch building for the weekend. Down the road, North Melbourne's split from long-time coach Alastair Clarkson is dominating the footy conversation, while back on the books it's Tuesday's GDP figures and the fresh RBA rate-hike chatter that are actually worth your attention this week.",
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
