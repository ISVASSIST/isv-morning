#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 08 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 08 Aug (BOM)
    "{{WEATHER_1}}": "SAT 08 · 🌦️ Partly cloudy, showers most likely early morning · 6–14°C",
    "{{WEATHER_2}}": "SUN 09 · 🌧️ High chance of showers, windy in the afternoon · 7–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 10 · 🌬️ Cloudy, very high chance of rain, windy · 8–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 11 · 🌧️ Very high chance of rain, easing later · 8–12°C",
    "{{WEATHER_5}}": "WED 12 · 🌦️ Showers morning, easing to light rain · 8–10°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings current for Melbourne / Carrum Downs, but a genuinely wet, windy spell builds Sunday through Tuesday",

    # World
    "{{WORLD_1_FLAG}}": "🇸🇩 SUDAN · DRONE STRIKES AND A WORSENING CHOLERA OUTBREAK BATTER BESIEGED EL-OBEID",
    "{{WORLD_1_HEADLINE}}": "Drone Strikes and a Worsening Cholera Outbreak Batter Sudan's Besieged City of El-Obeid",
    "{{WORLD_1_SUMMARY}}": "Residents of the half-million-strong city of El-Obeid describe skies filled with as many as 40 drones at a time, with strikes now hitting schools, a market, fuel stations, water points and the city's main power station — crippling medical facilities just as cholera tears through some communities. The UN warns of a growing risk of mass atrocities as Sudan's civil war, which has killed at least 59,000 people since 2023, grinds on with no resolution in sight.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/07/nx-s1-5921212/el-obeid-sudan-war",

    "{{WORLD_2_FLAG}}": "🇮🇷 IRAN · PARLIAMENT MOVES TO BAN US AND ISRAELI SHIPS FROM THE STRAIT OF HORMUZ",
    "{{WORLD_2_HEADLINE}}": "Iran's Parliament Reviews a Bill to Ban US and Israeli Ships From the Strait of Hormuz",
    "{{WORLD_2_SUMMARY}}": "The draft bill would bar vessels linked to the US, Israel and other 'hostile' countries from the strait until Iran is compensated for war damage, while charging other commercial vessels fees of up to 7% of cargo value to transit — with 20% fines for violations. The Trump administration has rejected the plan outright, but with roughly a fifth of the world's oil passing through the strait, it's another reason global fuel and shipping costs remain jumpy.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/08/06/nx-s1-5923623/iran-strait-hormuz-us-israel-ban",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺⛽ FUEL · UNLEADED PRICES SET TO CLIMB INTO THE MID-TO-HIGH 210S THIS WEEK",
    "{{ECON_1_HEADLINE}}": "Bowser Prices Are Set to Climb Further This Week as Wholesale Costs Catch Up With the Excise Rise",
    "{{ECON_1_SUMMARY}}": "The NRMA's latest weekly fuel report has average regular unleaded already up 45.9c/L since 30 June, and expects prices to push into the mid-to-high 210s cents per litre over the coming week as wholesale costs keep catching up with the 3 August excise rebate removal. Worth locking in a fill-up early in the week rather than waiting, and flagging the trend in any job costed more than a few days out.",
    "{{ECON_1_URL}}": "https://www.mynrma.com.au/cars-and-driving/fuel-finder/weekly-report",

    "{{ECON_2_FLAG}}": "🇦🇺🏦 RATES · ALL 37 ECONOMISTS IN A REUTERS POLL EXPECT THE RBA TO HOLD AT 4.35% TUESDAY",
    "{{ECON_2_HEADLINE}}": "Every One of 37 Economists in a Reuters Poll Expects the RBA to Hold Rates Tuesday",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank hands down its decision at 2:30pm Tuesday 11 August, with Governor Michele Bullock's press conference an hour later, and a unanimous hold call from economists means the bigger story will be the tone of the statement rather than the number itself. June's inflation came in softer than expected, but with the trimmed mean still above target, it's worth waiting for Tuesday's language before locking in any big loan or equipment finance decision.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💾 HARDWARE · SAMSUNG UNVEILS NEXT-GEN AI MEMORY IT SAYS COULD RUN 8X FASTER",
    "{{TECH_1_HEADLINE}}": "Samsung Unveils Next-Gen AI Memory Chips It Says Could Run Eight Times Faster Than Today's",
    "{{TECH_1_SUMMARY}}": "At the Future of Memory and Storage event in Santa Clara, Samsung previewed zHBM, zNAND-O and a 400-layer V10 BV-NAND chip — concept designs it says could deliver roughly eight times the performance of today's HBM5 memory for AI systems. None of it ships yet, but it's a sign the industry is racing to build its way out of the same AI-driven memory crunch that's been pushing up laptop and PC prices all year.",
    "{{TECH_1_URL}}": "https://news.samsung.com/global/samsung-unveils-next-gen-3d-memory-vision-at-fms-2026-charting-the-future-of-ai-infrastructure",

    "{{TECH_2_FLAG}}": "🤖 AI TALENT · GOOGLE'S JEFF DEAN LEAVES TO LAUNCH A NEW AI-FOR-SCIENCE STARTUP",
    "{{TECH_2_HEADLINE}}": "Google AI Chief Jeff Dean Departs to Launch an AI Research Startup With Former Colleagues",
    "{{TECH_2_SUMMARY}}": "Dean is stepping down from Google to found Discovery Loop, a public benefit corporation aimed at using AI to speed up scientific research, alongside fellow Google veterans Sanjay Ghemawat, Quoc Le and Oriol Vinyals. It's the latest sign of how fierce the fight for top AI talent has become between the big labs — a race that's ultimately what keeps pushing better, cheaper AI tools down to small business level.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳🤖 ROBOTICS · BYD CONFIRMS ITS FIRST HUMANOID ROBOT DEBUTS IN SHOWROOMS THIS MONTH",
    "{{ROBOT_1_HEADLINE}}": "BYD Confirms Its First Humanoid Robot, Xiao Di, Is Debuting in Car Showrooms This Month",
    "{{ROBOT_1_SUMMARY}}": "The world's largest EV maker says Xiao Di is a fully functional prototype, not just a concept — able to greet customers, translate across six Chinese dialects and six foreign languages, and demonstrate vehicles at its Di Space showrooms. Executive VP Stella Li says the goal is 'two or three robots in every store,' making BYD the latest Chinese manufacturer chasing Tesla into the humanoid robot race.",
    "{{ROBOT_1_URL}}": "https://www.scmp.com/business/china-business/article/3362362/byd-debut-first-humanoid-robots-august-rivalry-tesla-intensifies",

    # Australia
    "{{AUS_1_HEADLINE}}": "Vietnam's President Arrives for a Landmark First State Visit to Australia",
    "{{AUS_1_SUMMARY}}": "General Secretary and President To Lam lands for a state visit running 9–12 August, meeting Prime Minister Albanese in Canberra on Tuesday to discuss deepening the two countries' Comprehensive Strategic Partnership across defence, trade, energy and digital cooperation — his first visit to Australia since taking office.",
    "{{AUS_1_URL}}": "https://www.pm.gov.au/media/visit-australia-general-secretary-and-president-socialist-republic-vietnam",

    "{{AUS_2_HEADLINE}}": "Census Night Lands Tuesday — Here's What Households and Businesses Need to Know",
    "{{AUS_2_SUMMARY}}": "The 2026 Census falls on Tuesday 11 August, with the ABS reminding households to complete it as soon as their letter or paper form arrives — the data feeds directly into planning for local infrastructure, services and the kind of demand data councils and businesses use to understand their area.",
    "{{AUS_2_URL}}": "https://www.abs.gov.au/media-centre/media-releases/one-week-until-census-night-0",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Manslaughter Charge Laid Over Death of Sunshine Grocer Van Viet Truong",
    "{{VIC_1_SUMMARY}}": "A 15-year-old boy has been charged with manslaughter after Van Viet Truong, owner of the Hong Hung Asian Grocery in Melbourne's west, died from injuries suffered while going to a fellow retail worker's aid during an alleged theft last Saturday — a case that's prompted Sunshine traders to meet with police and a local MP over round-the-clock patrols for the strip.",

    # Science
    "{{SCI_1_FLAG}}": "🦈 PALAEONTOLOGY · LOST MEGALODON FOSSILS FOUND ON A MUSEUM SHELF CONFIRM A 79-FOOT GIANT",
    "{{SCI_1_HEADLINE}}": "Megalodon Fossils Thought Destroyed in 1989 Turn Up on a Museum Shelf, Confirming a 79-Foot Giant",
    "{{SCI_1_SUMMARY}}": "Enormous 11-million-year-old vertebrae from a single Megalodon, found in Denmark and long presumed destroyed during a 1989 museum move, have turned up unnoticed on a shelf at the Natural History Museum of Denmark. At 23cm across, they're the largest Megalodon vertebrae on record, strengthening evidence the giant shark could exceed 24 metres in length and live for nearly a century.",

    # Business insight
    "{{INSIGHT_TITLE}}": "A Hard Week for Melbourne Retailers Is a Reminder — AI-Powered CCTV Can Flag Trouble Before It Escalates",
    "{{INSIGHT_BODY}}": "This week's tragic death of a Sunshine shop owner, after he went to help a colleague confront an alleged theft, is a stark reminder that a quiet shopfront or yard can turn dangerous fast. Modern AI-powered camera systems don't just record after the fact — they can flag unusual movement, loitering or a group approaching after hours, and push an alert straight to your phone before anything escalates, rather than leaving footage to be reviewed once it's too late. For a small operation with a yard, storeroom or shopfront sitting empty overnight, it's worth a serious look at whether your current setup is just recording, or actually watching.",

    # Fun facts
    "{{FACT_1}}": "The Hills Hoist rotary clothesline was built by Adelaide returned serviceman Lance Hill in his own backyard in 1945, after his wife's old rope line kept tangling in a tree — his cog-and-pinion winding mechanism to raise and lower the whole frame became the basis of a company that turned an unremarkable backyard fix into an Australian household fixture.",
    "{{FACT_2}}": "The wine cask, or 'goon bag,' was patented in 1965 by South Australian winemaker Thomas Angove as a collapsible bladder in a box — the airtight, non-drip tap that made it actually practical wasn't added until Penfolds employee Charles Malpas refined the design two years later, in 1967.",
    "{{FACT_3}}": "The pneumatic tyre wasn't invented by an engineer — Scottish-born vet John Boyd Dunlop came up with it in 1887 in Belfast, wrapping his son's solid-rubber bicycle wheels in an inflated rubber hose to smooth out the ride, and patented the idea the following year, decades before it became standard on every vehicle on the road.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the mobile car detailer never double-book a client?",
    "{{JOKE_PUNCHLINE}}": "Because his diary was as spotless as the cars he left behind.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The most dangerous phrase in the language is, 'We've always done it this way.'\"",
    "{{CLOSING_ATTR}}": "— Grace Hopper",
    "{{CLOSING_MESSAGE}}": "It's a partly cloudy Saturday in Carrum Downs, with showers building into a genuinely wet, windy stretch from Sunday right through to Tuesday — worth getting any outdoor jobs locked in early while the weather holds. Keep Tuesday 11 August marked for both the RBA's rate call and census night, and if you're around the yard this weekend, it's a fair prompt to check your own site security is actually watching, not just recording.",
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
