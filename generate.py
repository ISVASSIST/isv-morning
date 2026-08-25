#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 26 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 26 Aug (BOM)
    "{{WEATHER_1}}": "WED 26 · ⛅ Partly cloudy, mostly dry with a slight chance of a shower · 13–21°C",
    "{{WEATHER_2}}": "THU 27 · 🌫️ Partly cloudy, chance of morning fog in the north-east suburbs · 8–15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 28 · ⛅ Partly cloudy, mild · 9–18°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 29 · 🌧️ Showery and windy, southwesterly winds gusting to 25km/h · 7–11°C",
    "{{WEATHER_5}}": "SUN 30 · ⛅ Partly cloudy, clearing · 8–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or Carrum Downs. This week is mostly dry and mild, with a cold, showery, windy change moving through Saturday — today through Friday are your best outdoor coating and blasting windows before the weekend cool-down.",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 UKRAINE · WORLD-FIRST ALL-ROBOT INDEPENDENCE DAY PARADE",
    "{{WORLD_1_HEADLINE}}": "Ukraine Replaces Marching Soldiers With Robots and Drones in World-First Independence Day Parade",
    "{{WORLD_1_SUMMARY}}": "Ukraine marked 35 years of independence with what President Volodymyr Zelenskyy called the world's first all-drone parade, sending dozens of unmanned ground vehicles built for combat, logistics and casualty evacuation down Kyiv's main street, alongside naval drones on the Dnipro River and bomber and interceptor drones overhead — a deliberate substitute for the tanks and marching troops of past years.",
    "{{WORLD_1_URL}}": "https://www.abc.net.au/news/2026-08-25/ukraine-drone-robot-parade-on-independence-day/107074202",

    "{{WORLD_2_FLAG}}": "🔥 INDONESIA · WILDFIRE HAZE CHOKES SUMATRA AND BORNEO",
    "{{WORLD_2_HEADLINE}}": "Indonesians Pray for Rain as Wildfire Haze From Over 10 Provinces Blankets Cities",
    "{{WORLD_2_SUMMARY}}": "Peatland and forest fires across Sumatra and Kalimantan have pushed hazardous haze into cities including Palembang, where about 3,000 residents gathered for a special rain prayer, as authorities deploy dozens of aircraft for cloud-seeding and water-bombing and have arrested 72 people suspected of deliberately lighting fires to clear land.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/08/25/nx-s1-5944062/indonesians-brave-choking-smoke-to-pray-for-rain-as-country-battles-wildfires",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL · MELBOURNE AVERAGE HOLDS AROUND $2.01 A LITRE",
    "{{ECON_1_HEADLINE}}": "Melbourne Unleaded Averages $2.01, With a Wide Spread Between the City's Cheapest and Priciest Bowsers",
    "{{ECON_1_SUMMARY}}": "Melbourne's average unleaded price sits around 201.2c/L today, with the cheapest reported price 184.5c/L at a members-only Preston station — independents and discount chains in outer suburbs like Dandenong, Sunshine and Broadmeadows are typically the best value for everyone else, worth a small detour before topping up the ute this week.",
    "{{ECON_1_URL}}": "https://fuelradar.com.au/fuel-prices/vic/melbourne",

    "{{ECON_2_FLAG}}": "🛒 RETAIL · COLES SETS ASIDE $235M OVER WORKER UNDERPAYMENTS",
    "{{ECON_2_HEADLINE}}": "Coles Posts $1.1 Billion Profit But Sets Aside $235 Million to Fix Underpaid Staff",
    "{{ECON_2_SUMMARY}}": "Coles reported a $1.1 billion full-year profit and a bigger dividend for shareholders, even as it put aside $235 million to address staff underpayments uncovered internally — a reminder that even sophisticated payroll systems at Australia's biggest employers can get award rates and entitlements wrong.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💻 AI PRICING · NVIDIA HIKES AI SERVER CHIP PRICES OVER 15%",
    "{{TECH_1_HEADLINE}}": "Nvidia Tells Customers Its AI Server Chip Prices Are Rising More Than 15%",
    "{{TECH_1_SUMMARY}}": "Nvidia has notified major customers that server systems built on its AI chips, including the upcoming Vera Rubin platform, will cost more than 15% more from early 2027 — a sign the underlying cost of AI compute keeps climbing even as the tools built on top of it get cheaper to use, and a reason to lock in current software pricing where you can.",
    "{{TECH_1_URL}}": "https://finance.yahoo.com/technology/ai/articles/nvidia-says-raising-prices-more-224321093.html",

    "{{TECH_2_FLAG}}": "🤖 AI TOOLS · CHATGPT REINSTATES USAGE CAPS FOR PLUS USERS",
    "{{TECH_2_HEADLINE}}": "OpenAI Brings Back a 5-Hour Usage Limit for ChatGPT Plus's Work and Coding Tools",
    "{{TECH_2_SUMMARY}}": "After six weeks of unrestricted access, OpenAI has reinstated a rolling five-hour usage cap on ChatGPT Plus's \"Work\" agent and Codex coding tool from today, while higher-tier Pro, Enterprise and Edu accounts are unaffected — worth knowing if you're leaning on the free-flowing version of ChatGPT to draft quotes, emails or job notes.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦿 HUMANOID ROBOTS · XPENG'S ROBOTICS ARM RAISES $900M+",
    "{{ROBOT_1_HEADLINE}}": "Xpeng's Robotics Unit Raises Over $900 Million in China's Largest-Ever Embodied AI Funding Round",
    "{{ROBOT_1_SUMMARY}}": "Xpeng's robotics division has raised more than US$900 million at a US$6.3 billion valuation, backed by Alibaba, Tencent and IDG Capital, as it pushes its IRON humanoid toward mass production by the end of 2026 — the largest single private funding round yet recorded in China's humanoid robotics industry.",
    "{{ROBOT_1_URL}}": "https://electrek.co/2026/08/24/xpeng-robotics-900m-iron-humanoid-robot-valuation/",

    # Australia
    "{{AUS_1_HEADLINE}}": "BHP and Port Hedland Unions Head Back to the Table After Failing to Reach a Wage Deal",
    "{{AUS_1_SUMMARY}}": "Talks between BHP and the Combined BHP Ports Unions resumed today after months of failed negotiations over a new pay deal for around 450 operators and maintenance staff at the Port Hedland iron ore terminal, with a union counterproposal now on the table ahead of further Fair Work Commission-backed talks in September.",
    "{{AUS_1_URL}}": "https://www.miningweekly.com/article/port-hedland-unions-place-wage-deal-counterproposal-to-bhp-ahead-of-september-8-talks-2026-08-25",

    "{{AUS_2_HEADLINE}}": "Brisbane Bans Smart Glasses and Cameras From Filming People at Council Pools Without Consent",
    "{{AUS_2_SUMMARY}}": "Brisbane City Council has banned the non-consensual use of camera-enabled smart glasses, phones and action cameras at its public pools, giving lifeguards the power to eject anyone filming other patrons without permission — a response to swimmers' growing unease about covert recording devices.",
    "{{AUS_2_URL}}": "https://www.abc.net.au/news/2026-08-25/brisbane-bans-non-consensual-filming-at-public-pools/107075886",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Apprentice Numbers Keep Falling in Victoria, With About Half Quitting Before They Finish",
    "{{VIC_1_SUMMARY}}": "New national data shows Victorian trade apprenticeship commencements have fallen to their lowest level since 2001, with about half of all apprentices nationally now dropping out before completing their training — researchers point to low pay, weak mentoring and long regional travel times as the main drivers.",

    # Science
    "{{SCI_1_FLAG}}": "🦅 WILDLIFE HEALTH · BACKYARD BIRD FEEDERS FLAGGED AS BIRD FLU RISK",
    "{{SCI_1_HEADLINE}}": "Backyard Bird Feeders Could Become Unexpected H5N1 Hotspots as Bird Flu Spreads",
    "{{SCI_1_SUMMARY}}": "Researchers warn that backyard bird feeders and baths may be inadvertently helping Australia's H5N1 bird flu outbreak spread, by drawing together wild bird species that would rarely otherwise mix — a reminder to clean feeders regularly and space them out if you keep any near the workshop or yard.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Coles Just Set Aside $235 Million for Underpaying Staff — Could an AI Payroll Check Catch Your Mistake First?",
    "{{INSIGHT_BODY}}": "Even Coles, with a payroll department and enterprise software most small operators could only dream of, has just put aside $235 million to fix staff it underpaid — proof that award rates, allowances and overtime rules are genuinely easy to get wrong, not just a \"big business\" problem. For a trades operator running casuals, apprentices and subbies across different rates and hours, an AI-assisted payroll check — feeding your timesheets and the relevant award into a tool built for the job — can flag mismatches between what's owed and what's paid before the ATO or Fair Work does. It's a task that takes minutes, not days, and a lot cheaper than a backpay bill with your name on it.",

    # Fun facts
    "{{FACT_1}}": "The AI term \"hallucination\" didn't start with chatbots — computer vision researchers were using it back in the 2000s to describe image-processing software that \"hallucinated\" plausible-looking details into blurry or low-resolution photos, decades before it came to mean an AI confidently inventing a fake court case.",
    "{{FACT_2}}": "Garnet, now one of the most common abrasives for blasting and waterjet cutting, only became an industrial material by accident — New York's Barton family started commercially mining it in the 1870s after noticing it was tough enough to shred the sandpaper being used to grind it smooth.",
    "{{FACT_3}}": "VisiCalc, released for the Apple II in 1979, is credited as the world's first spreadsheet program and the software that convinced small businesses a computer was worth buying — inventor Dan Bricklin said the idea came to him while watching a professor erase and rewrite numbers on a classroom blackboard.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the EV charger installer never stress about a slow week?",
    "{{JOKE_PUNCHLINE}}": "He always had a few jobs charging quietly in the background.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Obstacles are those frightful things you see when you take your eyes off your goal.\"",
    "{{CLOSING_ATTR}}": "— Henry Ford",
    "{{CLOSING_MESSAGE}}": "It's a mild, mostly dry Wednesday in Carrum Downs before the week turns wet and windy again on Saturday, so today through Friday are the ones to make the most of outdoors. Between Coles' $235 million payroll bill, Victoria's shrinking apprentice pipeline and Nvidia's chip prices climbing again, it's a fair day to double check your own numbers are holding up as well as the headlines suggest.",
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
