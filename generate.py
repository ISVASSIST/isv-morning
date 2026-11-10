#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 11 November 2026',
'{{WEATHER_1}}': 'WED 11 NOV · ⛅ Mild and mostly dry, about 13-20°C, low rain chance',
'{{WEATHER_2}}': 'THU 12 NOV · ☀️ Mostly dry and sunny, per Weatherzone',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'FRI 13 NOV · 🌦️ Mostly dry; one model shows a little rain (about 1-2 mm)',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SAT 14 NOV · ☀️ Dry and mostly sunny, per Weatherzone',
'{{WEATHER_5}}': 'SUN 15 NOV · 🌧️ Wettest day of the run, patchy rain likely',
'{{WEATHER_ALERT}}': "Mild and mostly dry from today through Saturday, then rain looks most likely on Sunday. These are Melbourne figures from aggregator sites (Weatherzone, yr.no, timeanddate), not BoM and not Carrum Downs, and they don't agree on today's top temperature (17-20°C) or on Friday's rain, so check BoM before locking in outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 IRAN',
'{{WORLD_1_HEADLINE}}': 'Qatar Says It Sees Progress in US-Iran Talks After White House Meeting',
'{{WORLD_1_SUMMARY}}': "Euronews reports Qatar's prime minister called the talks positive after meeting Trump. The reported framework would have Iran reopen the Strait of Hormuz in exchange for sanctions relief, with nuclear talks to follow. Rubio still says it's not on the verge of a breakthrough, and Iranian officials are giving mixed messages. I only saw search summaries, not the full article.",
'{{WORLD_1_URL}}': 'https://www.euronews.com/2026/11/10/qatar-sees-progress-in-us-iran-talks-after-white-house-meeting',
'{{WORLD_2_FLAG}}': '🌍 UKRAINE',
'{{WORLD_2_HEADLINE}}': 'New Round of Russia-US-Ukraine Talks Opens in Abu Dhabi',
'{{WORLD_2_SUMMARY}}': "Xinhua reports a new round of three-way talks began in Abu Dhabi on Tuesday, and media reports say the first day has ended. UNITED24 says China pushed at the UN Security Council for a binding peace deal and backed the talks, which are scheduled for 10 to 11 November. No outcome has been reported yet, and I only saw headlines and summaries.",
'{{WORLD_2_URL}}': 'https://united24media.com/world/china-calls-for-binding-ukraine-peace-deal-ahead-of-abu-dhabi-talks-24218',
'{{ECON_1_FLAG}}': '🛢️ OIL',
'{{ECON_1_HEADLINE}}': 'Brent Crude Dips Below US$90 for the First Time Since August',
'{{ECON_1_SUMMARY}}': "CNBC reports Brent hit an intraday low of US$89.03 a barrel on 10 November on hopes the Iran war could wind down, about 22% below its late-October peak near US$118. It bounced back into the low $90s later in the session. If it holds, diesel should ease over the coming weeks, but a single bad headline from the Gulf could reverse it.",
'{{ECON_1_URL}}': 'https://www.cnbc.com/2026/11/10/oil-prices-trump-iran.html',
'{{ECON_2_FLAG}}': '📉 BUSINESS',
'{{ECON_2_HEADLINE}}': 'NAB Survey: Business Conditions Slip Into Negative Territory as Costs Bite',
'{{ECON_2_SUMMARY}}': "An ITBrief write-up of the latest NAB survey says conditions slipped to -2, with higher oil prices and borrowing costs squeezing retail and housing-linked firms while mining holds up. Brokerdaily notes the gap between input and selling prices is widest in construction and manufacturing. I couldn't confirm which month's survey this is, so treat the figures with care.",
'{{TECH_1_FLAG}}': '🤖 AI · AGENTS',
'{{TECH_1_HEADLINE}}': 'Skyfall AI Moves to Let an AI System Run a Small Business It Buys',
'{{TECH_1_SUMMARY}}': "The startup plans to buy a small software or e-commerce business for up to US$1 million and hand an AI system pricing, marketing, support and finance, with humans stepping back over time. A 10 November roundup says it has launched cooperating agents for the job, but other reports say no purchase has closed yet. It's an experiment to watch, not a model to copy yet.",
'{{TECH_1_URL}}': 'https://thelogic.co/briefing/skyfall-ai-wants-to-buy-a-small-tech-business-and-run-it-with-ai/',
'{{TECH_2_FLAG}}': '🤖 AI · TOOLS',
'{{TECH_2_HEADLINE}}': 'New AI Tools Keep Landing: Meta Spaces, Cheaper Claude and an Agent "Kill Switch"',
'{{TECH_2_SUMMARY}}': "Weekly roundups from 8-9 November list Meta's Spaces (build custom AI tools from a plain-English description in its Muse app), Anthropic's cheaper Fable 5.2, and a CrowdStrike kill switch for misbehaving AI agents. The practical takeaway: tools are getting cheaper and easier, and so are the controls to switch them off. Several of these come from aggregators, so check the official pages.",
'{{ROBOT_1_FLAG}}': '🛰️ SPACE ROBOTICS',
'{{ROBOT_1_HEADLINE}}': "Caltech's ASTRA Robot Builds Part of a Structure in Orbit, a Claimed First",
'{{ROBOT_1_SUMMARY}}': "A roughly one-cubic-metre robotic workshop picked struts and joints from onboard dispensers and assembled a section of an antenna frame in space, with ground engineers checking each step by photo. The team says it is unlikely to finish all 11 sections before the mission ends in December. It's simple, repeatable automation, not AI improvising, which is exactly how industrial robots earn their keep too.",
'{{ROBOT_1_URL}}': 'https://lifeboat.com/blog/2026/11/robot-successfully-builds-space-structure-in-first-autonomous-construction-demo',
'{{AUS_1_HEADLINE}}': 'Qantas Lay-Offs Show the Tourism Industry Grappling With AI',
'{{AUS_1_SUMMARY}}': "An ABC analysis on its homepage ties Qantas job cuts to the wider tourism industry's struggle with AI. Earlier this year the Australian Services Union disputed Qantas head-office redundancies it linked to AI, which Qantas denied was the direct cause. I only saw the headline, not the analysis itself.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/',
'{{AUS_2_HEADLINE}}': "Pilbara Traditional Owners Say Woodside's $50 Billion Browse Project Should Not Go Ahead",
'{{AUS_2_SUMMARY}}': "An ABC Kimberley and Pilbara briefing on 10 November reports a group of traditional owners wants the offshore gas project stopped or delayed. It comes a day after an analyst warned stalled power projects in South-East Asia put Woodside at risk. I only saw the briefing summary.",
'{{VIC_1_HEADLINE}}': 'One Nation Dumps Its Preston Candidate Over Hitler Comments',
'{{VIC_1_SUMMARY}}': "ABC reports One Nation dropped Franco Guardiani after social media posts that appeared to praise Hitler. It puts the Coalition's deal to preference One Nation ahead of Labor under more scrutiny. Antony Green counts 734 lower-house candidates for 88 seats, and early voting opens on 18 November ahead of the 28 November poll.",
'{{SCI_1_FLAG}}': '😊 PSYCHOLOGY',
'{{SCI_1_HEADLINE}}': "Forcing a Smile Can Backfire, a University of Florida Study Finds",
'{{SCI_1_SUMMARY}}': "Research reported on 9 November found a single posed smile gave a small mood lift, but repeated smiling, or smiling under threat of lower pay, sometimes left people less happy and more irritated. The work appears in the Journal of Experimental Social Psychology. I couldn't confirm the reported sample of about 1,100 people.",
'{{INSIGHT_TITLE}}': 'Let AI Draft a One-Page Site Induction Sheet for New Workers and Subbies',
'{{INSIGHT_BODY}}': "Every new casual or subbie needs the same briefing: site rules, PPE, emergency contacts, who to call, where the gear lives, and what not to touch. Give an AI tool your existing notes and SWMS and ask it to turn them into a single plain-English page, with a short checklist at the bottom to sign. Check every safety detail yourself before it's used, because the AI can invent things that sound right. Print it, laminate it, and hand it over on day one.",
'{{FACT_1}}': "Brent crude hit an intraday low of US$89.03 a barrel on 10 November, its lowest level since August, according to CNBC.",
'{{FACT_2}}': "Caltech's ASTRA robot workshop is about one cubic metre, and the full antenna frame it is building in orbit needs 11 sections.",
'{{FACT_3}}': "ABC election analyst Antony Green counts 734 lower-house candidates for Victoria's 88 seats, an average of 8.3 per seat.",
'{{JOKE_SETUP}}': "Why did the carpet layer's bookkeeper sleep so well at tax time?",
'{{JOKE_PUNCHLINE}}': '"Because nothing ever got swept under the rug."',
'{{CLOSING_QUOTE}}': '"They shall grow not old, as we that are left grow old."',
'{{CLOSING_ATTR}}': '— Laurence Binyon, For the Fallen',
'{{CLOSING_MESSAGE}}': "It's Remembrance Day, so take a minute at 11am if you can. The weather looks mild and dry through Saturday, a good stretch for outdoor jobs before Sunday's rain. Oil dipped under US$90 overnight, so diesel may finally start easing.",
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
