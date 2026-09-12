#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 13 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 13 Sep (BOM Melbourne-area forecast)
    "{{WEATHER_1}}": "SUN 13 SEP · 🌦️ Partly cloudy, medium chance of a shower this evening, chance of a late-afternoon thunderstorm, northerly winds 25–40km/h · 13–23°C",
    "{{WEATHER_2}}": "MON 14 SEP · 🌧️ Cloudy, high chance of showers, winds N–NW 20–30km/h turning W 15–20km/h · 12–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 15 SEP · ⛈️ Partly cloudy, high chance of showers with possible small hail in the afternoon and evening, W turning SW 25–35km/h · 9–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 16 SEP · ☁️ Cloudy, slight chance of a shower mostly in the morning · 9–13°C",
    "{{WEATHER_5}}": "THU 17 SEP · ⛅ Mostly cloudy, shower risk easing · 8–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — a mild, showery start to the week sharpens into a cool change with possible small hail Tuesday afternoon, before settling cloudy and cool by midweek.",

    # World
    "{{WORLD_1_FLAG}}": "🇾🇪 BAB EL-MANDEB · HOUTHIS SEIZE STRAIT ISLAND AS SAUDI PIPELINE STAYS SHUT",
    "{{WORLD_1_HEADLINE}}": "Houthi Forces Seize Strategic Red Sea Island, Completing Control of the Bab el-Mandeb Shipping Lane",
    "{{WORLD_1_SUMMARY}}": "Iran-backed Houthi forces reached the strategic island of Perim on Friday, sealing their takeover of the Bab el-Mandeb Strait — the narrow chokepoint linking the Red Sea to the Indian Ocean — just as Saudi Arabia's critical East-West oil pipeline remained shut following this week's drone strikes on its pumping stations. Analysts warn effective Houthi control of the strait hands Iran fresh leverage over global oil shipping, adding to an already jumpy energy market.",
    "{{WORLD_1_URL}}": "https://fortune.com/2026/09/12/saudi-arabia-nightmare-scenario-houthis-red-sea-shipping-route-drone-attacks-closure-east-west-pipeline/",

    "{{WORLD_2_FLAG}}": "🇮🇳 NEW DELHI · XI, PUTIN AND MODI MEET AT BRICS SUMMIT AMID TRUMP PRESSURE",
    "{{WORLD_2_HEADLINE}}": "India Hosts Xi, Putin and Modi at BRICS Summit as Bloc Tests Unity Under US Tariff Pressure",
    "{{WORLD_2_SUMMARY}}": "China's Xi Jinping, Russia's Vladimir Putin and host Narendra Modi met in New Delhi for the 18th BRICS Summit, themed 'Intra-BRICS cooperation for continuity, consolidation and consensus,' as the bloc's emerging economies look for common ground in the face of US tariffs, sanctions and the ongoing Iran war.",
    "{{WORLD_2_URL}}": "https://www.cnbc.com/2026/09/12/brics-summit-xi-putin-modi-trump.html",

    # Economics
    "{{ECON_1_FLAG}}": "📈 RATES · MARKETS PUSH RBA HIKE ODDS TO 72% AS OIL SURGE ADDS TO INFLATION RISK",
    "{{ECON_1_HEADLINE}}": "RBA Rate-Hike Odds Jump to 72% as This Week's Middle East Oil Shock Threatens to Reignite Inflation",
    "{{ECON_1_SUMMARY}}": "Markets now price a 72% chance the RBA lifts the cash rate to 4.60% at its 29 September meeting, up from 54% at the start of the month, after July's trimmed-mean inflation held at 3.6% — still above target — and this week's Houthi and Saudi pipeline disruptions pushed oil back above US$100 a barrel. A hike would add roughly $121 a month to repayments on an average mortgage, and typically flows through fast to overdraft and equipment-finance rates too.",
    "{{ECON_1_URL}}": "https://www.fxstreet.com/news/australian-dollar-climbs-on-rba-rate-hike-expectations-as-traders-await-us-cpi-202609111100",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE UNLEADED AVERAGING ~212C/L, BEFORE THIS WEEK'S OIL SPIKE HITS",
    "{{ECON_2_HEADLINE}}": "Melbourne Petrol Still Averaging Around 212c/L — But the Bowser Hasn't Caught Up to This Week's Oil Shock Yet",
    "{{ECON_2_SUMMARY}}": "Melbourne unleaded is averaging about 211–212c/L across the city's 1,100-plus stations this week, with the cheapest sites near 190c/L, according to the ACCC's latest weekly monitoring — but that snapshot predates the Houthi and Saudi-pipeline-driven oil spike, and pump prices typically take one to two weeks to catch up to a crude move. Worth building a fuel-surcharge buffer into quotes now rather than absorbing it after the next price cycle turns.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💬 WORKPLACE AI · SLACK LETS YOU BUILD A LIVE DASHBOARD JUST BY ASKING",
    "{{TECH_1_HEADLINE}}": "Slack's New 'Surfaces' Feature Builds Live Dashboards and Reports Just From a Plain-English Request",
    "{{TECH_1_SUMMARY}}": "Salesforce-owned Slack this week launched Slackforce Surfaces, letting anyone describe a dashboard, report, poll or one-page site to Slackbot and have it built on the spot, staying connected to the underlying data and refreshing as it changes. It's available to every workspace with Slackbot enabled, including free accounts — a glimpse of how easy it's becoming to turn scattered team chat and files into something you can actually glance at each morning.",
    "{{TECH_1_URL}}": "https://dataconomy.com/2026/09/11/slack-ai-powered-surfaces-interactive-reports-chats/",

    "{{TECH_2_FLAG}}": "🧠 AI MODELS · DEEPSEEK'S NEW FLASH MODEL UNDERCUTS RIVALS ON COST AND SPEED",
    "{{TECH_2_HEADLINE}}": "DeepSeek Launches V4.1 Flash, a Free-to-Use Open Model That Beats Its Predecessor on Speed and Price",
    "{{TECH_2_SUMMARY}}": "Chinese AI lab DeepSeek released V4.1 Flash this week, a 552-billion-parameter model that outperforms its own pricier 'Pro' tier on benchmarks while running faster and cheaper, and is freely available for commercial use under an open MIT licence. It's another sign that capable AI is getting steadily cheaper to run — useful context if you're weighing up which AI tool to build a business workflow around.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 PHYSICAL AI · NEW ULTRASOUND SENSOR GIVES ROBOT HANDS A SENSE OF TOUCH THAT DOESN'T WEAR OUT",
    "{{ROBOT_1_HEADLINE}}": "UltraSense Unveils an Ultrasound Tactile Sensor Built to Give Industrial Robot Hands a Sense of Touch That Survives Years of Contact",
    "{{ROBOT_1_SUMMARY}}": "Chipmaker UltraSense Systems this week launched an ultrasound-based tactile sensing platform that reads touch through a protected sub-surface layer instead of an exposed sensor skin, letting robotic hands and grippers detect contact, location and force without the wear and tear that degrades current touch sensors over time. It's aimed squarely at humanoid hands and industrial end-effectors — the kind of unglamorous reliability problem that decides whether a robot actually survives a working factory floor.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/ultrasound-offers-scalable-path-tactile-intelligence-physical-ai/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Optus Outage Knocks Out Triple Zero Calls Across Victoria, SA, Tasmania and the NT",
    "{{AUS_1_SUMMARY}}": "An Optus network fault disrupted voice calls for about 75 minutes, with roughly 40 calls failing to connect to Triple Zero across four states and territories. Victoria Police carried out welfare checks on affected callers with no adverse outcomes, while Victoria's health minister called it 'incredibly disappointing and unacceptable' — the third such outage from Optus or Telstra in 12 months.",
    "{{AUS_1_URL}}": "https://thenightly.com.au/australia/optus-outage-hits-triple-zero-calls-across-victoria-south-australia-tasmania-and-northern-territory-c-22860089",

    "{{AUS_2_HEADLINE}}": "Rio Tinto's 2029 Nhulunbuy Exit Looms Over NT's Mulka By-Election",
    "{{AUS_2_SUMMARY}}": "Rio Tinto confirmed its north-east Arnhem Land bauxite mine will stop production in 2029, stripping the NT town of Nhulunbuy of its biggest employer just as Woolworths also prepares to pull out — a second major blow after the local alumina refinery closed in 2014. The fallout is shaping today's Mulka by-election, triggered by a sitting MP's resignation last month.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Fire Guts Historic Wattle Park Chalet Hours Before a Wedding Was Due to Start",
    "{{VIC_1_SUMMARY}}": "Firefighters found Melbourne's 1928-built Wattle Park Chalet in Surrey Hills well alight about 6:30am Saturday, with fire, smoke and water damage wrecking roughly 30% of the venue's main hall. The new owner — five months into running the business — is now scrambling to relocate a 110-guest wedding booked for that same night; police are treating the blaze as suspicious.",

    # Science
    "{{SCI_1_FLAG}}": "🦖 PALEONTOLOGY · A FEATHER FOSSILISED INSIDE DINOSAUR DROPPINGS REWRITES HOW BIRDS SURVIVED",
    "{{SCI_1_HEADLINE}}": "A 66-Million-Year-Old Feather Found Inside Fossilised Dinosaur Droppings May Explain Why Birds Survived the Asteroid",
    "{{SCI_1_SUMMARY}}": "Field Museum researchers have identified the first-ever fossil feather preserved inside a coprolite — fossilised droppings, likely from a T. rex or Nanotyrannus that had eaten a diving bird. The feathers show a primitive, fluffier underlayer than modern birds, suggesting their insulation wasn't fully evolved yet — a clue to why only some bird lineages made it through the asteroid impact's 'impact winter' 66 million years ago, published this week in Current Biology.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Ask, Don't Build: What Slack's New Live Dashboards Mean for a Business Your Size",
    "{{INSIGHT_BODY}}": "Slack's new Surfaces feature lets anyone type a plain-English request — 'show me which jobs are overdue and what we're still owed' — and get a live, self-updating dashboard back, no spreadsheet formulas or BI software required. You don't need Slack to get the same result: point ChatGPT, Gemini or Claude at your own job-tracking sheet or invoicing export and ask the identical question. The shift worth noticing isn't the specific tool — it's that 'build me a report' is quietly becoming something you ask for instead of something you pay someone to make.",

    # Fun facts
    "{{FACT_1}}": "The Bab el-Mandeb Strait separating Yemen from the Horn of Africa narrows to about 29 kilometres across at its tightest point, yet roughly 10% of the world's seaborne oil trade passes through it — which is why this week's Houthi advance into the strait rattled energy markets far beyond Yemen's borders.",
    "{{FACT_2}}": "The term 'BRICS' wasn't coined by a diplomat but by Goldman Sachs economist Jim O'Neill in a 2001 research paper grouping Brazil, Russia, India and China as future growth engines — the acronym outlived the paper and grew into the 10-plus-nation bloc that met in New Delhi this week.",
    "{{FACT_3}}": "Australia's 000 emergency number was chosen in 1961 partly because '0' sits at the very end of a rotary dial, making it the easiest digit to find by feel in the dark or in a panic — a design logic that still shapes how seriously any outage affecting it is taken today.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the blinds and curtains installer's small business never miss a deadline?",
    "{{JOKE_PUNCHLINE}}": "Because he always measured twice and invoiced once.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Inaction breeds doubt and fear. Action breeds confidence and courage.\"",
    "{{CLOSING_ATTR}}": "— Dale Carnegie",
    "{{CLOSING_MESSAGE}}": "It's a mild, showery start to the week around Carrum Downs, with a cool change and a chance of small hail moving through on Tuesday — worth getting outdoor jobs wrapped up before then rather than after. With oil back above US$100 a barrel on this week's Middle East disruption and RBA rate-hike odds now sitting at 72%, it's shaping up as a week where getting quotes out early, fuel surcharge included, beats waiting and wearing the cost creep yourself.",
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
