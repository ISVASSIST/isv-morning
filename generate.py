#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 28 October 2026',
'{{WEATHER_1}}': 'WED 28 OCT · 🌦️ Cloudy, medium chance of showers, mostly afternoon and evening · max 18°C',
'{{WEATHER_2}}': 'THU 29 OCT · ☁️ Cloudy, slight chance of a morning shower · max 19°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'FRI 30 OCT · ⛅ Partly cloudy, mostly dry · max 25°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SAT 31 OCT · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_5}}': 'SUN 1 NOV · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Showers are most likely this afternoon and evening, so get exterior coating and blasting done early or hold it for Thursday and Friday, which look mostly dry. Wednesday to Friday are from the Bureau of Meteorology's Melbourne forecast, not a Carrum Downs-specific page, and I couldn't confirm minimums or the weekend, so check BoM before committing to outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 SAUDI ARABIA · IRAN',
'{{WORLD_1_HEADLINE}}': "Saudi, Turkish and Pakistani Officials Hold Rare Talks in Tehran as Houthis Claim New Strikes",
'{{WORLD_1_SUMMARY}}': "The four countries agreed to keep talking, with Riyadh saying the visit aims to prevent a return to military escalation. The Houthis claim they hit pumping stations on Saudi Arabia's East-West pipeline and Riyadh's airport, which Saudi Arabia hasn't confirmed. The pipeline is the main route around Hormuz, so this feeds straight into fuel prices.",
'{{WORLD_1_URL}}': 'https://www.ynetnews.com/article/r1benganfg',
'{{WORLD_2_FLAG}}': '🌍 EGYPT · SAUDI ARABIA',
'{{WORLD_2_HEADLINE}}': "Egypt's Parliament Authorises President Sisi to Take 'All Necessary Measures' to Help Defend Saudi Arabia",
'{{WORLD_2_SUMMARY}}': "The vote could draw Cairo directly into the fighting between Saudi Arabia and the Houthis. This comes from a single search summary and I couldn't open the original, so treat the details as unverified until more outlets confirm.",
'{{WORLD_2_URL}}': 'https://www.cbsnews.com/live-updates/iran-war-trump-us-diplomacy-oil-prices-strait-of-hormuz/',
'{{ECON_1_FLAG}}': '🛢️ OIL · BRENT',
'{{ECON_1_HEADLINE}}': 'Brent Holds Around US$115–116 as Hormuz Tanker Attacks Offset Tehran Diplomacy',
'{{ECON_1_SUMMARY}}': "Reuters-sourced reports had Brent near US$116 and WTI near US$102 on Tuesday, after touching its highest since April above US$117 last week. Oman also said talks with Iran produced an outline to restore free navigation in Hormuz, though I only found a single line on it. Diesel stays exposed either way.",
'{{ECON_1_URL}}': 'https://www.cnbc.com/amp/2026/10/21/oil-price-today-wti-brent-rise-on-middle-east-worries.html',
'{{ECON_2_FLAG}}': '⛽ FUEL · DIESEL',
'{{ECON_2_HEADLINE}}': 'Retail Diesel Eases Slightly but Wholesale Prices Keep Climbing',
'{{ECON_2_SUMMARY}}': "The ACCC's weekly report put five-city retail diesel at 276.6 cents a litre on 21 October, down about 1.9 cents on the week. Sydney terminal gate diesel was 267.7 cents on 27 October, up from 263.1 on 21 October, so pump prices may not keep falling. Worth building into quotes for longer jobs.",
'{{TECH_1_FLAG}}': '🤖 AI · BUSINESS',
'{{TECH_1_HEADLINE}}': "Google Rolls Out Gemini Marketing and Finance Skills and Connected Apps for Small Businesses",
'{{TECH_1_SUMMARY}}': "Google says a business landing page, marketing and finance skills and new connected apps are rolling out over the coming days to all Gemini app users. I couldn't confirm the exact announcement date, so it may be a little older than 48 hours. Handy to test on quoting follow-ups and cashflow questions.",
'{{TECH_1_URL}}': 'https://blog.google/innovation-and-ai/products/gemini-app/new-tools-small-business-owners/',
'{{TECH_2_FLAG}}': '🤖 AI · AGENTS',
'{{TECH_2_HEADLINE}}': "Meta Releases a Small-Business Version of Its Muse AI Agent",
'{{TECH_2_SUMMARY}}': "Meta's agent can draft ad campaigns, analyse social media performance and manage content creation. Date unconfirmed from my search, so treat it as recent rather than today's news. Only worth a look if you advertise on Facebook or Instagram.",
'{{ROBOT_1_FLAG}}': '🤖 HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': "Tesla Reportedly Begins Optimus Humanoid Production in Fremont, in an Early Ramp Phase",
'{{ROBOT_1_SUMMARY}}': "This comes from a 26 October press release by a third party, YYForce, relaying Tesla's statement, so it is secondhand. Tesla said hardware and manufacturing processes will keep evolving during the ramp. Treat the output claims with caution until Tesla gives numbers.",
'{{ROBOT_1_URL}}': 'https://www.globenewswire.com/news-release/2026/10/26/3388177/0/en/yyforce-applauds-tesla-and-elon-musk-on-commencing-manufacturing-of-optimus-humanoid-robots.html',
'{{AUS_1_HEADLINE}}': "Senate Probes $6 Million Marrickville Golf Club Grant in Albanese's Electorate",
'{{AUS_1_SUMMARY}}': "The Senate has launched an inquiry into the $560 million community infrastructure grants program. Albanese says the money addresses flood-related sewage problems, though the club's own breakdown lists a clubhouse redevelopment, stormwater harvesting and a botanical garden. Albanese and Catherine King declined to appear.",
'{{AUS_1_URL}}': 'https://www.golfaustralia.com.au/news/albaneses-6m-golf-club-grant-under-scrutiny-628783',
'{{AUS_2_HEADLINE}}': "Department Officials Reject Albanese's Sewerage Explanation as Senate Estimates Runs",
'{{AUS_2_SUMMARY}}': "ABC's 27 October live blog reports officials rejecting the PM's claim that the grant was partly to fix sewerage. The same day One Nation's Barnaby Joyce said the party will vet its satirical cartoons 'more often' after concerns about online content.",
'{{VIC_1_HEADLINE}}': "Business Council Names Victoria the Worst State for Business, Weeks Before the Election",
'{{VIC_1_SUMMARY}}': "ABC reports the Business Council's latest ranking, which has placed Victoria last before, though critics say it measures tax and regulation settings rather than actual investment. I could only see the headline, not the full article. The state election is on 28 November.",
'{{SCI_1_FLAG}}': '💡 PHYSICS',
'{{SCI_1_HEADLINE}}': "A Tiny Laser Beam Could Make Computer Memory 1,000 Times Faster",
'{{SCI_1_SUMMARY}}': "UC San Diego researchers reported a way to store digital data with light instead of magnets, which could make memory faster and more energy-efficient. ScienceDaily, 25–27 October. Early lab work, so don't expect it in your next laptop.",
'{{INSIGHT_TITLE}}': "Let AI Chase Your Overdue Invoices Politely",
'{{INSIGHT_BODY}}': "Cashflow is where small trades businesses get squeezed, especially with fuel and rates up. Paste your overdue invoice list, with names, amounts and days overdue, into an AI tool and ask for three reminder emails: friendly, firm and final. Check each one for tone and the figures before sending, and keep customer details out of the tool if you can. Fifteen minutes a week on this tends to pull payments forward without a single awkward phone call.",
'{{FACT_1}}': "Australia's fuel excise is 53.7 cents a litre before GST, and GST is then charged on top of the whole price.",
'{{FACT_2}}': "Saudi Arabia's East-West pipeline carries roughly 70% of Riyadh's crude exports to Yanbu on the Red Sea, bypassing the Strait of Hormuz.",
'{{FACT_3}}': "Australian five-city diesel peaked at 322.4 cents a litre on 31 March this year, according to the ACCC.",
'{{JOKE_SETUP}}': "Why did the forklift driver win Employee of the Month?",
'{{JOKE_PUNCHLINE}}': '"He was always lifting everyone\'s spirits and never once dropped the ball."',
'{{CLOSING_QUOTE}}': '"Tough times never last, but tough people do."',
'{{CLOSING_ATTR}}': '— Robert H. Schuller',
'{{CLOSING_MESSAGE}}': "Showers are likely this afternoon and evening, so get the outdoor jobs done this morning and leave the shed work for later. Thursday and Friday look drier, which is a good window to book in anything that needs to be outside.",
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
