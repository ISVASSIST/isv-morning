#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 15 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 15 Sep (BOM Melbourne-area forecast)
    "{{WEATHER_1}}": "TUE 15 SEP · ⛅ Cloudy with a slight chance of a shower near the ranges, mostly dry on the coast, winds light becoming N–NW 15–25km/h · 9–15°C",
    "{{WEATHER_2}}": "WED 16 SEP · ☀️ Sunny, winds northerly 20–30km/h · 8–17°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "THU 17 SEP · 🌦️ Partly cloudy, medium chance of showers, winds N–NW shifting SW during the day · 9–16°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 18 SEP · 🌧️ Cloudy, high chance of showers most likely in the morning, winds N–NW easing then W 15–20km/h · 10–15°C",
    "{{WEATHER_5}}": "SAT 19 SEP · ⛈️ Partly cloudy, high chance of showers with possible small hail in the afternoon, winds W turning SW 25–35km/h · 9–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — a dry, mild start to the week gives way to increasing showers from Thursday, with possible small hail by Saturday afternoon.",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 UKRAINE · RUSSIAN DRONE HITS TRAIN NEAR POLISH BORDER MINUTES AFTER A DIPLOMATIC DELEGATION PASSED THROUGH",
    "{{WORLD_1_HEADLINE}}": "Russian Drone Strikes a Train Near the Ukraine-Poland Border Just After a Delegation Including Boris Johnson Rolled Through",
    "{{WORLD_1_SUMMARY}}": "A diplomatic train carrying former UK PM Boris Johnson, former Swedish PM Carl Bildt and EU security advisers left Yahodyn station ahead of schedule after a conference in Kyiv — narrowly avoiding a Russian drone that struck the platform and track minutes later. A separate train still at the station, carrying former CIA director David Petraeus, was also hit; no casualties were reported, but the strike underlines how close Western officials are now operating to the front line.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/09/14/g-s1-143140/russian-drone-hits-train-near-ukraine-poland-border-soon-after-dignitaries-passed-through/",

    "{{WORLD_2_FLAG}}": "🇨🇳 AI DIPLOMACY · BEIJING CALLS ANTHROPIC CEO'S AI WARNING 'FEARMONGERING' AHEAD OF THE TRUMP-XI SUMMIT",
    "{{WORLD_2_HEADLINE}}": "China Rejects Anthropic CEO's Call to Curb Its AI Development as 'Fearmongering'",
    "{{WORLD_2_SUMMARY}}": "An essay from Anthropic's Dario Amodei warning that a Chinese lead in AI would pose 'grave danger' to the world drew a sharp rebuke from Beijing's Foreign Ministry, which accused the industry of stoking Cold War-style panic days before Xi Jinping is due in Washington for a September 24 summit with Trump on trade, AI chips and Taiwan. A reminder that the rules governing which AI tools you get to use are being fought over well above your pay grade.",
    "{{WORLD_2_URL}}": "https://www.bloomberg.com/news/articles/2026-09-14/china-rejects-ai-fearmongering-after-amodei-urges-slowdown",

    # Economics
    "{{ECON_1_FLAG}}": "📈 RATES · INFLATION NOW 'PROBLEM NUMBER ONE' AS RBA HIKE ODDS TOP 75%",
    "{{ECON_1_HEADLINE}}": "RBA Says Inflation Is Economic Problem Number One as Markets Price a 75%+ Chance of a Rate Hike This Month",
    "{{ECON_1_SUMMARY}}": "With the cash rate already lifted three times this year, the Reserve Bank is signalling inflation remains its central concern, and markets are now pricing at least a 75% chance of a hike to a 15-year high of 4.6% at the September 29 board meeting. NAB, Deutsche Bank, UBS and Morgan Stanley have all shifted to forecasting a hike this month rather than November, which flows straight through to overdraft and equipment-finance rates.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-15/rba-inflation-economy-interest-rates/107151344",

    "{{ECON_2_FLAG}}": "⛽ FUEL · PUMP PRICES SET TO CLIMB FURTHER AS MIDDLE EAST CONFLICT ESCALATES",
    "{{ECON_2_HEADLINE}}": "Australian Fuel Prices Expected to Rise Again as Middle East Conflict Escalates",
    "{{ECON_2_SUMMARY}}": "Average unleaded is already sitting around $2.11 a litre nationally, and analysts warn there's more to come as the conflict widens and crude holds above US$100 a barrel — only about a third of the recent spike in landed fuel costs has reached the bowser so far. Worth building a fuel surcharge into quotes now rather than absorbing another jump in a fortnight.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💼 AI IN FINANCE · ANTHROPIC LAUNCHES CLAUDE FOR FINANCIAL ADVISERS, WIRED DIRECTLY INTO PORTFOLIO DATA",
    "{{TECH_1_HEADLINE}}": "Anthropic Launches 'Claude for Financial Advisors', Connecting Its AI Directly to Real Client Portfolios",
    "{{TECH_1_SUMMARY}}": "The new tool plugs Claude straight into investment analytics and wealth-management software from BlackRock, Charles Schwab and Addepar, so advisers can prep for client meetings and review portfolios without re-typing numbers into a chat window. The bigger trend for a small operator: 'wire the AI into your real numbers, not just a chat box' is already available through everyday bookkeeping software like Xero — you don't need a bespoke version built for your trade to start using it.",
    "{{TECH_1_URL}}": "https://money.usnews.com/investing/news/articles/2026-09-14/anthropic-targets-financial-advisers-with-new-claude-tool",

    "{{TECH_2_FLAG}}": "📞 AI RECEPTIONISTS · AUSTRALIAN-ACCENT AI PHONE AGENTS ARE NOW CHEAP ENOUGH FOR A ONE-TRUCK BUSINESS",
    "{{TECH_2_HEADLINE}}": "AI Phone-Answering Services With Natural Australian Accents Are Maturing Fast for Small Trades Businesses",
    "{{TECH_2_SUMMARY}}": "A wave of Australian-hosted AI receptionist services now start from under $100 a month, answering calls around the clock, qualifying jobs, sending SMS follow-ups and booking straight into trade-specific software like ServiceM8, simPRO or AroFlo. The catch is where the call audio actually gets processed — an obvious overseas accent still makes plenty of callers hang up, and routing audio offshore can raise its own privacy questions, so it's worth asking any provider exactly where the data goes before you sign up.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 HUMANOID ROBOTS · UNITREE UPGRADES ITS G1 HUMANOID TO THE G1+, SHARPENING PERCEPTION AND BATTERY LIFE",
    "{{ROBOT_1_HEADLINE}}": "Unitree Launches the G1+, a Fully Upgraded Version of Its Popular Humanoid Robot",
    "{{ROBOT_1_SUMMARY}}": "The refresh brings six upgrades across motion performance, perception and intelligence — stronger neck and joint movement, better visual and tactile sensing, longer battery life and improved far-field voice pickup so the robot can be commanded across a noisy work floor. It's another sign the humanoid robot market is iterating like a consumer electronics category now, not a research demo — hardware generations arriving every few months rather than every few years.",
    "{{ROBOT_1_URL}}": "https://panews.io/articles/01a09ef1-21bc-762f-a419-1d09651f7797",

    # Australia
    "{{AUS_1_HEADLINE}}": "Whyalla Steelworks' Blast Furnace Confirmed Permanently Closed, About 500 Jobs to Go",
    "{{AUS_1_SUMMARY}}": "Administrators confirmed on Monday the furnace will never be relit, ending months of failed restart attempts since an unplanned shutdown in April. A $10.2 million support package has been announced for the roughly 500 employees and 100-plus labour-hire workers affected, while the sale of the wider steelworks to Jindal Steel or M Resources remains on track by year's end.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-14/hundreds-of-jobs-to-go-at-whyalla-steelworks/107149844",

    "{{AUS_2_HEADLINE}}": "SA Health Staffer Reprimanded for Snooping on AFL Legend Tony Modra's Medical Records",
    "{{AUS_2_SUMMARY}}": "One of three SA Health employees investigated for inappropriately accessing Modra's records after his serious truck crash injury in June has been formally reprimanded, with two more investigations still open. A pointed reminder that any business holding client or patient data needs a genuine access log, not just a password.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne's Auction Clearance Rate Holds Above 60%, Among the Strongest of Any Australian Capital",
    "{{VIC_1_SUMMARY}}": "Melbourne's weekly clearance rate sat at roughly 64% heading into the weekend, comfortably ahead of the sub-52% national average, as buyers keep moving despite the prospect of another rate rise this month — a sign the local property and renovation pipeline is still healthy even while household budgets tighten elsewhere.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 CARDIOLOGY · A WEARABLE PATCH CATCHES A HIDDEN CAUSE OF HIGH BLOOD PRESSURE THAT ROUTINE TESTS MISS",
    "{{SCI_1_HEADLINE}}": "Scientists Find a Hidden Cause of High Blood Pressure That Routine Tests Can Miss",
    "{{SCI_1_SUMMARY}}": "A UK-led team fitted 60 patients with a waist-worn device called U-RHYTHM, sampling fluid beneath the skin every 20 minutes for 24 hours, and found bursts of hormone production overnight — while asleep — in people with a condition called primary aldosteronism, which affects up to one in five people with high blood pressure and is rarely caught by a single daytime blood test. It could shift hypertension diagnosis away from one-off pinpricks and towards tracking the body's rhythm over a full day and night.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Anthropic Just Launched an AI Tool for Financial Advisers — Your Bookkeeping Software Already Has the Trades Version",
    "{{INSIGHT_BODY}}": "Claude for Financial Advisors, launched this week, connects Anthropic's AI directly to real portfolio data from BlackRock, Schwab and Addepar so advisers stop re-typing numbers into a chat window and start asking questions about the actual figures. The same idea — wiring AI straight into your real numbers instead of a generic chatbot — is already sitting inside the bookkeeping software plenty of trades businesses already pay for, from Xero to MYOB. You don't need to wait for someone to build a 'tradie edition'; the AI copilot in your existing accounting software is the trades equivalent, and it's worth ten minutes this week finding out what yours can already do.",

    # Fun facts
    "{{FACT_1}}": "The Bessemer process, patented by Henry Bessemer in 1856, was the first method to mass-produce steel cheaply — blasting air through molten pig iron to burn off impurities in minutes rather than the better part of a day's blacksmith labour. It's the reason steel could become the backbone of bridges, rail and blast furnaces everywhere, including the one that just went cold for good at Whyalla this week.",
    "{{FACT_2}}": "Singapore's fertility rate has fallen to just 0.87 births per woman, against the roughly 2.1 a developed economy needs to hold its population steady — a shortfall serious enough that the government is now offering close to $55,000 in support per child, a reminder that a modern economy's biggest long-term problem can end up being its labour supply rather than its factories.",
    "{{FACT_3}}": "The diplomatic train that dodged a Russian drone near the Ukraine-Poland border this week left its station ahead of schedule specifically to avoid being targeted — the same tactic used to move VIPs through active front lines since at least the First World War, when unmarked, unscheduled services were the safest way to move anyone worth targeting.",

    # Joke
    "{{JOKE_SETUP}}": "A commercial window tinting installer was asked how his small business always kept every client happy, even in the middle of a Melbourne heatwave.",
    "{{JOKE_PUNCHLINE}}": "He said the secret was simple: never let the quote get too transparent before the job's actually locked in.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Today's accomplishments were yesterday's impossibilities.\"",
    "{{CLOSING_ATTR}}": "— Robert H. Schuller",
    "{{CLOSING_MESSAGE}}": "It's a dry, mild start to the week around Carrum Downs, with showers building from Thursday and a chance of small hail by Saturday — a good window to get outdoor jobs done before then. Locally the week's news is a mixed bag: Whyalla's blast furnace has gone cold for good and another rate rise looks increasingly likely, but Melbourne's auction market is still humming along above 60%, and Tuesday's a fair day to make sure your own numbers — and your AI tools — are working as hard as you are.",
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
