#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 24 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 24 May (BOM forecast)
    "{{WEATHER_1}}": "SUN 24 · ☀ Mostly sunny · 19°C",
    "{{WEATHER_2}}": "MON 25 · 🌧 Showers likely · 17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 26 · 🌧 Showers · 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 27 · ⛅ P/Cloudy · 14°C",
    "{{WEATHER_5}}": "THU 28 · ⛅ Cloudy · 13°C",
    "{{WEATHER_ALERT}}": "☔ RAIN FROM MONDAY",

    # World
    "{{WORLD_1_FLAG}}": "🇨🇳 CHINA · MINE DISASTER",
    "{{WORLD_1_HEADLINE}}": "Gas Explosion at Liushenyu Coal Mine in Shanxi Kills 82 — China's Worst Mining Accident in Over a Decade",
    "{{WORLD_1_SUMMARY}}": "A gas explosion ripped through the Liushenyu Coal Mine in Qinyuan County, Shanxi Province on the evening of 22 May, killing 82 people and injuring 128 more. Of 247 workers underground at the time, all have now been accounted for. Carbon monoxide sensors had triggered elevated-level alarms before the blast. President Xi Jinping ordered a national review of workplace safety standards across all industries, and authorities have vowed criminal investigations. China's coal mines remain among the world's most dangerous, with poor enforcement, production quotas, and corruption regularly cited as structural failures. It is the deadliest mining accident in China in over a decade.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/5/23/gas-explosion-at-chinese-coal-mine-kills-at-least-90",

    "{{WORLD_2_FLAG}}": "🇺🇸 QUAD · DIPLOMACY",
    "{{WORLD_2_HEADLINE}}": "Rubio Arrives in India to Reset US-India Ties Ahead of Quad Ministerial — Penny Wong Also Attending",
    "{{WORLD_2_SUMMARY}}": "U.S. Secretary of State Marco Rubio touched down in India on Saturday for a four-day visit culminating in the Quad ministerial meeting in New Delhi on Tuesday 26 May. Australian Foreign Minister Penny Wong, Japanese FM Toshimitsu Motegi, and Indian EAM S. Jaishankar will join Rubio for discussions covering China's maritime assertiveness in the South China Sea, critical minerals supply chains, and semiconductor investment corridors. The visit is Rubio's first official trip to India and comes as Washington seeks to repair diplomatic ties strained by Trump-era tariffs on Indian exports. The Quad's agenda has direct implications for Australia's Indo-Pacific security posture and critical minerals trade policy.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/05/23/nx-s1-5832394/rubio-arrives-india",

    # Economics
    "{{ECON_1_FLAG}}": "📉 AUSTRALIA · PMI",
    "{{ECON_1_HEADLINE}}": "Australia's Composite PMI Crashes to 47.8 in May — Business Confidence Hits Lowest Level Since COVID Pandemic Onset",
    "{{ECON_1_SUMMARY}}": "The S&P Global Australia flash composite PMI fell from 50.4 in April to 47.8 in May — the second contraction in three months — as new orders dropped at the fastest pace since September 2021. Services collapsed from 50.7 to 47.7, while manufacturing slipped to 50.3. Business sentiment reached its joint-lowest level since the survey began, equalling only the March 2020 COVID shock. Private sector employment fell marginally for the first time in months, and input price inflation driven by fuel, raw materials, and transport remained elevated. Respondents directly cited uncertainty from the Middle East conflict as the primary drag on conditions. For trades operators: discretionary residential spend contracts fastest in this environment; maintenance and compliance-driven industrial work holds longer.",
    "{{ECON_1_URL}}": "https://investinglive.com/news/australia-flash-pmi-slumps-to-478-in-may-as-new-orders-fall-at-fastest-pace-since-2021-20260520/",

    "{{ECON_2_FLAG}}": "🏗 BUDGET 2026 · CONSTRUCTION",
    "{{ECON_2_HEADLINE}}": "Budget Commits $85M to Fast-Track Migrant Tradie Skills Assessments — 4,000 Extra Construction Workers Per Year Targeted",
    "{{ECON_2_SUMMARY}}": "The federal government's 2026-27 Budget allocated $85.2 million to modernise and accelerate skills assessment pathways for migrant tradespeople, aiming to add 4,000 qualified construction workers to the Australian workforce annually. The program will cut current wait times of up to 12 months by hiring extra assessors and piloting offshore testing hubs. Australia's construction labour shortage is projected to peak at more than 50,000 unfilled positions between 2026 and 2027. For established operators: the new labour supply takes 12–18 months to materialise — near-term, skilled trades capacity remains tight and pricing power holds.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 ANTHROPIC · VALUATION",
    "{{TECH_1_HEADLINE}}": "Anthropic Closes In on $900 Billion Valuation — Set to Surpass OpenAI as World's Most Valuable Private AI Company",
    "{{TECH_1_SUMMARY}}": "Anthropic is in advanced talks to close a $30+ billion funding round at a pre-money valuation above $900 billion, which would vault the Claude maker past OpenAI's $852 billion valuation to become the world's most valuable private AI company. Sequoia Capital, Dragoneer, Altimeter, and Greenoaks are expected as co-leads. The company is projecting Q2 2026 revenue of $10.9 billion — double the prior quarter — and is forecasting its first profitable quarter. A public listing is being eyed as early as October 2026. Context for Liall: Anthropic builds Claude, the model running this briefing. The tools available to a sole trades operator today are backed by infrastructure valued at more than nine of Australia's largest public companies combined.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/05/20/anthropic-revenue-explosive-growth-ipo-profitable-quarter.html",

    "{{TECH_2_FLAG}}": "🔒 GITHUB · SUPPLY CHAIN",
    "{{TECH_2_HEADLINE}}": "GitHub Confirms 3,800 Internal Repositories Compromised via Trojanized VS Code Extension — 18-Minute Attack Window",
    "{{TECH_2_SUMMARY}}": "GitHub disclosed that threat actor group TeamPCP exfiltrated approximately 3,800 internal repositories on 18 May through a trojanized Nx Console extension that was live on the Visual Studio Marketplace for just 18 minutes before detection. The extension harvested authentication tokens and pushed data to external servers before being pulled. No customer repository data was confirmed as accessed and all affected credentials were rotated. The incident underscores that software supply chain risk has moved upstream into everyday developer tooling — a VS Code extension downloaded by a trusted developer can carry the same payload as a phishing attack, with no user action required.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "📦 WAREHOUSE · LIVE DEMO",
    "{{ROBOT_1_HEADLINE}}": "Plus One Robotics Livestreams 8-Hour Autonomous Warehouse Test — Nearly 20,000 Parcel Picks at 2,488 Per Hour",
    "{{ROBOT_1_SUMMARY}}": "Plus One Robotics conducted a live, unedited eight-hour warehouse automation performance test on 22 May, achieving 19,790 parcel picks at an average throughput of 2,488 picks per hour and 1.45 seconds per pick — without human intervention and in front of a live audience. The event was streamed publicly as a transparency play, with real-time performance data visible throughout. The company reached 2 billion cumulative picks in April 2026 across its global fleet of AI-powered parcel and depalletisation robots. The demonstration is part of a broader industry shift toward validated, published throughput data replacing marketing claims as the procurement benchmark for warehouse automation — a dynamic accelerating adoption across logistics and fulfilment globally.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/05/22/plus-one-robotics-streams-eight-hours-of-live-warehouse-automation-performance/101835/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Federal Budget Fast-Tracks $85M for Migrant Tradie Skills Assessments — 4,000 Extra Construction Workers Per Year",
    "{{AUS_1_SUMMARY}}": "Australia's 2026-27 Federal Budget commits $85.2 million to modernise the skills assessment and occupational licensing pathway for migrant tradespeople, targeting an additional 4,000 qualified construction workers entering the workforce annually. The program will reduce current assessment wait times — which can reach 12 months — by hiring extra assessors and piloting offshore testing hubs. Construction labour shortages are projected to peak at more than 50,000 unfilled positions over 2026–27. For established operators already in the market, the near-term effect is continued tight labour supply — and pricing power that won't be diluted for at least 12 to 18 months while the new pipeline builds.",
    "{{AUS_1_URL}}": "https://thenightly.com.au/politics/federal-budget-2026-foreign-tradies-to-be-fast-tracked-into-australia-in-hopes-of-curbing-construction-crisis-c-22273506",

    "{{AUS_2_HEADLINE}}": "Penny Wong Heads to New Delhi for Quad Ministerial — Australia Joins US, India, and Japan on Indo-Pacific Security and Trade",
    "{{AUS_2_SUMMARY}}": "Australian Foreign Minister Penny Wong is attending the Quad ministerial meeting in New Delhi on 26 May alongside U.S. Secretary of State Rubio and Japan's FM Motegi. Core agenda items include China's maritime expansion in the South China Sea, critical minerals supply chain resilience, and joint semiconductor investment strategy. The meeting lands as Australia navigates its most complex trade geometry in decades — balancing iron ore and LNG revenue from China with deepening defence and technology partnerships with the US and Indo-Pacific allies.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Commits Over $1 Billion to Road Resurfacing and Pothole Repair in 2026-27 Budget — Plus $674M for 25 New Trains",
    "{{VIC_1_SUMMARY}}": "The Victorian government's 2026-27 State Budget allocates more than $1 billion for road repairs, pothole rectification, and resurfacing across the state, alongside $674 million for 25 new train sets to be built by local workers in Ballarat. The Metro Tunnel is now fully operational with five new stations, the West Gate Tunnel is open and cutting travel times from the western suburbs, and eight further level crossings are set for removal this year. For trades businesses running vehicles across Melbourne's road network — including routes between Carrum Downs and metro job sites — the sustained road renewal commitment means progressively better conditions and reduced running costs over the next two to three years.",

    # Science
    "{{SCI_1_FLAG}}": "🦖 PALAEONTOLOGY · TEXAS",
    "{{SCI_1_HEADLINE}}": "'T. Rex of the Seas': Scientists Name Tylosaurus Rex — 43-Foot Marine Predator Identified from Texas Fossils",
    "{{SCI_1_SUMMARY}}": "A new species of mosasaur, formally named Tylosaurus rex — 'king of the tylosaurs' — has been identified from 80-million-year-old fossils collected in northern Texas since the 1960s. Researchers from the American Museum of Natural History, Dallas's Perot Museum, and Southern Methodist University reanalysed more than a dozen museum specimens long misclassified as Tylosaurus proriger and confirmed they represent a distinct species. Stretching up to 43 feet — twice the length of a great white shark — Tylosaurus rex had finely serrated teeth, robust jaw musculature, and fossil evidence of violent intraspecific combat. One Texas specimen, nicknamed 'The Black Knight,' showed a fractured jaw and missing snout consistent with an attack from a member of the same species. Published ScienceDaily, 22 May 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "From Quoting to Invoice Paid: How AI Can Run Your Entire Admin Cycle While You're on the Tools",
    "{{INSIGHT_BODY}}": "Every hour you spend on site is an hour not spent chasing quotes, sending follow-ups, raising invoices, or updating your job management system. For a sole operator or small crew, that creates a predictable bottleneck: admin piles up, invoices go out late, and jobs get lost because follow-up never happened. AI changes this with a workflow most tradies haven't set up yet. A voice note recorded on the drive home — captured via your phone's transcription and passed to Claude or ChatGPT — can generate a job completion summary, a draft invoice with line items, a follow-up email to the client, and a note for your schedule, all from that single input. Set up properly once, this workflow recovers 5 to 10 hours per week that currently sits in the cracks. For a trades business billing at $120 to $200 per hour, that is between $600 and $2,000 in recovered billable capacity — every week. The catch is that the setup requires about two hours of investment upfront to build the right prompt and test it with a real job. That is what Sunday afternoons are for.",

    # Fun Facts
    "{{FACT_1}}": "Australia has approximately 1.2 million feral camels — more per capita than any country on Earth. They were imported from Afghanistan and India in the 1860s for outback exploration and transport, then released when motor vehicles made them redundant. Their population doubles roughly every nine years. Australian wild camels are now considered genetically elite: Saudi Arabia, the UAE, and Oman periodically import live animals from Australia because the bloodlines are considered exceptionally pure.",

    "{{FACT_2}}": "The first commercial home video game console was not Atari — it was the Magnavox Odyssey, released in 1972, two years before Atari's iconic Pong arcade cabinet. The Odyssey had no sound, no score display, and no microprocessor. Players taped plastic overlays to the television screen to create different game environments. Magnavox sold around 100,000 units and later sued Atari for copying the paddle-and-ball concept in Pong — and won.",

    "{{FACT_3}}": "The human liver is the only internal organ capable of regenerating from as little as 25% of its original mass. Living organ donors can safely give up to 60% of their liver; both the donor's remaining portion and the recipient's new segment regrow to full functional size within six to eight weeks. This unique capacity is why partial liver transplants from living donors are now standard in major transplant hospitals worldwide — no other complex mammalian organ can recover after surgical removal.",

    # Joke
    "{{JOKE_SETUP}}": "Why do welders make the best friends?",
    "{{JOKE_PUNCHLINE}}": "Once they bond with you, it's permanent.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The greater danger for most of us lies not in setting our aim too high and falling short; but in setting our aim too low, and achieving our mark.”",
    "{{CLOSING_ATTR}}": "— Michelangelo",
    "{{CLOSING_MESSAGE}}": "Sunday morning in Carrum Downs — mostly sunny today with a high of 19°C, your last clear day before showers push back in from Monday and hold through Tuesday. If there is site work, outdoor prep, or coating work to be done this weekend, today is the window. The economic week delivered a sharp warning: Australia's composite PMI fell to 47.8 in May, the second contraction in three months, with business confidence matching only the COVID-onset reading from March 2020. For ISV, the resilience is in maintenance and compliance-driven industrial work — that pipeline holds longer than discretionary residential. The Federal Budget's skilled tradie pipeline will take 12 to 18 months to materialise, so near-term labour remains tight and your pricing power is intact. And on the AI front: Anthropic — the company behind this briefing — is closing a funding round at a $900 billion valuation. The tools you are already using are built on infrastructure moving faster than any technology cycle since the internet. Aim high today, Liall.",
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
