#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 19 November 2026',
'{{WEATHER_1}}': 'THU 19 NOV · 🌤️ Warm, about 13-25°C, a late shower possible',
'{{WEATHER_2}}': 'FRI 20 NOV · ⛈️ Showers and a likely storm, possibly severe, about 20-26°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'SAT 21 NOV · 🌦️ A morning shower or two, then clearing, 15-24°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SUN 22 NOV · 🌧️ Hot then wet, up to 28°C, 90% chance of rain, late storm',
'{{WEATHER_5}}': 'MON 23 NOV · ⛅ Outlook not firm yet, check the BoM on the weekend',
'{{WEATHER_ALERT}}': "Today is the last dry window before Friday. The BoM's Melbourne forecast gives Friday showers and a thunderstorm that could be severe, with heavy rain that may cause flash flooding. Get any outdoor coating done today and make sure it has cured before tonight's possible late shower. Saturday should clear after a morning shower. Sunday warms to about 28°C but has a 90% chance of 2-15mm of rain and a late storm. These figures come from the BoM's Cranbourne and Melbourne forecasts, so check the BoM again before you plan Friday's work.",
'{{WORLD_1_FLAG}}': '🌏 CHINA · APEC',
'{{WORLD_1_HEADLINE}}': 'Trump, Xi and Putin Meet in Shenzhen for Rare Three-Way Talks at APEC',
'{{WORLD_1_SUMMARY}}': "Donald Trump arrived in Shenzhen on Wednesday for the APEC summit. In a break from normal protocol, both Xi Jinping and Vladimir Putin greeted him at the airport. The three leaders are expected to hold three-way talks on Thursday, covering the Iran war, Russia's war in Ukraine and broader strategic stability. Expectations of a concrete outcome are low. Trump is also reported to be holding a separate meeting with Putin, their first since last year's failed Alaska talks. At the welcome banquet, Xi stressed cutting trade restrictions, which matters for Australian exporters.",
'{{WORLD_1_URL}}': 'https://www.cnbc.com/2026/11/18/trump-xi-putin-china-apec.html',
'{{WORLD_2_FLAG}}': '🇹🇷 COP31 · CLIMATE',
'{{WORLD_2_HEADLINE}}': 'COP31 Draft Calls for a Fossil Fuel Phase-Out as Talks Head for a Friday Deadline',
'{{WORLD_2_SUMMARY}}': "The climate talks in Antalya, Türkiye, are due to finish on Friday, but countries are still split on the main text. Australia's Chris Bowen is chairing the negotiations, and the 18-page draft calls for faster action to phase out fossil fuels. Several big producers have pushed back, and the EU's climate envoy Wopke Hoekstra says the draft \"does not go in the right direction\". Bowen says the final text will differ substantially from this draft, and at least one more draft is expected. The United States has sent no official delegation.",
'{{WORLD_2_URL}}': 'https://www.technology.org/2026/11/18/cop31-draft-fossil-fuel-phase-out-antalya-bowen/',
'{{ECON_1_FLAG}}': '💵 WAGES',
'{{ECON_1_HEADLINE}}': 'Wages Rise 1.1% in the Quarter, the Biggest Jump Since Late 2023',
'{{ECON_1_SUMMARY}}': "The ABS Wage Price Index rose 1.1% in the September quarter and 3.5% over the year, its strongest quarterly rise since December 2023. Private sector wages rose 1.0% in the quarter and public sector wages 1.3%. The main driver was the Fair Work Commission's 4.75% rise in award rates from 1 July. Inflation was 4.3% over the year, so wages are still behind prices for a fourth straight quarter. With the RBA watching wages closely, this adds to the case against rate relief. October jobs figures are due at 11:30am today.",
'{{ECON_1_URL}}': 'https://www.abs.gov.au/media-centre/media-releases/highest-quarterly-wage-growth-december-quarter-2023',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Diesel Falls Another 9 Cents in a Week as Wholesale Prices Keep Dropping',
'{{ECON_2_SUMMARY}}': "The ACCC's latest weekly figures put average diesel in the five biggest cities at 266.4 cents a litre, down 9.4 cents in a week and 56 cents below the 31 March peak. Capital-city unleaded averaged about 221 cents, down 13 cents on the week. Wholesale prices are still falling, and the NRMA expects pump prices to follow over the coming week. Pump prices still vary a lot between stations, so compare before you fill up. With Friday looking stormy, today is a good day to fill the truck and compressor.",
'{{TECH_1_FLAG}}': '💻 AI · CHIPS',
'{{TECH_1_HEADLINE}}': "Nvidia Doubles Its Revenue but Rules Out Jensen Huang's Return as CEO",
'{{TECH_1_SUMMARY}}': "Nvidia, which makes most of the chips that train and run AI tools like ChatGPT, reported third-quarter revenue of US$115.8 billion, up 103% on a year ago. On the same day, chair Harvey Jones said the board had unanimously accepted Jensen Huang's resignation and does not plan to reinstate him, despite a petition with more than 180,000 signatures. Huang stepped down last week after reports of extramarital affairs. Interim CEO Colette Kress is in charge, and an independent investigation is under way. The record sales show spending on AI isn't slowing.",
'{{TECH_1_URL}}': 'https://www.cnn.com/2026/11/17/tech/nvidia-earnings-jensen-huang-exit',
'{{TECH_2_FLAG}}': '🏪 AI · SMALL BUSINESS',
'{{TECH_2_HEADLINE}}': "Australian Businesses With Premises Can't Yet Claim Their ChatGPT Listing",
'{{TECH_2_SUMMARY}}': "SmartCompany reports that OpenAI has opened ChatGPT Business Hub listing claims to eligible Australian online businesses, but businesses with physical premises can't claim theirs yet. Business Hub lets owners verify their business, correct details such as hours and services, and see how often ChatGPT mentions them. For a workshop-based business like a blasting yard, that means waiting for now. In the meantime, keep your Google Business Profile and website up to date, because AI tools draw on them when people ask who to call.",
'{{ROBOT_1_FLAG}}': '🦾 INDUSTRIAL ROBOTS',
'{{ROBOT_1_HEADLINE}}': 'Inlif Signs More Than US$10 Million in Orders for Its New Six-Axis Industrial Robots',
'{{ROBOT_1_SUMMARY}}': "Nasdaq-listed Inlif, based in Quanzhou, China, says its next-generation six-axis industrial robots are now on the market, and partners have signed purchase and sales agreements worth more than US$10 million. Six-axis arms are the type used for welding, painting, spraying and machine tending. The announcement is a company claim, and Inlif hasn't said how many units are involved. Cheaper Chinese-built arms like these are making robotic spraying and handling cells more affordable for smaller workshops.",
'{{ROBOT_1_URL}}': 'https://manilatimes.net/2026/11/18/tmt-newswire/globenewswire/inlif-inlf-advances-commercialization-of-its-next-generation-six-axis-industrial-robots-securing-more-than-us10-million-in-partner-purchase-and-sales-agreements/2473102',
'{{AUS_1_HEADLINE}}': "Albanese Takes China's 55% Beef Tariff to APEC",
'{{AUS_1_SUMMARY}}': "Anthony Albanese arrived in China on Wednesday for the APEC summit in Shenzhen. He says he'll raise the 55% tariff Australian beef exporters face now that they have passed their annual quota. He says hitting the quota shows how strong Chinese demand for Australian beef is, and that the government will keep advocating for Australian businesses. Albanese is due to call on Xi Jinping on Friday before meeting Premier Li Qiang in Beijing. Penny Wong is still negotiating with China over iron ore. The outcome matters for export earnings and regional jobs.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-18/federal-politics-live-blog-nov-18/107396066',
'{{AUS_2_HEADLINE}}': 'One Nation Pledges to Scrap Parent Visas and Cut the Humanitarian Intake to 2,000',
'{{AUS_2_SUMMARY}}': "One Nation leader Pauline Hanson has announced plans to scrap the parent visa program and cut Australia's humanitarian intake to 2,000 places a year. The announcement came on Wednesday as migration settings stay a live issue in Canberra, and One Nation holds a key bloc of Senate votes. In the same sitting week, the government's gas reservation bill is still short of support. Penny Wong also announced new sanctions on people and groups linked to settlement expansion in the West Bank.",
'{{VIC_1_HEADLINE}}': 'Development Victoria Sues Lendlease Over the Crumbling Docklands Promenade',
'{{VIC_1_SUMMARY}}': "Development Victoria has taken Supreme Court action against Lendlease over the Victoria Harbour Promenade in Docklands, which has been closed throughout 2026 because of structural problems. The claim concerns allegedly defective wharf structures, including marine worm infestation and deteriorating piles. It seeks damages, indemnity, interest and costs under a 2001 development agreement. The allegations haven't been tested in court. Lendlease points out the promenade was handed over between 2004 and 2014. It shows what poor protection costs on marine structures.",
'{{SCI_1_FLAG}}': '⚡ ENERGY',
'{{SCI_1_HEADLINE}}': "America's Biggest Data Centres Now Use as Much Power as Some US States",
'{{SCI_1_SUMMARY}}': "A Harvard-led study in Nature Sustainability mapped 403 hyperscale data centres across the United States, the giant facilities that run AI and cloud services. It estimates they used 68 to 99 terawatt-hours of electricity a year, roughly as much as some US states, and about 54% of it came from fossil fuels. The authors say the pollution from that generation falls on communities near power stations, although they did not directly measure health effects. With AI use still growing, the study shows where its energy actually comes from.",
'{{INSIGHT_TITLE}}': 'Let AI Check Your Bank Statements for Fees You Never Agreed To',
'{{INSIGHT_BODY}}': "ASIC is suing CommBank, alleging that about 42,000 business customers were charged CommBiz fees they were never properly told about, many of them 25 cents at a time. Small fees like that are easy to miss in a busy month. Export the last three months of business bank and merchant statements as CSV and remove the account numbers. Then ask ChatGPT, Claude or Gemini to list every fee by type and how often it appears, and to flag anything new, duplicated or changed. Compare that list with your bank's current fee schedule. If something doesn't match, raise it with the bank in writing. Even a few dollars a week adds up over a year.",
'{{FACT_1}}': "Australian wages rose 1.1% in the September quarter, the biggest quarterly rise since December 2023.",
'{{FACT_2}}': "A Harvard-led study estimates America's 403 hyperscale data centres used 68 to 99 terawatt-hours of electricity, with about 54% from fossil fuels.",
'{{FACT_3}}': "The first major data release from Europe's Euclid space telescope turned up about 15,000 new candidate gravitational lenses, the largest collection yet.",
'{{JOKE_SETUP}}': "Why wasn't the crane operator surprised by the wage figures?",
'{{JOKE_PUNCHLINE}}': "He's spent his whole career watching things go up slowly, one careful lift at a time.",
'{{CLOSING_QUOTE}}': '"Beware of little expenses; a small leak will sink a great ship."',
'{{CLOSING_ATTR}}': '— Benjamin Franklin',
'{{CLOSING_MESSAGE}}': "It's a warm Thursday and the last dry day before Friday's storms, so get outdoor coating work finished early. The jobs figures land at 11:30am, wages are rising faster than they have in nearly three years, and diesel is still falling. While the rain keeps you inside tomorrow, it's worth going through your bank fees. Have a productive Thursday.",
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
