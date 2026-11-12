#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 13 November 2026',
'{{WEATHER_1}}': 'FRI 13 NOV · ☁️ Overcast and mild, about 13-19°C, mostly dry, sprinkles possible late',
'{{WEATHER_2}}': 'SAT 14 NOV · 🌦️ Light drizzle or a shower or two, about 13-18°C, 1-2 mm',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SUN 15 NOV · 🌦️ Light drizzle or a shower or two, about 11-18°C, up to 2 mm',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'MON 16 NOV · ☁️ Cloudy and cool, about 10-16°C',
'{{WEATHER_5}}': 'TUE 17 NOV · ⛅ Cloudy, about 9-19°C, 20-40% chance of a shower',
'{{WEATHER_ALERT}}': "Today looks like the last mostly dry day before a damp, drizzly weekend, so get any outdoor coating work done today. Next week starts cool and cloudy. These are Melbourne figures from search snippets of weather-au.com, WillyWeather and BoM pages, some of them old, not a Carrum Downs forecast. Check BoM before booking weekend jobs.",
'{{WORLD_1_FLAG}}': '🌍 UKRAINE',
'{{WORLD_1_HEADLINE}}': 'US Envoys Meet Putin in the Kremlin, Then Fly to Dublin to See Zelensky',
'{{WORLD_1_SUMMARY}}': "NPR and CBC report Steve Witkoff and Jared Kushner met Vladimir Putin for about two hours on 12 November, after the Abu Dhabi talks ended with a prisoner swap and little else. Kushner said one aim was getting Putin to agree to European representatives joining talks on wider European security. The envoys then flew to Dublin to meet Zelensky, with Europeans expected to join. I only saw search summaries.",
'{{WORLD_1_URL}}': 'https://www.npr.org/2026/11/12/nx-s1-6038809/us-envoys-meet-putin-russia-ukraine-war-talks',
'{{WORLD_2_FLAG}}': '🌍 UNITED STATES',
'{{WORLD_2_HEADLINE}}': 'Brooklyn Building Collapse Kills at Least Eight, Including Two Children',
'{{WORLD_2_SUMMARY}}': "A three-storey building in Flatbush, Brooklyn, collapsed into a neighbouring construction site on 11 November. ABC News (US) reports at least eight dead, including two children, and 17 to 18 injured, among them firefighters. City building inspectors are checking the stability of nearby buildings. It's a grim reminder of how much can go wrong when excavation runs beside an old structure. Figures were still changing when I checked.",
'{{WORLD_2_URL}}': 'https://abcnews.com/US/rescue-operations-underway-after-building-collapses-brooklyn-new/story?id=138059620',
'{{ECON_1_FLAG}}': '🛢️ OIL',
'{{ECON_1_HEADLINE}}': 'Brent Climbs Back Toward US$94 After Trump Says the US No Longer Needs an Iran Deal',
'{{ECON_1_SUMMARY}}': "Yahoo Finance had Brent at US$94.58 a barrel early on 12 November (US time), and Oilprice.com reports it briefly hit about US$94 after Trump's comments. That's up from about US$89 on Tuesday, though still well below the late-October high of about US$118. Rising OPEC+ output is pulling the other way, so expect diesel prices to keep wobbling for a while yet.",
'{{ECON_1_URL}}': 'https://finance.yahoo.com/energy/articles/current-price-oil-november-12-120000703.html',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Wholesale Diesel Keeps Easing, but Pump Prices Lag Behind',
'{{ECON_2_SUMMARY}}': "AIP terminal gate prices show Sydney diesel at 252.6 cents a litre on 12 November, down from 259.2 on 6 November, with petrol falling faster to 200.3. Other capitals show similar drops. Retail diesel was still averaging about 278 cents nationally on 7 November, per IBTimes. With crude bouncing again this week, the wholesale fall may slow, so fill the ute when you see a good price.",
'{{TECH_1_FLAG}}': '🤖 AI · CHIPS',
'{{TECH_1_HEADLINE}}': 'Nvidia CEO Jensen Huang Resigns; CFO Colette Kress Steps In as Interim Boss',
'{{TECH_1_SUMMARY}}': "Nvidia's board announced on 12 November that Huang has resigned as CEO, president and director, effective immediately. CFO Colette Kress is interim CEO and former Synopsys chief Harvey Jones becomes Nvidia's first chairman. Nvidia gave no reason, but media reports link it to an affair with a woman US agencies suspect of spying for China. Shares fell more than 11%. Nvidia makes most of the chips behind today's AI tools.",
'{{TECH_1_URL}}': 'https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition',
'{{TECH_2_FLAG}}': '🤖 AI · WORKPLACE',
'{{TECH_2_HEADLINE}}': 'Canberra Releases a Draft Best-Practice Guide for Using AI at Work',
'{{TECH_2_SUMMARY}}': "Employment Minister Amanda Rishworth released the voluntary draft guide on 12 November, built around three themes (Plan, Enable, Embed) and eight principles. It came out of months of talks with unions and employer groups, with input from Microsoft, CommBank, Kmart and Telstra. Rishworth says the key is trust with workers. Public consultation is open until 27 January 2027 at consultations.dewr.gov.au.",
'{{ROBOT_1_FLAG}}': '🦾 HUMANOID ROBOTS',
'{{ROBOT_1_HEADLINE}}': 'J.P. Morgan Says US Humanoid Robot Output Could Hit 400,000 a Year by 2030',
'{{ROBOT_1_SUMMARY}}': "Reuters reports the bank expects 300,000 to 400,000 US-made humanoids a year by 2030 and about 1.5 million by 2035, driven by labour shortages in manufacturing, logistics and warehousing. It says the main bottlenecks are hands, actuators, the robot's 'brain' and factory capacity, and that costs are nearing parity with labour. A multi-shift robot could save a customer about US$100,000 a year.",
'{{ROBOT_1_URL}}': 'https://ca.investing.com/news/stock-market-news/us-humanoid-robot-production-could-hit-400000-by-2030-as-deployment-ramps-jp-morgan-says-4951895',
'{{AUS_1_HEADLINE}}': '$88 Million to Lure Tradies Into Building Nuclear Submarines',
'{{AUS_1_SUMMARY}}': "Defence Minister Richard Marles launched the 2026 Nuclear-Powered Submarine Workforce Strategy at HMAS Stirling on 12 November. The $88 million funds two programs, Tradie2Trainer and the Professional Submarine Pathways Program, to support at least 275 apprentices and trainees in WA and SA over six years. AAP says the aim is to move carpenters, plumbers and sparkies into submarine work. Expect more competition for skilled trades.",
'{{AUS_1_URL}}': 'https://www.minister.defence.gov.au/media-releases/2026-11-12/building-workforce-delivering-australias-future-nuclear-powered-submarine-capability',
'{{AUS_2_HEADLINE}}': 'New $76 Million Hub to Tackle Online Youth Extremism on Gaming Platforms',
'{{AUS_2_SUMMARY}}': "The ABC reports a new federal counterterrorism centre in Sydney will bring ASIO and the AFP together to intercept youth radicalisation on platforms such as Discord and Roblox. Home Affairs Minister Tony Burke called it the government's first dedicated hub for online extremism. Children make up 40 per cent of Australia's counterterrorism caseload this year. I only saw search summaries.",
'{{VIC_1_HEADLINE}}': 'Businesses and Unions Slam Labor Over $1.3 Billion WorkCover Grab',
'{{VIC_1_SUMMARY}}': "The pre-election budget update counts $1.3 billion from WorkSafe toward the state's bottom line. The Australian Industry Group says it was stunned, given businesses already paid heavily through premiums, and Trades Hall's Luke Hilakari says the surplus is built by taking money from injured workers. For small employers it's worth watching: premiums rose sharply after the 2024 WorkCover reforms. Victorians vote on 28 November.",
'{{SCI_1_FLAG}}': '❤️ HEALTH SCIENCE',
'{{SCI_1_HEADLINE}}': 'Energy Drinks and Stimulant Supplements Linked to 11 Times More Cardiac Arrest Reports',
'{{SCI_1_SUMMARY}}': "A preliminary study presented at the American Heart Association's Scientific Sessions in Chicago reviewed more than 28,000 US FDA adverse-event reports from 2017 to 2025. Reports involving caffeinated energy drinks or stimulant supplements were about 11 times more likely to mention cardiac arrest and 4.5 times more likely to mention a heart attack. About 45% involved people aged 18 to 34. It shows an association, not proof of cause.",
'{{INSIGHT_TITLE}}': 'Use AI to Write a One-Page AI Rules Sheet for Your Crew',
'{{INSIGHT_BODY}}': "With Canberra's draft guide on AI at work out this week, it's a good time to set a few simple rules in your own business. Ask an AI tool to draft a one-page sheet covering what staff can use it for (quotes, emails, SWMS drafts), what they must never paste in (client details, pricing, bank info), and that a person always checks anything before it goes to a customer. Read it, cut what doesn't fit, and go through it at the next toolbox talk. Ten minutes now beats cleaning up a privacy mistake later.",
'{{FACT_1}}': "Children make up 40 per cent of Australia's counterterrorism caseload this year, according to reporting on the new $76 million online extremism hub.",
'{{FACT_2}}': "Some pre-workout supplements contain more than 12 times as much caffeine per fluid ounce as brewed coffee, according to the American Heart Association.",
'{{FACT_3}}': "Nvidia has never had a separate chairman before: former Synopsys CEO Harvey Jones became its first on 12 November.",
'{{JOKE_SETUP}}': "Why did the electrician turn up on Friday the 13th without a worry in the world?",
'{{JOKE_PUNCHLINE}}': '"Because the only thing he\'s superstitious about is a wire someone swore was dead."',
'{{CLOSING_QUOTE}}': '"Shallow men believe in luck. Strong men believe in cause and effect."',
'{{CLOSING_ATTR}}': '— Ralph Waldo Emerson',
'{{CLOSING_MESSAGE}}': "It's Friday the 13th, but luck has nothing to do with it: today is overcast and mostly dry before a drizzly weekend, so get the outdoor work wrapped up early. Oil is back near US$94, so keep an eye on diesel, and have a good weekend.",
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
