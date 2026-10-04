#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Monday, 5 October 2026',
'{{WEATHER_1}}': 'MON 5 OCT · ⛅ Partly cloudy, light winds · 9–15°C',
'{{WEATHER_2}}': 'TUE 6 OCT · 🌦️ Showers likely, NW winds shifting S/SW 20–30 km/h · 9–19°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'WED 7 OCT · ☀️ Mostly sunny · 7–20°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'THU 8 OCT · ☀️ Sunny · 9–23°C',
'{{WEATHER_5}}': 'FRI 9 OCT · ⛅ Mostly sunny, medium chance of a late shower, gusty northerlies · 12–25°C',
'{{WEATHER_ALERT}}': "Today is dry, so get outdoor coating work done now. Showers and a southwesterly change arrive Tuesday, then Wednesday and Thursday look excellent for blasting and painting, with Thursday and Friday warming up. Forecast is the BOM Melbourne outlook, so Carrum Downs may differ slightly.",
'{{WORLD_1_FLAG}}': '🇧🇷 BRAZIL · LULA V BOLSONARO, RUNOFF LIKELY',
'{{WORLD_1_HEADLINE}}': 'Brazil Votes in Deeply Polarised Election Pitting Lula Against Bolsonaro',
'{{WORLD_1_SUMMARY}}': "Voters chose a president yesterday, with 80-year-old Lula seeking a fourth term against Senator Flavio Bolsonaro. Final polls had neither clearing 50%, so a runoff on 25 October is widely expected, and markets are watching closely.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/10/4/brazil-votes-in-deeply-polarised-election-pitting-lula-against-bolsonaro',
'{{WORLD_2_FLAG}}': '🇮🇷 IRAN · HORMUZ STILL SHUT PENDING SEVEN CONDITIONS',
'{{WORLD_2_HEADLINE}}': "Iran Talking Peace but Unwilling to Bend to Trump, US Nuclear Demands",
'{{WORLD_2_SUMMARY}}': "Iran says the Strait of Hormuz won't reopen until seven conditions are met in a deal being negotiated via Islamabad, with Qatar mediating. The strait is the main driver of the diesel prices your fleet and suppliers are paying.",
'{{WORLD_2_URL}}': 'https://www.foxnews.com/live-news/us-iran-war-hormuz-strait-peace-talks-donald-trump-october-4',
'{{ECON_1_FLAG}}': '⛽ FUEL · OIL EASES BUT STILL ABOVE US$100',
'{{ECON_1_HEADLINE}}': 'ACCC Weekly Fuel Update: Capital City Fuel Prices Slightly Lower as Brent Slips to About US$102',
'{{ECON_1_SUMMARY}}': "Retail petrol and diesel prices eased a little in capital cities last week while regional prices stayed flat, as refined fuel benchmarks remain high. Brent closed Friday near US$102, so don't expect real relief yet; keep a fuel line in your quotes.",
'{{ECON_1_URL}}': 'https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update',
'{{ECON_2_FLAG}}': '🏦 SMALL BUSINESS · BANKS PASS ON RATE HIKE THIS WEEK',
'{{ECON_2_HEADLINE}}': "CBA Lifts Variable Business Loan Rates by 0.25% From Friday 9 October After RBA Lifts Cash Rate to 4.6%",
'{{ECON_2_SUMMARY}}': "It's the fourth RBA hike this year and the highest cash rate since 2011. Macquarie follows on 15 October. If you have an overdraft, equipment finance or a variable business loan, check your repayments and talk to your bank before the change lands.",
'{{TECH_1_FLAG}}': '🛰️ AI · GOOGLE PUTS TPUS IN ORBIT',
'{{TECH_1_HEADLINE}}': 'Google Launches Project Suncatcher Prototype Satellite With Four TPUs',
'{{TECH_1_SUMMARY}}': 'Launched 1 October on a SpaceX rideshare, the refrigerator-sized prototype is the first step towards solar-powered AI data centres in space. Two more prototypes follow by early 2027. Not a tool for the workshop, but a sign of how hard the industry is chasing cheap AI compute.',
'{{TECH_1_URL}}': 'https://www.opb.org/article/2026/10/01/google-launches-project-suncatcher-a-step-towards-ai-data-centers-in-space/',
'{{TECH_2_FLAG}}': '💬 AI · DOORDASH LAUNCHES TEXT-TO-ORDER AGENT',
'{{TECH_2_HEADLINE}}': "DoorDash Releases an AI Agent That Takes Orders by Text Message",
'{{TECH_2_SUMMARY}}': "Customers can now text the agent to place an order in a chat thread instead of the app. The same pattern, an AI handling a simple request over SMS, is exactly how trades could take quote requests and booking enquiries after hours.",
'{{ROBOT_1_FLAG}}': '🤖 USA · ASTRIBOT BRINGS T1 HUMANOID TO NORTH AMERICA',
'{{ROBOT_1_HEADLINE}}': 'Astribot Brings Its T1 Humanoid Robot to North America at IROS 2026',
'{{ROBOT_1_SUMMARY}}': "Shown at IROS in Pittsburgh, the T1 starts at US$18,000, a fraction of what humanoids cost a year ago. IDC says global humanoid shipments hit about 25,000 in the first half of 2026, up 432% year on year. Published 2 October.",
'{{ROBOT_1_URL}}': 'https://roboticsandautomationnews.com/2026/10/02/astribot-brings-its-t1-humanoid-robot-to-north-america/105448/',
'{{AUS_1_HEADLINE}}': "Pacific Leaders Challenge Australia's Fossil Fuel Expansion Ahead of Pre-COP31 Talks in Fiji",
'{{AUS_1_SUMMARY}}': "Pre-COP31 talks open in Fiji today, with Prime Minister Anthony Albanese attending, just days after approval of the Hunter Valley Operations coal mine extension to 2045. Pacific voices call continued expansion 'a slap in the face'.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-05/pre-cop31-australia-challenged-over-fossil-fuel-expansion/107220650',
'{{AUS_2_HEADLINE}}': 'Newcastle Knights Fall Short in NRL Grand Final but Fans Keep the Faith',
'{{AUS_2_SUMMARY}}': "Newcastle's premiership tilt ended in defeat on the weekend, though the club's fans are finding pride in the run. It follows the Saturday car incident at the Knights farewell in Wallsend that injured ten people.",
'{{VIC_1_HEADLINE}}': "Victoria's Premier Faces Two Oppositions Heading Into the State Election",
'{{VIC_1_SUMMARY}}': "With the 28 November election eight weeks away, Premier Ben Carroll is fighting Jess Wilson's Coalition, One Nation (polling around one in four voters) and his own Labor record. Expect heavy talk on construction corruption, cost of living and law and order.",
'{{SCI_1_FLAG}}': '🌙 SPACE · THE MOON HIDES A MAGNETIC TIME CAPSULE',
'{{SCI_1_HEADLINE}}': "Chang'e-6 Lunar Soil Contains a Surprising Magnetic Time Capsule",
'{{SCI_1_SUMMARY}}': "Scientists found gamma iron, a form of metallic iron normally stable only at high temperature, preserved in tiny impact-glass grains from the Moon's far side. It can lock in magnetic signals, helping reveal the Moon's lost magnetic field. ScienceDaily, 1 October 2026.",
'{{INSIGHT_TITLE}}': 'Photos In, Paperwork Out: Let AI Turn Your Job Photos Into Quotes and Handover Notes',
'{{INSIGHT_BODY}}': "You already take photos of every job before, during and after. Upload a handful to an AI assistant with a short prompt such as 'list the surfaces, approximate areas, defects and prep steps visible, then draft a scope of work in plain English'. You get a first-draft quote scope and a handover note for the customer in minutes, rather than an hour at the kitchen table that night. Always check measurements and prices yourself, but with rates rising and margins squeezed, claiming back that admin time is one of the cheapest wins in your business.",
'{{FACT_1}}': "Gamma iron, found in Chang'e-6 Moon soil, is a form of iron normally stable only above roughly 900°C, yet it survived on the lunar surface because impacts froze it in place inside glass.",
'{{FACT_2}}': "Astribot's T1 humanoid starts at US$18,000, which is cheaper than many new utes sold in Australia.",
'{{FACT_3}}': "Brazil's president is elected by two-round voting: if nobody wins more than 50% of valid votes, the top two candidates face a runoff three weeks later, which this year falls on 25 October.",
'{{JOKE_SETUP}}': 'A fencing contractor was asked how his small business never ran out of work, even in a slow year.',
'{{JOKE_PUNCHLINE}}': 'He said, "Simple — I build fences that make good neighbours, and they always talk about the job over the top."',
'{{CLOSING_QUOTE}}': '"It does not matter how slowly you go as long as you do not stop."',
'{{CLOSING_ATTR}}': '— Confucius',
'{{CLOSING_MESSAGE}}': "It's Monday 5 October and the week starts dry, so use today to get outdoor jobs moving before Tuesday's showers. With a rate rise hitting business loans on Friday, now is a good day to look over your numbers.",
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
