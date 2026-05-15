#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 16 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 16 May
    "{{WEATHER_1}}": "SAT 16 · ☀️ 22°C",
    "{{WEATHER_2}}": "SUN 17 · ⛅ 19°C · 40%",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 18 · 🌧️ 13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 19 · 🌦️ 15°C",
    "{{WEATHER_5}}": "WED 20 · ⛅ 17°C",
    "{{WEATHER_ALERT}}": "COOL CHANGE SUNDAY",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸🇨🇳 US–CHINA",
    "{{WORLD_1_HEADLINE}}": "Trump Departs Beijing After Summit — US Touts Trade Deals, China Issues Taiwan Warning",
    "{{WORLD_1_SUMMARY}}": "President Trump concluded his two-day Beijing summit with Xi Jinping on Friday, claiming 'fantastic trade deals' including Chinese pledges to buy American oil and 200 Boeing aircraft. China's account diverged sharply — Beijing said it delivered firm warnings over US arms sales to Taiwan and disputed that binding trade agreements were signed. Both sides agreed to a framework of 'strategic stability' for the next three years and exchanged invitations for future meetings, with Xi invited to Washington in September.",
    "{{WORLD_1_URL}}": "https://www.cnbc.com/2026/05/15/trump-wraps-up-two-day-china-trip-invites-xi-for-a-september-visit.html",

    "{{WORLD_2_FLAG}}": "🎵 EUROPE",
    "{{WORLD_2_HEADLINE}}": "Eurovision Grand Final Is Tonight — Five Nations Have Walked Out in History's Biggest Boycott",
    "{{WORLD_2_SUMMARY}}": "Tonight's Eurovision Song Contest grand final in Vienna proceeds despite the contest's largest boycott: Spain, Ireland, Slovenia, the Netherlands and Iceland have all withdrawn over Israel's continued participation amid the Gaza war. Sponsorships were pulled, protests erupted outside the venue, and Switzerland's 2024 winner returned their trophy to the EBU in protest. The EBU has capped public votes at 10 per person in response to past allegations of Israeli government vote-buying campaigns.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/05/15/entertainment/eurovision-final-israel-boycott-intl",

    # Economics
    "{{ECON_1_FLAG}}": "🏘️ HOUSING",
    "{{ECON_1_HEADLINE}}": "Coalition Ties Migration Intake to Housing Supply — A Policy Shift With Real Consequences for Trades",
    "{{ECON_1_SUMMARY}}": "In Thursday's federal budget reply, Opposition Leader Angus Taylor proposed capping net overseas migration at the number of new homes built annually — roughly 175,000. The policy mirrors One Nation's platform, following last week's Farrer by-election loss, and signals a major shift in Coalition thinking. For trades businesses, the proposal cuts two ways: lower migration may tighten an already thin skilled labour pool, while any easing of population growth could soften the construction project pipeline over the medium term.",
    "{{ECON_1_URL}}": "https://www.thenewdaily.com.au/news/politics/australian-politics/2026/05/14/coalition-budget-reply",

    "{{ECON_2_FLAG}}": "⛽ FUEL",
    "{{ECON_2_HEADLINE}}": "Diesel Down 25% From April Peak — But Small Businesses Warned Government Excise Cut Expires June 30",
    "{{ECON_2_SUMMARY}}": "Australian retail diesel prices have fallen roughly 25% and petrol around 30% from their April highs, according to ACCC weekly monitoring data, providing significant relief to fleet-heavy trades operations. However, the government's 26-cent fuel excise reduction — introduced on 1 April — is set to expire on 30 June. Industry groups are urging small business owners to plan now for a potential pump price rebound from July 1, particularly for operations running multiple vehicles or plant equipment daily.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💰 AI INVESTMENT",
    "{{TECH_1_HEADLINE}}": "Global AI Investment Hits $297 Billion — Enterprises Abandon Pilots for Full-Scale Deployment",
    "{{TECH_1_SUMMARY}}": "A BCC Research report published 14 May reveals global venture funding in AI surged to $297 billion, with enterprise organisations abandoning cautious pilot programs for company-wide AI deployment. Spending is near-doubling year-on-year as Fortune 500 companies embed AI across manufacturing, logistics, finance and supply chains. The report marks a decisive shift: AI adoption is now driven by documented operational savings, not competitive curiosity — and the gap between early adopters and laggards is widening fast.",
    "{{TECH_1_URL}}": "https://www.globenewswire.com/news-release/2026/05/14/3295186/0/en/AI-Technology-Investment-Surges-to-297-Billion-Globally-as-Enterprise-Deployment-Accelerates-Toward-Production-Scale.html",

    "{{TECH_2_FLAG}}": "🇨🇳 AI",
    "{{TECH_2_HEADLINE}}": "Four Chinese AI Labs Drop Frontier Coding Models Simultaneously — at One-Third of Western Prices",
    "{{TECH_2_SUMMARY}}": "Z.ai, MiniMax, Moonshot and DeepSeek have released open-weights AI coding models in the same week, each matching the capability ceiling of leading Western competitors while costing under one-third the inference price. The coordinated releases intensify competitive pressure across the global AI industry and signal that capable AI tools are getting dramatically cheaper — relevant for any small business evaluating AI software platforms or considering custom workflow automation.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 INDUSTRY",
    "{{ROBOT_1_HEADLINE}}": "Intelligent Automation Hits a Structural Tipping Point — AI Cobots Record 13% Growth as Market Heads to $172B",
    "{{ROBOT_1_SUMMARY}}": "A market analysis published 15 May by RoboticsTomorrow confirms AI-powered collaborative robots — designed to work alongside humans without safety cages — are recording 12.92% annual growth as manufacturers shift from fixed to flexible automation cells. Material handling and packaging now account for 31% of all robot deployments globally. The industrial robotics market is projected to reach $172 billion by 2032 — more than doubling — with Asia-Pacific contributing 44% of current revenue and the Middle East recording the fastest regional growth at 12.22% CAGR.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/05/15/industrial-robotics-market-report-why-intelligent-automation-is-redefining-global-manufacturing/26572/",

    # Australia
    "{{AUS_1_HEADLINE}}": "One Nation Eyes Victoria After Farrer Win — Party Plans Up to 20 Federal Lower-House Contests",
    "{{AUS_1_SUMMARY}}": "Buoyed by its historic Farrer by-election win — the party's first-ever lower house seat — One Nation has signalled plans to contest up to 20 federal seats at the next election, with outer-suburban Melbourne and regional Victoria firmly in its sights. Political analysts describe it as the most significant realignment in Australian federal politics since Palmer United in 2013, with implications for Coalition and Labor both in marginal electorates across the south-east.",
    "{{AUS_1_URL}}": "https://theconversation.com/with-wind-in-its-sails-one-nation-looks-to-replicate-farrer-success-in-victoria-and-federally-282477",

    "{{AUS_2_HEADLINE}}": "Canberra Quietly Welcomes Trump-Xi Hormuz Commitment as Australian Fuel Supply Chain Risk Eases",
    "{{AUS_2_SUMMARY}}": "The agreement between Trump and Xi that the Strait of Hormuz must remain open to international energy shipping was received cautiously but positively in Canberra. Australia imports a significant share of its refined fuel via Persian Gulf routes, and April's supply disruption — which drove diesel shortages and price spikes — placed energy security high on the domestic policy agenda. If the Hormuz commitment holds, analysts say it offers a path toward longer-term fuel price stability for trade-intensive industries.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Design Week Is On This Weekend — 400+ Events Across the City Through 24 May",
    "{{VIC_1_SUMMARY}}": "Australia's biggest annual design festival is mid-run this weekend, with Melbourne Design Week events spread across NGV, Craft Victoria, and dozens of independent venues. This year marks its tenth edition — themed 'Design the world you want' — with keynote talks from US architect Tom Kundig and interior designer Mary Featherston. Entry is free to the majority of events, with ticketed sessions at select venues. Program runs daily through Sunday 24 May.",

    # Science
    "{{SCI_1_FLAG}}": "🦕 PALAEONTOLOGY",
    "{{SCI_1_HEADLINE}}": "Original Organic Molecules Found in 66-Million-Year-Old Dinosaur Fossil — Challenging a Core Assumption of Palaeontology",
    "{{SCI_1_SUMMARY}}": "Scientists have found compelling evidence of original organic molecules — including collagen protein fragments — preserved inside a 66-million-year-old Edmontosaurus fossil from South Dakota. Published this week, the study used mass spectrometry, protein sequencing and microscopy together to rule out contamination. If confirmed, it overturns the long-held assumption that fossilisation destroys all organic material, opening a molecular window into extinct species that could reveal evolutionary relationships, physiology and even disease patterns across tens of millions of years.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI Tender Tools Are Helping Small Trades Win Bigger Contracts — Without Hiring a Contracts Manager",
    "{{INSIGHT_BODY}}": "Writing a competitive tender response used to cost a small operator days of work — capability statements, methodology sections, safe work plans and pricing schedules all assembled from scratch for every new opportunity. AI tools now let tradespeople generate professional tender documents in hours by drawing on past job data, compliance templates and industry pricing benchmarks. For a business bidding on industrial or government maintenance contracts, that is a genuine competitive edge. Winning tenders are not always the cheapest — they are the most credible, and AI helps small operators look as professional as large players without dedicated contract staff. Start with one section: ask an AI tool to draft your capability statement from three recent job descriptions, review it once, and save it as a reusable template you sharpen with every submission.",

    # Fun Facts
    "{{FACT_1}}": "The Eiffel Tower grows approximately 15 centimetres taller each summer due to thermal expansion of its iron structure — and contracts back in winter. The same physics governs every steel bridge, pipeline and industrial structure on Earth. Engineers must account for it through expansion joints and flexible connections, otherwise the cumulative force would eventually buckle the structure. It is one reason why expansion joints, flexible pipe couplings and protective coatings on structural steel all require regular inspection and maintenance.",
    "{{FACT_2}}": "A tardigrade — also called a water bear — is a microscopic eight-legged animal less than one millimetre long that can survive temperatures from −272°C to +150°C, radiation doses 1,000 times the lethal threshold for humans, and the vacuum of outer space. It achieves this through cryptobiosis: suspending all biological processes until conditions improve, drying itself to less than 3% water content. Tardigrades have existed on Earth for at least 530 million years — surviving every mass extinction event in the fossil record.",
    "{{FACT_3}}": "The first mobile phone call in history was made on 3 April 1973 by Motorola engineer Martin Cooper, who immediately rang a rival at Bell Labs to tell him he was calling from a handheld mobile. The device weighed 1.1 kilograms, the battery lasted 20 minutes, and it took 10 hours to recharge. It was another 11 years before the first commercial mobile phones went on sale to consumers — in 1984.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the forklift operator win employee of the month three times running?",
    "{{JOKE_PUNCHLINE}}": "He kept raising the bar.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The best way to predict the future is to create it.\"",
    "{{CLOSING_ATTR}}": "Peter Drucker",
    "{{CLOSING_MESSAGE}}": "Saturday morning in Carrum Downs — sunny and 22°C today before Sunday's cool change arrives. Melbourne Design Week is on across the city if you're looking for something to do, and Eurovision's grand final is tonight if you're keen to watch history get made (or argued about). Inflation is finally easing, the Trump-Xi summit has wrapped, and the week's news is done. Make the most of the last warm day before the rain rolls in Monday. Have a good weekend, Liall.",
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
