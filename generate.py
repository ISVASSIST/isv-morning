#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 31 October 2026',
'{{WEATHER_1}}': 'SAT 31 OCT · ⛈️ Thunderstorms, possibly severe · about 21°C',
'{{WEATHER_2}}': 'SUN 1 NOV · 🌦️ Milder, a few showers',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'MON 2 NOV · ⛈️ Showers likely, afternoon storm possible',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'TUE 3 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_5}}': 'WED 4 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Saturday's storm is the main risk, with damaging winds possible late morning to early afternoon and an improvement after about 3-4pm. Secure loose sheets, hoses and gear before it hits. Sunday looks milder and Monday is wet again with a possible afternoon storm. These are greater Melbourne figures from several forecast sites, not a Carrum Downs-specific BoM page, and I couldn't confirm temperatures beyond Saturday or any forecast for Tuesday and Wednesday, so check BoM before planning.",
'{{WORLD_1_FLAG}}': '🌍 SPAIN',
'{{WORLD_1_HEADLINE}}': "Death Toll From Spain's High-Speed Train Crash Rises to 74",
'{{WORLD_1_SUMMARY}}': "Spain's transport ministry says 74 people have died after two high-speed trains collided near Toledo, up from 68 earlier in the week. Transport Minister Óscar Puente blamed what he called an inexplicable order from a central command centre after a safety system failed. It is Spain's second deadly rail disaster this year.",
'{{WORLD_1_URL}}': 'https://www.thejournal.ie/spain-train-crash-7208508-Oct2026/',
'{{WORLD_2_FLAG}}': '🌍 CRYPTO',
'{{WORLD_2_HEADLINE}}': "Binance Hit by Biggest Crypto Theft on Record, Bitcoin Slides Below US$78,000",
'{{WORLD_2_SUMMARY}}': "Binance estimates about US$6.3 billion in assets were affected and says it has set aside company funds to cover customer losses. It says the entry point was a compromised engineer's laptop, and one security firm has linked the attack to a North Korean group, though that isn't formally confirmed. Figures vary between outlets.",
'{{WORLD_2_URL}}': 'https://www.coindesk.com/markets/2026/10/30/usd6-billion-binance-hack-sends-bitcoin-ether-tumbling-standard-chartered-sees-more-losses-ahead',
'{{ECON_1_FLAG}}': '🛢️ OIL · BRENT',
'{{ECON_1_HEADLINE}}': 'Brent Holds Around US$116 on Friday as Hormuz Mine Claims Keep Prices High',
'{{ECON_1_SUMMARY}}': "Brent traded roughly between US$112 and US$118 on Friday, depending on the contract month, with Iranian claims of tanker mine strikes keeping nerves up (US Central Command calls those claims false). The December contract expires today, so the headline price will switch to the cheaper January contract from Monday. That is a paperwork change, not real relief at the bowser.",
'{{ECON_1_URL}}': 'https://financefeeds.com/brent-crude-oil-price-116-friday-hormuz-mine-strikes-december-expiry-fourth-monthly-gain-bull-120-bear-108/',
'{{ECON_2_FLAG}}': '📉 MARKETS',
'{{ECON_2_HEADLINE}}': 'Nasdaq Dives Over 3% as an AI Sell-Off Grips Wall Street',
'{{ECON_2_SUMMARY}}': "US shares fell sharply on Friday, with the Nasdaq down more than 3% in a sell-off tied to doubts about AI spending. It's worth watching if your super or business savings have market exposure, and the RBA meets on Tuesday. I only saw the headline, so check the source for details.",
'{{TECH_1_FLAG}}': '🤖 AI · ANTHROPIC',
'{{TECH_1_HEADLINE}}': "Anthropic Files for IPO, Reportedly Showing US$16.3 Billion in Half-Year Revenue",
'{{TECH_1_SUMMARY}}': "The filing reportedly reveals a founder-controlled governance structure alongside the revenue figure. For a small business owner it mostly signals how much money is behind the AI tools you're starting to use. Figures are as reported by SiliconANGLE, not from the filing itself.",
'{{TECH_1_URL}}': 'https://siliconangle.com/2026/10/30/as-anthropic-finally-files-for-ipo-rising-risks-arent-slowing-the-ai-buildout-yet',
'{{TECH_2_FLAG}}': '🤖 AI · INSPECTION',
'{{TECH_2_HEADLINE}}': "Percepto Launches Axion, an AI Platform to Unify Inspection Data From Any Drone or Robot",
'{{TECH_2_SUMMARY}}': "Axion is hardware-agnostic, so it pulls inspection data from different drones and robots into one analysis platform. It's aimed at big industrial sites, but it shows where inspection records are heading. Reported by The Robot Report on 30 October.",
'{{ROBOT_1_FLAG}}': '🤖 ROBOT TARIFFS',
'{{ROBOT_1_HEADLINE}}': "White House Finds Robot Imports Pose a National Security Threat Under Section 232",
'{{ROBOT_1_SUMMARY}}': "The US determination covers foreign-made robots, but one industry voice says it isn't a new tariff today and is better read as a sign of direction. If tariffs follow, imported robot and automation prices could rise, which matters for anyone pricing equipment. The Robot Report, 29 October.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/white-house-makes-section-232-determination-regarding-foreign-made-robots/',
'{{AUS_1_HEADLINE}}': "Government Reportedly Plans to Ban Data Centres Being Built Too Close to Homes",
'{{AUS_1_SUMMARY}}': "Nine Newspapers reports the Albanese government will restrict data centre locations as more communities oppose them in their suburbs. This is a media report rather than an announced policy, so details could change. From the ABC's 30 October federal politics blog.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-30/federal-politics-live-blog-oct-30/107324978',
'{{AUS_2_HEADLINE}}': "One Nation Accuses PM of Playing 'Dirty Games' Over Offer of Extra Staff to Farrer MP",
'{{AUS_2_SUMMARY}}': "David Farley reportedly received a letter authorising an extra staffer on a $200,000 package, an offer he rejected, and Labor denies it was trying to win him over. I haven't seen the letter, so this is the reported account only.",
'{{VIC_1_HEADLINE}}': "Police Launch Operation Furlong Road Blitz From 30 October to 4 November",
'{{VIC_1_SUMMARY}}': "Victoria Police are targeting speeding, distracted driving, drink and drug driving and fatigue statewide, saying speeding accounts for 29 per cent of road deaths in 2026. Expect plenty of testing if the work ute is out this weekend.",
'{{SCI_1_FLAG}}': '💪 AGEING',
'{{SCI_1_HEADLINE}}': "Ageing Muscles Have a Hidden Defence That Trades Strength for Cell Protection",
'{{SCI_1_SUMMARY}}': "University of Copenhagen researchers report that ageing muscles sacrifice some strength to protect their cells from damage, which may help explain why strength fades with age. ScienceDaily, 28 October.",
'{{INSIGHT_TITLE}}': "Let AI Draft Your Weather-Delay Messages Before the Phone Starts Ringing",
'{{INSIGHT_BODY}}': "When a storm shuffles the week, the slow part is telling every customer. List the affected jobs, give an AI tool the new rough dates, and ask for a short, polite message for each one in your own plain tone. Read each before sending, and don't promise dates you can't keep. Do it the evening before a bad forecast and customers hear it from you first, not after you've missed the job.",
'{{FACT_1}}': "Victoria Police says speeding accounts for 29 per cent of the state's road deaths in 2026.",
'{{FACT_2}}': "Spain has the world's second-longest high-speed rail network after China, yet had no deadly crash in more than three decades until this year.",
'{{FACT_3}}': "Bedrock Robotics, which makes autonomous kits for heavy equipment, raised US$600 million at a US$4.1 billion valuation on 26 October.",
'{{JOKE_SETUP}}': "Why did the scaffolder get nervous when the wind warning came through?",
'{{JOKE_PUNCHLINE}}': '"He knew the whole job was about to get a bit shaky, and he hates being left hanging."',
'{{CLOSING_QUOTE}}': '"A smooth sea never made a skilled sailor."',
'{{CLOSING_ATTR}}': '— Franklin D. Roosevelt',
'{{CLOSING_MESSAGE}}': "A possibly severe storm is forecast for Saturday late morning to early afternoon, so tie down loose gear and sheets now and keep the ute off the road until it clears. If you do head out this weekend, expect the Operation Furlong police testing, and Monday looks wet again.",
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
