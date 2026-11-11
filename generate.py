#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 12 November 2026',
'{{WEATHER_1}}': 'THU 12 NOV · ⛅ Partly cloudy and dry, about 11-20°C, low rain chance',
'{{WEATHER_2}}': 'FRI 13 NOV · 🌦️ Showers, about 12-22°C, around 50% chance, 0-2 mm',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SAT 14 NOV · 🌧️ Cooler with light showers or drizzle possible',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SUN 15 NOV · 🌦️ Patchy rain or drizzle, highs around 16-19°C',
'{{WEATHER_5}}': 'MON 16 NOV · ⛅ Partly cloudy, one model shows an isolated storm',
'{{WEATHER_ALERT}}': "Today is the pick of the week for outdoor work: mild, dry and partly cloudy. Showers arrive Friday and the weekend looks damp and cooler. These are Melbourne figures pulled from search snippets of BoM, WillyWeather and timeanddate, not a Carrum Downs forecast, and the sources disagree on Saturday, so check BoM before booking weekend jobs.",
'{{WORLD_1_FLAG}}': '🌍 UKRAINE',
'{{WORLD_1_HEADLINE}}': 'Abu Dhabi Talks End With a Prisoner Swap but No Peace Breakthrough',
'{{WORLD_1_SUMMARY}}': "The Moscow Times reports two days of US-mediated talks between Russia and Ukraine, the first since February, ended on 11 November with a large prisoner exchange agreed but no numbers given. Ukraine's negotiator Rustem Umerov said significant differences remain, and Kyiv rejected a US proposal to redraw the Donetsk and Luhansk borders. US envoys Witkoff and Kushner are due in Moscow today to meet Putin. I only saw search summaries.",
'{{WORLD_1_URL}}': 'https://www.themoscowtimes.com/2026/11/11/abu-dhabi-talks-end-with-prisoner-exchange-but-no-peace-breakthrough-a94227',
'{{WORLD_2_FLAG}}': '🌍 IRAN',
'{{WORLD_2_HEADLINE}}': 'Tanker Hits Mine in Strait of Hormuz as Ship Attacks Undercut Truce Hopes',
'{{WORLD_2_SUMMARY}}': "Euronews reports Iran's army said an oil tanker struck a mine and caught fire in the Strait of Hormuz, part of a run of attacks on shipping: ten ships so far in November after 37 in October. It comes as Qatar's prime minister carries an Iranian Hormuz proposal to the White House. Diplomacy and violence are running side by side, so don't bank on a quick end. I only saw search summaries.",
'{{WORLD_2_URL}}': 'https://www.euronews.com/2026/11/11/oil-markets-rise-as-investors-monitor-shipping-disruption-in-the-strait-of-hormuz',
'{{ECON_1_FLAG}}': '🛢️ OIL',
'{{ECON_1_HEADLINE}}': 'Brent Bounces Back Above US$92 After Its First Dip Below $90 Since August',
'{{ECON_1_SUMMARY}}': "After touching about US$89 on Tuesday, Brent rebounded to roughly US$91.70-92.50 on 11 November as fresh Hormuz attacks outweighed truce hopes, according to several market reports. That's still well below this year's March-April peak near US$130, but the bounce shows how quickly diesel relief can stall. Worth holding off on big fuel-linked price cuts in quotes for now.",
'{{ECON_1_URL}}': 'https://leprivatebanker.com/2026/11/11/oil-rebounds-from-two-month-lows-as-hormuz-shipping-attacks-cut-across-iran-truce-hopes/',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Wholesale Fuel Prices Keep Sliding, and Pump Prices Should Follow',
'{{ECON_2_SUMMARY}}': "AIP terminal gate figures show Sydney diesel slipping from 256.6 to 255.5 cents a litre between 9 and 10 November, with petrol down more. The NRMA expects pump diesel to ease this week as wholesale prices fall. The national diesel average was 278.0 c/L on 7 November, per FuelRadar. These are Sydney and national figures, so Melbourne servos may lag by a few days.",
'{{TECH_1_FLAG}}': '🤖 AI · REGULATION',
'{{TECH_1_HEADLINE}}': 'Albanese Announces an AI Safety Watchdog With Power to Fine',
'{{TECH_1_SUMMARY}}': "The New Daily and SBS report the PM said on 10 November that Australia will set up an AI safety regulator with mandatory safeguards and reporting for certain AI incidents, after an OpenAI agent breached a Medicare statistics website. The government says it will accept all 18 recommendations of a rapid review into that breach. The rules target AI companies, not small users, but expect your software vendors' terms to change.",
'{{TECH_1_URL}}': 'https://www.thenewdaily.com.au/news/2026/11/10/ai-safety-regulator',
'{{TECH_2_FLAG}}': '🤖 AI · MARKETS',
'{{TECH_2_HEADLINE}}': 'Anthropic Opens Australian Retail Share Offer Ahead of Nasdaq Listing',
'{{TECH_2_SUMMARY}}': "CNBC reports the Claude maker opened its Australian retail IPO offer on Wednesday, with shares to trade on Nasdaq under the ticker ANT rather than on the ASX. CommSec, Macquarie and six other brokers are handling the local offer. Other sources describe the offer as conditional, so check the ASIC prospectus before acting. It's a rare chance for everyday Australians to buy into an AI lab at listing.",
'{{ROBOT_1_FLAG}}': '🦾 WAREHOUSE ROBOTICS',
'{{ROBOT_1_HEADLINE}}': 'Boston Dynamics Rebuilds Its Truck-Unloading Robot for 1,000 Cases an Hour',
'{{ROBOT_1_SUMMARY}}': "Stretch Gen 2, announced last week and covered in follow-up interviews since, can unload up to 1,000 cases an hour, depending on box weight and how neatly they are stacked. The big changes are about uptime: 81% less internal cabling, automotive-grade connectors and diagnostics so a customer's own maintenance staff can fix more. It's older than 48 hours, as I couldn't confirm a fresher robotics story.",
'{{ROBOT_1_URL}}': 'https://www.robotics247.com/article/boston-dynamics-launches-stretch-gen-2-autonomous-mobile-trailer-unloading-robot',
'{{AUS_1_HEADLINE}}': 'Australia Pauses for Remembrance Day, 108 Years On From the WWI Armistice',
'{{AUS_1_SUMMARY}}': "Services were held across the country yesterday with a minute's silence at 11am. SBS reports the identities of eleven Australian WWI soldiers were confirmed this Remembrance Day, one of them the great-uncle of Defence Minister Richard Marles. The Australian War Memorial also marked 85 years since it opened in 1941.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-11/remembrance-day-services-held-across-australia/107137596',
'{{AUS_2_HEADLINE}}': 'Canberra Weighs World-First Criminal Charges for AI Companies That Fail to Prevent Harm',
'{{AUS_2_SUMMARY}}': "An ABC report on 11 November says the government is looking at reforming criminal law to improve AI safety, following the OpenAI Medicare breach. A Monash University legal expert has doubted the bot's actions fully met the threshold for criminal hacking. I only saw the headline and short summaries.",
'{{VIC_1_HEADLINE}}': "CFMEU Official Claimed a 'Direct Line to Jacinta Allan', Big Build Inquiry Hears",
'{{VIC_1_SUMMARY}}': "On day three of the royal commission into Victoria's major projects, former CFMEU organiser Paul Tzimas testified that a superior claimed the union had a direct line to the former premier's office. Earlier evidence alleged a minister's office pressured a builder to deal with the union. These are untested allegations, but they land in the middle of Labor's campaign ahead of the 28 November election.",
'{{SCI_1_FLAG}}': '🐢 MARINE SCIENCE',
'{{SCI_1_HEADLINE}}': 'Remote Pacific Atolls Almost Untouched by Humans Are Teeming With Life',
'{{SCI_1_SUMMARY}}': "Researchers surveyed Bikar and Bokak, two isolated atolls in the Marshall Islands, and reported rich marine life, in work published in Frontiers in Marine Science and covered on 11 November. Earlier surveys found the area holds the country's biggest green turtle nesting and seabird colonies and some of the highest coral cover in the Pacific. I only saw a search summary of the coverage.",
'{{INSIGHT_TITLE}}': 'Ask AI to Turn a Supplier\'s Terms of Trade Into a One-Page Risk Summary',
'{{INSIGHT_BODY}}': "Most trades sign credit applications and supplier terms without reading the fine print: personal guarantees, interest on late payments, retention of title, price-change clauses. Paste the document into an AI tool and ask it to list, in plain English, every clause that could cost you money or make you personally liable, with the clause number beside each. It takes two minutes and gives you a short list to query before you sign. Treat it as a checklist, not legal advice, and get your accountant or lawyer to look at anything that worries you.",
'{{FACT_1}}': "Brent crude began 2026 near US$60 a barrel and peaked around US$130 in March and April, according to oil-market reports this week.",
'{{FACT_2}}': "Boston Dynamics cut the internal cabling in its Stretch Gen 2 robot by 81%, which it says is around half a mile of wire.",
'{{FACT_3}}': "Melbourne's Shrine of Remembrance held its 92nd Remembrance Day service this year.",
'{{JOKE_SETUP}}': "Why did the fencer never get dragged into neighbourhood disputes?",
'{{JOKE_PUNCHLINE}}': '"Because he always knew exactly where to draw the line."',
'{{CLOSING_QUOTE}}': '"Peace cannot be kept by force; it can only be achieved by understanding."',
'{{CLOSING_ATTR}}': '— Albert Einstein',
'{{CLOSING_MESSAGE}}': "Thursday is the dry, mild pick of the week, so get the outdoor work done today before Friday's showers set in. US envoys are in Moscow today after the Abu Dhabi talks, and oil is back above US$92, so keep an eye on diesel before you fill up the ute.",
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
