#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 04 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Mon 4 May (BOM)
    "{{WEATHER_1}}": "Mon 4 May · Partly cloudy, PM showers · 20°C",
    "{{WEATHER_2}}": "Tue 5 May · Showers likely · 18°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Wed 6 May · Cloudy, showers · 19°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "Thu 7 May · Cold front, showers · 14°C",
    "{{WEATHER_5}}": "Fri 8 May · Cold &amp; gusty · 13°C",
    "{{WEATHER_ALERT}}": "⚠ Cold front Thu–Fri · Alpine snow",

    # World
    "{{WORLD_1_FLAG}}": "🌐 MIDDLE EAST · CONFLICT",
    "{{WORLD_1_HEADLINE}}": "Iran Tables 14-Point Counter-Proposal as US-Iran Stalemate Threatens Prolonged Oil Crisis",
    "{{WORLD_1_SUMMARY}}": "Iran has formally submitted a 14-point counter-proposal to American ceasefire terms, but with Washington signalling it can endure a long stand-off and Tehran matching that rhetoric, hopes for a rapid resolution have dimmed. Before the conflict, roughly 3,000 vessels per month transited the Strait of Hormuz — in March just 154 did. Analysts now warn both sides are using negotiations as a signalling exercise rather than a genuine peace process, keeping global oil supply disrupted indefinitely.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/5/2/iran-war-whats-happening-on-day-64-as-trump-rejects-tehrans-proposal",

    "{{WORLD_2_FLAG}}": "🇲🇲 MYANMAR",
    "{{WORLD_2_HEADLINE}}": "\"Moving Her Is Not Freeing Her\" — Suu Kyi's Son Rejects Myanmar Junta's House Arrest Claim",
    "{{WORLD_2_SUMMARY}}": "Kim Aris, son of imprisoned former Myanmar leader Aung San Suu Kyi, told NPR on Sunday he cannot independently confirm the military junta's claim that his 80-year-old mother has been moved from prison to house arrest after more than five years. \"She remains a hostage, cut off from the world,\" he said. Human rights groups called the move a PR exercise designed to rehabilitate the junta's image following a prisoner amnesty tied to a Buddhist holiday — and noted she still faces more than 13 years of her politically motivated sentence.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/05/03/nx-s1-5808875/aung-san-suu-kyi-myanmar-son-house-arrest",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 ECONOMICS · RBA",
    "{{ECON_1_HEADLINE}}": "RBA Board Meets Today — Markets Pricing 70% Chance of Rate Hike to 4.35% Tomorrow",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank of Australia's monetary policy board convened this morning for its May 4–5 meeting, with Governor Michele Bullock set to announce the cash rate decision at 2:30pm AEST tomorrow. Inflation running at 4.6% — the highest since September 2023 — has pushed market pricing to a 70–75% probability of a 25bp hike. Economists calculate a further rise would add an estimated $5,000–$10,000 per year to the operating costs of a typical $2M-revenue small business.",
    "{{ECON_1_URL}}": "https://www.canstar.com.au/news/what-to-expect-from-the-rba-in-may-2026/",

    "{{ECON_2_FLAG}}": "⛽ FUEL · SMALL BUSINESS",
    "{{ECON_2_HEADLINE}}": "Federal Fuel Excise Cut Expires June 30 — Trades Operators Urged to Plan for Price Snapback",
    "{{ECON_2_SUMMARY}}": "The federal government's temporary 50% fuel excise cut expires June 30, 2026. With peace talks stalled and Hormuz shipping still disrupted, there is no guarantee prices will ease before the snapback. The Heavy Vehicle Industry Association is urging fleet operators to explore contract fuel pricing before the cut expires. For trades businesses quoting jobs that run past July, building in a fuel cost increase now is prudent risk management.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💻 AI · ENTERPRISE",
    "{{TECH_1_HEADLINE}}": "Back-Office AI Officially Moves From Pilot to Production — Enterprise Platforms Confirm Live Deployments",
    "{{TECH_1_SUMMARY}}": "A May 3 industry analysis tracking enterprise AI adoption confirms that AI-powered back-office automation — covering invoicing, HR, compliance reporting, and supplier management — has transitioned from proof-of-concept to live production at platforms including Salesforce and Workday. AI use across HR tasks alone reached 43% of companies surveyed in 2026, up from 26% two years ago. For small trades operators, the timing signal is clear: tools Fortune 500 companies are running at scale today typically reach the SME market within 12–18 months at a fraction of the enterprise price.",
    "{{TECH_1_URL}}": "https://asanify.com/blog/news/ai-back-office-automation-may-3-2026/",

    "{{TECH_2_FLAG}}": "📈 AI · MARKETS",
    "{{TECH_2_HEADLINE}}": "Goldman Sachs Calls AI Software Sell-Off \"Overdone\" as Enterprise Adoption Data Beats Estimates",
    "{{TECH_2_SUMMARY}}": "Goldman Sachs analysts issued a note on Sunday maintaining overweight positions across AI-exposed software stocks, calling the recent market pullback \"overdone\" given that Q1 2026 earnings consistently showed enterprise AI adoption beating analyst estimates. The bank highlighted strong quarter-on-quarter growth in AI credit consumption at platforms including Atlassian (20% month-on-month) and Figma as evidence corporate AI usage is accelerating rather than plateauing. For anyone watching where AI investment is heading: enterprise adoption is real, it is accelerating, and it is pulling the broader software market with it.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "⚙️ ROBOTICS · SIMULATION",
    "{{ROBOT_1_HEADLINE}}": "$8.5M Startup Antioch Bets Cloud Simulation Will Break the Deadlock Slowing Industrial Robot Deployment",
    "{{ROBOT_1_SUMMARY}}": "New York-based Antioch, founded in 2025, has raised $8.5 million to build a cloud platform that lets robotics teams develop, train, and evaluate autonomous systems entirely in simulation — removing the need for costly, time-consuming real-world testing. Backers include A*, Category Ventures, and MaC Venture Capital. The company argues over-reliance on physical testing is the single biggest bottleneck slowing industrial automation adoption, drawing parallels to how cloud computing transformed software development by making iteration cheap and fast.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/05/03/antioch-raises-8-5-million-to-accelerate-simulation-based-development-of-autonomous-systems/101171/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Man Charged With Murder of Five-Year-Old Kumanjayi in NT After Death Sparked Riots",
    "{{AUS_1_SUMMARY}}": "NT Police have charged Jefferson Lewis, 47, with the murder of five-year-old Kumanjayi in Alice Springs — a death that sparked violent community protests and clashes with police last week. Lewis also faces two additional charges. The case has reignited national debate about child safety in remote Indigenous communities and the adequacy of youth justice policy in the Northern Territory.",
    "{{AUS_1_URL}}": "https://www.aljazeera.com/news/2026/5/3/man-charged-over-murder-of-australian-indigenous-girl-that-sparked-riots",

    "{{AUS_2_HEADLINE}}": "Australia's Student Visa Crackdown Hits Record Refusal Rates — Universities Warn of Funding Crisis",
    "{{AUS_2_SUMMARY}}": "From May 1, sweeping new student visa reforms — a tougher Genuine Student test, graduate visa age cap cut from 50 to 35, and mandatory savings of AUD $31,200 — have dramatically tightened the international student pathway. Refusal rates from South Asia are at record highs and a national annual cap of 295,000 approvals means many eligible applicants are simply turned away. Smaller universities that rely heavily on international fee revenue are warning of a serious funding squeeze.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Liberals Retain Nepean Seat — One Nation's 24.7% Primary Vote Puts State Parties on Notice",
    "{{VIC_1_SUMMARY}}": "Liberal candidate Anthony Marsh won the Nepean by-election on Saturday with 63.5% on a two-candidate preferred count, retaining the seat for his party. But it was One Nation's strong 24.7% primary vote that dominated post-election analysis, with strategists warning it signals broader discontent — particularly in outer-suburban electorates — that could reshape the upcoming Victorian state election.",

    # Science
    "{{SCI_1_FLAG}}": "🌍 GEOSCIENCE",
    "{{SCI_1_HEADLINE}}": "\"Double Quake\" Scenario: Researchers Find San Andreas and Cascadia Faults Can Rupture in Tandem",
    "{{SCI_1_SUMMARY}}": "Oregon State University scientists, publishing in the journal Geosphere, have found sediment evidence that the Cascadia Subduction Zone and the Northern San Andreas Fault periodically synchronise — with at least three events in the past 1,500 years where both fault systems ruptured within minutes to hours of each other. A simultaneous rupture would place San Francisco, Portland, Seattle, and Vancouver all in emergency status at once, overwhelming any planned response capacity. The study received wide coverage on May 2, 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI Can Write Your SWMS in 60 Seconds — But You Still Need to Sign It Off",
    "{{INSIGHT_BODY}}": "For any trade working with hazardous processes — coatings, blasting, confined spaces, heights — Safe Work Method Statements (SWMS) and Job Safety Analyses (JSAs) are compulsory before starting higher-risk work. In practice, these documents take 30–60 minutes to write properly from scratch, and many operators either reuse old templates (creating legal exposure) or cut corners on time-pressed jobs. AI tools like Claude, ChatGPT, or purpose-built platforms such as SafetyDocs and ProcedureFlow can now generate a detailed, task-specific first-draft SWMS in under a minute once you describe the scope and key hazards. The output covers standard risk categories, control measures, and PPE requirements — enough to give your supervisor a solid base to review rather than a blank page to fill. On a multi-job week, that can save two to four hours of admin, improve your compliance trail, and give you a defensible audit record if anything goes wrong on site. The catch: no AI can do your site assessment or take legal responsibility. But for getting the document structure right quickly, it has become genuinely useful.",

    # Fun Facts
    "{{FACT_1}}": "The platypus hunts with its eyes, ears, and nostrils completely sealed — navigating underwater using a bill packed with electroreceptors that detect the tiny electrical fields generated by its prey's muscle contractions. It is one of only a handful of mammals on Earth with this electroreception ability, and the only venomous one.",
    "{{FACT_2}}": "The word \"concrete\" traces to the Latin \"concretus\" meaning \"condensed\" or \"hardened.\" Roman engineers made a superior hydraulic concrete from volcanic ash (pozzolana), lime, and seawater — structures built with it two thousand years ago, including the Pantheon's unreinforced dome, still stand today, while many 20th-century Portland cement buildings are already crumbling. Materials scientists are still reverse-engineering exactly why it lasts.",
    "{{FACT_3}}": "Steel is essentially iron with a very precise amount of carbon: 0.2%–2.1% by weight. Too little carbon and you get soft wrought iron; too much and you get brittle cast iron. The entire modern built world — bridges, buildings, ships, tools — rests on the ability to control that margin down to a fraction of a per cent.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the gasfitter get promoted so quickly?",
    "{{JOKE_PUNCHLINE}}": "He always worked well under pressure.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Whether you think you can, or you think you can't — you're right.\"",
    "{{CLOSING_ATTR}}": "Henry Ford",
    "{{CLOSING_MESSAGE}}": "Monday morning in Carrum Downs — a decent 20°C today with showers possible late afternoon. Make the most of the dry start: Thursday brings a Southern Ocean cold front pushing temperatures down to 14°C with strong winds and Alpine snow, making outdoor coatings and blasting work difficult. Two big decisions land tomorrow: the RBA cash rate announcement at 2:30pm AEST, and the Victorian State Budget. Worth keeping Tuesday afternoon clear to assess what both mean for your costs and pipeline.",
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
