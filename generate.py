#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 10 November 2026',
'{{WEATHER_1}}': 'TUE 10 NOV · ⛅ Mostly sunny, about 11-28°C, slight late shower chance',
'{{WEATHER_2}}': 'WED 11 NOV · ☁️ Cloudy, about 14-18°C, slight morning shower chance',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'THU 12 NOV · ❓ Not confirmed in my sources, check BoM',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'FRI 13 NOV · ❓ Not confirmed in my sources, check BoM',
'{{WEATHER_5}}': 'SAT 14 NOV · ❓ Not confirmed; one undated source says dry and sunny',
'{{WEATHER_ALERT}}': 'Warm and mostly sunny today, up near 28°C with a small chance of a late shower, then a cooler cloudy day Wednesday. These are Melbourne figures from weather aggregator sites, not BoM and not Carrum Downs, and they differ slightly between sources, so check BoM before scheduling outdoor work. I could not confirm Thursday to Saturday.',
'{{WORLD_1_FLAG}}': '🌍 IRAN',
'{{WORLD_1_HEADLINE}}': 'Trump Meets Qatar PM as Rubio Says Iran Talks Are Not Close to a Deal',
'{{WORLD_1_SUMMARY}}': "Fox News reports Trump met Qatar's prime minister, a key mediator, while Secretary of State Rubio said he wouldn't call it a breakthrough. A CNN explainer says the US and Iran are negotiating quietly with no deal announced and the Strait of Hormuz still disrupted. Reports conflict on how close the sides are, and I only saw search summaries.",
'{{WORLD_1_URL}}': 'https://www.foxnews.com/world/trump-meets-key-iran-war-mediator-uae-reveals-major-oil-export-surge-despite-conflict',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'US and Iran Are Quietly Negotiating as the Middle East Stays on Edge, CNN Explains',
'{{WORLD_2_SUMMARY}}': "CNN's 9 November explainer says Iran is holding publicly firm, demanding an end to the war on all fronts and the lifting of the maritime blockade, while Axios reports it has offered to reopen the strait and move toward nuclear inspections first. The Revolutionary Guard also reported tankers burned in the strait. I saw only a summary of the article, so details may differ.",
'{{WORLD_2_URL}}': 'https://www.cnn.com/2026/11/09/middleeast/iran-us-talks-explainer-intl',
'{{ECON_1_FLAG}}': '⛽ FUEL',
'{{ECON_1_HEADLINE}}': 'Retail Petrol and Diesel Slip Again, but Diesel Is Still Near 278 Cents',
'{{ECON_1_SUMMARY}}': "FuelRadar's 7 November data puts the national average at 234.3 cents a litre for unleaded 91, down 5.5c on the week, and 278.0 for diesel, down 4.0c. Wholesale petrol fell 13.7c to 211.5 over five days, though diesel doesn't follow the petrol cycle, so there's no reliable low to wait for. This is an aggregator figure seen through a search summary.",
'{{ECON_1_URL}}': 'https://fuelradar.com.au/fuel-data',
'{{ECON_2_FLAG}}': '🛢️ OIL',
'{{ECON_2_HEADLINE}}': 'Oil Prices Fall as Markets Open After Trump Says New Iran Strikes Unlikely',
'{{ECON_2_SUMMARY}}': "A search summary says oil fell at Monday's open after Trump said renewed attacks were highly unlikely if talks progress. Lower crude would eventually ease diesel and freight costs, but Trump has also hinted at resuming strikes, so it could reverse quickly. I couldn't open the original report.",
'{{TECH_1_FLAG}}': '🤖 AI · ANTHROPIC',
'{{TECH_1_HEADLINE}}': 'Anthropic Launches Fable 5.2 With a Price Cut',
'{{TECH_1_SUMMARY}}': "The New Stack reports Anthropic released Fable 5.2 and Mythos 5.2, with Fable pricing cut from US$10/$50 to US$8/$40 per million input/output tokens and availability on AWS, Google Cloud and Azure. Mythos stays limited to verified organisations. Cheaper models help tools built on them, though I couldn't confirm the exact launch date or any effect on consumer plans.",
'{{TECH_1_URL}}': 'https://thenewstack.io/anthropic-fable-coding-upgrade',
'{{TECH_2_FLAG}}': '🤖 AI · POLICY',
'{{TECH_2_HEADLINE}}': 'Google and Microsoft Join OpenAI and Anthropic in Backing a robots.txt Signal for AI Training',
'{{TECH_2_SUMMARY}}': "Mezha reports the four companies now back a shared opt-out signal that lets website owners say whether their content can be used to train AI. Only Anthropic says it already honours it, and OpenAI hasn't given a date. Worth knowing if you run your own business website. I only saw a summary of this report.",
'{{ROBOT_1_FLAG}}': '🤖 INDUSTRIAL ROBOTS',
'{{ROBOT_1_HEADLINE}}': "China Blocks SoftBank's Planned Acquisition of ABB Robotics",
'{{ROBOT_1_SUMMARY}}': "The Robot Report says ABB Robotics confirmed China's foreign investment security review office has blocked SoftBank's planned purchase, with experts framing it around concerns over robot data and AI. It shows how strategic industrial robots have become. I only saw a search summary, not the full article.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/industry-experts-discuss-china-blocking-softbank-acquisition-abb-robotics/',
'{{AUS_1_HEADLINE}}': 'Independent MP Helen Haines Stable After Being Struck by a Car Outside Her Office',
'{{AUS_1_SUMMARY}}': "ABC regional briefings on 9 November say Haines' condition has improved and she is now stable after the incident outside her electorate office. I only saw a briefing summary, so I have no details on the circumstances.",
'{{AUS_1_URL}}': 'https://abc.net.au/news/2026-11-09/central-victoria-local-news-briefing/107362220',
'{{AUS_2_HEADLINE}}': 'Analyst Warns Stalled Power Projects in South-East Asia Put Woodside at Risk',
'{{AUS_2_SUMMARY}}': "An ABC briefing item on 9 November says an analyst believes cancelled and stalled power projects in South-East Asia put Australia's largest gas producer at risk. It matters for energy markets more than the bowser directly. I only saw the one-line summary.",
'{{VIC_1_HEADLINE}}': 'BoM Says Victoria\'s South-West Coast May Have a Slightly Drier Rest of Spring',
'{{VIC_1_SUMMARY}}': "An ABC regional briefing on 9 November reports the Bureau of Meteorology outlook for a slightly drier remainder of spring on Victoria's south-west coast. That's the south-west, not Melbourne, so treat it as a regional guide only. I only saw a one-line summary.",
'{{SCI_1_FLAG}}': '🌳 ECOLOGY',
'{{SCI_1_HEADLINE}}': 'Thirty-Five Years of Research Link Acorn Crops to Lyme Disease Risk',
'{{SCI_1_SUMMARY}}': "ScienceDaily carries a 9 November item on more than 35 years of research into what drives Lyme disease risk, with acorns a headline factor. The date was partly truncated in my search results and I haven't read the study, so the details are unconfirmed.",
'{{INSIGHT_TITLE}}': 'Let AI Draft a Scope-Confirmation Message Before You Start Any New Job',
'{{INSIGHT_BODY}}': "Most disputes start with a vague quote. Paste your quote and site notes into an AI tool and ask it to write a short, plain-English message listing what's included, what's excluded, access needs, and what happens if conditions differ. Send it to the customer before the first day and ask for a reply to confirm. Read it carefully first, because the AI can add things you never agreed to. Five minutes up front can save an argument over a variation later.",
'{{FACT_1}}': "Anthropic's Fable price drops from US$10/$50 to US$8/$40 per million input/output tokens with the 5.2 release, according to The New Stack.",
'{{FACT_2}}': 'North American robot orders rose 24.8% in Q3 2026, according to A3 as shown on The Robot Report homepage.',
'{{FACT_3}}': "FuelRadar's 7 November figures put the national average diesel price at 278.0 cents a litre, down 4.0c in a week.",
'{{JOKE_SETUP}}': 'Why did the sparky quote the job in pencil?',
'{{JOKE_PUNCHLINE}}': '"Because the customer kept saying the budget was flexible, and he wanted to be ready."',
'{{CLOSING_QUOTE}}': '"A good plan violently executed now is better than a perfect plan next week."',
'{{CLOSING_ATTR}}': '— George S. Patton',
'{{CLOSING_MESSAGE}}': "Today is the warmest day of the week, near 28°C, before a cooler cloudy Wednesday, so get the outdoor work done this afternoon. Oil eased overnight, but the Iran talks are still unsettled, so keep an eye on fuel before you quote.",
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
