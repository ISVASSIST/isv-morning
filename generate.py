#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 06 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Wed 6 May
    "{{WEATHER_1}}": "Wed 6 May · Heavy showers · 13–18°C",
    "{{WEATHER_2}}": "Thu 7 May · Very heavy rain · 12–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Fri 8 May · Showers easing · 11–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "Sat 9 May · Partly cloudy · 10–14°C",
    "{{WEATHER_5}}": "Sun 10 May · Mostly dry · 9–13°C",
    "{{WEATHER_ALERT}}": "⚠ Heavy rain Wed–Thu · Easing Friday",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 UKRAINE / RUSSIA",
    "{{WORLD_1_HEADLINE}}": "Zelensky and Putin Declare Rival Ceasefires — Ukraine's Starts Today, Russia's Is for Victory Day",
    "{{WORLD_1_SUMMARY}}": "President Zelensky declared a Ukrainian ceasefire beginning at midnight May 5–6, pre-empting Russia's proposed Victory Day truce on May 8–9. Putin's offer — floated during a call with Trump — came with a threat of 'massive missile strikes' on Kyiv if violated. Ukraine called Russia's terms 'not serious,' refusing to observe a ceasefire timed around a Russian military holiday. The duelling truces highlight the fragility of any peace push; markets are watching closely for breakthrough or breakdown.",
    "{{WORLD_1_URL}}": "https://kyivindependent.com/zelensky-announces-earlier-ceasefire-starting-may-6-ahead-of-russias-victory-day-truce/",

    "{{WORLD_2_FLAG}}": "🌊 MIDDLE EAST · HORMUZ",
    "{{WORLD_2_HEADLINE}}": "US Military Sinks Iranian Boats in Operation to Reopen the Strait of Hormuz",
    "{{WORLD_2_SUMMARY}}": "US Apache helicopters and Navy vessels sank at least six Iranian boats on May 4 under Operation Project Freedom — Trump's order to escort stranded shipping through the blockaded Strait of Hormuz. Iran claims civilian vessels were struck, killing five people; the US disputes the account. The UAE reported Iranian missile and drone strikes on Emirati territory in the same period. The operation has placed the fragile US-Iran ceasefire under severe pressure, with Iran threatening to strike European military bases.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/5/5/iran-says-us-military-killed-five-civilians-in-attacks-on-passenger-boats",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 INTEREST RATES · RBA",
    "{{ECON_1_HEADLINE}}": "RBA Raises Cash Rate to 4.35% — Third Hike This Year as Inflation Stays at 4.6%",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank raised the official cash rate by 25 basis points to 4.35% today, with eight of nine board members voting in favour. The decision follows March headline inflation of 4.6% — more than double the 2–3% target — driven significantly by fuel prices tied to the Hormuz crisis. The hike wipes out all three 2025 rate cuts. Westpac forecasts two further 25bp hikes in June and August that would push the cash rate to 4.85%. For small businesses on variable-rate equipment finance, this feeds through to monthly repayments within weeks.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/media-releases/2026/mr-26-08.html",

    "{{ECON_2_FLAG}}": "⛽ FUEL · PRICES",
    "{{ECON_2_HEADLINE}}": "Diesel at 222c/Litre — Fuel Excise Cut Expires June 30, 56 Days Away",
    "{{ECON_2_SUMMARY}}": "Terminal gate diesel prices are running around 222 cents per litre nationally, held down by the government's fuel excise halved to 26.3c/litre from March 30 to June 30. That's 56 days until expiry, and with Hormuz tensions re-escalating after US military action on May 4, a post-July price snapback is a genuine risk. Any quotes you're writing for jobs running past July should include a fuel cost contingency right now.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · FINANCIAL SERVICES",
    "{{TECH_1_HEADLINE}}": "Anthropic Launches 10 Ready-to-Run AI Agents for Banks, Insurers and Asset Managers",
    "{{TECH_1_SUMMARY}}": "Anthropic unveiled 10 pre-built agent templates at an invite-only New York event on May 5, covering tasks like pitch building, KYC screening, earnings review, and month-end reconciliation. The release includes full Microsoft 365 integration — letting Claude run as a single agent across Excel, PowerPoint, Word, and Outlook — and a Moody's data partnership covering 600 million companies. While aimed at large institutions, the direction is unmistakable: AI is moving from assistant to autonomous operator across every industry.",
    "{{TECH_1_URL}}": "https://fortune.com/2026/05/05/anthropic-wall-street-financial-services-agents-jamie-dimon/",

    "{{TECH_2_FLAG}}": "📊 AI · PERFORMANCE",
    "{{TECH_2_HEADLINE}}": "AI Agents Now Succeed at Real-World Tasks 77% of the Time — Up From 20% Just 12 Months Ago",
    "{{TECH_2_SUMMARY}}": "New benchmarking data from Terminal-Bench shows AI agents now successfully complete real-world tasks 77.3% of the time, compared to just 20% in mid-2025. AI handling cybersecurity challenges now solves them 93% of the time, up from 15% in 2024. The pace of improvement is extraordinary. If you evaluated AI tools and found them unreliable a year ago, the landscape has fundamentally changed — and the gap between early adopters and late movers is widening every month.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 CHINA · INDUSTRIAL ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "IFR: China Makes AI-Powered Robots the Core of Its 15th Five-Year Plan",
    "{{ROBOT_1_SUMMARY}}": "The International Federation of Robotics published analysis yesterday confirming China has elevated robotics and 'embodied intelligence' to the same strategic tier as nuclear fusion in its 15th Five-Year Plan (2026–2030). Humanoid robots now access an $8.2 billion (60B yuan) National AI Industry Investment Fund. China already deploys approximately 2 million industrial robots — 4.5 times more than Japan — and accounted for 54% of all new industrial robots installed globally in 2025. The strategic gap with the rest of the world is widening rapidly.",
    "{{ROBOT_1_URL}}": "https://ifr.org/ifr-press-releases/news/china-makes-ai-powered-robots-core-of-national-strategy",

    # Australia
    "{{AUS_1_HEADLINE}}": "Federal Budget Next Week — Earned Income Offset, EV Tax Changes and Cost-of-Living Relief Expected",
    "{{AUS_1_SUMMARY}}": "Treasurer Jim Chalmers delivers the Federal Budget next week, with measures flagged including an 'earned income offset' for low-to-middle income earners, scrapping the EV discount, and cost-of-living relief packages. Consumer confidence sits at just 67.2 — only 15% of Australians say now is a good time for major purchases — and 61% of businesses expect bad economic conditions over the next year.",
    "{{AUS_1_URL}}": "https://www.roymorgan.com/findings/roy-morgan-update-may-5-2026",

    "{{AUS_2_HEADLINE}}": "Business Confidence Hits Lowest Level Since COVID as Rate Hike Wipes Out 2025 Cuts",
    "{{AUS_2_SUMMARY}}": "ANZ-Roy Morgan data from May 5 shows 61.3% of Australian businesses now expect bad economic conditions over the next year — the worst reading since the COVID downturn. The RBA's third consecutive hike today has undone all three 2025 cuts. Market consensus is for at least one more rise before year end. For small operators, the window to refinance or restructure debt is narrowing.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Budget: $14M AI Adoption Fund, $30M Frankston TAFE AI Centre, $19M for Small Business",
    "{{VIC_1_SUMMARY}}": "The state budget delivered Tuesday includes a $19 million small business support package, a $14 million AI career conversion fund to protect workers impacted by automation, and a $30 million Digital, AI and Technology TAFE Centre of Excellence being built at Chisholm Institute's Frankston campus — in Liall's backyard. Free public transport extends until end of May with half-price fares for the remainder of 2026. Budget projects a $700 million surplus in 2025-26.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ PARTICLE PHYSICS",
    "{{SCI_1_HEADLINE}}": "LHC 'Charming Penguins' Hint at New Physics — 1-in-16,000 Chance the Result Is Just Noise",
    "{{SCI_1_SUMMARY}}": "Physicists at CERN's Large Hadron Collider have measured B meson decays where the angle of emerging particles disagrees with the Standard Model at 4-sigma significance — roughly a 1-in-16,000 chance the result is random noise. The anomaly, accepted for Physical Review Letters and corroborated by the CMS experiment, involves quantum processes called 'charming penguin diagrams' — a name coined after a physicist lost a pub darts game at CERN in 1977. If confirmed, the discovery could reveal undiscovered particles or forces that rewrite our understanding of fundamental physics.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Know Your Numbers Before the Budget Drops: How AI Can Build Your Rate-Rise Survival Plan",
    "{{INSIGHT_BODY}}": "With the cash rate now at 4.35% and the Federal Budget landing next week, right now is the moment to run a realistic financial health check on your business. AI tools can take your last 12 months of invoices, material costs, and fuel receipts and generate a plain-English cash flow projection in minutes — flagging whether a further rate rise would tip you into difficulty and identifying which cost lines are eating the most margin. The tradies who come out the other side of a tightening cycle are the ones who see the crunch coming early. If you don't have a financial model for your business, an AI tool and a morning of data entry can change that today — well before Chalmers delivers his numbers next week.",

    # Fun Facts
    "{{FACT_1}}": "The term 'penguin diagram' in particle physics was coined after a 1977 darts game at CERN. Physicist John Ellis lost a bet and was required to include the word 'penguin' in his next scientific paper — so he named a class of quantum loop diagrams after the bird. Nearly 50 years later, LHC scientists are still chasing 'charming penguins' for clues about new physics.",
    "{{FACT_2}}": "When Australia decimalised its currency in 1966, Prime Minister Menzies proposed calling the new unit the 'royal.' A public vote overwhelmingly rejected it. 'Dollar' was chosen instead — making Australia one of the very few countries to name its currency by popular opinion.",
    "{{FACT_3}}": "Garlic turns blue-green when it meets acid. The sulphur compounds in garlic react with trace amino acids in the presence of vinegar or lemon juice, producing harmless blue-green pigments. It alarms cooks every time, but it is completely safe to eat — and happens routinely when pickling.",

    # Joke
    "{{JOKE_SETUP}}": "Why do scaffolders always seem so calm under pressure?",
    "{{JOKE_PUNCHLINE}}": "They're used to working at every level.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"In the middle of every difficulty lies opportunity.\"",
    "{{CLOSING_ATTR}}": "Albert Einstein",
    "{{CLOSING_MESSAGE}}": "Heavy rain today and through Thursday — keep outdoor jobs pushed to the back half of the week and the wet-weather kit in the van. The big move this morning is the RBA hike to 4.35%, officially wiping out last year's rate cuts: run the numbers on your variable-rate finance today. On a brighter note, yesterday's Victorian budget earmarked a $30 million AI and tech training centre at Frankston — practically next door. The tools are coming to you, Liall. Make it count.",
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
