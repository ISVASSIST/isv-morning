#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 21 September 2026",

    # Weather — Carrum Downs / Melbourne bayside, 5-day from Mon 21 Sep
    "{{WEATHER_1}}": "MON 21 SEP · 🌦️ Showers clearing, cooler behind Sunday's front, SW–S winds 20–30km/h · 9–15°C",
    "{{WEATHER_2}}": "TUE 22 SEP · ☀️ Sunny, light winds · 9–17°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "WED 23 SEP · ⛅ Partly cloudy, mild · 10–19°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "THU 24 SEP · ☀️ Sunny and warm for the season · 18–24°C",
    "{{WEATHER_5}}": "FRI 25 SEP · ☀️ Sunny periods, mild · 14–24°C",
    "{{WEATHER_ALERT}}": "Sunday's damaging wind warning for Victoria's Central district has eased overnight; today brings a cooler, showery start to the week behind the front.",

    # World
    "{{WORLD_1_FLAG}}": "🇸🇦🇾🇪 YEMEN WAR · SAUDI AIR DEFENCES INTERCEPT BALLISTIC MISSILE FIRED AT RIYADH AS TALKS WITH IRAN STALL",
    "{{WORLD_1_HEADLINE}}": "Houthis Fire Missile at Riyadh, Forcing Saudi Arabia to Postpone Planned Talks With Iran",
    "{{WORLD_1_SUMMARY}}": "Saudi-led coalition forces said they intercepted and destroyed a Houthi ballistic missile aimed at the Saudi capital at dawn, with further strikes attempted on Bisha, Taif, Farasan and Yanbu — the attack came days after a separate strike knocked out Saudi Arabia's East-West oil pipeline, and has pushed Gulf states to postpone planned talks with Iran just as the region's biggest oil producer tries to contain the fallout.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/9/19/saudi-led-coalition-says-defences-intercept-houthi-missile-fired-at-riyadh",

    "{{WORLD_2_FLAG}}": "🇷🇺🇺🇦 RUSSIA-UKRAINE WAR · KYIV LAUNCHES ITS LARGEST-EVER DRONE BARRAGE ON MOSCOW DURING RUSSIA'S ELECTION",
    "{{WORLD_2_HEADLINE}}": "Record Ukrainian Drone Attack Sets Moscow Oil Refinery Ablaze on the Final Day of Russia's Vote",
    "{{WORLD_2_SUMMARY}}": "Moscow's mayor said the city intercepted more than 1,600 drones overnight, around 450 of them aimed at the capital, in what officials are calling the largest attack on Moscow since the war began — at least three people died and the Gazpromneft refinery in Kapotnya, which supplies 40% of the city's fuel, was set on fire, with Russian officials linking the timing directly to the final day of parliamentary voting.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/09/20/europe/moscow-ukraine-attack-russia-election",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · BOWSER PRICES KEEP CLIMBING AS THE MIDDLE EAST CONFLICT WIDENS ON A SECOND FRONT",
    "{{ECON_1_HEADLINE}}": "Petrol and Diesel Set to Rise Again as Yemen's War Escalates and a Key Saudi Pipeline Stays Shut",
    "{{ECON_1_SUMMARY}}": "Average pump prices have already climbed sharply since June as Middle East disruption drags on, and analysts warn this week's widening Yemen conflict and the still-closed Saudi East-West pipeline mean there's little reason to expect relief soon — the ACCC has moved to weekly fuel monitoring as households and small businesses alike absorb the increases at the bowser.",
    "{{ECON_1_URL}}": "https://www.sbs.com.au/news/article/australia-fuel-petrol-prices-middle-east-war-oil-inflation/wczp6rjwr",

    "{{ECON_2_FLAG}}": "📊 RATES WATCH · MARKETS NOW PRICE AN 80% CHANCE OF A RATE RISE AT NEXT WEEK'S RBA MEETING",
    "{{ECON_2_HEADLINE}}": "RBA Decision Looms on September 29 as Hot Inflation Data Firms Up Rate Hike Bets",
    "{{ECON_2_SUMMARY}}": "July's CPI print came in hotter than the RBA expected, with trimmed mean inflation stuck at 3.6% — above the Bank's 2–3% target band — and markets are now pricing around an 80% chance of a quarter-point hike to 4.6% when the board meets on 29 September, adding to pressure on any small business already squeezed by rising fuel and input costs.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📝 AI AT WORK · CHATGPT NOW LIVES INSIDE MICROSOFT WORD ON EVERY PLAN, INCLUDING FREE",
    "{{TECH_1_HEADLINE}}": "ChatGPT's New Word Add-In Drafts, Edits and Formats Documents Without Leaving the Page",
    "{{TECH_1_SUMMARY}}": "OpenAI has embedded a ChatGPT sidebar directly into Microsoft Word, letting users turn rough notes into a structured draft, tighten wording, fix formatting or summarise a document without switching apps — it's rolling out now on every plan including Free, and becomes a default, always-on feature in workplace accounts from 1 October.",
    "{{TECH_1_URL}}": "https://windowsreport.com/chatgpt-comes-to-word-powerpoint-and-excel-for-all-plans/",

    "{{TECH_2_FLAG}}": "🤖 AI IN PRACTICE · ANTHROPIC SAYS CLAUDE NOW LEADS OVER A QUARTER OF ITS OWN AI RESEARCH WORK",
    "{{TECH_2_HEADLINE}}": "Anthropic's First Detailed Measurements Show Claude Completing 26% of the Company's AI R&D End-to-End",
    "{{TECH_2_SUMMARY}}": "Anthropic's new 'R&D Automation Index' found Claude now leads 26% of the company's model research tasks end-to-end under human supervision, up from zero in February — the company was careful to stress no task runs fully autonomously, but the trajectory is a reminder of how fast the tools reshaping every other industry are also being used to build themselves.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 PHYSICAL AI · FARADAY FUTURE UNVEILS NINE NEW ROBOTS ACROSS QUADRUPED, HUMANOID AND MOBILE FORMS",
    "{{ROBOT_1_HEADLINE}}": "Faraday Future Launches Nine AI Robots, Including Quadruped Security and Inspection Units, at Its Annual Event",
    "{{ROBOT_1_SUMMARY}}": "FF's '919' launch introduced nine new EAI robot configurations — humanoid, quadruped and mobile manipulator — plus four industry-specific solutions for education, research, security and inspection, with the Aegis quadruped series also on display at IMTS Chicago this month showing off industrial inspection and site-security applications closer to what a services business might actually deploy.",
    "{{ROBOT_1_URL}}": "https://www.financialcontent.com/article/bizwire-2026-9-20-faraday-future-launches-four-industry-productivity-solutions-nine-new-eai-devices-at-its-919-event-building-its-one-brain-multi-form-multi-capability-ff-eai-robot-world-20-all-new-futurist-now-on-sale-and-master-mini-starts-at-9990",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australian Eucalyptus Oil Producers Invest Millions to Fight Off Cheap, Sometimes Fake Imports",
    "{{AUS_1_SUMMARY}}": "Victorian producers GR Davis and FGB Natural Products have each sunk millions into new ultra-efficient distilleries and genetically selected high-yield blue mallee plantations, fighting back against cheap imported oil that's sometimes cut with camphor oil — despite founding the industry in 1852, Australia now supplies only around 5% of the world's eucalyptus oil.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-20/australian-eucalyptus-oil-industry-investment/107164508",

    "{{AUS_2_HEADLINE}}": "Experts Warn Australia's Battery Recycling Sector Isn't Keeping Pace With the EV Boom",
    "{{AUS_2_SUMMARY}}": "With battery electric vehicles now making up nearly a quarter of new car sales, industry figures say the waste sector still lacks the trained workforce to safely handle a coming wave of end-of-life EV and home batteries — a gap that could be worth $6.9 billion and 34,600 jobs by 2050 if the skills and infrastructure catch up in time.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Greens MP and Former GP Tim Read Dies Aged 64 After Public Cancer Battle",
    "{{VIC_1_SUMMARY}}": "The Member for Brunswick, who spent his final year in parliament fighting the planned closure of VicHealth after revealing his metastatic melanoma diagnosis in January, has been remembered across party lines as a kind, funny and decent man.",

    # Science
    "{{SCI_1_FLAG}}": "🩸 MEDICINE · A BLOOD-TYPE MYSTERY FIRST SPOTTED IN 1972 FINALLY GETS ITS ANSWER",
    "{{SCI_1_HEADLINE}}": "Scientists Name the World's 47th Blood Group After Solving a 50-Year-Old Genetic Mystery",
    "{{SCI_1_SUMMARY}}": "NHS Blood and Transplant researchers have traced the rare 'AnWj-negative' blood type — first noticed in a pregnant patient's sample in 1972 — to a deleted gene called MAL, whose protein normally sits on the surface of every red blood cell; the discovery creates the new MAL blood group system and could prevent dangerous transfusion reactions in the roughly 1-in-1,000 people who lack the antigen.",

    # Business insight
    "{{INSIGHT_TITLE}}": "ChatGPT Just Moved Into Microsoft Word — What That Means for Every Quote and SWMS You Type Up",
    "{{INSIGHT_BODY}}": "OpenAI's new Word add-in turns a rough dot-point list into a structured, properly formatted document — drop in notes from a site visit and it'll draft something close to a finished quote, method statement or client letter, right inside the same window you already work in. It won't know your pricing, your standard clauses, or what actually happened on site, so nothing should go out the door without you reading it line by line first. But if quoting and paperwork are the jobs that eat your evenings, this is one more sign that the drafting half of that work is quietly getting easier, well before the on-site half changes much at all.",

    # Fun facts
    "{{FACT_1}}": "Russia says it intercepted more than 1,600 drones in Sunday night's barrage on Moscow, over three times the roughly 500 V-1 flying bombs that hit London in the worst week of the 1944 Blitz — a scale of aerial attack that's now become almost routine in a war heading into its fourth year.",
    "{{FACT_2}}": "Australia's pharmacist Joseph Bosisto pioneered the eucalyptus oil trade from a Victorian distillery back in 1852, and Australia once supplied the entire world's oil — yet today it produces only about 5% of it, undercut by cheaper imports, which is exactly the pressure now pushing two Victorian producers to spend millions modernising.",
    "{{FACT_3}}": "It took NHS Blood and Transplant's Dr Louise Tilley nearly 20 years to trace a blood anomaly first noticed in a single patient's sample in 1972 back to one missing gene — the same kind of slow, unglamorous detective work behind naming the world's 47th recognised blood group system this month.",

    # Joke
    "{{JOKE_SETUP}}": "A driveway sealing contractor was asked how his small business always finished every job before the first drop of rain.",
    "{{JOKE_PUNCHLINE}}": "He said he'd learned to read a weather forecast better than most meteorologists — and price a job just as fast.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"If you want to go fast, go alone. If you want to go far, go together.\"",
    "{{CLOSING_ATTR}}": "— African Proverb",
    "{{CLOSING_MESSAGE}}": "It's Monday, and Carrum Downs is waking up to showers and a cooler change behind Sunday's wind warning — good weather for admin, not for anything that needs to stay dry on site. With fuel prices climbing again on the back of a widening Middle East conflict and another RBA rate rise looking likely next week, this is a week to get ahead on invoicing rather than behind it.",
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
