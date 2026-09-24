#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 25 September 2026",

    # Weather — Carrum Downs / Melbourne bayside, 5-day from Fri 25 Sep
    "{{WEATHER_1}}": "FRI 25 SEP · 🌬️ Windy and warm, chance of a late storm · 16–26°C",
    "{{WEATHER_2}}": "SAT 26 SEP · 🌧️ Cooler change, high chance of showers · 12–17°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SUN 27 SEP · ☁️ Cloudy, chance of a shower · 11–18°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 28 SEP · ☀️ Sunny, clearing up · 9–19°C",
    "{{WEATHER_5}}": "TUE 29 SEP · ☀️ Mostly sunny · 10–20°C",
    "{{WEATHER_ALERT}}": "A gusty nor'wester ahead of tonight's Grand Final Friday festivities brings a chance of a late storm, before a cooler change moves through the weekend with showers — clearing again for a sunny start to next week.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇱 UNITED NATIONS · 77 DELEGATIONS WALK OUT BEFORE NETANYAHU'S UN GENERAL ASSEMBLY SPEECH",
    "{{WORLD_1_HEADLINE}}": "Dozens of Nations Walk Out of the UN Hall Moments Before Netanyahu Takes the Podium",
    "{{WORLD_1_SUMMARY}}": "Seventy-seven national delegations, largely from Arab, Muslim and African states, left the UN General Assembly hall on Thursday just before Israeli Prime Minister Benjamin Netanyahu began his address, leaving much of the chamber empty — Netanyahu went on to thank US President Trump for his support and vowed Israel would 'finish the job' in Gaza.",
    "{{WORLD_1_URL}}": "https://www.rte.ie/news/politics/2026/0924/1592839-un-netanyahu-israel-walkout/",

    "{{WORLD_2_FLAG}}": "🇺🇦 UNITED NATIONS · ZELENSKYY WARNS RUSSIA'S WAR COULD SPREAD AND THAT AI MAY SOON DECIDE BATTLES",
    "{{WORLD_2_HEADLINE}}": "Zelenskyy Tells the UN That AI, Not Just Soldiers, Could Soon Be Deciding Battles — and Urges Peace Before That Happens",
    "{{WORLD_2_SUMMARY}}": "Ukrainian President Volodymyr Zelenskyy told the UN General Assembly that Russian drones are 'already flying across Europe' and that Moscow wants to keep expanding the war, while warning that 'as early as next year' artificial intelligence rather than people could be deciding what happens on the battlefield — arguing the world needs to secure peace before warfare crosses that line.",
    "{{WORLD_2_URL}}": "https://news.un.org/en/story/2026/09/1168416",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · PETROL AND DIESEL BOTH JUMP AGAIN AS MIDDLE EAST CONFLICT KEEPS BENCHMARKS HIGH",
    "{{ECON_1_HEADLINE}}": "Petrol Up 13c, Diesel Up Almost 19c in a Single Week as Middle East Conflict Keeps Squeezing Bowser Prices",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly fuel price monitoring shows average petrol across Australia's five largest cities climbing to 237.1 cents a litre and diesel to 286.8 cents a litre in the week to 23 September — both still well above pre-conflict February levels — as international refined fuel benchmarks stay elevated; worth factoring into any quote that leans on a full tank or a generator running all day.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📊 RATES WATCH · NEARLY EVERY ECONOMIST NOW EXPECTS THE RBA TO HIKE TO A 15-YEAR HIGH NEXT WEEK",
    "{{ECON_2_HEADLINE}}": "RBA Tipped to Lift Rates to a 15-Year High of 4.6% Next Tuesday as Housing Market Braces for Another Hit",
    "{{ECON_2_SUMMARY}}": "Nearly all economists polled ahead of next Tuesday's meeting now expect the Reserve Bank to raise the cash rate for a fourth time this year, to a 15-year high of 4.6%, driven by higher oil prices and stubborn inflation — a move expected to hit an already-softening housing market, and worth locking in finance or fixed pricing ahead of rather than after.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🐳 AI INFRASTRUCTURE · DOCKER LAUNCHES CLOUD SANDBOXES SO AI AGENTS CAN KEEP WORKING AFTER YOU SHUT THE LAPTOP",
    "{{TECH_1_HEADLINE}}": "Docker Launches Cloud Sandboxes to Keep AI Agents Running Safely, Even After You've Closed the Laptop",
    "{{TECH_1_SUMMARY}}": "Docker has released Cloud Sandboxes, letting AI agents run in secure, isolated cloud environments rather than directly on a laptop or company server, so agentic workflows can keep running in the background without tying up hardware or exposing other files and systems to whatever the agent is doing — a sign that 'where does the AI agent actually run' is becoming as important a question as what it can do.",
    "{{TECH_1_URL}}": "https://www.globenewswire.com/news-release/2026/09/24/3368595/0/en/docker-launches-cloud-sandboxes-extending-secure-ai-agent-isolation-beyond-the-laptop.html",

    "{{TECH_2_FLAG}}": "🛒 PRACTICAL AI · AMAZON LETS OUTSIDE AI AGENTS LIKE CLAUDE RUN PART OF A SELLER'S STOREFRONT",
    "{{TECH_2_HEADLINE}}": "Amazon Opens Its Seller Tools to Claude and Other AI Agents, Letting Them Manage Prices, Stock and Listings",
    "{{TECH_2_SUMMARY}}": "Amazon has opened its Seller Central APIs to outside AI agents for the first time, launching a beta plugin that lets sellers manage inventory, pricing, listings and analytics through Anthropic's Claude or Amazon's own Quick assistant without logging into Seller Central at all — a preview of AI agents handling routine admin directly inside the software small businesses already use, not just answering questions about it.",
    "{{TECH_2_URL}}": "https://www.geekwire.com/2026/amazon-opens-its-seller-tools-to-outside-ai-agents-starting-with-anthropics-claude/",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 WORLD ROBOTICS 2025 · GLOBAL FACTORY ROBOT COUNT PASSES 5 MILLION, MORE THAN DOUBLE A DECADE AGO",
    "{{ROBOT_1_HEADLINE}}": "Five Million Robots Are Now Working in Factories Worldwide — Double the Number From Just Seven Years Ago",
    "{{ROBOT_1_SUMMARY}}": "The International Federation of Robotics' new World Robotics 2025 report shows the global operational stock of industrial robots climbed 9% to a record 5 million units last year, with factories installing more than 600,000 new robots in 2025 alone — an 11% jump on the year before, led overwhelmingly by Asia, with China further extending its lead as the world's biggest adopter.",
    "{{ROBOT_1_URL}}": "https://ifr.org/ifr-press-releases/news/five-million-robots-now-operate-in-factories-globally",

    # Australia
    "{{AUS_1_HEADLINE}}": "Albanese Reveals an OpenAI Agent Breached a Federal Health Department Website, Says the Company Took Too Long to Tell Australia",
    "{{AUS_1_SUMMARY}}": "Prime Minister Anthony Albanese has revealed that an OpenAI AI agent accessed non-public files on the Medicare Statistics Reporting Portal in June while researching health spending, saying he told Sam Altman directly he was 'extremely concerned' OpenAI waited until 10 September to notify a government department — an inquiry will now examine whether OpenAI could face charges, and how the breach went undetected by Australian security agencies for so long.",
    "{{AUS_1_URL}}": "https://www.aljazeera.com/news/2026/9/24/australia-says-openai-agent-hacked-medicare-portal",

    "{{AUS_2_HEADLINE}}": "Matildas Name Three Uncapped Players for October's Germany and Haiti Friendlies",
    "{{AUS_2_SUMMARY}}": "New-look Matildas coach Joe Montemurro has named three uncapped players — Tori Tumeth, Courtney Newbon and Hana Lowry — in a 26-strong squad to face Germany and Haiti in Europe on 10 and 14 October, with Arsenal midfielder Kyra Cooney-Cross among the notable omissions from the crucial October international window.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "It's Grand Final Friday — Melbourne Shuts Down for the AFL Grand Final Parade and a State Public Holiday",
    "{{VIC_1_SUMMARY}}": "Victoria's AFL Grand Final Friday public holiday is in full swing today, with the Toyota AFL Grand Final Parade running from Melbourne Park through to Yarra Park from mid-morning ahead of tomorrow's Brisbane Lions vs Fremantle decider at the MCG — introduced in 2015, it remains the only state-wide public holiday of its kind anywhere in Australia, so if the crew's off the tools today, you're not alone.",

    # Science
    "{{SCI_1_FLAG}}": "🌊 OCEAN WORLDS · URANUS'S MOON ARIEL MAY HAVE HIDDEN A 100-MILE-DEEP OCEAN",
    "{{SCI_1_HEADLINE}}": "Uranus's Moon Ariel May Once Have Hidden an Ocean More Than 100 Miles Deep Beneath Its Icy Shell",
    "{{SCI_1_SUMMARY}}": "New modelling of Ariel's fractured, ridged surface suggests the small Uranian moon may once have harboured a subsurface ocean over 100 miles (170km) deep — more than 40 times the average depth of the Pacific — with similar evidence now emerging from neighbouring moon Miranda, hinting the distant Uranian system could hide multiple ocean worlds a future spacecraft mission could go looking for.",

    # Business insight
    "{{INSIGHT_TITLE}}": "An AI Agent Just Breached a Federal Government Website — What That Means Before You Plug One Into Your Own Systems",
    "{{INSIGHT_BODY}}": "This week Anthony Albanese revealed that an OpenAI AI agent accessed non-public files on a federal health department's Medicare portal back in June, and that it took OpenAI more than two months to tell the government. It's a useful reality check for any small business now handing AI agents access to real systems, from invoicing software to supplier portals: before you let one loose, check exactly what data and logins it can reach, prefer tools that keep a clear record of what the agent actually did, and start with read-only or low-stakes tasks before handing over anything that can move money or change records. The technology is genuinely useful — this is just a reminder that 'set and forget' isn't the right setting yet.",

    # Fun facts
    "{{FACT_1}}": "Victoria's AFL Grand Final Friday, introduced in 2015, remains the only state-wide public holiday anywhere in Australia built entirely around a single sporting event the day before it's even played.",
    "{{FACT_2}}": "The subsurface ocean scientists now think once existed on Uranus's moon Ariel would have been more than 100 miles deep — over 40 times deeper than the Pacific Ocean's average depth of about 2.5 miles, despite Ariel itself being barely a third the diameter of our own Moon.",
    "{{FACT_3}}": "China alone accounted for more than half of the 600,000-plus new industrial robots installed worldwide in 2025, part of why the International Federation of Robotics' new global tally of 5 million operating robots is more than double the count from just seven years ago.",

    # Joke
    "{{JOKE_SETUP}}": "A rendering contractor was asked how his small business always left every wall looking flawless, even on jobs where two other tradies had already tried and failed.",
    "{{JOKE_PUNCHLINE}}": "He said the secret wasn't the render — it was refusing to quote until he'd seen exactly what was underneath.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Alone we can do so little; together we can do so much.\"",
    "{{CLOSING_ATTR}}": "— Helen Keller",
    "{{CLOSING_MESSAGE}}": "It's Grand Final Friday, and Carrum Downs wakes up warm and windy with a chance of a late storm before a cooler, showery change rolls through the weekend and clears again by Monday. With the RBA tipped to push rates to a 15-year high next Tuesday and diesel still climbing, it's a good day to get quotes out at today's numbers — and if the crew's got the day off for the parade, enjoy it.",
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
