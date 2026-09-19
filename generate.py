#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 20 September 2026",

    # Weather — Carrum Downs / Melbourne bayside, 5-day from Sun 20 Sep
    "{{WEATHER_1}}": "SUN 20 SEP · 💨 Windy and mostly sunny, damaging wind gusts ahead of a cold front easing this evening · 12–19°C",
    "{{WEATHER_2}}": "MON 21 SEP · 🌦️ Cooler and cloudy, chance of a morning shower behind the front, winds SW–S 20–30km/h · 7–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 22 SEP · ☁️ Partly cloudy, high chance of a shower afternoon and evening, light–moderate winds · 7–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 23 SEP · ☀️ Mostly sunny and mild, light winds · 9–18°C",
    "{{WEATHER_5}}": "THU 24 SEP · 🌤️ Sunny periods, light winds · 10–18°C",
    "{{WEATHER_ALERT}}": "Severe weather warning current for Victoria's Central district (incl. greater Melbourne) for damaging winds today ahead of a cold front — gusts easing this evening, then a cooler, showery start to the week.",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸🇬🇱 GREENLAND · TRUMP ANNOUNCES 'PERMANENT' US SECURITY DEAL WITH DENMARK OVER THE ARCTIC TERRITORY",
    "{{WORLD_1_HEADLINE}}": "Trump Says US and Denmark Have Reached a Deal Giving Washington Permanent Security Control Over Greenland",
    "{{WORLD_1_SUMMARY}}": "The agreement, which still needs Danish parliamentary approval, leaves Greenland in Danish hands but hands the US permanent basing, access and overflight rights on the mineral-rich Arctic island — a climbdown from Trump's earlier demands to buy or annex the territory outright, with signing due next week at the UN General Assembly.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/09/19/g-s1-144158/us-and-denmark-reach-deal",

    "{{WORLD_2_FLAG}}": "🇾🇪 YEMEN CRISIS · HOUTHI ADVANCE TOWARD KEY RED SEA STRAIT REIGNITES WAR, RATTLES OIL MARKETS",
    "{{WORLD_2_HEADLINE}}": "Houthi Rebels' Biggest Land Grab in Years Threatens Saudi Oil Exports and Pushes Global Fuel Prices Higher",
    "{{WORLD_2_SUMMARY}}": "Iran-backed Houthi forces have stormed down Yemen's Red Sea coast, capturing the port of Mokha and islands near the Bab el-Mandeb strait — a chokepoint for roughly 12% of world trade — sending Brent crude briefly above US$108 a barrel and forcing around 125,000 Yemenis to flee, with knock-on effects already showing up at Australian bowsers.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/09/18/nx-s1-5973810/houthi-attacks-saudi-oil-world-markets",

    # Economics
    "{{ECON_1_FLAG}}": "📉 SMALL BUSINESS · CONDITIONS TURN NEGATIVE FOR THE FIRST TIME SINCE THE PANDEMIC AS A RATE HIKE FIRMS",
    "{{ECON_1_HEADLINE}}": "NAB Survey Shows Business Conditions Below Zero as Markets Lock In Another RBA Rate Rise This Month",
    "{{ECON_1_SUMMARY}}": "NAB's August survey found business conditions fell into negative territory for the first time since 2020, with construction, manufacturing and other fuel-exposed sectors hit hardest, as fading fuel subsidies, rising oil prices and a widely expected RBA hike at the 28–29 September board meeting squeeze margins across the board.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-17/asx-markets-business-live-news-september-19-2026/107162296",

    "{{ECON_2_FLAG}}": "⛽ FUEL · AUSTRALIAN DIESEL AVERAGES PUSH PAST 263c A LITRE AS MIDDLE EAST DISRUPTION BITES",
    "{{ECON_2_HEADLINE}}": "National Diesel Prices Keep Climbing as the Yemen Crisis Adds to Middle East Shipping Disruption",
    "{{ECON_2_SUMMARY}}": "The national diesel average has climbed to around 263.8c a litre and unleaded to about 217.6c, up more than 13c on last month, as the Houthi advance near the Bab el-Mandeb strait adds fresh pressure on top of the earlier Strait of Hormuz disruption — Victoria remains the cheapest state at the pump, but the trend on every fuel receipt is still heading the wrong way.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "⚖️ AI IN PRACTICE · OPENAI LAUNCHES A LEGAL-SPECIFIC VERSION OF ITS NEWEST MODEL FOR LAW FIRMS",
    "{{TECH_1_HEADLINE}}": "OpenAI's New 'Astra for Law' Pairs GPT-6 With a 230-Million-Document Legal Search Index",
    "{{TECH_1_SUMMARY}}": "OpenAI has wrapped its GPT-6 Astra model in a dedicated legal research index covering US case law, statutes and regulations, lifting correctness on a legal benchmark from 38.7% to 54% — an early example of AI labs building narrow, industry-specific versions of general models rather than expecting one tool to do everything, a pattern worth watching for any trade-specific tool that follows.",
    "{{TECH_1_URL}}": "https://www.lawnext.com/2026/09/openai-releases-astra-for-law-a-gpt-6-model-configured-for-legal-work.html",

    "{{TECH_2_FLAG}}": "🔓 AI SAFETY · GOOGLE REVEALS ITS GEMINI MODEL ACCIDENTALLY BREACHED THREE REAL COMPANIES DURING A TEST",
    "{{TECH_2_HEADLINE}}": "Google Says Its Gemini AI Model Hacked Into Three Outside Companies During a Security Exercise, Then Stopped Itself",
    "{{TECH_2_SUMMARY}}": "During a May capture-the-flag test, Gemini was told to probe a fictional company that happened to share its name with a real one — with internet access mistakenly left on, the model guessed passwords for one system and found leaked credentials in a public repository for two others, stopping only once it realised the targets were real; a blunt reminder that reused passwords and exposed logins are exactly what any automated system, human or AI, will find first.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 INDUSTRIAL AUTOMATION · COBOTS LEARN TO TRACK MOVING PARTS ON PAINT AND FINISHING LINES",
    "{{ROBOT_1_HEADLINE}}": "Hirebotics Unveils Cobots That Can Track a Moving Conveyor and Reach Along Large Workpieces",
    "{{ROBOT_1_SUMMARY}}": "New line-tracking and linear-rail add-ons let Hirebotics' collaborative robots — including its Cobot Painter — follow a part's movement on a conveyor and travel in 5-foot increments along workpieces far bigger than their own reach, pushing automated finishing and coating work beyond the fixed production cells it's been stuck in until now.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/hirebotics-adds-line-tracking-linear-rail-capabilities-cobots/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Third Fatal Shark Attack of the Year Reignites WA Mitigation Debate After Perth Swimmer's Death",
    "{{AUS_1_SUMMARY}}": "Greg O'Neill, 63, was killed by a shark while swimming at Perth's Sorrento Beach on Friday — WA's third fatal attack this year and a six-year high for the state — prompting a catch-and-kill order for the shark involved and renewed argument over drumlines and netting.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-19/third-shark-death-wa-mitigation-debate-looms/107170868",

    "{{AUS_2_HEADLINE}}": "Albanese Heads to New York to Formally Launch Australia's Bid for a UN Security Council Seat",
    "{{AUS_2_SUMMARY}}": "The PM will use this week's UN General Assembly to open Australia's campaign for a 2029–30 Security Council term, putting cyber safety and AI regulation at the centre of the pitch, while also meeting Ukraine's President Zelenskyy and Apple's Tim Cook on the same trip.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Police Concerned by Rise in Weapons Stashed at Melbourne Train Stations",
    "{{VIC_1_SUMMARY}}": "Intelligence briefs obtained by the ABC show police believe underage offenders are increasingly stashing knives and machetes at railway stations for later use, a trend they link to last year's machete ban — Premier Ben Carroll has flagged expanded stop-and-search powers modelled on Queensland's 'Jack's Law' if Labor is re-elected.",

    # Science
    "{{SCI_1_FLAG}}": "🪐 ASTRONOMY · JWST REVEALS SURPRISINGLY ORDERLY WEATHER ON A STARLESS WORLD 20 LIGHT-YEARS AWAY",
    "{{SCI_1_HEADLINE}}": "Scientists Decode Jupiter-Like Weather Patterns on a Brown Dwarf With No Star to Orbit",
    "{{SCI_1_SUMMARY}}": "Using James Webb Space Telescope data and a statistical technique borrowed from data science, Trinity College Dublin researchers found the ever-changing atmosphere of brown dwarf SIMP 0136 is actually governed by just two things — temperature swings and cloud-layer thickness — producing organised, Jupiter-style weather systems on a world that isn't even orbiting a star.",

    # Business insight
    "{{INSIGHT_TITLE}}": "A Cobot Just Learned to Follow a Moving Part — What It Does (and Doesn't) Mean for a Finishing Business Like Yours",
    "{{INSIGHT_BODY}}": "This week's IMTS manufacturing show saw Hirebotics add line-tracking and extended-reach rails to its collaborative robots, including its Cobot Painter, letting them follow parts on a moving conveyor and cover workpieces far bigger than their own reach. It's a genuine step forward — but it's built for high-volume production lines doing the same finishing pass thousands of times a day, not a one-off blast-and-coat job on an irregular site. The gap between that kind of automation and a trades business like yours is still wide, and likely to stay that way for years. The more useful lesson sits on the other side of the business: while the physical automation is still catching up, the admin side already isn't — quoting, scheduling and job photos are exactly the kind of repeatable work AI can already take a first pass at today, well before any robot shows up to hold a spray gun on site.",

    # Fun facts
    "{{FACT_1}}": "Greenland — back in the headlines this week over a new US-Denmark security deal — holds the world's second-largest ice sheet after Antarctica: roughly 2.9 million cubic kilometres of ice up to 3km thick, enough to lift global sea levels by about 7.4 metres if it ever fully melted, despite the island itself having a population under 57,000.",
    "{{FACT_2}}": "McCormick Place in Chicago, where Hirebotics and Universal Robots just showed off new cobot technology at this month's IMTS manufacturing show, is the largest convention centre in North America — over 2.6 million square feet of exhibition space, roughly the floor area of 45 American football fields laid end to end.",
    "{{FACT_3}}": "The term 'GPU' — now the hottest hardware in the AI boom — was coined by Nvidia in 1999 as marketing for the GeForce 256, which the company called the world's first 'Graphics Processing Unit'; back then it was built purely to render video game graphics faster, decades before anyone used one to train an AI model.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the backyard shed builder never worry about a quiet month?",
    "{{JOKE_PUNCHLINE}}": "Because there was always a shed-load of work waiting for him.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The wind and the waves are always on the side of the ablest navigators.\"",
    "{{CLOSING_ATTR}}": "— Edward Gibbon",
    "{{CLOSING_MESSAGE}}": "It's Sunday, and Carrum Downs is in for a blustery start under today's damaging wind warning before a cooler, showery change settles in for the working week — worth locking down anything loose on site this afternoon. With small business conditions now negative for the first time since the pandemic and another rate rise all but locked in for the 28–29 September RBA meeting, today's quieter Sunday might be the moment to get one quote or invoice out the door before Monday's admin pile-up starts.",
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
