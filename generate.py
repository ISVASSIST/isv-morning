#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 13 October 2026',
'{{WEATHER_1}}': 'TUE 13 OCT · 🌧️ Cloudy with showers, about a 50% chance but only 0–1 mm · max about 15°C',
'{{WEATHER_2}}': 'WED 14 OCT · ☁️ Cloudy, 10% chance of rain · max about 15°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'THU 15 OCT · ☀️ Mostly sunny, 5% chance of rain · max about 21°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'FRI 16 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'SAT 17 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': 'Today is the showery day, but totals look light at 0 to 1 mm, so outdoor work should mostly be manageable with a few breaks. Wednesday is cloudy and dry, then Thursday looks like the best day of the week: mostly sunny and around 21°C. Based on a mirror of the Bureau of Meteorology Melbourne forecast issued Monday 12 October, so Carrum Downs may differ, and Friday and Saturday could not be confirmed.',
'{{WORLD_1_FLAG}}': '🌀 USA · HURRICANE ISAIAS',
'{{WORLD_1_HEADLINE}}': 'Hurricane Isaias Hits the Florida Panhandle, the First US Mainland Hurricane Landfall in Two Years',
'{{WORLD_1_SUMMARY}}': 'Isaias came ashore near Destin on 9 October (US time) as a Category 2 hurricane with winds of about 105 mph, after briefly reaching Category 3. It then weakened and brought flooding, wind and tornadoes across the Southeast. This is at the edge of the 48-hour window.',
'{{WORLD_1_URL}}': 'https://weather.com/2026/10/08/storms/hurricane/tropical-storm-hurricane-isaias-gulf-coast-louisiana-florida',
'{{WORLD_2_FLAG}}': '✈️ SAUDI ARABIA · RIYADH FLIGHTS',
'{{WORLD_2_HEADLINE}}': 'Houthis Warn Airlines Off Saudi Airspace as Hundreds of Riyadh Flights Are Cancelled',
'{{WORLD_2_SUMMARY}}': 'After the missile strikes on King Khalid International Airport, flight tracking showed 335 flights cancelled at Riyadh on 8 October and oil prices rose. The Houthis claimed the strike and warned airlines, though Saudi Arabia has not confirmed every claim. Flight cancellations can lift fuel costs here.',
'{{WORLD_2_URL}}': 'https://aviationweek.com/air-transport/airports-networks/riyadh-airport-attacked-houthis-second-time',
'{{ECON_1_FLAG}}': '🏆 NOBEL · ECONOMICS',
'{{ECON_1_HEADLINE}}': 'Robert Hall and Michael Woodford Win the 2026 Nobel Prize in Economics',
'{{ECON_1_SUMMARY}}': 'Announced 12 October, the prize honours the "microeconomic foundations of macroeconomic stabilisation", work on how fiscal and monetary policy can soften booms and busts. Handy context with the RBA at 4.60% and its next meeting on 3 November.',
'{{ECON_1_URL}}': 'https://www.cnbc.com/2026/10/12/nobel-economics-prize-winner-woodford-hall.html',
'{{ECON_2_FLAG}}': '⛽ FUEL · WHOLESALE PRICES',
'{{ECON_2_HEADLINE}}': 'Wholesale Petrol Climbs Again While Diesel Eases Slightly',
'{{ECON_2_SUMMARY}}': 'Australian Institute of Petroleum terminal gate data shows Sydney petrol rising from 235.6 to 240.7 cents a litre between 5 and 9 October, while diesel eased from 266.4 to 264.1. That is Sydney, not Melbourne, so check your own fuel card pricing before quoting.',
'{{TECH_1_FLAG}}': '⚡ AI · CHEAPER SMALL MODEL',
'{{TECH_1_HEADLINE}}': 'Anthropic Releases Claude Haiku 5.5, a Faster, Cheaper Small Model Built for High-Volume Work',
'{{TECH_1_SUMMARY}}': 'Aimed at jobs like summaries, data extraction and live customer support, with a reported average 75% cost saving over its predecessor. Figures are Anthropic\'s own and the release was 7 October, so this is slightly older than 48 hours.',
'{{TECH_1_URL}}': 'https://yourstory.com/ai-story/claude-haiku-5-5-anthropic-small-ai-model',
'{{TECH_2_FLAG}}': '🧩 AI · AGENTS AT WORK',
'{{TECH_2_HEADLINE}}': 'Google Cloud Introduces a "Universal Agent for Work" That Picks the Best Model for Each Job',
'{{TECH_2_SUMMARY}}': 'Per a weekly AI roundup, the agent assigns each task to the best-fitting model, choosing between Gemini and, for now, Anthropic\'s Claude. This comes from aggregator coverage rather than a Google announcement, so verify before relying on it.',
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · HUMANOIDS IN CARS',
'{{ROBOT_1_HEADLINE}}': 'BYD Unveils Design of Its First Self-Developed Humanoid Robot via a Patent',
'{{ROBOT_1_SUMMARY}}': 'A design patent published in China on 9 October describes an "Embodied AI Robot" meant for service, educational and industrial settings. It is a design filing, not a product launch, so there is no price or release date yet.',
'{{ROBOT_1_URL}}': 'https://carnewschina.com/2026/10/10/byd-unveils-design-for-its-first-self-developed-humanoid-robot',
'{{AUS_1_HEADLINE}}': 'Government Reworks Its Disaster Recovery Funding Framework to Deliver More Money After Disasters',
'{{AUS_1_SUMMARY}}': 'A 9 October federal announcement says the proposed framework will be changed after consultation, to put more funding into communities after disasters. I could only confirm the headline, not the dollar figures, so check the release for details.',
'{{AUS_1_URL}}': 'https://www.pm.gov.au/media',
'{{AUS_2_HEADLINE}}': 'Australia Signs a Bilateral Security Agreement With Ukraine as the Army Expands Its HIMARS Fleet',
'{{AUS_2_SUMMARY}}': 'Federal defence releases from 7 October list the Ukraine agreement and a larger Army HIMARS rocket launcher fleet. This is older than 48 hours and I could not confirm the terms.',
'{{VIC_1_HEADLINE}}': 'Premier Carroll and Opposition Leader Wilson Unveil Duelling Policies on Mineral Royalties and Technical Colleges',
'{{VIC_1_SUMMARY}}': 'ABC News Victoria reports the Monday announcements come ahead of next month\'s state election. Separately, a seventh straight day of Melbourne arson attacks includes a Fitzroy North tobacco shop fire.',
'{{SCI_1_FLAG}}': '🍄 BIOLOGY · MUSHROOM DISEASE',
'{{SCI_1_HEADLINE}}': 'A 100-Year-Old Mushroom Disease Turns Out to Involve More Than 17 Species of Harmful Bacteria',
'{{SCI_1_SUMMARY}}': 'ScienceDaily reports researchers found the long-studied disease is not caused by one bacterium as believed but by a whole group. I only saw the headline summary, so check the full study for details.',
'{{INSIGHT_TITLE}}': 'Write Your Quoting Process Down First: AI Can Only Copy a Process You Can Describe',
'{{INSIGHT_BODY}}': 'New AI tools keep getting cheaper and faster, but they do the same job you give them, which is only as clear as your instructions. Before you pay for another tool, spend an hour writing down how you quote: what you measure, which prices you check, what you add for travel and fuel, and what you always forget. That one page becomes the instruction sheet for any AI helper and a checklist for staff, and it exposes the guesswork that quietly eats margin. Start with your most common job type and test the page on a past quote.',
'{{FACT_1}}': 'The Economics Nobel is formally the Sveriges Riksbank Prize, created by Sweden\'s central bank in 1968, so it is not one of the five original prizes in Alfred Nobel\'s will.',
'{{FACT_2}}': 'Hurricane Isaias was the first hurricane to make landfall on the US mainland in exactly two years, in an unusually quiet Atlantic season.',
'{{FACT_3}}': 'Anthropic says Claude Haiku 5.5 scored 72.4% on a computer-use test subset where its predecessor managed only 15.7%.',
'{{JOKE_SETUP}}': 'Why did the excavator operator keep winning tenders against bigger firms?',
'{{JOKE_PUNCHLINE}}': '"He always dug deep into the numbers before he broke any ground."',
'{{CLOSING_QUOTE}}': '"Measure twice, cut once."',
'{{CLOSING_ATTR}}': '— English Proverb',
'{{CLOSING_MESSAGE}}': "It's Tuesday 13 October with light showers around, but only 0 to 1 mm is expected, so keep outdoor work flexible and do quotes and paperwork in the wet patches. Thursday looks sunny and warmer at about 21°C, so line up the best outdoor job for then. Write down how you quote today and your future self will thank you.",
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
