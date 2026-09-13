#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 14 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 14 Sep (BOM Melbourne-area forecast)
    "{{WEATHER_1}}": "MON 14 SEP · 🌤️ Mostly sunny, medium chance of a shower late afternoon and evening, northerly winds 30–45km/h decreasing 20–30km/h · 14–23°C",
    "{{WEATHER_2}}": "TUE 15 SEP · 🌧️ Cloudy, high chance of showers most likely in the morning, winds N–NW 20–30km/h turning W 15–20km/h · 11–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 16 SEP · ⛈️ Partly cloudy, very high chance of showers with possible small hail in the afternoon and evening, W turning SW 25–35km/h · 9–13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 17 SEP · ⛅ Sunny, slight chance of a shower easing through the day · 9–15°C",
    "{{WEATHER_5}}": "FRI 18 SEP · ☀️ Sunny and warming up, little to no chance of rain · 11–21°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — a mild, mostly dry start to the week gives way to a wetter, cooler midweek change with possible small hail Wednesday, before clearing and warming again by Friday.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇩 JAVA SEA · FERRY CAPSIZES, ABOUT 130 MISSING IN INDONESIA'S WORST MARITIME DISASTER THIS YEAR",
    "{{WORLD_1_HEADLINE}}": "Indonesian Ferry Capsizes in the Java Sea, Leaving About 130 Missing After 243 People Were Aboard",
    "{{WORLD_1_SUMMARY}}": "The passenger ferry Virgo Transport 8 lost contact and capsized in rough seas early Sunday while sailing from Surabaya to Banjarmasin, with waves reported up to three metres before the captain's distress call. Six bodies have been recovered and more than 100 survivors rescued by nearby commercial vessels and navy warships, with search operations continuing in the shallow, squall-prone Java Sea.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/09/13/g-s1-143114/about-130-missing-after-indonesian-passenger-ship-overturns",

    "{{WORLD_2_FLAG}}": "🇺🇦 UKRAINE · RUSSIA HITS POWER GRID OVERNIGHT AS KYIV STRIKES A RUSSIAN OIL REFINERY",
    "{{WORLD_2_HEADLINE}}": "Russia Pounds Ukrainian Power Stations Overnight While Kyiv's Drones Strike a Russian Oil-Refining Hub",
    "{{WORLD_2_SUMMARY}}": "Russia launched a fresh wave of drones and missiles at Ukrainian energy infrastructure overnight, while Ukrainian forces struck an oil-refining hub deep inside Russian territory in a tit-for-tat exchange now well into the war's fifth year, as US envoys continue shuttling between Moscow and Kyiv trying to broker fresh talks.",
    "{{WORLD_2_URL}}": "https://www.bloomberg.com/news/articles/2026-09-13/russia-strikes-ukraine-power-sites-as-kyiv-targets-refining-hub",

    # Economics
    "{{ECON_1_FLAG}}": "📈 RATES · RBA HIKE ODDS NEAR 80% AS HAWKISH SIGNALS AND THE OIL SHOCK COLLIDE",
    "{{ECON_1_HEADLINE}}": "Markets Now Price Close to an 80% Chance of an RBA Rate Hike This Month as Inflation and Oil Both Run Hot",
    "{{ECON_1_SUMMARY}}": "The Australian dollar pushed toward a four-month high this week after RBA Deputy Governor Andrew Hauser flagged that the September board meeting will focus squarely on whether to raise rates again, with markets now pricing close to an 80% chance of a hike to 4.60% on 29 September. A hike would add further pressure to overdraft and equipment-finance rates just as fuel costs bite into margins.",
    "{{ECON_1_URL}}": "https://www.fxstreet.com/news/australian-dollar-softens-to-near-07150-us-cpi-inflation-data-looms-202609110251",

    "{{ECON_2_FLAG}}": "⛽ FUEL · PETROL HITS $2.11/L AS STRAIT OF HORMUZ TANKER ATTACKS RIPPLE THROUGH TO THE BOWSER",
    "{{ECON_2_HEADLINE}}": "Australian Petrol Climbs to $2.11 a Litre, Up From $1.55 in July, as Tanker Attacks Rattle the Strait of Hormuz",
    "{{ECON_2_SUMMARY}}": "Average unleaded prices have climbed to $2.11 a litre nationally as both sides in the Middle East conflict target oil tankers in the Strait of Hormuz, pushing crude back above US$100 a barrel. Economists warn the pain isn't over yet, with further pump-price rises still working their way through the supply chain — worth locking in a fuel surcharge on quotes now rather than eating the cost later.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🍏 APPLE · SIRI FINALLY GETS ITS AI OVERHAUL AS IOS 27 ROLLS OUT TODAY",
    "{{TECH_1_HEADLINE}}": "Apple's Long-Awaited Siri AI Overhaul Rolls Out Today in iOS 27, Starting in English Only",
    "{{TECH_1_SUMMARY}}": "iOS 27 lands today with the AI-rebuilt Siri Apple has spent two years promising — able to see what's on your screen, act across apps and draw on your calendar and email with permission — though it starts in English only, with daily usage caps and a paid 'expanded access' tier flagged for later. Worth a look once it's on your phone, if only to see how far behind ChatGPT or Claude it still is for actual work tasks.",
    "{{TECH_1_URL}}": "https://www.macrumors.com/2026/09/09/apple-siri-ai-usage-limits/",

    "{{TECH_2_FLAG}}": "🎙️ VOICE AI · OPENAI'S NEW REAL-TIME VOICE MODEL COSTS 5 CENTS A MINUTE",
    "{{TECH_2_HEADLINE}}": "OpenAI Opens Up GPT-Live-1, a Real-Time Voice AI Model, to Developers at 5 Cents a Minute",
    "{{TECH_2_SUMMARY}}": "OpenAI has released GPT-Live-1 through its API, a 'full-duplex' voice model that listens and talks at the same time rather than waiting for you to finish — priced at just 5 US cents a minute. It's the kind of building block that's making a decent AI phone-answering or booking assistant a realistic, cheap option for a small operation, not just a call centre.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "👁️ ROBOT PERCEPTION · EX-APPLE FACE ID ENGINEERS RAISE $165M TO GIVE ROBOTS A TRUSTWORTHY VIEW OF THE WORLD",
    "{{ROBOT_1_HEADLINE}}": "Startup Founded by Apple's Face ID Engineers Raises $165M to Build Robots' Sense of Sight",
    "{{ROBOT_1_SUMMARY}}": "Lyte, founded by engineers who built Apple's Face ID sensors, has raised a $165 million Series C at a $1.6 billion valuation to build custom perception chips and sensors that let robots reliably sense where they are and what's moving around them. Better, cheaper perception hardware is exactly the unglamorous layer that decides whether a robot arm or mobile robot can be trusted on a real, cluttered factory or warehouse floor rather than just a demo stage.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/lyte-raises-165m-help-robots-better-sense-their-surroundings/",

    # Australia
    "{{AUS_1_HEADLINE}}": "$18 Million Mining Shovel Gutted by Fire at Kalgoorlie's Super Pit, Operator Escapes Unhurt",
    "{{AUS_1_SUMMARY}}": "WorkSafe WA is investigating after fire engulfed the cab of a 750-tonne Komatsu PC8000 shovel — one of the largest mechanical shovels in the world — during a night shift at Kalgoorlie's Super Pit on 9 September. The operator escaped without injury, but the $18 million machine, due for retirement in November anyway, is a write-off.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-13/fire-destroys-cab-of-shovel-at-kalgoorlie-super-pit/107142366",

    "{{AUS_2_HEADLINE}}": "Balcony Solar Set to Become Legal, Opening Rooftop-Free Solar to Millions of Renters",
    "{{AUS_2_SUMMARY}}": "Australia's energy ministers have agreed to explore a pathway for 'plug-in' balcony solar, which could let apartment dwellers and renters — almost 3 million households — plug a small solar panel straight into a power point for the first time. Campaigners want a firm timeline by December on when the ban actually lifts.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "World-First Trial Finds Floating Wetlands Cut a Phillip Island Wastewater Lagoon's Emissions by 30%",
    "{{VIC_1_SUMMARY}}": "A two-year RMIT, Westernport Water and CSIRO trial found a 330-square-metre floating garden of native reeds and sedges cut a wastewater lagoon's carbon dioxide emissions by up to 36%, methane by up to 66% and nitrogen by 18%, compared with an untreated lagoon — a low-tech fix with obvious appeal for any business running its own wastewater ponds.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 QUANTUM PHYSICS · A LASER'S SIDEWAYS \"CURVEBALL\" ON A SINGLE ATOM, CONFIRMED FOR THE FIRST TIME",
    "{{SCI_1_HEADLINE}}": "Physicists Catch a Laser Beam Pushing an Atom Sideways for the First Time",
    "{{SCI_1_SUMMARY}}": "Researchers trapped a single calcium ion and fired a tightly focused laser at it, confirming a decades-old prediction called the optical Magnus effect — the beam interacts most strongly with the atom slightly off-centre, the same physics that curves a spinning table-tennis ball through the air. It matters beyond curiosity: because lasers are used to control quantum computer qubits, the effect could introduce errors — or offer a new way to link qubits together.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Real-Time AI Voice Calls Just Got Cheap Enough to Actually Use",
    "{{INSIGHT_BODY}}": "OpenAI's new GPT-Live model talks and listens at the same time — no more waiting for you to finish a sentence — and it costs about 5 cents a minute through the API, roughly the price of the call itself. That's the kind of pricing that turns 'an AI answering the phone' from a novelty into something a two-person outfit could actually wire up to take bookings and rough quotes while you're on the tools, with a human doing the follow-up call once you're back at the desk.",

    # Fun facts
    "{{FACT_1}}": "The Java Sea, where a ferry carrying 243 people capsized this week, has an average depth of only about 46 metres — shallow enough that its notoriously sudden squalls can still overturn a large vessel in minutes.",
    "{{FACT_2}}": "Kalgoorlie's Super Pit — where an $18 million mining shovel caught fire this week — is Australia's largest open-cut gold mine, roughly 3.5km long and 1.5km wide, and easily visible from space.",
    "{{FACT_3}}": "The \"optical Magnus effect\" confirmed by physicists this week is named after the same 19th-century effect that curves a spinning soccer or cricket ball — only here it's a laser beam nudging a single atom sideways by a few hundred nanometres.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the skylight installer never worry about a rainy day?",
    "{{JOKE_PUNCHLINE}}": "Because he'd already sealed the deal before the first drop fell.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The science of today is the technology of tomorrow.\"",
    "{{CLOSING_ATTR}}": "— Edward Teller",
    "{{CLOSING_MESSAGE}}": "It's a mild, mostly sunny start to the week around Carrum Downs, with the wetter, cooler change holding off until Wednesday — a good window to get outdoor jobs ticked off before then. Locally the week's news cuts both ways: another rate rise looks increasingly likely and fuel's not getting any cheaper, but voice AI and other practical tools are also getting cheap enough to actually save a trades business time, not just talk about it.",
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
