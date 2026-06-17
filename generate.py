#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 18 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 18 Jun
    # BOM forecast: Thu–Fri heavy showers & N'ly 25-40 km/h; Sat 80% shower risk easing; Sun winter solstice clearing; Mon mostly cloudy
    "{{WEATHER_1}}": "THU 18 · 🌧 Showers · 19°C",
    "{{WEATHER_2}}": "FRI 19 · 🌧 Showers · 16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 20 · 🌦 Shower risk · 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 21 · ⛅ Clearing · 15°C",
    "{{WEATHER_5}}": "MON 22 · 🌥 Mostly cloudy · 15°C",
    "{{WEATHER_ALERT}}": "⚠ HEAVY SHOWERS & N'LY WINDS THU–FRI · EASING THROUGH WEEKEND",

    # World
    "{{WORLD_1_FLAG}}": "🌐 US · Iran · Zurich",
    "{{WORLD_1_HEADLINE}}": "US-Iran 60-Day Ceasefire Heads to Switzerland for Formal Signing — Strait of Hormuz to Reopen to All Traffic From Tomorrow",
    "{{WORLD_1_SUMMARY}}": "The US-Iran ceasefire deal — including the full reopening of the Strait of Hormuz — is set for a formal signing ceremony in Zurich on Friday, with Pakistan's Prime Minister Shehbaz Sharif confirming his attendance as key mediator. The 60-day memorandum of understanding lifts both Iran's and the US Navy's duelling naval blockades that have restricted approximately 20% of the world's traded oil for months. Global markets reacted immediately: S&P 500 up 1.9%, oil prices fell nearly 5%. For Australian trades businesses, cheaper global crude typically takes two to four weeks to reach the pump — but with Australia's own fuel excise cut also ending June 30, the net effect on July fuel costs is still uncertain. A formal peace agreement following the 60-day window could reshape the global energy price environment for 2026–27.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/06/15/nx-s1-5858590/us-iran-deal-updates",

    "{{WORLD_2_FLAG}}": "🌐 Ukraine · Kharkiv",
    "{{WORLD_2_HEADLINE}}": "Russian Drone and Missile Strikes Kill Three in Kharkiv as Front-Line Fighting Intensifies",
    "{{WORLD_2_SUMMARY}}": "Russian drone and missile strikes on Kharkiv Oblast killed three people and wounded 18 in overnight attacks on June 16–17, with residential areas and the Kyiv district of Kharkiv city directly hit. Ukrainian forces reported more than 237 combat engagements along the front line in the past 24 hours with no significant Russian territorial advances recorded. European defence ministers agreed to accelerate long-range weapons deliveries following the strikes. Ukrainian officials have warned that this week's global focus on the US-Iran signing in Zurich is creating a dangerous distraction from Russia's continued aerial campaign against civilian infrastructure.",
    "{{WORLD_2_URL}}": "https://kyivindependent.com/russian-drone-missile-attack-kills-3-injures-18-in-kharkiv-oblast/",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ Fuel Excise · June 30",
    "{{ECON_1_HEADLINE}}": "Australia's Halved Fuel Excise Ends in 12 Days — Petrol Prices Set to Jump Up to 28.9c/L From 1 July",
    "{{ECON_1_SUMMARY}}": "The temporary halving of Australia's fuel excise — saving motorists 26.3 cents per litre since April — expires at 11:59pm on June 30. From July 1 the excise reverts to the full indexed rate, adding approximately 28.9c/L at the pump after GST. For a trades business running two work vehicles at 200km per day each, the monthly fuel bill increase could reach $300 to $500. However, the US-Iran ceasefire deal has driven global crude prices down nearly 5% this week, which analysts expect will partially offset the excise reversal — the likely net July pump price increase may be closer to 10–15c/L if oil markets hold. Do not rely on that outcome: update vehicle running costs and job pricing before June 30.",
    "{{ECON_1_URL}}": "https://fueldaddy.com.au/blog/fuel-excise-cut-2026/",

    "{{ECON_2_FLAG}}": "📈 ASX · June 2026",
    "{{ECON_2_HEADLINE}}": "ASX Hits Nine-Week High as Oil Prices Tumble on Iran Deal — AUD Strengthens",
    "{{ECON_2_SUMMARY}}": "The ASX 200 reached a nine-week high this week as Australian shares broadly rallied on falling global oil prices triggered by the US-Iran ceasefire agreement. The Australian dollar also strengthened as commodity markets adjusted to the prospect of the Strait of Hormuz reopening on Friday. For small businesses, falling oil prices ripple through the supply chain: cheaper fuel for logistics, lower feedstock costs for suppliers, and reduced import price pressure. The key risk is that lower oil prices could drag iron ore and resource-linked stocks, but in the near term the oil price drop is broadly positive for a trades business's July cost base.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 Meta · AI Infrastructure",
    "{{TECH_1_HEADLINE}}": "Meta Signs $27 Billion AI Compute Deal With Nebius — One of the Largest AI Infrastructure Commitments in History",
    "{{TECH_1_SUMMARY}}": "Meta has entered a five-year, $27 billion agreement with AI infrastructure provider Nebius to secure critical compute capacity, including $12 billion in dedicated infrastructure featuring one of the first large-scale deployments of Nvidia's next-generation Vera Rubin chip platform. The deal is one of the largest single AI infrastructure commitments ever announced. For trades and small business operators using AI tools: the ferocious competition between Meta, Google, and OpenAI to acquire compute is what is currently keeping AI subscription prices low. That competitive dynamic will not last indefinitely — the time to build AI habits into your business is now, while the tools are fast, cheap, and getting more capable every month.",
    "{{TECH_1_URL}}": "https://techcrunch.com/category/artificial-intelligence/",

    "{{TECH_2_FLAG}}": "🇺🇸 White House · AI Policy",
    "{{TECH_2_HEADLINE}}": "White House Issues Executive Order on AI Innovation — Removes Biden Safety Testing Mandates, Accelerates Federal AI Deployment",
    "{{TECH_2_SUMMARY}}": "The White House published an executive order titled 'Promoting Advanced Artificial Intelligence Innovation and Security,' formally removing several Biden-era AI safety testing mandates while establishing new federal frameworks for AI development and government procurement. The order signals a clear innovation-first posture, accelerating AI deployment across US defence, federal agencies, and commercial applications. For Australian businesses that use or trade with US-developed AI products and services, the practical effect is faster rollout of AI-enabled tools. Australia's own AI policy framework tends to follow US and G7 settings within 12–18 months.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 Semiconductors · Physical AI",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robots Set to Enter Chip Fabrication Plants for the First Time — Industry's Most Demanding Environment",
    "{{ROBOT_1_SUMMARY}}": "Semiconductor manufacturers are preparing to deploy humanoid robots inside chip fabrication facilities — among the most precision-demanding and contamination-sensitive industrial environments on Earth. Chip fabs require nanometre-level accuracy, clean-room conditions, and 24/7 continuous operation. Until now, the complexity and delicacy of the environment had placed fabs beyond the reach of autonomous robots. If successful, this will be the first time humanoid robots have operated inside active semiconductor fabrication plants — validating robot dexterity in what many engineers considered the last truly untouchable industrial domain. What works in a chip fab works anywhere.",
    "{{ROBOT_1_URL}}": "https://interestingengineering.com/ai-robotics/humanoid-robots-to-join-chip-production-factories",

    # Australia
    "{{AUS_1_HEADLINE}}": "Coogee Beach Shark Attack Leaves Leah Stewart on Life Support — Eastern Suburbs Beaches Shut",
    "{{AUS_1_SUMMARY}}": "Leah Stewart was left on life support following a shark attack at Coogee Beach, Sydney, prompting temporary closure of multiple beaches across the eastern suburbs. Stewart, described as an experienced ocean swimmer, was attacked in clear and calm conditions and reached by emergency responders quickly, but suffered serious injuries. The incident has reignited debate about shark mitigation strategies, drum lines, and emergency protocols at popular NSW swimming beaches, and follows several shark sightings and encounters along the NSW coast this year.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news",

    "{{AUS_2_HEADLINE}}": "Pauline Hanson Calls for Rollback of Renewables and Multiculturalism at National Press Club — Address Briefly Disrupted by Protester",
    "{{AUS_2_SUMMARY}}": "One Nation leader Pauline Hanson used a National Press Club appearance to demand the rollback of renewable energy investment, restrictions on multiculturalism, and defunding of the ABC. The address was briefly interrupted when a protester unfurled a banner in the gallery before being removed. Political analysts noted the speech was timed to coincide with cost-of-living pressure and upcoming Senate campaign activity targeting outer-suburban and regional voters.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Festival of Football Packs Broadmeadows Fan Zone for World Cup Group Stage — Socceroos v USA Screen Event Planned for Saturday Dawn",
    "{{VIC_1_SUMMARY}}": "Victoria's official FIFA World Cup 2026 fan zone at Broadmeadows runs daily through June 28 with free entry, live match screenings, food stalls, and football activities. Organisers are planning a special pre-dawn screening for the Socceroos v USA group-stage clash on Saturday June 20 (kickoff 5:00am AEST on SBS). The Victorian government-backed activation has drawn strong crowds throughout the group stage, with Melbourne's diverse football community turning out in force.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 Entomology · Zootaxa",
    "{{SCI_1_HEADLINE}}": "New Amazonian Spider Named Taczanowskia waska Discovered — It Mimics the Very Fungus That Kills Spiders",
    "{{SCI_1_SUMMARY}}": "Scientists have described a new spider species from the Llanganates-Sangay Corridor of South America with a remarkable and previously unknown adaptation: it disguises itself as a Gibellula fungus — the very pathogen that infects and kills spiders. The species, Taczanowskia waska, features elongated abdominal projections and pale colouring that closely replicates the appearance and posture of the parasitic fungus growing on a dead spider host. The discovery was initially made via the citizen science platform iNaturalist during a night expedition when researchers mistook the spider for a mushroom. Published in Zootaxa in June 2026 by the Leibniz Institute for the Analysis of Biodiversity Change, it is the first known case of a spider mimicking a spider-killing fungus — a strategy researchers describe as evolutionarily 'weaponising fear.'",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Twelve Days to EOFY — Here Is the AI Prompt That Builds Your Action Plan Before June 30",
    "{{INSIGHT_BODY}}": "Twelve days from now, the financial year closes. The $20,000 instant asset write-off disappears. The ATO's Super Clearing House shuts permanently. Trust income distributions need documenting. Fuel prices jump when the excise reverts on July 1. And every quote you have sent in the past two weeks that has not converted yet will need repricing before you reissue it. Experienced trades business owners know this final fortnight is different — every decision has a hard deadline. AI will not file your paperwork. But it can make sure you do not miss anything. Here is the prompt to run this morning: 'I run a trades business. Give me a day-by-day action plan for June 18 to June 30, covering what to purchase before EOFY, which invoices to finalise and chase, what superannuation to check, what fuel and vehicle costs to reprice for July 1, and what documentation must be signed before midnight on June 30. Flag any items that need action before the next business day.' Print the output. Work through it one item at a time. The businesses that close the financial year clean are the ones that start July 1 with real numbers and no surprises. Twelve days is enough — but only if you start today.",

    # Fun Facts
    "{{FACT_1}}": "The diesel engine was demonstrated at the 1900 World Exhibition in Paris running on peanut oil — Rudolf Diesel specifically designed it to run on vegetable fuels so small farmers could produce their own power source. Diesel himself mysteriously disappeared from a mail steamer crossing from Antwerp to Harwich in September 1913; his body was recovered from the North Sea ten days later. Whether the cause was accident, suicide, or foul play was never determined by German police. His engine went on to power submarines, freight trains, generators, and the work vans of tradies on every continent.",

    "{{FACT_2}}": "The Pacific Ocean is larger than all of Earth's landmass combined. It covers approximately 165 million square kilometres — more than all continents and islands put together, which total roughly 148 million square kilometres. It holds more than half of the world's free surface water. If you dropped every continent into the Pacific, you would still have a gap roughly the size of Africa left unfilled.",

    "{{FACT_3}}": "The world's first industrial robot to work on a production assembly line was UNIMATE, installed at a General Motors plant in Ewing Township, New Jersey in 1961. Designed by George Devol and Joseph Engelberger, it handled hot die castings from metal — tasks too dangerous and repetitive for human workers — at a reported purchase cost of $25,000, roughly $260,000 in today's money. The arm technology from that single machine influenced the design of every industrial robot built in the six decades since.",

    # Joke
    "{{JOKE_SETUP}}": "Why do traffic controllers make the best life coaches?",
    "{{JOKE_PUNCHLINE}}": "They know exactly when to stop you, when to slow you down, and when to wave you straight through — and they charge by the hour either way.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The reasonable man adapts himself to the world; the unreasonable one persists in trying to adapt the world to himself. Therefore, all progress depends on the unreasonable man.”",
    "{{CLOSING_ATTR}}": "— George Bernard Shaw",
    "{{CLOSING_MESSAGE}}": "It's a wet Thursday in Carrum Downs with heavy showers and northerly winds running hard through at least Friday — plan outdoor work accordingly. The fuel excise cut ends in 12 days: July 1 is going to cost more at the bowser, even with global oil prices falling on the back of the US-Iran deal being formally signed in Zurich tomorrow. Run the EOFY prompt from the insight this morning. The Socceroos face the USA at 5am Saturday — Broadmeadows fan zone has big screens if you want the atmosphere without the early alarm. Winter solstice is Sunday: the shortest day of the year. From here, the days get longer. Stay unreasonable, Liall.",
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
