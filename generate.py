#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 08 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 8 Sep (BOM)
    "{{WEATHER_1}}": "TUE 8 SEP · 🌤️ Mostly sunny, slight chance of a shower in the SE suburbs overnight · 7–15°C",
    "{{WEATHER_2}}": "WED 9 SEP · 🌧️ Cooler and blustery, showers becoming likely · 7–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 10 SEP · ⛅ Partly cloudy, isolated shower · 7–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 11 SEP · 🌦️ Damp start, showers easing, gusty northerly · 8–15°C",
    "{{WEATHER_5}}": "SAT 12 SEP · ⛈️ Showers, risk of a thunderstorm in the afternoon · 10–17°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Melbourne this morning — today stays mild and mostly dry, but a cooler, blustery change moves through Wednesday ahead of a damp, thundery weekend.",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 KYIV · ZELENSKY EXPECTS THE WAR \"WILL CONTINUE\" INTO WINTER",
    "{{WORLD_1_HEADLINE}}": "Trump to Call Putin, Then Zelensky, After Envoys' Moscow-Kyiv Peace Push Ends Without a Breakthrough",
    "{{WORLD_1_SUMMARY}}": "US envoys Steve Witkoff and Jared Kushner briefed Trump after back-to-back visits to Moscow and Kyiv, with Trump expected to call Putin first and then Zelensky to relay the outcome. Zelensky gave an upbeat account of the talks but said he still expects \"the war will continue\" into winter and is counting on US and European energy and air-defence support — a reminder that despite all the shuttle diplomacy, nothing here has actually changed yet.",
    "{{WORLD_1_URL}}": "https://tsarizm.com/news/eastern-europe/2026/09/07/trump-to-call-putin-first-then-zelensky-after-envoys-deliver-moscow-kyiv-briefing/",

    "{{WORLD_2_FLAG}}": "🌍 MIDDLE EAST · OIL SURGES AS US AND IRAN TRADE STRIKES NEAR HORMUZ",
    "{{WORLD_2_HEADLINE}}": "Brent Crude Tops $97 a Barrel as US and Iran Exchange Strikes Near the Strait of Hormuz",
    "{{WORLD_2_SUMMARY}}": "Brent crude pushed toward $97 a barrel on Monday after the US targeted three Iranian oil tankers over the weekend and Tehran hit back at tankers and vessels linked to Washington, sending tanker traffic through the Strait to its lowest level since May. The Strait carries roughly a fifth of the world's traded oil, so this is exactly the kind of flare-up that keeps turning up at the Australian bowser weeks later.",
    "{{WORLD_2_URL}}": "https://blockonomi.com/crude-oil-surges-past-97-amid-u-s-iran-naval-confrontation-in-hormuz-strait",

    # Economics
    "{{ECON_1_FLAG}}": "💰 RATES · MARKETS NOW PRICE A NEAR-80% CHANCE OF A SEPTEMBER HIKE",
    "{{ECON_1_HEADLINE}}": "Rate Markets Push the Odds of a 29 September RBA Hike to Nearly 80%",
    "{{ECON_1_SUMMARY}}": "Interest-rate markets have moved close to fully pricing a quarter-point RBA hike at the 29 September meeting, with NAB, Deutsche Bank, UBS and Morgan Stanley all now tipping a move to a 4.60% cash rate on the back of inflation stuck at 3.6% on the trimmed mean measure — only Westpac still expects a hold. If a ute, compressor or blast pot purchase is on the cards, the next three weeks look like the cheaper window to lock in finance.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-04/asx-markets-business-news-live-updates/107113674",

    "{{ECON_2_FLAG}}": "⛽ FUEL · BOWSER PRICES STAY NEAR MULTI-MONTH HIGHS",
    "{{ECON_2_HEADLINE}}": "Melbourne Fuel Prices Hold Near Multi-Month Highs as Middle East Tensions Push Crude Back Toward $97",
    "{{ECON_2_SUMMARY}}": "With Brent crude climbing again on the latest US-Iran exchange near Hormuz, terminal gate prices are sitting around 201c/L for unleaded and 237c/L for diesel, and the ACCC says Melbourne's normal six-week discount cycle still hasn't properly restarted since the conflict escalated. Same advice as it's been for months — shop between servos on the day rather than waiting for a cheap trough that isn't turning up.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔐 CYBER AI · GOOGLE, ANTHROPIC AND OPENAI RELEASE RIVAL DEFENDER MODELS",
    "{{TECH_1_HEADLINE}}": "Google, Anthropic and OpenAI All Release Competing \"Cyber\" AI Models Built to Find Software Flaws Before Attackers Do",
    "{{TECH_1_SUMMARY}}": "In the space of a week, Google (Gemini 3.8 Flash Cyber), Anthropic (Claude Mythos 5.1) and OpenAI (Astra) have all released models built specifically to hunt for and patch software vulnerabilities autonomously, alongside new access programs restricting the most capable versions to vetted security teams. It's a genuine leap in defensive capability — but the same autonomous skill for finding weaknesses and writing convincing text is exactly what's making scam emails and fake supplier-invoice requests harder to pick by eye.",
    "{{TECH_1_URL}}": "https://thehackernews.com/2026/09/google-anthropic-and-openai-unveil.html",

    "{{TECH_2_FLAG}}": "📋 PRACTICAL AI · GEMINI NOW REMEMBERS YOUR PREFERENCES ACROSS GOOGLE DOCS, GMAIL AND SHEETS",
    "{{TECH_2_HEADLINE}}": "Google Expands Persistent Gemini \"Custom Instructions\" to Gmail, Sheets, Slides, Chat and Drive",
    "{{TECH_2_SUMMARY}}": "Google has widened its custom-instructions feature — until now limited to Google Docs — across the rest of Workspace, so a business can set its tone, formatting and standard preferences once and have Gemini apply them automatically whenever it drafts a quote, invoice follow-up or email reply. Small, unglamorous, and exactly the kind of low-effort setup worth doing once rather than repeating a preference in every prompt.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏃 PHYSICAL AI · A ROBOT JUST OUTRAN USAIN BOLT'S WORLD RECORD",
    "{{ROBOT_1_HEADLINE}}": "A Humanoid Robot Clocked 9.39 Seconds Over 100 Metres at Beijing's World Humanoid Robot Games — Faster Than Bolt's World Record",
    "{{ROBOT_1_SUMMARY}}": "More than 2,000 humanoid robots competed across 51 events at Beijing's World Humanoid Robot Games last month, headlined by the Tianzhuo team's robot beating Usain Bolt's 9.58-second 100m world record. A fresh analysis this week argues the sprint times are the least important part of the story — the real action is a quieter rulebook now being drafted behind closed doors covering audits, export controls and kill-switches for machines this capable.",
    "{{ROBOT_1_URL}}": "https://americanbazaaronline.com/2026/09/07/march-of-the-robots-next-decade-487650/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Tony Burke Accuses Coalition of \"Leaving Health Policy to Organised Crime\" Over Tobacco Excise",
    "{{AUS_1_SUMMARY}}": "Health Minister Tony Burke used parliament to accuse the Coalition of ceding health policy to organised crime by opposing changes to the tobacco excise, which Labor blames for fuelling the illicit cigarette trade now linked to firebombings and turf wars in several states. Albanese separately spruiked a record month of new-dwelling construction loans in June — a rare bit of good news for anyone quoting residential jobs.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-07/federal-politics-live-blog-sept-7/107122668",

    "{{AUS_2_HEADLINE}}": "Australia and Solomon Islands Reach In-Principle Agreement on New Security and Development Treaty",
    "{{AUS_2_SUMMARY}}": "Canberra and Honiara have reached an in-principle agreement on a new bilateral treaty, though the announcement was overshadowed by a leaked text message from a senior official involved in the negotiations. Part of the broader Pacific-engagement push that's been quietly running alongside the noisier domestic headlines all year.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Coalition Pledges $288 Million to Restore Country Roads and Bridges Funding for Victoria's 48 Rural Councils",
    "{{VIC_1_SUMMARY}}": "The state Coalition has promised to reinstate the Country Roads and Bridges program ahead of November's election, handing each of Victoria's 48 rural and regional councils $1.5 million a year for four years in untied funding for local road and bridge work. If it lands, it's the kind of program that turns into real work orders for tradies servicing those shires — worth watching if you quote jobs outside metro Melbourne.",

    # Science
    "{{SCI_1_FLAG}}": "🦠 BIOLOGY · A \"PAC-MAN\" ENZYME THAT EATS BOTH PLASTIC AND ANTIBIOTICS",
    "{{SCI_1_HEADLINE}}": "Scientists Discover a Soil Bacteria Enzyme That Breaks Down Both Bioplastics and Penicillin",
    "{{SCI_1_SUMMARY}}": "University of Konstanz researchers studying how bacteria digest new plant-based bioplastics found an esterase enzyme — nicknamed the \"Pac-Man enzyme\" — that can also cleave the beta-lactam ring in penicillin-type antibiotics, an unexpected dual ability that ties plastic biodegradation directly to antibiotic resistance. It's early-stage research, but it's the kind of accidental discovery that ends up mattering in two completely unrelated fields at once.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The Big Three AI Labs Just Went to War Over Cybersecurity — Here's the One Habit That Still Beats All of Them",
    "{{INSIGHT_BODY}}": "This week's news that Google, Anthropic and OpenAI have all released rival AI models built to autonomously hunt down software vulnerabilities is genuinely good news for defenders — but the same underlying skill, finding weaknesses and generating convincing, error-free text, is exactly what's making scam emails and fake invoice requests harder to spot by eye than they were even a year ago. You don't need to buy anything to respond to this one. The single habit that still beats all three labs' new models combined is a phone call: any request to change a supplier's bank details, however professional the email looks, gets verified by calling a number you already had on file — never one supplied in the email itself. It costs nothing, takes two minutes, and is still the one thing AI-generated fraud hasn't found a way around.",

    # Fun facts
    "{{FACT_1}}": "In 1785, Scottish doctors John Aitken and James Jeffray invented what's considered the first chainsaw — a hand-cranked chain of small teeth strung between two wooden handles — not for timber, but to cut through pelvic cartilage and bone during difficult childbirths, a procedure called a symphysiotomy that remained in use into the late 1800s.",
    "{{FACT_2}}": "The ring-pull drink can exists because Dayton engineer Ermal Fraze couldn't find a can opener at a family picnic in 1959 and had to prise his beer open on a car bumper — he sketched the pop-top design that same night in his basement workshop and had it patented by 1963.",
    "{{FACT_3}}": "The nail gun traces back to engineer Morris Pynoos's work on Howard Hughes's giant wooden flying boat, the Spruce Goose, in the 1940s — nails were driven in purely to hold glued panels together while the adhesive cured, then pulled out again, and it took another decade before Paslode turned the idea into the pneumatic nailer tradies use today.",

    # Joke
    "{{JOKE_SETUP}}": "An insulation installer was asked how his small business always kept its cash flow steady through even the coldest Melbourne months.",
    "{{JOKE_PUNCHLINE}}": "He said good insulation works both ways — it keeps the cold out and the profits in.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"We must all suffer one of two things: the pain of discipline or the pain of regret.\"",
    "{{CLOSING_ATTR}}": "— Jim Rohn",
    "{{CLOSING_MESSAGE}}": "Tuesday stays mild and mostly dry around Carrum Downs, so it's a good day to get anything outdoors finished before Wednesday's cooler, blustery change moves through. Keep an eye on the Brent crude number this week too — every US-Iran exchange near Hormuz has a habit of turning up at the local bowser about a fortnight later.",
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
