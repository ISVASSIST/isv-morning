#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 1 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Thu 1 May
    "{{WEATHER_1}}": "Thu · Partly cloudy · 17°C",
    "{{WEATHER_2}}": "Fri · Cloudy · 16°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Sat · Showers · 14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "Sun · Clearing · 15°C",
    "{{WEATHER_5}}": "Mon · Fine · 18°C",
    "{{WEATHER_ALERT}}": "Rain Saturday",

    # World
    "{{WORLD_1_FLAG}}": "🌍 GULF · ENERGY",
    "{{WORLD_1_HEADLINE}}": "UAE Officially Exits OPEC as Iran War Reshapes the Global Oil Order",
    "{{WORLD_1_SUMMARY}}": "The United Arab Emirates formally left OPEC today — effective 1 May — stripping the cartel of its third-largest producer and dealing a heavy blow to Saudi Arabia's grip on oil policy. The exit follows months of tension over production caps and comes as the ongoing US-Israel war on Iran has already slashed OPEC's combined output by nearly 8 million barrels per day.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/4/28/uae-leaves-opec-and-opec",

    "{{WORLD_2_FLAG}}": "👑 ROYALS · GEOPOLITICS",
    "{{WORLD_2_HEADLINE}}": "King Charles Praises AUKUS in Historic Address to US Congress",
    "{{WORLD_2_SUMMARY}}": "In his first speech to a joint session of Congress, King Charles called the AUKUS defence partnership \"ambitious and vital for the Indo-Pacific\", while highlighting the strength of the US–UK–Australia alliance. President Trump called the King \"a fantastic person,\" though relations with UK PM Keir Starmer remain fraught.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/04/28/world/live-news/iran-war-trump-israel",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 AUSTRALIA · FUEL",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Cut Is Delivering Savings — But the Middle East War Is Eating Them Back",
    "{{ECON_1_SUMMARY}}": "Australia's halved fuel excise (26.3 cents per litre off, valid to 30 June) delivered early savings of 20–26 cents per litre at the pump, but surging global crude prices driven by the Iran war have partially clawed those gains back. The ACCC is actively monitoring whether retailers — particularly diesel sellers — are passing on recent falls in international refined fuel prices.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/media-release/accc-monitors-fuel-excise-cut-fuel-surcharges-and-fuel-price-movements",

    "{{ECON_2_FLAG}}": "🏦 AUSTRALIA · RATES",
    "{{ECON_2_HEADLINE}}": "RBA Rate Pause Widely Expected as May Board Meeting Looms Next Week",
    "{{ECON_2_SUMMARY}}": "With the cash rate already raised twice in 2026 to 4.10%, most economists expect the Reserve Bank to hold at its 4–5 May meeting, giving borrowers a short reprieve. Australia's inflation sits at 4.6% — well above the 2–3% target — and the RBA is under pressure to balance cost-of-living relief against energy-driven price pressures.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🇦🇺 AUSTRALIA · AI",
    "{{TECH_1_HEADLINE}}": "MYOB and Microsoft Launch AI Agents for Australian Small Businesses — Cashflow Forecasting to Compliance Nudges",
    "{{TECH_1_SUMMARY}}": "Microsoft confirmed its Agent 365 platform hit general availability today, the same day MYOB began embedding AI agents directly into its accounting software for Australia's 3.28 million SMEs. The agents forecast cash flow, guide compliance readiness, and surface proactive insights — all inside the tools small businesses already use, with no coding required.",
    "{{TECH_1_URL}}": "https://news.microsoft.com/source/asia/2026/04/08/myob-and-microsoft-sign-five-year-strategic-partnership/",

    "{{TECH_2_FLAG}}": "🌐 AI · ENTERPRISE",
    "{{TECH_2_HEADLINE}}": "40% of Enterprise Apps to Feature AI Agents by Year-End — But Only 10% Have Scaled Beyond Pilots",
    "{{TECH_2_SUMMARY}}": "A new cross-industry report finds agentic AI is entering mainstream tools faster than expected, but scaling remains elusive. Just one in ten organisations has moved beyond test deployments — mostly due to governance gaps and hallucination risks. Google Workspace Studio and Anthropic's Managed Agents are among the latest platforms trying to close the gap.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇩🇪 GERMANY · AUTO",
    "{{ROBOT_1_HEADLINE}}": "BMW Puts Humanoid Robots on the Factory Floor in Europe — An Industrial First",
    "{{ROBOT_1_SUMMARY}}": "BMW Group has deployed AEON — a humanoid robot developed by Hexagon Robotics — at its Leipzig plant, marking the first time Physical AI of this kind has entered European automotive production. Two AEON units will work on high-voltage battery assembly and exterior component manufacturing, following a successful US pilot where a humanoid robot logged 1,250 hours and moved over 90,000 sheet metal parts.",
    "{{ROBOT_1_URL}}": "https://www.press.bmwgroup.com/global/article/detail/T0455864EN/bmw-group-to-deploy-humanoid-robots-in-production-in-germany-for-the-first-time?language=en",

    # Australia
    "{{AUS_1_HEADLINE}}": "eSafety Commissioner Stands Firm Despite Wave of Online Threats After Social Media Ban",
    "{{AUS_1_SUMMARY}}": "Australia's eSafety Commissioner says the volume of abuse and threats she has received since implementing the under-16s social media restrictions has only hardened her resolve. \"They only encourage me to dig in,\" she told media. The restrictions remain in force and are being actively enforced.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news",

    "{{AUS_2_HEADLINE}}": "Government Targets Loopholes Letting Tech Giants Dodge Australian News Payments",
    "{{AUS_2_SUMMARY}}": "A new government proposal would close gaps in Australia's news media bargaining code that allow platforms like Meta and Google to avoid triggering mandatory arbitration with publishers. The move comes as concerns grow that major platforms have been renegotiating deals below market rate — or avoiding them altogether.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Victory v Sydney FC: A-League Elimination Final Set for Saturday Night at AAMI Park",
    "{{VIC_1_SUMMARY}}": "Melbourne Victory face Sydney FC in a winner-takes-all A-League Elimination Final on Saturday 2 May, kick-off 7:40pm AEST at AAMI Park. The loser goes home — and with Melbourne's finals record shaky of late, home-ground advantage and a vocal crowd will need to count for something.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 BIOLOGY · MEDICINE",
    "{{SCI_1_HEADLINE}}": "Scientists Crack a 100-Year-Old Problem: How to Freeze Transplant Organs Without Shattering Them",
    "{{SCI_1_SUMMARY}}": "Researchers at Texas A&M University have developed a cryopreservation technique that dramatically reduces the cracking that has plagued frozen organ storage for over a century. By engineering solutions with higher glass transition temperatures, the team may have unlocked a path to organs being preserved for days or weeks rather than hours — potentially transforming transplant waiting lists worldwide.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Job Notes Are a Goldmine — If You Let AI Organise Them",
    "{{INSIGHT_BODY}}": "Most tradies take job notes in their head, on scraps of paper, or in voice memos that never get typed up. That's lost knowledge — and lost time when it comes to quoting similar work, training a new person, or defending a scope-of-work dispute. AI transcription tools like Otter.ai and voice-to-text on your phone now let you speak your notes after a job and have them turned into a clean, searchable summary in seconds. For a blasting and coatings operation, that means every job's surface conditions, product used, square metreage, and hours on-site become a record you can actually find — building the institutional knowledge that lets you quote faster and win more of the right work.",

    # Fun Facts
    "{{FACT_1}}": "A honeybee visits around 2,000 flowers to produce a single teaspoon of honey — and the average worker bee makes only about one-twelfth of a teaspoon in its entire lifetime.",
    "{{FACT_2}}": "Melbourne's tram network is the largest outside of Europe, with over 250 kilometres of track and roughly 1,700 stops — and it's free to ride within the CBD fare zone.",
    "{{FACT_3}}": "Your body contains approximately 37 trillion human cells — but it's home to an estimated 38 trillion bacteria, meaning there are slightly more microbes in you than there are \"you.\"",

    # Joke
    "{{JOKE_SETUP}}": "Why did the tiler refuse to start on the kitchen floor?",
    "{{JOKE_PUNCHLINE}}": "He had too many grout expectations.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Do what you can, with what you have, where you are.\"",
    "{{CLOSING_ATTR}}": "Theodore Roosevelt",
    "{{CLOSING_MESSAGE}}": "It's Thursday — the first day of May — and the global energy order just shifted again with the UAE walking out of OPEC this morning. Closer to home, showers are due Saturday, so if outdoor blasting work is on the schedule this week, tomorrow's cool dry morning is your best window. RBA rate decision lands Tuesday. Good week to get a step ahead.",
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
