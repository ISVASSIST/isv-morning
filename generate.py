#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 19 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 19 Jul (BOM)
    "{{WEATHER_1}}": "SUN 19 · 🌫️❄️☀️ Morning frost & fog (SE suburbs), then sunny · 4–17°C",
    "{{WEATHER_2}}": "MON 20 · 🌫️☀️ Morning fog patches, mostly sunny · 5–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "TUE 21 · 🌦️ Shower or two, cooler · 6–12°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 22 · 🌦️ Partly cloudy, shower chance · 7–16°C",
    "{{WEATHER_5}}": "THU 23 · ⛅ Partly cloudy, mild · 7–15°C",
    "{{WEATHER_ALERT}}": "⚠ FROST & FOG PATCHES THIS MORNING (SE SUBURBS) · SHOWERS RETURN TUESDAY · NO SEVERE WARNINGS ACTIVE",

    # World
    "{{WORLD_1_FLAG}}": "🇰🇼🇯🇴 GULF & JORDAN · IRAN WIDENS TARGETS · DESALINATION PLANTS AND US ALLIES HIT",
    "{{WORLD_1_HEADLINE}}": "Iran Widens Its Targets Beyond Military Sites, Striking Kuwaiti Infrastructure as Jordan Intercepts a Record Missile Barrage",
    "{{WORLD_1_SUMMARY}}": "Washington says it struck bridges and military logistics infrastructure in southern Iran overnight, while Tehran retaliated by hitting a power and desalination plant in Kuwait for the second time this week, a US radar station in Oman, and military facilities in Bahrain, Jordan and — for the first time — Syria, a claim the US disputes. Jordan's military intercepted ten Iranian missiles in a single night, its highest count of the conflict so far, and Brent crude jumped to a one-month high above $88 a barrel on the news, with Iranian officials saying recent US strikes have now killed dozens and wounded hundreds more.",
    "{{WORLD_1_URL}}": "https://www.foxnews.com/live-news/iran-war-trump-israel-hormuz-oil-july-18-2026",

    "{{WORLD_2_FLAG}}": "⚽🌎 NEW JERSEY · WORLD CUP FINAL · SPAIN AND ARGENTINA CLASH FOR THE TROPHY",
    "{{WORLD_2_HEADLINE}}": "Spain and Argentina Meet in Tonight's World Cup Final, Capping the First 48-Team Tournament Hosted Across Three Nations",
    "{{WORLD_2_SUMMARY}}": "Spain and Argentina face off at MetLife Stadium in New Jersey (3pm ET Sunday, 5am Monday AEST), a day after France beat England in the third-place playoff in Miami. It's the first World Cup with 48 teams and the first ever hosted jointly by three countries — the USA, Mexico and Canada — and Lionel Messi has already become the first player to reach 10 career assists in World Cup history during this tournament, giving the final an extra layer of send-off theatre regardless of who lifts the trophy.",
    "{{WORLD_2_URL}}": "https://www.espn.com/soccer/story/_/id/49382572/spain-vs-argentina-fifa-world-cup-2026-final-tv-channel-how-watch-kick-live-stream-injury-predicted-line-ups",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ OIL MARKETS · BRENT HITS ONE-MONTH HIGH · KUWAIT PLANT STRIKE SPOOKS TRADERS",
    "{{ECON_1_HEADLINE}}": "Brent Crude Jumps to a One-Month High Above $88 a Barrel After Iran Strikes a Second Kuwaiti Desalination Plant",
    "{{ECON_1_SUMMARY}}": "Brent crude futures surged about 4.6% to close at $88.10 a barrel on Friday, its highest level in a month, after Kuwait reported Iran had struck a power and water desalination plant for the second time this week, with retaliatory strikes also reported in Bahrain, Jordan, Oman, Qatar and Syria. With roughly 20% of the world's oil normally moving through the Strait of Hormuz and that flow still disrupted, expect the bowser to keep tracking this conflict rather than settling down, whatever the fuel excise relief scheme is doing in the background.",
    "{{ECON_1_URL}}": "https://www.cnbc.com/2026/07/17/oil-price-today-brent-wti.html",

    "{{ECON_2_FLAG}}": "🏗️ SMALL BUSINESS · NEW FINANCIAL YEAR BITES · INSOLVENCY RISK RISING IN CONSTRUCTION",
    "{{ECON_2_HEADLINE}}": "New Financial Year Compliance Costs Are Stacking Up, With Insolvency Risk Rising Fastest in Construction and Hospitality",
    "{{ECON_2_SUMMARY}}": "The raft of changes that landed on July 1 — higher ASIC registration fees, Payday Super's new cash-flow timing, and a 4.75% minimum wage rise — has added compliance and cash-flow pressure right as analysts flag construction and hospitality as the industries most exposed to a coming uptick in insolvencies through the rest of this financial year. None of it is a crisis on its own, but stacked together it's exactly the kind of slow squeeze that catches thin-margin trades businesses off guard if the books aren't watched closely.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔐 AI SECURITY · MICROSOFT'S PROJECT PERCEPTION · CHEAPER RIVAL TO ANTHROPIC'S MYTHOS",
    "{{TECH_1_HEADLINE}}": "Microsoft Prepares to Launch Project Perception, an AI Tool That Hunts and Fixes Software Vulnerabilities on the Cheap",
    "{{TECH_1_SUMMARY}}": "Microsoft is set to release Project Perception this month, a security tool that routes each vulnerability-hunting task to whichever AI model — its own, OpenAI's or Anthropic's — handles it most cheaply, rather than running everything through the most expensive option. It's aimed at big enterprise security teams for now, but it's a preview of where AI-assisted cybersecurity tools are heading: cheaper, always-on vulnerability scanning that smaller software vendors, including whatever quoting or scheduling app your business runs on, will likely inherit within a year or two.",
    "{{TECH_1_URL}}": "https://www.techrepublic.com/article/news-microsoft-project-perception-ai-security-tool/",

    "{{TECH_2_FLAG}}": "🤖 AI PRICING · CLAUDE'S FABLE 5 SETTLES · SUBSCRIPTION LIMBO ENDS",
    "{{TECH_2_HEADLINE}}": "Anthropic Ends Months of Back-and-Forth, Locking Its Most Powerful Claude Model Into Paid Plans From Monday",
    "{{TECH_2_SUMMARY}}": "After extending free access to its flagship Fable 5 model three times since June, Anthropic has settled on a permanent structure from July 20: Max and Team Premium subscribers keep it bundled in at half their usual usage limits, while Pro and Team Standard users move to pay-as-you-go credits plus a one-off $100 top-up. If your business runs job quotes, emails or admin through any AI chatbot, it's a reminder that the free-and-unlimited phase of this technology is ending — worth checking which plan you're actually on before the next bill lands.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇰🇷🤖 SEOUL · SAMSUNG'S HUMANOID PUSH · NEW 'HX' DIVISION TAKES SHAPE",
    "{{ROBOT_1_HEADLINE}}": "Samsung Consolidates Its Robotics Teams Into a New 'HX' Division to Chase Factory-Floor Humanoid Robots",
    "{{ROBOT_1_SUMMARY}}": "Samsung is merging robot research and commercialisation teams currently scattered across its Future Robotics Office, Samsung Research and Global Technology Research into a single new organisation, tentatively called 'HX' for Humanoid Experience, with a mandate to get robotic hands to factory-ready standard and eventually spin off into its own business division. It's the latest sign that the humanoid robot race isn't just Tesla and the Chinese makers — Korea's biggest manufacturer is now betting its own production lines will run on them too.",
    "{{ROBOT_1_URL}}": "https://www.koreajoongangdaily.com/business/samsung-revamps-robotics-operations-for-humanoid-pushnbspfloats-new-hx-division/12778404",

    # Australia
    "{{AUS_1_HEADLINE}}": "Home Affairs Minister Admits There's 'No Easy Answer' to Australia's Decades-Long Parent Visa Backlog",
    "{{AUS_1_SUMMARY}}": "Home Affairs Minister Tony Burke conceded there are no quick fixes to the parent visa backlog, which has swollen to around 157,000 applications with only 8,500 places allocated each year — leaving contributory visa applicants facing waits of roughly 15 years and non-contributory applicants up to 33 years. A 2023 expert panel recommended switching to a ballot system like New Zealand's and Canada's; Burke says a range of options are still on the table, but nothing is imminent.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/podcast-episode/minister-says-no-easy-solutions-to-parent-visa-backlog-midday-news-bulletin-18-july-2026/g3xrwi5xc",

    "{{AUS_2_HEADLINE}}": "Albanese Declares 'No Place' for Anti-Muslim Hatred as Government Acts on Islamophobia Under-Reporting",
    "{{AUS_2_SUMMARY}}": "Prime Minister Anthony Albanese said there is no place in Australia for anti-Muslim hatred or racial intolerance, framing new measures as practical steps to strengthen social cohesion, while Home Affairs Minister Tony Burke said Islamophobia remains significantly under-reported nationally. The comments come as the Middle East conflict continues to spill into domestic community tensions here, with the government keen to be seen getting ahead of it rather than reacting to an incident.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Run Melbourne Shuts CBD Roads From 3:30am, While Essendon and North Melbourne Host AFL Round 19 Today",
    "{{VIC_1_SUMMARY}}": "Run Melbourne brings road closures and parking restrictions across the CBD from 3:30am to 1:30pm today, with extra train and tram services laid on and bus replacements running on the Hurstbridge line for scheduled works between Heidelberg and Greensborough — worth building into any Sunday morning run through the city. Footy-wise, Essendon hosts GWS at Marvel Stadium this afternoon and North Melbourne faces Melbourne, rounding out AFL Round 19.",

    # Science
    "{{SCI_1_FLAG}}": "🚀 SPACE · INDIA JOINS THE CLUB · FIRST PRIVATE ORBITAL LAUNCH STICKS THE LANDING",
    "{{SCI_1_HEADLINE}}": "India's Skyroot Aerospace Reaches Orbit on Its First Try, Becoming the World's Third Nation With a Private Orbital Launch Capability",
    "{{SCI_1_SUMMARY}}": "Skyroot Aerospace's Vikram-1 rocket lifted off from the Satish Dhawan Space Centre on Saturday, reaching its planned 450-kilometre orbit just 15 minutes after liftoff and deploying two cubesats exactly on schedule despite a late technical hold. Called Mission Aagaman ('arrival' in Sanskrit), it makes India just the third country after the US and China with a commercial launch provider capable of reaching orbit — a major vote of confidence for a homegrown space industry that barely existed a decade ago.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Compressor Won't Text You Before It Fails — AI-Powered Predictive Maintenance Is Starting To",
    "{{INSIGHT_BODY}}": "A blown compressor or a spray rig going down mid-job doesn't just cost the repair — it costs the day, and sometimes the client. A new generation of predictive maintenance apps now plug into cheap vibration and temperature sensors on compressors, generators and spray equipment, watching for the small changes that come before a breakdown rather than waiting for the failure itself. None of this requires an enterprise budget anymore — a $50-a-month sensor and app combination can flag a bearing on its way out weeks before it seizes, which is usually the difference between a scheduled half-day and a lost week.",

    # Fun Facts
    "{{FACT_1}}": "The word 'boycott' comes from Captain Charles Boycott, a land agent in 1880s Ireland who was so thoroughly shunned by local tenants and tradespeople — nobody would harvest his crops, deliver his mail or serve him in shops — that his name became the word for the tactic itself.",

    "{{FACT_2}}": "Bamboo is the fastest-growing woody plant on Earth — some species can shoot up 91 centimetres in a single day, or roughly 4cm an hour, fast enough that you can genuinely watch it grow if you sit still long enough.",

    "{{FACT_3}}": "Pac-Man's four ghosts each run a different targeting algorithm rather than just chasing the player — Blinky hunts directly, Pinky aims ahead of you, Inky uses Blinky's position to flank, and Clyde wanders off when he gets close — making the 1980 arcade game one of the earliest well-known examples of distinct AI 'personalities' in software.",

    # Joke
    "{{JOKE_SETUP}}": "A welder's apprentice asked why his boss never rushed a joint, even with a client breathing down his neck about the deadline.",
    "{{JOKE_PUNCHLINE}}": "He said, 'Mate, a bad weld looks perfectly fine for about a week — after that, it's not my signature holding it together anymore, it's my licence.'",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The way to get started is to quit talking and begin doing.\"",
    "{{CLOSING_ATTR}}": "— Walt Disney",
    "{{CLOSING_MESSAGE}}": "It's a frosty, foggy start to Sunday in Carrum Downs before the sun gets through — 4–17°C, with showers not due back until Tuesday. Run Melbourne has the CBD half shut this morning if you're heading that way, footy's on at Marvel Stadium this afternoon, and the World Cup final kicks off in the small hours of Monday AEST — a fitting note to end the tournament on before Brent crude and the Hormuz situation are back on the desk tomorrow.",
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
