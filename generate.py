#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 06 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 6 Jul (BOM)
    "{{WEATHER_1}}": "MON 6 · 🌫️ Frosty start, sunny arvo · 4–15°C",
    "{{WEATHER_2}}": "TUE 7 · 🌫️ Frosty start, partly cloudy · 4–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "WED 8 · ⛅ Partly cloudy · 4–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "THU 9 · ⛅ Partly cloudy · 4–13°C",
    "{{WEATHER_5}}": "FRI 10 · ⛅ Partly cloudy · 4–15°C",
    "{{WEATHER_ALERT}}": "⚠ MODERATE FROST WARNING MON–TUE MORNINGS · ALLOW EXTRA WARM-UP TIME FOR GEAR & VEHICLES",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 IRAN · STATE FUNERAL · FINAL DAY OF MOURNING FOR KHAMENEI",
    "{{WORLD_1_HEADLINE}}": "Iran's State Funeral for Slain Supreme Leader Khamenei Reaches Its Final Day With a 10km Tehran Procession",
    "{{WORLD_1_SUMMARY}}": "Iran's multi-day state funeral for Supreme Leader Ayatollah Ali Khamenei, killed in February's US-Israeli strikes, culminates today with a procession covering 10 kilometres from Imam Hossein Square to Azadi Square. Authorities say 1.3 million people made over 3 million metro trips overnight as the second day of events unfolded, with officials expecting 15 to 20 million mourners in total — making it the largest state funeral in Iran's history. Khamenei's sons Mostafa, Meysam and Masoud have appeared at the ceremonies, but his named successor, Mojtaba, has been notably absent throughout.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/7/5/sons-of-irans-leader-ali-khamenei-attend-funeral-but-mojtaba-is-absent",

    "{{WORLD_2_FLAG}}": "🇻🇪 VENEZUELA · EARTHQUAKE RECOVERY · DEATH TOLL TOPS 2,950",
    "{{WORLD_2_HEADLINE}}": "Venezuela's Earthquake Death Toll Passes 2,950 as Displaced Families Block Roads Demanding Housing",
    "{{WORLD_2_SUMMARY}}": "Officials now report 2,954 deaths and over 16,500 injuries from the magnitude 7.5 and 7.2 earthquakes that struck Venezuela on June 24, with recovery work shifting from search-and-rescue to debris removal. An estimated 15,000 people remain homeless, and residents in hard-hit Caraballeda blocked a main road over the weekend demanding the government deliver on promised temporary housing. More than 3,300 international rescuers are still assisting alongside local teams, with nearly 900 aftershocks recorded since the initial quakes.",
    "{{WORLD_2_URL}}": "https://www.wmnf.org/venezuela-earthquake-live-updates-july-5-2026/",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL PRICES · EXCISE STEP-UP · PUMP PRICES CLIMBING THIS WEEK",
    "{{ECON_1_HEADLINE}}": "Petrol and Diesel Prices Start Climbing This Week as the Fuel Excise Discount Halves to 16 Cents a Litre",
    "{{ECON_1_SUMMARY}}": "The fuel excise discount dropped from 32 cents to 16 cents a litre on July 1, and the ACCC's weekly monitoring shows retail petrol and diesel prices beginning to move higher in response — up to 16 cents a litre over the past week in some capital cities. Prices are still well down on the March peak (regular unleaded around 152.3 cents a litre, diesel 176.6 cents in Sydney), but if you set a fuel budget line based on last month's bowser price, it's worth checking again this week rather than assuming it still holds.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🛣️ NSW TOLLS · WEEKLY CAP CUT · UP TO $520 BACK FOR HEAVY USERS",
    "{{ECON_2_HEADLINE}}": "NSW Cuts Its Weekly Toll Cap From $60 to $50, Starting Today",
    "{{ECON_2_SUMMARY}}": "A temporary reduction in the weekly toll cap from $60 to $50 takes effect today across NSW for the next 12 months, expected to deliver up to $520 in extra relief per heavy toll user and around $227.4 million back to motorists over 2026–27. For any trades business running vans across toll roads for supply runs or metro jobs, it's a real, automatic saving worth checking has actually landed on your account.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 TESLA · AI COST CONTROLS · $200/WEEK STAFF CAP FROM TODAY",
    "{{TECH_1_HEADLINE}}": "Tesla Caps Staff AI Spending at $200 a Week as Employee Token Bills Balloon",
    "{{TECH_1_SUMMARY}}": "From today, Tesla is limiting how much its employees can spend on AI tools to $200 a week, with anything above that requiring manager sign-off — after some software engineers were burning through thousands of dollars in tokens weekly, with internal dashboards even ranking staff by usage. Notably, the cap excludes Musk's own xAI/Grok tools. Uber, Meta, Amazon and Walmart have all introduced similar limits recently. A useful sign for any small business quietly racking up AI subscriptions: even the biggest users are now treating this as a real, trackable cost line, not a free perk.",
    "{{TECH_1_URL}}": "https://electrek.co/2026/07/02/tesla-caps-employee-ai-spending-200-week/",

    "{{TECH_2_FLAG}}": "🌐 UNITED NATIONS · AI GOVERNANCE · GENEVA DIALOGUE OPENS TODAY",
    "{{TECH_2_HEADLINE}}": "UN's First Global Dialogue on AI Governance Opens in Geneva Today",
    "{{TECH_2_SUMMARY}}": "The inaugural UN Global Dialogue on AI Governance begins today in Geneva, running alongside this week's ITU AI for Good Global Summit, as member states begin thrashing out international rules for how AI systems should be built, deployed and held accountable. It's early-stage diplomacy rather than binding law, but a reminder that the AI tools already sitting in most businesses' workflows are heading toward a genuine global rulebook, not just a provider's terms of service.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · PUDU ROBOTICS · WORLD-FIRST ROBOT-RUN HOTEL PLANNED",
    "{{ROBOT_1_HEADLINE}}": "Pudu Robotics Unveils Plans for the World's First Fully Robot-Run Hotel",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics maker Pudu Robotics has detailed plans for a 44-room hotel on Shenzhen's West Artificial Island where robots handle reception, room service, luggage delivery, cleaning and food preparation, coordinated through its PuduFM 1.0 embodied-intelligence platform. Public trials begin late 2026, with a full opening slated for 2027. It's a step beyond the single-task cleaning or delivery robots already common in hospitality — a real test of whether multiple robots can run an entire service business end to end.",
    "{{ROBOT_1_URL}}": "https://www.foxnews.com/tech/chinas-robot-run-hotel-opens-public-2027",

    # Australia
    "{{AUS_1_HEADLINE}}": "NSW Becomes Third State to Confirm Deadly H5N1 Bird Flu Strain in Wild Birds",
    "{{AUS_1_SUMMARY}}": "CSIRO's Australian Centre for Disease Preparedness has confirmed high-pathogenicity H5N1 bird flu in a giant petrel found near Hawks Nest, making NSW the third state to record the strain in wild birds. There's no evidence yet of spread to commercial poultry, but free-range farmers have been urged to temporarily keep hens under cover while authorities ramp up surveillance with ground searches, drones and boat patrols.",
    "{{AUS_1_URL}}": "https://www.thenewdaily.com.au/news/state/nsw/2026/07/05/bird-flu-nsw",

    "{{AUS_2_HEADLINE}}": "Albanese Signs Vuvale Union Agreement With Fiji on Three-Nation Pacific Tour",
    "{{AUS_2_SUMMARY}}": "Prime Minister Albanese landed in Suva to sign the Vuvale Union agreement with Fijian PM Sitiveni Rabuka today, deepening the two nations' partnership, before travelling on to the Solomon Islands, where he'll become the first foreign leader to join the country's Independence Day celebrations — part of a broader push to cement Australia's standing across the Pacific.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Bureau of Meteorology Issues Moderate Frost Warning Across Regional Victoria",
    "{{VIC_1_SUMMARY}}": "A moderate frost warning is current for Northern Country, North Central, North East, South West, Central, West and South Gippsland forecast districts, with areas of frost and morning fog set to continue into the start of the week before clearer, sunnier afternoons return — worth factoring into any early job starts this week.",

    # Science
    "{{SCI_1_FLAG}}": "🔭 ASTRONOMY · NASA / HUBBLE · STELLAR NURSERY IMAGED",
    "{{SCI_1_HEADLINE}}": "Hubble Captures a Sparkling Nursery of 2,500 Baby Stars Still Being Born",
    "{{SCI_1_SUMMARY}}": "NASA's Hubble Space Telescope has released a striking new image of LH 95, a star-forming region in the Large Magellanic Cloud where roughly 2,500 young stars are still pulling in gas and dust on their way to becoming full stars — including one still-forming giant packing 60 to 70 times the Sun's mass that appears to be a million years younger than its neighbours. A reminder that star formation is a far longer, messier process than the tidy diagrams suggest.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Toolbox Talk Shouldn't Just Be a Signature on a Page — AI Can Turn It Into Real Evidence",
    "{{INSIGHT_BODY}}": "Most small trades businesses run some form of toolbox talk or pre-start safety chat before a job, but the record of it usually stops at a signed sheet shoved in a folder — no detail on what was actually discussed, no easy way to prove what was covered if WorkSafe or an insurer ever comes asking. A simple fix: record the toolbox talk on your phone, run the audio through an AI transcription tool, and ask it to pull out the hazards discussed, the actions agreed and who was present, filed straight against the job number. It turns five minutes of talking into a genuine, timestamped audit trail — the kind of paperwork that actually protects you, instead of just ticking a box.",

    # Fun Facts
    "{{FACT_1}}": "Food safety's 'danger zone' sits between 5°C and 60°C — bacteria in food held in that range can double in number roughly every 20 minutes, which is the entire reason behind the commercial '4-hour/2-hour rule' for anything left out at room temperature.",

    "{{FACT_2}}": "The world's first known video game tournament was held at Stanford University in 1972 for the game Spacewar — the grand prize for the winner was a year's subscription to Rolling Stone magazine.",

    "{{FACT_3}}": "The term 'artificial intelligence' was coined in 1956 at a summer research workshop at Dartmouth College, where a small group of scientists confidently predicted the core problems of AI could be solved within a single generation.",

    # Joke
    "{{JOKE_SETUP}}": "Why do panel beaters make the calmest small business owners on the block?",
    "{{JOKE_PUNCHLINE}}": "Because they've spent their whole career proving that even the biggest mess can be hammered back into shape.",

    # Closing
    "{{CLOSING_QUOTE}}": "“A year from now you may wish you had started today.”",
    "{{CLOSING_ATTR}}": "— Karen Lamb",
    "{{CLOSING_MESSAGE}}": "It's a properly frosty start across Melbourne and regional Victoria this morning, so budget extra warm-up time for compressors and vehicles before the first job — clearer skies are forecast by the afternoon. Further afield, the PM's signed a fresh Pacific agreement in Fiji and Tehran is holding the final day of its state mourning, reminders the world keeps turning well beyond the ute. Frosty Monday or not, it's a fresh week — make the first few hours count.",
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
