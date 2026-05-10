#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 11 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Mon 11 May
    "{{WEATHER_1}}": "Mon 11 May · Cloudy · 16°C/8°C",
    "{{WEATHER_2}}": "Tue 12 May · Drizzle · 14°C/11°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Wed 13 May · Fog → Sunny · 17°C/7°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Thu 14 May · Mostly Sunny · 18°C/7°C",
    "{{WEATHER_5}}": "Fri 15 May · Sunny · 18°C/8°C",
    "{{WEATHER_ALERT}}": "🌧 Drizzle Tue · ☀️ Clears Wed",

    # World
    "{{WORLD_1_FLAG}}": "🌍 UKRAINE",
    "{{WORLD_1_HEADLINE}}": "Russia-Ukraine Three-Day Ceasefire Expires This Morning — Guns Expected to Resume",
    "{{WORLD_1_SUMMARY}}": "The US-brokered ceasefire covering Russia's Victory Day weekend — 9 to 11 May — formally expires this morning. Both sides exchanged 1,000 prisoners during the truce. Trump called it \"the beginning of the end\" of the four-year war, but Russian officials stressed the pause was temporary only. Negotiators meet today to determine whether a longer pause — or any pathway to a permanent settlement — is achievable. Markets and energy traders are watching closely.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/5/8/trump-announces-three-day-ceasefire-in-russia-ukraine-war",

    "{{WORLD_2_FLAG}}": "🌍 MIDDLE EAST",
    "{{WORLD_2_HEADLINE}}": "US Navy Opens Fire on Iranian Tankers After Armed Exchange in Strait of Hormuz",
    "{{WORLD_2_SUMMARY}}": "US naval forces fired on two Iranian oil tankers following an exchange of fire with Iranian forces in the Strait of Hormuz — the waterway through which roughly 20% of all globally traded oil flows. Iran is under a US-enforced naval blockade as food prices surge and its currency collapses. The UAE separately reported a fresh Iranian missile and drone attack over the weekend. The escalation has renewed global concern about oil supply disruption.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/middleeast",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 BUDGET NIGHT",
    "{{ECON_1_HEADLINE}}": "Federal Budget Tomorrow Night — Watch the Instant Asset Write-Off and the $150 Small Biz Energy Rebate",
    "{{ECON_1_SUMMARY}}": "Treasurer Jim Chalmers delivers the 2026-27 budget Tuesday evening. Pre-confirmed: a $150 energy rebate for small businesses and the $10.7bn Fuel Security Package. The key watch for small operators is whether the $20,000 instant asset write-off gets made permanent — it expires 30 June. COSBOA is pushing for the small business tax rate to drop from 25% to 20%. Pre-budget leaks also suggest a 30% baseline tax on trust distributions, which could hit family business structures.",
    "{{ECON_1_URL}}": "https://www.smartcompany.com.au/federal-budget-2026/federal-budget-what-we-know-businesses-2026-fuel-negative-gearing-capital-gains/",

    "{{ECON_2_FLAG}}": "🏦 RATES",
    "{{ECON_2_HEADLINE}}": "RBA Raises Cash Rate to 4.35% — Third Straight Hike Fully Reverses Last Year's Rate Cuts",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank lifted its cash rate to 4.35% at its May meeting, fully unwinding the 2025 easing cycle. Inflation sits at 4.6% — its highest since September 2023 — driven by energy costs and Middle East supply disruptions. The RBA has flagged stagflation risk if shocks persist. For small businesses, higher borrowing costs now stack on top of elevated fuel and materials prices heading into a traditionally slower winter period.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💡 AI & WORK",
    "{{TECH_1_HEADLINE}}": "AI Is Restructuring Jobs, Not Eliminating Them — Software Dev Employment Up 4% Amid AI Surge",
    "{{TECH_1_SUMMARY}}": "New CNN analysis published Sunday finds AI is automating specific tasks within roles rather than replacing workers outright. US software developer employment rose 4% year-on-year in Q1 2026 as global AI adoption reached 17.8% of the working-age population. For trades operators, the lesson is the same: AI is most likely to absorb the administrative burden — quoting, scheduling, compliance docs — leaving the skilled site work untouched. The question is whether you let it work for you, or watch a competitor do it first.",
    "{{TECH_1_URL}}": "https://www.cnn.com/2026/05/10/tech/ai-taking-jobs",

    "{{TECH_2_FLAG}}": "📱 AI HARDWARE",
    "{{TECH_2_HEADLINE}}": "Qualcomm CEO: The Smartphone Era Is Ending — AI Agents Will Run Your Personal 'Ecosystem'",
    "{{TECH_2_SUMMARY}}": "Qualcomm's CEO told Fortune this weekend that the smartphone-centric world is giving way to an interconnected 'ecosystem of you': AI-powered glasses, smart earbuds, and a persistent AI agent tying everything together. The company is already working with OpenAI, Meta, and other major players on undisclosed wearable devices. The vision: less phone-in-pocket, more always-on AI assistant that's aware of your environment and context — all day, hands-free.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 IFR · GLOBAL",
    "{{ROBOT_1_HEADLINE}}": "Global Industrial Robot Installations Hit All-Time High of US$16.7 Billion",
    "{{ROBOT_1_SUMMARY}}": "The International Federation of Robotics has confirmed that the global market value of industrial robot installations reached a record US$16.7 billion, with demand accelerating across automotive, electronics, food processing, and logistics. The IFR's State of Robotics 2026 report — published Saturday — shows physical automation is no longer a future trend: manufacturers worldwide are integrating robot arms, autonomous mobile platforms, and early-stage humanoids alongside human workers in standard daily production. Australia's adoption remains below the global average but is growing.",
    "{{ROBOT_1_URL}}": "https://ifr.org/ifr-press-releases/news/top-5-global-robotics-trends-2026",

    # Australia
    "{{AUS_1_HEADLINE}}": "Chalmers Announces $2 Billion to Unlock 65,000 New Homes Ahead of Tuesday Budget",
    "{{AUS_1_SUMMARY}}": "Treasurer Jim Chalmers confirmed the federal budget will include $2 billion in infrastructure funding to unlock 65,000 new homes, targeting Australia's housing affordability crisis. The investment front-funds roads, water and essential services in growth corridors to accelerate land release. Labor expects the package to support thousands of additional construction trade jobs across the country as new estates are opened up faster than currently possible.",
    "{{AUS_1_URL}}": "https://www.bloomberg.com/news/articles/2026-05-09/australia-to-tackle-unacceptable-housing-market-chalmers-says",

    "{{AUS_2_HEADLINE}}": "Jewish Families Tell Antisemitism Royal Commission: 'We Fear for Our Children's Future in Australia'",
    "{{AUS_2_SUMMARY}}": "Parents and community leaders gave emotional testimony to Australia's Royal Commission into Antisemitism and Social Cohesion, describing persistent fear for their children's safety in schools and public spaces following the Bondi terror attack. Witnesses called for stronger government protections, curriculum changes, and greater accountability for social media platforms. The commission is expected to deliver interim findings by mid-year.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne to Double Community Safety Officers and Build a 5,000 sqm Southbank Public Park",
    "{{VIC_1_SUMMARY}}": "The City of Melbourne's draft 2026-27 budget doubles Community Safety Officers from 11 to 22, targeting antisocial behaviour and rough sleeping in the CBD. The Southbank City Road Undercroft is also set to become a 5,000 square metre public park featuring a roller rink, skate park, bouldering wall, and basketball courts. Melbourne Design Week launches Thursday 14 May, with over 400 events across two weeks celebrating the festival's 10th anniversary.",

    # Science
    "{{SCI_1_FLAG}}": "🧬 LONGEVITY · UNIVERSITY OF ROCHESTER",
    "{{SCI_1_HEADLINE}}": "Scientists Transfer Naked Mole Rat's Anti-Ageing Gene Into Mice — Lifespan Extends by 4.4%",
    "{{SCI_1_SUMMARY}}": "Researchers at the University of Rochester engineered mice to carry the naked mole rat's version of the hyaluronan synthase 2 gene — the gene behind the animal's extraordinary levels of high-molecular-weight hyaluronic acid. The result: modified mice lived 4.4% longer, with significantly less inflammation across multiple organs, better gut health, and stronger cancer resistance. Naked mole rats can live up to 41 years — nearly ten times longer than other rodents of similar size. Published Saturday in ScienceDaily.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Quote Follow-Up Is a Revenue Leak — Here's How AI Plugs It",
    "{{INSIGHT_BODY}}": "Most tradies send a quote and move on. But research consistently shows that following up just once lifts conversion rates by 20–35% — and the biggest barrier is time. AI tools like Claude or a simple automated workflow can now send a personalised follow-up message 48–72 hours after each quote, referencing the job details, offering to answer questions, and nudging the decision without you lifting a finger. For a trades business sending 10–15 quotes a week, capturing just one or two extra jobs per month at your average ticket size can clear $5,000–$15,000 per year in recovered revenue. Set it up once. Let it run.",

    # Fun Facts
    "{{FACT_1}}": "The word \"muscle\" comes from the Latin \"musculus\" — meaning \"little mouse\" — because Romans thought the rippling movement of a flexed muscle beneath the skin looked like a mouse moving under cloth. They used exactly the same word for both the animal and the body part.",
    "{{FACT_2}}": "More steel is recycled every year than all other materials combined — approximately 650 million tonnes globally, at a recycling rate of around 85%. Recycling a single tonne of steel saves 1.4 tonnes of iron ore, 740 kilograms of coal, and enough energy to power a home for nearly two days.",
    "{{FACT_3}}": "Antarctica is the world's largest desert. Most of the continent receives less than 200mm of precipitation per year — technically drier than the Sahara. Most of the snow on Antarctica doesn't fall from the sky: it blows in from the coast and gets redistributed by katabatic winds that can exceed 300 km/h.",

    # Joke
    "{{JOKE_SETUP}}": "A builder proudly told his accountant: 'Ten jobs on the go, booked solid for six months, just hired two new blokes.'",
    "{{JOKE_PUNCHLINE}}": "His accountant said: 'Wonderful. Now go and collect some of the money you're owed — your account is empty.'",

    # Closing
    "{{CLOSING_QUOTE}}": "\"You have power over your mind, not outside events. Realise this, and you will find strength.\"",
    "{{CLOSING_ATTR}}": "Marcus Aurelius",
    "{{CLOSING_MESSAGE}}": "A significant week ahead, Liall. The federal budget lands tomorrow night — watch closely for the instant asset write-off decision and what the energy rebate means for your cost base. Foggy mornings to kick off the week but the sun pushes through by Wednesday. The Ukraine ceasefire ended this morning and the Middle East remains unpredictable. Lock in the week, follow up any open quotes, and have a strong Monday.",
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
