#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Sunday, 25 October 2026',
'{{WEATHER_1}}': 'SUN 25 OCT · ⛈️ Storm day, thunderstorms likely early in Melbourne then showers, with 30–40 mm possible across Saturday night and Sunday',
'{{WEATHER_2}}': 'MON 26 OCT · 🌦️ Cooler, showery afternoon, clearing to a chilly evening · about 15°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'TUE 27 OCT · 🌤️ Some sun with a shower or two possible · about 16°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'WED 28 OCT · ☀️ Mostly cloudy to sunny, drier · about 17°C',
'{{WEATHER_5}}': 'THU 29 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "The Bureau of Meteorology says Melbourne could see 30 to 40 mm of rain from Saturday night into Sunday, with severe thunderstorms possible across central and eastern Victoria and the best chance of storms in Melbourne early this morning. Much cooler air follows from the west. I couldn't find an official BoM forecast for Carrum Downs itself, so the Monday to Wednesday temperatures come from commercial forecast sites and Thursday is unconfirmed. Check BoM before planning outdoor or coating work.",
'{{WORLD_1_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_1_HEADLINE}}': "Saudi Forces Say They Intercepted Two Houthi Missiles Aimed at Yanbu and Taif",
'{{WORLD_1_SUMMARY}}': "Dawn's live coverage reports Saudi forces shot down the missiles. Yanbu is the Red Sea export hub that lets Riyadh bypass the Hormuz blockade, so attacks near it matter for oil prices. The reports come from a live blog and I could not check them against an official statement.",
'{{WORLD_1_URL}}': 'https://dawn.com/live/iran-israel-war',
'{{WORLD_2_FLAG}}': '🌍 IRAN',
'{{WORLD_2_HEADLINE}}': "Iran Says Hormuz Reopening Conditions Still Stand, With Strait Reopening on Day Six of a Seven-Day Ceasefire Plan",
'{{WORLD_2_SUMMARY}}': "CBS News's live updates report Foreign Minister Araghchi saying Tehran is reviewing US comments on the plan, with the strait reopening on day six and talks starting on day seven if the US lifts its blockade of Iranian ports. Trump has previously rejected the plan, and the IMO warns the route may not be clear of mines.",
'{{WORLD_2_URL}}': 'https://www.cbsnews.com/live-updates/iran-war-us-trump-strait-of-hormuz-yemen-houthis-saudi-arabia/',
'{{ECON_1_FLAG}}': '📈 ASX · MARKETS',
'{{ECON_1_HEADLINE}}': 'ASX 200 Edges Up on Friday to About 8,795 as Oil Climbs and US Tech Stocks Slide on AI Spending Doubts',
'{{ECON_1_SUMMARY}}': "ABC's Friday close blog has the local market barely higher, with the Aussie dollar near 70 US cents and gold around US$4,021 an ounce. Markets are shut over the weekend, so this is the latest close. The next test is Monday, with oil near US$113 a barrel.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/news/2026-10-23/asx-markets-business-news-live-updates-oct-23/107291840',
'{{ECON_2_FLAG}}': '⛽ FUEL · DIESEL',
'{{ECON_2_HEADLINE}}': 'Diesel Still Near 280 Cents a Litre as Brent Crude Pushes Back Above US$100',
'{{ECON_2_SUMMARY}}': "The latest ACCC figures I could find (week to 14 October) had the five-city average at 278.5 cents for diesel and 241.9 for petrol, so these are not today's bowser prices. Brent has since climbed on fresh Houthi attacks on Saudi Arabia, which points to more pain at the pump. Check your fuel card prices before booking the week's runs.",
'{{TECH_1_FLAG}}': '🔐 SECURITY · WEBSITES',
'{{TECH_1_HEADLINE}}': "AI-Found PHP Flaws ('PHP2Shell') Force Patches Worldwide After Government Sites Went Dark",
'{{TECH_1_SUMMARY}}': "CNN and Fortune report two critical remote code execution flaws in PHP, which runs a huge share of websites, found with AI help. Fixes shipped in PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35. If your website or booking system runs on PHP (WordPress does), ask your web host whether they have patched. The story is from 21 to 22 October, with follow-up coverage since.",
'{{TECH_1_URL}}': 'https://www.cnn.com/2026/10/21/tech/php2shell-vulnerability-ai-intl',
'{{TECH_2_FLAG}}': '🤖 AI · INDUSTRY',
'{{TECH_2_HEADLINE}}': "Anthropic's Draft IPO Filing Shows $16.3 Billion in Half-Year Revenue and an $80.7 Billion Loss",
'{{TECH_2_SUMMARY}}': "WSJ-sourced reports say about 20% of revenue came from just two customers. It is a reminder that even the biggest AI vendors are burning cash and changing fast, so keep your quotes and customer records in files you own. The figures come from reports on a draft filing, not the SEC document, and I haven't verified them.",
'{{ROBOT_1_FLAG}}': '🤖 AMR · WAREHOUSE',
'{{ROBOT_1_HEADLINE}}': "HOJ Innovations Deploys an Autonomous Mobile Robot Fleet at Hunter Douglas's Salt Lake City Fulfilment Centre",
'{{ROBOT_1_SUMMARY}}': "Robotics 24/7 reports the robots replaced an overhead conveyor system that was causing safety risks and breaking down often. A practical example of automation arriving in a working warehouse rather than a lab. The article is listed as about a day old but carries no exact date.",
'{{ROBOT_1_URL}}': 'https://www.robotics247.com/article/hoj-innovations-deploys-amr-fleet-at-hunter-douglas-salt-lake-city-fulfillment-center',
'{{AUS_1_HEADLINE}}': "Independent MP Helen Haines Now Serious but Stable in Hospital After Alleged Attack",
'{{AUS_1_SUMMARY}}': "ABC News reports the Indi MP, who was struck by a car, has improved from critical condition, and the hospital says her condition is better. Brendan Nugent has been charged with three offences.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-24/helen-haines-condition-update/107304464',
'{{AUS_2_HEADLINE}}': "Perth Grandmother Donna Nelson Returns Home From Japan on an International Prisoner Transfer",
'{{AUS_2_SUMMARY}}': "ABC News reports she is back in Western Australia and her family says they are overjoyed to have her home.",
'{{VIC_1_HEADLINE}}': "Weekend Washout: Severe Thunderstorms Possible Across Central and Eastern Victoria",
'{{VIC_1_SUMMARY}}': "ABC News says storm season is intensifying across the country, with thunderstorms most likely in Melbourne early on Sunday morning. Secure loose gear, check gutters and downpipes at the yard, and expect wet roads on the Monday commute.",
'{{SCI_1_FLAG}}': '🧠 HEALTH',
'{{SCI_1_HEADLINE}}': "Seven-Year Study Finds Exercise Slows Memory and Movement Decline in Parkinson's Disease",
'{{SCI_1_SUMMARY}}': "ScienceDaily reports a study in Neurology found people exercising more than eight hours a week showed almost no average cognitive decline. The release is dated 22 October, a little over the 48-hour window.",
'{{INSIGHT_TITLE}}': "Ask AI to Compare Supplier Price Lists and Flag Increases Before You Quote",
'{{INSIGHT_BODY}}': "With fuel and freight costs moving, supplier prices drift up in small steps that are easy to miss. Paste last month's and this month's price list into an AI tool and ask it to list every line that went up, by how much, and which jobs in your pipeline use those items. Use the result to update quotes before they go out. Check the numbers yourself against the original invoices, and leave customer names and bank details out of what you paste. It takes about ten minutes and can save you from quoting on yesterday's prices.",
'{{FACT_1}}': "After the PHP2Shell disclosure, government websites in France, the Netherlands, Belgium and Australia were reportedly taken offline as a precaution.",
'{{FACT_2}}': "The Bureau of Meteorology has said Melbourne could see 30 to 40 mm of rain from Saturday night into Sunday.",
'{{FACT_3}}': "Wiz says the PHP flaws affect every PHP release of the past decade, going back to version 5.4.",
'{{JOKE_SETUP}}': "Why did the concreter love a quiet Sunday?",
'{{JOKE_PUNCHLINE}}': '"It was the only day everything finally set."',
'{{CLOSING_QUOTE}}': '"Rest is not idleness."',
'{{CLOSING_ATTR}}': '— John Lubbock',
'{{CLOSING_MESSAGE}}': "It's Sunday, and the storms are due early with 30 to 40 mm possible, so let the rain make the call. Make sure the gear is secure, ask your web host about the PHP patch, and ease into a showery Monday.",
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
