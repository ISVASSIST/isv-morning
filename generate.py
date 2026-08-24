#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 25 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 25 Aug (BOM)
    "{{WEATHER_1}}": "TUE 25 · 🌧️ Partly cloudy, high chance of showers, most likely this afternoon and evening · 10–15°C",
    "{{WEATHER_2}}": "WED 26 · 🌧️ Cloudy, very high chance of rain, most likely morning and afternoon · 11–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 27 · ⛅ Partly cloudy, medium chance of a shower, most likely morning · 10–17°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 28 · ⛅ Partly cloudy, slight chance of a shower · 9–17°C",
    "{{WEATHER_5}}": "SAT 29 · ☀️ Partly cloudy, mostly dry · 8–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or Carrum Downs. A vigorous low is bringing this week's heaviest rain today into Wednesday morning, easing from Thursday — Friday and Saturday are your best windows for any outdoor coating or blasting work.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 IRAN · US LAUNCHES 'ECONOMIC D-DAY' SANCTIONS CAMPAIGN",
    "{{WORLD_1_HEADLINE}}": "US Treasury Unveils Sweeping New Iran Sanctions in What Trump Calls an 'Economic D-Day'",
    "{{WORLD_1_SUMMARY}}": "Treasury Secretary Scott Bessent unveiled a broad new sanctions campaign against Iran, dubbed \"Operation Economic Outcast,\" targeting brokers, shipping networks and shell companies across the UAE, Hong Kong, China, Singapore and Europe that move Iranian oil and revenue to the IRGC. Iran has vowed to respond \"in a seismic manner,\" another sign the standoff behind this year's oil price volatility is far from resolved.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/24/g-s1-139743/treasury-secretary-scott-bessent-to-unveil-new-economic-sanctions-on-iran",

    "{{WORLD_2_FLAG}}": "🎯 RUSSIA-UKRAINE · DRONES HIT RETAILER'S WAREHOUSES AGAIN",
    "{{WORLD_2_HEADLINE}}": "Ukrainian Drones Strike Russian Online Retailer's Warehouses for a Third Straight Night",
    "{{WORLD_2_SUMMARY}}": "Ukrainian drones killed at least ten people and hit logistics centres belonging to Russian online retailer Ozon — Russia's answer to Amazon — across southern Russia and occupied Crimea overnight, the third consecutive night the retailer's warehouses have been targeted. Ozon evacuated more than 300 staff from its largest facility in Orenburg as the campaign against Russian commercial infrastructure keeps widening.",
    "{{WORLD_2_URL}}": "https://kyivindependent.com/ukraine-strikes-wildberries-rival-in-russias-orenburg/",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL · MELBOURNE AVERAGE EASES TO $2.00 A LITRE",
    "{{ECON_1_HEADLINE}}": "Melbourne Petrol Prices Ease to $2.00 Average, 5c Cheaper Than Yesterday",
    "{{ECON_1_SUMMARY}}": "Melbourne's average unleaded price has eased to around $2.00 a litre today, 5 cents down on yesterday and 12 cents below the early-August peak of $2.12, with prices still ranging from 183.5c/L at the cheapest Preston station to over 300c/L at the priciest across the city's 1,172 stations. Tuesday to Thursday is typically the cheapest stretch of Melbourne's price cycle, so today and tomorrow are reasonable days to fill the ute before prices likely start climbing again toward the weekend.",
    "{{ECON_1_URL}}": "https://petrolmate.com.au/city/vic/melbourne",

    "{{ECON_2_FLAG}}": "📉 PROFESSIONAL SERVICES · KPMG AXES 5% OF ITS AUSTRALIAN STAFF",
    "{{ECON_2_HEADLINE}}": "KPMG Cuts 27 Partners and 360 Jobs as Audit Scandal Fallout Deepens",
    "{{ECON_2_SUMMARY}}": "KPMG's Australian arm is cutting 27 partners and around 360 jobs, mostly from its consulting division, after client contracts dried up in the wake of last year's audit leaks scandal and consulting revenue fell almost 17% for the year. A reminder that even the Big Four aren't immune to a tighter market for professional services — a decent moment to check whether your own accounting or advisory fees are still competitive.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔍 AI SEARCH · NVIDIA IN TALKS FOR $30BN+ PERPLEXITY STAKE",
    "{{TECH_1_HEADLINE}}": "Nvidia Reportedly in Talks to Back AI Search Startup Perplexity at a $30 Billion-Plus Valuation",
    "{{TECH_1_SUMMARY}}": "Nvidia is discussing a fresh funding round for AI search company Perplexity that could value it above $30 billion, more than 50% higher than a year ago, as Perplexity's annualised revenue jumps past $750 million on the back of its AI agent tools. It's the latest sign chipmakers are moving beyond just selling the hardware behind AI tools to taking direct stakes in the software layer small businesses increasingly rely on.",
    "{{TECH_1_URL}}": "https://www.benzinga.com/trading-ideas/long-ideas/26/08/61383040/nvidia-perplexity-investment-ai-strategy",

    "{{TECH_2_FLAG}}": "🔬 AI HARDWARE · PUSH FOR CHEAPER ON-DEVICE AI CHIPS",
    "{{TECH_2_HEADLINE}}": "STMicroelectronics and Singapore University Launch Four-Year Lab for Cheaper On-Device AI Chips",
    "{{TECH_2_SUMMARY}}": "STMicroelectronics and the National University of Singapore have opened a joint research lab chasing more energy-efficient semiconductors that can run AI workloads directly on a device rather than in the cloud — the kind of advance that eventually flows through to cheaper, faster AI features in everyday tools and machinery, not just server farms.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 INDUSTRIAL ROBOTS · WORLD ROBOT CONFERENCE WRAPS IN BEIJING",
    "{{ROBOT_1_HEADLINE}}": "2026 World Robot Conference Closes in Beijing With 311 New Robots Unveiled",
    "{{ROBOT_1_SUMMARY}}": "The week-long World Robot Conference wrapped up in Beijing having drawn over 300 exhibitors from 26 countries and 3,000-plus products on display, including a newly unveiled 4-metre-tall hybrid hydraulic-electric humanoid capable of handling loads from a few kilograms up to several hundred tonnes. The event's focus this year shifted noticeably from flashy demos toward real factory and logistics deployments, underscoring how fast industrial automation is moving from showcase to shop floor.",
    "{{ROBOT_1_URL}}": "https://en.people.cn/n3/2026/0823/c90000-20491301.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Renting a Unit Now Costs More Than Half Take-Home Pay in Every Australian Capital",
    "{{AUS_1_SUMMARY}}": "Housing advocacy group Everybody's Home says a single worker on the median $74,100 income now spends 56% of take-home pay renting an average capital-city apartment, with vacancy rates as low as 1.2% pushing advertised rents up almost 8% over the past year.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-24/everybodys-home-rental-increases-half-average-income/107070036",

    "{{AUS_2_HEADLINE}}": "Albanese Rules Out Any Change to WA's $47bn GST Deal Despite Call to Scrap It",
    "{{AUS_2_SUMMARY}}": "On his first WA visit since a Productivity Commission report branded the 2018 GST carve-up a \"costly mistake\" that has cost federal taxpayers almost $23 billion, the Prime Minister repeated there will be \"no change whatsoever\" to the arrangement while he remains in office.",
    "{{AUS_2_URL}}": "https://www.abc.net.au/news/2026-08-24/anthony-albanese-pledges-no-change-to-wa-gst-deal/107071388",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Doctors Warn of Possible Contaminated Batch Behind Seventh Liver Toxicity Case From Fake Weight-Loss Peptides",
    "{{VIC_1_SUMMARY}}": "Victorian doctors say a seventh patient has been hospitalised with acute liver toxicity after using a counterfeit peptide sold online as the weight-loss drug retatrutide, with the cluster's local pattern pointing to a contaminated batch rather than one-off bad luck.",

    # Science
    "{{SCI_1_FLAG}}": "😴 HEALTH SCIENCE · THE SLEEP SWEET SPOT FOR SLOWER AGING",
    "{{SCI_1_HEADLINE}}": "Scientists Pin Down the Sleep Range Linked to the Slowest Biological Aging",
    "{{SCI_1_SUMMARY}}": "A Columbia University-led analysis of 23 biological aging clocks across 17 organ systems in the UK Biobank found a clear U-shaped pattern: people sleeping between 6.4 and 7.8 hours a night aged the slowest, while both short sleep (under 6 hours) and long sleep (over 8 hours) were linked to faster aging throughout the body, not just the brain.",

    # Business insight
    "{{INSIGHT_TITLE}}": "KPMG Just Cut 5% of Its Australian Workforce — What It Means for What You Pay Your Accountant",
    "{{INSIGHT_BODY}}": "KPMG's Australian arm is axing 27 partners and around 360 jobs after a bruising year of lost contracts and a 17% slide in consulting revenue — proof that even the biggest professional services firms are under real pricing pressure right now, not just small operators. That pressure tends to flow down: as big firms compete harder to hold onto clients, mid-sized and boutique accounting and bookkeeping practices are increasingly leaning on AI-assisted tools — automated BAS prep, bank reconciliation, anomaly-flagging — to protect their own margins without lifting fees. If your bookkeeping or BAS costs haven't been reviewed in a year or two, it's a reasonable time to ask your accountant what tasks they've automated on their end, and whether that saving is actually being passed on to you.",

    # Fun facts
    "{{FACT_1}}": "Melbourne's Skipping Girl Vinegar sign in Abbotsford, first lit in 1936, is believed to be the city's first animated neon sign — when the original was pulled down in 1968, locals protested so loudly that a near-identical replica went up two years later and still runs today.",
    "{{FACT_2}}": "The jerrycan, still basically unchanged after 88 years, was engineered in 1937 by a German firm to a military brief: stamped from two pressed-steel halves with no seams, rivets or fittings that could work loose and leak, and shaped so one soldier could carry two full cans at once.",
    "{{FACT_3}}": "The Royal Game of Ur, played in Mesopotamia around 2500 BC, sat unplayed for over 4,000 years until British Museum curator Irving Finkel deciphered a 2,000-year-old clay tablet of rules in the 1980s — you can now play the exact same game your Bronze Age counterpart did.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pergola builder never argue with a customer about the quote?",
    "{{JOKE_PUNCHLINE}}": "Because he always built in a bit of shade before things got heated.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Well begun is half done.\"",
    "{{CLOSING_ATTR}}": "— Aristotle",
    "{{CLOSING_MESSAGE}}": "It's the wettest day of the week in Carrum Downs, with showers building through this afternoon and evening before Wednesday's system moves through properly — Friday and Saturday are shaping up as the better windows for anything outdoors. Between KPMG's job cuts, Melbourne's rent squeeze back in the headlines and the usual Tuesday dip in petrol prices, it's a fair day to run your own numbers as well as everyone else's.",
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
