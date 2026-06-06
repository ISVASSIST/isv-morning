#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 07 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 7 Jun
    # Cool winter week; light showers Wednesday, otherwise mostly clear
    "{{WEATHER_1}}": "SUN 7 · ☁ Partly cloudy · 8–15°C",
    "{{WEATHER_2}}": "MON 8 · ⛅ Clearing · 9–16°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "TUE 9 · 🌤 Mostly clear · 9–17°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "WED 10 · 🌧 Light showers · 12–16°C",
    "{{WEATHER_5}}": "THU 11 · ⛅ Patchy cloud · 13–18°C",
    "{{WEATHER_ALERT}}": "⚽ WORLD CUP OPENS IN 4 DAYS",

    # World
    "{{WORLD_1_FLAG}}": "🌍 MIDDLE EAST · IRAN-GULF WAR",
    "{{WORLD_1_HEADLINE}}": "Iranian Missiles Target Kuwait and Bahrain — US Strikes Iran Radar Sites as Conflict Nears 100 Days",
    "{{WORLD_1_SUMMARY}}": "Iran launched ballistic missiles at US military bases in Kuwait and Bahrain on Saturday, and sent attack drones toward the Strait of Hormuz — prompting American forces to intercept six of seven incoming missiles and strike Iranian radar facilities on Qeshm Island and at Goruk. Kuwait's army confirmed engaging seven missiles, with material damage but no reported casualties. Pakistan's Interior Minister arrived in Tehran on Saturday offering new proposals to revive stalled peace talks, as Secretary of State Rubio paradoxically declared the war \"over\" — even as the exchange of strikes continued. The conflict is now approaching 100 days with no ceasefire framework in place.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/liveblog/2026/6/6/iran-war-live-us-says-iranian-drones-shot-down-radar-sites-attacked",

    "{{WORLD_2_FLAG}}": "🗳 SOUTH AMERICA · PERU",
    "{{WORLD_2_HEADLINE}}": "Peruvians Vote Today in Presidential Runoff — Keiko Fujimori and Roberto Sánchez Statistically Tied",
    "{{WORLD_2_SUMMARY}}": "Polling stations opened Sunday across Peru for the decisive second-round presidential election between right-wing Keiko Fujimori (Popular Force) and left-wing Roberto Sánchez (Juntos por el Perú), with the latest Ipsos survey putting both candidates at roughly 43% — the tightest runoff in decades. Fujimori is running on security and free-market economics; Sánchez on poverty reduction and partial resource nationalisation. The result will reshape Peru's policy direction significantly, with particular implications for mining, energy and social spending in Latin America's fourth-largest economy.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/6/5/fujimori-vs-sanchez-what-to-know-about-perus-presidential-run-off-election",

    # Economics
    "{{ECON_1_FLAG}}": "💼 ECONOMY · FAIR WORK",
    "{{ECON_1_HEADLINE}}": "Wage Umpire Lifts Minimum Pay 4.75% from July 1 — Employers Warn of \"Tipping Point\" for Small Business",
    "{{ECON_1_SUMMARY}}": "The Fair Work Commission handed down its 2026 Annual Wage Review on June 2, lifting the national minimum wage by 6% to $26.44/hour and award rates across most classifications by 4.75%, effective 1 July 2026. Unions welcomed the result as a real wage increase above 4.2% CPI; employer groups warned it could push marginal small businesses over the edge. For a trades operator running two or three employees on award rates, the increase adds hundreds of dollars per month in payroll costs — arriving the same day the temporary fuel excise cut expires and full diesel excise returns.",
    "{{ECON_1_URL}}": "https://www.sbs.com.au/news/article/2026-national-minimum-wage-decision/3eoj4s9iz",

    "{{ECON_2_FLAG}}": "⛽ FUEL · SMALL BUSINESS",
    "{{ECON_2_HEADLINE}}": "Fuel Excise Cut Expires June 30 — No Extension Confirmed as Government Weighs Billion-Dollar Budget Cost",
    "{{ECON_2_SUMMARY}}": "Australia's temporary 50% fuel excise cut — reducing petrol and diesel excise from 52.6c/L to 26.3c/L since April 1 — expires on June 30, with no extension yet confirmed. If left to lapse, pump prices jump roughly 26 cents per litre on July 1, compounding simultaneously with the wage rise. The government has left the door open to an extension but the budget cost runs into billions. ACCC monitoring confirms the cut was passed through at the pump; the snapback, if unaddressed, will be equally direct for anyone running vehicles, plant or generators.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🚗 EUROPE · AUTONOMOUS VEHICLES",
    "{{TECH_1_HEADLINE}}": "Spain Gets Europe's First Commercial Robotaxi — WeRide, Uber and AVOMO Launch in Madrid",
    "{{TECH_1_SUMMARY}}": "WeRide, Uber and Spanish operator AVOMO announced the launch of Spain's first commercial robotaxi service on June 2, with rides available via the Uber app in the Madrid region. The fleet scales progressively from supervised operation to fully driverless commercial service, with WeRide providing the autonomous driving technology. Madrid becomes the 12th city globally to host WeRide robotaxi operations and the first in continental Europe. The launch puts pressure on regulators in other countries — including Australia — to clarify their own frameworks for driverless commercial passenger services.",
    "{{TECH_1_URL}}": "https://cnevpost.com/2026/06/02/weride-uber-to-launch-first-commercial-robotaxi-service-spain/",

    "{{TECH_2_FLAG}}": "💻 CHINA · AI MODELS",
    "{{TECH_2_HEADLINE}}": "MiniMax Launches M3 — Open-Weight AI with 1 Million Token Context at One-Twentieth the Compute Cost",
    "{{TECH_2_SUMMARY}}": "Chinese AI company MiniMax released M3 on June 1 — an open-weight model with frontier-level coding, native multimodality, and a 1-million-token context window at just 1/20th the per-token compute of its previous generation. Prefill runs 9× faster and decoding 15× faster at maximum context, making very large document processing commercially viable. API pricing starts at $0.30 per million tokens, dropping to roughly $0.06 with cache optimisation; open weights are expected on Hugging Face shortly. For trades businesses, the practical implication is AI assistants that can eventually review your entire quote and job history in a single session — without needing to re-brief them from scratch.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 CHINA · BYD",
    "{{ROBOT_1_HEADLINE}}": "BYD Confirms Humanoid Robot Program — 20,000 Factory Units This Year, Open Platform and Dealer Sales to Follow",
    "{{ROBOT_1_SUMMARY}}": "Chinese EV giant BYD confirmed on June 3–4 that it is entering the humanoid robotics market with an internal programme codenamed 'Yao-Shun-Yu', developed since 2022 inside its electronic integration division. Around 150 prototype units are already deployed in BYD's own factories, with a target of 20,000 internal units in 2026 and a new Xi'an industrial park designed for 50,000 units per year. BYD plans an open robot platform accommodating third-party designs, and future household robots may be sold through its automotive dealer network. The announcement adds the world's largest EV maker to the list of manufacturing giants operating their own in-house humanoid robot programmes.",
    "{{ROBOT_1_URL}}": "https://cnevpost.com/2026/06/03/byd-enters-humanoid-robot-market/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Name World Cup Squad — 17 Debutants Join Veterans Leckie and Ryan for Group D Campaign",
    "{{AUS_1_SUMMARY}}": "Football Australia has confirmed the CommBank Socceroos' 26-man squad for FIFA World Cup 2026, featuring 17 first-timers alongside veterans Mathew Leckie and Mat Ryan, who equal a national record by appearing at their fourth World Cup. Two uncapped players — Cristian Volpato and Tete Yengi — are included. Australia opens Group D against Turkey in Vancouver on June 14, faces co-host USA on June 20, then Paraguay on June 26.",
    "{{AUS_1_URL}}": "https://footballaustralia.com.au/news/commbank-socceroos-squad-named-fifa-world-cup-2026tm",

    "{{AUS_2_HEADLINE}}": "Australia Commits $5M to WHO Ebola Response as Central Africa Outbreak Passes 600 Cases",
    "{{AUS_2_SUMMARY}}": "Foreign Minister Penny Wong announced a $5 million emergency contribution to the global Ebola response on June 5, as confirmed cases in the DRC-centred outbreak surpassed 600. Funding supports WHO vaccination teams, laboratory capacity and safe-burial protocols. Wong described the contribution as part of Australia's 'enduring commitment to global health security.'",

    # Victoria
    "{{VIC_1_HEADLINE}}": "RISING Festival Closes This Weekend — Final Chance for Melbourne's Biggest New Art Event Before Monday",
    "{{VIC_1_SUMMARY}}": "RISING 2026 — Melbourne's annual festival of new art, performance and music — enters its final weekend today, closing Monday June 9. Running since May 28 across 60+ events and 50 venues, the festival spans site-specific performance, large-scale visual art, live music and theatre throughout the CBD and inner suburbs. Today is one of the last chances to catch anything still on the program.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 BIOLOGY · DARTMOUTH",
    "{{SCI_1_HEADLINE}}": "Octopuses Learn to Use Mirrors to Find Hidden Food — First Invertebrate to Show Mirror-Mediated Spatial Cognition",
    "{{SCI_1_SUMMARY}}": "Researchers at Dartmouth College have demonstrated for the first time that California two-spot octopuses (Octopus bimaculoides) can learn to use mirrors to locate food hidden completely outside their line of sight — a form of mediated spatial perception previously documented only in vertebrates. Published in Current Biology on June 3, the study showed octopuses processed mirror reflections to intercept prey concealed behind barriers, mentally linking a visible image to a real location they could not directly see. While the team stops short of claiming mirror self-recognition, the finding extends cognitive skills previously considered exclusive to mammals, birds and fish deep into invertebrate territory — adding further evidence that cephalopod intelligence is far more sophisticated than long assumed.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How a Sunday Night AI Session Can Set Your Business Up to Win the Week",
    "{{INSIGHT_BODY}}": "A 20-minute conversation with an AI assistant on a Sunday evening can completely change how your Monday morning starts. Brief it on your job schedule for the coming week, outstanding quotes, follow-ups you've been putting off, and the risks you're watching — whether that's a materials delivery, a tight deadline, or an invoice that's overdue. Ask it to flag gaps in your schedule, prioritise your callbacks, draft two or three follow-up messages ready to send at 7am Monday, and identify any materials you need to order before they cause a site delay. Most tradies go into Monday reactive — scrambling, catching up, making decisions without the full picture. The ones winning right now go in prepared. Twenty minutes on Sunday night doesn't eat into your weekend — it buys back two or three hours on Monday and gets you in front of problems before they become costs.",

    # Fun Facts
    "{{FACT_1}}": "Australia is the only country to have had a piece of NASA infrastructure crash on its territory — Skylab debris scattered across Western Australia's Balladonia region in 1979, and the Shire of Esperance fined NASA $400 for littering. NASA paid the fine in 2009, thirty years later, after a US radio presenter raised the money from listeners.",

    "{{FACT_2}}": "Saturn's rings are just 10 to 30 metres thick on average despite spanning 282,000 kilometres from edge to edge. If you scaled Saturn down to the size of a basketball, its rings would be roughly as thick as a sheet of paper — a structure that vast and that thin would be essentially invisible to the naked eye if held at arm's length.",

    "{{FACT_3}}": "Cooking in a cast iron pan measurably increases the iron content of food. Eggs scrambled in a cast iron pan contain up to five times more dietary iron than the same eggs cooked in a non-reactive stainless steel pan. The effect is most pronounced with acidic ingredients — tomato sauce, citrus or vinegar — where the acid draws iron from the pan directly into the food.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the kitchen fitter always get five-star reviews?",
    "{{JOKE_PUNCHLINE}}": "He was the only tradie whose cabinets closed on the day he said they would.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Perseverance is not a long race; it is many short races one after the other.”",
    "{{CLOSING_ATTR}}": "— Walter Elliot",
    "{{CLOSING_MESSAGE}}": "A cool Sunday morning in Carrum Downs — partly cloudy and around 15°C, which is about as good as winter gets down this end of Port Phillip Bay. Peru is voting today in one of the tightest presidential runoffs in decades, and the World Cup opens in four days. With July 1 now under 25 days away and the fuel excise cut expiring the same day as the wage rise, it's worth running the numbers on what that double hit actually means for your job pricing — 20 minutes with an AI this morning beats a nasty surprise on a Tuesday in July. Have a good one, Liall.",
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
