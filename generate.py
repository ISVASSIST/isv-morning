#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 18 November 2026',
'{{WEATHER_1}}': 'WED 18 NOV · 🌥️ Cloudy and dry, about 16-20°C',
'{{WEATHER_2}}': 'THU 19 NOV · 🌦️ Warmer, about 13-25°C, a shower or two in the evening',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'FRI 20 NOV · ⛈️ Rain and a likely thunderstorm, 5-25mm',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SAT 21 NOV · ⛅ Partly cloudy, 30% chance of rain',
'{{WEATHER_5}}': 'SUN 22 NOV · 🌧️ Showers increasing, possible storms, 90% chance of rain',
'{{WEATHER_ALERT}}': "Today is the best day this week for outdoor coating: cloudy but dry. Thursday warms up with a shower or two possible in the evening. The BoM gives Friday a 95% chance of rain, with 5-25mm and a likely thunderstorm, and Sunday looks wet again. Saturday is the only gap. These are Melbourne forecasts from the BoM and other forecast sites, not Carrum Downs, so check the BoM again before you book outdoor work for Thursday afternoon or Friday.",
'{{WORLD_1_FLAG}}': '🇺🇦 UKRAINE',
'{{WORLD_1_HEADLINE}}': "Ukraine Hits Russia's Kerch Bridge to Crimea Two Days Running",
'{{WORLD_1_SUMMARY}}': "Ukraine struck the Kerch Bridge, which links Russia to occupied Crimea, on Monday and again on Tuesday. Ukraine's SBU security service says one of the bridge's metal arches and the road span beneath it were destroyed, and traffic was suspended. Russia says rail traffic has resumed on one track. President Zelenskyy called the attack \"unprecedented\" and said it was retaliation for Russian strikes on Ukraine's power grid. It comes just before Vladimir Putin is due to meet Donald Trump and Xi Jinping in Shenzhen, China. The damage reports are still developing.",
'{{WORLD_1_URL}}': 'https://www.cnbc.com/2026/11/17/kerch-bridge-ukraine-russia-putin-kyiv.html',
'{{WORLD_2_FLAG}}': '🌏 ASIA-PACIFIC',
'{{WORLD_2_HEADLINE}}': 'Quad Leaders Agree on Maritime Surveillance, Undersea Cables and AI in Manila',
'{{WORLD_2_SUMMARY}}': "Anthony Albanese, Donald Trump, Narendra Modi and Japan's Sanae Takaichi met in Manila on Tuesday for the first in-person Quad leaders' summit in more than two years. They announced a joint maritime surveillance effort, with the first exercise set for March 2027 near Guam. They also agreed to widen undersea cable protection to include energy cables and put more than US$85 million into trusted AI access. Without naming China, they raised \"grave concerns\" about economic coercion, including export restrictions on critical minerals. India will host a first Quad business forum in Mumbai in early 2027.",
'{{WORLD_2_URL}}': 'https://www.tribuneindia.com/news/world/quad-leaders-unveil-5-outcomes-at-manila-summit-india-to-host-business-leaders-forum-in-2027',
'{{ECON_1_FLAG}}': '📉 MARKETS · RATES',
'{{ECON_1_HEADLINE}}': 'ASX Drops 1.8% as RBA Minutes Show Further Rate Rises Are Still on the Table',
'{{ECON_1_SUMMARY}}': "The ASX 200 fell 161.5 points, or 1.79%, on Tuesday to close at 8,883.2, its lowest close since late October. Miners and banks led the fall, and utilities were the only sector to rise. The minutes of the RBA's 2-3 November meeting showed the board split 6-3 on raising the cash rate to 4.85%. Most members said 4.85% was \"not clearly sufficient\" to get inflation back to target, and inflation is expected to stay above 3% until late 2027. Thursday's October jobs figures are the next big test. Don't count on rate relief before Christmas.",
'{{ECON_1_URL}}': 'https://www.marketindex.com.au/news/asx-200-live-today-tuesday-17th-november',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Melbourne Diesel Keeps Easing, but Shop Around Before You Fill Up',
'{{ECON_2_SUMMARY}}': "Fuel-price trackers put Melbourne's average diesel price at about 265 cents a litre, down roughly 15 cents since 1 November. Unleaded is averaging somewhere between 211 and 218 cents. Wholesale prices point to further falls: the AIP terminal gate price for Melbourne diesel was 247.1 cents on Monday, down from 254.3 cents a week earlier. Pump prices still vary widely, with the cheapest diesel stations about 20 cents below the average. With storms due Friday, fill the truck and compressor today or tomorrow, and compare prices first.",
'{{TECH_1_FLAG}}': '🔐 AI · PRIVACY',
'{{TECH_1_HEADLINE}}': 'Google Will Keep Gemini Chats for Two Months, Even With History Turned Off',
'{{TECH_1_SUMMARY}}': "Google is extending how long it keeps Gemini conversations when chat history is off, from 72 hours to about two months, with the change rolling out worldwide over the coming weeks. It is also splitting chat history and AI training into two separate settings. Google says both new settings will be off by default for people who had previously turned off Keep Activity. If you or the crew use Gemini for quotes or customer emails, check those settings now and keep bank details, passwords and customer personal information out of the chat box.",
'{{TECH_1_URL}}': 'https://techcrunch.com/2026/11/17/google-to-keep-gemini-chats-for-two-months-up-from-72-hours-even-with-history-off/',
'{{TECH_2_FLAG}}': '🤖 AI · JOBS',
'{{TECH_2_HEADLINE}}': 'Bunnings Cuts 230 Tech Jobs and Sends Work to India as It Leans on AI',
'{{TECH_2_SUMMARY}}': "Bunnings will make about 230 permanent technology roles redundant and end 120 contractor agreements, moving that work to Tata Consultancy Services teams in India and the Philippines. The handover starts next month and runs to June. About 500 tech staff will stay in Australia. Managing director Mike Schneider called it \"a necessary but important change\", and the company says it is already investing in AI. It follows Qantas's cut of 850 corporate jobs. Affected staff are being offered redundancy packages, redeployment where possible and career transition support.",
'{{ROBOT_1_FLAG}}': '🦾 CONSTRUCTION ROBOTICS',
'{{ROBOT_1_HEADLINE}}': 'Bricklaying Robot Maker Says Its Machine Can Lay 800 Bricks a Day',
'{{ROBOT_1_SUMMARY}}': "At a construction robotics conference covered on Tuesday, Salar Al Khafaji, CEO of Dutch start-up Monumental, said its mobile bricklaying robot can place 800 bricks a day, about double an average human bricklayer. Other reporting puts the robot closer to one human mason per shift, and output depends on the building design, site conditions and materials. The same report covers logistics firm GXO's plan to roll out up to 1,000 Apptronik humanoids and Google DeepMind's Gemini Robotics 2.5. For trades, it shows that robots are moving onto building sites, but the claimed numbers still need independent checks.",
'{{ROBOT_1_URL}}': 'https://roboticsandautomationnews.com/2026/11/17/conference-report-construction-industry-on-the-verge-of-a-robotics-revolution/107197/',
'{{AUS_1_HEADLINE}}': 'Bupa GP Clinic Told Doctors to Bill Costly Medicare Items to Lift Revenue',
'{{AUS_1_SUMMARY}}': "The ABC has obtained a June email from a Bupa-owned GP clinic telling its doctors to make sure \"revenue is increasing\" and to make more use of chronic condition plans, which attract higher Medicare payments. Bupa says the email was sent at one clinic and was meant to remind doctors to think about preventative care. Senior doctors say they are worried that corporate-owned GP practices are putting profit ahead of patient care.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-18/bupa-clinic-urged-gps-to-bill-costly-medicare-items-lift-revenue/106981358',
'{{AUS_2_HEADLINE}}': 'Gas Reservation Bill Stalls in the Senate Over a WA Carve-Out',
'{{AUS_2_SUMMARY}}': "The government's plan to make the biggest gas exporters keep 20% of their output for the Australian market from 2028 was debated in the Senate on Tuesday, but no deal was reached. Opposition Leader Angus Taylor won't support the bill unless it excludes Western Australia, which has had its own gas reservation policy since 2006. Labor has rejected the carve-out over constitutional concerns. The Greens and One Nation oppose the bill, so the government still lacks the numbers. Domestic gas supply feeds into power and manufacturing costs, so watch how this ends this week.",
'{{VIC_1_HEADLINE}}': 'Early Voting Opens Today as Wilson Wins the Undecided Voters at the Leaders\' Forum',
'{{VIC_1_SUMMARY}}': "Early voting for the 28 November state election opens at 9am today. More than 200 centres will be open from 9am to 6pm daily until Friday 27 November, except Sunday 22 November, and you don't need a reason to vote early. At Tuesday's televised forum before 100 undecided voters, Opposition Leader Jess Wilson took 39% of the audience vote, ahead of Premier Ben Carroll and Greens leader Ellen Sandell. Debt, crime and integrity dominated the night. Check the VEC website for your nearest centre.",
'{{SCI_1_FLAG}}': '🧠 HEALTH',
'{{SCI_1_HEADLINE}}': "Flashing Light-and-Sound Headset Shows No Benefit for Alzheimer's in a Large Trial",
'{{SCI_1_SUMMARY}}': "A year-long trial of Cognito Therapeutics' Spectris headset, which uses flickering lights and sounds to stimulate 40 Hz \"gamma\" brain waves, found no cognitive benefit for people with Alzheimer's, Nature reports. The 673 participants used either the real device or a sham for an hour a day. After 12 months, the group using the real device did no better than the sham group. The results were presented at the Clinical Trials on Alzheimer's Disease meeting in Boston on 16 November. One investigator said it seemed to work better in milder cases, but that will need another trial to prove.",
'{{INSIGHT_TITLE}}': 'Let AI Draft Your Christmas Shutdown Notice and Last-Booking Cut-Off Now',
'{{INSIGHT_BODY}}': "Christmas is about five weeks away, and the jobs that get squeezed in before the break are often the ones that blow out. Give ChatGPT, Claude or Gemini your shutdown and reopening dates and the last day you can take new blasting or coating jobs. Tell it how long a typical job takes, including cure time. Ask it to write a short notice for your website and Google profile, an email to regular customers, and a line for your quote template. Read it through, fix the dates, and send it this week. Customers get a clear cut-off, you avoid the panic calls on 22 December, and you don't end up promising coatings that can't cure before the break.",
'{{FACT_1}}': "Ukraine's SBU says its strike on the Kerch Bridge to Crimea destroyed one of the bridge's metal arches and the road span beneath it.",
'{{FACT_2}}': "The Victorian Electoral Commission is opening more than 200 early voting centres for this state election, up from 155 in 2022.",
'{{FACT_3}}': "Monumental's CEO says its bricklaying robot can place 800 bricks a day, about double what an average human bricklayer lays.",
'{{JOKE_SETUP}}': "Why did the glazier vote early on the first day of pre-poll?",
'{{JOKE_PUNCHLINE}}': "He likes to keep things transparent, and he'd already seen right through every promise.",
'{{CLOSING_QUOTE}}': '"Opportunities multiply as they are seized."',
'{{CLOSING_ATTR}}': '— Sun Tzu',
'{{CLOSING_MESSAGE}}': "It's a cloudy but dry Wednesday, the best outdoor day this week before rain and likely storms on Friday, so get the coating jobs done early. Early voting opens at 9am, diesel is still easing, and the RBA minutes say rate relief isn't coming soon. Have a productive Wednesday.",
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
