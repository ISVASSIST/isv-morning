#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 08 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 8 Jun
    # Cool winter week; showers today and Friday, clearing midweek
    "{{WEATHER_1}}": "MON 8 · 🌧 Showers · 8–14°C",
    "{{WEATHER_2}}": "TUE 9 · ⛅ Clearing · 9–16°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "WED 10 · 🌤 Mostly clear · 8–16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "THU 11 · ⛅ Cloudy · 9–15°C",
    "{{WEATHER_5}}": "FRI 12 · 🌧 Showers · 8–14°C",
    "{{WEATHER_ALERT}}": "👑 KING'S BIRTHDAY PUBLIC HOLIDAY",

    # World
    "{{WORLD_1_FLAG}}": "🌍 MIDDLE EAST · IRAN-US",
    "{{WORLD_1_HEADLINE}}": "Iran Accuses US of Ceasefire Violations — Strikes on Qeshm Radar Sites Condemned as 'Clear Breach'",
    "{{WORLD_1_SUMMARY}}": "Iran's foreign ministry strongly condemned US strikes against radar and coastal surveillance facilities at Sirik and Qeshm Island on Saturday, calling them a \"clear violation of the April 8 ceasefire.\" Tehran accused Washington of complete disregard for international law, saying the targeted facilities protect maritime navigation safety through the Strait of Hormuz. Meanwhile, Israeli forces launched renewed strikes against Hezbollah targets in south Beirut on Sunday, threatening to derail fragile US-Iran peace talks. There is no active ceasefire framework in place and Iran has warned that continued US adventurist actions pose serious escalation risks to regional security.",
    "{{WORLD_1_URL}}": "https://www.cbsnews.com/live-updates/iran-us-war-israel-hezbollah-fighting-ceasefire-efforts/",

    "{{WORLD_2_FLAG}}": "🇦🇱 EUROPE · ALBANIA",
    "{{WORLD_2_HEADLINE}}": "Thousands March in Tirana as Albania Greenlights Kushner's $1.6B Resort on Protected Adriatic Coastline",
    "{{WORLD_2_SUMMARY}}": "Thousands of Albanians protested in Tirana over the weekend against a $1.6 billion luxury resort project on the protected Sazan-Karaburun peninsula, backed by Jared Kushner's Affinity Partners. Demonstrators say the project was fast-tracked by Prime Minister Edi Rama without adequate environmental assessment and threatens one of Europe's last pristine Adriatic coastlines. Protesters waved Albanian and EU flags, raising questions about transparency and the approvals process as Albania's EU accession talks continue.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/world/europe/kushner-luxury-resort-plan-protests-albania-rcna348612",

    # Economics
    "{{ECON_1_FLAG}}": "📊 ECONOMY · AUS GDP",
    "{{ECON_1_HEADLINE}}": "Australia's Economy Grew Just 0.3% in Q1 — Weakest in a Year as War, Weather and Weak Demand Bite",
    "{{ECON_1_SUMMARY}}": "The ABS confirmed that Australia's GDP expanded only 0.3% in the March quarter of 2026, well below the 0.5% forecast and down from 0.9% growth in the prior quarter — the weakest result in a year. Severe weather disrupted mining, exports fell on lower coal and iron ore shipments, and household spending remained subdued. The RBA has flagged further slowing as the Middle East conflict squeezes energy markets and household budgets stay tight — a backdrop that makes the July 1 double-hit of wage rises and fuel excise snapback all the more significant for small business planning right now.",
    "{{ECON_1_URL}}": "https://www.cnbc.com/2026/06/03/australia-gdp-q1-economic-growth-weather-weak-demand-middle-east-war-energy-costs.html",

    "{{ECON_2_FLAG}}": "🏗️ CONSTRUCTION · ABS",
    "{{ECON_2_HEADLINE}}": "Australian Building Approvals Fall 3.4% in April — Trades Pipeline Cooling as High Costs Bite",
    "{{ECON_2_SUMMARY}}": "Australian building approvals fell 3.4% in April 2026, well worse than the 1.5% expected decline, while company gross operating profits fell 1.3% in Q1. The softening approvals trend signals a tightening forward pipeline for new residential and commercial construction — arriving at the same time as higher wages and expiring fuel relief. For small trades operators, a cooling pipeline makes quoting efficiency, relationship retention, and margin discipline more important heading into the second half of the year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🍎 USA · APPLE WWDC",
    "{{TECH_1_HEADLINE}}": "Apple WWDC 2026 Keynote Today — Siri Gets Full AI Overhaul with Gemini Integration, iOS 27 Announced",
    "{{TECH_1_SUMMARY}}": "Apple's WWDC 2026 keynote goes live tonight Australian time (10am Pacific), with Siri set for its biggest transformation since 2011. Apple has rebuilt Siri as a full chatbot with LLM-powered intelligence and deep integration with Google's Gemini models — the first time a third-party AI provider has been embedded in Apple's core assistant. iOS 27, macOS 27, watchOS 27 and visionOS 27 are all expected, along with expanded Apple Intelligence features and the option to set Claude, ChatGPT or Gemini as default for specific tasks. Developer betas drop today; public release expected September.",
    "{{TECH_1_URL}}": "https://www.macrumors.com/roundup/wwdc/",

    "{{TECH_2_FLAG}}": "🧠 USA · ANTHROPIC",
    "{{TECH_2_HEADLINE}}": "Anthropic: Claude Now Writes 80% of Its Own Production Code — Company Warns AI Needs a Brake Pedal",
    "{{TECH_2_SUMMARY}}": "In a striking disclosure published last week, Anthropic revealed that more than 80% of the code merged into its production codebase in May 2026 was authored by Claude — up from near zero just 18 months earlier. Rather than celebrating the milestone, Anthropic used it as a warning: the company called on all frontier AI labs to agree on a coordinated mechanism to slow or pause development if AI systems begin recursively self-improving faster than humans can manage. Claude succeeded on its hardest unsupervised coding tasks 76% of the time in May — a 50 percentage point improvement in six months.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 USA · AMAZON ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "Amazon's One-Million-Robot Fleet Gets an AI Brain — DeepFleet Cuts Travel Time by 10%, Delivery Robots Next",
    "{{ROBOT_1_SUMMARY}}": "Amazon has crossed one million robots deployed across its global fulfilment network and has now layered a generative AI routing system called DeepFleet on top — optimising robot movement in real time to cut fleet travel time by 10% without adding hardware. The company's next step is autonomous last-mile delivery robots, with MIT collaborating on solving outdoor routing challenges. Amazon says 75% of its global deliveries are already assisted by a robot at some stage. The deployment scale — one million physical robots, AI-coordinated routing, and delivery robots next — is arguably the most concrete current example of what end-to-end robotic logistics looks like at commercial scale.",
    "{{ROBOT_1_URL}}": "https://nationalcioreview.com/articles-insights/extra-bytes/amazons-logistics-strategy-evolves-with-deepfleet-and-one-million-robots/",

    # Australia
    "{{AUS_1_HEADLINE}}": "King's Birthday Public Holiday Today — Victoria and Most States Observe Long Weekend",
    "{{AUS_1_SUMMARY}}": "Monday 8 June is the King's Birthday public holiday in Victoria, New South Wales, South Australia, Tasmania and the ACT, marking King Charles III's official birthday. Shops and most businesses are closed, while workers required to come in are entitled to public holiday penalty rates under the Fair Work Act. Note: Queensland and Western Australia observe King's Birthday on separate dates later in the year.",
    "{{AUS_1_URL}}": "https://business.vic.gov.au/business-information/public-holidays/victorian-public-holidays-2026",

    "{{AUS_2_HEADLINE}}": "World Cup in Three Days: Socceroos Depart for North America, Group D Campaign Begins June 14",
    "{{AUS_2_SUMMARY}}": "The FIFA World Cup 2026 opens this Thursday June 11 in Mexico City, and Australia's Socceroos begin their Group D campaign against Turkey in Vancouver on June 14 — then face co-hosts USA on June 20 and Paraguay on June 26. The 26-man squad features veterans Mathew Leckie and Mat Ryan alongside 17 debutants. The tournament spans 16 cities across three host nations over 39 days.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "21-Gun Salute at the Shrine as Melbourne Marks King Charles III's Official Birthday",
    "{{VIC_1_SUMMARY}}": "A 21-gun salute at Melbourne's Shrine of Remembrance this morning officially marks King Charles III's birthday across Victoria, with the state observing the public holiday long weekend. Across greater Melbourne and regional Victoria, most businesses are closed. RISING Festival, Melbourne's annual new art event, also wraps up today after running since May 28 across 60+ events at 50 venues — its final day coinciding with the public holiday.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 USA · LOS ALAMOS",
    "{{SCI_1_HEADLINE}}": "Scientists Solve the Last Piece of Schrödinger's 100-Year-Old Colour Theory — With Implications for Your TV Screen",
    "{{SCI_1_SUMMARY}}": "Researchers led by Los Alamos National Laboratory scientist Roxana Bujack have resolved the final unfinished element of Erwin Schrödinger's mathematical theory of colour perception — first formulated in the 1920s. The team used Riemannian geometry to formally define the 'neutral axis' of colour space (the line from pure black through grey to white) that Schrödinger described qualitatively but never pinned down mathematically. Correcting this gap in the model used by the entire colour-reproduction industry has immediate practical implications for display calibration in televisions, monitors and medical imaging, as well as for textile and paint manufacturers who rely on colour-matching algorithms. Published ScienceDaily, 6 June 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Why the King's Birthday Long Weekend Is the Best Four Hours You'll Spend on Your Business All Year",
    "{{INSIGHT_BODY}}": "With July 1 now under three weeks away and two significant cost increases set to land simultaneously — the Fair Work wage rise and the fuel excise snapback — this public holiday morning is arguably the most valuable uninterrupted planning window you will get before the financial year turns. Use it to do three things with AI: first, stress-test your current job rates against the new wage structure and fuel costs to find out which job types are quietly going underwater; second, have AI draft revised rate cards and quote templates ready to go from next week; third, run a debrief on your last ten jobs to spot the margin patterns you have been too busy to notice. Most trades operators will spend this morning doing nothing, or doing unpaid work out of habit. The ones who come out of July still making money will be the ones who used today to get ahead of it.",

    # Fun Facts
    "{{FACT_1}}": "The tradition of celebrating a British monarch's birthday on a separate 'official' date began with King George II (1683–1760), whose actual birthday fell in late October — poor weather for the outdoor military reviews the occasion required in England. Every British and Commonwealth sovereign since has maintained a ceremonial birthday distinct from their real one. King Charles III was born on 14 November 1948 but is officially celebrated across most of Australia on the second Monday of June.",

    "{{FACT_2}}": "The human eye contains only three types of colour-detecting cone cells, yet the brain interprets combinations of their signals to distinguish roughly 10 million shades. The vast majority of those shades have no name in any language — we experience them but cannot describe them precisely with words. Colour-blindness, most commonly a reduced ability to tell red from green, affects around 8 per cent of men but only 0.5 per cent of women.",

    "{{FACT_3}}": "Space Invaders (1978) was so popular in Japan within months of launch that it caused a temporary shortage of 100-yen coins, prompting the government to quadruple coin production to keep up with demand. It was also the first video game to save high scores — allowing players to see and try to beat previous bests — a design mechanic that has since driven the engagement model of virtually every game, app, and fitness platform built in the decades since.",

    # Joke
    "{{JOKE_SETUP}}": "How does a trades business owner spend the King's Birthday public holiday?",
    "{{JOKE_PUNCHLINE}}": "Invoicing last week's jobs, quoting next week's leads, and technically calling it a day off.",

    # Closing
    "{{CLOSING_QUOTE}}": "“He who is not courageous enough to take risks will accomplish nothing in life.”",
    "{{CLOSING_ATTR}}": "— Muhammad Ali",
    "{{CLOSING_MESSAGE}}": "It's a cool, showery Monday morning in Carrum Downs — 8 to 14 degrees, King's Birthday long weekend, and a good day to be near the bay. Apple's WWDC keynote fires up tonight Australian time — the new Siri looks like the biggest iPhone shift in years. With July 1 now under three weeks away and two cost hits landing on the same day, if you can carve out a couple of hours today before the weekend ends, running the numbers on what the wage rise and fuel snapback actually cost you per job is time well spent. The World Cup opens Thursday. Socceroos kick off June 14. Have a good one, Liall.",
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
