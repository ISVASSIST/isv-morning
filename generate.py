#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 1 October 2026',
'{{WEATHER_1}}': 'THU 1 OCT · ⛈️ Rain increasing, very high chance, possible afternoon and evening thunderstorm, 15–35mm · 16–22°C',
'{{WEATHER_2}}': 'FRI 2 OCT · 🌧️ Rain, cool · 12–17°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SAT 3 OCT · 🌦️ Showers · 10–18°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SUN 4 OCT · ⛅ Partly cloudy · 9–18°C',
'{{WEATHER_5}}': 'MON 5 OCT · ⛅ Clearing, mostly dry · 9–19°C',
'{{WEATHER_ALERT}}': 'Wet start to October: rain builds today with a possible afternoon and evening thunderstorm and 15–35mm, then a cool, wet Friday and showery Saturday before it clears Sunday. Forecast based on Melbourne BOM outlooks.',
'{{WORLD_1_FLAG}}': '🇺🇸🇮🇶 IRAQ · PENTAGON SAYS LAST US TROOPS HAVE LEFT, ENDING 12-YEAR MISSION',
'{{WORLD_1_HEADLINE}}': 'US Military Completes Withdrawal From Iraq, Ending Operation Inherent Resolve',
'{{WORLD_1_SUMMARY}}': "The Pentagon says the last US troops and equipment made an 'orderly departure' from Erbil Air Base, closing the 12-year campaign against Islamic State, though there are concerns in Iraqi Kurdistan about defence gaps and Iran-aligned militias.",
'{{WORLD_1_URL}}': 'https://www.abc.net.au/news/2026-09-30/us-military-completes-iraq-withdrawal/107214128',
'{{WORLD_2_FLAG}}': '🇺🇸 WASHINGTON · TOP AI COMPANIES SIGN WHITE HOUSE "SELF-POLICING" ACCORD',
'{{WORLD_2_HEADLINE}}': 'Trump Says Top Tech Firms Have Signed a Voluntary Accord to "Self-Police" AI Development',
'{{WORLD_2_SUMMARY}}': "CEOs including Anthropic, OpenAI, Google, Meta, Microsoft and Amazon signed a non-binding pledge for internal controls and outside audits, and Trump signed an order telling agencies to call AI 'super intelligence'; it creates no enforceable federal rules.",
'{{WORLD_2_URL}}': 'https://www.kpbs.org/news/politics/2026/09/29/trump-says-top-tech-firms-have-signed-accord-to-self-police-ai-development',
'{{ECON_1_FLAG}}': '💳 CARD SURCHARGES · BAN TAKES EFFECT TODAY, SMALL BUSINESS BRACES',
'{{ECON_1_HEADLINE}}': "Card Surcharge Ban Starts Today as Businesses Brace for Higher Costs and Some Go Cash-Only",
'{{ECON_1_SUMMARY}}': "From 1 October merchants can no longer add a surcharge to debit, credit or eftpos payments; ACCI says it is causing 'dread' among small businesses, and the practical fix is building fees into your quoted prices and removing surcharge wording from invoices, quotes and websites.",
'{{ECON_1_URL}}': 'https://www.sbs.com.au/news/article/australia-card-surcharge-ban-explained/0jm5w5v40',
'{{ECON_2_FLAG}}': '⛽ DIESEL · STANDARD TIGHTENS TODAY WITH DIESEL STILL NEAR $2.85',
'{{ECON_2_HEADLINE}}': 'Diesel Standard Tightens From 1 October, Narrowing Import Options While Prices Sit Near $2.85 a Litre',
'{{ECON_2_SUMMARY}}': "The temporary 60.5C flash-point allowance ends and the usual 61.5C minimum returns, limiting what fuel Australia can import during a volatile global market; Sydney diesel averages about 285c a litre, so keep fuel costs in every quote.",
'{{TECH_1_FLAG}}': '🤖 AI · RUNWAY LAUNCHES AUTONOMOUS AD ENGINE FOR SMALL TEAMS',
'{{TECH_1_HEADLINE}}': 'Runway Launches "Runway Ads", an AI Engine That Makes, Publishes and Tunes Ads on Meta, Google and TikTok',
'{{TECH_1_SUMMARY}}': "It reads performance data and iterates creative on its own; Runway says it lifted its own weekly ad volume from 77 to 900 and cut cost per subscriber 41%. A sign AI marketing is reaching small operators, though keep a human approving anything that goes public.",
'{{TECH_1_URL}}': 'https://agilebrandguide.com/yesterdays-martech-ai-cx-news-september-30-2026/',
'{{TECH_2_FLAG}}': '💬 AI · BRAZE BRINGS AI CHAT AGENTS TO WHATSAPP AND SMS',
'{{TECH_2_HEADLINE}}': 'Braze Launches Conversational AI Agents for WhatsApp, SMS and Web With Brand Guardrails',
'{{TECH_2_SUMMARY}}': "The beta agents answer customers using your product catalogue and FAQs within rules you set once, with human sign-off available — the same idea small trades can borrow for after-hours enquiries and quote follow-ups.",
'{{ROBOT_1_FLAG}}': '🤖 GLOBAL · IFR REPORT: SERVICE ROBOT SHIPMENTS JUMP 24%, HUMANOIDS HIT 7,000 UNITS',
'{{ROBOT_1_HEADLINE}}': 'Global Sales of Professional Service Robots Surge 24% as Humanoids Emerge as a New Market Segment',
'{{ROBOT_1_SUMMARY}}': "The IFR's World Robotics 2026 report shows almost 250,000 professional service robots shipped in 2025, led by 117,000 transport and logistics machines, with about 7,000 humanoids; the US overtook Japan as the second-biggest industrial robot market with 38,500 installs.",
'{{ROBOT_1_URL}}': 'https://manilatimes.net/2026/09/30/tmt-newswire/media-outreach-newswire/global-sales-of-professional-service-robots-surge-24/2435885',
'{{AUS_1_HEADLINE}}': 'NDIS Community Participation Funding Cut 50% From Today as Plans Are Renewed',
'{{AUS_1_SUMMARY}}': 'Budgets for social and community participation supports fall 50% and improved daily living supports 10%, applied only as plans are created or reassessed, with personal care and accommodation protected; providers are warning of closures.',
'{{AUS_1_URL}}': 'https://www.ndis.gov.au/news/11695-changes-support-budgets-1-october',
'{{AUS_2_HEADLINE}}': 'Macarthur Solar Collapses, Leaving Customers Out of Pocket on Subsidised Batteries',
'{{AUS_2_SUMMARY}}': "Customers paid deposits of $1,500 to $17,600, sometimes up to 50% upfront, for batteries under the federal Cheaper Home Batteries Program; the company owes about $3.4 million and NSW is investigating after 100+ complaints.",
'{{VIC_1_HEADLINE}}': 'Keilor East Station on Melbourne Airport Rail to Be Built by 2031',
'{{VIC_1_SUMMARY}}': 'Early work on a 7.4km line from Albion via Keilor East starts within weeks, with major construction from 2028; there is still no firm date for trains to reach the airport itself.',
'{{SCI_1_FLAG}}': '🦇 EVOLUTION · BATS LIKELY FIRST EVOLVED IN EUROPE ABOUT 65 MILLION YEARS AGO',
'{{SCI_1_HEADLINE}}': 'Bat Genomes and Fossils Point to a European Origin About 65 Million Years Ago',
'{{SCI_1_SUMMARY}}': "A Nature study by 137 researchers combined genomes from every living bat family with fossils, overturning Asian, African and North American origin theories and suggesting flight and echolocation appeared right at the start of bat evolution.",
'{{INSIGHT_TITLE}}': "The White House 'Self-Policing' AI Pledge — Why Your Business Still Needs Its Own AI Rules",
'{{INSIGHT_BODY}}': "Big AI companies just signed a voluntary accord to police themselves, but it creates no enforceable rules, so protecting your business is still on you. Write a one-page policy: which tools staff may use, what customer and pricing data must never go into them, who checks AI-drafted quotes and emails before they're sent, and who to tell if something goes wrong. Ask every AI vendor where your data is stored and whether it trains their models. A simple policy costs an afternoon and is far cheaper than explaining a leaked quote to a client.",
'{{FACT_1}}': "Melbourne Airport Rail's first stage is a 7.4-kilometre line from Albion, including a 500-metre bridge over the Maribyrnong River, with major construction not due to start until 2028.",
'{{FACT_2}}': "Only about 7,000 humanoid robots shipped worldwide in 2025, compared with 117,000 transport and logistics robots, showing where the real money in robotics still is.",
'{{FACT_3}}': "Iran's rial has hit a record low of more than 2.5 million to the US dollar, less than a month after its previous record low.",
'{{JOKE_SETUP}}': "A pest controller was asked how his small business kept getting referrals, even when the quote was higher than the other blokes'.",
'{{JOKE_PUNCHLINE}}': 'He said, "Simple — I never leave a job until the customer has nothing left to bug me about."',
'{{CLOSING_QUOTE}}': '"A smooth sea never made a skilled sailor."',
'{{CLOSING_ATTR}}': '— English Proverb',
'{{CLOSING_MESSAGE}}': "It's Thursday 1 October, with rain building through the day, a possible afternoon thunderstorm and up to 35mm around Carrum Downs. Get outdoor work wrapped up early, and check your quotes and invoices no longer mention a card surcharge, which is banned from today.",
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
