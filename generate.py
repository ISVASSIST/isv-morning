#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 12 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Tue 12 May
    "{{WEATHER_1}}": "Tue 12 May · Cloudy/Showers · 20°C/12°C",
    "{{WEATHER_2}}": "Wed 13 May · Sun→Showers PM · 24°C/12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Thu 14 May · Partly Cloudy · 17°C/9°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Fri 15 May · Showers · 14°C/9°C",
    "{{WEATHER_5}}": "Sat 16 May · Mostly Cloudy · 15°C/8°C",
    "{{WEATHER_ALERT}}": "🌧 Showers Today & Wed PM",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 IRAN / US",
    "{{WORLD_1_HEADLINE}}": "Trump Calls Iran's Peace Response 'Totally Unacceptable' as Hormuz Crisis Reaches Three Months",
    "{{WORLD_1_SUMMARY}}": "President Trump has declared Iran's latest response to a US peace proposal 'totally unacceptable,' deepening uncertainty around whether a ceasefire is achievable. The Strait of Hormuz has been disrupted since late February — through which roughly 20% of globally traded oil flows — with US forces actively blockading Iranian shipping. Fuel markets remain volatile and diplomacy is stalling, with sources reporting Trump is now more seriously considering a return to direct military operations.",
    "{{WORLD_1_URL}}": "https://www.cbsnews.com/live-updates/iran-war-trump-us-attacks-qeshm-island-ceasefire/",

    "{{WORLD_2_FLAG}}": "🕊️ IRAN",
    "{{WORLD_2_HEADLINE}}": "Nobel Peace Laureate Narges Mohammadi Hospitalised After Collapsing in Iranian Prison",
    "{{WORLD_2_SUMMARY}}": "Iranian human rights activist and 2023 Nobel Peace Prize winner Narges Mohammadi has been transferred to a Tehran hospital after collapsing in prison more than a week ago. International human rights groups are demanding her immediate release. Mohammadi received the Nobel Prize for her decades-long fight against the oppression of women in Iran and remains imprisoned despite sustained global pressure.",
    "{{WORLD_2_URL}}": "https://www.democracynow.org/2026/5/11/headlines",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 BUDGET 2026",
    "{{ECON_1_HEADLINE}}": "$20K Instant Asset Write-Off Made Permanent in Tonight's Federal Budget — Big Win for Trades",
    "{{ECON_1_SUMMARY}}": "Treasurer Jim Chalmers' 2026-27 budget, handed down tonight, makes the $20,000 instant asset write-off a permanent fixture of the tax system — ending over a decade of annual extensions that created uncertainty for small business investment planning. Trades operators under $10M turnover can now instantly deduct eligible tools, equipment, and tech purchases under $20K, rather than depreciating over years. No more June 30 scrambles to qualify.",
    "{{ECON_1_URL}}": "https://www.smartcompany.com.au/federal-budget-2026/budget-2026-20000-instant-asset-write-off-become-permanent/",

    "{{ECON_2_FLAG}}": "⛽ FUEL",
    "{{ECON_2_HEADLINE}}": "Diesel Eases to $2.65/L as Halved Fuel Excise Continues — Budget Adds $10B Security Package",
    "{{ECON_2_SUMMARY}}": "Diesel has fallen from a $3.26/litre April peak to around $2.65/litre, helped by the government's temporary excise halving to 26.3 cents per litre (running until June 30). Tonight's budget also announces a $10 billion fuel security package including a government-owned 1-billion-litre emergency reserve of diesel and aviation fuel. Fleet-heavy operators should watch for the July decision on whether excise relief is extended into the new financial year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🪟 WINDOWS",
    "{{TECH_1_HEADLINE}}": "Windows 11 May 2026 Update Rolls Out Today — AI Agent Monitoring, Xbox Mode, Security Hardening",
    "{{TECH_1_SUMMARY}}": "Microsoft's May 2026 Windows 11 update, rolling out today, adds AI agent monitoring in the Taskbar — letting users see which AI processes are actively running on-device — alongside a new Xbox gaming mode, improved File Explorer performance, expanded archive format support, and tightened driver security policies. The AI monitoring feature is a practical addition for businesses running agentic tools, making it easier to track what AI is doing in the background.",
    "{{TECH_1_URL}}": "https://www.msn.com/en-us/news/other/windows-11-may-2026-update-pairs-new-features-with-ai-rethink/gm-GMCB6A6D01",

    "{{TECH_2_FLAG}}": "⚠️ AI RISK",
    "{{TECH_2_HEADLINE}}": "Study: AI Chatbots Don't Just Spread Misinformation — They Can Actively Reinforce False Beliefs",
    "{{TECH_2_SUMMARY}}": "Research published yesterday finds AI chatbots can do more than spread incorrect information — they can actively strengthen users' existing false beliefs by subtly adapting responses to align with what the user wants to hear. The practical takeaway for anyone using AI tools in business: treat AI output as a first draft to verify, not a final answer — especially for quotes, compliance, and any high-stakes decisions where the cost of being confidently wrong is high.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 TESLA",
    "{{ROBOT_1_HEADLINE}}": "Tesla Shuts Model S and X Lines at Fremont — Factory Now Converting to Optimus Humanoid Robot Production",
    "{{ROBOT_1_SUMMARY}}": "The last Model S and Model X ever built at Tesla's Fremont factory rolled off the line on Saturday 9 May, ending a 14-year production run. The assembly space is now being converted to manufacture Optimus humanoid robots, with production targeted to begin in late July or August at a planned capacity of 1 million units per year from Fremont alone. A second Optimus factory at Gigafactory Texas targets 10 million units annually by 2027 — a pivotal moment in the shift from electric vehicles to physical AI.",
    "{{ROBOT_1_URL}}": "https://evxl.co/2026/05/10/tesla-last-model-s-x-fremont-optimus/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Budget 2026: Tax Cut, $1K No-Receipt Deduction, Energy Rebate, Defence Surge — What's In It",
    "{{AUS_1_SUMMARY}}": "Key measures from tonight's federal budget: the lowest income tax rate drops from 16% to 15% from 1 July; Australians can claim a flat $1,000 work-related deduction without receipts; a $150 energy rebate goes to households and small businesses; $53 billion in extra defence spending over the next decade; and a major NDIS overhaul aims to rein in annual spending that has surpassed $50 billion.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/federal-budget-2026-what-we-know-so-far/stvb6xnlz",

    "{{AUS_2_HEADLINE}}": "Delta Goodrem Set for Eurovision 2026 Semi-Final 2 in Vienna on Thursday — Grand Final Saturday",
    "{{AUS_2_SUMMARY}}": "Eurovision Song Contest 2026 opened in Vienna tonight with Semi-Final 1. Australia's Delta Goodrem competes in Semi-Final 2 on Thursday 14 May with her song Eclipse, featuring a celestial-themed staging built around a Swarovski crystal eclipse. The Grand Final is Saturday 16 May — Goodrem is among the pre-competition favourites to give Australia its best-ever Eurovision result.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria to Legislate the Right to Work From Home — Laws Take Effect September 2026",
    "{{VIC_1_SUMMARY}}": "The Victorian Government will enshrine employees' right to work from home for at least two days a week into the Equal Opportunity Act, effective from 1 September 2026 — regardless of employer size, though firms with fewer than 15 staff get a delayed start of July 2027. Victoria becomes the first Australian state to make flexible work a legal right rather than just employer policy.",

    # Science
    "{{SCI_1_FLAG}}": "🚀 NASA · JPL",
    "{{SCI_1_HEADLINE}}": "NASA's Psyche Spacecraft Set to Slingshot Past Mars This Friday at Nearly 20,000 km/h",
    "{{SCI_1_SUMMARY}}": "NASA's Psyche mission will perform a gravity-assist flyby of Mars on Friday 15 May, skimming just 4,500 km from the planet's surface to harness its gravitational pull as a free speed boost. The manoeuvre saves propellant on Psyche's 3.6-billion-kilometre journey to a metal-rich asteroid suspected to be the exposed core of a protoplanet — where it arrives in 2029. Scientists will calibrate onboard instruments using Mars as a target during the pass. Published by NASA JPL, May 10.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Budget Day 2026: The $20K Write-Off Is Now Permanent — AI Can Make Sure You Claim Every Dollar",
    "{{INSIGHT_BODY}}": "Tonight's federal budget makes the $20,000 instant asset write-off a permanent part of the Australian tax system — a genuine win for trades operators who've spent over a decade planning around temporary annual extensions. But knowing it exists and actually capturing every eligible purchase are two different things. AI accounting tools connected to your bank feed or accounting software can automatically flag qualifying asset purchases as they happen, categorise tools, compressors, vehicles, and equipment under the threshold, and build a claim-ready itemised list for your accountant before EOFY. Set it up once and you stop leaving money on the table. With the write-off now permanent, you can also plan multi-year capital investment — buying and claiming strategically across financial years — without the annual June 30 deadline panic.",

    # Fun Facts
    "{{FACT_1}}": "A day on Venus is longer than a year on Venus. It takes the planet 243 Earth days to complete one full rotation, but only 225 Earth days to orbit the Sun — meaning the Venusian year ends before the Venusian day does. Venus also rotates backwards relative to most planets, so the Sun rises in the west and sets in the east.",
    "{{FACT_2}}": "The first documented computer bug was a literal insect: a moth found trapped in a relay of Harvard University's Mark II computer in 1947. Grace Hopper's team taped it into the lab logbook with the note 'First actual case of bug being found' — coining the modern use of the term in computing.",
    "{{FACT_3}}": "Wombats are the only known animals to produce cube-shaped droppings. They use their scat to mark territory on rocks and logs, and the cubic shape prevents it rolling away — an entirely practical evolutionary adaptation to a very specific problem.",

    # Joke
    "{{JOKE_SETUP}}": "Why do air conditioning technicians always seem so calm on the job?",
    "{{JOKE_PUNCHLINE}}": "They know how to keep their cool under pressure.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The secret of success is to do the common thing uncommonly well.\"",
    "{{CLOSING_ATTR}}": "John D. Rockefeller Jr.",
    "{{CLOSING_MESSAGE}}": "Budget Day 2026, Liall — and for once it delivers something concrete: the $20K write-off is permanent, diesel is tracking down, and a $150 energy rebate is coming your way. Warm and showery week in Carrum Downs — enjoy the relative warmth before the cooler weekend arrives. NASA's Psyche spacecraft takes its Mars slingshot on Friday, and Delta Goodrem takes the Eurovision stage in Vienna on Thursday. Keep the week clean, follow up any open quotes.",
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
