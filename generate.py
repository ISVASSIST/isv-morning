#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 28 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 28 Jun
    # Wet Sunday; rain continues Monday; drying from Tuesday EOFY
    "{{WEATHER_1}}": "SUN 28 · 🌧 Showers likely · 7–12°C",
    "{{WEATHER_2}}": "MON 29 · 🌦 Rainy · 6–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 30 EOFY · ⛅ Mostly cloudy · 8–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "WED 1 JUL · 🌤 Fine and cold · 9–15°C",
    "{{WEATHER_5}}": "THU 2 · ⛅ Partly cloudy · 8–14°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS SUN–MON · EOFY TUE 30",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸 US · IRAN · CEASEFIRE",
    "{{WORLD_1_HEADLINE}}": "US Launches Strikes on Iranian Military Sites After Drone Attack on Strait of Hormuz Shipping",
    "{{WORLD_1_SUMMARY}}": "President Trump accused Iran of a \"foolish violation\" of the June ceasefire after Iranian drones targeted cargo ships transiting the Strait of Hormuz. US Central Command struck Iranian missile launch sites, drone storage facilities and coastal radar installations on Friday night. The attacks came weeks after the US and Iran signed a memorandum of understanding to reopen the critical oil corridor, and directly undermine that agreement. Oil prices edged higher as markets absorbed the renewed tension. Iran's top negotiator said its military remains \"ready to respond\" while Trump insisted the ceasefire remains technically intact.",
    "{{WORLD_1_URL}}": "https://www.pbs.org/newshour/world/u-s-strikes-iran-in-response-to-drone-attack-on-cargo-ship-that-trump-says-violated-ceasefire",

    "{{WORLD_2_FLAG}}": "🇻🇪 VENEZUELA · EARTHQUAKE",
    "{{WORLD_2_HEADLINE}}": "Venezuela Earthquake Death Toll Reaches 1,430 — Search-and-Rescue Window Closing as Aid Effort Struggles",
    "{{WORLD_2_SUMMARY}}": "The death toll from the twin magnitude 7.5 and 7.2 earthquakes that struck Venezuela on June 24 has risen to 1,430, with more than 3,200 injured across La Guaira and Caracas. Rescue teams continue to work collapsed buildings as the critical 72-hour search-and-rescue window has now passed. The earthquakes are Venezuela's deadliest since a catastrophic quake flattened Caracas in 1900. The country's pre-existing economic collapse and strained international relations have complicated aid delivery, with global relief organisations reporting logistical and diplomatic barriers slowing response.",
    "{{WORLD_2_URL}}": "https://abcnews.com/International/live-updates/venezuela-earthquakes-updates/?id=134196335",

    # Economics
    "{{ECON_1_FLAG}}": "🪙 AUS ECONOMY · FUEL EXCISE ENDS MONDAY",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Relief Ends Tomorrow — Tradies Face Immediate 26c/Litre Rise at the Pump from Tuesday",
    "{{ECON_1_SUMMARY}}": "The temporary halving of Australia's fuel excise duty — which has been cutting approximately 26.3 cents per litre from petrol and diesel prices since April 1 — expires at midnight Monday June 30. From Tuesday July 1, pump prices rise by that full amount. The ACCC's most recent weekly monitoring shows retail diesel sitting around $1.87 per litre in major cities before the excise return. With 72% of Australian businesses reporting negative fuel cost impacts across 2026, the increase lands alongside simultaneous rises in minimum wages, superannuation, and energy tariffs on the same day. Trades and transport operators who have not reviewed their July pricing structure this weekend will feel it immediately on the first job of FY2027.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🏠 PROPERTY · AUSTRALIA · MARKET COOLING",
    "{{ECON_2_HEADLINE}}": "Auction Clearance Rate Falls Below 50% for First Time Since COVID — Negative Gearing Uncertainty Bites",
    "{{ECON_2_SUMMARY}}": "Australia's combined capital city auction clearance rate dropped to 47.4% in the week ending June 21 — the first time it has fallen below 50% since April 2020. The May Budget's proposed changes to negative gearing (restricting it to new homes from July 2027) and the capital gains tax discount (dropping from 50% to 30%) have cooled investor appetite and reduced borrowing capacity by up to 30% for some buyers. For small trades businesses in the renovation, fit-out and maintenance space, a sustained slowdown in investor-driven property activity typically translates to fewer discretionary projects in the twelve months ahead.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔬 IBM · CHIP TECH · SUB-1NM",
    "{{TECH_1_HEADLINE}}": "IBM Packs 100 Billion Transistors onto a Fingernail-Sized Chip — 50% Faster or 70% More Energy-Efficient Than Current Best",
    "{{TECH_1_SUMMARY}}": "IBM unveiled the world's first sub-1 nanometer chip architecture on June 25, stacking transistors vertically in a 3D \"NanoStack\" design at the 0.7nm node. The result: nearly 100 billion transistors on a processor the size of a fingernail — almost twice the density of its previous 2nm generation. IBM projects the architecture will deliver 50% higher computing performance or 70% better energy efficiency compared to current chips. The breakthrough is expected to underpin next-generation AI hardware, with commercial adoption possible within five years. The design goes beyond physical limits that were thought to constrain conventional chip-making by building up rather than sideways.",
    "{{TECH_1_URL}}": "https://newsroom.ibm.com/2026-06-25-ibm-debuts-worlds-first-sub-1-nanometer-chip-technology",

    "{{TECH_2_FLAG}}": "🍎 APPLE · SIRI AI · iOS 27",
    "{{TECH_2_HEADLINE}}": "Apple Rebuilds Siri From Scratch With Google Gemini — iOS 27 Bets on Practical, Embedded AI for Every App",
    "{{TECH_2_SUMMARY}}": "Apple's WWDC 2026 revealed a completely rebuilt Siri, developed in partnership with Google and running on Apple Foundation Models plus Gemini. The new Siri can access the internet, retain personal context across conversations, and take action across apps. iOS 27 embeds AI into Photos, Safari, Messages, Mail, Calendar and Shortcuts — organising tabs, creating calendar events from natural language, providing contextual assistance during phone calls, and grouping smart home notifications intelligently. Available on iPhone 15 Pro and later when iOS 27 ships in autumn 2026. Apple's bet: AI is most valuable when it works invisibly inside the tools you already use, not as a separate chatbot you open deliberately.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 ROBOTICS · MID-2026 · INDUSTRY PICTURE",
    "{{ROBOT_1_HEADLINE}}": "Industrial Robot Orders Hold Steady as Humanoid Supply Begins to Outpace Near-Term Demand — Mid-2026 Industry Analysis",
    "{{ROBOT_1_SUMMARY}}": "A new mid-year robotics industry analysis finds that traditional industrial robot orders remain stable despite the headlines dominated by humanoid platforms. Autonomous Mobile Robots (AMRs) are now operating commercial shifts at Toyota manufacturing sites in North America under robots-as-a-service contracts. Meanwhile, humanoid robot production capacity from major manufacturers is beginning to outpace confirmed near-term industrial demand — suggesting the sector is scaling faster than buyers can absorb. For Australian manufacturing and trades operators weighing automation investment, the practical picture is unchanged: proven AMR and collaborative robot technology offers the lower-risk entry point, while humanoid platforms continue maturing toward reliable commercial deployment in the next two to three years.",
    "{{ROBOT_1_URL}}": "https://www.marketscale.com/industries/industrial-iot/humanoid-supply-outpaces-demand-amrs-hit-toyota-plants-and-robot-orders-hold-steady-automations-defining-stories-of-mid-2026/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Doubles Social Media Ban Fines to $99M as 85% of Under-16s Still Using Banned Platforms",
    "{{AUS_1_SUMMARY}}": "The Albanese government announced Friday it will double the maximum fine for platforms failing to keep under-16s off social media from $49.5 million to $99 million, and strengthen the eSafety Commissioner's powers. Despite the ban taking effect in December 2025, evidence shows 85% of 12-to-15-year-olds are still active on banned platforms. Facebook, Instagram, YouTube, Snapchat and TikTok are currently under eSafety investigation. Prime Minister Albanese said big tech is \"not doing enough to comply with the law\" and the new penalties signal the government intends to escalate enforcement.",
    "{{AUS_1_URL}}": "https://www.cnbc.com/2026/06/27/australia-toughens-kids-social-media-ban-doubles-tech-firm-fines.html",

    "{{AUS_2_HEADLINE}}": "Socceroos Face Egypt in World Cup Round of 32 — Match in Arlington, Texas at 4am AEST Next Saturday",
    "{{AUS_2_SUMMARY}}": "Australia sealed their place in the 2026 FIFA World Cup knockout stage with a 0-0 draw against Paraguay, their third time reaching the knockout rounds. The Socceroos will face Egypt in the Round of 32 next Saturday at 4am AEST at AT&T Stadium in Arlington, Texas. Cape Verde's stunning debut among the 48-team field and a first weekend of upsets across the bracket have made this one of the most open World Cups in years. Set the alarm.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Commits to Legislating a Right to Work From Home by September — A First in Australia",
    "{{VIC_1_SUMMARY}}": "The Victorian Government has committed to passing legislation establishing a formal right to work from home before September 2026, making Victoria the first Australian jurisdiction to enshrine remote work flexibility in law. The move will primarily affect office-based employees in sectors including administration, project management and engineering. For trades and field service businesses, the direct on-site impact is limited — but it signals a shift in workplace expectations that may influence how support roles are structured and recruited across the broader construction and services sector.",

    # Science
    "{{SCI_1_FLAG}}": "🌌 ASTRONOMY · BLACK HOLE · WHITE DWARF",
    "{{SCI_1_HEADLINE}}": "Astronomers May Have Captured the First Direct Evidence of an Intermediate-Mass Black Hole Devouring a White Dwarf Star",
    "{{SCI_1_SUMMARY}}": "Using data from China's Einstein Probe space telescope, an international research team believes they have witnessed an intermediate-mass black hole — the long-sought \"missing link\" between stellar and supermassive black holes — tearing apart and consuming a white dwarf star. The event produced a spectacular X-ray outburst alongside simultaneous gamma-ray bursts detected by NASA's Fermi Gamma-ray Space Telescope. Published June 25 via ScienceDaily, the observation would represent the first direct evidence of this class of cosmic event, and could help resolve longstanding questions about how the universe's most massive black holes built up their bulk over billions of years.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "New Financial Year, Clean Slate: The One-Hour AI Setup Worth Doing This Sunday",
    "{{INSIGHT_BODY}}": "The start of a new financial year is the single best moment to change how you run your business — not because the calendar forces it, but because everyone around you expects something to be different. For a trades operator, the window to build a new quoting habit, a new documentation workflow, or a new scheduling rhythm is wide open right now. AI tools are not magic, but they remove the friction that kills good intentions. Pick one process you currently handle manually that wastes fifteen or twenty minutes every time — a quote, a site inspection note, a job card, a completion email. Spend one hour this Sunday finding an AI tool or building a prompt template that handles it. That single investment, compounded across a hundred jobs in FY2027, saves more time than any productivity subscription you will pay for this year. New financial year. Clean sheet. One hour today, recurring payoff tomorrow.",

    # Fun Facts
    "{{FACT_1}}": "The 2026 FIFA World Cup is the first in history to feature 48 national teams — up from 32 in Qatar 2022 — producing 104 group stage matches across the United States, Canada and Mexico before the knockout rounds begin. It is the largest sporting event in history by total match count, and the first ever co-hosted by three nations simultaneously.",

    "{{FACT_2}}": "Portland cement — the most widely used construction material on Earth — was named not after a chemical formula but after the Isle of Portland in England. Victorian engineer Joseph Aspdin patented it in 1824 and called it \"Portland cement\" because the hardened product resembled the prized Portland limestone used in London's finest public buildings. Today it forms the backbone of virtually every concrete pour, mortar mix and render system in trades work globally.",

    "{{FACT_3}}": "Roman concrete, used to build the Pantheon dome in 125 AD and still structurally sound nearly 1,900 years later, actually gets stronger over time rather than weaker. When seawater infiltrates the mix, it triggers a mineral crystallisation process that progressively self-seals microcracks. Engineers at universities across the US and Europe are reverse-engineering ancient Roman marine concrete formulas hoping to produce modern mixes that far outlast the current 50-year design standard.",

    # Joke
    "{{JOKE_SETUP}}": "Why do carpenters make terrible liars?",
    "{{JOKE_PUNCHLINE}}": "Because the truth always comes out in the finish.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Don’t count the days; make the days count.”",
    "{{CLOSING_ATTR}}": "— Muhammad Ali",
    "{{CLOSING_MESSAGE}}": "It is a wet Sunday morning in Carrum Downs — showers likely today, rain continuing into Monday. The financial year ends in two days, and three major costs land simultaneously on Tuesday: fuel excise back at full rate, minimum wages up, superannuation at 12%. If your July pricing structure has not been reviewed yet, this morning is the window before it costs you on the first job of FY2027. On the better side of the ledger: the Socceroos are through to the World Cup Round of 32 and face Egypt next Saturday at 4am — set the alarm now. IBM has just announced a chip with 100 billion transistors packed onto something the size of your fingernail. Even on a cold, wet winter Sunday, the world is doing interesting things. Make it a good one.",
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
