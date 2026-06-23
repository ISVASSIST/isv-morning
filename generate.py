#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 24 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 24 Jun
    "{{WEATHER_1}}": "WED 24 · 🌧 Showers · 13°C",
    "{{WEATHER_2}}": "THU 25 · ☁ Cloudy/showers · 12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 26 · 🌧 Showers · 13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 27 · ⛅ Partly cloudy · 14°C",
    "{{WEATHER_5}}": "SUN 28 · ⛅ Partly cloudy · 14°C",
    "{{WEATHER_ALERT}}": "☁ DAMP WEEK · 6 DAYS TO EOFY",

    # World
    "{{WORLD_1_FLAG}}": "🌐 USA · IRAN · PEACE AGREEMENT",
    "{{WORLD_1_HEADLINE}}": "Trump and Iran Sign Initial Peace Agreement — 60-Day Nuclear Roadmap and Hormuz Deconfliction Channel Established",
    "{{WORLD_1_SUMMARY}}": "US President Donald Trump and Iranian President Masoud Pezeshkian signed an initial agreement on Wednesday aimed at formally ending Middle East hostilities, as mediators confirmed a 60-day roadmap for a final nuclear deal reached in Switzerland. Three working groups on sanctions, nuclear oversight, and weapons arrangements have been established, alongside a dedicated Strait of Hormuz deconfliction channel to reduce the risk of maritime incidents. The core question — the extent of Iran's uranium enrichment — remains unresolved and is expected to dominate the negotiating period ahead. For Australian businesses tracking fuel costs, the 60-day window runs to late August, meaning the Strait of Hormuz remains an elevated geopolitical risk on global diesel prices well beyond July 1, when Australia's domestic excise restoration adds roughly 32 cents per litre regardless of how the talks progress.",
    "{{WORLD_1_URL}}": "https://www.nbcnews.com/world/iran/us-iran-talks-war-vance-trump-hormuz-lebanon-switzerland-foundation-rcna351112",

    "{{WORLD_2_FLAG}}": "🌐 CHINA · USA · SANCTIONS",
    "{{WORLD_2_HEADLINE}}": "China Sanctions 10 US Defence Companies in Latest Tech Decoupling Escalation",
    "{{WORLD_2_SUMMARY}}": "China's government announced sanctions against 10 US military-related companies on Monday, in direct retaliation for the US decision to bar leading Chinese technology companies from defence contracts. The move represents the latest chapter in a sustained bilateral technology decoupling reshaping global supply chains for electronics, semiconductors, and industrial components — sectors that flow directly through Australian trade networks. For businesses importing equipment with US or Chinese-origin components, the escalating sanctions environment adds cost and lead-time uncertainty to procurement decisions, particularly for industrial equipment purchasing windows extending beyond the current quarter.",
    "{{WORLD_2_URL}}": "https://abcnews.com/international",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ NBN · SUBCONTRACTORS · FUEL SQUEEZE",
    "{{ECON_1_HEADLINE}}": "NBN Subcontractors Stage 24-Hour Walkout in NSW — Rising Fuel Costs and Pay Cuts the Core Grievance",
    "{{ECON_1_SUMMARY}}": "Subcontractors working on NBN rollout and maintenance in New South Wales staged a 24-hour industrial walkout this week, citing the compounding pressure of rising fuel costs alongside cuts to pay rates under newly restructured contracts. The action highlights the acute position facing sub-contracting businesses in sectors where diesel is a direct daily operating cost — familiar territory for any Carrum Downs operator running work vehicles and mobile equipment. The walkout falls in the final week before Australia's fuel excise reduction expires: from July 1, diesel rises roughly 32 cents per litre, and any subcontract agreement that does not explicitly address post-July 1 fuel costs will lock operators into rates that are already under pressure before the excise restoration lands.",
    "{{ECON_1_URL}}": "https://www.smartcompany.com.au/economy/australia-fuel-crisis-essential-updates-businesses/",

    "{{ECON_2_FLAG}}": "🏠 PROPERTY · AUCTIONS · JUNE 2026",
    "{{ECON_2_HEADLINE}}": "National Auction Clearance Rate Falls Below 50% for First Time Since COVID — Leading Signal for Trades Demand in H2 2026",
    "{{ECON_2_SUMMARY}}": "Australia's residential property auction clearance rate has fallen below 50 per cent nationally for the first time since the early COVID period, according to CoreLogic data for the week ending June 21. Melbourne has been among the most affected markets as rate-sensitive buyers step back amid uncertainty over the Albanese government's proposed negative gearing and capital gains tax changes. For small trades operators in Melbourne's southeast, falling clearance rates are a leading indicator: fewer property transactions means reduced demand for pre-sale preparation, post-purchase renovation, and the discretionary maintenance work that drives a significant share of residential trades revenue heading into the second half of 2026.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 META · AI · RESTRUCTURE · JUNE 2026",
    "{{TECH_1_HEADLINE}}": "Meta Begins 8,000-Employee Layoffs in AI Restructure — a Further 7,000 Reassigned to AI-Focused Teams",
    "{{TECH_1_SUMMARY}}": "Meta has begun implementing approximately 8,000 layoffs, with a further 7,000 employees internally reassigned to AI-focused divisions — a significant restructuring reflecting the company's strategic bet that its future across advertising, hardware, and platforms depends on AI at every layer of the stack. It continues the broader industry shift of major technology companies reorganising around AI capabilities rather than traditional product lines. The practical signal for small business operators arrives in 12 to 24 months: the Meta platforms used daily for advertising and client communication — Instagram, WhatsApp Business, Facebook — will be increasingly AI-automated. Businesses that understand AI-driven content and advertising today will hold a structural advantage as platforms automate what currently requires specialist knowledge or agency spend.",
    "{{TECH_1_URL}}": "https://techcrunch.com/category/artificial-intelligence/",

    "{{TECH_2_FLAG}}": "🖥️ REFLECTION AI · NVIDIA · COMPUTE RACE",
    "{{TECH_2_HEADLINE}}": "Reflection AI to Pay $150 Million Per Month for Nvidia GB300 Chips From July 1 — The True Scale of the AI Infrastructure Race",
    "{{TECH_2_SUMMARY}}": "Reflection AI has committed to spending $150 million per month from July 1, 2026 through to 2029 for priority access to Nvidia's latest GB300 AI accelerator chips — a three-year commitment totalling over $5 billion for compute alone. The numbers contextualise why AI tools available through cloud services are improving at pace: the companies building foundation models are deploying capital at a rate that was unthinkable in enterprise technology just two years ago. The AI capabilities reaching trades businesses through Claude, Copilot, and Gemini-class tools over the next 12 to 24 months are funded by commitments like this — meaning the capability step-change coming is already locked in and being built right now.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 FIGURE AI · BOTQ · PRODUCTION MILESTONE",
    "{{ROBOT_1_HEADLINE}}": "Figure AI Reaches One Humanoid Robot Per Hour at BotQ — 24× Production Throughput Improvement Achieved in Under 120 Days",
    "{{ROBOT_1_SUMMARY}}": "Figure AI's BotQ production facility has reached a rate of one Figure 03 humanoid robot completed per hour — up from one per day at the start of the year — a 24-fold throughput improvement achieved in under 120 days of ramping. End-of-line first-pass yield rates are running above 80 per cent, which is considered strong manufacturing performance for a product class that did not commercially exist before 2024. At current run rates, the facility is on track for approximately 8,000 to 12,000 units annually, with further capacity expansion planned. The ramp is being watched closely as the first clear market signal of when humanoid robot supply can begin matching industrial demand — a crossover point that mid-2026 production data now suggests is approaching faster than most forecasts assumed.",
    "{{ROBOT_1_URL}}": "https://www.marketscale.com/industries/industrial-iot/humanoid-supply-outpaces-demand-amrs-hit-toyota-plants-and-robot-orders-hold-steady-automations-defining-stories-of-mid-2026/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Greens Vow to Fight NDIS Spending Cuts in Senate as Disability Sector Warns of Access Rollbacks",
    "{{AUS_1_SUMMARY}}": "The Greens have confirmed they will use their Senate crossbench position to block or substantially amend the Albanese government's proposed NDIS expenditure changes, with senators warning the reforms will reduce access for existing participants. The government argues the changes are essential to manage scheme costs now approaching $50 billion annually; disability advocates say the restructure will leave many participants without adequate support. The standoff will play out over coming weeks as the Senate works through a packed budget legislation calendar ahead of the mid-year economic and fiscal update.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/",

    "{{AUS_2_HEADLINE}}": "Two Sydney Residents Face Life Sentences After 200kg Drug Haul Uncovered in Bunkers Beneath Shipping Containers",
    "{{AUS_2_SUMMARY}}": "Two Sydney residents have been charged after approximately 200 kilograms of drugs were discovered concealed in plastic tubs buried in bunkers hidden beneath three shipping containers in NSW, with the find made on June 19 following an extended investigation. Both accused face potential life sentences. The case highlights the continued use of Australian port and logistics infrastructure for large-scale drug concealment operations, and is among the largest single seizures recorded in New South Wales this year.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Half-Price Public Transport Fares Continue Through 2026 as July Fuel Price Rise Approaches",
    "{{VIC_1_SUMMARY}}": "Victoria's public transport fares remain at half the standard rate across the network for the remainder of 2026, providing ongoing cost relief for commuters on metropolitan rail, trams, and regional coaches. The Frankston line serving Carrum Downs and Melbourne's wider southeast corridor is among the routes where workers continue to benefit. With fuel excise restoration set to lift diesel and petrol prices roughly 32 cents per litre from July 1, the continued half-price fare structure makes public transport an increasingly competitive option for workers commuting into Melbourne's southeast industrial zones, including those heading to and from Carrum Downs.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 NATURE · NUCLEAR CLOCKS · JUNE 23 2026",
    "{{SCI_1_HEADLINE}}": "World's First Nuclear Clocks Start Ticking — Two Independent Teams Publish Simultaneously in Nature, Opening a New Era in Precision Physics",
    "{{SCI_1_SUMMARY}}": "Two independent teams of physicists — one European, one at Tsinghua University in Beijing — have simultaneously built and published working nuclear clocks: timekeepers that use oscillations within a thorium-229 atomic nucleus rather than the electron energy states used by conventional atomic clocks. Because atomic nuclei are far more tightly bound than electron clouds, nuclear clocks are potentially up to 1,000 times more precise than the best current atomic clocks. More significantly, they are sensitive to three of the four fundamental forces — the strong nuclear force, weak nuclear force, and electromagnetism — making them powerful tools for detecting dark matter, testing whether the physical constants of the universe are truly constant over time, and probing a hypothetical fifth fundamental force. Two teams, two different approaches, the same result published in Nature on June 23: a new era in precision timekeeping has begun.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The One-Hour AI Audit Every Trades Business Should Run Before July 1",
    "{{INSIGHT_BODY}}": "Six days from now, three simultaneous cost changes land for Australian small businesses: fuel excise restoration adds approximately 32 cents per litre to diesel and petrol, the minimum award wage rises by $26.44 per week per full-time employee, and payday superannuation takes effect — requiring super to be paid every pay cycle rather than quarterly. For a Carrum Downs trades business running two employees and a work vehicle, the combined daily cost impact across a typical job could be $80 to $120. One hour with an AI tool before July 1 can turn that into a clear plan rather than a July shock. Ask Claude or a similar tool to model the impact: input your current charge-out rates, employee costs, daily fuel usage, and target margin — the AI will calculate your new breakeven rate, identify which job types are most exposed to the combined cost increase, and produce a revised rate card for FY2027. It will also draft client notification language — professional, direct, non-apologetic — explaining the July 1 adjustment before it lands as a surprise. The businesses that navigate cost shocks well are the ones that modelled the impact in advance, adjusted their rates decisively, and communicated clearly before the change arrived. Six days is still enough runway. The hour you spend with AI this week is worth more than the hours you will spend recalculating margins by hand in August.",

    # Fun Facts
    "{{FACT_1}}": "The world's oldest known cookbook is not a book — it is a set of four clay tablets known as the Yale Culinary Tablets, dating to around 1700 BC from ancient Mesopotamia (modern Iraq). Written in Akkadian cuneiform, they record 35 recipes including three types of meat stew and assume professional kitchen knowledge, suggesting they were written for trained cooks rather than home use. The oldest individual recipe recorded in human history is a lamb broth.",

    "{{FACT_2}}": "Koalas have fingerprints so similar to human fingerprints that forensic examiners have occasionally mistaken koala prints for human ones at crime scenes — a finding confirmed in published forensic research. Koalas and humans evolved fingerprints entirely independently over tens of millions of years of separate evolutionary history, making this one of the most striking examples of convergent evolution in the animal kingdom. Among all non-human animals, only great apes, koalas, and a handful of primate species have true fingerprints.",

    "{{FACT_3}}": "The world's first commercial nuclear power plant — the Obninsk Nuclear Power Plant in the Soviet Union — began generating electricity on 27 June 1954, producing just 5 megawatts from a single reactor. This Saturday marks its 72nd anniversary. Today nuclear power provides approximately 10 per cent of global electricity; France leads the world at around 70 per cent nuclear generation — the same fleet currently under peak summer stress from this week's European heatwave.",

    # Joke
    "{{JOKE_SETUP}}": "I tried to cook the perfect steak using the sous vide method my apprentice recommended.",
    "{{JOKE_PUNCHLINE}}": "Four hours, a water bath, and three leads running off the one board — tasted exactly like the $12 sizzle steak I could've done in eight minutes on the gas.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The way I see it, if you want the rainbow, you gotta put up with the rain.”",
    "{{CLOSING_ATTR}}": "— Dolly Parton",
    "{{CLOSING_MESSAGE}}": "It's Wednesday June 24 — six days to the end of the financial year and the July 1 triple cost hit. Winter is fully locked in at Carrum Downs today, showers and 13°C; plan outdoor work in short windows and keep diesel topped up before the price jumps. Overnight news: Trump and Iran's Pezeshkian signed an initial peace agreement — significant for global oil markets, though the 60-day nuclear negotiating window means Hormuz risk stays elevated through August. China sanctioned 10 US defence companies on Monday. Closer to home, national auction clearance rates dropped below 50% for the first time since COVID — a leading signal for consumer spending and residential trades demand in the second half of the year. Meta is laying off 8,000 people and refocusing on AI; Figure AI is now building one humanoid robot per hour. Two independent teams of physicists just published the world's first nuclear clocks in Nature yesterday. Some weeks move fast. Six days left in this financial year — make the one hour with AI count before July 1 arrives.",
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
