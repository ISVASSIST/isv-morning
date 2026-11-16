#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 17 November 2026',
'{{WEATHER_1}}': 'TUE 17 NOV · ☁️ Overcast and mostly dry, about 14-18°C',
'{{WEATHER_2}}': 'WED 18 NOV · 🌥️ Cloudy, mostly dry, about 20°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'THU 19 NOV · ⛈️ Warmer, about 22-30°C, isolated storms late',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'FRI 20 NOV · ⛈️ Thunderstorms and rain likely, about 24-26°C',
'{{WEATHER_5}}': 'SAT 21 NOV · 🌦️ Mostly cloudy, isolated storms possible, about 19°C',
'{{WEATHER_ALERT}}': "Today and Wednesday look like the best days for outdoor coating this week. Thursday warms up with storms possible late, and Friday looks the wettest, with thunderstorms and rain. These figures come from timeanddate, weather-forecast.com and similar Melbourne forecast sites, not the BoM, and they disagree on Thursday's top (somewhere between 22°C and 30°C). None of it is a Carrum Downs forecast, so check the BoM before you book outdoor work for Thursday or Friday.",
'{{WORLD_1_FLAG}}': '🇪🇺 EUROPE',
'{{WORLD_1_HEADLINE}}': 'EU Sanctions Nearly 50 Russian Banks and Accuses Moscow of Dragging Out the War',
'{{WORLD_1_SUMMARY}}': "EU foreign ministers agreed new sanctions on Monday covering 12 people and 101 organisations, including nearly 50 Russian banks and financial institutions. The aim is to cut off the money channels funding Russia's war. EU foreign policy chief Kaja Kallas said Russia's peace demands \"remain maximalist\" and called them cover for continuing the war. Russian strikes killed at least three people in Ukraine the same day, as Russia keeps hitting power plants ahead of winter. Kallas says a 22nd sanctions package will be presented in the coming days.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/11/16/russian-attacks-kill-three-in-ukraine-eu-accuses-moscow-of-prolonging-war',
'{{WORLD_2_FLAG}}': '🌏 ASIA-PACIFIC',
'{{WORLD_2_HEADLINE}}': 'Quad Leaders Are Due to Meet in Manila Today as the ASEAN Summit Wraps Up',
'{{WORLD_2_SUMMARY}}': "The White House says Donald Trump will meet the other Quad leaders in Manila today: the prime ministers of India, Japan and Australia. It would be their first in-person summit in two years. Critical minerals, maritime security and energy security are expected to be on the agenda. The ASEAN summit also finishes today, when the Philippines hands the ASEAN chair to Singapore. Several leaders then head to Shenzhen, China, for APEC on 18 and 19 November.",
'{{WORLD_2_URL}}': 'https://www.thestar.com.my/aseanplus/aseanplus-news/2026/11/14/trump-other-quad-leaders-to-meet-in-manila-on-tuesday-sources-say',
'{{ECON_1_FLAG}}': '⛽ FUEL',
'{{ECON_1_HEADLINE}}': 'Diesel Is Finally Coming Down, Falling 9.4 Cents in a Week',
'{{ECON_1_SUMMARY}}': "The ACCC says average retail diesel in the five biggest cities was 266.4 cents a litre on 11 November, down 9.4 cents in a week and 56 cents below the 31 March peak. Wholesale prices suggest there's more to come. Melbourne's terminal gate price for diesel was 247.1 cents on Monday, and unleaded was 195.4 cents. Regional diesel is still higher, averaging 276 cents. If you're filling the truck and the compressor this week, compare prices before you fill up.",
'{{ECON_1_URL}}': 'https://aip.com.au/pricing/terminal-gate-prices/',
'{{ECON_2_FLAG}}': '📉 MARKETS',
'{{ECON_2_HEADLINE}}': 'ASX Slips Again as Miners Fall for a Third Straight Day',
'{{ECON_2_SUMMARY}}': "The ASX 200 fell 37.5 points, or 0.41%, on Monday to close at 9,044.7. Materials fell 1.7%, a third day of losses, as iron ore, copper and lithium prices dropped. Coles also disclosed a cyber incident during the session. This week's big number is still the ABS October jobs data on Thursday. With the cash rate at 4.85%, a weak result would strengthen the case for a pause in December.",
'{{TECH_1_FLAG}}': '🔐 CYBER',
'{{TECH_1_HEADLINE}}': 'Coles Investigates a Cybersecurity Incident, but Says Shoppers Are Unaffected So Far',
'{{TECH_1_SUMMARY}}': "Coles told the ASX on Monday that it is investigating a cybersecurity incident, working with outside experts and the Australian Cyber Security Centre to \"contain and secure\" its IT systems. So far it has found no evidence that customer, staff or supplier data was taken. Stores, the app, online orders, gift cards and Flybuys are all working. Coles hasn't said what happened or which systems were affected. If you shop or order supplies through Coles accounts, watch for scam emails that use the news as bait.",
'{{TECH_1_URL}}': 'https://www.abc.net.au/news/2026-11-16/coles-investigates-cybersecurity-breach-but-little-detail/107390824',
'{{TECH_2_FLAG}}': '🤖 AI · SMALL BUSINESS',
'{{TECH_2_HEADLINE}}': 'Businesses Can Now Claim a Free Profile Inside ChatGPT',
'{{TECH_2_SUMMARY}}': "OpenAI's new Business Hub, in beta, lets businesses in countries where ChatGPT is available claim a free profile. You verify by phone, business email, website domain or Shopify. OpenAI says claiming doesn't buy better placement, because ChatGPT still makes its own recommendations, and it hasn't ruled out charging later. A separate Business Agents feature, where an AI talks to customers for you, is only available to some US online businesses for now. More customers are asking ChatGPT who to call, so it's worth checking what it says about you.",
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS',
'{{ROBOT_1_HEADLINE}}': 'Swiss Start-up Unveils AIR, a Wheeled Robot Built to Work Next to People Without a Safety Cage',
'{{ROBOT_1_SUMMARY}}': "EPFL spin-off Embodied AI has unveiled AIR, a two-armed robot on a wheeled base, at Humanoid Europe 2026 in Munich. Its tendon-driven arms give way on contact, so it is designed to work beside factory staff without a cage. A human operator controls it remotely for each new job, and it learns from those runs to do the task on its own. The company claims about a 95% success rate in paid pilots and says it has signed contracts with major manufacturers, but it hasn't named them. Orders are now open and the price hasn't been disclosed.",
'{{ROBOT_1_URL}}': 'https://roboticsandautomationnews.com/2026/11/15/embodied-ai-unveils-air-humanoid-robot-designed-to-learn-factory-tasks-on-the-job/107133',
'{{AUS_1_HEADLINE}}': "Albanese Won't Rule Out an APEC Group Photo With Putin",
'{{AUS_1_SUMMARY}}': "Prime Minister Anthony Albanese has left open the possibility of standing in an APEC leaders' group photo with Vladimir Putin when the summit is held in Shenzhen, China, later this week. It follows the ASEAN summit in Manila, where he signed a new defence agreement with the Philippines. He also raised the case of Hiep Tran, an Australian detained in Vietnam, with Vietnam's new prime minister. The APEC meeting is set to include talks between Donald Trump and Xi Jinping.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-15/albanese-will-not-rule-out-apec-photo-with-putin/107387814',
'{{AUS_2_HEADLINE}}': "Senate Vote This Week Decides the Government's Gas Reservation Plan",
'{{AUS_2_SUMMARY}}': "The Senate is expected to vote this week on the bill that would make the biggest gas exporters keep 20% of their output for the Australian market from 2028. It has passed the House, but the government needs either the Coalition or the Greens to get it through the Senate. The Greens have rejected it, One Nation has ruled it out, and the Coalition wants changes, including a carve-out for Western Australia. Jacqui Lambie says she'll back it. This is a Senate-only sitting week and one of the last two parliamentary weeks of the year.",
'{{VIC_1_HEADLINE}}': 'Wilson Promises a Youth Offender Bootcamp as Early Voting Opens Tomorrow',
'{{VIC_1_SUMMARY}}': "At the Liberal campaign launch, Opposition Leader Jess Wilson promised a bootcamp for young offenders and \"adult crime, adult time\" laws for 25 serious offences, to be in place before Christmas. Premier Ben Carroll launched Labor's campaign with promises to cut elective surgery waits and add more specialist appointments. Early voting opens at 9am tomorrow, Wednesday 18 November, and a record number of Victorians are expected to vote early. Election day is Saturday 28 November.",
'{{SCI_1_FLAG}}': '🐸 ECOLOGY',
'{{SCI_1_HEADLINE}}': 'Deadly Virus Linked to an 83% Drop in Tree Frog Breeding in a Brazilian Rainforest Reserve',
'{{SCI_1_SUMMARY}}': "A study in Biodiversity and Conservation tracked monkey frogs at a pond in Santa Catarina, in Brazil's Atlantic Forest. It linked repeated outbreaks of ranavirus, a disease that kills frogs, fish and reptiles, to an 83% drop in the frogs' breeding there. Ranavirus has caused frog die-offs on several continents. The researchers say it shows that disease can quietly wipe out frogs even inside protected reserves, so monitoring needs to look for infection as well as counting animals.",
'{{INSIGHT_TITLE}}': 'Ask ChatGPT Who to Call for Blasting in Your Area, Then Claim Your Profile',
'{{INSIGHT_BODY}}': "More customers now ask an AI chatbot for a recommendation before they search Google. Open ChatGPT, Claude or Gemini and ask the questions a customer would, such as \"who does abrasive blasting and protective coatings near Carrum Downs?\" and \"who can sandblast a trailer chassis in Melbourne's south-east?\" Check whether your business comes up and whether the details are right. With OpenAI's new Business Hub, you can claim a free ChatGPT profile and fix your services, service area and contact details. Make sure your website and Google profile say the same thing. It takes about 20 minutes, and it doesn't buy placement, but it stops the AI telling customers you don't do something you do.",
'{{FACT_1}}': "The EU's latest Russia sanctions cover 113 targets: 12 people and 101 organisations, nearly 50 of them banks and financial institutions.",
'{{FACT_2}}': "Under the gas reservation bill before the Senate this week, Australia's biggest gas exporters would have to keep 20% of their output for the local market from 2028.",
'{{FACT_3}}': "Retail diesel in Australia's five biggest cities is now 56 cents a litre cheaper than at its 31 March peak, according to the ACCC.",
'{{JOKE_SETUP}}': "Why did the arborist stay calm when the forecast showed Friday storms?",
'{{JOKE_PUNCHLINE}}': '"Every branch the wind brings down is just another job falling into his lap."',
'{{CLOSING_QUOTE}}': '"The time to repair the roof is when the sun is shining."',
'{{CLOSING_ATTR}}': '— John F. Kennedy',
'{{CLOSING_MESSAGE}}': "It's an overcast but dry Tuesday, and Wednesday looks similar, so make the most of both before storms arrive Thursday and Friday. Diesel is finally falling, so compare prices before you fill up. Quad leaders meet in Manila today, and early voting in the state election opens tomorrow. Have a productive Tuesday.",
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
