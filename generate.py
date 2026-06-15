#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 16 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 16 Jun
    # Showers and northerly winds today; heavy rain Thu; easing Fri–Sat
    "{{WEATHER_1}}": "TUE 16 · 🌧 Showers · 18°C",
    "{{WEATHER_2}}": "WED 17 · 🌧 Shower risk · 13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 18 · 🌧 Heavy showers · 13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 19 · ⛅ Easing · 12°C",
    "{{WEATHER_5}}": "SAT 20 · 🌤 Clearing · 14°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS & N'LY WINDS · HEAVY RAIN THU",

    # World
    "{{WORLD_1_FLAG}}": "🌐 Middle East · Hormuz",
    "{{WORLD_1_HEADLINE}}": "US-Iran Framework Deal Confirmed — Formal Signing Friday in Switzerland as Hormuz Blockade Lifts",
    "{{WORLD_1_SUMMARY}}": "The United States and Iran have confirmed a landmark agreement to end their military conflict and reopen the Strait of Hormuz — through which roughly 20% of the world's traded oil flows. Pakistan's mediation secured a formal signing ceremony scheduled for Friday in Switzerland. Oil prices fell more than $4 a barrel on the announcement and global markets surged. The deal also includes Iran shipping its enriched uranium stocks out of the country. A successful Hormuz reopening could provide meaningful relief on global crude prices heading into July — directly relevant for any Australian business running a diesel fleet.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/06/15/nx-s1-5858590/us-iran-deal-updates",

    "{{WORLD_2_FLAG}}": "🌐 G7 · France",
    "{{WORLD_2_HEADLINE}}": "OpenAI, Anthropic and Google DeepMind CEOs Appear Before G7 World Leaders Together — A Historic First",
    "{{WORLD_2_SUMMARY}}": "Sam Altman, Dario Amodei, and Demis Hassabis are all at the G7 Summit in France this week — June 15–17 — marking the first time the three leaders of rival frontier AI companies have simultaneously addressed heads of government. Topics include AI compute as national security infrastructure, cross-border data sovereignty rules, and coordinated approaches to AI safety oversight. The moment signals a shift that has been building all year: frontier AI is no longer purely a technology story — it is a geopolitical one, with the policy decisions made at summits like this shaping the regulatory environment every Australian business using AI will operate in.",
    "{{WORLD_2_URL}}": "https://aiweekly.co/ai-news-today/anthropic-news",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 RBA · Decision Day",
    "{{ECON_1_HEADLINE}}": "RBA Announces June Interest Rate Decision at 2:30pm AEST Today — Hold at 4.35% Expected",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank of Australia delivers its June monetary policy decision at 2:30pm AEST today following two days of board deliberation. The cash rate sits at 4.35% after three consecutive hikes in 2026. Major banks broadly expect a hold, though CBA and NAB have flagged an August cut as possible if the Iran deal stabilises oil prices and June inflation data comes in subdued. For trades businesses carrying equipment finance, overdrafts, or variable commercial loans, today's accompanying statement will be the clearest forward signal yet on when rate relief is coming — and by how much.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/monetary-policy/int-rate-decisions/",

    "{{ECON_2_FLAG}}": "⛽ Fuel · July 1",
    "{{ECON_2_HEADLINE}}": "Iran Deal Could Soften July Fuel Pain — But Australia's Excise Cut Still Expires June 30 Regardless",
    "{{ECON_2_SUMMARY}}": "The US-Iran Hormuz agreement has already pushed crude oil down more than $4 a barrel, and further relief could follow if the deal holds through Friday's signing. But for Australian tradies, the 32-cents-per-litre fuel excise reduction expires on June 30 regardless of what crude oil does internationally. Diesel currently averages around 214 cents per litre nationally; the July 1 bowser price will reflect both crude movements and the excise reversal. The net effect is uncertain, but the baseline risk is a price rise. Any job quoted at today's fuel rates for July or later still needs a buffer.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🌐 G7 · AI Policy",
    "{{TECH_1_HEADLINE}}": "All Three Rival AI Lab CEOs at G7 Together — Governments Formally Treating AI as National Infrastructure",
    "{{TECH_1_SUMMARY}}": "The G7 AI governance discussions in France this week feature an unprecedented lineup: the heads of OpenAI, Anthropic, and Google DeepMind simultaneously addressing the world's major governments for the first time. Key issues on the table include AI compute access as a national security asset, data-localisation rules that will determine who can build and sell into regulated markets, and coordinated safety oversight frameworks. The practical implication for Australian business owners: the rules governing which AI tools you can use, how your data is stored, and what liability looks like for AI-generated outputs are now being drafted at the highest political level. Worth watching.",
    "{{TECH_1_URL}}": "https://aiweekly.co/ai-news-today/anthropic-news",

    "{{TECH_2_FLAG}}": "💼 Agentic AI · SMB",
    "{{TECH_2_HEADLINE}}": "Agentic AI Has Crossed Into SMB Territory — Workflow Automation That Saves 12 Hours a Week From $20/Month",
    "{{TECH_2_SUMMARY}}": "Agentic AI tools — systems that complete multi-step tasks without human prompting at each step — are now genuinely accessible for small businesses in 2026. Early adopters report saving 12 or more hours per week once agents are properly integrated into workflows, handling tasks like lead response, document summarisation, CRM updates, invoice follow-up, and customer FAQ routing. The key lesson from real deployments: start internal, not customer-facing. Automate your meeting notes and job record summaries before you automate anything a client sees. The entry cost is now under $20 per month per agent.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 Industrial · Automate 2026",
    "{{ROBOT_1_HEADLINE}}": "Teradyne Robotics Unveils Production-Ready Physical AI for Factory Floors at Automate 2026",
    "{{ROBOT_1_SUMMARY}}": "Teradyne Robotics announced on June 15 that it is showcasing production-ready physical AI automation at Automate 2026 in Chicago, running June 22–25. The company — which owns Universal Robots collaborative arms and MiR autonomous mobile robots — is demonstrating AI-powered systems capable of adaptive assembly, vision-guided picking, and autonomous material handling with no specialist programming required. The emphasis on 'production-ready' marks a meaningful shift: physical AI for the factory floor is no longer a research demo. It is being sold as a deployable product to real facilities right now. What enters Tier 1 industrial today typically reaches the trades and industrial services sector within five to seven years.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/06/15/teradyne-robotics-unveils-production-ready-physical-ai-applications-at-automate-2026/102536/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Stun Turkey 2-0 in World Cup Opener — Irankunda Youngest-Ever Australian World Cup Scorer",
    "{{AUS_1_SUMMARY}}": "Australia opened their 2026 FIFA World Cup campaign with a commanding 2-0 win over Türkiye at BC Place in Vancouver on June 14 — one of the Socceroos' strongest World Cup performances in decades. Nestory Irankunda struck in the 27th minute to become Australia's youngest-ever World Cup goal-scorer, with Connor Metcalfe sealing the result in the 75th. Goalkeeper Patrick Beach made eight saves against a Turkish side that dominated possession (72%) and registered 30 shots. Australia faces hosts USA on June 20 in Seattle — a win would almost guarantee a round of 16 spot in Group D.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/live-blog/australia-vs-turkiye-world-cup-live-score-updates/e7r7yd3iz",

    "{{AUS_2_HEADLINE}}": "NDIS Minister Defends Plan to Cut 160,000 Participants as Disability Advocates Warn of Life-Threatening Impact",
    "{{AUS_2_SUMMARY}}": "Health Minister Mark Butler is defending reforms targeting a reduction of NDIS participant numbers from 760,000 to around 600,000 by 2030, redirecting under-8s with developmental delays to a new Thriving Kids programme starting July 1. Senate inquiry hearings have drawn fierce opposition, with disability advocates and specialist medical associations warning the eligibility changes are life-threatening for people with complex needs. The government argues scheme growth — adding around 40,000 participants per year at rising average plan costs of $31,000 — is fiscally unsustainable. The inquiry continues this week.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Metro Tunnel Works Bring Rolling Weekend Train Suspensions to Melbourne's Western and South-Western Lines",
    "{{VIC_1_SUMMARY}}": "A series of weekend train service suspensions affecting Sunbury, Melton, Ballarat, Newport, Point Cook, Werribee, and Wyndham Vale lines is underway as Metro Tunnel construction enters a critical phase. Replacement buses are running but journey times are significantly longer. The programme is part of Victoria's $7.3 billion transport infrastructure push including level crossing removals and the Suburban Rail Loop. Tradespeople scheduling crew movements on the Werribee or Wyndham Vale corridors should check Metro Trains Melbourne's website before booking Saturday or Sunday travel.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 Ecology · Science",
    "{{SCI_1_HEADLINE}}": "Scientists Map Earth's Underground Fungal Superhighway for the First Time — Networks Stretch 110 Quadrillion Kilometres",
    "{{SCI_1_SUMMARY}}": "Researchers have published the first complete global map of Earth's mycorrhizal fungal networks — the vast underground system connecting plant roots to soil nutrients. Published in Science on June 14, the study estimates these networks collectively stretch 110 quadrillion kilometres and move approximately 4 billion tonnes of carbon dioxide into soils each year. Around 70 percent of all plant species rely on this underground exchange — meaning most of the world's trees, crops, and grasses sustaining life above ground are plugged into a biological internet that no one had fully mapped until now. The discovery has significant implications for soil carbon sequestration and understanding ecosystem resilience under climate stress.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Today's RBA Call Is a Prompt, Not a Verdict — AI Can Stress-Test Your Loan Exposure in Five Minutes",
    "{{INSIGHT_BODY}}": "Whether the RBA holds at 4.35% today or signals cuts are coming, the real question for any trades business carrying equipment finance, a line of credit, or an overdraft is: what's my actual annual interest cost, and what does a rate cut save me? Most small operators know their monthly repayment figure but haven't modelled their total debt exposure — or run the numbers on what 25 or 50 basis points lower would actually mean for cash flow. AI closes that gap in minutes. Paste your current loan balances, rates, and remaining terms into any capable AI tool — Claude, ChatGPT, or equivalent — and ask it to build a scenario table: annual interest at current rates, at minus 25bp, and at minus 50bp. Then ask it which facilities might benefit from switching to fixed before cuts arrive, and whether your current repayment schedule is optimised given your cash flow cycle. The whole exercise takes five minutes. You will very likely discover a number you didn't know — and that number tells you exactly how much today's RBA announcement matters to your bottom line.",

    # Fun Facts
    "{{FACT_1}}": "The total weight of all ants on Earth is roughly comparable to the total weight of all humans. Scientists estimate approximately 20 quadrillion ants exist at any given time, collectively weighing around 12 million tonnes — roughly equal to humanity's combined mass. Because individual ants weigh as little as one milligram, this staggering number is effectively invisible: the average suburban backyard contains tens of thousands of individual ants beneath the lawn.",

    "{{FACT_2}}": "The Great Dividing Range running along eastern Australia extends approximately 3,500 kilometres — roughly the flying distance from Melbourne to Singapore — yet its highest point, Mount Kosciuszko, reaches only 2,228 metres. The same elevation would rank as a moderate foothill in the Swiss Alps, where over 70 peaks exceed Kosciuszko's height. Despite this, the range acts as the continent's water divide, separating rivers that drain east to the Pacific from those that flow inland toward the Murray-Darling system.",

    "{{FACT_3}}": "Nintendo deliberately disguised the NES as a toy for its 1985 North American launch because the US video game market had collapsed in 1983, losing over US$3 billion in retail value in two years. Major retailers refused to stock anything described as a 'game console.' Nintendo bundled the system with a plastic toy robot (R.O.B.), called it a 'Control Deck,' and placed it in toy stores as a home entertainment product. The strategy worked: the NES revived an entire industry and went on to sell 61.9 million units worldwide.",

    # Joke
    "{{JOKE_SETUP}}": "Why does the window cleaner always get repeat business?",
    "{{JOKE_PUNCHLINE}}": "His clients can see right through him — and they keep liking what they see.",

    # Closing
    "{{CLOSING_QUOTE}}": "“It is not the mountain we conquer but ourselves.”",
    "{{CLOSING_ATTR}}": "— Sir Edmund Hillary",
    "{{CLOSING_MESSAGE}}": "It's a wet Tuesday in Carrum Downs — showers and northerly winds are in for most of the day, so keep an eye on site access and any weather-sensitive work. The headline event this afternoon is at 2:30pm AEST when the RBA drops its June rate decision. Whatever they say, it sets the tone for borrowing costs heading into the new financial year. Elsewhere, the Iran-Hormuz deal is on track for Friday's signing in Switzerland, which could soften fuel prices before July 1. Two weeks to EOFY, Liall — a rainy Tuesday is a good day to be at a desk running the numbers.",
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
