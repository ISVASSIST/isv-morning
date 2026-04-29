#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 29 April 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Wed 29 Apr
    "{{WEATHER_1}}": "Wed 29 Apr · Partly cloudy · 18°C",
    "{{WEATHER_2}}": "Thu 30 Apr · Sunny · 22°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Fri 1 May · Mostly sunny · 20°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Sat 2 May · Showers · 17°C",
    "{{WEATHER_5}}": "Sun 3 May · Heavy showers · 15°C",
    "{{WEATHER_ALERT}}": "Rain Sat–Sun",

    # World
    "{{WORLD_1_FLAG}}": "🛢️ IRAN · OIL",
    "{{WORLD_1_HEADLINE}}": "Trump Rejects Iran's Strait of Hormuz Offer — Brent Crude Surges Past $116",
    "{{WORLD_1_SUMMARY}}": "Iran proposed halting attacks on Strait of Hormuz shipping if the US lifted its blockade — but Trump rejected the deal, insisting any agreement must first address Iran's nuclear program. With talks deadlocked and Brent crude now trading above $116 a barrel, the Middle East war is in its 60th day. US military costs have hit $25 billion with no ceasefire in sight. For Australian businesses still carrying Middle East fuel surcharges, there's no early relief on the horizon.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/04/29/world/live-news/iran-war-peace-proposal-trump",

    "{{WORLD_2_FLAG}}": "🇰🇷 SOUTH KOREA",
    "{{WORLD_2_HEADLINE}}": "Ousted South Korean President Yoon Gets 7 More Years — Already Serving Life for Rebellion",
    "{{WORLD_2_SUMMARY}}": "A Seoul appeals court sentenced former President Yoon Suk Yeol to an additional seven years in prison on Wednesday for resisting arrest and bypassing a mandatory Cabinet meeting before his failed martial law declaration in December 2024. That sentence stacks on top of a life sentence he already received on rebellion charges — making him one of the most heavily punished leaders in South Korean democratic history. His legal team plans to appeal to the Supreme Court.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/04/29/g-s1-119165/south-korean-court-sentences-ex-president-yoon",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 AUSTRALIA · RATES",
    "{{ECON_1_HEADLINE}}": "Australia's Inflation Hits a 2-Year High at 4.09% — Raising the Stakes at the RBA's May Meeting",
    "{{ECON_1_SUMMARY}}": "Australia's Q1 2026 inflation came in at 4.09% annually — the highest reading in over two years. It was fractionally below the 4.2% forecast, but still well outside the RBA's 2–3% target band, with Middle East fuel costs continuing to drive the trimmed mean. The Reserve Bank board meets in early May, and while most economists forecast a hold, another hike is on the table. Any move up will add directly to repayments for businesses carrying commercial loans, equipment finance, or vehicle debt.",
    "{{ECON_1_URL}}": "https://www.cnbc.com/2026/04/29/australia-inflation-q1-rba-rate-hike-outlook.html",

    "{{ECON_2_FLAG}}": "⛽ AUSTRALIA · FUEL",
    "{{ECON_2_HEADLINE}}": "Retail Diesel Finally Falling — But the 26.3¢ Excise Cut Helping You Expires June 30",
    "{{ECON_2_SUMMARY}}": "The ACCC's latest weekly fuel monitoring shows international diesel prices dropped 18% in the week to 22 April, and retail pump prices are beginning to follow. That's a genuine short-term win for transport-heavy trades. But the temporary halving of the fuel excise — saving 26.3 cents per litre — expires 30 June with no confirmed extension. If the excise snaps back while Middle East tensions persist, the combined cost hit for diesel-dependent operators could be significant heading into Q3.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤝 AI · DEAL",
    "{{TECH_1_HEADLINE}}": "OpenAI and Microsoft End Exclusivity — AWS Immediately Launches Three New OpenAI Services",
    "{{TECH_1_SUMMARY}}": "OpenAI and Microsoft have restructured their foundational partnership, ending Microsoft's exclusive grip on where OpenAI models can be deployed. AWS responded within hours, announcing three new OpenAI-based services on its Bedrock platform — including a jointly built agent service. For any business choosing an AI stack: cloud competition is now real, prices will fall, and you're no longer locked into Azure to access the world's most capable AI models.",
    "{{TECH_1_URL}}": "https://thenewstack.io/openai-microsoft-partnership-restructured/",

    "{{TECH_2_FLAG}}": "⚖️ AI · LEGAL",
    "{{TECH_2_HEADLINE}}": "The OpenAI vs Elon Musk Trial Begins — Billions and the Governance of AI at Stake",
    "{{TECH_2_SUMMARY}}": "The closely-watched lawsuit between Elon Musk and OpenAI CEO Sam Altman went to trial in federal court in Oakland on Tuesday. Musk alleges OpenAI betrayed its founding non-profit mission by prioritising commercial gain over humanity's safety. OpenAI argues Musk walked away, later tried to seize control, and is now using litigation to hamper a competitor. The outcome could reshape how AI companies worldwide are governed, funded, and held accountable.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 USA · HUMANOID",
    "{{ROBOT_1_HEADLINE}}": "Apptronik Hires Waymo's Top Product Executive to Drive Apollo Robot Into Mass Production",
    "{{ROBOT_1_SUMMARY}}": "Austin-based humanoid robot startup Apptronik has appointed Waymo veteran Daniel Chu as Chief Product Officer, tasked with leading the commercial rollout of its Apollo robot following a $935 million raise. Chu joins alongside executives from Amazon, Boston Dynamics, and Paramount — a C-suite assembly that signals Apptronik is moving hard from R&D into market deployment. Factory and logistics deployments are planned for 2026. This is the commercialisation phase starting in earnest for physical AI.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/apptroniks-new-cpo-chu-hire-major-step-right-direction/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Moves to Tax Meta, Google and TikTok Unless They Pay News Publishers",
    "{{AUS_1_SUMMARY}}": "The Albanese government tabled draft legislation Tuesday that would hit Meta, Google and TikTok with a 2.25% tax on their Australian revenue if they refuse to strike commercial deals with news publishers. Expected to generate $144–179 million per year, distributed to media organisations by journalist headcount. The platforms are calling it a backdoor digital services tax — but the bill heads to Parliament by 2 July.",
    "{{AUS_1_URL}}": "https://www.npr.org/2026/04/29/g-s1-119142/australia-moves-to-tax-meta-google-and-tiktok-to-fund-newsrooms",

    "{{AUS_2_HEADLINE}}": "Japan's PM Takaichi Arrives in Canberra This Weekend for Energy and Defence Talks",
    "{{AUS_2_SUMMARY}}": "Japanese Prime Minister Sanae Takaichi flies into Canberra on Sunday for the annual Australia–Japan Leaders' Meeting, where she'll meet PM Albanese on Monday. LNG supply security, AUKUS cooperation, and the 50th anniversary of the Australia–Japan friendship treaty are all on the agenda — at a critical time with Middle East disruption squeezing global LNG supply chains.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne's Southbank to Get an $8 Million Public Park Underneath a Busy Overpass",
    "{{VIC_1_SUMMARY}}": "The City Road Undercroft in Southbank will be transformed into a 5,000 sqm public park under Melbourne's draft 2026–27 budget — combining $5.5 million from the City of Melbourne with $4 million in federal funding. Plans include a street-style skate plaza, roller rink, bouldering walls, basketball and netball courts, and greenery pockets. Construction begins late 2026, pending approvals.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 PHYSICS · MEDICINE",
    "{{SCI_1_HEADLINE}}": "MIT Scientists Found That Chaotic Laser Light Can Teach Itself to Focus — and Now They're Using It to Image the Brain 25× Faster",
    "{{SCI_1_SUMMARY}}": "Researchers at MIT have discovered that under specific conditions, a chaotic scatter of laser light will spontaneously self-organise into a tightly focused 'pencil beam' — a paradoxical phenomenon that shouldn't work according to conventional optics. They turned it into a tool: the self-organising beam can image the human blood-brain barrier in 3D at speeds 25 times faster than any existing technique, without contrast agents or fluorescent dyes. The research, published in Nature Methods this week, could accelerate the development of treatments for Alzheimer's and other neurological diseases.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Phone Can't Answer at 10pm — But an AI Chatbot Can",
    "{{INSIGHT_BODY}}": "Most trade jobs get booked in the evening, when the client has finally had a moment to think about it. For small operators in blasting, coatings, or construction, that's typically when the phone goes to voicemail — and the inquiry goes to whichever competitor picks up first. AI-powered chatbot tools costing under $100 a month can be added to your website or Google Business profile to handle incoming inquiries, collect job details, and confirm a callback time — 24 hours a day, seven days a week. You don't need a developer to set one up. Tools like Tidio, Crisp, or a custom Claude integration can be configured in an afternoon. For a sole operator or small team, being genuinely 'always on' without working nights is one of the highest-leverage improvements you can make to your inquiry conversion rate.",

    # Fun Facts
    "{{FACT_1}}": "Sea otters hold hands while they sleep — a behaviour known as 'rafting.' Without an anchor, they'd drift apart from their mate in open water. Pairs clasp paws to stay together, and some otters also wrap themselves in kelp fronds to keep from floating away overnight.",
    "{{FACT_2}}": "Honey never spoils. Archaeologists have found 3,000-year-old honey sealed in Egyptian tomb vessels that was still perfectly edible. Its extreme acidity, very low moisture content, and naturally occurring hydrogen peroxide create an environment where bacteria simply cannot survive.",
    "{{FACT_3}}": "The word 'salary' comes from the Latin 'salarium' — the allowance given to Roman soldiers specifically to buy salt. Salt was so valuable in the ancient world it functioned as currency across multiple civilisations. 'Worth his salt' entered English directly from this tradition.",

    # Joke
    "{{JOKE_SETUP}}": "What do you call a concreter who retires at 50?",
    "{{JOKE_PUNCHLINE}}": "Set for life.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Quality is not an act, it is a habit.\"",
    "{{CLOSING_ATTR}}": "Aristotle",
    "{{CLOSING_MESSAGE}}": "It's Wednesday morning, Liall — the week is sitting well. Partly cloudy today with a warm, sunny stretch forecast for Thursday and Friday before rain closes in over the weekend. Australia's Q1 inflation just printed at 4.09%, so watch the RBA's May meeting closely. The Iran/Hormuz deadlock continues to keep fuel costs elevated, but retail diesel did fall this week — worth timing your next fill-up. Make the most of the dry window.",
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
