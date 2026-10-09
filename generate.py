#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 10 October 2026',
'{{WEATHER_1}}': 'SAT 10 OCT · ⛅ Mostly dry, 20% chance of an early shower · 15–21°C',
'{{WEATHER_2}}': 'SUN 11 OCT · 🌤️ Fair to partly cloudy, dry · 12–23°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'MON 12 OCT · ⛈️ Showers very likely, afternoon thunderstorm possible',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'TUE 13 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'WED 14 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': 'Saturday and Sunday look mostly dry and mild, a good window for outdoor coating work. Monday turns wet, with showers very likely and a possible afternoon thunderstorm. Based on Bureau of Meteorology and Yr.no Melbourne forecasts, so Carrum Downs may differ slightly, and Tuesday and Wednesday could not be confirmed.',
'{{WORLD_1_FLAG}}': '🌊 HORMUZ · IRGC STRIKES TANKER',
'{{WORLD_1_HEADLINE}}': 'Iran\'s IRGC Strikes Tanker and Threatens to Target Vessels Beyond Hormuz',
'{{WORLD_1_SUMMARY}}': 'Euronews reports the latest tanker strike and a threat to extend attacks past the Strait of Hormuz. CNBC says tanker attacks have hit a wartime high, with eleven ships targeted in the week to 4 October. Shipping risk here flows straight into diesel and freight costs.',
'{{WORLD_1_URL}}': 'https://www.euronews.com/2026/10/09/irans-irgc-strikes-tanker-and-threatens-to-target-vessels-beyond-hormuz',
'{{WORLD_2_FLAG}}': '🇺🇸 IRAN WAR · MIDTERMS PRESSURE',
'{{WORLD_2_HEADLINE}}': 'Trump Promises Not to Resume Strikes on Iran Before the US Midterm Elections',
'{{WORLD_2_SUMMARY}}': 'Oil backed off its highs after the pledge, though NBC, citing unnamed sources, reported strikes are still being considered for the coming weeks. The Washington Post says Iran\'s stepped-up Hormuz attacks are piling pressure on the White House ahead of the November vote.',
'{{WORLD_2_URL}}': 'https://www.cbsnews.com/live-updates/iran-war-nuclear-donald-trump-vance-rubio-strait-of-hormuz/',
'{{ECON_1_FLAG}}': '⛽ FUEL · ACCC WEEKLY UPDATE',
'{{ECON_1_HEADLINE}}': 'ACCC: Petrol Prices Edge Up and Diesel Edges Down Over the Past Week, Tracking International Benchmarks',
'{{ECON_1_SUMMARY}}': 'The ACCC\'s 9 October update says the moves broadly reflect international fuel benchmarks. Terminal gate diesel on 8 October was about 265 cents a litre in Sydney, slightly lower than a week earlier. Brent still closed at US$104.28 on Thursday, so keep a fuel line in your quotes.',
'{{ECON_1_URL}}': 'https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update',
'{{ECON_2_FLAG}}': '💱 AUD · DOLLAR SLIPS TO 69.6c',
'{{ECON_2_HEADLINE}}': 'Australian Dollar Falls to About US69.6 Cents, Down 3.6% Over the Past Month',
'{{ECON_2_SUMMARY}}': 'Trading Economics has AUD/USD at 0.6959 on 9 October. A softer dollar makes imported materials, consumables and fuel dearer in Australian dollars, so check supplier price lists before locking in fixed-price quotes.',
'{{TECH_1_FLAG}}': '🤖 AI · GEMINI GOES AGENTIC',
'{{TECH_1_HEADLINE}}': 'Google Brings Agentic AI to Gemini, Starting With Businesses',
'{{TECH_1_SUMMARY}}': 'At a Google Cloud event on Thursday, Google said Gemini can now plan and carry out multi-step work across business apps, with its own workplace identity including an email address. Powerful, but treat any agent like a new hire and limit what it can access.',
'{{TECH_1_URL}}': 'https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/',
'{{TECH_2_FLAG}}': '🚗 AI · HELM.AI CONTRACTS',
'{{TECH_2_HEADLINE}}': 'Helm.ai Reaches US$70 Million in Signed Commercial Contracts',
'{{TECH_2_SUMMARY}}': 'The Robot Report says the autonomous driving software company has hit US$70M in signed commercial contracts, a sign that practical AI for vehicles is moving from demos into paid deployments.',
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · HUMANOIDS TO MASS PRODUCTION',
'{{ROBOT_1_HEADLINE}}': 'Jabil Discusses the Pace of Humanoid Robot Development and Production',
'{{ROBOT_1_SUMMARY}}': 'Jabil, the manufacturing services provider working with Apptronik, says humanoids are moving from prototypes toward mass production, with Tesla, 1X, XPeng and UBTECH all preparing to ramp up. It is commentary rather than a product launch, but it shows where the supply chain is heading.',
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/jabil-discusses-pace-humanoid-robot-development-production/',
'{{AUS_1_HEADLINE}}': 'AFL Approves Five-Club Trade as Zak Butters Moves to the Bulldogs',
'{{AUS_1_SUMMARY}}': 'The deal involves Port Adelaide, the Western Bulldogs, Melbourne, Carlton and Hawthorn, and Ben King\'s move to Hawthorn is also done. Plenty of footy talk for the smoko room.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-09/afl-trade-period-live-blog-friday-october-9/107243946',
'{{AUS_2_HEADLINE}}': 'Sydney\'s Nick Blakey Reportedly Chooses North Melbourne, With Trade Terms Still to Be Worked Out',
'{{AUS_2_SUMMARY}}': 'Reports say Blakey has nominated the Kangaroos, and the Swans and North Melbourne must now agree what a trade looks like before the window closes.',
'{{VIC_1_HEADLINE}}': 'Seaford Man Charged After Police Pursuit Through Melbourne\'s South-East',
'{{VIC_1_SUMMARY}}': 'Police say the 31-year-old was spotted in a car with false registration plates in Chadstone before the pursuit. Worth a thought if you are on the roads in the south-east this weekend.',
'{{SCI_1_FLAG}}': '🪸 OCEAN · NEW CORAL FAMILY',
'{{SCI_1_HEADLINE}}': 'Yellow Deep-Sea Coral Off Costa Rica Is So Unusual Scientists Created a New Family for It',
'{{SCI_1_SUMMARY}}': 'ScienceDaily reports on 8 October that the coral was different enough from known groups to need its own family, a reminder of how much of the deep ocean is still unexplored.',
'{{INSIGHT_TITLE}}': 'Treat Your AI Agent Like a New Apprentice: Give It a Narrow Job and Limited Access',
'{{INSIGHT_BODY}}': 'Google has just launched Gemini agents for businesses that can run multi-step tasks across your apps and even have their own email address. For a small trades business, that could mean an agent that chases overdue invoices or books site visits, but it also means a new set of logins that can email your customers. Start the way you would with a new apprentice: one narrow job, such as sending polite payment reminders, access only to the files it needs, and a rule that you read what it sends for the first two weeks. Do it this week: write down one repetitive admin task, list the exact data it needs, and keep everything else out of reach.',
'{{FACT_1}}': 'About 9.5 million barrels a day left the Strait of Hormuz in the week to Tuesday, roughly 30% below pre-war levels, according to Kpler.',
'{{FACT_2}}': 'Eleven tankers were attacked while transiting Hormuz in the week to 4 October, the most since the war began in late February, according to the International Maritime Organization.',
'{{FACT_3}}': 'Port Adelaide declined to match Zak Butters\' offer from the Bulldogs and received Pick 5 as compensation.',
'{{JOKE_SETUP}}': 'Why did the carpet layer never lose a quote to the big firms?',
'{{JOKE_PUNCHLINE}}': '"He always had his prices covered wall to wall."',
'{{CLOSING_QUOTE}}': '"A smooth sea never made a skilled sailor."',
'{{CLOSING_ATTR}}': '— Franklin D. Roosevelt',
'{{CLOSING_MESSAGE}}': "It's Saturday 10 October, mild and mostly dry up to 21°C, so it's a good window to get outdoor jobs and yard tidying done before Monday's showers and possible thunderstorm. With Hormuz tanker attacks at a wartime high, keep a fuel line in every quote next week.",
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
