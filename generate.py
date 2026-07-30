#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 31 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 31 Jul (BOM)
    "{{WEATHER_1}}": "FRI 31 · ☁️ Cloudy, shower or two easing tonight · 8–15°C",
    "{{WEATHER_2}}": "SAT 01 AUG · 🌧️ Showers, most likely SE suburbs · 5–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 02 AUG · 🌫️ Partly cloudy, isolated shower later · 6–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 03 AUG · 🌫️ Partly cloudy, slight chance of a shower · 6–13°C",
    "{{WEATHER_5}}": "TUE 04 AUG · ☀️ Partly cloudy, becoming mostly sunny · 5–14°C",
    "{{WEATHER_ALERT}}": "⚠ NO SEVERE WEATHER WARNINGS CURRENTLY ACTIVE FOR VICTORIA",

    # World
    "{{WORLD_1_FLAG}}": "🇪🇸🇫🇷 EUROPE · WILDFIRE EVACUEES RETURN HOME · FRESH HEATWAVE THREATENS NEW OUTBREAKS",
    "{{WORLD_1_HEADLINE}}": "Spain and France Let Wildfire Evacuees Go Home, But a Fresh Heatwave Threatens to Reignite the Crisis",
    "{{WORLD_1_SUMMARY}}": "Tens of thousands of residents in Spain and France began returning home this week after fire crews brought blazes near Madrid and in France's Bordeaux region under control, following evacuation orders that had displaced more than 300,000 people and killed at least one person. Authorities in both countries are warning the danger isn't over, with a fresh heatwave sweeping back across southern Europe threatening to reignite new outbreaks just as the region catches its breath.",
    "{{WORLD_1_URL}}": "https://www.france24.com/en/europe/20260730-spain-eases-evacuations-as-france-battles-fresh-wildfires-amid-new-heatwave",

    "{{WORLD_2_FLAG}}": "🇮🇷🇺🇸 MIDDLE EAST · US LAUNCHES 'HEAVY WAVE' OF STRIKES ON IRAN · KUWAIT HIT, ONE KILLED",
    "{{WORLD_2_HEADLINE}}": "US Hits Dozens of Iranian Targets Overnight, Hours After an Iranian Strike Kills a Worker in Kuwait",
    "{{WORLD_2_SUMMARY}}": "US Central Command carried out a two-hour 'heavy wave' of strikes on dozens of Iranian Revolutionary Guard sites — including missile factories, command centres and coastal defences — in response to Iran's attempted attack on US forces in the region. Hours earlier, an Iranian strike hit a Chinese-owned building in northern Kuwait, killing one worker, after Jordan's air defences shot down five missiles fired from Iran a day earlier.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/7/30/us-launches-another-round-of-attacks-on-iran",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺📊 SMALL BUSINESS · SALES GROWTH COOLS TO 6.5% · RATES AND FUEL COSTS START TO BITE",
    "{{ECON_1_HEADLINE}}": "Australian Small Business Sales Growth Cools as Higher Rates and Fuel Costs Start to Bite, Xero Data Shows",
    "{{ECON_1_SUMMARY}}": "New Xero Small Business Insights data released this week shows sales growth easing to 6.5 per cent year-on-year in the June quarter, down from a two-year high of 7.9 per cent in Q1, with hospitality, retail and arts & recreation slowing hardest while construction, mining and utilities kept outperforming. It's an early signal that the cost pressures households have felt all year are starting to flow through to trade and discretionary spending too.",
    "{{ECON_1_URL}}": "https://www.marketscreener.com/news/new-xero-data-australian-small-business-growth-cools-as-interest-rate-rises-and-fuel-prices-bite-ce7f51d3df88f726",

    "{{ECON_2_FLAG}}": "🇦🇺⛽ FUEL · DIESEL ALREADY AT 227¢/L · EXCISE DISCOUNT ENDS SUNDAY, ADDING MORE",
    "{{ECON_2_HEADLINE}}": "Diesel's Already Pushing 227 Cents a Litre — And That's Before Sunday's Excise Hike Even Lands",
    "{{ECON_2_SUMMARY}}": "The Australian Institute of Petroleum's weekly price monitoring shows the national average diesel price has climbed to 227.2 cents a litre and unleaded to 182.0 cents, even before the government's fuel excise discount expires at midnight Sunday and adds roughly another 17 cents a litre to both. For any business running a ute and trailer between jobs, it's worth locking in a fill this weekend before the price floor moves again.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI COSTS · OPENAI CUTS GPT-5.6 PRICES BY UP TO 80% · CHEAPEST FRONTIER AI YET",
    "{{TECH_1_HEADLINE}}": "OpenAI Slashes GPT-5.6 Prices by Up to 80% as Competition From Cheaper Rivals Intensifies",
    "{{TECH_1_SUMMARY}}": "OpenAI cut the price of its GPT-5.6 Luna model by 80 per cent and Terra by 20 per cent this week, crediting efficiency gains from the model's own code-optimisation work, with the discount flowing straight through to ChatGPT Work and Codex usage limits. It's part of a broader price war as rivals push out cheaper models — good news for any small business already using AI tools for quoting, admin or client comms, since the same subscription now stretches further.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/07/30/open-ai-price-cut-gpt.html",

    "{{TECH_2_FLAG}}": "🤖 GOOGLE · GEMINI NOTEBOOK SPOTTED BUILDING APPS FROM YOUR OWN FILES · NOT YET LIVE",
    "{{TECH_2_HEADLINE}}": "Google Is Quietly Testing a Gemini Notebook Feature That Turns Your Own Files Into a Working App",
    "{{TECH_2_SUMMARY}}": "Code spotted inside Gemini Notebook points to a new 'App' artifact sitting alongside its existing audio, video and slide-deck outputs — letting users type a prompt and turn their own uploaded documents into an interactive tool, such as a simple dashboard or calculator, rather than just a written summary. Nothing is public yet and no release date has been set, but it points to where note-taking AI is heading: from summarising your paperwork to actually doing something useful with it.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · ACTUATORS MAKE UP 56% OF A HUMANOID ROBOT'S WEIGHT · NEW SUPPLY-CHAIN REPORT",
    "{{ROBOT_1_HEADLINE}}": "New Industry Report Reveals Actuators — Not Chips — Make Up More Than Half a Humanoid Robot's Weight",
    "{{ROBOT_1_SUMMARY}}": "A new IDTechEx report breaks down the 'muscles' behind humanoid robot movement, finding that a typical humanoid packs around 31 actuators excluding hands, and that these electric, hydraulic and pneumatic components alone account for roughly 56 per cent of the robot's total weight. With humanoid unit sales forecast to grow at a 47 per cent compound annual rate over the next decade, the report flags a fast-emerging supply-chain opportunity for manufacturers who can build the motors, gears and materials these robots depend on to walk, lift and grip.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/07/30/trends-and-outlook-for-actuators-the-muscles-behind-humanoid-motion/103750/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia's Commonwealth Games Gold Tally Hits 47 as Big Athletics Finals Land Today at Scotstoun",
    "{{AUS_1_SUMMARY}}": "Australia now leads the Glasgow medal table with 47 gold, 21 silver and 35 bronze heading into today's athletics finals, including sprinter Lachlan Kennedy's national-record 100m silver — the country's first men's sprint medal in 64 years — and defending champion Nina Kennedy in the women's pole vault. The Games wrap up Sunday.",
    "{{AUS_1_URL}}": "https://www.olympics.com/en/news/australia-commonwealth-games-2026-schedule-31-july",

    "{{AUS_2_HEADLINE}}": "Markets All But Rule Out an August Rate Rise as Big Banks Start Tipping Cuts in 2027",
    "{{AUS_2_SUMMARY}}": "Following this week's softer inflation read, financial markets have pushed the odds of an RBA rate hike at the 11 August meeting down to near zero, with CBA, NAB and ANZ now expecting the cash rate to hold steady for the rest of 2026 — though Westpac isn't ruling out one more rise. Three of the big four banks are now pencilling in the first rate cuts for mid-2027, a shift in tone that will matter to any small business carrying equipment or vehicle finance.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "New Premier Ben Carroll's First Big Call: A Royal Commission Into Victoria's Corruption-Plagued Big Build",
    "{{VIC_1_SUMMARY}}": "Days after being sworn in, Ben Carroll used his first press appearance as Premier to announce a royal commission into corruption and organised-crime allegations engulfing Victoria's $109 billion Big Build infrastructure program — claims reported to have cost taxpayers around $15 billion and that helped bring down his predecessor. It's a high-stakes opening move just four months out from November's state election.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 EVOLUTION · GALÁPAGOS 'GIANT DAISIES' CAUGHT EVOLVING IN REAL TIME · NEW SPECIES FORMING NOW",
    "{{SCI_1_HEADLINE}}": "More Than 150 Years After Darwin's Finches, Galápagos Daisies Are Rewriting the Same Evolutionary Story",
    "{{SCI_1_SUMMARY}}": "Researchers who sequenced the genomes of 396 Galápagos giant daisy (Scalesia) plants across all 15 known species found that separate island populations independently evolved the same heat-tolerant, deeply lobed leaf shape — but each lineage got there using a different combination of genes. The genetic differences between isolated populations are now large enough that scientists say new daisy species may be forming on the islands right now — published 29 July 2026.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Construction and Utilities Are Still Booming While Retail Stalls — Is Your Client Mix Built for a Two-Speed Economy?",
    "{{INSIGHT_BODY}}": "This week's Xero data shows Australian small business sales growth cooling to 6.5 per cent overall, but the slowdown is nowhere near even — construction sales are up 10.8 per cent year-on-year and utilities up 13.1 per cent, while hospitality and retail are barely growing above 2 to 3 per cent. For a trades business that can work across both commercial infrastructure and residential or retail fit-outs, now's the moment to look at your job pipeline and lean into the sectors still spending — an AI-assisted CRM or job-tracking tool can quickly show you which client types have kept booking work through 2026's slowdown, and which have gone quiet, before next quarter's numbers make the pattern impossible to ignore.",

    # Fun facts
    "{{FACT_1}}": "Decaffeinated coffee was discovered by accident in 1903, when a shipment of coffee beans arriving in Germany was soaked in seawater during a rough voyage — merchant Ludwig Roselius noticed the salt water had stripped out much of the caffeine while leaving the flavour largely intact, leading to the first commercial decaf, Kaffee Hag, by 1906.",
    "{{FACT_2}}": "In 1997, IBM's Deep Blue became the first computer to beat a reigning world chess champion, Garry Kasparov, in a full match — Kasparov accused IBM of cheating and demanded a rematch, but IBM dismantled the machine rather than agree to one.",
    "{{FACT_3}}": "Titanic's hull was fastened by two different riveting methods — machine-driven steel rivets along the straight midsection, and hand-driven wrought-iron rivets hammered in by four-person crews around the curved bow and stern — and some engineers believe that metallurgical difference helped the iceberg damage spread as far as it did.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the lift technician's small business never miss a scheduled maintenance call?",
    "{{JOKE_PUNCHLINE}}": "With clients trapped between floors, 'I'll get to it eventually' was never going to cut it.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The best preparation for tomorrow is doing your best today.\"",
    "{{CLOSING_ATTR}}": "— H. Jackson Brown Jr.",
    "{{CLOSING_MESSAGE}}": "It's a showery start to the weekend that should ease off tonight, with Australia chasing more athletics gold at Scotstoun today as the Commonwealth Games heads toward Sunday's close. New Premier Ben Carroll's first big call — a royal commission into the Big Build — lands right as the working week wraps up, and it's worth topping up the ute before Sunday midnight, when the fuel excise discount runs out for good.",
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
