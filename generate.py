#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 05 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Tue 5 May
    "{{WEATHER_1}}": "Tue 5 May · Showers · 14–17°C",
    "{{WEATHER_2}}": "Wed 6 May · Heavy showers · 13–18°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Thu 7 May · Very heavy showers · 12–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "Fri 8 May · Clearing · 11–15°C",
    "{{WEATHER_5}}": "Sat 9 May · Mostly dry · 9–14°C",
    "{{WEATHER_ALERT}}": "⚠ Heavy rain Wed–Thu · Up to 20mm",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 MIDDLE EAST · IRAN",
    "{{WORLD_1_HEADLINE}}": "Trump Calls US-Iran Talks \"Very Positive\" as Both Sides Exchange Responses on Peace Terms",
    "{{WORLD_1_SUMMARY}}": "US President Donald Trump said on Sunday that his representatives are having 'very positive discussions' with Iran, even as both sides exchange conflicting signals on key sticking points. Iran has now received a formal US response to its 14-point peace proposal — which demands sanctions relief, war reparations, and US force withdrawal — but Washington continues to insist on stringent nuclear restrictions as a precondition. Day 65 of the conflict: global oil supply disruption through the Strait of Hormuz remains severe, with shipping still well below pre-war levels.",
    "{{WORLD_1_URL}}": "https://www.cnbc.com/2026/05/03/trump-iran-war-peace-proposal.html",

    "{{WORLD_2_FLAG}}": "🌐 PRESS FREEDOM",
    "{{WORLD_2_HEADLINE}}": "Global Press Freedom Falls to 25-Year Low — 471 Journalists Imprisoned, 13 Killed in 2026",
    "{{WORLD_2_SUMMARY}}": "Reporters Without Borders released its 2026 World Press Freedom Index on World Press Freedom Day (May 3), recording the lowest press freedom scores in a quarter century. Thirteen journalists have been killed globally so far in 2026, 471 are behind bars, and at least 21 are held hostage. The report cites authoritarian crackdowns, AI-generated disinformation, and the fallout from ongoing geopolitical conflicts as the key drivers of the decline.",
    "{{WORLD_2_URL}}": "https://www.democracynow.org/2026/5/4/headlines",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 INTEREST RATES · RBA",
    "{{ECON_1_HEADLINE}}": "RBA Decision at 2:30pm Today — Markets Tip 25bp Hike Taking Cash Rate to 4.35%",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank of Australia announces its May cash rate decision at 2:30pm AEST this afternoon. Markets are pricing a 70–75% chance of a 25-basis-point hike that would take the cash rate to 4.35% — its highest since 2011 — with headline inflation stuck at 4.6%, well above the 2–3% target. For small businesses carrying variable-rate debt or equipment finance, a rise feeds through to repayments within weeks. Worth keeping an eye on the 2:30pm announcement.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/monetary-policy/int-rate-decisions/",

    "{{ECON_2_FLAG}}": "⛽ FUEL · EXCISE",
    "{{ECON_2_HEADLINE}}": "Fuel Excise Cut Runs to 30 June — But the 56-Day Countdown Demands a Pricing Plan Now",
    "{{ECON_2_SUMMARY}}": "The Government's 32c/litre fuel excise cut (April 1 – June 30) continues to hold retail diesel at roughly $2.75 nationally — real relief for trades operators running fleets. But the June 30 expiry is 56 days away, and with Hormuz disruptions ongoing and the global oil market still volatile, a post-July price snapback is a genuine risk. For any job you're quoting that runs past July, building a fuel cost contingency into your pricing now is basic risk management.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · LEADERSHIP",
    "{{TECH_1_HEADLINE}}": "IBM Study: 76% of Major Companies Now Have a Chief AI Officer — Up From 26% a Year Ago",
    "{{TECH_1_SUMMARY}}": "A major IBM Institute for Business Value study of 2,000 CEOs across 33 countries (released May 4) reveals that AI leadership has exploded: 76% of organisations now have a dedicated Chief AI Officer, up from just 26% in 2025. Sixty-four per cent of CEOs say they are comfortable making major strategic decisions based on AI-generated input. Companies that redesigned five core business functions around AI were four times more likely to meet their business objectives.",
    "{{TECH_1_URL}}": "https://newsroom.ibm.com/2026-05-04-ibm-study-ceos-are-reshaping-c-suite-roles-for-the-ai-era",

    "{{TECH_2_FLAG}}": "🔒 AI · MILITARY",
    "{{TECH_2_HEADLINE}}": "Google Staff Revolt Over Pentagon Deal — 600 Employees Oppose Military Use of Gemini AI",
    "{{TECH_2_SUMMARY}}": "Close to 600 Google employees have signed an open letter opposing the company's agreement to provide its Gemini AI models to US military classified networks for 'any lawful purpose.' The backlash, reported May 4, echoes the 2018 Project Maven controversy that forced Google to withdraw from military AI contracts. The episode deepens the debate about where ethical lines sit as AI becomes embedded in defence and national security infrastructure.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 WAREHOUSE ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "Locus Robotics Launches AI-Powered \"Locus Array\" for Fully Autonomous Warehouse Fulfillment",
    "{{ROBOT_1_SUMMARY}}": "Locus Robotics unveiled 'Locus Array' on May 3 — a fully autonomous order fulfillment system combining mobile robots, an integrated picking arm, and AI-powered perception that completes end-to-end warehouse workflows without any human intervention. The launch marks a significant step beyond assisted picking toward true lights-out automation. Early deployments are underway in North America, with global rollout across Europe and Asia-Pacific planned as demand for fully autonomous fulfillment accelerates.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/05/03/locus-robotics-rolls-out-locus-array-for-end-to-end-warehouse-fulfillment/101175/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia and Japan Sign Landmark Pact on Defence, Energy Security and Critical Minerals",
    "{{AUS_1_SUMMARY}}": "Prime Ministers Anthony Albanese and Japan's Sanae Takaichi signed major new agreements in Canberra on Monday, deepening cooperation on defence, energy security, and critical minerals supply chains. The deal directly targets China's dominance of rare earth production and comes as the Iran war underscores the strategic value of Australia-Japan energy ties — Australia already supplies close to half of Japan's LNG.",
    "{{AUS_1_URL}}": "https://www.bnnbloomberg.ca/business/2026/05/04/japan-and-australia-agree-to-deepen-cooperation-on-energy-defence-and-critical-minerals/",

    "{{AUS_2_HEADLINE}}": "Royal Commission on Antisemitism Opens First Public Hearings Across Australia",
    "{{AUS_2_SUMMARY}}": "Australia's Royal Commission into antisemitism and social cohesion commenced its first public hearings on Monday, with witnesses sharing testimony about their personal experiences. The commission will take evidence from communities, educators, and institutions across the country over several months as it examines the current state of social cohesion nationally.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Budget to Double Safety Officers and Turn Southbank Underpass Into 5,000m² Public Park",
    "{{VIC_1_SUMMARY}}": "The City of Melbourne's draft 2026-27 budget proposes doubling Community Safety Officers from 11 to 22 to address rising antisocial behaviour concerns, and converting a neglected Southbank concrete underpass into a 5,000 square metre activated public space — featuring a roller rink, skate park, bouldering wall, basketball courts, and improved lighting.",

    # Science
    "{{SCI_1_FLAG}}": "🦋 EVOLUTION",
    "{{SCI_1_HEADLINE}}": "Evolution Has Used the Same Two Genes to Build Identical Wing Patterns for 120 Million Years",
    "{{SCI_1_SUMMARY}}": "An international team led by the University of York and Wellcome Sanger Institute has found that distantly related butterflies and moths in South American rainforests independently evolved near-identical warning colour patterns by reusing the exact same pair of genes — ivory and optix — across 120 million years. Rather than altering the genes themselves, evolution acted on genetic 'switches' that control when and where they activate. The finding challenges assumptions about evolutionary randomness, suggesting life follows more predictable genetic pathways than previously thought. Published in PLOS Biology.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "When Material Costs Spike, AI Can Be Your Purchasing Manager — For Free",
    "{{INSIGHT_BODY}}": "With inflation running at 4.6% and supply chains still absorbing the shocks of global energy disruption, small trades operators are being squeezed from both directions — rising material costs and the prospect of higher borrowing costs. AI tools integrated with supplier catalogues and invoicing platforms can now monitor price movements, generate alternative supplier comparisons, and draft purchase enquiries automatically. Tradies who've started using AI for procurement report savings of 8–15% by identifying better-priced substitutes or flagging when to buy ahead of known price rises. The investment is zero beyond a subscription you may already have — the question is whether you're putting it to work yet.",

    # Fun Facts
    "{{FACT_1}}": "A bolt of lightning is roughly five times hotter than the surface of the sun — reaching around 30,000°C — yet is only about 2–3 centimetres wide. Earth is struck by lightning approximately 1.4 billion times every year.",
    "{{FACT_2}}": "The wingspan of a Boeing 747 is longer than the entire first flight made by the Wright Brothers — the Flyer covered just 37 metres at Kitty Hawk in 1903, while a 747's wings span 68 metres tip to tip.",
    "{{FACT_3}}": "Australia's Anna Creek Station in South Australia is the world's largest working cattle station at around 24,000 square kilometres — bigger than Israel and roughly the size of Wales.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the carpenter win the workplace safety award?",
    "{{JOKE_PUNCHLINE}}": "He was the only one on site who knew when to stop — and he never cut corners.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Price is what you pay. Value is what you get.\"",
    "{{CLOSING_ATTR}}": "Warren Buffett",
    "{{CLOSING_MESSAGE}}": "A wet Tuesday in Carrum Downs — showers all day, so keep the gear covered and the van stocked. The big moment this afternoon is the RBA rate decision at 2:30pm: if they hike to 4.35%, start thinking about what that means for any variable-rate finance you're carrying. Wednesday and Thursday look heavier still — up to 20mm — so plan your outdoor jobs around the forecast. Good luck out there, Liall.",
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
