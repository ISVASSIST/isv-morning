#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 29 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 29 Aug (BOM)
    "{{WEATHER_1}}": "SAT 29 · ⛈️ Showers, chance of a storm, most likely PM · 7–17°C",
    "{{WEATHER_2}}": "SUN 30 · 🌧️ Cloudy, very high chance of showers, windy · 8–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 31 · ⛅ Clearing, sunny spells, cooler start · 6–16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "TUE 1 SEP · ☀️ Mostly sunny and mild · 8–18°C",
    "{{WEATHER_5}}": "WED 2 SEP · 🌤️ Partly cloudy, isolated late shower · 9–17°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula. Sunday's the pick of a wet, blustery stretch with north-westerlies gusting 25–35 km/h, before it clears into a dry, mild run from Monday — today's still your best outdoor window before the wind and rain properly set in tomorrow.",

    # World
    "{{WORLD_1_FLAG}}": "🇳🇴 NORWAY · KING HARALD V DIES AGED 89",
    "{{WORLD_1_HEADLINE}}": "Norway's King Harald V Dies Aged 89, Son Ascends as King Haakon",
    "{{WORLD_1_SUMMARY}}": "Europe's oldest reigning monarch died at Oslo's Rikshospitalet on Friday after treatment for haemolytic anaemia, ending a 35-year reign remembered for modernising the Norwegian monarchy; his son immediately succeeded him as King Haakon VIII.",
    "{{WORLD_1_URL}}": "https://www.abc.net.au/news/2026-08-28/norway-king-harald-dies/107091974",

    "{{WORLD_2_FLAG}}": "🇨🇩 DR CONGO · EBOLA OUTBREAK MAY BE FAR BIGGER THAN REPORTED",
    "{{WORLD_2_HEADLINE}}": "Congo's Record Ebola Outbreak May Be Three Times Worse Than Official Count",
    "{{WORLD_2_SUMMARY}}": "The DRC's Ebola outbreak — already the deadliest in the country's history with 5,794 confirmed cases and 2,786 deaths across 54 health zones — may be undercounted by as much as three times, Africa CDC warns, as a vaccination drive for frontline health workers got under way this week in Kisangani.",
    "{{WORLD_2_URL}}": "https://www.bloomberg.com/news/articles/2026-08-27/congo-ebola-cases-may-be-three-times-higher-than-official-count-africa-cdc-says",

    # Economics
    "{{ECON_1_FLAG}}": "📈 RATES · NAB JOINS CBA, ANZ TIPPING BACK-TO-BACK HIKES",
    "{{ECON_1_HEADLINE}}": "NAB Joins CBA and ANZ in Forecasting Rate Rises to a 15-Year High",
    "{{ECON_1_SUMMARY}}": "NAB has followed CBA and ANZ in tipping the RBA to lift the cash rate in both September and November, potentially to 4.85% — the highest since the GFC — as fuel-driven inflation keeps core price pressure elevated, adding to the cost of carrying equipment finance or a business loan.",
    "{{ECON_1_URL}}": "https://www.savings.com.au/news/nab-tips-september-cash-rate-hike-cba-says-november",

    "{{ECON_2_FLAG}}": "⛽ FUEL · PETROL AVERAGING OVER $2/L AS EXCISE FULLY RETURNS",
    "{{ECON_2_HEADLINE}}": "Melbourne Petrol Prices Push Past $2 a Litre as Full Fuel Excise Bites",
    "{{ECON_2_SUMMARY}}": "With the fuel excise cut fully unwound since 3 August, Melbourne's average unleaded price has climbed to around 206.5 cents a litre — some stations over $2.79 — and the ACCC says it's watching retailers closely for price gouging as trades businesses absorb the extra cost at the bowser.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "⚖️ AI POLICY · JUDGE BLOCKS PENTAGON'S ANTHROPIC BLACKLIST",
    "{{TECH_1_HEADLINE}}": "Federal Judge Rules Pentagon's Blacklisting of Anthropic Was Illegal",
    "{{TECH_1_SUMMARY}}": "A US judge struck down the Defense Department's designation of Anthropic as a \"supply chain risk,\" ruling the administration retaliated against the AI firm for refusing to let its Claude models be used for autonomous weapons or mass surveillance — a case with real implications for how far governments can pressure AI developers on safety terms.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/08/28/judge-blocks-pentagon-blacklist--anthropic-.html",

    "{{TECH_2_FLAG}}": "💬 AI ADOPTION · ONE-THIRD OF US ADULTS NOW ASK AI ABOUT HEALTH",
    "{{TECH_2_HEADLINE}}": "A Third of US Adults Now Use AI Chatbots for Health Questions, Pew Finds",
    "{{TECH_2_SUMMARY}}": "New Pew Research polling finds 34% of Americans have used an AI chatbot for a health-related task — mostly quick symptom checks and low-cost information — though fewer than a third feel comfortable sharing personal health data with the tools, a sign trust is still catching up to adoption.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦆 PHYSICAL AI · HUGGING FACE LAUNCHES $399 OPEN-SOURCE ROBOT",
    "{{ROBOT_1_HEADLINE}}": "Hugging Face Unveils Microduck, a $399 Waddling, Roller-Skating Robot",
    "{{ROBOT_1_SUMMARY}}": "Built with Pollen Robotics, the 25cm open-source biped packs 15 motors, a camera and lidar into a duck-shaped body that can pick up small objects with its beak, recover from falls and even roller-skate — a sign the cost of getting hands-on with real-world robotics keeps dropping fast.",
    "{{ROBOT_1_URL}}": "https://techcrunch.com/2026/08/27/hugging-face-is-selling-a-cute-399-open-source-duck-robot-microduck/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Sends $5 Million in Aid to Nepal as 39 Citizens Remain Missing",
    "{{AUS_1_SUMMARY}}": "The Albanese Government has committed $5 million in flood relief for Nepal-China border communities and deployed extra consular staff, as the number of missing Australians climbed to 39 following the catastrophic glacial flood.",
    "{{AUS_1_URL}}": "https://www.southasiatimes.com.au/south-asia/nepal/nepal-floods-australia-5m-aid-39-missing/",

    "{{AUS_2_HEADLINE}}": "Albanese Intervenes to Guarantee Refugee Intake Stays at 20,000",
    "{{AUS_2_SUMMARY}}": "The Prime Minister personally stepped in this week to reverse a planned cut to Australia's humanitarian intake after a backbench revolt, confirming the 20,000-place annual quota will continue rather than dropping to 13,750.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "CBD Stabbing Victim Speaks Out, Calls for Tougher Consequences for Street Violence",
    "{{VIC_1_SUMMARY}}": "Cherie Holt, stabbed four times and assaulted alongside her 10-year-old son near Victoria Police headquarters this week, has called publicly for tougher penalties, reigniting debate over street violence in Melbourne's CBD.",

    # Science
    "{{SCI_1_FLAG}}": "🚀 SPACE · NASA'S ROMAN TELESCOPE 'GO' FOR SUNDAY LAUNCH",
    "{{SCI_1_HEADLINE}}": "NASA's Roman Space Telescope Cleared for Sunday Launch",
    "{{SCI_1_SUMMARY}}": "NASA and SpaceX have cleared the Nancy Grace Roman Space Telescope for its planned Sunday liftoff on a Falcon Heavy rocket from Kennedy Space Center — a mission with a field of view 100 times wider than Hubble's, expected to detect around 100,000 new exoplanets over its lifetime, more than every previous planet-hunting mission combined.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Petrol Just Cracked $2 a Litre in Melbourne — Is Your Callout Fee Still Doing the Job?",
    "{{INSIGHT_BODY}}": "With the fuel excise fully restored and Melbourne's average unleaded price now sitting above 206 cents a litre, every kilometre between jobs is costing more than it did a month ago. Many small trades operators haven't touched their callout or travel fee since well before this year's excise changes, quietly eating the difference on every job outside their core radius. A quick AI-assisted review of your last three months of job locations against current fuel costs — most accounting or job-management software can now do this in minutes — can show exactly where your travel fee needs to move, before the next fuel jump makes the gap even bigger.",

    # Fun facts
    "{{FACT_1}}": "Sandblasting was patented in 1870 by American engineer Benjamin Chew Tilghman, who got the idea after noticing that windblown desert sand had etched and frosted glass windowpanes — a natural process he then recreated on demand with compressed air.",
    "{{FACT_2}}": "Two years before the Atari 2600, the Fairchild Channel F (1976) was the first home console to use interchangeable ROM game cartridges — but a higher price and Atari's marketing muscle meant it's now largely forgotten outside gaming history circles.",
    "{{FACT_3}}": "The old claim that a duck's quack doesn't echo was debunked in 2003 by University of Salford acoustics engineer Trevor Cox, who recorded a duck inside an anechoic chamber and proved it echoes perfectly well — just too faintly for most people to notice.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pool fencing installer's small business always pass its council inspection on the first try?",
    "{{JOKE_PUNCHLINE}}": "Because he never left a gap — in the fence or the paperwork.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The best way out is always through.\"",
    "{{CLOSING_ATTR}}": "— Robert Frost",
    "{{CLOSING_MESSAGE}}": "It's a showery, blustery Saturday in Carrum Downs with Sunday set to be even wetter before it clears from Monday, so today's a fair one to keep outdoor jobs flexible. With petrol now over $2 a litre and a third big bank tipping a rate rise, it's a good weekend to run the numbers on your travel fees and finance before both costs climb further.",
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
