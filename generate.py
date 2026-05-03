#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 03 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Sun 3 May
    "{{WEATHER_1}}": "Sun 3 May · Clearing showers · 20°C",
    "{{WEATHER_2}}": "Mon 4 May · Showers · 16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Tue 5 May · Rain · 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "Wed 6 May · Mostly cloudy · 16°C",
    "{{WEATHER_5}}": "Thu 7 May · Partly sunny · 17°C",
    "{{WEATHER_ALERT}}": "⚠ Showers Mon–Tue",

    # World
    "{{WORLD_1_FLAG}}": "🌐 MIDDLE EAST · CONFLICT",
    "{{WORLD_1_HEADLINE}}": "Trump Rejects Iran's 14-Point Ceasefire Plan — Senior Commander Warns Conflict 'Possible'",
    "{{WORLD_1_SUMMARY}}": "US President Trump dismissed Iran's latest peace proposal — which included opening the Strait of Hormuz, withdrawing US forces, and lifting sanctions — saying Tehran asks for terms he \"can't agree to.\" A senior Iranian military official warned that renewed conflict is now \"possible.\" With the war in its 64th day, both sides remain under a fragile ceasefire but negotiations have effectively stalled, and Trump confirmed he is reviewing military options.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/5/2/iran-war-whats-happening-on-day-64-as-trump-rejects-tehrans-proposal",

    "{{WORLD_2_FLAG}}": "🇩🇪 EUROPE · NATO",
    "{{WORLD_2_HEADLINE}}": "Pentagon Orders 5,000 US Troops Out of Germany — Trump Hints the Number Will Go Much Further",
    "{{WORLD_2_SUMMARY}}": "The United States will withdraw approximately 5,000 troops — around 14% of its German garrison — within six to twelve months, amid Trump's escalating public feud with Chancellor Friedrich Merz over the Iran conflict. Trump told reporters the actual number will go \"a lot further\" than 5,000. Republican lawmakers and NATO allies have warned the move weakens Western security and benefits Vladimir Putin.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/05/02/g-s1-119864/u-s-withdraw-troops-germany",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ GLOBAL · ENERGY",
    "{{ECON_1_HEADLINE}}": "Oil Still 17% Above Pre-War Levels — Why Prices Aren't Falling Despite the Ceasefire",
    "{{ECON_1_SUMMARY}}": "Global crude oil prices have retreated from their 60% war-peak but remain roughly 17% above pre-conflict levels, even with a ceasefire technically in place. CNN's analysis explains the persistent premium: futures traders are pricing in renewed conflict risk as Trump reviews military options, and Strait of Hormuz cargo flows remain disrupted. For Australian trades businesses, this means diesel and freight costs stay elevated — planning for fuel above $2 per litre through Q3 is prudent.",
    "{{ECON_1_URL}}": "https://www.cnn.com/2026/05/01/business/oil-market-price-high-low-iran",

    "{{ECON_2_FLAG}}": "🇦🇺 SMALL BUSINESS",
    "{{ECON_2_HEADLINE}}": "HVIA Fuel Security Update: Diesel at Eastern Australia Truck Stops Still Up 28% on Pre-War Levels",
    "{{ECON_2_SUMMARY}}": "The Heavy Vehicle Industry Association's May 1 fuel security update reports diesel prices at major truck stops across eastern Australia remain approximately 28% above pre-Iran-conflict levels, even with the halved federal excise in place. With the excise cut expiring June 30 and peace talks stalled, HVIA is urging operators to lock in fuel contracts or supplier agreements before the snapback. Trades businesses running vans and utes should recalculate their cost-per-job figures now.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "⚖️ AI · LAW",
    "{{TECH_1_HEADLINE}}": "Chinese Court Rules It Illegal to Fire Workers Solely to Replace Them with AI",
    "{{TECH_1_SUMMARY}}": "The Hangzhou Intermediate People's Court upheld a landmark ruling that a tech company acted unlawfully when it dismissed a senior worker — whose role was taken over by AI large language models — purely to cut costs. The court found that while companies may benefit from AI efficiency gains, the risks of \"technological iteration\" cannot be shifted entirely onto employees. The decision sets a precedent across China's technology sector and is being watched closely by labour advocates in Australia and globally.",
    "{{TECH_1_URL}}": "https://www.npr.org/2026/05/01/nx-s1-5807131/tech-worker-china-ai",

    "{{TECH_2_FLAG}}": "🤖 AI · AGENTS",
    "{{TECH_2_HEADLINE}}": "OpenAI's Codex Revenue Doubles in Under a Week as 'Agentic AI' Moves Into the Mainstream",
    "{{TECH_2_SUMMARY}}": "OpenAI reported this week that revenue from Codex — its AI coding agent that takes multi-step actions autonomously — doubled in under seven days, driven by surging enterprise demand. The rapid uptake signals that \"agentic\" AI, which can complete sequences of tasks without constant human prompting, is moving into mainstream business infrastructure faster than most anticipated. For trades businesses, the practical implication: AI agents that can draft quotes, follow up on invoices, and manage job workflows are arriving in standard software platforms much sooner than most people expect.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 BIG TECH · ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "Meta Buys AI Robotics Startup Assured Robot Intelligence to Power Its Humanoid Push",
    "{{ROBOT_1_SUMMARY}}": "Meta Platforms has acquired Assured Robot Intelligence (ARI), a startup building foundation AI models that help robots understand and physically adapt to human behaviour in dynamic, unstructured environments. ARI's team — including former Nvidia researcher and UC San Diego professor Xiaolong Wang — joins Meta's Superintelligence Labs. Rather than making robots directly, Meta aims to become the \"Android of robotics\": an enabling AI platform for the broader humanoid industry, in a market analysts value at $5 trillion by 2035.",
    "{{ROBOT_1_URL}}": "https://techcrunch.com/2026/05/01/meta-buys-robotics-startup-to-bolster-its-humanoid-ai-ambitions/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia's Teen Social Media Ban Gets Quietly Amended — Critics Say Tech Firms Won New Workarounds",
    "{{AUS_1_SUMMARY}}": "New amendments to Australia's world-first under-16 social media ban have paved the way for tech companies to work around the policy's core restrictions, according to Crikey analysis. The original law — which came into force in December — barred platforms from allowing Australians under 16 to create accounts. Critics argue the latest changes, which were not publicly highlighted, gut the original intent and reflect successful lobbying by major platforms.",
    "{{AUS_1_URL}}": "https://www.crikey.com.au/2026/05/01/teen-social-media-ban-australia-changes/",

    "{{AUS_2_HEADLINE}}": "Man Charged with Attempted Murder After Two Jewish Men Stabbed in London; Australian Groups Call for Action",
    "{{AUS_2_SUMMARY}}": "A 45-year-old man has been charged with attempted murder after stabbing two Jewish men in London in the latest in a string of antisemitic attacks alarming communities in the UK and Australia. Australian Jewish organisations are calling on the federal government to act on the Antisemitism Royal Commission's interim recommendations ahead of its final report, due December 14. PM Albanese condemned the attack.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian State Budget Handed Down Tuesday — Business Groups Push for Confidence Boost Amid Rising State Debt",
    "{{VIC_1_SUMMARY}}": "The Victorian Government delivers its 2026-27 State Budget on Tuesday 5 May, with the Victorian Chamber of Commerce and industry bodies urging Treasurer Jaclyn Symes to prioritise measures that restore business confidence and reduce regulatory complexity. Victoria's state debt has risen sharply and business confidence trails the national average. The City of Melbourne's separate $804.8 million draft budget — covering parks upgrades, safer streets, and community hubs — is also open for public consultation.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 NEUROSCIENCE",
    "{{SCI_1_HEADLINE}}": "Scientists Find a Way to Help the Brain Clear Its Own Alzheimer's Plaques — Published May 2",
    "{{SCI_1_SUMMARY}}": "Researchers at Baylor College of Medicine, publishing in Nature Neuroscience on May 2, found that boosting a protein called Sox9 reactivates astrocytes — the brain's star-shaped support cells — to actively engulf and remove the amyloid plaques characteristic of Alzheimer's disease. In mouse models that already had established cognitive impairment, the technique cleared plaques and preserved memory. Unlike most current approaches that focus on neurons or preventing new plaque formation, this strategy harnesses the brain's own built-in housekeeping system.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Stop Losing Repeat Business: How AI Can Turn Every Completed Job into Tomorrow's Lead",
    "{{INSIGHT_BODY}}": "For most small trades businesses, the biggest untapped asset isn't the tools in the van — it's the database of customers they've already done work for. AI-powered CRM and follow-up tools can automatically trigger a check-in message six months after a job, send maintenance reminders, request a Google review while the experience is still fresh, and suggest repeat services based on job history. For an abrasive blasting and coatings operation in Melbourne's south-east, that means proactively prompting past clients about recoating cycles or upcoming asset inspections rather than waiting for them to call. Platforms like ServiceM8 and Tradify include basic versions of this, and standalone AI follow-up tools typically run under $50 per month. In a competitive market, the operator who communicates most consistently wins the repeat work without fighting on price.",

    # Fun Facts
    "{{FACT_1}}": "Octopuses have three hearts: two pump blood through each set of gills, while a third — the systemic heart — circulates it around the body. Their blood is blue because it uses copper-based haemocyanin instead of iron-based haemoglobin. When an octopus swims hard, the systemic heart actually stops beating, which is why octopuses strongly prefer crawling over swimming.",
    "{{FACT_2}}": "The world's largest living organism by area isn't a blue whale or a giant sequoia — it's a single honey fungus (Armillaria ostoyae) growing underground in Oregon's Malheur National Forest. It spans roughly 9.6 square kilometres and is estimated to be between 2,000 and 8,000 years old. It was discovered in 1998 when foresters were investigating a mysterious die-off of trees.",
    "{{FACT_3}}": "Australia holds the record for the world's longest fence — the Dingo Fence, stretching approximately 5,614 kilometres from south-western Queensland to the South Australian coast. Built in the 1880s to protect south-eastern sheep pastures from wild dingoes, it remains actively maintained today.",

    # Joke
    "{{JOKE_SETUP}}": "Why don't plumbers make great comedians?",
    "{{JOKE_PUNCHLINE}}": "Their timing is always off — and the punchline usually turns up a week late and costs twice what was quoted.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Knowing is not enough; we must apply. Willing is not enough; we must do.\"",
    "{{CLOSING_ATTR}}": "Johann Wolfgang von Goethe",
    "{{CLOSING_MESSAGE}}": "Happy Sunday, Liall — autumn showers clearing through the morning in Carrum Downs, with a mild 20°C peak this afternoon before rain returns Monday and Tuesday. Good day to clear the desk before the week ramps up. Two big announcements land Tuesday afternoon: the RBA cash rate decision at 2:30pm and the Victorian State Budget. If you're carrying variable-rate finance or watching state procurement, worth keeping Tuesday afternoon free.",
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
