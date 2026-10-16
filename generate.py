#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 17 October 2026',
'{{WEATHER_1}}': 'SAT 17 OCT · ⛅ Partly cloudy, 5% chance of rain · 12–25°C',
'{{WEATHER_2}}': 'SUN 18 OCT · ☀️ Sunny, 5% chance of rain · 13–26°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'MON 19 OCT · outlook not confirmed',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'TUE 20 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'WED 21 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': "A dry, mild weekend: Saturday 12–25°C and partly cloudy, Sunday 13–26°C and sunny, per the Bureau of Meteorology Melbourne forecast issued 4:05am Friday. UV is forecast to reach 8 (very high) both days, so cover up. I could not find a confirmed outlook for Monday to Wednesday, and Carrum Downs may differ slightly from these Melbourne figures.",
'{{WORLD_1_FLAG}}': '🇾🇪 YEMEN · HOUTHIS',
'{{WORLD_1_HEADLINE}}': "Houthis Reportedly Strike Yemen Government Seat in Aden, Killing Five",
'{{WORLD_1_SUMMARY}}': "Just Security's 16 October Early Edition reports the strike on Maashiq Palace, the seat of Yemen's internationally recognised government. The prime minister was not hurt. I only saw the opening items, so details are limited.",
'{{WORLD_1_URL}}': 'https://www.justsecurity.org/161058/early-edition-october-16-2026/',
'{{WORLD_2_FLAG}}': '🛢️ IRAN WAR · OIL',
'{{WORLD_2_HEADLINE}}': 'Iran Has Exported Some LPG and Jet Fuel Since July Despite the US Naval Blockade, Sources Say',
'{{WORLD_2_SUMMARY}}': "The same 16 October roundup cites Reuters sources and shipping intelligence. It suggests the blockade is leakier than advertised, which matters for fuel prices. Summary only, so treat the detail with caution.",
'{{WORLD_2_URL}}': 'https://www.justsecurity.org/161058/early-edition-october-16-2026/',
'{{ECON_1_FLAG}}': '⛽ FUEL · AUSTRALIA',
'{{ECON_1_HEADLINE}}': 'Petrol Tops $2.40 a Litre Nationally for the First Time in Over Six Months',
'{{ECON_1_SUMMARY}}': "Reports from 12 to 14 October put the national petrol average near $2.41, up about 3 cents on the week, tied to Middle East conflict. ABC is asking whether high fuel prices are here to stay. The figures are a few days old, so check your own supplier.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/listen/programs/abc-news-top-stories/is-the-high-price-of-fuel-here-to-stay-/107268406',
'{{ECON_2_FLAG}}': '🚛 DIESEL · G7 RELEASE',
'{{ECON_2_HEADLINE}}': 'Diesel Eases to About $2.83 a Litre After G7 Oil Reserve Release, But Relief Looks Limited',
'{{ECON_2_SUMMARY}}': "Reports around 12 to 14 October say diesel slipped 1 cent after the G7 agreed to release 100 million barrels, though Australia's reliance on imported refined fuel limits the benefit. Figures are a few days old, so check your fuel card rate before quoting fuel-heavy jobs.",
'{{TECH_1_FLAG}}': '🤖 AI · GOOGLE',
'{{TECH_1_HEADLINE}}': 'Google Releases Gemini 4 Argon in Antigravity for AI Pro Subscribers',
'{{TECH_1_SUMMARY}}': 'A tech blog reports the release on 15 October, with a weekly quota separate from the Gemini 3.8 Flash one. I only saw a secondary source, but it is a newer model you can try on a paid plan.',
'{{TECH_1_URL}}': 'https://pasqualepillitteri.it/en/news/24640/gemini-4-argon-antigravity-ai-pro-separate-weekly-quota',
'{{TECH_2_FLAG}}': '⚙️ AI · AGENTS',
'{{TECH_2_HEADLINE}}': 'Anthropic Managed Agents Adds Dynamic Workflows, Scheduled Deployments and Lower Cache Pricing',
'{{TECH_2_SUMMARY}}': 'A Substack roundup lists the update. It is aimed at developers rather than tradies, and I could not confirm the exact date, but cheaper and more automated agents tend to reach the business tools you use.',
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS · KOREA',
'{{ROBOT_1_HEADLINE}}': "Korea Clears Safety Rules to Put 20 Robros Humanoid Robots on Factory Floors",
'{{ROBOT_1_SUMMARY}}': "Seoul Economic Daily (14 October, so slightly outside 48 hours) says the pilot puts 20 bipedal humanoids alongside people at semiconductor, auto, shipbuilding and logistics sites. Summary only seen.",
'{{ROBOT_1_URL}}': 'https://en.sedaily.com/finance/2026/10/14/korea-clears-safety-rules-to-put-20-humanoid-robots-on',
'{{AUS_1_HEADLINE}}': "Government Open to Greens' Push to Let People Sue Online Platforms",
'{{AUS_1_SUMMARY}}': "Crikey's 16 October piece says the government is open to giving individuals a right to take legal action against platforms, after dropping ministerial powers to designate new online harms. Paywalled, so I saw only the opening.",
'{{AUS_1_URL}}': 'https://www.crikey.com.au/2026/10/16/labor-digital-bill-greens-david-shoebridge-trump-livestream-execution/',
'{{AUS_2_HEADLINE}}': 'Federal Assessment Pauses a Large Wind Farm Project in Victoria and the Murray Region',
'{{AUS_2_SUMMARY}}': "ABC's 16 October Mildura-Swan Hill and Wimmera briefing says federal assessors asked for more information before the project can proceed. Briefing summary only.",
'{{VIC_1_HEADLINE}}': 'Ambulance Services Face Disruption as Paramedics Take Industrial Action Over Pay',
'{{VIC_1_SUMMARY}}': "ABC's 16 October Goulburn-Murray and Shepparton briefing reports the action. Summary only, so check the Ambulance Victoria notices for how it affects your area.",
'{{SCI_1_FLAG}}': '🧠 NEUROSCIENCE',
'{{SCI_1_HEADLINE}}': 'Yale Scientists Discover How Stress Changes the Brain to Make Emotional Memories Stronger',
'{{SCI_1_SUMMARY}}': 'ScienceDaily lists it on 16 October, tracing how the stress hormone cortisol helps form stronger, longer-lasting memories of emotional events. I only saw the teaser.',
'{{INSIGHT_TITLE}}': 'Ask AI to Check Your Quote Against the Job Brief for Missed Items',
'{{INSIGHT_BODY}}': "Missed items are where tradies lose money: a second coat, access gear, disposal or travel time. Paste the customer's brief and your draft quote (no personal details) into an AI tool and ask it to list anything in the brief the quote does not cover. It takes two minutes, and you decide what to add. One caught item on a job can pay for the whole month's subscription, which matters with diesel near $2.83 a litre.",
'{{FACT_1}}': 'Yale researchers say the stress hormone cortisol helps the brain form stronger, longer-lasting memories of emotional events.',
'{{FACT_2}}': "Shanghai's new plan targets 8,000 humanoid robots working in factories and 500 advanced smart factories by 2028.",
'{{FACT_3}}': 'The G7 agreed to release 100 million barrels of oil and diesel from strategic reserves, according to recent reports.',
'{{JOKE_SETUP}}': 'Why did the landscaper never worry about a late-paying client?',
'{{JOKE_PUNCHLINE}}': '"Because he always planted the invoice before the first seed."',
'{{CLOSING_QUOTE}}': '"Slow and steady wins the race."',
'{{CLOSING_ATTR}}': '— Aesop',
'{{CLOSING_MESSAGE}}': "It's Saturday 17 October, partly cloudy and up to 25°C with a sunny, dry Sunday to follow, a good weekend to rest or tick off jobs around home. Petrol is above $2.40 and diesel near $2.83, so go over your fuel costs before Monday's quotes.",
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
