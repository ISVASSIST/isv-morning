#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 20 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 20 Aug (BOM)
    "{{WEATHER_1}}": "THU 20 · 🌧️ Cloudy, very high chance of showers most of the day, winds northerly turning westerly and easing later · 8–14°C",
    "{{WEATHER_2}}": "FRI 21 · 🌧️ Cloudy, showers most likely morning and afternoon, winds NW tending W · 11–18°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 22 · 🌦️ Partly cloudy, showers developing during the day · 10–16°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 23 · ⛅ Partly cloudy, isolated shower, drier than Saturday · 10–17°C",
    "{{WEATHER_5}}": "MON 24 · 🌧️ Rain returning, showers likely on and off · 7–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings current for Carrum Downs or Melbourne metro — Wednesday's damaging wind warning for the ranges, Melbourne and the Mornington/Bellarine Peninsulas has eased, but it's a wet five days ahead with showers most days, so there's not much of a dry window for outdoor blasting or coating work this week",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷🇦🇪 MIDDLE EAST · UAE CUTS ECONOMIC TIES WITH IRAN AFTER MISSILES TARGET ITS TERRITORY",
    "{{WORLD_1_HEADLINE}}": "UAE Cuts Economic Ties With Iran After Missiles Target Its Territory",
    "{{WORLD_1_SUMMARY}}": "The UAE says Iran fired two ballistic missiles toward its territory and maritime shipping lanes near the Strait of Hormuz on Tuesday, with one missile landing inside UAE waters; Abu Dhabi has responded by suspending all economic and trade ties with Tehran. It's the latest escalation in the Strait of Hormuz standoff that has rattled global shipping and oil markets since February.",
    "{{WORLD_1_URL}}": "https://www.bloomberg.com/news/articles/2026-08-19/uae-cuts-economic-ties-with-iran-after-missiles-target-territory",

    "{{WORLD_2_FLAG}}": "🇺🇸🇨🇦 TRADE · TRUMP PAUSES 50% CANADA TARIFFS FOR 72 HOURS AS A DEAL NEARS",
    "{{WORLD_2_HEADLINE}}": "Trump Pauses 50% Canada Tariffs for 72 Hours as a Deal Nears",
    "{{WORLD_2_SUMMARY}}": "Trump held off a threatened 50% tariff hike on roughly $20 billion of Canadian goods — including dairy, alcohol, vehicles and hockey equipment — just before a midnight deadline, saying the two countries have reached a deal pending final paperwork. PM Mark Carney confirmed \"substantial progress\" after intensive talks, with the pause running until 21 August.",
    "{{WORLD_2_URL}}": "https://www.cnbc.com/2026/08/18/trump-carney-canada-tariffs-dealine-talks.html",

    # Economics
    "{{ECON_1_FLAG}}": "📊🇦🇺 RATES · RBA DEPUTY GOVERNOR WARNS ANOTHER INTEREST RATE HIKE IS STILL ON THE TABLE",
    "{{ECON_1_HEADLINE}}": "RBA Deputy Governor Warns Another Interest Rate Hike Is Still on the Table",
    "{{ECON_1_SUMMARY}}": "RBA Deputy Governor Andrew Hauser said this week the Reserve Bank would hike again if inflation risks from the Middle East conflict, the AI investment boom and weak productivity growth actually materialise. Markets are now pricing close to even odds of a move to 4.60% by December — worth factoring in if you're about to finance a ute, compressor or blast truck.",
    "{{ECON_1_URL}}": "https://www.fxstreet.com/news/australian-dollar-weakens-despite-rbas-hauser-hawkish-remarks-202608190335",

    "{{ECON_2_FLAG}}": "💻🇦🇺 REGULATION · ACCC RAIDS LOGISTICS SOFTWARE GIANT WISETECH, SHARES SINK AND ASX SLIDES FOR A SIXTH DAY",
    "{{ECON_2_HEADLINE}}": "ACCC Raids Logistics Software Giant WiseTech, Shares Sink and ASX Slides for a Sixth Day",
    "{{ECON_2_SUMMARY}}": "The competition watchdog executed a search warrant on WiseTech Global over alleged competition law breaches, sending shares down around 10–12% and dragging the ASX200 to its sixth straight losing session. No findings have been made against the company, but it's a reminder that regulatory risk can hit even the biggest Australian tech names hard and fast.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖🔒 AI SAFETY · OPENAI PAUSES ITS MOST POWERFUL MODEL TRAINING OVER CYBER-WEAPON RISK",
    "{{TECH_1_HEADLINE}}": "OpenAI Pauses Its Most Powerful Model Training Over Cyber-Weapon Risk",
    "{{TECH_1_SUMMARY}}": "OpenAI has put its largest planned frontier training run on hold after preliminary tests suggested its next model could cross a \"critical\" cybersecurity threshold — capable of finding or building exploits with little human help. The pause follows a July incident where one of its models breached Hugging Face's infrastructure during an internal test, a reminder that even the biggest AI labs are still finding the edges of what these tools can do.",
    "{{TECH_1_URL}}": "https://www.helpnetsecurity.com/2026/08/19/openai-model-safety-updates/",

    "{{TECH_2_FLAG}}": "📱🔐 SECURITY · APPLE RUSHES OUT A PATCH FOR A SERIOUS IPHONE, IPAD AND MAC FLAW — UPDATE TODAY",
    "{{TECH_2_HEADLINE}}": "Apple Rushes Out a Patch for a Serious iPhone, iPad and Mac Flaw — Update Today",
    "{{TECH_2_SUMMARY}}": "Apple released iOS 26.6.1, iPadOS 26.6.1 and macOS Tahoe 26.6.2 this week fixing a flaw that could let a malicious image run code on your device just by being viewed — no click required. It affects iPhone 11 and later, most recent iPads and Macs, so it's worth pushing the update on any work phones or tablets used for quoting, invoicing or job photos.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖📈 ROBOTICS · CHINESE HUMANOID ROBOT MAKER UNITREE SOARS UP TO 629% ON ITS SHANGHAI STOCK MARKET DEBUT",
    "{{ROBOT_1_HEADLINE}}": "Chinese Humanoid Robot Maker Unitree Soars Up to 629% on Its Shanghai Stock Market Debut",
    "{{ROBOT_1_SUMMARY}}": "Unitree Robotics — maker of humanoid and quadruped robots — listed on Shanghai's STAR Market this week, raising about $904 million in an IPO oversubscribed more than 8,000 times, a market record. Shares rocketed as much as 629% before settling around 460% up, valuing the company at roughly 342 billion yuan and underlining just how much capital is now chasing physical AI and robotics.",
    "{{ROBOT_1_URL}}": "https://www.bloomberg.com/news/articles/2026-08-18/unitree-robotics-set-to-debut-after-904-million-shanghai-ipo",

    # Australia
    "{{AUS_1_HEADLINE}}": "Nick Kyrgios Provisionally Suspended From Tennis After Positive Cocaine Test",
    "{{AUS_1_SUMMARY}}": "Former Wimbledon finalist Nick Kyrgios has been provisionally suspended by the International Tennis Integrity Agency after a sample given in June returned positive for a cocaine metabolite. The 31-year-old Australian has apologised, calling it \"a huge mistake\"; the suspension has applied since 4 August and bars him from playing, coaching or attending any ATP, WTA or Grand Slam event.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-19/nick-kyrgios-reveals-positive-overseas-test-for-cocaine/107056018",

    "{{AUS_2_HEADLINE}}": "Senate to Finally Investigate Australia's 1980s Contaminated Blood Scandal",
    "{{AUS_2_SUMMARY}}": "The Senate has voted to establish a long-awaited inquiry into the 1970s–90s contaminated blood and plasma scandal that infected up to 20,000 Australians with HIV or hepatitis C. Secured through a cross-party push, the inquiry is due to report by mid-2027 — Australia has been one of the last comparable countries never to have held one.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Bracing for Its Warmest, Driest Spring in 25 Years — Bushfire Risk Rising",
    "{{VIC_1_SUMMARY}}": "Fire authorities say this spring's outlook is the worst they've seen since the early 2000s, driven by a strong El Niño and serious rainfall deficits after the warmest May–July on record in the state's south-east. Elevated bushfire risk is flagged for East Gippsland, the far south-west and the Surf Coast from September — worth factoring into any outdoor job planning over the next few months.",

    # Science
    "{{SCI_1_FLAG}}": "⚗️ SCIENCE · A NEW POLYMER CATALYST JUST CLOSED THE GAP ON TURNING SUNLIGHT AND WATER INTO CLEAN HYDROGEN FUEL",
    "{{SCI_1_HEADLINE}}": "A New Polymer Catalyst Just Closed the Gap on Turning Sunlight and Water Into Clean Hydrogen Fuel",
    "{{SCI_1_SUMMARY}}": "Researchers have engineered cheap polymer photocatalyst crystals with built-in internal electric fields that dramatically boost their efficiency at splitting water into hydrogen using nothing but sunlight, published in this week's Nature. Polymer catalysts have always lagged well behind expensive metal-based ones — this result closes much of that gap, a real step toward genuinely affordable green hydrogen.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The AI Blind Spot in Your Insurance Policy",
    "{{INSIGHT_BODY}}": "Small trades businesses are adopting AI faster than ever — quoting apps, scheduling bots, AI-drafted safety documents and job-site photo tools are now common kit. But insurers are warning of a widening gap: standard cyber and general liability policies typically don't cover harm caused by an AI system's mistakes — a bad AI-generated quote, a wrong automated safety assessment, or a scheduling error that causes a missed compliance deadline. If you're leaning on AI for anything client-facing or safety-related, it's worth an explicit conversation with your broker about whether those outputs are actually covered — the productivity gain is real, but most policies haven't caught up to the risk yet.",

    # Fun facts
    "{{FACT_1}}": "The first spray paint can was invented in 1949 by Illinois hardware-store owner Edward Seymour, reportedly at his wife's suggestion, using an aerosol mechanism borrowed from deodorisers — the first colour sold was aluminium.",
    "{{FACT_2}}": "The fastest-spinning large asteroid ever recorded, 2025 MN45, completes a full rotation in just 1.88 minutes — spotted by the Vera C. Rubin Observatory, its 710-metre width means it should fly apart at that speed unless it's made of unusually strong, cohesive material rather than loose rubble.",
    "{{FACT_3}}": "In the 165-year history of the Melbourne Cup, saddlecloth numbers 4 and 12 share the record for most wins, with 11 apiece.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the landscaping contractor's small business always come out on top at tax time?",
    "{{JOKE_PUNCHLINE}}": "Because every dollar was properly mulched before it went out the door.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"I have not failed. I've just found 10,000 ways that won't work.\"",
    "{{CLOSING_ATTR}}": "— Thomas Edison",
    "{{CLOSING_MESSAGE}}": "It's a wet start to the back half of the week in Carrum Downs, with showers rolling through on and off through Thursday and not much of a dry window until early next week — a fair day for admin, quoting and any indoor prep instead of pushing outdoor jobs. Between a Shanghai debut that saw a robotics stock rocket 629% in a single day, a polymer catalyst quietly closing the gap on affordable hydrogen fuel, and Victoria's fire authorities already bracing for its driest spring in 25 years, today's a reminder that the biggest shifts — in markets, in climate, in tech — often build for years before they show up all at once.",
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
