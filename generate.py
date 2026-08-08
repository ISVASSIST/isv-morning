#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 09 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 09 Aug (BOM)
    "{{WEATHER_1}}": "SUN 09 · 🌧️ Very high chance of rain, windy N–NE 30–45km/h · 7–17°C",
    "{{WEATHER_2}}": "MON 10 · 🌬️ Very high chance of rain, windy turning westerly · 8–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 11 · 🌦️ High chance of showers, most likely afternoon/evening · 8–12°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 12 · 🌧️ Very high chance of showers, windy · 8–10°C",
    "{{WEATHER_5}}": "THU 13 · ⛅ Partly cloudy, medium chance of showers · 7–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings current for Melbourne / Carrum Downs, but a genuinely wet, windy stretch runs from today right through to Wednesday",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 UKRAINE · RUSSIAN STRIKES KILL AT LEAST FOUR IN KYIV REGION, INCLUDING A THREE-YEAR-OLD",
    "{{WORLD_1_HEADLINE}}": "Russian Drone and Missile Strikes Kill at Least Four in the Kyiv Region as Air Defences Fall Short",
    "{{WORLD_1_SUMMARY}}": "Overnight strikes on Kyiv and the neighbouring Brovary district killed two grandparents and their three-year-old grandson, with at least one more death in the city itself after a barrage of six ballistic missiles hit civilian infrastructure. Ukraine's air force said it downed 135 of 151 drones launched overnight, but Kyiv's depleted air defences are increasingly struggling to keep pace with nightly Russian barrages more than four years into the war.",
    "{{WORLD_1_URL}}": "https://abcnews.com/International/wireStory/russian-attacks-kill-4-kyiv-surrounding-region-air-135478347",

    "{{WORLD_2_FLAG}}": "🇮🇶 IRAQ · MORE THAN 20 MILLION PILGRIMS GATHER IN KARBALA FOR ARBAEEN AMID REGIONAL TENSIONS",
    "{{WORLD_2_HEADLINE}}": "More Than 20 Million Shia Pilgrims Gather in Karbala for the World's Largest Annual Pilgrimage",
    "{{WORLD_2_SUMMARY}}": "Pilgrims marking the 7th-century killing of the Prophet Muhammad's grandson Husayn ibn Ali walked to Karbala for Arbaeen this week, one of the largest human gatherings on Earth, with organisers estimating more than three million came from Iran alone. This year's pilgrimage carried extra weight given the ongoing US-Israel-Iran tensions, with many Iranian pilgrims saying their numbers were swelled by mourning for their own recently killed religious leader.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/08/06/nx-s1-5922415/shia-pilgrimage-to-karbala-includes-millions-of-iranians",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺🏦 RATES · ALL FOUR MAJOR BANKS NOW EXPECT THE RBA TO HOLD AT 4.35% ON TUESDAY",
    "{{ECON_1_HEADLINE}}": "Westpac Drops Its Rate-Hike Call, Bringing All Four Major Banks Into Line for Tuesday's RBA Hold",
    "{{ECON_1_SUMMARY}}": "Westpac has abandoned its lone forecast of an August rate rise after softer-than-expected June quarter inflation, meaning CBA, NAB, ANZ and Westpac are now all tipping the RBA to hold at 4.35% when it hands down its decision at 2:30pm Tuesday. It's a reminder that the cash rate outlook can still shift fast — worth holding off on locking in equipment finance or a big loan until Governor Michele Bullock's press conference makes the tone of the call clear.",
    "{{ECON_1_URL}}": "https://www.finder.com.au/news/finders-rba-survey-7-august-2026",

    "{{ECON_2_FLAG}}": "🇦🇺🏗️ CONSTRUCTION · VICTORIAN BUILDING APPROVALS FELL 13.9% IN JUNE WHILE QUEENSLAND AND NSW ROSE",
    "{{ECON_2_HEADLINE}}": "Victorian Building Approvals Slid 13.9% in June Even as Queensland and NSW Approvals Jumped",
    "{{ECON_2_SUMMARY}}": "The ABS's latest figures, released this week, show private dwelling approvals climbing in Queensland (+33.4%), NSW (+13.2%) and WA (+10.7%) in June, while Victoria fell 13.9% and Tasmania and South Australia also dropped. For anyone quoting on residential work locally, it's a sign the pipeline may be thinner here than in the states getting the headlines — worth factoring into how far ahead you're booking jobs.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · OPENAI DROPS TEXT CHAT LIMITS FOR FREE CHATGPT USERS, ROLLS OUT SMARTER DEFAULT MODEL",
    "{{TECH_1_HEADLINE}}": "OpenAI Scraps Text Chat Limits for Free ChatGPT Users as GPT-5.6 Luna Becomes the New Default",
    "{{TECH_1_SUMMARY}}": "From the week of 10 August, free ChatGPT users get unlimited text chats plus a new 'Think' button for tougher questions, as GPT-5.6 Luna replaces the older GPT-5.5 Instant as the default free model. It's a meaningful upgrade for any small business using the free tier for quotes, emails or job notes — file uploads and images still have limits, but the core chat function is no longer capped.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/08/06/openai-brings-unlimited-chatgpt-text-chats-to-free-users/",

    "{{TECH_2_FLAG}}": "🤖 AI LEADERSHIP · GOOGLE DEEPMIND'S DEMIS HASSABIS STEPS DOWN AS CEO IN MAJOR RESHUFFLE",
    "{{TECH_2_HEADLINE}}": "Google DeepMind Co-Founder Demis Hassabis Steps Down as CEO in a Major AI Leadership Shake-Up",
    "{{TECH_2_SUMMARY}}": "Hassabis is moving into a new role as Chair of Google DeepMind and Chief Scientist of Alphabet, with long-time CTO Koray Kavukcuoglu stepping up to run day-to-day Gemini model development and frontier research. It's the second big AI leadership exit in a week after Jeff Dean's departure to launch his own startup — a sign of just how fluid the race for AI talent has become at the very top of the industry.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇦🇺🤖 AUTOMATION · AUSTRALIAN WAREHOUSES TARGET DENSER STORAGE WITH NEW ROBOTIC RACKING SYSTEM",
    "{{ROBOT_1_HEADLINE}}": "CH Racking Targets Denser Australian Warehouses With a New Robotic Storage System",
    "{{ROBOT_1_SUMMARY}}": "CH Racking's ACR/CTU system pairs robotic goods-to-person retrieval with high-density racking, sending robots to fetch cartons, bins and totes so staff aren't walking aisles to pick stock. General manager Jessica Zhu says it's aimed at operators under pressure to move more inventory without the labour or the floor space to build a bigger shed — a squeeze plenty of small Victorian operators would recognise.",
    "{{ROBOT_1_URL}}": "https://mhdsupplychain.com.au/2026/08/06/ch-racking-targets-warehouse-density-with-robotic-storage-system",

    # Australia
    "{{AUS_1_HEADLINE}}": "Vietnam's President Lands in Australia for a Landmark First State Visit",
    "{{AUS_1_SUMMARY}}": "General Secretary and President To Lam arrives today for a visit running through 12 August, meeting Prime Minister Albanese in Canberra on Tuesday to deepen the two countries' Comprehensive Strategic Partnership across trade, defence, energy and digital cooperation — his first visit to Australia since taking office.",
    "{{AUS_1_URL}}": "https://www.pm.gov.au/media/visit-australia-general-secretary-and-president-socialist-republic-vietnam",

    "{{AUS_2_HEADLINE}}": "Wallabies Survive Late Japan Fightback to Win 35-32 in Les Kiss's First Test in Charge",
    "{{AUS_2_SUMMARY}}": "Australia held on despite playing most of the second half a player down after a red card, with new coach Les Kiss opening his tenure with a win in Osaka — a promising start to the post-Joe Schmidt era ahead of the Wallabies' spring tour.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "AFLW Season Kicks Off Tonight at Marvel Stadium in a First-Ever AFL/AFLW Double-Header",
    "{{VIC_1_SUMMARY}}": "St Kilda hosts Carlton in the 2026 AFLW season opener at 4:35pm, followed by the same two clubs' AFL sides in the sixth annual Spud's Game at 7:20pm — the first time the men's and women's competitions have shared a marquee fixture, raising funds for mental health research in honour of former Saint Danny 'Spud' Frawley.",

    # Science
    "{{SCI_1_FLAG}}": "☀️ ASTRONOMY · RECORD-SHARP TELESCOPE IMAGES REVEAL NEVER-BEFORE-SEEN WHIRLPOOLS ON THE SUN'S SURFACE",
    "{{SCI_1_HEADLINE}}": "The Sharpest-Ever Images of the Sun Reveal Tiny Whirlpools Scientists Never Knew Were There",
    "{{SCI_1_SUMMARY}}": "Using Hawaii's four-metre Inouye Solar Telescope, an international team captured plasma vortices as small as 20 kilometres across swirling on the Sun's surface — the first confirmed sighting of a long-predicted effect called Kelvin-Helmholtz instability outside a lab. The whirlpools may help explain how energy builds up and releases in small solar flares, and how magnetic fields spread through the Sun's atmosphere faster than current models can account for.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Vietnam's President Just Landed in Canberra — Could AI Help You Find a Cheaper Supplier Before Your Next Big Quote?",
    "{{INSIGHT_BODY}}": "With Vietnam's President beginning a state visit today aimed at deepening trade ties across manufacturing and industry, it's a timely nudge to look at where your own materials and consumables are actually coming from. AI-powered sourcing tools can now scan supplier catalogues, compare landed costs including freight and duty, and surface alternative Asia-Pacific suppliers in minutes rather than the hours it used to take ringing around — useful when a single line item on a job costing can move your margin more than the labour does. It won't replace the supplier relationships you've built over years, but running a quick AI comparison before your next big materials order costs nothing and might turn up a saving worth having.",

    # Fun facts
    "{{FACT_1}}": "Penicillin might have stayed a forgotten lab curiosity if not for Australian pathologist Howard Florey — Alexander Fleming discovered it in 1928, but it was Florey's Oxford team who worked out how to purify and mass-produce it in time to treat wounded soldiers in World War II, a breakthrough credited with saving well over 100 million lives since.",
    "{{FACT_2}}": "Speedo started life in 1914 as MacRae Knitting Mills, a Sydney hosiery and underwear manufacturer — the brand name was reportedly the winning entry in a 1928 staff slogan competition, 'Speed on in your Speedos,' decades before it became the world's dominant competitive swimwear label.",
    "{{FACT_3}}": "Melbourne surgeon Graeme Clark performed the world's first successful multi-channel cochlear implant in 1978, restoring hearing by sending electrical signals straight to the auditory nerve — he reportedly worked out how the device's electrode array needed to curl by experimenting with drinking straws and grass stems from his garden.",

    # Joke
    "{{JOKE_SETUP}}": "A septic tank contractor was asked how he always kept his small business running so smoothly.",
    "{{JOKE_PUNCHLINE}}": "He said the secret was simple — never let anything back up, in the pipes or the paperwork.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Fortune favours the bold.\"",
    "{{CLOSING_ATTR}}": "— Virgil",
    "{{CLOSING_MESSAGE}}": "It's a wet, windy Sunday in Carrum Downs, with rain and gusty north-to-northeasterly winds building right through to Wednesday — worth locking in any outdoor jobs early in the week while there's a gap. Vietnam's President touches down in Australia today for a first-ever state visit, and Tuesday brings the RBA's rate call, so it's a week worth keeping half an eye on the news alongside the tools.",
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
