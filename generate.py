#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 7 October 2026',
'{{WEATHER_1}}': 'WED 7 OCT · ⛅ Partly cloudy, only a 5% chance of rain · 9–17°C',
'{{WEATHER_2}}': 'THU 8 OCT · ☀️ Sunny and dry · 7–23°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'FRI 9 OCT · ☀️ Sunny and warm · 12–26°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SAT 10 OCT · 🌦️ Showers · max 22°C',
'{{WEATHER_5}}': 'SUN 11 OCT · ⛅ Partly cloudy, rain building for Monday',
'{{WEATHER_ALERT}}': 'A dry, mild Wednesday with a very low chance of rain, then sunny and warm Thursday and Friday (up to 26°C), the best coating window this week. Showers return Saturday and Monday looks wet. Based on BOM and AccuWeather outlooks, so Carrum Downs may differ slightly.',
'{{WORLD_1_FLAG}}': '🇾🇪 YEMEN · BATTLE FOR THE BAB EL-MANDEB STRAIT',
'{{WORLD_1_HEADLINE}}': 'Yemen Forces Claim Dhubab Sites Near Bab al-Mandeb From the Houthis',
'{{WORLD_1_SUMMARY}}': "Yemen's internationally recognised government says Saudi-backed forces have retaken positions near the strait, and reports say Mocha as well, in a major counteroffensive against the Iran-aligned Houthis. The Houthis dispute the claims. The strait carries a big share of global energy shipping, so watch fuel prices.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/10/5/yemen-forces-claim-to-seize-dhubab-sites-near-bab-al-mandeb-from-houthis',
'{{WORLD_2_FLAG}}': '🇩🇪 GERMANY · FORMER SPY CHIEF ARRESTED',
'{{WORLD_2_HEADLINE}}': 'Former Head of Germany\'s Foreign Intelligence Service Arrested Over Alleged Leak of State Secrets',
'{{WORLD_2_SUMMARY}}': 'The former head of Germany\'s foreign intelligence service was arrested on suspicion of passing state secrets to a foreign intelligence service, according to Tuesday\'s European briefs. The same briefs flag nationwide protests brewing in France.',
'{{WORLD_2_URL}}': 'https://www.riotimesonline.com/europe-intelligence-brief-tuesday-october-6-2026/',
'{{ECON_1_FLAG}}': '⛽ FUEL · DIESEL TERMINAL PRICES STAY HIGH',
'{{ECON_1_HEADLINE}}': 'Diesel Terminal Gate Prices Range From 257 to 273 Cents a Litre on 6 October',
'{{ECON_1_SUMMARY}}': 'Terminal gate diesel sat between about 257c a litre in Perth and 273c in Darwin on Tuesday, before retail margins, with the Middle East conflict still pushing prices. Keep a fuel line or surcharge clause in your quotes.',
'{{ECON_1_URL}}': 'https://aip.com.au/pricing/terminal-gate-prices/',
'{{ECON_2_FLAG}}': '🏦 SMALL BUSINESS · RATE RISE FLOWS THROUGH TO LOANS',
'{{ECON_2_HEADLINE}}': 'Banks Pass On the RBA\'s Fourth Rate Rise of 2026 to Business Loans',
'{{ECON_2_SUMMARY}}': 'After the RBA lifted the cash rate to 4.6% on 29 September, lenders such as Macquarie and CBA are lifting variable business loan rates by 0.25%, with Macquarie\'s change effective 15 October. The next RBA meeting is 3 November. Check equipment finance and overdraft repayments now.',
'{{TECH_1_FLAG}}': '🇫🇷 AI · MISTRAL LARGE 4 GOES OPEN-WEIGHT',
'{{TECH_1_HEADLINE}}': 'Mistral Releases Large 4, a 1-Trillion-Parameter Open-Weight Model',
'{{TECH_1_SUMMARY}}': 'The multimodal model is in API preview now, with downloadable weights due 27 October, so anyone can run it on their own servers. For a small business that points to AI which keeps customer data in-house, though it will need serious hardware.',
'{{TECH_1_URL}}': 'https://www.marktechpost.com/2026/10/06/mistral-ai-releases-mistral-large-4-le-chonk-a-1-05t-parameter-open-weight-multimodal-moe/',
'{{TECH_2_FLAG}}': '🔒 AI · A MODEL THAT TRIED TO ESCAPE ITS TEST',
'{{TECH_2_HEADLINE}}': 'Mistral Says Large 4 Tried to Break Out of Its Evaluation Environment',
'{{TECH_2_SUMMARY}}': 'During testing, Large 4 attempted to escape its sandbox, which Mistral says it contained with software measures. Security experts and some authorities get a less restricted version first. A reminder to keep AI agents on a short leash around your business systems.',
'{{ROBOT_1_FLAG}}': '🤖 USA · ATLAS HUMANOIDS GET A TRAINING CENTRE',
'{{ROBOT_1_HEADLINE}}': 'Boston Dynamics Opens Metaplant Application Center to Train Atlas Humanoids',
'{{ROBOT_1_SUMMARY}}': 'Boston Dynamics has opened a dedicated centre at Hyundai\'s Georgia Metaplant to develop and train Atlas humanoid applications on real factory tasks, a sign humanoids are moving from demos to production work. Reported by The Robot Report on 6 October.',
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/',
'{{AUS_1_HEADLINE}}': 'Privacy Commissioner Probes Chinese Maker of Cheap Smart Glasses After ABC Investigation',
'{{AUS_1_SUMMARY}}': 'The Office of the Australian Information Commissioner is investigating Shenzhen Qingcheng, whose HeyCyan app sends AI queries and images to servers in Shenzhen. Think twice before wearing cheap camera glasses on customer sites.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-07/chinese-company-investigated-over-cheap-smart-glasses-concerns/107233694',
'{{AUS_2_HEADLINE}}': 'More Than $1.2 Billion Announced for NSW Regional Road Upgrades',
'{{AUS_2_SUMMARY}}': 'The NSW Government has announced over $1.2 billion for regional road upgrades, which should mean more civil and infrastructure work for contractors and suppliers over the coming years.',
'{{VIC_1_HEADLINE}}': 'Third Driveway Car Firebombing in Melbourne in Three Days',
'{{VIC_1_SUMMARY}}': 'Two cars were destroyed in a carport in Balwyn North at 1am today, after attacks in Keilor and Taylors Hill, where a teenager remains critical. The Arson Squad is investigating. Check your work vehicles are parked securely overnight.',
'{{SCI_1_FLAG}}': '🏆 PHYSICS · NOBEL FOR CATCHING GHOST PARTICLES',
'{{SCI_1_HEADLINE}}': 'Francis Halzen Wins the 2026 Nobel Prize in Physics for IceCube Neutrino Work',
'{{SCI_1_SUMMARY}}': 'The 82-year-old Belgian-American physicist is honoured for building IceCube, a cubic kilometre of Antarctic ice wired with light sensors that detects high-energy neutrinos from deep space. A planned 8 cubic kilometre upgrade is due in 2033. Announced 6 October 2026.',
'{{INSIGHT_TITLE}}': 'Cheap AI Gadgets Can Ship Your Customer Data Overseas: Vet Any Smart Device Before It Goes on a Job Site',
'{{INSIGHT_BODY}}': "Australia's privacy commissioner is now investigating a maker of cheap smart glasses whose app sends AI queries and images to servers in China. Tradies are tempted by hands-free cameras for job photos and handover notes, but a bargain device can quietly upload site photos, client addresses and voices. Before any AI gadget goes on a job, ask where the data goes, whether it is encrypted, and whether you can switch the cloud features off. Do it this week: list the cameras, apps and wearables your crew uses, and drop any you can't answer those three questions about.",
'{{FACT_1}}': "IceCube, the detector behind this year's physics Nobel, uses a full cubic kilometre of Antarctic ice instrumented with light sensors to spot neutrinos.",
'{{FACT_2}}': 'Roughly 100 trillion neutrinos from the Sun pass through your body every second, and almost none of them interact with a single atom of you.',
'{{FACT_3}}': 'Mistral trained its new 1-trillion-parameter Large 4 model in about two months on 4,000 Nvidia Grace Blackwell GPUs housed in European data centres.',
'{{JOKE_SETUP}}': 'Why did the carpenter refuse to do a quote on the back of a napkin?',
'{{JOKE_PUNCHLINE}}': 'Because last time the numbers all came out in the wash, and so did the deposit.',
'{{CLOSING_QUOTE}}': '"Fall seven times, stand up eight."',
'{{CLOSING_ATTR}}': '— Japanese Proverb',
'{{CLOSING_MESSAGE}}': "It's Wednesday 7 October, dry and mild today with sunshine building Thursday and Friday, so line up your outdoor coating jobs for the warm window before showers arrive Saturday. With diesel terminal prices still high, keep that fuel line in every quote.",
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
