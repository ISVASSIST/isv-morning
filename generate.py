#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 07 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 7 Sep (BOM)
    "{{WEATHER_1}}": "MON 7 SEP · 🌥️ Partly cloudy, medium chance of a shower, mostly overnight · 11–14°C",
    "{{WEATHER_2}}": "TUE 8 SEP · 🌧️ Cloudy, high chance of showers, most likely during the morning · 7–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 9 SEP · ☀️ Mostly sunny, slight chance of an early shower far southeast · 9–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "THU 10 SEP · ⛅ Cloudy, slight chance of a shower · 9–15°C",
    "{{WEATHER_5}}": "FRI 11 SEP · 🌤️ Partly cloudy, slight chance of a shower · 8–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Melbourne this morning — Friday's damaging wind warning was cancelled Saturday night, but a wetter, blustery spell moves through tomorrow before it dries out again from Wednesday.",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 KYIV · TRUMP ENVOYS HOLD \"SUBSTANTIVE\" TALKS AFTER MOSCOW SIT-DOWN",
    "{{WORLD_1_HEADLINE}}": "US Envoys Witkoff and Kushner Hold \"Substantive\" Kyiv Talks With Zelensky After Meeting Putin in Moscow",
    "{{WORLD_1_SUMMARY}}": "Steve Witkoff and Jared Kushner flew into Kyiv on Sunday for talks with President Zelensky, a day after a lengthy Moscow meeting with Vladimir Putin, with both sides reportedly observing a 72-hour pause on strikes against each other's capitals to allow the visits. Witkoff called the sessions \"substantive\" and said he was \"very encouraged,\" though no ceasefire has been signed — still, it's the kind of story that moves oil and diesel prices more than most headlines do.",
    "{{WORLD_1_URL}}": "https://www.upi.com/Top_News/World-News/2026/09/06/ukraine-kushner-witkoff/3791788700900/",

    "{{WORLD_2_FLAG}}": "🌍 MIDDLE EAST · STRAIT OF HORMUZ TENSIONS FLARE AGAIN",
    "{{WORLD_2_HEADLINE}}": "Israeli Strikes Kill Four in Southern Lebanon as Iran Claims Two Tankers Mined in the Strait of Hormuz",
    "{{WORLD_2_SUMMARY}}": "A weekend of Israeli airstrikes on southern Lebanon reportedly killed four people and injured about twenty, adding to a tense few days that also saw Iran claim two tankers were mined in the Strait of Hormuz. The Strait carries roughly a fifth of the world's traded oil, so every flare-up there is one more reason diesel keeps refusing to come back down.",
    "{{WORLD_2_URL}}": "https://www.aa.com.tr/en/world/morning-briefing-sept-6-2026/4048504",

    # Economics
    "{{ECON_1_FLAG}}": "💰 RATES · MARKETS NOW PRICE A 76% CHANCE OF A SEPTEMBER HIKE",
    "{{ECON_1_HEADLINE}}": "Interest Rate Markets Now Price a 76% Chance the RBA Hikes Again on 29 September",
    "{{ECON_1_SUMMARY}}": "Futures markets have pushed the odds of a quarter-point RBA rate rise this month to 76%, with NAB, Deutsche Bank and UBS all now tipping a move to a 4.6% cash rate and a possible peak near 4.8% — only Westpac still holds out for no further rises this year. If you're about to finance a ute, compressor or blast pot, the window to lock in a rate before the board meets is closing fast.",
    "{{ECON_1_URL}}": "https://au.finance.yahoo.com/news/two-big-reasons-australia-is-about-to-see-a-new-interest-rate-reality-set-to-be-significant-190000699.html",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE'S NORMAL PRICE CYCLE STILL FROZEN",
    "{{ECON_2_HEADLINE}}": "Melbourne Fuel Prices Sit Near Multi-Month Highs as the Usual Price Cycle Stays Broken",
    "{{ECON_2_SUMMARY}}": "The ACCC says Melbourne's normal six-week discount cycle has barely run since the Middle East conflict escalated in late February, with terminal gate prices around 197c/L for unleaded and 231c/L for diesel and retail prices tracking higher again from there. Without a reliable cheap trough to time a big fill around, shopping between servos on the day is about the only lever left.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🖥️ PRACTICAL AI · GPT-6 ASTRA NOW LANDING FOR BUSINESS USERS",
    "{{TECH_1_HEADLINE}}": "OpenAI's GPT-6 Astra Starts Rolling Out to ChatGPT Business and Enterprise Accounts This Week",
    "{{TECH_1_SUMMARY}}": "OpenAI's new GPT-6 Astra model is built around genuine \"computer use\" — operating software and finishing multi-step office tasks like building a spreadsheet or working through a template document — and after landing with Plus and Pro users last week is now extending to Business, Enterprise and API access. It's a step away from chatbot novelty and toward AI that can actually sit down and do the paperwork.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html",

    "{{TECH_2_FLAG}}": "⚛️ INDUSTRIAL AI · REACTING FASTER THAN ANY HUMAN OPERATOR CAN",
    "{{TECH_2_HEADLINE}}": "Princeton's PACMAN AI System Can Now Control Fusion Reactor Plasma in 20 Milliseconds Flat",
    "{{TECH_2_SUMMARY}}": "Princeton Plasma Physics Laboratory has demonstrated an AI framework that reads reactor sensor data and issues correcting commands in about 20 milliseconds, catching plasma instabilities roughly 200 milliseconds before they'd otherwise hit — well beyond any human's reaction time. It's a clean example of AI taking over split-second, safety-critical equipment monitoring, the same category of job slowly filtering down into smaller industrial gear.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🚜 PHYSICAL AI · EXCAVATORS NOW DIGGING WITH NOBODY IN THE CAB",
    "{{ROBOT_1_HEADLINE}}": "Unmanned Excavators Are Now Doing Paid Commercial Earthworks on US Construction Sites",
    "{{ROBOT_1_SUMMARY}}": "Bedrock Robotics' retrofit kit — cameras, LiDAR and sensors bolted onto ordinary excavators — is now running genuinely unmanned cut-and-fill work on active sites in Texas and Nevada for contractors Sundt and Zachry, auto-stopping if a person or object strays too close. A human only needs to step in \"relatively rarely,\" the company says — an early but unmistakable sign of where AI-driven automation is heading in physical site work.",
    "{{ROBOT_1_URL}}": "https://www.foxnews.com/tech/autonomous-excavators-digging-empty-cabs",

    # Australia
    "{{AUS_1_HEADLINE}}": "Coalition Proposes Jail Time for Flag Burning and a Plebiscite Lock on Australia Day",
    "{{AUS_1_SUMMARY}}": "The federal Coalition wants a new offence carrying up to 12 months' jail for burning the Australian flag to incite hatred, plus a requirement that any future change to January 26 as the national day go to a plebiscite first; Opposition Leader Angus Taylor denied it was aimed at winning back One Nation voters. It's at least the eighth such federal push in Australian history — none of the previous seven got up.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/the-proposal-that-could-make-flag-burning-illegal-in-australia/u3wmvvhfi",

    "{{AUS_2_HEADLINE}}": "Government to Introduce Social Media Algorithm \"Opt-Out\" Laws to Parliament This Week",
    "{{AUS_2_SUMMARY}}": "Federal legislation due in parliament this week would force social media platforms to give users an opt-out from their recommendation algorithms and hold them responsible for minimising harm — a separate push to Senator Hanson-Young's own private member's bill on the same issue. Worth watching if the business leans on social ads or organic reach for leads; the rules for reaching customers online may be about to shift again.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Labor Commits $550 Million to Fix the Western Freeway Through Melbourne's Fastest-Growing Corridor",
    "{{VIC_1_SUMMARY}}": "The Victorian government has pledged $550 million — on top of $1 billion already promised federally — to widen the Western Freeway between Melton and Caroline Springs, upgrading three interchanges and adding a new one at Mount Cottrell Road as Melton's population heads toward 456,000 within two decades. Handy context if you're quoting jobs anywhere along that growth corridor — expect roadworks before it gets better.",

    # Science
    "{{SCI_1_FLAG}}": "🧬 GENETICS · LIFE'S FOUR-LETTER CODE JUST DOUBLED IN THE LAB",
    "{{SCI_1_HEADLINE}}": "Scientists Get a Natural Enzyme to Correctly Read an Eight-Letter Genetic Alphabet, Twice the Size of Ours",
    "{{SCI_1_SUMMARY}}": "UC San Diego researchers used cryo-electron microscopy to show that E. coli's RNA polymerase — the enzyme every living thing uses to read DNA — can accurately transcribe a synthetic eight-letter \"Hachimoji\" genetic code, doubling the four letters (A, T, C, G) all known natural life relies on. It won't change biology overnight, but it's a genuine foundation stone for future synthetic-biology diagnostics.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Empty Cabs, Real Earthworks — What Unmanned Excavators Mean for a Business Like Yours",
    "{{INSIGHT_BODY}}": "This week's news that Bedrock Robotics has excavators doing genuine, paid civil earthworks in the US with nobody in the operator's seat isn't really about excavators — it's a signal about how fast AI-driven sensor retrofits are moving from lab demo to commercial reality on heavy equipment. You're not buying an autonomous excavator any time soon, and neither is most of the trades sector — but the same underlying shift (cheap cameras plus AI models turning \"dumb\" machinery into something that can monitor itself and flag problems) is already showing up in far more affordable forms: AI-based compressor and equipment monitoring that flags a failing seal before it costs you a job, and AI site-camera systems that can spot a missing hard hat or an unsafe access point automatically. The lesson isn't \"robots are coming for your job\" — it's that the cost of adding a layer of AI-powered awareness to existing gear is falling fast, and the businesses that adopt cheap versions of it early will be running leaner than competitors who wait until it's mainstream. Worth a five-minute look this week at what an entry-level AI monitoring add-on would cost for your compressor or blast pot fleet.",

    # Fun facts
    "{{FACT_1}}": "Melbourne's Athenaeum Theatre premiered \"The Story of the Kelly Gang\" on Boxing Day 1906 — running over an hour, it's recognised as the world's first full-length narrative feature film, at a time when most films ran about 12 minutes.",
    "{{FACT_2}}": "The aircraft \"black box\" flight recorder was invented at Melbourne's Fisherman's Bend by scientist David Warren in the 1950s — Australian officials initially showed little interest, and it took an English manufacturer and a fatal 1960 Mackay air crash before Australia became the first country in the world to make cockpit voice recording mandatory.",
    "{{FACT_3}}": "The world's first traffic lights, installed outside Britain's Houses of Parliament in December 1868, used gas lamps for their night-time signals — they were removed within a year after a gas leak exploded at the base and badly injured the policeman operating them.",

    # Joke
    "{{JOKE_SETUP}}": "A mobile phone repair technician was asked how his small business kept a full appointment book, even in the depths of a Melbourne winter.",
    "{{JOKE_PUNCHLINE}}": "He said screens crack all year round — but his quotes never do.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Fortune favors the prepared mind.\"",
    "{{CLOSING_ATTR}}": "— Louis Pasteur",
    "{{CLOSING_MESSAGE}}": "Carrum Downs gets a shot at showers overnight before Tuesday turns properly wet, so it's worth locking down anything loose on site this evening if gear's staying out. The more interesting story to watch this week is happening a long way from here — Trump's envoys landing in both Moscow and Kyiv on the same weekend is the kind of quiet diplomatic movement that's easy to scroll past, but occasionally ends up mattering more than the headline gave it credit for.",
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
