#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 19 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 19 Aug (BOM)
    "{{WEATHER_1}}": "WED 19 · ⚠️ Vigorous cold front crossing the state — very high chance of showers with damaging northerly winds possible before dawn, easing later · 7–14°C",
    "{{WEATHER_2}}": "THU 20 · 🌦️ Partly cloudy, medium chance of showers, winds easing to the northwest · 8–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 21 · ☁️ Cloudy with a medium chance of showers, winds turning light · 8–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 22 · 🌥️ Shower chances easing, winds turning lighter · 8–16°C",
    "{{WEATHER_5}}": "SUN 23 · 🌤️ Rain chances continuing to ease, a brighter finish to the week · 8–17°C",
    "{{WEATHER_ALERT}}": "Damaging wind warning current for Port Phillip and parts of Melbourne metro this morning as the front comes through — worth securing loose gear, signage and scaffolding on site before conditions ease this afternoon",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦🇷🇺 UKRAINE · KYIV LAUNCHES 620-DRONE BARRAGE AT MOSCOW REGION, ONE OF WAR'S LARGEST STRIKES",
    "{{WORLD_1_HEADLINE}}": "Ukraine Launches Its Largest Drone Barrage in Years, Sending Over 620 Drones at the Moscow Region",
    "{{WORLD_1_SUMMARY}}": "Moscow's mayor says more than 620 drones were launched at the city and surrounding region overnight, with Russian air defences downing around 180 of them; a Wildberries warehouse was hit and three people were wounded, including a 10-year-old girl, while Crimea reported widespread power outages from a related barrage. It's one of the largest aerial attacks of the war so far — another sign there's no ceasefire in sight, and that the shipping, energy and grain disruptions rippling out from it keep landing on costs everywhere else, Australia included.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/8/18/russia-says-more-than-600-drones-targeted-moscow-region",

    "{{WORLD_2_FLAG}}": "🇦🇪🇮🇷 GULF · UAE SAYS IT DOWNED TWO BALLISTIC MISSILES FIRED FROM IRAN",
    "{{WORLD_2_HEADLINE}}": "UAE Says It Intercepted Two Ballistic Missiles Launched From Iran as Hormuz Tensions Escalate Again",
    "{{WORLD_2_SUMMARY}}": "The UAE says its air defences detected and downed two ballistic missiles fired from Iran, one falling outside its territorial waters and the other within them, as talks over reopening the Strait of Hormuz remain stalled. Qatar says mediators are waiting on a bilateral deal between Iran and Oman before broader talks resume — a reminder the strait crisis rattling global oil and shipping costs still has no resolution in sight, months in.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/liveblog/2026/8/18/iran-war-live-trump-rejects-mou-extension-as-us-claims-control-of-hormuz",

    # Economics
    "{{ECON_1_FLAG}}": "⛽🇦🇺 FUEL · PUMP PRICES STAY ELEVATED AS ACCC KEEPS WEEKLY WATCH ON THE MARKET",
    "{{ECON_1_HEADLINE}}": "Petrol Still Sitting Well Above $2 a Litre as the ACCC Keeps Weekly Watch on Fuel Prices",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly monitoring shows capital city pump prices remaining elevated since the fuel excise concession fully ended in early August, with Victoria still the cheapest state at an average around 204.6c/L for unleaded but well up on where prices sat before the excise cut expired. For a business running a ute and a trailer every day, it's worth shopping around and checking the ACCC's weekly figures rather than assuming last month's fuel budget still holds.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🏗️🇦🇺 LABOUR HIRE · VICTORIA THREATENS TO PULL LICENCES OVER SUBSTANDARD WORKER HOUSING",
    "{{ECON_2_HEADLINE}}": "Victorian Labour Hire Firms Risk Losing Their Licence Over Substandard Migrant Worker Housing",
    "{{ECON_2_SUMMARY}}": "Victoria's Labour Hire Authority has tightened accommodation standards for labour hire providers, with non-compliant operators risking licence loss and fines above $160,000 after cases of migrant workers found housed in mould-affected, overcrowded properties. Any trades business that leans on labour hire to fill gaps on site is worth double-checking its provider's licence and living arrangements are actually up to standard — the fallout can land on the host business too, not just the labour hire firm.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖⚠️ CYBERSECURITY · BUSINESSES WARNED TO BRACE FOR A WAVE OF AI-POWERED CYBERATTACKS",
    "{{TECH_1_HEADLINE}}": "Businesses Told to Brace for AI-Powered Cyberattacks as Agentic Tools Get Better at Finding Vulnerabilities",
    "{{TECH_1_SUMMARY}}": "Security researchers are warning businesses of all sizes to prepare for a rise in AI-powered cyberattacks, as agentic AI tools become increasingly capable of automatically discovering and exploiting software weaknesses faster than defenders can patch them. For a small trades operation running invoicing, scheduling and email through cloud tools, it's a nudge to make sure multi-factor authentication is actually switched on everywhere, not just on the accounts that feel important.",
    "{{TECH_1_URL}}": "https://techstartups.com/2026/08/18/top-tech-news-today-august-18-2026-apple-baidu-bytedance-google-meta-openai-xiaomi-more/",

    "{{TECH_2_FLAG}}": "🤖👦 AI SAFETY · OPENAI LAUNCHES A DEDICATED, MORE RESTRICTED CHATGPT FOR TEENS",
    "{{TECH_2_HEADLINE}}": "OpenAI Rolls Out a Teen-Specific Version of ChatGPT With Tighter Safety Guardrails",
    "{{TECH_2_SUMMARY}}": "OpenAI has launched a dedicated ChatGPT experience for 13-to-17-year-olds that blocks conversations around self-harm and romantic or sexual content, using age-prediction technology to automatically route younger users into the restricted mode. Worth knowing if there are teenagers in the house using the same tools you use for the business — the protections aren't automatic unless the account is actually set up as a teen one.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖🏭 ROBOTICS · MARK CUBAN-BACKED FORT ROBOTICS TO LIST ON NASDAQ VIA SPAC",
    "{{ROBOT_1_HEADLINE}}": "Mark Cuban-Backed Fort Robotics to Go Public, Betting Big on Making Physical AI Safe",
    "{{ROBOT_1_SUMMARY}}": "Fort Robotics, which builds safety and control systems for autonomous machines and industrial robots, has agreed to go public via a SPAC merger valuing the combined company at about $556 million, with Google DeepMind among its 600-plus customers. The company reports 62% revenue growth last year and more than 19,500 safety-critical units deployed — a sign that as robots and automation spread onto more worksites, the business of keeping them from hurting the humans nearby is becoming serious in its own right.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/08/18/fort-robotics-to-go-public-via-business-combination-with-newbury-street-ii-acquisition-corp-to-advance-the-safety-of-physical-ai/26962/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Economist Gordon de Brouwer Takes Up the Role of ANU's 14th Chancellor Today",
    "{{AUS_1_SUMMARY}}": "Dr Gordon de Brouwer — an economist, former Australian Public Service Commissioner and ANU alumnus — officially becomes the university's 14th chancellor today, taking over from Julie Bishop, who resigned in May. He's being described as a steady, process-focused pick after a turbulent stretch for the university's governance.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-17/anu-appoints-new-chancellor-to-replace-julie-bishop/107045364",

    "{{AUS_2_HEADLINE}}": "New Global Study Finds Older Australians Face Serious Heat Risk at Much Lower Temperatures Than Thought",
    "{{AUS_2_SUMMARY}}": "A new global study has found that people over 60 can lose the ability to regulate their core body temperature at levels roughly 4.7 to 7.5 degrees lower than younger adults, more than doubling earlier estimates of how many older people are exposed to dangerous heat each year. Researchers are calling for age-specific heat warnings — worth knowing if you've got an older tradesperson, parent or client planning to be out and about once the warmer months roll back around.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Police Fear Fadi Haddara Shooting Could Spark Wider Underworld Violence in Melbourne",
    "{{VIC_1_SUMMARY}}": "Law enforcement and underworld sources fear the Sunday night ambush shooting of alleged crime family patriarch Fadi Haddara, who remains in a critical but stable condition, could trigger a fresh wave of violence tied to long-running tensions over Melbourne's illicit tobacco trade. Police say they're doing everything they can to stop it escalating further — a reminder the city's gang tensions haven't gone anywhere, even on an otherwise ordinary Wednesday.",

    # Science
    "{{SCI_1_FLAG}}": "🐋🔬 MARINE SCIENCE · FIRST-EVER PYGMY BLUE WHALE SIGHTING IN THE GULF OF CARPENTARIA ENDS IN STRANDING",
    "{{SCI_1_HEADLINE}}": "A Pygmy Blue Whale Has Died After Beaching in the Gulf of Carpentaria — the First Time the Species Has Ever Been Recorded There",
    "{{SCI_1_SUMMARY}}": "A 20-metre pygmy blue whale stranded and died off Groote Eylandt in the Northern Territory, in what researchers believe is the first confirmed sighting of the species in the Gulf of Carpentaria. Traditional owners spotted the whale about 500 metres offshore on Friday; with the carcass too large to move and already being fed on by tiger sharks, Anindilyakwa Land and Sea Rangers and Charles Darwin University researchers are instead gathering samples to try to understand why it turned up so far from its known range.",

    # Business insight
    "{{INSIGHT_TITLE}}": "An AI Store Manager Just Fired Its First Human Employee — Here's the Rule to Set Before You Hand Over Any Real Decision",
    "{{INSIGHT_BODY}}": "A US retail experiment called Andon Market handed its AI 'manager', Luna, a budget, a corporate card and real hiring and firing authority — and this month Luna recommended dismissing a staff member after they missed 17 of 23 rostered shifts, a decision the humans running the company then reviewed and carried out. It's the first documented case of an AI making a real termination call, and it worked here largely because a person still checked the reasoning and signed off before anything happened. For a trades business starting to lean on AI for rostering, quoting or chasing overdue invoices, that's the model worth copying: let the AI do the recommending and the paperwork, but keep a human as the last checkpoint before anything with real consequences — a job offer, a firing, a big quote — actually goes out the door.",

    # Fun facts
    "{{FACT_1}}": "August 19 is National Aviation Day in the United States, chosen in 1939 to mark the birthday of Wright brother Orville Wright — the same Orville who, alongside brother Wilbur, ran a small bicycle repair shop in Dayton, Ohio before building the first powered aircraft.",
    "{{FACT_2}}": "Corrugated iron, patented by English engineer Henry Robinson Palmer in 1829, became one of colonial Australia's most-used building materials simply because it was light enough to ship flat-packed by the thousands and could be put up by almost anyone without a tradesman's skill.",
    "{{FACT_3}}": "Melbourne's reputation for 'four seasons in one day' traces back to a line Mark Twain used after visiting in 1895, joking the city could serve up every kind of weather within a few hours — a description that still holds up on a day like today, with damaging wind, rain and clearer skies all forecast inside the same 24 hours.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the shade sail installer become the most in-demand tradie every summer?",
    "{{JOKE_PUNCHLINE}}": "Because no matter how hot it got, he always had everyone covered.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The best preparation for tomorrow is doing your best today.\"",
    "{{CLOSING_ATTR}}": "— H. Jackson Brown Jr.",
    "{{CLOSING_MESSAGE}}": "It's a genuinely Melbourne kind of Wednesday in Carrum Downs — a vigorous cold front bringing damaging winds and a very high chance of showers this morning, easing into a calmer afternoon, so it's worth locking down loose gear and site signage early rather than late. Between Gordon de Brouwer taking the reins at ANU today, a pygmy blue whale turning up somewhere it's never been recorded before, and an AI store manager overseas making its first real call to let someone go, it's a fair reminder that the biggest changes — in the weather or in the tools we're using — often show up quietly before anyone's ready for them.",
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
