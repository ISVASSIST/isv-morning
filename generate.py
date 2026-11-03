#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 04 November 2026',
'{{WEATHER_1}}': 'WED 4 NOV · 🌧️ Rain, about 5 to 15mm · high around 18-21°C',
'{{WEATHER_2}}': 'THU 5 NOV · 🌦️ Morning shower, easing',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'FRI 6 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SAT 7 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_5}}': 'SUN 8 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Today looks like the wettest day of the week, with third-party sites tipping roughly 5 to 15mm across greater Melbourne and some saying afternoon thunderstorms. Thursday may keep a morning shower before it clears. Those are greater Melbourne figures from AccuWeather, Weather Underground, The Weather Network and WillyWeather, not a Carrum Downs BoM page, and I couldn't find Friday to Sunday at all. Check BoM before planning outdoor coatings work.",
'{{WORLD_1_FLAG}}': '🌍 QATAR · IRAN',
'{{WORLD_1_HEADLINE}}': "Qatar Says It Remains 'Hopeful' of a US-Iran Deal as Draft Proposal Circulates",
'{{WORLD_1_SUMMARY}}': "Al Arabiya reports Qatar is still hopeful after the Doha talks, with a draft proposal said to link reopening the Strait of Hormuz, releasing frozen Iranian assets and restarting nuclear talks. Reports conflict on whether Iran's negotiators have left Doha and nothing is final, so check the source for updates.",
'{{WORLD_1_URL}}': 'https://english.alarabiya.net/News/gulf/2026/11/03/qatar-says-remains-hopeful-of-a-usiran-deal',
'{{WORLD_2_FLAG}}': '🌍 GULF',
'{{WORLD_2_HEADLINE}}': "Arab States Warn Iran of Individual and Collective Retaliation Over Attacks, WSJ Reports",
'{{WORLD_2_SUMMARY}}': "Iran International relays a Wall Street Journal report that Gulf states have warned Tehran of retaliation if attacks on them continue. Separate coverage says Trump has not decided on any strike after the US midterms. I've only seen the headline and search summaries, not the full article.",
'{{WORLD_2_URL}}': 'https://www.iranintl.com/en/202611020302',
'{{ECON_1_FLAG}}': '🏦 RBA',
'{{ECON_1_HEADLINE}}': 'RBA Lifts Cash Rate to 4.85%, an 18-Year High, With the Board Split 6-3',
'{{ECON_1_SUMMARY}}': "The Reserve Bank raised rates 25 basis points on Cup Day, the fifth rise this year, citing inflation, the Middle East war and oil prices. Three members wanted to hold. Governor Bullock reportedly said two more rises in the first half of next year can't be ruled out, while Standard Chartered reads the split vote as a sign the RBA may be done. If you carry variable finance or an overdraft, check your repayments.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/news/2026-11-03/rba-lifts-interest-rates-november-2026-highest-rate-in-18-years/107340050',
'{{ECON_2_FLAG}}': '🛢️ OIL · FUEL',
'{{ECON_2_HEADLINE}}': 'Brent Slides Back Near US$104 on Iran Peace Hopes, but Pump Relief Lags',
'{{ECON_2_SUMMARY}}': "Brent closed Monday around US$104.77 after a fall of about 7.6%, and a live feed showed roughly US$103.50 on Tuesday, though sources differ by a dollar or two. The last local figure I could find was 91 unleaded averaging about 237c/L in late October, so don't expect cheaper diesel at the bowser for a week or two. I couldn't confirm a current Australian price.",
'{{TECH_1_FLAG}}': '🤖 AI · CLAUDE',
'{{TECH_1_HEADLINE}}': "Anthropic Opens 'Message Threads' Beta to Cut Wait Times in Long AI Agent Sessions",
'{{TECH_1_SUMMARY}}': "Agents send the full conversation once and then only new messages, which Anthropic says cuts the wait before Claude replies by about 35% on very long sessions. It's a developer API feature rather than something you'd use directly, but it's the kind of plumbing that makes AI assistants cheaper and quicker. Reported 2 November.",
'{{TECH_1_URL}}': 'https://thenextweb.com/news/anthropic-message-threads-beta-claude-api-agents',
'{{TECH_2_FLAG}}': '🤖 AI · CODING',
'{{TECH_2_HEADLINE}}': "Android Studio Now Lets Developers Plug In More Than 40 Third-Party AI Coding Agents",
'{{TECH_2_SUMMARY}}': "Google's 'Bring Your Own Agent' feature in the stable Android Studio works over an open protocol, so developers can switch between agents such as Claude and Codex. Note this was announced on 28 October and is still being covered in this week's roundups, so it's slightly older than 48 hours. Of limited direct use to a trades business, but it shows tools becoming interchangeable.",
'{{ROBOT_1_FLAG}}': '🤖 AGILITY',
'{{ROBOT_1_HEADLINE}}': "Agility Robotics Reportedly Set to List on Nasdaq, With Trading Expected 5 November",
'{{ROBOT_1_SUMMARY}}': "A KuCoin news flash says the maker of the Digit warehouse humanoid is listing through a US$46.5 million merger deal and that its robots are already moving totes in customer warehouses. This is a single crypto-news source, so verify it with Agility or a financial outlet before relying on the numbers.",
'{{ROBOT_1_URL}}': 'https://www.kucoin.com/news/flash/agility-robotics-to-list-on-nasdaq-with-46-5m-merger-deal',
'{{AUS_1_HEADLINE}}': "Albanese Pushes Australia's UN Security Council Bid in CHOGM Speech in Antigua",
'{{AUS_1_SUMMARY}}': "The Prime Minister gave a wide-ranging speech aimed at progressing Australia's bid for a temporary Security Council seat from 2029. The ABC's 3 November live blog also covered the RBA decision. Based on search summaries of the live blog.",
'{{AUS_1_URL}}': 'https://abc.net.au/news/2026-11-03/federal-politics-live-blog-albanese-interest-rates-nov-3/107338214',
'{{AUS_2_HEADLINE}}': "Matt Canavan Confirms He Will Contest Capricornia, Setting Up a Clash With One Nation",
'{{AUS_2_SUMMARY}}': "Canavan says he will seek the Queensland lower house seat, which sets up a potential contest with One Nation's James Ashby. This is from a 2 November report as summarised in search results, so I haven't read the full story.",
'{{VIC_1_HEADLINE}}': "Point of Law Wins the 2026 Melbourne Cup, Ciaron Maher Trains the Trifecta",
'{{VIC_1_SUMMARY}}': "The favourite, sold by King Charles III in July, won in just its sixth start with Ethan Brown aboard, his first Cup win. Maher saddled seven runners and took first, second and third, reportedly a first for a trainer. Per the ABC, 3 November.",
'{{SCI_1_FLAG}}': '🕳️ BLACK HOLES',
'{{SCI_1_HEADLINE}}': "Scientists Find a Loophole That Could Let Fast-Spinning Black Holes Split in Two",
'{{SCI_1_SUMMARY}}': "A theoretical study in Physical Review D suggests the physics doesn't entirely rule out a fast-spinning black hole dividing in two, though the conditions would be extreme. It's theory, not an observation. ScienceDaily, 1 November.",
'{{INSIGHT_TITLE}}': "Ask AI to Turn Messy Supplier Emails Into a One-Page Order Summary",
'{{INSIGHT_BODY}}': "Quantities, delivery dates and price changes get buried in long email chains, and that is where wrong orders and surprise freight charges come from. Paste the thread into an AI tool and ask for a one-page table of items, quantities, prices, delivery dates and anything still unconfirmed. Check it against the original quote before you place the order, and leave out account numbers and card details. It takes a couple of minutes and catches the small mistakes that eat margin.",
'{{FACT_1}}': "The RBA's rate rise on 3 November was a 6-3 decision, the cash rate is now 4.85%, and the ABC calls it the highest level in 18 years.",
'{{FACT_2}}': "Ciaron Maher's trifecta in the 2026 Melbourne Cup is reported as a first for a trainer, from seven runners in a A$10 million race.",
'{{FACT_3}}': "A 3 November market report projects the humanoid robot actuator market will grow to US$470 million in 2026, up from US$280 million in 2025.",
'{{JOKE_SETUP}}': "Why did the roofer take Wednesday off?",
'{{JOKE_PUNCHLINE}}': '"The forecast said rain, and he likes to be on top of things, not underneath them."',
'{{CLOSING_QUOTE}}': '"No great thing is created suddenly."',
'{{CLOSING_ATTR}}': '— Epictetus',
'{{CLOSING_MESSAGE}}': "Wednesday looks like the wet one, so push any outdoor coating or blasting prep to a drier day and use the time for quotes. With the RBA lifting rates again yesterday, it's a good morning to check your finance repayments.",
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
