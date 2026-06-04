#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 05 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 5 Jun
    # Cold front cleared overnight Thursday; showers easing Friday, brightening into the weekend
    "{{WEATHER_1}}": "FRI 5 · ⛅ Showers easing · 7–13°C",
    "{{WEATHER_2}}": "SAT 6 · 🌧 Showers possible · 9–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 7 · ☀ Mostly sunny · 11–17°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 8 · ☀ Mostly sunny · 9–18°C",
    "{{WEATHER_5}}": "TUE 9 · ⛅ Cloudy & cool · 8–15°C",
    "{{WEATHER_ALERT}}": "⚠ POST FRONT · SHOWERS EASING THIS MORNING",

    # World
    "{{WORLD_1_FLAG}}": "🌏 ASIA · NORTH KOREA",
    "{{WORLD_1_HEADLINE}}": "Kim Jong Un Unveils Third Nuclear Enrichment Plant — Vows 'Exponential' Arsenal Expansion",
    "{{WORLD_1_SUMMARY}}": "North Korea's Kim Jong Un inspected a newly operational nuclear materials facility on June 4, photographed walking between rows of uranium centrifuges. State media declared Pyongyang had more than doubled its weapons-grade uranium production capacity over the past five years, and Kim vowed to 'beef up' North Korea's nuclear forces 'at an exponential rate.' South Korea's military assessed the site as a uranium enrichment plant — North Korea's third publicly disclosed enrichment facility — believed to be at Yongbyon. The announcement marks a significant escalation and further complicates any prospect of US-led denuclearisation.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/06/04/g-s1-126041/north-korea-unveils-a-new-plant-to-produce-fuel-for-nuclear-weapons",

    "{{WORLD_2_FLAG}}": "🌍 MIDDLE EAST · CEASEFIRE",
    "{{WORLD_2_HEADLINE}}": "Gaza, Lebanon, Iran Ceasefires Are Fraying — Experts Warn the Word Has Lost Its Meaning",
    "{{WORLD_2_SUMMARY}}": "A Washington Post analysis published June 2 found that multiple simultaneous ceasefires across the Middle East — in Gaza, Lebanon and with Iran — are increasingly fragile and contested. In Gaza, Israel has carried out near-daily airstrikes since the October 2025 ceasefire took effect, killing more than 850 people. A senior UN official warned that failure to advance the peace framework risked leaving two million Palestinians without a viable future while cementing Israel's long-term presence in the shattered territory. The parallel Lebanon and Iran ceasefires show similar strains, with military activity continuing under the cover of technical truces.",
    "{{WORLD_2_URL}}": "https://www.washingtonpost.com/world/2026/06/02/iran-us-israel-gaza-lebanon-hamas-hezbollah-fighting-ceasefire/",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL · SMALL BUSINESS",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Cut Expires June 30 — Petrol and Diesel to Jump ~26c/L on July 1 Unless Extended",
    "{{ECON_1_SUMMARY}}": "Australia's temporary 50% fuel excise reduction — which slashed petrol and diesel excise from 52.6c/L to 26.3c/L from April 1 — expires at 11:59pm on June 30. Unless the government extends the measure, pump prices will jump by roughly 26 cents per litre on July 1 — the same day the national minimum wage and award rates increase. The ACCC is monitoring daily. The government has left the door open to extending the relief but has not committed. For trades businesses running vehicles and plant every day, the double hit of higher labour costs and a fuel price spike arrives simultaneously.",
    "{{ECON_1_URL}}": "https://fairworkmate.com.au/blog/fuel-excise-cut-ends-30-june-2026-what-happens-next",

    "{{ECON_2_FLAG}}": "🏦 ECONOMY · RBA",
    "{{ECON_2_HEADLINE}}": "RBA Cash Rate at 4.35% — June 16 Decision Has Economists Divided on Hold vs Another Hike",
    "{{ECON_2_SUMMARY}}": "Australia's Reserve Bank holds its next rate-setting meeting on June 16, with economists divided sharply on the outcome. Commonwealth Bank expects a pause after May's increase; Westpac tips another hike as underlying inflation runs at 3.7% — above the 2–3% target band. The RBA has already raised rates three times this year. GDP growth has been revised down to 1.3% for 2026 — its weakest in a decade — and staff forecasts have inflation remaining above 3% until late 2027. For small businesses navigating rising wage costs and expiring fuel relief, the June 16 decision is one to watch closely.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💻 USA · MICROSOFT BUILD",
    "{{TECH_1_HEADLINE}}": "Microsoft Unveils Own-Brand MAI Reasoning and Coding Models at Build 2026 — No OpenAI Required",
    "{{TECH_1_SUMMARY}}": "At Microsoft Build 2026 (June 2–3), Microsoft launched its first proprietary AI model suite: MAI-Thinking-1 — a reasoning model with 1 trillion total parameters that outperforms Claude Sonnet 4.6 in blind human preference tests on math and software engineering benchmarks — and MAI-Code-1-Flash, a fast coding model outperforming Claude Haiku-4.5 on core reasoning tasks. Both are trained entirely on Microsoft-owned commercially licensed data, with no distillation from third-party models — an explicit move to reduce dependency on OpenAI. MAI-Code-1-Flash is rolling out now to GitHub Copilot users in VS Code.",
    "{{TECH_1_URL}}": "https://www.neowin.net/news/microsoft-unveils-mai-thinking-1-reasoning-and-mai-code-1-coding-models/",

    "{{TECH_2_FLAG}}": "🔐 CYBERSECURITY · AI",
    "{{TECH_2_HEADLINE}}": "First Confirmed AI-Autonomous Cyberattack Exfiltrates Full Database in Under One Hour — No Human Required",
    "{{TECH_2_SUMMARY}}": "Sysdig researchers documented the first confirmed live cyberattack conducted entirely by an LLM agent, requiring no human direction after initial deployment. The agent exploited a known vulnerability, extracted cloud credentials, reached AWS Secrets Manager, and exfiltrated a full PostgreSQL database in four pivots — all in under an hour. The agent made real-time decisions, adapted when it hit unexpected outputs, and operated at a speed no human operator could match. Sysdig warned the incident marks a turning point: sophisticated multi-pivot intrusions that once required skilled operators can now be largely automated by AI.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 VIETNAM · ICRA 2026",
    "{{ROBOT_1_HEADLINE}}": "VinRobotics Debuts 'Made in Vietnam' VR-H3 Humanoid Robot at ICRA 2026 in Vienna",
    "{{ROBOT_1_SUMMARY}}": "VinRobotics — a subsidiary of Vietnamese conglomerate Vingroup — unveiled its third-generation VR-H3 humanoid robot at the IEEE International Conference on Robotics and Automation (ICRA 2026) in Vienna and COMPUTEX Taipei in early June 2026. The VR-H3 carries 31+ actuators and dual onboard edge computers, lifts 6–8 kg payloads, and can perform assembly operations. At ICRA, it demonstrated real-time teleoperation via VR headset with integrated motion capture — no external tracking equipment required. The launch marks Vietnam's first globally competitive humanoid robot, entering a market dominated by Chinese, US and European players.",
    "{{ROBOT_1_URL}}": "https://technode.global/2026/06/03/vietnams-conglomerate-vingroup-launches-humanoid-robots-on-global-stage/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australian Fans Spending $20,000–$25,000 to Chase Socceroos at the World Cup",
    "{{AUS_1_SUMMARY}}": "With the FIFA World Cup 2026 kicking off across North America on June 12, Australian fans following the Socceroos are facing the most expensive tournament travel in the event's history. FIFA's dynamic ticket pricing, surging hotel and flight costs driven by Middle East-related fuel prices, and long-haul North American travel have pushed total trip budgets to $20,000–$25,000 for many. The Socceroos open Group D against Turkey in Vancouver on June 14, face the US in Seattle, then Paraguay in Santa Clara.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/fifa-world-cup-2026/article/the-australian-fans-paying-up-to-25-000-for-their-fifa-world-cup-2026-dream/pe2workq9",

    "{{AUS_2_HEADLINE}}": "South Australia Hands Down Budget: $189M Surplus Forecast But Net Debt Heading for $53.6B by 2030",
    "{{AUS_2_SUMMARY}}": "South Australia's 2026–27 budget projects a $189 million operating surplus for the current financial year, but net debt is forecast to hit $53.6 billion by 2030 — costing taxpayers close to $5.3 million per day in interest alone, rising toward $8 million per day by 2029. The state maintains a AA+ credit rating and a net debt-to-revenue ratio second lowest nationally. The Allan government said the debt reflected necessary infrastructure investment; the opposition argued Labor had no credible plan to manage the trajectory.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Fed Square Confirmed as Melbourne World Cup Live Site — All Three Socceroos Group Games on Screen",
    "{{VIC_1_SUMMARY}}": "Victorian Premier Jacinta Allan stepped in to reverse an earlier Melbourne Arts Precinct decision not to host a World Cup live site at Federation Square. All three Socceroos group stage matches will be screened at Fed Square, with fencing, entry gates and bag searches in place for safety. Regional live sites are also confirmed at AAMI Park, Ballarat, Bendigo, Geelong, Gippsland and Shepparton. Football Australia called it a win for Victorian fans, with the tournament starting June 12.",

    # Science
    "{{SCI_1_FLAG}}": "🌍 GEOLOGY",
    "{{SCI_1_HEADLINE}}": "Scientists Confirm 'Impossible' Earthquake 90 Kilometres Deep in Utah — Rewriting What We Know About Solid Earth",
    "{{SCI_1_SUMMARY}}": "Researchers publishing via ScienceDaily on June 2 confirmed that a mysterious seismic event first detected near Utah in 1979 really did originate nearly 90 kilometres underground — far deeper than the established threshold for continental earthquakes, where rock is expected to slowly flow rather than fracture and snap. By reanalysing decades of seismic records, the team identified a rare class of 'continental mantle earthquakes' that challenge fundamental models of Earth's interior. The discovery suggests the upper mantle can sustain brittle fracture in ways not previously thought possible, with implications for earthquake hazard modelling in geologically complex regions worldwide.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI-Powered Invoice Follow-Up: The Easiest Revenue You're Not Chasing",
    "{{INSIGHT_BODY}}": "If you've got more than a handful of outstanding invoices right now, you're not alone — but you might be leaving real money on the table. Most trades operators follow up once, maybe twice, and then let it slide. An AI tool can help you close that gap in about ten minutes. Feed it your outstanding invoice list and ask it to draft tailored follow-up messages for each account: a friendly reminder at seven days overdue, a firmer nudge at thirty, and a formal notice past sixty. Vary the tone by customer relationship and job value. With EOFY landing on June 30 and two major cost increases arriving simultaneously on July 1 — both the fuel excise reversal and the award rate rise — getting your books clear before that date isn't just good practice. It's cash in hand when you need it most.",

    # Fun Facts
    "{{FACT_1}}": "The oldest known evidence of life on Earth sits in Western Australia. Stromatolites — fossilised mats built by ancient cyanobacteria — found in the Pilbara region are approximately 3.5 billion years old. These layered rock formations are still forming today at Shark Bay, making WA home to both the oldest traces of life on the planet and some of the only living examples of the organisms that created them.",

    "{{FACT_2}}": "FIFA World Cup 2026 is the first tournament with 48 teams — up from 32 in 2022 — spread across 16 four-team groups in three host nations: the United States, Canada, and Mexico. It requires 104 matches from June 11 to July 19, making it the largest World Cup in history. Australia's Socceroos are in Group D and play their first match against Turkey on June 14 in Vancouver.",

    "{{FACT_3}}": "Concrete quietly absorbs CO₂ over its entire lifetime through a natural chemical process called carbonation — atmospheric carbon dioxide reacts with calcium hydroxide in the cement paste, gradually locking it into stable calcium carbonate. Researchers estimate that buildings, bridges, pavements and demolition rubble worldwide collectively re-absorb approximately 4 billion tonnes of CO₂ per year — equivalent to around 43% of the carbon released during cement production in the first place.",

    # Joke
    "{{JOKE_SETUP}}": "What do you call a tradie who finishes every job on time, under budget, and has all invoices paid before June 30?",
    "{{JOKE_PUNCHLINE}}": "Their accountant's favourite client — and literally nobody else's.",

    # Closing
    "{{CLOSING_QUOTE}}": "“A ship in harbour is safe — but that is not what ships are built for.”",
    "{{CLOSING_ATTR}}": "— John A. Shedd",
    "{{CLOSING_MESSAGE}}": "Friday rolls in cold and clearing after Thursday's front swept through Carrum Downs — showers should ease through the morning and a brighter weekend is on the way. With EOFY now 25 days out and both the fuel excise cut and new award rates landing together on July 1, this is worth treating as a working Friday rather than a sliding one. A quiet morning is a good time to chase outstanding invoices, revisit your rate card, and get ahead of the paperwork before the double-hit arrives. The World Cup countdown is down to one week — Socceroos and Turkey in Vancouver next Saturday. Have a sharp end to the week, Liall.",
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
