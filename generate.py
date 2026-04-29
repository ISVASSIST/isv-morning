#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 2 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Fri 2 May
    "{{WEATHER_1}}": "Fri 2 May · Cloudy · 16°C",
    "{{WEATHER_2}}": "Sat · Showers · 14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Sun · Clearing · 15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Mon · Fine · 18°C",
    "{{WEATHER_5}}": "Tue · Partly cloudy · 17°C",
    "{{WEATHER_ALERT}}": "Rain Saturday",

    # World
    "{{WORLD_1_FLAG}}": "🛢️ UAE · OPEC",
    "{{WORLD_1_HEADLINE}}": "UAE Formally Exits OPEC — the Cartel's Biggest Blow in Decades",
    "{{WORLD_1_SUMMARY}}": "The United Arab Emirates officially left OPEC and OPEC+ yesterday, effective 1 May, stripping the cartel of its third-largest producer. Months of tension over production quotas came to a head as Iran's sustained attacks on Strait of Hormuz shipping throttled the UAE's ability to export at scale. The withdrawal leaves Saudi Arabia scrambling and removes OPEC's key moderating voice at the worst possible time.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/4/28/uae-leaves-opec-and-opec",

    "{{WORLD_2_FLAG}}": "👑 UK · US",
    "{{WORLD_2_HEADLINE}}": "King Charles Addresses US Congress — Praises AUKUS, Offers Pointed Warning on Democracy",
    "{{WORLD_2_SUMMARY}}": "King Charles III became only the second British monarch to address a joint session of Congress on Monday, calling the AUKUS defence pact \"ambitious and vital\" for Indo-Pacific stability and reaffirming the US–UK \"special relationship.\" He offered a carefully worded but unmistakable warning about the importance of democratic institutions — remarks that drew sharp commentary in Washington. A state dinner with President Trump followed.",
    "{{WORLD_2_URL}}": "https://edition.cnn.com/2026/04/28/us/live-news/king-charles-queen-camilla-us-visit",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 AUSTRALIA · RATES",
    "{{ECON_1_HEADLINE}}": "RBA Board Meets Tuesday — Hold Expected, But 4.6% Inflation Keeps Everyone on Edge",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank of Australia convenes Tuesday 5 May for its next rate decision. Two hikes this year have already lifted the cash rate to 4.10%, and most economists forecast a hold — but with annual inflation stuck at 4.6% and Middle East energy disruption still flowing through supply chains, the board faces pressure from both directions. Any move up would add meaningful monthly cost for businesses carrying commercial debt or equipment finance.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/monetary-policy/int-rate-decisions/",

    "{{ECON_2_FLAG}}": "⛽ AUSTRALIA · FUEL",
    "{{ECON_2_HEADLINE}}": "Fuel Excise Cut Expires June 30 — Operators Warned to Plan for the Snapback",
    "{{ECON_2_SUMMARY}}": "Australia's temporary 50% fuel excise cut runs out on 30 June, and with no extension confirmed, diesel-heavy operators should factor a 26.3 cents per litre cost increase back into their July pricing. Industry groups are pushing for an extension, but the government has not yet committed. The Iran war has already eroded much of the original saving — when the excise snaps back, the combined hit to transport-intensive trades will be significant.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤝 AI · DEAL",
    "{{TECH_1_HEADLINE}}": "OpenAI and Microsoft Rip Up Their Partnership — OpenAI Is No Longer Tied to Azure Alone",
    "{{TECH_1_SUMMARY}}": "OpenAI and Microsoft have renegotiated their foundational partnership, allowing OpenAI to deploy its models across cloud platforms beyond Microsoft Azure for the first time. Microsoft retains preferred-provider status but loses its exclusive grip — a structural shift that intensifies competition between cloud giants and gives businesses more real choice in which AI stack they build on.",
    "{{TECH_1_URL}}": "https://thenewstack.io/openai-microsoft-partnership-restructured/",

    "{{TECH_2_FLAG}}": "🌐 AI · OPEN SOURCE",
    "{{TECH_2_HEADLINE}}": "DeepSeek V4 Goes Open-Weight: China's Most Capable AI Is Now Free to Use and Modify",
    "{{TECH_2_SUMMARY}}": "Chinese AI lab DeepSeek released V4-Flash and V4-Pro in open-weight preview last week — the Pro model packs 1.6 trillion parameters, a 1-million token context window, and benchmarks that rival closed-source models from OpenAI and Anthropic at a fraction of the running cost. For small businesses evaluating AI tools: capable, enterprise-grade AI is getting dramatically cheaper every quarter.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 GERMANY · INDUSTRIAL",
    "{{ROBOT_1_HEADLINE}}": "\"Autonomous Alfie\" — A Self-Learning Humanoid Robot Built for Factory Floors, No Programmer Required",
    "{{ROBOT_1_SUMMARY}}": "German robotics startup RobCo unveiled Autonomous Alfie at Hannover Messe 2026 — a humanoid robot designed for precision assembly, material handling, and intralogistics that adapts to new workflows without rigid reprogramming. Delivered as Robotics-as-a-Service with no upfront capital, it targets mid-sized manufacturers who have been locked out of automation by integration costs. First customer deployments are scheduled for later this year.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/04/20/robco-unveils-autonomous-alfie-humanoid-robot-for-industrial-automation-at-hannover-messe/100762/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Japan's \"Iron Lady\" PM Takaichi Arrives in Australia on Sunday for Landmark Energy and Defence Talks",
    "{{AUS_1_SUMMARY}}": "Japanese Prime Minister Sanae Takaichi arrives in Canberra on Sunday 3 May for her first official Australian visit. She meets PM Albanese at Parliament House on Monday for the annual Australia–Japan Leaders' Meeting, with LNG supply agreements, AUKUS cooperation, and the 50th anniversary of the Australia–Japan friendship treaty all on the agenda.",
    "{{AUS_1_URL}}": "https://www.pm.gov.au/media/visit-australia-prime-minister-japan-0",

    "{{AUS_2_HEADLINE}}": "WA Grain Belt Hit by Worst Mouse Plague in Years — and Farmers Are Running Out of Bait",
    "{{AUS_2_SUMMARY}}": "Mouse populations have exploded across key cropping regions in Western Australia, with surveys recording up to 4,000 burrows per hectare in the worst-affected zones around Northampton and Ravensthorpe. Demand for zinc phosphide bait has outstripped supply ahead of seeding season, and with no federal assistance funding, growers are absorbing the cost on top of elevated fuel and fertiliser prices.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Victory vs Sydney FC — A-League Elimination Final Tomorrow Night at AAMI Park",
    "{{VIC_1_SUMMARY}}": "Melbourne Victory host Sydney FC in a winner-takes-all A-League Elimination Final tomorrow night, Saturday 3 May, kick-off 7:40pm at AAMI Park. Lose and the season ends immediately. Victory's home record has been the backbone of their year — they'll need the crowd and the form to drag them through.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 MEDICINE · ONCOLOGY",
    "{{SCI_1_HEADLINE}}": "A Daily Vitamin D Supplement Boosted Breast Cancer Treatment Success by 79% in New Study",
    "{{SCI_1_SUMMARY}}": "Brazilian researchers at São Paulo State University found that breast cancer patients who took a modest 2,000 IU daily vitamin D supplement alongside standard chemotherapy were dramatically more likely to achieve complete cancer remission — nearly half the supplemented group achieved full remission, compared to fewer than one in four in the placebo group. The study of 80 women was published this week and adds to a growing body of evidence that widespread vitamin D deficiency may quietly be undermining treatment outcomes worldwide.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your T&Cs Are Your First Line of Defence — AI Can Write Them in Minutes",
    "{{INSIGHT_BODY}}": "Most small trades operators send a quote and start work — and when a job turns ugly over payment, scope creep, or site access, they discover a quote isn't a contract. AI tools like Claude or ChatGPT can now draft a custom set of terms and conditions for your trade in under five minutes: covering scope of work, variation clauses, payment terms, late fees, and liability limits. Get a solicitor to review once, then bolt them onto every quote you send. For blasting and coatings work — where surface conditions, product substitutions, and weather delays create real scope ambiguity — written T&Cs aren't just protection. They signal to commercial clients that you run a professional outfit worth trusting with their project.",

    # Fun Facts
    "{{FACT_1}}": "Most of the \"wasabi\" served in Australian and Western restaurants is actually a blend of horseradish, mustard, and green food colouring. Genuine Wasabia japonica is so difficult to cultivate that real fresh wasabi costs around $300 per kilogram — making it one of the world's most expensive culinary plants.",
    "{{FACT_2}}": "Since 2012, the computing power used in the world's largest AI training runs has doubled roughly every six months — an increase of more than 600,000-fold in just over a decade, a pace that makes Moore's Law look leisurely.",
    "{{FACT_3}}": "The world's first recorded labour strike took place in ancient Egypt in 1170 BC, when workers building the royal tomb complex at Deir el-Medina downed tools because their rations of grain, fish, and beer hadn't been delivered on time. They essentially invented industrial action.",

    # Joke
    "{{JOKE_SETUP}}": "What do you call a tradesman who's booked solid for six months?",
    "{{JOKE_PUNCHLINE}}": "Excellent.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Give me six hours to chop down a tree and I will spend the first four sharpening the axe.\"",
    "{{CLOSING_ATTR}}": "Abraham Lincoln",
    "{{CLOSING_MESSAGE}}": "It's Friday — get any outdoor blasting locked in today while the sky is still dry. Rain rolls in tomorrow along with the A-League elimination final at AAMI Park. Japanese PM Takaichi arrives in Canberra Sunday, and the RBA board makes its rates call on Tuesday. Solid finish to the week — make the most of the morning.",
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
