#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 15 October 2026',
'{{WEATHER_1}}': 'THU 15 OCT · ☀️ Mostly sunny · 7–21°C',
'{{WEATHER_2}}': 'FRI 16 OCT · ⛅ Partly cloudy, 10% chance of rain · 10–23°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SAT 17 OCT · ☀️ Mostly sunny, 5% chance of rain · 13–25°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SUN 18 OCT · ☀️ Sunny, 5% chance of rain · 13–26°C',
'{{WEATHER_5}}': 'MON 19 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': "A dry, sunny run through to the weekend, with temperatures climbing from 21°C today to 26°C on Sunday. Figures are from the Bureau of Meteorology Melbourne forecast issued 14 October, so Carrum Downs could differ slightly, and Monday could not be confirmed. UV is forecast to reach high levels on Saturday, so cover up if you're outdoors.",
'{{WORLD_1_FLAG}}': '🛢️ IRAN · STRAIT OF HORMUZ',
'{{WORLD_1_HEADLINE}}': 'Iranian Officials Say Tehran Is Using New Tactics Against Ships in the Strait of Hormuz',
'{{WORLD_1_SUMMARY}}': "Just Security's 14 October roundup, citing Reuters, says Iranian officials claim the new tactics began about 10 days ago and aim to keep oil prices high ahead of the US midterms. I only saw excerpts of the roundup, so details are limited.",
'{{WORLD_1_URL}}': 'https://www.justsecurity.org/160738/early-edition-october-14-2026/',
'{{WORLD_2_FLAG}}': '🇬🇧 UK · MI5',
'{{WORLD_2_HEADLINE}}': 'MI5 Chief Says the Agency Is Putting More Resources Into State Threats Than During the Cold War',
'{{WORLD_2_SUMMARY}}': 'The MI5 director general told a London audience the focus on hostile state activity is now greater than in the Cold War era. Listed in the same 14 October Just Security roundup; I only saw the headline and a short excerpt.',
'{{WORLD_2_URL}}': 'https://www.justsecurity.org/160738/early-edition-october-14-2026/',
'{{ECON_1_FLAG}}': '⛽ FUEL · PETROL & DIESEL',
'{{ECON_1_HEADLINE}}': 'Petrol Climbs Above $2.40 a Litre Again While Diesel Tops $2.80',
'{{ECON_1_SUMMARY}}': 'Neos Kosmos reported on 14 October that regular unleaded is above $2.40 for the first time in over six months, with diesel above $2.80, blamed on Middle East conflict. ACCC-based figures for the week to 7 October put Melbourne diesel at about $2.82.',
'{{ECON_1_URL}}': 'https://neoskosmos.com/en/2026/10/14/news/petrol-prices-climb-above-2-40-a-litre-again/',
'{{ECON_2_FLAG}}': '📉 DIESEL · WHOLESALE',
'{{ECON_2_HEADLINE}}': 'Wholesale Diesel Drifts Lower, With the NRMA Expecting Pump Diesel to Ease This Week',
'{{ECON_2_SUMMARY}}': "Sydney terminal gate diesel eased from 265.2 to 262.8 cents between 8 and 14 October, and the NRMA's 12 October report expects diesel to fall while petrol rises into the mid 240s. These come from price pages and a summary, not a full report, so check your supplier before locking in quotes.",
'{{TECH_1_FLAG}}': '💼 AI · MICROSOFT COPILOT',
'{{TECH_1_HEADLINE}}': 'Microsoft Starts Previewing Work IQ, Linking Copilot Agents to Live Business Data',
'{{TECH_1_SUMMARY}}': 'An AI Business report says the October preview connects Copilot and autonomous agents to live Dynamics 365 and Power Platform data. Pricing and general availability are not announced, and I could not confirm the exact date, so treat it as a preview to watch.',
'{{TECH_1_URL}}': 'https://aibusiness.com/agentic-ai/microsoft-recommits-to-ai-agents',
'{{TECH_2_FLAG}}': '🖥️ AI · CHIPS',
'{{TECH_2_HEADLINE}}': 'Microsoft Says Its Maia 200 Chip Is Now Serving Production Workloads, Including Copilot',
'{{TECH_2_SUMMARY}}': "Reported as a 12 October announcement in a weekly AI roundup, so it is a little over 48 hours old and I could not check it against Microsoft's own page. Mostly relevant as a sign of cheaper AI to come.",
'{{ROBOT_1_FLAG}}': '🏠 ROBOTICS · HOMEBUILDING',
'{{ROBOT_1_HEADLINE}}': 'Promise Robotics Signs Multi-Year Deal With D.R. Horton to Build Homes in a Robotic Factory',
'{{ROBOT_1_SUMMARY}}': "The Robot Report lists the 13 October deal for Promise Robotics' Factory-as-a-Service to produce more than 1,250 US homes. I only saw the listing, but it is a real example of automation moving into building trades.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/promise-robotics-partners-d-r-horton-physical-ai-homebuilding/',
'{{AUS_1_HEADLINE}}': 'ACCC Takes Sunny Queen and 11 Other Egg Producers to Court Over Alleged Cartel Conduct',
'{{AUS_1_SUMMARY}}': "ABC's 14 October regional briefing says the regulator alleges cartel conduct, and Sunny Queen denies the claims. I only saw the briefing summary, not the court filing, and it is not a small trades issue, but it shows the ACCC is active.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-14/southern-queensland-local-news-briefing/107263172',
'{{AUS_2_HEADLINE}}': 'Report Says the Health Spending Gap Between Regional and City Australians Is Growing',
'{{AUS_2_SUMMARY}}': "A National Rural Health Alliance report, noted in ABC's 14 October South East SA briefing, says the gap is widening. I only saw a one-line summary, so check the report for figures.",
'{{VIC_1_HEADLINE}}': 'Regional Victorian Voters Say They Are Disillusioned as Labor Faces Rising One Nation Support',
'{{VIC_1_SUMMARY}}': 'ABC reported on 14 October, just over six weeks from the 28 November state election, that regional voters are turning away from Labor, with Bendigo East one seat to watch. I only saw search excerpts of the story.',
'{{SCI_1_FLAG}}': '⚛️ QUANTUM PHYSICS',
'{{SCI_1_HEADLINE}}': 'Oxford Physicists Recreate a Bizarre Quantum Effect on a Hybrid Quantum Computer',
'{{SCI_1_SUMMARY}}': 'ScienceDaily listed the 13 October story: a particle reacts to a magnetic field without ever travelling through it. I only saw the teaser, so details are thin.',
'{{INSIGHT_TITLE}}': 'Let AI Draft Your Complaint and Defect Replies: You Check the Facts, Then Press Send',
'{{INSIGHT_BODY}}': "A tense email from a customer is hard to answer at 6pm after a long day. Paste the complaint into an AI tool, add your job notes and photos, and ask for a calm, factual draft that offers a fix and a date. Then read every line: check the dates, the spec and any promise it makes, because the tool can invent details. You stay in charge of what goes out, but the drafting that used to take 30 minutes takes five, and your tone stays professional when you're tired.",
'{{FACT_1}}': "The James Webb Space Telescope's 6.5-metre primary mirror is made of 18 hexagonal beryllium segments coated in a thin layer of gold.",
'{{FACT_2}}': 'A diesel engine has no spark plugs: it squeezes air so hard it gets hot enough, above 500°C, to ignite the fuel on its own.',
'{{FACT_3}}': "The magnetic-field quantum effect behind this week's Oxford story was first predicted by physicists Yakir Aharonov and David Bohm in 1959.",
'{{JOKE_SETUP}}': 'Why did the bricklayer never worry about a slow month?',
'{{JOKE_PUNCHLINE}}': '"Because he always had a solid foundation of repeat customers."',
'{{CLOSING_QUOTE}}': '"Courage is grace under pressure."',
'{{CLOSING_ATTR}}': '— Ernest Hemingway',
'{{CLOSING_MESSAGE}}': "It's Thursday 15 October, sunny and around 21°C in Carrum Downs, a good day to get outdoor work done. The weekend looks even warmer, so book anything weather-sensitive for Saturday or Sunday. Diesel is still above $2.80, so check your fuel costs before you quote big jobs.",
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
