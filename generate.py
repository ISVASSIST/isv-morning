#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 10 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 10 Sep (BOM Melbourne forecast)
    "{{WEATHER_1}}": "THU 10 SEP · ☁️ Cloudy, slight shower chance, SW wind easing · 10–15°C",
    "{{WEATHER_2}}": "FRI 11 SEP · 🌫️ Morning fog then sunny, light winds · 10–15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SAT 12 SEP · 🌤️ Morning fog then mostly sunny, winds turning northerly · 7–17°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SUN 13 SEP · ⛅ Partly cloudy, slight shower chance late, northerly 15–25km/h · 8–21°C",
    "{{WEATHER_5}}": "MON 14 SEP · 🌦️ Cooler change, partly cloudy with a shower or two · 9–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — Friday and Saturday are the pick of the run (dry, mild, light winds) before Sunday's northerly pushes the top into the low 20s ahead of a cooler, shower-bearing change Monday.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 GULF OF OMAN · US DESTROYS FIVE MORE IRANIAN OIL TANKERS, IRAN HITS BACK AT JORDAN",
    "{{WORLD_1_HEADLINE}}": "US Destroys Five More Iranian Oil Tankers, Iran Retaliates With Missile Strikes on a US Base in Jordan",
    "{{WORLD_1_SUMMARY}}": "The US military destroyed five more Iranian oil tankers on Tuesday — the Kivik, Charminar, Horizon 1 and Riesco in the Gulf of Oman, plus the Derya near Kharg Island — taking the total sunk since Saturday to eight, after Iran's Revolutionary Guard fired on a US carrier and destroyer that both evaded the strikes. Iran retaliated within hours with ballistic missiles at the Al-Azraq base in Jordan; Jordanian air defences intercepted 18 of 20, with two landing in unpopulated areas and no casualties reported.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/09/09/nx-s1-5962641/us-destroy-iranian-oil-tankers",

    "{{WORLD_2_FLAG}}": "🇮🇱 WEST BANK · UK, FRANCE AND CANADA BAN TRADE WITH ILLEGAL ISRAELI SETTLEMENTS",
    "{{WORLD_2_HEADLINE}}": "UK, France and Canada Announce Ban on Goods From Illegal Israeli Settlements, Israel Shuts UK's Jerusalem Consulate in Response",
    "{{WORLD_2_SUMMARY}}": "The UK, France and Canada announced Tuesday they'll ban imports of goods and some services from Israeli settlements in the occupied West Bank, joining Belgium, Ireland, the Netherlands, Norway and Spain in similar measures — though none touch goods from Israel itself. Israel responded within hours by closing Britain's East Jerusalem consulate, ending British training of Palestinian Authority security forces and barring entry to a dozen British politicians.",
    "{{WORLD_2_URL}}": "https://www.abc.net.au/news/2026-09-08/three-g7-countries-announce-import-ban-on-goods-from-settlements/107130998",

    # Economics
    "{{ECON_1_FLAG}}": "📊 SMALL BUSINESS · CONDITIONS TURN NEGATIVE FOR FIRST TIME SINCE THE PANDEMIC",
    "{{ECON_1_HEADLINE}}": "NAB Survey Finds Business Conditions Turn Negative for the First Time in Six Years as Fuel Costs Bite",
    "{{ECON_1_SUMMARY}}": "NAB's August business survey shows conditions fell five points to -1 — negative for the first time since the pandemic — with profitability down ten points to a new post-COVID low as input costs keep outpacing prices. The weakness is broad-based, with construction, mining and manufacturing leading the falls, and it lands just as fuel costs overtake every other worry for small operators in MYOB's latest Business Monitor.",
    "{{ECON_1_URL}}": "https://www.nab.com.au/news/economy-markets/business-conditions-drop-into-negative-territory-business-survey-august26",

    "{{ECON_2_FLAG}}": "⛽ FUEL · BRENT TOPS $100 A BARREL, MELBOURNE PUMP PRICES STAY ELEVATED",
    "{{ECON_2_HEADLINE}}": "Brent Crude Breaks $100 a Barrel for the First Time in Six Weeks — Melbourne Pump Prices Stay Near Multi-Month Highs",
    "{{ECON_2_SUMMARY}}": "Brent crude broke back above US$100 a barrel on Tuesday after the latest round of Middle East tanker strikes, and that's still working its way to the bowser — Melbourne unleaded is averaging around 205c/L and diesel around 254c/L, both up slightly on last week. The cheapest sites remain 15–20c/L below the average, so the usual advice holds: shop on the day rather than waiting for a discount cycle that keeps getting interrupted.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 CONSUMER AI · META LAUNCHES 'MUSE', AN AI AGENT THAT ACTUALLY DOES THE ADMIN",
    "{{TECH_1_HEADLINE}}": "Meta Launches Muse, a Personal AI Agent That Fills Out Forms, Books Appointments and Handles Admin On Its Own",
    "{{TECH_1_SUMMARY}}": "Meta's new Muse agent, live in the US on web, iOS, Android and WhatsApp, doesn't just answer questions — it opens a browser inside its own secure virtual machine, fills out forms and completes real tasks like booking appointments or coordinating steps across connected services on your behalf. It's free for everyday use, with $20 and $100 monthly tiers for heavier workloads — a solid preview of what \"AI does the admin\" looks like once it moves past the demo stage.",
    "{{TECH_1_URL}}": "https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/",

    "{{TECH_2_FLAG}}": "📈 SMB MARKETING · GOOGLE ADS ADDS TEXT-PROMPT AI DASHBOARDS FOR EVERYDAY ADVERTISERS",
    "{{TECH_2_HEADLINE}}": "Google Ads Rolls Out AI Dashboards That Build a Performance Report From a Plain-English Question",
    "{{TECH_2_SUMMARY}}": "Google Ads has begun rolling out AI Dashboards that build a full visual performance report from a plain-English request — 'show me which campaigns drove in-store visits this month' — instead of you building the report yourself, alongside a new Local Customer Optimisation toggle aimed at nearby, in-market customers for shopfronts and local service businesses. For an owner-operator managing their own account between jobs, it's a small but genuinely time-saving change.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦺 INDUSTRIAL AI · CHINESE FIRM OPEN-SOURCES TRAINING CODE FOR ITS HAZARD-DUTY HUMANOID",
    "{{ROBOT_1_HEADLINE}}": "Deep Robotics Open-Sources the Training Pipeline Behind Its All-Weather DR02 Humanoid, Built for Hazardous Industrial Sites",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics firm Deep Robotics has published the reinforcement-learning training code behind its DR02 — the world's first IP66-rated, all-weather humanoid, built to work in rain, dust and temperature extremes on hazardous industrial sites. Releasing the sim-to-real pipeline rather than just showreel footage hands other teams a ready-made blueprint for training rugged field robots, and is being read as a pointed contrast with the closed training stacks still standard among Western rivals.",
    "{{ROBOT_1_URL}}": "https://robotics.sg/2026/09/08/dr02-humanoid-robot-locomotion-open-source-rl-training-code-explanation/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Labor Unveils 'My Feed, My Way' Laws Letting Australians Switch Off Social Media Algorithms",
    "{{AUS_1_SUMMARY}}": "The Albanese government has released draft Digital Duty of Care legislation that would force platforms like Instagram and TikTok to let users over 16 opt out of algorithm-recommended feeds and see only content from accounts they follow, with non-compliant platforms facing fines of up to $109.2 million. The opposition and One Nation argue it hands the communications minister too much power over what counts as harmful content, a claim the Prime Minister rejects.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-08/labour-s-social-media-algorithm-choice-duty-of-care-bill/107130100",

    "{{AUS_2_HEADLINE}}": "World's First Solar Power Station, Built in Outback NSW in 1981, Added to State Heritage Register",
    "{{AUS_2_SUMMARY}}": "White Cliffs Solar Power Station near Broken Hill — 14 sun-tracking parabolic dishes built by an ANU team in 1981 to power the remote opal-mining town off-grid — has been added to the NSW heritage register after unanimous community support, in a listing expected to help protect the site and unlock maintenance grants.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Auditor-General Finds Nearly Half of State Roads in 'Very Poor' Condition, Warns of Multi-Billion-Dollar Repair Backlog",
    "{{VIC_1_SUMMARY}}": "The Victorian Auditor-General's Office says 48% of state-managed roads are now in 'very poor' condition, with the share rated poor or very poor up 23% since 2021 as a growing maintenance backlog lets damage accumulate faster than crews can repair it. The Department of Transport and Planning estimates it would cost more than $3 billion a year just to hold pavement condition where it is, meaning crews are increasingly limited to reactive, safety-critical fixes rather than cheaper preventative work.",

    # Science
    "{{SCI_1_FLAG}}": "🧪 CHEMISTRY · HIDDEN CATALYST STRUCTURE SUPERCHARGES METHANE CONVERSION",
    "{{SCI_1_HEADLINE}}": "Chinese Chemists Discover a Hidden Atomic Structure That Lets an Ultra-Low-Nickel Catalyst Outperform Ones With Ten Times the Metal",
    "{{SCI_1_SUMMARY}}": "Researchers at the Dalian Institute of Chemical Physics built a catalyst using just 0.8% nickel by weight that converts methane as effectively as one containing ten times as much metal, after discovering a near-invisible atomic structure forming on the catalyst's surface — not the metallic nickel long assumed to do the work — was actually driving the reaction. Conversion held at 92% with hydrogen and carbon monoxide selectivity above 87%, a finding that could make industrial methane processing dramatically cheaper to catalyse.",

    # Business insight
    "{{INSIGHT_TITLE}}": "You'll Sell This Business One Day — AI Can Start Building the Numbers That Prove What It's Worth",
    "{{INSIGHT_BODY}}": "Most trades owners are too flat out running the business to ever assemble the file a buyer, a bank or even a future business partner would actually want to see — job margins by type, the split between repeat clients and one-off jobs, a current plant and equipment register, and a few years of genuinely clean numbers rather than a shoebox of BAS lodgements. A general-purpose AI tool can now turn your existing job records, invoices and Xero or MYOB exports into a first-pass version of exactly that pack in an afternoon — the kind of document accountants used to charge thousands to compile for due diligence. You don't need to be selling next year for it to be worth doing; a business that's easy to value is also easier to finance, insure and eventually hand to someone else to run.",

    # Fun facts
    "{{FACT_1}}": "The chalk line still snapped across a slab or stud wall on every job site today is one of the oldest tools in continuous use in construction — ancient Egyptian builders dipped a taut string in ochre or ash and snapped it to mark dead-straight lines for the Pyramids, more than 4,000 years before the modern chalk box was ever patented.",
    "{{FACT_2}}": "The stapler predates the paperclip by well over a century — one of the earliest known versions was handmade for the court of France's King Louis XV in the 1700s, with each individual staple stamped with the royal insignia, while the modern paperclip wasn't patented until 1899.",
    "{{FACT_3}}": "A narwhal's tusk isn't just for show — it's an oversized tooth riddled with around 10 million nerve endings, and scientists have shown the animal's heart rate changes when seawater of a different salinity is run past it, suggesting the tusk works as a giant sensory probe.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the epoxy flooring contractor refuse to shake hands the morning after a big pour?",
    "{{JOKE_PUNCHLINE}}": "His hands were still curing from the day before.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The time is always right to do what is right.\"",
    "{{CLOSING_ATTR}}": "— Martin Luther King Jr.",
    "{{CLOSING_MESSAGE}}": "Thursday's mild and mostly dry around Carrum Downs — 10 to 15°C with only a slight shower chance — and Friday and Saturday look like the pick of the run if there's outdoor prep or coatings work that needs a stable window before Sunday's northerly and next week's cooler change roll through. Worth keeping an eye on the bowser too: Brent just broke back above US$100 a barrel on fresh Middle East strikes, and that tends to show up locally within a fortnight.",
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
