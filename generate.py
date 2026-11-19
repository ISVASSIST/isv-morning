#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Friday, 20 November 2026',
'{{WEATHER_1}}': 'FRI 20 NOV · ⛈️ Showers, then afternoon storms, possibly severe, about 24-26°C',
'{{WEATHER_2}}': 'SAT 21 NOV · 🌤️ Clearing and mostly fine, low rain chance',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SUN 22 NOV · 🌦️ Hot, near 29-30°C, then a cold front with showers and a possible storm',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'MON 23 NOV · 🌧️ Cooler and showery, about 20°C, breezy',
'{{WEATHER_5}}': 'TUE 24 NOV · 🌦️ Morning showers clearing, cool, about 16-18°C',
'{{WEATHER_ALERT}}': "The BoM says a thunderstorm is likely in Melbourne today and may be severe, with damaging winds, large hail and heavy rain that could cause flash flooding. Showers build through the morning and storms are most likely from mid-afternoon into the evening, so the trip home could be messy. The Melbourne Airport forecast gives a 90% chance of rain and 3-20mm. Keep coating work under cover today, tie down anything loose in the yard, and don't leave freshly coated steel outside overnight. Saturday is the dry day. Sunday turns hot before a cold front brings showers and a cooler, wetter Monday and Tuesday. Check the BoM warnings page before you head out.",
'{{WORLD_1_FLAG}}': '🌏 CHINA · APEC',
'{{WORLD_1_HEADLINE}}': 'Trump, Xi and Putin Hold Their First Three-Way Talks in Shenzhen',
'{{WORLD_1_SUMMARY}}': "Donald Trump, Xi Jinping and Vladimir Putin met together on Thursday at the APEC summit in Shenzhen, the first time the three have met as a trio. Al Jazeera reports the closed-door talks lasted about 55 minutes, after each leader also held separate one-on-one meetings. Putin's opening remarks pointed to the war in Ukraine as the main focus, and Xi later called the meeting \"positive, constructive and fruitful\". No agreement or joint statement has been released, so it's not yet clear what, if anything, was decided. Trump is heading home and is due to brief the press today.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/11/19/trump-meets-putin-and-xi-ahead-of-us-russia-china-trilateral-talks',
'{{WORLD_2_FLAG}}': '🇹🇷 COP31 · CLIMATE',
'{{WORLD_2_HEADLINE}}': 'COP31 Draft Drops Fossil Fuel Wording on the Last Scheduled Day',
'{{WORLD_2_SUMMARY}}': "The climate talks in Antalya, Türkiye, are due to finish today, but the latest draft of the main political agreement has dropped explicit references to moving away from fossil fuels. Australia's Chris Bowen, who is chairing the negotiations, defended the draft and said talks would continue overnight until there is consensus. Critics, including Power Shift Africa, say the text has gone backwards from earlier in the week. Around 21 agenda items were still unresolved midweek, and observers expect the conference to run at least one extra night.",
'{{WORLD_2_URL}}': 'https://news.un.org/en/story/2026/11/1168839',
'{{ECON_1_FLAG}}': '📉 JOBS',
'{{ECON_1_HEADLINE}}': 'Unemployment Jumps to 4.9%, the Highest in About Five Years',
'{{ECON_1_SUMMARY}}': "The ABS says the unemployment rate rose to 4.9% in October, its third straight monthly rise and the highest since about October 2021. Employment fell by 43,500 people, and the number of unemployed rose by 17,800 to 753,700. Youth unemployment rose to 11.3%. The result was weaker than most economists expected, and several now say the RBA is likely to keep rates on hold until at least February. For trades, a softer jobs market usually means customers delay discretionary work, but it can also make good workers easier to find.",
'{{ECON_1_URL}}': 'https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release',
'{{ECON_2_FLAG}}': '⚠️ RECESSION RISK',
'{{ECON_2_HEADLINE}}': 'Economists Warn Australia May Be Heading Into Recession',
'{{ECON_2_SUMMARY}}': "After Thursday's jobs figures, leading economists told the ABC that Australia is either close to a recession or may already be in one. Westpac expects unemployment to peak at 5.2%. Opposition Leader Angus Taylor called it an \"economic crisis\", while Employment Minister Amanda Rishworth says the economy remains resilient. Fuel is still a big cost: the ACCC's latest weekly report (to 11 November) had big-city diesel at about 266 cents a litre, around 90 cents above February, although wholesale prices are still falling. Keep a close eye on debtor days and quote pipelines over summer.",
'{{TECH_1_FLAG}}': '🧾 AI · ACCOUNTING',
'{{TECH_1_HEADLINE}}': 'OpenAI Launches ChatGPT for Accounting, Linking Xero, QuickBooks and FreshBooks',
'{{TECH_1_SUMMARY}}': "OpenAI has launched ChatGPT for Accounting, a plugin that connects ChatGPT to accounting software including Xero, QuickBooks, FreshBooks, BILL and NetSuite. Business owners can ask plain-English questions about their own books, such as which invoices are overdue or which expenses are missing receipts. FreshBooks announced on Thursday that its connection is read-only, so ChatGPT can look at the data but can't change it or send invoices. Reports say the Xero connection is also read-only for now. OpenAI hasn't published pricing, and ChatGPT Business users can install it without admin approval.",
'{{TECH_1_URL}}': 'https://www.globenewswire.com/news-release/2026/11/19/3406729/0/en/freshbooks-partners-with-openai-to-release-chatgpt-for-accounting-bringing-ai-innovation-to-small-business-owners.html',
'{{TECH_2_FLAG}}': '🤖 AI · MODELS',
'{{TECH_2_HEADLINE}}': 'Google Releases Gemini 4 Neon, a Cheaper Mid-Tier AI Model',
'{{TECH_2_SUMMARY}}': "Google has released Gemini 4 Neon, a mid-tier model in its Gemini 4 family, priced at US$3 per million input tokens and US$15 per million output tokens for developers. It can work with very long documents (a 1 million token context) and has four \"thinking\" levels, so users can trade speed for more careful answers. It's rolling out in the Gemini app for paid subscribers and in Google's business products. Google says it's cheaper per task than its bigger Carbon model, but one independent test found it can cost more at the highest thinking setting.",
'{{ROBOT_1_FLAG}}': '🦾 HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': "Boston Dynamics' Atlas Humanoid Heads Into Chip Factories",
'{{ROBOT_1_SUMMARY}}': "Boston Dynamics says chipmaker GlobalFoundries will start testing its Atlas humanoid robot in its chip plants from early 2027. GlobalFoundries is the first customer outside the car industry in Atlas's early adopter program. No specific task, plant or number of robots has been named yet. The two companies will work out which chip-making jobs a humanoid can actually do. GlobalFoundries is also rolling out Boston Dynamics' Spot robot dog for inspections at plants in the US, Germany and Singapore, after using it in Vermont for more than four years.",
'{{ROBOT_1_URL}}': 'https://www.techtimes.com/articles/331062/20261119/globalfoundries-test-boston-dynamics-atlas-humanoid-robot-chip-fabs-no-task-named.htm',
'{{AUS_1_HEADLINE}}': 'Albanese Meets Xi Today With the 55% Beef Tariff on the Table',
'{{AUS_1_SUMMARY}}': "Anthony Albanese is due to meet Xi Jinping in Shenzhen today, on the sidelines of APEC, before talks with Premier Li Qiang. He's expected to raise China's 55% tariff on Australian beef, which kicked in after Chinese importers filled this year's 205,000-tonne quota in June. The Australian Meat Industry Council estimates the tariff could cut beef exports to China by about $1 billion a year. The meeting is likely to be overshadowed by Thursday's Trump-Xi-Putin talks, and no outcome has been announced yet.",
'{{AUS_1_URL}}': 'https://www.therural.com.au/story/9395015/tough-act-to-follow-pms-xi-meeting-overshadowed/',
'{{AUS_2_HEADLINE}}': 'Cheap New EVs Are Pushing Down Used Petrol and Diesel Values',
'{{AUS_2_SUMMARY}}': "The ABC reports that low-cost new cars, especially Chinese-built EVs, are putting pressure on used petrol and diesel car prices. Carma's September report found used car prices were 6.5% lower than a year earlier, and listings of Chinese-brand cars rose 58% in a year. Industry voices say the hit depends on whether buyers see a cheap EV as good as a petrol car. If you're thinking about trading in a work vehicle, check current listings before you set a price.",
'{{VIC_1_HEADLINE}}': 'Big Build Royal Commission Refers Two Witnesses to Police',
'{{VIC_1_SUMMARY}}': "The royal commission into crime and corruption on Victoria's Big Build construction projects has referred two witnesses to Victoria Police for possible prosecution, over allegations they failed to answer its questions. Counsel assisting Chris Carr SC didn't name them, though the ABC has reported who they are. Under the Inquiries Act, anyone who obstructs the commission can be referred to police. The next block of hearings runs from 30 November to 11 December, and the inquiry has become a big issue in the state election campaign.",
'{{SCI_1_FLAG}}': '🔥 ENERGY',
'{{SCI_1_HEADLINE}}': 'Salt in the Air Decides Whether a Hydrogen Flame Can Be Seen',
'{{SCI_1_SUMMARY}}': "Hydrogen flames are almost invisible, which is a safety problem for hydrogen in homes and industry. Researchers from Adelaide University, UNSW and Gas Infrastructure Research Australia found that the orange glow they sometimes show comes mainly from sodium in the air, often sea salt blown inland. In outdoor tests near Adelaide, the sodium signal varied by more than 28 times between the lowest and highest readings with the burner unchanged. The study, in Next Energy, says safety systems should rely on UV, infrared or heat sensors rather than flame colour.",
'{{INSIGHT_TITLE}}': 'Before You Sell or Trade the Old Ute, Ask AI to Price It Against Live Listings',
'{{INSIGHT_BODY}}': "Used vehicle values are falling, and dealers know it. Before you trade in or sell a work ute or van, copy 10 to 15 current listings for the same make, model and year range from carsales or Gumtree into ChatGPT, Claude or Gemini. Add your own vehicle's kilometres, service history, fit-out and any damage. Ask it to rank the comparable listings, estimate a realistic private sale price and a likely trade-in price, and list what's pushing your value up or down. Then ask it to draft the sale ad. Check the numbers yourself before you accept an offer, but you'll walk into the dealership knowing what the vehicle is worth.",
'{{FACT_1}}': "Australia's unemployment rate hit 4.9% in October 2026, its highest since about October 2021, as employment fell by 43,500 people.",
'{{FACT_2}}': "The orange glow sometimes seen in hydrogen flames comes mostly from airborne sodium, and in Adelaide tests it varied more than 28-fold with the burner unchanged.",
'{{FACT_3}}': "GlobalFoundries' chip plant in Vermont has used Boston Dynamics' Spot robot dog for more than four years.",
'{{JOKE_SETUP}}': "Why was the stormwater drainer the only tradie smiling at Friday's storm warning?",
'{{JOKE_PUNCHLINE}}': "For once, all the work was going to flow straight to him.",
'{{CLOSING_QUOTE}}': '"When everything seems to be going against you, remember that the airplane takes off against the wind, not with it."',
'{{CLOSING_ATTR}}': '— Henry Ford',
'{{CLOSING_MESSAGE}}': "It's Friday, and the storms are due this afternoon, so finish anything outdoors this morning and get the yard secured before you knock off. The jobs figures were rough and the recession talk is getting louder, but diesel is still easing and Saturday looks dry. Use the wet afternoon to check your books and quotes. Have a safe Friday and a good weekend.",
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
