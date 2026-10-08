#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 9 October 2026',
'{{WEATHER_1}}': 'FRI 9 OCT · ☀️ Mostly sunny, warm · 8–26°C',
'{{WEATHER_2}}': 'SAT 10 OCT · 🌦️ Cloudy, shower or two · 13–20°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SUN 11 OCT · ⛅ Partly cloudy, mostly dry · 12–19°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'MON 12 OCT · 🌧️ Showers, 5–10mm possible · 12–19°C',
'{{WEATHER_5}}': 'TUE 13 OCT · 🌧️ Rain likely, cooler (low confidence)',
'{{WEATHER_ALERT}}': 'Warm, mostly sunny Friday with a top of about 26°C and gusty northerlies, so it is a good day for outdoor coating work. Showers move in Saturday morning, Sunday looks mostly dry, and rain builds again Monday and Tuesday. Based on BOM and Elders forecasts for the Frankston area, so Carrum Downs may differ slightly.',
'{{WORLD_1_FLAG}}': '🌊 HORMUZ · TANKER HIT OFF QATAR',
'{{WORLD_1_HEADLINE}}': 'Tanker Reports Being Hit by Multiple Projectiles in the Gulf as Iran Says It Will Close an Oil Bypass Route',
'{{WORLD_1_SUMMARY}}': 'UKMTO says a tanker off the north coast of Qatar was struck by multiple projectiles, and the attacker was not identified. Iran also said it would close a route used to move oil around its blockade of the Strait of Hormuz. Shipping risk here flows straight into diesel and freight costs.',
'{{WORLD_1_URL}}': 'https://dropsitenews.com/p/ansarallah-saudi-airports-russia-ukraine-bus-attack-us-inflation',
'{{WORLD_2_FLAG}}': '🇺🇦 UKRAINE · DEADLY STRIKE IN DONBAS',
'{{WORLD_2_HEADLINE}}': 'Russian Strikes in Eastern Ukraine Kill More Than 30 People, Including a Bus Attack',
'{{WORLD_2_SUMMARY}}': 'Authorities report around 30 dead and at least 18 injured, with one outlet putting the Kramatorsk bomb attack toll at 33. Counts differ and may still change. The war continues to weigh on energy, grain and European security.',
'{{WORLD_2_URL}}': 'https://dropsitenews.com/p/ansarallah-saudi-airports-russia-ukraine-bus-attack-us-inflation',
'{{ECON_1_FLAG}}': '🛢️ OIL · BRENT BACK ABOVE US$104',
'{{ECON_1_HEADLINE}}': 'Brent Crude Climbs Back Above US$104 a Barrel on Hormuz Attacks',
'{{ECON_1_SUMMARY}}': 'Reports attribute the move to the Gulf tanker attack and storm-related shut-ins in the Gulf of Mexico. Australia imports most of its diesel, so a sustained jump feeds into pump prices and freight within weeks. Keep a fuel line in your quotes.',
'{{ECON_1_URL}}': 'https://dropsitenews.com/p/ansarallah-saudi-airports-russia-ukraine-bus-attack-us-inflation',
'{{ECON_2_FLAG}}': '🇺🇸 OIL OUTLOOK · TRUMP WEIGHS IRAN STRIKES',
'{{ECON_2_HEADLINE}}': 'Trump Weighs Renewed Iran Strikes After the Midterms as the White House Warns of the "Easy Way or Hard Way"',
'{{ECON_2_SUMMARY}}': 'Reports say Trump rejected Tehran\'s latest offer and military operations could intensify after the US midterms. Another round of fighting would be a fresh upside risk for oil, diesel and the RBA\'s rate path.',
'{{TECH_1_FLAG}}': '💸 AI · CLAUDE HAIKU 5.5 IS MUCH CHEAPER',
'{{TECH_1_HEADLINE}}': 'Anthropic Ships Claude Haiku 5.5 at US$0.10 per Million Input Tokens and Adds Claude to Google Docs, Sheets and Slides',
'{{TECH_1_SUMMARY}}': 'The small model is roughly 75% cheaper than Haiku 4.5 for prompts up to 100K tokens, and Claude now runs as a sidebar in Google Workspace on every paid plan. Cheaper AI makes routine quoting and paperwork automation easier to justify.',
'{{TECH_1_URL}}': 'https://theaimarketingcollective.substack.com/p/anthropic-shipped-claude-haiku-55',
'{{TECH_2_FLAG}}': '🧩 AI · GPT-6 REACHES FREE USERS',
'{{TECH_2_HEADLINE}}': 'OpenAI Rolls GPT-6 Out Across ChatGPT, With Free Users Getting It on 8 October',
'{{TECH_2_SUMMARY}}': 'Paid tiers got GPT-6 with interactive answers straight away, with Free and Go users following. OpenAI also opened a public beta of a cheaper GPT-6 Luna model for developers. Worth a trial on quoting and email drafts, but keep customer data out of free tiers.',
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · BOSTON DYNAMICS NAMES NEW CEO',
'{{ROBOT_1_HEADLINE}}': 'Boston Dynamics Appoints Former Amazon Alexa AI Chief Rohit Prasad as CEO',
'{{ROBOT_1_SUMMARY}}': 'Prasad, who spent 12 years at Amazon leading Alexa and AGI work, took over on 7 October from interim CEO Amanda McMaster. The Hyundai-controlled company says the move accelerates its "Physical AI" push to commercialise intelligent robots in industrial settings.',
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/boston-dynamics-appoints-former-amazon-executive-rohit-prasad-new-ceo/',
'{{AUS_1_HEADLINE}}': 'North Melbourne Reportedly Offers Sydney\'s Nick Blakey About $11 Million Over Eight Years as AFL Trade Period Heats Up',
'{{AUS_1_SUMMARY}}': 'Sydney\'s list boss admits the club was blindsided by Blakey\'s meetings with rival clubs, while Geelong has ended the Rowan Marshall trade saga. Plenty of footy talk to fill the smoko room today.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-08/afl-trade-period-live-blog-thursday-october-8/107239586',
'{{AUS_2_HEADLINE}}': 'Teen Burned in Botched Taylors Hill Firebombing Took Orders From Middlemen on WhatsApp',
'{{AUS_2_SUMMARY}}': 'Police arrested three teenagers over the attack, and the 13-year-old boy hurt in it is in hospital. It adds to a growing picture of organised crime recruiting young people for arson.',
'{{VIC_1_HEADLINE}}': 'Six Cars Set Alight Across Melbourne on the Fourth Straight Night of Residential Arson Attacks',
'{{VIC_1_SUMMARY}}': 'Police believe the attacks may be linked to organised crime and intimidation, though no link between incidents is confirmed. Park work utes and trailers inside or in well-lit spots, and keep an eye on the yard cameras.',
'{{SCI_1_FLAG}}': '🔭 SPACE · ATMOSPHERE ON A LAVA WORLD',
'{{SCI_1_HEADLINE}}': 'James Webb Telescope Finds Strong Evidence of an Atmosphere on Lava World HD 3167 b',
'{{SCI_1_SUMMARY}}': 'The rocky planet orbits its star every 24 hours under extreme heat, yet Webb sees signs it still holds a gas envelope. It is a big step in understanding whether small rocky worlds can keep atmospheres. Reported 7 October 2026.',
'{{INSIGHT_TITLE}}': 'AI Just Got 75% Cheaper: Use the Small Model for Routine Paperwork',
'{{INSIGHT_BODY}}': 'With Claude Haiku 5.5 priced at US$0.10 per million input tokens and cheaper GPT-6 options arriving, the cost of AI for day-to-day office tasks is now close to nothing. For a small trades business, the smart move is to stop paying for the biggest model on jobs that do not need it. Use a small, cheap model for routine work such as turning job notes into invoices, drafting follow-up emails and tidying quote wording, and save the premium tier for tricky jobs like contract review. Do it this week: pick one repetitive paperwork task, run it through a small model on ten past jobs, and compare the result with what you wrote by hand.',
'{{FACT_1}}': 'Boston Dynamics began in 1992 as a spin-off from MIT, founded by Marc Raibert, and Hyundai bought a controlling stake in 2021.',
'{{FACT_2}}': 'HD 3167 b orbits its star in about 24 hours, so a full year on this lava world is shorter than a single working day.',
'{{FACT_3}}': 'Australia\'s rate of inflation hit 4.0% in August 2026, up from 3.5% in July, according to reporting on the ABS figures.',
'{{JOKE_SETUP}}': 'Why did the chippy always get paid on time?',
'{{JOKE_PUNCHLINE}}': '"He never left a job without a tight finish."',
'{{CLOSING_QUOTE}}': '"Rome was not built in a day, but they were laying bricks every hour."',
'{{CLOSING_ATTR}}': '— John Heywood',
'{{CLOSING_MESSAGE}}': "It's Friday 9 October, mostly sunny and up to 26°C, so get the outdoor coating work done today before showers arrive Saturday morning. With oil back above US$104, keep a fuel line in every quote heading into next week.",
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
