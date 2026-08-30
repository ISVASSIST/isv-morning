#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 31 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 31 Aug (BOM)
    "{{WEATHER_1}}": "MON 31 · ⛅ Partly cloudy, mild, slight shower chance · 8–15°C",
    "{{WEATHER_2}}": "TUE 1 SEP · 🌦️ Partly cloudy, showers most likely early morning · 7–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 2 SEP · 🌧️ Showers likely, windy northerly change · 9–16°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 3 SEP · 🌧️ Cloudy, very high chance of rain, windy · 9–15°C",
    "{{WEATHER_5}}": "FRI 4 SEP · 🌦️ Showers easing, cooler · 8–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula. Today is the last day of winter — a mild, partly cloudy send-off — before a wetter, windier pattern builds through Wednesday and Thursday as spring gets underway.",

    # World
    "{{WORLD_1_FLAG}}": "🇳🇵 NEPAL · FLOOD TOLL CLIMBS TO 750, THOUSANDS STILL MISSING",
    "{{WORLD_1_HEADLINE}}": "Nepal-Tibet Flood Death Toll Rises to 750 as Over 3,000 Remain Missing",
    "{{WORLD_1_SUMMARY}}": "The death toll from last week's catastrophic Himalayan flash floods has climbed to 750 across Nepal and Tibet, with more than 3,000 people still unaccounted for; officials say 734 of the dead were in Nepal, where 7,514 people have been rescued so far, while 16 deaths and 546 missing have been confirmed on the Chinese side of the border.",
    "{{WORLD_1_URL}}": "https://abcnews.com/International/nepal-tibet-flood-death-toll-rises-750-officials/story?id=136067514",

    "{{WORLD_2_FLAG}}": "🇮🇸 ICELAND · VOTERS REJECT REOPENING EU MEMBERSHIP TALKS",
    "{{WORLD_2_HEADLINE}}": "Iceland Narrowly Votes Against Restarting EU Membership Talks",
    "{{WORLD_2_SUMMARY}}": "Icelanders voted 52.8% to 47.2% against resuming European Union accession negotiations in a closely fought referendum, where control over fishing rights outweighed the case for closer security ties with Europe; Reykjavik was the only region where a majority backed reopening talks.",
    "{{WORLD_2_URL}}": "https://www.abc.net.au/news/2026-08-30/iceland-eu-referendum-result/107095748",

    # Economics
    "{{ECON_1_FLAG}}": "📉 ASX · SHARES SLIDE AS BANKS FLAG AN EARLIER RATE HIKE",
    "{{ECON_1_HEADLINE}}": "ASX Posts Worst Session Since June as Three of the Big Four Banks Warn a Rate Hike Could Land Sooner",
    "{{ECON_1_SUMMARY}}": "The S&P/ASX200 fell just under 1% in its worst session since early June after ANZ and CommBank economists brought forward their call for a rate rise to November and NAB flagged a possible move as soon as the RBA's 29 September meeting, following a hotter-than-expected 3.6% trimmed-mean inflation reading; a September or November hike would land squarely in the middle of spring trading for anyone carrying equipment finance or a business loan.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-08-27/asx-markets-business-news-live-updates-thursday-27-august/107083084",

    "{{ECON_2_FLAG}}": "⛽ DIESEL · NATIONAL AVERAGE NOW PAST $2.50 A LITRE",
    "{{ECON_2_HEADLINE}}": "Diesel Climbs Past $2.50 a Litre Nationally as Full Excise Bites Harder Than Petrol",
    "{{ECON_2_SUMMARY}}": "With the temporary fuel excise cut fully unwound since 3 August, the national diesel average has climbed to around 252 cents a litre against roughly 205 cents for unleaded — a gap that hits trade vehicles, generators and diesel-powered compressors hardest, on top of prices already running about 13.6 cents higher than a month ago.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "⚖️ AI COPYRIGHT · MUSIC PUBLISHERS SUE ANTHROPIC OVER CLAUDE",
    "{{TECH_1_HEADLINE}}": "Sony Music Publishing and Warner Chappell Sue Anthropic Over Song Lyrics Used to Train Claude",
    "{{TECH_1_SUMMARY}}": "Two of the three major music publishers have filed a multi-billion-dollar lawsuit accusing Anthropic of illegally torrenting and scraping tens of thousands of copyrighted songs — including 'Eye of the Tiger' and 'All I Want for Christmas Is You' — to train its Claude models, seeking up to $150,000 per work; a reminder that the AI tools a business leans on can carry legal risk from well outside its own four walls.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/08/29/sony-music-warner-sue-anthropic-alleging-a-brazen-campaign-of-intellectual-property-theft/",

    "{{TECH_2_FLAG}}": "🤖 AI LABOUR · AMAZON SHUTS DOWN 21-YEAR-OLD 'ARTIFICIAL AI' PLATFORM",
    "{{TECH_2_HEADLINE}}": "Amazon to Close Mechanical Turk on 30 September After 21 Years",
    "{{TECH_2_SUMMARY}}": "Amazon is shutting down Mechanical Turk, the crowdsourced task marketplace Jeff Bezos once called 'artificial artificial intelligence,' after newer data-labelling startups and far more capable AI models made the platform redundant — a small sign of how quickly the tools underneath the AI boom keep turning over.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 INDUSTRIAL HUMANOIDS · ATLAS GOES INTO MASS PRODUCTION",
    "{{ROBOT_1_HEADLINE}}": "Boston Dynamics Moves All-Electric Atlas Into Mass Production for Factory and Hazardous-Site Work",
    "{{ROBOT_1_SUMMARY}}": "Boston Dynamics and Hyundai are scaling up production of the all-electric Atlas humanoid, which swaps the old hydraulic system for high-torque electric actuators aimed at the reliability and energy-efficiency problems that kept earlier versions as lab demos; fleets are already doing logistics and material-handling work at Hyundai's Georgia Metaplant, built to be tough enough for hazardous, awkward jobs yet dexterous enough to handle variable parts.",
    "{{ROBOT_1_URL}}": "https://newatlas.com/ai-humanoids/boston-dynamics-production-atlas-hyundai/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Adelaide Reveals $96 Million MotoGP Street Circuit Design, Nearly 400 Parklands Trees to Go",
    "{{AUS_1_SUMMARY}}": "South Australian Premier Peter Malinauskas has unveiled the design for a 4.13km MotoGP street circuit through Adelaide's eastern parklands, with 42 significant trees and 335 others to be removed for the 2027-targeted track; the government says it will replant at a 10-to-1 ratio and put $15 million toward habitat restoration along the Torrens River.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-30/sa-motogp-street-circuit-design-released/107094958",

    "{{AUS_2_HEADLINE}}": "Queensland's Toughest-in-the-Country E-Bike and E-Scooter Laws Start Today",
    "{{AUS_2_SUMMARY}}": "From today, Queensland riders need to be at least 16 and hold a driver's licence to ride an e-bike or e-scooter solo, with under-16s banned from riding unsupervised — among the strictest e-mobility licensing rules in the world, though a three-month grace period applies for anyone seeking a medical exemption.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Premier Ben Carroll Commits Extra $352 Million to Double Pothole Repairs This Year",
    "{{VIC_1_SUMMARY}}": "Premier Ben Carroll has announced an extra $352 million in road funding to lift the number of potholes fixed this year from 250,000 to 500,000, prioritising the Princes and Western highways and other regional roads, with most repairs expected through the second half of the year and into January when conditions are driest.",

    # Science
    "{{SCI_1_FLAG}}": "🔴 MARS · A HIDDEN HEAT DIVIDE DEEP INSIDE THE RED PLANET",
    "{{SCI_1_HEADLINE}}": "Scientists Discover Mars's Southern Interior Is Hundreds of Degrees Hotter Than Its North — and Possibly Still Molten",
    "{{SCI_1_SUMMARY}}": "A Caltech-led gravity study published in Nature finds Mars's interior beneath its southern hemisphere runs 200-400°C hotter than the north and may be partially molten, a discovery that could help explain the planet's lopsided magnetism, seismic quirks and the timing of its ancient, wetter past.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Construction Is Australia's Most AI-Shy Industry — That's Actually Good News for You",
    "{{INSIGHT_BODY}}": "Regular AI use across Australian small and medium businesses has jumped from 40% to 69% in under two years, but construction and agriculture remain the stragglers, both still under 30% adoption — the lowest of any sector tracked. It's tempting to read that as trades being behind, but it also means the bar most tradies are being judged against is still low: a handful of well-used tools for quoting, scheduling and follow-up admin puts you ahead of most of the industry, not just even with it. The businesses that will feel the squeeze aren't the ones moving carefully — they're the ones that never move at all.",

    # Fun facts
    "{{FACT_1}}": "One of the first video games with a graphical display, Tennis for Two, was built in 1958 by physicist William Higinbotham on an oscilloscope at Brookhaven National Laboratory for a public open house — an analog computer simulated gravity, and visitors could even adjust the setting to play under the gravity of the Moon or Jupiter.",
    "{{FACT_2}}": "Chicken tikka masala, often called Britain's true national dish, is widely credited to a Glasgow curry house in the 1970s, where a chef reportedly added a tin of tomato soup to a dry chicken tikka after a customer complained it needed gravy.",
    "{{FACT_3}}": "The Zamboni ice resurfacer was invented in 1949 by Californian rink owner Frank Zamboni, who got sick of it taking well over an hour of tractor towing and hand squeegeeing to resurface his own rink between skating sessions.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the asbestos removal contractor become the most trusted businessman in town?",
    "{{JOKE_PUNCHLINE}}": "Because he was the only tradie who always came clean.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Spring is the time of plans and projects.\"",
    "{{CLOSING_ATTR}}": "— Leo Tolstoy",
    "{{CLOSING_MESSAGE}}": "It's the last day of winter in Carrum Downs — mild and partly cloudy today before a wetter, windier pattern builds through Wednesday and Thursday as spring properly arrives tomorrow. With three of the big four banks now tipping a rate rise as soon as September, and diesel sitting well above $2.50 a litre, it's a fair Monday to get outdoor jobs moving early and double-check any finance or fuel budgeting before the numbers shift again.",
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
