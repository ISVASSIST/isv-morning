#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 05 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 5 Sep (BOM)
    "{{WEATHER_1}}": "SAT 5 SEP · ⛈️ Cloudy, very high chance of showers, chance of a thunderstorm (possibly severe) morning/afternoon · 9–17°C",
    "{{WEATHER_2}}": "SUN 6 SEP · 🌧️ Cloudy, high chance of showers about the ranges, medium chance elsewhere, gusty nor'easter · 10–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 7 SEP · 🌧️ Cloudy, very high chance of rain, most likely morning and afternoon, winds turning westerly · 10–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 8 SEP · 🌤️ Improving, decreasing chance of a shower, winds easing · 8–15°C",
    "{{WEATHER_5}}": "WED 9 SEP · ☀️ Clearing, just a slight chance of an early shower, light winds · 7–14°C",
    "{{WEATHER_ALERT}}": "No severe thunderstorm warning current as of this morning, but the Bureau is flagging a chance of a severe storm with damaging winds today. A wet, blustery run continues through the weekend into Monday before easing Tuesday.",

    # World
    "{{WORLD_1_FLAG}}": "🇳🇵 TRISHULI · TWO PULLED ALIVE FROM NEPAL TUNNEL, NINE DAYS ON",
    "{{WORLD_1_HEADLINE}}": "Search Teams Rescue Two Workers Alive From a Nepal Hydropower Tunnel, Nine Days After Deadly Floods",
    "{{WORLD_1_SUMMARY}}": "Rescuers pulled mechanical foreman Sanjay Shah and supervisor Kabir Maharjan alive from the flood-buried Trishuli 3A hydropower tunnel on Friday, more than a week after a glacier collapse triggered flash flooding that has now killed over 1,300 people across Nepal; hundreds are still believed trapped in other tunnels, and the rescue has lifted hopes more survivors can be found.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/9/4/nepal-search-teams-rescue-two-workers-from-hydropower-tunnel",

    "{{WORLD_2_FLAG}}": "🇷🇺 VLADIVOSTOK · PUTIN SEES A CHANCE FOR A UKRAINE DEAL",
    "{{WORLD_2_HEADLINE}}": "Putin Says a Ukraine Peace Deal Is Still Possible as Zelenskiy Reports US Negotiators Set to Visit Both Countries",
    "{{WORLD_2_SUMMARY}}": "Vladimir Putin told an economic forum in Russia's Far East that a peace agreement remains possible, though he said fresh Ukrainian strikes on shipping and a Kyiv warning to civilian aircraft over Russian airspace were making talks harder; Volodymyr Zelenskiy said US negotiators would soon travel to both Moscow and Kyiv, with no formal peace talks having taken place since February despite 4.5 years of war.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/world/ukraine/ukraine-new-dynamic-peace-efforts-vladimir-putin-chance-deal-rcna595914",

    # Economics
    "{{ECON_1_FLAG}}": "📈 RBA WATCH · THIRD MAJOR BANK NOW TIPS A RATE HIKE",
    "{{ECON_1_HEADLINE}}": "NAB, Deutsche Bank and Now UBS All Expect the RBA to Lift Rates on September 29",
    "{{ECON_1_SUMMARY}}": "A growing list of banks now expects the Reserve Bank to raise the cash rate from 4.35% to 4.6% at its 29 September meeting, after inflation data showed the trimmed mean measure holding at 3.6%; ANZ and CBA still expect the hike to land in November instead, while Westpac is the lone holdout tipping no move at all before year's end, leaving anyone about to lock in equipment or vehicle finance watching the next three weeks closely.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-04/asx-markets-business-news-live-updates/107113674",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE UNLEADED HOLDING JUST OVER 200C/L",
    "{{ECON_2_HEADLINE}}": "Melbourne Unleaded Averaging Around 203c/L as Diesel Sits Above 234c/L at the Cheapest Sites",
    "{{ECON_2_SUMMARY}}": "Melbourne bowsers are averaging roughly 202.8c/L for unleaded (cheapest E10 sites near 186.2c/L) and from about 234.5c/L for diesel at the cheapest outlets, with prices still elevated months on from the Middle East-driven spike — worth shopping around by suburb before a big fill, since the gap between the cheapest and priciest sites in Melbourne is still running well over 15c/L.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🧠 AI MILESTONE · OPENAI RELEASES GPT-6 ASTRA, DECLARES 'AGI ERA'",
    "{{TECH_1_HEADLINE}}": "OpenAI Releases GPT-6 Astra and Declares the Arrival of the 'AGI Era'",
    "{{TECH_1_SUMMARY}}": "OpenAI released its GPT-6 Astra model, with the company declaring it marks the arrival of an 'AGI era'; the model scored 63% on the ARC-AGI-3 reasoning benchmark, beat the human baseline on action efficiency, and used fewer moves than the median human across 96% of test levels — a big claim, and one worth watching rather than acting on, but a sign of how fast the tools underneath everyday AI apps are moving.",
    "{{TECH_1_URL}}": "https://techstartups.com/2026/09/04/top-tech-news-today-september-4-2026-amazon-google-microsoft-nvidia-openai-tesla-more/",

    "{{TECH_2_FLAG}}": "🎙️ PRACTICAL AI · MICROSOFT CUTS TRANSCRIPTION PRICE 72%",
    "{{TECH_2_HEADLINE}}": "Microsoft Releases Cheaper, Faster Speech-to-Text Model Covering 60 Languages",
    "{{TECH_2_SUMMARY}}": "Microsoft AI released MAI-Transcribe-2, a speech-recognition model it says beats rivals from OpenAI, Google and ElevenLabs on speed and accuracy, pricing it at 10 cents per audio hour through the end of 2026 — down about 72% from the $0.36 it charged five months ago — while adding speaker separation and word-level timestamps across 60 languages, making accurate voice-to-text a much cheaper add-on for anyone's note-taking or invoicing app.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🚕 ROBOTAXIS · FEDS PROBE TESLA'S DRIVERLESS CYBERCAB DAY ONE",
    "{{ROBOT_1_HEADLINE}}": "US Regulators Open a Federal Investigation Into Tesla's Steering-Wheel-Free Cybercab, a Day After Its Launch",
    "{{ROBOT_1_SUMMARY}}": "The US National Highway Traffic Safety Administration opened an Office of Defects Investigation into Tesla's Cybercab within a day of the driverless, steering-wheel-free robotaxi hitting the streets of Austin, examining the data behind Tesla's safety certification for a vehicle that has no steering wheel, mirrors or brake pedal; the probe covers roughly 1,000 vehicles already in service.",
    "{{ROBOT_1_URL}}": "https://techcrunch.com/2026/09/04/feds-launch-investigation-into-teslas-cybercab-deployment/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Deploys Specialist Drone Teams and a Further $3 Million to the Nepal Disaster Response",
    "{{AUS_1_SUMMARY}}": "The federal government is sending a 15-person Disaster Assistance Response Team, including drone specialists from Fire and Rescue NSW and the Queensland Fire Department, to help map and search flood-hit areas of Nepal, alongside a further $3 million to match public donations — taking Australia's humanitarian support past $11 million as 36 Australians remain unaccounted for.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-03/australia-deploys-drones-to-nepal-as-death-toll-passes-1200/107111120",

    "{{AUS_2_HEADLINE}}": "CFMEU Delegate Charged Over Alleged Drug Dealing at Melbourne Construction Sites",
    "{{AUS_2_SUMMARY}}": "Victoria Police allege a 35-year-old union delegate was part of a trio importing steroids and other drugs through the mail and selling them across Melbourne construction sites, after Taskforce Hawk raided properties at Mulgrave, Heathmont and Fitzroy on Thursday; the man faces trafficking and weapons charges alongside two co-accused, all bailed to face Melbourne Magistrates' Court in January.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Bird Flu Confirmed in a Victorian Fox for the First Time, With a Dolphin Death Also Suspected",
    "{{VIC_1_SUMMARY}}": "Authorities have confirmed H5 bird flu killed a fox at Torquay, south-west of Melbourne — Victoria's first known case of the virus in a mammal — and suspect it's also behind the death of a dolphin found at nearby Lorne, a week after a dolphin died of bird flu on South Australia's Fleurieu Peninsula.",

    # Science
    "{{SCI_1_FLAG}}": "🐾 PALAEONTOLOGY · THE 'AMERICAN CHEETAH' WASN'T A CHEETAH",
    "{{SCI_1_HEADLINE}}": "Ancient DNA Reveals the Extinct 'American Cheetah' Was Actually a Fish-Eating Cousin of the Puma",
    "{{SCI_1_SUMMARY}}": "A UC Santa Cruz-led study analysing ancient DNA and isotopes from fossils as far north as the Yukon has found that Miracinonyx trumani, long nicknamed the 'American cheetah,' is genetically closest to the puma, not true cheetahs, and that its northern Arctic population specialised in eating salmon and other fish to survive — extending the species' known range 20 degrees of latitude further north than previously thought.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Microsoft Just Cut AI Transcription Prices 72% — A Cheap Way to Turn Site Voice Notes Into Paperwork",
    "{{INSIGHT_BODY}}": "Microsoft's newest speech-to-text model dropped to 10 cents an audio hour this week, down from 36 cents, while adding better accuracy, speaker separation and word-level timestamps across 60 languages. That price drop matters more than it sounds for a small trades business: transcription is the unglamorous engine behind a lot of AI tools you might already be using or considering — voice memos turned into job notes, a recorded site walk-through turned into a scope of works, or a phone call with a client turned into a written record of what was actually agreed. If you've held off on any app that promises to turn talk into text because the running cost felt uncertain, this is the kind of quiet infrastructure price cut that makes it cheaper to actually try. It won't write your quote for you, but it can save you twenty minutes of typing up notes after every site visit.",

    # Fun facts
    "{{FACT_1}}": "Duct tape was invented in 1942 by Permacel, a division of Johnson & Johnson, to make a waterproof tape the US military could use to quickly reseal ammunition cases in the field — it was originally called 'duck tape' for its cotton duck-cloth backing, and wasn't put to work sealing actual air ducts until well after the war ended.",
    "{{FACT_2}}": "The cigarette lighter socket found in almost every ute and van today was standardised in the 1920s purely for lighting cigarettes in the dash — it only became the default 12-volt power socket for phone chargers, tyre inflators and fridges decades later, essentially by accident, because the plug shape was already everywhere.",
    "{{FACT_3}}": "The world's first webcam wasn't built for video calls — in 1991, computer scientists at Cambridge University pointed a camera at a coffee pot in another room and streamed the image to their desks, so they wouldn't waste a walk down the hall only to find it empty.",

    # Joke
    "{{JOKE_SETUP}}": "A bore and water-well driller was asked how his small business always managed to find water on blocks where three other contractors had already given up and gone home.",
    "{{JOKE_PUNCHLINE}}": "He said it wasn't a lucky divining rod — it was refusing to lock in a fixed price until after the test hole came back clean.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"What lies behind us and what lies ahead of us are tiny matters compared to what lives within us.\"",
    "{{CLOSING_ATTR}}": "— Ralph Waldo Emerson",
    "{{CLOSING_MESSAGE}}": "It's a wet, blustery Saturday in Carrum Downs, with a chance of a severe thunderstorm this morning and afternoon before easing tonight — worth keeping half an eye on the radar if you're on the tools outdoors. Overnight, the rescue of two workers alive from a Nepal hydropower tunnel nine days on is the kind of story worth pausing on, a reminder of what patient, methodical work can still pull off against long odds.",
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
