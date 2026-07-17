#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 18 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 18 Jul (BOM)
    "{{WEATHER_1}}": "SAT 18 · 🌫️🌦️ Morning fog, shower developing · 8–14°C",
    "{{WEATHER_2}}": "SUN 19 · 🌫️☀️ Morning fog, then sunny · 6–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 20 · ❄️🌫️☀️ Frost & fog patches, mostly sunny · 5–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "TUE 21 · 🌦️ Shower or two, cooler · 6–12°C",
    "{{WEATHER_5}}": "WED 22 · 🌦️ Partly cloudy, shower chance · 7–16°C",
    "{{WEATHER_ALERT}}": "⚠ MORNING FOG & SHOWERS TODAY · FROST PATCHES MONDAY · NO SEVERE WARNINGS ACTIVE",

    # World
    "{{WORLD_1_FLAG}}": "🇶🇦🇰🇼 GULF STATES · IRAN STRIKES SIXTH NIGHT · QATAR & KUWAIT INTERCEPT FRESH BARRAGE",
    "{{WORLD_1_HEADLINE}}": "Qatar and Kuwait Intercept Fresh Iranian Strikes as US Bombs Iran for a Sixth Consecutive Night",
    "{{WORLD_1_SUMMARY}}": "US Central Command launched a sixth straight night of airstrikes on Iranian targets around Bandar Abbas, while Kuwait's air defences intercepted 32 drones since dawn and Qatar shot down further incoming fire over Doha, wounding a child with falling shrapnel. Shipping through the Strait of Hormuz has all but stopped, with just three vessels transiting in the past 24 hours compared with roughly 110 a day before the conflict began, and there's still no sign either side is ready to de-escalate.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/07/16/world/live-news/iran-war-trump",

    "{{WORLD_2_FLAG}}": "🇨🇳🤖 SHANGHAI · XI LAUNCHES 29-NATION AI BLOC · RIVAL TO US-LED AI RULES",
    "{{WORLD_2_HEADLINE}}": "Xi Jinping Launches 29-Nation AI Alliance, Positions China as the World's Affordable AI Partner",
    "{{WORLD_2_SUMMARY}}": "Speaking at Shanghai's World AI Conference, Xi Jinping unveiled the World AI Cooperation Organisation, a new 29-country bloc including Indonesia, Brazil, South Africa and Russia, and pledged 5,000 free AI training slots for developing nations over the next five years. He argued AI development shouldn't be a 'solo performance' by one country — a clear jab at Washington — as the US and China now openly compete over whose AI rules and hardware the rest of the world ends up standing on.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/7/17/chinas-xi-jinping-launches-new-ai-alliance-what-is-it",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AT THE BOWSER · ACCC WEEKLY REPORT · EXCISE CUT HALVED, HORMUZ CRISIS ADDS PRESSURE",
    "{{ECON_1_HEADLINE}}": "ACCC's Latest Fuel Report Confirms Prices Still Climbing as Excise Relief Halves and Hormuz Crisis Drags On",
    "{{ECON_1_SUMMARY}}": "The ACCC's 19th weekly fuel report, released July 17, shows capital-city unleaded averaging 170.1 cents a litre and diesel 191.9 cents, both up sharply since the temporary fuel excise cut dropped from 32 cents to 16 cents a litre on July 1. Darwin is now the most expensive capital at 215 cents a litre, and with the relief scheme due to expire August 2 and the Strait of Hormuz still effectively closed to shipping, there's no clear signal the bowser eases off before spring.",
    "{{ECON_1_URL}}": "https://www.ibtimes.com.au/rising-petrol-prices-australia-causes-consumer-tips-1872184",

    "{{ECON_2_FLAG}}": "📊 BUSINESS MOOD · NAB & WESTPAC SURVEYS · CONFIDENCE CLAWS BACK AS FEARS EASE",
    "{{ECON_2_HEADLINE}}": "Business Confidence and Consumer Sentiment Both Lift as Worst-Case Middle East Fears Fail to Materialise",
    "{{ECON_2_SUMMARY}}": "Westpac's July 17 briefing shows consumer sentiment up 4.1% for the month while NAB's business confidence index jumped nine points, both a relief rally after fears of a full-blown oil shock and unemployment spike didn't play out. The catch: consumers are still deeply pessimistic by historical standards and remain sensitive to the Hormuz conflict, which flared again mid-survey — a reminder that any bounce in trade inquiries right now is fragile, not a trend.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · GEMINI 3.5 PRO GOES LIVE TODAY · GOOGLE'S BIGGEST REBUILD YET",
    "{{TECH_1_HEADLINE}}": "Google's Gemini 3.5 Pro Launches Today After a Ground-Up Rebuild, Reportedly Packing a 2-Million-Token Context Window",
    "{{TECH_1_SUMMARY}}": "Google DeepMind's next flagship model is rolling out today after engineers scrapped the original build entirely and restarted pretraining following structural failures in recursive tool-calling. Leaks point to a 2-million-token context window and a new 'Deep Think' reasoning tier — landing the same week Shanghai's AI conference opens with Xi Jinping in person, making today arguably the single biggest AI news day of the year so far.",
    "{{TECH_1_URL}}": "https://www.techtimes.com/articles/320308/20260713/gemini-35-pro-targets-july-17-after-full-rebuild-every-spec-remains-unconfirmed.htm",

    "{{TECH_2_FLAG}}": "📈 AI ADOPTION · NAB BUSINESS PULSE · 42% OF AUSSIE SMES NOW USING AI",
    "{{TECH_2_HEADLINE}}": "42% of Australian Small Businesses Are Now Using AI Tools, NAB Data Shows — But Trust Is Still the Biggest Barrier",
    "{{TECH_2_SUMMARY}}": "NAB's latest Business Pulse data shows 42% of Australian SMEs are now using AI tools day-to-day, with another 14% planning to adopt, led by property services, finance and business services. The bigger story is who's missing out: about 65% of non-adopters say it's a lack of trust or a preference to keep humans in control, and one in five say they simply don't know where to start — which is exactly the gap a single well-chosen tool, tried on one job this month, can start to close.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳🦾 FACTORY FLOOR · CHINA'S HUMANOID PUSH · THOUSANDS DEPLOYED TO LOGISTICS & BATTERY PLANTS",
    "{{ROBOT_1_HEADLINE}}": "China Sends Thousands of Humanoid Robots Into Factories and Logistics Hubs to Learn on the Job",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics startups are deploying humanoids into real workplaces faster than anywhere else, with Robotera machines working a dozen logistics hubs and Galbot robots doing heavy lifting at a battery plant for CATL, backed by a Beijing push to get 10,000 units into service by year's end. It's a shift from demo-stage 'look what it can do' videos to actual repetitive shift work — with China explicitly using the real-world data to train the robots' underlying AI faster than competitors can.",
    "{{ROBOT_1_URL}}": "https://www.insurancejournal.com/news/international/2026/07/16/877906.htm",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Summons Laos Ambassador Over 'Bitterly Disappointing' Charges in Backpacker Methanol Deaths",
    "{{AUS_1_SUMMARY}}": "Canberra summoned Laos' ambassador on Friday, saying it was 'deeply frustrated and bitterly disappointed' that Lao authorities are pursuing only minor charges — carrying up to a year's jail and a $1,600 fine — over the 2024 methanol poisoning deaths of Melbourne teenagers Holly Bowles and Bianca Jones. Foreign Minister Penny Wong says she'll press the issue directly with her Lao counterpart at next week's ASEAN meeting in Manila, after the victims' families said they were 'furious' at the proposed charges.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/podcast-episode/laos-ambassador-summoned-amid-methanol-victims-families-devastation-midday-news-bulletin-17-july-2026/xoid0c5db",

    "{{AUS_2_HEADLINE}}": "Canberra to Set Up a National AI Office and World-First Data Centre Standards",
    "{{AUS_2_SUMMARY}}": "The federal government is establishing an Office of AI within Prime Minister and Cabinet and drafting Australian Standards for AI data centres, forcing big operators to fund their own power connections and hit water-efficiency targets, with legislation planned for 2027. It's aimed at the hyperscale end of the market, but it's a signal that the regulatory ground under every AI tool your business uses is about to start shifting.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Liberals Formally Dump Moira Deeming as a Candidate Ahead of November's Election",
    "{{VIC_1_SUMMARY}}": "The Victorian Liberal Party's state executive has voted to disendorse first-term MP Moira Deeming from her Western Metropolitan Legislative Council spot, following her allegation that colleague Matthew Guy 'headlocked' her at a community event — an account CCTV footage appeared to contradict. Deeming withdrew a Supreme Court challenge to the move earlier this week; the party will now restart candidate selection for the seat.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 GUT HEALTH · CAMBRIDGE STUDY · 39 SWEETENERS TESTED, MOST CHANGE YOUR GUT BACTERIA",
    "{{SCI_1_HEADLINE}}": "Cambridge Scientists Test 39 Sweeteners and Find Most Alter Gut Bacteria Growth in the Lab",
    "{{SCI_1_SUMMARY}}": "University of Cambridge researchers grew 25 species of gut bacteria and exposed each to 39 common sweeteners — natural and artificial — finding around three-quarters changed how at least one species grew, with some slowing beneficial strains. They also found more than 100 cases where a sweetener behaved differently when combined with common medications or caffeine, with one combination — isosteviol and the antidepressant duloxetine — proving especially disruptive to gut diversity.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Canberra's Building an AI Office — Get Your Business Ahead of the Rules, Not Behind Them",
    "{{INSIGHT_BODY}}": "This week's federal announcement of a national Office of AI and legislated data centre standards is aimed at the big end of town, but regulation has a habit of trickling down to every business using the tools it's built for. Right now there's no compliance burden on a trades operator using AI for quotes, scheduling or customer chat — but that's the easiest time to start doing it properly: know which tools you use, where the data goes, and who's actually reviewing what the AI produces before it reaches a client. Get that habit locked in now, while it's optional, and you'll barely notice when it stops being optional.",

    # Fun Facts
    "{{FACT_1}}": "The QWERTY keyboard layout was designed in the 1870s partly to slow typists down — spacing out commonly paired letters so the mechanical arms on early typewriters wouldn't jam and lock up mid-sentence.",

    "{{FACT_2}}": "The Snowy Mountains Scheme, completed in 1974 after 25 years of work by labourers from more than 30 countries, remains the largest engineering project ever undertaken in Australia — 16 dams, 7 power stations and 225 kilometres of tunnels dug largely by hand and gelignite.",

    "{{FACT_3}}": "The first commercial microwave oven, Raytheon's 1947 Radarange, stood 1.8 metres tall, weighed 340 kilograms and cost about $5,000 — roughly $70,000 today — which is why it took another 20 years to shrink into something that would fit on a kitchen bench.",

    # Joke
    "{{JOKE_SETUP}}": "A stonemason's apprentice asked why he always finished every quote exactly on time, never early, never late.",
    "{{JOKE_PUNCHLINE}}": "He said, 'Mate, I've been laying stone long enough to know — rush a wall and it falls down, rush a client and they never call back.'",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Opportunities don't happen. You create them.\"",
    "{{CLOSING_ATTR}}": "— Chris Grosser",
    "{{CLOSING_MESSAGE}}": "It's a foggy, showery start to Saturday in Carrum Downs — 8–14°C, with the fog likely to lift by mid-morning and frost rolling back in for Monday. Business confidence just clawed back nine points and consumer sentiment's up too, but fuel's still climbing and the Hormuz crisis shows no sign of easing, so treat the bounce as fragile rather than a trend — and if Gemini 3.5 Pro lands as promised today, it's worth a look over the weekend coffee.",
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
