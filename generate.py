#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 18 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 18 May (BOM forecast issued 17 May)
    "{{WEATHER_1}}": "MON 18 · ☁ Showers · 16°C",
    "{{WEATHER_2}}": "TUE 19 · 🌧 Rain · 15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 20 · 🌧 Rain · 14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 21 · ⛅ Clearing · 15°C",
    "{{WEATHER_5}}": "FRI 22 · ⛅ Mostly cloudy · 17°C",
    "{{WEATHER_ALERT}}": "☔ SHOWERS MON–WED",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 UKRAINE",
    "{{WORLD_1_HEADLINE}}": "Ukraine Launches Its Largest Drone Strike in Over a Year — 500 Drones Hit Moscow Oil Refineries",
    "{{WORLD_1_SUMMARY}}": "Ukraine launched a massive overnight 500-drone assault targeting Russian oil refineries, storage terminals, and fuel distribution infrastructure near Moscow — killing four people and wounding twelve. Russian air defences intercepted more than 1,000 drones within 24 hours, but fires erupted at multiple refinery sites including the Moscow Oil Refinery in Kapotnya. President Zelenskyy confirmed the operation as \"entirely justified\" retaliation for ongoing Russian attacks on Kyiv.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/05/17/nx-s1-5824987/ukrainian-drone-strikes-on-russia-kill-4-moscow",

    "{{WORLD_2_FLAG}}": "🌍 GLOBAL HEALTH",
    "{{WORLD_2_HEADLINE}}": "WHO Declares DR Congo–Uganda Ebola Outbreak a Global Emergency — Rare Strain Has No Vaccine",
    "{{WORLD_2_SUMMARY}}": "The World Health Organization declared the Bundibugyo Ebola outbreak in eastern DR Congo and Uganda a Public Health Emergency of International Concern on May 17. At least 80 suspected deaths and 246 suspected cases span Ituri Province, with confirmed cases now appearing in Kampala. The Bundibugyo strain has no approved vaccine or proven treatment — unlike the better-known Zaire strain — raising serious international concern about containment and cross-border spread.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/5/17/who-declares-ebola-outbreak-in-drc-uganda-a-global-health-emergency",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 RATES",
    "{{ECON_1_HEADLINE}}": "Three Rate Hikes In — Economists Say RBA Has Room to Pause in June, But the Squeeze Is Already Here",
    "{{ECON_1_SUMMARY}}": "With the RBA cash rate now at 4.35% — the highest since 2011 after three consecutive hikes this year — CBA economists say the board has \"room to pause\" when it next meets in June. Headline CPI is forecast to peak near 4.8% this quarter before slowly easing into 2027. For small trades businesses carrying equipment loans, vehicle finance, or overdrafts, the cost of debt is materially higher than 18 months ago — and a June hold doesn't signal relief is coming anytime soon.",
    "{{ECON_1_URL}}": "https://www.commbank.com.au/articles/newsroom/2026/05/rba-may-interest-rates-cba-economists-analysis.html",

    "{{ECON_2_FLAG}}": "⛽ FUEL",
    "{{ECON_2_HEADLINE}}": "Fuel Excise Relief of 32¢/Litre Expires June 30 — Lock In Second-Half Quote Rates Before Diesel Resets",
    "{{ECON_2_SUMMARY}}": "The government's fuel excise reduction of 32 cents per litre — cutting costs across petrol and diesel since 1 April — expires on 30 June 2026. With diesel running around 25% below last year's elevated peaks during this relief period, the expiry creates a real pricing recalculation for any business that factors fuel into its rate schedule. Fleet-heavy trades should review cost assumptions in second-half quotes now — before prices written today become losses delivered in August.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📡 AI DIFFUSION",
    "{{TECH_1_HEADLINE}}": "Global AI Usage Climbs to 17.8% of Working-Age Population — Up 1.5 Points in a Single Quarter",
    "{{TECH_1_SUMMARY}}": "A Microsoft report tracking global AI diffusion shows usage climbed from 16.3% to 17.8% of the world's working-age population in Q1 2026 alone — a 1.5-point quarterly jump that confirms AI adoption is still in rapid uptake, not plateau. Enterprise AI integration stands at 88% of large organisations. Agentic AI — systems that autonomously execute complex multi-step tasks — is the fastest-growing category, with documented productivity gains now widely published in logistics, customer service, and operational management.",
    "{{TECH_1_URL}}": "https://blogs.microsoft.com/on-the-issues/2026/05/07/the-state-of-global-ai-diffusion-in-2026/",

    "{{TECH_2_FLAG}}": "🏛 AI GOVERNANCE",
    "{{TECH_2_HEADLINE}}": "US Regulators Now Get Early Access to AI Models Before Public Launch — Microsoft and xAI Among Firms That Agreed",
    "{{TECH_2_SUMMARY}}": "In a significant policy shift, US government regulators are now requiring pre-deployment access to frontier AI models before they reach the public. Microsoft and xAI are among the companies that have agreed to provide early model access for safety testing and bias review. The move signals the end of the \"launch first, regulate later\" pattern that has defined AI development to date — and will likely slow the fastest model release cycles while increasing market confidence in tools that do ship.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 PHYSICAL AI",
    "{{ROBOT_1_HEADLINE}}": "Accenture, Vodafone, and SAP Deploy Humanoid Robots in Live Warehouse — Integrated Directly Into SAP EWM",
    "{{ROBOT_1_SUMMARY}}": "In one of the most enterprise-complete humanoid robot deployments to date, Accenture, Vodafone Procure & Connect, and SAP piloted humanoid robots inside Vodafone's operational warehouse in Duisburg, Germany — integrated directly with SAP's Extended Warehouse Management system. The robots execute picking, sorting, and logistics tasks while reporting findings in real time into SAP for operational visibility. Presented at Hannover Messe 2026, the pilot is being closely watched as a blueprint for deploying humanoid robots into existing enterprise infrastructure without replacing legacy systems.",
    "{{ROBOT_1_URL}}": "https://newsroom.accenture.com/news/2026/accenture-vodafone-procure-connect-and-sap-pilot-humanoid-robotics-in-warehouse-operations",

    # Australia
    "{{AUS_1_HEADLINE}}": "Two Queensland Liberals Defect to One Nation Amid Budget Backlash — LNP Recovery Narrative Takes a Hit",
    "{{AUS_1_SUMMARY}}": "Two high-profile Queensland Liberal members defected to One Nation this weekend, citing grassroots anger at the federal budget's superannuation and capital gains changes and dissatisfaction with the state LNP's response. The defections come within 24 hours of the Stafford by-election revealing a swing toward the LNP — creating a fractured picture for Queensland conservatives as both parties navigate the political fallout from the Chalmers budget.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news",

    "{{AUS_2_HEADLINE}}": "Delta Goodrem Finishes Fourth for Australia at Eurovision 2026 — Bulgaria Wins the 70th Competition in Vienna",
    "{{AUS_2_SUMMARY}}": "Australia's entry, pop icon Delta Goodrem, placed fourth at the 70th Eurovision Song Contest held in Vienna, with Bulgaria's performer Dara taking the top prize with a high-energy anthem that dominated both jury and public vote. Australia has competed as a non-European wildcard since 2015. Goodrem, performing with a live band and receiving strong televote support, confirmed she'd be honoured to compete again.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Design Week Enters Its Second Week — 400+ Events Still Ahead, Free Entry to Most",
    "{{VIC_1_SUMMARY}}": "Melbourne Design Week 2026 — celebrating its 10th anniversary and the Asia-Pacific's largest design festival — begins its second and final week today, running through Sunday May 24. Themes include AI-driven design futures, circular sustainability, and Australian-made craft. Japanese designer Shunji Yamanaka delivers a keynote this week at the National Communication Museum on prosthetics, robotics, and future product design. Full program at designweek.melbourne.",

    # Science
    "{{SCI_1_FLAG}}": "🌌 SPACE",
    "{{SCI_1_HEADLINE}}": "Blue-Whale-Sized Asteroid Passes Earth Tonight at Just 90,000 km — Closer Than Many Satellites",
    "{{SCI_1_SUMMARY}}": "Asteroid 2026 JH2, discovered only eight days ago by the Mt. Lemmon Survey in Arizona, sweeps past Earth tonight at 21:23 UTC at just 90,000 km — less than a quarter of the Moon's distance, closer than some geostationary satellites. The 15–35-metre rock is roughly the size of a blue whale and poses zero impact risk. At magnitude +11.5 during closest approach, it'll briefly be visible through a small telescope under dark skies. The Virtual Telescope Project is hosting a free public livestream of the event.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Turning a Wet Week Into a Productivity Sprint: The AI Tools That Pay Back in the Field",
    "{{INSIGHT_BODY}}": "With showers forecast through to Wednesday in Carrum Downs, this is the week to convert unavoidable downtime into a genuine productivity investment. AI tools like Claude or ChatGPT can produce a complete, editable Safe Work Method Statement in under 10 minutes, rewrite a standard quote template from your existing examples, or draft a professional client newsletter from three bullet points in under five. The highest-return exercise for a slow Monday: ask an AI tool to analyse your last 10 to 20 completed jobs and identify the common factors behind your worst margin performers. That single exercise — taking roughly an hour — can reshape how you estimate an entire category of work for years to come. Small trades businesses that treat wet-day downtime as strategic thinking time are quietly building the operational advantage their competitors won't see until it is too late.",

    # Fun Facts
    "{{FACT_1}}": "The banana is technically a berry in botanical terms, while a strawberry is not — it is classified as a \"false fruit.\" Even more surprising: the banana plant is not a tree at all. What looks like a trunk is a pseudostem made of tightly rolled leaf bases, making the banana the world's largest herbaceous plant despite growing up to nine metres tall.",
    "{{FACT_2}}": "Recycling a single aluminium can saves enough energy to run a television for roughly three hours. Aluminium can be recycled indefinitely without any loss of quality or purity, using just 5% of the energy required to refine it from raw bauxite ore. Australia is the world's largest producer of bauxite — the raw material all primary aluminium starts from — making it the foundation of one of the planet's most energy-efficient recycling chains.",
    "{{FACT_3}}": "Velcro was invented in 1941 by Swiss engineer George de Mestral after he noticed burdock seed burrs sticking to his dog's fur on a country walk. Under a microscope he saw thousands of tiny hooks. It took ten years of development to recreate the effect synthetically. He named his invention Velcro by combining the French words for velvet (velours) and hook (crochet) — and NASA later adopted it for the Apollo missions.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the earthmoving contractor refuse to upgrade to the new GPS-guided excavator?",
    "{{JOKE_PUNCHLINE}}": "Said he'd been digging himself into holes for thirty years — he wasn't about to let a computer start finding them first.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The only way to do great work is to love what you do.\"",
    "{{CLOSING_ATTR}}": "— Steve Jobs",
    "{{CLOSING_MESSAGE}}": "It's a grey Monday in Carrum Downs, with showers forecast through to mid-week. Tonight an asteroid the size of a blue whale passes closer than some satellites — no drama, just a reminder the universe keeps its own schedule. Melbourne Design Week is in its second week with free events running through Sunday. And with six weeks until payday super kicks in and the fuel excise cut expiring on the same day, the June-to-July window is shaping up as a genuine financial planning sprint. Stay dry, stay across the numbers — and use the downtime well, Liall.",
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
