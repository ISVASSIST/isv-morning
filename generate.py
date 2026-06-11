#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 12 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 12 Jun
    # Cold front delivering rain today, showers Saturday, clearing Sunday onward
    "{{WEATHER_1}}": "FRI 12 · 🌧 Rain · 13–16°C",
    "{{WEATHER_2}}": "SAT 13 · 🌧 Showers · 9–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 14 · ⛅ Partly Cloudy · 8–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 15 · ☁ Cloudy · 9–14°C",
    "{{WEATHER_5}}": "TUE 16 · ☁ Cloudy · 8–13°C",
    "{{WEATHER_ALERT}}": "🛢️ FUEL EXCISE ENDS 30 JUNE — 18 DAYS TO THE PUMP PRICE JUMP",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸 USA · MIDDLE EAST",
    "{{WORLD_1_HEADLINE}}": "Trump Cancels Iran Strikes and Claims a Deal Is 'Approved' — But Tehran Has Not Confirmed Any Agreement",
    "{{WORLD_1_SUMMARY}}": "President Trump reversed course on June 11, cancelling planned US strikes on Iran and posting that Tehran had 'approved' a ceasefire framework that would reopen the Strait of Hormuz and begin 60 days of nuclear negotiations. Iran's state news agency denied any agreement had been finalised, though officials said talks were ongoing via Qatari mediation. The reversal came hours after Trump vowed to hit Iran 'VERY HARD.' Previous ceasefire signals in this conflict have not held. For Australian businesses, even a rumoured deal is worth watching: every development in the Hormuz standoff flows directly through to crude oil prices and arrives at the bowser within 2–3 weeks.",
    "{{WORLD_1_URL}}": "https://www.nbcnews.com/world/iran/live-blog/live-updates-us-strikes-iran-trump-hormuz-closed-rcna349554",

    "{{WORLD_2_FLAG}}": "🚀 SPACEX · NASDAQ",
    "{{WORLD_2_HEADLINE}}": "SPCX Opens on Nasdaq This Morning — SpaceX Begins Trading as History's Most Valuable IPO",
    "{{WORLD_2_SUMMARY}}": "After pricing at $135 per share Thursday night, SpaceX (SPCX) opens for its first day of trading on the Nasdaq this morning at a $1.75 trillion valuation — the largest IPO in US and global market history, more than triple the previous record. The company reported $15.2 billion in revenue in 2025, primarily from Starlink and launch services. Elon Musk retains roughly 82% of post-listing voting control. Also this week: Anthropic filed a confidential S-1 on June 1 at $965 billion, and OpenAI filed on June 8 at $852 billion. Three of the world's most valuable technology companies are heading to public markets at the same time — the AI era is now a publicly listed industry.",
    "{{WORLD_2_URL}}": "https://www.tradingkey.com/analysis/stocks/us-stocks/261904604-spacex-ipo-spcx-date-set-for-june-12-175-trillion-valuation-tradingkey",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 FUEL COSTS · JUNE 30",
    "{{ECON_1_HEADLINE}}": "Australia's Fuel Excise Cut Expires June 30 — 18 Days Before Pump Prices Rise by 29 Cents Per Litre",
    "{{ECON_1_SUMMARY}}": "The three-month halving of Australia's fuel excise — in place since April 1 — expires at 11:59pm on June 30, 2026. From July 1, the excise reverts from 26.3c/L to the full indexed rate of approximately 52.6c/L. Including GST, that's a real-world pump price increase of around 28–29 cents per litre overnight. For a trades business running two diesel vehicles doing 400–500 kilometres a week, that's an extra $150–200 per week in operating costs — on top of the Middle East risk premium already embedded in crude. Any fleet fuel card arrangements, job cost models, or day rates based on current bowser prices need revisiting before June 30.",
    "{{ECON_1_URL}}": "https://fairworkmate.com.au/blog/fuel-excise-cut-ends-30-june-2026-what-happens-next",

    "{{ECON_2_FLAG}}": "📊 ABS · SMALL BUSINESS",
    "{{ECON_2_HEADLINE}}": "ABS Survey: 72% of Australian Businesses Reporting Negative Impact From Fuel Costs as Hormuz War Disrupts Supply Chains",
    "{{ECON_2_SUMMARY}}": "A special ABS Business Conditions and Sentiments survey — the first since June 2022, commissioned specifically in response to the Middle East conflict — found three in four Australian businesses report fuel prices or availability are harming their operations. One in six report active supply chain disruptions from the Strait of Hormuz closure. For trades businesses, the pressure arrives from both ends: vehicle and equipment fuel, and the supply chains that move materials to site. With the excise cut expiring in 18 days and the conflict unresolved, conditions are set to tighten further before they ease.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · IPO MARKETS",
    "{{TECH_1_HEADLINE}}": "OpenAI Files Confidential IPO S-1 — Anthropic and OpenAI Both Heading to Public Markets as the AI Era Goes Listed",
    "{{TECH_1_SUMMARY}}": "OpenAI submitted its confidential S-1 prospectus to the SEC on June 8, targeting a Nasdaq listing by December 2026 at approximately $852 billion. It comes one week after Anthropic filed its own confidential S-1 at $965 billion. Combined with SpaceX opening on Nasdaq today, three of the most valuable technology companies on Earth are entering public markets simultaneously. Public investors will be able to compare two frontier AI labs' actual financials side by side for the first time — validating or challenging the AI valuations that private markets have been operating on. OpenAI reported roughly $2 billion per month in revenue as of early 2026, primarily from ChatGPT subscriptions and API usage.",
    "{{TECH_1_URL}}": "https://fortune.com/2026/06/09/openai-files-confidential-s-1-sec-ipo/",

    "{{TECH_2_FLAG}}": "💼 AI · ENTERPRISE",
    "{{TECH_2_HEADLINE}}": "OpenAI Enterprise Models Now Available Through Oracle Cloud — AI Enters the Business Infrastructure Layer",
    "{{TECH_2_SUMMARY}}": "OpenAI announced on June 11 that enterprise customers can now access its frontier AI models and Codex through existing Oracle Universal Credits — meaning companies already on Oracle Cloud Infrastructure can deploy OpenAI tools without a separate procurement process. The partnership reflects a broader shift: AI capabilities are being embedded directly into the business software platforms organisations already run on. For small and mid-size businesses, this signals that practical AI access will increasingly arrive bundled with existing tools rather than as separate standalone subscriptions.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 HUMANOID · FACILITY MANAGEMENT",
    "{{ROBOT_1_HEADLINE}}": "Unitree G1 Humanoid Robots Deployed in Commercial Facility Management — Cleaning and Maintenance Roles Automated Across Malls and Hotels",
    "{{ROBOT_1_SUMMARY}}": "YY Group (Nasdaq: YYGH), an AI-native workforce and facility management company, announced the commercial deployment of Unitree G1 Edu Ultimate humanoid robots across shopping malls, hotels, and commercial real estate. The robots — equipped with 3D touch-sensitive hands and an NVIDIA Jetson Orin AI processor — are targeting high-frequency, labour-intensive cleaning and maintenance workflows. YY Group is using human cleaners wearing data-collection gear to generate the training datasets that teach the robots the tasks. This is one of the first commercial deployments of humanoid robots in the physical facility maintenance sector — the same category as industrial services, building maintenance, and asset protection — signalling that the first real-world wave of humanoid automation is arriving in physical maintenance, not just manufacturing.",
    "{{ROBOT_1_URL}}": "https://www.globenewswire.com/news-release/2026/06/09/3309337/0/en/YY-Group-NASDAQ-YYGH-Launches-Commercial-Humanoid-Robotics-Initiative-to-Drive-AI-Driven-Margin-Expansion-and-Address-Global-Facility-Management-Labor-Shortages.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Open World Cup Campaign Against Türkiye This Sunday — 2pm AEST, Vancouver",
    "{{AUS_1_SUMMARY}}": "Australia kicks off their 2026 FIFA World Cup campaign on Sunday June 14 at 2:00pm AEST, facing Türkiye at BC Place in Vancouver. The Socceroos are in Group D alongside world No.1 ranked USA and Paraguay — all three group stage matches are on the US West Coast. The 2pm Sunday opener against Türkiye is the ideal watching time for Australian fans; the USA match on June 20 is a 5:00am AEST early-morning fixture. The 2026 World Cup is the first 48-team edition, giving Australia a genuine path through the group stage into the knockout rounds.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/socceroos-australia-world-cup-2026-explained/5w41ackgb",

    "{{AUS_2_HEADLINE}}": "Western Sydney International Airport Sets October 25 for First Passenger Flights — NSW's Second Airport Is 135 Days Away",
    "{{AUS_2_SUMMARY}}": "The Federal Government confirmed Western Sydney International Airport (Nancy-Bird Walton) will open for passengers on October 25, with freight beginning July 26. Jetstar will operate the inaugural commercial service — an A320 to the Gold Coast at 11am. The airport is designed for 10 million passengers annually and is the largest infrastructure project ever built in NSW. From late October it adds critical capacity to Australia's most congested aviation market and opens new direct freight routes with competitive implications for east-coast logistics pricing.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "NGV Opens Cartier: Winter Masterpieces Today — Melbourne Hosts the Largest Cartier Exhibition Ever Staged in Australia",
    "{{VIC_1_SUMMARY}}": "The National Gallery of Victoria opens CARTIER: Winter Masterpieces 2026 today at NGV International on St Kilda Road, running through to October 4. Nearly 400 jewels, timepieces and precious objects are on display — almost 300 never before seen in Australia — including pieces owned by Elizabeth Taylor, Grace Kelly, Princess Margaret and Dame Nellie Melba. Created in partnership with the V&A London. For Melbourne this winter the Cartier show joins Lightscape at the Royal Botanic Gardens and World Cup live-site screenings across the city as the three headline draws through July.",

    # Science
    "{{SCI_1_FLAG}}": "🔭 SPACE · JWST",
    "{{SCI_1_HEADLINE}}": "James Webb Reveals Two Completely Different Atmospheres on the Same Planet — An Alien World Where Dawn and Dusk Look Nothing Alike",
    "{{SCI_1_SUMMARY}}": "NASA's James Webb Space Telescope has captured the most detailed atmospheric portrait ever obtained of an exoplanet, revealing that the ultra-hot gas giant WASP-121b — 880 light-years from Earth — has fundamentally different conditions on its morning and evening sides. The dayside averages nearly 2,500°C, hot enough to break apart water molecules; the nightside drops to around 725°C. Fierce eastward winds carry heat from the blazing dayside, creating a hotter and chemically distinct evening terminator. On the cooler nightside, JWST also detected methane — a sign of strong upward winds that current atmospheric models had not predicted. Published in Nature Astronomy, June 11 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Help You Model the June 30 Fuel Price Jump Before It Hits Your Cash Flow",
    "{{INSIGHT_BODY}}": "In 18 days, the temporary fuel excise cut expires and pump prices will rise by approximately 29 cents per litre overnight on July 1. For a trades business with two or three diesel vehicles doing 300–500km a week, that is a real cash flow hit — arriving at the same moment as the Fair Work wage adjustment and any material cost increases flowing from the Middle East energy disruption. The mistake most trades operators make is absorbing cost increases reactively: they feel the margin squeeze in August and only then start adjusting quotes. By that point you have already lost four to six weeks of margin on every job. Here is where AI earns its keep. Open Claude or ChatGPT today and ask it to calculate what an extra 29c/L costs your business per week, per month, and per job type at your current utilisation. Then ask it to model two scenarios — absorbing the cost versus passing it through as a fuel levy or rate adjustment. Ask it to draft the four-line client message you would send to lock in any current pricing before July 1. And ask it to identify which of your job types are most exposed to fuel cost as a proportion of total job value. None of this takes more than 20 minutes. But the difference between doing this analysis today and waiting until late July is the difference between getting ahead of the change and spending the rest of the financial year chasing ground you already lost.",

    # Fun Facts
    "{{FACT_1}}": "The inaugural FIFA World Cup was held in Uruguay in 1930 with just 13 teams and no qualifying tournament — nations received personal invitations. Only four European teams attended, because most refused the two-week ocean voyage by ship. Uruguay, the reigning Olympic gold medallist, defeated Argentina 4–2 in the final in Montevideo. Today's 2026 edition, with 48 teams across three host nations, is more than three times larger than that first edition — and opens its second day of group stage matches tonight.",

    "{{FACT_2}}": "The QR code was invented in 1994 by Masahiro Hara, an engineer at Toyota supplier Denso Wave, to track car parts on factory assembly lines — standard barcodes were too slow. Hara published the standard royalty-free, which is why it spread to restaurant menus, parking meters, bank transfers, and every smartphone on Earth. A QR code's three corner squares are its most recognisable feature: they allow any camera to read the code from any angle, at any rotation, without needing to be perfectly aligned.",

    "{{FACT_3}}": "Aerogel is the world's lightest solid — just approximately 1.5 times denser than air — and one of the best thermal insulators ever made. NASA uses silica aerogel blankets on Mars rovers: a panel just 2.5 centimetres thick maintains the rover's interior 20°C above ambient on the Martian surface, where temperatures drop to −60°C. The same technology is now appearing in industrial pipe insulation and high-performance building wall panels on Earth.",

    # Joke
    "{{JOKE_SETUP}}": "Why do tradies always seem so refreshed on wet Fridays?",
    "{{JOKE_PUNCHLINE}}": "It's the one day the rain forces them inside — and they finally discover they have 847 unread emails.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Champions keep playing until they get it right.”",
    "{{CLOSING_ATTR}}": "— Billie Jean King",
    "{{CLOSING_MESSAGE}}": "It is Friday morning in Carrum Downs and the rain is already here — northerly winds overnight and 7–15mm expected through the day. SpaceX (SPCX) opens for trading on the Nasdaq this morning as the most valuable company ever to list on a US exchange. The 2026 FIFA World Cup is underway after Mexico opened with a goal from Julián Quiñones at the Azteca last night. The Socceroos open their campaign on Sunday afternoon at 2pm AEST against Türkiye in Vancouver — a reasonable hour and a proper occasion. Keep an eye on any Iran ceasefire developments over the weekend: if the Strait of Hormuz reopens, fuel prices will respond quickly, but the excise cut still ends in 18 days regardless. Good wet Friday, Liall — and a better weekend than the sky would suggest.",
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
