#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Monday, 12 October 2026',
'{{WEATHER_1}}': 'MON 12 OCT · ⛈️ Showers very likely, thunderstorm possible in the morning · up to 19°C · 3–15 mm',
'{{WEATHER_2}}': 'TUE 13 OCT · 🌧️ High chance of showers, mostly afternoon and evening · 8–16°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'WED 14 OCT · ☁️ Cloudy · 9–16°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'THU 15 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'FRI 16 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': 'Monday is the wettest day of the week: showers very likely with 3 to 15 mm possible and a chance of a morning thunderstorm, so keep outdoor work flexible. Tuesday stays showery, then Wednesday turns cloudy and cool. Based on Bureau of Meteorology Melbourne forecasts issued Saturday 10 October, so Carrum Downs may differ, and Thursday and Friday could not be confirmed.',
'{{WORLD_1_FLAG}}': '🌎 PANAMA · MAJOR EARTHQUAKE',
'{{WORLD_1_HEADLINE}}': 'Magnitude 7.7 Earthquake Strikes Panama, Collapsing Buildings Near the Epicentre',
'{{WORLD_1_SUMMARY}}': 'The USGS first reported magnitude 8.0 before revising to 7.7 for the Friday 9 October quake near Herrera Province. Evacuations were ordered across the country and aftershocks up to magnitude 6.0 followed. This is slightly older than 48 hours, and casualty details are still emerging.',
'{{WORLD_1_URL}}': 'https://www.nbcmiami.com/news/national-international/strong-earthquake-shakes-panama/3870962/',
'{{WORLD_2_FLAG}}': '✈️ SAUDI ARABIA · AIRPORT ATTACK',
'{{WORLD_2_HEADLINE}}': 'World Condemns Deadly Houthi Attack on Riyadh Airport That Killed a Saudia Pilot',
'{{WORLD_2_SUMMARY}}': 'Saudi aviation authorities say three people died, including a Saudia pilot, after strikes on King Khalid International Airport and a Saudia aircraft. The GCC, Qatar, the UN, UK and EU condemned it. Outlets disagree on the exact date, between 6 and 8 October.',
'{{WORLD_2_URL}}': 'https://qna.org.qa/en/News-Area/News/2026-10/9/gcc-condemns-deadly-houthi-attack-on-riyadh-airport',
'{{ECON_1_FLAG}}': '🛢️ RATES · OIL SHOCK RISK',
'{{ECON_1_HEADLINE}}': 'Commentary Warns the RBA\'s Rate Rise Risks Turning an Oil Shock Into a Recession',
'{{ECON_1_SUMMARY}}': 'An Independent Australia opinion piece argues that lifting the cash rate to 4.60% on top of high fuel costs could tip the economy into recession. It is commentary, not a forecast, but worth watching if you carry finance or an overdraft. Next RBA meeting is 3 November.',
'{{ECON_1_URL}}': 'https://independentaustralia.net/article-display/rba-rate-rise-risks-turning-oil-shock-into-recession,21624',
'{{ECON_2_FLAG}}': '🧾 TAX OFFICE · CARD BAN DELAYED',
'{{ECON_2_HEADLINE}}': 'Treasurer Forces ATO to Delay Its Own Credit Card Payment Ban Until 30 June 2027',
'{{ECON_2_SUMMARY}}': 'The Tax Office had planned to stop taking card payments from 30 November, but small business groups argued cards help manage lumpy cash flow. The ATO says card fees would cost it almost $200 million a year. Funding is to be finalised in December.',
'{{TECH_1_FLAG}}': '🛡️ AI · AGENT SAFETY',
'{{TECH_1_HEADLINE}}': 'Anthropic Cuts Internal Agent Evaluations Off From the Live Internet',
'{{TECH_1_SUMMARY}}': 'TechCrunch reports Anthropic says it cannot yet reliably control its AI agents, so internal tests now run without live internet access. A useful reminder to test any AI agent in a sandbox before it touches real customer systems.',
'{{TECH_1_URL}}': 'https://techcrunch.com/2026/10/09/anthropic-cant-reliably-control-its-ai-agents-its-cutting-off-its-internal-evals-from-the-live-internet',
'{{TECH_2_FLAG}}': '💬 AI · CHATGPT GETS INTERACTIVE',
'{{TECH_2_HEADLINE}}': 'OpenAI Rolls GPT-6 Into ChatGPT With an "Intelligent UI" of Charts, Forms and Calculators',
'{{TECH_2_SUMMARY}}': 'A weekly AI roundup says paid ChatGPT tiers can now build interactive calculators and forms inside a conversation, handy for quick job-costing tools. This comes from aggregator coverage rather than an OpenAI announcement, so check before relying on it.',
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · HUMANOIDS ON THE LINE',
'{{ROBOT_1_HEADLINE}}': 'Renault Puts Wandercraft\'s Calvin-40 Humanoid Into Service at Its French EV Plant',
'{{ROBOT_1_SUMMARY}}': 'Renault reports about 350 more humanoids planned over 18 months, aiming to cut production hours per vehicle by 30%. The figures are company-reported, and I could not confirm the publication date, so it may be older than 48 hours.',
'{{ROBOT_1_URL}}': 'https://letsdatascience.com/news/renault-deploys-humanoid-robots-to-boost-production-4ad0dba0',
'{{AUS_1_HEADLINE}}': 'Coalition Calls Card Ban Delay a "Stay of Execution" for Small Business, Not a Solution',
'{{AUS_1_SUMMARY}}': 'Shadow Treasurer Tim Wilson says the Prime Minister dragged the Treasurer into the backdown, while the Coalition also criticised the original timeline. Sourced from a Liberal Party statement dated 9 October, so it is partisan.',
'{{AUS_1_URL}}': 'https://www.canberratimes.com.au/story/9365558/treasurer-swipes-left-on-tax-office-credit-card-ban/',
'{{AUS_2_HEADLINE}}': 'High Court Hands Down Decision on the Mount Pleasant Coal Mine',
'{{AUS_2_SUMMARY}}': 'A 7 October decision on the Hunter Valley mine was listed in political statements, but I could not confirm the ruling details, so check a news site for the outcome.',
'{{VIC_1_HEADLINE}}': 'Teen Critical After Alleged Botched Firebombing as Melbourne Arson Wave Continues',
'{{VIC_1_SUMMARY}}': 'ABC Melbourne reports a 13-year-old boy is in critical condition, and his sister is urging teens not to take cash for crimes. It follows six straight days of car arson attacks across the city.',
'{{SCI_1_FLAG}}': '⏱️ PHYSICS · NUCLEAR CLOCK',
'{{SCI_1_HEADLINE}}': 'Vienna Team Builds the First Self-Stabilising Nuclear Clock',
'{{SCI_1_SUMMARY}}': 'Published in Nature on 7 October, a thorium-229 crystal kept a laser on frequency for over 24 hours with no manual adjustment. Drift is estimated at about one second in 30 million years, but it is still a lab prototype.',
'{{INSIGHT_TITLE}}': 'Sandbox First: Trial Any AI Agent on Dummy Jobs Before It Touches Real Customers',
'{{INSIGHT_BODY}}': 'Anthropic has just locked its own test agents away from the live internet because it cannot yet fully control them. If the company that built the tool does that, a small trades business should too. Before you let an AI assistant send quotes, chase invoices or answer customers, run it on a few made-up jobs and a spare email address. Read what it would have sent, fix the instructions, and only then switch it on for real. An hour of dummy runs is far cheaper than one embarrassing email to a good client.',
'{{FACT_1}}': 'The USGS first reported Friday\'s Panama earthquake as magnitude 8.0, then revised it down to 7.7 as more seismic data came in.',
'{{FACT_2}}': 'The new thorium-229 nuclear clock is estimated to drift by about one second in 30 million years, yet its makers say it is not yet as good as the best optical atomic clocks.',
'{{FACT_3}}': 'The International Federation of Robotics estimates only about 7,000 humanoid robots were sold worldwide in 2025, mostly for collecting AI training data rather than doing productive work.',
'{{JOKE_SETUP}}': 'Why did the glazier never lose a customer over a late job?',
'{{JOKE_PUNCHLINE}}': '"He always said he could see right through the delay, and so could they."',
'{{CLOSING_QUOTE}}': '"A bad workman always blames his tools."',
'{{CLOSING_ATTR}}': '— English Proverb',
'{{CLOSING_MESSAGE}}': "It's Monday 12 October with showers and a possible morning thunderstorm, so plan indoor prep and paperwork first and save outdoor work for a drier window. Get the week's quotes out early.",
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
