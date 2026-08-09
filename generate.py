#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 10 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 10 Aug (BOM)
    "{{WEATHER_1}}": "MON 10 · 🌧️ Very high chance of rain, most likely morning and afternoon · 10–14°C",
    "{{WEATHER_2}}": "TUE 11 · 🌦️ High chance of showers, most likely evening · 9–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 12 · 🌧️ Very high chance of showers, most likely morning and afternoon · 9–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 13 · 🌤️ Medium chance of showers, mostly easing · 9–16°C",
    "{{WEATHER_5}}": "FRI 14 · ⛅ Medium chance of a shower · 9–15°C",
    "{{WEATHER_ALERT}}": "No severe warnings for Carrum Downs itself, but a Flood Watch and damaging-wind warning are current further north across Victoria's alpine, Gippsland and North East regions after a vigorous weekend rain band — expect today's heaviest local rain before it eases through midweek",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 IRAN · TEHRAN DEMANDS US END BLOCKADE BEFORE REOPENING STRAIT OF HORMUZ",
    "{{WORLD_1_HEADLINE}}": "Iran Demands End to US Naval Blockade Before It Will Fully Reopen the Strait of Hormuz",
    "{{WORLD_1_SUMMARY}}": "Iran's national security leadership says it won't fully reopen the Strait of Hormuz to commercial shipping until the US ends its naval blockade, withdraws troops and pays compensation, even as Foreign Minister Abbas Araghchi signalled a narrower Iran-Oman shipping arrangement is close. President Trump said Washington is only \"semi-negotiating\" with Tehran, a day after oil prices fell almost 5% on hopes a planned US strike had been shelved. The strait has been substantially blocked since the war began in late February, with two Qatari LNG tankers struck there in the past fortnight alone.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/liveblog/2026/8/9/iran-war-live-tehran-demands-end-to-us-blockade-to-reopen-strait-of-hormuz",

    "{{WORLD_2_FLAG}}": "🇧🇷 BRAZIL · TOURIST HELICOPTER CRASH KILLS FOUR IN RIO NATIONAL PARK",
    "{{WORLD_2_HEADLINE}}": "Sightseeing Helicopter Crash Kills Four, Including Three Colombian Tourists, in Rio's Tijuca National Park",
    "{{WORLD_2_SUMMARY}}": "A sightseeing helicopter crashed into dense forest near the Vista Chinesa lookout in Rio de Janeiro's Tijuca National Park on Saturday, killing the pilot and three Colombian tourists who were in Brazil celebrating a family member's 15th birthday. The thick vegetation at the crash site slowed recovery efforts through the weekend. Rio's mayor has since called for tighter oversight of the city's popular tourist helicopter industry.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/8/8/four-killed-in-helicopter-crash-in-brazils-rio-de-janeiro",

    # Economics
    "{{ECON_1_FLAG}}": "⛽🇦🇺 FUEL · PETROL AND DIESEL KEEP CLIMBING AS EXCISE RELIEF FULLY ENDS",
    "{{ECON_1_HEADLINE}}": "Petrol and Diesel Prices Keep Climbing as Fuel Excise Relief Fully Ends",
    "{{ECON_1_SUMMARY}}": "The temporary fuel excise relief ended in full on 2 August, with the excise rate returning to 53.7 cents a litre and pump prices climbing across most capital cities and more than 190 regional locations since. The ACCC's monitoring shows average petrol prices across the five largest cities are still 37c/L higher than before the Middle East conflict began, with diesel up 71c/L, and NRMA's live tracking has further rises flagged this week as wholesale costs flow through. For a business running utes, compressors and site vehicles daily, it's worth re-checking fuel surcharges on quotes rather than absorbing the difference.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🇦🇺🏦 RATES · RBA BOARD MEETS TODAY, HOLD AT 4.35% WIDELY EXPECTED TOMORROW",
    "{{ECON_2_HEADLINE}}": "RBA Board Meets Today, With a Hold at 4.35% Widely Expected When the Decision Lands Tomorrow",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank's Monetary Policy Board began its scheduled two-day meeting today, with economists near-unanimous that Governor Michele Bullock and the board will hold the cash rate at 4.35% when the decision lands at 2:30pm tomorrow. A softer-than-expected inflation read last quarter underpins the call, though the unresolved Strait of Hormuz standoff and its flow-through to fuel and freight costs means there's no clear signal yet on when a cut might follow — worth factoring in before locking in equipment finance this week.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · CHATGPT ATLAS BROWSER SHUT DOWN TODAY, FOLDED BACK INTO CHATGPT",
    "{{TECH_1_HEADLINE}}": "OpenAI Shuts Down Its Standalone Atlas Browser, Folding Agentic Features Back Into ChatGPT",
    "{{TECH_1_SUMMARY}}": "OpenAI's standalone Atlas browser, launched only last October, was switched off today as the company folds its agentic browsing features — multi-tab research, downloads, saved logins — directly into ChatGPT and Codex instead of maintaining a separate app. OpenAI says the lesson from nine months of Atlas was that a standalone browser was \"the wrong package\" for the technology. Anyone who signed up for Atlas should export bookmarks and saved pages before access disappears entirely.",
    "{{TECH_1_URL}}": "https://www.techedt.com/chatgpt-atlas-to-shut-down-on-9-august-as-openai-moves-browser-features-into-chatgpt",

    "{{TECH_2_FLAG}}": "🤖 AI COSTS · COMPANY BUILT AN AI SPEND METER AFTER COSTS SPIRALLED 80% A MONTH",
    "{{TECH_2_HEADLINE}}": "Rippling Built an 'AI Spend Console' After Its Own AI Bill Spiralled 80% a Month",
    "{{TECH_2_SUMMARY}}": "HR software company Rippling has launched an 'AI Spend Console' after its own AI token costs hit roughly 40% of its R&D headcount budget and kept growing 80% a month. The tool tracks AI usage and cost per employee or team and actively gates spend rather than just reporting on it after the fact. It's a useful prompt for any small business now juggling a ChatGPT subscription, a quoting tool and an invoicing assistant to actually total up what all those AI tools are costing each month.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇺🇸🤖 FABRICATION · WELDING COBOTS DELIVER A 12X PRODUCTIVITY GAIN FOR STEEL FABRICATOR",
    "{{ROBOT_1_HEADLINE}}": "Data-Centre Builder Boosts Welding Output 12-Fold With a Fleet of 58 Collaborative Robots",
    "{{ROBOT_1_SUMMARY}}": "Data-centre infrastructure builder Tate has deployed a fleet of 58 Hirebotics 'Cobot Welder' systems across its Arkansas, Virginia and Kentucky facilities, lifting throughput per welder twelvefold on structural steel assembly work. Unlike the humanoid robots grabbing headlines, these are collaborative welding arms designed to work safely alongside existing crews rather than replace a whole production line. It's a real-world example of automation tackling the same skilled-labour shortage familiar to any Australian fabrication or coatings business.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/08/07/data-center-infrastructure-company-tate-boosts-welding-productivity-12-fold-with-fleet-of-58-hirebotics-cobots/103993/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Greens Threaten to Bypass Labor and Legislate Their Own Gambling Ad Crackdown",
    "{{AUS_1_SUMMARY}}": "Greens senator Sarah Hanson-Young says her party won't support the Albanese government's gambling advertising reform package as currently drafted — which would cap betting ads at three per hour on free-to-air TV between 6am and 8:30pm — and has warned the crossbench could legislate tougher rules itself in the Senate if Labor won't budge. She wants gambling inducements eliminated entirely, while leaving room to negotiate on online betting ad opt-ins.",
    "{{AUS_1_URL}}": "https://www.canberratimes.com.au/story/9326651/do-it-ourselves-ultimatum-for-labor-on-gambling-laws/",

    "{{AUS_2_HEADLINE}}": "Federal Government Launches $10 Million National Campaign to Tackle School Bullying",
    "{{AUS_2_SUMMARY}}": "The federal government launched its 'Let's Stop Bullying' campaign on Sunday, backed by $10 million split between a national advertising blitz and new resources for teachers, students and parents. It follows a review that found one in four students in Years 4 to 9 experience regular bullying, and will require all Australian schools to respond to bullying complaints within two school days and publish aligned policies by Term 1 2027.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Flood Watch Issued for North East, Gippsland and Central Victoria After Weekend Deluge",
    "{{VIC_1_SUMMARY}}": "The Bureau of Meteorology issued a Flood Watch on Sunday for parts of North East, Gippsland and Central Victoria as a vigorous rain band moved through, with an initial moderate flood warning for the King River and minor warnings for the Ovens and Goulburn Rivers. A separate severe weather warning covered damaging winds in the alpine areas over the same period — Carrum Downs itself is set for its heaviest rain today before conditions ease into a showery, cooler midweek.",

    # Science
    "{{SCI_1_FLAG}}": "☀️ ASTRONOMY · RARE TOTAL SOLAR ECLIPSE CROSSES ICELAND AND SPAIN THIS WEDNESDAY",
    "{{SCI_1_HEADLINE}}": "A Rare Total Solar Eclipse Sweeps Across Iceland and Spain This Wednesday — First Seen From Mainland Europe Since 1999",
    "{{SCI_1_SUMMARY}}": "A total solar eclipse sweeps from far-northern Siberia across the Arctic and Greenland on Wednesday before crossing western Iceland and reaching northern Spain and a sliver of Portugal near sunset, delivering up to two minutes eighteen seconds of totality. It will be the first total eclipse visible from mainland Europe since 1999, and the first seen from the Iberian Peninsula in over a century. Iceland gets a higher, clearer afternoon view, while Spain's low, sunset-angle eclipse will be more weather-dependent.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Your AI Subscriptions Are Adding Up Quietly — Here's How to Keep Tabs on Them Before They Spiral",
    "{{INSIGHT_BODY}}": "One of today's tech stories is HR software company Rippling building a whole internal tool just to track its own AI spend after costs grew 80% in a single month — a scale problem, but the underlying habit applies just as much to a small trades business. It's easy to end up paying for a ChatGPT subscription, a quoting tool with AI built in, an invoicing assistant and a scheduling app, each a modest monthly fee, without ever adding them up against what each one is actually saving in admin time. A five-minute review once a month — list every AI tool you're paying for, what it replaced, and whether you'd notice if it disappeared — is enough to catch subscriptions quietly running on autopilot long after they've stopped earning their keep.",

    # Fun facts
    "{{FACT_1}}": "The name LEGO comes from the Danish phrase \"leg godt,\" meaning \"play well\" — coined by Danish carpenter Ole Kirk Christiansen in 1934, more than two decades before the interlocking brick itself was patented.",
    "{{FACT_2}}": "Pavlova is named after Russian ballerina Anna Pavlova, whose 1926 tour is credited with inspiring the dessert — but Australia and New Zealand still argue fiercely over which country actually invented it first.",
    "{{FACT_3}}": "Backgammon is one of the oldest known board games — archaeologists found a version of it among 5,000-year-old artefacts at the Burnt City site in modern-day Iran, played long before dice games spread through the rest of the ancient world.",

    # Joke
    "{{JOKE_SETUP}}": "A tow truck driver was asked how he built such a loyal customer base.",
    "{{JOKE_PUNCHLINE}}": "He said it's simple — he always turns up before they've finished dialling the second company.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The expert in anything was once a beginner.\"",
    "{{CLOSING_ATTR}}": "— Helen Hayes",
    "{{CLOSING_MESSAGE}}": "It's a wet start to the week in Carrum Downs, with today bringing the heaviest rain before it eases into a showery, cooler run through Wednesday — a Flood Watch is current further north in Victoria's alpine and Gippsland regions, worth checking road conditions if you're travelling that way. The RBA's rate call lands tomorrow and fuel prices are still climbing as excise relief winds back, so it's a Monday worth keeping half an eye on both the bowser and the news.",
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
