#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 12 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 12 Sep (BOM Melbourne-area forecast)
    "{{WEATHER_1}}": "SAT 12 SEP · ⛅ Partly cloudy, slight chance of a shower, light winds · 8–15°C",
    "{{WEATHER_2}}": "SUN 13 SEP · 🌦️ Partly cloudy, medium chance of a shower most likely early morning · 6–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 14 SEP · 🌧️ Cloudy, high chance of showers most likely afternoon and evening · 7–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 15 SEP · ☀️ Mostly sunny, winds turning northerly 25–40km/h, UV moderate · 9–19°C",
    "{{WEATHER_5}}": "WED 16 SEP · ⛈️ Cloudy, very high chance of rain as a strong northerly change moves through 35–50km/h · 11–18°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current for Victoria — a showery start to the weekend clears into a mostly sunny Tuesday as winds swing northerly, before a strong wind change brings a further rain risk through Wednesday.",

    # World
    "{{WORLD_1_FLAG}}": "🇸🇦 RIYADH · SAUDI ARABIA SHUTS KEY OIL PIPELINE AFTER DRONE ATTACKS",
    "{{WORLD_1_HEADLINE}}": "Saudi Arabia Shuts Its Key East-West Oil Pipeline After Drone Strikes Spark Fires at Pumping Stations",
    "{{WORLD_1_SUMMARY}}": "Saudi Arabia's energy ministry shut down the East-West pipeline — the kingdom's main workaround for shipping oil without transiting the Strait of Hormuz — as a precaution on Thursday after several drone strikes hit pumping stations in the Riyadh and Medina regions, sparking fires and causing injuries. A US official said the drones appeared to have launched from Iraq; the strike on one pumping station alone is estimated to have cut throughput by 700,000 barrels a day, adding fresh pressure to an already jumpy oil market.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/09/11/politics/saudi-arabian-oil-pipeline-hit-by-projectiles-triggering-fires",

    "{{WORLD_2_FLAG}}": "🇷🇺 SARATOV · UKRAINIAN DRONES SET RUSSIAN OIL REFINERY AND MAJOR WAREHOUSE ABLAZE",
    "{{WORLD_2_HEADLINE}}": "Ukrainian Drone Barrage Sets Russian Oil Refinery and Ozon Warehouse Ablaze in Saratov",
    "{{WORLD_2_SUMMARY}}": "A wave of Ukrainian drones struck the Rosneft-owned Saratov oil refinery and a major Ozon e-commerce warehouse overnight, sparking fires at both sites and prompting Ozon to suspend all orders and deliveries across the region. It's the latest in a sustained Ukrainian campaign against Russian energy and logistics infrastructure, this time reaching well south of the usual border regions.",
    "{{WORLD_2_URL}}": "https://kyivindependent.com/ukrainian-drones-reportedly-strike-saratov-oil-refinery-ozon-warehouse/",

    # Economics
    "{{ECON_1_FLAG}}": "📈 INTEREST RATES · RBA HIKE ODDS JUMP TO 80% AS OIL SPIKES",
    "{{ECON_1_HEADLINE}}": "RBA Rate-Hike Odds Hit 80% as Oil Tops $100 a Barrel, Australian Dollar Jumps",
    "{{ECON_1_SUMMARY}}": "Markets pushed the probability of a 25-basis-point RBA hike on 29 September to around 80% on Thursday, up sharply after July's hot inflation print and a stronger GDP number, sending the Australian dollar higher even as Brent crude broke back above US$100 a barrel on the Saudi pipeline attacks. A hike would take the cash rate to 4.60% and add roughly $121 a month to repayments on an average $731,000 mortgage — and typically flows through fast to overdraft and equipment-finance rates too.",
    "{{ECON_1_URL}}": "https://www.vantagemarkets.com/market-analysis/aud-usd-rba-hike-odds-oil-driven-dollar-september-11-2026/",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE PUMP PRICES HOLD NEAR 206C/L AHEAD OF OIL SPIKE FLOW-THROUGH",
    "{{ECON_2_HEADLINE}}": "Melbourne Unleaded Holds Near 206c/L, but This Week's Oil Price Jump Hasn't Hit the Bowser Yet",
    "{{ECON_2_SUMMARY}}": "Melbourne unleaded is averaging around 205–210c/L across the city's roughly 1,100 stations this week, with the cheapest sites still under 190c/L — but that snapshot predates this week's spike in global oil prices following the Saudi Arabia pipeline attacks, and pump prices typically take one to two weeks to catch up to a crude move. Worth locking in a fuel surcharge on quotes now rather than after the next price cycle turns.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📁 CLOUD FILES · CHATGPT LIBRARY NOW SEARCHES DROPBOX, BOX AND SHAREPOINT",
    "{{TECH_1_HEADLINE}}": "OpenAI Rolls ChatGPT's File Library Out to Dropbox, Box and SharePoint, No Re-Uploading Required",
    "{{TECH_1_SUMMARY}}": "ChatGPT's Library feature — previously limited to Google Drive — began rolling out access to Dropbox, Box and SharePoint files this week for Go, Plus, Pro, Business and Enterprise users on the web, letting you browse, search and @mention existing files straight into a chat instead of uploading them again. For a trade business already storing quotes, invoices and site photos across a mix of cloud folders, it's a small but genuine time-saver rather than a gimmick.",
    "{{TECH_1_URL}}": "https://itdaily.com/news/software/openai-chatgpt-connectors/",

    "{{TECH_2_FLAG}}": "💻 DESKTOP AI · GOOGLE SHIPS A DEDICATED GEMINI APP FOR WINDOWS",
    "{{TECH_2_HEADLINE}}": "Google Launches a Gemini Desktop App for Windows With Built-In Video Generation and Multi-Step AI Agents",
    "{{TECH_2_SUMMARY}}": "Google rolled out a dedicated Gemini app for Windows this week that sits in the system tray and pops open over whatever you're working on with Alt+Space, adding AI video generation and 'multi-agent' workflows that can handle multi-step tasks without constant prompting, plus direct links into Gmail and Google Drive to summarise documents. It's a sign AI assistants are moving off the browser tab and onto the desktop itself — useful if you're running the office side of the business from a single PC between jobs.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 GERMANY · SCHAEFFLER PUTS HEXAGON'S AEON HUMANOID THROUGH A PURPOSE-BUILT 'HUMANOID GYM'",
    "{{ROBOT_1_HEADLINE}}": "Schaeffler and Hexagon Open a 'Humanoid Gym' to Train the AEON Robot Before It Hits the Factory Floor",
    "{{ROBOT_1_SUMMARY}}": "Hexagon Robotics and German manufacturer Schaeffler have placed the AEON humanoid robot inside a purpose-built 'Humanoid Gym' training facility, a controlled environment where it can practise and validate real factory tasks before going anywhere near a live production line — part of a plan to eventually deploy at least 1,000 of the robots across Schaeffler's global operations. It's a reminder that even well-funded industrial robot rollouts are choosing to prove reliability in a sandbox first, the same instinct any small operator would apply before trusting new gear with a paying job.",
    "{{ROBOT_1_URL}}": "https://www.electronicsforu.com/news/humanoid-robot-begins-training-for-industrial-factory-deployment",

    # Australia
    "{{AUS_1_HEADLINE}}": "High Court Shuts Down Giggle for Girls' Final Appeal in Landmark Tickle Gender-Discrimination Case",
    "{{AUS_1_SUMMARY}}": "The High Court has refused special leave to appeal, with costs, ending app founder Sall Grover's last avenue of appeal against Roxanne Tickle, who was awarded $10,000 in damages after being barred from the female-only Giggle app for not looking 'sufficiently female'. The case, Tickle v Giggle, was the first time an Australian court ruled on gender-identity discrimination.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-11/giggle-v-tickle-app-founder-denied-high-court-appeal/107142432",

    "{{AUS_2_HEADLINE}}": "Gold Coast ATO Worker Charged Over Alleged Leaks to Organised Crime Figures",
    "{{AUS_2_SUMMARY}}": "A 32-year-old Australian Taxation Office employee has been charged with unlawfully disclosing sensitive information to organised crime figures, after a joint National Anti-Corruption Commission, AFP and ATO probe codenamed Operation Esk-Jerboa. Suspended without pay, he's due to face court on the Gold Coast on 21 September.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "49ers Rout Rams 27–7 in Australia's First-Ever NFL Regular-Season Game at a Sold-Out MCG",
    "{{VIC_1_SUMMARY}}": "San Francisco beat Los Angeles 27–7 in front of a sold-out MCG crowd, with Brock Purdy throwing three touchdowns to headline the first regular-season NFL game ever played in Australia. A big win for Melbourne's event calendar, but expect the CBD and surrounding transport links to still be feeling the after-effects of the crowds into the weekend.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 PHYSICS · STUDY SUGGESTS TIME ITSELF MAY CARRY A TINY BUILT-IN UNCERTAINTY",
    "{{SCI_1_HEADLINE}}": "Physicists Suggest Time Itself May Have a Tiny Fundamental Uncertainty, Setting an Ultimate Limit on Clock Precision",
    "{{SCI_1_SUMMARY}}": "A study examining 'quantum collapse' theories — alternatives to standard quantum mechanics — finds that time itself may carry a tiny intrinsic uncertainty, placing an ultimate limit on how precisely any clock, however advanced, could ever measure it. The effect is many orders of magnitude below anything current atomic clocks can detect, so it won't affect your watch or GPS, but researchers say it may reveal a hidden link between quantum mechanics, gravity and the structure of spacetime itself.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Your Documents Just Got Easier to Find — Turn ChatGPT's New Dropbox and SharePoint Search Into an Instant Job Paper Trail",
    "{{INSIGHT_BODY}}": "With ChatGPT's Library now able to search Dropbox, Box and SharePoint directly instead of just Google Drive, a business that's been scattering quotes, invoices, safety certificates and job photos across two or three different cloud folders can finally point one AI tool at all of it at once. Ask it to pull together every document tied to a client or job number, draft a variation notice from last month's quote and this month's material invoices, or flag which safety certificates are close to expiring — all without re-uploading a single file. It's not a new system to learn, just a five-minute setup that turns folders you already have into a searchable paper trail for the next time a client, insurer or the ATO comes asking.",

    # Fun facts
    "{{FACT_1}}": "The Phillips-head screw was designed in the 1930s by American businessman Henry F. Phillips specifically so a power driver would 'cam out' — slip out of the screw head — the moment it hit the right torque, preventing overtightening on the Cadillac production line that first adopted it in 1936.",
    "{{FACT_2}}": "A 'second' is officially defined by counting exactly 9,192,631,770 oscillations of a caesium-133 atom, and the best caesium fountain clocks are accurate enough to drift by less than one second over roughly 300 million years — the kind of precision the physicists behind today's 'tiny glitch in time' study are trying to probe even further.",
    "{{FACT_3}}": "The chocolate chip cookie was an accident: in 1938, Ruth Wakefield of the Toll House Inn in Massachusetts ran out of baker's chocolate and chopped up a block of Nestlé semi-sweet instead, expecting it to melt smoothly into the dough — it held its shape, and Nestlé later paid her with a lifetime supply of chocolate for the rights to print her recipe on the packet.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the bouncy castle hire operator never worry about a quiet winter?",
    "{{JOKE_PUNCHLINE}}": "Because he'd already bounced back from worse.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"I would rather have questions that can't be answered than answers that can't be questioned.\"",
    "{{CLOSING_ATTR}}": "— Richard Feynman",
    "{{CLOSING_MESSAGE}}": "It's a quieter Saturday after a huge week for Melbourne — the 49ers' 27–7 win over the Rams gave the MCG its first taste of NFL football, so expect a bit of residual traffic around the city today. Weather-wise, today and tomorrow carry a shower risk around Carrum Downs before it clears into a mostly sunny Tuesday, so it's worth planning outdoor jobs around the midweek window rather than the weekend. And with oil back above US$100 a barrel after the Saudi pipeline attacks and RBA hike odds now at 80%, it's shaping up as a week to get quotes out early rather than wait and wear the cost creep yourself.",
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
