#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 28 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 28 Jul (BOM)
    "{{WEATHER_1}}": "TUE 28 · 🌧️ Showers, windy periods · 7–12°C",
    "{{WEATHER_2}}": "WED 29 · 🌧️ Shower or two, cold change · 7–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 30 · 🌥️ Mostly cloudy, isolated shower · 6–11°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 31 · 🌤️ Partly cloudy, slight chance of a shower · 6–13°C",
    "{{WEATHER_5}}": "SAT 01 AUG · 🌤️ Partly cloudy, mild for winter · 6–14°C",
    "{{WEATHER_ALERT}}": "⚠ NO SEVERE WEATHER WARNINGS CURRENTLY ACTIVE FOR VICTORIA",

    # World
    "{{WORLD_1_FLAG}}": "🇵🇸🪖 WEST BANK · ISRAEL LAUNCHES MAJOR CRACKDOWN · SETTLER VIOLENCE SURGES",
    "{{WORLD_1_HEADLINE}}": "Israel's West Bank Crackdown Intensifies as Troops Storm Villages and Settler Violence Spirals",
    "{{WORLD_1_SUMMARY}}": "Israeli troops have stormed towns and villages across the occupied West Bank and detained hundreds of Palestinians in what officials are calling the most intensive operation in years, ordered by Prime Minister Netanyahu after two Israelis were killed in a shootout on Friday. Settler violence has surged alongside the crackdown — a mosque was set alight in the village of Qusra and slogans scrawled on its walls — while the Israeli military presses ahead with home demolitions linked to the attack. Four Palestinians were also killed in the same clash that triggered the operation.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/7/26/israeli-crackdown-in-occupied-west-bank-intensifies-settlers-cause-mayhem",

    "{{WORLD_2_FLAG}}": "🇺🇸🔫 SEATTLE · FOOD FESTIVAL SHOOTING · 3 DEAD, TODDLER AMONG WOUNDED",
    "{{WORLD_2_HEADLINE}}": "Three Killed in Shooting at Seattle's Bite of Seattle Food Festival, Teen Suspect in Custody",
    "{{WORLD_2_SUMMARY}}": "Three people were killed and four others wounded, including a two-year-old boy, when gunfire broke out at Seattle's long-running Bite of Seattle food festival on Sunday. Police believe two shooters were firing at each other in what investigators suspect was gang-related violence; a 15-year-old is now in custody while a second suspect remains at large. It's the latest in a string of mass-casualty shootings at US public events this year.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/07/26/us/seattle-center-shooting-festival",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺📊 AUSTRALIA · RBA GOVERNOR SPEAKS TODAY · Q2 CPI DUE WEDNESDAY",
    "{{ECON_1_HEADLINE}}": "RBA Governor Michele Bullock Faces the Market Today, With Wednesday's Inflation Data the Real Test for Rates",
    "{{ECON_1_SUMMARY}}": "RBA Governor Michele Bullock speaks in Sydney today, with markets and small business owners alike watching for any hint on where rates head next before Wednesday's Q2 CPI print — the number the central bank has flagged as the real decision point. Major banks aren't tipping another hike, pointing to a softening labour market, but a stubborn trimmed-mean inflation reading above 3.5 per cent would keep the pressure on borrowing costs for businesses carrying equipment loans.",
    "{{ECON_1_URL}}": "https://www.canberratimes.com.au/story/9317636/rate-watchers-eye-inflation-data-and-rba-chiefs-speech/",

    "{{ECON_2_FLAG}}": "🇦🇺⛽ FUEL COSTS · DIESEL PUSHES PAST 214¢/L · EXCISE RESTORATION KEEPS BITING",
    "{{ECON_2_HEADLINE}}": "Diesel and Petrol Prices Keep Climbing as the Restored Fuel Excise Works Through the Bowser",
    "{{ECON_2_SUMMARY}}": "Bowser prices are still climbing as the temporary cut to fuel excise winds back — Sydney diesel hit 213.5 cents a litre and unleaded 174.1 cents on Monday evening, with wholesale prices tipped to push averages into the high 170s this week. The government's excise relief is due to taper further by 2 August, meaning the diesel bill for a ute-and-trailer trades operation is only heading one way in the short term.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI INFRASTRUCTURE · NVIDIA'S $250B OPENAI BACKSTOP · BIGGEST DATA CENTRE BET YET",
    "{{TECH_1_HEADLINE}}": "Nvidia in Talks to Guarantee $250 Billion So OpenAI Can Lease a 10-Gigawatt Ohio Data Centre",
    "{{TECH_1_SUMMARY}}": "Nvidia is in talks to guarantee roughly $250 billion in financing so OpenAI can lease capacity from a planned 10-gigawatt data centre being built on a former uranium enrichment site in Ohio, part of a project expected to cost more than $500 billion in total. The unusual structure exists because OpenAI, still not profitable, can't get an investment-grade credit rating on its own — a reminder of just how much borrowed money is now underwriting the AI boom everyone's software runs on.",
    "{{TECH_1_URL}}": "https://finance.yahoo.com/technology/ai/articles/nvidia-talks-back-openai-ohio-114515389.html",

    "{{TECH_2_FLAG}}": "🤖 AI AT WORK · OPENAI LAUNCHES 'CHATGPT WORK' AGENT · WHOLE WORKFLOWS, NOT JUST CHAT",
    "{{TECH_2_HEADLINE}}": "OpenAI Rolls Out ChatGPT Work, an Agent That Runs Entire Admin Workflows in the Background",
    "{{TECH_2_SUMMARY}}": "OpenAI has rolled out ChatGPT Work, a new agent built on its GPT-5.6 models that can read data from your other apps and carry out entire multi-step tasks in the background rather than just answering questions in a chat window. It's part of a broader consolidation of OpenAI's tools into one desktop app, and a sign that the next wave of AI software is shifting from 'ask a question' to 'hand off a job.'",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · 948 ROBOTS, ONE WAREHOUSE · EUROPE'S FULFILMENT GOES AUTONOMOUS",
    "{{ROBOT_1_HEADLINE}}": "Hai Robotics Deploys Nearly 1,000 Warehouse Robots at a New Romanian Fulfilment Centre in Under Six Months",
    "{{ROBOT_1_SUMMARY}}": "Fashion logistics operator LPP Logistics has gone live with 948 Hai Robotics robots — 278 case-handling units and 670 fast-moving companion bots — at a new fulfilment centre near Bucharest, built and switched on in under six months. The goods-to-person system now processes more than 9,400 totes an hour across 625,000 storage locations, another sign of how quickly warehouse automation is scaling well beyond the flashier humanoid robot headlines.",
    "{{ROBOT_1_URL}}": "https://www.einpresswire.com/article/928774497/lpp-logistics-deploys-948-hai-robotics-robots-for-e-commerce-fulfillment-in-southeastern-europe",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Calls Trump's New Forced-Labour Tariffs 'Unjustified' as Albanese Vows to Raise It Directly",
    "{{AUS_1_SUMMARY}}": "Prime Minister Anthony Albanese says he'll raise new US tariffs directly with Donald Trump after Washington imposed a 12.5 per cent levy on Australian goods and 37 other nations last Friday, citing unproven claims about forced-labour supply chains. Canberra has called the tariffs 'unjustified' and says it won't retaliate, instead pointing to Australia's existing modern slavery protections as it pushes for the levy to be dropped.",
    "{{AUS_1_URL}}": "https://www.manilatimes.net/2026/07/27/world/asia-oceania/australia-calls-new-us-tariffs-unjustified/2391643",

    "{{AUS_2_HEADLINE}}": "Australia's Commonwealth Games Gold Rush Rolls On in Glasgow, Now Clear of the Next Four Nations Combined",
    "{{AUS_2_SUMMARY}}": "Australia's swimmers have driven a medal haul that now clears the next four nations on the table combined, with 13 golds banked as competition enters its final days in the pool at the Glasgow Commonwealth Games. Four-time Olympian Cameron McEvoy backed up Sunday's 50m freestyle gold with more finals today, as track and field events also start delivering medals.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Premier Jacinta Allan Fights to Save Her Job as Labor Caucus Meets Today Over a Leadership Spill",
    "{{VIC_1_SUMMARY}}": "Victorian Premier Jacinta Allan is fighting to keep her job as Labor's caucus meets today amid an open leadership challenge from her deputy, Ben Carroll, just months out from November's state election. Factional powerbrokers concluded over the weekend that Allan no longer holds majority support in the party room; she's refused calls to resign and has asked state secretary Steve Staikos to prepare for a possible members' ballot if the contest drags on.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 CANCER GENETICS · WHY DNA DAMAGE HITS SOME PEOPLE HARDER · CAMBRIDGE STUDY",
    "{{SCI_1_HEADLINE}}": "Scientists Reveal Why the Same DNA Damage From Smoking or UV Causes Cancer in Some People, Not Others",
    "{{SCI_1_SUMMARY}}": "Cambridge researchers bred four genetically diverse mouse strains and exposed them to an identical dose of a carcinogen found in cigarette smoke, finding that the animals' inherited genetic background — not just the mutation itself — steered how their cancers evolved. The finding helps explain a long-standing mystery: why two people with near-identical exposure to smoking or UV damage can end up with wildly different cancer outcomes, and could eventually help doctors tailor screening to a patient's genetic risk rather than their exposure alone.",

    # Business insight
    "{{INSIGHT_TITLE}}": "OpenAI's New 'ChatGPT Work' Agent Can Run Entire Admin Workflows — What That Means for a One-Person Trades Office",
    "{{INSIGHT_BODY}}": "OpenAI's new ChatGPT Work agent, released this week alongside the GPT-5.6 model family, doesn't just answer questions — it can log into your apps, follow a multi-step process, and keep working in the background while you're back on the tools. For a one- or two-person trades office, that's the difference between an AI you have to babysit and one you can actually hand a job to: reconcile last month's fuel receipts, chase three overdue invoices, or draft a supplier order, then report back with what it did. It's early days and still rolling out gradually, but agents that can finish a task rather than just describe one are the next real productivity jump for a business too small to hire an office manager.",

    # Fun facts
    "{{FACT_1}}": "The cordless drill traces back to a joint NASA and Black & Decker project for the Apollo missions — the same low-torque, battery-powered motor developed so astronauts could core-sample the Moon later shrank down into the household power drill.",
    "{{FACT_2}}": "Bagpipes are thousands of years older than their association with Scotland — similar reed-and-bag instruments were played across the ancient Middle East and Roman Empire long before they became a Highland tradition.",
    "{{FACT_3}}": "Victoria was originally awarded the 2026 Commonwealth Games before withdrawing in 2023 over a budget blowout from an estimated $2.6 billion to more than $6 billion — handing hosting rights to Glasgow, where the Games are now underway.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the fire alarm technician never panic during a callout?",
    "{{JOKE_PUNCHLINE}}": "He'd already tested every worst-case scenario twice before lunch.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The harder the conflict, the more glorious the triumph.\"",
    "{{CLOSING_ATTR}}": "— Thomas Paine",
    "{{CLOSING_MESSAGE}}": "It's a damp, blustery Tuesday with more showers rolling through — and back home, Victoria's Labor caucus meets today to decide if Jacinta Allan survives as Premier, while over in Glasgow the Commonwealth Games gold rush keeps building. If you're bracing for the diesel bill, today's also the day RBA Governor Bullock speaks in Sydney, with Wednesday's inflation print the one that actually moves rates.",
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
