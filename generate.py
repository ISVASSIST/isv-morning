#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    '{{DATE}}': 'Tuesday, 29 September 2026',
    '{{WEATHER_1}}': 'TUE 29 SEP · ⛅ Partly cloudy, gusty northerly, warm · 10–24°C',
    '{{WEATHER_2}}': 'WED 30 SEP · ☁️ Cloudy, medium chance of showers late · 17–23°C',
    '{{WEATHER_2_CLASS}}': 'rain',
    '{{WEATHER_3}}': 'THU 1 OCT · ⛈️ Cloudy, very high chance of showers, possible storm · 16–22°C',
    '{{WEATHER_3_CLASS}}': 'rain',
    '{{WEATHER_4}}': 'FRI 2 OCT · 🌦️ Partly cloudy, shower or two in the morning · 11–16°C',
    '{{WEATHER_5}}': 'SAT 3 OCT · ⛅ Partly cloudy, cool · 9–16°C',
    '{{WEATHER_ALERT}}': 'Gusty northerlies and a warm 24° today give way to showers Wednesday afternoon and a very high chance of showers with a possible thunderstorm Thursday, before a much cooler 16° finish to the week.',
    '{{WORLD_1_FLAG}}': "🇺🇸🇮🇷 GULF · OIL JUMPS AFTER TRUMP REJECTS IRAN'S SEVEN-DAY PLAN TO REOPEN HORMUZ",
    '{{WORLD_1_HEADLINE}}': "Oil Surges After Trump Rejects Iran's Plan to Reopen the Strait of Hormuz Within Seven Days",
    '{{WORLD_1_SUMMARY}}': "Iran's foreign minister offered to reopen the Strait within a week if the US ended its 'acts of aggression', lifted its naval blockade and released Iranian assets; Trump rejected the terms while signalling he's open to more talks, and Brent jumped more than 2.5% to around $107 a barrel as peace talks stalled.",
    '{{WORLD_1_URL}}': 'https://www.aljazeera.com/economy/2026/9/28/oil-prices-surge-after-trump-rejects-irans-plan-to-reopen-strait-of-hormuz',
    '{{WORLD_2_FLAG}}': "🇺🇸 EAST COAST · RARE SEPTEMBER NOR'EASTER LEAVES ONE DEAD AND 100,000+ WITHOUT POWER",
    '{{WORLD_2_HEADLINE}}': "Rare September Nor'easter Batters the US East Coast, Leaving One Dead and Over 100,000 Without Power",
    '{{WORLD_2_SUMMARY}}': "A slow-moving storm dumped more than 4 inches of rain on parts of New Jersey, flooding coastal towns from North Carolina to Maine at levels residents hadn't seen in nearly a decade; a New York housing worker was killed by a falling tree, and more than 3,000 flights were delayed on Saturday alone.",
    '{{WORLD_2_URL}}': 'https://rollingout.com/2026/09/28/noreaster-northeast-flood-power-outages/',
    '{{ECON_1_FLAG}}': '🏦 RBA DAY · 2:30PM DECISION, 25-POINT HIKE TO 4.60% ALMOST FULLY PRICED IN',
    '{{ECON_1_HEADLINE}}': 'RBA Decision Lands at 2:30pm Today, With a Hike to 4.60% Priced at About 93%',
    '{{ECON_1_SUMMARY}}': 'Markets see a 92–94% chance the cash rate lifts from 4.35% to 4.60% — its highest since 2011 — with the major banks all tipping a September hike and ANZ pencilling in another in November; Treasurer Chalmers also flagged a $6 billion budget improvement yesterday while defending spending as borrowing costs rise.',
    '{{ECON_1_URL}}': 'https://www.vantagemarkets.com/market-news/rba-rate-decision-hike-4-60-september-29-2026/',
    '{{ECON_2_FLAG}}': '🛢️ OIL SHOCK · BRENT BACK ABOVE $107 AS HORMUZ TALKS STALL, DIESEL ALREADY AT 286.8c',
    '{{ECON_2_HEADLINE}}': 'Brent Climbs Back Above $107 Just as Diesel Sits at 286.8 Cents a Litre',
    '{{ECON_2_SUMMARY}}': "With the ACCC's latest weekly data showing diesel up 18.9 cents in a week to 286.8c/L across the five big cities, Monday's oil jump after the stalled Hormuz talks means relief at the bowser is unlikely soon — keep a fuel-cost buffer in every quote and consider a fuel-card to smooth out cash flow.",
    '{{TECH_1_FLAG}}': "🤝 WASHINGTON · TRUMP DINES WITH ANTHROPIC'S AMODEI AS AI SAFETY DEBATE HEATS UP",
    '{{TECH_1_HEADLINE}}': 'Trump Has a Private Dinner With Anthropic CEO Dario Amodei After Months of Friction',
    '{{TECH_1_SUMMARY}}': "The Sunday night White House dinner was the first private sit-down between the two after a Pentagon contract dispute and export-control fight; Trump says he still won't slow AI development because keeping the lead over China matters more, even as Amodei urges safety measures keep pace.",
    '{{TECH_1_URL}}': 'https://www.aljazeera.com/economy/2026/9/28/anthropic-ceo-amodei-to-have-dinner-with-trump-at-white-house',
    '{{TECH_2_FLAG}}': '🏛️ WHITE HOUSE · TRUMP AND SPEAKER JOHNSON CONVENE TOP AI EXECUTIVES TODAY',
    '{{TECH_2_HEADLINE}}': 'Trump and Speaker Johnson Meet Top AI Executives Today on Safety and the China Race',
    '{{TECH_2_SUMMARY}}': "Set for Tuesday 29 September US time, the meeting comes as Republicans face pressure to regulate AI before November's midterms — whatever emerges on guardrails will shape which AI tools and agents small businesses everywhere can access and how they're allowed to operate.",
    '{{ROBOT_1_FLAG}}': '🖐️ HANGZHOU · UNITREE PUTS A 22-JOINT, HUMAN-SIZED ROBOT HAND ON SALE FOR US$6,500',
    '{{ROBOT_1_HEADLINE}}': 'Unitree Launches the Dex5-S, a 22-Joint Human-Sized Robot Hand From US$6,500',
    '{{ROBOT_1_SUMMARY}}': 'Every joint is driven and backdrivable, the hand weighs about 620 grams and can carry up to 2kg — aimed squarely at the dexterity bottleneck holding back humanoids, the same fiddly-hands problem Tesla is wrestling with on Optimus. (Note: launched 21 September; nothing newer with a verifiable source could be found in the 48-hour window.)',
    '{{ROBOT_1_URL}}': 'https://www.digitimes.com/news/a20260922PD221/robot-investment-component-robotics.html',
    '{{AUS_1_HEADLINE}}': 'Chalmers Unveils $6 Billion Budget Improvement Ahead of Expected Rate Hike',
    '{{AUS_1_SUMMARY}}': "The Treasurer says the underlying deficit is $6 billion better than the May budget forecast thanks to lower payments and higher receipts, and that deficits will shrink each year — while defending 2% spending growth against the Coalition's 4.1% as global borrowing costs rise.",
    '{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-09-28/federal-politics-live-blog-chalmers-budget/107202364',
    '{{AUS_2_HEADLINE}}': 'Government Presses On With Ballots and Caps for Second- and Third-Year Working Holiday Visas Despite Industry Concerns',
    '{{AUS_2_SUMMARY}}': "Chalmers says backpackers will keep an 'ongoing role' filling workforce gaps, but the planned annual caps have industry groups worried about labour shortages in sectors that lean on working holiday makers.",
    '{{VIC_1_HEADLINE}}': 'Labor Pledges $80 Million Study to Duplicate the Upfield Line, and Delays Upgrades Until 2033',
    '{{VIC_1_SUMMARY}}': 'Premier Ben Carroll says the duplication — estimated at $650 million to $1.4 billion — will happen by 2033 if Labor is re-elected in November, while eight level crossing removals are pushed back, a reminder that transport projects across Melbourne are now firmly an election battleground.',
    '{{SCI_1_FLAG}}': "🧬 CLEVELAND · ONE CRISPR INFUSION HALVES 'BAD' CHOLESTEROL FOR A FULL YEAR",
    '{{SCI_1_HEADLINE}}': 'A Single CRISPR Treatment Cuts LDL Cholesterol and Triglycerides by About Half for a Full Year',
    '{{SCI_1_SUMMARY}}': 'In a first-in-human trial, one infusion of the gene-editing therapy CTX310 switched off the liver gene ANGPTL3, lowering LDL by up to 52.5% and triglycerides by 47.8% a year later in patients whose lipid disorders resisted drugs, with no serious treatment-related adverse events reported.',
    '{{INSIGHT_TITLE}}': 'Backpacker Visa Caps Are Coming — How AI Can Soak Up the Admin When Labour Stays Tight',
    '{{INSIGHT_BODY}}': "With the government pressing ahead with ballots and caps on second- and third-year working holiday visas, many trades may find casual labour harder to come by just as rates and fuel bite. You can't prompt your way to a spare pair of hands on site, but you can claw back the hours the office side eats: draft quotes and follow-ups from a voice note, turn job photos into a written scope, and let an assistant chase overdue invoices. Even two saved hours a week is real capacity — start with one repetitive task this week, keep a human check on anything that goes to a customer, and measure the time saved before adding another.",
    '{{FACT_1}}': 'The CRISPR therapy CTX310 targets ANGPTL3 because people who are naturally born without working copies of that gene tend to have very low cholesterol and triglycerides — so scientists effectively copied a rare, harmless natural variation rather than inventing something new.',
    '{{FACT_2}}': "Nor'easters are named for the direction their winds blow from — the northeast — and they usually peak between December and February, which is why this weekend's September storm along the US East Coast was such a rarity.",
    '{{FACT_3}}': "The Strait of Hormuz, at the heart of this week's oil jump, is only about 39 kilometres wide at its narrowest point, yet roughly a fifth of the world's oil normally passes through it.",
    '{{JOKE_SETUP}}': "A stonemason was asked how his small business kept customers so loyal, even when the quote came in higher than the other blokes'.",
    '{{JOKE_PUNCHLINE}}': 'He said, "Simple — every job I leave, the customer can still see it standing solid in fifty years."',
    '{{CLOSING_QUOTE}}': '"Courage is not the absence of fear, but the triumph over it."',
    '{{CLOSING_ATTR}}': '— Nelson Mandela',
    '{{CLOSING_MESSAGE}}': "It's a warm, gusty Tuesday in Carrum Downs, good for getting outdoor work done before showers arrive tomorrow afternoon and a possible storm on Thursday. With the RBA's 2:30pm decision due today and diesel still near 287c a litre, it's a smart day to check your quotes, cash flow and fuel buffers before the rain sets in.",
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
