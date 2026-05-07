#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 08 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Fri 8 May
    "{{WEATHER_1}}": "Fri 8 May · Rain clearing · 12°C",
    "{{WEATHER_2}}": "Sat 9 May · Partly cloudy · 15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Sun 10 May · Mostly sunny · 16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Mon 11 May · Partly cloudy · 17°C",
    "{{WEATHER_5}}": "Tue 12 May · Budget Day · Showers · 16°C",
    "{{WEATHER_ALERT}}": "⚠ Cold polar blast · clearing Sat",

    # World
    "{{WORLD_1_FLAG}}": "🌐 MIDDLE EAST",
    "{{WORLD_1_HEADLINE}}": "1,600 Ships Stranded in Hormuz as Trump Pauses 'Project Freedom' Amid Iran Deal Talks",
    "{{WORLD_1_SUMMARY}}": "After only two escorted transits, President Trump suspended his 'Project Freedom' naval escort operation through the Strait of Hormuz, saying talks with Iran via Pakistani intermediaries show 'great progress.' Roughly 1,600 vessels remain stranded in or near the strait, and Tehran is reviewing the latest US proposal. Iran's Foreign Minister says navigation will normalise only once sanctions are lifted and the conflict formally ends. Global oil markets are on edge — the next 72 hours may be decisive.",
    "{{WORLD_1_URL}}": "https://www.nbcnews.com/world/iran/us-iran-war-trump-open-hormuz-attacks-ships-ceasefire-rcna343604",

    "{{WORLD_2_FLAG}}": "🇮🇳 SOUTH ASIA",
    "{{WORLD_2_HEADLINE}}": "One Year Since India's Operation Sindoor — Analysts Warn 2026 Conflict Risks Remain High",
    "{{WORLD_2_SUMMARY}}": "May 7 marked the one-year anniversary of India's Operation Sindoor — the strikes into Pakistan-administered territory triggered by the Pahalgam terror attack that killed 26 civilians. A fragile ceasefire has held since May 10, 2025, but a new analysis in The Diplomat warns the space for restraint is narrowing. Indian officials have signalled that any future terrorist incident traced to Pakistan will be met with a firm, decisive response — raising the stakes of any next crisis considerably.",
    "{{WORLD_2_URL}}": "https://thediplomat.com/2026/05/a-year-after-operation-sindoor-rising-risks-and-deepening-instability/",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 INTEREST RATES",
    "{{ECON_1_HEADLINE}}": "RBA Lifts to 4.35% for Third Time in 2026 — CBA Says Pause Likely, Westpac Sees August Rise",
    "{{ECON_1_SUMMARY}}": "One day after the Reserve Bank's third consecutive rate rise to 4.35%, the major banks are split on what comes next. CBA economists say the bank now has room to pause, with 2026 GDP growth revised down to 1.3%. Westpac still forecasts another rise in August. For small businesses on variable-rate equipment finance or overdraft facilities, yesterday's increase flows through in weeks. Now is the moment to review your loan structure before the next move.",
    "{{ECON_1_URL}}": "https://www.commbank.com.au/articles/newsroom/2026/05/rba-may-interest-rates-cba-economists-analysis.html",

    "{{ECON_2_FLAG}}": "⛽ FUEL & BUDGET",
    "{{ECON_2_HEADLINE}}": "Fuel Excise Relief Ends June 30 — Petrol Near $2/L, Diesel Near $3/L as Budget Week Arrives",
    "{{ECON_2_SUMMARY}}": "The government's halved fuel excise (saving 26.3c per litre) expires June 30 — and Treasurer Chalmers has signalled Tuesday's budget will be restrained, making an extension far from certain. National petrol averages are hovering around $1.95–$2.10 per litre and diesel near $2.80–$3.00 per litre, driven by ongoing Hormuz supply disruption. For trades businesses with ongoing or multi-month contracts, now is the time to factor a fuel contingency into your pricing.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI MODELS",
    "{{TECH_1_HEADLINE}}": "OpenAI Releases GPT-5.5 Instant — 52% Fewer Hallucinations, 30% More Concise — New Default for All Users",
    "{{TECH_1_SUMMARY}}": "OpenAI's GPT-5.5 Instant became the default model for all ChatGPT users this week, replacing GPT-5.3 Instant. The update delivers 52.5% fewer hallucinated claims on high-stakes topics — medicine, law, and finance — and cuts response length by around 30% without losing accuracy. Enhanced memory personalisation using past conversations and connected Gmail is rolling out to paid users first. If you use ChatGPT as a regular business tool, the day-to-day quality has genuinely improved.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/05/05/openai-releases-gpt-5-5-instant-a-new-default-model-for-chatgpt/",

    "{{TECH_2_FLAG}}": "📊 AI ADOPTION",
    "{{TECH_2_HEADLINE}}": "Microsoft: 17.8% of Working-Age Population Now Uses AI — Developer Code Commits Up 78% Year-on-Year",
    "{{TECH_2_SUMMARY}}": "Microsoft's 2026 State of Global AI Diffusion report, published yesterday, found AI usage among the global working-age population grew from 16.3% to 17.8% in a single quarter. Developers are leading the charge — global software commits jumped 78% year-on-year, the fastest productivity acceleration the industry has recorded. For businesses still holding off on AI adoption, the productivity gap with early users is widening every quarter.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 INDUSTRIAL AI · USA",
    "{{ROBOT_1_HEADLINE}}": "Boston Dynamics Embeds Google's Gemini AI Into Spot Robots — Units Now Continuously Learn Their Sites",
    "{{ROBOT_1_SUMMARY}}": "Boston Dynamics has integrated Google DeepMind's Gemini Robotics ER 1.6 model into its Spot robots and Orbit enterprise platform under a new AIVI-Learning system. Deployed robots now continuously build and update a detailed AI model of the specific facility they work in — going far beyond pre-programmed routines to genuine on-site adaptive intelligence. For industrial operators, the shift from 'robot as tool' to 'robot as learning system' is no longer theoretical.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/boston-dynamics-and-google-deepmind-are-using-gemini-to-make-spot-smarter/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Scraps Most of $45B Inland Rail — Project Halted North of Parkes Ahead of Tuesday's Budget",
    "{{AUS_1_SUMMARY}}": "The government announced Wednesday it is placing an indefinite hold on all Inland Rail construction north of Parkes, NSW, after an independent review found the Melbourne-to-Brisbane route would cost at least $45 billion — nearly three times the original $16.4B estimate. The completed southern leg from Melbourne to Parkes proceeds; $1.75B is redirected to alternative freight rail and shipping initiatives. The scrapping lands just days before Tuesday's May 12 federal budget.",
    "{{AUS_1_URL}}": "https://www.bloomberg.com/news/articles/2026-05-06/australia-scraps-much-of-inland-rail-project-to-save-budget-cash",

    "{{AUS_2_HEADLINE}}": "Polar Blast Delivers Coldest May Conditions in Decades to Southeast Australia",
    "{{AUS_2_SUMMARY}}": "A deep polar airmass swept Victoria, NSW, and Tasmania this week, bringing snow to alpine areas above 600 metres and overnight frost warnings across regional Victoria. Ski resorts recorded temperatures as low as −6°C for the first time this season. The cold snap is lifting through Friday, with clearing conditions and milder temperatures expected from Saturday.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Writers Festival Wraps Up This Sunday — Free Sessions Still Available at CBD Venues",
    "{{VIC_1_SUMMARY}}": "Melbourne Writers Festival closes Sunday May 10 with sessions across the city covering AI, technology, economics, culture, and the future of work. Most events are free or low-cost and walk-in friendly. If the polar blast in Carrum Downs has you looking for a reason to get into the city this Saturday, this is a solid one.",

    # Science
    "{{SCI_1_FLAG}}": "💊 METABOLISM · USA",
    "{{SCI_1_HEADLINE}}": "Scientists Engineer a 'Trojan Horse' GLP-1 Drug That Smuggles a Metabolic Activator Directly Into Fat Cells",
    "{{SCI_1_SUMMARY}}": "Researchers have developed a next-generation weight-loss approach: instead of simply mimicking GLP-1 and GIP gut hormones, they engineered molecules that use those hormones as a delivery vehicle — a Trojan horse — to smuggle a powerful metabolic activator directly into fat and liver cells. Early results show faster and more sustained fat loss than standard GLP-1 drugs alone. With Ozempic-era medications already reshaping healthcare, food consumption patterns, and global agriculture, this points toward a considerably more potent second generation already in development.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "From Site Photo to Client Report in 30 Seconds — The AI Habit Most Tradies Are Still Missing",
    "{{INSIGHT_BODY}}": "Every tradie takes photos on site — but most of those images die in a camera roll filed somewhere in May. Those exact photos, fed into an AI with a simple prompt — 'here's today's site photo, write a short progress report for my client' — produce a clean, professional update in under a minute. Add a line about what's still to come, and you have a ready-to-send client message that took thirty seconds. Clients who receive regular updates are far less likely to dispute invoices, delay payment, or leave a negative review. For a business running multiple jobs at once, this habit alone can transform client relationships — and it costs nothing but a moment and a prompt. Try it on your next site visit today.",

    # Fun Facts
    "{{FACT_1}}": "The Great Wall of China was built using a mortar made from sticky rice flour mixed with calcium carbonate — and it turned out to be one of the toughest building materials ever recorded. Some sections constructed with this mix have resisted earthquake damage and tree root penetration for over 1,500 years, still outperforming lime-only mortar of the same era.",
    "{{FACT_2}}": "Australia is the only inhabited continent with no active volcanoes on its mainland — a result of sitting near the centre of its tectonic plate rather than on a boundary. The nearest active volcanoes in Australian sovereign territory are on Heard Island and McDonald Islands, roughly 4,000 kilometres southwest in the Southern Ocean.",
    "{{FACT_3}}": "Titanium is the ninth most abundant element in Earth's crust, yet costs around 30 times more per kilogram to produce than steel — because extracting pure titanium requires heating ore to 850°C under a blanket of magnesium gas to strip away oxygen and chlorine one molecule at a time. The production process has not changed fundamentally since it was developed in 1940.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the plasterer never lose an argument?",
    "{{JOKE_PUNCHLINE}}": "He always knew how to smooth things over.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Opportunity is missed by most people because it is dressed in overalls and looks like work.\"",
    "{{CLOSING_ATTR}}": "Thomas A. Edison",
    "{{CLOSING_MESSAGE}}": "Cold and wet in Carrum Downs this Friday morning — the polar blast is still sitting but should lift by tomorrow. Yesterday's RBA hike to 4.35% is the new rate environment, Tuesday is budget day, and fuel excise relief expires June 30. Three things worth getting in front of today before the week closes. Have a strong Friday, Liall.",
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
