#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 29 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 29 Jun
    "{{WEATHER_1}}": "MON 29 · 🌦 Showers · 6–12°C",
    "{{WEATHER_2}}": "TUE 30 EOFY · ⛅ Clearing · 8–13°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "WED 1 JUL · 🌤 Fine and cold · 9–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "THU 2 · ⛅ Partly cloudy · 9–14°C",
    "{{WEATHER_5}}": "FRI 3 · 🌤 Sunny spells · 10–15°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS TODAY · EXCISE ENDS MIDNIGHT",

    # World
    "{{WORLD_1_FLAG}}": "🌏 FIFA WORLD CUP 2026 · KNOCKOUT STAGE SET",
    "{{WORLD_1_HEADLINE}}": "World Cup Group Stage Complete — All 32 Round of 32 Matchups Set as Knockout Fever Grips the Globe",
    "{{WORLD_1_SUMMARY}}": "The 2026 FIFA World Cup group stage wrapped on June 28–29 with all 32 spots in the Round of 32 confirmed across the USA, Canada and Mexico. England topped Group L after a 2–0 win over Panama — Harry Kane's header became his 11th World Cup goal, passing Gary Lineker as England's all-time leading World Cup scorer. Germany, Brazil, Netherlands and Australia all advanced. With 48 nations competing in this historic expanded tournament, the bracket is the most open and unpredictable in World Cup history. First knockout matches begin July 1.",
    "{{WORLD_1_URL}}": "https://www.espn.com/soccer/story/_/id/49204379/world-cup-2026-today-blog-28-06-2026-live-updates-news-fixtures-schedule-results-england-top-group-congo-dr",

    "{{WORLD_2_FLAG}}": "🌐 TRADE · US TARIFFS · GLOBAL REALIGNMENT",
    "{{WORLD_2_HEADLINE}}": "US Tariff Pressure Accelerates EU-Brazil Trade Alliance — New Economic Blocs Forming as America's Partners Pivot",
    "{{WORLD_2_SUMMARY}}": "Sustained US tariff policy is driving accelerated trade agreement negotiations between the European Union and Brazil — a deal that had stalled for more than two decades. With US import costs rising steeply across manufacturing, agriculture and consumer goods, both blocs are fast-tracking bilateral frameworks covering aircraft components, agricultural exports and industrial goods. Economists note the realignment is becoming structural: exporters and manufacturers in both regions are diversifying away from US market dependence in ways likely to persist regardless of future American policy changes. For Australian exporters and importers, the reshuffling of global supply chains creates both new competition and new opportunity.",
    "{{WORLD_2_URL}}": "https://www.abc.net.au/news/world",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL EXCISE · LAST DAY · FILL UP TODAY",
    "{{ECON_1_HEADLINE}}": "Diesel and Petrol Excise Cut Ends Tonight at Midnight — Last Chance to Fill Up at the Reduced Rate Before July 1",
    "{{ECON_1_SUMMARY}}": "Tonight at midnight marks the end of the federal government's temporary fuel excise reduction, which has cut approximately 26.3 cents per litre from diesel and petrol since April 1. The ACCC's most recent monitoring puts Melbourne retail diesel around $1.87/L — expect it to climb toward $2.13/L or higher from Wednesday July 1. For any trades operation running a diesel van, ute, generator or compressor, today is literally the last day to fill every tank and any jerry cans at the reduced rate. The excise return coincides with the minimum wage rise, superannuation hitting 12%, and the start of a new financial year — all landing on the same day.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "💰 WAGES · FAIR WORK · +4.75% FROM WEDNESDAY",
    "{{ECON_2_HEADLINE}}": "Australia's Minimum Wage Rises 4.75% From July 1 — Tradies With Employees Must Update Payroll Before Wednesday's First Shift",
    "{{ECON_2_SUMMARY}}": "The Fair Work Commission has confirmed a 4.75% increase to the national minimum wage and all modern award rates, effective from the first full pay period on or after July 1 2026. The national minimum wage rises to $1,004.90 per week ($26.44/hr). For trades businesses paying Building and Construction Award rates, every payroll run from Wednesday must reflect the new figures. Combined with superannuation reaching its legislated 12% ceiling on the same day, the cost of employing a full-time award-rate tradie rises by an estimated $2,500–$3,500 annually from this week. If your payroll software or timesheet system has not been updated, today is your last window to check.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 OPENAI · BROADCOM · JALAPEÑO CHIP",
    "{{TECH_1_HEADLINE}}": "OpenAI's First Custom AI Chip Promises 50% Cost Cut in Running AI — Jalapeño Built With Broadcom in Record Nine Months",
    "{{TECH_1_SUMMARY}}": "OpenAI and Broadcom unveiled Jalapeño — OpenAI's first ever custom-designed AI inference chip, co-developed from initial design to manufacturing tape-out in just nine months, believed to be the fastest ASIC development cycle ever achieved for advanced high-performance semiconductors. Unlike graphics cards that handle both training and inference, Jalapeño is purpose-built for inference — running trained AI models to answer user queries. Early testing shows roughly 50% cost savings versus current GPU-based AI infrastructure. Commercial deployment is targeted by end of 2026. For businesses using AI tools today, the practical implication is clear: AI infrastructure is getting cheaper fast, which means more capable features at lower subscription prices over the next 12–18 months.",
    "{{TECH_1_URL}}": "https://openai.com/index/openai-broadcom-jalapeno-inference-chip/",

    "{{TECH_2_FLAG}}": "📊 AI MARKET · CHATGPT BELOW 50%",
    "{{TECH_2_HEADLINE}}": "ChatGPT's Market Share Falls Below 50% for the First Time — Claude, Gemini and DeepSeek Eating Into OpenAI's Lead",
    "{{TECH_2_SUMMARY}}": "New industry data from late June 2026 confirms that ChatGPT's share of the AI assistant market has dropped below 50% for the first time since its launch in late 2022. Anthropic's Claude, Google's Gemini, and DeepSeek have collectively taken enough of the market to tip OpenAI below majority share. The shift reflects growing user sophistication: businesses are learning which AI tools perform specific tasks best, rather than defaulting to one platform for everything. For small trades businesses, this market maturity is good news — AI tools will continue to specialise, compete on price, and improve at pace. The era of a single dominant AI tool is over.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 KAWASAKI · 8-AXIS · PHYSICAL AI ROBOT",
    "{{ROBOT_1_HEADLINE}}": "Kawasaki Unveils World's First 8-Axis Industrial Robot — Extra Joints Let It Work in Spaces a Human Arm Barely Fits",
    "{{ROBOT_1_SUMMARY}}": "Kawasaki Robotics showcased the RL030N at Automate 2026 in Chicago last week — the world's first industrial robot with eight degrees of freedom. While conventional robots use six axes, the RL030N adds a seventh and eighth joint via additional elbow articulation, giving it the ability to fold into confined spaces, avoid obstacles in real time, and eliminate the singularity problem where aligned robot axes cause a conventional arm to lose control. The open KRNX control API allows third-party AI software, ROS environments and vision systems to directly control the robot in real time. Designed for adaptive assembly, confined-space manufacturing and complex motion tasks — a meaningful step from robots that repeat the same action, toward robots that navigate genuinely unpredictable environments.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/06/26/kawasaki-robotics-showcases-8-axis-physical-ai-robot-and-intelligent-automation-technologies-at-automate-2026/102869/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Lincraft Confirms All Stores Closing — 300 Jobs Gone as 88-Year Australian Retailer Goes Fully Online",
    "{{AUS_1_SUMMARY}}": "Fabric and craft retailer Lincraft has confirmed plans to progressively close all 28 remaining physical stores across Australia and New Zealand over the coming months, with 300 employees losing their jobs. The 88-year-old retailer is moving to an online-only model following a prolonged period of challenging retail conditions, changing consumer behaviour, rising operating costs and pressure from international online competitors. For the building and renovation trades, Lincraft's exit from high streets continues the pattern of bricks-and-mortar specialty retail contracting — reducing foot traffic in shopping centres and strip retail that renovation and fit-out trades often service.",
    "{{AUS_1_URL}}": "https://www.nzherald.co.nz/business/lincraft-shutting-physical-stores-as-retailer-moves-fully-online-300-jobs-affected/HFJRZSRTSVCB7C65BGMLERRB6U/",

    "{{AUS_2_HEADLINE}}": "Albanese Government Faces Mounting Backbench Pressure to Delay Negative Gearing Reforms as Property Market Cools",
    "{{AUS_2_SUMMARY}}": "Prime Minister Albanese is facing escalating pressure from Labor backbenchers, real estate groups and outer-suburban voters to delay or moderate the government's planned changes to negative gearing and the capital gains tax discount, scheduled for July 2027. With auction clearance rates below 50% nationally and some mortgage-belt markets already cooling significantly, several Labor MPs representing suburban electorates are openly questioning the timing. The government has maintained its position that redirecting investment toward new housing construction will improve affordability over time, but the political calculus is tightening ahead of the next election cycle.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Magic Festival Opens Tonight — 400 Performances, 59 Shows, the Southern Hemisphere's Biggest Magic Event Kicks Off in Carlton",
    "{{VIC_1_SUMMARY}}": "The Melbourne Magic Festival officially opens this evening with the Stage Magic Gala at The Houdini Theatre in Carlton, running through July 11. The festival features 400+ performances across 59 shows by Australian and international performers including world champions. More than 120 shows sold out last year — bookings recommended at melbournemagicfestival.com. The festival runs through the school holiday period, making it one of the stronger family and date-night options across Melbourne over the next two weeks.",

    # Science
    "{{SCI_1_FLAG}}": "🌋 GEOLOGY · YELLOWSTONE · SUPERVOLCANO",
    "{{SCI_1_HEADLINE}}": "Yellowstone's Supervolcano Is Fuelled by a 'Mantle Wind', Not a Deep Plume — And It Rewrites Eruption Science Globally",
    "{{SCI_1_SUMMARY}}": "A study published this week by Chinese and US researchers has overturned decades of conventional thinking about what powers Yellowstone's supervolcano. Rather than a deep mantle plume rising from near the Earth's core — the long-accepted model — the team found evidence of a broad horizontal 'mantle wind': a flow of hot rock from the shallow upper mantle pushed beneath Yellowstone from the west. This mechanism, they argue, better explains why Yellowstone has stayed active for so long and how it sustains such a massive magma reservoir. The findings apply to supervolcanoes globally — including Taupo in New Zealand, Campi Flegrei in Italy and systems across Indonesia — and may revise how geologists assess eruption potential at each site. Current Yellowstone activity remains at background normal levels.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The After-Job Email Your Clients Never Forget — and How AI Writes It in 30 Seconds",
    "{{INSIGHT_BODY}}": "Most trades businesses send no email after completing a job. The invoice goes out and that is it — the interaction ends there, and the relationship ends with it. That is a missed opportunity at exactly the moment client satisfaction is at its peak. A short, professional follow-up email sent within 24 hours of job completion does three things simultaneously: it invites a Google review while the work is fresh in the client's mind, it surfaces any minor concerns before they escalate into disputes or negative feedback, and it signals the kind of professionalism that generates referrals in a market where most operators never make contact again after the invoice. The problem has always been time — writing a polished, personalised email after a long day on site takes five minutes you do not have. AI solves this completely. Give your tool the client name, job type, site address and one or two specifics from the job, and ask it to write a brief professional completion email with a Google review request. The whole thing takes 30 seconds. Set this up as a template prompt on your phone today, and your post-job communication becomes automatic from the very first job of FY2027.",

    # Fun Facts
    "{{FACT_1}}": "Australia's financial year runs from 1 July to 30 June — making it one of the few countries that does not align its tax year with the calendar year. The July–June cycle was introduced in 1915 partly to align government revenue collection with the Southern Hemisphere's agricultural harvest season, when farmers would have cash on hand from selling grain and livestock. The first Australian income tax was levied at that time at a rate of between 1 and 9 pence in the pound.",

    "{{FACT_2}}": "Honeybee queens communicate with unhatched rivals through vibration — the laying queen 'toots' at roughly 200 Hz through the comb structure, and capped virgin queens yet to emerge respond with lower-pitched 'quacks.' The queen uses these calls to locate rivals and decide whether to depart with a swarm or stay and fight. Beekeepers can hear this exchange clearly by pressing a stethoscope against the outside of the hive during swarm season — no need to open the box.",

    "{{FACT_3}}": "Saffron is the world's most expensive spice by weight, valued at up to AUD $17,000 per kilogram. It takes between 150,000 and 200,000 individual Crocus sativus flowers — each hand-picked the same morning it blooms — to produce just one kilogram of dried saffron threads, which are the three stigmas extracted from each flower. Iran produces over 90 per cent of the world's supply.",

    # Joke
    "{{JOKE_SETUP}}": "Why do roofers always seem the most relaxed people on any job site?",
    "{{JOKE_PUNCHLINE}}": "Best view in the office — and they know exactly how to stay on top of things.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Quality is not an act, it is a habit.”",
    "{{CLOSING_ATTR}}": "— Aristotle",
    "{{CLOSING_MESSAGE}}": "A wet Monday in Carrum Downs to finish off FY2026 — midnight tonight is the hard deadline for cheaper fuel, so fill up the van and anything else with a tank before end of day. EOFY is tomorrow, then July 1 arrives with wages up 4.75%, super at 12% and the full fuel excise back on all at once. On the better side: the Melbourne Magic Festival opens tonight at The Houdini Theatre in Carlton if you need an excuse to get out, scientists just rewrote the textbook on what powers Yellowstone, and the World Cup knockout stage begins Wednesday. A full week of it. Make it a good one, Liall.",
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
