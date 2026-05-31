#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 01 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 1 Jun (BOM/AccuWeather forecast)
    "{{WEATHER_1}}": "MON 1 · ⛅ Partly cloudy · 8–14°C",
    "{{WEATHER_2}}": "TUE 2 · 🌧 Showers · 9–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 3 · ☁ Cloudy · 8–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "THU 4 · ⛅ Mostly cloudy · 9–14°C",
    "{{WEATHER_5}}": "FRI 5 · ⛅ Clearing · 9–15°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS EXPECTED TUESDAY",

    # World
    "{{WORLD_1_FLAG}}": "🌏 MIDDLE EAST · HORMUZ",
    "{{WORLD_1_HEADLINE}}": "US and Iran Agree 60-Day Ceasefire Extension as Strait of Hormuz Deal Framework Takes Shape",
    "{{WORLD_1_SUMMARY}}": "The United States and Iran have entered a 60-day ceasefire extension framework as both sides work toward a final agreement to formally end the 2026 Iran war. The Strait of Hormuz — through which roughly 20% of global oil trade passes — is being progressively de-mined under US Navy escort, with President Trump saying talks are 'largely negotiated.' The fragile truce has been punctuated by skirmishes, and US forces struck Iranian drone positions near Bandar Abbas last week after detecting preparations for fresh attacks. For Australian businesses, the Hormuz conflict has been the primary driver of the fuel crisis that pushed CPI to 4.6% and triggered the temporary fuel excise cut. A durable deal would ease oil price pressure; a breakdown would reinstate the oil shock immediately.",
    "{{WORLD_1_URL}}": "https://en.wikipedia.org/wiki/2026_Iran_war_ceasefire",

    "{{WORLD_2_FLAG}}": "🇺🇦 UKRAINE · SECURITY",
    "{{WORLD_2_HEADLINE}}": "Zelenskyy: Ukraine Intelligence Confirms Russia Planning Major Drone and Missile Barrage",
    "{{WORLD_2_SUMMARY}}": "Ukrainian President Volodymyr Zelenskyy has warned that Kyiv has received credible intelligence indicating Russia is preparing a large coordinated drone and missile assault. Ukraine has issued civilian warnings and is requesting expedited Western air defence deliveries. The announcement comes as the frontline situation remains under pressure ahead of summer, and as European and US officials weigh the scale of continued military support.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 INTEREST RATES",
    "{{ECON_1_HEADLINE}}": "RBA Meets June 16 as CPI Hits 4.6% — Westpac Forecasts Two More Rate Hikes by August",
    "{{ECON_1_SUMMARY}}": "Australia's annual inflation rate has climbed to 4.6% — its highest since September 2023 — with fuel prices and supply chain disruption the primary drivers, tied directly to the US-Iran conflict around the Strait of Hormuz. The RBA board meets in 16 days on June 16, with the cash rate currently sitting at 4.35% after three consecutive hikes this year. CBA, ANZ and NAB are forecasting a hold; Westpac economists are predicting a further 25bp rise, with another possible in August, lifting the rate to 4.85%. Small trades businesses carrying variable-rate finance, equipment loans, or commercial mortgages should model the cost impact of a potential mid-June hike before quoting on larger jobs.",
    "{{ECON_1_URL}}": "https://www.aussie.com.au/insights/news/expert-predictions-rba-rates/",

    "{{ECON_2_FLAG}}": "💼 JULY 1 · COST CRUNCH",
    "{{ECON_2_HEADLINE}}": "July 1 Double Hit: Minimum Wage Rise and Fuel Excise Snap-Back Land on Australian Businesses Simultaneously",
    "{{ECON_2_SUMMARY}}": "Two cost increases arrive on the same day for Australian small businesses: from July 1, the national minimum wage rises (lifting modern award pay points across trades and construction), and the fuel excise reverts from 26.3 cents to 52.6 cents per litre — adding approximately 28.9c/L at the pump once GST is applied. For a trades operator running two employees and three vehicles, the combined weekly cost base jumps materially from that date. Jobs quoted today using current pump prices and current award rates will be underpriced for work scheduled in July or later.",
    "{{ECON_2_URL}}": "",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · ANTHROPIC",
    "{{TECH_1_HEADLINE}}": "Anthropic's Claude Opus 4.8 Sets New AI Coding Benchmark With 1M Token Context and Parallel Agent Workflows",
    "{{TECH_1_SUMMARY}}": "Released last week, Claude Opus 4.8 scores 69.2% on SWE-Bench Pro — outperforming GPT-5.5 and Gemini 3.1 Pro — with a default one-million-token context window across major platforms. The headline feature is 'dynamic workflows': a single session can now orchestrate hundreds of parallel AI sub-agents, enabling automation of large-scale tasks such as codebase-wide migrations or multi-document research across hundreds of thousands of lines. An effort control slider lets users dial Claude's reasoning depth to trade speed for quality. For business users, the practical implication is AI that can handle more complex, multi-step projects without human handoffs at each stage.",
    "{{TECH_1_URL}}": "https://www.anthropic.com/news/claude-opus-4-8",

    "{{TECH_2_FLAG}}": "📊 AI · BUSINESS RESULTS",
    "{{TECH_2_HEADLINE}}": "AI-Referred Traffic to Retail Sites Up 393% in Q1 2026 — and Converting 42% Better Than Any Other Channel",
    "{{TECH_2_SUMMARY}}": "New data from retail analytics firms shows AI-referred visitors surged 393% year-over-year in Q1 2026 and converted to purchases at a rate 42% higher than all other traffic sources. Analysts say 2026 is the year AI definitively moves from hype to measurable revenue driver — with the sharpest gains concentrated in businesses that integrated AI into actual customer workflows, not just marketing copy. The pattern applies across sectors: the gap between AI-integrated operators and those still waiting to start is widening every quarter.",
    "{{TECH_2_URL}}": "",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳 CHINA · MANUFACTURING",
    "{{ROBOT_1_HEADLINE}}": "AGIBOT's G2 Humanoids Go Live on Chinese Electronics Factory Line — Running Tablet Tests Autonomously",
    "{{ROBOT_1_SUMMARY}}": "AGIBOT's G2 humanoid robots are now running automated tablet testing directly on the live production line at Longcheer Technology's manufacturing facility in China — what the company describes as a world first for humanoid deployment in consumer electronics production. The robots handle functional testing tasks previously performed by human technicians, operating within the existing factory setup without line modification. AGIBOT has shipped more than 10,000 humanoid units to date and has declared 2026 its 'Deployment Year One,' with targets for 100+ deployed robots across automotive, semiconductor, and energy sectors by Q3. The company holds a 39% global market share in humanoid shipments.",
    "{{ROBOT_1_URL}}": "https://interestingengineering.com/ai-robotics/agibot-g2-humanoid-robots-live-production-line",

    # Australia
    "{{AUS_1_HEADLINE}}": "AUKUS Shake-Up: Australia to Buy All Three Nuclear Submarines Second-Hand From the US",
    "{{AUS_1_SUMMARY}}": "Defence Minister Richard Marles has confirmed Australia will acquire three used Block IV Virginia-class nuclear submarines under a revised AUKUS arrangement announced at the Shangri-La Dialogue in Singapore. The change replaces the original plan for a mix of used and new vessels, with the joint US-UK-Australia statement citing simplified supply chain management, maintenance efficiencies, and significant cost savings. Australia will also build five SSN-AUKUS submarines locally from the late 2030s. The revision is expected to save Australia billions in procurement and long-term maintenance costs over the life of the programme.",
    "{{AUS_1_URL}}": "https://www.anews.com.tr/world/2026/05/31/australia-will-purchase-3-second-hand-nuclear-powered-submarines-under-revised-aukus-deal",

    "{{AUS_2_HEADLINE}}": "Australia's CPI Hits 4.6% as Hormuz Conflict Drives Fuel and Supply Chain Costs Higher",
    "{{AUS_2_SUMMARY}}": "Australia's annual CPI has climbed to 4.6% — its highest level since September 2023 — with fuel prices and supply chain disruption tied to the US-Iran conflict around the Strait of Hormuz the primary drivers. Freight costs, materials, and energy bills have all risen sharply across the economy. Small business operators are caught in a compound squeeze: the temporary fuel excise cut provides partial relief until June 30, but underlying inflation dynamics are not expected to ease quickly even if a Hormuz deal is finalised.",
    "{{AUS_2_URL}}": "",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Knife Crime Shows First Signs of Decline One Year After Australia's First Machete Ban",
    "{{VIC_1_SUMMARY}}": "New data confirms knife-related offences are beginning to ease across Victoria, one year after the government announced the ban on machetes — and nine months since it took effect in September 2025. Officers seized nearly 22,000 edged weapons across the state in 2025, averaging 48 per day, while 18,031 machetes were surrendered during the pre-ban amnesty. A Victorian government spokesperson acknowledged crime rates remained too high but said the latest enforcement reforms were working. Victoria remains the only Australian state to completely prohibit machetes, with possession carrying penalties of up to two years imprisonment or $47,000 fines.",
    "{{VIC_1_URL}}": "",

    # Science
    "{{SCI_1_FLAG}}": "🕊 BIOLOGY · NAVIGATION",
    "{{SCI_1_HEADLINE}}": "Homing Pigeons Navigate Via Iron-Rich Immune Cells in Their Livers — Scientists Call It 'Mind-Blowing'",
    "{{SCI_1_SUMMARY}}": "An international team of German researchers has discovered that homing pigeons navigate using iron-rich macrophages — immune cells normally associated with breaking down red blood cells — located in the liver. The iron makes these cells superparamagnetic, allowing them to respond to shifts in Earth's magnetic field. The cells sit adjacent to nerve fibres, suggesting magnetic signals travel directly to the brain during flight. In experiments, removing the macrophages caused pigeons to lose directional ability on overcast days while still navigating successfully using solar cues when the sky was clear — confirming two completely independent navigation systems operating in parallel. Published in ScienceDaily on May 29, the finding overturns decades of assumptions about where animal magnetic sensing is located.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "30 Days to the New Financial Year — How AI Can Lock In Smarter Rates for FY2027 Before the Costs Hit",
    "{{INSIGHT_BODY}}": "The next 30 days are probably the most financially consequential stretch of the year for a small trades business. On July 1, the fuel excise snaps back — adding roughly 29 cents per litre to diesel overnight. The minimum wage rises the same day. And if Westpac's economists are right, the RBA may add another 25 basis points on June 16, lifting variable-rate finance costs from mid-July. Most operators will absorb all three quietly, chip away at the margin they've spent twelve months rebuilding, and try not to notice. The smarter move is to spend 60 to 90 minutes this week with an AI tool — Claude, ChatGPT, whichever you're comfortable with — and model what your revised rate card needs to look like by July 1. Feed it your current hourly rate, your average weekly diesel spend, your labour costs, and your finance repayments. Ask it to calculate the break-even impact of each July change and propose a revised rate. You don't have to quote it to every customer tomorrow. But knowing the number — before your margin gets quietly eaten — is the entire game.",

    # Fun Facts
    "{{FACT_1}}": "The original London Bridge was sold in 1968 for $2.46 million to an American businessman who had it dismantled stone by stone and shipped to Lake Havasu City, Arizona, where it was fully reassembled and opened in 1971. The buyer, Robert McCulloch, was widely reported to have believed he was purchasing the far more iconic Tower Bridge. He insisted he knew exactly what he was buying — but the story persists, and the bridge still stands in the Arizona desert.",

    "{{FACT_2}}": "A woodpecker drills at up to 20 pecks per second — an impact that would cause a concussion in any other animal. Its brain is protected by three overlapping adaptations: a spongy, shock-absorbing skull that distributes force; highly compressed neck muscles acting as suspension; and a tongue so long it wraps entirely around the back of the skull like a biological seatbelt, cushioning each strike before it reaches the brain. Engineers have studied the design to improve helmet and protective equipment technology.",

    "{{FACT_3}}": "The United States has never officially adopted the metric system — making it one of only three countries in the world, alongside Myanmar and Liberia, that have not done so. A Metric Conversion Act passed in 1975, but voluntary compliance only. The story traces partly to 1793, when a French vessel carrying the official metric reference standards to the US sank en route. By the time replacement standards arrived, the political moment had passed — and the imperial system was too deeply embedded to shift.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the landscaper keep getting promoted?",
    "{{JOKE_PUNCHLINE}}": "Because every time there was a problem, he just mulched it over.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Great things are done by a series of small things brought together.”",
    "{{CLOSING_ATTR}}": "— Vincent van Gogh",
    "{{CLOSING_MESSAGE}}": "Monday, 1 June 2026 — the first day of meteorological winter in Melbourne, and exactly 30 days until the end of the financial year. Half-price public transport kicks in across Victoria from today, so if any of your team commutes by PT the tap-on cost has halved. The bigger number to keep in mind: July 1 now brings a triple cost event — fuel excise snap-back, minimum wage rise, and potentially another RBA hike on the 16th. Cold mornings ahead, and some real financial decisions to make before the month is out. Get the rate card right before the crunch hits. Have a good week, Liall.",
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
