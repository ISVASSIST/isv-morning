#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 17 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 17 Aug (BOM)
    "{{WEATHER_1}}": "MON 17 · 🌤️ Morning fog clearing to a mostly sunny afternoon, light winds · 6–18°C",
    "{{WEATHER_2}}": "TUE 18 · ⛅ Patchy morning fog, then mostly sunny to partly cloudy · 7–20°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "WED 19 · 🌦️ Cloudy, showers increasing later in the day, winds picking up · 11–18°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 20 · 🌧️ Cloudy, very high chance of showers on and off · 10–16°C",
    "{{WEATHER_5}}": "FRI 21 · 🌧️ Cloudy, rain likely during the morning and afternoon · 9–15°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings for Carrum Downs or Melbourne metro — just a Strong Wind Warning current for Port Phillip Wednesday as showers and stronger northwesterlies move in, so it's worth getting outdoor blasting or coating work done in the first half of the week while conditions stay calm",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦🇷🇺 UKRAINE · KYIV LAUNCHES ONE OF ITS LARGEST DRONE ATTACKS OF THE WAR, KILLING AT LEAST SIX IN RUSSIA",
    "{{WORLD_1_HEADLINE}}": "Ukraine Launches One of Its Largest Drone Attacks of the War, Killing at Least Six in Russia",
    "{{WORLD_1_SUMMARY}}": "Ukraine fired hundreds of drones at targets across multiple Russian regions overnight Saturday, with Russia's military saying it destroyed 822 of them; an 83-year-old man was killed in the Moscow region and five people died when a roughly 150-drone strike hit towns in the Rostov region, damaging homes, a railway station and sparking a forest fire. It's one of Kyiv's largest aerial assaults of the war so far, and also struck a major retail warehouse near Podolsk, south of Moscow.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/16/nx-s1-5933006/ukraine-aerial-attack-6-dead-russia",

    "{{WORLD_2_FLAG}}": "🇮🇹 ITALY · THIEVES STEAL FOUR RENAISSANCE MASTERPIECES FROM A SICILY MUSEUM DURING FERRAGOSTO FESTIVITIES",
    "{{WORLD_2_HEADLINE}}": "Thieves Steal Four Renaissance Masterpieces From a Sicily Museum During Ferragosto Festivities",
    "{{WORLD_2_SUMMARY}}": "Thieves broke into Messina's Museo Interdisciplinare Regionale, bypassing the alarm system and forcing open an armoured display case to steal four works attributed to Renaissance master Antonello da Messina, including three panels of the 1473 San Gregorio Polyptych. The break-in happened during Italy's Ferragosto holiday and the city's La Vara religious festival, when Messina was packed with distracted crowds; the local culture chief called it \"a disaster.\"",
    "{{WORLD_2_URL}}": "https://www.euronews.com/culture/2026/08/16/thieves-bypass-security-to-steal-four-renaissance-artworks-from-sicily-museum",

    # Economics
    "{{ECON_1_FLAG}}": "🏠🇦🇺 HOUSING · SYDNEY'S HOUSE PRICE CORRECTION ACCELERATES, NOW DOWN MORE THAN 6% FROM ITS PEAK",
    "{{ECON_1_HEADLINE}}": "Sydney's House Price Correction Accelerates, Now Down More Than 6% From Its Peak",
    "{{ECON_1_SUMMARY}}": "Sydney dwelling values have now fallen more than 6% from their peak, with the decline accelerating to 1.4% over just the past 28 days — a pace of roughly 17% a year if it continues. ANZ is now forecasting a 10.6% national peak-to-trough fall, with Sydney leading the way at -14.5%. For a Carrum Downs blasting and coatings business, it's worth watching: renovation, new-build and property fit-out work — a real slice of the pipeline — tends to soften as home values keep falling.",
    "{{ECON_1_URL}}": "https://www.macrobusiness.com.au/2026/08/sydneys-house-price-correction-hits-new-milestone/",

    "{{ECON_2_FLAG}}": "⛽🇦🇺 FUEL · PETROL AND DIESEL PRICES KEEP EASING AS INTERNATIONAL BENCHMARK COSTS SOFTEN",
    "{{ECON_2_HEADLINE}}": "Petrol and Diesel Prices Keep Easing as International Benchmark Costs Soften",
    "{{ECON_2_SUMMARY}}": "The ACCC's most recent fuel price monitoring shows average retail petrol and diesel prices across Australia's five largest cities are now down 56c/L and 81c/L respectively from their end-March peak, as softer international benchmark costs flow through at the bowser. It's still worth budgeting on the high side for a fleet of utes, compressors and a blast truck, but for once the trend is running in your favour rather than against it.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖🖼️ AI TOOLS · GOOGLE SHUTS DOWN ITS IMAGEN 4 IMAGE MODELS TODAY, PUSHING DEVELOPERS TO NEWER 'NANO BANANA' MODELS",
    "{{TECH_1_HEADLINE}}": "Google Shuts Down Its Imagen 4 Image Models Today, Pushing Developers Toward Newer 'Nano Banana' Models",
    "{{TECH_1_SUMMARY}}": "Google is retiring its Imagen 4 family of AI image-generation models — standard, fast and ultra — from its Gemini API today, steering developers toward its newer Gemini image models instead. It's a practical reminder for anyone using an AI tool to knock up social posts, before-and-after job photos or quote graphics: if that tool is built on someone else's AI model under the hood, it can be switched off with a deadline you never see coming.",
    "{{TECH_1_URL}}": "https://kingy.ai/ai-launch-tracker/google-will-shut-down-three-imagen-4-api-models-august-17/",

    "{{TECH_2_FLAG}}": "🤖💻 AI TOOLS · ANTHROPIC ADDS AN 'AUTO-CONTINUE' FEATURE SO STALLED AI CODING SESSIONS RESUME THEMSELVES",
    "{{TECH_2_HEADLINE}}": "Anthropic Adds an 'Auto-Continue' Feature So Stalled AI Coding Sessions Resume Themselves",
    "{{TECH_2_SUMMARY}}": "Anthropic has added a small but useful feature to its Claude Code desktop app this month: an auto-continue option that automatically resumes a stalled AI session the moment your usage limit resets, rather than you having to remember to retry manually. It's part of a broader shift toward AI tools that quietly manage themselves in the background — worth keeping an eye on if you're relying on any AI tool for admin or quoting and don't want to be the one babysitting it.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🚀🤖 ROBOTICS · NASA'S NEXT MOON MISSION WILL TEST WHETHER A TEAM OF ROVERS CAN THINK FOR THEMSELVES",
    "{{ROBOT_1_HEADLINE}}": "NASA's Next Moon Mission Will Test Whether a Team of Rovers Can Think for Themselves",
    "{{ROBOT_1_SUMMARY}}": "NASA's CADRE mission will send three small rovers to the Moon later this year, where they'll spend about two weeks mapping terrain as a self-coordinating team — electing a \"leader,\" dividing up tasks and replanning on the fly if one rover's battery runs low, with no joystick and no human sign-off on individual moves. It's the first time NASA has run multiple robots beyond Earth as a single autonomous system, and the same fleet-coordination software is exactly the kind of thing now migrating into warehouse robots, autonomous forklifts and construction-site machinery that need to work without constant supervision.",
    "{{ROBOT_1_URL}}": "https://phys.org/news/2026-08-exploring-moon-require-rovers.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Federal and NSW Governments Strike Deal on a Major Post-Bondi Gun Buyback Scheme",
    "{{AUS_1_SUMMARY}}": "The Commonwealth and NSW governments have agreed to jointly fund a national gun buyback scheme in response to December's Bondi Beach terror attack, with NSW first to launch on 2 November 2026. Firearm owners exceeding new four-gun ownership limits will be compensated $650–$1,000 per weapon, with costs split evenly between federal and state governments and a second phase targeting higher-value firearms planned for early 2027.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/major-federal-state-gun-buyback-scheme/qh4ymqbmu",

    "{{AUS_2_HEADLINE}}": "Australian Swim Team Caps a Historic Pan Pacific Championships With 35 Medals",
    "{{AUS_2_SUMMARY}}": "The Dolphins finished the Pan Pacific Championships in Irvine, California with a record 15 gold, 11 silver and 9 bronze medals — nearly double their haul from 2018 — despite missing several of their biggest stars. On the final night, Lani Pallister beat American legend Katie Ledecky in the 800m freestyle and Sam Short broke Grant Hackett's long-standing Australian 1500m freestyle record.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Opposition Pledges a $50 Weekly Toll Cap for Small-Business Fleets Ahead of November's Election",
    "{{VIC_1_SUMMARY}}": "Victorian Opposition Leader Jess Wilson has pledged to cap weekly toll costs at $50 for two years for cars, vans and small-business fleets of up to five vehicles — rising to a permanent $60 cap from mid-2027 — while Premier Ben Carroll countered with a plan to recruit 200 retired police officers for back-of-house duties. The competing pitches mark the opening moves ahead of Victoria's state election on 28 November, and the toll cap would directly cover a small trade fleet running EastLink or CityLink daily.",

    # Science
    "{{SCI_1_FLAG}}": "🦴 SCIENCE · A 1950s FOSSIL SITTING IN A MUSEUM DRAWER TURNS OUT TO BE A BRAND NEW ICE AGE SPECIES",
    "{{SCI_1_HEADLINE}}": "A 1950s Fossil Sitting in a Museum Drawer Turns Out to Be a Brand New Ice Age Species",
    "{{SCI_1_SUMMARY}}": "A single fossil bone from Los Angeles's La Brea Tar Pits, collected in the 1950s and sitting unexamined in a museum collection for nearly 30 years, has just been identified as Spea labreae — a new species of Ice Age spadefoot toad and only the second extinct amphibian ever found in North America. A researcher finally re-examining the Tar Pits' amphibian bones spotted subtle features on an incomplete hip bone that set it apart from every known species, a reminder that genuinely new discoveries are still hiding in plain sight in old museum drawers.",

    # Business insight
    "{{INSIGHT_TITLE}}": "AI Can Now Scan a Job-Site Photo for Missing PPE — Is It Worth Adding to Your Safety Checklist?",
    "{{INSIGHT_BODY}}": "A new wave of AI vision tools can scan an ordinary job-site photo and flag a missing hard hat, respirator or hi-vis vest before an inspector does, built on the same image-recognition tech behind everyday phone apps. For a blasting and coatings business already juggling WorkSafe paperwork on every job, running a quick AI photo check before a client walk-through or audit could catch an issue while it's still cheap to fix, rather than after a stop-work notice lands. It's no substitute for a proper safety system — but as a five-minute second pair of eyes before someone official turns up, it's worth a look.",

    # Fun facts
    "{{FACT_1}}": "Pong, the 1972 game credited with kicking off the video game industry, was first tested in a single bar in Sunnyvale, California — the prototype machine broke within days, not from a fault, but because it was jammed solid with quarters.",
    "{{FACT_2}}": "Worcestershire sauce was invented by accident — 1830s Worcester chemists John Lea and William Perrins mixed a batch, hated the taste, and abandoned the barrel in a cellar for two years before rediscovering it fully fermented and genuinely good.",
    "{{FACT_3}}": "The wheelbarrow is believed to have first appeared in China around the 2nd century AD, with a single wheel positioned to carry the full load — a design clever enough that one person could shift what would otherwise take two.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the scaffolding contractor's small business always stand up to scrutiny at tax time?",
    "{{JOKE_PUNCHLINE}}": "Because every figure was properly braced before it went out the door.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Believe you can and you're halfway there.\"",
    "{{CLOSING_ATTR}}": "— Theodore Roosevelt",
    "{{CLOSING_MESSAGE}}": "It's a sunny start to the week in Carrum Downs once the morning fog burns off, with the calm holding until Wednesday's wind and showers roll in — good conditions for getting outdoor jobs finished while they last. Between Sydney's housing correction, a fossil that sat unexamined in a drawer for 30 years before turning out to be a brand new species, and the Dolphins wrapping up a record-breaking Pan Pacs campaign, today's a fair reminder that patience with the details usually pays off — on a job site or anywhere else.",
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
