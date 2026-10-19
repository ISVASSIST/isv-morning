#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 20 October 2026',
'{{WEATHER_1}}': 'TUE 20 OCT · ⛅ Mostly cloudy and warm, small chance of drizzle · 18–27°C',
'{{WEATHER_2}}': 'WED 21 OCT · 🌦️ Partly cloudy, afternoon shower or storm possible (20–30%) · 14–27°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'THU 22 OCT · ☀️ Sunny and warm, 5% chance of rain · up to 29°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'FRI 23 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'SAT 24 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': "Warm and mostly cloudy today, around 26–27°C with only a slight chance of drizzle. Wednesday could bring an afternoon shower or storm, so get outdoor coating work done early. Thursday looks sunny and the warmest of the week. Forecast sources disagreed a little, so check BoM before committing to outdoor jobs.",
'{{WORLD_1_FLAG}}': '🌍 IRAN WAR · HORMUZ',
'{{WORLD_1_HEADLINE}}': "Vance Says the US Has 'Prevailed' in Iran War; Tehran Urges Acceptance of Its Strait of Hormuz Reopening Proposal",
'{{WORLD_1_SUMMARY}}': "Just Security's 19 October roundup reports Iran's foreign minister Abbas Araghchi answering the US Vice President by warning Washington against resuming strikes, while urging it to accept a proposal to reopen the Strait of Hormuz within seven days. Any real reopening would flow straight through to fuel and freight costs.",
'{{WORLD_1_URL}}': 'https://www.justsecurity.org/161263/early-edition-october-19-2026/',
'{{WORLD_2_FLAG}}': '🚀 YEMEN · MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'Houthi Ballistic Missiles Hit Yemeni Government Training Camp, Killing at Least 18',
'{{WORLD_2_SUMMARY}}': "The same 19 October roundup says the strike hit morning drills in Shabwa province. It also notes Egypt's National Defense Council pledging all possible support for Saudi Arabia's defence, a sign of the region staying on edge.",
'{{WORLD_2_URL}}': 'https://www.justsecurity.org/161263/early-edition-october-19-2026/',
'{{ECON_1_FLAG}}': '⛽ FUEL · ACCC',
'{{ECON_1_HEADLINE}}': 'ACCC: Retail Petrol Edges Up and Diesel Edges Down Over the Past Week',
'{{ECON_1_SUMMARY}}': "The ACCC's weekly update dated 16 October says average retail petrol prices rose slightly and diesel fell slightly. FuelRadar's price history page shows a national average of about 244.2 c/L as of 18 October. Diesel is still near $2.80 a litre, so keep fuel runs tight.",
'{{ECON_1_URL}}': 'https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update',
'{{ECON_2_FLAG}}': '🏦 RATES · RBA',
'{{ECON_2_HEADLINE}}': 'Business Loan Rates Rising After RBA Lifts Cash Rate to 4.60%, With CPI Due 28 October',
'{{ECON_2_SUMMARY}}': "Banks including CBA and Macquarie have passed the 0.25% rise on to variable business loans this month, and commentary says the 28 October CPI could decide whether another hike comes in November. These are secondary sources, so verify the rate at rba.gov.au. Worth checking your equipment finance and overdraft repayments.",
'{{TECH_1_FLAG}}': '🧠 AI · ANTHROPIC',
'{{TECH_1_HEADLINE}}': 'Anthropic Plans to Put 5% of Its Shares Into a New Public Benefit Fund',
'{{TECH_1_SUMMARY}}': 'Reported on 18 October, subject to stockholder approval, with the fund barred from lobbying or political giving. Not a tool for your shed, but it shows how fast the big AI firms are changing. Based on an aggregator listing, so details are unconfirmed.',
'{{TECH_1_URL}}': 'https://aiweekly.co/ai-news-today/anthropic-news',
'{{TECH_2_FLAG}}': '🛒 AI · GOOGLE',
'{{TECH_2_HEADLINE}}': "Google Launches 'Universal Cart' in the US, One Basket Across Stores via AI Mode and Gemini",
'{{TECH_2_SUMMARY}}': 'Dated 15 October by an aggregator, so slightly outside 48 hours. AI-driven shopping is heading for suppliers and consumables, so make sure your own pricing and product details are easy for these tools to read.',
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · OPENAI',
'{{ROBOT_1_HEADLINE}}': 'Sam Altman Confirms OpenAI Will Build a Humanoid Robot, Targeting a 2027 Demo',
'{{ROBOT_1_SUMMARY}}': "Engadget is cited on 17 October for the confirmation. A 2027 demo is a long way from a working tool, but another big AI firm entering humanoids adds pressure on the field. Details are from an aggregator listing, so treat them as unconfirmed.",
'{{ROBOT_1_URL}}': 'https://aiweekly.co/ai-news-today/openai-news',
'{{AUS_1_HEADLINE}}': "PM Says Attack on Independent MP Helen Haines Was 'No Accident'; Counter-Terrorism Task Force Activated",
'{{AUS_1_SUMMARY}}': "NPR reports the Indi MP is critically injured after being hit by a car outside her electorate office, with a 43-year-old arrested at the scene and motive unknown. Home Affairs figures cited show over 1,000 threats against politicians in 2025-26.",
'{{AUS_1_URL}}': 'https://npr.org/2026/10/19/g-s1-148737/australia-lawmaker-critically-injured',
'{{AUS_2_HEADLINE}}': 'Albanese Reportedly Preparing a Cabinet Reshuffle as Poll Numbers Slide',
'{{AUS_2_SUMMARY}}': "A News24 headline roundup says the Coalition is also calling for Communications Minister Anika Wells to go. The publication date was not confirmed, so treat the detail as unverified until the ministry is announced.",
'{{VIC_1_HEADLINE}}': "Helen Haines Attack Happened in Wangaratta, North-East Victoria",
'{{VIC_1_SUMMARY}}': "ABC's live blog on 19 October places the incident outside her electorate office in Wangaratta. With the Victorian election on 28 November, expect security for candidates and MPs to be a big topic.",
'{{SCI_1_FLAG}}': '🌋 GEOSCIENCE',
'{{SCI_1_HEADLINE}}': 'Penn State Finds Evidence of Two Hidden Magma Sources Beneath Nicaragua\'s Masaya Volcano',
'{{SCI_1_SUMMARY}}': 'ScienceDaily lists the study around 18-19 October. The two-source finding could improve eruption forecasting for a volcano that sits near 2 million people. I only saw the summary, not the paper.',
'{{INSIGHT_TITLE}}': 'Rates Are Rising: Ask AI to Draft Your Price Update Note to Regular Customers',
'{{INSIGHT_BODY}}': "With loan repayments and fuel both biting, many tradies sit on old prices because the conversation feels awkward. Paste in your current rates, your cost increases and your customer's name, and ask an AI tool for a short, polite note that explains the change and gives a start date. Read it, fix anything that doesn't sound like you, and send it yourself. It takes ten minutes and beats absorbing costs for another quarter.",
'{{FACT_1}}': 'Masaya volcano in Nicaragua has a long-lived lava lake that draws tourists, yet it sits near about 2 million people.',
'{{FACT_2}}': "A battery that lets a humanoid robot work more than 20 hours a day would let one machine cover almost three shifts, if charging is fast enough.",
'{{FACT_3}}': "The RBA's cash rate of 4.60% is the highest since late 2011, according to recent commentary.",
'{{JOKE_SETUP}}': "Why did the sparky's invoices always get paid first?",
'{{JOKE_PUNCHLINE}}': '"Because he made sure customers knew the quote was current."',
'{{CLOSING_QUOTE}}': '"The man who moves a mountain begins by carrying away small stones."',
'{{CLOSING_ATTR}}': '— Confucius',
'{{CLOSING_MESSAGE}}': "It's a warm, mostly cloudy Tuesday with a shower or storm possible tomorrow arvo, so get the outdoor work done today. Rates are up and diesel is near $2.80, so a price check could be worth ten minutes this week.",
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
