#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 23 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 23 Jun
    "{{WEATHER_1}}": "TUE 23 · ⛅ Partly cloudy · 15°C",
    "{{WEATHER_2}}": "WED 24 · 🌧 Showers likely · 13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 25 · ☁ Becoming cloudy · 12°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 26 · 🌫 Foggy/showers · 13°C",
    "{{WEATHER_5}}": "SAT 27 · 🌧 Morning showers · 14°C",
    "{{WEATHER_ALERT}}": "☁ COOL GREY WEEK · 7 DAYS TO EOFY",

    # World
    "{{WORLD_1_FLAG}}": "🌐 UK · LABOUR · LONDON",
    "{{WORLD_1_HEADLINE}}": "UK Prime Minister Keir Starmer Resigns — Britain Set for Its Seventh Leader in a Decade",
    "{{WORLD_1_SUMMARY}}": "Keir Starmer announced his resignation as UK Prime Minister on Monday after a sustained party revolt triggered by Labour's catastrophic May local election losses — more than 1,000 council seats lost to Reform UK and the Liberal Democrats. Nominations to replace him as Labour leader open July 9 and close when Parliament rises for summer recess July 16. His expected successor, Andy Burnham — former Mayor of Greater Manchester — won a by-election in Makerfield last week, securing a parliamentary seat from which to contest the leadership. If confirmed, Burnham will be Britain's seventh prime minister in ten years. The UK remains Australia's third-largest trading partner, and the Australia-UK Free Trade Agreement (AUKFTA) implementation will be one of the early policy files for whoever takes the top job.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/06/22/nx-s1-5866231/keir-starmer-resigns",

    "{{WORLD_2_FLAG}}": "🌐 USA · IRAN · NUCLEAR",
    "{{WORLD_2_HEADLINE}}": "US and Iran Agree on 60-Day Roadmap to Final Nuclear Deal — Strait of Hormuz Deconfliction Channel Established",
    "{{WORLD_2_SUMMARY}}": "Mediators Qatar and Pakistan announced Monday that US and Iranian negotiators in Switzerland had agreed to a roadmap for reaching a final deal within 60 days, establishing three working groups on oversight, sanctions, and nuclear arrangements. A dedicated contact channel was also set up to prevent incidents in the Strait of Hormuz — the chokepoint through which roughly 20% of globally traded oil flows daily — and a deconfliction cell for Lebanon was agreed. Nothing substantive has yet been negotiated on uranium enrichment levels, with those discussions expected during the 60-day window. For Australian businesses and fuel buyers, the timeline matters: the negotiating period runs through to late August, meaning Hormuz remains an elevated geopolitical risk to fuel prices well beyond July 1 when Australia's domestic excise relief ends.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/6/22/us-iran-agree-on-roadmap-towards-final-deal-in-switzerland-talks",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ ACCC · DIESEL · JUNE 30",
    "{{ECON_1_HEADLINE}}": "ACCC Diesel Monitor: National Average 198.6¢/L as 32¢ Excise Restoration Now 7 Days Away",
    "{{ECON_1_SUMMARY}}": "The ACCC's 15th weekly fuel monitoring report (June 19) shows national diesel averaging 198.6¢/L under the temporary excise reduction expiring June 30. Melbourne retail diesel has been tracking 188–195¢/L during the relief period. The ACCC has confirmed it will monitor retailer behaviour closely after July 1 to ensure any price increases match the actual 32¢ restoration rather than expanded margins — a direct response to uneven pass-through observed in April. For Carrum Downs trades operators with diesel vehicles, compressors and equipment, every quote issued today for work extending past July 1 should be costed at post-excise fuel levels (approximately $2.20–2.30/L) rather than today's suppressed rate. The final ACCC weekly update before the change is due Thursday June 26.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📊 ATO · SMALL BUSINESS · JUNE 30",
    "{{ECON_2_HEADLINE}}": "Small Business Energy Incentive Final 7 Days — 120% Deduction on Qualifying Energy-Efficient Equipment Closes With the Financial Year",
    "{{ECON_2_SUMMARY}}": "The Small Business Energy Incentive — extended through to June 30, 2026 — allows eligible businesses with aggregated turnover under $50 million to claim a bonus 20% deduction on top of the full cost of qualifying energy-efficient assets (effectively a 120% deduction), capped at $100,000 per asset. Eligible items include energy-efficient HVAC, LED lighting, battery storage, and EV charging infrastructure. For trades businesses in Carrum Downs considering equipment upgrades, any qualifying asset purchased, delivered, and ready for use before June 30 can be included in the FY2026 tax return. The ATO has confirmed the incentive will not carry over to FY2027 — after June 30 the same equipment is deducted at the standard rate only. This week is the last practical window to act.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 FOXCONN · NVIDIA · FACTORY AI",
    "{{TECH_1_HEADLINE}}": "Foxconn Deploys MoMClaw — 80% Faster Fault Diagnosis as Multi-Agent AI Runs Across Live Production Lines",
    "{{TECH_1_SUMMARY}}": "Foxconn — the world's largest contract manufacturer — has publicly detailed MoMClaw, its multi-agent AI manufacturing system now running across live production facilities. Built on NVIDIA's Factory Operations Blueprint (FOX), MoMClaw connects hundreds of AI agents to real-time machine sensors, ERP data, and safety systems simultaneously, giving plant managers natural-language access to the entire factory's state. The reported results: 80% faster root-cause analysis when equipment faults occur, a 15% labour productivity improvement, and a 10% reduction in equipment failure rates. For smaller industrial operators, the principle is scale-independent — AI tools that continuously monitor your operational data and flag emerging patterns before they become problems are available today using standard job management software, without the data centre investment.",
    "{{TECH_1_URL}}": "https://roboticsandautomationnews.com/2026/06/11/nvidia-launches-ai-factory-manager-blueprint-for-autonomous-manufacturing/102491/",

    "{{TECH_2_FLAG}}": "🤖 AI · AGENTIC WORKFLOWS · 2026",
    "{{TECH_2_HEADLINE}}": "Gartner: 40% of Enterprise Apps Will Integrate AI Agents by End of 2026 — Small Trades Businesses Are Already Feeling the Shift",
    "{{TECH_2_SUMMARY}}": "Gartner's latest AI forecast projects that 40% of enterprise applications will integrate AI agents — capable of executing multi-step tasks autonomously — by the end of 2026. McKinsey data shows 62% of organisations already experimenting with agents, with 23% having scaled them across the business. The practical shift is from 'chatbot' to 'workflow operator': rather than answering a question, AI agents draft the quote, send the follow-up email, log the completed job, and book the next service call without a human prompting each step. For a trades operator currently handling all of that manually after hours, the question is no longer whether AI can do these tasks — it demonstrably can — but how many weeks of setup time you're prepared to invest to get the hours back permanently.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 AUTOMATE 2026 · HUMANOID FORUM · CHICAGO",
    "{{ROBOT_1_HEADLINE}}": "Automate 2026 Humanoid Robot Forum Opens Today — Boston Dynamics, NVIDIA and Toyota on Six-Month Factory Payback Economics",
    "{{ROBOT_1_SUMMARY}}": "The Humanoid Robot Forum at Automate 2026 formally opened Tuesday at Chicago's McCormick Place, with speakers from Boston Dynamics, Neura Robotics, NVIDIA, and the Toyota Research Institute presenting on the real-world economics of humanoid robot deployment. The forum runs across today and Wednesday alongside the NVIDIA-sponsored Humanoid Robot Pavilion, displaying more than 20 operational humanoid robots from manufacturers across the US, China, Japan and Europe. The A3 Innovation Awards are also being presented today, recognising standout developments across industrial automation and AI-guided manufacturing. The most consistent message from today's presentations: structured industrial environments with repeatable tasks are now achieving six-month capital payback periods on humanoid deployment — a figure that has compressed dramatically since the first commercial trials in 2024. What is happening in Chicago this week is the clearest available signal of what Australian factory floors will look like in 18 to 24 months.",
    "{{ROBOT_1_URL}}": "https://www.automateshow.com/education-networking/humanoid-robot-forum",

    # Australia
    "{{AUS_1_HEADLINE}}": "NRL State of Origin — Blues Star Ruled Out of Sydney Decider as Queensland Leads Series",
    "{{AUS_1_SUMMARY}}": "A key New South Wales Blues player has been ruled out of the State of Origin Game III decider after sustaining an injury, adding to selection pressure on NSW coach Michael Maguire ahead of the must-win clash at Accor Stadium in Sydney. Queensland leads the 2026 series 1-0 after claiming Game II, meaning NSW must win at home to level the series. Game III is one of the most watched sporting events of the Australian winter calendar — for Melbourne's large NSW-origin community it is appointment viewing, and for Queensland fans in the southeast suburbs, bragging rights on the line.",
    "{{AUS_1_URL}}": "https://www.nrl.com/news/state-of-origin/",

    "{{AUS_2_HEADLINE}}": "2026 Logie Award Nominees Revealed — Television's Night of Nights Returns to the Gold Coast in August",
    "{{AUS_2_SUMMARY}}": "TV Week has published the full list of nominees for the 2026 Logie Awards, with the Seven Network, Nine Network, and the ABC featuring prominently across the major categories. The Gold Logie — the industry's highest individual honour — will be decided by public vote, with nominations open until late July. The ceremony returns to The Star Gold Coast in August. The Logies remain Australia's longest-running television awards, and the nominee list is a reasonable snapshot of which Australian productions captured national attention across the past 12 months.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Level Crossing Removal Program Passes 88 Completions — Southeast Rail Corridor Among State's Most Transformed",
    "{{VIC_1_SUMMARY}}": "Victoria's Big Build has now removed 88 level crossings statewide, with a further 8 targeted for completion in 2026. The Frankston and Pakenham rail lines serving Melbourne's southeast — including the Carrum corridor — have been among the program's most heavily upgraded, with multiple grade separations built and frequency improvements delivered. For trades operators in Carrum Downs, the upgraded lines have measurably reduced commute times for employees travelling from Melbourne's northern and western suburbs, and the removal of at-grade crossings has improved heavy vehicle travel times along key arterials serving the industrial zone. The state's $21.4 billion infrastructure investment program continues through the 2025-26 budget year.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 UNIVERSITY OF BRISTOL · NATURE COMMUNICATIONS · JUNE 2026",
    "{{SCI_1_HEADLINE}}": "Tropical Butterfly Defies Ageing — Heliconius Species Live Up to 25 Times Longer Than Close Relatives With No Physical Decline",
    "{{SCI_1_SUMMARY}}": "Scientists at the University of Bristol have discovered that certain Heliconius butterflies have evolved a dramatic resistance to the ageing process, living up to 25 times longer than closely related species. The longest-lived, Heliconius hewitsoni, reached a maximum lifespan of 348 days while a close relative, Dione juno, lived just 14 days. Unusually, the long-lived species showed no evidence of the physical decline typically associated with ageing — maintaining body mass, muscle function and reproductive activity throughout their extended lives. The lifespan advantage persisted even when dietary pollen was removed, suggesting the longevity has been genetically encoded through evolution rather than purely driven by diet. Published in Nature Communications on June 16 and covered by ScienceDaily June 22, the findings open Heliconius as a powerful model for understanding what biological mechanisms allow some animals to age far more slowly than others.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Training Your Next Generation: How AI Is Helping Small Trades Businesses Onboard Apprentices Faster and Keep Them Longer",
    "{{INSIGHT_BODY}}": "Apprentice onboarding is one of the most time-consuming, underdocumented processes in a small trades business — and one where AI is delivering genuine operational value right now. The core problem: most of what an apprentice needs to know to work safely and productively lives inside the operator's head, not on paper. AI tools like Claude allow you to extract and structure that knowledge quickly — describe how you handle a job type, what safety checks you run before a task, how you respond to common site problems, and the AI turns that conversation into structured training notes, task checklists, and a first-week orientation guide in under an hour. Beyond onboarding documents, AI can draft SWMS templates for your most common tasks, prepare communication scripts for a first-year's initial client phone calls, and generate knowledge-check questions to test retention after practical training. Australian apprenticeship completion rates sit around 50% nationally — a significant part of that attrition stems from apprentices feeling underprepared and unsupported in the first months on site. A structured, documented onboarding process, built in a single evening with AI assistance, is one of the most direct investments a small Carrum Downs operator can make in both retention and productivity. The apprentices most likely to stay are the ones who felt set up to succeed from day one.",

    # Fun Facts
    "{{FACT_1}}": "Polar bears do not have white fur — their individual hairs are actually hollow and transparent, appearing white due to light scattering. Beneath the fur, polar bear skin is jet black, absorbing solar heat directly to supplement the insulation of the coat. The hollow-fibre structure also traps air as an additional thermal barrier against Arctic temperatures, making polar bear fur one of the most effective natural insulation systems on Earth.",

    "{{FACT_2}}": "The world's oldest continuously operating restaurant is Sobrino de Botín in Madrid, established in 1725 by French cook Jean Botín, and certified by Guinness World Records. Its original wood-fired oven — installed in 1725 — is still in use today, making it the oldest working oven in continuous commercial use. Ernest Hemingway famously ended his 1926 novel 'The Sun Also Rises' at Botín, where the characters order roast suckling pig.",

    "{{FACT_3}}": "The Gamburtsev Mountains beneath Antarctica are the size of the European Alps — with peaks reaching 2,700 metres — yet they are entirely invisible, buried under approximately 4 kilometres of ice. Discovered in 1958 by Soviet seismologist Grigory Gamburtsev using seismic surveys, they remain one of Earth's great geological mysteries: mountain ranges of this age should have been eroded completely flat hundreds of millions of years ago, yet the Gamburtsevs are largely intact beneath the ice sheet.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pest controller always have a full diary?",
    "{{JOKE_PUNCHLINE}}": "Because his work was always bugging someone.",

    # Closing
    "{{CLOSING_QUOTE}}": "“You miss 100% of the shots you don’t take.”",
    "{{CLOSING_ATTR}}": "— Wayne Gretzky",
    "{{CLOSING_MESSAGE}}": "It's Tuesday June 23 — seven days to the end of the financial year. Partly cloudy in Carrum Downs today, around 15°C, with showers likely from Wednesday through the weekend so plan outdoor work accordingly. The world had a busy Monday night: Keir Starmer is out as UK Prime Minister, with Andy Burnham set to become Britain's seventh PM in ten years; and the US and Iran agreed a 60-day roadmap for a nuclear deal, with a Hormuz deconfliction channel as part of the package — keeping fuel price risk elevated past July 1. Diesel is nationally at 198.6¢/L right now; that jumps roughly 32¢ a litre next Monday when the excise relief ends. If you've been planning any energy-efficient equipment purchases, the Small Business Energy Incentive bonus deduction closes with the financial year this Sunday. The Humanoid Robot Forum at Automate 2026 is running today and tomorrow in Chicago — the world's clearest real-time signal of where industrial robotics is heading in the next 18 months. Seven days, Liall. Make them count.",
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
