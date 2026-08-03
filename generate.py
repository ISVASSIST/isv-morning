#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 04 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 04 Aug (BOM)
    "{{WEATHER_1}}": "TUE 04 · 🌧️ Showers, most likely SE suburbs, easing tonight · 5–12°C",
    "{{WEATHER_2}}": "WED 05 · 🌦️ Shower or two, most likely later in the day · 6–13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 06 · 🌦️ Shower or two, similar pattern · 6–13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 07 · ⛅ Partly cloudy, drier stretch begins · 6–14°C",
    "{{WEATHER_5}}": "SAT 08 · ⛅ Mostly cloudy, isolated shower chance · 6–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings current for Melbourne / Carrum Downs",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇱🇵🇸 GAZA · ISRAELI STRIKES KILL 18 AS NETANYAHU SPOKESMAN CASTS DOUBT ON PUBLICLY DISCLOSED PEACE DEAL",
    "{{WORLD_1_HEADLINE}}": "Israeli Strikes Kill 18 in Gaza as a Netanyahu Spokesman Says the Publicly Announced Peace Deal 'Doesn't Reflect Israel's Positions'",
    "{{WORLD_1_SUMMARY}}": "Israeli airstrikes hit Gaza for a second straight day, killing at least 18 Palestinians across Gaza City, Deir al-Balah and Khan Younis, even as the Board of Peace announced Hamas had accepted the next phase of last year's ceasefire roadmap — a claim a Netanyahu spokesman quickly disputed. Israel has now expanded its territorial control to roughly two-thirds of Gaza, up from just over half when the ceasefire began, another reminder that a headline deal doesn't always match what's happening on the ground.",
    "{{WORLD_1_URL}}": "https://www.newstribune.com/news/2026/aug/03/israeli-strikes-kill-18-in-gaza-minister-says-no-deal-to-halt-attacks/",

    "{{WORLD_2_FLAG}}": "🇮🇷🇺🇸 IRAN · US AND IRANIAN NEGOTIATORS SET TO RESUME DIRECT TALKS TODAY OVER A HORMUZ DEAL",
    "{{WORLD_2_HEADLINE}}": "US and Iranian Negotiators Are Set to Resume Direct Talks Today as Trump Holds Off a Planned Strike",
    "{{WORLD_2_SUMMARY}}": "Trump says he's holding off a strike on Iran that would have been the largest since World War II, with negotiators due back at the table today after Iran reportedly agreed in principle to fully reopen the Strait of Hormuz to commercial shipping. Oil prices dropped more than $5 a barrel on the news, given roughly a fifth of the world's traded oil passes through that strait — worth watching this week if today's talks hold.",
    "{{WORLD_2_URL}}": "https://www.cbsnews.com/live-updates/iran-war-us-trump-strait-of-hormuz-kuwait-jordan-air-base/",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺🏠 HOUSING · NATIONAL HOME VALUES POST THEIR STEEPEST MONTHLY FALL IN ALMOST FOUR YEARS",
    "{{ECON_1_HEADLINE}}": "Australian Home Values Just Recorded Their Steepest Monthly Fall in Nearly Four Years",
    "{{ECON_1_SUMMARY}}": "National home values dropped 0.7% in July — the biggest single-month fall since December 2022 — with Sydney down 1.4% and Melbourne down 1.2%, as high interest rates keep squeezing buyers. A softer housing market can mean smaller reno and maintenance budgets from homeowners, so it's worth watching which of your regular residential clients start trimming scope on upcoming jobs.",
    "{{ECON_1_URL}}": "https://www.bloomberg.com/news/articles/2026-08-02/australia-s-housing-market-worsens-with-falls-getting-steeper",

    "{{ECON_2_FLAG}}": "🇦🇺⛽ FUEL · EXCISE RISE NOW FULLY IN EFFECT · ACCC WATCHING FOR PRICE GOUGING AT THE BOWSER",
    "{{ECON_2_HEADLINE}}": "The Fuel Excise Increase Is Now Fully in Effect, With the ACCC Watching for Price Gouging at the Bowser",
    "{{ECON_2_SUMMARY}}": "With the excise now sitting at 53.7 cents a litre following Sunday's rise, capital city petrol and diesel have already climbed as much as 42 cents a litre in places, and the consumer watchdog has been urged to keep a close eye on retailers padding margins on top of the legitimate increase. Worth comparing a couple of servos near your sites this week rather than assuming the nearest bowser is still the cheapest.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 GOOGLE WORKSPACE · GEMINI NOW LETS YOU DROP TIMESTAMPED COMMENTS ON VIDEOS IN GOOGLE DRIVE",
    "{{TECH_1_HEADLINE}}": "Google Drive Now Lets You Anchor Comments to an Exact Moment in a Video, Rolling Out From Today",
    "{{TECH_1_SUMMARY}}": "From today, Google Workspace users can leave comments pinned to a specific timestamp on any video stored in Drive, rather than just commenting on the file as a whole. A genuinely practical one for a trades business — it means a foreman can flag the exact second in a site walkthrough or toolbox-talk video that needs fixing, instead of writing a paragraph trying to describe where in the clip the problem is.",
    "{{TECH_1_URL}}": "https://workspaceupdates.googleblog.com/2026/",

    "{{TECH_2_FLAG}}": "🇨🇳🤖 AI MODELS · DEEPSEEK RELEASES ITS CHEAP, HIGH-AGENCY V4-FLASH MODEL TO THE PUBLIC",
    "{{TECH_2_HEADLINE}}": "DeepSeek Has Publicly Released Its V4-Flash Model, Undercutting Rivals on Price for Agentic AI Work",
    "{{TECH_2_SUMMARY}}": "Chinese AI lab DeepSeek this week pushed its V4-Flash model out of preview and into general release, with stronger autonomous 'agent' capabilities and lower running costs than its earlier version. It's a reminder that the AI tools doing your admin and quoting don't need to be the most famous or expensive ones on the market — cheaper, capable models are landing every few weeks now.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · EX-GOOGLE DEEPMIND TEAM LAUNCHES REIMAGINE ROBOTICS, ROBOTS THAT LEARN ON THE JOB",
    "{{ROBOT_1_HEADLINE}}": "A New Robotics Startup Founded by Ex-Google DeepMind Leaders Has Launched Robots That 'Learn on the Job'",
    "{{ROBOT_1_SUMMARY}}": "Reimagine Robotics, founded by former leaders of Google DeepMind's Applied Robotics team, has come out of stealth with a system that lets ordinary factory workers train a robot directly on the line, cutting what used to take a day of specialist programming down to about 10 minutes. It's already running in advanced manufacturing and electronics disassembly sites — another sign the barrier to using a robot on the floor is dropping fast, not just for giant firms with in-house coders.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/reimagine-robotics-emerges-stealth-with-robotslearn-on-the-job/",

    # Australia
    "{{AUS_1_HEADLINE}}": "New National Health Report Finds Overweight and Obesity Have Overtaken Smoking as Australia's Leading Cause of Ill Health",
    "{{AUS_1_SUMMARY}}": "The Australian Institute of Health and Welfare's Australia's Health 2026 report finds about two in three adults now live with overweight or obesity, which has overtaken tobacco as the leading risk factor behind disease and death — even as overall life expectancy keeps climbing, now 81.1 years for men and 85.1 for women. Worth a thought if your business is one of the many trades with long hours, servo lunches and not much time for a proper feed.",
    "{{AUS_1_URL}}": "https://www.aihw.gov.au/news-media/media-releases/2026/july/latest-report-card-on-australia-s-health-reveals-areas-of-improvement-and-challenges",

    "{{AUS_2_HEADLINE}}": "A New Poll Shows One Nation Now Running Slightly Ahead of Labor Nationally, With the Nationals Leader Open to Working With Them",
    "{{AUS_2_SUMMARY}}": "The latest Redbridge poll has One Nation edging ahead of Labor for the second time in four months, and Nationals leader Matt Canavan says he's 'willing to co-operate' with the party as its support climbs. A sign the political ground is shifting well before the next federal contest, regardless of where your own vote sits.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "A Qantas Flight Bound for Chile Was Diverted to Melbourne Overnight, Stranding Nearly 200 Passengers",
    "{{VIC_1_SUMMARY}}": "Qantas flight QF27 left Sydney for Santiago on Sunday night but developed a problem about 4.5 hours in, forcing the Boeing 787 to turn back across the Tasman and land in Melbourne around 11pm rather than Sydney, which was shut by its overnight curfew. Passengers were put up overnight before continuing on a replacement flight — a good reminder that even a well-planned schedule can end up somewhere nobody booked.",

    # Science
    "{{SCI_1_FLAG}}": "🌿 PHARMACOLOGY · SCIENTISTS MAP HOW TWO POISONOUS PLANTS BUILD COMPOUNDS THAT COULD INSPIRE NEW MEDICINES",
    "{{SCI_1_HEADLINE}}": "Scientists Have Mapped How Two Poisonous Plants Build Their Toxins — and the Same Chemistry Could Inspire New Medicines",
    "{{SCI_1_SUMMARY}}": "Researchers have identified six enzymes that wolfsbane and larkspur use to build a complex, medically promising compound, opening a path to producing similar chemicals in the lab rather than relying on foraging dangerous plants. A handy reminder that some of the nastiest things growing in a paddock are also where a fair bit of modern medicine quietly comes from.",

    # Business insight
    "{{INSIGHT_TITLE}}": "House Prices Just Had Their Worst Month in Nearly Four Years — Is Your Quoting Fast Enough for a Tighter Market?",
    "{{INSIGHT_BODY}}": "National home values just posted their steepest monthly fall in almost four years, with Melbourne down 1.2% in July alone — a sign more homeowners will be trimming reno and maintenance budgets rather than committing to big-ticket jobs. In a more price-sensitive market, the trades that win aren't always the cheapest — they're often the ones who get a proper quote back to the customer before a nervous homeowner gets three more quotes and cold feet. An AI tool that pulls from your past job costings can turn a same-day site visit into a same-day formal quote, and that turnaround speed alone can matter more than shaving a few dollars off the price. Worth testing on your next few enquiries and watching whether it moves your win rate.",

    # Fun facts
    "{{FACT_1}}": "The Sydney Harbour Bridge was built from both shores at once using six million hand-driven rivets, with the two halves of the steel arch meeting in the middle in 1930 to within a few millimetres of true — all worked out with slide rules and drafting tables, decades before computer modelling existed.",
    "{{FACT_2}}": "The QWERTY keyboard layout wasn't designed for speed — Christopher Latham Sholes arranged it in the 1870s specifically to separate commonly paired letters and slow typists down, so the mechanical arms of early typewriters wouldn't jam and tangle.",
    "{{FACT_3}}": "The Wright brothers' first powered flight in 1903 covered just 37 metres — shorter than the wingspan of a modern Boeing 747-8, which stretches 68.4 metres tip to tip.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the electrician's small business never get its wires crossed at tax time?",
    "{{JOKE_PUNCHLINE}}": "Because he always kept his books properly earthed.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"It always seems impossible until it's done.\"",
    "{{CLOSING_ATTR}}": "— Nelson Mandela",
    "{{CLOSING_MESSAGE}}": "It's a showery start to Tuesday in Carrum Downs, with today's rain most likely over the south-east suburbs and easing tonight before a similar pattern repeats through the week. The fuel excise rise is now fully baked into prices at the bowser, so budget for it on your next fill, and keep an eye on the Middle East today — direct US-Iran talks are due to resume, and a good outcome there could take some heat out of oil prices for everyone.",
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
