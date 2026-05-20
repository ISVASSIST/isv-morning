#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 21 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 21 May (BOM forecast)
    "{{WEATHER_1}}": "THU 21 · 🌫 Foggy start · 16°C",
    "{{WEATHER_2}}": "FRI 22 · ⛅ Partly cloudy · 17°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SAT 23 · ☀ Mostly sunny · 19°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SUN 24 · ⛅ Mild · 14°C",
    "{{WEATHER_5}}": "MON 25 · ☁ Cloudy · 14°C",
    "{{WEATHER_ALERT}}": "🌫 FOG RISK THIS MORNING",

    # World
    "{{WORLD_1_FLAG}}": "🌊 IRAN · OIL",
    "{{WORLD_1_HEADLINE}}": "Strait of Hormuz Remains Effectively Closed — 230 Tankers Stranded as Iran Charges $1M+ Per Ship",
    "{{WORLD_1_SUMMARY}}": "Despite the Iran war ceasefire declared in early May, the Strait of Hormuz remains 'effectively closed' according to Abu Dhabi National Oil Company CEO Sultan Al Jaber. Iran has established a new 'Persian Gulf Strait Authority' that vets and taxes ships seeking passage — with reported tolls exceeding $1 million per vessel — and 230 fully loaded oil tankers remain stranded inside the Gulf. US Secretary of State Marco Rubio called the arrangement 'unacceptable.' US forces have exchanged fire with Iranian units in the strait and disabled two Iranian tankers. Every day those ships can't move, global oil supply tightens — and Australian diesel prices will remain volatile until the blockade lifts.",
    "{{WORLD_1_URL}}": "https://en.wikipedia.org/wiki/2026_Strait_of_Hormuz_crisis",

    "{{WORLD_2_FLAG}}": "🦠 GLOBAL HEALTH",
    "{{WORLD_2_HEADLINE}}": "WHO Holds Emergency Briefing on Cruise Ship Hantavirus Outbreak — 8 Cases, 3 Deaths Across 23 Countries",
    "{{WORLD_2_SUMMARY}}": "The WHO Director-General held a press conference today on the Hantavirus cluster linked to the Dutch cruise ship MV Hondius, which departed Ushuaia, Argentina in April and travelled through Antarctica and the South Atlantic. Eight cases have been confirmed — six laboratory-confirmed as Andes virus — with three deaths, a case fatality rate of 38%. Cases have since emerged in the Netherlands, South Africa, and Switzerland. The WHO assesses global public health risk as low, but this is the first documented Hantavirus outbreak aboard a ship, and health authorities in 23 countries are monitoring returned passengers.",
    "{{WORLD_2_URL}}": "https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON600",

    # Economics
    "{{ECON_1_FLAG}}": "💼 WAGES",
    "{{ECON_1_HEADLINE}}": "ACTU Lifts Minimum Wage Claim to 6% — Fair Work Commission Decision Weeks Away, July 1 Effect",
    "{{ECON_1_SUMMARY}}": "Australian unions have raised their minimum wage claim before the Fair Work Commission from 5% to 6% for the country's three million lowest-paid workers, citing rising living costs and the ongoing Iran-driven economic shock. The FWC decision is expected in early June 2026, taking effect from the first full pay period after 1 July. Employer groups are pushing back hard, pointing to payday super obligations also kicking in on 1 July and sustained margin pressure on small business. For trades operators with apprentices or casuals on award rates, a 6% rise would add hundreds of dollars a week to labour cost — on top of all the other July changes.",
    "{{ECON_1_URL}}": "https://www.actu.org.au/media-release/unions-increase-their-minimum-wages-claim-to-6/",

    "{{ECON_2_FLAG}}": "⛽ FUEL / EXCISE",
    "{{ECON_2_HEADLINE}}": "Federal Fuel Excise Cut Expires June 30 — Six Weeks to Lock In Lower-Cost Quotes Before Triple Cost Hit",
    "{{ECON_2_SUMMARY}}": "The Federal Government's 32 cents-per-litre excise reduction on petrol and diesel — introduced from 1 April 2026 to offset the global fuel shock — expires 30 June 2026, the same day payday superannuation obligations begin. For south-east Melbourne trades businesses running vans and equipment across multiple jobs daily, the 32c cut has been providing genuine cost relief. When it expires on 1 July — alongside higher super contributions and a likely award wage rise — the simultaneous hit will be sharp. Jobs being quoted this week for work extending into July should factor in all three changes, or risk locking in a margin hit before the ink is dry.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔵 GOOGLE I/O",
    "{{TECH_1_HEADLINE}}": "Google Gemini 3.5 Flash Now Live — Frontier AI Speed at a Fraction of the Cost, Built for Agents",
    "{{TECH_1_SUMMARY}}": "Launched at Google I/O on Tuesday and now generally available, Gemini 3.5 Flash is Google DeepMind's newest frontier AI model — running four times faster than comparable models at $1.50 per million input tokens. It outperforms Gemini 3.1 Pro on complex coding and agentic benchmarks and is live across the Gemini API, Google AI Studio, Vertex AI, GitHub Copilot, and the Gemini app. For small business owners using AI tools for quotes, job summaries, or client emails, this represents a meaningful drop in cost-per-use. Frontier-level AI is no longer something that requires a subscription premium to access.",
    "{{TECH_1_URL}}": "https://www.marktechpost.com/2026/05/20/google-introduces-gemini-3-5-flash-at-i-o-2026-a-faster-and-cheaper-model-for-ai-agents-and-coding/",

    "{{TECH_2_FLAG}}": "⛪ TECH & SOCIETY",
    "{{TECH_2_HEADLINE}}": "Pope Leo XIV to Release First Papal Document on AI and Human Dignity — 'Magnifica Humanitas' Due Sunday",
    "{{TECH_2_SUMMARY}}": "Pope Leo XIV will publish his first encyclical, titled 'Magnifica Humanitas' (Magnificent Humanity), on Sunday 25 May 2026, setting out the Catholic Church's formal ethical framework for artificial intelligence. The document is expected to address automation, labour displacement, and the boundaries of human–machine interaction. Anthropic co-founder Christopher Olah is expected at the Vatican launch. Whatever your personal views, a papal encyclical on AI will shape ethical discourse in over 100 countries — a clear signal the AI debate has moved well beyond the tech sector into fundamental questions about work and what it means to be human.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "📊 INDUSTRY ROI",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robots Hit 6-Month Factory Payback Periods — Industry Analysis Signals Commercial Tipping Point",
    "{{ROBOT_1_SUMMARY}}": "A major industry analysis published this week confirms humanoid robots are beginning to show a clear return on investment, with payback periods in high-utilisation factory settings falling to approximately six months — down from 15 months just a year ago. Hardware costs continue to fall, with entry-level functional humanoids approaching $25,000: the level at which annual robot operating costs undercut a single human shift worker. Amazon, Apptronik at Mercedes-Benz, Boston Dynamics at Hyundai, and AgiBot are all in active commercial deployment. For industrial services businesses, the window to understand what these systems need — cleaning, protective coating, maintenance access — is closing faster than most realise.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/05/19/humanoid-robots-show-clearer-roi-but-commercial-success-depends-on-effective-output/101714/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Qantas Frontline Staff Approve 14% Pay Rise — Wage Benchmark Signal Ahead of Fair Work Decision",
    "{{AUS_1_SUMMARY}}": "Qantas frontline workers have voted to approve a new enterprise agreement delivering a 14% pay rise — one of the largest single rounds of wage growth seen at a major Australian employer in recent years. Labour economists are watching closely as a potential benchmark ahead of the Fair Work Commission's minimum wage decision in June, with some flagging it strengthens the case for a higher-than-expected award increase from July 1. For trades businesses, the broader signal is clear: wage expectations across the Australian workforce are resetting upward. Businesses that haven't reviewed award entitlements recently should do so before the July decision lands.",
    "{{AUS_1_URL}}": "https://www.aerotime.aero/articles/qantas-staff-secure-14-wage-increase-and-roster-protections-under-new-agreement",

    "{{AUS_2_HEADLINE}}": "Sydney CBD Teen Attack: Two Girls Charged After Assault on Bus Driver, Passenger and American Tourists",
    "{{AUS_2_SUMMARY}}": "NSW Police have charged two teenage girls — aged 16 and 17 — following an alleged assault spree in Sydney's CBD on Sunday 17 May. The pair allegedly attacked a bus driver and a 35-year-old passenger before assaulting two American female tourists on the street. A 19-year-old male was issued a move-on direction. Both girls were refused bail and appeared in the Children's Court on Monday 18 May. Security footage of the incident circulated widely online and reignited national debate about public safety on public transport.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Three Wyndham Teens Arrested Over Alleged Melbourne Nightclub Arson Attacks",
    "{{VIC_1_SUMMARY}}": "Victoria Police arrested three Wyndham men — two aged 18 and one aged 17 — on Wednesday 20 May after search warrants across Tarneit and Maribyrnong. The arrests relate to alleged arson attacks on Melbourne nightclubs La Di Da (CBD) and Electric Bar (Prahran) in early May, in which a vehicle was driven into the Prahran venue before accelerant was poured through both clubs. One suspect was allegedly found carrying a machete at Highpoint Shopping Centre. The trio face charges of arson, attempted arson, criminal damage, burglary, and vehicle theft, and are being interviewed by detectives.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ PHYSICS",
    "{{SCI_1_HEADLINE}}": "Decades-Long Physics Mystery May Have Just Been a Calculation Error All Along",
    "{{SCI_1_SUMMARY}}": "For over 50 years, physicists measured a subtle property of the muon — a heavy cousin of the electron — and found it stubbornly at odds with the Standard Model's predictions. The persistent discrepancy fuelled serious speculation about hidden forces and undiscovered particles beyond our current understanding of the universe. Now, after years of intensive supercomputer calculations, a team led by Professor Zoltan Fodor at Pennsylvania State University has concluded the anomaly was almost certainly a calculation error: the most mathematically difficult part of the puzzle — how the 'strong force' of quarks influences the muon's magnetic moment — had been computed incorrectly all along. The Standard Model holds. The search for physics beyond it now shifts to other frontiers. Reported by ScienceDaily and TechExplorist, May 19, 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Systematise Your New Client Onboarding — and Stop Every Job Starting in Chaos",
    "{{INSIGHT_BODY}}": "Most trades businesses treat new client onboarding the same way: wing it, get the job done, deal with the details later. But every time you start a job without a consistent intake process, you're building in risk — unsigned scopes, unclear access arrangements, no documented site conditions, and no paper trail if something goes sideways. AI can fix this without adding much admin time. The approach is straightforward: use Claude or ChatGPT to draft a standard new-client intake checklist — eight to ten questions covering scope, access, site hazards, payment terms, and any client-specific requirements. Drop it into a Google Form and make it your non-negotiable first step before any quote goes out. Then ask AI to generate a one-page client confirmation summary from the intake responses: what's agreed, what's excluded, and what the payment schedule looks like. You've created a light contract without paying a lawyer. For ISV, where jobs involve chemical handling, access to occupied premises, and equipment on third-party sites, a consistent intake process is also a WHS paper trail. AI makes the setup fast — a few hours once. After that, every job starts better than the one before.",

    # Fun Facts
    "{{FACT_1}}": "A 'jiffy' is an actual unit of scientific measurement, not just an expression. In computing, one jiffy equals one hundredth of a second — ten milliseconds — and governs the minimum interval between system clock ticks in many operating systems. In physics, a jiffy is the time it takes light to travel one centimetre, approximately 33 picoseconds. The word entered English in the 18th century as slang for 'a very short time' before being formally adopted as a precise quantity in multiple scientific disciplines.",

    "{{FACT_2}}": "Spider silk is approximately five times stronger than steel by weight, and can stretch up to 40 per cent of its own length before breaking. A thread the diameter of a garden hose would theoretically be strong enough to halt a Boeing 747 in mid-flight. Despite decades of biotechnology research, no manufacturing process has successfully replicated the full combination of tensile strength, elasticity, and lightness that spiders achieve at room temperature using nothing but protein dissolved in water.",

    "{{FACT_3}}": "Coffee is the world's most traded agricultural commodity by value, and the second most traded commodity of any kind after crude oil. It is produced by approximately 125 million people concentrated in a band of countries between the Tropics of Cancer and Capricorn known as the Coffee Belt. Australia grows its own coffee in small quantities in the Atherton Tablelands of far north Queensland — conditions are marginal for the plant, but yields command premium prices on the specialty market.",

    # Joke
    "{{JOKE_SETUP}}": "Why do land surveyors always win property boundary disputes?",
    "{{JOKE_PUNCHLINE}}": "They know exactly where to draw the line.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Remember to look up at the stars and not down at your feet.”",
    "{{CLOSING_ATTR}}": "— Stephen Hawking",
    "{{CLOSING_MESSAGE}}": "Thursday morning in Carrum Downs — foggy to start, clearing to 16°C with a mostly cloudy afternoon, and then things get genuinely good: partly cloudy Friday, mostly sunny Saturday at 19°C. The Strait of Hormuz situation continues to simmer overnight — Iran is running a million-dollar-a-ship toll booth and 230 loaded tankers are going nowhere, so fuel cost volatility isn't resolving this week. On the wages front, the ACTU lifted its Fair Work claim to 6% — the decision lands in weeks. July 1 is shaping up as a triple cost hit: fuel excise ends, payday super starts, and a likely wage rise kicks in. If you're quoting work that runs past July 1, factor all three in now rather than explain the shortfall in August. Good week ahead, Liall.",
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
