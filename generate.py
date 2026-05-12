#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 13 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Wed 13 May
    "{{WEATHER_1}}": "Wed 13 May · Showers · 19°C/10°C",
    "{{WEATHER_2}}": "Thu 14 May · Partly Cloudy · 20°C/10°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Fri 15 May · Cloudy/Rain · 18°C/11°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "Sat 16 May · Mostly Sunny · 22°C/15°C",
    "{{WEATHER_5}}": "Sun 17 May · Partly Cloudy · 19°C/13°C",
    "{{WEATHER_ALERT}}": "🌧 Showers Today",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸 USA / 🇨🇳 CHINA",
    "{{WORLD_1_HEADLINE}}": "Trump Touches Down in Beijing — First US Presidential Visit to China in Nearly a Decade",
    "{{WORLD_1_SUMMARY}}": "US President Donald Trump has arrived in Beijing for a three-day state visit with President Xi Jinping — the first American presidential visit to China in almost nine years. Trade tariffs, the post-Iran ceasefire regional order, Taiwan security, and rare earth mineral access are all on the agenda. A delegation of American CEOs — including those of Boeing and Mastercard — joined the trip, underscoring that this summit carries as much economic weight as geopolitical significance.",
    "{{WORLD_1_URL}}": "https://www.cnbc.com/2026/05/12/trump-xi-china-trade-iran-taiwan.html",

    "{{WORLD_2_FLAG}}": "🛡️ MIDDLE EAST",
    "{{WORLD_2_HEADLINE}}": "Israel Deployed Iron Dome to UAE During Iran War — First Official Confirmation",
    "{{WORLD_2_SUMMARY}}": "US Ambassador to Israel Mike Huckabee has officially confirmed that Israel deployed Iron Dome anti-missile batteries and dozens of personnel to the United Arab Emirates during the Iran conflict — the first acknowledged deployment of Israeli military to the Emirates. The UAE absorbed over 550 ballistic missiles and more than 2,200 drones from Tehran during the war, making it the most targeted country in the region. The disclosure reveals the depth of the Israel-Gulf security partnership that emerged from the conflict.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/5/12/israel-sent-iron-dome-anti-missile-batteries-and-personnel-to-uae-us-envoy",

    # Economics
    "{{ECON_1_FLAG}}": "🏗️ BUDGET",
    "{{ECON_1_HEADLINE}}": "Budget 2026 Fast-Tracks 4,000 Extra Skilled Tradies a Year to Close Construction Labour Gap",
    "{{ECON_1_SUMMARY}}": "Yesterday's Federal Budget funds accelerated skills assessments and occupational licensing for migrant tradespeople, aiming to bring up to 4,000 additional skilled workers into the Australian workforce per year — cutting qualification timelines by up to six months. Electrical, plumbing, and carpentry trades are among the priority categories. While the measure targets the chronic construction labour shortage, it also signals more operators entering the market in the years ahead.",
    "{{ECON_1_URL}}": "https://thenightly.com.au/politics/federal-budget-2026-foreign-tradies-to-be-fast-tracked-into-australia-in-hopes-of-curbing-construction-crisis-c-22273506",

    "{{ECON_2_FLAG}}": "⛽ FUEL",
    "{{ECON_2_HEADLINE}}": "Diesel at 8-Month Low — Excise Cut Continues to June 30 as Budget Signals Longer Relief",
    "{{ECON_2_SUMMARY}}": "Australian retail diesel prices have fallen approximately 25% from their April peak and are tracking near an 8-month low, as global oil prices ease and the government's 32c/litre fuel excise cut continues through June 30, 2026. Budget 2026 also commits to a longer-term fuel security package including a new national diesel reserve — positive news for fleet-heavy trades operators planning fuel costs into the new financial year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📱 GOOGLE",
    "{{TECH_1_HEADLINE}}": "Google Rebuilds Android Around Gemini AI — 'We're Transitioning from an OS to an Intelligence System'",
    "{{TECH_1_SUMMARY}}": "Google's Android Show 2026, held yesterday, unveiled Gemini Intelligence — a sweeping initiative that rebuilds Android around its Gemini AI model, turning phones, watches, cars, and laptops into proactive assistants that can see your screen, understand context, and complete multi-step tasks without prompting. A new 'Googlebook' laptop category was also announced, with major partners Acer, ASUS, and Dell building devices around Gemini at the core. First features roll out to Pixel and Galaxy devices this northern summer.",
    "{{TECH_1_URL}}": "https://9to5google.com/2026/05/12/the-android-show-2026/",

    "{{TECH_2_FLAG}}": "🤖 GEMINI",
    "{{TECH_2_HEADLINE}}": "Google's Gemini 3.1 Pro Hits 50%+ Benchmark Gain — Built for Agentic Legal, Commerce, and Multilingual Tasks",
    "{{TECH_2_SUMMARY}}": "Google's Gemini 3.1 Pro delivers more than a 50% improvement over its predecessor in real-world task benchmarks. Thomson Reuters is deploying it for legal reasoning and contract analysis; Shopify reports reliable agentic execution with minimal prompt tuning; Rakuten uses it for multilingual meeting transcription with speaker identification. Available through Google AI Studio, Vertex AI, and Gemini Enterprise — with a developer API tier.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 INDUSTRIAL",
    "{{ROBOT_1_HEADLINE}}": "SAP and Cyberwave Deploy Fully Autonomous AI Robots in Live Logistics Warehouse — Physical AI Goes Operational",
    "{{ROBOT_1_SUMMARY}}": "SAP and robotics firm Cyberwave have deployed fully autonomous AI-powered robots in an active SAP logistics warehouse in St. Leon-Rot, Germany — performing box folding, packaging, and shipping fulfilment without human supervision in a live production environment. Published May 12, the deployment marks a decisive step beyond proof-of-concept, demonstrating that end-to-end autonomous logistics is commercially viable today and cutting deployment lead times from years to months.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/05/12/sap-and-cyberwave-deploy-fully-autonomous-ai-powered-robots-in-live-sap-logistics-warehouse/26548/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Budget 2026: $250 Tax Cut, Negative Gearing Limited, $150 Energy Rebate, 4,000 Tradies Fast-Tracked",
    "{{AUS_1_SUMMARY}}": "Treasurer Jim Chalmers' 2026-27 Federal Budget, handed down last night, delivers up to $250 annual income tax relief for 13 million workers, limits negative gearing on established properties from July 2027, provides a $150 energy rebate for households and small businesses, and fast-tracks 4,000 skilled migrant tradespeople into the workforce annually. The budget is designed to ease cost-of-living pressure while rebalancing the housing market toward first home buyers and new supply.",
    "{{AUS_1_URL}}": "https://www.thenewdaily.com.au/federal-budget/2026/05/12/budget-2026-winners-losers",

    "{{AUS_2_HEADLINE}}": "Delta Goodrem Performs 'Eclipse' for Australia at Eurovision 2026 — Semi-Final 2 in Vienna on Friday",
    "{{AUS_2_SUMMARY}}": "Pop icon Delta Goodrem represents Australia at Eurovision 2026 in Vienna this Friday morning at 5am AEST, performing 'Eclipse' in Semi-Final 2 at the Wiener Stadthalle. Her custom gown took over 500 hours to make and is embedded with 7,000 Swarovski crystals. Bookmakers currently have Australia in the top five for the Grand Final on Saturday May 16.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Federal Budget Commits $3.8 Billion to Victoria's Suburban Rail Loop — Melbourne's Biggest Rail Project",
    "{{VIC_1_SUMMARY}}": "The Federal Budget handed down last night includes $3.8 billion for Victoria's Suburban Rail Loop, the largest public transport project in Melbourne's history. The underground orbital rail line will connect eight suburbs from Cheltenham to Box Hill without going through the CBD, directly serving growth corridors in Melbourne's southeast. The funding announcement locks in Commonwealth support for a project previously at risk of federal wavering.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 McGILL / NATURE",
    "{{SCI_1_HEADLINE}}": "Brown Fat's Hidden 'Switch' Found — Same Trigger Controls Calorie-Burning and Bone Strength",
    "{{SCI_1_SUMMARY}}": "Researchers at McGill University have identified a molecular switch in brown fat — a glycerol-sensing enzyme called TNAP — that activates a secondary heat-producing pathway when the body is cold, solving a long-standing mystery in metabolic science. Published in Nature on 11 May 2026, the finding carries a bonus: the same molecular switch also governs bone mineralisation, opening potential new treatments for obesity, metabolic disorders, and bone disease simultaneously.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "More Tradies Are Coming — Here's How AI Helps You Compete on Service, Not Just Price",
    "{{INSIGHT_BODY}}": "Yesterday's federal budget fast-tracks up to 4,000 additional skilled migrant tradespeople into the Australian workforce every year — welcome for the construction pipeline, but it also means more competition arriving. When the market gets crowded, racing to the bottom on price is a losing strategy. The businesses that keep winning are the ones clients trust: they communicate clearly, show up when promised, and follow through consistently. AI tools give small operators exactly that edge — automated quote follow-ups so no lead goes cold, professional client update messages sent the moment a job is booked, and post-job check-ins that turn one-time customers into repeat business. You have the relationships and the reputation your newer competitors haven't had time to build. AI helps you scale that advantage without adding headcount. The budget just made the market more competitive. The right response isn't to cut your rates — it's to look twice as professional.",

    # Fun Facts
    "{{FACT_1}}": "Sharks have existed on Earth for approximately 450 million years — meaning they were swimming in ancient seas roughly 100 million years before the first trees appeared on land. They have survived all five of Earth's mass extinction events, including the asteroid impact that ended the non-avian dinosaurs 66 million years ago.",
    "{{FACT_2}}": "Nintendo was founded in 1889 — 96 years before the original Super Mario Bros. was released — as a playing card company handcrafting traditional Japanese Hanafuda cards in Kyoto. It is the world's oldest gaming company still in operation today.",
    "{{FACT_3}}": "Umami — the fifth taste alongside sweet, sour, salty, and bitter — was only scientifically identified in 1908, when Japanese chemist Kikunae Ikeda isolated the savoury compound glutamate from seaweed broth. Ingredients like parmesan, anchovies, miso, and mushrooms are so intensely satisfying because they are exceptionally high in free glutamates.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the old-school sparky refuse to try the new AI quoting software?",
    "{{JOKE_PUNCHLINE}}": "He said no machine would ever do his job — but by smoko, the AI had written the quote, sent it, and was already chasing the deposit.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"It is not the strongest of the species that survives, nor the most intelligent, but the one most responsive to change.\"",
    "{{CLOSING_ATTR}}": "Charles Darwin",
    "{{CLOSING_MESSAGE}}": "A big Wednesday, Liall — Trump has touched down in Beijing for the most significant US-China summit in a decade, and Australia is still absorbing yesterday's budget. On the business side: diesel is at an 8-month low, the fuel excise cut runs to June 30, and a $150 energy rebate is heading your way. Carrum Downs looks showery today but Saturday hits 22°C — your best outdoor window of the week. Delta Goodrem takes the Eurovision stage in Vienna on Friday morning AEST. One of those weeks where knowing which bits matter to your operation is half the job done.",
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
