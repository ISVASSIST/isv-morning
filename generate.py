#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 20 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 20 May (BOM forecast)
    "{{WEATHER_1}}": "WED 20 · 🌧 Showers · 14°C",
    "{{WEATHER_2}}": "THU 21 · ⛅ Clearing · 15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 22 · ⛅ Partly cloudy · 16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 23 · ☁ Mostly cloudy · 17°C",
    "{{WEATHER_5}}": "SUN 24 · ⛅ Mild · 17°C",
    "{{WEATHER_ALERT}}": "☔ SHOWERS TODAY",

    # World
    "{{WORLD_1_FLAG}}": "🌍 US–IRAN",
    "{{WORLD_1_HEADLINE}}": "Trump Was 'An Hour Away' From Striking Iran — Gulf Leaders Called It Off With 48 Hours to Spare",
    "{{WORLD_1_SUMMARY}}": "President Trump announced Monday that he called off a planned military strike on Iran after receiving direct appeals from the leaders of Saudi Arabia, the UAE, and Qatar — who said active negotiations were underway and could produce a deal 'very acceptable' to all sides. Trump confirmed he had been 'an hour away' from launching the attack when he agreed to the pause, giving Iran 'two or three days' to reach an agreement or face a full-scale assault. Oil markets swung sharply on the news. The standoff is the most acute military flashpoint in the region since the war began — and every movement in oil futures flows directly into Australian fuel prices within days.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/05/19/g-s1-122762/trump-says-hes-called-off-iran-strike",

    "{{WORLD_2_FLAG}}": "🇺🇸 USA",
    "{{WORLD_2_HEADLINE}}": "Three Killed in Hate-Crime Attack on San Diego Mosque — Two Teen Suspects Found Dead",
    "{{WORLD_2_SUMMARY}}": "Three people were killed on Sunday in a targeted attack at the Islamic Center of San Diego — the city's largest mosque. The victims included security guard Amin Abdullah, described by police as a hero who saved additional lives, and two staff members. Two teen suspects were found dead in a nearby car from self-inflicted gunshot wounds. Hate speech was scrawled on a recovered weapon and a suicide note expressing racial pride was found. Authorities are treating the attack as a hate crime. It is the deadliest mosque attack in US history.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/5/18/san-diego-police-say-responding-to-an-active-shooter-at-islamic-center",

    # Economics
    "{{ECON_1_FLAG}}": "📉 INFLATION",
    "{{ECON_1_HEADLINE}}": "Australia's Inflation Cools to 4.3% — First Clear Sign the Fuel Price Surge Is Peaking",
    "{{ECON_1_SUMMARY}}": "Australia's annual inflation rate eased to 4.3% in the 12 months to May 2026, down from 4.6% in March — the first back-to-back monthly cooling since the global energy shock began. Fuel's contribution to inflation dropped from 8.9% year-on-year in March to 6.8% in May, reflecting some stabilisation in global oil markets and the current 32¢/litre federal excise cut. For small business operators watching margins, this is cautiously good news — though the excise cut expires June 30 and the Iran standoff is keeping wholesale crude prices volatile. The RBA cash rate remains at 4.35% as the Board monitors whether the cooling holds.",
    "{{ECON_1_URL}}": "https://www.ibtimes.com.au/australia-inflation-eases-slightly-43-may-2026-fuel-pressures-begin-moderate-1868689",

    "{{ECON_2_FLAG}}": "💼 WAGES",
    "{{ECON_2_HEADLINE}}": "Fair Work Wage Review Decision Due in Weeks — 3–4% Rise Expected for Award Workers From July 1",
    "{{ECON_2_SUMMARY}}": "The Fair Work Commission's annual wage review is entering its final phase, with a decision expected in the first or second week of June 2026, taking effect from the first full pay period on or after July 1. Based on current economic data and recent decision history, most analysts forecast an increase of 3–4% to the National Minimum Wage (currently $24.95/hr) and all modern award rates. For trades businesses with casuals, apprentices, or staff on award rates, this means a material jump in your labour cost from mid-July — one that needs to be factored into quotes you're writing this week.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔵 GOOGLE I/O",
    "{{TECH_1_HEADLINE}}": "Google Unveils Gemini Spark — A Personal AI Agent That Takes Action Across Your Apps",
    "{{TECH_1_SUMMARY}}": "At Google I/O 2026 on Tuesday, Google unveiled Gemini Spark — a new general-purpose AI agent embedded in the Gemini app that doesn't just answer questions but actively takes action across your connected apps 'on your behalf, while under your direction.' Spark can reason across Gmail, Calendar, Drive, Maps, and third-party apps, draft replies, book appointments, and manage tasks autonomously. Google also announced Gemini 3.5 Flash, priced at roughly one-third of comparable frontier models. For small business operators, this is the clearest signal yet that AI is moving from a typing assistant to an active business partner — one that can manage your admin while you're on the tools.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/05/19/google-ai-ultra-gemini-spark-omni.html",

    "{{TECH_2_FLAG}}": "💰 AI FUNDING",
    "{{TECH_2_HEADLINE}}": "Anthropic Closing $30 Billion Round at $900 Billion+ Valuation — Would Overtake OpenAI as Most Valuable Private AI Company",
    "{{TECH_2_SUMMARY}}": "Bloomberg reports that Anthropic's $30 billion fundraising round — led by Dragoneer, Sequoia Capital, Greenoaks, and Altimeter Capital — is expected to close by end of May 2026 at a valuation exceeding $900 billion, which would overtake OpenAI's March valuation of $852 billion. Anthropic's annualised revenue has surged from $9 billion at end-2025 to over $44 billion by May 2026. For context: this valuation is larger than the entire ASX top 20 combined. The AI investment wave is not a bubble narrative — the revenue growth is real and accelerating at a pace few technology businesses in history have matched.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇦🇹 EUROPE",
    "{{ROBOT_1_HEADLINE}}": "Hexagon AEON Humanoid Begins Live Factory Deployment in Austria — Schaeffler Signs Fleet Deal",
    "{{ROBOT_1_SUMMARY}}": "Hexagon Robotics' AEON humanoid robot has entered active deployment at Fill Maschinenbau's advanced manufacturing facility in Gurten, Austria — handling machine tending, inspection, and data capture within live production workflows. The pilot is one of the first genuine factory-floor humanoid deployments in the European engineering sector. In a separate announcement, global precision manufacturer Schaeffler committed to deploying a fleet of AEON humanoids across its global factory network. The pace of humanoid factory adoption in Europe has accelerated markedly: two major industrial firms have signed AEON commitments in the same fortnight.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/05/15/hexagon-and-fill-maschinenbau-partner-to-advance-manufacturing-autonomy-using-humanoids/101578/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Queensland Flooding Kills Woman, Dozens of Teenagers Rescued as Storms Sweep Southeast",
    "{{AUS_1_SUMMARY}}": "A woman was killed and dozens of teenagers were rescued after severe flash flooding struck southeast Queensland on Monday, inundating roads and overwhelming emergency services. Dozens of school students were among those stranded and required emergency evacuation. The Bureau of Meteorology warned further rainfall was likely across southeastern Queensland through midweek. For trades businesses, flood events like this consistently drive elevated demand for flood remediation, drainage work, waterproofing, and protective coatings in the weeks and months that follow.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news",

    "{{AUS_2_HEADLINE}}": "$20K Instant Asset Write-Off Now Permanent — Budget's Biggest Gift to Small Business Takes Effect July 1",
    "{{AUS_2_SUMMARY}}": "The 2026-27 Federal Budget has permanently extended the $20,000 instant asset write-off for small businesses with annual turnover up to $10 million — removing the annual uncertainty that previously forced businesses to time equipment purchases before sunset clauses expired. From July 1, eligible tools, equipment, and assets can be written off in the year of purchase. For trades businesses considering plant, machinery, or vehicles before end of FY2026, there is now a clear tax planning window open between now and June 30 — and the write-off won't disappear in 2027 even if you miss it this year.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Rent Controls Bill in Parliament — First CPI-Linked Cap Could Reshape Melbourne's Investment Property Market",
    "{{VIC_1_SUMMARY}}": "The Allan Government's Rent Controls Bill, introduced in April 2026, is currently before the Victorian Parliament and proposes capping annual rent increases at CPI — which would make Victoria the first Australian state to impose legislated rent controls in the modern era. Landlord and property industry groups warn it will reduce rental supply further at the worst possible time. The bill follows broader Victorian rental reforms that took effect in late 2025, banning no-fault evictions and rental bidding. The outcome will materially affect Melbourne's residential property market dynamics and the investment appetite that underpins renovation and maintenance work across the south-east.",

    # Science
    "{{SCI_1_FLAG}}": "🌊 CLIMATE",
    "{{SCI_1_HEADLINE}}": "Antarctica's Hektoria Glacier Retreated 24 Kilometres in 15 Months — Fastest Grounded Ice Loss Ever Recorded",
    "{{SCI_1_SUMMARY}}": "Scientists have confirmed that Antarctica's Hektoria Glacier set a modern record for grounded ice loss, retreating approximately 24 kilometres in just 15 months — a pace that stunned glaciologists worldwide. The collapse was driven by 'buoyancy-driven calving,' where warming seawater infiltrates beneath the glacier at high tide and intermittently lifts large sections of ice off the bedrock, causing them to break away at once. While Hektoria is relatively small, researchers warn that the same mechanism could trigger far more catastrophic losses in Antarctica's vastly larger glaciers — with serious long-term consequences for global sea level rise projections. Published in ScienceDaily, May 18, 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Getting Ahead of July's Wage Rise: Why the Next Six Weeks Are Critical for Your Job Pricing",
    "{{INSIGHT_BODY}}": "The Fair Work Commission's annual wage review decision is landing in the first or second week of June, with the increase taking effect from the first full pay period after July 1. Most analysts are forecasting a 3–4% rise. For a small trades business employing three or four workers on award or close-to-award rates, that is hundreds of dollars a week added to your labour cost — and it hits immediately on every job running through July. The problem isn't the rise itself; it's the quotes you're writing right now. If you're pricing three-week projects that run into July without adjusting your labour rate, you're locking in a margin hit before the decision is even handed down. AI tools make this easy: pull your last 20 quotes, run your current labour cost assumptions through a simple model, and test what a 3.5% increase does to your margin across each job type. You can do this in an afternoon with ChatGPT or Claude — no accountant required. Build the new rate into your quoting template now, and when the decision lands in June you're already pricing correctly. The businesses that won't act are the ones writing quotes this week on last year's numbers.",

    # Fun Facts
    "{{FACT_1}}": "The blue whale's heart weighs approximately 180 kilograms — roughly the size of a small car — and beats just 4 to 8 times per minute when the animal is diving deep. Its main aorta is wide enough for a small child to crawl through. Despite powering the largest animal ever known to have existed, the blue whale's lifespan of 80 to 90 years is comparable to that of a human.",

    "{{FACT_2}}": "Saffron is the world's most expensive spice by weight — typically $5,000 to $10,000 per kilogram depending on grade and origin. The price comes from the harvest: each Crocus sativus flower produces only three red stigmas, and a single kilogram of dried saffron requires between 150,000 and 200,000 flowers, all of which must be picked by hand at dawn during a brief autumn window of just two to three weeks per year.",

    "{{FACT_3}}": "Epoxy adhesive was developed almost simultaneously and independently by chemists at Shell Development Company in the United States and Ciba in Switzerland in the mid-1940s — both reached the same solution without knowing about each other. The two-part resin system was commercially introduced in 1947. Today, over 800,000 tonnes of epoxy resin are consumed globally every year, used in everything from industrial coatings and concrete flooring to aircraft construction and printed circuit boards.",

    # Joke
    "{{JOKE_SETUP}}": "Why do fencing contractors make the best negotiators?",
    "{{JOKE_PUNCHLINE}}": "They've spent their whole career working with people who can never agree on where the boundary is.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Perfect is the enemy of good.\"",
    "{{CLOSING_ATTR}}": "— Voltaire",
    "{{CLOSING_MESSAGE}}": "It's a wet Wednesday morning in Carrum Downs, with showers likely through the day before things start to clear toward Thursday. The big story overnight was Iran: Trump confirmed he was an hour away from launching strikes before Gulf leaders stepped in and bought 48–72 hours of tense diplomacy — oil markets are watching every word, and your diesel costs this week reflect that. Closer to home, the wage review clock is ticking toward a June decision, and if you haven't modelled what a 3–4% labour cost rise does to your July pricing, this morning's a good time to run those numbers. Stay dry, Liall.",
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
