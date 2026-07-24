#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 25 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 25 Jul (BOM)
    "{{WEATHER_1}}": "SAT 25 · 🌦️ Shower or two, cool · 7–13°C",
    "{{WEATHER_2}}": "SUN 26 · ☁️🌧️ Cloudy, chance of a shower · 6–13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 27 · 🌫️☀️ Morning fog patches, then sunny · 5–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "TUE 28 · ☁️ Mostly cloudy, isolated shower · 7–14°C",
    "{{WEATHER_5}}": "WED 29 · 🌦️ Shower or two, cooler · 6–12°C",
    "{{WEATHER_ALERT}}": "⚠ NO SEVERE WEATHER WARNINGS ACTIVE FOR METRO MELBOURNE",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷⚓ STRAIT OF HORMUZ · NEIGHBOURS BUILD AROUND THE BLOCKADE · PIPELINE PROJECTS ACCELERATE",
    "{{WORLD_1_HEADLINE}}": "Iran Weaponised the Strait of Hormuz — Now Its Neighbours Are Building Around It",
    "{{WORLD_1_SUMMARY}}": "With the Strait of Hormuz still the single biggest flashpoint of the conflict, Gulf states are quietly fast-tracking overland pipeline routes that bypass the strait entirely, redrawing the region's energy map for good. US forces carried out a 13th consecutive night of strikes on Iranian military targets, Iran has rejected a ceasefire proposal carried by Iraq's prime minister, and an Omani delegation is now in Tehran attempting to broker a resolution over the strait's future.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/07/24/politics/middle-east-energy-map-redrawn-pipeline-projects-mcgurk-vis",

    "{{WORLD_2_FLAG}}": "🇺🇸💱 TRADE · NEW TARIFFS HIT 60 ECONOMIES · CANBERRA AMONG THOSE PUSHING BACK",
    "{{WORLD_2_HEADLINE}}": "Trump Imposes New Tariffs on 60 Trading Partners as Old Duties Expire",
    "{{WORLD_2_SUMMARY}}": "The US has begun collecting fresh 10–12.5% duties on goods from 60 economies — covering 99.4% of US imports — after a broader tariff was ruled unlawful by the Supreme Court. Washington is citing forced-labour enforcement as the justification, but trading partners from Canberra to Brasília have rejected that reasoning and say they'll keep negotiating rather than retaliate outright.",
    "{{WORLD_2_URL}}": "https://www.cnbc.com/2026/07/24/trump-global-tariffs-trade-imbalance-forced-labor.html",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AT THE BOWSER · DIESEL TOPS 214¢/L · ACCC'S 20TH WEEKLY REPORT CONFIRMS THE JUMP",
    "{{ECON_1_HEADLINE}}": "Diesel Climbs Past 214 Cents a Litre as Excise Restoration Bites Hard",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly fuel report, out yesterday, shows average retail petrol across the five biggest cities hit 179.5 cents a litre and diesel 214.9 cents by July 22 — up 28.0 and 41.4 cents respectively since June 30. Melbourne recorded the country's biggest diesel jump of any capital, up 43.1 cents, as the partial restoration of the fuel excise continues to work its way through bowser prices.",
    "{{ECON_1_URL}}": "https://www.indexbox.io/blog/accc-fuel-price-report-july-2026-shows-increases-after-excise-restoration/",

    "{{ECON_2_FLAG}}": "📉 OUTLOOK · DELOITTE CUTS GROWTH FORECAST · SLOWEST STRETCH SINCE THE '90S RECESSION",
    "{{ECON_2_HEADLINE}}": "Deloitte Slashes Australia's Growth Forecast to 1.3%, Warns of Longest Sub-2% Stretch Since the '90s",
    "{{ECON_2_SUMMARY}}": "Deloitte Access Economics has cut its 2026-27 growth forecast from 1.9% to 1.3%, citing higher interest rates and the still-unresolved Middle East oil shock, and expects unemployment to average 4.9% and possibly touch 5%. It's a soft-demand backdrop worth planning around — a good year to focus on winning work through service and reliability rather than chasing volume.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · CLAUDE OPUS 5 LAUNCHES · HALF THE PRICE OF ANTHROPIC'S PREVIOUS FLAGSHIP",
    "{{TECH_1_HEADLINE}}": "Anthropic Launches Claude Opus 5 at Half the Price, With a Dial for Cost vs Capability",
    "{{TECH_1_SUMMARY}}": "Anthropic's new flagship model launched yesterday priced the same as its predecessor despite big performance gains, and adds a toggle letting users choose low, medium or high 'effort' to balance cost against how hard the model works on a task. It's a direct response to the loudest complaint from business AI users all year — the bills — and another sign that day-to-day AI tools are getting cheaper, not more expensive, even as they get more capable.",
    "{{TECH_1_URL}}": "https://fortune.com/2026/07/24/anthropic-debuts-claude-opus-5-with-feature-that-lets-users-toggle-between-cost-and-capability/",

    "{{TECH_2_FLAG}}": "⚖️ BIG TECH · EU FINES GOOGLE $1B · FIRST MAJOR DIGITAL MARKETS ACT PENALTY",
    "{{TECH_2_HEADLINE}}": "Europe Fines Google $1 Billion in First Major Enforcement of Its Digital Markets Act",
    "{{TECH_2_SUMMARY}}": "The European Commission has fined Google roughly $1 billion (€890 million) for favouring its own services in search results and restricting how Play Store developers direct users to cheaper deals elsewhere. Google has 60 days to change its practices or face penalties of up to 5% of its global turnover — a reminder that the platforms most small businesses rely on for leads and reviews are under heavier regulatory pressure than they've ever faced.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · SAMSUNG ENTERS THE RACE · NEW HUMANOID DIVISION, FACTORY-TESTED AI ALREADY IN HAND",
    "{{ROBOT_1_HEADLINE}}": "Samsung Launches a Dedicated Humanoid Robot Division, Says Its Robot AI Is Already Factory-Tested",
    "{{ROBOT_1_SUMMARY}}": "Samsung has consolidated years of scattered robotics work into a single new business unit and declared humanoid robots its next major push, arriving with an AI control system its research arm says already makes 17 decisions a second on factory floors. It's the latest sign that humanoid robotics is shifting from Silicon Valley hype to a genuine contest between the world's biggest manufacturers — Samsung, Hyundai, Tesla and a fast-growing field of Chinese makers all now building for the factory floor, not the demo stage.",
    "{{ROBOT_1_URL}}": "https://www.techtimes.com/articles/321464/20260724/samsung-launches-humanoid-robot-division-robot-brain-ai-already-tested-factories.htm",

    # Australia
    "{{AUS_1_HEADLINE}}": "Labor Delegates Vote to Strengthen Gambling Reform Ahead of National Conference Push",
    "{{AUS_1_SUMMARY}}": "Delegates at Labor's national conference unanimously backed stronger gambling regulation yesterday, agreeing to boost regulators' powers and examine cutting ties between sport and gambling advertising aimed at young people — though it stops short of the national regulator recommended in the 2023 Murphy report.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/podcast-episode/labor-backs-gambling-reform-not-regulator-evening-news-bulletin-24-july-2026/nkh1359xi",

    "{{AUS_2_HEADLINE}}": "China Tells Australia to ‘Back Off’ as South China Sea Tensions Build at ASEAN Summit",
    "{{AUS_2_SUMMARY}}": "Foreign Minister Penny Wong raised concerns over Chinese military activity in the South China Sea at the ASEAN Foreign Ministers' meetings in Manila, which wrapped up yesterday, prompting a pointed rebuke from Beijing even as Chinese Foreign Minister Wang Yi publicly talked up regional cooperation.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "North Melbourne Host St Kilda at Marvel Stadium in Today's Big Saturday Fixture",
    "{{VIC_1_SUMMARY}}": "It's a 1:05pm bounce at Marvel Stadium as North Melbourne take on St Kilda in today's marquee AFL clash — good excuse to get jobs wrapped up early and the tools packed away before kick-off.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 SPACE · CHINESE ORBITER'S RARE VANTAGE POINT · NEW VIEW OF AN INTERSTELLAR VISITOR",
    "{{SCI_1_HEADLINE}}": "China's Tianwen-1 Mars Orbiter Captures Rare Images of Interstellar Comet 3I/ATLAS",
    "{{SCI_1_SUMMARY}}": "Newly published observations show China's Tianwen-1 spacecraft imaged interstellar comet 3I/ATLAS from Mars orbit using its HiRIC camera — a vantage point well outside the comet's orbital plane that's giving scientists a rare, different-angle look at how its tail and coma changed shape as it passed through the inner solar system.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Trump's New Tariffs Landed Overnight — How AI Can Help You Reprice Imported Materials Before Costs Bite",
    "{{INSIGHT_BODY}}": "New US tariffs on 60 economies kicked in overnight, and while they're aimed at trade partners not tradies, tariff shocks like this ripple through global supply chains fast — imported abrasives, coatings, fasteners and equipment can all get more expensive within weeks as suppliers reprice. Before your next big materials order, try feeding your supplier list into an AI tool and asking it to flag which of your regular imported line items are most exposed to overseas price and currency swings. A 15-minute check now beats discovering a 10% cost blowout halfway through a job you've already quoted at yesterday's prices.",

    # Fun facts
    "{{FACT_1}}": "The Commonwealth Games, which opened this week in Glasgow, began life in 1930 as the 'British Empire Games' in Hamilton, Ontario — just 11 countries and about 400 athletes took part, versus the 74 nations competing this year.",
    "{{FACT_2}}": "A standard oil barrel is fixed at 42 US gallons for a reason that has nothing to do with chemistry — 19th-century Pennsylvania oil producers settled on that size because it matched the leak-resistant fish and herring barrels already being mass-produced, and the standard simply stuck worldwide.",
    "{{FACT_3}}": "Aztec and Maya societies used cacao beans as actual currency long before Europeans arrived — a rabbit reportedly cost around 10 beans, and counterfeiters were known to hollow out real beans and refill them with dirt to pass as fakes.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the commercial cleaning contractor never lose a tender?",
    "{{JOKE_PUNCHLINE}}": "She was the only one who actually read the site inspection report before pricing the job.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Action is the foundational key to all success.\"",
    "{{CLOSING_ATTR}}": "— Pablo Picasso",
    "{{CLOSING_MESSAGE}}": "It's a cool, showery Saturday to kick off the weekend — good excuse to get the quotes out of the way indoors before North Melbourne take on St Kilda at Marvel Stadium this afternoon. Showers stick around through Sunday before easing into a foggy but sunnier Monday.",
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
