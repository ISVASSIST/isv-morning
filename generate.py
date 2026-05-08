#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 09 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Sat 9 May
    "{{WEATHER_1}}": "Sat 9 May · Partly cloudy · 14°C/8°C",
    "{{WEATHER_2}}": "Sun 10 May · Mostly cloudy · 14°C/7°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Mon 11 May · Showers · 15°C/8°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "Tue 12 May · Budget Day · 14°C/9°C",
    "{{WEATHER_5}}": "Wed 13 May · Mostly cloudy · 15°C/8°C",
    "{{WEATHER_ALERT}}": "❄ Cold start — polar blast easing",

    # World
    "{{WORLD_1_FLAG}}": "🦠 HEALTH — GLOBAL",
    "{{WORLD_1_HEADLINE}}": "Hantavirus Cruise Ship Arrives at Canary Islands as Death Toll Reaches Three",
    "{{WORLD_1_SUMMARY}}": "The MV Hondius, a cruise ship with eight confirmed or suspected hantavirus cases and three deaths on board, is due to dock in Tenerife today after weeks at sea. Spain agreed to take the vessel after Cape Verde was unable to handle the medical response. All 147 passengers and crew will be examined, isolated, and repatriated. The Andes strain of hantavirus — linked to rodents in South America — is unusually capable of limited human-to-human transmission, making international health authorities closely watch for spread.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/05/08/g-s1-121055/spain-readies-for-evacuations",

    "{{WORLD_2_FLAG}}": "🇺🇸 MIDDLE EAST — US/IRAN",
    "{{WORLD_2_HEADLINE}}": "US-Iran Ceasefire Teeters After Navy Ships Intercepted Iranian Missiles in Hormuz",
    "{{WORLD_2_SUMMARY}}": "Three US warships were targeted by Iranian missiles, drones and small assault boats during a Strait of Hormuz transit on 7 May — all threats were destroyed and no ships were hit. The Pentagon launched self-defence strikes on Iranian ports in response. Secretary of State Rubio said on 8 May he expected Tehran's response to a peace deal proposal by end of day, adding: 'The red line is clear — threaten Americans and you'll get blown up.' Global oil prices remain elevated as the standoff continues.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/05/07/g-s1-120978/u-s-military-intercepted-iran-attacks-navy-ships-hormuz",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 BUDGET 2026",
    "{{ECON_1_HEADLINE}}": "Budget Night on Tuesday: $20K Asset Write-Off and Fuel Excise Extension in Frame for Small Business",
    "{{ECON_1_SUMMARY}}": "Treasurer Jim Chalmers hands down the 2026-27 Federal Budget on Tuesday 12 May. Two key measures are on small business watch lists: whether the $20,000 instant asset write-off is made permanent (it expires 30 June if not extended), and whether the 26.3 c/litre fuel excise cut is extended beyond June 30. A $10.7 billion Australian Fuel Security and Resilience Package — including a permanent government-owned fuel reserve — has already been confirmed as a budget item.",
    "{{ECON_1_URL}}": "https://dynamicbusiness.com/featured/what-is-in-the-2026-federal-budget-for-small-business-here-is-what-we-know-so-far.html",

    "{{ECON_2_FLAG}}": "⛽ FUEL PRICES",
    "{{ECON_2_HEADLINE}}": "ACCC: Retail Petrol and Diesel Trending Lower — But Excise Cut Expiry on 30 June Still a Watchpoint",
    "{{ECON_2_SUMMARY}}": "The ACCC's latest weekly fuel monitoring shows retail petrol and diesel prices continuing to fall as the April fuel excise cut flows through. The 26.3 c/litre reduction runs until 30 June 2026, with ACCC monitoring weekly to ensure the savings pass to consumers and businesses. With the Middle East crisis keeping wholesale prices volatile, whether that cut gets extended in Tuesday's budget could make a material difference to trades transport costs heading into winter.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI — GOVERNANCE",
    "{{TECH_1_HEADLINE}}": "Google, Microsoft and xAI Sign Up for US Government AI Safety Testing Programme",
    "{{TECH_1_SUMMARY}}": "Three of the world's biggest AI developers have committed to having their models tested by the US Department of Commerce's Centre for AI Standards and Innovation (CAISI). The White House is simultaneously drafting an executive order to vet all new AI models before public release — a process compared to FDA drug approval. The framework marks a significant shift from voluntary commitments to structured government oversight of AI deployment.",
    "{{TECH_1_URL}}": "https://www.euronews.com/next/2026/05/08/tech-giants-agree-to-us-government-ai-testing",

    "{{TECH_2_FLAG}}": "📊 AI — ADOPTION",
    "{{TECH_2_HEADLINE}}": "Microsoft Report: 17.8% of Workers Use AI — But Frontier Businesses Are Pulling 3.5x Further Ahead",
    "{{TECH_2_SUMMARY}}": "Microsoft's 2026 Global AI Diffusion Report, published Thursday, finds just 17.8% of working-age people worldwide use AI tools — but a sharp divide is opening. Firms in the top 5% of AI adoption now deploy it 3.5 times more per worker than the average, up from 2x a year ago. Software developer employment rose 4% year-on-year, suggesting AI is augmenting skilled workers rather than replacing them. The productivity gap between early adopters and the rest is widening every quarter.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳 ROBOTICS — FUNDING",
    "{{ROBOT_1_HEADLINE}}": "China's ROBOTERA Closes $200M+ Round, Already Delivering Humanoids to 10+ Logistics Centres",
    "{{ROBOT_1_SUMMARY}}": "ROBOTERA, backed by SF Group, Alibaba, Geely Capital and Hillhouse among others, has closed a funding round exceeding $200 million USD — following a separate RMB 1 billion strategic round in March. The company is already operating humanoid robots across 10+ logistics centres through partnerships with China Post and SF Group, reports 300%+ growth in Q2 2026, and says 95% of core components are built in-house. Deployments are now expanding from logistics into automotive and electronics manufacturing globally.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/05/08/robotera-raises-over-usd-200-million-in-new-round-led-by-sf-group-hsg-and-idg-capital/26534/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Three 'ISIS Brides' Arrested at Sydney and Melbourne Airports on Slavery and Terror Charges",
    "{{AUS_1_SUMMARY}}": "Three Australian women returning from Syria — among 13 Australians, including nine children, repatriated from former Islamic State territory — were arrested by counter-terrorism teams at Sydney and Melbourne airports on Thursday. Two women arrested in Melbourne face slavery-related charges; a third arrested in Sydney faces terrorism charges including membership of a proscribed organisation. The returns follow years of government negotiations.",
    "{{AUS_1_URL}}": "https://www.washingtonpost.com/world/2026/05/07/isis-brides-australia-syria-islamic-state/cf4efcd2-49e9-11f1-a119-857cd2bf4fd4_story.html",

    "{{AUS_2_HEADLINE}}": "Inland Rail Scrapped North of Parkes After $45 Billion Cost Blowout",
    "{{AUS_2_SUMMARY}}": "The Albanese government has cancelled the northern section of the Inland Rail project — originally designed to connect Melbourne to Brisbane — after costs blew out from $16.4 billion to more than $45 billion, a 450% increase. The Melbourne-to-Parkes southern section will still be completed by 2027, enabling double-stacked freight trains to run between Melbourne and Perth via Parkes.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Marks 125 Years Since First Federal Parliament with Free Events at Royal Exhibition Building",
    "{{VIC_1_SUMMARY}}": "Today — 9 May 2026 — marks exactly 125 years since Australia's first Federal Parliament opened at Melbourne's Royal Exhibition Building in Carlton Gardens. Free public events run 12pm–5pm today and tomorrow, featuring building tours, historical exhibitions, Charles Nuttall's famous 1901 painting of the opening ceremony (not publicly displayed since 2001), and the original State Landau Coach. A good excuse to get into the city if the cold weather permits.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 PHYSICS — UK",
    "{{SCI_1_HEADLINE}}": "Universe's Fundamental Constants Are Precisely Tuned to Allow Life — Right Down to How Blood Flows in Cells",
    "{{SCI_1_SUMMARY}}": "Researchers at Queen Mary University of London have published evidence that the Universe's fundamental constants — including Planck's constant and the charge of an electron — sit within an extraordinarily narrow range that allows liquids to flow correctly inside living cells. Even a few percent shift in these values would make blood too thick, water too sticky, or cellular motion impossible. Published 8 May, the work extends the 'fine-tuning' argument from nuclear reactions inside stars all the way down to the biochemistry of the cell — suggesting life's existence depends on a precise balance written into the deepest physics of the cosmos.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Supplier Relationships Are a Business Asset — AI Can Help You Manage Them Like One",
    "{{INSIGHT_BODY}}": "Most trades operators know their top suppliers by feel — who's reliable, who stretches lead times, who's quietly crept up on price. But with material costs volatile and supply chains unpredictable heading into the back half of 2026, gut feel isn't enough. AI tools can now scan your purchase history — invoices, emails, delivery dockets — and build a plain-language supplier scorecard in minutes: average lead times, price variance over six months, where the biggest gaps are. A prompt like 'compare my three main supply contacts on price and delivery reliability across the last 12 months' can surface patterns you'd never spot manually. That kind of insight doesn't need a purchasing manager — it needs a habit. Start with your most-used supplier, feed in the data you have, and ask what story it tells.",

    # Fun Facts
    "{{FACT_1}}": "A cloud, despite looking light and airy, typically weighs around 500 tonnes — roughly equivalent to 100 adult elephants. The water droplets that make up a cloud are so tiny and spread across such a vast volume that rising air currents support the weight. A large storm cloud can weigh millions of tonnes.",
    "{{FACT_2}}": "Tooth enamel is the hardest substance the human body produces — rating 5 on the Mohs hardness scale, comparable to a steel file. But the cells that form it (ameloblasts) die before the tooth erupts from the gum, meaning enamel can never regenerate once worn or cracked. There is no biological fallback once it is gone.",
    "{{FACT_3}}": "The dot over a lowercase letter 'i' or 'j' is called a 'tittle' — a term used in English typography for centuries. It appears in the Biblical phrase 'not one jot or tittle shall pass from the law', where 'jot' referred to the smallest Hebrew letter and 'tittle' to the smallest mark within a letter.",

    # Joke
    "{{JOKE_SETUP}}": "Why do boilermakers make terrible liars?",
    "{{JOKE_PUNCHLINE}}": "Everything they say is under pressure.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Success usually comes to those who are too busy to be looking for it.\"",
    "{{CLOSING_ATTR}}": "Henry David Thoreau",
    "{{CLOSING_MESSAGE}}": "A cold Saturday in Carrum Downs — but a significant one. Today marks exactly 125 years since Australia's first Federal Parliament opened at the Royal Exhibition Building in Melbourne, with free public events running from noon. Budget night is Tuesday, the fuel excise cut expiry is ticking, and a hantavirus-hit cruise ship is docking in the Canary Islands. Stay warm, keep an eye on Tuesday's budget, and make the most of the weekend, Liall.",
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