#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Sunday, 4 October 2026',
'{{WEATHER_1}}': 'SUN 4 OCT · ⛅ Sun and cloud, 20% chance of rain · 9–16°C',
'{{WEATHER_2}}': 'MON 5 OCT · ☁️ Mainly cloudy, 40% chance of a shower, about 1mm · 13–16°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'TUE 6 OCT · 🌧️ Showers, 5–10mm · 10–14°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'WED 7 OCT · ⛅ Partly cloudy · 9–16°C',
'{{WEATHER_5}}': 'THU 8 OCT · outlook not confirmed, check BOM',
'{{WEATHER_ALERT}}': "Clocks went forward at 2am, so you've lost an hour. Today is the best window of the week: mostly dry with sun and cloud. Monday is mainly cloudy, and showers of 5–10mm return Tuesday, so get outdoor coating work done early. Wed/Thu outlook is lower confidence.",
'{{WORLD_1_FLAG}}': '🇨🇩 DR CONGO · EBOLA DEATH TOLL TOPS 4,000',
'{{WORLD_1_HEADLINE}}': 'France Pledges More Support as Congo Ebola Outbreak Passes 4,000 Deaths',
'{{WORLD_1_SUMMARY}}': "Official figures show about 4,018 deaths from 8,300 cases, the largest DRC outbreak on record and the second deadliest Ebola epidemic ever. French Foreign Minister Jean-Noël Barrot visited the affected east on Saturday and promised extra help.",
'{{WORLD_1_URL}}': 'https://www.inkl.com/news/france-pledges-more-support-to-fight-drc-ebola-outbreak-as-deaths-top-4-000',
'{{WORLD_2_FLAG}}': '🇺🇸 USA · ALITO SAYS HE WILL KEEP THINKING ABOUT RETIRING',
'{{WORLD_2_HEADLINE}}': "Justice Alito Says He 'Thought About' Retiring and Will Again in 2027",
'{{WORLD_2_SUMMARY}}': "In a CBS interview released Friday, the 76-year-old said he considered stepping down this year, while telling the Wall Street Journal he is 'here for another term'. A vacancy would reshape the US Supreme Court's balance.",
'{{WORLD_2_URL}}': 'https://thehill.com/regulation/court-battles/6127267-alito-considered-supreme-court-retirement/',
'{{ECON_1_FLAG}}': '⛽ FUEL · DIESEL STILL NEAR $2.86 A LITRE AS RELIEF ENDS',
'{{ECON_1_HEADLINE}}': 'Diesel Averages $2.86 a Litre in Capital Cities as Truckers Press for Fuel Tax Relief',
'{{ECON_1_SUMMARY}}': "Capital city diesel rose another 18.9c in the week to late September, and excise went back up to 53.7c a litre after relief ended in August. Canberra has ruled out another cut, so build fuel into quotes and keep your fuel tax credit claims current.",
'{{ECON_1_URL}}': 'https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update',
'{{ECON_2_FLAG}}': '💳 SMALL BUSINESS · CARD SURCHARGE BAN BITES',
'{{ECON_2_HEADLINE}}': 'Small Businesses Brace for Squeeze as Card Surcharge Ban Takes Effect',
'{{ECON_2_SUMMARY}}': "Since 1 October businesses can no longer add surcharges to card payments but still pay Visa and Mastercard fees. The ATO also stops accepting credit cards for tax after 30 November, so watch cash flow.",
'{{TECH_1_FLAG}}': '🔐 AI · GOOGLE LAUNCHES GEMINI 4 ARGON TO CYBER DEFENDERS FIRST',
'{{TECH_1_HEADLINE}}': 'Google Launches Gemini 4 Argon With a 1 Million Token Output Limit',
'{{TECH_1_SUMMARY}}': 'Argon can find, validate and patch software vulnerabilities, and early access goes to vetted defenders before paid API customers get it at US$2 per million input tokens. Handy for the future of securing your own business systems and email.',
'{{TECH_1_URL}}': 'https://www.ghacks.net/2026/10/02/google-launches-gemini-4-argon-with-a-1-million-token-output-limit-starting-with-cyber-defenders/',
'{{TECH_2_FLAG}}': '🛍️ AI · SHOPIFY AND WIX PUSH AI AGENTS FOR SMALL BUSINESS',
'{{TECH_2_HEADLINE}}': "Wix Launches Symphony and Shopify Launches Canvas to Put AI Agents to Work in Small Businesses",
'{{TECH_2_SUMMARY}}': "Wix's Symphony helps owners set up AI agents to run workflows, while Shopify's Canvas lets merchants build custom stores through its Sidekick agent. A Bluevine report says 74% of small business owners are using or testing AI.",
'{{ROBOT_1_FLAG}}': '🎨 GERMANY · DÜRR LAUNCHES FOUR NEW PAINT-SHOP ROBOTS',
'{{ROBOT_1_HEADLINE}}': 'Dürr Launches Four New EcoRS Robots for Automotive Paint Shops',
'{{ROBOT_1_SUMMARY}}': "The Generation 2 range covers payloads from 20 to 150kg with reach up to 3,100mm, for sealing, cleaning and material handling. It's built around paint-shop processes rather than adapted from general-purpose arms, which is a coatings story worth watching. Published 1 October.",
'{{ROBOT_1_URL}}': 'https://roboticsandautomationnews.com/2026/10/01/durr-launches-four-new-robots-for-automotive-paint-shops/105393/',
'{{AUS_1_HEADLINE}}': 'Ten Injured After Car Drives Into Knights Fans at Newcastle Grand Final Farewell',
'{{AUS_1_SUMMARY}}': "A car hit a crowd farewelling the Newcastle Knights at Wallsend about 9:30am Saturday, injuring 10 including three children. A five-year-old girl and a 67-year-old man are critical. An 18-year-old driver was arrested and police say terrorism is not suspected.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-03/newcastle-knights-car-crash-wallsend-injuries/107224666',
'{{AUS_2_HEADLINE}}': 'Daylight Saving Starts Today in Victoria, NSW, SA, Tasmania and the ACT',
'{{AUS_2_SUMMARY}}': "Clocks jumped from 2am to 3am this morning, so you lost an hour of sleep but gain lighter evenings. Queensland, WA and the NT stay put, so check call times with interstate clients and suppliers this week.",
'{{VIC_1_HEADLINE}}': 'One Nation Launches Victorian Campaign and Promises to Restart Native Timber Logging',
'{{VIC_1_SUMMARY}}': "Pauline Hanson's party launched its state election campaign in Southbank on Saturday with a law-and-order push and a pledge to resume native logging, though it hasn't costed the policy. Logging was shut down in January 2024 and the Coalition also wants it restarted.",
'{{SCI_1_FLAG}}': '🔬 BIOCHEMISTRY · LEUCINE POWERS UP YOUR CELLS',
'{{SCI_1_HEADLINE}}': 'Leucine Does More Than Build Muscle: It Boosts Cellular Energy Production',
'{{SCI_1_SUMMARY}}': 'The essential amino acid protects key proteins on mitochondria from being destroyed, which boosts energy production. The finding links nutrition and metabolism and could eventually inform treatments for metabolic disorders and cancer. ScienceDaily, 1 October 2026.',
'{{INSIGHT_TITLE}}': 'Your Shopfront Is Now an AI Conversation: Check What AI Says About Your Business',
'{{INSIGHT_BODY}}': "With AI agents now being built into Shopify, Wix and Google tools, customers increasingly ask an AI assistant who to call before they ever visit a website. Spend ten minutes this week asking ChatGPT and Gemini for 'the best coating contractor in south-east Melbourne' and see what comes back. Fix what's wrong first: update your Google Business Profile, make sure services, suburbs and phone number match everywhere, and ask recent customers for reviews. The business with the clearest, most consistent information is the one the AI recommends.",
'{{FACT_1}}': "Dürr's new EcoRS Generation 2 paint-shop robots reach up to 3,100mm and carry payloads from 20kg to 150kg, replacing several application-specific robot configurations with one platform.",
'{{FACT_2}}': "Victorian clocks went forward at 2am this morning, so today is only 23 hours long, the shortest day of the year for most Victorians.",
'{{FACT_3}}': "The Congo Ebola outbreak is caused by the rarer Bundibugyo species and is now the second deadliest Ebola epidemic on record, behind West Africa's 2014–2016 outbreak.",
'{{JOKE_SETUP}}': 'A plasterer was asked how his small business kept finishing jobs on time, even when the weather turned and the site was damp all week.',
'{{JOKE_PUNCHLINE}}': 'He said, "Simple — I just give every wet wall time to come around."',
'{{CLOSING_QUOTE}}': '"Do the hard jobs first. The easy jobs will take care of themselves."',
'{{CLOSING_ATTR}}': '— Dale Carnegie',
'{{CLOSING_MESSAGE}}': "It's Sunday 4 October, the clocks have gone forward and you're down an hour. Make the most of today's drier spell, then use the lighter evenings this week to get outdoor jobs done before Tuesday's showers.",
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
