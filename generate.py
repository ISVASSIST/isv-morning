#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 2 October 2026',
'{{WEATHER_1}}': 'FRI 2 OCT · ⛈️ Cloudy, very high chance of rain, possible afternoon/evening thunderstorm, 10–35mm · 11–17°C',
'{{WEATHER_2}}': 'SAT 3 OCT · 🌧️ Rain, cool · 11–17°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SUN 4 OCT · ☀️ Mostly clear, dry · 11–17°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'MON 5 OCT · ☁️ Cloudy, dry · 8–18°C',
'{{WEATHER_5}}': 'TUE 6 OCT · 🌦️ Showers, cool · 10–14°C',
'{{WEATHER_ALERT}}': 'Wet and cool today: very high chance of rain with a possible afternoon and evening thunderstorm and 10–35mm, easing to a dry Sunday and Monday before showers return Tuesday. Forecast based on Melbourne BOM and online outlooks.',
'{{WORLD_1_FLAG}}': '✈️ UAE / SAUDI ARABIA · PASSENGERS FOIL ATTEMPT TO CRASH DUBAI–TEL AVIV FLIGHT',
'{{WORLD_1_HEADLINE}}': 'Passengers Help Foil Attempted Hijacking of Flydubai Jet After Cockpit Stabbing',
'{{WORLD_1_SUMMARY}}': 'A Flydubai 737 MAX lost more than 14,000 feet in under 30 seconds after a pilot reportedly stabbed his colleague; passengers and crew overpowered the attacker and a second pair of pilots landed safely at Tabuk in Saudi Arabia. The suspect has since been transferred to the UAE and Flydubai has suspended its Israel flights.',
'{{WORLD_1_URL}}': 'https://www.cnn.com/2026/10/01/world/live-news/flydubai-flight-israel-pilot-passengers-intl',
'{{WORLD_2_FLAG}}': '🇹🇭 THAILAND · BANGKOK FLOODWATERS EASE AFTER WORST FLOODS IN 15 YEARS',
'{{WORLD_2_HEADLINE}}': 'Thailand Floods Kill 24 as Water Recedes in Bangkok',
'{{WORLD_2_SUMMARY}}': 'Torrential rain has hit about 2.6 million people across 29 provinces and Bangkok since mid-September, with a flood emergency declared in the capital on 26 September; waters are now receding but the clean-up and airport disruption continue.',
'{{WORLD_2_URL}}': 'https://www.thestar.com.my/aseanplus/aseanplus-news/2026/10/01/thailand-floods-kill-24-as-water-recedes-in-bangkok',
'{{ECON_1_FLAG}}': '📉 ASX · SHARES SLUMP 2% TO LOWEST LEVEL SINCE JUNE',
'{{ECON_1_HEADLINE}}': 'ASX Drops 2 Per Cent to Lowest Level Since Mid-June as Oil Prices and Bond Yields Bite',
'{{ECON_1_SUMMARY}}': "Every sector fell as higher oil prices pushed global bond yields up and rate-hike fears grew after a Wall Street sell-off. For a small operator it's another signal that borrowing costs and fuel are staying high, so keep a buffer and price jobs accordingly.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/news/2026-10-01/asx-markets-business-news-live-updates-thursday-1-october/107204216',
'{{ECON_2_FLAG}}': '🏦 RBA · CASH RATE AT 4.60% AS FUEL AND SUPPLIER COSTS SQUEEZE SMALL BUSINESS',
'{{ECON_2_HEADLINE}}': 'Rate Hikes, Fuel Costs and Cautious Customers Keep Pressure on Small Business',
'{{ECON_2_SUMMARY}}': "With the cash rate at 4.6% after the RBA's fourth hike this year and the end of fuel subsidies, commentators say higher interest, fuel and supplier costs are weighing on small business confidence. Review your pricing and payment terms, and chase overdue invoices early.",
'{{TECH_1_FLAG}}': '🧰 AI · PERPLEXITY "SKILLS" GIVE SMALL BUSINESSES READY-MADE WORKFLOWS',
'{{TECH_1_HEADLINE}}': 'Amex Business Cardholders Get Prebuilt AI "Skills" Inside Perplexity Computer',
'{{TECH_1_SUMMARY}}': 'Skills are ready-made workflows for everyday business tasks, and from 1 October eligible cardholders can claim 1,000 bonus credits with a Perplexity Enterprise subscription. A sign AI is shifting from blank chat boxes to plug-in task templates.',
'{{TECH_1_URL}}': 'https://upgradedpoints.com/news/amex-business-cards-perplexity-ai-benefits/',
'{{TECH_2_FLAG}}': '💬 AI · EZ TEXTING LAUNCHES AI-DRIVEN RCS BUSINESS MESSAGING',
'{{TECH_2_HEADLINE}}': 'EZ Texting Launches RCS Messaging Tool That Builds Templates and Automates Customer Replies',
'{{TECH_2_SUMMARY}}': 'The tool generates interactive message templates, handles rich media and automates response flows. Handy idea for trades wanting quote follow-ups and appointment reminders without lifting a finger, though keep a human checking anything pricing-related.',
'{{ROBOT_1_FLAG}}': '🤖 USA · AGILITY ROBOTICS AND FORT ROBOTICS TEAM UP ON HUMANOID SAFETY',
'{{ROBOT_1_HEADLINE}}': 'Agility Robotics Signs MOU With FORT Robotics to Build an Off-Robot Safety Bridge for Digit',
'{{ROBOT_1_SUMMARY}}': "The Offboard Safety Bridge will connect Digit humanoids to a facility's own safety systems, extending safety beyond the robot itself, a key step before humanoids can work alongside people in warehouses and factories.",
'{{ROBOT_1_URL}}': 'https://www.humanoidsdaily.com/',
'{{AUS_1_HEADLINE}}': 'Howard-Era Minister Voted to Outlaw Offshore Casinos, Then Co-Founded One',
'{{AUS_1_SUMMARY}}': 'ABC reports former minister De-Anne Kelly was a co-founder and part-owner of LuckyBet, an online casino registered in the Caribbean, after voting for the 2001 law banning offshore casinos from taking Australian customers.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-02/former-minister-de-anne-kelly-co-founded-offshore-casino/107197106',
'{{AUS_2_HEADLINE}}': 'Keogh Says He Can Still Work With Veterans After Health Cap Backdown',
'{{AUS_2_SUMMARY}}': "Veterans' Affairs Minister Matt Keogh says he listened to veterans and can still work collaboratively with them after the government scrapped a budget plan to cap veterans' allied health services at $5,000 a year.",
'{{VIC_1_HEADLINE}}': 'Melbourne International Games Week Kicks Off, Running 2–11 October',
'{{VIC_1_SUMMARY}}': 'Venues across Melbourne are hosting the latest digital games for the public to see and play over the next ten days, a good excuse for a gamer to duck out after a wet Friday.',
'{{SCI_1_FLAG}}': '🦗 BIOLOGY · NEW GIANT AUSTRALIAN STICK INSECTS FOUND, ONE WITH LIDDED EGGS',
'{{SCI_1_HEADLINE}}': 'Giant Stick Insect Fooled Scientists for Decades, Revealing Two New Australian Species',
'{{SCI_1_SUMMARY}}': 'Researchers identified two new species of large Australian stick insects, one laying remarkable lidded eggs never recorded in the group, and found a familiar species had been misidentified for decades. ScienceDaily, 30 September 2026.',
'{{INSIGHT_TITLE}}': "AI 'Skills' Are Ready-Made Workflows — Pick One Repeatable Job and Start There",
'{{INSIGHT_BODY}}': "Tools like Perplexity are now shipping prebuilt 'Skills', packaged workflows for common tasks, which means you no longer have to invent prompts from scratch. Pick one repetitive job, such as writing quote follow-ups, summarising supplier emails or drafting job completion notes, and run it as a trial for two weeks. Time how long it used to take, check every output before it reaches a customer, and keep it only if it saves you real hours. One small win beats five half-adopted tools.",
'{{FACT_1}}': 'Floods in Thailand have affected about 2.6 million people across 29 provinces and Bangkok since mid-September, making them the worst to hit the capital in 15 years.',
'{{FACT_2}}': 'The new Australian stick insect species found this week lay eggs with tiny lids, a feature never before recorded in the group.',
'{{FACT_3}}': "The Flydubai jet in this week's cockpit scare dropped more than 14,000 feet in less than 30 seconds before it was brought back under control.",
'{{JOKE_SETUP}}': 'A mobile window tinter was asked how his small business kept customers coming back, even when it rained all week and the jobs kept getting pushed.',
'{{JOKE_PUNCHLINE}}': 'He said, "I just keep a clear view of the forecast — and I never leave anyone in the dark."',
'{{CLOSING_QUOTE}}': '"Quality means doing it right when no one is looking."',
'{{CLOSING_ATTR}}': '— Henry Ford',
'{{CLOSING_MESSAGE}}': "It's Friday 2 October with a cool, wet day around Carrum Downs, a possible afternoon thunderstorm and up to 35mm. Push outdoor jobs to Sunday's dry window, use the wet hours for quotes and invoicing, and if you're keen on games, Melbourne International Games Week starts today.",
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
