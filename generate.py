#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Monday, 16 November 2026',
'{{WEATHER_1}}': 'MON 16 NOV · ☁️ Cloudy, southerly breeze, 20% chance of rain, about 10-16°C',
'{{WEATHER_2}}': 'TUE 17 NOV · 🌤️ Partly cloudy and dry, about 8-18°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'WED 18 NOV · 🌤️ Partly cloudy, mostly dry, about 11-21°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'THU 19 NOV · 🌦️ Warm, up to about 25°C, showers developing',
'{{WEATHER_5}}': 'FRI 20 NOV · ⛈️ Possible thunderstorms (aggregator outlook only)',
'{{WEATHER_ALERT}}': "Tuesday and Wednesday look like the driest days this week for outdoor coating. Showers should develop on Thursday as it warms up, and Friday may bring storms. Monday to Thursday are from the BoM's Melbourne forecast issued Saturday night. Friday is from timeanddate.com, not the BoM. None of it is a Carrum Downs forecast, so check the BoM before you book outdoor work.",
'{{WORLD_1_FLAG}}': '🌏 ASIA-PACIFIC',
'{{WORLD_1_HEADLINE}}': 'ASEAN Summit Opens in Manila, With the South China Sea High on the Agenda',
'{{WORLD_1_SUMMARY}}': "The 49th ASEAN Summit opened in Metro Manila on Sunday and runs until Tuesday 17 November. The Philippine foreign secretary says the South China Sea code of conduct is about 80% agreed but won't be finished at this summit. Myanmar, the energy crisis and trade are also on the agenda. Donald Trump is due to arrive near the end and may hold a sideline meeting with the other Quad leaders: India, Japan and Australia. Singapore takes over as ASEAN chair when the summit closes.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/11/15/asean-summit-whos-attending-and-whats-at-stake',
'{{WORLD_2_FLAG}}': '🇺🇸 UNITED STATES',
'{{WORLD_2_HEADLINE}}': 'More Than 14,000 US Flights Cancelled After a Nationwide FAA Ground Stop',
'{{WORLD_2_SUMMARY}}': "A nationwide ground stop on Friday 13 November led to more than 14,000 cancelled flights on Friday and Saturday, with about 900 more cancelled early Sunday. FAA chief Bryan Bedford blamed faulty equipment and expected flights to be back to normal by the end of the weekend. Transport Secretary Sean Duffy said the cause was either bad equipment or human error while a contractor was replacing old copper lines with fibre. An FAA union says its technicians weren't included in the upgrade. If you have US travel coming up, check your flights.",
'{{WORLD_2_URL}}': 'https://www.cnn.com/2026/11/14/politics/faa-ground-stop-what-we-know',
'{{ECON_1_FLAG}}': '⛽ FUEL',
'{{ECON_1_HEADLINE}}': 'Melbourne Wholesale Petrol Falls About 10 Cents in a Week',
'{{ECON_1_SUMMARY}}': "Melbourne's terminal gate price for petrol fell from 205.8 cents a litre on Monday 9 November to 195.7 cents on Friday, as crude kept easing. FuelRadar's Melbourne average for unleaded 91 is about 218 cents, with the cheapest sites under 190 cents. Diesel is still around 265-273 cents depending on the source. It doesn't follow the petrol cycle and has been slower to fall. Shop around before filling the ute and the compressor tanks.",
'{{ECON_1_URL}}': 'https://fuelradar.com.au/fuel-prices/vic/melbourne',
'{{ECON_2_FLAG}}': '📉 MARKETS',
'{{ECON_2_HEADLINE}}': "ASX Ends the Week Lower, and October Jobs Figures Are Due Thursday",
'{{ECON_2_SUMMARY}}': "The ASX 200 fell 0.71% on Friday to 9,082.2. Materials led the fall, down 1.61%, and Paladin Energy dropped about 17.6% after a $525 million capital raise. This week's big number is the ABS October jobs data, out Thursday 19 November at 11:30am. Unemployment was 4.7% in September. After five rate rises this year took the cash rate to 4.85%, a weak result would support a pause in December. A strong one would keep another rise on the table.",
'{{TECH_1_FLAG}}': '💳 AI · PAYMENTS',
'{{TECH_1_HEADLINE}}': 'OpenAI Launches ChatGPT Wallet So AI Agents Can Pay for Things',
'{{TECH_1_SUMMARY}}': "OpenAI has launched ChatGPT Wallet, built with Visa, Mastercard and American Express. It lets ChatGPT's agents make purchases using a stand-in token instead of your real card number. Every purchase still needs a Face ID or fingerprint check. For now it's only for US ChatGPT Pro users with credit cards, and debit cards aren't supported. OpenAI says it eventually wants to allow purchases under preset spending limits without approving each one. It's a sign that AI ordering supplies on your behalf is getting closer.",
'{{TECH_1_URL}}': 'https://www.ghacks.net/2026/11/15/openai-launches-chatgpt-wallet-so-agents-can-pay-without-seeing-your-card-details/',
'{{TECH_2_FLAG}}': '🖥️ MICROSOFT 365',
'{{TECH_2_HEADLINE}}': "Microsoft Says a Network Upgrade, Not Hackers, Caused Friday's Outage. Australian Cyber Experts Are Still Worried",
'{{TECH_2_SUMMARY}}': "Microsoft says Friday's Outlook and Teams outage came from a problem during an earlier network capacity upgrade, not a cyberattack or AI. It has promised a preliminary incident report within two business days. The Australian Information Security Association warns that while it was down, staff used personal email, USB drives and other apps, so sensitive information may have bypassed normal security. If your crew did the same, check what was sent and where it was saved.",
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS',
'{{ROBOT_1_HEADLINE}}': "ASUS Unveils Gallop, a Humanoid Robot Learning to Pack Motherboard Parts",
'{{ROBOT_1_SUMMARY}}': "ASUS has detailed Gallop, its first humanoid robot, which is being trained to pack motherboard accessories at one of its electronics factories. The target is a 99.5% success rate in under 20 seconds per board, which is about the pace of a human worker. Customer trials are planned for 2027 and commercial sales for the second half of 2028. The robot is aimed at fiddly, repetitive bench work rather than heavy lifting.",
'{{ROBOT_1_URL}}': 'https://interestingengineering.com/ai-robotics/asus-gallop-humanoid-robot-unveiled',
'{{AUS_1_HEADLINE}}': 'Australia and the Philippines Sign a New Defence Pact in Manila',
'{{AUS_1_SUMMARY}}': "Prime Minister Anthony Albanese signed a new defence agreement with the Philippines on Sunday while in Manila for the ASEAN summit. It focuses on maritime security and makes joint patrols, military exercises and disaster relief easier to organise. It updates a 1995 agreement. It comes as Philippine and Chinese coast guard ships keep clashing in the South China Sea.",
'{{AUS_1_URL}}': 'https://www.sbs.com.au/news/podcast-episode/australia-signs-a-new-defence-deal-with-the-philippines-evening-news-bulletin-15-november-2026/wgms5m22g',
'{{AUS_2_HEADLINE}}': 'Kangaroos and Jillaroos Both Win Rugby League World Cup Finals in Brisbane',
'{{AUS_2_SUMMARY}}': "The Kangaroos beat New Zealand 32-12 in Sunday's men's World Cup final in Brisbane, winning their fourth straight title. They led 24-6 at half-time. Liam Martin, Jack Bostock, Bradman Best and Tom Trbojevic scored the tries, and Cameron Munster kicked four goals. Earlier in the day, the Jillaroos beat the Kiwi Ferns 34-10 to win the women's final.",
'{{VIC_1_HEADLINE}}': 'Labor and the Coalition Launch Their Campaigns With Early Voting Starting Wednesday',
'{{VIC_1_SUMMARY}}': "Both major parties held their official campaign launches in Melbourne over the weekend, ahead of the 28 November election. Jess Wilson called the election a choice between Labor and \"a fresh start\" and promised 3,000 extra police. Premier Ben Carroll focused on health, promising to cut emergency department waits by 20%, halve surgery waiting lists and remove dental care costs. A poll released Friday has the Coalition on track to win. Early voting opens on Wednesday 18 November.",
'{{SCI_1_FLAG}}': '🧠 NEUROSCIENCE',
'{{SCI_1_HEADLINE}}': "Brain Scans May Flag Alzheimer's Risk Years Before Memory Problems Appear",
'{{SCI_1_SUMMARY}}': "A Stanford-led team published in Science Advances has built a brain-connectivity score from resting-state brain scans. In older adults whose memory tests looked normal, the score separated people into 'SuperAger-like' and 'Alzheimer-like' groups. The researchers say it predicted risk as well as or better than existing biomarkers like amyloid and tau, and earlier. It worked best combined with them. Reports say it predicted who developed the disease within about 5 to 12 years. It's still a research tool, not a clinical test yet.",
'{{INSIGHT_TITLE}}': 'Let AI Turn a Coating Datasheet Into a One-Page Cheat Sheet for the Crew',
'{{INSIGHT_BODY}}': "Coating datasheets run to several pages, and the numbers that matter on site are buried in them: minimum and maximum application temperature, humidity limits, how far above the dew point the steel must be, recoat windows, pot life and full cure time. Upload the manufacturer's PDF into ChatGPT, Claude or Copilot and ask for a one-page table of those figures in plain English, with the warm and cold-weather limits up front. Check every number against the original before it goes in the van, then laminate it or put it in the job folder. In a week like this, with dry days followed by a 25°C Thursday and possible storms, the crew can check the recoat window on the spot without phoning the office.",
'{{FACT_1}}': "Singapore takes over the rotating ASEAN chair from the Philippines when this week's Manila summit closes on 17 November.",
'{{FACT_2}}': "ChatGPT Wallet never gives the agent your real card number. A card-network token stands in for it, and only after a Face ID or fingerprint check.",
'{{FACT_3}}': "Melbourne's wholesale petrol price fell about 10 cents a litre in four trading days last week, from 205.8 cents on Monday to 195.7 cents on Friday.",
'{{JOKE_SETUP}}': "Why did the bobcat operator never complain about Mondays?",
'{{JOKE_PUNCHLINE}}': '"No matter how deep a hole the weekend left him in, he could always dig his way out by smoko."',
'{{CLOSING_QUOTE}}': '"Never leave that till tomorrow which you can do today."',
'{{CLOSING_ATTR}}': '— Benjamin Franklin',
'{{CLOSING_MESSAGE}}': "It's a cloudy, cool Monday. Tuesday and Wednesday look dry, then showers and possible storms arrive Thursday and Friday, so get the outdoor coating done early in the week. Petrol is falling, so shop around before you fill up. Watch for Thursday's jobs figures, and early voting opens Wednesday. Have a good week.",
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
