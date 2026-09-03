#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 04 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 4 Sep (BOM)
    "{{WEATHER_1}}": "FRI 4 SEP · 🌦️ Partly cloudy, medium chance of a shower in the early morning · 6–14°C",
    "{{WEATHER_2}}": "SAT 5 SEP · 🌧️ Partly cloudy, high chance of showers in the afternoon and evening, breezy nor'wester · 7–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 6 SEP · 🌧️ Cloudy, very high chance of rain, strong to gale-force north to north-easterly winds · 10–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 7 SEP · 🌧️ Cloudy, very high chance of rain easing later, gusty north to north-westerly winds · 10–14°C",
    "{{WEATHER_5}}": "TUE 8 SEP · 🌤️ Clearing, slight chance of an early shower, winds becoming light · 8–15°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula. A wet, blustery spell moves through this weekend and into Monday before clearing by Tuesday.",

    # World
    "{{WORLD_1_FLAG}}": "🇪🇬 CAIRO · XI VISITS EGYPT FOR FIRST TIME IN A DECADE",
    "{{WORLD_1_HEADLINE}}": "China's Xi Meets Egypt's Sisi in Cairo, Marking Beijing's First State Visit to the Country in 10 Years",
    "{{WORLD_1_SUMMARY}}": "Xi Jinping held talks with President Abdel Fattah el-Sisi in Cairo this week, urging Middle Eastern countries to oppose external interference and back regional dialogue on peace and security as both leaders discussed the six-month US-Israel war on Iran; the two nations also signed an agreement to launch a third phase of the Suez Canal industrial zone, deepening Beijing's roughly $10 billion in investment across Egypt.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/09/03/nx-s1-5954184/chinas-xi-visits-egypt-for-the-first-time-in-a-decade",

    "{{WORLD_2_FLAG}}": "🇺🇸 NEW YORK · MADURO CLAIMS HEAD-OF-STATE IMMUNITY IN DRUG CASE",
    "{{WORLD_2_HEADLINE}}": "Ousted Venezuelan Leader Nicolás Maduro Asks US Judge to Dismiss Drug Trafficking Case on Immunity Grounds",
    "{{WORLD_2_SUMMARY}}": "Lawyers for Nicolás Maduro and his wife, Cilia Flores, filed papers in Manhattan federal court arguing the judge must reject the indictment because it cannot be brought against a foreign head of state; the pair have been held in a Brooklyn jail since US forces seized them in a night-time raid on their Caracas home in January, with oral arguments on the dismissal motion now set for 17 November.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/09/03/g-s1-141764/ex-venezuelan-president-nicolas-maduro-and-wife-seek-to-end-drug-charges-case-on-immunity-grounds",

    # Economics
    "{{ECON_1_FLAG}}": "📈 ASX · MARKET SNAPS BACK AS HORMUZ FEARS EASE",
    "{{ECON_1_HEADLINE}}": "ASX 200 Snaps Three-Day Losing Streak as Strait of Hormuz Tensions Ease and Banks Rebound",
    "{{ECON_1_SUMMARY}}": "The ASX 200 climbed back toward 9,011 points on Thursday, supported by an absence of fresh US strikes on Iran for the first time in three sessions and a rebound in the big banks after August's sharp sell-off, while gold and mining stocks also firmed as some of the heat came out of the recent rally in energy prices and bond yields.",
    "{{ECON_1_URL}}": "https://www.marketindex.com.au/news/asx-200-live-today-thursday-3rd-september",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE BOWSERS STILL RUNNING ABOVE 200C/L",
    "{{ECON_2_HEADLINE}}": "Melbourne Unleaded Still Averaging Above 200c/L, With the Normal Price Cycle Yet to Properly Return",
    "{{ECON_2_SUMMARY}}": "Melbourne drivers are paying an average of roughly 203–206.5c/L for unleaded, with the cheapest sites near 186.5c/L in Preston and diesel still elevated, as the region's usual predictable discounting cycle remains largely disrupted months on from the Middle East conflict — NRMA modelling shows regular unleaded up close to 50c/L since excise was fully restored in early August, making it worth comparing prices before a big fill rather than assuming a cheap patch is coming.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤝 AI DEALS · NVIDIA CONFIRMS $12.9BN HUGGING FACE ACQUISITION",
    "{{TECH_1_HEADLINE}}": "Nvidia Confirms It Will Buy AI Model Hub Hugging Face for $12.9 Billion",
    "{{TECH_1_SUMMARY}}": "Nvidia confirmed it is acquiring Hugging Face, the platform hosting roughly three million AI models, a million applications and half a million datasets used by more than 18 million developers, in a deal signalling how central open AI infrastructure has become to the chipmaker's strategy — a sign of just how much consolidation is happening at the plumbing layer underneath the AI tools small businesses are starting to use.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/09/03/nvidia-confirms-it-will-buy-hugging-face-for-12-9-billion/",

    "{{TECH_2_FLAG}}": "🎙️ PRACTICAL AI · GOOGLE ADDS VOICE FEATURES TO GMAIL, DOCS AND KEEP",
    "{{TECH_2_HEADLINE}}": "Google Launches Conversational AI Voice Features Inside Gmail, Docs and Keep",
    "{{TECH_2_SUMMARY}}": "Google has rolled out voice-driven AI features letting users ask questions about their inbox or documents and complete tasks with natural-language dictation directly inside Gmail, Docs and Keep, without switching to a separate chatbot app — a small but genuinely practical step for anyone who'd rather talk through a job note or reply than type one out on a phone.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 HUMANOID ROBOTS · CAN A ROBOT 'HOLD THE ROOM'?",
    "{{ROBOT_1_HEADLINE}}": "Robotics Firm Realbotix Launches Pilot Putting Humanoid Robots in Front of Live Audiences for a European Telco",
    "{{ROBOT_1_SUMMARY}}": "Realbotix has begun a pilot with a major European telecommunications company testing whether its humanoid robots can work as presenters, hosts and brand ambassadors at live events and product demonstrations, not just in one-on-one interactions — an early test of humanoid robots moving from labs and warehouses into customer-facing, audience-scale roles.",
    "{{ROBOT_1_URL}}": "https://www.globenewswire.com/news-release/2026/09/03/3355897/0/en/onconetix-acquisition-target-realbotix-launches-pilot-with-leading-european-telecommunications-company-to-deploy-humanoid-robots-in-live-presentations-and-events.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "SA Ambulance Ramping Hits a Record High as Independent Review Finds the State's Health System Has 'Deteriorated'",
    "{{AUS_1_SUMMARY}}": "Patients spent 5,891 hours ramped outside South Australian public hospitals in August, a new record, landing the same day an independent review tabled in state parliament found SA's public health system has 'deteriorated' since 2022, with the share of metro patients handed over from paramedics within 30 minutes collapsing from more than 92% a decade ago to under half today.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-03/ambulance-ramping-hits-record-high-at-sa-hospitals/107110560",

    "{{AUS_2_HEADLINE}}": "Small Businesses Turn to Blue Lights to Spot Fake Notes as Counterfeit Cash Seizures Surge",
    "{{AUS_2_SUMMARY}}": "Business owners are increasingly scanning banknotes with blue lights at the till as the Australian Border Force reports a sharp jump in counterfeit currency entering the country, with more than $2.5 million in fake notes seized across 330 packages since last year and a single August haul of $747,000 — authorities say the fakes, mostly arriving from Asia, are of increasing quality and some now bear 'strong similarities' to genuine notes.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Man Fights for Life After Melton Tobacconist Firebombing Goes Wrong",
    "{{VIC_1_SUMMARY}}": "A man in his 20s is in a critical condition after police say a targeted firebombing at a Melton tobacconist early Thursday went wrong, engulfing him in flames after accelerant was allegedly poured inside the shop and ignited; investigators believe the men involved were burned in the fire they are accused of starting, and Victoria Police are still hunting two others believed to be linked to the attack.",

    # Science
    "{{SCI_1_FLAG}}": "🛰️ SPACE FIRST · INDIA ATTEMPTS ITS FIRST GEOSYNCHRONOUS EARTH-IMAGING LAUNCH",
    "{{SCI_1_HEADLINE}}": "ISRO Attempts a Milestone Launch, Sending Its First Imaging Satellite Toward Geosynchronous Orbit",
    "{{SCI_1_SUMMARY}}": "India's space agency ISRO launched its GSLV-F17 rocket carrying the EOS-05 Earth observation satellite in the early hours of Friday, aiming to place a satellite in geosynchronous orbit for the first time in the country's history — a feat ISRO has never previously pulled off — with the 2,367kg spacecraft designed to keep a high, steady watch over the same patch of Earth for continuous imaging.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Google Just Put a Voice Assistant Inside Gmail and Docs — A Genuinely Low-Effort Way to Try AI On the Tools",
    "{{INSIGHT_BODY}}": "Google this week rolled out conversational AI voice features directly inside Gmail, Docs and Keep, letting you dictate a message, ask a question about your inbox, or draft a document just by talking, without downloading a separate chatbot app. For a small trades business that hasn't touched AI yet, that's a much lower bar than it sounds: no new software, no learning curve, no bill — just talking to tools you already have open every day. The obvious use is a quote or job note dictated between jobs while your hands are still dirty, or a client email drafted by voice while you're driving between sites (hands-free, parked, or via a passenger — never while driving). It won't replace your invoicing software, but as a way to actually start using AI rather than reading about it, talking to Gmail is about as close to zero-risk as it gets.",

    # Fun facts
    "{{FACT_1}}": "The first commercial sunscreen was cooked up in a backyard in Adelaide in 1932, when chemist H.A. Milton Blake used a kerosene heater to brew batches of French-perfumed 'sunburn vanishing cream' — his small operation grew into Hamilton Laboratories, which still makes sunscreen today.",
    "{{FACT_2}}": "The safety pin was invented in 1849 by New York mechanic Walter Hunt, who twisted a length of brass wire while trying to think of a way to pay off a $15 debt — he sold the patent rights for just $400 and never made another cent from an invention that's still unchanged in every sewing kit today.",
    "{{FACT_3}}": "Nobody actually knows who invented the stubby holder — Australians have claimed it since at least the 1970s, with rival stories crediting a fisherman insulating his beer with old drink cans and a 1980s pioneer who first used wetsuit neoprene, and the true inventor will probably never be settled.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the hot water system installer's small business never run cold?",
    "{{JOKE_PUNCHLINE}}": "Because he never let a quote go lukewarm — every job got followed up before it had the chance to cool off.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"When you can do the common things in life in an uncommon way, you will command the attention of the world.\"",
    "{{CLOSING_ATTR}}": "— George Washington Carver",
    "{{CLOSING_MESSAGE}}": "It's Friday in Carrum Downs, with just a medium chance of an early shower before a wet, blustery spell rolls through the weekend and into Monday — worth getting outdoor jobs wrapped up today if you can. Over in Cairo, Xi Jinping's first visit to Egypt in a decade is reshaping the week's world news, while closer to home, business owners scanning banknotes with blue lights over a counterfeit cash surge is a timely reminder to keep an eye on what's coming across the counter this week.",
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
