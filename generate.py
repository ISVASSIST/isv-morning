#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 14 November 2026',
'{{WEATHER_1}}': 'SAT 14 NOV · 🌧️ Showers easing, cool, about 13-18°C, 1-5 mm possible',
'{{WEATHER_2}}': 'SUN 15 NOV · 🌦️ Drier, lower chance of a light shower, about 12-17°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'MON 16 NOV · 🌧️ Cloudy with showers and gusty southerlies, about 10-16°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'TUE 17 NOV · ⛅ Partly cloudy, mostly dry, about 9-19°C',
'{{WEATHER_5}}': 'WED 18 NOV · 🌤️ Partly cloudy and warmer, about 10-23°C',
'{{WEATHER_ALERT}}': "A damp Saturday, a drier Sunday and a showery, windy Monday, then it warms up and dries out from Tuesday. Wednesday looks like the best coating day of the week. These are Melbourne figures pulled from search summaries of WillyWeather, Meteored and other forecast sites, which didn't all agree. They're not a Carrum Downs forecast, so check BoM before booking outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 UKRAINE',
'{{WORLD_1_HEADLINE}}': 'Europe to Get a Seat at Next Week\'s Ukraine Peace Talks After Dublin Meeting',
'{{WORLD_1_SUMMARY}}': "Zelensky met US envoys Steve Witkoff and Jared Kushner for just under an hour at Baldonnel Aerodrome outside Dublin on 12 November. Zelensky and Kushner said a European delegation will join the next round of talks in Abu Dhabi next week, and Zelensky said Russia has accepted a prisoner exchange. Taoiseach Micheál Martin says it remains to be seen whether Russia is serious. I only saw search summaries.",
'{{WORLD_1_URL}}': 'https://www.rte.ie/news/ireland/2026/1113/1599056-eu-leaders-dublin/',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'Houthis Claim Attacks on Saudi Oil Sites as Tankers Are Hit Near Hormuz',
'{{WORLD_2_SUMMARY}}': "Yemen's Houthis say they targeted the Yanbu oil facility, an Aramco site in Riyadh and a pumping station on Saudi Arabia's East-West Pipeline on 12 November. The Saudi-led coalition says it shot down two drones. Separately, Iran's military said four tankers were hit by explosions in the Strait of Hormuz, and maritime security firms reported at least two ships struck. Saudi-side damage hasn't been confirmed.",
'{{WORLD_2_URL}}': 'https://www.democracynow.org/2026/11/13/headlines/houthis_claim_fresh_attacks_on_saudi_oil_facilities_including_east_west_pipeline',
'{{ECON_1_FLAG}}': '🛢️ OIL',
'{{ECON_1_HEADLINE}}': 'Brent Heads for a Second Weekly Fall as the IEA Sees the First Oil Surplus Since the Iran War',
'{{ECON_1_SUMMARY}}': "Brent traded around US$95-96 a barrel on Friday, after jumping 3.3% on Thursday on the Saudi attack claims. It was still on track for a 2.4% weekly fall, after a 16% plunge the week before. The IEA says global supply has overtaken demand for the first time since the Iran war began, and OPEC+ output rose by about 2 million barrels a day in October. That points to cheaper diesel ahead, if the Gulf stays calm.",
'{{ECON_1_URL}}': 'https://invezz.com/ng/news/2026/11/13/oil-price-today-brent-falls-below-dollar96-as-iea-sees-first-surplus-since-iran-war/',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Diesel Drops Below 275 Cents but Still Sits Well Above Wholesale',
'{{ECON_2_SUMMARY}}': "Fuelradar puts the national average diesel price at 274.3 cents a litre on 12 November, down 6.8 cents in a week, with unleaded at 228.9. AIP figures show Sydney wholesale diesel fell from 256.6 to 249.4 cents between Monday and Friday. Diesel at the pump is still about 17 cents above the wholesale price, so there's room for retailers to cut further. Shop around before filling the ute and the compressor tanks.",
'{{TECH_1_FLAG}}': '💻 TECH · OUTAGE',
'{{TECH_1_HEADLINE}}': 'Global Microsoft 365 Outage Knocks Out Outlook, Teams and Copilot',
'{{TECH_1_SUMMARY}}': "The outage began around 1pm US Eastern time on 12 November (early Friday in Melbourne) and hit email, Teams and Copilot worldwide. Microsoft says there's no sign of a cyberattack and has been restarting servers, and many users got a flood of delayed emails as services came back. Home Affairs Minister Tony Burke said Canberra activated a digital resilience agreement with Microsoft to get Australia priority. Microsoft hasn't given a root cause yet.",
'{{TECH_1_URL}}': 'https://www.abc.net.au/news/2026-11-13/microsoft-outage-affects-users-worldwide/107381050',
'{{TECH_2_FLAG}}': '🤖 AI · EMAIL',
'{{TECH_2_HEADLINE}}': 'Gemini Email Summaries and Drafting Switch On by Default for Google Workspace Business Accounts',
'{{TECH_2_SUMMARY}}': "Google is rolling out Gemini's thread summaries and 'Help me write' in Gmail to all Workspace users aged 18 and over, including business accounts, with both features on by default. The rollout started on 10 November and can take up to 15 days. Admins can switch Gemini off, but coverage notes the same switch also disables other smart features. If your business email runs on Google, expect to see these tools in the next week or two.",
'{{ROBOT_1_FLAG}}': '🦾 HUMANOID ROBOTS',
'{{ROBOT_1_HEADLINE}}': 'GXO Signs Up for as Many as 1,000 Apptronik Apollo Humanoids, if Trials Pay Off',
'{{ROBOT_1_SUMMARY}}': "Logistics giant GXO and Apptronik signed a non-binding letter of intent on 12 November to roll out up to 1,000 Apollo humanoid robots over four years. Expanded warehouse trials start in 2027 for picking, packing, sorting and moving totes, with first paid deployments targeted for late 2027 on a robots-as-a-service model. Each robot has to hit agreed performance targets first. Reports cite a cost target of about US$15 an hour.",
'{{ROBOT_1_URL}}': 'https://globenewswire.com/news-release/2026/11/12/3401413/0/en/gxo-and-apptronik-expand-partnership-to-scale-humanoid-deployment.html',
'{{AUS_1_HEADLINE}}': 'Canberra Rethinks Its Backpacker Visa Crackdown After Farm and Hospitality Backlash',
'{{AUS_1_SUMMARY}}': "Home Affairs Minister Tony Burke says he's open to changes to the working holiday visa overhaul, though total numbers can't move and a resolution is 'very close'. Reports expect a big lift in third-year visa places, possibly to 25,000 from the 5,000 announced in September, and a delay to the planned ballot, possibly with tougher regional work rules. The National Farmers' Federation had warned the cuts risked food security. Nothing's final yet.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-13/backpacker-working-holiday-visa-immigration-uk-rethink/107381884',
'{{AUS_2_HEADLINE}}': 'ASX Slips 0.7% as the Nvidia Shock Spreads and Bank Bosses Face MPs',
'{{AUS_2_SUMMARY}}': "The ASX 200 closed down 0.7% at 9,082 points on Friday after Nvidia shares fell on Jensen Huang's exit, with only utilities and energy finishing higher. NAB's Andrew Irvine and CBA's Matt Comyn faced a parliamentary committee about mortgages and the economy. CBA figures show a record fall in investor lending and the weakest monthly wage growth this year. Cotality says home values in the major cities are down 8.1% in seven months.",
'{{VIC_1_HEADLINE}}': 'Labor Promises a Train Every 10 Minutes on Five Melbourne Lines and a $30 Weekly Fare Cap',
'{{VIC_1_SUMMARY}}': "Premier Ben Carroll says a $100 million plan would run trains every 10 minutes from 7am to 7pm on weekdays, and from 9:30am on weekends, on the Mernda, Hurstbridge, Belgrave, Lilydale and Glen Waverley lines. Labor also promised to cap public transport fares at $30 a week, which the ABC says the Coalition hasn't matched. That follows Thursday's $420 million regional rail pledge. Victorians vote on 28 November.",
'{{SCI_1_FLAG}}': '🧠 NEUROSCIENCE',
'{{SCI_1_HEADLINE}}': 'Scientists Publish the Most Detailed Map Yet of the Brain\'s Movement and Habit Centre',
'{{SCI_1_SUMMARY}}': "NIH BRAIN Initiative researchers released a collection of about 27 papers in Cell Press journals on 12 November mapping the basal ganglia, the deep brain structures that control deliberate movement, learning and focus. The atlas catalogues more than 25 million cells across humans, mice, marmosets and monkeys, and names 61 cell groups. The region is central to Parkinson's and Huntington's disease. It's a research resource, not a treatment.",
'{{INSIGHT_TITLE}}': 'When Outlook and Teams Go Down, Have AI Write Your One-Page Outage Plan Now',
'{{INSIGHT_BODY}}': "Friday's global Microsoft outage was a reminder that your email, calendar and job notes can vanish for hours without warning. Ask an AI tool to draft a short outage plan: which customers to phone first, where a printed copy of this week's jobs and contacts lives, which personal phone or text number to use instead, and who tells the crew. Keep it on the fridge in the workshop and in the ute. It takes ten minutes, and it means the next outage costs you a coffee break instead of a day's work.",
'{{FACT_1}}': "In a Science study from the University of Tübingen, carrion crows judged the direction of moving dots in about 235 milliseconds on average, roughly twice as fast as humans and monkeys in earlier studies.",
'{{FACT_2}}': "The new basal ganglia brain atlas's 21 million human cells came from just six donated brains.",
'{{FACT_3}}': "Logistics firm GXO has run more than 45 humanoid robot pilots with several vendors, including Apptronik, Agility Robotics and Reflex Robotics.",
'{{JOKE_SETUP}}': "Why did the painter refuse to start an outdoor job on a drizzly Saturday?",
'{{JOKE_PUNCHLINE}}': '"He knew it would only end in tears, and runs."',
'{{CLOSING_QUOTE}}': '"There is no such thing as bad weather, only different kinds of good weather."',
'{{CLOSING_ATTR}}': '— John Ruskin (attributed)',
'{{CLOSING_MESSAGE}}': "It's a showery Saturday, so it's a good day for paperwork, a backup plan for the next Microsoft outage, and a cuppa. Diesel is finally easing, and the drier, warmer days from Tuesday should make for a solid working week. Enjoy the weekend.",
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
