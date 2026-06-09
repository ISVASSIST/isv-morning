#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 10 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 10 Jun
    # Wet Wednesday, clearing Thursday, fine weekend ahead
    "{{WEATHER_1}}": "WED 10 · 🌧 Showers · 10–15°C",
    "{{WEATHER_2}}": "THU 11 · ⛅ Partly Cloudy · 11–16°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 12 · 🌤 Mostly Fine · 11–16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 13 · ☀️ Fine · 10–17°C",
    "{{WEATHER_5}}": "SUN 14 · ⛅ Partly Cloudy · 12–17°C",
    "{{WEATHER_ALERT}}": "⚽ WORLD CUP KICKS OFF TOMORROW",

    # World
    "{{WORLD_1_FLAG}}": "🇰🇪 AFRICA · KENYA",
    "{{WORLD_1_HEADLINE}}": "Kenyan Police Fire Tear Gas on Protesters Opposing US Ebola Quarantine Centre as Demonstrations Turn Deadly",
    "{{WORLD_1_SUMMARY}}": "Kenyan police fired tear gas in Nanyuki on Tuesday as protests against a proposed US-run quarantine facility for Americans exposed to Ebola turned violent for a second day. At least two people were killed on Monday when the demonstrations escalated. The 50-bed unit at an air force base would house asymptomatic Americans exposed to the DRC and Uganda Ebola outbreak — but Kenyans accuse Washington of offloading its health risk onto a poorer country. A court suspended construction on Friday and extended the order three weeks further on Tuesday; US military planes have continued ferrying staff and equipment regardless.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/6/9/protests-erupt-in-kenya-over-us-ebola-quarantine-centre-in-nanyuki",

    "{{WORLD_2_FLAG}}": "⚽ GLOBAL · SPORT",
    "{{WORLD_2_HEADLINE}}": "FIFA World Cup 2026 Opens Tomorrow — Shakira and Burna Boy to Headline Ceremony at Mexico City's Iconic Azteca",
    "{{WORLD_2_SUMMARY}}": "The 48-team, 104-match 2026 FIFA World Cup kicks off in Mexico City tomorrow, June 11, as co-hosts Mexico face South Africa at the Estadio Azteca. Shakira and Burna Boy will perform the tournament's official anthem Dai Dai at the opening ceremony, joined by Maná, J Balvin, Alejandro Fernández, and Tyla. It's the first World Cup co-hosted across three nations — Mexico, the US, and Canada — and the largest tournament in history. Mexico City has declared June 11 a public holiday.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/sports/2026/6/9/world-cup-opening-ceremony-whos-performing-when-it-starts-how-to-watch",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL PRICES · AUS",
    "{{ECON_1_HEADLINE}}": "ACCC Data: Diesel at 209c/L, Petrol at 173c/L — Both Set to Spike When July 1 Excise Snapback Hits",
    "{{ECON_1_SUMMARY}}": "The ACCC's June 5 weekly monitoring report shows diesel averaging 209.3 cents per litre and petrol at 173.3 cents per litre across Australia's five largest cities — down 113 and 84 cents respectively from March 31, entirely due to the temporary 32c/L excise halving that ends June 30. Regional diesel is higher still at 221.1 cents per litre. In three weeks those reductions reverse. For a trades business running two vehicles on 1,000+ km per week, the July 1 snapback lands on the same day as the annual Fair Work wage adjustment — the repricing window is closing fast.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📊 CONSUMER CONFIDENCE · AUS",
    "{{ECON_2_HEADLINE}}": "Australian Consumer Confidence Falls to Near 50-Year Low — Westpac Index Drops to 80.6, Fourth Monthly Decline",
    "{{ECON_2_SUMMARY}}": "The Westpac–Melbourne Institute Consumer Sentiment Index fell 2.9% to 80.6 in June — its fourth consecutive monthly decline and one of the weakest readings in the survey's 50-year history. Pessimists now outnumber optimists by nearly 20 percentage points. The survey found cost-of-living concerns dominate household thinking, with the fuel excise cut rated only 'a small and brief reprieve.' House price expectations dropped below their long-run average for the first time in nearly three years — a potential headwind for construction and renovation-adjacent trades heading into the new financial year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🇺🇸 USA · AI POLICY",
    "{{TECH_1_HEADLINE}}": "Trump Signs Executive Order on AI Innovation and Security — White House Fast-Tracks Federal AI Deployment",
    "{{TECH_1_SUMMARY}}": "A June 2026 White House Executive Order titled 'Promoting Advanced Artificial Intelligence Innovation and Security' directs federal agencies to remove regulatory barriers to AI adoption and prioritise American AI providers in procurement across healthcare, defence, infrastructure, and economic planning. The order signals a clear US government shift from AI oversight to AI acceleration — deepening investment in the major platforms (Anthropic, OpenAI, Google) and flowing through to the capabilities small business users access via those tools in the months ahead.",
    "{{TECH_1_URL}}": "https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/",

    "{{TECH_2_FLAG}}": "🤖 AI AGENTS · JUNE 2026",
    "{{TECH_2_HEADLINE}}": "AI Is Moving From Chat to Action — Claude Opus 4.8 Completes 750,000-Line Migration in 11 Days Using Autonomous Subagents",
    "{{TECH_2_SUMMARY}}": "The shift from AI as a question-answering tool to AI as a working system is now documented in practice. Claude Opus 4.8 (released May 28) dynamically generates orchestration scripts and deploys multiple parallel subagents — one developer used this to migrate 750,000 lines of legacy code in just 11 days. OpenAI separately launched real-time voice agents with live translation this month. For small business owners, the shift that matters is that AI is no longer just answering questions — it's completing multi-step workflows autonomously, including quoting, scheduling, and client follow-up sequences.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 CONSUMER ROBOTS · NORWAY",
    "{{ROBOT_1_HEADLINE}}": "1X Opens Pre-Orders for $20,000 NEO Home Robot — World's First Consumer-Ready Humanoid With 2026 Delivery",
    "{{ROBOT_1_SUMMARY}}": "Norwegian robotics startup 1X has opened pre-orders for NEO, billed as the world's first consumer-ready humanoid robot, at US$20,000 with a $200 deposit to secure delivery. At 29 kg, NEO can lift over 68 kg, operates at near-silent 22 decibels, and carries 22-degrees-of-freedom hands with human-level dexterity. Day-one capabilities include fetching items, opening doors, and operating appliances. US deliveries are planned for 2026; Australia from 2027. The home humanoid robot — long theoretical — is now a commercial product you can order today.",
    "{{ROBOT_1_URL}}": "https://www.robotics247.com/article/video_1x_announces_neo_consumer_ready_humanoid_robot_pre_order_details_with_200_deposit",

    # Australia
    "{{AUS_1_HEADLINE}}": "Demons Win Emotional Big Freeze at MCG — Kozzy Pickett Seals Eight-Point Win in Tribute to Neale Daniher",
    "{{AUS_1_SUMMARY}}": "Melbourne defeated Collingwood 83–75 in Monday's King's Birthday Big Freeze blockbuster at the MCG, with Kozzy Pickett kicking the match-sealing goal in a tense final quarter. The game carried deep emotional weight following the passing of Neale Daniher — the inspirational former Demons coach who founded the Big Freeze event in 2015 to raise awareness and funds for MND research. AFL Round 13 drew a record national crowd of 390,752 across all games.",
    "{{AUS_1_URL}}": "https://www.afl.com.au/news/1536297/melbourne-demons-down-collingwood-magpies-pies-in-kings-birthday-battle-royale-marred-by-serious-injury-concern",

    "{{AUS_2_HEADLINE}}": "Australian Dollar Falls to 0.7028 as Consumer Gloom Deepens Ahead of EOFY",
    "{{AUS_2_SUMMARY}}": "The AUD/USD slid to 0.7028 on Tuesday, June 9, as the Westpac June consumer sentiment data confirmed Australian households are at their most pessimistic in decades. A weaker dollar pushes up the cost of imported materials, machinery, and equipment priced in USD — relevant for any trades business buying overseas-manufactured coatings, fasteners, or plant heading into the new financial year.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's $767M West Melbourne Infrastructure Blitz Underway — Roads, Rail Freight and Port Upgrades Reshape Industrial Corridor",
    "{{VIC_1_SUMMARY}}": "Victoria's $767 million infrastructure investment in Melbourne's western industrial corridor — four major road projects plus a new international freight gateway — is now under active construction. The works target freight connectivity between the port precinct and outer western and southern industrial zones, cutting heavy vehicle travel times. The state is separately on track to remove its 88th level crossing later in 2026, maintaining the momentum of Australia's most ambitious urban rail-road separation program.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 NEUROSCIENCE · JAPAN",
    "{{SCI_1_HEADLINE}}": "Scientists Identify the Brain Chemical That Helps Break Old Habits — Pathway to Treating Addiction, OCD and Parkinson's",
    "{{SCI_1_SUMMARY}}": "Researchers at the Okinawa Institute of Science and Technology have identified acetylcholine — released by specific cholinergic interneuron brain cells — as the key signal enabling behavioural flexibility: the ability to break a habit and adapt when circumstances change. The study observed mice adjusting their choices after losing an expected reward, finding that cholinergic interneurons fire to trigger a mental 'reset.' The finding offers potential new treatment pathways for addiction, obsessive-compulsive disorder, and Parkinson's disease, where rigid habitual behaviour is a central feature. Published in Nature Communications, June 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Too Busy to Look at the Numbers? AI Can Run Your EOFY Business Health Check in 10 Minutes",
    "{{INSIGHT_BODY}}": "For most trades business owners, EOFY arrives and the real story of the year only becomes clear in your accountant's office — weeks after you could have done anything about it. The problem isn't laziness; it's that pulling a genuine picture of margin, job profitability, and cash flow position takes time you rarely have during the busy season. AI changes this. Open Claude or ChatGPT and describe your last quarter: the types of jobs you ran, your rough sense of margins, your labour-to-materials split, and any patterns you've noticed — jobs that always run over, clients who negotiate late, materials that keep surprising you. Ask the AI to help you identify which job types are probably your most and least profitable, and what questions you should be asking your accountant before June 30. It won't replace your bookkeeper — but it turns a vague anxiety about the numbers into a sharp list of specific questions. You'll walk into your EOFY meeting with more clarity and less chance of leaving money on the table. Twenty minutes. Today.",

    # Fun Facts
    "{{FACT_1}}": "Mexico City's Estadio Azteca — where the World Cup opens tomorrow — is the only stadium in history to have hosted two FIFA World Cup finals: Brazil vs Italy in 1970 and Argentina vs West Germany in 1986. The same ground hosted Diego Maradona's legendary 1986 quarter-final against England, where he scored both the 'Hand of God' goal and the 'Goal of the Century' four minutes apart — arguably the two most famous moments in football history, in the same match, at the same ground.",

    "{{FACT_2}}": "A Rubik's Cube has 43,252,003,274,489,856,000 possible configurations — roughly 43 quintillion. Yet any scrambled cube in any state can be solved in 20 moves or fewer. Mathematicians call this 'God's Number,' and proving it in 2010 required 35 CPU-years of computational time donated by Google engineers to verify every possible configuration.",

    "{{FACT_3}}": "Acetylcholine — the brain chemical in today's science story — is also the same molecule that triggers every deliberate movement you make. It's released at the neuromuscular junction to initiate muscle contractions: every time you grip a tool, lift equipment, or sign a quote, acetylcholine is what starts the process. This dual role controlling both movement and mental flexibility makes it one of the most consequential chemicals in the body.",

    # Joke
    "{{JOKE_SETUP}}": "I asked my apprentice if he'd been watching any of the World Cup.",
    "{{JOKE_PUNCHLINE}}": "He said: 'I don't need to — I already get enough penalty shootouts every time I submit a quote.'",

    # Closing
    "{{CLOSING_QUOTE}}": "“Empty your mind, be formless. Shapeless, like water. You put water into a cup — it becomes the cup. Be water, my friend.”",
    "{{CLOSING_ATTR}}": "— Bruce Lee",
    "{{CLOSING_MESSAGE}}": "It's Wednesday morning in Carrum Downs — wet today, but clearing tomorrow and a fine weekend on the way. The World Cup kicks off in Mexico City tomorrow with Shakira on stage and 48 nations on the pitch — the biggest tournament ever, arriving in your time zone. The Demons honoured Neale Daniher with a big Monday win at the MCG, which felt right. Consumer confidence is at near 50-year lows, the dollar is soft, and the July 1 fuel clock is running. If the business is in good shape, now's the time to lock that in. If it isn't, now's the time to find out. Have a good Wednesday, Liall.",
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
