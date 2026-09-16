#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 17 September 2026",

    # Weather — Carrum Downs / Melbourne bayside, 5-day from Thu 17 Sep
    "{{WEATHER_1}}": "THU 17 SEP · ☁️ Cloudy, slight chance of a shower easing during the day, light winds · 9–15°C",
    "{{WEATHER_2}}": "FRI 18 SEP · ☀️ Sunny, morning fog possible near the hills, winds becoming N–NW 15–25km/h · 7–22°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SAT 19 SEP · ☀️ Sunny, winds northerly 20–30km/h · 12–25°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SUN 20 SEP · 🌦️ Partly cloudy, medium chance of showers, winds N–NW shifting SW 15–25km/h · 14–24°C",
    "{{WEATHER_5}}": "MON 21 SEP · 🌤️ Partly cloudy, slight chance of a shower, winds becoming S–SW 15–20km/h · 11–17°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — today's cloud clears into two warm, dry days before a slight chance of showers returns by early next week.",

    # World
    "{{WORLD_1_FLAG}}": "🇪🇺🇨🇦 EU–CANADA · VON DER LEYEN OFFERS CANADA A PATH TO BECOME THE BLOC'S FIRST-EVER 'ASSOCIATE MEMBER'",
    "{{WORLD_1_HEADLINE}}": "EU Chief Proposes Canada Become the Bloc's First 'Associate Member' as Ottawa Pivots Away From Trump's Tariffs",
    "{{WORLD_1_SUMMARY}}": "European Commission President Ursula von der Leyen told the European Parliament in Strasbourg that Brussels and Ottawa should move from a trading relationship to a broader 'alliance for the future,' days after Canadian PM Mark Carney said Canada was seeking a 'unique alliance' with the EU — a sign of how far Trump-era tariff policy is pushing traditional US allies elsewhere.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/9/16/eu-chief-von-der-leyen-proposes-associate-member-status-for-canada",

    "{{WORLD_2_FLAG}}": "🇽🇰 KOSOVO · WAR CRIMES COURT SENTENCES EX-PRESIDENT HASHIM THACI TO 25 YEARS",
    "{{WORLD_2_HEADLINE}}": "Former Kosovo President Hashim Thaci Convicted of War Crimes, Sentenced to 25 Years in Prison",
    "{{WORLD_2_SUMMARY}}": "A Kosovo Specialist Chambers panel found Thaci and three co-defendants criminally responsible for the arbitrary detention of 385 people, the torture of 303 and the murder of 96 during the 1998–99 independence war — a verdict that splits a country where many still see the wartime KLA leadership as national heroes.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/9/16/former-kosovo-president-hashim-thaci-convicted-of-war-crimes",

    # Economics
    "{{ECON_1_FLAG}}": "📈 MARKETS · ASX BOUNCES BACK FROM ITS THREE-MONTH LOW AS MINERS RALLY",
    "{{ECON_1_HEADLINE}}": "ASX Edges Higher as Miners Rebound, BHP Reclaims $60 a Share",
    "{{ECON_1_SUMMARY}}": "The ASX 200 rose 24 points (+0.28%) to 8,696.5 on Wednesday as BHP notched its first positive session in a week and gold firmed to roughly $A6,067 an ounce — a small reprieve after Tuesday's slide to a three-month low on oil-driven inflation fears.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-16/asx-markets-business-live-news/107157842",

    "{{ECON_2_FLAG}}": "⛽ FUEL · BRENT CRUDE PUSHES TOWARD US$107 A BARREL AS THE AUSSIE DOLLAR SOFTENS",
    "{{ECON_2_HEADLINE}}": "Brent Crude Climbs Toward $107 a Barrel While a Weaker Australian Dollar Adds to Import Costs",
    "{{ECON_2_SUMMARY}}": "Brent crude has risen roughly 8% over the past week to above US$107, and a softening Australian dollar is compounding the hit on landed fuel costs — meaning the diesel and freight line in a standing quote can move faster than the headline oil price suggests.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI FOR SMALL BUSINESS · ANTHROPIC ADDS 43 WORKFLOWS AND DIRECT LINKS INTO QUICKBOOKS, HUBSPOT AND MORE",
    "{{TECH_1_HEADLINE}}": "Anthropic Upgrades Claude for Small Business With 43 Ready-Made Workflows and 27 App Integrations",
    "{{TECH_1_SUMMARY}}": "The update wires Claude directly into QuickBooks, PayPal, HubSpot, Canva, DocuSign, Google Workspace and Microsoft 365, with ready-made workflows for payroll planning, invoice chasing and month-end reconciliation — the kind of admin most one-truck operators end up doing on a Sunday night.",
    "{{TECH_1_URL}}": "https://www.pymnts.com/artificial-intelligence-2/2026/anthropic-launches-claude-ai-agents-for-small-business-finance/",

    "{{TECH_2_FLAG}}": "🎯 AI AGENTS · SALESFORCE GIVES ITS AI AGENTS NAMES AND JOB TITLES",
    "{{TECH_2_HEADLINE}}": "Salesforce Names Seven Agentforce AI Agents, Each Built for One Specific Business Job",
    "{{TECH_2_SUMMARY}}": "Rather than one general chatbot, Salesforce's new Agentforce lineup — Casey, Paige, Carter and four others — assigns a named AI agent to each business function such as sales, service and marketing, reflecting a broader shift toward narrow, purpose-built AI tools over a single do-everything assistant.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏠 HOME ROBOTS · UBTECH BEGINS DELIVERING ITS $16,500-PLUS U1 HUMANOID COMPANION ROBOT",
    "{{ROBOT_1_HEADLINE}}": "UBTech Starts Delivering Its Humanoid Companion Robot to the First of Its 13,000-Plus Buyers",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics maker UBTech has begun home deliveries of its UWORLD U1 humanoid, priced from roughly $16,500 to $135,000, after racking up more than 13,000 pre-orders in China — a reminder that the same humanoid hardware now filling warehouses is only a couple of years from turning up on a residential street.",
    "{{ROBOT_1_URL}}": "https://startupfortune.com/ubtech-starts-delivering-its-16500-humanoid-companion-robots-today/",

    # Australia
    "{{AUS_1_HEADLINE}}": "International Students Face Ban on Bringing Family to Australia Under Burke's Migration Overhaul",
    "{{AUS_1_SUMMARY}}": "Home Affairs Minister Tony Burke uses a National Press Club address today to unveil changes effectively barring international students from bringing family members to Australia, part of a push to cut net overseas migration from 300,000 to 225,000 by 2028.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-16/federal-politics-tony-burke-bar-international-students-family/107160258",

    "{{AUS_2_HEADLINE}}": "Plymouth Brethren Leaders to Face Parliamentary Inquiry Over Election Harassment Claims",
    "{{AUS_2_SUMMARY}}": "Members of the Plymouth Brethren Christian Church will be hauled before the Joint Standing Committee on Electoral Matters over allegations the church paid activists to track the PM and harass candidates at the last federal election — claims the church denies.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Premier Orders Cost Review of $1.5 Billion Western Renewables Link, Pauses Land Acquisition",
    "{{VIC_1_SUMMARY}}": "Hours after approving the transmission line's environmental statement, Premier Ben Carroll paused compulsory land acquisition along the 190km Bulgana-to-Sydenham route and ordered a fresh cost review after the project's price tag more than tripled from its original 2019 estimate.",

    # Science
    "{{SCI_1_FLAG}}": "🦴 PALAEONTOLOGY · A NEWLY NAMED 240-MILLION-YEAR-OLD TANZANIAN SPECIES RESHAPES THE DINOSAUR TIMELINE",
    "{{SCI_1_HEADLINE}}": "Newly Named Triassic Species Could Reshape the Timeline of Early Dinosaur Evolution",
    "{{SCI_1_SUMMARY}}": "A fossil unearthed at one of the world's most significant Triassic sites in Tanzania has been formally named as a new species, Dinodontosaurus isiyavamanda, dating back almost 240 million years — and the find suggests some of the earliest known dinosaur relatives found nearby are younger than previously thought.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Anthropic Just Wired Claude Straight Into QuickBooks and HubSpot — Your Invoicing Software May Have Just Got a Free Upgrade",
    "{{INSIGHT_BODY}}": "The headline out of Anthropic this week isn't a flashy new model, it's plumbing: Claude can now sit inside QuickBooks, HubSpot, DocuSign and Microsoft 365 and run 43 pre-built workflows for the admin that actually eats a small operator's evening — chasing overdue invoices, reconciling the month's spending, routing a contract for signature. None of it needs a new subscription or a data migration; if you're already using one of those platforms, the AI is arguably already sitting there waiting to be switched on. Worth ten minutes this week to see whether it can take even one recurring task off your plate before the next BAS deadline creeps up.",

    # Fun facts
    "{{FACT_1}}": "The European Union's founding treaties contain no provision at all for an 'associate member' — the status Ursula von der Leyen floated for Canada this week would have to be invented from scratch, much the way the Schengen zone itself began as a side agreement between five countries with no basis in EU law at the time.",
    "{{FACT_2}}": "The Tanzanian fossil beds that just produced newly named species Dinodontosaurus isiyavamanda sit in the Ruhuhu Basin, one of only a handful of places on Earth preserving the exact 240-million-year-old window when the ancestors of dinosaurs were still an also-ran next to their crocodile-line cousins.",
    "{{FACT_3}}": "The necktie traces back to 17th-century Croatian mercenaries serving in France, whose knotted neckerchiefs (called 'cravates', from the French word for Croat) caught the eye of Louis XIV's court and were adopted as high fashion — meaning the ancestor of every business tie began as military kit.",

    # Joke
    "{{JOKE_SETUP}}": "A vinyl wrap installer was asked how his small business always kept every ute looking showroom-fresh, even on a same-day turnaround.",
    "{{JOKE_PUNCHLINE}}": "He said the trick was never cutting corners — literally, he trims every panel by hand.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"If you do build a great experience, customers tell each other about that.\"",
    "{{CLOSING_ATTR}}": "— Jeff Bezos",
    "{{CLOSING_MESSAGE}}": "Today's the day Tony Burke lays out the federal government's migration overhaul at the National Press Club, and the cloud sitting over Carrum Downs this morning should clear into two dry, sunny days from tomorrow — a good window to get outdoor jobs locked in before showers return early next week. Worth another glance at your fuel line items too, with Brent crude still pushing toward $107 a barrel.",
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
