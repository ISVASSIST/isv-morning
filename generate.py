#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 11 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 11 Jun
    # Warm northerly Thu before cold front, rain Fri-Sat, clearing Sun-Mon
    "{{WEATHER_1}}": "THU 11 · ⛅ Mostly Cloudy · 13–22°C",
    "{{WEATHER_2}}": "FRI 12 · 🌧 Rain · 11–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 13 · 🌧 Showers · 9–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 14 · ⛅ Partly Cloudy · 8–13°C",
    "{{WEATHER_5}}": "MON 15 · ⛅ Cloudy · 9–14°C",
    "{{WEATHER_ALERT}}": "⚽ WORLD CUP OPENS TODAY — MEXICO v SA AT AZTECA",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸 USA · MIDDLE EAST",
    "{{WORLD_1_HEADLINE}}": "US and Iran Exchange Strikes Over Hormuz — Tehran Fires Back at US Bases in Bahrain, Kuwait and Jordan",
    "{{WORLD_1_SUMMARY}}": "The US-Iran conflict entered a dangerous new phase on June 10 when US forces struck Qeshm Island and Iranian coastal installations along the Strait of Hormuz, after Iran downed a US Apache helicopter. Tehran's IRGC retaliated with drone attacks on the US Fifth Fleet in Bahrain and a Kuwaiti airbase, plus a long-range missile strike on Jordan. President Trump said the US would resume attacks on Iran on Thursday, citing stalled ceasefire talks. A Qatari delegation was in Tehran Wednesday attempting to broker a deal. Oil markets are pricing a sustained risk premium above $12 per barrel — extending global energy inflation well beyond the July 1 domestic excise change.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/6/10/iran-strikes-bahrain-and-jordan-in-retaliation-for-us-attacks-in-hormuz",

    "{{WORLD_2_FLAG}}": "🚀 MARKETS · USA",
    "{{WORLD_2_HEADLINE}}": "SpaceX Prices Its Record $75 Billion IPO Tonight — The Largest Market Listing in History Opens on Nasdaq Tomorrow",
    "{{WORLD_2_SUMMARY}}": "SpaceX prices its initial public offering tonight, June 11, under the ticker SPCX at $135 per share — targeting a $75 billion raise, the largest IPO in recorded market history, more than triple the previous US record set by Alibaba in 2014. At its implied $1.75 trillion valuation, SpaceX will rank among the world's ten most valuable companies from the moment SPCX opens for trading on Friday. The IPO is already fully oversubscribed. Elon Musk retains approximately 82% of post-listing voting power. The company that changed how humans reach orbit becomes tomorrow the company every fund manager has to have a view on.",
    "{{WORLD_2_URL}}": "https://finance.yahoo.com/markets/stocks/articles/spcx-ipo-record-75-billion-155245946.html",

    # Economics
    "{{ECON_1_FLAG}}": "📊 US INFLATION · GLOBAL IMPACT",
    "{{ECON_1_HEADLINE}}": "US CPI Hits 4.2% — Highest in Three Years as Iran War Energy Shock Drives 40% Jump in Petrol Prices",
    "{{ECON_1_SUMMARY}}": "The US Bureau of Labor Statistics May CPI report, released June 10, showed annual inflation at 4.2% — the highest since early 2023. Energy accounted for over 60% of the monthly increase, with US petrol prices up 40.5% year-on-year driven by the Iran war and Strait of Hormuz risk premium. Core inflation (excluding food and energy) is still running at 2.9%. For Australian businesses, the mechanism is direct: sustained high crude oil prices flow through to bowser prices within 2–3 weeks. With the domestic 32c/L excise cut expiring June 30, international energy pressure extends the fuel cost squeeze well into the new financial year.",
    "{{ECON_1_URL}}": "https://www.cnbc.com/2026/06/10/cpi-inflation-report-may-2026.html",

    "{{ECON_2_FLAG}}": "🇦🇺 SMALL BUSINESS · FEDERAL BUDGET",
    "{{ECON_2_HEADLINE}}": "Permanent $20K Instant Asset Write-Off Confirmed for July 1 — 19 Days to Capture FY2026 Tools and Equipment",
    "{{ECON_2_SUMMARY}}": "The 2026–27 Federal Budget permanently locks in the $20,000 instant asset write-off for businesses with annual turnover under $10 million, effective July 1. Any tool, machine, or equipment purchased and in use before June 30 can be fully expensed this financial year — directly reducing your taxable income up to $20K. For trades businesses planning to upgrade a compressor, fit out a vehicle, or replace a piece of plant, the 19-day window before financial year-end is the most tax-effective time to act. The asset must be in use before midnight June 30 — not merely ordered.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🍎 APPLE · WWDC 2026",
    "{{TECH_1_HEADLINE}}": "Apple Rebuilds Siri With Google's Gemini — Every iPhone Business User Gets a Vastly More Capable AI From Autumn",
    "{{TECH_1_SUMMARY}}": "At WWDC 2026 on June 8, Apple unveiled a completely rebuilt Siri powered by a custom 1.2-trillion-parameter Google Gemini model, licensed at approximately $1 billion per year. New Siri holds multi-turn conversations, recalls past interactions, accesses context across apps, and completes multi-step tasks automatically. Users can choose ChatGPT, Gemini, or Anthropic's Claude as their AI backend. For any trades business owner running operations from an iPhone or iPad, iOS 27 this autumn will make the device meaningfully more capable as an on-site business tool — drafting quotes, summarising site notes, and writing client follow-ups in plain English.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/06/08/apple-wwdc-2026-live-updates.html",

    "{{TECH_2_FLAG}}": "⚖️ AI REGULATION · USA",
    "{{TECH_2_HEADLINE}}": "June 30 Is the First US AI Enforcement Deadline — Colorado's AI Act Applies to Any System Making Decisions About People",
    "{{TECH_2_SUMMARY}}": "On June 30, Colorado's Consumer Protections for Artificial Intelligence Act becomes enforceable — the first AI law in the United States with real penalties. It covers any high-risk AI system used in decisions affecting employment, housing, credit, or healthcare, requiring risk management programs, annual impact assessments, and consumer rights to explanation and appeal. Companies under $25 million revenue get a grace period. The broader signal for Australian operators: the era of unregulated AI deployment is ending. Australia's own AI regulatory framework is expected to take shape in late 2026 — what Colorado's enforcement looks like in practice will inform what arrives here.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 HUMANOID · USA",
    "{{ROBOT_1_HEADLINE}}": "Agility Robotics Deploys Digit Humanoids at Toyota Canada — Robot-as-a-Service Model Signals the Pivot From Pilot to Platform",
    "{{ROBOT_1_SUMMARY}}": "Agility Robotics has more than seven Digit humanoid robots operating on the Toyota Canada production floor under a Robot-as-a-Service commercial model — Toyota pays per operational hour, not as a capital purchase. The RaaS structure removes the upfront cost barrier that has kept humanoid robots in pilot territory and is now regarded by industry analysts as the deployment mechanism most likely to drive volume adoption through 2026. With Figure, Boston Dynamics, and Agility all active in real automotive and logistics facilities this month, the shift from proof-of-concept to sustained production deployment is now documented fact.",
    "{{ROBOT_1_URL}}": "https://kraneshares.com/humanoid-robotics-in-2026-the-race-from-pilot-to-platform/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Western Sydney Airport to Open for Freight in July, Passengers from 25 October — Sydney's Second Airport Is Almost Here",
    "{{AUS_1_SUMMARY}}": "The Federal Government confirmed Western Sydney International (Nancy-Bird Walton) Airport will begin freight operations July 26 and open to passengers on October 25, 2026. Jetstar will operate the first commercial service — an Airbus A320 to the Gold Coast at 11am on October 25. The airport is the largest infrastructure project ever built in NSW and adds critical capacity to a Sydney aviation system that has been near its operational limits for years. For Australian businesses, a second Sydney gateway means more competitive freight options and new direct flight routes from late 2026.",
    "{{AUS_1_URL}}": "https://www.pm.gov.au/media/its-official-western-sydney-open-passengers-25-october-and-freight-26-july-2026",

    "{{AUS_2_HEADLINE}}": "Seven West Media Cuts Up to 200 Jobs in $400M Southern Cross Merger — Newsrooms and Local Hubs Hollowed Out",
    "{{AUS_2_SUMMARY}}": "Up to 200 positions will be permanently cut at Seven West Media this week following its $400 million merger with Southern Cross Media, as the combined group targets $30 million in annual cost savings. Local broadcast hubs and investigative reporting capabilities are among the hardest-hit areas. The restructuring reflects an accelerating collapse in linear television advertising revenue, with digital competition pushing traditional broadcast media to the point where cost reduction — rather than reinvestment — is the only available lever.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "5,000 Blue Beanies at the MCG — Melbourne Farewells Neale Daniher in a State Funeral Worthy of a Champion",
    "{{VIC_1_SUMMARY}}": "Over 5,000 Victorians gathered at the Melbourne Cricket Ground on Wednesday June 10 to farewell Neale Daniher AO — former Demons coach, Australian of the Year 2025, and the driving force behind the fight against Motor Neurone Disease. Eulogies came from his four children and wife Jan. Paul Kelly closed the service with Leaps and Bounds. The hearse made one final lap of the MCG before proceeding down Daniher Way. FightMND, the charity Daniher founded, has raised more than $150 million for MND research since 2015.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 NEUROSCIENCE · USA",
    "{{SCI_1_HEADLINE}}": "Scientists Complete the First Full Brain Map of Any Adult Animal — 160,000 Neurons and 50 Million Connections in a Fruit Fly",
    "{{SCI_1_SUMMARY}}": "An international team led by Harvard Medical School and Princeton University has published the first complete connectome of an adult animal's entire nervous system — mapping every neuron and synapse in a fruit fly's brain and nerve cord at electron microscope resolution. The Brain and Nerve Cord (BANC) dataset captures all ~160,000 neurons and over 50 million connections, assembled from thousands of microscopy images stitched together by AI. The key finding: most fly behaviours appear to be directed by local neural circuits distributed through the body, not by a single central command in the brain. The full dataset is freely available online as an open-source resource for neuroscience globally. Published in Nature, June 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Building Your FY2027 Rate Card With AI: How to Model the July 1 Cost Hit Before It Lands",
    "{{INSIGHT_BODY}}": "On July 1, two cost changes land simultaneously: the 32 cents per litre fuel excise cut expires, and the Fair Work annual wage adjustment takes effect. For most trades operators, those two line items alone add hundreds of dollars per week to the cost base. If your rates don't adjust before that date — not after — the hit lands directly on margin. Most business owners know this is coming but haven't sat down to model what it actually means for their specific operation. That's exactly the task AI is built for. Open Claude or ChatGPT and describe your business: how many crew, how many vehicles, your approximate weekly fuel spend, your current day rates, and the mix of job types you run. Ask the AI to estimate the dollar impact of the excise change and the wage rise on your cost per job, per crew day, and per week. Then ask it to draft updated rate card entries — realistic numbers that absorb the increases without sending clients a shock. Ask it to write the advisory message you'll send to regular clients: professional, factual, framed around industry cost reality rather than apology. Do this before June 30. It takes less than an hour with AI doing the modelling. The operators who do this now will start July 1 in front. The ones who wait will spend the rest of the financial year chasing ground they already lost.",

    # Fun Facts
    "{{FACT_1}}": "Tonight SpaceX prices the largest initial public offering in recorded market history — targeting $75 billion at $135 per share under the ticker SPCX on Nasdaq. For context, the previous US IPO record was Alibaba's $25 billion in 2014; Saudi Aramco's global record was $35.4 billion in 2019. At $1.75 trillion, SpaceX is valued at more than Toyota, LVMH, and every company listed on the ASX 200 combined. Elon Musk, who founded SpaceX in 2002 with $100 million of his PayPal proceeds, retains roughly 82% of voting control after the float.",

    "{{FACT_2}}": "Since 1989, a single whale nicknamed 'the 52 Hz whale' has been tracked by US Navy hydrophone networks crossing and recrossing the North Pacific, singing at 52 Hz — far above the 10–40 Hz calls of blue whales and 20 Hz of fin whales, and outside the vocal range of every other known whale species. For over 35 years its calls have gone unanswered. Scientists believe it is a rare blue/fin whale hybrid whose anatomy produces a frequency no other whale can receive. It is the only whale on Earth no other whale can hear — and it has been singing alone into the ocean longer than the World Wide Web has existed.",

    "{{FACT_3}}": "Melbourne's winter solstice is just 10 days away — June 21 is the shortest day of the year in the Southern Hemisphere. On that day, Carrum Downs will receive approximately 9 hours and 20 minutes of daylight, compared to nearly 14 hours and 50 minutes at the summer solstice in December. For trades working outdoors, this 5.5-hour seasonal difference in available daylight compresses the effective working window through winter, tightens cure times for exterior coatings, and limits the time available for photographing completed work in natural light.",

    # Joke
    "{{JOKE_SETUP}}": "My sparky told me he'd invested $10,000 in the SpaceX IPO overnight.",
    "{{JOKE_PUNCHLINE}}": "I said: 'Mate, you can't even get your quotes off the ground.' He said: 'That's exactly why I need to diversify.'",

    # Closing
    "{{CLOSING_QUOTE}}": "“No winter lasts forever; no spring skips its turn.”",
    "{{CLOSING_ATTR}}": "— Hal Borland",
    "{{CLOSING_MESSAGE}}": "It's Thursday morning in Carrum Downs — warmer than you'd expect thanks to those northerly winds, before rain arrives tomorrow and the weekend turns properly wintry. Today the 2026 FIFA World Cup opens in Mexico City: Mexico vs South Africa at the Azteca, and the greatest football tournament in history is officially underway. Tonight SpaceX prices the largest IPO in market history, and yesterday's US inflation data confirmed that global energy costs aren't cooling any time soon. July 1 is 19 days away. If the rate card isn't done, today is the day to start. Have a good Thursday, Liall.",
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
