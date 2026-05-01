#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 02 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Sat 2 May
    "{{WEATHER_1}}": "Sat 2 May · Showers · 15°C",
    "{{WEATHER_2}}": "Sun 3 May · Mostly cloudy · 15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Mon 4 May · Clearing · 17°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Tue 5 May · Fine · 19°C",
    "{{WEATHER_5}}": "Wed 6 May · Partly cloudy · 19°C",
    "{{WEATHER_ALERT}}": "Wet Saturday morning",

    # World
    "{{WORLD_1_FLAG}}": "🇲🇲 MYANMAR · POLITICS",
    "{{WORLD_1_HEADLINE}}": "Myanmar Junta Moves Aung San Suu Kyi from Prison to House Arrest After Five Years",
    "{{WORLD_1_SUMMARY}}": "Myanmar's military government transferred the detained Nobel Peace Prize laureate and former leader Aung San Suu Kyi from Naypyidaw prison to house arrest on April 30, following a partial sentence reduction tied to a Buddhist holiday amnesty. Suu Kyi, 80, still faces over 13 years of her sentence. Her lawyers and son Kim Aris say they cannot confirm the transfer and warn she remains cut off from contact with the outside world. The UN Secretary-General called it \"a meaningful step,\" while democracy advocates remain cautious.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/4/30/myanmars-former-leader-aung-san-suu-kyi-moved-from-prison-to-house-arrest",

    "{{WORLD_2_FLAG}}": "⚓ MIDDLE EAST · CONFLICT",
    "{{WORLD_2_HEADLINE}}": "Israeli Navy Intercepts Gaza Aid Flotilla in International Waters; 170 Activists Detained",
    "{{WORLD_2_SUMMARY}}": "The Israeli navy intercepted the Global Sumud Flotilla late Wednesday while the convoy attempted to reach Gaza, stopping it more than 500 nautical miles from Israel — off Crete. Around 170 activists from multiple countries were detained and taken ashore, including six Australians. Two activists remained in Israeli custody. Flotilla organisers condemned the interception as an act of piracy in international waters; Israel said the vessels were stopped to enforce the maritime blockade.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/5/1/gaza-aid-flotilla-vessels-taken-to-crete-after-israeli-interception",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 AUSTRALIA · RBA",
    "{{ECON_1_HEADLINE}}": "RBA Rate Decision Due Tuesday — Economists Now Tipping Another Rise to 4.35%",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank meets Monday–Tuesday (May 4–5) and announces its decision at 2:30pm AEST Tuesday. The cash rate sits at 4.10% following March's rise. With inflation hitting 4.6% — a three-year high driven by the Middle East supply shock — CBA and Westpac are now both tipping a further 25-basis-point rise to 4.35%. For small business owners carrying variable-rate loans, two rises this close together is a meaningful cost increase. Worth reviewing fixed-rate options before Tuesday's call.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/monetary-policy/int-rate-decisions/",

    "{{ECON_2_FLAG}}": "⛽ AUSTRALIA · FUEL",
    "{{ECON_2_HEADLINE}}": "Fuel Excise Cut Helping at the Pump — But It Expires June 30 and Inflation Stays Elevated",
    "{{ECON_2_SUMMARY}}": "The government's temporary halving of the fuel excise to 26.3 cents per litre has provided some pump relief since April 1, but economists warn the cut expires June 30 and underlying inflation remains at 4.6%. Fuel costs have spread through the supply chain, lifting freight, materials, and services pricing. For Melbourne trades operators, diesel prices are still well above pre-crisis levels even with the excise cut in place — auditing your fuel surcharge agreements now, before the excise snaps back, is a smart move.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🇺🇸 US · DEFENSE AI",
    "{{TECH_1_HEADLINE}}": "Pentagon Signs AI Deals with OpenAI, Google, Nvidia, Microsoft and Amazon for Classified Military Use",
    "{{TECH_1_SUMMARY}}": "The US Department of Defense announced on May 1 that seven leading AI companies — OpenAI, Google, Nvidia, Microsoft, Amazon Web Services, Reflection AI, and SpaceX — have signed agreements to deploy their AI on the Pentagon's most classified networks (Impact Level 6 and 7). The technology will be used for battlefield decision-making and intelligence analysis. More than 1.3 million Defence personnel have already used the military's AI platform. Anthropic was notably excluded after being designated a supply-chain risk earlier this year.",
    "{{TECH_1_URL}}": "https://www.washingtonpost.com/technology/2026/05/01/pentagon-ai-deals-microsoft-amazon-google-classified-military/",

    "{{TECH_2_FLAG}}": "🔬 AI · RESEARCH",
    "{{TECH_2_HEADLINE}}": "Study: Top AI Agents Still Perform at Half the Level of Expert Human Scientists on Complex Tasks",
    "{{TECH_2_SUMMARY}}": "A study published in Nature found that the best autonomous AI agents perform at only about half the level of PhD-level human experts when given genuinely complex scientific tasks requiring original reasoning and judgement. While AI tools are dramatically boosting individual researcher output, they are not yet replacing domain expertise on hard problems. For business owners evaluating AI tools: the data confirms they work best as high-powered assistants to skilled people — not as stand-alone replacements for experience.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳 CHINA · ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "China Commits $1 Billion to Deploy 8,500 Robots — Including 5,000 Robot Dogs — Across Its National Power Grid",
    "{{ROBOT_1_SUMMARY}}": "China's State Grid Corporation, operator of the world's largest electricity network, has allocated 6.8 billion yuan (~$1 billion AUD) in 2026 to acquire roughly 8,500 AI-powered robots for power infrastructure operations. The fleet includes about 5,000 quadruped 'robot dogs' for patrol and inspection in remote and mountainous terrain, plus humanoid and dual-arm robots for high-risk maintenance tasks. Described as the single largest embodied-AI procurement by any government entity worldwide, the deployment covers substations, transmission lines, and transformer yards across China. Industrial-scale robot deployment has moved from pilot programme to national infrastructure strategy.",
    "{{ROBOT_1_URL}}": "https://interestingengineering.com/ai-robotics/china-8500-robots-power-grid",

    # Australia
    "{{AUS_1_HEADLINE}}": "Six Australians Detained on Gaza Flotilla Moved to Crete; DFAT Providing Consular Assistance",
    "{{AUS_1_SUMMARY}}": "Six Australians who were aboard the Global Sumud Flotilla — intercepted by Israeli forces in international waters on Wednesday — have been transferred to Crete, where DFAT is providing consular assistance. The group includes a doctor and several activists. Families say they have been unable to make phone contact and are calling for urgent access.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/israel-sumudarrests-approximately-175-gaza-flotilla-activists-in-international-waters-near-greece/w99w04idl",

    "{{AUS_2_HEADLINE}}": "Antisemitism Royal Commission Releases Interim Report; Government Accepts All 14 Recommendations",
    "{{AUS_2_SUMMARY}}": "The interim report from Australia's Royal Commission into antisemitism and the December 2025 Bondi attack has been released, with the Albanese government committing to implement all 14 recommendations. Key measures include nationally consistent gun laws, a firearm buyback programme, enhanced security at places of worship, and a full-time national counter-terrorism coordinator. The final report is due by December 14.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Victory Host Sydney FC in A-League 'Big Blue' Elimination Final Tonight at AAMI Park",
    "{{VIC_1_SUMMARY}}": "Melbourne Victory host fifth-placed Sydney FC in an A-League Men Elimination Final at AAMI Park tonight, kick-off at 7:40pm AEST. Dubbed the 'Big Blue,' it's the first time the two foundation clubs have met in the finals series since 2019. The loser goes home. Live on Paramount+ and Network 10.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 SCIENCE · MEDICINE",
    "{{SCI_1_HEADLINE}}": "New DNA-Based Treatment Cuts 'Bad' LDL Cholesterol by Nearly 50% — Without Statins or Side Effects",
    "{{SCI_1_SUMMARY}}": "Researchers at the University of Barcelona have developed a novel treatment using DNA molecules called polypurine hairpins (PPRHs) that block the PCSK9 protein — the key regulator that prevents the body from clearing LDL 'bad' cholesterol from the bloodstream. By silencing the PCSK9 gene, early trials showed LDL levels cut by nearly 50%, without the muscle pain and other side effects linked to statins. Published May 1 in Biochemical Pharmacology, the approach could offer a new path for the millions of Australians managing cholesterol with daily medication.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI-Assisted Job Scheduling Is Killing the Double-Booking Problem for Small Trades",
    "{{INSIGHT_BODY}}": "For small operators juggling multiple crews, varied job lengths, and unpredictable travel time across Melbourne's south-east, scheduling is one of the most expensive invisible costs in the business. AI-assisted scheduling tools — built into platforms like ServiceM8, Tradify, and Fergus, or available as standalone apps — analyse your job pipeline, crew locations, and travel time in real time, flagging conflicts before they become missed appointments or back-to-back blowouts. Businesses trialling these tools report fewer double-bookings, smarter crew sequencing, and better client communication through automated reminders and updated ETAs. In a market where reliability is a genuine point of difference, a tool that prevents one double-booking a month could easily pay for itself in retained customers alone.",

    # Fun Facts
    "{{FACT_1}}": "The mantis shrimp has 16 types of colour photoreceptors in its eyes — compared to just 3 in humans — yet it's a surprisingly poor colour discriminator. Scientists discovered it doesn't compare wavelengths the way humans do; instead it uses rapid eye movements to scan the spectrum like a barcode reader, trading colour nuance for extraordinary processing speed.",
    "{{FACT_2}}": "Your gut contains approximately 100 million neurons — more than the entire spinal cord — forming what neuroscientists call the 'enteric nervous system' or 'second brain.' It operates largely independently of your head brain, continuing to regulate digestion, immune responses, and serotonin production even after the nerve connection between them is severed.",
    "{{FACT_3}}": "The Apollo Guidance Computer that landed humans on the Moon in 1969 had just 4 kilobytes of RAM and ran at 0.043 MHz. A modern smartphone has roughly 8 billion times more RAM. The software was hand-woven into core rope memory by MIT programmers — it was this project that led Margaret Hamilton to coin the term 'software engineering.'",

    # Joke
    "{{JOKE_SETUP}}": "Why did the painter refuse to repaint the kitchen ceiling?",
    "{{JOKE_PUNCHLINE}}": "He said the last coat was still a bit above his head.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"It always seems impossible until it's done.\"",
    "{{CLOSING_ATTR}}": "Nelson Mandela",
    "{{CLOSING_MESSAGE}}": "It's Saturday, Liall — wet morning forecast in Carrum Downs, which makes it a good day for desk work before tonight's A-League Big Blue at AAMI Park (Victory vs Sydney FC, 7:40pm). RBA decision lands Tuesday, so keep an eye on your loan costs. Six Australians are safely in Crete. Make it a productive one.",
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
