#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 15 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 15 Jul (BOM)
    "{{WEATHER_1}}": "WED 15 · 🌧️ Showers, windy · 7–13°C",
    "{{WEATHER_2}}": "THU 16 · ☁️ Cloudy, slight shower · 8–13°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 17 · ☁️ Cloudy, slight shower · 8–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 18 · ⛅ Partly cloudy · 8–13°C",
    "{{WEATHER_5}}": "SUN 19 · ⛅ Partly cloudy, patchy fog · 7–13°C",
    "{{WEATHER_ALERT}}": "⚠ WINDY SHOWERS TODAY · DRYING OUT LATER IN THE WEEK",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦🇪🇺 PARIS · UKRAINE · 10-NATION MISSILE DEFENCE COALITION ANNOUNCED",
    "{{WORLD_1_HEADLINE}}": "Ukraine and Nine European Nations Announce New Ballistic Missile Defence Coalition",
    "{{WORLD_1_SUMMARY}}": "Meeting in Paris with more than 30 countries in the so-called Coalition of the Willing, Ukraine and nine European nations — including Britain, France, Germany, Italy and Spain — announced a new shared coalition aimed at building ballistic missile defence capability across Europe. It's a fresh show of long-term commitment to Ukraine as Russia keeps testing the region's resolve, with leaders including Macron, Merz and Starmer among those at the table.",
    "{{WORLD_1_URL}}": "https://www.pbs.org/newshour/world/ukraine-and-9-other-countries-form-coalition-to-protect-europe-from-ballistic-missiles",

    "{{WORLD_2_FLAG}}": "🇳🇿🎬 TRIBUTE · JURASSIC PARK STAR DIES AT 78 IN SYDNEY",
    "{{WORLD_2_HEADLINE}}": "Jurassic Park Star Sam Neill Dies Aged 78 After Recovering From Cancer",
    "{{WORLD_2_SUMMARY}}": "New Zealand actor Sam Neill, best known for playing Dr Alan Grant in Jurassic Park and for his role in The Piano, has died in Sydney aged 78, his family confirmed. He'd revealed in April he was cancer-free after a battle with a rare blood cancer, making the loss sudden despite the earlier good news.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/07/13/nx-s1-5891505/actor-sam-neill-dies",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · EXCISE RELIEF HALVES · BOWSER PRICES CLIMB AGAIN",
    "{{ECON_1_HEADLINE}}": "Petrol Jumps 12c a Litre in a Week as the Fuel Excise Cut Gets Halved",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly monitoring has capital city unleaded averaging 170.1c/L and diesel at 191.9c/L, up 12.2 cents on the previous week, as the fuel excise discount dropped from 32 cents to 16 cents a litre for July before reverting further from 2 August. Worth factoring a fresh look at your fuel surcharge line before the next job goes out the door.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📉 ECONOMY · GROWTH FORECAST CUT · WEAKEST RUN SINCE THE EARLY '90S",
    "{{ECON_2_HEADLINE}}": "Deloitte Slashes Australia's Growth Forecast, Warns of Weakest Stretch Since the Early-1990s Recession",
    "{{ECON_2_SUMMARY}}": "Deloitte Access Economics has cut its 2026-27 growth forecast from 1.9% to just 1.3%, citing rising interest rates, weak consumer and business confidence, stalling housing investment and the drawn-out cost-of-living squeeze. It points to the longest run of sub-2% annual growth since the early 1990s recession — a reminder to keep a close eye on receivables and cash buffers rather than banking on a quick bounce-back.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤝 SOFTWARE · MICROSOFT U-TURN · MEETING AI HANDED BACK TO ORGANISERS",
    "{{TECH_1_HEADLINE}}": "Microsoft Backs Down on Pushy AI in Teams, Lets Meeting Organisers Switch It Off",
    "{{TECH_1_SUMMARY}}": "After backlash over features like the AI 'Facilitator' quietly monitoring meetings, Microsoft has introduced new controls letting Teams meeting organisers turn AI-powered features on or off live during a call. A small but useful sign that software vendors are finally giving users an actual off switch rather than just more AI by default.",
    "{{TECH_1_URL}}": "https://www.forbes.com/sites/quickerbettertech/2026/07/12/small-business-technology-news-roundup-microsoft-makes-a-major-ai-u-turn/",

    "{{TECH_2_FLAG}}": "📈 MARKETING · GOOGLE ADS · CLICK COSTS UP 15% IN A YEAR",
    "{{TECH_2_HEADLINE}}": "Google Ads Costs Jumped 15% in the Past Year, Squeezing Small Business Marketing Budgets",
    "{{TECH_2_SUMMARY}}": "New industry data shows average cost-per-click on Google Ads has risen around 15% year-on-year, partly driven by Google's AI Overviews cutting organic click volume and pushing more traffic through paid channels. If you're running any paid ads for the business, it's a good week to check what you're actually paying per lead rather than assuming last year's budget still buys the same result.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · CHINA · HUMANOID MAKERS RACE TOWARD IPOs",
    "{{ROBOT_1_HEADLINE}}": "Chinese Humanoid Robot Makers LimX and Unitree Both Push Toward IPOs This Week",
    "{{ROBOT_1_SUMMARY}}": "LimX Dynamics confirmed a $200 million pre-IPO raise and plans to ship thousands of humanoids to the Middle East, while Unitree Robotics won approval for a Shanghai STAR Market listing that could raise around $619 million for new AI models and robot designs. It's another sign the humanoid robotics race has shifted from lab demos to a straight-out commercial and capital-markets sprint.",
    "{{ROBOT_1_URL}}": "https://www.cnbc.com/2026/07/13/chinese-humanoid-startups-ipo-limx-unitree.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Albanese to Unveil Australia's First National AI Framework in Major Sydney Speech Today",
    "{{AUS_1_SUMMARY}}": "Prime Minister Anthony Albanese delivers his 'AI in Australia's Interests' address in Sydney today, announcing a new Office of AI within his own department to coordinate a single national framework — covering everything from a digital duty of care and chatbot risks to children, through to AI's role in skills, manufacturing and defence.",
    "{{AUS_1_URL}}": "https://www.canberratimes.com.au/story/9310618/anthony-albanese-established-new-pmc-ai-office-to-make-australia-world-first/",

    "{{AUS_2_HEADLINE}}": "New National Data Shows Cancer Outcomes Improving for Aboriginal and Torres Strait Islander People",
    "{{AUS_2_SUMMARY}}": "A new AIHW report shows the cancer incidence rate for First Nations people fell from 342 to an estimated 315 per 100,000 between 2011 and 2025, with the mortality rate down from 148 to 105 deaths per 100,000 over the same period. Rates remain higher than for non-Indigenous Australians, but the improvement is outpacing the general population's.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Parliament Passes Bill Banning Phones and Smartwatches in Every School",
    "{{VIC_1_SUMMARY}}": "The Legislative Assembly has passed a bill extending Victoria's existing mobile phone ban to every school in the state, including non-government schools, and for the first time also covering wearables like smartwatches and wireless earbuds. It now heads to the Legislative Council, with the full ban set to apply from 28 January 2027.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 BIOLOGY · ITCH DECODED · HIDDEN NERVE NETWORK FOUND IN SKIN",
    "{{SCI_1_HEADLINE}}": "Scientists Discover a Dedicated Nerve Network Behind Chronic 'Mechanical' Itch",
    "{{SCI_1_SUMMARY}}": "University of Michigan researchers have identified a previously unknown class of fine 'vellus-like' hairs and a specialised set of touch-sensitive nerve cells that form a dedicated pathway for mechanical itch — distinct from the chemical itch triggered by mosquito bites or poison ivy. Because humans appear to have the same pathway, the findings, published in Neuron on 14 July, could point toward better treatments for chronic conditions like eczema.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Google Ads Just Got 15% More Expensive — How AI Can Help You Spend Smarter, Not More",
    "{{INSIGHT_BODY}}": "Cost-per-click on Google Ads has climbed roughly 15% over the past year, partly because Google's own AI Overviews are eating into free organic clicks and pushing more traffic through paid results — meaning the same ad budget now buys noticeably fewer leads than it did in 2025. Rather than simply raising spend to compensate, an AI tool that scores and pre-qualifies leads as they come in (or drafts faster, better follow-ups on the ones that matter) can lift your return per dollar without touching the ad budget at all — worth a look before your next campaign renews.",

    # Fun Facts
    "{{FACT_1}}": "Sandpaper's earliest known ancestor comes from 13th-century China, where crushed seashells and sand were bonded to parchment with plant gum to smooth wood and stone — the same basic idea behind every sheet of abrasive paper still used on a job site today.",

    "{{FACT_2}}": "Nintendo designer Shigeru Miyamoto based the original Legend of Zelda on childhood memories of exploring the fields, woods and a hidden cave near his hometown outside Kyoto — he wanted players to feel the same thrill of discovery he felt finding that cave as a boy.",

    "{{FACT_3}}": "Baking soda and baking powder aren't interchangeable — baking soda is a pure base that needs an acid like buttermilk or brown sugar to react, while baking powder already contains its own acid (cream of tartar) plus a buffer, giving it a slower, two-stage rise baking soda can't do alone.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the carpet layer's business always land on its feet?",
    "{{JOKE_PUNCHLINE}}": "He never let a customer walk all over him without a signed quote first.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Amateurs sit and wait for inspiration, the rest of us just get up and go to work.\"",
    "{{CLOSING_ATTR}}": "— Stephen King",
    "{{CLOSING_MESSAGE}}": "It's a showery, blustery Wednesday in Carrum Downs, 7–13°C, easing into calmer, mostly cloudy days through the rest of the week. Albanese fronts the cameras in Sydney today to unveil the government's first proper national AI framework — worth a few minutes over lunch if you're thinking about where AI fits into the business long-term. And if you need a distraction tonight, Argentina and England meet in the first World Cup semi-final.",
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
