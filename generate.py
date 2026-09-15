#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 16 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 16 Sep (BOM Melbourne-area forecast)
    "{{WEATHER_1}}": "WED 16 SEP · ☀️ Sunny, winds northerly 20–30km/h · 8–17°C",
    "{{WEATHER_2}}": "THU 17 SEP · 🌦️ Partly cloudy, medium chance of showers, winds N–NW shifting SW during the day · 9–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 18 SEP · 🌧️ Cloudy, high chance of showers most likely in the morning, winds N–NW easing then W 15–20km/h · 10–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 19 SEP · ⛈️ Partly cloudy, high chance of showers with possible small hail in the afternoon, winds W turning SW 25–35km/h · 9–14°C",
    "{{WEATHER_5}}": "SUN 20 SEP · 🌬️ Windy with a continued chance of showers easing later in the day, winds SW 25–35km/h tending W 15–25km/h · 10–15°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — a sunny midweek gives way to a cooler, showery stretch from Thursday through the weekend, with a continued chance of small hail Saturday afternoon.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 IRAN–US · TEHRAN REJECTS TRUMP'S OFFER OF TALKS, DEMANDS REPARATIONS AND SANCTIONS RELIEF FIRST",
    "{{WORLD_1_HEADLINE}}": "Iran Rejects Any Talks With the US After Trump Signals He's Open to Negotiating",
    "{{WORLD_1_SUMMARY}}": "Iran's Supreme National Security Council secretary Mohsen Rezaei dismissed Donald Trump's Monday remarks that he was open to resuming talks, posting that there will be 'no talks until Iran's conditions are met' — including war reparations and the lifting of sanctions — as the war over the Strait of Hormuz drags into its fifth month.",
    "{{WORLD_1_URL}}": "https://www.brecorder.com/news/40439580/iran-rejects-any-talks-with-us-after-trump-remarks",

    "{{WORLD_2_FLAG}}": "🇸🇦 MIDDLE EAST · HOUTHI MISSILES AND DRONES WOUND 13 CIVILIANS IN SOUTHERN SAUDI ARABIA",
    "{{WORLD_2_HEADLINE}}": "Saudi Arabia Vows a 'Firm' Response After Houthi Missile and Drone Attacks Wound 13 Civilians",
    "{{WORLD_2_SUMMARY}}": "Yemen's Iran-backed Houthis struck Khamis Mushait, Abha and Taif with missiles and drones, wounding 13 people, prompting the Saudi-led coalition to warn it would take 'all necessary operational measures' to deter further attacks — the latest escalation since the Houthis seized Yemen's Red Sea coast and the Bab el-Mandeb Strait last week.",
    "{{WORLD_2_URL}}": "https://www.france24.com/en/middle-east/20260915-middle-east-live-houthi-attacks-wound-13-civilians-in-southern-saudi-arabia",

    # Economics
    "{{ECON_1_FLAG}}": "📉 MARKETS · ASX SINKS TO A SIX-WEEK LOW AS OIL-DRIVEN INFLATION FEARS BITE",
    "{{ECON_1_HEADLINE}}": "ASX Slides to Its Lowest Level Since June as Rising Oil Prices Stoke Inflation Fears",
    "{{ECON_1_SUMMARY}}": "The local share market closed at a six-week low on Tuesday after Westpac forecast the RBA will lift the cash rate again in November, joining NAB's call for a hike as early as this month — both banks pointing to the same driver: oil holding above US$100 a barrel and threatening to push petrol and freight costs through the economy just as businesses were hoping for relief.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-15/asx-markets-business-news-live-updates-tuesday-15-september/107153476",

    "{{ECON_2_FLAG}}": "⛽ FUEL · ANALYSTS WARN OIL COULD HIT $150 A BARREL IF THE MIDDLE EAST WAR DRAGS ON",
    "{{ECON_2_HEADLINE}}": "Oil Price Could Surge to $150 a Barrel as the Middle East War Intensifies, Analysts Warn",
    "{{ECON_2_SUMMARY}}": "With the Strait of Hormuz, the Red Sea and now inland Saudi Arabia all active war zones, the International Energy Agency is calling it the largest supply disruption in the oil market's history — meaning the fuel surcharge you build into a quote today might already be out of date by the time you invoice.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🛡️ CYBERSECURITY · AUSTRALIA'S SIGNALS DIRECTORATE WANTS AN AI 'EARLY WARNING SYSTEM'",
    "{{TECH_1_HEADLINE}}": "Australia Needs an AI 'Early Warning System', Top Cybersecurity Chief Warns",
    "{{TECH_1_SUMMARY}}": "Australian Signals Directorate director-general Abigail Bradshaw says the country needs to get ahead of AI-powered cyberattacks by using AI defensively too — a reminder for any small business that the same tools now automating your quotes and admin are also worth pointing at your own email security and password habits.",
    "{{TECH_1_URL}}": "https://www.abc.net.au/news/2026-09-15/australia-needs-ai-warning-system-cyber-security-chief-says/107151268",

    "{{TECH_2_FLAG}}": "⚖️ AI COPYRIGHT · LEAKED FEDERAL DOCUMENTS SHOW A PLAN TO LET AI TRAIN ON CONTENT FREE OF CHARGE",
    "{{TECH_2_HEADLINE}}": "Leaked Documents Reveal a Federal Plan to Let AI Companies Train on Content Without Paying Creators",
    "{{TECH_2_SUMMARY}}": "A leaked Attorney-General's Department proposal, tabled in the Senate by David Pocock, would let AI companies train on Australian content for free once they've struck deals with enough rights-holder groups — even covering people who never signed up. It's a live reminder that the job photos, site videos and marketing copy your business puts online may already sit in a legal grey zone once an AI company decides to scrape it.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 HUMANOID ROBOTS · AGILITY ROBOTICS' DIGIT 5 CAN NOW WORK NEXT TO PEOPLE WITHOUT A SAFETY CAGE",
    "{{ROBOT_1_HEADLINE}}": "Agility Robotics Unveils Digit 5, a Humanoid Robot Safe Enough to Work Beside People With No Barriers",
    "{{ROBOT_1_SUMMARY}}": "The latest version of Agility's warehouse humanoid ships with new legs, upgraded batteries and a more comprehensive safety architecture that the company says lets it operate in close proximity to people without physical safety barriers — another sign that 'robot on the floor next to you' is moving from pilot program to standard fit-out.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/agilitys-digit-5-humanoid-has-new-legs-batteries-safety-upgrades/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Greens Accuse Labor of 'Betraying Pensioners' Over Private Health Rebate Changes",
    "{{AUS_1_SUMMARY}}": "The federal government is moving to wind back the private health insurance rebate for people aged 65 and over, but will need the Greens' support to pass it — the Greens say the move breaks a promise to older Australians already stretched by cost-of-living pressure.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-15/federal-politics-live-september-15/107152270",

    "{{AUS_2_HEADLINE}}": "Pauline Hanson Offers a Qualified Apology Over Comments About Indigenous Australians and the PM's Mother",
    "{{AUS_2_SUMMARY}}": "In the same day's parliamentary sitting, the One Nation leader walked back remarks that had drawn cross-party condemnation, offering a qualified apology — a reminder that even a fairly ordinary sitting week in Canberra can still produce a headline by lunchtime.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria-Wide Public Hospital Doctors' Strike Called Off at the Eleventh Hour",
    "{{VIC_1_SUMMARY}}": "A 24-hour strike by public hospital doctors across Victoria, planned for midday Tuesday over stalled pay talks, was pulled after the Victorian Hospitals Industrial Association won a Fair Work Commission bid arguing the strike notice period was too short — the underlying pay dispute remains unresolved.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 QUANTUM ENGINEERING · A MICROSCOPE POWERED BY A QUANTUM COMPUTER COULD SEE MORE WHILE DAMAGING LESS",
    "{{SCI_1_HEADLINE}}": "Scientists Are Building a Microscope Powered by a Quantum Computer",
    "{{SCI_1_SUMMARY}}": "Researchers are combining electron microscopy with quantum computing techniques to pull far more information out of each electron that hits a sample, aiming to image delicate materials — like biological tissue or heat-sensitive electronics — in sharper detail while hitting them with less energy than a conventional electron microscope requires.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Oil at $100-Plus a Barrel Isn't a One-Off Anymore — How AI Can Help You Reprice Before It Costs You",
    "{{INSIGHT_BODY}}": "With analysts now warning oil could hit $150 a barrel if the Middle East war drags on, the businesses getting hurt aren't the ones using more fuel — they're the ones whose quotes and standing contracts haven't caught up with what fuel actually costs by the time the job runs. A handful of AI-powered quoting and job-costing tools, many already built into ServiceM8, Tradify and Simpro, can now flag a job's fuel and travel cost against a recent price feed and prompt you to adjust the quote before you send it, rather than finding out at BAS time that a fixed-price job quietly ate your margin. It's ten minutes of setup for a habit that pays for itself the next time crude jumps overnight.",

    # Fun facts
    "{{FACT_1}}": "Agility Robotics' new Digit 5 humanoid, unveiled this week, is built to work within arm's reach of people with no safety cage at all — a shift only possible because collaborative-robot safety standards, which took regulators the better part of two decades to write for industrial arms, are now being adapted for robots that walk around on legs.",
    "{{FACT_2}}": "The 159-litre oil barrel used to price every 'oil hits $100' headline traces back to 19th-century Pennsylvania producers, who simply grabbed whatever cask was lying around in bulk at the time — old herring barrels — meaning the unit behind today's oil market panic is a 160-year-old fish-packing measurement.",
    "{{FACT_3}}": "Israel's Knesset is elected entirely by nationwide proportional representation with no local electorates at all, which is why a brand-new party like Gadi Eisenkot's Yashar, formed only this year, can leap to the top of the polls within months rather than needing years to win seats one district at a time.",

    # Joke
    "{{JOKE_SETUP}}": "A bricklayer was asked how his small business always kept every course dead straight, even on a job that had to be rushed.",
    "{{JOKE_PUNCHLINE}}": "He said the secret was staying level-headed — literally, he never once put the spirit level down.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"You miss 100% of the shots you don't take.\"",
    "{{CLOSING_ATTR}}": "— Wayne Gretzky",
    "{{CLOSING_MESSAGE}}": "Today's shaping up as the calm before a showery stretch around Carrum Downs, with sunshine giving way to a cooler, wetter run from Thursday through the weekend — a good excuse to get outdoor jobs locked in today. Oil pushing back above $100 a barrel, with talk of $150 if the Middle East war grinds on, is the story actually worth watching this Wednesday — worth a quick check that your fuel line items still add up.",
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
