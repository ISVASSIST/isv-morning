#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 10 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Sun 10 May
    "{{WEATHER_1}}": "Sun 10 May · Cloudy · 16°C/13°C",
    "{{WEATHER_2}}": "Mon 11 May · Showers · 16°C/12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Tue 12 May · Partly cloudy · 17°C/12°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Wed 13 May · Mostly cloudy · 17°C/11°C",
    "{{WEATHER_5}}": "Thu 14 May · Clearing · 16°C/10°C",
    "{{WEATHER_ALERT}}": "🌧 Mon showers · Budget night Tue",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦🇷🇺 UKRAINE · RUSSIA",
    "{{WORLD_1_HEADLINE}}": "Trump Announces Surprise 3-Day Russia-Ukraine Ceasefire Tied to WWII Victory Day",
    "{{WORLD_1_SUMMARY}}": "President Trump announced that Russia and Ukraine have agreed to pause all hostilities from 9–11 May and exchange 1,000 prisoners each. The deal — brokered hours before Moscow's Victory Day parade on 9 May — was confirmed by Ukrainian President Zelenskyy, who issued a presidential decree barring Ukrainian strikes on Red Square for the duration. Trump called it \"the beginning of the end\" of the war. Both sides had broken earlier ceasefire attempts within hours, raising cautious hopes for this one.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/5/8/trump-announces-three-day-ceasefire-in-russia-ukraine-war",

    "{{WORLD_2_FLAG}}": "🇺🇸🇮🇷 MIDDLE EAST",
    "{{WORLD_2_HEADLINE}}": "US Awaits Iran's Formal Response to Peace Framework as War Death Toll Passes 6,000",
    "{{WORLD_2_SUMMARY}}": "American officials are holding their breath for Tehran's formal reply to a framework proposal aimed at ending the Iran war, which has now claimed over 3,400 lives in Iran, 2,700 in Lebanon, and dozens across Gulf states. UK naval vessel HMS Dragon has been deployed to the Middle East for mine-clearance operations in the Strait of Hormuz. The UN reported global food prices rose for the third straight month in April, citing disrupted shipping routes as a key driver of supply chain pressure worldwide.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/05/09/world/live-news/iran-war-news",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 FUEL SECURITY",
    "{{ECON_1_HEADLINE}}": "Albanese's $10.7 Billion Fuel Security Package: A Billion-Litre Government Reserve for Australia",
    "{{ECON_1_SUMMARY}}": "PM Albanese announced Australia's biggest-ever fuel security package this week — a $3.2bn government-owned reserve of 1 billion litres of diesel and aviation fuel, plus a $7.5bn fuel and fertiliser security facility. Minimum private stock-holding obligations will rise by 10 days to a 50-day minimum nationally. The plan directly targets the Hormuz vulnerability that exposed how quickly Australia could run dry in a supply disruption — a risk that hits trades operators within days, not weeks.",
    "{{ECON_1_URL}}": "https://www.sbs.com.au/news/article/australia-fuel-security-package-reserves-stockholding/r8el4u2mn",

    "{{ECON_2_FLAG}}": "📉 INFLATION",
    "{{ECON_2_HEADLINE}}": "Australia's Inflation Climbs to 4.6% — Small Business Owners Brace as Rate Hike Prospect Returns",
    "{{ECON_2_SUMMARY}}": "Energy costs driven by the Middle East conflict have pushed Australia's annual inflation rate to 4.6% — its highest since September 2023. Employment Hero's latest SME sentiment data shows fuel, labour and materials are the three biggest cost concerns for trades businesses entering winter. The Reserve Bank of Australia's May Statement on Monetary Policy forecasts modest GDP growth, but the inflation figure has renewed market speculation about whether the RBA could reverse its recent rate cuts before year-end.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🧠 AI · INFRASTRUCTURE",
    "{{TECH_1_HEADLINE}}": "Anthropic Secures SpaceX's Entire Colossus 1 Data Centre — 300 MW to Handle 80x AI Demand Growth",
    "{{TECH_1_SUMMARY}}": "Anthropic has locked in all available compute at SpaceX's Colossus 1 facility in Memphis — more than 300 megawatts of capacity — after reporting 80-fold growth in AI usage demand during Q1 2026 alone. The deal reflects an industry-wide compute scramble: Microsoft, Meta, Amazon and Alphabet have collectively flagged roughly $725 billion in capital expenditure for 2026, almost entirely directed to AI data centres and custom chips. The AI tools available to a small business today are being built on this infrastructure — and the next generation is already under construction.",
    "{{TECH_1_URL}}": "https://imfounder.com/science-tech/ai/ai-updates-may-2026/",

    "{{TECH_2_FLAG}}": "⚡ AI · INDUSTRY",
    "{{TECH_2_HEADLINE}}": "Cloudflare Cuts 20% of Global Workforce After Internal AI Usage Surges 600% in 90 Days",
    "{{TECH_2_SUMMARY}}": "Web infrastructure giant Cloudflare announced cuts of more than 1,100 jobs — about 20% of its global workforce — after its own AI tools dramatically reduced the headcount needed to run the same operations. CEO Matthew Prince framed the cuts as structural, not cyclical. Coinbase cut 14% of staff the same week for identical reasons. The pattern emerging across the tech sector — AI compressing the ratio of revenue to headcount — is now spreading beyond software into any business where knowledge work is a significant cost.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 ROBOTICS · USA",
    "{{ROBOT_1_HEADLINE}}": "Figure AI Scales BotQ Factory to One Humanoid Robot Per Hour — 12,000 Units Per Year Now in Reach",
    "{{ROBOT_1_SUMMARY}}": "Figure AI has achieved a 24-fold throughput improvement at its BotQ manufacturing facility in under 120 days — going from one Figure 03 per day to one per hour. With more than 350 units delivered and 9,000+ custom actuators produced in-house, the line can now manufacture up to 12,000 humanoids annually. The latest Figure 03 with 'System 0' AI can navigate stairs and uneven terrain without prior training on the specific site — a critical real-world capability for factory and warehouse deployment.",
    "{{ROBOT_1_URL}}": "https://www.figure.ai/news/ramping-figure-03-production",

    # Australia
    "{{AUS_1_HEADLINE}}": "One Nation Wins Farrer By-Election — First Federal Lower House Seat in the Party's History",
    "{{AUS_1_SUMMARY}}": "One Nation's David Farley won the federal seat of Farrer on Saturday night, becoming the first One Nation candidate elected to the House of Representatives in the party's three-decade history. The seat had been held by Liberal or National MPs since 1949. The Coalition primary vote collapsed, with independent Michelle Milthorpe coming second. Political analysts say the result reflects deep dissatisfaction in regional NSW with the major parties and will increase pressure on the Liberal-National relationship heading into the next federal election.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/one-nation-wins-farrer-by-election/5ukevc345",

    "{{AUS_2_HEADLINE}}": "Australia Cancels Inland Rail North of Parkes — $45 Billion Cost Blowout Kills Brisbane Freight Dream",
    "{{AUS_2_SUMMARY}}": "The federal government has confirmed it will not fund the northern section of the Melbourne-to-Brisbane Inland Rail after costs blew out from $16.4 billion to more than $45 billion — nearly three times the original estimate. Construction continues only as far as Parkes in central NSW by 2027, completing a double-stack freight corridor to Western Australia. Queensland businesses and regional farmers described the decision as a \"hammer blow\" that leaves the eastern seaboard without the freight infrastructure it was promised for decades.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "67-Storey Apartment Tower Approved for Melbourne CBD in Bid to Ease Housing Crunch",
    "{{VIC_1_SUMMARY}}": "Victorian planning authorities have approved a 67-storey residential tower for the Melbourne CBD — one of the tallest residential buildings ever approved in the city. The development adds hundreds of new dwellings near the city centre as Victoria continues pushing for density to address the housing affordability crisis. The approval follows a series of high-rise rezonings across inner suburbs under the state government's Plan for Victoria framework, with further towers in the pipeline.",

    # Science
    "{{SCI_1_FLAG}}": "🧬 GENETICS · EARLHAM INSTITUTE",
    "{{SCI_1_HEADLINE}}": "Scientists Stumble on a Pond Creature Whose DNA Breaks Life's Most Universal Rule",
    "{{SCI_1_SUMMARY}}": "Researchers at the Earlham Institute, conducting a routine DNA sequencing experiment on pond water, discovered a microscopic ciliate whose genetic code has reassigned the universal DNA 'stop codons' — the molecular full stops that tell cells to end protein production — to instead code for amino acids. In virtually all life on Earth, this rule has held unchanged for billions of years. Finding an organism that evolved exceptions to it raises fresh questions about how fixed the genetic code really is, and how many more such exceptions may be hiding in the world's overlooked microbiomes. Published 7 May 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Help You Win Government Work — What Changes When the Contracts Get Bigger",
    "{{INSIGHT_BODY}}": "Most small trades operators have never submitted a formal government tender — the paperwork feels designed for bigger businesses. But with the federal government committing $10.7 billion to fuel infrastructure and state governments continuing to fund maintenance and capital works, there is real money flowing into contracts that subcontractors can win. AI tools can now draft a capability statement, structure a price schedule, and format a compliance document in about an hour — work that used to take a week with a consultant. The barrier isn't capability; it's the paperwork. Start with a prompt like: 'Write a 300-word capability statement for a surface protection contractor in Melbourne targeting government maintenance contracts.' You might be surprised how close you already are.",

    # Fun Facts
    "{{FACT_1}}": "Copper has been used in plumbing for at least 4,500 years. Archaeologists excavating the Pyramid of Sahure in Egypt found a functioning copper pipe system dating to around 2,500 BC — over a thousand years before the first Olympic Games. Modern copper plumbing uses essentially the same technology and the same metal, unchanged across four-and-a-half millennia.",
    "{{FACT_2}}": "The original 1972 Pong arcade cabinet — the first commercially successful video game — failed at its first test installation within days. Not from a technical fault, but because the coin slot jammed from being too full of quarters. It had generated $40 on its opening night (roughly $300 today). Atari's test site rang to report it was broken.",
    "{{FACT_3}}": "Stainless steel is self-repairing. The chromium in the alloy reacts with oxygen to form an invisible oxide layer just a few nanometres thick that continuously regenerates if scratched or worn away — rebuilding itself within hours when exposed to air. This 'passive layer' is the only reason stainless steel doesn't rust like ordinary steel, and was discovered accidentally by metallurgist Harry Brearley in Sheffield in 1913.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the tradie ring his mum on Mother's Day from the job site?",
    "{{JOKE_PUNCHLINE}}": "She's the only client who never argues with the invoice.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The way to get started is to quit talking and begin doing.\"",
    "{{CLOSING_ATTR}}": "Walt Disney",
    "{{CLOSING_MESSAGE}}": "Happy Mother's Day to the mums of Carrum Downs and beyond — hope the morning starts with coffee rather than a call-out. It's a cloudy Sunday with a chance of morning drizzle, easing through the week. One Nation made history last night in Farrer. The Ukraine ceasefire is holding for now. Budget night Tuesday — keep an eye on that instant asset write-off. Have a good one, Liall.",
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
