#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 6 October 2026',
'{{WEATHER_1}}': 'TUE 6 OCT · 🌦️ Showers, high chance early afternoon, gusty NW winds · 9–17°C',
'{{WEATHER_2}}': 'WED 7 OCT · ⛅ Cloud clearing, very low chance of rain · 9–18°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'THU 8 OCT · ☀️ Sunny and dry · 8–23°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'FRI 9 OCT · ☀️ Mostly sunny and warm · 12–26°C',
'{{WEATHER_5}}': 'SAT 10 OCT · ⛈️ Showers likely, possible storms · 13–24°C',
'{{WEATHER_ALERT}}': 'Showers and gusty north-westerlies today, so keep outdoor coating and blasting indoors or on hold until Wednesday. Thursday and Friday look dry and warm, the best window this week, before rain returns Saturday. Sources are BOM Melbourne and AccuWeather outlooks, so Carrum Downs may differ slightly.',
'{{WORLD_1_FLAG}}': '🇪🇸 SPAIN · SNAP ELECTION CALLED OVER HOUSING CRISIS',
'{{WORLD_1_HEADLINE}}': "Spain's Pedro Sánchez Announces Snap Election Amid Housing Crisis",
'{{WORLD_1_SUMMARY}}': 'After parliament voted down two emergency renter-protection decrees, Sánchez called a general election for 29 November, saying he needs a bigger progressive majority. He faces conservative Popular Party leader Alberto Núñez Feijóo.',
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/10/5/spanish-prime-minister-pedro-sanchez-announces-snap-election',
'{{WORLD_2_FLAG}}': '🏅 SWEDEN · NOBEL PRIZE FOR USING LIGHT TO SWITCH ON BRAIN CELLS',
'{{WORLD_2_HEADLINE}}': 'Deisseroth, Hegemann and Nagel Awarded 2026 Nobel Prize in Medicine',
'{{WORLD_2_SUMMARY}}': 'The prize recognises optogenetics, a technique that uses light and genetics to switch individual nerve cells on or off. It grew from studying how algae swim toward light, and it now underpins brain research worldwide.',
'{{WORLD_2_URL}}': 'https://www.statnews.com/2026/10/05/nobel-prize-medicine-2026-winner-deisseroth-hegemann-nagel/',
'{{ECON_1_FLAG}}': '⛽ FUEL · DIESEL STILL NEAR RECORD HIGHS',
'{{ECON_1_HEADLINE}}': 'Australian Diesel Stays Above $2.60 a Litre After a 40% Climb Since July',
'{{ECON_1_SUMMARY}}': 'ACCC-confirmed data shows diesel hit about 287 cents a litre in late September, up roughly 40% from the early July low, with the US-Iran conflict still driving supply. Keep a fuel line or surcharge clause in every quote.',
'{{ECON_1_URL}}': 'https://dailyfuels.com/australia/',
'{{ECON_2_FLAG}}': '🏦 SMALL BUSINESS · RATES AND FUEL SQUEEZE TOGETHER',
'{{ECON_2_HEADLINE}}': 'Fuel Prices and Rate Expectations Pressure Australian Businesses',
'{{ECON_2_SUMMARY}}': 'With the cash rate at 4.6%, a 15-year high, and fuel costs flowing through to supplies, small operators face higher borrowing and input costs while customers get more cautious. Review overdraft and equipment finance repayments now.',
'{{TECH_1_FLAG}}': '💬 AI · CHATGPT FREE TIER GETS VISUAL ADS',
'{{TECH_1_HEADLINE}}': 'OpenAI to Test Visual Ads Inside ChatGPT Image Generation',
'{{TECH_1_SUMMARY}}': 'A US test starts later this month on the free tier, showing clearly labelled ads beside generated images, while paid plans stay ad-free. If your business uses free AI tools, assume they are ad-funded and check what you paste into them.',
'{{TECH_1_URL}}': 'https://enterprisetimes.co.uk/2026/10/05/security-and-ai-news-from-the-week-beginning-28-september-2026',
'{{TECH_2_FLAG}}': '🕶️ AI · SILENT HANDWRITING WITH META NEURAL BAND',
'{{TECH_2_HEADLINE}}': "Meta's Neural Band Lets Wearers Write Messages and AI Queries With a Finger",
'{{TECH_2_SUMMARY}}': 'The wrist band reads muscle signals so you can write on any surface and message or ask AI without touching a phone. Early days, but hands-free input suits workshops where gloves and dust make screens a pain.',
'{{ROBOT_1_FLAG}}': '🤖 USA · FCC LIMITS NEW FOREIGN-MADE MOBILE ROBOTS',
'{{ROBOT_1_HEADLINE}}': 'FCC Robot Restrictions Could Accelerate Shift to Local AI',
'{{ROBOT_1_SUMMARY}}': 'US rules now block FCC authorisation for new foreign-made humanoids, quadrupeds and other connected mobile robots, so builders are pushing processing onto the robot itself. Expect more local-AI robots, and pricing and supply shifts for imports. Published 5 October.',
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/fcc-robot-restrictions-could-accelerate-shift-to-local-ai/',
'{{AUS_1_HEADLINE}}': "South Australia's AI Royal Commission Prepares to Face OpenAI and Big Tech",
'{{AUS_1_SUMMARY}}': 'The first Australian royal commission into AI began 1 October and will examine work, education and public services, reporting by July 2027. Its findings could shape how small businesses are allowed to use AI.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-06/openai-fronts-ai-inquiry/107230434',
'{{AUS_2_HEADLINE}}': 'Tornado Rips Through Ulladulla Cafe on NSW South Coast',
'{{AUS_2_SUMMARY}}': 'A tornado tore chairs and tables off a cafe balcony in Ulladulla amid severe storms, a reminder to check outdoor equipment and site securing when wild weather is forecast.',
'{{VIC_1_HEADLINE}}': "Three Oppositions Are Contesting Victoria's Election, and the Premier Leads One",
'{{VIC_1_SUMMARY}}': 'Eight weeks out from the 28 November election, Premier Ben Carroll is fighting the Coalition, One Nation (polling around one in four voters) and his own Labor record. One Nation launched its platform on Saturday with a heavy law-and-order and tax-relief focus.',
'{{SCI_1_FLAG}}': '🪐 SPACE · A PLANET BORN FROM A DEAD STAR',
'{{SCI_1_HEADLINE}}': "Astronomers Find a 'Phoenix' Planet Reborn From Its Star's Ashes",
'{{SCI_1_SUMMARY}}': "University of Warwick-led astronomers using Hubble found the first likely second-generation planet orbiting a white dwarf, HS 0209+0832, about 270 light-years away. The star's atmosphere is rich in niobium, zinc and copper. Published 5 October 2026.",
'{{INSIGHT_TITLE}}': 'Free AI Is Becoming Ad-Funded: Pay for the Tier Where Your Customer Data Stays Private',
'{{INSIGHT_BODY}}': "With ads heading to ChatGPT's free tier, the old rule applies: if you aren't paying, your inputs are part of the product. Before you paste a customer quote, address or site photo into a free AI tool, check the privacy settings. A paid business plan costs about the price of a few coffees a month and usually keeps your data out of training. Do it this week: list the AI tools you use, note which are free, and move any that touch customer details onto a paid plan.",
'{{FACT_1}}': "Niobium, found at about 1,000 times solar levels in the white dwarf HS 0209+0832's atmosphere, is the same metal added in tiny amounts to high-strength steel for pipelines and bridges.",
'{{FACT_2}}': 'Optogenetics grew from Chlamydomonas, a single-celled green alga that swims toward light using rhodopsin proteins, the same family of proteins found in your eyes.',
'{{FACT_3}}': "The Nobel Prize in Physiology or Medicine comes with 12 million Swedish crowns, about US$1.7 million, which the three optogenetics winners will split between them.",
'{{JOKE_SETUP}}': 'A roof plumber was asked how his small business never lost a customer, even when he turned up in the rain.',
'{{JOKE_PUNCHLINE}}': 'He said, "Simple — I quote the job fair, and when it rains I still show up, because a customer will forgive a wet plumber but never a no-show."',
'{{CLOSING_QUOTE}}': '"Whatever you can do, or dream you can, begin it. Boldness has genius, power and magic in it."',
'{{CLOSING_ATTR}}': '— Johann Wolfgang von Goethe',
'{{CLOSING_MESSAGE}}': "It's Tuesday 6 October and showers with gusty winds are due this afternoon, so keep outdoor work indoors and plan the dry window on Thursday and Friday. With diesel near $2.60 a litre, check every quote carries a fuel line.",
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
