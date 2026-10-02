#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 3 October 2026',
'{{WEATHER_1}}': 'SAT 3 OCT · ⛈️ Very high chance of rain, possible morning storm, 6–25mm · 12–19°C',
'{{WEATHER_2}}': 'SUN 4 OCT · 🌦️ Possible morning shower, mostly dry · 11–16°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'MON 5 OCT · ⛅ Partly cloudy, dry · 10–16°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'TUE 6 OCT · 🌧️ Showers, 1–7mm · 12–19°C',
'{{WEATHER_5}}': 'WED 7 OCT · ⛅ Partly cloudy · 9–16°C',
'{{WEATHER_ALERT}}': 'Wet start to the weekend: a severe weather warning and flood watch are in place for parts of Victoria, with a possible morning storm and up to 25mm around Carrum Downs. Easing to a mostly dry Sunday and Monday, showers return Tuesday. Forecast from Melbourne BOM and online outlooks.',
'{{WORLD_1_FLAG}}': '🇵🇰 PAKISTAN / AFGHANISTAN · AIRSTRIKES ESCALATE BORDER FIGHTING',
'{{WORLD_1_HEADLINE}}': 'Pakistani Airstrikes Hit Three Houses in Afghanistan, Taliban Say Nine Killed',
'{{WORLD_1_SUMMARY}}': 'Strikes on Kunar and Helmand provinces ended three months of relative calm. Kabul says women and children were among the dead, while Islamabad says it killed 22 militants; the UN mission puts civilian deaths at 10, mostly children.',
'{{WORLD_1_URL}}': 'https://www.usnews.com/news/world/articles/2026-09-30/pakistani-airstrikes-on-afghanistan-kill-nine-kabul-says',
'{{WORLD_2_FLAG}}': '🇪🇹 ETHIOPIA / ERITREA · DIPLOMATIC TIES SEVERED AFTER DRONE STRIKES',
'{{WORLD_2_HEADLINE}}': 'Eritrea Cuts Ties With Ethiopia After Drones Strike Near Addis Ababa Military HQ',
'{{WORLD_2_SUMMARY}}': "Ethiopia closed its embassy in Asmara and expelled 10 Eritrean diplomats, accusing Eritrea of backing Tigray rebels, and Eritrea responded by severing ties. It's the worst confrontation between the neighbours since their 2018 peace deal.",
'{{WORLD_2_URL}}': 'https://www.dailymaverick.co.za/article/2026-10-02-eritrea-severs-diplomatic-ties-with-ethiopia-after-addis-ababa-orders-closure-of-embassy-in-asmara/',
'{{ECON_1_FLAG}}': '⛽ FUEL · MELBOURNE DIESEL TERMINAL GATE PRICE SITS NEAR 263 CENTS A LITRE',
'{{ECON_1_HEADLINE}}': 'Diesel Terminal Gate Price Holds Around $2.63 a Litre in Melbourne as Fuel Costs Bite',
'{{ECON_1_SUMMARY}}': 'Terminal gate diesel was about 263.5c/L in Melbourne on 2 October, before retail margins, with regional prices nearing $3. If you run diesel gear, check your fuel tax credit claims are up to date and build fuel into every quote.',
'{{ECON_1_URL}}': 'https://aip.com.au/pricing/terminal-gate-prices/',
'{{ECON_2_FLAG}}': '🥩 TRADE · CHINA BEEF TARIFF HITS BRAZIL, AUSTRALIA ALREADY OVER ITS QUOTA',
'{{ECON_2_HEADLINE}}': 'China Slaps 55% Tariff on Brazilian Beef After Quota Fills, Australia Hit Its Cap in June',
'{{ECON_2_SUMMARY}}': "China's 55% over-quota beef tariff kicked in for Brazil on 1 October, while Australia exhausted its 205,000-tonne allocation months ago. Trade friction like this ripples through regional economies and freight, a reminder to watch your customers in agriculture.",
'{{TECH_1_FLAG}}': '📞 AI · BT LAUNCHES AI RECEPTIONIST FOR SMALL FIRMS',
'{{TECH_1_HEADLINE}}': 'BT Business Launches AI Receptionist and Free AI Adoption Hub for Small Firms',
'{{TECH_1_SUMMARY}}': 'The AI Receptionist answers calls 24/7, aimed at the roughly £3.7 billion UK firms lose to missed calls, and the free hub offers practical guides and prompt packs. UK-based, but the idea is exactly what a busy tradie on the tools needs.',
'{{TECH_1_URL}}': 'https://www.webwire.com/ViewPressRel.asp?aId=361333',
'{{TECH_2_FLAG}}': '🛠️ AI · OPENAI UNVEILS NEW AGENT STACK WITH PERSISTENT CLOUD MACHINES',
'{{TECH_2_HEADLINE}}': 'OpenAI Introduces Faster Computer-Use Agents and a Decisions API for Cheap, Quick Answers',
'{{TECH_2_SUMMARY}}': 'The new stack adds persistent cloud machines and async tooling so agents can keep working on admin-style tasks in the background. Early days, but it points to AI handling routine workflows like quoting and scheduling, with you checking the output.',
'{{ROBOT_1_FLAG}}': '🦾 USA · BOSTON DYNAMICS GIVES ATLAS A NEW FOUR-FINGER HAND',
'{{ROBOT_1_HEADLINE}}': 'Boston Dynamics Unveils 13-Degree-of-Freedom Hand for Atlas Humanoid',
'{{ROBOT_1_SUMMARY}}': 'The new hand has a four-DOF opposable thumb and dense tactile sensors across the fingertips and palm, built for tool use and industrial durability. Hand dexterity has been the humanoid bottleneck, so this is a meaningful step.',
'{{ROBOT_1_URL}}': 'https://roboticsandautomationnews.com/2026/10/02/boston-dynamics-unveils-new-four-finger-hand-for-atlas-humanoid-robot/105440/',
'{{AUS_1_HEADLINE}}': 'Albanese Heads to Pacific Pre-COP Talks as Rate-Rise Blame Game Intensifies',
'{{AUS_1_SUMMARY}}': 'The PM flies to Fiji and Tuvalu for Pre-COP climate talks while the government heads into a tough final quarter, with the latest rate rise sharpening the blame argument and a budget update due in December.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-02/anthony-albanese-climate-change-ai-interest-rates/107217568',
'{{AUS_2_HEADLINE}}': 'Severe Weather Warning and Flood Watch Issued for Large Parts of Victoria',
'{{AUS_2_SUMMARY}}': 'Heavy rainfall warnings cover Gippsland, the North East, and central, south-west and north-west Victoria after Friday afternoon delivered 27mm in two hours across Melbourne. Worth checking site drainage and delaying outdoor coating work.',
'{{VIC_1_HEADLINE}}': 'Magnitude 4.8 Earthquake Near Leongatha Jolts Melbourne and Much of Victoria',
'{{VIC_1_SUMMARY}}': 'The shallow quake struck about 2am Saturday near Arawata in South Gippsland, drawing almost 15,000 felt reports with no injuries or damage reported. Geoscience Australia says it is one of the strongest in the region in two decades.',
'{{SCI_1_FLAG}}': '🧠 HEALTH · MIND DIET LINKED TO SLOWER BRAIN AGEING',
'{{SCI_1_HEADLINE}}': 'Closer Following the MIND Diet Linked to Brain Ageing Delayed by About 2.5 Years',
'{{SCI_1_SUMMARY}}': 'People who followed the diet more closely showed slower brain shrinkage and less grey matter loss over time, with the strongest differences equal to about 2.5 years of delayed brain ageing. ScienceDaily, 30 September 2026.',
'{{INSIGHT_TITLE}}': 'Missed Calls Are Missed Jobs — Trial an AI Receptionist Before You Hire Anyone',
'{{INSIGHT_BODY}}': "When you're up a ladder or in a booth, the phone rings out and that customer rings the next tradie. New AI receptionist products are now aimed squarely at small firms, answering calls, taking job details and booking callbacks around the clock. Before paying for one, track your missed calls for a week and estimate what each lead is worth. If the number is meaningful, trial a tool on a short contract, tell callers it's an assistant, and review the transcripts daily so quotes and prices still come from you.",
'{{FACT_1}}': 'The magnitude 4.8 quake near Leongatha on Saturday morning drew almost 15,000 felt reports in a few hours and was followed by a 3.1 aftershock before 3am.',
'{{FACT_2}}': "Boston Dynamics' new Atlas hand has 13 degrees of freedom, including a four-degree opposable thumb, plus tactile sensors across the fingertips and palm.",
'{{FACT_3}}': "Friday afternoon's downpour dropped 27mm on Melbourne in two hours, more than the whole of September's rainfall total.",
'{{JOKE_SETUP}}': 'A gutter cleaner was asked how his small business kept customers happy, even when storms kept refilling the same gutters he had just cleared.',
'{{JOKE_PUNCHLINE}}': 'He said, "Easy — I just treat every downpour as a repeat customer."',
'{{CLOSING_QUOTE}}': '"Whatever you are, be a good one."',
'{{CLOSING_ATTR}}': '— Abraham Lincoln',
'{{CLOSING_MESSAGE}}': "It's Saturday 3 October, wet and stormy around Carrum Downs with up to 25mm and a flood watch across the state. After a 4.8 quake rattled you awake at 2am, take the wet day to do quotes and invoicing, and aim outdoor jobs at Sunday and Monday's drier windows.",
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
