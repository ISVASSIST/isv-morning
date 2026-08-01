#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 02 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 02 Aug (BOM)
    "{{WEATHER_1}}": "SUN 02 · ☀️ Sunny, patches of morning frost · 3–17°C",
    "{{WEATHER_2}}": "MON 03 · 🌧️ Showers, possible small hail · 9–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 04 · 🌧️ Showers, easing later · 8–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 05 · ⛅ Partly cloudy, drier · 7–15°C",
    "{{WEATHER_5}}": "THU 06 · 🌦️ Shower or two, clearing · 7–13°C",
    "{{WEATHER_ALERT}}": "⚠ NO SEVERE WEATHER WARNINGS CURRENTLY ACTIVE FOR VICTORIA",

    # World
    "{{WORLD_1_FLAG}}": "🇪🇸🇲🇦 CEUTA · BORDER CRISIS DEATH TOLL CLIMBS TO 67 · 60,000 CROSSED FRONTIER IN 24 HOURS",
    "{{WORLD_1_HEADLINE}}": "Death Toll in Spain's Ceuta Border Crisis Reaches 67 as Tens of Thousands Cross Back Into Morocco",
    "{{WORLD_1_SUMMARY}}": "Around 60,000 migrants breached the frontier of Spain's North African enclave Ceuta over a single 24-hour period, most swimming around breakwaters or crossing on foot, in a stampede that killed dozens by drowning or crush injuries. Spain is now installing a 500-metre containment barrier and says most who entered have already returned to Morocco — a stark reminder of how quickly a stable border situation can unravel, though the direct impact on Australian trade is minimal.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/01/nx-s1-5916271/ceuta-spain-border-morocco",

    "{{WORLD_2_FLAG}}": "🇮🇷🇺🇸 MIDEAST · TRUMP THREATENS FRESH IRAN STRIKES · US EMBASSIES TELL CITIZENS TO BE READY TO LEAVE",
    "{{WORLD_2_HEADLINE}}": "Trump Threatens New Strikes on Iran as US Embassies Across the Middle East Warn Citizens to Prepare to Depart",
    "{{WORLD_2_SUMMARY}}": "US missions in Amman, Jerusalem, Muscat, Baghdad and Beirut issued security alerts warning of 'unforeseen escalation' after Trump vowed to hit Iran 'very hard' again in a push to reopen the Strait of Hormuz. It's the kind of flashpoint that tends to move oil markets fast — worth watching given roughly a fifth of the world's traded oil passes through that strait, with any spike likely to show up at the bowser here within days.",
    "{{WORLD_2_URL}}": "https://www.washingtonpost.com/world/2026/08/01/trump-iran-strait-hormuz-israel-gaza-mideast/6818cc9c-8d86-11f1-8912-d71e69d679d7_story.html",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺⛽ FUEL · EXCISE DISCOUNT ENDS AT MIDNIGHT TONIGHT · PETROL AND DIESEL SET TO JUMP FROM MONDAY",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Discount Ends at Midnight Tonight, With Petrol and Diesel Both Set to Rise From Monday",
    "{{ECON_1_SUMMARY}}": "Treasurer Jim Chalmers has confirmed the remaining fuel excise discount disappears at midnight tonight, with unleaded expected to rise by up to 16 cents a litre from Monday plus a further indexation increase on top. Diesel is already averaging around 231 cents a litre nationally, so tonight's the last cheap fill before it and the ute both cost more from tomorrow.",
    "{{ECON_1_URL}}": "https://www.carexpert.com.au/car-news/fuel-prices-to-rise-when-excise-cut-ends-within-days",

    "{{ECON_2_FLAG}}": "🇦🇺📊 SMALL BUSINESS · AUSTRALIAN SMES NOW THE LEAST OPTIMISTIC IN THE ASIA-PACIFIC",
    "{{ECON_2_HEADLINE}}": "Australian Small Businesses Are the Least Optimistic in the Asia-Pacific, New Regional Survey Finds",
    "{{ECON_2_SUMMARY}}": "CPA Australia's Asia-Pacific Small Business Survey found just 53 per cent of Australian small businesses expect to grow in 2026, well below the 70 per cent survey average and the lowest growth expectation of the 11 markets surveyed. It's a useful gut-check for benchmarking your own outlook against the wider small business sector rather than assuming everyone else is having an easier run.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI ECONOMICS · CHINA'S DEEPSEEK RELEASES FRONTIER-CLASS MODEL AT A TENTH OF WESTERN PRICING",
    "{{TECH_1_HEADLINE}}": "DeepSeek Quietly Releases a Frontier-Class AI Model at Roughly a Tenth of the Price of Its Western Rivals",
    "{{TECH_1_SUMMARY}}": "DeepSeek's V4 Flash model officially exited preview this week priced at 14 US cents per million input tokens, matching or beating larger rivals on agent benchmarks despite the bargain price. It's another data point in a now-familiar pattern — useful AI capability keeps getting cheaper every few months — worth keeping in mind before you commit to a pricier subscription for the software you're using to run quotes or admin.",
    "{{TECH_1_URL}}": "https://www.digitalapplied.com/blog/deepseek-v4-flash-0731-official-release-agent-benchmarks",

    "{{TECH_2_FLAG}}": "🎓 AI ACCESS · OPENAI COMMITS $250M TO GIVE 100,000 RESEARCHERS FREE ACCESS TO ITS TOP MODELS",
    "{{TECH_2_HEADLINE}}": "OpenAI Commits $250 Million to Give 100,000 Researchers Free Access to Its Best AI Models",
    "{{TECH_2_SUMMARY}}": "OpenAI's new 'ChatGPT for Academic Researchers' program starts with 10,000 scientists this year, scaling to 100,000 by 2027, each able to bring four collaborators along for free. It shows how hard the big AI labs are competing on giving capability away for loyalty right now — a trend that tends to flow through to cheaper or free tiers for everyday users and small businesses over time.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · UNITREE OPENS IPO BOOK-BUILDING · FIRST PROFITABLE HUMANOID ROBOT MAKER TO GO PUBLIC",
    "{{ROBOT_1_HEADLINE}}": "Unitree Opens IPO Subscription in Shanghai, Set to Become the First Profitable Humanoid Robot Maker to List Publicly",
    "{{ROBOT_1_SUMMARY}}": "Unitree shipped more than 5,500 humanoid robots in 2025 and is targeting 20,000 this year, with book-building opening this week ahead of a Shanghai STAR Market listing at a roughly ¥42 billion valuation. It's the first real market test of whether humanoid robotics is an actual profitable business today rather than just a well-funded hype story.",
    "{{ROBOT_1_URL}}": "https://www.techtimes.com/articles/322574/20260731/unitree-ipo-subscription-opens-profitable-robot-maker-vs-39b-no-revenue-figure-ai.htm",

    # Australia
    "{{AUS_1_HEADLINE}}": "Bluey Learns to Speak Yolŋu Matha as Garma Festival Celebrates a First for Indigenous Language on Screen",
    "{{AUS_1_SUMMARY}}": "Five episodes of Bluey dubbed entirely in Yolŋu Matha by local voice talent screened for the first time at the Garma Festival in Arnhem Land, produced by Yolŋu Radio, ABC and Ludo Studio alongside the Aboriginal Resource and Development Services. A genuinely heartwarming story out of Australia's largest Indigenous gathering, running through the weekend.",
    "{{AUS_1_URL}}": "https://www.dailyadvertiser.com.au/story/9321152/bluey-big-ideas-and-bukmak-all-in-as-garma-lights-up/",

    "{{AUS_2_HEADLINE}}": "Australia Wraps Up Its Best-Ever Commonwealth Games as Glasgow's Closing Ceremony Hands the Torch to Ahmedabad 2030",
    "{{AUS_2_SUMMARY}}": "Team Australia heads into tonight's closing ceremony with 55 gold medals and 128 medals overall, comfortably topping the table ahead of Canada and England, with swimming, athletics and even 3x3 basketball all contributing. Simple Minds headlines the handover show at Glasgow's Hydro arena before the Games move to India in 2030.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Has the Cheapest Petrol in the Country Tonight — That Won't Survive the Weekend",
    "{{VIC_1_SUMMARY}}": "Victoria currently has the lowest average unleaded price of any state at 197.1 cents a litre, but that edge disappears once the federal fuel excise discount ends at midnight and prices rise nationwide from Monday. If you're planning to fill up the ute or any site plant, tonight is genuinely the cheapest it'll be for a while.",

    # Science
    "{{SCI_1_FLAG}}": "🌋 GEOLOGY · 'SUPERHEATED' MAGMA FOUND TO RADICALLY CHANGE HOW VOLCANOES ERUPT",
    "{{SCI_1_HEADLINE}}": "Scientists Discover 'Superheated' Magma Can Radically Change How a Volcano Erupts",
    "{{SCI_1_SUMMARY}}": "A University of Manchester-led team studying magma from the 2021 Tajogaite eruption on La Palma found that magma heated beyond the temperature at which crystals normally form delays crystallisation as it rises toward the surface, changing how the eruption unfolds. It's a previously overlooked mechanism that could improve eruption forecasting at similar volcanoes worldwide, published this week.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Fake Supplier Invoices Are Getting Harder to Spot — Here's How AI Can Help You Catch One Before You Pay It",
    "{{INSIGHT_BODY}}": "Invoice fraud has moved on from obviously dodgy emails — scammers now intercept a genuine supplier's invoice, quietly swap the BSB and account number, and send it back through what looks like the same email thread, banking on nobody double-checking a bill from a supplier they've paid a hundred times before. For a small trades business without a dedicated accounts team, an AI tool can act as that second set of eyes — cross-checking a new invoice's bank details against what that supplier used last time and flagging anything that's changed before you hit pay. It won't replace calling the supplier on a known number to confirm a big or unusual invoice, but it's a genuinely low-effort habit to build into the two minutes before you process payment.",

    # Fun facts
    "{{FACT_1}}": "Frost can form on your ute's windscreen even when the forecast says the air temperature never dropped below zero — flat surfaces radiate their own heat into a clear night sky and cool well below the surrounding air, a process called radiative cooling, which is why grass and glass can frost over on a night logged as '4°C.'",
    "{{FACT_2}}": "Glasgow, hosting this year's Commonwealth Games, first hosted the event in 2014 — making it only the second city ever to host the Games twice, after London held them in 1934 and 2002.",
    "{{FACT_3}}": "The fluorescent 'hi-vis' colours on modern safety vests trace back to brothers Bob and Joe Switzer, who accidentally discovered fluorescent pigments in their parents' garage in the 1930s while experimenting with UV light to treat one brother's eye injury — the pigments became DayGlo paint and eventually the orange and yellow now standard on every job site.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the rigger's small business never drop a client?",
    "{{JOKE_PUNCHLINE}}": "He always double-checked the sling before he trusted the load.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"I attribute my success to this: I never gave or took any excuse.\"",
    "{{CLOSING_ATTR}}": "— Florence Nightingale",
    "{{CLOSING_MESSAGE}}": "It's a crisp, frosty start to Sunday in Carrum Downs before a mostly sunny day, with showers moving in from tomorrow — so it's worth grabbing any outdoor jobs today while it's dry. Fill the ute before midnight if you can, since fuel goes up nationwide from tomorrow, and keep an eye out tonight for the Commonwealth Games closing ceremony, with Australia sitting on its best-ever medal haul.",
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
