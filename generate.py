#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 14 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Thu 14 May
    "{{WEATHER_1}}": "Thu 14 May · Polar Blast Clearing · 14°C",
    "{{WEATHER_2}}": "Fri 15 May · Partly Cloudy · 16°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Sat 16 May · Cool & Dry · 16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Sun 17 May · Mild · 17°C",
    "{{WEATHER_5}}": "Mon 18 May · Mild · 17°C",
    "{{WEATHER_ALERT}}": "❄️ POLAR BLAST — COLD START",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸🇨🇳 US–CHINA SUMMIT",
    "{{WORLD_1_HEADLINE}}": "Trump and Xi Begin High-Stakes Talks in Beijing — Trade, AI Safety, Iran War and Taiwan on the Agenda",
    "{{WORLD_1_SUMMARY}}": "US President Donald Trump arrived in Beijing Wednesday evening for a landmark state visit — the first US presidential trip to China in nearly a decade. Talks begin Thursday with Xi Jinping covering Nvidia chip exports, AI safety dialogue, Taiwan security, Iran war fallout, and rare earth access. Trump was accompanied by Elon Musk, Apple's Tim Cook, and Nvidia's Jensen Huang, signalling the summit's heavy commercial dimension alongside its geopolitical stakes.",
    "{{WORLD_1_URL}}": "https://www.cnbc.com/2026/05/13/trump-china-xi-beijing-meeting-ceos.html",

    "{{WORLD_2_FLAG}}": "🦠 GLOBAL HEALTH",
    "{{WORLD_2_HEADLINE}}": "Hantavirus Cruise Ship Outbreak Grows to 11 Cases and Three Deaths — WHO Monitoring Multi-Country Spread",
    "{{WORLD_2_SUMMARY}}": "The Andes strain of hantavirus linked to the Dutch cruise ship MV Hondius has now infected 11 people across multiple countries, with three confirmed deaths. The vessel was travelling between Argentina and the Canary Islands when the rodent-borne virus spread, potentially through rare human-to-human transmission. All passengers have been flown home on government and military aircraft; the WHO assesses global risk as low but is actively monitoring.",
    "{{WORLD_2_URL}}": "https://www.cidrap.umn.edu/misc-emerging-topics/hantavirus-outbreak-grows-11-cases-9-confirmed",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL COSTS",
    "{{ECON_1_HEADLINE}}": "Diesel Still Near $2.80/Litre as Fuel Excise Cut Ticks Down to June 30 — No Extension Confirmed",
    "{{ECON_1_SUMMARY}}": "Despite easing from April's crisis peak, diesel remains near $2.70–$3.00 per litre nationally and the government's 26-cent-per-litre excise cut expires June 30 with no extension confirmed. Around 120 service stations are still reporting diesel outages — a fraction of the April peak but still disruptive for fleet-dependent trades operators. A new government fuel reserve program capable of holding up to 1 billion litres is underway but won't deliver relief until 2027.",
    "{{ECON_1_URL}}": "https://www.ibtimes.com.au/australia-fuel-crisis-deepens-may-2026-middle-east-war-disrupts-supplies-budget-relief-kicks-1868716",

    "{{ECON_2_FLAG}}": "🏗️ BUDGET 2026",
    "{{ECON_2_HEADLINE}}": "$20,000 Instant Asset Write-Off Made Permanent — Small Business Gets Certainty as Budget Locks In the Threshold",
    "{{ECON_2_SUMMARY}}": "The 2026-27 Federal Budget, handed down Tuesday night, makes the $20,000 instant asset write-off a permanent fixture for businesses with annual turnover under $10 million. Previously renewed year-to-year and subject to political uncertainty, the threshold is now a settled planning tool. Eligible equipment, tools, vehicles, and technology can be fully deducted in the year of purchase — a clear incentive to invest ahead of the new financial year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📊 STANFORD AI INDEX",
    "{{TECH_1_HEADLINE}}": "Stanford 2026 AI Index: Generative AI Hit 53% Global Adoption in Three Years — Faster Than PC or Internet",
    "{{TECH_1_SUMMARY}}": "Stanford University's Human-Centred AI Institute released its 2026 AI Index report Wednesday, tracking the fastest technology adoption in recorded history. Generative AI reached 53% of the global working-age population within three years of mass release — surpassing the adoption rates of the PC, the internet, and the smartphone. The estimated annual consumer value of free AI tools reached $172 billion in the US alone, with the median value per user tripling between 2025 and 2026.",
    "{{TECH_1_URL}}": "https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report",

    "{{TECH_2_FLAG}}": "💼 TECH EMPLOYMENT",
    "{{TECH_2_HEADLINE}}": "AI Is Eliminating Entire Job Functions at Major Firms — Restructuring Wave Accelerates as Adoption Surges",
    "{{TECH_2_SUMMARY}}": "A wave of corporate restructuring linked directly to AI is gathering pace, with firms cutting entire departments while reporting record revenues. Cloudflare this month cut 1,100 staff — 20% of its workforce — citing a 600% surge in internal AI usage in three months while revenue hit an all-time high. Analysts caution that small businesses supplying services to white-collar sectors may face contracting demand as AI absorbs administrative, finance, HR, and marketing workloads at enterprise scale.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇬🇧🇩🇪 UK / GERMANY",
    "{{ROBOT_1_HEADLINE}}": "UK Startup Humanoid Lands Landmark Deal to Deploy 2,000 Robots in Schaeffler's Global Factories by 2032",
    "{{ROBOT_1_SUMMARY}}": "Humanoid, a UK AI and robotics company founded in 2024, has signed a binding Robot-as-a-Service agreement with German precision engineering giant Schaeffler to deploy between 1,000 and 2,000 wheeled humanoid robots across global manufacturing sites. The first units go live at two German facilities in December 2026. Schaeffler simultaneously becomes Humanoid's preferred actuator supplier — one of the largest disclosed humanoid deployment agreements ever announced.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/05/13/humanoid-secures-landmark-deal-with-schaeffler-to-deploy-thousands-of-humanoid-robots/26562/",

    # Australia
    "{{AUS_1_HEADLINE}}": "PM Defends Budget Tax Overhaul as Coalition Cries Foul — Negative Gearing and CGT Changes Dominate Debate",
    "{{AUS_1_SUMMARY}}": "Treasurer Jim Chalmers' 2026-27 Federal Budget limits negative gearing to new builds from July 2027 and replaces the 50% CGT discount with cost-base indexation. The PM is defending the changes as long-overdue rebalancing of property investment incentives; the Coalition has accused the government of breaking election promises. Independent MPs are calling for revenue from the reforms to flow back to Australians as income tax relief.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/federal-budget-2026-five-minute-guide/2g0jf7tvz",

    "{{AUS_2_HEADLINE}}": "Australia to Ban Betting Ads During Live Sports Broadcasts from January 2027",
    "{{AUS_2_SUMMARY}}": "The Albanese government has tabled its response to the landmark Murphy gambling inquiry, proposing a national ban on wagering advertisements during live sports broadcasts on free-to-air TV between 6am and 8:30pm. Restrictions also extend to social media platforms, sporting venues, and player uniforms. Legislation will be developed throughout 2026, with the full reforms taking effect from January 1, 2027.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Wakes to Coldest Morning of 2026 — Polar Blast Clears as Alpine Resorts Celebrate Early Snowfalls",
    "{{VIC_1_SUMMARY}}": "Melbourne recorded its coldest temperature of the year as a powerful polar blast sent temperatures 4–8°C below the May average across Victoria this week. Snowfalls of up to 20 centimetres were reported at Mount Buller and Falls Creek, with ski resorts kicking off the season early. The blast is clearing Thursday morning, with milder conditions returning gradually through the weekend.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ QUANTUM PHYSICS — JAPAN",
    "{{SCI_1_HEADLINE}}": "Japanese Scientists Crack Major Quantum Bottleneck — Instant Detection of 'W States' Advances Quantum Internet",
    "{{SCI_1_SUMMARY}}": "Researchers in Japan have solved a critical obstacle in quantum networking by developing a photonic circuit that can instantly detect 'W states' — exotic multi-particle entangled configurations essential for quantum teleportation and distributed computing. Previous methods required exponentially many measurements as photon count increased, making them impractical at scale. The team demonstrated a stable three-photon device operating without active control, a key requirement for real-world quantum network deployment. Published 13 May 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The Trades Business That Doesn't Have an AI Strategy by 2027 Will Be Competing on Price Alone",
    "{{INSIGHT_BODY}}": "Stanford's 2026 AI Index — released this week — confirms that generative AI has reached 53% of the global population in just three years: the fastest technology adoption in recorded history. For a small trades business like ISV, this isn't just a tech headline. It means your customers, competitors, and subcontractors are all becoming AI-literate simultaneously, and the ones building AI into their operations now will have a structural cost and service advantage by 2027 that will be very hard to close on price. AI-assisted quoting, scheduling, client communication, and compliance documentation can let a three-person operation work like a six-person one — without the payroll. The businesses that figure this out in 2026 won't need to cut their rates next year. The ones that wait will have no choice.",

    # Fun Facts
    "{{FACT_1}}": "Every giant panda at every zoo in the world is technically owned by China — all animals are on loan under agreements costing around USD $1 million per pair per year, and cubs born outside China are also Chinese property that must eventually be returned. Fewer than 1,900 giant pandas are known to exist worldwide.",
    "{{FACT_2}}": "When glass fractures, the crack propagates at speeds of up to 5,500 kilometres per hour — roughly 1.5 kilometres per second. The shattering sound you hear isn't the glass breaking but air rushing into the crack. In a vacuum, glass would shatter in complete silence.",
    "{{FACT_3}}": "The United States has more public libraries than McDonald's restaurants — around 17,000 public library branches compared to approximately 13,700 US McDonald's outlets. Total annual library visits in the US exceed attendance at all major professional sport events combined.",

    # Joke
    "{{JOKE_SETUP}}": "How many estimators does it take to change a lightbulb?",
    "{{JOKE_PUNCHLINE}}": "One. But you won't know the final cost until after it's done.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The only limit to our realization of tomorrow will be our doubts of today.\"",
    "{{CLOSING_ATTR}}": "Franklin D. Roosevelt",
    "{{CLOSING_MESSAGE}}": "Thursday in Carrum Downs — the polar blast is clearing and you're heading into the back half of the working week. The federal budget landed Tuesday night and there's plenty to absorb: the $20K write-off is now permanent, the fuel excise cut runs to June 30, and negative gearing reforms kick in from 2027. Across in Beijing today, Trump and Xi are sitting down for talks that could reshape technology access and trade flows for years. Cold start this morning, but the weekend is looking mild. Get the day moving.",
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
