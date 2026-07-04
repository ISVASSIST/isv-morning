#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 05 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 5 Jul
    "{{WEATHER_1}}": "SUN 5 · ☁️ Cloudy · 9–14°C",
    "{{WEATHER_2}}": "MON 6 · ☀️ Sunny, frosty start · 3–15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "TUE 7 · ⛅ Mostly sunny · 5–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "WED 8 · ⛅ Partly cloudy · 6–14°C",
    "{{WEATHER_5}}": "THU 9 · 🌧 Showers return · 7–13°C",
    "{{WEATHER_ALERT}}": "⚠ FROSTY START MONDAY · ELECTRICITY DEFAULT OFFER PRICES DOWN FROM THIS MONTH",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸 UNITED STATES · AMERICA 250 · NATION MARKS QUARTER-MILLENNIUM",
    "{{WORLD_1_HEADLINE}}": "The United States Marks Its 250th Birthday With the Largest Fireworks Display in History",
    "{{WORLD_1_SUMMARY}}": "America celebrated 250 years of independence on Friday with tall ships from 30 nations sailing into New York Harbour, a record-breaking fireworks display, and a heat dome pushing Fourth of July temperatures toward all-time highs across more than half the country. World leaders including European Council President António Costa sent congratulatory messages marking the milestone, even as the Trump administration's migration policies continue to draw friction with allies. A reminder of how much the world still calibrates its calendar around the US, for better or worse.",
    "{{WORLD_1_URL}}": "https://www.cbsnews.com/live-updates/july-4th-america-250-birthday/",

    "{{WORLD_2_FLAG}}": "🇻🇦 VATICAN · CATHOLIC CHURCH · DEEPEST SCHISM SINCE 1988",
    "{{WORLD_2_HEADLINE}}": "Vatican Declares Traditionalist Society in Schism, Excommunicates Its Bishops",
    "{{WORLD_2_SUMMARY}}": "The Vatican formally declared the Society of St Pius X to be in schism this week, automatically excommunicating its bishops after the traditionalist group consecrated four new bishops on July 1 without papal authorisation. The SSPX's superior general rejected the ruling in a letter to Pope Leo XIV on Friday, calling it 'objectively unjust and invalid' — marking the most serious rupture in the Catholic Church since the original Lefebvre consecrations of 1988.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/world/the-vatican/vatican-declares-society-st-pius-x-schism-excommunicates-bishops-inval-rcna352691",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL PRICES · FEDERAL GOVERNMENT · EXCISE RELIEF EXTENDED",
    "{{ECON_1_HEADLINE}}": "Government Extends Fuel Excise Relief for Another Month, Keeping Petrol and Diesel 16 Cents Cheaper",
    "{{ECON_1_SUMMARY}}": "The Albanese Government has extended the fuel excise discount for a further month, keeping petrol and diesel 16 cents a litre cheaper than normal through to August 2 — worth roughly $11 a tank — at a cost to the budget of around $400 million. The Heavy Vehicle Road User Charge has been cut by the same 16 cents for truck operators over the same period. It's smaller relief than the original 32-cent cut that applied through June, so don't assume last month's fuel line item still holds.",
    "{{ECON_1_URL}}": "https://www.pm.gov.au/media/additional-fuel-excise-relief-month-july",

    "{{ECON_2_FLAG}}": "🔌 ENERGY PRICES · AER · DEFAULT OFFER FALLS UP TO 21%",
    "{{ECON_2_HEADLINE}}": "Electricity Default Market Offer Prices Drop Sharply From July 1 — Small Business Rates Down Up to 21% in Some Regions",
    "{{ECON_2_SUMMARY}}": "New Default Market Offer pricing took effect this month, cutting small business electricity rates by 7.6% to 21.2% in parts of NSW, 12.8% in South East Queensland and 15.2% in South Australia, depending on distribution zone. Unlike the federal energy rebates that ended last December, this saving happens automatically on the default offer — but only if you're actually on it. Worth a quick check with your retailer this week if you haven't looked at your rate since last financial year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 ANTHROPIC · CLAUDE SONNET 5 · NEW DEFAULT MODEL LIVE",
    "{{TECH_1_HEADLINE}}": "Anthropic Makes Claude Sonnet 5 the New Default AI Model for Free and Pro Users",
    "{{TECH_1_SUMMARY}}": "Anthropic's Claude Sonnet 5 became the default model for Free and Pro users this week — its most agentic Sonnet yet, running close to flagship-level performance at a fraction of the price, with introductory pricing locked in until the end of August. For a small business owner who's never had to think about which AI model they're using, the practical upshot is simple: the free or cheap version of the tool just got meaningfully more capable overnight, with no action required.",
    "{{TECH_1_URL}}": "https://www.anthropic.com/news/claude-sonnet-5",

    "{{TECH_2_FLAG}}": "🤖 SQUARE · AI COMMERCE · ORDERS PLACED INSIDE CHATGPT AND CLAUDE",
    "{{TECH_2_HEADLINE}}": "Square Lets US Food and Beverage Sellers Take Orders Directly Inside ChatGPT and Claude",
    "{{TECH_2_SUMMARY}}": "Square switched on a new integration this month letting customers discover a restaurant, browse its menu and place an order entirely inside a ChatGPT or Claude conversation — routing straight into the seller's existing POS with no setup and no added marketplace commission on top of standard processing fees. It's a small, concrete example of AI chat moving from 'assistant that answers questions' to 'assistant that takes the sale' — worth watching for how fast that idea spreads from ordering a burger to booking a tradie.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · AGIBOT · HUMANOID ROBOT-AS-A-SERVICE LAUNCHES IN UK",
    "{{ROBOT_1_HEADLINE}}": "AGIBOT Debuts Its A3 Humanoid Robot in Europe and Launches a UK Robot-as-a-Service Rental Model",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics maker AGIBOT unveiled its A3 humanoid at a partner conference in London this week, alongside a new UK rental scheme offering the robot from £1,999 a day rather than requiring an outright purchase. It's a notable shift in how this hardware reaches smaller operators — renting a humanoid by the day rather than buying one outright is the same logic as hiring in a excavator for a job rather than owning your own, and it's a sign the economics are being built for exactly that kind of customer.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/07/02/agibot-debuts-a3-humanoid-robot-in-europe-and-launches-uk-robot-as-a-service-model/103018/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Doubles Maximum Penalty for Social Media Age-Law Breaches to $99 Million",
    "{{AUS_1_SUMMARY}}": "The Government has doubled the maximum penalty for social media platforms that fail to keep under-16s off their services, from $49.5 million to $99 million, after studies found more than 85% of Australian teens under 16 are still finding ways onto Facebook, Instagram, Snapchat, TikTok and YouTube. The eSafety Commissioner can now compel platforms to prove what they've actually done to enforce the ban, rather than just claiming compliance.",
    "{{AUS_1_URL}}": "https://www.pm.gov.au/media/stronger-powers-and-double-penalties-world-leading-social-media-law",

    "{{AUS_2_HEADLINE}}": "Australia and Vanuatu Sign Nakamal Agreement, Blocking Foreign Military Bases in the Pacific Nation",
    "{{AUS_2_SUMMARY}}": "Prime Minister Albanese and Vanuatu's Prime Minister Jotham Napat signed the Nakamal Agreement in Canberra last week, with Vanuatu committing to allow no foreign military base on its territory in exchange for deeper Australian policing, training and maritime security support — a deal read widely as locking China out of a potential Pacific foothold.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Moira Deeming Wins Court Reprieve, Delaying Victorian Liberal Party's Bid to Disendorse Her",
    "{{VIC_1_SUMMARY}}": "Victorian Liberal MP Moira Deeming secured a Supreme Court undertaking on Friday preventing the party from moving to disendorse her while her legal challenge against state president Brian Loughnane proceeds, with the matter now set down for a full day's hearing on 17 July. The dispute traces back to Deeming's allegation that a colleague put her in a headlock at a community event, a claim police investigated and found no case to answer on.",

    # Science
    "{{SCI_1_FLAG}}": "🧬 MEDICAL RESEARCH · TUBERCULOSIS · NASAL VACCINE BREAKTHROUGH",
    "{{SCI_1_HEADLINE}}": "New Nasal-Spray Vaccine Targets the Drug-Resistant Tuberculosis Bacteria That Hide From Antibiotics",
    "{{SCI_1_SUMMARY}}": "Johns Hopkins researchers have developed an intranasal DNA vaccine that targets dormant 'persister' TB bacteria able to survive prolonged antibiotic treatment and cause relapse — in animal studies it cleared infections faster, cut lung inflammation and boosted existing drug performance against resistant strains, with immune responses still detectable six months later in primate trials. A genuinely new angle of attack on a disease that still kills more people worldwide each year than any other infection.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Electricity Bill Is About to Fall — Don't Let AI Sit This One Out",
    "{{INSIGHT_BODY}}": "New Default Market Offer pricing landed this month, cutting small business electricity rates by anywhere from 7% to over 20% depending on your distribution zone — but only for businesses actually sitting on the default offer, not a locked-in market contract from a year or two back. For a business running compressors, generators and site equipment, power is a real line item, and most operators have never actually compared what they're paying against what's now on the table. This week's genuinely useful ten minutes: paste your last electricity bill's plan details into an AI assistant and ask it to compare your current rate against the new default offer for your postcode and usage profile — if there's a gap, that's a phone call to your retailer worth making before the next quarter's invoice lands.",

    # Fun Facts
    "{{FACT_1}}": "Thomas Jefferson and John Adams — two of the men who negotiated the Declaration of Independence — both died on 4 July 1826, within five hours of each other, exactly fifty years to the day after it was adopted. A third founding father and president, James Monroe, also died on a 4 July, five years later in 1831.",

    "{{FACT_2}}": "Henry Ford's Model T was only ever sold in black from 1914 to 1925 — not for style, but because black japan enamel was the only paint formula that dried fast enough to keep pace with his moving assembly line; every other colour available at the time took days longer to cure.",

    "{{FACT_3}}": "Vegemite was invented in 1922 by Melbourne food technologist Cyril Callister, who was tasked with finding a use for the leftover brewer's yeast being discarded by Melbourne's breweries — turning a waste byproduct into a jar that's sat in Australian pantries for over a century.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the removalist quote every job with an extra hour built in?",
    "{{JOKE_PUNCHLINE}}": "Because the one thing heavier than a queen-size bed is the couch that 'definitely fit through the door on the way in.'",

    # Closing
    "{{CLOSING_QUOTE}}": "“Do the best you can until you know better. Then when you know better, do better.”",
    "{{CLOSING_ATTR}}": "— Maya Angelou",
    "{{CLOSING_MESSAGE}}": "It's a quiet, cloudy Sunday before a proper frosty start on Monday morning — worth allowing extra warm-up time for gear and vehicles before the first job. With the new electricity default offer now in effect and last week's Payday Super changes still bedding in, it's a good week to run the numbers rather than assume nothing's changed since June. Take the rest of today though — Monday will still be there in the morning.",
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
