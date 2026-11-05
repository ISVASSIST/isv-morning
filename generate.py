#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 06 November 2026',
'{{WEATHER_1}}': 'FRI 6 NOV · 🌧️ Showers, 70% chance of rain · about 22-23°C',
'{{WEATHER_2}}': 'SAT 7 NOV · ⛈️ Showers very likely, possible thunderstorm, small hail in SE suburbs',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SUN 8 NOV · ☁️ Cloudy, much lower rain chance · about 16-17°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'MON 9 NOV · ☀️ Sunny · about 21°C',
'{{WEATHER_5}}': 'TUE 10 NOV · 🌤️ Partly cloudy · about 26-27°C',
'{{WEATHER_ALERT}}': "Saturday is the day to plan around, with showers very likely and a possible early-afternoon thunderstorm, and BoM says small hail is possible in the south-east suburbs, which includes Carrum Downs. Friday is showery too. Monday and Tuesday look much better. These are BoM Melbourne figures as issued 4 November, not a Carrum Downs page, and the Saturday max temperature wasn't confirmed, so check BoM before scheduling outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 EUROPE',
'{{WORLD_1_HEADLINE}}': 'Bomb Threats Force Diversion of Flights Across Europe for a Second Time in a Week',
'{{WORLD_1_SUMMARY}}': "CNN's live coverage on 5 November reports more than a dozen flights were diverted after bomb threats, with Czech police saying four planes heading to Prague were threatened. Several authorities say no devices have been found. Details were still changing when I checked.",
'{{WORLD_1_URL}}': 'https://www.cnn.com/2026/11/05/world/live-news/plane-flights-bomb-threats-europe-intl',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'Iran Says Two Oil Tankers and a Tug Caught Fire in the Strait of Hormuz',
'{{WORLD_2_SUMMARY}}': "Iran's Revolutionary Guard says the vessels burned in separate incidents after trying to use unauthorised routes through the strait. I only saw this in a wire headline roundup (NPR's news page), so treat the cause as Iran's claim rather than confirmed fact.",
'{{WORLD_2_URL}}': 'https://www.npr.org/sections/news/',
'{{ECON_1_FLAG}}': '🏦 SMALL BUSINESS',
'{{ECON_1_HEADLINE}}': "Small Business Groups Say Buffers Are 'Running Low' After the RBA Hike",
'{{ECON_1_SUMMARY}}': "COSBOA says small businesses are squeezed three ways: weaker customer spending, dearer business loans and higher mortgage costs for owners. It wants the government to cut spending and red tape in the mid-year budget update. Employment Hero warned the hike could hurt Christmas trade.",
'{{ECON_1_URL}}': 'https://www.news24.com.au/latest/small-businesses-call-for-federal-government-cut-spending-and-red-tape-after-rba-rate-hike/news-story/df1d1f8b929728afa6517e4d0bdc6b80',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Wholesale Fuel Prices Easing This Week, Which May Soon Flow Through to the Bowser',
'{{ECON_2_SUMMARY}}': "AIP terminal gate prices in Sydney fell from 226.5 to 217.8 cents for unleaded and from 269.1 to 260.9 for diesel between 30 October and 5 November. NRMA's outlook was mixed, so there's no guarantee pump prices follow. These are Sydney wholesale figures, not Melbourne bowser prices.",
'{{TECH_1_FLAG}}': '🤖 AI · OPENAI',
'{{TECH_1_HEADLINE}}': 'OpenAI Lists Plan to Acquire Pierre Computer Company',
'{{TECH_1_SUMMARY}}': "OpenAI's news page carries an item dated 4 November about acquiring Pierre Computer Company, Inc. I couldn't find any coverage explaining what the company does or the price, so check the source before relying on it.",
'{{TECH_1_URL}}': 'https://openai.com/news/',
'{{TECH_2_FLAG}}': '🤖 AI · DATA CENTRES',
'{{TECH_2_HEADLINE}}': 'TeraWulf Announces Google Credit Support for a Data Centre Being Built for Anthropic',
'{{TECH_2_SUMMARY}}': "The deal reportedly backs a data centre build for Anthropic, another sign of how much physical infrastructure sits behind AI tools. This came from a secondary news digest, not a company filing, so details are unconfirmed.",
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS INDUSTRY',
'{{ROBOT_1_HEADLINE}}': "The Robot Report Publishes Its Second Annual Robotics Startup Radar",
'{{ROBOT_1_SUMMARY}}': "The 4 November report spotlights new companies developing commercial robotics and related technologies. It's a useful look at which robot makers are emerging, though I only saw the introduction, not the full list.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/robotics-startup-radar-2026/',
'{{AUS_1_HEADLINE}}': 'While Albanese Is at CHOGM, Issues Pile Up Back Home',
'{{AUS_1_SUMMARY}}': "ABC's weekly politics wrap says Chalmers is under pressure to find budget savings before the mid-year update, and a frontbench reshuffle is possible. It also reports Albanese did not secure tighter work rules in the UK trade deal talks. Analysis, not settled fact.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-05/albanese-chogm-week-in-politics/107336024',
'{{AUS_2_HEADLINE}}': "Banks Lift Rates After the RBA Hike as Chalmers Promises to Be 'Helpful' on Inflation",
'{{AUS_2_SUMMARY}}': "The ABC homepage reports the Treasurer rejecting blame for the hike. The ABC estimates an extra $115 a month on a $750,000 mortgage if lenders pass on the full rise. I only saw the homepage summary, so check the full story.",
'{{VIC_1_HEADLINE}}': 'Bullet Hole Found in Victorian Election Campaign Sign',
'{{VIC_1_SUMMARY}}': "Police are investigating after a bullet hole was found in a sign for independent Benambra candidate Lachlan McKeeman in north-east Victoria. Police say it's not clear whether the shot was politically motivated. The election is on 28 November.",
'{{SCI_1_FLAG}}': '🧲 PHYSICS',
'{{SCI_1_HEADLINE}}': 'SLAC Scientists Report Experimental Proof of a Third Type of Magnetism',
'{{SCI_1_SUMMARY}}': "A study in Science reports evidence for altermagnetism, a magnetic phase combining traits of the two familiar types, ferromagnetism and antiferromagnetism. It could matter for future electronics. Reported by ScienceDaily on 4 November; I only saw the headline summary.",
'{{INSIGHT_TITLE}}': 'Let AI Turn Your Friday Job Notes Into a Clean Monday Start List',
'{{INSIGHT_BODY}}': "With Saturday looking wet and rates biting, a tidy handoff into next week saves real money. Before you knock off Friday, dump your rough notes on unfinished jobs, materials to order and customers to call into an AI tool and ask for a prioritised start list for Monday, sorted by deadline and by what weather-dependent work can go first. Read it over and fix anything wrong, since it only knows what you typed. It takes five minutes and stops Monday morning starting with a scramble.",
'{{FACT_1}}': "Tutor Intelligence has raised US$75 million in a Series B, bringing its total funding to US$117 million, to put warehouse robots it rents out by the hour to work.",
'{{FACT_2}}': "A Roy Morgan poll taken 26 to 29 October put One Nation on 22 per cent in Victoria, close behind Labor on 22.5 per cent and the Coalition on 29.5.",
'{{FACT_3}}': "The ABC estimates the RBA's latest rate rise adds about $115 a month to repayments on a $750,000 mortgage if lenders pass it all on.",
'{{JOKE_SETUP}}': "Why did the plumber's van have a calendar taped to the dashboard?",
'{{JOKE_PUNCHLINE}}': '"Because he found that jobs booked in pencil tend to leak, and he preferred his schedule watertight."',
'{{CLOSING_QUOTE}}': '"A life is not important except in the impact it has on other lives."',
'{{CLOSING_ATTR}}': '— Jackie Robinson',
'{{CLOSING_MESSAGE}}': "It's Friday with showers today and a wet, possibly stormy Saturday, so get the outdoor work finished early and use the afternoon to line up Monday, when it turns sunny. Rates just went up again, so it's also a good day to check your quote terms.",
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
