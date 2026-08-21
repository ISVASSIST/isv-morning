#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 22 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 22 Aug (BOM)
    "{{WEATHER_1}}": "SAT 22 · ☁️ Cloudy, slight chance of a shower · 7–16°C",
    "{{WEATHER_2}}": "SUN 23 · 🌦️ Showers, most likely morning and afternoon · 8–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 24 · 🌧️ Cloudy, medium chance of showers · 11–18°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 25 · ⛅ Partly cloudy, isolated shower · 9–14°C",
    "{{WEATHER_5}}": "WED 26 · ☁️ Mostly cloudy, chance of a shower easing · 8–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or Carrum Downs — only minor to moderate flood warnings remain, for the Avoca, Kiewa, Loddon and Ovens/King Rivers well north of the city. With showers likely through the weekend into Monday, Tuesday or Wednesday is the better window for any exterior coating or blasting work that needs a dry surface.",

    # World
    "{{WORLD_1_FLAG}}": "🇵🇪 PERU · POWERFUL QUAKE SHAKES SOUTHERN ANDES",
    "{{WORLD_1_HEADLINE}}": "Magnitude 6.7 Earthquake Rattles Peru's Southern Andes",
    "{{WORLD_1_SUMMARY}}": "A magnitude 6.7 earthquake struck at an intermediate depth of 108km near Coracora in Peru's Ayacucho region on Thursday, injuring at least two people and damaging homes, health centres and schools across the Ica and Arequipa regions. Peru's position on the Pacific Ring of Fire means the country is well drilled for seismic events, and authorities reported no major structural collapse despite the quake's strength.",
    "{{WORLD_1_URL}}": "https://www.washingtonpost.com/world/2026/08/20/peru-earthquake-andes-mountains/c56dfb8e-9cc6-11f1-9cc4-2dc9b46e2d5c_story.html",

    "{{WORLD_2_FLAG}}": "🏴‍☠️ YEMEN · SOMALI PIRACY AT A 10-YEAR HIGH",
    "{{WORLD_2_HEADLINE}}": "Somali Pirates Hijack Suspected Iranian Shadow-Fleet Tanker Off Yemen",
    "{{WORLD_2_SUMMARY}}": "Gunmen seized the Eritrean-flagged tanker SIBU 1 roughly 136 nautical miles off the Yemeni port of Al-Mukalla, the second hijacking in the region in four days and possibly the fifteenth of the year, according to maritime trackers. Analysts say the surge — the worst in over a decade — is being fuelled by regional conflict pulling naval patrols away from anti-piracy duties.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/8/20/gunmen-seize-tanker-off-yemen-amid-resurgence-of-somali-piracy",

    # Economics
    "{{ECON_1_FLAG}}": "💵 CURRENCY · AUD HITS 11-WEEK HIGH",
    "{{ECON_1_HEADLINE}}": "Australian Dollar Extends Longest Winning Streak Since 2020",
    "{{ECON_1_SUMMARY}}": "The Aussie pushed to an 11-week high of US$0.7134 on Friday, its eighth straight weekly gain, as a global bond sell-off and a failed US Treasury buyback plan kept the US dollar under pressure. A stronger dollar cuts both ways for a small business — cheaper imported gear and consumables, but it also chips away at the competitiveness of any export-exposed customers on your books.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-08-21/asx-markets-business-live-news-august-21-2026/107061908",

    "{{ECON_2_FLAG}}": "📊 FEDERAL BUDGET · DEBT PASSES $1 TRILLION",
    "{{ECON_2_HEADLINE}}": "Australia's Gross Debt Ticks Over $1 Trillion for the First Time",
    "{{ECON_2_SUMMARY}}": "The Australian Office of Financial Management issued a further $4.1 billion of debt on Thursday, tipping the Commonwealth's total borrowings past $1,000.8 billion — about 34% of GDP — almost twenty years to the week after the Howard government declared net debt eliminated. It's a symbolic milestone more than an immediate cost, but it adds weight to the case that further RBA rate cuts are further away than businesses carrying loans might like.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💳 RETAIL · WALMART FINALLY GOES CONTACTLESS",
    "{{TECH_1_HEADLINE}}": "Walmart to Accept Apple Pay and Google Pay Across US Stores",
    "{{TECH_1_SUMMARY}}": "After a decade of favouring its own in-house Walmart Pay system, the retail giant confirmed Friday it will roll out contactless tap-to-pay — including Apple Pay and Google Pay — to all US stores and Sam's Club locations by year's end, starting at select sites from 24 August. Even the biggest holdouts eventually cave to the payment method customers actually want — worth a thought if your own EFTPOS setup is still card-only.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/08/21/walmart-to-finally-start-accepting-apple-pay-and-google-pay/",

    "{{TECH_2_FLAG}}": "🤖 WORKPLACE AI · GOOGLE CHAT GETS AN AI BRAIN",
    "{{TECH_2_HEADLINE}}": "Google Rolls Out \"Ask Gemini\" Inside Google Chat",
    "{{TECH_2_SUMMARY}}": "Google has begun replacing Google Chat's old side panel with \"Ask Gemini,\" letting Workspace users search across Gmail, Drive and Calendar, generate images and manage events without leaving a conversation. It's rolling out to Business and Enterprise Workspace tiers now, with usage limits relaxed until 1 October so teams can properly test it before the meter starts running.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🚜 INDUSTRIAL AUTOMATION · SELF-DRIVING YARD GEAR",
    "{{ROBOT_1_HEADLINE}}": "Agtonomy's Autonomy Platform Learns to Reverse Into Tight Spaces on Its Own",
    "{{ROBOT_1_SUMMARY}}": "Agtonomy has added fully autonomous multi-point turning to its commercial off-road autonomy platform, letting retrofitted Kubota and Bobcat equipment execute complex manoeuvres in tight headland spaces without a driver. Each vehicle now streams more than two terabytes of field data per hour back to the platform — a sign of how fast heavy equipment autonomy is moving from open paddocks toward the tighter, more cluttered spaces every trades yard actually has to deal with.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/agtonomy-releases-new-autonomous-multi-point-turning-features/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Origin Energy Confirms Hacker Accessed Full Bank Details of 60 Customers",
    "{{AUS_1_SUMMARY}}": "Origin Energy's investigation into a July data breach has confirmed a hacker accessed the complete bank account numbers of around 60 customers and ID document numbers for 100 more, out of roughly 900,000 people affected overall. Authorities have traced the attack to a former contractor linked to a Manila call centre — a reminder that even a giant utility's customer database isn't bulletproof, let alone a small business running its books on a shared laptop.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-21/origin-energy-hack-update-60-customers-bank-account-access/107062636",

    "{{AUS_2_HEADLINE}}": "Flannel Flower Crowned Australia's Favourite Wildflower",
    "{{AUS_2_SUMMARY}}": "The flannel flower took out National Science Week's wildflower poll with 16,567 of the roughly 70,000 votes cast, narrowly beating the flying duck orchid into second place. Despite looking like a daisy, it's actually a relative of carrots and parsley — one of 14 Australian species in a plant family better known for what's on the dinner plate than what's growing on the east coast scrub.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Regulator Orders Childcare Giant to Shut 65 Centres Overnight",
    "{{VIC_1_SUMMARY}}": "The Victorian Early Childhood Regulatory Authority has suspended Ignite Minds Family Day Care for 90 days and stood down four educators, after an inspection blitz found unresolved fencing, sleeping-safety and strangulation risks the regulator had already flagged. It's a sharp reminder of how quickly a Victorian regulator will shut a business down when compliance notices go unresolved.",

    # Science
    "{{SCI_1_FLAG}}": "🏃 EXERCISE SCIENCE · THE POWER OF A SHORT, SHARP EFFORT",
    "{{SCI_1_HEADLINE}}": "Three Minutes of Sprinting Beats 90 Minutes of Moderate Exercise, Study Finds",
    "{{SCI_1_SUMMARY}}": "Rockefeller University researchers found that six 30-second all-out sprints altered nearly a quarter of the proteins measured in participants' blood and more than 200 metabolites, compared with barely a quarter of one per cent after 90 minutes of steady cycling. Many of the affected proteins are linked to lower risk of obesity and type 2 diabetes — welcome news for anyone whose idea of a workout is sprinting for the ute when it starts raining on an uncovered load.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The Robots Making Headlines Aren't Coming for Your Ute Yet — But Your Paperwork Should Already Be Automated",
    "{{INSIGHT_BODY}}": "This week's robotics news is a two-tonne autonomous forklift teaching itself to reverse into tight loading docks — genuinely impressive engineering, but years away from anything that helps a two-truck coatings business on a Tuesday morning. The AI that actually moves the needle for an operation like ISV is far less glamorous: a model that drafts your quotes, chases overdue invoices, and turns a stack of job-site photos into a client report before you've finished your coffee. Chasing the flashiest new robot headline is a distraction — picking one reliable AI tool and using it on the same task every single day is what actually pays back.",

    # Fun facts
    "{{FACT_1}}": "The first robot built in Japan, Gakutensoku, was unveiled in 1929 by biologist Makoto Nishimura — powered entirely by compressed air, it could change its facial expression and move its head and hands, decades before anyone coined the term \"robotics.\"",
    "{{FACT_2}}": "Canada holds more natural lakes than the rest of the world combined — roughly two million of them, holding close to a fifth of the planet's fresh surface water.",
    "{{FACT_3}}": "Female sharks have evolved noticeably thicker skin than males of the same species — up to twice as thick in some — because males often bite down on females to hold on during mating.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the deck builder's small business never wobble, even in a tough economy?",
    "{{JOKE_PUNCHLINE}}": "Because everything he built started with solid foundations.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Done is better than perfect.\"",
    "{{CLOSING_ATTR}}": "— Sheryl Sandberg",
    "{{CLOSING_MESSAGE}}": "Showers are on the cards through the weekend and into Monday in Carrum Downs, so if there's exterior coating work that needs a dry surface, Tuesday or Wednesday is shaping up as the better window. Between Origin Energy's breach update, Walmart finally catching up on tap-to-pay, and a childcare operator losing 65 centres overnight for letting compliance slide, it's a Saturday that's a decent nudge to check your own paperwork and payment systems are as tidy as your tools.",
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
