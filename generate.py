#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 21 October 2026',
'{{WEATHER_1}}': 'WED 21 OCT · 🌤️ Partly cloudy, slight chance of an afternoon shower · up to ~25–28°C',
'{{WEATHER_2}}': 'THU 22 OCT · ☀️ Sunny and hot for spring · ~29–30°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'FRI 23 OCT · ☀️ Mostly sunny, gusty northerlies 25–40 km/h · ~29°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SAT 24 OCT · 🌧️ Cold front, showers increasing · ~24°C',
'{{WEATHER_5}}': 'SUN 25 OCT · outlook not confirmed, expect cooler after the front',
'{{WEATHER_ALERT}}': "First 30-degree days since March are forecast for Thursday and Friday, with strong northerly winds Friday, so watch heat on site and wind on any outdoor coating work. A cold front brings showers and a sharp drop on Saturday. Sources disagreed on Wednesday and Friday showers, so check BoM before committing to outdoor jobs.",
'{{WORLD_1_FLAG}}': '🌍 IRAN WAR',
'{{WORLD_1_HEADLINE}}': "Iranian Officials Tell Reuters Tehran Is Stalling Talks and Preparing for Renewed Strikes, Not a Deal",
'{{WORLD_1_SUMMARY}}': "Just Security's 20 October roundup says the officials claim they have dragged out talks to weaken President Trump before the US midterms. Pakistan's army chief is set to travel to Iran, with Pakistan a key mediator this year. No deal means Hormuz stays tight, and fuel and freight costs stay high.",
'{{WORLD_1_URL}}': 'https://www.justsecurity.org/161419/early-edition-october-20-2026/',
'{{WORLD_2_FLAG}}': '🛡️ MIDDLE EAST · YEMEN',
'{{WORLD_2_HEADLINE}}': 'Hegseth Meets Netanyahu on the Iran War as Britain Expands RAF Patrols to Back Saudi Arabia Against the Houthis',
'{{WORLD_2_SUMMARY}}': "The same 20 October roundup says the Shabwa governor now puts the death toll from the Houthi attack on a government training camp at 58, with more than 200 injured. The region is escalating rather than calming.",
'{{WORLD_2_URL}}': 'https://www.justsecurity.org/161419/early-edition-october-20-2026/',
'{{ECON_1_FLAG}}': '⛽ FUEL · OIL',
'{{ECON_1_HEADLINE}}': 'Brent Crude Falls About 2.5% to Around US$107 as the G7 Reserve Release Weighs, but Hormuz Remains Disrupted',
'{{ECON_1_SUMMARY}}': "A Kalkine report cites Brent at US$107.13 after Monday's fall, still far above the start of the year. The latest ACCC pump data I found (14-16 October) had five-city diesel around $2.78-2.82 a litre, so any relief will take a while to reach the bowser. Verify current prices before quoting jobs.",
'{{ECON_1_URL}}': 'https://kalkine.com.au/news/economic-news/brent-crude-price-2026-up-76-why-the-hormuz-crisis-still-outweighs-a-russia-sanctions-waiver',
'{{ECON_2_FLAG}}': '🏦 RATES · AUD',
'{{ECON_2_HEADLINE}}': 'Aussie Dollar Pushes Toward US$0.70 After Hawkish RBA Remarks and Strong China GDP',
'{{ECON_2_SUMMARY}}': "FXStreet says the dollar rose about 0.5% on 19 October after RBA Assistant Governor Christopher Kent's hawkish comments, while China's Q3 GDP grew 4.5%. With the cash rate at 4.60% and the next RBA decision on 3 November, expect loan costs to stay high. A firmer dollar helps imported gear, but not repayments.",
'{{TECH_1_FLAG}}': '🚚 AI · FLEETS',
'{{TECH_1_HEADLINE}}': 'Motive Brings Agentic AI to Physical Operations, With Agents That Act Before Problems Escalate',
'{{TECH_1_SUMMARY}}': "SiliconANGLE reports on 19 October that Motive's agents aim to flag and act on issues in fleet and field operations early. Aimed at larger fleets, but it shows where vehicle and job-site AI is heading. I only saw the headline summary, so details are unconfirmed.",
'{{TECH_1_URL}}': 'https://siliconangle.com/2026/10/19/motive-brings-agentic-ai-to-physical-operations-with-agents-that-act-before-problems-escalate',
'{{TECH_2_FLAG}}': '🧰 AI · SMALL BUSINESS',
'{{TECH_2_HEADLINE}}': "Weekly Small-Business AI Roundup Lists Gemini 4 Argon and ChatGPT Pro Splitting Tasks Between Agents",
'{{TECH_2_SUMMARY}}': "A blog roundup dated 18 October, so near the edge of the 48-hour window, with no primary company sources. Treat the product names as unconfirmed, but the trend is AI tools that handle several admin tasks at once.",
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · TESLA',
'{{ROBOT_1_HEADLINE}}': "Tesla's Shareholder Report Says Optimus V3 Is Ready for Mass Production, Lifting China's Robotics Stocks",
'{{ROBOT_1_SUMMARY}}': "BigGo Finance reports the report filed 19 October says first production lines are under construction, and Chinese humanoid stocks rallied on 20 October. Claims about readiness come from the company and a finance site, so treat the timeline with caution.",
'{{ROBOT_1_URL}}': 'https://finance.biggo.com/news/10127d79-8a19-4a31-a82b-80fd13c826b8',
'{{AUS_1_HEADLINE}}': "Albanese Says There Is No Place for Political Violence After Attack on MP Helen Haines",
'{{AUS_1_SUMMARY}}': "The PM held a briefing in Melbourne with the Victorian premier and the AFP commissioner. Haines, 65, was airlifted to hospital after being struck by a vehicle outside her Wangaratta electorate office.",
'{{AUS_1_URL}}': 'https://abc.net.au/news/2026-10-19/live-blog-victoria-indi-mp-helen-haines-injured-wangaratta/107285046',
'{{AUS_2_HEADLINE}}': 'Victorian Man Brendan Nugent Charged Over the Attack on Helen Haines',
'{{AUS_2_SUMMARY}}': "ABC's 20 October live blog headline reports the charge. I could only see the headline, so check ABC for the specific charges and court dates.",
'{{VIC_1_HEADLINE}}': "Victorian Election Campaigning Paused Out of Respect for Haines; VEC to Work With Police on Election Safety",
'{{VIC_1_SUMMARY}}': "Campaigning paused on Tuesday ahead of the 28 November state election. The Victorian Electoral Commission says it will work with safety and law enforcement agencies to keep the poll secure.",
'{{SCI_1_FLAG}}': '🧠 NEUROSCIENCE',
'{{SCI_1_HEADLINE}}': "Overactive Brain Immune Cells Drive Sleep Loss in Alzheimer's, and Removing Them Restored Over Two Hours of Sleep in Mice",
'{{SCI_1_SUMMARY}}': "ScienceDaily's release is dated 18 October (US), so right on the edge of the 48-hour window, and I found nothing newer that was clearly dated. It is a mouse study, so it is early-stage, but sleep is clearly tied to brain health.",
'{{INSIGHT_TITLE}}': 'Let AI Draft Your Hot-Weather Safety Checklists: You Review, Then Sign',
'{{INSIGHT_BODY}}': "With 30-degree days forecast, heat, hydration and wind are worth a written plan on every job. Give an AI tool the site details, task and crew size and ask for a short checklist covering breaks, water, shade, PPE and wind limits. Then check it against your own SWMS and WorkSafe Victoria guidance and fix anything that doesn't fit your site. It saves paperwork time, but the signature and responsibility stay yours.",
'{{FACT_1}}': "Unitree's shares jumped about 16% on 19 October after new Chinese government guidance called for more robots in household services and commercial logistics.",
'{{FACT_2}}': "Kpler put Strait of Hormuz oil transits at 11.62 million barrels a day in the week to 13 October, against a pre-war baseline of 17.15 million.",
'{{FACT_3}}': "Australia currently holds about 43 days of petrol and 31 days of diesel in reserve, according to recent reports.",
'{{JOKE_SETUP}}': "Why did the electrician's apprentice never get lost on site?",
'{{JOKE_PUNCHLINE}}': '"Because he always followed the current."',
'{{CLOSING_QUOTE}}': '"A journey of a thousand miles begins with a single step."',
'{{CLOSING_ATTR}}': '— Lao Tzu',
'{{CLOSING_MESSAGE}}': "It's a warm, partly cloudy Wednesday with 30 degrees coming Thursday and Friday, so plan water, shade and early starts. A cold front arrives Saturday, so get any outdoor coating work done before then.",
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
