#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 05 November 2026',
'{{WEATHER_1}}': 'THU 5 NOV · 🌥️ Cloudy, a few early sprinkles · about 17°C',
'{{WEATHER_2}}': 'FRI 6 NOV · 🌦️ Mostly cloudy, afternoon showers likely · about 22°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SAT 7 NOV · ⛈️ Wet and cool, isolated thunderstorms · about 14°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SUN 8 NOV · 🌤️ Mostly dry, sun later · about 16-17°C',
'{{WEATHER_5}}': 'MON 9 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Saturday is the one to plan around, with the most rain, the coolest temperatures and isolated thunderstorms. Friday is the warmest day but showery by afternoon. These are greater Melbourne figures from several forecast sites (timeanddate, AccuWeather, Weather Underground), not a Carrum Downs BoM page, and I couldn't confirm Monday, so check BoM before scheduling outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 SPAIN',
'{{WORLD_1_HEADLINE}}': "Spain's Transport Minister Resigns After Second Deadly Train Crash in a Year",
'{{WORLD_1_SUMMARY}}': "Óscar Puente quit on Tuesday after the high-speed collision near Toledo that killed 69 people, saying a transport minister can't stay after two accidents this severe in under a year. He is also withdrawing from the PSOE list for the 29 November snap election. Death tolls vary between outlets.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/11/4/spanish-transport-minister-resigns-after-train-crash-killed-69-people',
'{{WORLD_2_FLAG}}': '🌍 US · MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'Trump Says US Will Stop Giving Israel US$4 Billion a Year in Military Aid',
'{{WORLD_2_SUMMARY}}': "Democracy Now's 4 November headlines report the US will end the annual military aid but keep selling Israel weapons. It lands as US midterm results come in and the Iran conflict continues. I only saw the headline summary, so check the source for detail.",
'{{WORLD_2_URL}}': 'https://www.democracynow.org/2026/11/4/headlines',
'{{ECON_1_FLAG}}': '🏦 RBA',
'{{ECON_1_HEADLINE}}': 'RBA Lifts Cash Rate to 4.85% on Cup Day, Its Fifth Hike This Year',
'{{ECON_1_SUMMARY}}': "The board split 6-3, with three members preferring to hold at 4.60%. It's the highest cash rate since 2008, and the RBA expects inflation to stay elevated into 2027. If your business has equipment finance or an overdraft, expect repayments to rise.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/news/2026-11-03/rba-interest-rates-markets-live-coverage/107338216',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Petrol Holds Near 237 Cents a Litre, Diesel Around 280',
'{{ECON_2_SUMMARY}}': "The AIP's weekly report to 1 November put the national average petrol price at 237.4 cents, with wholesale rising. NRMA expects petrol to hover in the mid-230s this week, and diesel is around 281 cents in Sydney. These are national and Sydney figures, not Melbourne bowser prices.",
'{{TECH_1_FLAG}}': '🤖 AI · ANTHROPIC',
'{{TECH_1_HEADLINE}}': 'Anthropic Is Building an Open System to Prove Which AI Model Wrote a Piece of Text',
'{{TECH_1_SUMMARY}}': "TechCrunch reports researchers released a technical specification and working code to verify that an output came from a particular model. It's research only, with no plans to deploy it yet, but it points to a future where you can check whether AI-written material is genuine.",
'{{TECH_1_URL}}': 'https://techcrunch.com/2026/11/03/anthropic-is-working-on-a-system-to-prove-ai-models-identity',
'{{TECH_2_FLAG}}': '🤖 AI · CODING TOOLS',
'{{TECH_2_HEADLINE}}': "Google's Android Studio Now Works With Third-Party AI Coding Agents Like Claude and Codex",
'{{TECH_2_SUMMARY}}': "Via the open Agent Client Protocol, developers can use outside AI agents inside Android Studio. It's aimed at app builders, but it shows AI tools becoming interchangeable. Reported by an AI news aggregator, so I haven't checked Google's own announcement.",
'{{ROBOT_1_FLAG}}': '🤖 LOGISTICS ROBOTS',
'{{ROBOT_1_HEADLINE}}': 'Boston Dynamics Launches Stretch Gen 2, Its Next-Generation Trailer-Unloading Robot',
'{{ROBOT_1_SUMMARY}}': "The redesign targets uptime and simpler maintenance in high-volume logistics, where Stretch unloads trailers on its own. It's a warehouse machine rather than anything for a workshop, but it shows where heavy repetitive lifting is heading. From Boston Dynamics' own announcement on 3 November.",
'{{ROBOT_1_URL}}': 'https://bostondynamics.com/news/boston-dynamics-launches-next-generation-stretch-robot',
'{{AUS_1_HEADLINE}}': 'High Court Hears Challenge to Under-16 Social Media Ban',
'{{AUS_1_SUMMARY}}': 'Reddit and the Digital Freedom Project argue the law burdens political communication, while the government says the burden is modest and aimed at addictive design features. It conceded many under-16s have dodged age checks. The ban stays in force and judgment is pending.',
'{{AUS_1_URL}}': 'https://www.ibtimes.com.au/high-court-hears-australia-under-16-social-media-ban-challenge-1877797',
'{{AUS_2_HEADLINE}}': "Angus Taylor Says PM and Treasurer Are 'in Denial' on the Economy After Rate Hike",
'{{AUS_2_SUMMARY}}': "The Opposition Leader argues government spending is too high and needs cutting to ease demand, while Jim Chalmers rejects blame for the hike. From the ABC's 4 November federal politics blog, so this is political argument rather than settled fact.",
'{{VIC_1_HEADLINE}}': 'Victorian Election Promise Tracker: Labor Pledges 10 Free Public Dental Clinics',
'{{VIC_1_SUMMARY}}': "The Carroll government's $230 million pledge covers seven clinics in Melbourne and three in regional Victoria, per the ABC's 4 November tracker. The state election is on 28 November, so expect plenty more promises.",
'{{SCI_1_FLAG}}': '🦟 BIOLOGY',
'{{SCI_1_HEADLINE}}': "Different Mosquito Species Are Drawn to Different People's Scent",
'{{SCI_1_SUMMARY}}': 'A study of 119 people and three common mosquito species found each species ranks individuals differently, and no one person attracted all three. This may explain why some people get bitten more. Reported by SciTechDaily on 3 November; the underlying paper may be earlier.',
'{{INSIGHT_TITLE}}': 'Let AI Turn Your Equipment Service Log Into a Maintenance Calendar',
'{{INSIGHT_BODY}}': 'Breakdowns cost more than servicing, and finance costs are rising, so unplanned downtime hurts. Paste your service dates, hours and manufacturer intervals for each compressor, hose and pump into an AI tool and ask for a simple calendar with reminders a week ahead. Check it against the manuals, since the AI only knows what you give it. Ten minutes of setup can keep a surprise failure from landing on a busy week.',
'{{FACT_1}}': "Australia's High Court was told nearly 5 million social media accounts have been blocked on 10 platforms since the under-16 ban began.",
'{{FACT_2}}': "Spain's snap general election is on 29 November, less than four weeks after its transport minister quit over the train crashes.",
'{{FACT_3}}': 'ROBOTWORLD 2026, running 4 to 7 November in Goyang, South Korea, features 402 exhibitors from 17 countries.',
'{{JOKE_SETUP}}': "Why did the glass-fitter's quotes always include a validity date?",
'{{JOKE_PUNCHLINE}}': '"Because he\'d learned the hard way that prices, like windows, can crack if you leave them out in the weather too long."',
'{{CLOSING_QUOTE}}': '"If you fail to plan, you are planning to fail."',
'{{CLOSING_ATTR}}': '— Benjamin Franklin',
'{{CLOSING_MESSAGE}}': "Rates are up again after Cup Day, so it's a good Thursday to check your quote terms and finance costs. Friday is the warmest day but showery, and Saturday looks cool and wet with possible thunderstorms, so get the outdoor jobs done early.",
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
