#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Sunday, 18 October 2026',
'{{WEATHER_1}}': 'SUN 18 OCT · ☀️ Sunny, 5% chance of rain · 13–26°C',
'{{WEATHER_2}}': 'MON 19 OCT · ☀️ Sunny, windy northerlies · up to about 27°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'TUE 20 OCT · 🌦️ Possible shower, 40% chance of rain · 18–27°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'WED 21 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'THU 22 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': "Sunny and warm today, 13–26°C with only a 5% chance of rain, then sunny and breezy on Monday with strong northerlies (25–40 km/h) and a top near 27°C. Tuesday is the one to watch: a possible shower and a 40% chance of rain. Figures come from Bureau of Meteorology Melbourne forecasts (Tuesday via a site relaying BOM data) and Carrum Downs may differ slightly. I could not find a confirmed outlook for Wednesday or Thursday.",
'{{WORLD_1_FLAG}}': '🌊 BLACK SEA · NATO',
'{{WORLD_1_HEADLINE}}': "Bulgaria Asks NATO for Combat Aircraft and Anti-Drone Systems After Black Sea Ship Attacks",
'{{WORLD_1_SUMMARY}}': "Just Security's 16 October Early Edition reports the request after drone strikes on commercial shipping off Bulgaria's coast, with one vessel sunk earlier this month. Ukraine blames Russia, which denies involvement. Roundup summary only, so detail is limited.",
'{{WORLD_1_URL}}': 'https://www.justsecurity.org/161058/early-edition-october-16-2026/',
'{{WORLD_2_FLAG}}': '🛢️ IRAN WAR · OIL',
'{{WORLD_2_HEADLINE}}': 'Iran Has Exported Some LPG and Jet Fuel Despite the US Naval Blockade, Reuters Sources Say',
'{{WORLD_2_SUMMARY}}': "The same 16 October roundup cites Reuters sources and shipping data, suggesting the blockade is leakier than advertised, which matters for fuel prices. It also notes reports of US strike planning against Iranian energy sites. Summary only, so treat the detail with caution.",
'{{WORLD_2_URL}}': 'https://www.justsecurity.org/161058/early-edition-october-16-2026/',
'{{ECON_1_FLAG}}': '⛽ FUEL · AUSTRALIA',
'{{ECON_1_HEADLINE}}': 'Petrol Up 5 Cents a Litre Nationally Last Week While Diesel Eases to About $2.84',
'{{ECON_1_SUMMARY}}': "FuelRadar's weekly report to 12 October has unleaded averaging 245.2 c/L (up 5.0) and diesel 284.3 c/L (down 1.5). Wholesale petrol prices were forecast to ease through 16 October, so pump prices may soften. Figures are a few days old, so check your own supplier.",
'{{ECON_1_URL}}': 'https://fuelradar.com.au/blog/weekly-fuel-report-2026-10-12',
'{{ECON_2_FLAG}}': '🚛 DIESEL · NRMA',
'{{ECON_2_HEADLINE}}': 'NRMA Expects Diesel Prices to Decrease This Week as Wholesale Prices Fall',
'{{ECON_2_SUMMARY}}': "NRMA's 12 October weekly report had Sydney diesel at 281.7 c/L and expected relief in line with falling wholesale prices. Any drop is modest against prices near $2.80, so keep fuel allowances in quotes. Report is a few days old.",
'{{TECH_1_FLAG}}': '📊 AI · OPENAI',
'{{TECH_1_HEADLINE}}': 'OpenAI Launches ChatGPT Slides With Real-Time Co-Editing and PowerPoint Export',
'{{TECH_1_SUMMARY}}': 'Reported as launching on 16 October for eligible Pro, Business and Enterprise users, with export to PowerPoint, PDF, Google Slides and Keynote. Handy for quote presentations or tender packs, but it needs a paid business plan. Seen via an aggregator, not the OpenAI announcement.',
'{{TECH_1_URL}}': 'https://aiweekly.co/ai-news-today',
'{{TECH_2_FLAG}}': '🧠 AI · GOOGLE',
'{{TECH_2_HEADLINE}}': 'Google Makes Gemini 4 Argon Broadly Available After 13 October Announcement',
'{{TECH_2_SUMMARY}}': 'An aggregator roundup lists the wider rollout of Google\'s newer Gemini model. I could not confirm the exact availability or plans from a primary source, so check what your current plan includes.',
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS · BOSTON DYNAMICS',
'{{ROBOT_1_HEADLINE}}': "Boston Dynamics Shows a New Humanoid Hand",
'{{ROBOT_1_SUMMARY}}': "The Robot Report's homepage lists the story dated 16 October. I only saw the headline, not the article, so details are unconfirmed. Hands are the hard part of making humanoids useful for real handling work.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/',
'{{AUS_1_HEADLINE}}': "Coalition and Greens Team Up to Throw Out Labor's Private Health Rebate Bill",
'{{AUS_1_SUMMARY}}': "ABC's 14 October federal politics live blog reports the bill to wind back the private health rebate for over-65s was thrown out of parliament. This is slightly outside 48 hours and I could not find anything fresher, so treat it as recent background.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-14/federal-politics-live-blog-october-14/107261908',
'{{AUS_2_HEADLINE}}': 'Albanese Government Tables 9 Per Cent Pay Offer for Public Servants',
'{{AUS_2_SUMMARY}}': "The Canberra Times reports Finance Minister Katy Gallagher called the offer fair and reasonable in a constrained fiscal environment, and the CPSU has opened a member poll. I could not confirm the publication date, so it may be older than 48 hours.",
'{{VIC_1_HEADLINE}}': 'Victorian Government Agrees In Principle to 28.3 Per Cent Teacher Pay Rise Over Four Years',
'{{VIC_1_SUMMARY}}': "The Sector reports a 12 per cent rise by October 2026 as the first step, with the state election set for 28 November. I could not confirm the publication date, so it may be older than 48 hours.",
'{{SCI_1_FLAG}}': '💊 CANCER RESEARCH',
'{{SCI_1_HEADLINE}}': 'USC Scientists Find a Way to Create a Never-Ending Supply of Cancer-Fighting Immune Cells',
'{{SCI_1_SUMMARY}}': 'ScienceDaily lists it around 15 October: growing and modifying immature immune cells rather than mature ones could let the body keep producing tumour-fighting cells. I only saw the teaser, and it is early research.',
'{{INSIGHT_TITLE}}': 'Ask AI to Reshuffle Your Week Around the Forecast and Your Fuel Runs',
'{{INSIGHT_BODY}}': "Paste your booked jobs, locations and the week's forecast into an AI tool and ask it to suggest an order that keeps outdoor work on dry days and groups jobs by area to cut fuel runs. With a shower possible Tuesday and diesel near $2.84 a litre, a few fewer kilometres adds up. The AI doesn't know your customers' deadlines or site access, so treat its plan as a first draft and adjust it yourself.",
'{{FACT_1}}': 'Cancer cells that are unusually small can be more aggressive than larger ones, according to Virginia Tech researchers.',
'{{FACT_2}}': 'Agility Robotics\' Digit humanoid runs roughly 4 hours per charge, so warehouses use a rotating fleet to cover a full shift.',
'{{FACT_3}}': 'Australia\'s federal public service pay offer on the table this week is 9 per cent, per the Canberra Times.',
'{{JOKE_SETUP}}': 'Why did the carpenter never worry about being behind schedule?',
'{{JOKE_PUNCHLINE}}': '"Because he always knew the deadline was only a rough cut."',
'{{CLOSING_QUOTE}}': '"The harder you work, the luckier you get."',
'{{CLOSING_ATTR}}': '— Gary Player',
'{{CLOSING_MESSAGE}}': "It's a sunny Sunday, 26°C and dry, so a good day to rest or get stuff done at home. Monday is windy with northerlies and Tuesday may bring a shower, and diesel is still around $2.84, so plan outdoor work and fuel runs for the week.",
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
