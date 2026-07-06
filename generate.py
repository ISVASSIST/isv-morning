#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 07 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 7 Jul (BOM)
    "{{WEATHER_1}}": "TUE 7 · 🌫️ Frosty start, partly cloudy · 3–13°C",
    "{{WEATHER_2}}": "WED 8 · ☁️ Cloudy · 5–12°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "THU 9 · ⛅ Morning fog, partly cloudy · 4–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 10 · 🌤️ Morning fog, mostly sunny arvo · 4–15°C",
    "{{WEATHER_5}}": "SAT 11 · ⛅ Partly cloudy · 5–15°C",
    "{{WEATHER_ALERT}}": "⚠ MODERATE FROST WARNING TUESDAY MORNING · ALLOW EXTRA WARM-UP TIME FOR GEAR & VEHICLES",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 UKRAINE · SECOND MASS STRIKE IN 4 DAYS · AT LEAST 11 KILLED IN KYIV",
    "{{WORLD_1_HEADLINE}}": "Russia Hits Kyiv With a Second Mass Missile and Drone Barrage in Four Days, Killing at Least 11",
    "{{WORLD_1_SUMMARY}}": "Russia launched 351 drones and 68 missiles at Ukraine's capital overnight, with all 29 ballistic missiles fired striking their targets, killing at least 11 people and wounding around 60 as rescuers dug through wrecked apartment blocks. It's the second mass strike on Kyiv in under a week, following an attack last Thursday that killed 31 — Russia says the bombardment is retaliation for Ukrainian long-range strikes that have caused fuel shortages at home. The attack lands just as President Zelenskyy heads to Ankara for this week's NATO summit, where he's expected to press allies for more Patriot interceptor batteries.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/07/06/g-s1-132088/russian-missile-drone-attack-kyiv-kills-at-least-11",

    "{{WORLD_2_FLAG}}": "🇵🇸 GAZA · GOVERNANCE SHIFT · HAMAS DISSOLVES CIVILIAN RULING BODY",
    "{{WORLD_2_HEADLINE}}": "Hamas Announces Dissolution of Its Gaza Governing Body After Nearly 20 Years in Power",
    "{{WORLD_2_SUMMARY}}": "Hamas has dissolved the emergency committee that has run Gaza's civilian government, with the head of that committee formally resigning to make way for a new National Committee for the Administration of Gaza — part of the group's stated plan to step back from day-to-day governance under October's ceasefire. An Israeli official dismissed the move as \"spin,\" arguing Hamas is buying time rather than genuinely handing over control, with the thornier issue of the group's disarmament still unresolved.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/7/6/hamas-announces-dissolution-of-gaza-governing-body",

    # Economics
    "{{ECON_1_FLAG}}": "🚙 VICTORIA · REGO REBATE · 20% OFF CLOSES 31 JULY, UP TO $186 BACK",
    "{{ECON_1_HEADLINE}}": "Victoria's 20% Rego Rebate Window Shuts at the End of This Month — Here's How to Claim It",
    "{{ECON_1_SUMMARY}}": "Victorians have until 31 July to claim 20% back on light vehicle registration fees paid between 1 July 2025 and 30 June 2026, worth up to roughly $186 per vehicle and claimable on up to two personal vehicles — utes, vans and motorcycles under 4.5 tonnes all qualify. It's processed through Service Victoria and doesn't require much more than your rego details, but with the deadline three weeks out, it's an easy one to let lapse if it's not already in the diary for the work ute and the family car.",
    "{{ECON_1_URL}}": "https://service.vic.gov.au/find-services/transport-and-driving/registration/rego-rebate",

    "{{ECON_2_FLAG}}": "💵 AUSTRALIAN DOLLAR · RATE WATCH · AUD HOLDS NEAR 69 US CENTS",
    "{{ECON_2_HEADLINE}}": "Australian Dollar Holds Firm Near 69 US Cents as Traders Weigh Another Possible RBA Hike",
    "{{ECON_2_SUMMARY}}": "The Aussie dollar sat around 69.4 US cents this week, up slightly on a softer US jobs report, as markets digested the RBA's June meeting minutes flagging persistent inflation risk and the chance of a further cash rate rise later this year. A steadier dollar helps a little on the cost of imported tools, vehicles and equipment, but with the RBA's board not due to meet again until August, don't expect the rate picture to shift before then.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🚕 TESLA · ROBOTAXI · UNSUPERVISED LAUNCH IN MIAMI, FIFTH US CITY",
    "{{TECH_1_HEADLINE}}": "Tesla's Robotaxi Goes Fully Unsupervised in Miami — No Safety Driver, From Day One",
    "{{TECH_1_SUMMARY}}": "Tesla has expanded its Robotaxi service to Miami, its fifth US city after Austin, Dallas, Houston and Phoenix, and the first market where rides launched with no human safety monitor in the vehicle from the outset. The Model Y fleet covers a 10 to 14 square mile zone in western Miami-Dade, and it's also Tesla's first real test of its camera-only self-driving system against Florida's sudden tropical downpours and sun glare — conditions already under federal investigation over the system's handling of degraded visibility.",
    "{{TECH_1_URL}}": "https://www.gurufocus.com/news/8944904/tesla-launches-robotaxi-service-in-miami-tsla",

    "{{TECH_2_FLAG}}": "🧠 ANTHROPIC · CLAUDE FABLE 5 · FREE USAGE WINDOW ENDS TODAY",
    "{{TECH_2_HEADLINE}}": "Anthropic's Claude Fable 5 Moves to Metered Usage Credits Today After Its Free Access Window Closes",
    "{{TECH_2_SUMMARY}}": "From today, Claude Fable 5 shifts from being bundled free into Pro, Max and Team plans to metered usage credits, after Anthropic restored the model on 1 July following a 19-day suspension tied to US export controls and a jailbreak-bypass issue. It's a small but practical reminder for any business leaning on AI subscriptions: the tools themselves are moving fast, but so are the terms and pricing attached to them — worth a quick check of what plan you're actually on before assuming this week's bill looks like last week's.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · AGILITY ROBOTICS · $2.5B SPAC MERGER, LARGEST HUMANOID CAPITAL RAISE",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robot Maker Agility Robotics to Go Public in $2.5 Billion SPAC Deal",
    "{{ROBOT_1_SUMMARY}}": "Agility Robotics, maker of the Digit humanoid robot already working in warehouses and factories, is going public via a merger with Michael Klein's Churchill Capital, valuing the company at around $2.5 billion and raising more than $620 million — the largest capital raise in humanoid robotics history. The company's CEO was careful to temper expectations of a robot in every home any time soon, keeping the near-term focus squarely on warehouse and industrial floor work rather than consumer hype.",
    "{{ROBOT_1_URL}}": "https://techcrunch.com/2026/07/05/this-humanoid-robotics-company-is-going-public-but-its-ceo-isnt-promising-a-robot-in-your-home-anytime-soon/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australian Space Agency Confirms Mystery 'Space Balls' on Queensland Beaches Are Likely Rocket Debris",
    "{{AUS_1_SUMMARY}}": "Six silver spheres that washed up near Forrest Beach, roughly 80km north of Townsville, over the weekend are consistent with pressure vessels from a foreign rocket body that re-entered the atmosphere, the Australian Space Agency said. The objects, some containing potentially hazardous residual gases, have been assessed as posing no immediate safety risk, but authorities are urging anyone who spots similar debris to leave it untouched and call it in rather than handle it themselves.",
    "{{AUS_1_URL}}": "https://www.euronews.com/next/2026/07/06/space-debris-on-queensland-beach-space-balls-washed-ashore-do-not-touch",

    "{{AUS_2_HEADLINE}}": "Socceroos' World Cup Run Ends in Penalty Shootout Heartbreak Against Egypt",
    "{{AUS_2_SUMMARY}}": "Australia's historic World Cup campaign is over after a 1-1 draw with Egypt through extra time ended 4-2 to the Egyptians on penalties in the Round of 32, with misses from 18-year-old Lucas Herrington and defender Harry Souttar proving costly. It's heartbreak after a campaign that had already delivered Australia's first-ever World Cup knockout stage appearance — the wait for a first knockout win goes on for at least another four years.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Metro Tunnel Shuts Down Tonight for Five Days, Buses Replace Trains Across Five Lines",
    "{{VIC_1_SUMMARY}}": "Trains stop running through the Metro Tunnel from 8:30pm tonight until the last service on 12 July, with buses replacing trains on the Cranbourne, Pakenham and Sunbury lines, plus knock-on disruptions for Werribee, Williamstown and Sunbury passengers. If you're running a crew across town on public transport or timing deliveries around peak traffic, build in extra time this week — Southern Cross's coach terminal is expected to be especially busy.",

    # Science
    "{{SCI_1_FLAG}}": "🛰️ ASTRONOMY · JAXA · HAYABUSA2 ASTEROID FLYBY",
    "{{SCI_1_HEADLINE}}": "Japan's Hayabusa2 Probe Captures Stunning Close-Up Images of a Two-Headed Asteroid 62 Million Miles Away",
    "{{SCI_1_SUMMARY}}": "JAXA's Hayabusa2 spacecraft, already famous for its original sample-return mission, screamed past the asteroid Torifune at more than 18,000 km/h on Sunday, coming within just 800 metres to snap optical and infrared images of the double-lobed space rock. The infrared shots revealed Torifune's shadowed side is far cooler than its sun-facing surface, and the spacecraft transmitted the data home successfully and remains in good health — a genuine bonus mission for a probe that finished its main job years ago.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI Scams Are Getting Sharper — Your Business's Defences Need to Keep Pace",
    "{{INSIGHT_BODY}}": "Recent industry research shows 84% of Australian small businesses had a cyber incident in the past year, with four in five owners saying criminals are getting more sophisticated thanks to AI — yet fewer than one in five have actually put any guardrails around how their own team uses AI tools. The classic trap is a business email compromise: a very convincing AI-drafted email, supposedly from a regular supplier, asking you to send an invoice payment to \"updated\" bank details. The fix costs nothing — before changing any payment details or paying an unusual invoice, pick up the phone and confirm it with the supplier on a number you already have on file, not one in the email. It's a 30-second habit that beats almost every scam this smart.",

    # Fun Facts
    "{{FACT_1}}": "The 2026 FIFA World Cup is the first ever to feature 48 teams, up from 32, and the first hosted jointly by three nations — the USA, Mexico and Canada — spreading matches across a record 16 host cities.",

    "{{FACT_2}}": "Science fiction writer Isaac Asimov introduced his famous 'Three Laws of Robotics' in a 1942 short story called 'Runaround' — nearly 80 years before any real robot was capable of following them.",

    "{{FACT_3}}": "The fortune cookie isn't Chinese at all — it was popularised in early 1900s California by Japanese-American bakers, and China didn't see its first fortune cookie until decades later, imported as a novelty 'American' treat.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the carpenter's small business always come out even at tax time?",
    "{{JOKE_PUNCHLINE}}": "Because he measured every deduction twice and only cut once.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\"",
    "{{CLOSING_ATTR}}": "— Winston Churchill",
    "{{CLOSING_MESSAGE}}": "It's a frosty Tuesday start across Carrum Downs, so give the compressor and the van a few extra minutes before the first job — cloud building through the week means today's your best shot at clear afternoon sun. If you're relying on trains anywhere near the city tonight, the Metro Tunnel closure kicks in from 8:30pm, so plan around it. And spare a thought for the Socceroos — heartbreak on penalties overnight, but a knockout-stage World Cup run to be proud of all the same.",
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
