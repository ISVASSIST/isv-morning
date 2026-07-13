#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 14 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 14 Jul (BOM)
    "{{WEATHER_1}}": "TUE 14 · 🌧️ Showers, breezy · 9–14°C",
    "{{WEATHER_2}}": "WED 15 · 🌦️ Showers easing, windy · 8–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 16 · ⛅ Becoming cloudy, slight shower · 6–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 17 · ⛅ Partly cloudy, mostly dry · 6–13°C",
    "{{WEATHER_5}}": "SAT 18 · ☀️ Partly cloudy to sunny · 5–14°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS EASE MIDWEEK · CLEARING TOWARD THE WEEKEND",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸🇮🇷 US · IRAN · HORMUZ BLOCKADE REIMPOSED, 20% SHIPPING FEE",
    "{{WORLD_1_HEADLINE}}": "Trump Reinstates Strait of Hormuz Blockade, Demands 20% Fee on All Cargo Through It",
    "{{WORLD_1_SUMMARY}}": "President Trump announced the US will restart its naval blockade of Iranian ports from Tuesday and impose a 20% charge on all cargo shipping through the Strait of Hormuz, covering what he called the cost of providing security in the region. It's the second US blockade of Iranian waters this year, coming as Iran's IRGC hit US-linked targets in Kuwait, Bahrain and Jordan overnight — a fresh escalation with direct flow-on risk to global oil and shipping costs, Australia included.",
    "{{WORLD_1_URL}}": "https://www.cnbc.com/2026/07/13/trump-iran-hormuz-strait-charge-reimburse.html",

    "{{WORLD_2_FLAG}}": "🇺🇸 WASHINGTON · TRIBUTE · LONGTIME SENATOR DIES SUDDENLY",
    "{{WORLD_2_HEADLINE}}": "US Senator Lindsey Graham Dies at 71 After Sudden Aortic Dissection",
    "{{WORLD_2_SUMMARY}}": "South Carolina Senator Lindsey Graham, a leading Republican foreign policy voice and close Trump ally, died Saturday night at his Capitol Hill home from a ruptured aorta, his office confirmed. He'd served in the Senate since 2003 and was a key voice on the Ukraine and Middle East conflicts, and tributes have poured in from across the political aisle.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/07/12/nx-s1-5890790/us-sen-lindsey-graham-dies",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · HORMUZ FEE THREAT · BOWSER PRICES UNDER PRESSURE",
    "{{ECON_1_HEADLINE}}": "20% Hormuz Shipping Fee Threatens Fresh Fuel Price Rises on Top of Already-Climbing Bowser Costs",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly monitoring already had capital city petrol at 158.1c/L and diesel at 179.1c/L from 1 July as the fuel excise discount halved to 16c — and Trump's new 20% Hormuz shipping toll, layered on an active blockade, threatens to push global oil and freight costs higher still. Worth locking in a fuel surcharge clause on quotes now rather than absorbing another jump later.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "💰 PAYROLL · MINIMUM WAGE UP 4.75% · FIRST FULL PAY CYCLE HITS",
    "{{ECON_2_HEADLINE}}": "National Minimum Wage Rise and Payday Super Both Bite in the Same Pay Cycle This Week",
    "{{ECON_2_SUMMARY}}": "The National Minimum Wage rose 4.75% to $26.44 an hour ($1,004.90 a week) from the first full pay period after 1 July, landing in the same cycle as Payday Super's new requirement to pay super with every payday instead of quarterly. For any business running a team, that's higher wage costs and a tighter cash-flow cycle hitting at once — worth checking this week's payroll run lines up before it's overdue.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤝 BIG TECH · GOOGLE + MICROSOFT · ENTERPRISE AI AGENTS TEAM UP",
    "{{TECH_1_HEADLINE}}": "Google and Microsoft Quietly Team Up With Salesforce, Snowflake and ServiceNow on a Shared AI Agent Standard",
    "{{TECH_1_SUMMARY}}": "The five companies, which between them run the software holding most of the world's business data, are working toward a common technical standard for connecting AI agents to business systems — a direct answer to Anthropic's Model Context Protocol, which has become the default over the past 18 months. For any business running multiple apps (quoting, invoicing, scheduling), it's a sign these tools are getting closer to actually talking to each other properly, regardless of which AI vendor sits behind them.",
    "{{TECH_1_URL}}": "https://thenextweb.com/news/google-cloud-next-ai-agents-agentic-era",

    "{{TECH_2_FLAG}}": "🤖 AI MODEL WARS · ANTHROPIC EXTENDS FREE ACCESS AGAIN",
    "{{TECH_2_HEADLINE}}": "Anthropic Extends Free Access to Its Top Claude Model Again After OpenAI's Latest Release",
    "{{TECH_2_SUMMARY}}": "Anthropic has extended no-cost subscriber access to its flagship Claude Fable 5 model through July 19, its second extension in a week, directly responding to competitive pressure from OpenAI's newest ChatGPT release. Handy timing for anyone still deciding which AI subscription is worth paying for long-term.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · LAUNCH · HUMANOID BUILT FOR HARD-TO-STAFF JOBS",
    "{{ROBOT_1_HEADLINE}}": "Robot.com Launches R-Noid Humanoid for the Repetitive, Hard-to-Staff Jobs Businesses Can't Fill",
    "{{ROBOT_1_SUMMARY}}": "Robot.com has commercially launched R-noid, a humanoid robot explicitly targeted at multi-shift, repetitive, hard-to-staff roles across restaurant, packing, picking, folding and hosting jobs, spanning industrial, logistics, healthcare, food service and hospitality settings. It's part of a broader shift in 2026 from flashy robot demos toward robots aimed squarely at the labour-shortage roles small and mid-sized operators actually struggle to fill.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/07/13/robot-com-launches-humanoid-built-for-the-work-that-burns-people-out/103259/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Government Rules Out Any Support for Australian Men Held as Suspected IS Fighters in Iraq",
    "{{AUS_1_SUMMARY}}": "Home Affairs Minister Tony Burke says the federal government will not lift a finger to help repatriate around 13 Australian men suspected of being former IS group fighters, held in Baghdad's Al-Karkh Central Prison and reportedly being considered for release by Iraqi and US officials. Burke said their choices reflected a rejection of Australian values.",
    "{{AUS_1_URL}}": "https://thenightly.com.au/politics/australian-isis-detainees-in-iraq-could-be-released-from-al-karkh-central-prison-as-tony-burke-rules-out-help-c-22555008",

    "{{AUS_2_HEADLINE}}": "Handwritten Arrival Cards to Be Scrapped for Digital Border Declarations at Australian Airports",
    "{{AUS_2_SUMMARY}}": "The federal government says its new Australia Travel Declaration app will replace handwritten passenger arrival cards at all Australian airports in a national rollout from next year, aimed at improving biosecurity screening. It follows a trial of more than 450,000 passengers on Qantas international flights into Brisbane, Sydney and Melbourne since late 2024.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Antisemitism Royal Commission Opens Melbourne Hearings Into Australian Universities",
    "{{VIC_1_SUMMARY}}": "The Royal Commission on Antisemitism and Social Cohesion began its fourth hearing block in Melbourne today, running through Friday and focused specifically on antisemitism at Australian universities, including its impact on Jewish students and staff and how institutions have responded.",

    # Science
    "{{SCI_1_FLAG}}": "💡 PHYSICS · OPTICS · 200-YEAR-OLD EXPERIMENT REVIVED FOR DATA STORAGE",
    "{{SCI_1_HEADLINE}}": "Scientists Use a 200-Year-Old Light Trick to Create Exotic 'Optical Skyrmions'",
    "{{SCI_1_SUMMARY}}": "NTU Singapore researchers found they can generate complex swirling light patterns called optical skyrmions simply by shining a laser at a small disc and exploiting the 200-year-old 'Poisson spot' effect, instead of relying on costly engineered materials. The technique produced four related field patterns at once and could feed into future data storage and communications technology, reported by ScienceDaily on 13 July.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Payday Super Just Landed — Is Your Cash Flow Ready?",
    "{{INSIGHT_BODY}}": "From 1 July, super has to go out with every pay run instead of quarterly, and this week most PAYG employers are hitting their first full pay cycle under the new rules. Treasury has openly flagged this as the reform most likely to catch out small businesses that had quietly been using the old quarterly lag as informal working capital — miss the seven-business-day transfer window and you're up for the shortfall plus interest plus an administrative penalty of up to 60%. An AI-linked payroll and cash-flow forecasting tool can flag the new weekly or fortnightly super hit before it lands rather than after the account's already short, which is worth setting up now rather than after the first missed deadline.",

    # Fun Facts
    "{{FACT_1}}": "The Economist created the tongue-in-cheek 'Big Mac Index' in 1986 to gauge whether currencies are over- or under-valued, comparing the price of a McDonald's Big Mac across countries as a rough proxy for purchasing power parity. It's since been picked up by real economists and even central banks as a genuinely useful, if silly-sounding, benchmark.",

    "{{FACT_2}}": "The famous 'Konami Code' cheat (Up, Up, Down, Down, Left, Right, Left, Right, B, A) first appeared in 1986's Gradius, added by developer Kazuhisa Hashimoto purely so he could playtest his own brutally difficult game without dying constantly. It went on to become gaming's most recognisable cheat code, embedded in dozens of later Konami titles.",

    "{{FACT_3}}": "Monopoly's actual inventor was Lizzie Magie, who patented 'The Landlord's Game' in 1904 to demonstrate how landlords grow rich at tenants' expense under monopoly rents. Parker Brothers later bought the rights and marketed it as a celebration of property empire-building — the exact opposite of the message Magie intended.",

    # Joke
    "{{JOKE_SETUP}}": "What did the upholsterer say when a customer complained about the quote?",
    "{{JOKE_PUNCHLINE}}": "I don't pad the numbers — I pad the furniture.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Genius is one percent inspiration and ninety-nine percent perspiration.\"",
    "{{CLOSING_ATTR}}": "— Thomas Edison",
    "{{CLOSING_MESSAGE}}": "It's a showery, breezy Tuesday in Carrum Downs with more rain easing through midweek before things dry out toward the weekend — a fair excuse to keep today's work indoors and the paperwork moving, especially with Payday Super and the new minimum wage both landing in this week's pay run. If you need a distraction tonight, France and Spain meet in the first World Cup semi-final, with the winner through to Sunday's final.",
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
