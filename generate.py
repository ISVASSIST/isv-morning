#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 08 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 8 Jul (BOM / AccuWeather)
    "{{WEATHER_1}}": "WED 8 · 🌫️ Morning fog, clearing to sun · 4–13°C",
    "{{WEATHER_2}}": "THU 9 · ☁️ Cloudy periods, patchy frost · 3–13°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 10 · 🌤️ Mostly sunny · 8–16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 11 · 🌧️ Showers, breezy · 9–15°C",
    "{{WEATHER_5}}": "SUN 12 · ⛅ Partly cloudy, isolated shower · 8–13°C",
    "{{WEATHER_ALERT}}": "⚠ COOL FOGGY START TODAY · SHOWERS RETURN FROM SATURDAY, GET OUTDOOR PREP DONE WHILE IT'S DRY",

    # World
    "{{WORLD_1_FLAG}}": "🇨🇳 CHINA · MILITARY · RARE SUBMARINE BALLISTIC MISSILE TEST",
    "{{WORLD_1_HEADLINE}}": "China Test-Fires Submarine-Launched Ballistic Missile Into the Pacific on the Eve of the NATO Summit",
    "{{WORLD_1_SUMMARY}}": "China's navy publicly confirmed it fired a ballistic missile carrying a dummy warhead from a Type 094 nuclear-powered submarine into the Pacific, describing it as a routine annual exercise — but the timing, a day before NATO leaders gather in Ankara and alongside a joint drill with Russia, has been read as a deliberate show of strength. Australian Foreign Minister Penny Wong called the test \"destabilising to the region,\" with New Zealand and Japan issuing similar rebukes, as the launch effectively demonstrates China has now validated a full sea-based leg of its nuclear deterrent.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/7/6/china-missile-test-draws-criticism-from-australia-new-zealand-japan",

    "{{WORLD_2_FLAG}}": "🇴🇲 STRAIT OF HORMUZ · SHIPPING · TANKER SET ABLAZE OFF OMAN",
    "{{WORLD_2_HEADLINE}}": "Qatari LNG Tanker Set Ablaze in the Strait of Hormuz After Being Struck by a Projectile",
    "{{WORLD_2_SUMMARY}}": "The Qatari-flagged LNG tanker Al Rekayyat caught fire after being hit on its port side while sailing south out of the Strait of Hormuz near Limah, Oman, in the second such attack on shipping in the strait this week. Iranian state television said the vessel had ignored warnings but stopped short of an official claim, while Qatar condemned the strike as an \"unacceptable attack\" on international navigation — no injuries were reported, but the incident adds to pressure on a route that carries roughly a fifth of the world's traded oil.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/07/07/g-s1-132265/tanker-attack-strait-of-hormuz",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL EXCISE · COST OF LIVING · 16¢/L RELIEF EXTENDED TO 2 AUGUST",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Relief Extended to 2 August as Pump Prices Start Creeping Back Up",
    "{{ECON_1_SUMMARY}}": "The federal government has extended its temporary fuel excise cut — now trimmed to 16 cents a litre — through to 2 August, taking roughly $11 off a 65-litre tank, even as the ACCC's weekly monitoring shows capital-city petrol and diesel prices beginning to climb again as the earlier, deeper excise cut unwinds. For any business running a fleet of utes, vans or compressors, it's worth watching the bowser over the next few weeks rather than assuming the current relief carries on indefinitely.",
    "{{ECON_1_URL}}": "https://www.pm.gov.au/media/additional-fuel-excise-relief-month-july",

    "{{ECON_2_FLAG}}": "💰 RBA · CASH RATE · HOLDS AT 4.35%, NEXT CALL 11 AUGUST",
    "{{ECON_2_HEADLINE}}": "RBA Holds Cash Rate at 4.35% While It Watches Fallout From the Oil Supply Disruption",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank left the cash rate target unchanged at its last meeting, judging it appropriate to sit tight while it assesses both the effect of this year's earlier rate rises and the impact of Middle East oil disruptions on inflation. Housing prices have started easing in some capital cities and consumer spending growth is slowing as expected, with the board's next call not due until 11 August — so no fresh movement on borrowing costs is likely before then.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🎙️ OPENAI · VOICE AI · GPT-REALTIME-2.1 CUTS LATENCY FOR VOICE AGENTS",
    "{{TECH_1_HEADLINE}}": "OpenAI Ships GPT-Realtime-2.1, Cutting Latency for Production-Ready Voice Agents",
    "{{TECH_1_SUMMARY}}": "OpenAI has released gpt-realtime-2.1 and a cheaper mini version, trimming voice response latency by around a quarter and improving how the models handle noisy job sites, interruptions and alphanumeric details like phone numbers or job reference codes. It's aimed squarely at businesses building call-answering bots and after-hours enquiry lines rather than chasing a bigger, smarter model — a practical sign that voice AI is getting good enough to trust with real customer calls.",
    "{{TECH_1_URL}}": "https://www.marktechpost.com/2026/07/06/openai-gpt-realtime-2-1-mini-reasoning-realtime-api/",

    "{{TECH_2_FLAG}}": "🧠 ANTHROPIC · INFRASTRUCTURE · $19B, 20-YEAR KENTUCKY DATA CENTRE LEASE",
    "{{TECH_2_HEADLINE}}": "Anthropic Signs $19 Billion, 20-Year AI Data Centre Lease in Rural Kentucky",
    "{{TECH_2_SUMMARY}}": "Anthropic has signed a 20-year lease worth roughly $19 billion for around 401 megawatts of computing capacity at a converted bitcoin-mining site in Hawesville, Kentucky, with power coming online in phases from late 2027. It's another sign of just how much capital AI providers are locking in for raw compute — useful context next time a subscription price shifts or a model gets temporarily rationed, since demand for the underlying hardware still comfortably outstrips supply.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · APPTRONIK · ROBOT PARK OPENS, APOLLO 2 UNVEILED",
    "{{ROBOT_1_HEADLINE}}": "Apptronik Opens 'Robot Park' Training Facility in Texas and Unveils Its Apollo 2 Humanoid",
    "{{ROBOT_1_SUMMARY}}": "Humanoid robot maker Apptronik has opened an expanded data-collection and training facility in Austin, Texas, called Robot Park, alongside unveiling Apollo 2 in both bipedal and wheeled-base configurations. The data it gathers feeds directly into Google DeepMind's Gemini Robotics foundation models under the pair's research partnership — a reminder that the current bottleneck in industrial robotics isn't the hardware so much as the volume of real-world training data needed to make it reliable.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/07/06/apptronik-launches-robot-park-to-train-apollo-humanoid-robots-with-google-deepmind/103069/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia and Fiji Sign 'Ocean of Peace' Defence Pact as Albanese Wraps Up Pacific Tour",
    "{{AUS_1_SUMMARY}}": "Prime Minister Anthony Albanese capped a swing through Fiji and Solomon Islands by signing the Vuvale Union with Fijian PM Sitiveni Rabuka — Fiji's first-ever mutual defence pact, dubbed the \"Ocean of Peace\" and open to other Pacific nations to join. The trip, which also included becoming the first foreign leader to join Solomon Islands' independence day celebrations, is widely read as part of Canberra's push to shore up Pacific ties as China's regional military activity draws growing scrutiny.",
    "{{AUS_1_URL}}": "https://www.washingtonpost.com/world/2026/07/06/australia-fiji-china-defense-alliance/b723ed92-78f7-11f1-b194-f872dd4ec5aa_story.html",

    "{{AUS_2_HEADLINE}}": "New HELP Loan Repayment Rules Kick In, Easing the Squeeze for Younger Australians",
    "{{AUS_2_SUMMARY}}": "The threshold before HELP debt repayments kick in has jumped from $54,000 to $67,000, and repayments now apply only to earnings above that line rather than as a flat percentage of total income — meaning most borrowers, especially those under 35, will see more in their regular pay packet. If you've got apprentices or younger staff on the books with a HELP debt, it's worth flagging: smaller compulsory repayments mean the debt clears more slowly, even though annual indexation is now capped at the lower of inflation or wage growth.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Six-Hour Police Standoff Atop the Bolte Bridge Ends With Graffiti Tagger's Arrest",
    "{{VIC_1_SUMMARY}}": "A man climbed one of the Bolte Bridge's 140-metre pillars before dawn, abseiled down to spray a giant \"Pam the Bird\" tag, then refused to come down, triggering a six-hour standoff with police, water units and negotiators before he surrendered peacefully just after 11am. It's the latest chapter in a graffiti campaign that's already racked up an estimated $700,000 in damage to Melbourne landmarks — a reminder for anyone running a business with exposed walls or sheds that a quick coat of anti-graffiti coating is a lot cheaper than a repaint.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ MATERIALS SCIENCE · AI-ACCELERATED SUPERCONDUCTOR DISCOVERY",
    "{{SCI_1_HEADLINE}}": "Scientists Pair Machine Learning With Quantum Physics to Discover Two New Superconductors",
    "{{SCI_1_SUMMARY}}": "Researchers have combined machine learning with quantum physics calculations to identify two previously unknown superconductors, YRu3B2 and LuRu3B2, which get their superconductivity from electrons forming \"flat bands\" in a hexagonal kagome lattice pattern. More significant than the two materials themselves is the method — a much faster way to search vast chemical spaces for candidates — which researchers say meaningfully shortens the road toward the long-sought goal of a room-temperature superconductor.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Diesel Prices Are Moving Again — How AI Can Build a Fair Fuel Surcharge Into Every Quote",
    "{{INSIGHT_BODY}}": "With the fuel excise cut stepping down and bowser prices already creeping up, any business running compressors, generators or a fleet of utes is exposed to a cost that can swing well after a quote has already been accepted. A Fair Work Commission order earlier this year formally cleared the way for road transport businesses to pass on fuel cost rises through the contractual chain, and the same logic works for any trade: ask an AI tool to draft a short, transparent fuel surcharge clause tied to a public benchmark like the ACCC's weekly fuel price index, triggered only above a set threshold. Clients respond far better to a clear, pre-agreed formula than to an unexplained line item after the job's done.",

    # Fun Facts
    "{{FACT_1}}": "Spraying paint with compressed air dates back to the Southern Pacific Railroad in the early 1880s — more than 60 years before the aerosol spray can was developed in the 1940s as a US military tool for dispensing insecticide.",

    "{{FACT_2}}": "The 'Mechanical Turk', unveiled in 1770 by Hungarian inventor Wolfgang von Kempelen, appeared to be a chess-playing machine that beat the likes of Napoleon and Benjamin Franklin — it was actually an elaborate hoax, with a human chess master concealed inside operating its arm.",

    "{{FACT_3}}": "Official currency was so scarce in Australia's earliest colonial years that rum became the de facto medium of exchange — the military officers who controlled its supply, nicknamed the 'Rum Corps', grew so powerful they deposed the colonial governor in the 1808 Rum Rebellion, the only successful armed takeover of an Australian government.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the gutter installer never worry about cash flow?",
    "{{JOKE_PUNCHLINE}}": "Because in his business, everything eventually ran downhill.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"It does not matter how slowly you go as long as you do not stop.\"",
    "{{CLOSING_ATTR}}": "— Confucius",
    "{{CLOSING_MESSAGE}}": "It's a foggy, cool start across Carrum Downs this Wednesday, clearing to a mild afternoon — dry right through to Friday before showers roll back in for the weekend, so it's a good window to knock over any exposed prep work. Worth diarising that the fuel excise relief steps down again on 2 August, and if payday super has changed your pay run this month, keep an eye on that seven-day contribution window the ATO's now watching closely.",
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
