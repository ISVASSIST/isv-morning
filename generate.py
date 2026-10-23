#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 24 October 2026',
'{{WEATHER_1}}': 'SAT 24 OCT · ⛈️ Showers, mostly afternoon and evening, with a severe thunderstorm risk · 1–10 mm',
'{{WEATHER_2}}': 'SUN 25 OCT · 🌧️ Wet day, showers morning and afternoon, 100% chance · 15–35 mm',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'MON 26 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'TUE 27 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_5}}': 'WED 28 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "A wet weekend for the south-east: this afternoon and evening brings showers with a risk of severe thunderstorms, possibly with damaging winds and large hail, mainly across the outer suburbs. Sunday is the wetter day, with 15 to 35 mm possible. I couldn't confirm Carrum Downs temperatures or the Monday to Wednesday outlook, so check BoM before planning outdoor or coating work.",
'{{WORLD_1_FLAG}}': '🌍 IRAN WAR',
'{{WORLD_1_HEADLINE}}': "Trump Says Iran Is 'Making Up Fake Hits' on Ships to Drive Up Oil Prices Before the Midterms",
'{{WORLD_1_SUMMARY}}': "Times of Israel's 22 October live blog reports Trump accusing Iran of faking attacks, while Iran's Revolutionary Guard says it disabled seven tankers near Hormuz. The two sides' accounts directly conflict, so treat each with caution. Fuel prices remain exposed either way.",
'{{WORLD_1_URL}}': 'https://timesofisrael.com/liveblog-october-22-2026',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': "Iran Warns the Conflict 'Will Extend' to US Bases if Washington Keeps Escorting Ships Through Hormuz",
'{{WORLD_2_SUMMARY}}': "Fox News's 22 October coverage reports the Revolutionary Guard's 'serious warning'. Other reports say Trump told a reporter the US is not negotiating with Iran, while Tehran says a seven-day ceasefire proposal remains on the table. One US official reportedly left a weekend strike open.",
'{{WORLD_2_URL}}': 'https://www.foxnews.com/live-news/us-iran-war-strait-hormuz-oil-prices-10-22-26',
'{{ECON_1_FLAG}}': '📈 ASX · MARKETS',
'{{ECON_1_HEADLINE}}': 'ASX 200 Finishes Friday Flat at 8,795 as Surging Oil Hammers Miners and Gold Stocks',
'{{ECON_1_SUMMARY}}': "Market Index's Friday wrap has banks, utilities and healthcare holding the index up, with the Aussie dollar near 70 US cents. ABC's blog notes a US tech selloff over AI spending worries weighed on sentiment.",
'{{ECON_1_URL}}': 'https://www.marketindex.com.au/news/evening-wrap-asx-200-steady-as-gold-and-base-metals-bloodbath-sparks-rush',
'{{ECON_2_FLAG}}': '⛽ FUEL · OIL',
'{{ECON_2_HEADLINE}}': 'Oil Hits a Five-Month High With Brent Above US$113 After More Houthi Attacks on Saudi Arabia',
'{{ECON_2_SUMMARY}}': "ABC's Friday markets blog has Brent topping US$113 a barrel; some reports put intraday highs higher. Diesel at the bowser lags crude by a week or two, so check supplier prices before locking in quotes that include fuel.",
'{{TECH_1_FLAG}}': '🤖 AI · AGENTS',
'{{TECH_1_HEADLINE}}': "OpenAI Says Its Frontier Models and Codex Coding Agent Are Coming to Google Cloud 'in the Coming Weeks'",
'{{TECH_1_SUMMARY}}': "Reported by Tech Insider this week as the big three clouds all carry OpenAI models. Practically, it means more places for software vendors to offer AI features, and more competition on price. Details come from trade press, so wait for the vendors' own announcements.",
'{{TECH_1_URL}}': 'https://tech-insider.org/openai-models-google-cloud-big-3-2026/',
'{{TECH_2_FLAG}}': '💻 AI · MARKETS',
'{{TECH_2_HEADLINE}}': "Wall Street Tech Selloff Over AI Spending Concerns Weighs on Sentiment Ahead of the ASX Open",
'{{TECH_2_SUMMARY}}': "ABC's 23 October markets blog: the S&P 500 fell 1.2% overnight as investors questioned how fast huge AI investments will pay back. For small businesses the takeaway is to buy AI tools that save you time now, not on hype.",
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS · AUTOMOTIVE',
'{{ROBOT_1_HEADLINE}}': "Audi, Agile Robots, Dassault and NVIDIA Test Mobile Humanoids for Parts Sequencing at Ingolstadt",
'{{ROBOT_1_SUMMARY}}': "Announced 21 October at NVIDIA GTC Berlin: a proof of concept where humanoids pick parts from containers and place them in assembly order, tested first in a digital twin. Audi handles about a million picks a day there. It is still a trial, not a production rollout.",
'{{ROBOT_1_URL}}': 'https://www.audi.com/en/press-releases/agile-robots-and-audi-to-transform-automotive-logistics-with-mobile-humanoids-supported-by-dassault-systemes-and-nvidia-18390',
'{{AUS_1_HEADLINE}}': "Angus Taylor Ramps Up Criticism of the Energy Minister Over the Snowy 2.0 Cost Blowout",
'{{AUS_1_SUMMARY}}': "ABC's 23 October federal politics blog leads with the Opposition Leader's attack on the cost overrun at the Snowy 2.0 pumped hydro project. Power costs are a live issue for any business running compressors and heavy equipment.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-23/federal-politics-live-blog-october-23/107297588',
'{{AUS_2_HEADLINE}}': "No Government Websites Hacked After Global Security Flaw Found, Federal Politics Blog Reports",
'{{AUS_2_SUMMARY}}': "ABC's 22 October blog reports federal agencies checked their systems after a global security flaw was disclosed and found no breach. A reminder to keep your own business software and email logins patched.",
'{{VIC_1_HEADLINE}}': "Suburbs Across Victoria Face Changes to Their Look as High-Rise Housing Becomes an Election Battleground",
'{{VIC_1_SUMMARY}}': "ABC, 23 October: Labor's activity-centre high-rise plans are a key test ahead of the 28 November state election, while the Coalition promises to scrap them and return planning powers to councils. More building activity would mean more demand for trades.",
'{{SCI_1_FLAG}}': '🌋 GEOLOGY',
'{{SCI_1_HEADLINE}}': "One of Earth's Most Powerful Supervolcanoes Is Refilling With Fresh Magma",
'{{SCI_1_SUMMARY}}': "ScienceDaily, 23 October: Kobe University researchers used underwater seismic surveys to find a large magma store that has built up under Japan's Kikai caldera since its massive eruption about 7,300 years ago. Findings are preliminary and say nothing about timing of any eruption.",
'{{INSIGHT_TITLE}}': 'Let AI Write Plain-English Aftercare Sheets: Cure Times and Care Instructions Customers Will Actually Read',
'{{INSIGHT_BODY}}': "After a coating or repair job, most customer callbacks come down to something simple: how long before it can get wet, what not to use, when to recoat. Give AI the product data sheet and ask it for a one-page plain-English handover with cure times, do's and don'ts, and who to call. Put your own details at the top and keep your standard version as a template. Check every time figure against the manufacturer's data sheet before it goes out, because AI can get numbers wrong. A clear sheet cuts phone calls and protects you if there's a dispute later.",
'{{FACT_1}}': "Audi's Ingolstadt plant relies on about one million parts picks a day, which is why it is testing humanoid robots to sequence them.",
'{{FACT_2}}': "A survey of 30,000 Americans found non-dairy creamer has overtaken sugar and milk as the biggest source of added calories in coffee.",
'{{FACT_3}}': "The brain's locus coeruleus was long thought to broadcast one uniform norepinephrine signal, but mouse research from the Allen Institute shows it sends targeted messages.",
'{{JOKE_SETUP}}': "Why did the awning installer stay so calm when the storm warning came through?",
'{{JOKE_PUNCHLINE}}': '"He always had the weather covered."',
'{{CLOSING_QUOTE}}': '"Rivers know this: there is no hurry. We shall get there some day."',
'{{CLOSING_ATTR}}': '— A. A. Milne',
'{{CLOSING_MESSAGE}}': "It's Saturday, and a wet weekend is on the way with a thunderstorm risk this afternoon. Get anything outdoors secured early, and use Sunday's rain to catch up on quotes and paperwork.",
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
