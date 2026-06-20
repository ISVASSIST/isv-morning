#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 21 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 21 Jun (winter solstice)
    "{{WEATHER_1}}": "SUN 21 · ⛅ Partly cloudy · 16°C",
    "{{WEATHER_2}}": "MON 22 · 🌦 Showers · 14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 23 · ⛅ Partly cloudy · 13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "WED 24 · 🌧 Showers · 13°C",
    "{{WEATHER_5}}": "THU 25 · ⛅ Clearing · 15°C",
    "{{WEATHER_ALERT}}": "☁ SOLSTICE TODAY 6:24PM · 9 DAYS TO EOFY",

    # World
    "{{WORLD_1_FLAG}}": "🌐 Iran · Strait of Hormuz",
    "{{WORLD_1_HEADLINE}}": "Iran Re-Closes Strait of Hormuz After Ceasefire Breach — Oil Markets React as Diplomatic Framework Fractures",
    "{{WORLD_1_SUMMARY}}": "In a sharp reversal from yesterday's diplomatic optimism, Iran declared the Strait of Hormuz closed again on Saturday after Israel launched fresh airstrikes on southern Lebanon killing at least 21 people — a direct violation of the ceasefire conditions Iran had required of the US. Israel said it acted after Hezbollah killed four Israeli soldiers in the south, triggering the military response. US Central Command said commercial shipping in the strait actually increased despite Iran's declaration, and Vice President JD Vance told Fox News there was no evidence the strait remained closed — though he acknowledged underwater mines placed during the conflict may still affect commercial routes. Technical talks between US and Iranian officials scheduled for this weekend in Switzerland were postponed; both sides aim to resume negotiations the week of June 22. For Australia, the renewed closure is a direct upward pressure on global oil prices heading into July, exactly as the domestic fuel excise reduction is set to expire on June 30.",
    "{{WORLD_1_URL}}": "https://www.cbsnews.com/live-updates/iran-us-war-talks-suspended-trump-mou-israel-lebanon-hezbollah-fighting/",

    "{{WORLD_2_FLAG}}": "🌐 Lebanon · Israel · Hezbollah",
    "{{WORLD_2_HEADLINE}}": "Israel-Hezbollah Ceasefire Collapses Within Hours — Fresh Strikes Kill Dozens as Lebanon Truce Unravels",
    "{{WORLD_2_SUMMARY}}": "A ceasefire agreed between Israel and Hezbollah on Thursday June 19 effectively collapsed within hours as Israeli forces launched a fresh wave of strikes on southern Lebanon on Friday, killing at least 21 people and citing Hezbollah's killing of four Israeli soldiers as provocation. The Lebanese Health Ministry reported at least 47 deaths across two days of fighting. The violence directly threatened the broader US-Iran diplomatic framework: Iran has stated any agreement with the United States is contingent on hostilities in Lebanon ending. The fragility of the situation illustrates the interconnected nature of the Middle East diplomatic architecture — each military action can cascade into an oil supply disruption that flows through to fuel costs in markets as distant as Australia.",
    "{{WORLD_2_URL}}": "https://www.cbc.ca/news/world/israel-lebanon-strikes-9.7241314",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ Fuel · Australia",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Returns June 30 as Strait Crisis Reignites — July Diesel Could Jump Over 50 Cents Per Litre Overnight",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly fuel price monitoring update (June 19) confirmed retail diesel prices have fallen approximately 38% across Australia's major cities since the temporary 32-cent-per-litre excise reduction took effect on April 1 — with Melbourne diesel sitting around $1.85–1.90/L. Two simultaneous upward pressures are now converging on July 1: the certain expiry of the excise reduction, and fresh global supply uncertainty after Iran re-closed the Strait of Hormuz overnight. The excise alone pushes Melbourne retail diesel above $2.20/L from July 1. If global oil markets react materially to renewed strait disruption, a July diesel price above $2.50/L is within range. For a trades business in Carrum Downs with diesel vehicles, equipment and subcontractors, every job currently being quoted for July completion needs to absorb the higher fuel input before the quote is sent.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📊 EOFY · Small Business",
    "{{ECON_2_HEADLINE}}": "Nine Days, Three Cost Hits on the Same Morning — Why This Week Is the Most Important Financial Planning Window of 2026",
    "{{ECON_2_SUMMARY}}": "Nine days remain before a triple cost increase hits simultaneously on July 1: the minimum wage rise under the Fair Work Commission's annual review, the commencement of Payday Super (superannuation now due within seven business days of each pay run rather than quarterly), and the return of the full fuel excise as the temporary reduction expires. For a trades business in Carrum Downs with staff on award rates and diesel-dependent operations, these three changes represent a meaningful and permanent increase to weekly operating costs. This week — before the changes land — is the right window to review job pricing, update hourly rate calculations, and adjust any fixed-price quotes covering work that extends beyond June 30.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI Agents · Enterprise",
    "{{TECH_1_HEADLINE}}": "KPMG Deploys Microsoft AI Agents to 276,000 Staff — The Biggest Autonomous Workflow Rollout in Professional Services History",
    "{{TECH_1_SUMMARY}}": "KPMG and Microsoft announced an expansion of their global partnership rolling out Microsoft Agent 365 — a suite of autonomous AI agents — across KPMG's entire workforce of more than 276,000 professionals in 143 countries. The agents handle multi-step tasks autonomously: audit workflow sequences, tax research, compliance documentation and client reporting — without requiring a human to prompt each step. Gartner estimates 40% of enterprise applications will include task-specific AI agents by the end of 2026, up from less than 5% in 2025. For a sole-operator trades business, the same shift is underway at a smaller scale: the AI tools now available can handle quoting sequences, invoice follow-up, schedule management and supplier communications as connected, autonomous workflows — not just individual tasks. The gap between what the biggest firms are doing and what is available to a small operator has never been narrower.",
    "{{TECH_1_URL}}": "https://enterprisedna.co/resources/news/kpmg-microsoft-agent-365-enterprise-ai-agents-2026/",

    "{{TECH_2_FLAG}}": "🤖 AI · Small Business",
    "{{TECH_2_HEADLINE}}": "AI Agents Are Now Running Overnight Business Workflows — What That Means for the Tradesperson Working 6am to 6pm",
    "{{TECH_2_SUMMARY}}": "A practical pattern is emerging across small and medium business in Australia: AI agents handling email follow-ups, quote compilation, scheduling confirmations and supplier orders between 6pm and 7am — when the business owner is unavailable. Deployed through platforms like Microsoft 365 Copilot, Anthropic's Claude and Google Workspace AI, these autonomous workflows operate on defined rules, escalating only when they hit a decision that requires a human. For a solo trades operator who currently handles all admin after hours, this model — configurable in an afternoon — effectively extends the working day without adding hours. The practical entry point is relatively simple: a Claude or Copilot workflow that processes the day's emails, drafts replies, flags urgent items and sends a morning summary before 7am.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ABB Robotics · Automate 2026",
    "{{ROBOT_1_HEADLINE}}": "ABB Robotics Launches Physical AI-Ready PoWa Cobots at Automate 2026 — Arms That Train in Simulation, Deploy in Hours Not Weeks",
    "{{ROBOT_1_SUMMARY}}": "ABB Robotics has unveiled its PoWa high-speed cobot family at Automate 2026 in Chicago, incorporating NVIDIA Omniverse libraries directly into RobotStudio to allow manufacturers to train robotic workflows entirely in simulation before deploying to a live production floor. The PoWa arms offer higher payload and faster cycle times than previous ABB cobots and are designed to be operational in hours rather than the weeks of specialist programming traditionally required. This collapses the biggest barrier to small-to-medium manufacturer adoption: the need for expensive robot integrators and lengthy commissioning cycles. ABB is the world's second-largest industrial robotics company, with more than 400,000 robots installed annually. The integration of NVIDIA's physical AI stack into the robot programming environment marks a commercial inflection point for production-line automation.",
    "{{ROBOT_1_URL}}": "https://www.automate.org/robotics/news/abb-robotics-delivers-new-industry-ready-physical-ai-at-automate-2026-abb",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Activates National H5 Bird Flu Response After First Wild Bird Detection in Western Australia",
    "{{AUS_1_SUMMARY}}": "The Australian Government activated its national avian influenza response on June 20 after CSIRO's Australian Centre for Disease Preparedness confirmed H5 high pathogenicity bird flu in a wild brown skua seabird found sick in an isolated coastal area of southern Western Australia on June 14. This is Australia's first detection of the highly pathogenic strain that has been circulating globally — in a wild seabird, not a commercial flock. The Department of Agriculture is coordinating nationally, surveillance testing is underway on nearby wildlife, and poultry industry biosecurity measures have been reinforced. The Australian Centre for Disease Control advises human health risk is low, and Food Standards Australia confirms chicken and eggs remain safe if handled and cooked correctly.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/podcast-episode/australia-activates-bird-flu-response-evening-news-bulletin-20-june-2026/f8hzpom1w",

    "{{AUS_2_HEADLINE}}": "Socceroos Must Win Against Paraguay on June 25 to Reach World Cup Knockout Rounds",
    "{{AUS_2_SUMMARY}}": "After Australia's defeat to the United States in Seattle on June 19, the Socceroos must win their final Group D match against Paraguay on June 25 (9am AEST, Kansas City) to advance to the World Cup last 32. Australia opened Group D with a 2-0 win over Türkiye on June 13 and currently sit on three points — level with Paraguay. A win guarantees progression; a draw may be sufficient depending on goal difference. The match is live on SBS. For Melbourne viewers it is a Wednesday morning 9am kickoff — a convenient time before the day's first job.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Winter Solstice Falls at 6:24pm Tonight — Nightide Fire Festival Lights Up Queenscliff as Melbourne's Year Officially Turns",
    "{{VIC_1_SUMMARY}}": "Melbourne's winter solstice arrives at 6:24pm this evening, the precise moment Earth's axial tilt places the Southern Hemisphere at its maximum distance from the sun — just 9 hours and 20 minutes of daylight today, the least of any day this year. On the Bellarine Peninsula, the Nightide festival is underway at Queenscliff with burning sculptures, fire performances, food trucks and fireworks against the winter coast. Brunswick's Ceres community garden is hosting its annual Winter Solstice gathering, and city lantern walks are running through the CBD into the evening. From tomorrow, Melbourne gains approximately one to two minutes of daylight each day through to the summer solstice in December.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 Astrophysics · Neutrinos",
    "{{SCI_1_HEADLINE}}": '"Shadow Blaster" Galaxy Rewrites Cosmic Neutrino Theory — Extreme Star Formation, Not a Black Hole, Is the Source',
    "{{SCI_1_SUMMARY}}": "A distant galaxy nicknamed Shadow Blaster has disrupted the dominant theory about where the universe's highest-energy cosmic neutrinos originate. New research published in June 2026 found that instead of being generated by the supermassive black hole at the galaxy's centre — the previously assumed mechanism — the neutrinos appear to originate from an extreme burst of star formation within the galaxy itself. The finding challenges the blazar model that has dominated high-energy astrophysics for a decade and opens an entirely new category of cosmic neutrino source. Neutrinos are nearly massless, chargeless particles that travel at near-light speed across the universe without interaction, making them uniquely capable of carrying information from violent cosmic events that cannot be observed by any other means — including light, radio waves or X-rays.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI Can Write Your Job Ad, Screen the Replies, and Draft the Offer Letter — Tradies Are Hiring Smarter in 2026",
    "{{INSIGHT_BODY}}": "Finding a good apprentice or experienced labourer has never been harder — demand is high, skilled workers are scarce, and writing a decent job ad takes time most operators simply do not have. Posting on Seek, fielding forty unqualified replies, and drafting an offer letter can burn a full day you needed on the tools. AI changes the entire equation. Start by giving a language model your trade, the specific role, your suburb, and two or three things that make your business a good place to work — it will produce a sharp, targeted job ad in under two minutes. Paste the first batch of applications back in and ask it to score them against your criteria: relevant experience, location, availability, licences held. Then, when you have found your person, ask AI to draft the offer letter, employment summary, and induction checklist. The whole process — from blank page to a signed offer — can now happen in a Sunday evening. For a small operator in Carrum Downs competing for the same pool of apprentices and labourers as national contractors, a professional and well-written hire process is itself a competitive advantage before the first interview is held.",

    # Fun Facts
    "{{FACT_1}}": "Today, June 21, is Melbourne's winter solstice — Earth's axial turning point for the Southern Hemisphere. The exact moment of solstice is 6:24pm AEST this evening, when the Southern Hemisphere reaches its maximum tilt away from the sun. Stonehenge's massive central trilithon in southern England was deliberately constructed to frame the winter solstice sunset over 5,000 years ago — evidence that Bronze Age builders already understood the precise geometry of Earth's relationship with the sun well enough to engineer a stone monument aligned to within fractions of a degree.",

    "{{FACT_2}}": "The world's first ATM was installed by Barclays Bank at its Enfield branch in North London on 27 June 1967 — 59 years ago this week. British comedian and On the Buses star Reg Varney was selected as the first customer to withdraw cash. The machine dispensed notes encoded with mildly radioactive carbon-14 ink, the only technology of the era reliable enough for machine reading. Maximum withdrawal per visit: £10.",

    "{{FACT_3}}": "The smell of freshly cut grass is not a pleasant side effect of mowing — it is a plant distress broadcast. Lawn grasses release a cocktail of volatile organic compounds called green leaf volatiles (GLVs) when their cells are damaged, simultaneously warning neighbouring plants to ramp up their own chemical defences before any herbivore reaches them. The characteristic scent humans enjoy on a winter Sunday morning is, in botanical terms, a broadcast emergency signal.",

    # Joke
    "{{JOKE_SETUP}}": "Why do solar panel installers make the best optimists?",
    "{{JOKE_PUNCHLINE}}": "No matter what the weather does — they always look on the bright side.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Keep your face to the sunshine and you cannot see a shadow.”",
    "{{CLOSING_ATTR}}": "— Helen Keller",
    "{{CLOSING_MESSAGE}}": "Today is the winter solstice — the Southern Hemisphere's shortest day, with the sun setting at precisely 6:24pm to mark the turning point of the year. From tomorrow, every single day gets a little longer. The Strait of Hormuz situation reversed overnight after yesterday's ceasefire optimism, which means the July diesel picture is cloudier again — right as the domestic excise cut also expires on June 30. The Socceroos need a win against Paraguay on June 25 to stay in the World Cup. Nine days to EOFY: a good Sunday to lock in job pricing for the post-July cost environment, enjoy the winter light while it lasts, and keep your face to the sunshine. Have a good one, Liall.",
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
