#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 12 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 12 Jul (BOM)
    "{{WEATHER_1}}": "SUN 12 · ☀️ Clear, mild · 3–15°C",
    "{{WEATHER_2}}": "MON 13 · ❄️ Frost early, partly cloudy · 2–17°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "TUE 14 · 🌧️ Showers, windy N'ly · 9–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 15 · 🌧️ Showers, windy N'ly · 8–14°C",
    "{{WEATHER_5}}": "THU 16 · ☁️ Cloudy, showers likely · 9–14°C",
    "{{WEATHER_ALERT}}": "⚠ FROST RISK MONDAY MORNING · DAMAGING WINDS & SHOWERS BUILD FROM TUESDAY",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷🇺🇸 IRAN · US · HORMUZ STANDOFF DRAGS INTO NEW WEEK",
    "{{WORLD_1_HEADLINE}}": "US Demands Iran Publicly Guarantee Safe Passage Through the Strait of Hormuz",
    "{{WORLD_1_SUMMARY}}": "Washington is pushing Tehran to publicly commit to leaving the Strait of Hormuz open and dropping any talk of tolls, as Iranian and Omani officials met in Muscat to discuss \"appropriate mechanisms\" for safe shipping through the waterway that carries a fifth of the world's traded oil. President Trump has warned \"1,000 missiles\" are ready if Iran acts on threats against him, even as CNN reports US intelligence has found no evidence of a specific new assassination plot — a reminder the ceasefire remains fragile heading into another week.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/liveblog/2026/7/11/iran-war-live-us-demands-iran-publicly-state-strait-of-hormuz-open-for-all",

    "{{WORLD_2_FLAG}}": "🇺🇸 US · ENVIRONMENT · ENDANGERED SPECIES ACT NARROWED",
    "{{WORLD_2_HEADLINE}}": "Trump Administration Rolls Back a Key Habitat Protection for Endangered Wildlife",
    "{{WORLD_2_SUMMARY}}": "A rule finalised Friday narrows the definition of \"harm\" under the Endangered Species Act, meaning oil and gas drilling, mining and logging can now go ahead on critical habitat as long as the animals themselves aren't directly killed or injured. Environmental groups including Earthjustice say the change — first proposed in 2025 — opens the door to habitat destruction that could push already-vulnerable species toward extinction, and are preparing a legal challenge.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/07/11/nx-s1-5890025/trump-administration-imperiled-wildlife",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · ACCC · BOWSER PRICES CLIMBING AGAIN",
    "{{ECON_1_HEADLINE}}": "ACCC's Latest Weekly Report Confirms Petrol and Diesel Prices Rising as Excise Relief Halves",
    "{{ECON_1_SUMMARY}}": "The ACCC's 18th weekly fuel monitoring report, covering the week to 8 July, shows retail petrol and diesel prices continuing to climb in capital cities and most regional areas now that the excise cut has stepped down from 32c to 16c a litre — with the discount disappearing entirely from 2 August. Worth locking in a fuel surcharge line in every quote over the next few weeks rather than absorbing the difference on jobs already priced.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🏦 RBA WATCH · WESTPAC · CUTS PUSHED BACK TO 2027, NOT BROUGHT FORWARD",
    "{{ECON_2_HEADLINE}}": "Westpac Now Expects One More RBA Rate Rise Before Any Cuts Arrive in 2027",
    "{{ECON_2_SUMMARY}}": "Westpac's chief economist has pushed her forecast for the RBA's first rate cut out to August 2027, still tipping a hike as likely next month and a second in September as inflation proves stickier than hoped. For anyone with equipment finance or a business loan on variable rates, it's a signal to plan for borrowing costs staying elevated well into next year rather than banking on relief any time soon.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🕶️ WEARABLE TECH · SMART GLASSES · PRIVACY OVER RECORDING",
    "{{TECH_1_HEADLINE}}": "New Camera-Free Smart Glasses Bet That Productivity Beats Recording Everyone Around You",
    "{{TECH_1_SUMMARY}}": "Even Realities' new G2 glasses skip the camera and speaker entirely, using a monochrome heads-up display to show notes, directions and messages without anyone nearby worrying they're being filmed — a deliberate contrast to the camera-first smart glasses race. For a trades business, it's an early sign hands-free tech is heading toward quietly useful (checklists, measurements, job notes in your eyeline) rather than gimmicky.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/07/11/smart-glasses-without-a-camera-even-realities-bets-productivity-beats-recording-everyone/",

    "{{TECH_2_FLAG}}": "🤖 AI AGENTS · $100M FUNDRAISE ON AUTOPILOT",
    "{{TECH_2_HEADLINE}}": "AI Agent Startup Let Its Own Agent Run Its $100 Million Fundraising Round",
    "{{TECH_2_SUMMARY}}": "An AI agent startup handed its own software the job of managing investor outreach, scheduling and follow-up for a $100 million raise — a striking, if extreme, example of founders trusting agents with genuinely high-stakes admin rather than just drafting emails. It's a useful data point for any business owner wondering how far \"let the AI handle it\" can realistically go before a human needs to step back in.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "✋ ROBOTICS · HUMANOID HANDS · NEAR-HUMAN DEXTERITY",
    "{{ROBOT_1_HEADLINE}}": "1X Unveils a Tendon-Driven Robot Hand That Can Pour Tea, Zip a Jacket and Sort Grapes",
    "{{ROBOT_1_SUMMARY}}": "1X Technologies' new hand for its Neo humanoid packs 25 degrees of freedom and high-resolution tactile sensors into a tendon-driven design accurate to within 0.2mm, letting it manage fiddly tasks like zippers and stacking coins that have tripped up earlier robot hands. The company says it's already tooled up to build 10,000 units a year — a reminder that the bottleneck for humanoids doing genuinely useful physical work has always been the hands, not the legs.",
    "{{ROBOT_1_URL}}": "https://www.forbes.com/sites/johnkoetsier/2026/07/09/human-level-hands-1x-just-gave-humanoid-robot-neo-something-close/",

    # Australia
    "{{AUS_1_HEADLINE}}": "ACT Buys Canberra's CSIRO Ginninderra Site for $385 Million to Build 3,000 Homes",
    "{{AUS_1_SUMMARY}}": "The ACT government has locked in a $385 million deal for 243 hectares of CSIRO's Ginninderra research station between Belconnen and Gungahlin, with about 15% of the new suburb earmarked for affordable, community and public housing. CSIRO says it will plough the proceeds back into research infrastructure, closing out a sale process that's dragged on since 2015.",
    "{{AUS_1_URL}}": "https://www.canberratimes.com.au/story/9305684/act-buys-east-section-of-csiros-ginninderra-station-for-385m/",

    "{{AUS_2_HEADLINE}}": "Australians Living Longer as National Health Spend Hits $270 Billion, AIHW Reports",
    "{{AUS_2_SUMMARY}}": "The Australian Institute of Health and Welfare's Australia's Health 2026 report puts total health spending at $270.5 billion for 2023–24, with life expectancy climbing back above pre-pandemic levels — 81.1 years for boys and 85.1 for girls born today. A solid reminder for anyone running a physical trade to keep an eye on their own wear and tear, not just the business's.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Severe Weather Warning Issued for Damaging Winds and Large Hail Across Gippsland",
    "{{VIC_1_SUMMARY}}": "The Bureau has a severe weather warning current for parts of North East, East and West/South Gippsland, with damaging north to northwesterly winds gusting to around 100km/h over exposed ranges and a chance of large hail and isolated tornadoes. If you've got gear, scaffolding or a ute loaded up anywhere east of Melbourne this week, it's worth double-checking it's secured before the wind picks up.",

    # Science
    "{{SCI_1_FLAG}}": "🦗 ZOOLOGY · INVASIVE SPECIES · GIANT ASIAN MANTISES SPREAD ACROSS EUROPE",
    "{{SCI_1_HEADLINE}}": "Two Giant Asian Praying Mantis Species Formally Declared Invasive Across Europe",
    "{{SCI_1_SUMMARY}}": "A new study has officially classified Hierodula tenuidentata and Hierodula patellifera — two large, fast-breeding Asian mantis species — as invasive after their populations exploded across Mediterranean and continental Europe over the past decade. Researchers say the mantises, boosted by climate change and urban heat, are preying on native insects and pollinators and out-competing (sometimes literally eating) Europe's native mantis species during mating.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Interest Rates Are Still a Coin Toss — AI Cash Flow Forecasting Can Show You Trouble Before It Hits",
    "{{INSIGHT_BODY}}": "With Westpac now tipping another RBA rate rise before any cut arrives in 2027, and fuel costs climbing again as excise relief winds back, this is exactly the kind of stretch where a cash flow surprise can catch a small trades business out. AI-powered forecasting tools now built into platforms like Xero and MYOB can chew through your invoicing history, upcoming super and wage obligations, and seasonal patterns to flag a likely shortfall weeks out — not after the account's already tight. It won't replace knowing your numbers yourself, but it turns a monthly guessing game into an early warning system, which matters more when borrowing costs aren't going anywhere soon.",

    # Fun Facts
    "{{FACT_1}}": "Bunnings began life in 1886 as a timber and hardware yard in Fremantle founded by brothers Robert and Arthur Bunning — nearly a century before it became the trade warehouse chain that now supplies a huge share of Australia's tradies.",

    "{{FACT_2}}": "The world's first industrial robot, Unimate, started work on a General Motors assembly line in New Jersey in 1961, lifting and stacking hot die-cast metal parts straight out of the machine — a job considered too dangerous and repetitive for human workers even then.",

    "{{FACT_3}}": "David Unaipon, who appears on Australia's $50 note, held provisional patents for a mechanical sheep-shearing handpiece based on the principle of the boomerang — making him the only Australian to be pictured on a banknote alongside his own invention.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the locksmith get invited to every business networking event in town?",
    "{{JOKE_PUNCHLINE}}": "Because he always knew how to open doors.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The most difficult thing is the decision to act, the rest is merely tenacity.\"",
    "{{CLOSING_ATTR}}": "— Amelia Earhart",
    "{{CLOSING_MESSAGE}}": "It's a clear, still Sunday in Carrum Downs with a top of 15°C — the last dry window before frost bites Monday morning and showery, blustery weather rolls in from Tuesday, so today's the day for any outdoor prep or coating work you can bring forward. Keep half an eye on the severe weather warning if you're heading further into Gippsland this week, and enjoy the World Cup semi-finals or the Storm's home game against the Titans if you get a quiet hour this afternoon.",
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
