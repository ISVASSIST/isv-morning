#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 25 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 25 May (BOM forecast)
    "{{WEATHER_1}}": "MON 25 · 🌧 Showers · 14°C",
    "{{WEATHER_2}}": "TUE 26 · 🌧 Showers · 14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 27 · 🌧 Showers · 13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 28 · 🌧 Showers · 15°C",
    "{{WEATHER_5}}": "FRI 29 · 🌧 Showers · 14°C",
    "{{WEATHER_ALERT}}": "☔ WET WEEK AHEAD",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸🇮🇷 IRAN · DIPLOMACY",
    "{{WORLD_1_HEADLINE}}": "US and Iran Close In on Peace Deal as Rubio Reports 'Significant Progress' — Hormuz Reopening Key Sticking Point",
    "{{WORLD_1_SUMMARY}}": "US Secretary of State Marco Rubio declared 'significant progress' in ceasefire-to-settlement negotiations with Iran after President Trump stated the deal was 'largely negotiated' — a claim Iranian state media promptly disputed. Both sides are working toward a two-phase memorandum of understanding, but major disagreements remain over control of the Strait of Hormuz, nuclear program timelines, and the sequencing of sanctions relief. A resolution on Hormuz would directly ease the global oil supply squeeze behind Australia's ongoing fuel crisis — making this the single diplomatic development with the most direct near-term impact on costs for Australian trades operators running vehicle-heavy operations.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/05/24/middleeast/iran-us-proposed-deal-wwk-intl",

    "{{WORLD_2_FLAG}}": "🇺🇸 USA · WILDFIRES",
    "{{WORLD_2_HEADLINE}}": "Newsom Declares State of Emergency as Multiple Wildfires Force 10,000 Evacuations Across Southern California",
    "{{WORLD_2_SUMMARY}}": "California Governor Gavin Newsom declared a state of emergency in Orange County as multiple wildfires tore across Southern California over the weekend. The Santa Rosa Island blaze consumed more than 18,300 acres and forced closure of Channel Islands National Park. A failing chemical storage tank near Simi Valley raised fears of a catastrophic explosion, prompting additional evacuations. The Sandy Fire east of Los Angeles reached more than 2,100 acres before partial containment. Tens of thousands of residents remain displaced, with multiple structures confirmed destroyed and air quality warnings across the region.",
    "{{WORLD_2_URL}}": "https://www.foxnews.com/us/newsom-declares-state-emergency-orange-county-failing-chemical-tank-nears-catastrophic-explosion",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AUSTRALIA · FUEL RELIEF",
    "{{ECON_1_HEADLINE}}": "ACCC Weekly Monitor Confirms Fuel Prices Remain Well Below Pre-Crisis Levels Under Halved Excise",
    "{{ECON_1_SUMMARY}}": "The ACCC's weekly fuel monitoring update of 22 May confirms retail petrol and diesel prices across Australia's capital cities and more than 190 regional locations remain significantly lower than before the federal government halved the fuel excise on April 1 — cutting the rate from 52.6 cents to 26.3 cents per litre. The relief runs until June 30. The ACCC has been directed to publish weekly reports through to September 2026 as part of ongoing oversight of the market's response to the Iran war supply disruption. For trades operators in Carrum Downs and metro Melbourne running vehicle-heavy operations, this is a window of reduced operating costs — and it closes in five weeks.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🏘 AUSTRALIA · WEALTH GAP",
    "{{ECON_2_HEADLINE}}": "Australia's Wealth Gap Widens: Households Worth Over $1.6M Now Outnumber the Shrinking Middle Class",
    "{{ECON_2_SUMMARY}}": "New KPMG analysis released in May 2026 shows households with net wealth above $1.6 million now represent 22% of all Australians — up from 15% a decade ago, growing at 7% per year against overall household growth of 2.1%. The traditional middle-wealth band ($300k–$900k) has contracted to 28% of households as home ownership rates among younger Australians fall. With an estimated $5 trillion in intergenerational wealth transfers projected over the next 20 years, economists warn Australia is shifting from a meritocratic middle-class economy toward one where inherited wealth increasingly determines financial trajectory — with downstream effects on discretionary renovation and residential spending.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔍 GOOGLE · I/O 2026",
    "{{TECH_1_HEADLINE}}": "Google Launches Gemini 3.5 Flash and Gemini Omni at I/O 2026 — AI Mode in Search Tops One Billion Monthly Users",
    "{{TECH_1_SUMMARY}}": "At Google I/O 2026, the company launched Gemini 3.5 Flash — its fastest frontier-class model — and Gemini Omni, capable of generating content from any input including video. Google's AI Mode in Search has now surpassed one billion monthly active users and is being rebuilt around a new AI-powered interface handling text, images, files, videos, and Chrome tabs simultaneously — described as the biggest overhaul to the search interface in 25 years. For small businesses, the practical implication is that prospective customers are increasingly finding answers through AI-summarised results rather than clicking through to individual websites, making verified reviews and structured digital presence more important than raw SEO.",
    "{{TECH_1_URL}}": "https://blog.google/innovation-and-ai/sundar-pichai-io-2026/",

    "{{TECH_2_FLAG}}": "🤖 ANTHROPIC · REVENUE",
    "{{TECH_2_HEADLINE}}": "Anthropic Posts First-Ever Profit on $10.9B Revenue and Closes In on $900 Billion Valuation",
    "{{TECH_2_SUMMARY}}": "Claude AI maker Anthropic has crossed its first profitability milestone as revenues reached $10.9 billion, with the company simultaneously closing in on a $900 billion valuation and eyeing a potential IPO as early as October 2026. A $30 billion-plus funding round led by Sequoia Capital, Dragoneer, and Altimeter is expected to close imminently. Anthropic's quarterly revenue doubled, driven by API access and Claude's integration into enterprise workflows across legal, engineering, and operations sectors — signalling that frontier AI has moved from loss-making research into commercial-scale business.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 USA/CANADA · INDUSTRIAL AUTOMATION",
    "{{ROBOT_1_HEADLINE}}": "GE Vernova Acquires Robotech Automation to Accelerate Industrial Robotics Integration Across Its US Factories",
    "{{ROBOT_1_SUMMARY}}": "Energy and industrial giant GE Vernova announced on 21 May the acquisition of Robotech Automation, a specialist robotics and automation systems integrator based near Montreal with approximately 35 employees. Robotech delivers customised automation solutions combining in-house engineering design with third-party integration — already active on projects at GE Vernova's Schenectady, New York and Charleroi, Pennsylvania facilities. CEO Scott Strazik cited the move as accelerating the deployment of specialist robotics talent directly inside GE Vernova's manufacturing operations. The acquisition mirrors a broader industry trend of large industrials bringing automation integration expertise in-house rather than contracting it externally — compressing timelines and improving quality on the factory floor.",
    "{{ROBOT_1_URL}}": "https://www.gevernova.com/news/press-releases/ge-vernova-to-acquire-robotech-automation",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos in Florida as World Cup Countdown Begins — Injuries Hit Camp but Squad Taking Shape",
    "{{AUS_1_SUMMARY}}": "The CommBank Socceroos are underway at their FIFA World Cup 2026 pre-camp in Sarasota, Florida, with coach Tony Popovic assessing an extended train-on squad ahead of the final 26-player announcement on June 1. Two players departed with injuries — defender Hayden Matthews and striker Nick D'Agostino — while twelve new players joined camp this week. Australia opens Group D against Türkiye in Vancouver on June 13 (AEST June 14), before facing co-hosts the USA in Seattle (June 19) and Paraguay in Santa Clara (June 25). A May 30 friendly against Mexico in Los Angeles precedes the tournament.",
    "{{AUS_1_URL}}": "https://footballaustralia.com.au/news/commbank-socceroos-commence-fifa-world-cup-2026tm-pre-camp-sarasota-florida",

    "{{AUS_2_HEADLINE}}": "Australia's Dying Middle Class: Inherited Wealth Is Replacing Earned Income as the Key to Financial Security",
    "{{AUS_2_SUMMARY}}": "Multiple May 2026 analyses — from KPMG and SBS — are converging on the same conclusion: Australia's middle class is contracting as a structural economic force, with wealth concentrating at the top and inheritance, not wages, increasingly determining whether younger Australians can build assets. An estimated $5 trillion will transfer between generations over 20 years, but distribution will be deeply uneven. For trades businesses, the downstream effect is less discretionary spend on renovations and upgrades from younger homeowners — while established industrial and compliance-driven maintenance contracts become more reliable core revenue.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Last Week of Free Public Transport — Half-Price Fares for All Passengers Start Saturday 1 June",
    "{{VIC_1_SUMMARY}}": "Victorian commuters have until Sunday 31 May to take advantage of the state government's free public transport scheme — this is the final week. From Saturday 1 June, all train, tram, and bus fares across Victoria will be halved for all passengers until 1 January 2027, saving the average commuter around $850 over six months. Premier Jacinta Allan introduced the scheme to ease pump-price pressure and reduce road congestion during the ongoing fuel crisis, at a cost of $432 million in foregone revenue. Melbourne's network will be busier — but significantly cheaper — for the rest of the year.",

    # Science
    "{{SCI_1_FLAG}}": "🌌 ASTROPHYSICS · MEDITERRANEAN",
    "{{SCI_1_HEADLINE}}": "Scientists May Have Found the Origin of the Most Powerful Cosmic Particle Ever Detected",
    "{{SCI_1_SUMMARY}}": "A new study published in the Journal of Cosmology and Astroparticle Physics — covered by ScienceDaily on 23 May — suggests the most energetic neutrino ever recorded may originate from blazars, the most extreme objects in the known universe. The particle, designated KM3-230213A, was detected in February 2023 by the KM3NeT seafloor observatory off the coast of Sicily and carries approximately 220 PeV of energy — more than ten times greater than any previously observed high-energy neutrino. Blazars are active galactic nuclei powered by supermassive black holes that shoot plasma jets directly toward Earth at near light speed, and are now the leading candidate for accelerating particles to energies far beyond what any ground-based accelerator can achieve.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Monday Morning in 15 Minutes: How AI Can Plan Your Entire Trades Week Before You Leave the Driveway",
    "{{INSIGHT_BODY}}": "Most trades business owners don't have a motivation problem — they have a planning gap. The jobs are there, the crew is there, but Monday morning turns into a scramble because nothing was staged: which job starts when, which materials need ordering, which client is waiting on a call, which quote is still outstanding. AI can close that gap in fifteen minutes if you give it the right input. The habit is straightforward: Sunday evening or first thing Monday morning, open Claude or ChatGPT and paste in your job list, your crew roster, and any outstanding quotes or deliveries. Ask it to generate a prioritised weekly schedule, flag resource conflicts, draft brief client updates for any jobs delayed from last week, and list materials that need to be on order by close of business today. The model does the synthesis; you make the final calls. Trades operators who run this consistently report they stop losing a half-day every Monday to reactive planning — and their crew starts the week with clear direction instead of waiting for instructions while the clock ticks. The setup takes one session to get right. After that, it takes fifteen minutes. Monday mornings change fast.",

    # Fun Facts
    "{{FACT_1}}": "The dragonfly is the world's most effective aerial predator — catching its target prey in approximately 95% of attempts, compared to lions at around 25% and great white sharks at roughly 55%. This extraordinary success rate comes from compound eyes covering almost 360° of vision and a brain that calculates intercept trajectories, allowing the dragonfly to predict where prey will be and fly directly to that intercept point before the prey arrives. It does not chase — it ambushes the future.",

    "{{FACT_2}}": "The tomato is botanically a fruit, not a vegetable — but this distinction was actually ruled on by the US Supreme Court in 1893 in Nix v. Hedden. The court unanimously held that tomatoes are legally vegetables for customs tariff purposes, despite their botanical classification as the seed-bearing structure of a flowering plant. The ruling still stands. Over 180 million tonnes of tomatoes are grown globally each year, making them the world's most produced 'vegetable.'",

    "{{FACT_3}}": "The box jellyfish (Chironex fleckeri), found in the warm coastal waters of northern Australia, has 24 eyes arranged in four clusters — including eyes with a true cornea, lens, and retina capable of forming proper images. Despite this, the jellyfish has no brain; visual information is processed through a simple nerve ring around its bell. It is considered the most venomous marine animal on Earth, capable of killing a human in under five minutes from a severe sting — and it navigates and hunts entirely without a central nervous system.",

    # Joke
    "{{JOKE_SETUP}}": "Why do roof plumbers always make headlines?",
    "{{JOKE_PUNCHLINE}}": "Because everything they do ends up in the gutter.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Start where you are. Use what you have. Do what you can.”",
    "{{CLOSING_ATTR}}": "— Arthur Ashe",
    "{{CLOSING_MESSAGE}}": "Monday 25 May — a wet week ahead for Carrum Downs, with showers expected most days through to Friday. If there is any outdoor coating or surface prep work in the schedule, today is the window before conditions settle in wet. On the global front, the Iran-US peace deal is inching closer; a Hormuz reopening would begin easing oil supply pressure before the Australian fuel excise cut expires on June 30 — worth watching closely. Closer to home, this is Victoria's last week of free public transport before half-price fares kick in from June 1. The Socceroos are in Florida with the World Cup less than three weeks out. And the Monday planning habit in today's insight is worth reading — fifteen minutes this morning could clear the week. Have a sharp one, Liall.",
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
