#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 04 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 4 Jun
    # Cold front today with up to 30mm of rain, then easing through the week
    "{{WEATHER_1}}": "THU 4 · 🌧 Cold front, rain · 7–14°C",
    "{{WEATHER_2}}": "FRI 5 · 🌧 Showers likely · 7–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 6 · ⛅ Mostly cloudy · 8–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SUN 7 · ☀ Clearing · 8–14°C",
    "{{WEATHER_5}}": "MON 8 · 🌧 Shower possible · 7–13°C",
    "{{WEATHER_ALERT}}": "⚠ COLD FRONT TODAY · UP TO 30MM",

    # World
    "{{WORLD_1_FLAG}}": "🌏 UKRAINE · RUSSIA",
    "{{WORLD_1_HEADLINE}}": "Russia Fires 198 Drones at Ukraine — Six Dead in Kyiv as Ukrainian Drones Hit St. Petersburg Oil Terminal",
    "{{WORLD_1_SUMMARY}}": "Russian forces launched 198 drones at Ukrainian cities overnight June 2–3; air defences intercepted 189. Six civilians were killed and 90 injured across Kyiv. Ukrainian forces responded by striking Russia's largest Baltic Sea oil terminal in St. Petersburg, setting it ablaze. President Zelenskyy renewed urgent calls for additional Western air defence systems to counter the nightly barrages.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/world/europe/ukraine",

    "{{WORLD_2_FLAG}}": "🌎 SOUTH AMERICA · COLOMBIA",
    "{{WORLD_2_HEADLINE}}": "Tough-on-Crime Outsider Leads Colombia Presidential Race — Runoff Set Against Former Petro Ally",
    "{{WORLD_2_SUMMARY}}": "Aberaldo de la Espriella, a security-focused outsider running on a tough-on-crime platform, has emerged as the front-runner in Colombia's presidential election, setting up a runoff against Ivan Cepeda, a close ally of outgoing President Gustavo Petro. The result reflects deepening voter frustration with crime and insecurity across Latin America, with de la Espriella drawing strong support from regions hardest hit by gang violence.",
    "{{WORLD_2_URL}}": "https://www.npr.org/sections/world/",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 WAGES · SMALL BUSINESS",
    "{{ECON_1_HEADLINE}}": "National Minimum Wage Rises 5.97% to $26.44/Hr — Modern Award Rates Up 4.75% From 1 July",
    "{{ECON_1_SUMMARY}}": "The Fair Work Commission announced on June 2 that Australia's national minimum wage rises by nearly 6% to $26.44 an hour — or $1,004.90 a week — from July 1. Modern award rates covering most trade workers follow at 4.75%. The Commission described it as a 'particularly challenging' decision given inflation and cost-of-living pressures. Employers have 27 days to update payroll and reprice any work quoted under current rates.",
    "{{ECON_1_URL}}": "https://www.fairwork.gov.au/about-us/workplace-laws/annual-wage-review/annual-wage-review-2026",

    "{{ECON_2_FLAG}}": "⚡ ENERGY · DARWIN",
    "{{ECON_2_HEADLINE}}": "Ichthys LNG Strike Threatens Australia's Gas Exports — Rolling Stoppages Planned Through June 23",
    "{{ECON_2_SUMMARY}}": "The Offshore Alliance commenced protected industrial action at Inpex's Ichthys LNG facility near Darwin on June 2, running four-hour daily stoppages at Australia's largest gas export hub — 9.3 million tonnes per year. Escalating action is scheduled through June 23. Talks over pay rises and conditions have stalled after more than a year of negotiation, raising concerns about wholesale gas prices and supply security for Asian LNG buyers.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🏛️ USA · AI POLICY",
    "{{TECH_1_HEADLINE}}": "Trump Signs Executive Order Asking AI Companies to Give US Government 30-Day Early Access to New Models",
    "{{TECH_1_SUMMARY}}": "President Trump signed an executive order on June 2 asking AI companies to voluntarily submit new frontier models to the federal government for testing up to 30 days before public release. The order also establishes an 'AI cybersecurity clearinghouse' to track model vulnerabilities and directs agencies to harden critical infrastructure against AI-enabled threats. An earlier draft mandating a 90-day review period was scrapped after lobbying from major AI developers.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/06/02/trump-executive-order-ai.html",

    "{{TECH_2_FLAG}}": "💹 GLOBAL · AI MARKETS",
    "{{TECH_2_HEADLINE}}": "Goldman Sachs Revises Humanoid Robotics Forecast Sixfold — Now Sees $38 Billion Market by 2035",
    "{{TECH_2_SUMMARY}}": "Goldman Sachs dramatically upgraded its humanoid robotics market projection from $6 billion to $38 billion by 2035, citing AI advances and falling hardware costs — unit prices have dropped from $50,000–$250,000 to $30,000–$150,000 in a single year. The bank's base case calls for 250,000 industrial humanoid shipments by 2030, rising to 1.4 million annually by 2035, with China currently outpacing the US in deployment speed and manufacturing cost reduction.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 USA · NVIDIA",
    "{{ROBOT_1_HEADLINE}}": "NVIDIA and Unitree Unveil Isaac GR00T Open Humanoid Robot Platform for Global Research Labs",
    "{{ROBOT_1_SUMMARY}}": "Announced at NVIDIA GTC Taipei on June 1, the Isaac GR00T reference robot pairs Unitree's H2 Plus humanoid (6 feet tall, 75 degrees of freedom) with NVIDIA Jetson AGX Thor compute running at 2,070 TOPS, open-source GR00T AI models, and Sharpa tactile five-finger hands. Stanford Robotics Center, ETH Zurich, Ai2 and UC San Diego will use the platform to push the frontier of physical AI. Available from Unitree in late 2026, with model workflows dropping on GitHub and Hugging Face shortly.",
    "{{ROBOT_1_URL}}": "https://nvidianews.nvidia.com/news/nvidia-open-humanoid-robot-reference-design",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Confirm 26-Man World Cup Squad — Open Against Turkey in Vancouver on June 14",
    "{{AUS_1_SUMMARY}}": "Australia's FIFA World Cup 2026 squad was confirmed June 1, with 26 players drawn from European, Asian and A-League clubs. Coach Tony Popovic has publicly targeted a quarter-final — a milestone the Socceroos have never reached. They open Group D against Turkey in Vancouver on June 14, face the United States in Seattle, then Paraguay in Santa Clara.",
    "{{AUS_1_URL}}": "https://socceroos.com.au/news/socceroos-squad-numbers-revealed-fifa-world-cup-2026tm",

    "{{AUS_2_HEADLINE}}": "ACT Public Schools to Close June 11 as AEU Teachers' Strike Proceeds",
    "{{AUS_2_SUMMARY}}": "The ACT Education Directorate confirmed all ACT government schools will close on June 11 following AEU members' scheduled strike action. Teachers are pushing for better pay and conditions after protracted EBA negotiations. Parents across the territory have been notified to arrange childcare for the one-day closure.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "St Kilda Film Festival Opens Tonight — 11 Days of Australian Short Cinema From June 4 to 14",
    "{{VIC_1_SUMMARY}}": "Australia's longest-running short film festival opens Thursday at venues across St Kilda, running through June 14 with screenings, Q&As and industry events. The program spans comedy, documentary and drama shorts from local and international filmmakers. Free and ticketed sessions are available across the run.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ PHYSICS",
    "{{SCI_1_HEADLINE}}": "Scientists Reverse Energy Flow in Turbulence — Overturning an 80-Year-Old Theory",
    "{{SCI_1_SUMMARY}}": "Researchers at the University of Pittsburgh and University of Turin have shown for the first time that the direction of energy flow in turbulence can be deliberately altered, overturning the Kolmogorov 1941 theory that energy in 3D flows always cascades from large to small scales. Using a tensor-based mathematical framework, they demonstrated the flow can be reversed by changing how forces align. Published June 2 via ScienceDaily, the finding opens new possibilities for controlling ocean currents and improving medical fluid technologies.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The $26.44 Challenge: How Trades Operators Can Absorb the Wage Rise Without Losing Margin",
    "{{INSIGHT_BODY}}": "The Fair Work Commission just ruled that Australia's minimum wage rises to $26.44 an hour from 1 July — a 5.97% lift, with most trade award rates following at 4.75%. For a trades business running two or three people in the field, that is a real labour cost increase arriving in 27 days. The instinct is to absorb it and hope margins hold — but that approach rarely works. The smarter move: open an AI tool today, paste in your last ten job cards, and ask it to identify where your labour time is consistently running over your quoted hours. Most operators find two or three recurring job types bleeding time. Reprice those categories before July 1, tighten your labour allowances on standard quotes, and update your rate card to reflect the new cost baseline. Thirty minutes with AI this week could protect your margin for the entire second half of the financial year.",

    # Fun Facts
    "{{FACT_1}}": "Tungsten has the highest melting point of any pure metal at 3,422 degrees Celsius — hotter than the sun's surface during solar flares — making it the only material suitable for incandescent light bulb filaments and rocket nozzle throats. It was first isolated in 1783 by Spanish brothers Juan and Fausto Elhuyar, who named it from the Swedish 'tung sten' meaning 'heavy stone.'",

    "{{FACT_2}}": "The word 'deadline' originated in the American Civil War — a literal line marked around a prison camp, beyond which escaping prisoners would be shot on sight. It did not appear in a print publishing context until the early 1920s, and took another decade before it entered mainstream business use.",

    "{{FACT_3}}": "Caffeine is the world's most widely consumed psychoactive substance — roughly 80 per cent of the global adult population uses it daily. It works by blocking adenosine receptors that signal drowsiness, with effects peaking 30 to 60 minutes after consumption. Its half-life of 5 to 6 hours means half the caffeine from a 3pm coffee is still circulating in your brain at 9pm.",

    # Joke
    "{{JOKE_SETUP}}": "Why do building certifiers make the worst house guests?",
    "{{JOKE_PUNCHLINE}}": "They won't leave until they've signed off on everything.",

    # Closing
    "{{CLOSING_QUOTE}}": "“If everything seems under control, you’re not going fast enough.”",
    "{{CLOSING_ATTR}}": "— Mario Andretti",
    "{{CLOSING_MESSAGE}}": "Cold front rolling through Carrum Downs today with up to 30mm of rain possible and a feels-like temperature around 7 to 9 degrees — a good day to stay off exposed sites and push through paperwork, quotes, and that rate card update before the wage rise hits. The Fair Work Commission's decision gives you 27 days to reprice before award rates jump on July 1. A wet Thursday can be a productive one if you treat it that way. Have a sharp one, Liall.",
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
