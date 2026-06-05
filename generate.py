#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 06 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 6 Jun
    # Cold front cleared Friday; showers possible Saturday morning, improving through the week
    "{{WEATHER_1}}": "SAT 6 · 🌦 Showers possible · 9–15°C",
    "{{WEATHER_2}}": "SUN 7 · ⛅ Partly cloudy · 11–17°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 8 · 🌥 Mostly cloudy · 9–15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "TUE 9 · ⛅ Partly cloudy · 8–14°C",
    "{{WEATHER_5}}": "WED 10 · ⛅ Partly cloudy · 9–15°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS SAT MORNING · EASING AFTERNOON",

    # World
    "{{WORLD_1_FLAG}}": "🌍 MIDDLE EAST · IRAN",
    "{{WORLD_1_HEADLINE}}": "Trump Says Iran Nuclear Deal Possible \"This Weekend\" — Tehran Flatly Contradicts Him",
    "{{WORLD_1_SUMMARY}}": "US President Trump told reporters on June 4 that a nuclear agreement with Iran could be reached 'this weekend' following the latest round of Oman-mediated indirect talks. Within hours, Iran's Foreign Minister Abbas Araghchi publicly contradicted him, saying there had been no 'significant process' in negotiations and that Iran's core positions remained unchanged. Iran insists on maintaining domestic uranium enrichment; the US demands zero enrichment on Iranian soil — a gap analysts describe as unbridgeable in weeks. Trump's self-imposed June 30 deadline now looms with the two sides still far apart, and the contradictory public signals are raising doubts about whether any framework exists at all.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/06/04/world/live-news/iran-trump-war-news",

    "{{WORLD_2_FLAG}}": "🌍 EUROPE · RUSSIA–UKRAINE",
    "{{WORLD_2_HEADLINE}}": "Russian Drones Strike Kharkiv Overnight; Putin Vows to Accelerate Air Defence Expansion at St. Petersburg Forum",
    "{{WORLD_2_SUMMARY}}": "Russian drone attacks struck residential areas of Kharkiv and energy infrastructure near Zaporizhzhia overnight June 4–5, Ukrainian officials reported. At the St. Petersburg International Economic Forum — Russia's flagship annual investment summit — President Putin confirmed Russia would dramatically strengthen its layered air defence network to counter a sustained Ukrainian long-range drone campaign that has struck oil storage facilities and military airfields deep inside Russian territory over the past fortnight. The escalating exchanges have cast a shadow over the forum and signal both sides are preparing for sustained aerial warfare through summer.",
    "{{WORLD_2_URL}}": "https://www.bbc.com/news/world/europe",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 ECONOMY · RBA",
    "{{ECON_1_HEADLINE}}": "RBA Cash Rate at 4.35% — June 16 Board Meeting Has Economists Divided on Hold vs. Fourth Hike",
    "{{ECON_1_SUMMARY}}": "Australia's Reserve Bank board meets on June 16 with economists sharply divided on the outcome. Commonwealth Bank expects a pause following May's increase; Westpac tips a fourth hike as underlying inflation runs at 3.7% — above the 2–3% target band — with RBA forecasts showing it won't return to target until late 2027. GDP growth has been revised down to 1.3% for 2026, its weakest in a decade. For trades businesses navigating rising wage costs and the impending end of fuel excise relief, the June 16 decision could determine whether variable-rate business loans get more expensive on top of everything else landing on July 1.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/",

    "{{ECON_2_FLAG}}": "⛽ FUEL · SMALL BUSINESS",
    "{{ECON_2_HEADLINE}}": "Fuel Excise Cut Expires June 30 — Pump Prices to Jump ~26c/L on July 1 Unless Extended",
    "{{ECON_2_SUMMARY}}": "Australia's temporary 50% fuel excise reduction — cutting petrol and diesel excise from 52.6c/L to 26.3c/L since April 1 — expires at the end of June. Unless extended by the government, pump prices will jump roughly 26 cents per litre on July 1, the same day the national minimum wage and award rates increase. No extension has been committed to. For a trades business running vehicles and plant daily, the simultaneous 26c/L fuel rise and wage increase means two compounding margin pressures arriving together — and there are now only 24 days to price that into quotes.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 USA · ANTHROPIC",
    "{{TECH_1_HEADLINE}}": "Anthropic Moves Toward IPO at Near $1 Trillion Valuation — Daniela Amodei Defends AI's Return on Investment",
    "{{TECH_1_SUMMARY}}": "Anthropic co-founder and President Daniela Amodei appeared publicly on June 4 to defend the economics of AI development, telling TechCrunch that enterprise demand for Claude — particularly for coding and agentic workflows — was accelerating faster than infrastructure costs. The comments came days after Anthropic filed a confidential draft S-1 with the SEC, the first step toward a public listing at a valuation near $965 billion, with annualised revenue reported at $47 billion. Amodei pushed back firmly against analysts questioning AI's return on investment, saying commercial deployment in real workflows — not benchmark scores — would settle the debate in 2026.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/06/04/ahead-of-its-ipo-anthropics-daniela-amodei-shrugs-off-doubts-about-ais-returns/",

    "{{TECH_2_FLAG}}": "💻 USA · OPENAI",
    "{{TECH_2_HEADLINE}}": "OpenAI Rolls Out Dreaming V3 — ChatGPT Now Synthesises Your Conversation History Overnight",
    "{{TECH_2_SUMMARY}}": "OpenAI began rolling out Dreaming V3 — a new background memory architecture for ChatGPT — to Plus and Pro users in the US from June 4. Unlike previous memory that stored explicit notes, Dreaming V3 runs synthesis processes after each conversation, extracting patterns, preferences and context across all previous sessions. The system is around five times more compute-efficient than its predecessor, enabling free-tier access. For business users, it means ChatGPT should progressively understand your business context, communication style and preferences without needing re-briefing every session — practical for anyone using it regularly for quoting, planning or drafting.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 AUSTRIA · ICRA 2026",
    "{{ROBOT_1_HEADLINE}}": "AGIBOT World Challenge Brings 526 Teams to ICRA 2026 Vienna — Real Robots, Real Tasks, No Simulations",
    "{{ROBOT_1_SUMMARY}}": "Embodied AI company AGIBOT hosted the AGIBOT World Challenge 2026 alongside the IEEE International Conference on Robotics and Automation (ICRA 2026) in Vienna this week, drawing 526 research and enterprise teams from 27 countries. Unlike previous robotics competitions judged on simulation scores, all tasks were evaluated on real AGIBOT G2 humanoid robots performing closed-loop dexterous manipulation — picking, placing, assembling — without any simulation shortcuts. The shift signals a maturation in the field: real-world performance on physical hardware is now the benchmark that matters, and the gap between simulated ability and physical deployment is being closed rapidly.",
    "{{ROBOT_1_URL}}": "https://www.tradingview.com/news/eqs:09f22872d094b:0-agibot-world-challenge-2026-advances-embodied-ai-competition-from-simulation-to-real-robot-testing-at-icra-2026/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Face Switzerland Tonight in Final World Cup Warmup — Eight Days Until the Tournament Begins",
    "{{AUS_1_SUMMARY}}": "Australia's national squad takes on Switzerland in San Diego tonight (Saturday AEST) in their final preparatory match before the FIFA World Cup 2026 opens June 12 across the US, Canada and Mexico. Coach Tony Popovic's 26-man squad is notably young — 17 players set to make their World Cup debuts — with veterans Mathew Ryan and Mathew Leckie appearing in their fourth tournament. The Socceroos open Group D against Turkey in Vancouver on June 14, face co-host USA on June 20, then Paraguay on June 26.",
    "{{AUS_1_URL}}": "https://footballaustralia.com.au/",

    "{{AUS_2_HEADLINE}}": "Australia Commits AUD $5M to Ebola Response as Central Africa Outbreak Passes 600 Cases",
    "{{AUS_2_SUMMARY}}": "Foreign Minister Penny Wong announced a AUD 5 million emergency contribution to the global Ebola response on June 5, as confirmed cases in the Democratic Republic of Congo and neighbouring countries surpassed 600 for the current outbreak. Australia's funding will support WHO-led containment including vaccination teams, laboratory capacity and safe-burial protocols. Wong described the contribution as part of Australia's 'enduring commitment to global health security.'",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Oz Comic-Con Opens at MCEC Today; Science Gallery Melbourne Launches EMERGENCE[Y] Exhibition",
    "{{VIC_1_SUMMARY}}": "Melbourne is hosting two major events this weekend. Oz Comic-Con opens today at the Melbourne Convention and Exhibition Centre for its 2026 run, drawing thousands of fans across cosplay, gaming, collectibles and creator panels. Simultaneously, Science Gallery Melbourne launches EMERGENCE[Y] — a new exhibition running until December 5 bringing together artists, researchers and designers to examine how humanity might adapt to a rapidly changing planet. Both events are on across the weekend.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 PHYSICS · EPFL",
    "{{SCI_1_HEADLINE}}": "Scientists Fold a 42-Centimetre Laser Cavity to the Size of a Matchhead — 20 Years After It Was Declared Impossible",
    "{{SCI_1_SUMMARY}}": "Researchers at EPFL in Switzerland published a paper in Nature on June 3 describing the first chip-scale ultrafast laser to match the performance of a full-sized tabletop femtosecond system — a result the field had sought for over two decades. The team folded a 42-centimetre laser cavity into a space the size of a matchhead using a Mamyshev oscillator design, delivering 1.05 nanojoule pulses as short as 147 femtoseconds. Because photonic chips can be manufactured at wafer scale, more than 1,000 such laser cavities can be produced simultaneously — opening a path to cheap, portable ultrafast lasers for medical diagnostics, atomic clocks, precision sensing and spectrometry. Professor Tobias Kippenberg called the achievement 'a holy grail of integrated photonics.'",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Help You Track Your Margins Job by Job — Before the Numbers Tell a Bad Story",
    "{{INSIGHT_BODY}}": "Most trades businesses find out they've lost margin when the end-of-year numbers land. By then, it's too late to fix the jobs that ate your profit. AI tools can change that cycle — but only if you feed them the right data. Take any completed job and prompt an AI assistant with your quoted hours, actual hours, material costs, and final invoice. Ask it to calculate your gross margin and compare it to your target rate. Do this for five or ten recent jobs and ask the AI to find the pattern: are you consistently losing on labour hours? Material waste? Scope creep after day one? The answers won't surprise you — but having them written down with a number attached makes it much harder to ignore. With July 1 bringing both a wage increase and the end of the fuel excise cut, tracking margin job by job stops being a nice habit and starts being how you stay solvent.",

    # Fun Facts
    "{{FACT_1}}": "The average person walks approximately 160,000 kilometres over their lifetime — roughly four times around the Earth's circumference. Working-age adults typically cover 8,000 to 10,000 kilometres per year on foot. Tradies who spend their careers moving across job sites, up ladders and along scaffolding almost certainly log well above the average desk worker's tally.",

    "{{FACT_2}}": "Commercial aircraft windscreens are certified to survive a direct strike from a 1.8 kilogram bird at cruising speed without shattering — tested by firing a defrosted chicken from a compressed-air cannon at the glass. The same cannon is used to certify jet engine fan blades and high-speed train windscreens. The test is required before any new windscreen design is cleared for flight.",

    "{{FACT_3}}": "The Coriolis effect does not reliably determine which way water spirals down a drain or toilet — despite the widely held belief that it runs clockwise in the northern hemisphere and anticlockwise in the south. In practice, rotation in a small fixture is dominated entirely by the basin's geometry and the direction of the initial water flow. The Coriolis effect only becomes significant at scales of hundreds of kilometres — the size of weather systems.",

    # Joke
    "{{JOKE_SETUP}}": "Why do tradies make the best World Cup fans?",
    "{{JOKE_PUNCHLINE}}": "They've spent years watching jobs drag on past the deadline and still believing the finish line is just around the corner.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The pessimist complains about the wind; the optimist expects it to change; the realist adjusts the sails.”",
    "{{CLOSING_ATTR}}": "— William Arthur Ward",
    "{{CLOSING_MESSAGE}}": "A cool Saturday morning in Carrum Downs with showers possible before things clear this afternoon — good weather for getting the admin done without feeling guilty about being inside. The Socceroos face Switzerland in San Diego tonight, just eight days before the World Cup proper kicks off. With June 30 only 24 days out, the fuel excise cut expiring and award rates rising simultaneously on July 1 is a double hit worth pricing into your quotes this weekend. Enjoy the football tonight, Liall.",
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
