#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 22 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 22 Jun
    "{{WEATHER_1}}": "MON 22 · 🌦 Showers · 14°C",
    "{{WEATHER_2}}": "TUE 23 · ⛅ Partly cloudy · 13°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "WED 24 · 🌧 Showers · 13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 25 · ⛅ Clearing · 15°C",
    "{{WEATHER_5}}": "FRI 26 · ☁ Cloudy · 14°C",
    "{{WEATHER_ALERT}}": "☁ SHOWERS TODAY · 8 DAYS TO EOFY",

    # World
    "{{WORLD_1_FLAG}}": "🌐 USA · Iran · Hormuz",
    "{{WORLD_1_HEADLINE}}": "Trump Threatens Iran Strikes as Hormuz Diplomatic Progress Teeters — Talks Resume This Week Despite Escalating Rhetoric",
    "{{WORLD_1_SUMMARY}}": "With the US-Iran Memorandum of Understanding signed June 17 having allowed commercial shipping to gradually resume through the Strait of Hormuz — 25 vessels crossed on June 18, the highest count since April — the fragile ceasefire came under new pressure on Sunday as US President Donald Trump publicly threatened further strikes on Iran unless Hezbollah ceased operations in Lebanon. Iran's chief negotiator Mohammad Bagher Ghalibaf responded that the US should \"be careful with their statements.\" Technical talks between Washington and Tehran are scheduled to resume in Switzerland this week. For Australian businesses, the Hormuz diplomatic picture is directly connected to July fuel costs: the partial opening had been contributing to modest crude price relief heading into the June 30 fuel excise expiry, and any renewed escalation would compound the domestic excise increase with global supply pressure.",
    "{{WORLD_1_URL}}": "https://www.britannica.com/event/2026-Iran-war",

    "{{WORLD_2_FLAG}}": "🌐 Ukraine · Russia · Crimea",
    "{{WORLD_2_HEADLINE}}": "Ukraine Drone Strikes Knock Out Crimea Fuel Depots and Krasnodar Oil Terminal — Russia Halts All Civilian Petrol Sales on Peninsula",
    "{{WORLD_2_SUMMARY}}": "Ukraine carried out a major wave of drone strikes against Russian fuel infrastructure on Sunday June 21, hitting an oil depot in Crimea and an oil transport terminal in Russia's southern Krasnodar region — a key Black Sea supply hub. Russian-appointed Crimean authorities announced an indefinite suspension of civilian petrol and diesel sales, restricting fuel to government agencies only. Four people were killed and 28 injured in the Crimean strikes according to Russian officials. Ukrainian President Zelensky described the campaign as \"long-range sanctions\" on Russian energy infrastructure, targeting the fuel that sustains Russia's military operations in the region. The strikes underscore how energy supply infrastructure has become a direct military target in 2026 — a dynamic shaping the global energy price environment heading into the July 1 Australian fuel excise return.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/06/21/g-s1-129200/ukrainian-attacks-russia-crimea-halt-gas-sales",

    # Economics
    "{{ECON_1_FLAG}}": "📊 EOFY · Australia · July 1",
    "{{ECON_1_HEADLINE}}": "Eight Days: Payday Super Starts, Minimum Wage Rises 4.75%, and the SBSCH Closes Permanently — All on the Same Morning",
    "{{ECON_1_SUMMARY}}": "With eight days remaining before July 1, three simultaneous changes transform the payroll landscape for every Australian employer: the national minimum wage rises 4.75% to $26.44 per hour; Payday Superannuation commences, requiring super to reach employee funds within seven business days of each pay run rather than quarterly; and the Small Business Super Clearing House (SBSCH) closes permanently. This is the largest single-day payroll compliance event in two decades — affecting approximately 1.3 million employers with no exemptions for small business. Trades operators with even a single employee on award wages need updated payroll software, a transition away from the SBSCH to an alternative clearing service, and recalculated hourly cost rates before their next quote after June 30. This week is the last practical window to get it done before the change lands.",
    "{{ECON_1_URL}}": "https://business.gov.au/news/changes-for-businesses-from-1-july-2026",

    "{{ECON_2_FLAG}}": "⛽ Fuel · Australia",
    "{{ECON_2_HEADLINE}}": "Diesel to Jump More Than 30 Cents Per Litre on July 1 as Excise Relief Expires — Every Quote Going Out This Week Needs to Absorb It",
    "{{ECON_2_SUMMARY}}": "The temporary 32 cents-per-litre fuel excise reduction in place since April 1 expires on June 30. Melbourne retail diesel has been sitting around $1.85–1.90/L under the reduced rate; from July 1 that rises above $2.20/L overnight. For a trades business in Carrum Downs with diesel vehicles, equipment and subcontractors, every job being quoted today for work extending past June 30 needs to factor in the higher fuel input before the quote is sent. The Hormuz diplomatic situation adds some upside risk: if US-Iran tensions re-escalate this week, global crude prices could move higher and push July diesel toward $2.50/L in a worst-case scenario — making it critical to build a fuel cost buffer into any fixed-price quote being issued right now.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 Anthropic · Claude Code",
    "{{TECH_1_HEADLINE}}": "Claude Code Gets Live Shared Dashboards and Collaborative AI Workspaces — Biggest Platform Update to Anthropic's Business Toolkit in 2026",
    "{{TECH_1_SUMMARY}}": "Anthropic has updated Claude Code Artifacts to support live, shared collaborative dashboards and interactive workspaces accessible across enterprise teams simultaneously. The update — available on Max, Team and Enterprise plans — allows multiple users to interact with the same AI-generated outputs in real time, so AI-produced documents, schedules, quote templates and reporting summaries can function as live shared working files rather than static exports. For a small business operator, the practical version is straightforward: anything AI generates for your business — a job schedule, a quote template, a weekly debrief summary — can now be opened by your team and edited live, the same way a shared spreadsheet works. The update signals the direction Anthropic is taking Claude from single-user Q&A tool toward collaborative business infrastructure platform.",
    "{{TECH_1_URL}}": "https://venturebeat.com/data/anthropics-claude-code-artifacts-update-brings-live-shared-dashboards-and-interactive-workspaces-to-enterprises",

    "{{TECH_2_FLAG}}": "🤖 AI · Business Tools · 2026",
    "{{TECH_2_HEADLINE}}": "AI Has Stopped Being a Chatbot and Started Being a Business Operator — The 2026 Shift Every Trades Business Should Understand",
    "{{TECH_2_SUMMARY}}": "The practical shift in AI use across Australian small and medium business in 2026 is striking: the technology has moved from \"ask a question, get an answer\" to \"configure a workflow, get the output automatically.\" Platforms including Claude, Copilot and Google Workspace now support agentic sequences — where AI executes multi-step tasks (drafts the quote, sends the follow-up, logs the outcome, books the next job) without a human prompting each step. For a sole-operator trades business currently handling all admin after hours, the practical entry point is a single afternoon of setup: define the workflow, set the rules for escalation to you, and let the AI handle repeating low-cognitive tasks overnight. The businesses setting this up in 2026 are not large operators — they are exactly the kind of small trades and service businesses that can least afford to lose hours to admin.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 Google · Intrinsic · Automate 2026",
    "{{ROBOT_1_HEADLINE}}": "Google's Intrinsic Keynotes Automate 2026 Opening Day — \"Android for Robots\" Platform Shows AI-Native Industrial Programming to 50,000 Attendees",
    "{{ROBOT_1_SUMMARY}}": "North America's largest robotics and automation show, Automate 2026, opens at McCormick Place Chicago today (June 22) with Google's industrial robotics division Intrinsic delivering one of the event's six keynotes. Intrinsic's Flowstate platform — which Google has described as \"the Android of robotics\" — allows factory workers to build and modify robot work programs using AI-guided skill blocks and visual programming, eliminating the specialist code and robot engineers that have historically been the barrier to adoption. Configuration that once took days of specialist programming can now be completed by a trained factory floor worker in hours. For small industrial operations in Australia considering robotic assistance for repetitive production tasks, the consistent message from Automate this week is that both the hardware cost and the programming barrier are falling simultaneously — making 2026 the most practical entry point the sector has ever seen.",
    "{{ROBOT_1_URL}}": "https://www.automateshow.com/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Activates National H5 Bird Flu Response After First High-Pathogenicity Detection in Wild Seabird",
    "{{AUS_1_SUMMARY}}": "Australia's national avian influenza response was formally activated on June 20 after CSIRO's Australian Centre for Disease Preparedness confirmed high-pathogenicity H5 bird flu in a wild brown skua seabird found sick near a coastal area of southern Western Australia on June 14. This is Australia's first confirmed detection of the highly pathogenic strain circulating globally in 2025–2026 — and critically, it was found in a wild seabird, not a commercial poultry flock. The Department of Agriculture is coordinating national surveillance testing on nearby wildlife, and commercial poultry industry biosecurity measures have been reinforced. The Australian Centre for Disease Control advises human health risk remains low, and Food Standards Australia New Zealand confirms chicken and eggs remain safe when properly handled and cooked.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/podcast-episode/australia-activates-bird-flu-response-evening-news-bulletin-20-june-2026/f8hzpom1w",

    "{{AUS_2_HEADLINE}}": "Socceroos Must Beat Paraguay on Wednesday Morning to Stay in the World Cup — 9am AEST Kickoff in Kansas City",
    "{{AUS_2_SUMMARY}}": "Australia sits third in World Cup Group D on goal difference after a 2-0 win over Türkiye (June 13) and a 1-0 loss to the United States (June 19). The Socceroos need a win in their final group match against Paraguay on Wednesday June 25 at 9am AEST (Kansas City) to advance to the knockout rounds. Both Australia and Paraguay currently have three points — making Wednesday effectively a sudden-death match. Live on SBS; Federation Square, AAMI Park and Bunjil Place in Narre Warren will host public viewing events from 8:30am Wednesday, making it a convenient pre-work watch for Melbourne trades workers.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Record Winter Crowds Flock to NGV's World-Exclusive Cartier Exhibition — Melbourne's Biggest Cultural Show of 2026",
    "{{VIC_1_SUMMARY}}": "The National Gallery of Victoria's world-exclusive Cartier exhibition — more than 300 jewels, watches and treasures spanning 175 years of the French house — has drawn record winter audiences since opening June 12, with the NGV reporting its strongest weekday attendance figures in a decade. The exhibition runs through October 4 and is the only venue globally showing the full collection in 2026. Combined with Melbourne Museum's concurrent ROME exhibition (over 150 objects from Italian museums) and the Queen Victoria Market's weekly Wednesday Night Markets, Melbourne's winter cultural calendar is keeping foot traffic flowing through the CBD despite the cold — a reminder that Victoria's reputation for cultural programming makes it one of the few Australian cities where winter reliably draws rather than disperses visitors.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 Battery Science · Cell Press June 2026",
    "{{SCI_1_HEADLINE}}": "Chinese Sodium-Ion Battery Matches Tesla's Lithium Performance at a Fraction of the Cost — ScienceDaily, June 21 2026",
    "{{SCI_1_SUMMARY}}": "German researchers testing 120 sodium-ion cells from Chinese manufacturer Hina found their performance and manufacturing quality comparable to Tesla's lithium-ion batteries, according to research published June 21 in Cell Reports Physical Science. The cells charged in approximately 15 minutes — competitive with leading EV batteries — and maintained performance across temperatures from −20°C to 45°C. The battery uses a tabless double-aluminium current collector design that mirrors Tesla's current architecture. Sodium is approximately 40 times more abundant than lithium and a fraction of the cost; if energy density and cold-weather charging can be improved, sodium could become a mainstream alternative to lithium for both electric vehicles and large-scale grid storage. Australia is the world's largest lithium exporter — making any development that challenges lithium's dominance in battery technology directly relevant to the nation's mining and energy export economics.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your FY2026 Job History Is a Sales Asset — How AI Can Turn a Year of Completed Work Into Next Year's Best Business Credential",
    "{{INSIGHT_BODY}}": "Every job you completed between July 1, 2025 and June 30, 2026 is evidence of what your business can do — specific work types, project scale, complexity handled, repeat clients, problems solved, outcomes delivered. Most trades operators file that history and move on. The smarter move — especially at end of financial year when you're already reviewing the books — is to give your job list to AI and ask it to extract your strongest case study material. From a completed job log or invoice history, a language model like Claude can identify the jobs with the best narrative (complex scope, on-time delivery, satisfied repeat client), generate a short case study paragraph for each, draft a capability statement for your trade and suburb, and produce a template for a testimonial request to your best three clients. This process takes about an hour on a weeknight and produces material usable in every quote, tender submission and new-client conversation in FY2027. The difference between winning and losing a commercial quote often comes down to who presents the most credible prior work history — and AI can now help any small Carrum Downs operator match the polish of a larger firm in that presentation.",

    # Fun Facts
    "{{FACT_1}}": "The world's first commercial franchise system wasn't McDonald's or KFC — it was sewing machine company Singer, which in the 1850s developed a network of independently licensed dealers who paid for the right to use the Singer brand, method and sales territory. The modern concept of franchising — paying to operate under a proven business model — traces directly to Singer's solution for distributing complex consumer machinery across a country without a national retail chain.",

    "{{FACT_2}}": "Lightning does strike the same place twice — in fact, repeatedly. The Empire State Building is struck by lightning approximately 20 to 25 times per year. Tall structures naturally attract multiple strikes because they provide the shortest conductive path between storm clouds and earth, drawing repeated strikes across successive storms. The folk belief that \"lightning never strikes twice in the same place\" is one of the most thoroughly disproved ideas in everyday meteorology.",

    "{{FACT_3}}": "Worcestershire sauce was invented by accident. In 1837, chemists John Wheeley Lea and William Perrins of Worcester, England, were commissioned to recreate an Indian recipe from traveller Lord Marcus Sandys — the result was so foul when freshly made that it was moved to a cellar and forgotten. When rediscovered roughly two years later, fermentation had transformed it into something extraordinary. The sauce has been manufactured continuously in Worcester ever since.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the structural engineer refuse to take a holiday?",
    "{{JOKE_PUNCHLINE}}": "He was always worried everything would fall apart without him.",

    # Closing
    "{{CLOSING_QUOTE}}": "“You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose.”",
    "{{CLOSING_ATTR}}": "— Dr. Seuss",
    "{{CLOSING_MESSAGE}}": "It's Monday June 22 — the first working day after the winter solstice, which means Melbourne has turned the corner and will pick up a minute or two of daylight every day from here through to December. Wet start to the week today with showers through the morning, clearing Tuesday before more showers Wednesday. Eight days until the July 1 triple hit: minimum wage up, payday super starts, fuel excise returns. This week is the last practical window to get your payroll, rate cards and SBSCH transition sorted before the costs land. Automate 2026 opens in Chicago today — Google's Intrinsic kicking off with their pitch on AI-native robot programming. The Socceroos play Paraguay in a must-win on Wednesday morning at 9am — Federation Square will be screening it. Steer yourself in the right direction, Liall. Have a good week.",
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
