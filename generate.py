#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 16 October 2026',
'{{WEATHER_1}}': 'FRI 16 OCT · ☀️ Mostly sunny, 5% chance of rain · 8–23°C',
'{{WEATHER_2}}': 'SAT 17 OCT · ⛅ Partly cloudy · 12–25°C (unconfirmed)',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SUN 18 OCT · ☁️ Cloudy · 12–26°C (unconfirmed)',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'MON 19 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'TUE 20 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': "A mostly sunny, dry Friday with a top of about 23°C, from the Bureau of Meteorology Melbourne Airport page. UV is forecast to reach 8 (very high), so cover up outdoors. Saturday and Sunday come from a weather aggregator that doesn't show its update time, so treat them as a rough guide. Monday and Tuesday could not be confirmed, and Carrum Downs may differ slightly from these Melbourne figures.",
'{{WORLD_1_FLAG}}': '🚢 IRAN WAR · STRAIT OF HORMUZ',
'{{WORLD_1_HEADLINE}}': 'Two Ships Sink Near the Strait of Hormuz, With One Crew Member Killed',
'{{WORLD_1_SUMMARY}}': "Just Security's 15 October roundup, citing Reuters, says Singapore's maritime authority and the IMO reported both sinkings. All 21 crew on the other vessel were evacuated. I only saw excerpts, so the cause is not confirmed.",
'{{WORLD_1_URL}}': 'https://www.justsecurity.org/160924/early-edition-october-15-2026/',
'{{WORLD_2_FLAG}}': '🇺🇸 USA · IRAN',
'{{WORLD_2_HEADLINE}}': "US Military Draws Up Strike Plans That Could Use the 'Mother of All Bombs' on Iranian Targets",
'{{WORLD_2_SUMMARY}}': 'The same roundup, citing CNN and US officials, says the plans cover Iranian energy infrastructure and nuclear sites if Trump orders combat to resume. Trump also said at a Montana rally he is unsure who the US is negotiating with. Excerpt only, so details are limited.',
'{{WORLD_2_URL}}': 'https://www.justsecurity.org/160924/early-edition-october-15-2026/',
'{{ECON_1_FLAG}}': '✈️ FUEL · REGIONAL AIRLINES',
'{{ECON_1_HEADLINE}}': 'Rex Stops Flights to Port Macquarie and Orange From 25 October, Blaming Rising Fuel Costs',
'{{ECON_1_SUMMARY}}': "ABC's 15 October Broken Hill briefing reports the cuts. Another ABC briefing says a Bundaberg attraction's bookings fell 30 per cent in the September school holidays because of fuel costs. Briefing summaries only, but it shows fuel is hitting regional trade.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/news/2026-10-15/broken-hill-local-news-briefing/107268448',
'{{ECON_2_FLAG}}': '⛽ DIESEL · MELBOURNE',
'{{ECON_2_HEADLINE}}': 'Melbourne Diesel Sits Around 259 to 280 Cents a Litre Depending on Where You Look',
'{{ECON_2_SUMMARY}}': "Fuelradar's live feed (updated 15 October) showed diesel from 258.9c, while Fuel Daddy listed a 279.6c average and a cheapest price of 256.7c in Brunswick West. The trackers disagree, so check your fuel card or supplier before quoting fuel-heavy jobs.",
'{{TECH_1_FLAG}}': '⚖️ AI · POLICY',
'{{TECH_1_HEADLINE}}': 'OpenAI and Anthropic Back Some Binding AI Safety Rules at a UK Parliamentary Hearing',
'{{TECH_1_SUMMARY}}': 'An AI news roundup says OpenAI proposed mandatory incident reporting, while Google DeepMind and Meta did not endorse new legislation. I could not confirm the exact hearing date, and it is not a practical tool story, but rules like these usually flow through to the products you use.',
'{{TECH_1_URL}}': 'https://aiweekly.co/ai-news-today',
'{{TECH_2_FLAG}}': '🔍 AI · SAFETY TESTING',
'{{TECH_2_HEADLINE}}': 'Anthropic Gives Outside AI Evaluators Deeper Access to Its Internal Systems',
'{{TECH_2_SUMMARY}}': 'Benzinga reports the access lets outside evaluators publish findings Anthropic cannot block. Date not confirmed and only a headline and excerpt seen, so treat it as background rather than a tool you can use today.',
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS · SURGICAL',
'{{ROBOT_1_HEADLINE}}': 'Stryker Invests US$400M in CMR Surgical and Becomes Exclusive US Sales Agent for Its Versius Robots',
'{{ROBOT_1_SUMMARY}}': 'The Robot Report lists the deal as dated 15 October. I only saw the listing, and surgical robots are a long way from the workshop, but it shows serious money moving into physical robotics.',
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/robotics-news/',
'{{AUS_1_HEADLINE}}': 'Safe Work Australia Cuts Safe Exposure Limits for Hundreds of Dust Types From December',
'{{AUS_1_SUMMARY}}': "ABC's 15 October South West WA briefing reports the new rules. I could not confirm which substances or what the new limits are, so check Safe Work Australia directly. For a blasting and coatings shop this is worth chasing up before December.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-15/south-west-and-great-southern-wa-local-news-briefing/107269196',
'{{AUS_2_HEADLINE}}': "Failed Sunshine Coast Caravan Maker That Marketed Itself as Local Was Making Vans in China",
'{{AUS_2_SUMMARY}}': "ABC's 15 October Sunshine Coast briefing reports the revelation after the company collapsed. Only a briefing summary seen, but it is a reminder to check where your suppliers' products really come from.",
'{{VIC_1_HEADLINE}}': 'About 100 Bendigo Students March Against One Nation and Pauline Hanson',
'{{VIC_1_SUMMARY}}': "ABC's Central Victoria briefing of 15 October reports the Wednesday rally, six weeks out from the November state election. The same briefing says Labor has pledged more than $18.5 million for a Bendigo school building if it wins. Summary only.",
'{{SCI_1_FLAG}}': '🌾 PLANT SCIENCE',
'{{SCI_1_HEADLINE}}': 'Engineered Plant Immune Receptors May Offer a New Defence Against a Fungus Threatening Rice, Wheat and Barley',
'{{SCI_1_SUMMARY}}': 'ScienceDaily listed the story on 15 October. I only saw the teaser, so details on how well it works are thin.',
'{{INSIGHT_TITLE}}': 'Let AI Rank Your Overdue Invoices and Draft the Chase Messages',
'{{INSIGHT_BODY}}': "Chasing money is the job most tradies put off. Export your unpaid invoices list, paste it into an AI tool with no bank details, and ask it to rank them by amount and days overdue. Then have it draft a polite first reminder, a firmer second one and a final notice. You read each draft, fix the figures and send it yourself. In 20 minutes you have a full week of follow-ups done, and cash flow matters even more when diesel is near $2.80 a litre.",
'{{FACT_1}}': 'Vasuki indicus, a giant prehistoric snake from India, lived about 47 million years ago, according to ScienceDaily.',
'{{FACT_2}}': "The GBU-43/B 'mother of all bombs' weighs about 9,800 kg, making it the largest non-nuclear bomb in the US arsenal.",
'{{FACT_3}}': 'Australia cut the workplace limit for respirable crystalline silica from 0.1 to 0.05 mg/m³ in 2020, and now more dust limits are changing from December.',
'{{JOKE_SETUP}}': 'Why did the scaffolder never worry about late-paying customers?',
'{{JOKE_PUNCHLINE}}': '"Because he always took a deposit before he put anything up."',
'{{CLOSING_QUOTE}}': '"Action is the foundational key to all success."',
'{{CLOSING_ATTR}}': '— Pablo Picasso',
'{{CLOSING_MESSAGE}}': "It's Friday 16 October, mostly sunny and about 23°C, a good day to wrap up outdoor jobs before the weekend. Diesel is still near $2.60 to $2.80 a litre, so check your fuel costs on quotes. And with new dust limits coming in December, put a reminder in the diary to check them against your blasting setup.",
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
