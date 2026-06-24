#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 25 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 25 Jun
    # Winter cold snap; cloudy start with showers possible Friday, clearing for the weekend
    "{{WEATHER_1}}": "THU 25 · ☁ Cloudy · 8–12°C",
    "{{WEATHER_2}}": "FRI 26 · 🌧 Shower possible · 7–11°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 27 · 🌤 Clearing · 6–12°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SUN 28 · ⛅ Partly cloudy · 6–13°C",
    "{{WEATHER_5}}": "MON 29 · ☀ Fine · 7–14°C",
    "{{WEATHER_ALERT}}": "❄ COLD WEEK · 5 DAYS TO EOFY",

    # World
    "{{WORLD_1_FLAG}}": "🌐 MIDDLE EAST · IRAN · HORMUZ",
    "{{WORLD_1_HEADLINE}}": "Iran Closes Strait of Hormuz Again as US–Iran Nuclear Talks Enter a Critical and Fragile Phase",
    "{{WORLD_1_SUMMARY}}": "Iran's military announced it had once again closed the Strait of Hormuz, citing continued Israeli strikes in Lebanon as a violation of the terms agreed under last week's tentative ceasefire framework. The closure follows what Vice President JD Vance described as 18 hours of productive talks in Switzerland — both sides agreed a mechanism to keep the Strait open and maintain Lebanon's ceasefire, and Iran agreed to invite IAEA inspectors back into the country. But the on-again-off-again status of the world's most critical oil shipping lane underscores how fragile the framework remains. The Strait carries roughly 20% of globally traded oil and nearly 35% of the world's LNG. Every Hormuz closure ripples into global crude benchmarks within hours — and into Australian diesel prices within days. Small business owners running diesel-dependent operations are navigating both the June 30 domestic excise restoration and ongoing Middle East supply risk simultaneously.",
    "{{WORLD_1_URL}}": "https://www.cbsnews.com/live-updates/iran-us-war-trump-nuclear-sites-strait-of-hormuz/",

    "{{WORLD_2_FLAG}}": "🇬🇧 UNITED KINGDOM · LEADERSHIP",
    "{{WORLD_2_HEADLINE}}": "Keir Starmer Resigns as UK Prime Minister — Andy Burnham Widely Tipped as Successor",
    "{{WORLD_2_SUMMARY}}": "British Prime Minister Keir Starmer announced his resignation on June 22, stepping down after less than two years in office. Months of pressure from Labour MPs, catastrophic council election results in May, and the rapid surge of Nigel Farage's Reform UK eroded his authority beyond recovery. Starmer becomes the sixth UK Prime Minister to resign outside Downing Street in seven years — a striking streak of political instability in one of the world's oldest parliamentary democracies. Andy Burnham, the popular former Mayor of Greater Manchester and nicknamed the 'King of the North,' is the clear favourite to become Labour leader and the UK's seventh prime minister in a decade, with political analysts expecting a handover by mid-July.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/06/22/nx-s1-5866231/keir-starmer-resigns",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL PRICES · SMALL BUSINESS",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Cut Expires Monday June 30 — Diesel and Petrol Set to Jump ~32c/L Unless Extended",
    "{{ECON_1_SUMMARY}}": "The temporary 32 cents per litre fuel excise reduction — in effect since April 1 — expires at midnight on Monday June 30. Since it was introduced, diesel has fallen 39% and petrol 36% across Australia's five major cities; Melbourne unleaded averaged 163.9 cents per litre on June 17. The US–Iran deal signed on June 18 has helped ease global crude prices, but the domestic excise restoration will more than offset any international relief. For Carrum Downs businesses running work vehicles or diesel plant, the jump could add $50–$100 per week in fuel costs from July 1 — on top of the minimum wage increase and payday super changes landing the same day. The government has left the door open to an extension but has not committed. Five days left to update your July job pricing.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🏦 RBA · INTEREST RATES",
    "{{ECON_2_HEADLINE}}": "RBA Holds Cash Rate at 4.35% For First Time This Year — But Warns the Inflation Fight Isn't Over",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank of Australia paused its rate-hiking cycle at the June board meeting, holding the cash rate at 4.35% after three consecutive increases earlier this year. Governor Michele Bullock was explicit that the pause does not signal the end of tightening — financial markets are still pricing in roughly a one-in-two chance of a further rise before December. For small business operators with variable-rate debt or equipment finance linked to the cash rate, the hold is temporary relief but not resolution. Next RBA meeting: August 11.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🍎 APPLE · AI · SIRI OVERHAUL",
    "{{TECH_1_HEADLINE}}": "Apple Rebuilds Siri from Scratch as 'Siri AI' — Powered by Google's Gemini Through a Multi-Billion Dollar Deal",
    "{{TECH_1_SUMMARY}}": "Apple announced a complete overhaul of its voice assistant, rebranded 'Siri AI' and rebuilt from the ground up on Google's Gemini model through a landmark multi-billion dollar partnership. The redesigned assistant runs in a dedicated app, can chain context from photos, calendar, contacts, and maps into a single multi-step action — for example, finding a sunset photo, extracting its GPS coordinates, pulling a friend's address from contacts, and building a multi-stop navigation route in one request. It marks a fundamental shift from the original Siri's single-command model and the most significant AI investment Apple has made in the product's 15-year history. Practical implications for small business: voice-to-action AI on iPhones is about to get meaningfully more capable for scheduling, messaging, and on-the-go admin tasks.",
    "{{TECH_1_URL}}": "https://aistartupedge.com/latest-ai-news-june-2026/",

    "{{TECH_2_FLAG}}": "🏥 OPENAI · ENTERPRISE AI · HEALTHCARE",
    "{{TECH_2_HEADLINE}}": "AI Integration at Boston Children's Hospital Saves 60,000 Hours of Admin Time — One-Third of Staff Now Use AI Daily",
    "{{TECH_2_SUMMARY}}": "OpenAI and Boston Children's Hospital published results showing that embedding AI across clinical workflows has reclaimed more than 60,000 hours of manual administrative work, with over a third of all hospital staff now interacting with secure AI tools daily. The case is one of the most detailed documented examples of AI-driven efficiency gains in a heavily regulated industry — and the pattern translates directly to any business with repeatable paperwork processes: quoting, job notes, compliance documentation, client communications. The time savings are not theoretical. They come from systematically routing routine text-heavy tasks through AI rather than doing them manually, one document at a time.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 AUTOMATE 2026 · CHICAGO · CLOSING DAY",
    "{{ROBOT_1_HEADLINE}}": "Automate 2026 Closes in Chicago — Humanoid Robot Supply Now Outpacing Near-Term Industrial Demand",
    "{{ROBOT_1_SUMMARY}}": "The four-day Automate 2026 conference closed today in Chicago after drawing more than 50,000 attendees and 1,000 exhibitors across North America's largest automation trade show. The defining headline from closing-day analysis: humanoid robot supply is beginning to outpace near-term industrial demand in some product categories — a striking reversal from the supply-constrained environment of early 2025 when every manufacturer had waiting lists. Multiple companies are now competing for factory deployment slots rather than customers competing for robots. North American industrial robot orders remained strong at US$2.25 billion in 2025, and autonomous mobile robots are operating under commercial Robot-as-a-Service contracts at Toyota facilities in Canada. The central question coming out of the show: as supply expands faster than deployment programs can absorb, which manufacturers will win the integration process — and at what price point does humanoid automation become viable for mid-size industrial operators?",
    "{{ROBOT_1_URL}}": "https://www.marketscale.com/industries/industrial-iot/humanoid-supply-outpaces-demand-amrs-hit-toyota-plants-and-robot-orders-hold-steady-automations-defining-stories-of-mid-2026",

    # Australia
    "{{AUS_1_HEADLINE}}": "H5N1 Bird Flu Confirmed in Wild Seabird in Western Australia — Poultry Industry on High Alert",
    "{{AUS_1_SUMMARY}}": "Australia confirmed its first detection of highly pathogenic H5N1 avian influenza in a wild migratory brown skua found sick in southern Western Australia on June 14. The positive result was returned on June 20. A second seabird from the same location returned a suspect positive and is being further tested. No commercial poultry detections have been made and Australia retains its HPAI-free status for commercial birds under international standards. The Department of Agriculture has activated enhanced national biosecurity protocols, with major poultry producers including Inghams moving to a state of high biosecurity vigilance. H5N1 has spread through wild bird populations in Europe, Asia, and the Americas — Australia's isolation has provided protection but the detection signals the virus has crossed into our migratory bird population.",
    "{{AUS_1_URL}}": "https://thenightly.com.au/australia/h5n1-bird-flu-detected-in-western-australia-as-poultry-producers-boost-biosecurity-measures-c-22469289",

    "{{AUS_2_HEADLINE}}": "Socceroos Face Paraguay Tomorrow at Noon AEST — World Cup Last-16 Berth on the Line",
    "{{AUS_2_SUMMARY}}": "Australia meet Paraguay in their final Group D match of the 2026 FIFA World Cup on Friday June 26 at 12pm AEST at Levi's Stadium in Santa Clara, California. A win or draw sends the Socceroos through to the Round of 32. Australia sit second in Group D on three points — level with Paraguay but ahead on goal difference — after beating Türkiye 2–0 and losing 2–0 to the USA. The match is broadcast live and free on SBS and SBS On Demand. Melbourne live sites at Federation Square and AAMI Park will open for fans at midday.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne's World Cup Live Sites Ready at Federation Square and AAMI Park for Tomorrow's Socceroos Decider",
    "{{VIC_1_SUMMARY}}": "Federation Square and AAMI Park will host free public live sites for tomorrow's Socceroos vs Paraguay World Cup match at noon AEST — confirmed after Premier Jacinta Allan intervened to ensure the city had an official fan hub for the tournament. Security screening will be in place. The Valley Sounds music festival also launches tonight across Moonee Valley venues, running through to July 5. At the NGV, the landmark Cartier jewellery exhibition continues through October — Melbourne is one of the few cities outside Europe to host the full collection.",

    # Science
    "{{SCI_1_FLAG}}": "🌌 NASA · JWST · INTERSTELLAR VISITOR",
    "{{SCI_1_HEADLINE}}": "JWST Finds Interstellar Comet 3I/ATLAS May Be Almost as Old as the Universe — Chemistry Unlike Anything in Our Solar System",
    "{{SCI_1_SUMMARY}}": "NASA's James Webb Space Telescope has taken the first mid-infrared chemical fingerprint of interstellar comet 3I/ATLAS — the third confirmed interstellar object ever detected — and the results are extraordinary. Webb found unexpectedly high levels of methane relative to water: a ratio seen in no solar system comet and very few analogues anywhere in our known cosmic neighbourhood. Using carbon isotope ratios to estimate age, researchers believe the comet may be approximately 12 billion years old — nearly as ancient as the universe itself (13.8 billion years), and formed in a star system that almost certainly no longer exists. The comet is currently moving away from the Sun after its closest approach, carrying chemistry from the early universe through our solar system and continuing outward to wherever it came from.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Find the Margin Leaks in Your FY2026 Jobs Before the Books Close",
    "{{INSIGHT_BODY}}": "With five days left in the financial year, most trades business owners are focused on getting invoices out and keeping the ATO paperwork in order. But there is a faster win that fewer take: using AI to audit the actual margin on your completed jobs — not the quoted margin, but what you really made. Take any three jobs you finished this year and ask Claude or a similar AI tool to compare hours booked versus hours quoted, materials cost versus estimated, and any variations that were never charged. Ask it to find the pattern: which job types consistently underperform, which clients generate variation requests that erode margin without a cost conversation, and which categories of work take longer than quoted every single time. This is the kind of analysis that once required a bookkeeper and two hours with a spreadsheet. It now takes about fifteen minutes. The insight it surfaces does more than close the year cleaner — it directly informs your FY2027 rate card. If your preparation or inspection work consistently runs 20% over on labour, your new rates should reflect that before the first quote goes out in July. AI cannot recover the margin from jobs already done. But it can make sure the next ones are priced to protect it — and right now, before the financial year closes, is exactly the right moment to look.",

    # Fun Facts
    "{{FACT_1}}": "The Welcome Stranger — found just 3 centimetres below the surface at Moliagul in central Victoria on 5 February 1869 by miners John Deason and Richard Oates — is the largest alluvial gold nugget ever discovered, yielding approximately 70.5 kilograms of fine gold from a gross mass of around 100 kilograms including host quartz. It was so large it had to be broken into three pieces to fit in the assay office balance scales at Dunolly. The Welcome Stranger is one of two record-breaking gold nuggets found in Victoria's goldfields; the Welcome Stranger remains the world alluvial record and the state has never publicly disclosed where the host site actually was.",

    "{{FACT_2}}": "Salting pasta water does almost nothing to raise its boiling point — you would need roughly 58 grams of salt per litre to raise the temperature by just 1°C, far more salt than any recipe calls for. The real purpose of salted water is flavour: as pasta cooks, it absorbs water, and that water seasons the pasta from the inside. Professional cooks aim for water that tastes pleasantly salty — around 10 grams per litre — because it's the only window to season pasta through its entire thickness rather than just coating the outside with sauce.",

    "{{FACT_3}}": "The tradition of hiding 'Easter eggs' — secret messages or features — in software was popularised by programmer Warren Robinett in the 1979 Atari 2600 game Adventure. Atari's policy denied programmers public credit for their work; Robinett's response was to hide a room accessible only through an obscure sequence of actions that displayed the words 'Created by Warren Robinett.' Management only discovered it after he had already left the company. The tradition has continued for over 40 years: Google's search results, Microsoft Office, and dozens of video game series all contain hidden developer messages traceable to that one invisible room in Adventure.",

    # Joke
    "{{JOKE_SETUP}}": "What do the Socceroos and a small trades business owner have in common this week?",
    "{{JOKE_PUNCHLINE}}": "Both need one good result tomorrow and their finances sorted before Monday — or it's extra time with the accountant.",

    # Closing
    "{{CLOSING_QUOTE}}": "“You can’t go back and change the beginning, but you can start where you are and change the ending.”",
    "{{CLOSING_ATTR}}": "— C. S. Lewis",
    "{{CLOSING_MESSAGE}}": "Cold and cloudy this Thursday in Carrum Downs — 12°C with the chance of a shower through the morning, clearing into the afternoon. Tomorrow the Socceroos face Paraguay at noon on SBS with a World Cup last-16 spot on the line — worth having the radio on-site. Monday is June 30: end of financial year and the last day of the fuel excise cut. If your July job rates haven't been updated to account for the diesel price bounce, today is a good day to fix that. In the UK, Keir Starmer this week became the sixth British PM to resign in seven years — a streak that says something about the pace of change in politics right now. The science story worth pausing on: JWST detected chemistry on an interstellar comet that researchers believe formed 12 billion years ago, in a star system that almost certainly no longer exists. It passed through our solar system and is heading back out. Some things are worth slowing down for. Have a productive Thursday, Liall.",
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
