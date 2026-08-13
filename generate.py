#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 14 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 14 Aug (BOM)
    "{{WEATHER_1}}": "FRI 14 · ☁️ Cloudy, slight chance of a shower · 7–15°C",
    "{{WEATHER_2}}": "SAT 15 · ⛅ Partly cloudy, medium chance of a shower, most likely early morning · 6–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SUN 16 · 🌦️ Partly cloudy, high chance of showers, most likely afternoon and evening · 7–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 17 · 🌧️ Cloudy, very high chance of showers, windy · 8–16°C",
    "{{WEATHER_5}}": "TUE 18 · ⛅ Showers easing, partly cloudy · 7–15°C",
    "{{WEATHER_ALERT}}": "No BOM warnings currently listed for Carrum Downs — the wetter, breezier pattern building in from Saturday is the main thing to plan outdoor jobs around this weekend",

    # World
    "{{WORLD_1_FLAG}}": "🇨🇴 COLOMBIA · EARTHQUAKE DEATH TOLL CLIMBS PAST 270 AS RESCUE TEAMS DIG THROUGH RUBBLE",
    "{{WORLD_1_HEADLINE}}": "Colombia Earthquake Death Toll Passes 273 as Recovery Effort Grinds On in Cali and Pereira",
    "{{WORLD_1_SUMMARY}}": "The toll from Monday's 7.4-magnitude earthquake in western Colombia has climbed to at least 273 dead and nearly 3,300 injured, with officials reporting roughly 12,600 homes destroyed and almost 75,000 more damaged across Cali, Pereira and the Chocó region near the epicentre. Search and recovery crews are still working through collapsed buildings four days on, with the country's new government under mounting pressure to speed up aid to displaced families.",
    "{{WORLD_1_URL}}": "https://www.local10.com/news/world/2026/08/13/earthquake-in-colombia-at-least-273-dead-3284-injured/",

    "{{WORLD_2_FLAG}}": "🇺🇸 WHITE HOUSE · PRESS SECRETARY KAROLINE LEAVITT TO STEP DOWN AT MONTH'S END",
    "{{WORLD_2_HEADLINE}}": "Karoline Leavitt to Step Down as White House Press Secretary, Trump Says She'll Become a Top Adviser",
    "{{WORLD_2_SUMMARY}}": "President Trump announced this week that press secretary Karoline Leavitt, the youngest person to hold the role, will leave her post at the end of August to spend more time with her young family, moving into a role as one of his top outside advisers ahead of the November midterms. It's a reminder that even the most visible jobs in politics run on the same trade-off small business owners know well — long hours up front, then a deliberate step back when it's time to hand things over.",
    "{{WORLD_2_URL}}": "https://www.axios.com/2026/08/12/trump-karoline-leavitt-white-house-press",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺🏦 RBA · GOVERNOR MICHELE BULLOCK SPEAKS TODAY, DAYS AFTER THE BOARD HELD RATES AT 4.35%",
    "{{ECON_1_HEADLINE}}": "RBA Governor Michele Bullock Speaks Today, Three Days After the Board Held the Cash Rate at 4.35%",
    "{{ECON_1_SUMMARY}}": "Governor Michele Bullock is scheduled to speak this morning, coming just days after the Reserve Bank board held the cash rate steady at 4.35% and flagged that underlying inflation is still running above target while the labour market and housing have both started to soften. Any fresh signal on the timing of the next move is worth watching before locking in financing costs on new equipment or a vehicle upgrade.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/news/",

    "{{ECON_2_FLAG}}": "⛽🇦🇺 FUEL · MELBOURNE PETROL HOLDS STEADY AROUND $2.00/L AS THE POST-EXCISE ADJUSTMENT SETTLES",
    "{{ECON_2_HEADLINE}}": "Melbourne Petrol Holds Around $2.00/L This Week as the Post-Excise Price Shock Settles Down",
    "{{ECON_2_SUMMARY}}": "Melbourne's average unleaded price has barely moved over the past few days, sitting around $2.00 a litre with the cheapest sites near 186c/L, suggesting the adjustment from the fuel excise's return to full rate on 3 August has largely worked its way through the bowser. A quieter week on fuel is a decent window to firm up any transport costs still sitting on placeholder numbers in open quotes.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖💻 AI TOOLS · MICROSOFT CULLS UNDERUSED COPILOT FEATURES, MERGES ITS SEPARATE APPS",
    "{{TECH_1_HEADLINE}}": "Microsoft Kills Off Underused AI Features and Merges Its Separate Copilot Apps Into One",
    "{{TECH_1_SUMMARY}}": "Microsoft is retiring several Copilot features that failed to gain traction — including Group Chats, AI-generated podcasts and Copilot Labs experiments — by 18 August, while folding its various standalone Copilot apps into a single product. Even a company Microsoft's size is willing to cut tools nobody used rather than maintain them out of habit — a decent nudge to audit your own AI subscriptions and drop the ones that aren't actually saving you time.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/08/13/microsoft-kills-off-unsuccessful-ai-features-while-merging-its-separate-copilot-apps/",

    "{{TECH_2_FLAG}}": "🤖🏢 AI RACE · GOOGLE HANDS ITS GEMINI PUSH TO A NEW CHIEF TO CATCH ANTHROPIC AND OPENAI",
    "{{TECH_2_HEADLINE}}": "Google Elevates DeepMind Veteran Koray Kavukcuoglu to Lead Gemini as It Chases Anthropic and OpenAI",
    "{{TECH_2_SUMMARY}}": "Google has handed DeepMind veteran Koray Kavukcuoglu a new leadership role overseeing Gemini model development and the Gemini app, reporting directly to CEO Sundar Pichai, after the company went months without a frontier model release while Anthropic and OpenAI kept shipping. For a small business the reshuffle itself doesn't matter much — but it's a sign the big three are about to compete harder on price and features, which is generally good news for whoever's paying the subscription.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭🤖 ROBOTICS · UNITREE'S SHANGHAI IPO ALLOCATION RESULTS LAND TODAY",
    "{{ROBOT_1_HEADLINE}}": "Unitree's Shanghai STAR Market IPO Allocation Results Due Today, Ahead of China's First Listed Humanoid Robot Maker Going Public",
    "{{ROBOT_1_SUMMARY}}": "Allocation results for Unitree's roughly $900 million Shanghai IPO — priced at 150.80 yuan a share and oversubscribed more than 8,000 times by retail investors — are due to be announced today, with the listing expected within days, making it the first humanoid robotics maker on the Chinese stock market. It's another marker of how fast money is flowing into industrial and humanoid robotics right now, even if the practical automation most small operators will actually touch is still years off, not this stock listing.",
    "{{ROBOT_1_URL}}": "https://www.odaily.news/en/post/5212321",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Sets 'World-Leading' Minimum Pay and Insurance Rules for Gig Delivery Drivers From August 17",
    "{{AUS_1_SUMMARY}}": "New minimum standards take effect from 17 August for roughly 250,000 food and grocery delivery workers, setting hourly rates from $31.30 for e-bike riders up to $32 for drivers, alongside compulsory insurance obligations for both workers and the platforms that engage them. Both Uber and DoorDash have walked back earlier objections and are now working with the Transport Workers Union on the rollout — worth noting if your business relies on gig platforms for deliveries or last-mile logistics.",
    "{{AUS_1_URL}}": "https://www.insurancejournal.com/news/international/2026/08/13/881239.htm",

    "{{AUS_2_HEADLINE}}": "Bird Flu Spreads Further Across Australia as Scientists Warn of 'Extinction-Level' Risk to Native Wildlife",
    "{{AUS_2_SUMMARY}}": "Confirmed H5 bird flu cases have climbed past 230 nationally — including more than 160 in South Australia and dozens in Victoria — with scientists warning pelicans, black swans, cormorants and cassowaries face severe population decline if the virus takes hold in local strains. The Albanese government is reportedly weighing extra funding as the first vaccine rollout for vulnerable species begins.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "More Than 400 Extra Weekly Train Services Roll Out Across Melbourne's Network From August 23",
    "{{VIC_1_SUMMARY}}": "Victoria's new timetable adds more than 400 extra weekly services from 23 August, including trains every 10 minutes between Newport and Sandringham via Flinders Street for the first time, plus more frequent services on the Craigieburn and Upfield lines. Worth factoring into any job scheduling that leans on public transport for staff or apprentices getting to sites across the network.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 SCIENCE · A SINGLE BRAIN CELL MAY COMPUTE LIKE A WHOLE MINI NEURAL NETWORK",
    "{{SCI_1_HEADLINE}}": "Scientists Find a Single Human Brain Cell Can Compute Like a Deep Neural Network on Its Own",
    "{{SCI_1_SUMMARY}}": "New research published this week finds individual human cortical neurons carry out far more complex computations than previously thought — with a single neuron's information-processing power roughly comparable to an entire small deep neural network, well beyond neurons in other mammals. It may help explain how the human brain supports language, imagination and maths, and researchers say it could inspire a new generation of AI built from more powerful individual units rather than today's simplified ones.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Microsoft Just Culled Its Own AI Features — The Lesson for Your Trades Business",
    "{{INSIGHT_BODY}}": "Microsoft's decision this week to kill off underused Copilot features and merge its scattered AI apps into one is a useful mirror for any small operator who's signed up to three or four AI tools since the start of the year. If a company with Microsoft's resources is willing to cut tools that didn't earn their keep, it's worth doing the same audit on your own subscriptions: which AI tool actually saves you time on quoting, scheduling or invoicing every week, and which one is just a recurring charge you haven't looked at since the free trial ended? Pick the one or two that are pulling their weight, cancel the rest, and put the saved subscription cost toward the tool you actually use.",

    # Fun facts
    "{{FACT_1}}": "The Southern Cross windmill, first built in 1876 by South Australian blacksmith brothers Robert and George Griffiths, used a fixed, curved steel-blade design that needed no gears or oiling — pumping bore water across the outback for well over a century with only basic upkeep.",
    "{{FACT_2}}": "The Sunshine Harvester, built by H.V. McKay in Ballarat from 1885, was the first machine to strip, thresh and clean wheat in a single pass across a paddock — the landmark 1907 Harvester Judgment, which set Australia's first 'fair and reasonable' minimum wage, used the company's own production costs as its benchmark case.",
    "{{FACT_3}}": "The Australian term 'smoko' for a work break traces back to 19th-century shearing sheds and mining camps, where scheduled tea-and-tobacco breaks were common practice long before the word was formally written into union awards.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the TV antenna and aerial installer never miss a payment from a client?",
    "{{JOKE_PUNCHLINE}}": "Because he always made sure everything was above board — literally, up on the roof.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Nothing will work unless you do.\"",
    "{{CLOSING_ATTR}}": "— Maya Angelou",
    "{{CLOSING_MESSAGE}}": "It's a cloudy Friday in Carrum Downs with just a slight chance of a shower before a wetter, breezier pattern builds in from Saturday — a fair window to get outdoor jobs ticked off while conditions hold. With the RBA Governor speaking this morning and Unitree's IPO results landing in Shanghai today, it's a day with a bit more than usual moving in the background — worth a coffee before you open the inbox.",
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
