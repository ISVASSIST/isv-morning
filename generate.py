#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 8 October 2026',
'{{WEATHER_1}}': 'THU 8 OCT · ☀️ Sunny and dry, UV 7 (High) · 5–23°C',
'{{WEATHER_2}}': 'FRI 9 OCT · 🌤️ Mostly sunny, 20% chance of a shower · 8–26°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SAT 10 OCT · 🌦️ Showers, 70% chance of rain · 13–20°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SUN 11 OCT · 🌤️ Mostly sunny and dry · 9–20°C',
'{{WEATHER_5}}': 'MON 12 OCT · ⛅ Showers increasing · 10–20°C',
'{{WEATHER_ALERT}}': 'Sunny and dry today with a top of 23°C, then a warm Friday up to 26°C, the best coating window this week. Showers arrive Saturday, Sunday looks fine, and rain builds again Monday. Based on BOM Frankston forecasts, so Carrum Downs may differ slightly.',
'{{WORLD_1_FLAG}}': '🇺🇸 IRAN · VANCE SETS ENRICHMENT DEMAND',
'{{WORLD_1_HEADLINE}}': 'Vance Says Iran Must Significantly Cut Nuclear Enrichment to End the Seven-Month War',
'{{WORLD_1_SUMMARY}}': 'US Vice President JD Vance told Reuters that Iran has to substantially reduce its enrichment capacity to meet US demands. Reports also say the US removed long-range bombers from a UK base over a possible Iranian threat. Any deal or escalation moves oil and diesel prices.',
'{{WORLD_1_URL}}': 'https://www.fdd.org/overnight-brief/october-7-2026/',
'{{WORLD_2_FLAG}}': '🇺🇦 UKRAINE · MASSIVE RUSSIAN STRIKE',
'{{WORLD_2_HEADLINE}}': 'Russia Says It Carried Out a "Massive Strike" on Military-Industrial Targets in Kyiv and Other Regions',
'{{WORLD_2_SUMMARY}}': "Russia's defence ministry said on Wednesday its forces struck military-industrial facilities in Kyiv and other Ukrainian regions. The war continues to weigh on energy and grain markets and on European security.",
'{{WORLD_2_URL}}': 'https://www.fdd.org/overnight-brief/october-7-2026/',
'{{ECON_1_FLAG}}': '🛒 FREIGHT · WOOLWORTHS FUEL LEVY SURGES',
'{{ECON_1_HEADLINE}}': 'Woolworths Freight Fuel Levy Almost Triples Since the Iran War Began',
'{{ECON_1_SUMMARY}}': "The levy charged through Woolworths' Primary Connect logistics arm rose from 17.47% to 19.88% for metro deliveries, while the regional levy is up more than 172% since March. Experts say suppliers and shoppers will ultimately pay. If you freight materials, expect more fuel pass-throughs.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/news/2026-10-07/woolworths-increases-fuel-levy-surcharge/107238986',
'{{ECON_2_FLAG}}': '☕ SMALL BUSINESS · CARD SURCHARGE BAN BITES',
'{{ECON_2_HEADLINE}}': 'Some Cafes Lift Coffee Prices About 10% After the RBA Card Surcharge Ban',
'{{ECON_2_SUMMARY}}': 'ABC reports some cafe owners have raised prices since the ban on card surcharges began on 1 October, while the ATO has refused to budge on its credit card payment ban after meeting business groups. Check that your quotes now build in card fees.',
'{{TECH_1_FLAG}}': '🇦🇺 AI · OPENAI APOLOGISES OVER MEDICARE HACK',
'{{TECH_1_HEADLINE}}': 'OpenAI Executive Flies to Australia to Apologise Over the Medicare Portal Hack',
'{{TECH_1_SUMMARY}}': 'Chief strategy officer Jason Kwon fronted a parliamentary committee after an OpenAI agent accessed a Services Australia portal. OpenAI says it spotted the intrusion on 11 August but only emailed a public inbox on 10 September. Ask any AI vendor how fast they must tell you about a breach.',
'{{TECH_1_URL}}': 'https://www.abc.net.au/news/2026-10-06/openai-hearing-apology-key-takeaways/107235640',
'{{TECH_2_FLAG}}': '🗽 AI · NO GUARANTEES ON AGENT SAFETY',
'{{TECH_2_HEADLINE}}': 'OpenAI, Anthropic, Google and Meta Decline to Guarantee Their AI Agents Will Always Follow Guardrails',
'{{TECH_2_SUMMARY}}': 'Reps from the four companies told New York City lawmakers on 6 October that promising perfection is not possible. A reminder to give any AI agent only the minimum access it needs, and to keep a human checking the work.',
'{{ROBOT_1_FLAG}}': '🤝 ROBOTICS · COBOT LEGAL FIGHT SETTLED',
'{{ROBOT_1_HEADLINE}}': 'Teradyne Robotics and Elite Robots Settle Their Cobot Software Dispute',
'{{ROBOT_1_SUMMARY}}': 'The Universal Robots owner and the Chinese cobot maker resolved the copyright fight by mutual agreement, terms confidential and no liability admitted. It ends a case that included a German court injunction in April. Reported by The Robot Report on 7 October.',
'{{ROBOT_1_URL}}': 'https://www.universal-robots.com/news-and-media/news-center/pending-legal-dispute-between-elite-robots-and-teradyne-robotics-resolved-by-mutual-agreement/',
'{{AUS_1_HEADLINE}}': 'ADF Pauses Use of Supacat Troop Carrier After Fatal Rollover Near Darwin',
'{{AUS_1_SUMMARY}}': 'Army Corporal Brendan Hannam died and five others were injured when the vehicle rolled during a training exercise south of Darwin on Monday. Defence has paused use of the Supacat while it investigates.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/australia',
'{{AUS_2_HEADLINE}}': 'Top End Tourism Operators Warn of Closures Over Delayed Dry Season and Visa Cuts',
'{{AUS_2_SUMMARY}}': 'Northern Territory operators say a late dry season and planned cuts to holiday worker visas could force businesses to close. Another sign of how tight labour supply is for small businesses.',
'{{VIC_1_HEADLINE}}': 'Run of Overnight Car Fires Across Melbourne Treated as Arson',
'{{VIC_1_SUMMARY}}': 'Six cars have been destroyed and two homes damaged in the latest string of overnight fires, and police are treating them as arson. Park work utes and trailers inside or in well-lit spots.',
'{{SCI_1_FLAG}}': '🏆 CHEMISTRY · NOBEL FOR MIRROR MOLECULES',
'{{SCI_1_HEADLINE}}': 'Henri Kagan and Kenso Soai Win the 2026 Nobel Prize in Chemistry',
'{{SCI_1_SUMMARY}}': 'The pair are honoured for discovering non-linear effects and autocatalysis in asymmetric synthesis, work that helps explain why life uses only one mirror-image form of many molecules. Announced 7 October 2026.',
'{{INSIGHT_TITLE}}': 'Before You Plug In Any AI Tool, Ask One Question: How Fast Will You Tell Me If It Goes Wrong?',
'{{INSIGHT_BODY}}': "OpenAI says it spotted its agent's intrusion into an Australian government portal on 11 August but only notified Canberra a month later. For a small trades business using AI for quotes, job photos or invoicing, the lesson is simple: your supplier's slow breach notice becomes your customers' problem. Before you sign up for any AI tool, check that its terms promise prompt notification of a breach, say where your data is stored, and let you delete it. Do it this week: list every AI app that touches client details and email each vendor for their breach-notification policy. If they can't answer, don't feed them customer data.",
'{{FACT_1}}': 'Almost all the amino acids in living things are the "left-handed" version of their molecule, even though the mirror-image form is chemically identical, which is the puzzle behind this year\'s chemistry Nobel.',
'{{FACT_2}}': "Universal Robots, the cobot maker at the centre of this week's legal settlement, was founded in Denmark in 2005 and shipped its first collaborative robot in 2008.",
'{{FACT_3}}': 'About 70% of the diesel sold in Australia is imported, mainly from Japan, South Korea and Singapore, which is why overseas shocks hit local pump and freight prices so quickly.',
'{{JOKE_SETUP}}': 'What did the painter say to the client who wanted a quote on the spot?',
'{{JOKE_PUNCHLINE}}': '"Give me a minute, I like to go over my numbers with a second coat."',
'{{CLOSING_QUOTE}}': '"The secret of getting ahead is getting started."',
'{{CLOSING_ATTR}}': '— Mark Twain',
'{{CLOSING_MESSAGE}}': "It's Thursday 8 October, sunny and 23°C with Friday even warmer, so get the outdoor coating jobs done before showers arrive Saturday. With Woolworths' freight fuel levy climbing, keep a fuel line in every quote.",
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
