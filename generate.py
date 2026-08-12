#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 13 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 13 Aug (BOM)
    "{{WEATHER_1}}": "THU 13 · ⛅ Partly cloudy, slight chance of a shower · 6–14°C",
    "{{WEATHER_2}}": "FRI 14 · ☁️ Cloudy, slight chance of a shower, breezy · 7–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SAT 15 · 🌧️ Very high chance of showers, most likely morning · 7–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 16 · 🌦️ High chance of showers about the Dandenongs, medium elsewhere · 8–15°C",
    "{{WEATHER_5}}": "MON 17 · 🌤️ Cloudy early, medium chance of a shower, chance of morning fog · 8–16°C",
    "{{WEATHER_ALERT}}": "Nothing current for Carrum Downs itself — a Flood Warning remains active for the Wimmera and Richardson Rivers in western Victoria and a Coastal Hazard Warning continues for East, West and South Gippsland after last week's rain, so it's worth checking BOM directly before any job or drive that way",

    # World
    "{{WORLD_1_FLAG}}": "🇷🇺🇺🇸 RUSSIA · US MARINE VETERAN FREED AFTER NEARLY FOUR YEARS IN RUSSIAN DETENTION",
    "{{WORLD_1_HEADLINE}}": "US Marine Veteran Robert Gilman Freed From Russia After Nearly Four Years, Flown Home for Treatment",
    "{{WORLD_1_SUMMARY}}": "Robert Gilman, a 32-year-old US Marine veteran detained in Russia since 2022 on disputed charges, was released on humanitarian grounds this week after President Trump raised his deteriorating health directly with Vladimir Putin — no prisoner exchange took place. Gilman's advocates feared he was 'near death' after alleged torture and mistreatment; he's now on his way to a US military hospital in Texas for medical and psychological assessment.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/12/g-s1-138323/former-us-marine-russia",

    "{{WORLD_2_FLAG}}": "🇨🇴 COLOMBIA · DEATH TOLL PASSES 180 AFTER MAJOR EARTHQUAKE, RESCUERS RACE THE CLOCK",
    "{{WORLD_2_HEADLINE}}": "Colombia Earthquake Death Toll Passes 180 as Rescuers Struggle to Reach a Cut-Off Epicentre",
    "{{WORLD_2_SUMMARY}}": "A 7.4-magnitude earthquake that struck west of Bogotá has killed at least 181 people, injured close to 2,600 and left roughly 195 officially missing — with civilian-run databases putting that figure closer to 4,000. Rescue teams are still struggling to reach the cut-off epicentre as the search for survivors trapped in collapsed buildings runs up against a critical time window, straining Colombia's newly formed government.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/08/12/g-s1-138315/colombia-earthquake-updates",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺📊 RBA · CASH RATE HELD AT 4.35%, NO RELIEF YET FOR BORROWERS OR BUSINESS LOANS",
    "{{ECON_1_HEADLINE}}": "RBA Holds Cash Rate at 4.35% for a Second Straight Meeting as Inflation Stays 'Too High'",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank left the cash rate on hold at 4.35% this week, choosing not to add a fourth hike, with annual inflation easing slightly to 3.8% but the RBA's preferred underlying measure stuck at 3.6% — still above target. For a small trades operator, it's a pause rather than relief: business loan and equipment finance repayments stay where they are for now, with no clear signal on when — or if — the next move is down.",
    "{{ECON_1_URL}}": "https://www.smartcompany.com.au/economy/rba-leaves-interest-rate-unchanged-4-35-inflation-high/",

    "{{ECON_2_FLAG}}": "⛽🇦🇺 FUEL · MELBOURNE PETROL EASES OFF ITS EXCISE-DRIVEN HIGH, ACCC TIPS FURTHER FALLS",
    "{{ECON_2_HEADLINE}}": "Melbourne Petrol Eases to an Average 200.8c/L as the Post-Excise Spike Starts to Unwind",
    "{{ECON_2_SUMMARY}}": "Melbourne's average unleaded price has slipped back to around 200.8c/L this week, with the cheapest sites near 186c/L, as the spike from the fuel excise's return to full rate on 3 August starts to work its way back down — the ACCC's latest monitoring points to average prices easing further toward the mid-190s over coming days. Worth holding off locking in fuel surcharges on new quotes until the cycle settles.",
    "{{ECON_2_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖🏫 AI IN EDUCATION · ANTHROPIC LAUNCHES CLAUDE FOR TEACHERS AS AI RACES INTO THE CLASSROOM",
    "{{TECH_1_HEADLINE}}": "Anthropic Launches Claude for Teachers, Joining OpenAI and Google in the Race to Own Classroom AI",
    "{{TECH_1_SUMMARY}}": "Anthropic this week unveiled Claude for Teachers, a version of its assistant built around all 50 US states' academic standards to help with lesson planning, personalising materials to students, and using classroom data to guide instruction. It's the same pattern small trades operators are seeing everywhere AI touches — general tools getting purpose-built versions for specific jobs, which is worth watching for quoting, scheduling and admin tools built specifically for tradies rather than repurposed generic chatbots.",
    "{{TECH_1_URL}}": "https://keyt.com/stacker-ai/2026/08/11/anthropic-unveils-claude-for-teachers-joining-openai-and-google-in-race-to-dominate-classroom-ai/",

    "{{TECH_2_FLAG}}": "🤖📈 AI ADOPTION · GOOGLE'S GEMINI APP PASSES ONE BILLION MONTHLY USERS",
    "{{TECH_2_HEADLINE}}": "Google's Gemini App Hits One Billion Monthly Users, Becoming the Company's Fastest-Growing Product Ever",
    "{{TECH_2_SUMMARY}}": "Google confirmed this week that Gemini has passed one billion monthly active users, up from 650 million in October, with the company saying 63% of users now talk directly to the assistant rather than through a search box. With every major AI assistant now claiming a billion-user milestone, the practical question for a small business isn't which one is 'best' — it's picking one, learning its quirks properly, and sticking with it instead of chasing the newest name.",
    "{{TECH_2_URL}}": "https://www.pymnts.com/news/artificial-intelligence/2026/gemini-app-hits-1-billion-users-faster-than-any-other-google-product/",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭🤖 AUTOMATION · NORTH AMERICAN ROBOT ORDERS KEEP CLIMBING THROUGH Q2 2026",
    "{{ROBOT_1_HEADLINE}}": "North American Robot Orders Rise Again in Q2 2026 as Automation Demand Broadens Across Industries",
    "{{ROBOT_1_SUMMARY}}": "North American companies ordered 8,940 industrial robots worth $622 million in the second quarter of 2026, a 4.3% rise in units and 21.3% rise in order value on the same period last year, with first-half 2026 orders up across a widening spread of industries beyond car making. It's a reminder that most of the real automation growth right now isn't humanoids in the headlines — it's ordinary fixed and mobile robots quietly going into more factories and warehouses every quarter.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/08/11/robot-orders-increase-in-q2-as-automation-demand-broadens-across-industries/26934/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Federal Government Commits $308 Million for 448 New Homes for Women and Children Fleeing Violence",
    "{{AUS_1_SUMMARY}}": "Housing Minister Clare O'Neil confirmed a $308 million federal investment this week to deliver 448 homes nationally for women and children escaping domestic violence, including $16.8 million for 19 homes in one initial tranche. Family and domestic violence remains the leading cause of homelessness for women and children in Australia, with close to 12,000 seeking short-term accommodation missing out each year and being forced back into unsafe homes.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/podcast-episode/housing-in-spotlight-as-domestic-violence-crisis-continues/y18y0ip13",

    "{{AUS_2_HEADLINE}}": "Commonwealth Bank Posts Record Annual Profit, Cash Earnings Up 7% to Nearly $11 Billion",
    "{{AUS_2_SUMMARY}}": "Australia's largest bank reported cash profit after tax up 7% to $10.98 billion for the year to June, beating analyst forecasts, with home lending up 5.8% and business lending up 9.6% despite intense competition. CBA flagged the broader economy as still supported by low unemployment even as growth slows — a sign credit is still flowing to business borrowers even with rates on hold.",
    "{{AUS_2_URL}}": "https://www.investing.com/news/stock-market-news/commonwealth-bank-of-australias-annual-profit-rises-7-4852896",

    # Victoria
    "{{VIC_1_HEADLINE}}": "New Premier Ben Carroll Leaves the Door Open to a Sweeping Review of Melbourne's Suburban Rail Loop",
    "{{VIC_1_SUMMARY}}": "Since being sworn in as Victorian premier in late July, Ben Carroll has restructured his cabinet — scrapping both the transport infrastructure and Suburban Rail Loop ministerial posts — and has not denied reports he's weighing a full review of the multi-billion-dollar SRL project and whether its funding could be redirected. Carroll insists it isn't a precursor to cancelling the project outright, but for anyone in construction or trades tied to Victoria's Big Build pipeline, it's a live question worth watching over the coming weeks.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 SCIENCE · MIT FINDS THE BRAIN CAN REASON WITHOUT USING LANGUAGE AT ALL",
    "{{SCI_1_HEADLINE}}": "MIT Study Finds the Brain's Language and Logical Reasoning Systems Are Completely Separate",
    "{{SCI_1_SUMMARY}}": "MIT neuroscientists report that people with severe language impairment from stroke could still solve logic puzzles just as well as anyone else, while brain scans of healthy adults showed the language-processing regions stayed quiet during both inductive and deductive reasoning tasks. It overturns the assumption that words are the brain's vehicle for thought — reasoning, it turns out, runs on its own separate system entirely.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Every Big AI Assistant Just Passed a Billion Users — Your Business Doesn't Need the 'Best' One, Just One You'll Actually Use",
    "{{INSIGHT_BODY}}": "Between Gemini's billion-user milestone and Anthropic's new classroom-specific tool, this week is another reminder that every major AI player is racing to be the one assistant you open by default. For a small trades business, that race is mostly noise — the AI tools that actually save time are the boring ones already built into the job management software you use for quoting and invoicing, not whichever chatbot is dominating headlines this month. Pick one tool, learn its quirks properly over a few weeks, and resist the urge to keep switching every time a new name gets a billion-user press release — consistency beats chasing the 'best' model every single time.",

    # Fun facts
    "{{FACT_1}}": "The Akubra hat traces back to a Tasmanian hat mill founded by Benjamin Dunkerley in 1874, with the name itself said to come from an Aboriginal word for 'head covering' — the felt is still made from rabbit fur, a material chosen because it's naturally water-resistant and holds its shape through decades of outdoor work.",
    "{{FACT_2}}": "The 'stump-jump plough,' developed by South Australian farmers in 1876, used a hinged, weighted blade that could ride up and over tree stumps and rocks instead of snapping on impact — the invention opened up vast stretches of mallee scrub country to wheat farming that had been considered unworkable.",
    "{{FACT_3}}": "The Australian slang word 'furphy,' meaning a rumour or tall tale, comes from water carts built by John Furphy's foundry in Shepparton, Victoria, from the 1880s — WWI soldiers swapped gossip and unverified stories while queued at the carts, and the brand name stamped on the tank stuck as the word for an unreliable yarn.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the artificial turf installer's small business never have a slow season?",
    "{{JOKE_PUNCHLINE}}": "Because his lawns never needed mowing, watering or excuses — just an invoice, twelve months of the year.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"In the midst of chaos, there is also opportunity.\"",
    "{{CLOSING_ATTR}}": "— Sun Tzu",
    "{{CLOSING_MESSAGE}}": "It's a mild, partly cloudy Thursday in Carrum Downs with just a slight chance of a shower, before the weekend brings a wetter, breezier turn — a good window to get outdoor jobs ticked off while it holds. With the RBA holding steady and fuel prices finally easing off their excise-driven high, it's a decent morning to run the numbers on any quotes that have been sitting on cost assumptions from a fortnight ago.",
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
