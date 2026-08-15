#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 16 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 16 Aug (BOM)
    "{{WEATHER_1}}": "SUN 16 · 🌤️ Morning fog clearing to a mostly sunny afternoon, light winds · 6–14°C",
    "{{WEATHER_2}}": "MON 17 · ☁️ Cloudy, cooler top, light winds · 9–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "TUE 18 · ⛅ Partly cloudy, winds picking up in the afternoon · 8–15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "WED 19 · ⛅ Partly cloudy, similar mild conditions continuing · 8–16°C",
    "{{WEATHER_5}}": "THU 20 · 🌥️ Mostly cloudy, chance of a shower returning · 8–15°C",
    "{{WEATHER_ALERT}}": "No BOM warnings currently listed for Carrum Downs — a calm, mild stretch after last week's active weather, just morning fog to plan around early on",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇩 INDONESIA · EARTHQUAKE DEATH TOLL PASSES 45 AFTER MAGNITUDE 7.7 QUAKE STRIKES OFF FLORES ISLAND",
    "{{WORLD_1_HEADLINE}}": "Indonesia Earthquake Death Toll Passes 45 After Magnitude 7.7 Quake Strikes Off Flores Island",
    "{{WORLD_1_SUMMARY}}": "A magnitude 7.7 earthquake struck early Saturday about 68 kilometres north-northwest of Ende in East Nusa Tenggara province, killing more than 45 people as dozens of aftershocks — the strongest a magnitude 6.1 — continued shaking the region. At least 157 houses were flattened and nearly 200 more damaged, with around 2,000 villagers moved into temporary shelters as rescue crews work through the rubble.",
    "{{WORLD_1_URL}}": "https://www.thenationalnews.com/news/asia/2026/08/15/indonesia-earthquake-death-toll-latest-news/",

    "{{WORLD_2_FLAG}}": "🇱🇧🇮🇱 LEBANON · ISRAELI STRIKES KILL 11 IN SOUTH LEBANON IN ONE OF THE DEADLIEST ATTACKS SINCE THE JUNE TRUCE",
    "{{WORLD_2_HEADLINE}}": "Israeli Strikes Kill 11, Including Three Children, in Southern Lebanon in One of the Deadliest Attacks Since the June Truce",
    "{{WORLD_2_SUMMARY}}": "At least 11 people, including three children, were killed in overnight Israeli strikes on the villages of Ansar and Deir Al Zahrani in southern Lebanon, with Israel's military saying it hit Hezbollah infrastructure in response to actions against its soldiers. Lebanon's prime minister rejected claims those killed were military targets, calling it one of the deadliest incidents since the fragile truce between Israel and Hezbollah took hold in June.",
    "{{WORLD_2_URL}}": "https://www.usnews.com/news/world/articles/2026-08-15/israeli-strike-kills-seven-in-south-lebanon-state-news-reports",

    # Economics
    "{{ECON_1_FLAG}}": "⛽🇦🇺 FUEL · PETROL AND DIESEL PRICES EASE SLIGHTLY THIS WEEK EVEN AS THE FULL FUEL EXCISE BITES",
    "{{ECON_1_HEADLINE}}": "Petrol and Diesel Prices Ease Slightly This Week as Lower International Benchmarks Offset the Full Fuel Excise",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly monitoring shows average retail petrol and diesel prices in Australia's five largest cities ticked down slightly this week on softer international benchmark prices, even after the fuel excise was fully restored to 53.7c/L in early August. Prices are still running 30c/L higher for petrol and 65c/L higher for diesel than before the Middle East conflict flared, so it's still worth shopping around before you fill the ute.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🇦🇺💵 AUD · AUSSIE DOLLAR HOLDS NEAR SEVEN-MONTH HIGHS AROUND US70.6c AS THE RBA STAYS PATIENT",
    "{{ECON_2_HEADLINE}}": "Australian Dollar Holds Near Seven-Month Highs Around US70.6c as the RBA Signals Patience on Rates",
    "{{ECON_2_SUMMARY}}": "The Aussie dollar is sitting around US70.6c, close to its highest levels in months, after the RBA held its cash rate at 4.35% and signalled it's watching incoming data rather than rushing another move either way. A firmer dollar is good news if you're importing gear or materials, though it can nibble at margins if any of your work has an export angle.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖💸 AI PRICING · DEEPSEEK HIKES SOME API PRICES BY OVER 1,100% FROM TODAY, SHIFTING TO PEAK AND OFF-PEAK RATES",
    "{{TECH_1_HEADLINE}}": "DeepSeek Hikes Some AI Model Prices by Over 1,100% From Today, Introducing Peak and Off-Peak Rates",
    "{{TECH_1_SUMMARY}}": "Chinese AI lab DeepSeek's new pricing takes effect today, with some token rates for its V4 models rising more than 1,100% during peak hours (01:00–04:00 and 06:00–10:00 UTC) as the company tries to spread demand away from its busiest periods. It's a reminder that behind-the-scenes pricing on the AI tools plugged into your quoting or admin can shift overnight — worth knowing which ones you're actually paying for, and what happens to the bill if a provider changes the rules.",
    "{{TECH_1_URL}}": "https://qz.com/deepseek-api-price-increase-v4-peak-off-peak-081326",

    "{{TECH_2_FLAG}}": "🤖🏢 AI RACE · MICROSOFT STARTS MERGING CONSUMER AND BUSINESS COPILOT INTO ONE APP, WITH A CHOICE OF AI MODEL",
    "{{TECH_2_HEADLINE}}": "Microsoft Starts Merging Its Consumer and Business Copilot Apps Into One, Giving Users a Choice of GPT-5.6 or Claude",
    "{{TECH_2_SUMMARY}}": "Microsoft has begun rolling out a unified Copilot app that combines its consumer and Microsoft 365 business tools into a single experience, starting with a small group of users this week ahead of a broader rollout. The bigger change under the hood is choice — users can now pick between OpenAI's and Anthropic's models rather than being locked into one — worth watching if your business leans on Microsoft's ecosystem for email, documents or admin.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭🤖 ROBOTICS · HUMANOID ROBOTS MOVE ONTO CAR FACTORY FLOORS AS BMW'S FIGURE 03 TAKES OVER PARTS SEQUENCING",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robots Are Moving Onto Car Factory Floors, With BMW's Figure 03 Now Taking Over Parts Sequencing",
    "{{ROBOT_1_SUMMARY}}": "At BMW's Spartanburg, South Carolina plant, Figure AI's Figure 03 humanoid robot is now handling parts sequencing in logistics, building on its predecessor Figure 02, which helped assemble more than 30,000 BMW X3 units. A BMW logistics executive says the robots are \"still slower than humans\" but \"advancing fast\" — another sign humanoid automation is moving past the demo stage and into real production work, one task at a time.",
    "{{ROBOT_1_URL}}": "https://hardware.slashdot.org/story/26/08/14/215204/robots-that-walk-and-talk-are-coming-to-car-factories",

    # Australia
    "{{AUS_1_HEADLINE}}": "Prime Minister Marks Five Years Since the Fall of Kabul With a Message of Solidarity for Afghanistan",
    "{{AUS_1_SUMMARY}}": "Australia's Prime Minister expressed solidarity with the people of Afghanistan on the fifth anniversary of the Taliban's return to power, as Taliban officials marked the milestone with celebrations in Kabul while a UN official warned of a deepening rights crisis. The anniversary lands as debate continues in Australia and allied nations over the legacy of the 20-year Afghan campaign and the thousands of former interpreters and support staff who were resettled here.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/podcast-episode/pm-expresses-solidarity-with-people-of-afghanistan-on-anniversary-midday-news-bulletin-15-august-2026/9mi0aoqeo",

    "{{AUS_2_HEADLINE}}": "Severe Storms Bring Flash Flooding to Adelaide and Damaging Winds to NSW and East Gippsland",
    "{{AUS_2_SUMMARY}}": "A broad low-pressure system has brought flooding, large hail and damaging winds across eastern and southern Australia this weekend, with the Bremer River at Wanstead Road in South Australia exceeding minor flood level and severe weather warnings current for damaging winds above 90km/h about the NSW Eastern Ranges and East Gippsland coast. Worth checking any exposed sites, scaffolding or signage in those areas before Monday.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "H5 Bird Flu Confirmed in a Little Penguin for the First Time as Vaccinations Begin at Phillip Island",
    "{{VIC_1_SUMMARY}}": "Victoria has recorded its first H5 bird flu detection in a little penguin, prompting authorities to begin vaccinating more than 5,000 penguins at Phillip Island and St Kilda from Monday evening, while three further wild bird detections confirmed the virus has now spread into East Gippsland. There are still no detections in commercial poultry, and the human health risk remains low.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 SCIENCE · STANFORD FINDS BLOOD IMMUNE CELLS FLOOD INTO THE AGING BRAIN, OVERTURNING A LONG-HELD ASSUMPTION",
    "{{SCI_1_HEADLINE}}": "Stanford Researchers Find Immune Cells From the Blood Flood Into the Aging Human Brain, Upending Decades of Assumptions",
    "{{SCI_1_SUMMARY}}": "Stanford scientists have found that large numbers of immune cells from the bloodstream begin entering the human brain as early as middle age, transforming into microglia — the brain's resident immune cells — in a way that doesn't happen in mice or other primates. Published in Nature, the discovery could open new paths for treating Alzheimer's and other neurological disease, since people with certain blood-cell mutations were found to be far less likely to develop the condition.",

    # Business insight
    "{{INSIGHT_TITLE}}": "One AI Provider Just Hiked Prices Over 1,100% Overnight — Don't Build Your Business on a Single Tool",
    "{{INSIGHT_BODY}}": "DeepSeek's new pricing landed today with some token rates up more than 1,100% during peak hours — a sharp reminder that the AI tools quietly running your quoting, admin or customer replies sit behind pricing that can change overnight, with little warning and no negotiation. If your business leans on one AI subscription for anything business-critical, it's worth a five-minute check this week: what would it actually cost you if that provider doubled its price tomorrow, and do you have a fallback tool you could switch to without missing a beat?",

    # Fun facts
    "{{FACT_1}}": "The Richter and moment magnitude scales are logarithmic, not linear — a magnitude 7.7 earthquake like the one that struck Indonesia this week releases roughly 30 times more energy than a magnitude 6.7, and close to a thousand times more than a magnitude 5.7.",
    "{{FACT_2}}": "Radiation fog — the kind that regularly blankets Melbourne's outer suburbs on still winter mornings — forms when the ground loses heat rapidly overnight under clear skies, cooling the air just above it below its dew point, which is why it often burns off from the CBD first while low-lying areas stay socked in for hours.",
    "{{FACT_3}}": "The Esky, now shorthand for any portable cooler in Australian English, started life in 1952 as the 'Esky Auto Box' — a portable ice box built by Sydney company Malley's and named as a playful abbreviation of 'Eskimo.'",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pressure-washing contractor's small business always come up clean at tax time?",
    "{{JOKE_PUNCHLINE}}": "Because he never let anything build up — receipts included.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"You can't build a reputation on what you're going to do.\"",
    "{{CLOSING_ATTR}}": "— Henry Ford",
    "{{CLOSING_MESSAGE}}": "It's a milder, calmer Sunday in Carrum Downs with the morning fog set to clear to sunshine by afternoon — good timing if you're catching up on the backyard or getting ahead before Monday. With Victoria's penguins now getting their bird flu jabs, an AI provider hiking prices overnight, and humanoid robots quietly clocking on at car factories overseas, it's a good day to switch off for a bit before the week kicks back into gear.",
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
