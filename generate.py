#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 24 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 24 Jul (BOM)
    "{{WEATHER_1}}": "FRI 24 · 🌥️ Cloudy, showers · 7–14°C",
    "{{WEATHER_2}}": "SAT 25 · 🌦️ Shower or two · 8–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 26 · 🌧️ Showers, most of the day · 8–16°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 27 · ⛅ Partly cloudy, isolated shower · 9–16°C",
    "{{WEATHER_5}}": "TUE 28 · 🌦️ Shower or two developing · 9–17°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS MOST DAYS THROUGH THE WEEKEND, EASING MONDAY · NO SEVERE WARNINGS FOR MELBOURNE METRO",

    # World
    "{{WORLD_1_FLAG}}": "🇾🇪🇸🇦 RED SEA ESCALATION · HOUTHIS STRIKE SAUDI OIL TANKERS · TRUMP THREATENS 'MASSIVE' IRAN STRIKE",
    "{{WORLD_1_HEADLINE}}": "Houthi Rebels Attack Two Saudi Oil Tankers in the Red Sea as the US Carries Out a 12th Night of Strikes on Iran",
    "{{WORLD_1_SUMMARY}}": "Yemen's Iran-backed Houthis said they struck the tankers Encelia and Layla with drones and missiles early Thursday, setting both alight in the first attacks since declaring a naval blockade of Saudi Arabia — while President Trump threatened a 'massive' new strike on Iran, 'bigger than ever before,' after a 12th consecutive night of US bombing. No casualties were reported, but the attacks mark a serious widening of a war already reshaping global shipping and oil markets.",
    "{{WORLD_1_URL}}": "https://www.usnews.com/news/world/articles/2026-07-23/houthis-say-they-attacked-2-saudi-oil-tankers-in-the-red-sea-as-us-carries-out-12th-night-of-strikes",

    "{{WORLD_2_FLAG}}": "🇫🇷🇮🇹🇪🇸 EUROPE WILDFIRES · HEATWAVE FUELS BLAZES ACROSS FRANCE, ITALY AND SPAIN · 3 FIREFIGHTERS DEAD",
    "{{WORLD_2_HEADLINE}}": "Three Firefighters Killed as Heatwave-Fuelled Wildfires Force Thousands to Flee Homes Across Southern Europe",
    "{{WORLD_2_SUMMARY}}": "Two firefighters died battling a blaze near Bordeaux airport in France and a third in Sicily, Italy, as an intense heatwave drove wildfires across France, Italy and Spain, forcing around 12,000 people to evacuate. Nearly 6,000 acres have burned west of Bordeaux alone, with temperatures topping 40°C in Sicily as roughly 6,000 firefighters battle hundreds of separate blazes.",
    "{{WORLD_2_URL}}": "https://www.france24.com/en/europe/20260723-wildfires-ravage-spain-france-and-italy-killing-three-firefighters",

    # Economics
    "{{ECON_1_FLAG}}": "📊 JOBS SHOCK · AUSTRALIAN EMPLOYMENT SURGES 76,300 IN JUNE · RATE-HIKE ODDS CLIMB",
    "{{ECON_1_HEADLINE}}": "Australian Employment Jumps by 76,300 in June — Five Times Forecasts — Fuelling Bets on Another Rate Rise",
    "{{ECON_1_SUMMARY}}": "The biggest monthly jobs rise in 14 months pushed the Australian dollar higher and lifted the market-implied chance of an August rate hike to 31%, from 23% before the data landed, even as unemployment held at 4.4%. For small business, a labour market this tight means wage pressure isn't easing any time soon — worth locking in staff and pricing accordingly before the next award review.",
    "{{ECON_1_URL}}": "https://www.tradingpedia.com/2026/07/23/australian-dollar-tops-0-7000-after-strong-jobs-data/",

    "{{ECON_2_FLAG}}": "🛢️ OIL AT $100 · BRENT CRUDE HITS TRIPLE FIGURES FOR FIRST TIME SINCE MAY",
    "{{ECON_2_HEADLINE}}": "Brent Crude Tops US$100 a Barrel for the First Time Since May After Houthi Attacks on Saudi Tankers",
    "{{ECON_2_SUMMARY}}": "Brent surged more than 7% to above $100 on Thursday — up nearly 36% over the past month — as the Red Sea attacks raised fears of a second oil chokepoint alongside the Strait of Hormuz. With the federal fuel excise relief already halved to 16 cents a litre and due to expire August 2, further bowser rises look likely before they look like easing.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🏢 AI INFRASTRUCTURE · OPENAI UNVEILS 'PRESENCE' ENTERPRISE AGENT PLATFORM AND $30BN GEORGIA DATA CENTRE",
    "{{TECH_1_HEADLINE}}": "OpenAI Launches 'Presence,' an Enterprise AI Agent Platform, Alongside Plans for a $30 Billion Georgia Data Centre",
    "{{TECH_1_SUMMARY}}": "OpenAI's new Presence platform is built to plug AI agents directly into a business's internal data, policies and workflows for jobs like customer service, sales and IT support — landing the same week the company revealed a 1,400-acre, $30 billion data centre project near Savannah to keep pace with demand. It's a reminder that the AI tools showing up in ordinary business software are backed by an infrastructure build-out on a genuinely historic scale.",
    "{{TECH_1_URL}}": "https://www.bloomberg.com/news/articles/2026-07-22/openai-plans-to-spend-over-30-billion-on-georgia-data-center",

    "{{TECH_2_FLAG}}": "💰 AI PRICE WAR · DEEPSEEK V4 GOES STABLE TODAY, SETTING A NEW INDUSTRY PRICE FLOOR",
    "{{TECH_2_HEADLINE}}": "DeepSeek's V4 Model Goes Fully Stable Today, Undercutting Rivals at Under Half a Cent per Million Output Tokens",
    "{{TECH_2_SUMMARY}}": "The Chinese lab's stable V4 release lands today alongside Kimi K3's open-weight launch next week, in what's shaping up as the industry's biggest cluster of open-weight model releases yet — with DeepSeek's pricing setting the benchmark every other provider gets compared against. For small businesses, it's part of why the AI features quietly appearing in your existing software keep getting cheaper or more capable without any change to your subscription.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 EUROPE'S FIRST HUMANOID ROBOTICS UNICORN · HUMANOID RAISES $152M, BOSCH TO MANUFACTURE AT SCALE",
    "{{ROBOT_1_HEADLINE}}": "UK Robotics Startup Humanoid Raises $152 Million to Become Europe's First Pure-Play Humanoid Robotics Unicorn",
    "{{ROBOT_1_SUMMARY}}": "London-based Humanoid closed a $152 million Series A at a $1.35 billion valuation, with Bosch signing on as contract manufacturer for its wheeled HMND 01 robot and Schaeffler committing to deploy thousands of the machines across its factories. It's another sign that humanoid robots are moving past flashy demos and into contracts for real, repetitive industrial work — the same shift already under way in warehouses and on production lines worldwide.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/07/22/humanoid-raises-152-million-at-1-35-billion-valuation-becoming-europes-first-pure-play-humanoid-robotics-unicorn/103561/",

    # Australia
    "{{AUS_1_HEADLINE}}": "ACT Deputy Chief Minister Yvette Berry Resigns From Cabinet After a Five-Year Corruption Inquiry Finds Against Her Former Chief of Staff",
    "{{AUS_1_SUMMARY}}": "Berry stepped down Thursday after the ACT Integrity Commission found her former chief of staff acted dishonestly in steering an $18 million Canberra school contract away from the recommended tenderer and toward a firm with links to the CFMEU. Chief Minister Andrew Barr accepted her resignation and apologised to Canberrans for the conduct uncovered by the five-year investigation.",
    "{{AUS_1_URL}}": "https://www.canberratimes.com.au/story/9316429/yvette-berry-resigns-from-cabinet-after-integrity-findings/",

    "{{AUS_2_HEADLINE}}": "Australia's Commonwealth Games Medal Hunt Begins in Earnest Today as Swimming Finals Open in Glasgow",
    "{{AUS_2_SUMMARY}}": "Friday marks the first full day of competition at Glasgow 2026, with nine swimming gold medals up for grabs at the Tollcross International Swimming Centre alongside para powerlifting and men's artistic gymnastics finals — the real start of Australia's campaign after Thursday's opening ceremony.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Open House Melbourne's 'Generous City' Weekend Kicks Off Today With 180 Free Events Across the City",
    "{{VIC_1_SUMMARY}}": "From today through Sunday, Open House Melbourne throws open around 180 of the city's buildings and spaces — from the Australian Ballet Centre's costume department to the new Transurban Freeway Control Centre — with roughly 70,000 visitors expected over the three days. Most sessions are free, though popular tours are booking out fast.",

    # Science
    "{{SCI_1_FLAG}}": "🔭 ASTRONOMY · JAMES WEBB TELESCOPE UNCOVERS A GIANT PLANET HIDING IN PLAIN SIGHT",
    "{{SCI_1_HEADLINE}}": "NASA's Webb Telescope Discovers a Hidden Giant Planet in One of Astronomy's Most Studied Star Systems",
    "{{SCI_1_SUMMARY}}": "Astronomers weren't even looking for a new planet when Webb's spectrograph picked up the chemical fingerprint — carbon monoxide, water vapour and methane — of a gas giant hidden inside Beta Pictoris' dusty disk, about twice Jupiter's mass and orbiting roughly where Neptune sits in our own solar system. It's the first time a planet has been found this way, by its atmosphere rather than its light, a technique astronomers say could uncover many more worlds hiding in plain sight.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI Got Cheaper Again Today — Here's Why That Actually Matters for a One-Truck Business",
    "{{INSIGHT_BODY}}": "Chinese AI lab DeepSeek pushed its V4 model to a full stable release today at under half a cent per million output tokens, the latest move in a price war that's dragging the cost of running AI tools down across the entire industry. Most small trades operators never see this directly — the quoting app, scheduling tool or customer chatbot you already pay for is quietly built on top of models like this — but it's exactly why the same subscription that felt basic and expensive a year ago keeps getting cheaper or picking up features for free. Worth a look at your software's changelog this month rather than assuming last year's plan is still the best one on offer.",

    # Fun Facts
    "{{FACT_1}}": "The word 'sabotage' comes from French factory workers in the 1800s who jammed machinery by throwing their wooden clogs — sabots — into the works during industrial disputes, giving English a word for deliberate disruption.",

    "{{FACT_2}}": "Snake, the black-and-white game preloaded on Nokia phones from 1997, is estimated to have been played by more people than any other video game in history simply because it shipped by default on hundreds of millions of handsets.",

    "{{FACT_3}}": "Anodising aluminium doesn't add a coating in the usual sense — it thickens the metal's own natural oxide layer from around 10 nanometres to as much as 25 microns, more than 2,000 times thicker, using the aluminium's own atoms rather than a separate applied layer.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the paving contractor's small business always stay level?",
    "{{JOKE_PUNCHLINE}}": "He never cut corners — literally.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The future depends on what you do today.\"",
    "{{CLOSING_ATTR}}": "— Mahatma Gandhi",
    "{{CLOSING_MESSAGE}}": "Friday starts cloudy and cool across Carrum Downs — 7–14°C — with showers sticking around most of the weekend before easing into Monday. Oil just hit US$100 a barrel for the first time since May after Houthi attacks on Saudi tankers, so expect more pressure at the bowser before it eases; meanwhile Australia's Commonwealth Games campaign gets going in earnest today with nine swimming golds on the line in Glasgow, and if you're free this weekend, Open House Melbourne has 180 buildings open across the city for a look behind the scenes.",
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
