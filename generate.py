#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 25 November 2026',
'{{WEATHER_1}}': 'WED 25 NOV · ☀️ Sunny and warmer, about 9-25°C, dry',
'{{WEATHER_2}}': 'THU 26 NOV · 🌦️ Partly cloudy, mid-20s, medium chance of an afternoon or evening shower',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'FRI 27 NOV · ⛈️ Warm, high 20s, high chance of showers and a possible afternoon storm',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SAT 28 NOV · 🌧️ Election day, showers likely, easing later according to some models',
'{{WEATHER_5}}': 'SUN 29 NOV · ❓ Too far out for a firm call, check the BoM later in the week',
'{{WEATHER_ALERT}}': "Today is the pick of the week. The BoM has a sunny day with light winds turning northwest to northeast at 15 to 20 km/h, and WillyWeather has Carrum Downs warming from about 9°C to 25°C. With a cold start, check dew point and steel temperature before you coat anything first thing, but by mid-morning conditions should be good. Thursday stays warm with a medium chance of showers, mostly in the afternoon and evening. Friday is the one to watch: the BoM has a high chance of showers and possibly a thunderstorm later in the day, with highs in the high 20s. Showers look likely again on Saturday, so take an umbrella if you're voting on the day. The forecast sites disagree on the timing from Thursday on, so check the BoM before you book outdoor work late in the week.",
'{{WORLD_1_FLAG}}': '🇪🇪 ESTONIA · RUSSIA',
'{{WORLD_1_HEADLINE}}': 'Russia Says Estonia Is on the Verge of Triggering Open War',
'{{WORLD_1_SUMMARY}}': "Russia's Foreign Ministry has accused Estonia, a NATO member, of hostile actions that are \"on the verge of triggering open war\". Moscow says Estonia has quietly let Ukrainian drones use its airspace to attack northwestern Russia, which Estonia denies. The warning came after Estonia said it will close its road crossings with Russia from 1 December for at least six months, citing an alleged attempted arson attack on an Estonian defence company that it says was ordered by Russian military intelligence. Estonian Foreign Minister Margus Tsahkna called the claims baseless and said Moscow is the real threat to European security. So far there's no sign of fighting, and Russia's response has been diplomatic.",
'{{WORLD_1_URL}}': 'https://www.cnbc.com/2026/11/24/russia-estonia-ukraine-war-nato-finland.html',
'{{WORLD_2_FLAG}}': '🇮🇩 INDONESIA · WORKPLACE SAFETY',
'{{WORLD_2_HEADLINE}}': 'Indonesian Candy Factory Fire Kills 24, With Around 30 Still Missing',
'{{WORLD_2_SUMMARY}}': "Indonesian authorities have confirmed 24 deaths after a fire at the PT Fonusa Agung Mulia candy factory in Serang, about 50 kilometres west of Jakarta. Rescuers are still searching for about 30 missing workers. The fire broke out on Saturday, and the first reports had three dead and 36 missing. A presidential labour adviser says early findings point to an electrical short circuit in an air-conditioning unit, and investigators are checking whether management followed workplace safety rules. Estimates of how many people were inside vary widely, from about 64 to 300. Families have been asked for DNA samples, and identifying the victims could take two to three weeks.",
'{{WORLD_2_URL}}': 'https://www.aljazeera.com/news/2026/11/23/indonesian-police-remove-24-body-bags-from-factory-fire-site',
'{{ECON_1_FLAG}}': '🧾 SMALL BUSINESS TAX',
'{{ECON_1_HEADLINE}}': 'Chalmers Flags Pre-Filled Tax Returns for Contractors and Simpler FBT',
'{{ECON_1_SUMMARY}}': "Treasurer Jim Chalmers has announced two consultations aimed at cutting business tax paperwork. The first would pre-fill more contractor income into sole traders' tax returns, which he estimates could save 400,000 hours of paperwork and $37 million a year. The ATO already pre-fills some contractor amounts reported through the taxable payments annual report, but coverage is patchy. The second would replace the case-by-case test for small fringe benefits under $300 with a simple annual threshold per employee, saving businesses about $15 million a year. It comes as the Coalition, at a small business rally outside Parliament House on Monday, promised to cut federal red tape by 25% and reverse the trust and capital gains tax changes. None of this changes your tax yet, but it's worth watching if you pay contractors or give staff small perks.",
'{{ECON_1_URL}}': 'https://www.smartcompany.com.au/tax/chalmers-reveals-plan-to-streamline-fbt-pre-fill-contractor-income/',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Wholesale Diesel in Melbourne Falls to $2.40 a Litre',
'{{ECON_2_SUMMARY}}': "The Australian Institute of Petroleum's terminal gate price for diesel in Melbourne was 240.0 cents a litre on Tuesday 24 November, including GST, down from 242.3 cents on Monday. That's the wholesale price. FuelRadar has Melbourne pump diesel averaging about 256.7 cents, with the cheapest stations around 238.5 cents, so shopping around can save close to 20 cents a litre. The ACCC's latest weekly report had diesel across the five biggest cities at 258.3 cents on 18 November, down 8.1 cents on the week. The risk is still the Strait of Hormuz, where tankers keep getting hit, so if you have bulk tanks or a fleet to fill, this week's prices are worth taking.",
'{{TECH_1_FLAG}}': '🛠️ AI · SOFTWARE',
'{{TECH_1_HEADLINE}}': 'Anthropic Launches Claude Ship, AI Agents That Review, Fix and Approve Code',
'{{TECH_1_SUMMARY}}': "Anthropic has launched Claude Ship, a set of three AI agents that work on code changes in GitHub. Code Review checks changes and is generally available. PR Steward, in beta, fixes failing tests, merge conflicts and review feedback. Claude Approvals, also in beta, reads a written policy and decides whether a change can be approved automatically or needs a person. Anthropic recommends running it in observe-only mode first, before letting it sign anything off. It's for Claude Team and Enterprise customers, so most tradies won't touch it directly. But it shows where AI tools are heading: agents that do a job and then check it against your own written rules, with a human only stepping in for the tricky cases.",
'{{TECH_1_URL}}': 'https://techcrunch.com/2026/11/23/anthropic-launches-claude-ship-letting-ai-agents-review-fix-and-approve-code-changes/',
'{{TECH_2_FLAG}}': '🛒 AI · SHOPPING AGENTS',
'{{TECH_2_HEADLINE}}': "Walmart Lets Meta's AI Agent Buy Black Friday Deals for Shoppers",
'{{TECH_2_SUMMARY}}': "Walmart has switched on its Agent Gateway, and Meta's Muse is the first AI agent allowed to buy things on Walmart.com for shoppers. You tell Muse what you want, sign in to Walmart, and the first purchase sets up an agent profile with a spending limit. Muse sees the same prices as the website and pays with the card already saved on your Walmart account, and Walmart's normal return policy applies. Reports say the agent can't see your full purchase history or card details. Walmart says other AI agents are coming. It's US-only for now, but it's the model Australian suppliers are likely to follow: letting an AI order consumables within a limit you set.",
'{{ROBOT_1_FLAG}}': '🤖 HUMANOID ROBOTS · CHIPS',
'{{ROBOT_1_HEADLINE}}': 'Infineon Adapts Car and Factory Chips to Make Humanoid Robots Safer',
'{{ROBOT_1_SUMMARY}}': "German chipmaker Infineon is adapting its automotive and industrial chips for humanoid robots, Digitimes reported on 24 November. The focus is functional safety, dexterity and power efficiency. Infineon wants to use the safety systems it builds for cars to stop a robot's AI from turning a bad decision into a dangerous movement. It has shown a board that combines a controller, gallium nitride (GaN) power chips and position sensors to drive motors of up to 1.2 kW, and GaN could shrink the electronics needed for each joint. Infineon estimates there's about US$500 of semiconductors in each humanoid robot. It hasn't given a production timeline, saying volumes will follow demand.",
'{{ROBOT_1_URL}}': 'https://www.digitimes.com/news/a20261124VL219/infineon-automotive-industrial-humanoid-robot-gan-development.html',
'{{AUS_1_HEADLINE}}': 'Tech Giants Face Fines of Up to 5% of Global Revenue Under Online Safety Deal',
'{{AUS_1_SUMMARY}}': "The government has struck a deal with the Greens to strengthen its Digital Duty of Care bill. Platforms like Google and Meta could now be fined up to 5% of their worldwide revenue, instead of the original cap of $109.2 million. Platforms would have to deal with risks such as addictive design features, an independent digital ombudsman would handle complaints, and people would be able to sue companies that breach their duty of care. Communications Minister Anika Wells called it the most significant online safety reform the country has ever had and says it will pass this week. The Coalition opposes it, and the US ambassador warned it could push platforms to censor lawful speech. Small business groups are still waiting on details of the promised exemption for low-risk websites.",
'{{AUS_1_URL}}': 'https://mumbrella.com.au/big-tech-faces-billions-in-fines-after-labor-greens-digital-duty-of-care-deal-945816',
'{{AUS_2_HEADLINE}}': 'Solomon Islands to End Its China Security Pact and Sign a Treaty With Australia',
'{{AUS_2_SUMMARY}}': "Solomon Islands has told China it will end its 2022 security pact, according to the ABC and Reuters. Reuters says the government won't renew the five-year deal when it expires in April. Prime Minister Matthew Wale is meeting Anthony Albanese today, and the two are expected to sign a broad treaty that would make Australia the country's main security partner. The China pact let Solomon Islands call in Chinese police and military personnel and allowed Chinese navy ships to stop there, which raised fears of a Chinese base in the Pacific. A Lowy Institute analyst called the move a \"massive win\" for Australia. China says its Pacific cooperation isn't aimed at any other country.",
'{{VIC_1_HEADLINE}}': 'Unions Step Back From Labor as Modelling Has It Winning Just 30 Seats',
'{{VIC_1_SUMMARY}}': "Several unions have quietly stepped back from supporting Victorian Labor this campaign, and some are openly urging members to vote for someone else, the ABC reports. RedBridge modelling now gives Labor about 30 seats on Saturday, down from 45 in the middle of the year. Premier Ben Carroll spent Tuesday campaigning in Eltham, where he ended up debating a One Nation volunteer, and One Nation's Victorian leader Warren Pickering is running in Pakenham. On housing, the Coalition is promising no stamp duty for first home buyers on homes up to $1 million, while Labor is promising more than 25,000 new homes for first-home buyers. Early voting is open every day until Friday if you'd rather avoid Saturday's queues and showers.",
'{{SCI_1_FLAG}}': '🔭 SPACE',
'{{SCI_1_HEADLINE}}': 'Euclid Telescope Finds the Most Distant Quasar Yet, From 630 Million Years After the Big Bang',
'{{SCI_1_SUMMARY}}': "Europe's Euclid space telescope has found the most distant quasar known, a blazing object powered by a giant black hole. Called J1504+6252 and nicknamed Dún Aonghasa, its light set out about 630 million years after the Big Bang, at a redshift of 8.13. That beats Euclid's own record from July, a quasar at redshift 7.77, by about 40 million years. Follow-up observations with the Hubble, Webb and Keck telescopes and the Large Binocular Telescope confirmed it. The black hole at its centre is about 360 million times the mass of the Sun. Astronomers aren't sure how something that big grew so fast when the universe was less than 5% of its current age. The results are published in Astronomy & Astrophysics, and ESA announced them on 24 November.",
'{{INSIGHT_TITLE}}': 'Before an AI Agent Spends Your Money, Write Down Its Rules and Its Limit',
'{{INSIGHT_BODY}}': "This week Walmart let an AI agent buy goods for shoppers within a set spending limit, and Anthropic released agents that approve work against a written policy. Both work the same way: the AI acts on its own, but only inside rules a person has written down. Suppliers and banks will offer the same thing to small businesses soon, so it's worth deciding your rules now. Open ChatGPT, Claude or Copilot and ask it to help you write a one-page purchasing policy: which suppliers you use, what you normally order, the most any single order can cost without your sign-off, and which purchases always need a person, like new equipment or anything for a specific job. Keep a copy for your office staff too. It's useful today for anyone ordering on the business card, and when an AI ordering tool does turn up, you'll already have the limits ready to set.",
'{{FACT_1}}': "The new record quasar is nicknamed Dún Aonghasa, after a prehistoric stone fort perched on a cliff edge on Inis Mór, one of Ireland's Aran Islands.",
'{{FACT_2}}': "A 100-million-year-old fossil flower named Tomlinsoniella pedicellata was just identified inside a museum rock collected in Kansas in the late 1800s. It's at most 1.5 mm tall, smaller than a grain of rice, and was found by micro-CT scanning a hollow mould where the flower used to be.",
'{{FACT_3}}': "Monocots, the flowering plant group that includes grasses, wheat, rice, palms, orchids and onions, make up roughly one in five of all flowering plant species.",
'{{JOKE_SETUP}}': "Why wouldn't the cabinetmaker let an AI agent do his Black Friday shopping?",
'{{JOKE_PUNCHLINE}}': "He only trusts a deal he's measured twice himself.",
'{{CLOSING_QUOTE}}': '"Trust, but verify."',
'{{CLOSING_ATTR}}': '— Russian proverb',
'{{CLOSING_MESSAGE}}': "It's Wednesday, and it's the best day of the week: sunny, light winds and about 25°C, with showers and possible storms arriving Thursday and Friday. If anything needs doing outdoors, today's the day. Wholesale diesel is still falling, so it's a good time to fill up before the weekend. And with AI agents starting to spend money and sign off work for people, it's a good week to write down your own rules. Pre-poll is open until Friday if you want to avoid Saturday's showers. Have a good day.",
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
