#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 06 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 6 Sep (BOM)
    "{{WEATHER_1}}": "SUN 6 SEP · 🌦️ Partly cloudy, medium chance of a shower, chance of a thunderstorm easing tonight, winds W to SW · 10–16°C",
    "{{WEATHER_2}}": "MON 7 SEP · 🌧️ Cloudy, high chance of showers about the ranges, medium chance elsewhere, winds SW · 9–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 8 SEP · 🌧️ Partly cloudy, medium chance of showers, most likely morning and afternoon, winds S to SW · 8–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 9 SEP · 🌤️ Cloudy clearing, medium chance of an early shower, winds SW turning S · 10–14°C",
    "{{WEATHER_5}}": "THU 10 SEP · ⛅ Partly cloudy, slight chance of a shower, light winds · 9–15°C",
    "{{WEATHER_ALERT}}": "No severe weather warning current this morning — today's thunderstorm risk eases tonight, then a showery, blustery pattern holds through Tuesday before it dries out midweek.",

    # World
    "{{WORLD_1_FLAG}}": "🇷🇺 MOSCOW · US ENVOYS ARRIVE WITH FRESH PEACE PUSH, KYIV NEXT",
    "{{WORLD_1_HEADLINE}}": "US Envoys Witkoff and Kushner Arrive in Moscow to Revive the Ukraine Peace Push, With a First-Ever Kyiv Visit to Follow",
    "{{WORLD_1_SUMMARY}}": "Steve Witkoff and Jared Kushner landed in Moscow on Saturday carrying a fresh Trump-backed proposal to end the war, ahead of a first visit to Kyiv; Vladimir Putin ordered a three-day halt to strikes on the Ukrainian capital to cover the trip, and Ukraine said it would hold off hitting Moscow over the same window, though no formal ceasefire has been reached after 4.5 years of war.",
    "{{WORLD_1_URL}}": "https://edition.cnn.com/2026/09/05/europe/witkoff-kushner-moscow-kyiv-proposal-war-intl",

    "{{WORLD_2_FLAG}}": "🇳🇵 NEPAL-CHINA BORDER · TOLL PASSES 1,375, THOUSANDS STILL MISSING",
    "{{WORLD_2_HEADLINE}}": "Nepal-China Flood Death Toll Climbs Past 1,375 as Rescuers Pull Another Survivor From a Buried Tunnel",
    "{{WORLD_2_SUMMARY}}": "Authorities on both sides of the border say the toll from the flash floods that struck 10 days ago has reached at least 1,375, with nearly 5,000 people still listed as missing; rescuers on Friday pulled a Chinese national alive from a flood-buried hydropower tunnel, a rare piece of good news as the search grinds into its second week.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/09/05/world/live-news/nepal-china-flood",

    # Economics
    "{{ECON_1_FLAG}}": "🏠 HOUSING · AFFORDABILITY HITS RECORD LOW DESPITE FALLING PRICES",
    "{{ECON_1_HEADLINE}}": "Housing Affordability Falls to Its Lowest Rate on Record, Even as Property Prices Ease",
    "{{ECON_1_SUMMARY}}": "New analysis shows a household on a typical income can now afford only around one in every ten homes sold nationally over the past financial year, with mortgage repayments as a share of income at their highest since 1989; economists say three rate rises this year have wiped out any relief from softer prices — a reminder of how squeezed household budgets are before you send the next quote.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-05/housing-affordability-hits-lowest-rate-on-record/107119844",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE UNLEADED STILL AVERAGING ABOVE 200C/L",
    "{{ECON_2_HEADLINE}}": "Melbourne Unleaded Averaging Around 203c/L, Diesel From 234.5c/L at the Cheapest Sites",
    "{{ECON_2_SUMMARY}}": "Melbourne bowsers are averaging close to 203c/L for unleaded and around 251c/L for diesel city-wide, though the cheapest reported sites are still down near 187.5c/L for unleaded and 234.5c/L for diesel in Preston — worth a quick check of your fuel app before a big fill, with the gap between cheapest and priciest sites still well over 15c/L.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🧮 AI RESEARCH · CLAUDE FORMALISES A 358-YEAR-OLD PROOF",
    "{{TECH_1_HEADLINE}}": "Anthropic Says Claude Produced the First Fully Computer-Checked Proof of Fermat's Last Theorem",
    "{{TECH_1_SUMMARY}}": "Anthropic reports its Claude model worked largely autonomously for 11 days to write a complete, machine-verified proof of Fermat's Last Theorem in the Lean programming language — 13 million lines of code proving over 29,000 supporting theorems; it's a research milestone rather than a product, but a sign of how far automated reasoning tools have come for anything that needs to be checked, not just guessed at.",
    "{{TECH_1_URL}}": "https://www.anthropic.com/research/formalizing-fermats-last-theorem",

    "{{TECH_2_FLAG}}": "📸 PRACTICAL AI · GEMINI CAN NOW RUN YOUR PHOTO LIBRARY",
    "{{TECH_2_HEADLINE}}": "Google's Gemini Spark Can Now Search, Edit and Organise Your Entire Google Photos Library on Command",
    "{{TECH_2_SUMMARY}}": "Google has connected its Gemini Spark agent to Google Photos for subscribed users, letting it search old albums, batch-edit and caption photos, build shareable albums and run scheduled photo tasks in the background — the kind of tedious sorting-and-labelling job that, pointed at a folder of site photos instead of holiday snaps, starts to look like a genuinely useful admin shortcut.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 PHYSICAL AI · FIGURE LOCKS IN UP TO $6B IN GPU COMPUTE",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robot Maker Figure Signs Up to $6 Billion in Compute With Nscale to Train Its Next-Generation Robots",
    "{{ROBOT_1_SUMMARY}}": "Figure has partnered with AI infrastructure firm Nscale to deploy up to 100,000 Nvidia Vera Rubin GPUs, starting with a $3.5 billion commitment that could scale past $6 billion, to train and run future versions of the Helix AI models powering its humanoid robots; the deal underlines just how much raw computing power now sits behind every 'robot learns a new task' headline coming out of the industry.",
    "{{ROBOT_1_URL}}": "https://www.pymnts.com/news/artificial-intelligence/2026/nscale-inks-3-5-billion-deal-with-robotics-firm-figure",

    # Australia
    "{{AUS_1_HEADLINE}}": "Victoria Police Hunt Man Who Allegedly Attacked Three People With an Axe in Gippsland",
    "{{AUS_1_SUMMARY}}": "Police allege a man in his 50s, known to his victims, attacked an elderly couple and another man with an axe and handsaw at a Tyers property on Friday, leaving two victims with life-threatening injuries; he remains on the run and the public has been warned not to approach him.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-05/alleged-axe-attack-gippsland-victoria-police-search/107120310",

    "{{AUS_2_HEADLINE}}": "Five Children Hospitalised as Wild Winds Lift Jumping Castles in Two States on the Same Day",
    "{{AUS_2_SUMMARY}}": "Two children were taken to hospital in Geelong after a jumping castle was lifted into the air at a birthday party in Victoria's south-west, while three more were hospitalised in Sydney after a separate incident, both linked to wind gusts topping 90km/h — a timely reminder to peg down anything inflatable before this week's blustery run properly sets in.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Soccer Club Demands Action After Girls' Match Halted Mid-Game to Make Way for Boys",
    "{{VIC_1_SUMMARY}}": "The Boroondara Eagles say an under-12 girls' match at Oakleigh was stopped at half-time so an under-11 boys' team could use the field, with the girls sent to a waterlogged backup pitch and the game ultimately abandoned — the club says a young coach left in tears, and it's demanding the league explain why the girls' fixture wasn't given the same protection as the boys'.",

    # Science
    "{{SCI_1_FLAG}}": "🔭 PHYSICS · A HINT OF DARK MATTER, BUT NOT YET A DISCOVERY",
    "{{SCI_1_HEADLINE}}": "Underground Detector Records a Tantalising, Unexplained Signal in the Hunt for Dark Matter",
    "{{SCI_1_SUMMARY}}": "The LUX-ZEPLIN experiment, buried 1.5km down in a former South Dakota gold mine, has recorded a single particle collision its team can't explain with any known background source, pointing towards a dark matter particle heavier than expected; it's only a 2.6-sigma result — well short of the 5-sigma bar physicists need to call it a discovery — but it's the most compelling hint the decade-long experiment has produced so far.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Google's Gemini Spark Can Now Manage a Whole Photo Library — Point the Same Idea at Job Photos Instead of Holiday Snaps",
    "{{INSIGHT_BODY}}": "This week Google switched on Gemini Spark's ability to search, sort, caption and share your entire Google Photos library on request, aimed at people drowning in years of unsorted holiday pictures. For a small trades business, the more useful version of that problem is the folder of before-and-after site photos, defect shots and completed-job proof sitting untouched on your phone. The same kind of AI photo-management tool — whether it's Google's own, or one built into a trade-specific app — can be pointed at a job folder to auto-caption what's in each shot, group everything by client or address, and pull together a tidy before/after set for an invoice or insurance claim in minutes instead of an evening. It won't replace your own eye for a defect, but it can turn a phone full of scattered photos into something a client — or an insurer — can actually use.",

    # Fun facts
    "{{FACT_1}}": "Pierre de Fermat scribbled his famous theorem in the margin of a book in 1637, claiming he had a proof too large to fit — it took 358 years and Andrew Wiles's seven-year effort to finally prove it in 1994, and this week Anthropic says its Claude model produced the first fully computer-checked version of that proof, running to 13 million lines of code.",
    "{{FACT_2}}": "The LUX-ZEPLIN dark matter detector sits 1.5 kilometres underground in a former gold mine in South Dakota, submerged in 10 tonnes of liquid xenon and shielded by a mountain of rock, purely so cosmic rays can't drown out the one-in-a-trillion chance of spotting a genuine dark matter particle colliding with an atom.",
    "{{FACT_3}}": "The term 'blue-collar' dates to 1920s America, when manual labourers wore hard-wearing chambray or denim work shirts — dyed blue partly because it hid dirt and grease better than the white dress shirts worn by office workers — giving rise to the blue-collar/white-collar divide that's still used almost a century later.",

    # Joke
    "{{JOKE_SETUP}}": "A carpet cleaner was asked why his small business never had a single unhappy customer, no matter how bad the stain.",
    "{{JOKE_PUNCHLINE}}": "He said the trick was never promising to get the stain out — it was telling the customer exactly what would still be there before he ever plugged the machine in.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Nothing in this world can take the place of persistence.\"",
    "{{CLOSING_ATTR}}": "— Calvin Coolidge",
    "{{CLOSING_MESSAGE}}": "It's a cooler, showery start to the week ahead in Carrum Downs, with today's thunderstorm risk easing tonight before a blustery, wet pattern holds into Tuesday — good tools-under-cover weather rather than tools-out. Overnight, word that Trump's envoys have reached Moscow with a fresh peace push, and are due in Kyiv next, is a story worth watching this week rather than acting on — a reminder that even the slowest-moving problems can shift once the right people finally sit down.",
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
