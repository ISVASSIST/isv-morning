#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 24 November 2026',
'{{WEATHER_1}}': 'TUE 24 NOV · 🌤️ Cool and partly cloudy, about 10-18°C, only a slight chance of an early shower',
'{{WEATHER_2}}': 'WED 25 NOV · ☀️ Mostly sunny and warmer, about 9-25°C, dry',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'THU 26 NOV · ⛅ Partly cloudy, about 13-25°C, an afternoon storm is possible',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'FRI 27 NOV · 🌦️ Warm, high 20s, chance of a shower',
'{{WEATHER_5}}': 'SAT 28 NOV · ❓ Election day, too far out for a firm call, check the BoM later in the week',
'{{WEATHER_ALERT}}': "Today is the cool one. The BoM has Carrum Downs at about 18°C, partly cloudy, with only a 10% chance of rain, so it's a dry day if you don't mind the chill. Wednesday is the pick of the week: mostly sunny, dry and warming to about 25°C, with a cold start near 9°C, so watch dew point and steel temperature first thing before you coat anything. Thursday stays in the mid-20s, but AccuWeather flags an afternoon thunderstorm while other sites only show a stray shower. Friday gets warmer again, high 20s, with a chance of showers. The forecast sites disagree by a few degrees from Thursday on, and none reach Saturday with confidence, so check the BoM forecast before you book outdoor work late in the week.",
'{{WORLD_1_FLAG}}': '🇱🇾 LIBYA · UKRAINE WAR',
'{{WORLD_1_HEADLINE}}': 'Ukrainian Sea Drones Hit a Russian Warship in Libya',
'{{WORLD_1_SUMMARY}}': "A Russian navy corvette, the Merkury, was hit by suspected Ukrainian sea drones at the Benghazi naval base in Libya. Libyan military officials say two drones struck the ship and started a fire, and four others were shot down. President Zelensky says seven sea drones were used, that the ship sank, and that a helicopter on board was destroyed. Satellite images appear to show the vessel submerged. The ship had stopped in Benghazi to refuel before heading home to Russia. Libya's eastern government says it's investigating jointly with Russia.",
'{{WORLD_1_URL}}': 'https://www.npr.org/2026/11/23/g-s1-155017/ukraine-attack-russian-warship-libya',
'{{WORLD_2_FLAG}}': '🛢️ MIDDLE EAST · SHIPPING',
'{{WORLD_2_HEADLINE}}': 'Attacks on Ships Near Hormuz Hit Their Highest Level of the Iran War',
'{{WORLD_2_SUMMARY}}': "CNN reports that attacks on ships in and around the Strait of Hormuz are now at their highest level since the conflict with Iran began in February. Three more tankers were hit over Friday and Saturday. The Captain Leon caught fire after a hit at the bow, and two Hong Kong-flagged tankers, the Torkel and the Arina, were struck near Khasab in Oman less than an hour apart. Maritime trade site Splash247 says that makes seven tankers hit since 16 November. Iran claims the ships hit naval mines, but that hasn't been verified. Because so much of the world's oil goes through Hormuz, this is the main thing that could stop fuel prices falling.",
'{{WORLD_2_URL}}': 'https://www.cnn.com/2026/11/22/middleeast/hormuz-attacks-highest-levels-iran-war-intl',
'{{ECON_1_FLAG}}': '📉 ECONOMY',
'{{ECON_1_HEADLINE}}': 'Chalmers Warns Growth Will Be Cut as Business Activity Shrinks at Its Fastest Pace in Five Years',
'{{ECON_1_SUMMARY}}': "Treasurer Jim Chalmers told Parliament that growth will come in below the forecast from six months ago, and warned that \"things might get a bit harder\". Reports say Treasury could put growth well below 2% for the next two years, with unemployment, already at 4.9%, expected to go above 5%. He said neither Treasury nor the Reserve Bank is forecasting a recession. On the same day, the S&P Global flash PMI fell to 46.1 in November, from 48.2 in October. That's the sharpest drop in private-sector activity since August 2021, and new orders fell for the first time in five months. The official numbers come in the mid-year budget update next month.",
'{{ECON_1_URL}}': 'https://www.bloomberg.com/news/articles/2026-11-23/australia-lower-economy-estimate-budget-update-inflation-unemployment-treasurer-jim-chalmers',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Wholesale Diesel in Melbourne Is Down to About $2.42 a Litre',
'{{ECON_2_SUMMARY}}': "The Australian Institute of Petroleum's terminal gate price for diesel in Melbourne was 242.3 cents a litre on Monday 23 November, including GST. That's the wholesale price, and pump prices usually trail it by a few days. The ACCC's latest figures had average pump diesel across the five biggest cities at 258.3 cents a litre on 18 November, down 8.1 cents on the week. So there's still room for diesel at the bowser to come down this week. The risk is Hormuz, where tanker attacks hit a new high over the weekend. If global oil jumps, the fall could stop quickly, so it's a reasonable week to fill the work vehicles and any bulk tanks.",
'{{TECH_1_FLAG}}': '💻 TECH · NVIDIA',
'{{TECH_1_HEADLINE}}': 'Nvidia Brings Back Jensen Huang as CEO, and Its Shares Jump',
'{{TECH_1_SUMMARY}}': "Nvidia's board has voted unanimously to reinstate Jensen Huang as chief executive, 11 days after he resigned over revelations about his personal life. Only days earlier, interim CEO Colette Kress had said he wouldn't return. Nvidia's filing says the decision followed input from \"senior levels\" of the US government, and President Trump says he convinced the board. The company's own investigation into Huang will continue, and it's hiring a new chief compliance officer. Nvidia shares jumped sharply on the news, after falling about 14% on Friday in Wall Street's worst week for tech stocks in more than six years. Nvidia makes most of the chips that run AI, so its swings move the whole AI market.",
'{{TECH_1_URL}}': 'https://www.cbsnews.com/news/nvidia-reinstates-jensen-huang-ceo/',
'{{TECH_2_FLAG}}': '🧰 AI · OFFICE TOOLS',
'{{TECH_2_HEADLINE}}': "Microsoft Rolls Out OpenAI's Newest Model in Copilot Worldwide",
'{{TECH_2_SUMMARY}}': "Microsoft is rolling out OpenAI's GPT-6.2 Sol to eligible Copilot users worldwide, including in Copilot Chat and inside Word, Excel and PowerPoint. If your business pays for Microsoft 365 Copilot, you should start seeing it without doing anything. Microsoft says the model only works with files and emails you already have permission to open. In practical terms, you can ask Excel to pull a job cost summary out of a messy spreadsheet, or ask Word to turn site notes into a tidy report. Rollouts happen in stages, so it may take a few days to reach every account. If you don't have Copilot, there's no need to sign up just for this.",
'{{ROBOT_1_FLAG}}': '🤖 HUMANOID ROBOTS · CHINA',
'{{ROBOT_1_HEADLINE}}': 'Ant Group Leads $100 Million Round in 16-Month-Old Robot Maker Simplexity',
'{{ROBOT_1_SUMMARY}}': "Hangzhou-based Simplexity Robotics has raised US$100 million in a round led by Ant Group, valuing the company at about US$1.6 billion, according to TechNode and Bloomberg. Simplexity was founded in July 2025 by former Li Auto executives and builds general-purpose robots. Its latest model, a wheeled humanoid called iX, has been shown making and delivering drinks, fetching objects and guiding visitors. Reports differ on who else joined the round, but filings name Alibaba, Tencent and HongShan. It's reportedly Ant Group's twelfth humanoid robot investment since early 2025. It's another sign of how fast Chinese money is flowing into robots that can work alongside people.",
'{{ROBOT_1_URL}}': 'https://technode.com/2026/11/23/ant-group-leads-100-million-round-in-humanoid-startup-simplexity-robotics/',
'{{AUS_1_HEADLINE}}': "Parliament's Last Sitting Week of the Year Begins With Key Laws Still Unpassed",
'{{AUS_1_SUMMARY}}': "Federal Parliament is sitting from Monday to Thursday this week, the last sitting week of 2026, and the government has four days to pass several major bills. They include a big tax reform bill, the European Free Trade Agreement, and the Digital Duty of Care online safety bill. The Coalition opposes the online safety bill, so the government needs the Greens to pass it in the Senate. Communications Minister Anika Wells has said low-risk small business websites will be excluded from the new duty of care. Negotiations are still going, and any bill that doesn't pass this week will have to wait until next year.",
'{{AUS_1_URL}}': 'https://www.canberratimes.com.au/story/9396092/crunch-time-for-key-laws-as-sun-sets-on-political-year/',
'{{AUS_2_HEADLINE}}': 'ASX Falls for an Eighth Straight Day After Wall Street Sell-Off',
'{{AUS_2_SUMMARY}}': "The ASX 200 closed lower for the eighth session in a row on Monday, down 0.26% to 8,570.6 points. It followed Friday's heavy falls on Wall Street, where the Nasdaq lost about 10% for the week and the S&P 500 lost 8.6%, their worst weeks in more than six years, on worries about AI spending. Miners held up better, with materials stocks up about 1.8%, and gold stocks ended their own losing run. US futures pointed to a rebound overnight. If you have super or shares, it's a rough patch, but one bad week doesn't change a long-term plan.",
'{{VIC_1_HEADLINE}}': 'Victorian Labor Braces for a Heavy Defeat as Albanese Keeps His Distance',
'{{VIC_1_SUMMARY}}': "With the state election on Saturday 28 November, the ABC reports Victorian Labor is bracing for a big loss, and federal Labor figures are keen to avoid any fallout. Prime Minister Anthony Albanese has largely stayed away from the campaign. Experts expect the Coalition, led by Jess Wilson, to win a majority, possibly on a scale close to Jeff Kennett's 1992 win. Recent polling in the Australian Financial Review had the Coalition on 31% of the primary vote, Labor on 23%, One Nation on 22% and the Greens on 15%. Premier Ben Carroll is spending the final week campaigning at early voting centres. Pre-poll is open all week if you'd rather vote before Saturday.",
'{{SCI_1_FLAG}}': '🌏 EARTH SCIENCE',
'{{SCI_1_HEADLINE}}': 'Scientists Explain How a Big Quake Can Set Off Small Ones Thousands of Kilometres Away',
'{{SCI_1_SUMMARY}}': "Big earthquakes sometimes trigger smaller ones on faults thousands of kilometres away, and it's never been clear why the passing waves are strong enough. Engineers Chao Huang and Jun Yang at the University of Hong Kong think they've found the answer. Their simulations, published in Science Advances, show the waves squeeze the crushed rock inside a fault and push up the water pressure in it. In their model, that pressure reached about 1.7 MPa, roughly 10 times the direct push from the waves, which weakens the fault enough to slip. The water drains slowly, so the fault can stay weak after the shaking stops. It also helps explain why rolling Rayleigh waves trigger quakes better than side-to-side Love waves. The results come from computer models, so lab tests on real fault rock are still needed. Phys.org covered it on 23 November.",
'{{INSIGHT_TITLE}}': 'Before the Slowdown Bites, Ask AI How Much of Your Work Comes From Your Top Three Customers',
'{{INSIGHT_BODY}}': "Yesterday's figures showed business activity shrinking at its fastest pace in five years, so now is a good time to check how exposed you are. Export the last 12 months of invoices from Xero or MYOB as a spreadsheet, take out bank details and anything private, and upload it to ChatGPT, Claude or Copilot. Ask it to group revenue by customer and by industry, and show what share your top three customers make up. If one or two clients bring in more than about a third of your work, or most of it comes from a single sector like construction or manufacturing, you're more exposed if that sector slows. Then ask the AI to list the customers who used you once or twice and haven't been back, and draft a short, friendly check-in for each. It takes about 20 minutes and gives you a clear list of where to look for work before things get quiet.",
'{{FACT_1}}': "Victoria was one of the first places in the world to use the secret ballot, at its 1856 election. It caught on so widely overseas that it's still sometimes called the \"Australian ballot\".",
'{{FACT_2}}': "The 2002 magnitude 7.9 Denali earthquake in Alaska set off swarms of small earthquakes at Yellowstone, more than 3,000 kilometres away.",
'{{FACT_3}}': "Love waves, the side-to-side earthquake waves, aren't named after romance. They're named after British mathematician Augustus Love, who described them in 1911.",
'{{JOKE_SETUP}}': "Why wasn't the concreter worried when the share market fell eight days in a row?",
'{{JOKE_PUNCHLINE}}': "He knows that once things stop moving, they usually set firm.",
'{{CLOSING_QUOTE}}': '"Smooth seas do not make skillful sailors."',
'{{CLOSING_ATTR}}': '— African proverb',
'{{CLOSING_MESSAGE}}': "It's Tuesday, a cool, dry 18°C day, and tomorrow looks like the best outdoor day of the week before storms become a chance on Thursday. The economic news is gloomy, with growth forecasts being cut and the ASX down eight days straight, but wholesale diesel is still falling. It's a good week to fill the tanks and check who your work is coming from. Pre-poll is open all week if you want Saturday free. Have a good day.",
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
