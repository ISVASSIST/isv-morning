#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Monday, 09 November 2026',
'{{WEATHER_1}}': 'MON 9 NOV · ☀️ Sunny, about 5-20°C',
'{{WEATHER_2}}': 'TUE 10 NOV · ⛅ Partly cloudy, about 10-26°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'WED 11 NOV · 🌦️ Drizzle, about 12-17°C, around 6 mm',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'THU 12 NOV · 🌦️ Drizzle, about 12-16°C, around 4 mm',
'{{WEATHER_5}}': 'FRI 13 NOV · ❓ Forecast not confirmed in my sources, check BoM',
'{{WEATHER_ALERT}}': 'Dry and sunny to start the week, warming to the mid-20s Tuesday, then drizzle Wednesday and Thursday. These figures are for Melbourne from a weather aggregator page about two days old, not BoM and not Carrum Downs, and sources conflicted, so check BoM before scheduling outdoor work.',
'{{WORLD_1_FLAG}}': '🌍 IRAN',
'{{WORLD_1_HEADLINE}}': "Trump Says US Carried Out 'Minor Strikes' on Iran as Missiles Hit Qeshm Island",
'{{WORLD_1_SUMMARY}}': "CNBC reports Trump confirmed limited strikes on an Iranian air-defence system on Qeshm Island near the Strait of Hormuz on 6 November. He also said resuming full attacks was 'highly unlikely' and a deal 'could happen'. I only saw the headline and summaries, and accounts differ.",
'{{WORLD_1_URL}}': 'https://cnbc.com/2026/11/07/trump-us-minor-strikes-iran-qeshm-island.html',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'Iran Demands Seven Conditions Before Reopening Hormuz as Mediators Push a Ceasefire Framework',
'{{WORLD_2_SUMMARY}}': "CBS News live coverage describes mediators working on a deal where Iran stops attacks in the strait in return for the US lifting its blockade of Iranian ports. Iran's state broadcaster claims 11 tankers caught fire in nine days, which the US disputes. This is a running live page, so details shift and I couldn't confirm the strait's current status.",
'{{WORLD_2_URL}}': 'https://www.cbsnews.com/live-updates/iran-war-trump-us-strait-hormuz-persian-gulf/',
'{{ECON_1_FLAG}}': '⛽ FUEL',
'{{ECON_1_HEADLINE}}': 'Petrol and Diesel Ease Slightly as Wholesale Costs Fall',
'{{ECON_1_SUMMARY}}': "IBTimes Australia reports average petrol across the five big cities fell 1.1c to 232.7 cents a litre and diesel fell 0.9c to 275.8 in the week to 4 November, with Melbourne's wholesale price falling from 225.0 to 211.7 between 2 and 6 November. Wholesale falls don't always reach the bowser quickly, and I saw this via a search summary.",
'{{ECON_1_URL}}': 'https://www.ibtimes.com.au/australian-fuel-prices-fall-wholesale-costs-1878124',
'{{ECON_2_FLAG}}': '✈️ FUEL COSTS',
'{{ECON_2_HEADLINE}}': 'Qantas Warns of Fare Rises and Flight Cuts as Fuel Prices Climb',
'{{ECON_2_SUMMARY}}': 'An ABC report from 6 November says Qantas is warning customers of higher fares and fewer flights because of fuel costs. It shows how fuel is still feeding into prices across the economy, including for trades travelling for work. I only saw the headline summary, so check the full story.',
'{{TECH_1_FLAG}}': '🤖 AI · OPENAI',
'{{TECH_1_HEADLINE}}': 'OpenAI Reportedly Launches GPT-6 Cyber, a Security Research Model for Vetted Teams',
'{{TECH_1_SUMMARY}}': 'A daily AI digest says OpenAI released GPT-6 Cyber, built for security research and rated Critical under its own safety framework, with access limited to vetted teams. This is aimed at professionals, not trades, and comes from a digest blog, not OpenAI, so treat it as unconfirmed.',
'{{TECH_1_URL}}': 'https://dev.to/hiroki-ii-ai/ai-daily-digest-november-6-2026-openai-ships-gpt-6-cyber-meta-buys-conductor-anthropic-locks-1jij',
'{{TECH_2_FLAG}}': '🤖 AI · ANTHROPIC',
'{{TECH_2_HEADLINE}}': "Anthropic Reportedly Adds a 'Personal Finance' Feature to Claude",
'{{TECH_2_SUMMARY}}': "A crypto-news roundup says Anthropic announced a Personal Finance feature for Claude on 5 November. I found no primary announcement and no details on how it works or whether it's available in Australia, so treat it as unverified.",
'{{ROBOT_1_FLAG}}': '🤖 HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': 'Agility Robotics Ends First Day on Nasdaq Up 2% at US$11.49',
'{{ROBOT_1_SUMMARY}}': 'The Robot Report says Agility began trading as AGLT after its SPAC merger and closed its first day about 2% above its opening price. The article gives a sense of how the market views humanoid robots. I only saw a search summary, not the full article.',
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/how-did-agility-robotics-perform-on-its-first-day-on-the-stock-market/',
'{{AUS_1_HEADLINE}}': 'Proposed AI Data Centre Cancelled After Public Opposition, ABC Sydney Reports',
'{{AUS_1_SUMMARY}}': "ABC Sydney's 8 November coverage says another proposed data centre has been scrapped, credited to public opposition. It's relevant to power costs and AI infrastructure here. I only saw the headline summary, so details are unconfirmed.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/sydney',
'{{AUS_2_HEADLINE}}': "Usman Khawaja's Claims About the 2018 Ball-Tampering Scandal Unsettle Australian Cricket",
'{{AUS_2_SUMMARY}}': "ABC Perth reports on 8 November that Khawaja's claims about the 2018 scandal have unsettled the sport. I only saw the headline, so I can't summarise the claims.",
'{{VIC_1_HEADLINE}}': 'Police Expand Operation Into Melbourne Arsons and Extortion',
'{{VIC_1_SUMMARY}}': "ABC reported on 6 November that police have expanded their operation into arsons and extortion in Melbourne. This is from a local news index page, so I couldn't read details, and it's slightly older than yesterday.",
'{{SCI_1_FLAG}}': '☄️ SPACE',
'{{SCI_1_HEADLINE}}': 'A Nuclear Blast Could Deflect an Asteroid, But Where It Hits Matters',
'{{SCI_1_SUMMARY}}': "Sandia National Laboratories modelling, published in Icarus and reported by ScienceDaily on 8 November, suggests an X-ray blast's effectiveness varies nearly fivefold depending on which side of the asteroid it hits. It's a simulation study, not a test.",
'{{INSIGHT_TITLE}}': 'Ask AI to Turn Supplier Price Rises Into a Quote Update Checklist',
'{{INSIGHT_BODY}}': "With fuel and freight costs moving, quotes go stale fast. Paste your last few supplier invoices and an old quote into an AI tool and ask it to list every line where the cost has changed, the percentage difference, and a suggested new price with a short note for the customer. Check the numbers against the real invoices, because it can misread figures. Ten minutes of this protects your margin on jobs you haven't started yet.",
'{{FACT_1}}': 'Agility Robotics trades on Nasdaq under the ticker AGLT, and its first day closed at US$11.49, according to The Robot Report.',
'{{FACT_2}}': "Melbourne's wholesale petrol price fell from 225.0 to 211.7 cents a litre between 2 and 6 November, according to IBTimes Australia.",
'{{FACT_3}}': 'AgiBot put six G2 wheeled humanoid robots to work in a Chinese store and livestreamed it, but two of the six failed the assessment.',
'{{JOKE_SETUP}}': 'Why did the bricklayer start the week by checking the level twice?',
'{{JOKE_PUNCHLINE}}': '"Because Monday is the one day nobody should start off-kilter, and the wall will tell on you either way."',
'{{CLOSING_QUOTE}}': '\"Rome wasn\'t built in a day.\"',
'{{CLOSING_ATTR}}': '— Traditional proverb',
'{{CLOSING_MESSAGE}}': "It's a sunny Monday in Melbourne with a warm Tuesday on the way, then drizzle midweek, so get outdoor jobs done early in the week. The Victorian election nominations closed at noon today, so expect plenty of campaign noise.",
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
