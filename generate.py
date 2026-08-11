#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 12 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 12 Aug (BOM)
    "{{WEATHER_1}}": "WED 12 · 🌧️ Very high chance of showers, most likely morning · 7–13°C",
    "{{WEATHER_2}}": "THU 13 · 🌦️ High chance of showers, easing during the day · 7–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 14 · ⛅ Medium chance of showers, most likely early morning · 8–15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 15 · 🌤️ Slight chance of a shower · 8–15°C",
    "{{WEATHER_5}}": "SUN 16 · ☀️ Mostly sunny · 9–16°C",
    "{{WEATHER_ALERT}}": "A flood warning remains current for the Yarra Valley and a Flood Watch continues for parts of North East, Gippsland and Central Victoria after last week's rain band — nothing current for Carrum Downs itself, but expect a wet, cloudy Wednesday before it clears toward the weekend",

    # World
    "{{WORLD_1_FLAG}}": "🇦🇫 AFGHANISTAN · UN SAYS 2.4 MILLION GIRLS STILL SHUT OUT OF SECONDARY SCHOOL",
    "{{WORLD_1_HEADLINE}}": "UN Says 2.4 Million Afghan Girls Remain Shut Out of Secondary School Five Years After Taliban Takeover",
    "{{WORLD_1_SUMMARY}}": "UNESCO reported this week that around 2.4 million Afghan girls remain excluded from secondary education five years after the Taliban's return to power, calling the continued exclusion of women and girls from schooling a grave violation of their fundamental rights. Afghanistan remains the only country in the world where girls and women are formally banned from secondary and higher education, reversing two decades of progress that had seen almost a million girls enrolled in secondary school by 2021.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/8/11/unesco-says-2-4-million-afghan-girls-denied-access-to-further-education",

    "{{WORLD_2_FLAG}}": "🇺🇦 UKRAINE · UN SAYS OVER 16,000 CIVILIANS DETAINED BY RUSSIA ARE STILL HELD",
    "{{WORLD_2_HEADLINE}}": "UN Estimates More Than 16,000 Civilians Detained by Russia During the War Are Still Being Held",
    "{{WORLD_2_SUMMARY}}": "The United Nations told the Security Council this week that more than 16,000 civilians detained by Russia during its war in Ukraine remain deprived of their liberty, many held incommunicado on grounds that don't comply with international law. UN investigators say widespread and systematic torture and ill-treatment of both civilian detainees and prisoners of war is continuing, with more than 95% of surveyed Ukrainian POWs and 85% of civilian detainees reporting torture or ill-treatment, often repeatedly.",
    "{{WORLD_2_URL}}": "https://www.washingtonpost.com/world/2026/08/11/ukraine-russia-war-united-nations-detainees-prisoners/f3196424-95a0-11f1-9ef9-1be722184483_story.html",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺📊 BUSINESS · NAB SURVEY FINDS CONDITIONS EDGE UP BUT CONFIDENCE STAYS FRAGILE",
    "{{ECON_1_HEADLINE}}": "NAB Survey Finds Business Conditions Edging Up But Confidence Still Fragile on Cost Pressures",
    "{{ECON_1_SUMMARY}}": "NAB's latest business survey shows conditions ticked higher in July but remain below the long-run average, while confidence stayed weak as firms flagged rising input costs, tied partly to higher oil prices flowing from Middle East tensions. For a small trades operator, it's a familiar split — the phone's still ringing and jobs are getting done, but the cost side of every quote keeps needing a second look before it goes out the door.",
    "{{ECON_1_URL}}": "https://investinglive.com/news/australian-business-conditions-edge-higher-in-july-but-confidence-stays-fragile/",

    "{{ECON_2_FLAG}}": "⛽🇦🇺 FUEL · MELBOURNE PETROL PUSHES PAST 205C/L AS THE EXCISE RISE KEEPS FLOWING THROUGH",
    "{{ECON_2_HEADLINE}}": "Melbourne Petrol Pushes Past 205c/L as the Fuel Excise Increase Keeps Flowing Through at the Bowser",
    "{{ECON_2_SUMMARY}}": "Melbourne's average unleaded price has climbed to around 204.9c/L, with prices up close to 30 cents on last month as the fuel excise, restored to 53.7 cents a litre from 3 August, continues to work its way through the pump price — Victoria still holds the country's cheapest average, with Frankston among the cheaper pockets locally, but the ACCC expects further upward pressure over coming weeks. Worth another pass over fuel surcharges on standing quotes before they quietly eat into the margin.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖💾 AI INFRASTRUCTURE · ANTHROPIC TEAMS WITH MACQUARIE AND GIC ON A NEW DATA-CENTRE VENTURE",
    "{{TECH_1_HEADLINE}}": "Anthropic Partners With Macquarie and GIC on a New Data-Centre Venture Called Theseus",
    "{{TECH_1_SUMMARY}}": "Anthropic has announced a strategic partnership with Macquarie Asset Management and Singapore's GIC to build and lease dedicated data-centre infrastructure at scale, with Macquarie and GIC funding the bulk of construction and Anthropic committing to long-term lease agreements. It's part of a broader race among AI labs to lock in compute capacity — for small businesses relying on AI tools day to day, more purpose-built capacity coming online is generally what keeps subscription prices and service reliability from swinging around as demand grows.",
    "{{TECH_1_URL}}": "https://therealdeal.com/national/2026/08/11/anthropic-recruits-macquarie-gic-for-data-center-venture/",

    "{{TECH_2_FLAG}}": "🤖🛡️ AI AGENTS · NEW PLATFORM LAUNCHES A 'SECURITY SCORE' TO VET AI AGENTS BEFORE THEY GO LIVE",
    "{{TECH_2_HEADLINE}}": "A New AI Agent Platform Launches With a Pre-Deployment Security Score to Vet Agents Before They Go Live",
    "{{TECH_2_SUMMARY}}": "SUPERAGENT AI this week launched SUPERAGENT 3.0, built around a lightweight pre-deployment security score that lets a business check how much access and risk an AI agent carries before switching it on, as incidents of autonomous agents overstepping their brief keep climbing. It's a sign the industry is starting to build in the guardrails small businesses have been missing — a quick way to check what an agent can actually touch before handing it the keys to bookings, invoicing or supplier orders.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇺🇸🤖 ROBOT SECURITY · NEW US FIRM 'SECURITY-HARDENS' CHINESE-MADE ROBOTS AFTER AN FCC IMPORT BAN",
    "{{ROBOT_1_HEADLINE}}": "A New US Company Launches to Security-Harden Chinese-Made Robots After the FCC Bans New Imports",
    "{{ROBOT_1_SUMMARY}}": "Days after the FCC added foreign-made humanoid and quadruped robots to its Covered List, blocking new models from Chinese manufacturers from being sold in the US, a new firm called Robo Inc launched on Monday offering to import the hardware, then strip, audit and re-secure its software and network connections on US soil before resale. It's a preview of a headache heading for any business eyeing cheap imported 'smart' gear generally — robots, cameras, sensors — where the real risk often isn't the hardware itself but what it's quietly phoning home to.",
    "{{ROBOT_1_URL}}": "https://www.techtimes.com/articles/323845/20260810/robo-inc-launches-us-humanoid-robot-integrator-china-spy-law-still-follows-hardware.htm",

    # Australia
    "{{AUS_1_HEADLINE}}": "Census Night Passes as Millions of Australians Complete the Compulsory 2026 Count",
    "{{AUS_1_SUMMARY}}": "Census night fell on Tuesday, with every person in Australia required to be counted, including international students, visitors and babies. This year's form runs to as many as 66 questions and for the first time asks people aged 16 and over about sexual orientation and gender, alongside the usual questions on ancestry, religion and how people got to work that day — data the ABS uses to plan everything from hospitals to roads.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/census-2026-guide-when-is-census-night-and-everything-you-need-to-know/7grekdcbf",

    "{{AUS_2_HEADLINE}}": "Flood Warning Issued for the Yarra Valley as Rivers Rise Across Victoria's North East",
    "{{AUS_2_SUMMARY}}": "The Bureau of Meteorology issued a flood warning for the Yarra Valley on Monday after heavy rain lifted river levels across North East, Gippsland and Central Victoria, with minor flooding possible along the Yarra upstream of Warrandyte and several other catchments including the Bunyip River and Dandenong Creek. Residents in low-lying areas near affected waterways are being told to monitor BOM warnings directly rather than assume the wet weather has moved on.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Pauline Hanson Unveils One Nation's Victorian Election Team, Bars Major Media Outlets From the Announcement",
    "{{VIC_1_SUMMARY}}": "Pauline Hanson was in Melbourne on Monday to name Warren Pickering as One Nation's Victorian state leader and unveil the party's upper house candidates ahead of November's state election, calling Victoria a 'basket case' and saying the party has fielded more than 1,000 candidate applications. The Age, the ABC and The Guardian were barred from the press conference, with Pickering threatening legal action over what he called 'character assassination' — a sign the minor party is positioning for a real shot at Legislative Council balance of power.",

    # Science
    "{{SCI_1_FLAG}}": "🐕 SCIENCE · BRAIN SCANS SHOW DOGS CAN TELL FEAR FROM SADNESS IN HUMAN FACES",
    "{{SCI_1_HEADLINE}}": "Brain Scans Show Dogs Can Tell Fear From Sadness in Human Faces",
    "{{SCI_1_SUMMARY}}": "University of Vienna researchers used fMRI on twelve awake, trained family dogs to see how their brains respond to human facial expressions of happiness, anger, fear and sadness, published this week in Cell Press journal iScience. Happy faces activated reward-linked regions in the dogs' brains, and — for the first time — the scans showed distinct patterns separating fear from anger and sadness, suggesting dogs read more nuance in a worried or upset face than they've been given credit for.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The US Just Banned Foreign 'Spy' Robots — Is Your Site's Smart Gear on the Same Network as Your Invoicing?",
    "{{INSIGHT_BODY}}": "Today's robotics story is about humanoid robots, but the underlying risk applies to any imported 'smart' device on a job site or in a workshop — security cameras, sensors, even the odd cheap smart plug — where nobody's checked what data it's quietly sending home. The fix a specialist security firm now charges good money for isn't complicated to start yourself: put anything internet-connected that isn't core business hardware on its own guest network or VLAN, separate from the computer or tablet running your invoicing, quoting and banking. If a cheap imported device is ever compromised, a segmented network means the worst it can do is sit on its own island — not walk straight into your accounts.",

    # Fun facts
    "{{FACT_1}}": "Australia's ute traces back to a 1932 letter from a Gippsland farmer's wife, asking Ford Australia for a vehicle 'to go to church in on Sunday and carry our pigs to market on Monday' — 22-year-old design draftsman Lewis Bandt sketched the coupe utility in response, and Ford built it the same year.",
    "{{FACT_2}}": "Kevlar, now woven into everything from work gloves to cut-resistant sleeves, was invented by accident in 1965 when DuPont chemist Stephanie Kwolek was looking for a lightweight material for car tyres and instead produced a stiff, cloudy liquid crystal solution nobody expected to be useful — until it spun into a fibre five times stronger than steel by weight.",
    "{{FACT_3}}": "Tonight, weather permitting, three rare sky events overlap within about 24 hours worldwide — a total solar eclipse crossing Greenland, Iceland and northern Spain (mainland Europe's first since 1999), a six-planet alignment, and the peak of the annual Perseid meteor shower.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the vending machine business owner never worry about late-paying customers?",
    "{{JOKE_PUNCHLINE}}": "Because every single one of them paid upfront, in coins, before they got a thing.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Do not let what you cannot do interfere with what you can do.\"",
    "{{CLOSING_ATTR}}": "— John Wooden",
    "{{CLOSING_MESSAGE}}": "It's a wet, cloudy Wednesday in Carrum Downs, with the wettest of it clearing through the morning before things ease over the rest of the week — worth checking the Yarra Valley flood warning if you've got a job or a drive planned that way today. If the cloud breaks tonight, mainland Europe's first total solar eclipse since 1999 sweeps through on the other side of the world alongside the Perseids peaking, a reminder the sky's doing plenty even on a grey Melbourne morning.",
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
