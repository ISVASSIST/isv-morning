#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 18 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 18 Aug (BOM)
    "{{WEATHER_1}}": "TUE 18 · 🌤️ Morning fog clearing to a mild, mostly sunny day, winds picking up later · 12–20°C",
    "{{WEATHER_2}}": "WED 19 · 🌧️ Cold front crosses the state — windy with showers, possibly squally · 13–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 20 · 🌦️ Showers clearing behind the front into a cooler, breezy southwesterly · 10–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 21 · 🌥️ Intermittent cloud, slight chance of an isolated shower, breezy southerly · 12–16°C",
    "{{WEATHER_5}}": "SAT 22 · ☀️ Improving — partly cloudy clearing to mostly sunny, lighter winds · 9–18°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings for Carrum Downs or Melbourne metro land areas — just a Strong Wind Warning current for Port Phillip Wednesday as the cold front and squally northwesterlies move through, so it's worth locking in outdoor blasting or coating work today while it's still calm and mild",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇩 INDONESIA · EARTHQUAKE DEATH TOLL CLIMBS TO 68 AS THOUSANDS AWAIT AID ON INDEPENDENCE DAY",
    "{{WORLD_1_HEADLINE}}": "Death Toll From Indonesia's Flores Earthquake Climbs to 68 as Independence Day Aid Effort Struggles",
    "{{WORLD_1_SUMMARY}}": "The magnitude-7.7 quake that struck off Flores Island on Saturday has now killed at least 68 people and displaced nearly 13,000, with landslides still blocking roads into Nagekeo regency days later. It hit right as the country marked its 81st Independence Day, turning what's usually a national celebration into a disaster response — a grim reminder that when the ground actually moves, \"supply chain resilience\" stops being a buzzword and starts being aid trucks that can't get through.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/8/17/thousands-await-aid-after-deadly-indonesia-quake-as-rescue-work-conducted",

    "{{WORLD_2_FLAG}}": "🇺🇦🇷🇺 UKRAINE · RUSSIA HITS DANUBE PORT AFTER KYIV'S MASSIVE DRONE ATTACK, INJURING FOUR",
    "{{WORLD_2_HEADLINE}}": "Russia Strikes Ukraine's Danube River Port Hours After Kyiv's Massive Drone Barrage",
    "{{WORLD_2_SUMMARY}}": "Moscow retaliated for one of Ukraine's largest aerial attacks of the war by striking the Izmail port district on the Danube, damaging a Togo-flagged civilian vessel and injuring four people. Russia says it hit \"military cargo\" facilities; Ukraine says it was a trade and export lifeline — another reminder the war keeps grinding on with no ceasefire in sight, and that global shipping and grain routes remain hostage to it, which eventually shows up in everyone's cost of doing business.",
    "{{WORLD_2_URL}}": "https://www.cnbc.com/2026/08/17/ukraine-war-russia-putin-moscow.html",

    # Economics
    "{{ECON_1_FLAG}}": "🏗️🇦🇺 MIGRATION · BUSINESS AND MINING BOSSES WARN AGAINST CUTS AS WORKER SHORTAGE BITES",
    "{{ECON_1_HEADLINE}}": "Business and Mining Bosses Warn Against Migration Cuts as the 'War for Talent' Intensifies",
    "{{ECON_1_SUMMARY}}": "As federal cabinet weighs cutting the migration intake, business and mining leaders are pushing back hard — the Minerals Council says the industry alone needs 40,000 new migrant workers over the next three years just to staff approved projects. Australian Industry Group's Innes Willox says the country is in a \"war for talent\" it can't afford to lose. For a Carrum Downs blasting and coatings outfit that's felt how thin the trades labour pool already is, this is one to watch closely — tighter migration settings could make finding a qualified blaster or painter even harder before it gets easier.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-08-17/mining-business-immigrant-worker-skilled-visa-economy/107043674",

    "{{ECON_2_FLAG}}": "💰🇦🇺 SUPERANNUATION · HANSON WANTS EARLY SUPER ACCESS FOR COST-OF-LIVING RELIEF, CHALMERS HITS BACK",
    "{{ECON_2_HEADLINE}}": "Pauline Hanson Wants Australians to Raid Their Super for Cost-of-Living Relief — Chalmers Says She'd 'Destroy' It",
    "{{ECON_2_SUMMARY}}": "One Nation's Pauline Hanson, backed by Barnaby Joyce, is pushing to let financially stretched Australians dip into their super early to cope with mortgage and living pressures, calling the system \"broken.\" Treasurer Jim Chalmers shot back that the plan would gut retirement savings for short-term relief. For a small business owner whose super balance often doubles as the retirement plan, it's a fight worth watching — loosening the rules now could mean less compulsory saving discipline, and a smaller nest egg, down the track.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖⚠️ AI TOOLS · CLAUDE SUFFERS ANOTHER OUTAGE, 14TH DISRUPTION IN TWO WEEKS",
    "{{TECH_1_HEADLINE}}": "Claude Goes Down Again — 14th Anthropic Outage in Just Two Weeks",
    "{{TECH_1_SUMMARY}}": "Anthropic's Claude — including Claude Code and Claude Cowork — went offline for about 36 minutes on Sunday night after an authentication fault cascaded into degraded service across five products. It's the fourteenth incident logged on the company's status page in a fortnight, right as Claude use is exploding in business settings. If you're leaning on any AI tool for quotes, scheduling or admin, it's worth having a five-minute fallback plan for the day it quietly goes dark mid-task.",
    "{{TECH_1_URL}}": "https://www.bleepingcomputer.com/news/artificial-intelligence/anthropic-confirms-claude-is-down-in-major-outage-affecting-multiple-services/",

    "{{TECH_2_FLAG}}": "🤖🎭 AI SCAMS · ASIC WARNS OF SURGING AI DEEPFAKE SCAMS IMPERSONATING PUBLIC FIGURES",
    "{{TECH_2_HEADLINE}}": "ASIC Warns of Surging AI Deepfake Scams Impersonating the PM, Alan Kohler and Gina Rinehart",
    "{{TECH_2_SUMMARY}}": "The corporate regulator says scammers are churning out AI-generated deepfake videos of trusted public figures — including Anthony Albanese, journalist Alan Kohler and Gina Rinehart — to lend fake investment schemes credibility, part of a network that saw over 19,400 scam sites removed this year, up 182%. ASIC's blunt message: a quick Google search is no longer proof anything is legit. Worth passing on to anyone in the business handling invoices or bank transfers — the same AI polish making these scams convincing is exactly what's coming for \"urgent payment\" requests too.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖🏭 ROBOTICS · INDUSTRIAL ROBOT INSTALLATIONS HIT RECORD HIGHS AS LABOUR SHORTAGES BITE",
    "{{ROBOT_1_HEADLINE}}": "Industrial Robot Installations Hit Record Highs as Employers Can't Find Enough Staff",
    "{{ROBOT_1_SUMMARY}}": "Global industrial robot installations climbed 11% in 2025 to around 38,000 units, with food and hospitality operators leading the charge as they simply can't staff repetitive, physically demanding roles at a sustainable wage. The report frames it plainly: automation has stopped being an experiment and become an operational necessity wherever labour is tight — the same pressure a Carrum Downs blasting and coatings crew feels trying to fill site roles, just playing out on factory floors first.",
    "{{ROBOT_1_URL}}": "https://www.globenewswire.com/news-release/2026/08/17/3346097/0/en/industrial-robot-installations-hit-record-highs-amid-labor-shortage-crisis.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Royal Commission on Antisemitism Enters Its Final Hearing Block Ahead of Bondi Anniversary",
    "{{AUS_1_SUMMARY}}": "The Royal Commission on Antisemitism and Social Cohesion has opened its ninth and final hearing block in Sydney, running to 29 August, after taking evidence from hundreds of witnesses and more than 20,000 submissions since the Bondi Beach terror attack. Commissioner Virginia Bell says she won't seek an extension past the one-year deadline — a significant moment in the national response to the attack that reshaped security and public debate across the country this year.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-17/bondi-antisemitism-social-cohesion-royal-commission-block-9/107025136",

    "{{AUS_2_HEADLINE}}": "Food Delivery Riders Win 'World-Leading' Minimum Pay and Insurance Rules",
    "{{AUS_2_SUMMARY}}": "Australia's Fair Work Commission has switched on the country's first legally enforceable minimum standards for gig delivery riders, guaranteeing at least $31.30 an hour for \"engaged\" time plus vehicle and insurance protections for roughly 250,000 workers. Worth noting for any small business dabbling in contractor or app-based labour arrangements — this is the direction gig-economy regulation is heading, and \"independent contractor\" is getting a lot less independent.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Alleged Gangland Boss Fadi Haddara Fights for Life After Ambush Shooting in Altona North",
    "{{VIC_1_SUMMARY}}": "Fadi Haddara, allegedly the head of a namesake crime clan with long-running tensions over Melbourne's illicit tobacco trade, remains in critical condition after being ambushed and shot outside his Altona North home on Sunday night. Police say they'll do \"everything\" possible to stop it sparking a wider gang feud — a stark reminder that Melbourne's underworld tensions haven't gone anywhere, even while the rest of the city gets on with a fairly ordinary Tuesday.",

    # Science
    "{{SCI_1_FLAG}}": "🕳️🔭 SCIENCE · ASTRONOMERS SPOT TWIN BLACK HOLES FEEDING TOGETHER INSIDE A TINY GALAXY",
    "{{SCI_1_HEADLINE}}": "Astronomers Spot a Pair of Black Holes Feeding Together Inside a Tiny 'Green Pea' Galaxy",
    "{{SCI_1_SUMMARY}}": "Using Chandra X-ray data and Keck spectroscopy, astronomers have confirmed the first dual supermassive black hole system inside a \"Green Pea\" galaxy — a compact, intensely star-forming galaxy type considered a local stand-in for the young universe. The two black holes, in galaxy J1622+3521, sit about 27,000 light-years apart and are actively merging — proof there are still oddities hiding in plain astronomical sight after years of searching for exactly this.",

    # Business insight
    "{{INSIGHT_TITLE}}": "New Jobs Report Says Tradies Are Nearly AI-Proof — Your Office Isn't",
    "{{INSIGHT_BODY}}": "A national jobs and skills analysis reported this month ranked hands-on trades — alongside nurses, carers and cleaners — among the occupations least likely to ever be displaced by AI, thanks to the physical judgement and on-site problem-solving no model can replicate. The same research flags the opposite trend for office-based roles, with bookkeepers, receptionists and admin staff sitting near the top of the list for AI exposure. For a business like ISV, that's a useful signal about where to actually point the technology: not at replacing anyone on the tools, but at the quoting, scheduling, invoicing and phone-answering load that increasingly can be automated. Read it as permission to lean harder into AI for the back office precisely because the trade itself is the part of the business AI genuinely can't take off your hands.",

    # Fun facts
    "{{FACT_1}}": "Honey badgers can take a bite from a puff adder or cobra that would drop most mammals in seconds — a genetic quirk in their nerve receptors means the venom only causes a few hours of drowsy paralysis before they wake up, shake it off, and finish eating the snake that bit them.",
    "{{FACT_2}}": "The torque wrench was invented in 1918 by Conrad Bahr, an engineer with the New York City water department, who built it purely to stop crews cracking water-main fittings by over-tightening them by feel — it wasn't formally patented until 1935, and only spread industry-wide after Chrysler licensed a beam-style version in the late 1930s.",
    "{{FACT_3}}": "The \"Wilhelm Scream\" — a stock sound effect first recorded for the 1951 film Distant Drums — has since turned up in more than 400 movies and TV shows, including every mainline Star Wars film, as a long-running in-joke passed down between generations of sound editors.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pool cleaner become the most trusted guy on the whole street?",
    "{{JOKE_PUNCHLINE}}": "Because he was the only bloke everyone was happy to see skimming a bit off the top.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"It's not about ideas. It's about making ideas happen.\"",
    "{{CLOSING_ATTR}}": "— Scott Belsky",
    "{{CLOSING_MESSAGE}}": "It's a mild, fog-to-sunshine start to the week in Carrum Downs, with the calm holding until Wednesday's cold front brings wind and showers through — good conditions for getting outdoor blasting and coating work knocked over today while it lasts. Between a jobs report putting tradies near the top of the AI-proof list, twin black holes finally caught feeding inside a galaxy astronomers had been hunting for years, and Anthropic's own tools going down for the fourteenth time this fortnight, today's a fair reminder that the hands-on trade is still the part of the business no outage can touch.",
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
