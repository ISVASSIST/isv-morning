#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 19 September 2026",

    # Weather — Carrum Downs / Melbourne bayside, 5-day from Sat 19 Sep
    "{{WEATHER_1}}": "SAT 19 SEP · ☀️ Sunny, winds N–NW 25–35km/h easing W–NW in the afternoon · 12–25°C",
    "{{WEATHER_2}}": "SUN 20 SEP · ☀️ Sunny, slight chance of an evening shower, winds N 25–35km/h increasing to 35–50km/h before turning westerly · 14–24°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 21 SEP · ☁️ Cloudy, medium chance of a morning shower as a cooler change comes through, winds W–SW turning S 20–30km/h · 11–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 22 SEP · 🌤️ Sunny, chance of morning frost near the hills, light winds · 8–17°C",
    "{{WEATHER_5}}": "WED 23 SEP · ☀️ Mostly sunny, light winds becoming NW–NE · 10–19°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — a breezy, sunny start to the weekend gives way to a cooler change with showers Monday morning before it clears again.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷🇺🇸 IRAN WAR · TRUMP SAYS HE'S HAD 'DIRECT' CONTACT WITH IRAN, HOPES WAR IS NEARING ITS END",
    "{{WORLD_1_HEADLINE}}": "Trump Claims Direct Contact With Iran, Says War Is 'Hopefully' Close to Over",
    "{{WORLD_1_SUMMARY}}": "Trump told reporters Iran had reached out to the US directly and wants to make a deal after seven months of war, though Tehran has not confirmed any contact and a senior Iranian official publicly rejected talks a day earlier — a reminder that ceasefire optimism and continued Middle East volatility are currently running side by side.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/9/17/trump-claims-direct-talks-with-iran-is-diplomacy-picking-up-again",

    "{{WORLD_2_FLAG}}": "🏔️ CLIMATE · STUDY LINKS DEADLY NEPAL-TIBET FLOODS TO HUMAN-CAUSED HIMALAYAN WARMING",
    "{{WORLD_2_HEADLINE}}": "Scientists Say Climate Change Was a Major Factor in the Nepal-Tibet Floods That Killed Over 1,400 People",
    "{{WORLD_2_SUMMARY}}": "A World Weather Attribution report found July–August temperatures in the region ran about 1.5°C warmer due to human-caused climate change, thinning glaciers and weakening slopes ahead of the flash floods and debris flows that devastated the Trishuli River valley on both sides of the Nepal–China border in late August.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/9/17/climate-change-had-major-role-in-triggering-nepal-floods-scientists-say",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 RATES · RBA GOVERNOR TELLS PARLIAMENT THE BANK MUST DECIDE IF RATES ARE HIGH ENOUGH",
    "{{ECON_1_HEADLINE}}": "RBA Governor Bullock Flags Inflation Risks Are Building Again as Markets Price In a 70–75% Chance of a Rate Hike Next Week",
    "{{ECON_1_SUMMARY}}": "Fronting a parliamentary economics committee, Michele Bullock said growth is slowing but pointed to the Middle East conflict, the AI boom and extreme weather as fresh upside risks to inflation, ahead of the RBA board's next meeting on 28–29 September — worth watching if you're financing a ute, compressor or new gear on variable terms.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-18/rba-governor-talks-interest-rates-at-parliamentary-hearing/107167676",

    "{{ECON_2_FLAG}}": "⛽ FUEL · DIESEL NEARS 269c A LITRE AS MIDDLE EAST ESCALATION KEEPS PUSHING PRICES UP",
    "{{ECON_2_HEADLINE}}": "National Diesel Average Climbs to Almost 269c a Litre as Middle East Shipping Disruptions Keep Fuel Costs Rising",
    "{{ECON_2_SUMMARY}}": "Diesel is now averaging close to 268.9c a litre nationally and unleaded around 225.4c, both up sharply over the past fortnight as fighting around the Bab el-Mandeb and Strait of Hormuz shipping routes squeezes oil supply — Victoria's average is still the cheapest of any state, but the fuel line on every quote is worth another look.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI DEVELOPMENT · ANTHROPIC SAYS CLAUDE NOW LEADS A QUARTER OF ITS OWN R&D",
    "{{TECH_1_HEADLINE}}": "Anthropic Says Its Claude Model Is Now Helping Build the Next Version of Itself",
    "{{TECH_1_SUMMARY}}": "Anthropic revealed Claude is completing most of its assigned research and development tasks 'end-to-end from a high-level prompt' under human supervision, now leading about 26% of the company's model R&D work — up from zero in February — a fast-moving sign of how much repeatable technical work can already be handed to an AI system with the right oversight.",
    "{{TECH_1_URL}}": "https://www.nbcnews.com/tech/tech-news/anthropic-says-model-claude-helping-build-next-version-rcna598494",

    "{{TECH_2_FLAG}}": "🔓 AI SECURITY · RESEARCHERS USED CLAUDE TO BREACH A RIVAL AI LAB'S PRIVATE SYSTEMS",
    "{{TECH_2_HEADLINE}}": "Security Researchers Used Anthropic's Claude to Penetrate OpenAI's Private Software Systems in a Bug Bounty Test",
    "{{TECH_2_SUMMARY}}": "Independent researchers used Claude to gain access to an OpenAI employee's account and reach the company's private GitHub service, then stopped and reported the find rather than dig further — a useful reminder that today's AI tools are already capable enough to expose weak passwords and reused logins in any small business's own systems.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 HUMANOID ROBOTS · CHINA'S AGIBOT OVERTAKES UNITREE AS TOP GLOBAL SHIPPER",
    "{{ROBOT_1_HEADLINE}}": "Agibot Claims Top Spot in Global Humanoid Robot Shipments as First-Half Volumes Nearly Quadruple",
    "{{ROBOT_1_SUMMARY}}": "Global humanoid robot shipments surged to more than 22,000 units in the first half of 2026 — up almost 300% on last year — with Shanghai's Agibot overtaking Unitree to lead the market on the back of industrial and commercial deployments, underlining how fast this technology is scaling even before it reaches a job site anywhere near Carrum Downs.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/09/18/agibot-claims-top-spot-in-global-humanoid-robot-shipments-in-first-half-of-2026/104930/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia and New Zealand Could Follow Canada Into a New 'Associate Member' Status With the EU",
    "{{AUS_1_SUMMARY}}": "European Parliament President Roberta Metsola floated Australia and New Zealand as candidates for a still-undefined 'associate membership' status with the EU, days after Ursula von der Leyen made the same offer to Canada — though New Zealand says no such talks have actually started.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-18/mark-carney-canada-associate-member-eu-welcome/107166490",

    "{{AUS_2_HEADLINE}}": "Australia's Flu Season Peaks Unusually Late, But Total Cases Running Well Below Last Year's Toll",
    "{{AUS_2_SUMMARY}}": "Health authorities say this year's influenza surge has arrived later than usual across several states, but a more effective vaccine match means the overall case count is tracking well below 2025's record toll of more than 1,700 flu-related deaths.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "650+ Young Musicians Take Over Queen Victoria Market for Melbourne Youth Orchestras' 'Big Busk'",
    "{{VIC_1_SUMMARY}}": "More than 650 young musicians perform today across a main stage and multiple busking spots at Queen Victoria Market as part of Melbourne Youth Orchestras' annual Big Busk — one of several free events on this weekend, alongside the Chinese Traditional Cultural Festival's return to Fed Square.",

    # Science
    "{{SCI_1_FLAG}}": "🌌 PHYSICS · A $100 POCKET DETECTOR REVEALS THE COSMIC PARTICLES RAINING THROUGH YOU RIGHT NOW",
    "{{SCI_1_HEADLINE}}": "MIT-Designed $100 Detector Shows the Invisible Stream of Cosmic Particles Passing Through All of Us",
    "{{SCI_1_SUMMARY}}": "CosmicWatch, a pocket-sized muon detector built from around $100 of parts by MIT's Spencer Axani, started as a student project and is now used everywhere from high school classrooms to professional physics experiments and balloon missions — a neat reminder that a shower of invisible cosmic particles passes through your body every second of every day, including this one.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Claude Is Now Helping Write Its Own Next Version — What That Says About Handing Over Repeat Work",
    "{{INSIGHT_BODY}}": "Anthropic says its Claude model now leads about a quarter of the company's own research and development work, running many tasks end-to-end from a single prompt with a human checking the result — up from doing none of that work back in February. You don't need to be training AI models to take the lesson: the same pattern of 'let AI run the repeatable bit, then look over the output' is exactly how a one-truck or one-office trades business gets the most out of AI right now, whether that's drafting quotes, chasing overdue invoices or turning yesterday's job notes into today's paperwork. Start with one task you already do the same way every time, let AI take the first pass, and keep checking the work until you trust it enough to check less often.",

    # Fun facts
    "{{FACT_1}}": "The Melbourne Cricket Ground, where this year's AFL Grand Final will be played on 26 September after Fremantle's stunning comeback win over Sydney, can hold more than 100,000 people — roughly double the entire population of Hobart.",
    "{{FACT_2}}": "A shower of subatomic particles called muons, created when cosmic rays slam into Earth's upper atmosphere, is passing through your body at a rate of roughly one per second right now — completely harmless, and detectable with a hobbyist device costing about $100.",
    "{{FACT_3}}": "The first CCTV system was installed in Germany in 1942 by Siemens engineer Walter Bruch, so military officials could watch V-2 rocket launches from a safe distance without risking a camera operator's life.",

    # Joke
    "{{JOKE_SETUP}}": "A security camera installer was asked how his small business always managed to win back a customer who'd started shopping around for a cheaper quote.",
    "{{JOKE_PUNCHLINE}}": "He said he never let a client walk away without keeping half an eye on the relationship.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Everything you've ever wanted is on the other side of fear.\"",
    "{{CLOSING_ATTR}}": "— George Addair",
    "{{CLOSING_MESSAGE}}": "It's Saturday, and Carrum Downs should get a breezy, sunny start to the weekend before a cooler change moves through with showers on Monday morning — good timing if there's an outdoor job on the books today. Grand Final fever is officially on after Fremantle's escape act at the SCG, and it might be worth a beat to see whether handing Claude one repeatable admin task this weekend, the way Anthropic says it's now doing with its own R&D, could free up an hour before Monday hits.",
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
