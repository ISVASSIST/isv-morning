#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 19 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 19 May (BOM forecast)
    "{{WEATHER_1}}": "TUE 19 · 🌧 Showers · 15°C",
    "{{WEATHER_2}}": "WED 20 · 🌧 Showers · 14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 21 · ⛅ Clearing · 15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 22 · ⛅ Partly cloudy · 16°C",
    "{{WEATHER_5}}": "SAT 23 · ☁ Mostly cloudy · 17°C",
    "{{WEATHER_ALERT}}": "☔ SHOWERS TUE–WED",

    # World
    "{{WORLD_1_FLAG}}": "🇦🇪 GULF",
    "{{WORLD_1_HEADLINE}}": "Drone Strikes the UAE's Only Nuclear Power Plant — Fire at Barakah Perimeter, No Radiation Release",
    "{{WORLD_1_SUMMARY}}": "A drone attack on Sunday ignited a fire at an electrical generator outside the inner perimeter of the Barakah Nuclear Energy Plant in Abu Dhabi — the Arab world's first commercial nuclear station. Three drones entered from the western border; two were shot down by air defences, while one broke through to start the blaze. No injuries were reported and all four reactor units continued operating normally with no radiological impact. IAEA chief Rafael Grossi expressed \"grave concern,\" warning that military activity near nuclear facilities is \"unacceptable.\" No group has claimed responsibility, and the UAE has launched a formal investigation.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/5/17/drone-strike-sparks-fire-at-uaes-barakah-nuclear-power-plant",

    "{{WORLD_2_FLAG}}": "🌍 MIDDLE EAST",
    "{{WORLD_2_HEADLINE}}": "Iran Submits Fresh Nuclear Deal Terms to US — Oil Markets Volatile as Diplomacy Staggers On",
    "{{WORLD_2_SUMMARY}}": "Iran has shared a revised set of conditions with the United States for a potential nuclear settlement, even as both governments signal readiness to resume military confrontation if talks collapse. President Trump warned \"the clock is ticking\" while Tehran said it was seeking \"balanced and fair\" terms. Crude oil markets have been swinging sharply on every diplomatic signal from the region. For Australian trades businesses, this is directly relevant — Middle East instability is one of the key variables keeping domestic fuel prices elevated and hard to predict heading into June.",
    "{{WORLD_2_URL}}": "https://www.cbsnews.com/live-updates/iran-war-trump-warning-oil-stock-prices-futures-ceasefire-diplomacy/",

    # Economics
    "{{ECON_1_FLAG}}": "🏛 FEDERAL BUDGET",
    "{{ECON_1_HEADLINE}}": "350,000 Small Businesses Face Restructure Under New 30% Trust Tax — Accountants Already Fielding Calls",
    "{{ECON_1_SUMMARY}}": "The federal budget's biggest structural hit to small business is a new 30% minimum tax on income distributed through discretionary trusts — a structure used by an estimated 350,000 Australian SMEs. Effective July 2028, the reform will force many family business owners to restructure or absorb a higher tax burden. Leading accounting firms warn that the real cost is \"time and resources diverted from growing the business to restructuring the business.\" Rollover relief is available from July 2027. If your business operates through a discretionary trust, your accountant needs to hear from you this week — not next year.",
    "{{ECON_1_URL}}": "https://www.smartcompany.com.au/federal-budget-2026/blunt-force-disruption-small-businesses-through-30-trust-tax/",

    "{{ECON_2_FLAG}}": "⛽ RATES & FUEL",
    "{{ECON_2_HEADLINE}}": "RBA Holds at 4.35% After Third Hike This Year — and the Fuel Excise Cut Expires June 30",
    "{{ECON_2_SUMMARY}}": "The RBA cash rate sits at 4.35% following May's third consecutive hike this year — its highest level since 2011. The board has signalled a potential pause, but with fuel-driven inflation still in the system, near-term relief is far from certain. On top of that, the government's 32¢/litre fuel excise reduction expires on June 30. For fleet-heavy trades businesses, the July price reset is a real recalculation. Any quotes written this week that factor in current diesel rates could become losses on jobs invoiced in August.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🏦 AI IN BUSINESS",
    "{{TECH_1_HEADLINE}}": "JPMorgan Formally Reclassifies AI as Core Infrastructure — Targeting $2.5 Billion in Annual Value",
    "{{TECH_1_SUMMARY}}": "JPMorgan Chase has moved AI from \"experimental R&D\" to \"core operational infrastructure\" — the most explicit declaration yet from a global financial institution that AI is no longer a pilot but a structural business requirement. The bank is deploying AI agents across three areas: internal productivity, cybersecurity defence, and personalised retail banking, with AI projected to generate $2.5 billion in annual value. For small business owners, this is the clearest signal yet that AI competency is transitioning from a competitive edge into a baseline expectation across every industry — and the window to be an early adopter is closing.",
    "{{TECH_1_URL}}": "https://www.crescendo.ai/news/latest-ai-news-and-updates",

    "{{TECH_2_FLAG}}": "⚡ AI MODELS",
    "{{TECH_2_HEADLINE}}": "Google's Fastest AI Model Yet Launches at $0.25 per Million Tokens — The Cost of AI Is Hitting the Floor",
    "{{TECH_2_SUMMARY}}": "Google has released its Gemini Flash-Lite model, delivering 2.5× faster response times and 45% quicker output generation than earlier Gemini versions — priced at just $0.25 per million input tokens, making it one of the cheapest capable AI models available to builders and businesses. For trades businesses considering AI-powered quoting tools, client chatbots, or automated admin, the cost barrier has never been lower. The trajectory is clear: AI is getting faster, cheaper, and more capable every quarter — which means the question is no longer whether to adopt, but when.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳 CHINA",
    "{{ROBOT_1_HEADLINE}}": "China Deploys Humanoid Robots at Vietnam Border in $37M Contract — Crowd Control, Patrol, and Passenger Guidance",
    "{{ROBOT_1_SUMMARY}}": "UBTECH Robotics has secured a $37 million contract to deploy its Walker S2 humanoid robots at the Fangchenggang border crossing in Guangxi, China — one of the largest real-world government humanoid deployments announced to date. The adult-sized robots will guide passenger queues, direct vehicles, answer traveller questions, and patrol corridors monitoring crowd patterns. UBTECH is targeting 5,000 units built by end of 2026 and 10,000 by 2027, with further deployments planned across automotive plants, logistics hubs, and smart factories. It is among the clearest signals yet that humanoid robots are moving from industrial pilots into government and public-facing operations at scale.",
    "{{ROBOT_1_URL}}": "https://interestingengineering.com/innovation/ubtech-secures-us37-million-deal",

    # Australia
    "{{AUS_1_HEADLINE}}": "Chalmers Fires Back at 'Death Tax' Attack — Budget Trust Tax Political Fight Heats Up",
    "{{AUS_1_SUMMARY}}": "Treasurer Jim Chalmers pushed back against what he called an \"unhinged scare campaign\" over the government's new 30% discretionary trust tax, as Opposition Treasury spokesperson Taylor labelled the measure a \"death tax by stealth.\" With roughly 350,000 SMEs operating through discretionary trusts, both sides are targeting small business owners in key electorates. Accounting firms and peak bodies are urging businesses not to make hasty restructuring decisions until the full legislation is released, with the 2028 effective date providing time to plan carefully.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/federal-budget-2026-five-minute-guide/2g0jf7tvz",

    "{{AUS_2_HEADLINE}}": "Two Sydney Teen Girls Charged After Assaulting Bus Driver, Passenger and American Tourists in CBD",
    "{{AUS_2_SUMMARY}}": "Two girls aged 16 and 17 were arrested and charged after allegedly assaulting a bus driver and a passenger on George Street in Sydney's CBD on Sunday morning, before turning on two American tourists on the street. None of the four victims required hospitalisation. A 19-year-old man also at the scene was issued a move-on direction. The incident has renewed calls for improved transport safety measures and greater law enforcement presence in the CBD.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Locks In First Budget Surplus in Seven Years — $1B+ Road Works and $22.8M for Apprentices in 2026-27",
    "{{VIC_1_SUMMARY}}": "The 2026-27 Victorian State Budget confirmed the state's first operating surplus in seven years at $700 million, alongside more than $1 billion in committed road works for the coming 12 months and $22.8 million over two years to support apprentices and trainees in construction, clean energy, and advanced manufacturing. For trades businesses in Melbourne's south-east, the road works pipeline is a tangible forward work opportunity. For those considering taking on an apprentice, expanded state and federal support now align — making 2026 the strongest incentive environment for apprentice hiring in years.",

    # Science
    "{{SCI_1_FLAG}}": "🦠 HEALTH SCIENCE",
    "{{SCI_1_HEADLINE}}": "Kimchi Microbe Found to Bind and Flush Nanoplastics From the Gut — South Korean Government Lab Study",
    "{{SCI_1_SUMMARY}}": "Scientists at South Korea's World Institute of Kimchi have discovered that a probiotic bacterium naturally occurring in kimchi clings tightly to nanoplastic particles under conditions designed to mimic the human intestine — binding and helping to excrete them before they accumulate in organs. In lab tests, the kimchi-derived strain retained a nanoplastic binding rate of 57% under intestinal conditions, compared to just 3% for a standard reference strain. The findings were published in Bioresource Technology and covered by ScienceDaily on May 17 — and the key ingredient is already in a lot of people's fridges.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How Responding to Your Google Reviews with AI Can Be One of the Best 10 Minutes You Spend This Week",
    "{{INSIGHT_BODY}}": "For a small trades business, trust is often built before anyone picks up the phone — and in 2026, that means your Google Business profile matters more than you might think. When a satisfied client leaves a five-star review and you respond promptly with a professional, personalised reply, the next person reading it sees an engaged, accountable business owner. When a critical or unfair review sits unanswered, it can look like indifference. AI can draft a professional response to any review — positive or negative — in seconds. Build a simple prompt with your business name, your preferred tone, and how you want to handle complaints, and you can clear a week of reviews in under 10 minutes. Most small trades businesses have no review-response strategy at all. That gap is worth closing today, because word of mouth has moved online — and your reply is now part of your pitch.",

    # Fun Facts
    "{{FACT_1}}": "The world's oldest known living tree is a Great Basin Bristlecone Pine nicknamed \"Methuselah,\" growing in the White Mountains of California. It is approximately 4,855 years old — already ancient when the Egyptian pyramids were under construction. Its exact location has never been publicly disclosed, to protect it from vandalism.",

    "{{FACT_2}}": "Autumn is technically the optimal season for exterior painting and protective coatings. Moderate temperatures between 15°C and 25°C combined with lower humidity create ideal evaporation conditions for both water-based and solvent-based coatings. In high-humidity summer conditions, latex paint can take up to three times longer to cure fully — and applied below 10°C, oil-based coatings risk failing to bond to the substrate at all.",

    "{{FACT_3}}": "The humble shipping container was invented by American truck driver Malcolm McLean in 1956. His standardised steel box reduced the cost of loading cargo from $5.86 per tonne to just 16 cents — a 97% reduction — and effectively created the modern global trade system. Today, roughly 90% of all internationally traded goods travel inside a shipping container at some stage of their journey.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the painter's quote always come in right on budget?",
    "{{JOKE_PUNCHLINE}}": "He only ever quoted one coat.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Luck is what happens when preparation meets opportunity.\"",
    "{{CLOSING_ATTR}}": "— Seneca",
    "{{CLOSING_MESSAGE}}": "It's a wet Tuesday in Carrum Downs, with showers sticking around through Wednesday before things start to clear toward the weekend. Overnight, a drone struck the perimeter of the UAE's only nuclear power plant — no radiation release, but a reminder of how quickly Middle East instability flows through to oil markets and your fuel costs. Closer to home, the political fight over the budget's trust tax is heating up fast — if your business runs through a discretionary trust, this week is worth a conversation with your accountant before the restructuring decisions get made for you. Stay warm, stay dry, and use the slower morning well, Liall.",
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
