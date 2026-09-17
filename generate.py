#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 18 September 2026",

    # Weather — Carrum Downs / Melbourne bayside, 5-day from Fri 18 Sep
    "{{WEATHER_1}}": "FRI 18 SEP · 🌤️ Mostly sunny, patchy morning fog/frost near the hills easing by mid-morning, winds N–NW 15–25km/h · 7–22°C",
    "{{WEATHER_2}}": "SAT 19 SEP · ☀️ Sunny, winds northerly 20–30km/h · 12–25°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SUN 20 SEP · ☀️ Mostly sunny, winds N–NW shifting SW later · 14–24°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 21 SEP · ☁️ Cloudy, cooler change moves through, winds SW 15–25km/h · 11–15°C",
    "{{WEATHER_5}}": "TUE 22 SEP · 🌤️ Partly cloudy, slight chance of a shower, winds S–SW 15–20km/h · 8–17°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — today's fog clears into a sunny, near-25°C weekend before a cooler change with cloud moves in Monday.",

    # World
    "{{WORLD_1_FLAG}}": "🇨🇦🇪🇺 CANADA–EU · CARNEY EMBRACES VON DER LEYEN'S OFFER TO MAKE CANADA THE BLOC'S FIRST 'ASSOCIATE MEMBER'",
    "{{WORLD_1_HEADLINE}}": "Carney Welcomes EU's 'Associate Member' Offer for Canada, Says Deeper Ties Stop Any Country 'Controlling Our Markets'",
    "{{WORLD_1_SUMMARY}}": "Addressing the European Parliament in Strasbourg, Canadian PM Mark Carney embraced Ursula von der Leyen's proposal to make Canada the EU's first-ever associate member, floating deeper integration on trade, defence, critical minerals, AI, energy and space — a direct response to Trump-era tariffs and talk of Canada becoming the '51st state.'",
    "{{WORLD_1_URL}}": "https://www.cnbc.com/2026/09/17/carney-canada-eu-associate-member.html",

    "{{WORLD_2_FLAG}}": "🇸🇪 SWEDEN · LEFT-WING BLOC SEALS NARROW ELECTION WIN, PM TO RESIGN",
    "{{WORLD_2_HEADLINE}}": "Sweden's Prime Minister Says He Will Resign After Left-Wing Bloc Narrowly Wins General Election",
    "{{WORLD_2_SUMMARY}}": "Sweden's governing coalition conceded defeat after a knife-edge result handed the left-wing opposition a narrow majority, with weeks of coalition negotiations expected before a new government can be sworn in.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/9/17/sweden-prime-minister-to-resign-as-left-wing-bloc-seals-narrow-election-win",

    # Economics
    "{{ECON_1_FLAG}}": "📈 MARKETS · ASX CLIMBS AS RBA RATE-HIKE ODDS RISE AFTER THE FED MOVES",
    "{{ECON_1_HEADLINE}}": "ASX Adds 0.4% to a Six-Week High as Markets Price in Near-90% Chance of an RBA Rate Hike This Month",
    "{{ECON_1_SUMMARY}}": "The ASX 200 closed up 0.4% at 8,732 on Thursday even as traders priced in a near-90% chance the Reserve Bank lifts rates later this month, after the US Federal Reserve's unanimous 25-basis-point hike overnight — a reminder that equipment finance and overdraft costs could tighten again before Christmas.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-17/asx-markets-business-live-news-september-19-2026/107162296",

    "{{ECON_2_FLAG}}": "⛽ FUEL · DIESEL PUSHES TOWARD $2.70 A LITRE AS AVERAGE PUMP PRICES KEEP CLIMBING",
    "{{ECON_2_HEADLINE}}": "National Average Diesel Price Climbs to Almost $2.69 a Litre, Unleaded Above $2.25, as Fuel Costs Keep Squeezing Trade Vehicles",
    "{{ECON_2_SUMMARY}}": "The latest fuel price tracking has diesel averaging around 268.9 cents a litre and 91-octane unleaded around 225.4 cents nationally, both up sharply on where they sat a fortnight ago — meaning the fuel line on a standing quote is worth another look before it eats into margin.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI TOOLS · ANTHROPIC MERGES CHAT AND COWORK, ADDS FREE DOCS AND SLIDES",
    "{{TECH_1_HEADLINE}}": "Anthropic Folds Claude Chat and Cowork Into One Interface, Adds Built-In Docs and Slides Tools",
    "{{TECH_1_SUMMARY}}": "Claude's chat, Cowork and Artifacts workspace are now one interface that automatically routes each request, with new Docs and Slides tools joining the Claude Design feature launched earlier this year — meaning a quote, a toolbox talk or a client one-pager can now be drafted and formatted without leaving the chat window or buying separate software.",
    "{{TECH_1_URL}}": "https://www.thestar.com.my/tech/tech-news/2026/09/17/anthropic-to-fold-claude-ai-features-into-one-interface-launches-document-tools",

    "{{TECH_2_FLAG}}": "👑 AI SAFETY · KING CHARLES WARNS GLOBAL AI LEADERS OF 'EXISTENTIAL DANGERS'",
    "{{TECH_2_HEADLINE}}": "King Charles Hosts OpenAI, Anthropic, Nvidia and Google DeepMind Leaders, Warns of AI's 'Existential Dangers'",
    "{{TECH_2_SUMMARY}}": "Charles convened AI industry leaders at his Dumfries House estate in Scotland to press the case for guardrails before the most powerful systems become too capable to rein in — a governance push that echoes Anthropic's own recent calls to slow the frontier down.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🧠 ROBOT CHIPS · CHINA'S D-ROBOTICS RAISES $400M TO BUILD 'THE BRAIN FOR EVERY ROBOT'",
    "{{ROBOT_1_HEADLINE}}": "D-Robotics Closes $400 Million Series C, China's Largest Robotics Funding Round in Four Years",
    "{{ROBOT_1_SUMMARY}}": "The Chinese robot-chip and software maker will use the funding to expand its Sunrise chip lineup — already shipped in more than 8 million units — and build a software platform spanning everything from mature robot categories to general-purpose humanoids, underlining how much of the coming robot boom is being built on Chinese silicon.",
    "{{ROBOT_1_URL}}": "https://theaiinsider.tech/2026/09/17/chinas-d-robotics-raises-400m-in-series-c-funding-to-expand-ai-robotics-platform/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Business Groups and Miners Welcome Labor's Migration Overhaul, But Farmers Warn of Worse Labour Shortages",
    "{{AUS_1_SUMMARY}}": "A day after Tony Burke unveiled the government's migration changes, business groups, miners and the housing industry welcomed the shake-up, while the National Farmers Federation warned it puts food security and regional economies at risk.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-18/business-groups-and-miners-welcome-labors-migration-policies/107163600",

    "{{AUS_2_HEADLINE}}": "Bigger, Taller Vehicles Linked to Higher Pedestrian Death Risk in New 13-Year Australian Crash Study",
    "{{AUS_2_SUMMARY}}": "Melbourne University researchers examined more than 10,000 Victorian crashes from 2012 to mid-2025 and found every 10cm of extra vehicle height raised the odds of a pedestrian fatality by 11% — a risk that showed up specifically for women and children as utes and SUVs have replaced sedans.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Australia's Biggest Wind Farm to Double in Size as a Quarter of Its Output Goes Straight to Data Centres",
    "{{VIC_1_SUMMARY}}": "The Golden Plains Wind Farm near Geelong — already the largest in the Southern Hemisphere and good for about 9% of Victoria's annual power demand — is expanding from 756 megawatts to 1.3 gigawatts, with Amazon and Equinix locking up more than a quarter of the extra capacity for their data centres.",

    # Science
    "{{SCI_1_FLAG}}": "❄️ PLANETARY SCIENCE · NEW HORIZONS SPOTS SIGNS OF LIQUID NITROGEN FLOWING ON PLUTO'S SURFACE",
    "{{SCI_1_HEADLINE}}": "NASA's New Horizons Finds First Evidence of Liquid Recently Flowing on Pluto's Surface",
    "{{SCI_1_SUMMARY}}": "Southwest Research Institute scientists comparing New Horizons images to Greenland ice-sheet imagery found dark, damp-looking features on the edge of Pluto's heart-shaped glacier, most likely liquid nitrogen seeping up from below — the first sign that any liquid has moved across Pluto's surface in the probe's decade of observations.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Claude Just Got One Interface for Everything — Docs and Slides Are Now Built Straight Into the Chat",
    "{{INSIGHT_BODY}}": "Anthropic has folded its separate Cowork and Artifacts tools into the main Claude chat window, adding ready-made Docs and Slides features alongside the Claude Design tool from earlier this year — so instead of switching apps to format a quote, write up a toolbox talk or put together a one-page client proposal, it's now one conversation that produces a finished document. For a business running on a laptop and a phone rather than a full office software stack, that's one less subscription to juggle and one less reason paperwork waits until Sunday night. It's rolling out to Pro and Max plans over the coming weeks — worth a look next time a job needs a proper write-up, not just a text message.",

    # Fun facts
    "{{FACT_1}}": "Sweden elects its parliament using the 'modified Sainte-Laguë method', a proportional system specifically designed so the biggest party can't scoop up extra seats — which is exactly why this week's wafer-thin left-wing election win still leaves weeks of coalition haggling before anyone can actually govern.",
    "{{FACT_2}}": "Liquid nitrogen can only exist on Earth in a narrow band between about -210°C and -196°C — so when NASA's New Horizons probe spotted signs of it recently flowing across Pluto's icy heart, it meant enough geothermal heat is escaping from 5.9 billion kilometres out to keep a liquid moving on one of the coldest surfaces in the solar system.",
    "{{FACT_3}}": "The Golden Plains Wind Farm west of Geelong, about to double in size, is already the single largest wind farm anywhere in the Southern Hemisphere — and on its own supplies close to 9% of all the electricity Victoria uses in a year.",

    # Joke
    "{{JOKE_SETUP}}": "A concrete resurfacing contractor was asked how his small business always kept every quote rock solid, even when clients tried to talk him down on price.",
    "{{JOKE_PUNCHLINE}}": "He said he never let the numbers crack under pressure.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"A goal properly set is halfway reached.\"",
    "{{CLOSING_ATTR}}": "— Zig Ziglar",
    "{{CLOSING_MESSAGE}}": "It's Friday, and Carrum Downs should shake off this morning's fog for a sunny run into the weekend, with the mercury pushing 25°C by Saturday. Worth a beat to see whether Anthropic's newly merged Claude interface can take one piece of paperwork off your plate before you clock off — and keep an eye on the fuel line in any quote going out today, with diesel still sitting north of $2.60 a litre.",
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
