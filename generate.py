#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Sunday, 11 October 2026',
'{{WEATHER_1}}': 'SUN 11 OCT · 🌤️ Mostly sunny, slight chance of a late shower · 13–25°C',
'{{WEATHER_2}}': 'MON 12 OCT · ⛈️ Showers very likely, afternoon thunderstorm possible · 16–21°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'TUE 13 OCT · 🌧️ High chance of showers, morning and afternoon',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'WED 14 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'THU 15 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': 'Today is the pick of the week: mostly sunny and up to 25°C. Showers set in late tonight and Monday looks wettest, with possible rainfall of 4 to 20 mm and an afternoon thunderstorm, then more showers Tuesday. Based on Bureau of Meteorology Melbourne-area forecasts, so Carrum Downs may differ, and Wednesday and Thursday could not be confirmed.',
'{{WORLD_1_FLAG}}': '🌊 HORMUZ · TRAFFIC STILL NEAR ZERO',
'{{WORLD_1_HEADLINE}}': 'Strait of Hormuz Tracker Shows Commercial Traffic at About 5% of Pre-Crisis Levels',
'{{WORLD_1_SUMMARY}}': 'A live tracker updated 10 October puts transits at 4 vessels on 4 October against a normal 85 a day. Tanker attacks are reported at a wartime high, so freight and diesel risk stays baked into prices. Figures come from an aggregator, so treat them as indicative.',
'{{WORLD_1_URL}}': 'https://straits.live/',
'{{WORLD_2_FLAG}}': '🗣️ HORMUZ · COMPETING CLAIMS',
'{{WORLD_2_HEADLINE}}': 'Rubio Says Hormuz Is Open; IRGC Adviser Says It Stays Closed Until Iran\'s Demands Are Met',
'{{WORLD_2_SUMMARY}}': 'Washington says vessels are still transiting and Iran has "lost complete control", while Tehran insists its forces are in charge. Until the two stories match, expect fuel markets to stay jumpy.',
'{{WORLD_2_URL}}': 'https://www.nbcnews.com/data-graphics/strait-of-hormuz-ports-traffic-trump-us-iran-war-rcna331507',
'{{ECON_1_FLAG}}': '🏦 RATES · BANKS PASS ON RBA HIKE',
'{{ECON_1_HEADLINE}}': 'Banks Pass On the RBA\'s 25-Point Hike, With the Cash Rate Now 4.60%',
'{{ECON_1_SUMMARY}}': 'The RBA lifted the cash rate on 29 September, citing oil supply disruption as an inflation risk. NAB\'s higher variable rates took effect 9 October and Macquarie follows on 15 October. If you carry equipment finance or an overdraft, check your repayments. Next RBA meeting is 3 November.',
'{{ECON_1_URL}}': 'https://www.rba.gov.au/media-releases/2026/mr-26-27.html',
'{{ECON_2_FLAG}}': '💳 SURCHARGES · BAN DELAYED',
'{{ECON_2_HEADLINE}}': 'Labor Backs Down on Card Surcharge Ban Timing, but Businesses Are Still Angry',
'{{ECON_2_SUMMARY}}': 'ABC reports Treasurer Jim Chalmers announced two backdowns on Friday, with Labor temporarily covering costs so the ban can be delayed by six months. Many businesses say it still falls short, so keep your pricing flexible.',
'{{TECH_1_FLAG}}': '🧰 AI · GOOGLE CLOSES CODE ASSIST SALES',
'{{TECH_1_HEADLINE}}': 'Google Stops Selling New Gemini Code Assist Subscriptions',
'{{TECH_1_SUMMARY}}': 'Google Cloud\'s release notes say new subscriptions ended from 9 October, with existing ones auto-renewing through the rest of 2026. A reminder that AI products come and go quickly.',
'{{TECH_1_URL}}': 'https://docs.cloud.google.com/release-notes',
'{{TECH_2_FLAG}}': '🤝 AI · ATLASSIAN x OPENAI',
'{{TECH_2_HEADLINE}}': 'Atlassian and OpenAI Expand Partnership to Bring OpenAI Models Into Rovo Agents',
'{{TECH_2_SUMMARY}}': 'An enterprise AI roundup for the week of 9 October reports the expanded tie-up, putting OpenAI models inside Atlassian\'s workplace agents. Details come from a roundup, not a primary announcement.',
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · BYD HUMANOID DESIGN',
'{{ROBOT_1_HEADLINE}}': 'BYD Reveals Design of Its First Self-Developed Humanoid Robot',
'{{ROBOT_1_SUMMARY}}': 'CarNewsChina reports on 10 October that the design emerged from a patent published in China on 9 October, with service, education and industrial uses in mind. It is a patent design, not a shipping product, and I could not corroborate it elsewhere.',
'{{ROBOT_1_URL}}': 'https://carnewschina.com/2026/10/10/byd-unveils-design-for-its-first-self-developed-humanoid-robot',
'{{AUS_1_HEADLINE}}': 'Nick Blakey Picks North Melbourne, but Sydney Is Setting a High Price',
'{{AUS_1_SUMMARY}}': 'Reports say Blakey did a medical at North Melbourne, which has tabled a reported $11 million-plus contract and its No.6 pick. The Swans have not accepted the initial bid. More footy talk for the smoko room.',
'{{AUS_1_URL}}': 'https://www.afl.com.au/news/1628990/star-sydney-swans-defender-nick-blakey-makes-call-on-future-amid-rival-interest',
'{{AUS_2_HEADLINE}}': 'Chalmers Announces Two Backdowns After Backlash Over the Card Payment Ban',
'{{AUS_2_SUMMARY}}': 'Back from Japan, the Treasurer called a hastily arranged Friday press conference, according to ABC. Worth watching whether the six-month delay settles the argument.',
'{{VIC_1_HEADLINE}}': 'Police Investigate Another Melbourne Car Fire After Six Days of Arson Attacks',
'{{VIC_1_SUMMARY}}': 'ABC Victoria reports a police commander believes the attacks are linked to organised crime and are an intimidation tactic. Lock up vehicles and report anything suspicious.',
'{{SCI_1_FLAG}}': '🦠 BIOLOGY · BACTERIA FIGHT BACK',
'{{SCI_1_HEADLINE}}': 'Virus Enzyme Cuts a Bacterial Sensor Protein and Triggers a Self-Destructing Immune Response',
'{{SCI_1_SUMMARY}}': 'ScienceDaily reports on 9 October that researchers found a new way bacteria detect viral attacks, which could lead to more effective phage therapies against drug-resistant infections.',
'{{INSIGHT_TITLE}}': 'AI Tools Get Switched Off: Keep Your Quotes and Customer Data in Files You Own',
'{{INSIGHT_BODY}}': 'Google has just stopped selling new Gemini Code Assist subscriptions, a reminder that AI products can be retired with little warning. For a small trades business, the lesson is simple: do not let your only copy of quote templates, price lists or customer notes live inside one AI tool. Keep them in plain documents or a spreadsheet you control, and treat the AI as a helper you can swap out. Then if a tool changes or disappears, you lose an afternoon, not your paperwork.',
'{{FACT_1}}': 'Commercial transit through the Strait of Hormuz was about 4 vessels on 4 October against a normal 85 a day, roughly 5% of pre-crisis traffic, according to one live tracker.',
'{{FACT_2}}': 'The RBA has raised the cash rate by a total of 100 basis points in 2026, with hikes in February, March, May and September, taking it to 4.60%.',
'{{FACT_3}}': 'A six-month study found high-intensity interval training helped older adults lose body fat while keeping muscle, unlike moderate workouts, which caused some lean muscle loss.',
'{{JOKE_SETUP}}': 'Why did the formwork carpenter never panic when a client wanted the job done yesterday?',
'{{JOKE_PUNCHLINE}}': '"He said he\'d already set the deadline in concrete, just not that one."',
'{{CLOSING_QUOTE}}': '"Make hay while the sun shines."',
'{{CLOSING_ATTR}}': '— English Proverb',
'{{CLOSING_MESSAGE}}': "It's Sunday 11 October, sunny and up to 25°C, so make the most of it before showers arrive tonight and Monday brings possible thunderstorms. Pack the tools and get any outdoor jobs sorted today.",
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
