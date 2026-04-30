#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 01 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Fri 1 May
    "{{WEATHER_1}}": "Fri 1 May · Showers likely · 17°C",
    "{{WEATHER_2}}": "Sat 2 May · Showers · 15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Sun 3 May · Mostly cloudy · 15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Mon 4 May · Clearing · 17°C",
    "{{WEATHER_5}}": "Tue 5 May · Fine · 19°C",
    "{{WEATHER_ALERT}}": "Wet start to May",

    # World
    "{{WORLD_1_FLAG}}": "🇦🇪 UAE · ENERGY",
    "{{WORLD_1_HEADLINE}}": "UAE Quits OPEC After 58 Years — Effective Today, Freeing It to Flood Markets with Oil",
    "{{WORLD_1_SUMMARY}}": "The United Arab Emirates formally left OPEC on May 1, ending 58 years of membership. Long frustrated by production quotas capping it at 3.2 million barrels per day while its actual capacity sits near 5 million, the UAE is now free to pump without restriction. Iran's closure of the Strait of Hormuz still blocks most Gulf exports, so the near-term impact on supply is limited — but if peace resumes traffic flow, the UAE could add up to 1.6 million barrels per day to global supply, roughly 1.5% of world output. For Australian businesses still absorbing Middle East fuel surcharges, this is a meaningful long-term price-relief signal.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/4/28/uae-leaves-opec-and-opec",

    "{{WORLD_2_FLAG}}": "🇬🇧 UK · DIPLOMACY",
    "{{WORLD_2_HEADLINE}}": "King Charles Addresses U.S. Congress — First British Monarch in 35 Years to Do So",
    "{{WORLD_2_SUMMARY}}": "King Charles III made a historic address to a joint session of the U.S. Congress on April 28, calling the Anglo-American alliance 'more important today than it has ever been.' In a nearly 30-minute speech he condemned a recent attack near the Capitol and urged united democracies to stand firm against violence and division. He later attended a White House state dinner hosted by President Trump. The last British monarch to address Congress was Queen Elizabeth II in 1991 — making this a significant diplomatic event.",
    "{{WORLD_2_URL}}": "https://thehill.com/policy/international/5853910-king-charles-address-congress/",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AUSTRALIA · FUEL",
    "{{ECON_1_HEADLINE}}": "China Agrees to Resume Jet Fuel Exports to Australia — Easing Aviation Supply Crunch",
    "{{ECON_1_SUMMARY}}": "Foreign Minister Penny Wong announced on April 30 that China has agreed to cooperate on resuming jet fuel exports to Australia, following high-level diplomatic talks. China had halted refined fuel exports in March amid Middle East supply disruptions — a significant blow given China supplied 32% of Australia's jet fuel imports in 2025. Export licences are now being issued to Chinese state-owned refiners for May loadings. It's a direct supply-chain win for Australian airlines and logistics operators, though broader pump prices remain elevated.",
    "{{ECON_1_URL}}": "https://www.france24.com/en/live-news/20260429-australia-fm-says-china-agrees-to-collaborate-on-jet-fuel-exports",

    "{{ECON_2_FLAG}}": "🏪 AUSTRALIA · COSTS",
    "{{ECON_2_HEADLINE}}": "ACCC Reports Surge in Fuel Surcharge Complaints — Some Small Businesses Charged Over 70%",
    "{{ECON_2_SUMMARY}}": "The competition regulator has recorded a sharp rise in complaints from small businesses about fuel surcharges imposed by transport and logistics contractors, with some surcharges for remote-area businesses exceeding 70%. The government's temporary halving of the fuel excise to 26.3 cents per litre offers partial relief — but expires June 30. For trades operators relying on freight or subcontractors, auditing your current surcharge agreements before the excise snaps back is a worthwhile task this week.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · BUSINESS",
    "{{TECH_1_HEADLINE}}": "Google Declares the 'Agentic Enterprise' Era — AI Is Shifting from Chat to Action",
    "{{TECH_1_SUMMARY}}": "Google Cloud CEO Thomas Kurian announced on April 30 the company's Agentic Enterprise strategy, framing it as the shift from AI as a 'system of intelligence' to a 'system of action' — where AI agents complete tasks, automate workflows, and operate independently in business software. This follows confirmation that Anthropic's annualised revenue crossed $30 billion in April, overtaking OpenAI's $25 billion for the first time. For small business owners: the AI tools being built right now won't just answer questions — they'll handle scheduling, quoting, ordering, and compliance without you touching them.",
    "{{TECH_1_URL}}": "https://www.devflokers.com/blog/ai-news-last-24-hours-april-29-30-2026-roundup",

    "{{TECH_2_FLAG}}": "🧠 AI · RESEARCH",
    "{{TECH_2_HEADLINE}}": "AI Model That Claimed to 'Think Like a Human' Was Just Memorising, Study Finds",
    "{{TECH_2_SUMMARY}}": "The much-hyped Centaur AI model, which claimed to replicate human cognitive behaviour across 160 tasks, has been challenged by new research published April 29 — finding the model wasn't truly thinking, just pattern-matching on memorised training data. The finding echoes longstanding debates about whether large language models truly understand or merely predict. Practical upshot for AI users: these tools are genuinely powerful precisely because of their pattern recognition, but knowing their limits helps you deploy them more effectively and catch their mistakes before they matter.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "✈️ JAPAN · ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "Japan Airlines Begins Testing Humanoid Robots for Baggage Handling at Haneda Airport",
    "{{ROBOT_1_SUMMARY}}": "Japan Airlines launched Japan's first demonstration experiment deploying humanoid robots for airport ground handling at Tokyo's Haneda tarmac, published April 30. The Unitree-built robots — roughly 130 cm tall — use 3D LiDAR and depth cameras to handle baggage and cargo containers alongside human staff. JAL's 4,000 ground handlers are stretched by surging inbound tourism and Japan's shrinking workforce. The two-year trial, running until 2028, aims to expand robots into cabin cleaning and ground equipment operation. Labour shortage is now driving real-world humanoid deployment at industrial scale.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/04/30/japan-trials-humanoid-robots-for-airport-operations-as-labor-shortages-intensify/101120/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Commits to All 14 Bondi Terror Attack Inquiry Recommendations — Including National Gun Reform",
    "{{AUS_1_SUMMARY}}": "The Albanese government announced it will enact all 14 recommendations from the interim report into the Bondi terror attack and antisemitism, which killed 15 people in December 2025. Key measures include nationally consistent gun laws, a firearm buyback, enhanced security at Jewish sites, and a full-time national counter-terrorism coordinator. A final Royal Commission report is due by December 14 — the one-year anniversary of the attack.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/counter-terrorism-laws-did-not-hinder-bondi-attack-prevention-interim-report-reveals/rujr8zvn9",

    "{{AUS_2_HEADLINE}}": "Gas Export Tax Debate Reaches Fever Pitch — PM Albanese Forced to Weigh In",
    "{{AUS_2_SUMMARY}}": "The proposed gas export levy has become one of the most contested policy battles in Canberra, with PM Albanese now directly weighing in after intense lobbying from industry. The tax — designed to redirect a share of LNG profits to Australian consumers and businesses during the energy crisis — could raise significant revenue, but gas companies warn it will chill investment. No final decision has been announced, but the political pressure is intensifying.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Free Public Transport Runs Through All of May — Then Half-Price to Year's End",
    "{{VIC_1_SUMMARY}}": "Free travel on trains, trams and buses across Victoria continues through May 31, before transitioning to half-price fares — capped at $5.70 daily — from June 1 until December 31, 2026. The extension eases cost-of-living pressure during the fuel crisis. Average commuters could save over $850 between June and year's end. Under-18s and eligible concession holders continue to travel permanently free.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 SCIENCE · MEDICINE",
    "{{SCI_1_HEADLINE}}": "Scientists Get First-Ever 3D View of Killer T Cells Destroying Cancer — at Nanometre Precision",
    "{{SCI_1_SUMMARY}}": "Researchers at the University of Geneva have captured the first three-dimensional images of cytotoxic T lymphocytes — the body's specialised 'killer cells' — in a near-native state as they eliminate cancer. Using cryo-expansion microscopy, the team flash-froze cells and physically expanded them using an absorbent hydrogel to reveal precise internal organisation at nanometre scale. They found killer T cells form a dome-shaped 'immune synapse' — a tightly controlled contact zone where toxic molecules destroy the cancer cell without harming surrounding healthy tissue. Published April 29, the breakthrough could help explain why some immunotherapy treatments fail and guide the next generation of cancer therapies.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI-Powered Route Planning Is Cutting Tradie Fuel Bills by Up to 20% — Right When It Matters Most",
    "{{INSIGHT_BODY}}": "With pump prices still elevated from the Middle East crisis and the government's fuel excise cut expiring June 30, every litre of diesel counts. AI-driven route optimisation tools — many already built into job management platforms like ServiceM8, Tradify, or standalone apps like Circuit or OptimoRoute — can cut your driving distance by 15–20% by sequencing jobs intelligently, accounting for live traffic, and eliminating backtracking. For a sole operator doing 30,000+ km a year for work, that's 4,500–6,000 km less driving — potentially $1,500–$2,500 saved on fuel annually, before factoring in tyre wear and maintenance savings. If you're still routing your day by habit or intuition, you're leaving money on the table every week, and the clock is ticking on the excise discount.",

    # Fun Facts
    "{{FACT_1}}": "Today is International Workers' Day — celebrated as a public holiday in over 80 countries on May 1 — and its origin traces to the 1886 Haymarket affair in Chicago, where workers striking for an eight-hour working day turned violent. Australia's own eight-hour day movement predates it by 30 years: Melbourne stonemasons won the right in 1856, making Victoria one of the first places in the world to achieve what is now the standard working week.",
    "{{FACT_2}}": "The Maillard reaction — the golden-brown crust you get when searing meat, toasting bread, or brewing coffee — was named after French chemist Louis-Camille Maillard, who first described it in 1912. It's a chemical reaction between amino acids and reducing sugars that produces hundreds of distinct flavour compounds. It has nothing to do with caramelisation, which involves only sugars — which is why boiled meat and seared meat taste completely different.",
    "{{FACT_3}}": "The original Doom (1993) was installed on so many computers that id Software's John Carmack claimed it was the most-installed program in PC history — more copies running than Windows 95, both released in the same year. The game's source code was eventually released publicly, and since then it has been ported to run on ATMs, digital cameras, a pregnancy test display, and even inside other video games.",

    # Joke
    "{{JOKE_SETUP}}": "Why do roofers make terrible secret agents?",
    "{{JOKE_PUNCHLINE}}": "They always blow their cover.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The secret of getting ahead is getting started.\"",
    "{{CLOSING_ATTR}}": "Mark Twain",
    "{{CLOSING_MESSAGE}}": "It's Friday, Liall — the week wraps up and a wet weekend is forecast, so lock in any outdoor work today. Two big energy stories broke overnight: the UAE officially left OPEC this morning after 58 years, and Penny Wong secured a deal to get jet fuel flowing from China again. Victoria's free public transport continues through all of May, saving commuters and crews real money. Make it a sharp morning.",
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
