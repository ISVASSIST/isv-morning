#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 30 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 30 Aug (BOM)
    "{{WEATHER_1}}": "SUN 30 · ⛅ Partly cloudy, mild · 8–16°C",
    "{{WEATHER_2}}": "MON 31 · 🌦️ Partly cloudy, slight shower chance · 7–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 1 SEP · ☀️ Morning fog clearing to sunny, unusually warm · 9–22°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "WED 2 SEP · 🌧️ Cloudy, showers most likely morning, cooler · 10–17°C",
    "{{WEATHER_5}}": "THU 3 SEP · 🌦️ Showers, windy northwesterly change · 9–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula. Melbourne just had its warmest winter on record, and Tuesday's forecast 22°C will be the warmest first day of spring in five years — before showers and a gusty north-westerly change return from midweek.",

    # World
    "{{WORLD_1_FLAG}}": "🇳🇵 NEPAL · FLOOD DEATH TOLL CLIMBS, NEARLY 3,000 MISSING",
    "{{WORLD_1_HEADLINE}}": "Nepal-Tibet Flood Death Toll Hits 676 as Nearly 3,000 Remain Missing",
    "{{WORLD_1_SUMMARY}}": "Satellite imagery shows a huge chunk of Himalayan glacier ice broke away and slammed into a river below, triggering flash floods that have now killed at least 676 people in Nepal and Tibet; Australian woman Cara Severino has been found safe, but dozens of other Australians remain unaccounted for.",
    "{{WORLD_1_URL}}": "https://www.abc.net.au/news/2026-08-29/death-toll-rises-as-rescuers-work-through-flood-devastation/107092742",

    "{{WORLD_2_FLAG}}": "🇳🇴 NORWAY · TENS OF THOUSANDS MOURN KING HARALD V",
    "{{WORLD_2_HEADLINE}}": "Tens of Thousands Lay Flowers for King Harald V as Norway Crowns King Haakon VIII",
    "{{WORLD_2_SUMMARY}}": "A sea of flowers covered the square outside Oslo's royal palace on Saturday as Norwegians paid tribute to King Harald V, a day after his death at 89; his son, Crown Prince Haakon, has become King Haakon VIII and addressed the nation for the first time as monarch.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/world/europe/tens-thousands-mourn-king-harald-v-oslo-norway-enters-new-royal-era-rcna594999",

    # Economics
    "{{ECON_1_FLAG}}": "💱 AUD · DOLLAR HITS 3-MONTH HIGH ON RATE HIKE BETS",
    "{{ECON_1_HEADLINE}}": "Australian Dollar Jumps to a 3-Month High as Markets Price In a September Rate Hike",
    "{{ECON_1_SUMMARY}}": "The Aussie dollar climbed to around 72 US cents — its best level since May — after hotter-than-expected July inflation data pushed the market-implied chance of a September RBA hike to about 50%, with Goldman Sachs now tipping the cash rate to reach 4.60% by November; a stronger dollar eases the cost of imported tools and equipment even as borrowing costs look set to rise.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-08-28/asx-markets-business-news-live-updates/107087998",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE UNLEADED STILL AVERAGING OVER $2/L",
    "{{ECON_2_HEADLINE}}": "Melbourne Petrol Still Averaging Above $2 a Litre as Full Excise Bites",
    "{{ECON_2_SUMMARY}}": "With the fuel excise cut fully unwound since 3 August, Melbourne's average unleaded price is sitting around 206.5 cents a litre — some stations charging close to $2.80 — and national prices are running about 13.6 cents higher than a month ago, adding real pressure to every kilometre a trades vehicle covers between jobs.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "⚔️ AI SUPPLY CHAIN · OPENAI CUTS OFF CURSOR AFTER SPACEX TAKEOVER",
    "{{TECH_1_HEADLINE}}": "OpenAI to Cut Cursor's Access to Its Models After SpaceX Acquisition",
    "{{TECH_1_SUMMARY}}": "OpenAI has told Cursor it will lose access to OpenAI models by 12 November, roughly three months after SpaceX completed its takeover of the coding-tool maker — a reminder that any business built on a single AI vendor's goodwill can lose access almost overnight if the ownership or terms change.",
    "{{TECH_1_URL}}": "https://www.businesstoday.in/technology/story/openai-vs-elon-musk-why-cursor-is-losing-access-to-openai-models-from-november-12-552049-2026-08-29",

    "{{TECH_2_FLAG}}": "🇦🇺 AI POLICY · AUSTRALIA'S 'SLIDING DOORS' MOMENT ON AI",
    "{{TECH_2_HEADLINE}}": "Australia Weighs How to Cash In on the AI Data Centre Boom",
    "{{TECH_2_SUMMARY}}": "With global tech giants racing to build data centres locally, the federal government is launching a push to get major Australian companies buying more homegrown AI technology, arguing the country's appeal as a data-centre destination gives it rare leverage to secure cheaper computing power for local businesses.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 HUMANOIDS · CHINESE AUTOMAKERS CHASE TESLA INTO ROBOTS",
    "{{ROBOT_1_HEADLINE}}": "Chinese Automakers Race Tesla Into Humanoid Robots as a New Profit Line",
    "{{ROBOT_1_SUMMARY}}": "BYD has unveiled its own humanoid, Xiao Di, for showroom duty, Chery's robotics arm AiMOGA is reportedly prepping an IPO, and Xpeng is said to be planning to pour up to US$13.8 billion into its Iron humanoid programme — with Changan, GAC, Li Auto, SAIC and Seres all chasing the same bet as Tesla that robots, not cars, could be the next big margin driver.",
    "{{ROBOT_1_URL}}": "https://techcrunch.com/2026/08/28/chinese-automakers-are-following-teslas-bet-that-robots-are-the-next-big-profit-machine/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Melbourne and Sydney Just Had Their Warmest Winter on Record",
    "{{AUS_1_SUMMARY}}": "Bureau of Meteorology data confirms Melbourne and Sydney recorded their warmest winter since records began in the 1850s, with Canberra also hitting its highest-ever winter temperatures — and forecasters say a scorching spring is likely to follow.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-29/spring-scorcher-to-follow-record-warm-winter-australia-weather/107090824",

    "{{AUS_2_HEADLINE}}": "Bird Flu Detected in a Dolphin for the First Time as Outbreak Tops 350 Events",
    "{{AUS_2_SUMMARY}}": "South Australian authorities have confirmed the country's first H5N1 detection in a dolphin, found dead at Goolwa, as Australia's bird flu outbreak — now more than 350 confirmed events across over 20 species — continues to spread from the coast into inland waterways.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Premier Ben Carroll Scraps $134,000 Dan Andrews Statue",
    "{{VIC_1_SUMMARY}}": "New Victorian Premier Ben Carroll has cancelled a taxpayer-funded bronze statue of predecessor Daniel Andrews outside Treasury Place, saying \"gratitude does not require a taxpayer-funded statue,\" after polling found almost three-quarters of Victorians opposed the plan.",

    # Science
    "{{SCI_1_FLAG}}": "👁️ VISION · EYE DROPS RESTORE SIGHT IN BLIND MICE",
    "{{SCI_1_HEADLINE}}": "Light-Activated Eye Drops Restore Sight in Completely Blind Mice",
    "{{SCI_1_SUMMARY}}": "A Barcelona-led research consortium has developed light-activated drugs that mimic degenerated photoreceptor cells, restoring light-driven behaviour in mice blinded by conditions similar to macular degeneration — with two of the most promising compounds working as simple eye drops, pointing to a possible future treatment path that needs no gene therapy or implant.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The Top 1% of Businesses Now Spend $7,400 a Month Per Employee on AI — You Don't Need to Get Close",
    "{{INSIGHT_BODY}}": "New data on US business AI spending shows the most aggressive corporate adopters now spend over $7,400 per employee per month on AI tools, more than 600 times what a typical business spends. It's a striking number, but it's also the wrong benchmark for a small trades operation — those companies are running AI research labs, not answering phones and chasing invoices. A handful of well-chosen, low-cost tools covering quoting, scheduling and admin can free up hours a week for a fraction of a fraction of that spend; the businesses actually falling behind aren't the ones with small budgets, they're the ones that haven't started at all.",

    # Fun facts
    "{{FACT_1}}": "The word \"ketchup\" didn't start with tomatoes — it comes from \"kê-tsiap,\" a fermented fish sauce from the Hokkien-speaking regions of China, brought back by British traders in the 17th century; tomatoes weren't added to Western recipes until the early 1800s.",
    "{{FACT_2}}": "The \"blue chip\" used to describe a safe, reliable company on the stock market borrows its name from poker, where the blue chip has traditionally carried the highest value of any colour on the table.",
    "{{FACT_3}}": "Alan Turing never claimed his 1950 \"Turing Test\" proved machines could think — he proposed it as a practical stand-in for a question he considered unanswerable, originally calling it simply \"the imitation game.\"",

    # Joke
    "{{JOKE_SETUP}}": "Why did the mobile mechanic's small business never miss a job?",
    "{{JOKE_PUNCHLINE}}": "Because his workshop went wherever the breakdown was.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"What we think, we become.\"",
    "{{CLOSING_ATTR}}": "— Buddha",
    "{{CLOSING_MESSAGE}}": "It's a mild, partly cloudy last Sunday of winter in Carrum Downs, with Tuesday set to bring the warmest first day of spring in five years before showers and a blustery change roll back through midweek — a fair window to get outdoor jobs done before spring properly turns it on. With the dollar firming and a September rate move now live in the mix, it's a good week to line up quotes on any imported gear before either one moves further.",
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
