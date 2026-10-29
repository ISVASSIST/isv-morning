#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 30 October 2026',
'{{WEATHER_1}}': 'FRI 30 OCT · ☀️ Mostly sunny, dry · up to 25°C',
'{{WEATHER_2}}': 'SAT 31 OCT · ⛈️ Showers and a likely storm · 16–25°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SUN 1 NOV · 🌦️ Showers, little rain · 11–21°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'MON 2 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_5}}': 'TUE 3 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Today is the dry one, so get any exterior blasting and coating done now. Saturday looks wet with a likely thunderstorm (BoM Melbourne Airport forecast, 2-10 mm possible), and Sunday is showery. These figures are for greater Melbourne, not a Carrum Downs-specific page, and I couldn't find a reliable Monday or Tuesday forecast, so check BoM before planning next week.",
'{{WORLD_1_FLAG}}': '🌍 SPAIN',
'{{WORLD_1_HEADLINE}}': "Spain Mourns After High-Speed Train Crash Kills at Least 68",
'{{WORLD_1_SUMMARY}}': "One high-speed train hit another that had stopped on the tracks on Wednesday, and Spain has begun three days of national mourning. Rescuers were still searching overnight, so the toll may rise. This comes from a news roundup rather than the original wire report.",
'{{WORLD_1_URL}}': 'https://www.democracynow.org/2026/10/29/headlines',
'{{WORLD_2_FLAG}}': '🌍 HORMUZ',
'{{WORLD_2_HEADLINE}}': "Iran Says Three Oil Tankers Caught Fire After Hitting Mines in the Strait of Hormuz",
'{{WORLD_2_SUMMARY}}': "Iranian officials say the tankers struck sea mines while trying to cross the strait, which is still carrying far less traffic than before the war. That is an Iranian claim carried in news roundups and I haven't seen independent confirmation.",
'{{WORLD_2_URL}}': 'https://www.euronews.com/video/2026/10/29/latest-news-bulletin-october-29th-2026-midday',
'{{ECON_1_FLAG}}': '🛢️ OIL · BRENT',
'{{ECON_1_HEADLINE}}': 'Brent Slips to About US$114 on Reports of US Outreach to Iran',
'{{ECON_1_SUMMARY}}': "Brent fell about 1.1% to US$114.05 by mid-morning GMT on Thursday on reports of renewed US-Iran contact, still just under the six-month high of US$117.18 set on 23 October. Hormuz incidents are keeping a risk premium in the price, so don't expect diesel relief just yet.",
'{{ECON_1_URL}}': 'https://uk.advfn.com/market-news/article/25337/brent-falls-to-114-05-as-iran-peace-initiatives-and-supply-developments-influence-oil-trading',
'{{ECON_2_FLAG}}': '🇦🇺 RBA',
'{{ECON_2_HEADLINE}}': 'Banks Hold Their Call for an RBA Rate Rise on 3 November',
'{{ECON_2_SUMMARY}}': "Westpac reaffirmed its November hike call after Wednesday's 4.3% inflation figure, and CommBank has also forecast a rise, with markets pricing roughly a 90% chance. Underlying (trimmed mean) inflation is 3.6%, so fuel is a big part of the gap. Worth knowing before you commit to any new equipment finance.",
'{{TECH_1_FLAG}}': '🤖 AI · GOOGLE',
'{{TECH_1_HEADLINE}}': "Google Unveils Gemini 4 Carbon, Limited to Select Cybersecurity Experts for Now",
'{{TECH_1_SUMMARY}}': "Google says its new flagship ranks first on the Artificial Analysis Intelligence Index and is priced at US$2 per million input tokens. It is not publicly available yet, so nothing to use today, but it signals where the tools you'll be using are heading. Based on an aggregator, not Google's own announcement.",
'{{TECH_1_URL}}': 'https://aiweekly.co/ai-news-today',
'{{TECH_2_FLAG}}': '🤖 AI · CHATGPT',
'{{TECH_2_HEADLINE}}': "ChatGPT Can Now Take Tasks by iMessage and RCS Text",
'{{TECH_2_SUMMARY}}': "OpenAI says you can assign tasks to ChatGPT by text message without opening the app, which could suit quick job-site requests like drafting a customer reply. Reported by an aggregator, and I haven't confirmed whether it is available in Australia.",
'{{ROBOT_1_FLAG}}': '🤖 ROBOT PRODUCTIVITY',
'{{ROBOT_1_HEADLINE}}': "AGIBOT Proposes 'Worken' to Measure How Much Useful Work Robots Actually Do",
'{{ROBOT_1_SUMMARY}}': "At its Innovation Day in Shanghai, AGIBOT introduced Worken as a way to measure robot productivity in real settings, alongside its AHA3 platform and G2 Max robot. A yardstick for real work matters, because buyers have mostly had demos and promises. The Robot Report, 29 October.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/agibot-introduces-worken-measure-robot-productivity-innovation-day-2026/',
'{{AUS_1_HEADLINE}}': "PM Says Police Were Called to the Lodge Over a Security Concern",
'{{AUS_1_SUMMARY}}': "Albanese revealed a security concern at his Canberra home on Wednesday night while repeating his call to 'turn down the heat' in politics. Details were limited in the ABC live blog I could see, so treat the full circumstances as unknown.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-29/federal-politics-live-blog-oct-29/107320104',
'{{AUS_2_HEADLINE}}': "Conroy Criticises Husic's Idea of Capping Prices on Milk and Eggs",
'{{AUS_2_SUMMARY}}': "Defence Industry Minister Pat Conroy pushed back on Labor colleague Ed Husic's suggestion to cap basic grocery prices, while Albanese said economic challenges won't be solved overnight. From the ABC's 29 October federal politics blog.",
'{{VIC_1_HEADLINE}}': "Police Identify Usernames Allegedly Directing Melbourne Arson Attacks",
'{{VIC_1_SUMMARY}}': "The ABC listed the story in its 29 October coverage, but I could only see the headline, so I can't give you details beyond that. Check the ABC Melbourne page for the full report.",
'{{SCI_1_FLAG}}': '🌋 EARTH SCIENCE',
'{{SCI_1_HEADLINE}}': "Scientists Find a Hidden Oxygen Reservoir Deep Inside Earth",
'{{SCI_1_SUMMARY}}': "A Science China Press study suggests magma deep in the Earth can hold extra oxygen, and that ancient volcanic eruptions may have helped turn the atmosphere oxygen-rich billions of years ago. ScienceDaily, listed 28 October.",
'{{INSIGHT_TITLE}}': "Ask AI to Turn Your Fuel Receipts Into a Cost-Per-Job Report",
'{{INSIGHT_BODY}}': "With diesel still a major cost, most small trades only see fuel as one lump on the credit card. Photograph or export a month of fuel receipts, add your job list and rough distances, and ask an AI tool to estimate fuel cost per job and flag the runs that eat your margin. Check its arithmetic against a couple of jobs you know, and keep customer names out of it. If a regular far-flung job is losing money, that's a price conversation, not a guess.",
'{{FACT_1}}': "Brent crude's six-month high is US$117.18, set on 23 October.",
'{{FACT_2}}': "North American robot orders rose 24.8% in the third quarter of 2026, according to the A3 industry group.",
'{{FACT_3}}': "Underlying (trimmed mean) inflation is 3.6%, well below headline inflation of 4.3%, because fuel is excluded from the underlying measure.",
'{{JOKE_SETUP}}': "Why did the tow-truck operator never lose a regular customer?",
'{{JOKE_PUNCHLINE}}': '"He was always there when they were down, and he never made them feel like a drag."',
'{{CLOSING_QUOTE}}': '"The only place success comes before work is in the dictionary."',
'{{CLOSING_ATTR}}': '— Vidal Sassoon',
'{{CLOSING_MESSAGE}}': "Friday is dry and up to 25°C, with a likely storm on Saturday, so push any outdoor work forward today and get tools and gear under cover before the weekend. The RBA meets on Tuesday, so it's a good day to look over your loan repayments.",
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
