#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Monday, 26 October 2026',
'{{WEATHER_1}}': 'MON 26 OCT · 🌦️ Showers likely in the southeast suburbs, mostly afternoon and evening · 8–15°C',
'{{WEATHER_2}}': 'TUE 27 OCT · 🌧️ Medium chance of showers, morning and afternoon · cool',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'WED 28 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'THU 29 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_5}}': 'FRI 30 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Showers are forecast for Melbourne's southeast on Monday and again Tuesday, so plan outdoor coating and blasting work around the afternoon. Monday figures come from WillyWeather (Moorabbin Airport reference station); I couldn't reach the Bureau of Meteorology or find an official Carrum Downs forecast, and Wednesday to Friday are unconfirmed. Check BoM before committing to exterior work.",
'{{WORLD_1_FLAG}}': '🌍 IRAN · US',
'{{WORLD_1_HEADLINE}}': "Trump Says He Is Weighing an Iran Deal Against Action to \"Finish Them Off\"",
'{{WORLD_1_SUMMARY}}': "CBS News live updates report Trump deciding between an agreement with Tehran and further military action, with foreign ministers from seven nations due to meet in Istanbul on the Strait of Hormuz. Iran says indirect talks via Pakistan and Qatar continue over its seven-day ceasefire plan. The Hormuz blockade is the root of your fuel and freight costs.",
'{{WORLD_1_URL}}': 'https://www.cbsnews.com/live-updates/iran-war-trump-us-oil-gas-prices-strait-of-hormuz-midterms/',
'{{WORLD_2_FLAG}}': '🌍 SAUDI ARABIA',
'{{WORLD_2_HEADLINE}}': "Houthis Launch Another Wave of Attacks on Saudi Arabia, Lifting Oil Prices",
'{{WORLD_2_SUMMARY}}': "The National and CNBC report Houthi strikes on Saudi targets including Dammam airport and an Aramco facility at Yanbu, with two people killed. Claims of damage at Yanbu are disputed and no Saudi barrels are confirmed lost, but the risk alone is pushing prices up. These reports are from 22 to 23 October, the latest I could find.",
'{{WORLD_2_URL}}': 'https://www.thenationalnews.com/business/energy/2026/10/23/oil-prices-rise-as-houthis-launch-another-wave-of-attacks-on-saudi-arabia/',
'{{ECON_1_FLAG}}': '🛢️ OIL · BRENT',
'{{ECON_1_HEADLINE}}': 'Brent Crude Settles at US$116.72, Its Highest Close Since Late April',
'{{ECON_1_SUMMARY}}': "Brent rose about 3 per cent on Friday and about 6 per cent over the week, its third weekly gain, on Houthi attacks and expectations of renewed US strikes on Iran. Other sources quote slightly different figures. Expect diesel to follow with a lag, so factor it into quotes for longer jobs.",
'{{ECON_1_URL}}': 'https://financefeeds.com/brent-crude-oil-price-116-72-saturday-week-ahead-houthi-saudi-fed-28-october-bull-120-bear-108/',
'{{ECON_2_FLAG}}': '⛽ FUEL · DIESEL',
'{{ECON_2_HEADLINE}}': 'Diesel Was Near 280 Cents a Litre in Sydney Last Week, With the Oil Jump Yet to Flow Through',
'{{ECON_2_SUMMARY}}': "NRMA's weekly report for 19 October had Sydney diesel at 280.1 cents and unleaded at 239.8, with unleaded expected to ease. That was before Friday's oil rally, and it is a Sydney figure from a week ago, not today's Melbourne bowser price. I couldn't find a newer national figure.",
'{{TECH_1_FLAG}}': '🤖 AI · AGENTS',
'{{TECH_1_HEADLINE}}': "Anthropic Launches Claude Duet, a Proactive Personal AI Agent, in Research Preview",
'{{TECH_1_SUMMARY}}': "Coverage says Duet sends a morning brief, checks in every few hours and asks for sign-off before big actions like payments. It is waitlist-only for US Pro and Max subscribers for now, so not usable in Australia yet. It was announced on 21 October, so slightly older than 48 hours.",
'{{TECH_1_URL}}': 'https://iphoneincanada.ca/2026/10/21/claude-duet-proactive-ai-agent-app',
'{{TECH_2_FLAG}}': '☁️ AI · CLOUD',
'{{TECH_2_HEADLINE}}': "OpenAI and Google Cloud Agree to Offer OpenAI Models and Codex Inside Google Cloud",
'{{TECH_2_SUMMARY}}': "The deal starts as a private preview and puts rival AI models on one cloud platform. For a small business it means more choice and likely price pressure on the AI tools you already pay for. I couldn't confirm the exact announcement date.",
'{{ROBOT_1_FLAG}}': '🤖 HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': "110 Humanoid Robots Set a Guinness World Record for Synchronised Dancing in China",
'{{ROBOT_1_SUMMARY}}': "Global Times reports the record, with the organisers pointing to large-scale deployment next. A stunt, but it shows how many coordinated units Chinese makers can now field. I couldn't confirm the exact publication date, so treat it as October 2026.",
'{{ROBOT_1_URL}}': 'https://www.globaltimes.cn/page/202610/1372888.shtml',
'{{AUS_1_HEADLINE}}': "Politicians to Get Security Briefing After Helen Haines Attack as MPs Report Rising Threats",
'{{AUS_1_SUMMARY}}': "The Nightly reports ASIO and the AFP will brief MPs and senators, while Haines remains in a critical but stable condition at the Alfred Hospital after losing both legs. Police have called it a targeted attack.",
'{{AUS_1_URL}}': 'https://thenightly.com.au/politics/politicians-to-get-security-brief-after-car-attack-left-independent-mp-helen-haines-fighting-for-life-c-23050990',
'{{AUS_2_HEADLINE}}': "First Flight Takes Off From Western Sydney International Airport",
'{{AUS_2_SUMMARY}}': "ABC News lists the first flight from the new airport among its top stories on 25 October.",
'{{VIC_1_HEADLINE}}': "Final MotoGP Race at Phillip Island Washed Out",
'{{VIC_1_SUMMARY}}': "ABC News reports the last MotoGP race at Phillip Island was lost to the weather, part of the wet weekend across southern Australia. Expect more showers around the bay this week.",
'{{SCI_1_FLAG}}': '🔭 ASTRONOMY',
'{{SCI_1_HEADLINE}}': "Three Giant Black Holes Found Feeding in One Galaxy From the Dawn of Time",
'{{SCI_1_SUMMARY}}': "Max Planck Institute astronomers report three actively feeding black holes in a galaxy more than 12.5 billion light-years away, two of them just 620 light-years apart and expected to merge eventually. ScienceDaily, 25 October.",
'{{INSIGHT_TITLE}}': "Rain on the Roster? Let AI Rebuild Your Week in Five Minutes",
'{{INSIGHT_BODY}}': "With showers forecast Monday and Tuesday, outdoor jobs shuffle fast. Paste your booked jobs, which ones are weather-sensitive and any cure or recoat time limits into an AI tool, and ask it to propose a reshuffle that puts indoor and shed work on wet days. Then ask it to draft short messages to the customers who move. It won't know your site, so check the plan, but it saves the phone-tag and gets the new dates out before anyone rings you.",
'{{FACT_1}}': "Brent crude settled at US$116.72 on Friday, its highest close since 29 April.",
'{{FACT_2}}': "Two of the three black holes in the newly reported galaxy are only about 620 light-years apart.",
'{{FACT_3}}': "From 1 October 2026 Australian businesses can no longer add a surcharge to eftpos, Mastercard, Visa or Amex payments.",
'{{JOKE_SETUP}}': "Why did the plasterer never argue with the weather forecast?",
'{{JOKE_PUNCHLINE}}': '"He knew a wet Tuesday was just a long smooth finish waiting to happen."',
'{{CLOSING_QUOTE}}': '"Plans are worthless, but planning is everything."',
'{{CLOSING_ATTR}}': '— Dwight D. Eisenhower',
'{{CLOSING_MESSAGE}}': "It's Monday with showers due this afternoon, so slot the indoor and prep jobs into the wet hours. Check what Friday's oil jump does to your diesel costs before you send this week's quotes.",
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
