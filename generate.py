#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 27 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 27 Aug (BOM)
    "{{WEATHER_1}}": "THU 27 · ⛅ Partly cloudy, light winds · 7–16°C",
    "{{WEATHER_2}}": "FRI 28 · 🌦️ A shower or two · 9–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 29 · 🌧️ Showery and windy, cold front · 8–11°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 30 · 🌦️ Showers easing, more rain likely PM · 8–13°C",
    "{{WEATHER_5}}": "MON 31 · ☀️ Clearing, sunny and warming · 7–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or Carrum Downs — Victoria's only active warning covers heavy rain and flash flooding in the alpine north-east. Today and Monday are your best outdoor blasting and coating windows before a windy, showery cold front stalls spraying through the weekend.",

    # World
    "{{WORLD_1_FLAG}}": "🇵🇰 PAKISTAN · HOSPITAL NURSERY FIRE KILLS 14 NEWBORNS",
    "{{WORLD_1_HEADLINE}}": "Fire at Islamabad's Largest Government Hospital Kills 14 Newborn Babies",
    "{{WORLD_1_SUMMARY}}": "A short-circuit in a nursery air-conditioning unit sparked a fire at Pakistan's largest government hospital, PIMS, in Islamabad early Wednesday, killing at least 14 infants and prompting the government to order an inquiry into delayed rescue efforts, as grieving families demand answers.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/26/nx-s1-5944808/hospital-nursery-fire-kills-14-newborns-pakistan",

    "{{WORLD_2_FLAG}}": "🇨🇦 CANADA · RETALIATES WITH DOLLAR-FOR-DOLLAR US TARIFFS",
    "{{WORLD_2_HEADLINE}}": "Canada Hits Back With Matching Tariffs on Over 700 US Products",
    "{{WORLD_2_SUMMARY}}": "After Washington imposed 50% tariffs on tens of billions of dollars of Canadian goods last week, Prime Minister Mark Carney announced retaliatory tariffs on more than 700 US products — from steel to farm equipment — effective 8 September, declaring \"you're at war when you get attacked,\" with Trump reportedly weighing further levies in response.",
    "{{WORLD_2_URL}}": "https://www.bloomberg.com/news/newsletters/2026-08-26/canada-retaliates-with-us-tariffs-trump-weighs-more-levies",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL & INFLATION · PETROL JUMPS AS EXCISE RELIEF UNWINDS",
    "{{ECON_1_HEADLINE}}": "Petrol Prices Jump 7.5% in July as Fuel Excise Relief Fully Unwinds",
    "{{ECON_1_SUMMARY}}": "New ABS data shows automotive fuel prices rose 7.5% in July — their first rise in four months — as global oil prices climbed and the federal government's fuel excise relief wound off completely, with economists warning August's figures will feel the pinch even harder; Melbourne's live averages already sit around 201c/L for unleaded and 241c/L for diesel.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-08-26/july-inflation-slows-heightened-risk-rba-rate-hike/107078580",

    "{{ECON_2_FLAG}}": "🚛 COMPLIANCE · REGULATOR GROUNDS ENTIRE 70-TRUCK FLEET",
    "{{ECON_2_HEADLINE}}": "Queensland Freight Operator's Whole Fleet Grounded Over Compliance Breaches",
    "{{ECON_2_SUMMARY}}": "The National Heavy Vehicle Regulator has grounded a Normanton-based freight operator's entire 70-truck fleet after a pattern of non-compliance findings, putting more than 70 jobs at risk while the company fights the order in Brisbane's Supreme Court — a sharp reminder of how fast one regulator finding can shut down a small operator.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💻 AI ADOPTION · AMAZON SHUTS DOWN MECHANICAL TURK AFTER 21 YEARS",
    "{{TECH_1_HEADLINE}}": "Amazon Retires Mechanical Turk as AI Takes Over the Human Gig Work It Was Built On",
    "{{TECH_1_SUMMARY}}": "Amazon will close its Mechanical Turk crowdsourced-labour marketplace on 30 September, ending the 21-year-old platform Jeff Bezos once called \"artificial artificial intelligence,\" as newer AI-training data firms and the AI models themselves have taken over much of the labelling work humans used to do by hand.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/08/25/amazon-service-that-jeff-bezos-called-artificial-ai-is-shutting-down.html",

    "{{TECH_2_FLAG}}": "🤖 AI TOOLS · CLAUDE'S MEMORY NOW FOLLOWS YOU ACROSS CHAT AND TASKS",
    "{{TECH_2_HEADLINE}}": "Anthropic Gives Claude a Shared Memory Across Chat and Agent Tasks",
    "{{TECH_2_SUMMARY}}": "Anthropic has merged Claude's memory systems so it now retains project details, deadlines and preferences whether you're chatting directly or handing it a task to run — with an editable, visible list of what it remembers, and sensitive topics excluded by default.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 WAREHOUSE AUTOMATION · ROBOT INTEGRATION CUT FROM MONTHS TO WEEKS",
    "{{ROBOT_1_HEADLINE}}": "New Partnership Cuts Warehouse Robot Deployment Time by Up to 40%",
    "{{ROBOT_1_SUMMARY}}": "Bear Robotics and BOWE IQ have teamed up to plug autonomous mobile robot fleets directly into existing warehouse and business software, cutting integration time from months to weeks for logistics, automotive and healthcare operators across the UK and Europe — a sign the barrier to adopting factory-floor robotics keeps dropping.",
    "{{ROBOT_1_URL}}": "https://www.accessnewswire.com/newsroom/en/computers-technology-and-internet/bear-robotics-and-bowe-iq-partner-to-cut-warehouse-robot-integrat-1206300",

    # Australia
    "{{AUS_1_HEADLINE}}": "Inflation Eases to 3.5% But Underlying Price Pressure Holds Firm",
    "{{AUS_1_SUMMARY}}": "ABS data released today shows annual inflation cooled to 3.5% in the year to July, down from 3.8% in June, driven largely by softer housing costs — though underlying \"trimmed mean\" inflation held steady at 3.6%, with housing and food still the biggest contributors to the annual rise.",
    "{{AUS_1_URL}}": "https://www.abs.gov.au/media-centre/media-releases/cpi-rose-35-year-july-2026",

    "{{AUS_2_HEADLINE}}": "Bondi Antisemitism Royal Commission Wraps Up After 62 Days of Hearings",
    "{{AUS_2_SUMMARY}}": "The Royal Commission on Antisemitism and Social Cohesion, established after the Bondi terror attack, has closed its hearings after taking evidence from 340 witnesses and over 20,000 submissions, with Commissioner Virginia Bell due to hand down her final report by 18 December.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Bystanders Help Police Make Swift Arrest After Random CBD Stabbing",
    "{{VIC_1_SUMMARY}}": "A 27-year-old man has been charged after allegedly attacking a woman and her 10-year-old son with scissors on Spencer Street, right outside Victoria Police headquarters — bystanders stepped in and police made a fast arrest, with both victims now in hospital in a stable, non-life-threatening condition.",

    # Science
    "{{SCI_1_FLAG}}": "🐾 CONSERVATION GENETICS · 190-YEAR-OLD MUSEUM SPECIMEN SOLVES PANGOLIN MYSTERY",
    "{{SCI_1_HEADLINE}}": "DNA From a 190-Year-Old Museum Skin Confirms a Hidden Pangolin Species",
    "{{SCI_1_SUMMARY}}": "DNA extracted from a pangolin skin shipped from Nepal to London in 1836 has confirmed the Himalayan pangolin as a species genuinely distinct from its Chinese cousin, settling a near two-century-old naming dispute — a find that matters well beyond taxonomy, since being able to genetically trace scales to a specific species and region gives investigators a real tool against the trafficking of the world's most-poached mammal.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Victoria's Work-From-Home Law Lands September 1 — Small Trades Get Until 2027, But Worth Setting Up Now",
    "{{INSIGHT_BODY}}": "Victoria's new right to request work from home (up to two days a week) takes effect from 1 September for most employers, though businesses with under 15 staff get a reprieve until July 2027. That's real runway — but the office and admin side of a trades business, quoting, invoicing, scheduling, is exactly the part that's workable from a laptop. Building cloud-based, AI-linked job systems now, so an admin person can quote, invoice or field calls from home without you losing visibility on site, turns a looming compliance deadline into a head start instead of a scramble.",

    # Fun facts
    "{{FACT_1}}": "The first-ever spam email was sent on 3 May 1978 by a Digital Equipment Corp marketer named Gary Thuerk, who blasted 393 ARPANET users with an ad for new computers — it annoyed the recipients, but reportedly helped generate $12 million in sales.",
    "{{FACT_2}}": "The \"immortal jellyfish\" (Turritopsis dohrnii) can, when injured, starving or aging, revert its adult cells back into an earlier polyp stage and effectively start life over — the only known animal capable of ageing backwards this way.",
    "{{FACT_3}}": "A live lobster's shell isn't naturally red — a blue-black pigment protein called crustacyanin masks the red astaxanthin underneath, and cooking heat breaks that protein apart, freeing the pigment and turning the shell red.",

    # Joke
    "{{JOKE_SETUP}}": "What did the knife sharpener say when a customer asked for a discount?",
    "{{JOKE_PUNCHLINE}}": "\"Sorry mate — my margins are already razor thin.\"",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Don't give up. Don't ever give up.\"",
    "{{CLOSING_ATTR}}": "— Jim Valvano",
    "{{CLOSING_MESSAGE}}": "It's a calm, mostly dry Thursday in Carrum Downs before the weekend turns wet and windy, so today's still a solid one for outdoor jobs. With petrol climbing again as fuel excise relief unwinds and Victoria's new work-from-home rules landing in a week, it's a fair day to get ahead of both — top up the ute early and start thinking about how your own admin side could run just as well from a laptop.",
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
