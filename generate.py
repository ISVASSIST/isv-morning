#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 15 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 15 Aug (BOM)
    "{{WEATHER_1}}": "SAT 15 · ⛅ Partly cloudy, slight chance of a shower, patchy morning fog near the hills · 6–14°C",
    "{{WEATHER_2}}": "SUN 16 · 🌤️ Partly cloudy, morning fog clearing to a mostly sunny afternoon · 7–15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 17 · ☀️ Morning fog easing to a mostly sunny afternoon, light winds · 7–16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "TUE 18 · ⛅ Partly cloudy, winds turning north-easterly 15–25 km/h · 8–16°C",
    "{{WEATHER_5}}": "WED 19 · ⛅ Partly cloudy, similar mild conditions continuing · 8–16°C",
    "{{WEATHER_ALERT}}": "No BOM warnings currently listed for Carrum Downs — a drier, calmer pattern than the past fortnight, with just patchy morning fog to plan around",

    # World
    "{{WORLD_1_FLAG}}": "🇨🇴 COLOMBIA · EARTHQUAKE DEATH TOLL HITS 285 AS DECISION TO DECLINE FOREIGN RESCUE TEAMS DRAWS CRITICISM",
    "{{WORLD_1_HEADLINE}}": "Colombia Earthquake Death Toll Hits 285 as Government's Early Decision to Decline International Rescue Teams Draws Scrutiny",
    "{{WORLD_1_SUMMARY}}": "The toll from the 7.4-magnitude earthquake that struck western Colombia on 10 August has climbed to 285 dead, with 379 people still missing and almost 4,000 injured, as criticism grows over the disaster agency's decision to decline offers of international rescue assistance in the early days of the response. More than 84,000 homes have now been damaged or destroyed across Cali, Pereira and the Chocó region, with recovery crews still working through rubble five days on.",
    "{{WORLD_1_URL}}": "https://thecitypaperbogota.com/news/petro-government-declined-foreign-rescue-teams-as-earthquake-death-toll-hits-285/",

    "{{WORLD_2_FLAG}}": "🇱🇧🇮🇱 LEBANON · ISRAEL VOWS NOT TO WITHDRAW FROM SECURITY ZONES AS LEBANON CONDEMNS HOME DEMOLITIONS",
    "{{WORLD_2_HEADLINE}}": "Lebanon Condemns Israeli Home Demolitions as Israel Vows Not to Withdraw From Security Zones in Lebanon, Syria or Gaza",
    "{{WORLD_2_SUMMARY}}": "Lebanon's government has condemned a wave of home demolitions by Israeli forces in the country's south as a \"serious violation of international law,\" after Israeli Defense Minister Israel Katz said Israel would clear certain areas and would not withdraw from security zones \"in Lebanon, not in Syria and not in Gaza\" under any circumstances. It's another flashpoint in a region already absorbing the fallout from Russian and Ukrainian strikes on Black Sea shipping that are stoking fresh fears over global food prices.",
    "{{WORLD_2_URL}}": "https://www.democracynow.org/2026/8/14/headlines",

    # Economics
    "{{ECON_1_FLAG}}": "⛽🇦🇺 FUEL · VICTORIA HOLDS AUSTRALIA'S CHEAPEST AVERAGE PETROL PRICE AS THE NATIONAL AVERAGE KEEPS CLIMBING",
    "{{ECON_1_HEADLINE}}": "Victoria Keeps Australia's Cheapest Average Petrol Price Even as the National Average Climbs 29 Cents in a Month",
    "{{ECON_1_SUMMARY}}": "Victoria's average unleaded price is sitting around 204.6c/L, the lowest of any state, while the national average has risen 29.4 cents over the past month as the fuel excise's return to full rate and firmer international benchmark prices work their way through the bowser. Worth locking in a fill before the weekend if your run sheet has you covering a lot of kilometres this week.",
    "{{ECON_1_URL}}": "https://petrolmate.com.au/monthly-fuel-report",

    "{{ECON_2_FLAG}}": "🇦🇺💵 AUD · AUSSIE DOLLAR FIRMS AS UNEMPLOYMENT HOLDS AT 4.4% AHEAD OF THE RBA'S SEPTEMBER CALL",
    "{{ECON_2_HEADLINE}}": "Australian Dollar Firms as Unemployment Holds at 4.4%, With Wage Growth Now the Number to Watch Before September",
    "{{ECON_2_SUMMARY}}": "The Australian dollar has pushed up to around US70.8c after unemployment held steady at 4.4% and employment grew by roughly 76,300 people last month, keeping the labour market resilient even as early signs of moderation build. With the RBA's next call not due until September, wage growth is now the figure economists are watching most closely for a read on where the cash rate goes next.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖⚡ AI SPEED · OPENAI'S NEW 'ULTRAFAST' MODE RUNS GPT-5.6 UP TO 14X FASTER, POWERED BY CEREBRAS",
    "{{TECH_1_HEADLINE}}": "OpenAI Launches 'Ultrafast' Mode That Runs GPT-5.6 Sol Up to 14 Times Faster Than Standard",
    "{{TECH_1_SUMMARY}}": "OpenAI has opened a limited preview of Ultrafast, a new API tier that runs its GPT-5.6 Sol model up to 14 times faster than standard processing — as fast as 750 tokens a second — using chips from partner Cerebras under their US$10 billion deal. For a trades business the headline speed number matters less than the trend underneath it: the AI tools behind your quoting and admin keep getting faster and cheaper, not slower and pricier.",
    "{{TECH_1_URL}}": "https://openai.com/index/previewing-ultrafast/",

    "{{TECH_2_FLAG}}": "🤖🏢 AI RACE · GOOGLE SHIPS A SHARPER, CHEAPER MODEL OVERNIGHT AS APPLE TRAINS A CHINA-SPECIFIC AI WITH ALIBABA",
    "{{TECH_2_HEADLINE}}": "Google Quietly Ships a Sharper, Cheaper AI Model Overnight as Apple Trains a China-Specific Version With Alibaba",
    "{{TECH_2_SUMMARY}}": "Google pushed out an upgraded, cheaper AI model overnight with little fanfare, while Apple has been quietly training a separate version of its AI for the Chinese market with help from Alibaba — the latest sign the big AI players are splitting their focus between cost-cutting at home and localised builds offshore. Another reminder that whichever tool you're paying for is being upgraded constantly in the background, so it's worth checking every few months that you're still on the best plan for what you actually use.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭🤖 ROBOTICS · CHINA'S AGIBOT OVERTAKES UNITREE AS THE WORLD'S TOP HUMANOID ROBOT MAKER",
    "{{ROBOT_1_HEADLINE}}": "China's AgiBot Overtakes Unitree as the World's Top Humanoid Robot Maker, With Chinese Firms Now 97% of Global Shipments",
    "{{ROBOT_1_SUMMARY}}": "Shanghai-based AgiBot shipped 8,400 humanoid robots in the first half of 2026 to take 44% of the global market and overtake Unitree, as Chinese manufacturers now account for 97% of the roughly 19,100 humanoids shipped worldwide since January — more than triple last year's volume. The mix has shifted fast too, with industrial and commercial use now over 70% of shipments, up from about half a year ago — a sign humanoid robotics is moving out of the lab and onto factory and warehouse floors faster than most people have clocked.",
    "{{ROBOT_1_URL}}": "https://www.scmp.com/tech/tech-trends/article/3363544/agibot-overtakes-unitree-top-global-humanoid-robot-vendor-first-half-amid-ipo-push",

    # Australia
    "{{AUS_1_HEADLINE}}": "National Workplace Fatalities Fall to 167 in 2025 as the Threshold for High-Risk Construction Work Tightens to Two Metres",
    "{{AUS_1_SUMMARY}}": "New national data shows workplace fatalities fell to 167 in 2025, down from 188 the year before, with construction among the improving sectors, as changes that took effect on 1 July lowered the trigger for \"high-risk construction work\" rules from three metres down to two metres. Worth a quick check that your site's SWMS and height-work sign-off reflect the new two-metre threshold rather than the old one.",
    "{{AUS_1_URL}}": "https://www.healthandsafetyinternational.com/article/1947111/workplace-fatalities-australia-fall-167-construction-safety-improves",

    "{{AUS_2_HEADLINE}}": "China's 55% Tariff Trigger Squeezes Australian Beef Exporters as Shipments Grind to a Near-Halt",
    "{{AUS_2_SUMMARY}}": "Australian beef exporters are grinding shipments to China to a near-halt as they approach the 205,000-tonne quota that triggers a punishing 55% tariff for the rest of the year under Beijing's new three-year import regime. Trade Minister Don Farrell says the government is \"disappointed\" and is pressing China to honour the free trade agreement — a reminder for any business with import or export exposure that trade terms can shift with little notice.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Becomes First State to Mandate Poultry Housing as H5 Bird Flu Detections Climb Past 175",
    "{{VIC_1_SUMMARY}}": "Victoria has become the first Australian state to mandate poultry housing, requiring anyone keeping 50 or more birds across metropolitan Melbourne, coastal and some neighbouring areas to house or confine their flock for an initial 14 days, after 20 further H5 bird flu detections in crested terns near Portland and Nelson took the state and national tally past 175. There are no detections yet in commercial poultry or the wider agriculture sector — worth knowing if you keep birds on-site or run jobs near the affected coastal areas.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ SCIENCE · WORLD'S FIRST SUPERCONDUCTING QUANTUM HEAT ENGINE COULD SIMPLIFY TOMORROW'S QUANTUM COMPUTERS",
    "{{SCI_1_HEADLINE}}": "Physicists Build the World's First Superconducting Quantum Heat Engine, a Step Toward Simpler Quantum Computers",
    "{{SCI_1_SUMMARY}}": "Researchers at Aalto University have built the first cyclic quantum heat engine inside a superconducting circuit, using a transmon qubit connected to a quantum-circuit refrigerator to convert heat near absolute zero into measurable work — effectively recreating a car engine's Otto cycle at the quantum scale. Future versions could let quantum computers read out their own qubits without the huge bundles of costly microwave cables current machines rely on, potentially simplifying how bigger quantum computers get built.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The Working-At-Height Threshold Just Dropped to Two Metres — Is Your Paperwork Still Written for Three?",
    "{{INSIGHT_BODY}}": "New national data released this week shows workplace fatalities fell to 167 in 2025, but the change most likely to catch out a trades business right now is a quieter one: since 1 July, \"high-risk construction work\" starts at two metres off the ground, not three. If your SWMS, site inductions or subcontractor paperwork were written before July, there's a good chance they still reference the old three-metre trigger — worth five minutes with an AI tool to scan your standard templates and flag anything that needs updating before an inspector or an insurer does it for you.",

    # Fun facts
    "{{FACT_1}}": "R.M. Williams began in 1932 when 20-year-old Reginald Murray Williams started making boots in a tin shed near Adelaide, perfecting a one-piece elastic-sided design cut from a single length of leather with barely any stitching — a construction method the company still uses today.",
    "{{FACT_2}}": "The Voyager Golden Record, launched into interstellar space aboard Voyager 1 and 2 in 1977, carries greetings in 55 languages, natural sounds of Earth and a curated selection of music — including Chuck Berry's 'Johnny B. Goode' — chosen by a committee led by astronomer Carl Sagan.",
    "{{FACT_3}}": "The Anglo-Zanzibar War of 27 August 1896 is the shortest war on record — the British ultimatum expired at 9am, bombardment began minutes later, and the Sultan's forces surrendered inside roughly 40 minutes.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the food truck operator's small business never run short of regulars?",
    "{{JOKE_PUNCHLINE}}": "Because he always parked exactly where the smell could do the marketing for him.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"You do not rise to the level of your goals. You fall to the level of your systems.\"",
    "{{CLOSING_ATTR}}": "— James Clear",
    "{{CLOSING_MESSAGE}}": "It's a milder, drier Saturday in Carrum Downs after a soggy fortnight, with just patchy morning fog to watch before a mostly sunny run into next week — good timing to get outdoor jobs back on the board. With Victoria's new poultry housing order now in force and China's humanoid robot makers dominating today's headlines, it's a quieter weekend news-wise — a good one to actually switch off for a bit.",
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
