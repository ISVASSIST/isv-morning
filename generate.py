#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 03 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 3 Jun
    "{{WEATHER_1}}": "WED 3 · ⛅ Part cloudy · 8–14°C",
    "{{WEATHER_2}}": "THU 4 · ☁ Cloudy · 8–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 5 · 🌧 Showers likely · 8–13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 6 · ⛅ Part cloudy · 8–14°C",
    "{{WEATHER_5}}": "SUN 7 · ☁ Overcast · 9–14°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS FROM FRIDAY",

    # World
    "{{WORLD_1_FLAG}}": "🌏 EUROPE · UKRAINE",
    "{{WORLD_1_HEADLINE}}": "Russia Fires 73 Missiles and 656 Drones at Ukraine — 17 Dead in Largest Barrage of 2026",
    "{{WORLD_1_SUMMARY}}": "Russia launched its largest aerial assault of 2026 overnight, firing 73 missiles — including eight hypersonic Zircon weapons — and 656 drones at Ukrainian cities. At least 17 people died across Kyiv, Dnipro and Kharkiv. Ukrainian air defences intercepted 40 missiles and 602 drones, but residential buildings and civilian infrastructure across eight Kyiv districts were damaged. President Zelenskyy called urgently for more Western air defence support.",
    "{{WORLD_1_URL}}": "https://abcnews.com/International/russia-launches-horrific-drone-missile-strikes-ukraine-killing/story?id=133506283",

    "{{WORLD_2_FLAG}}": "🌎 UNITED STATES · LAW",
    "{{WORLD_2_HEADLINE}}": "US Appeals Court Rules Trump's Transgender Military Ban Unconstitutional — Hegseth Vows Supreme Court Fight",
    "{{WORLD_2_SUMMARY}}": "A divided three-judge panel of the DC Circuit Court ruled on June 2 that the Pentagon's policy barring transgender troops from service was designed to 'harm a politically unpopular group' and violated the Constitution. The ruling protects current transgender service members from expulsion but does not allow new recruits to join. Defence Secretary Hegseth immediately signalled an appeal to the Supreme Court.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/06/02/g-s1-125323/pentagon-transgender-troops",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 FUEL · COST OF LIVING",
    "{{ECON_1_HEADLINE}}": "Australia's Fuel Excise Relief Ends June 30 — Prices to Jump ~29c/L Overnight on July 1",
    "{{ECON_1_SUMMARY}}": "The federal government's halved fuel excise — cutting 26.3 cents per litre off petrol and diesel since April 1 — expires in 28 days with no extension announced. Once GST is factored in, pump prices jump by approximately 29 cents per litre overnight on July 1. For trades operators filling multiple diesel tanks weekly, that adds hundreds of dollars in monthly running costs. Any work quoted this week for delivery after June 30 should account for this reset.",
    "{{ECON_1_URL}}": "https://fairworkmate.com.au/blog/fuel-excise-cut-ends-30-june-2026-what-happens-next",

    "{{ECON_2_FLAG}}": "🏭 SMALL BUSINESS · AUSTRALIA",
    "{{ECON_2_HEADLINE}}": "Small Business Input Costs at Record Highs — Energy, Insurance and Wages Squeeze 2026 Margins",
    "{{ECON_2_SUMMARY}}": "Australian industry research finds 40% of small businesses expect 2026 to be worse than last year, with energy prices, insurance premiums and wage pressures all at their highest in a decade. Despite some cautious optimism, SMEs say input cost pressure will remain elevated through the second half of FY26 — particularly hitting operators who have not updated their rate cards since 2024.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · MICROSOFT",
    "{{TECH_1_HEADLINE}}": "Microsoft Build 2026: Persistent AI Agents Now Embedded Across Office 365, Windows and Azure",
    "{{TECH_1_SUMMARY}}": "At its June 2 keynote in San Francisco, Microsoft launched Copilot Agent Mode for Office 365 — persistent AI agents that operate autonomously inside Word, Excel, Teams and Outlook, rolling out to subscribers in late June. Windows Local AI brings on-device agents to NPU-equipped PCs, and Azure AI Foundry now offers enterprise dashboards to manage thousands of deployed AI agents simultaneously. The shift from chatbot to always-on autonomous assistant is now built into the world's most widely used software platform.",
    "{{TECH_1_URL}}": "https://windowsnews.ai/article/build-2026-microsoft-unleashes-ai-agents-across-office-365-windows-and-azure-at-san-francisco-keynot.421349",

    "{{TECH_2_FLAG}}": "💰 AI · IPO",
    "{{TECH_2_HEADLINE}}": "Anthropic Files Confidential IPO at $965 Billion Valuation — First Major AI Lab to Head for Public Markets",
    "{{TECH_2_SUMMARY}}": "Anthropic submitted a confidential S-1 to the US SEC on June 1, targeting an October 2026 listing. The filing follows a $65 billion Series H that pushed its valuation to $965 billion — surpassing OpenAI's $852 billion. Annual revenue has surged from $10 billion to a $47 billion run rate in 2026, making it the fastest-growing enterprise software company in history. The listing would be the first IPO by a major frontier AI laboratory.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 CHINA · INDUSTRIAL ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "PUDU D7 Industrial Semi-Humanoid Launched for Factory Floors — 8-Hour Autonomous Operation, Self-Swapping Battery",
    "{{ROBOT_1_SUMMARY}}": "Pudu Robotics' Embodied division unveiled the PUDU D7 on June 1 — a 165cm, 45kg semi-humanoid robot built for manufacturing environments. Running on the PuduFM 1.0 AI foundation model, it handles dispensing, assembly and fine manipulation with millimetre-level force control across 50 degrees of freedom. Its standout feature: it independently removes, replaces and recharges its own battery, sustaining over 8 hours of continuous factory floor operation without any human intervention.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/06/01/pudu-embodied-unveils-the-next-generation-pudu-d7-opening-a-new-chapter-for-industrial-semi-humanoid-robotics/26651/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Confirm 26-Man World Cup Squad — Coach Popovic Targets Historic Quarter-Final in North America",
    "{{AUS_1_SUMMARY}}": "Australia's final FIFA World Cup 2026 squad was confirmed June 1, with coach Tony Popovic publicly targeting the quarter-finals — a milestone the Socceroos have never achieved. Drawn into Group D, they open against Turkey in Vancouver on June 14, face the USA in Seattle, then Paraguay in Santa Clara. The squad was named after a preparation camp in Sarasota, Florida.",
    "{{AUS_1_URL}}": "https://socceroos.com.au/news/socceroos-squad-numbers-revealed-fifa-world-cup-2026tm",

    "{{AUS_2_HEADLINE}}": "Traditional Owners Grieve as Bulldozers Move into Barrambin for Brisbane's 2032 Olympic Stadium",
    "{{AUS_2_SUMMARY}}": "Construction of Brisbane's $3.8 billion Olympic main stadium began June 1 at Barrambin (Victoria Park) with earth-moving machinery and police surrounding the heritage-listed site. First Nations custodians described watching sacred healing springs fenced off as an act of grief. More than a thousand trees, including pre-settlement natives, are expected to be cleared, with 10 federal applications lodged to protect significant Aboriginal areas.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Marks Mabo Day Tonight — Free Concert at Federation Square on 34th Anniversary of Landmark Land Rights Ruling",
    "{{VIC_1_SUMMARY}}": "A free Mabo Day concert presented by the Koorie Heritage Trust takes place at Federation Square tonight from 6pm to 8:30pm, featuring live music, an island feast, and the Blak Designer Mini Market. Today is the 34th anniversary of the High Court's Mabo v Queensland decision on June 3, 1992 — the ruling that overturned the doctrine of terra nullius and led directly to the Native Title Act 1993.",

    # Science
    "{{SCI_1_FLAG}}": "🔭 SPACE · NASA",
    "{{SCI_1_HEADLINE}}": "NASA's Roman Space Telescope Set to Find 100,000 New Worlds — More Than All Previous Missions Combined",
    "{{SCI_1_SUMMARY}}": "A new analysis published June 1 confirms NASA's Nancy Grace Roman Space Telescope — on track for launch in late 2026 — is expected to discover approximately 100,000 exoplanets in five years, dwarfing the roughly 6,300 found by all missions to date. Observing 100 million stars in largely uncharted Milky Way regions, it will search for rare Earth-sized worlds, study thousands of alien atmospheres, and catalogue rogue planets drifting without a star — potentially transforming the search for life in our galaxy.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Winter Is Here — How AI Can Turn Your Quiet Week Into a Profitable One",
    "{{INSIGHT_BODY}}": "For small trades operators in abrasive blasting, coatings, and industrial services, a run of cold or wet weather doesn't just slow site access — it can stall cash flow fast if you're not ready for it. The good news: quiet days are exactly when AI earns its keep. While the site slows this week, use AI to update your rate card with the July 1 fuel cost reset factored in. Have it draft follow-up messages for quotes over three weeks old. Ask it to generate SWMS templates for upcoming jobs. Get it to write a short case study from your last completed project for the website. Businesses that treat winter downtime as a business sprint — not dead time — consistently finish the second half of the year stronger than those who simply wait for the sun. With 29 days to EOFY, the admin you do this week could be worth thousands before August.",

    # Fun Facts
    "{{FACT_1}}": "Papua New Guinea has more distinct languages than any other country on Earth — over 840 spoken across its mountainous terrain, representing roughly 10% of all human languages despite a population of just 10 million. Many villages developed languages entirely unintelligible to neighbours a single valley away after thousands of years of isolated community life.",

    "{{FACT_2}}": "The total length of blood vessels in a single adult human body — arteries, veins and capillaries combined — is approximately 100,000 kilometres. That is enough to circle the Earth about 2.5 times, or travel from Melbourne to London and back roughly 47 times.",

    "{{FACT_3}}": "The Great Barrier Reef is the world's largest living structure — stretching 2,300 kilometres along Queensland's coast and covering an area larger than the UK, Switzerland and the Netherlands combined. Scientists estimate the reef has lost approximately 50% of its coral cover since 1995, primarily due to mass bleaching events driven by rising ocean temperatures.",

    # Joke
    "{{JOKE_SETUP}}": "Why do cabinet makers make the best project managers?",
    "{{JOKE_PUNCHLINE}}": "Because they understand exactly where every piece fits, they never leave a gap in the plan — and they know that if you rush the finish, it always shows.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Perfection is not attainable, but if we chase perfection we can catch excellence.”",
    "{{CLOSING_ATTR}}": "— Vince Lombardi",
    "{{CLOSING_MESSAGE}}": "Happy Wednesday, Liall. Rain arrives from Friday, so make the most of the dry days ahead. The fuel excise clock is ticking — 28 days until July 1 prices reset, so factor that into anything quoted this week for later delivery. The Socceroos confirmed their World Cup squad yesterday, Melbourne's Winter Night Market fires up at the QVM tonight, and today is Mabo Day — the 34th anniversary of the High Court's landmark ruling. A good mid-week to sprint on the admin before the cold sets in. Have a productive one.",
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
