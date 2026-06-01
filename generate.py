#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 02 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 2 Jun (BOM forecast)
    "{{WEATHER_1}}": "TUE 2 · ⛅ Part cloud, fog · 8–14°C",
    "{{WEATHER_2}}": "WED 3 · ☁ Cloudy · 9–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "THU 4 · 🌧 Showers likely · 9–13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 5 · 🌧 Showers · 9–14°C",
    "{{WEATHER_5}}": "SAT 6 · ⛅ Part cloud · 10–15°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS FROM THURSDAY",

    # World
    "{{WORLD_1_FLAG}}": "🌏 MIDDLE EAST · BREAKING",
    "{{WORLD_1_HEADLINE}}": "US Strikes Iranian Military Sites After American Drone Shot Down — Kuwait Hit by Missile Fire",
    "{{WORLD_1_SUMMARY}}": "US Central Command struck radar and drone control sites in Iran over the weekend after Tehran shot down an American MQ-1 Predator drone. Iran retaliated with its own strikes, with Kuwait reporting incoming drone and missile fire. Both countries continue ceasefire negotiations amid escalating regional tensions — with direct implications for global oil supply and fuel prices.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/06/01/g-s1-125126/us-iran-war-updates",

    "{{WORLD_2_FLAG}}": "🌎 LATIN AMERICA · POLITICS",
    "{{WORLD_2_HEADLINE}}": "Right-Wing Outsider Wins Colombia's First-Round Presidential Vote — June 21 Runoff Set Against Leftist Cepeda",
    "{{WORLD_2_SUMMARY}}": "Abelardo de la Espriella, a tough-on-crime right-wing candidate aligned with Trump, scored a surprise first-round win in Colombia's presidential election with 43.7% of the vote — defying all opinion polls. He will face leftist senator Iván Cepeda in a June 21 runoff that will define the country's political direction and its relationship with the United States.",
    "{{WORLD_2_URL}}": "https://www.pbs.org/newshour/world/polls-close-in-colombia-vote-with-espriella-and-cepeda-advancing-to-runoff",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 FUEL · EXCISE",
    "{{ECON_1_HEADLINE}}": "Australia's Half-Price Fuel Excise Relief Expires June 30 — Diesel Prices Set to Jump 29 Cents Per Litre",
    "{{ECON_1_SUMMARY}}": "Since April 1, federal fuel excise has been halved from 52.6¢ to 26.3¢ per litre, cutting diesel by 31% and petrol by 29% in major cities. That relief expires in four weeks on June 30, with full rates snapping back overnight — adding around 29 cents per litre once GST applies. Trades operators with vehicle-heavy operations should factor the July cost jump into any work quoted now for delivery after June 30.",
    "{{ECON_1_URL}}": "https://www.smartcompany.com.au/economy/australia-fuel-crisis-essential-updates-businesses/",

    "{{ECON_2_FLAG}}": "🏦 INTEREST RATES · RBA",
    "{{ECON_2_HEADLINE}}": "Economists Split on June 16 RBA Decision — NAB Tips Another Hike as Cash Rate Sits at 4.35%",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank of Australia meets in 14 days with economists divided on whether the cash rate rises again from 4.35%. NAB has flagged a June hike is likely; CBA, ANZ, and most others expect a hold. The RBA's May statement flagged inflation has 'picked up materially' driven by fuel and supply chain costs. Small businesses carrying variable-rate finance or equipment loans should model a further 25 basis point increase in their forward costs while the decision plays out.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · GOOGLE",
    "{{TECH_1_HEADLINE}}": "Google Gemini 3.5 Flash Now Live as Default AI in Search and Gemini App — Built for Agents, Not Chatbots",
    "{{TECH_1_SUMMARY}}": "Google's Gemini 3.5 Flash is now generally available and set as the default AI in both the Gemini app and AI Mode in Google Search globally. Designed from the ground up for agentic workflows — multi-step tasks, tool use, and autonomous operation rather than simple Q&A — it delivers frontier-level reasoning at significantly faster inference speeds. From June 8, it will be enabled by default in Gemini Enterprise and cannot be turned off.",
    "{{TECH_1_URL}}": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/",

    "{{TECH_2_FLAG}}": "💰 AI · INDUSTRY",
    "{{TECH_2_HEADLINE}}": "OpenAI Surpasses $25 Billion in Annualised Revenue as IPO Preparations Begin for Late 2026",
    "{{TECH_2_SUMMARY}}": "OpenAI has crossed $25 billion in annualised revenue and is taking early steps toward a public listing, potentially by late 2026. Rival Anthropic is approaching $19 billion. The rapid commercial growth of the leading AI labs confirms that enterprise AI adoption has crossed the inflection point from experiment to standard business infrastructure — and the monetisation gap between early and late adopters is now measured in billions.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "⚙️ PHYSICAL AI · NVIDIA",
    "{{ROBOT_1_HEADLINE}}": "NVIDIA Launches Cosmos 3 — Open Physical AI World Model Built to Power Robots and Autonomous Machines",
    "{{ROBOT_1_SUMMARY}}": "NVIDIA released Cosmos 3 on June 1, an open-source physical AI foundation model combining visual reasoning, world generation, and action prediction in a single architecture. Trained on 20 trillion tokens of real and synthetic robot, video, and sensor data, it is designed to be the reasoning engine for physical robots across factory floors, warehouses, and autonomous vehicles. Two versions: Cosmos 3 Nano (16B parameters) for real-time robot inference on workstation hardware, and Cosmos 3 Super (64B) for datacenter-scale deployment.",
    "{{ROBOT_1_URL}}": "https://www.globenewswire.com/news-release/2026/06/01/3303987/0/en/NVIDIA-Launches-Cosmos-3-the-Open-Frontier-Foundation-Model-for-Physical-AI.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "AUKUS Revised: Australia to Buy Three Second-Hand US Nuclear Submarines in Simplified Stopgap Deal",
    "{{AUS_1_SUMMARY}}": "Defence Minister Richard Marles confirmed at Singapore's Shangri-La Dialogue that Australia will now acquire all three Virginia-class nuclear submarines second-hand from the US Navy — replacing the original plan for a mix of new and used vessels. Defence cited the premium on simplicity in an 'incredibly complicated' endeavour. Australia's commitment to build five SSN-AUKUS submarines domestically from the late 2030s remains unchanged.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/drones-and-second-hand-submarines-latest-aukus-details-unveiled/zolbu9p5g",

    "{{AUS_2_HEADLINE}}": "Socceroos Fall 1–0 to Mexico in Pre-World Cup Friendly as Tournament Preparation Continues",
    "{{AUS_2_SUMMARY}}": "Australia's national men's football team suffered a 1–0 defeat to Mexico in a pre-World Cup friendly, providing a tough but useful test ahead of the tournament. The result against a strong North American side gives coaching staff key data as the Socceroos finalise their preparation and squad selection.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne's Draft 2026–27 City Budget Doubles Safety Officers and Expands Mental Health Homelessness Services",
    "{{VIC_1_SUMMARY}}": "The City of Melbourne's draft 2026–27 budget proposes doubling Community Safety Officers from 11 to 22, expanding homelessness services to include dedicated complex mental health support for the first time, and planting 3,000 new trees across the city. The plan reflects council's continued focus on safety and liveability as Melbourne's CBD continues its post-pandemic recovery and densification.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 MEDICINE · ONCOLOGY",
    "{{SCI_1_HEADLINE}}": "Experimental Drug Daraxonrasib Nearly Doubles Survival in Advanced Pancreatic Cancer — Results Published in NEJM",
    "{{SCI_1_SUMMARY}}": "Presented at the American Society of Clinical Oncology annual meeting and published simultaneously in the New England Journal of Medicine, daraxonrasib delivered median overall survival of 13.2 months versus 6.7 months on standard chemotherapy for patients with metastatic pancreatic cancer. The drug blocks the KRAS mutation driving tumour growth in over 90% of cases — a target that had resisted drugs for decades. Pancreatic cancer kills around 90% of patients within five years; these results are the first meaningful step forward in survival outcomes in a generation.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "New Month, New Habits: Five AI Prompts Every Trades Business Should Run at the Start of June",
    "{{INSIGHT_BODY}}": "A new month is your best natural reset point. Most small trades operators know they should review their numbers, check the pipeline, and plan ahead — but it rarely happens because there's no system. AI changes that. Take 10 minutes at the start of each month and prompt your AI assistant to: review your previous month's job log for patterns in margin and delays; draft a short cash flow projection based on your outstanding quotes; flag any recurring supplier invoices that have risen since last quarter; update your rate card with any cost increases since your last review; and draft a short follow-up message to any quotes older than three weeks. Each task takes under two minutes. Together, they deliver the discipline a bookkeeper, estimator, and business coach would charge thousands per month to provide — sitting quietly on your phone, ready when you need it. The financial year ends in 29 days. Start June right.",

    # Fun Facts
    "{{FACT_1}}": "The loudest sound in recorded history was the 1883 eruption of Krakatoa, which was heard clearly 4,800 kilometres away on Rodrigues Island near Mauritius. The pressure wave circled Earth four complete times and was recorded on barometers around the world for five consecutive days.",

    "{{FACT_2}}": "Switzerland is legally required to maintain emergency food stockpiles sufficient for its entire population — covering months of essential goods including coffee, sugar, edible oils, rice, and medicines. The strategic reserves are managed under the Federal Act on National Economic Supply and rotated continuously by law.",

    "{{FACT_3}}": "Hot-dip galvanising — plunging structural steel into molten zinc at around 450°C — was patented by Frenchman Stanislas Sorel in 1836. A correctly applied galvanising coat provides 50 to 100 years of corrosion protection with zero ongoing maintenance in most Australian environments, outperforming paint and other protective coatings by decades.",

    # Joke
    "{{JOKE_SETUP}}": "Why do arborists make the best managers?",
    "{{JOKE_PUNCHLINE}}": "Because they're brilliant at spotting deadwood — and cutting it before it brings the whole operation down.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less.”",
    "{{CLOSING_ATTR}}": "— Marie Curie",
    "{{CLOSING_MESSAGE}}": "First Tuesday of June, Liall — 29 days left in the financial year, and a wet week building from Thursday. Fuel excise relief is counting down to June 30 and the RBA decides in 14 days. A good morning to prompt the AI, tighten the rate card, and make sure any jobs quoted today account for what lands on July 1. Stay dry out there.",
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
