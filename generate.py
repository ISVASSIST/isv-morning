#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 26 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 26 Jul (BOM)
    "{{WEATHER_1}}": "SUN 26 · 🌦️ Partly cloudy, chance of a morning shower · 9–15°C",
    "{{WEATHER_2}}": "MON 27 · ☁️🌧️ Cloudy, shower likely (evening) · 9–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 28 · ☁️🌧️ Cloudy, very high chance of showers · 8–16°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 29 · 🌦️ Cloudy, shower or two · 8–14°C",
    "{{WEATHER_5}}": "THU 30 · ⛅ Partly cloudy, isolated shower · 7–13°C",
    "{{WEATHER_ALERT}}": "⚠ NO SEVERE WEATHER WARNINGS ACTIVE FOR METRO MELBOURNE",

    # World
    "{{WORLD_1_FLAG}}": "🇸🇦🛢️ SAUDI ARABIA · HOUTHIS STRIKE ARAMCO · OIL SURGES PAST $100 A BARREL",
    "{{WORLD_1_HEADLINE}}": "Houthi Missiles Hit Saudi Aramco Refineries at Jizan and Yanbu, Oil Rockets Past $100",
    "{{WORLD_1_SUMMARY}}": "Yemen's Houthi rebels struck Aramco's Jizan refinery and the Yanbu export terminal before dawn Saturday with a barrage of ballistic missiles and drones, setting the Jizan site ablaze and pushing Brent crude back above $100 a barrel for the first time since May. The strikes hit the very pipeline route Saudi Arabia spent five months building to bypass the Iran-blockaded Strait of Hormuz — only for the Houthis to declare the Bab al-Mandeb strait at the other end a blockade zone days earlier, squeezing Riyadh's oil exports from both directions.",
    "{{WORLD_1_URL}}": "https://www.techtimes.com/articles/321583/20260725/houthi-strike-burns-jizan-aramco-refinery-yanbu-attack-seals-saudi-arabias-oil-trap.htm",

    "{{WORLD_2_FLAG}}": "🇫🇷📵 FRANCE · UNDER-15S BANNED FROM SOCIAL MEDIA · FIRST IN THE EU",
    "{{WORLD_2_HEADLINE}}": "France Becomes First EU Nation to Pass a Blanket Social Media Ban for Under-15s",
    "{{WORLD_2_SUMMARY}}": "Both chambers of France's parliament voted this week to ban children under 15 from using social media outright, extend mobile phone bans into high schools, and require platforms to bring in age verification — a flagship push by President Macron after the country's public health watchdog linked social media to harm in teenage mental health, especially among girls.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/world/europe/french-lawmakers-approve-sweeping-social-media-ban-children-15-rcna588591",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AT THE BOWSER · DIESEL STILL ABOVE 214¢/L · ACCC'S 20TH WEEKLY REPORT",
    "{{ECON_1_HEADLINE}}": "Diesel Still Sitting Above 214 Cents a Litre as Excise Restoration Keeps Biting",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly fuel report, out Friday and covering to 22 July, has average petrol across the five biggest cities at 179.5 cents a litre and diesel at 214.9 cents — up 28.0 and 41.4 cents respectively since 30 June, with Melbourne recording the largest diesel jump of any capital. With Brent crude now back above $100 a barrel on the Red Sea escalation, worth assuming next week's report keeps climbing rather than levelling off.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📉 OUTLOOK · NAB CALLS IT 'LESS OF A SPIKE, MORE OF A GRIND' · SLOW GROWTH AHEAD",
    "{{ECON_2_HEADLINE}}": "NAB's July Outlook Sees Below-Trend Growth Into 2027, But Confirms AI Is Already Mainstream for SMEs",
    "{{ECON_2_SUMMARY}}": "NAB's latest Forward View still has Australian growth running below trend into next year and unemployment edging higher, citing the Middle East oil shock and elevated rates — but a companion NAB survey found 42% of Australian small and medium businesses are already using AI tools daily, with another 14% planning to, led by property, finance and business services.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · GOOGLE'S AI SPEND HITS $205B · RECORD CAPEX RAISE THIS WEEK",
    "{{TECH_1_HEADLINE}}": "Google Raises 2026 AI Spending to a Record $205 Billion as Compute Demand Outstrips Supply",
    "{{TECH_1_SUMMARY}}": "Alphabet lifted its 2026 capital expenditure guidance to $195–205 billion this week — up from an earlier cap of $190 billion — after its CFO told investors demand for AI compute is running ahead of what the company can build. Quarterly capex hit a record $44.9 billion and pushed Alphabet to its first-ever negative free cash flow quarter, a reminder of just how much money is being poured into the infrastructure behind the AI tools now reaching everyday businesses.",
    "{{TECH_1_URL}}": "https://www.bloomberg.com/news/articles/2026-07-22/google-boosts-2026-spending-estimate-to-as-much-as-205-billion",

    "{{TECH_2_FLAG}}": "⚖️ REGULATION · EU FORCES GOOGLE TO OPEN ANDROID · RIVAL AI ASSISTANTS GET SYSTEM ACCESS",
    "{{TECH_2_HEADLINE}}": "EU Orders Google to Open Android to Rival AI Assistants Like ChatGPT and Claude",
    "{{TECH_2_SUMMARY}}": "Brussels' Digital Markets Act ruling forces Google to grant competing AI assistants the same system-level access to Android that its own Gemini enjoys — wake-word invocation, app data, autonomous control of settings — across 11 capabilities by August 2027. It opens the door for the AI tools you already use to eventually run more of your phone directly, not just answer questions in a chat window.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · HYUNDAI WORKERS STRIKE OVER ATLAS · FIRST-EVER HUMANOID ROBOT LABOUR ACTION",
    "{{ROBOT_1_HEADLINE}}": "Hyundai's Ulsan Workers Escalate the Auto Industry's First-Ever Strike Over a Humanoid Robot",
    "{{ROBOT_1_SUMMARY}}": "Thousands of unionised workers at Hyundai's Ulsan complex have kept up four-hour daily partial strikes this week, demanding a binding guarantee that no Boston Dynamics Atlas robot enters the plant without a labour agreement first — even though Hyundai's own roadmap has Atlas starting only basic parts-sequencing work at its US plant from 2028. It's a preview of the conversation every business bringing in automation will eventually need to have with its own people, just playing out at industrial scale first.",
    "{{ROBOT_1_URL}}": "https://www.techtimes.com/articles/321150/20260721/hyundai-finalizes-boston-dynamics-takeover-workers-strike-over-atlas-same-day.htm",

    # Australia
    "{{AUS_1_HEADLINE}}": "Nationwide AusAlert Phone Test Set for 2pm Tomorrow Ahead of October Launch",
    "{{AUS_1_SUMMARY}}": "Every compatible phone in Australia will vibrate and sound a 10-second siren-like alert at 2pm AEST tomorrow as the government tests its new AusAlert emergency warning system ahead of its full launch in October — the message will clearly say it's a test, and no action is needed.",
    "{{AUS_1_URL}}": "https://www.nema.gov.au/about-us/media-centre/prepare-ausalert-national-test-27-july-2026",

    "{{AUS_2_HEADLINE}}": "Australia Tops the Pool at Commonwealth Games 2026 With Six Golds From Six Swims",
    "{{AUS_2_SUMMARY}}": "Australia led the swimming medal table on day two of the Commonwealth Games in Glasgow yesterday, with Lani Pallister (400m freestyle), Jenna Forrester (200m backstroke) and Para-swimmer Jenna Jones (100m freestyle S13) all taking gold.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "North Melbourne Close Out AFL Round 20 Against St Kilda at Marvel Stadium Today",
    "{{VIC_1_SUMMARY}}": "It's a 3:15pm bounce down at Marvel Stadium as North Melbourne host St Kilda to close out Round 20 — the last home-and-away Sunday fixture before finals jockeying starts to heat up.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 PLANETARY SCIENCE · VENUS ISN'T 'DEAD' AFTER ALL · RIFT VALLEYS ACTIVELY WIDENING",
    "{{SCI_1_HEADLINE}}": "Venus May Be Tearing Itself Apart From Within, New 3D Simulations Show",
    "{{SCI_1_SUMMARY}}": "High-resolution 3D modelling led by ETH Zurich, published this week, shows some of Venus's giant rift valleys are geologically young and may still be actively widening by 3–10cm a year — upending the long-held assumption that Venus is a 'geologically dead' world and suggesting its interior is still actively tearing the crust apart.",

    # Business insight
    "{{INSIGHT_TITLE}}": "OpenAI Just Built a Program Specifically for Small Business — Here's What's Actually Useful In It",
    "{{INSIGHT_BODY}}": "OpenAI launched a dedicated small-business program this week built around 'ChatGPT Work,' an agentic tool that handles multi-step admin tasks — not just chat — like expense management and accounts payable. It landed the same week NAB data confirmed 42% of Australian small and medium businesses are already using AI daily, with another 14% planning to. Skip the webinars and partner integrations aimed at bigger operators — the real signal for a business ISV's size is that the biggest AI labs are now explicitly designing for one-person back offices, which means the tools handling your quotes, invoices and supplier admin are about to get a lot more plug-and-play, not just something built for enterprise IT departments.",

    # Fun facts
    "{{FACT_1}}": "The Mayday distress call isn't an acronym — it comes from the French 'venez m'aider' ('come help me'), shortened in 1923 by Frederick Stanley Mockford, a senior radio officer at London's Croydon Airport, because it was equally easy for British and French pilots to say and understand over a crackly radio.",
    "{{FACT_2}}": "'Quarantine' comes from the Venetian Italian 'quaranta giorni' — forty days — the mandatory holding period Venice imposed on ships arriving from plague-affected ports in the 14th century, no matter how healthy the crew looked.",
    "{{FACT_3}}": "The electric eel isn't actually an eel — it's a knifefish — and carries three separate electric organs making up 80% of its body, capable of firing a discharge up to 860 volts, the highest voltage shock recorded from any living animal.",

    # Joke
    "{{JOKE_SETUP}}": "A client asked a shopfitter for a 'quick' turnaround on a retail fit-out before opening week.",
    "{{JOKE_PUNCHLINE}}": "He said sure — then quietly ordered four weeks' worth of coffee for the crew.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Difficulties strengthen the mind, as labor does the body.\"",
    "{{CLOSING_ATTR}}": "— Seneca",
    "{{CLOSING_MESSAGE}}": "It's a showery start to the week ahead — North Melbourne and St Kilda close out AFL Round 20 at Marvel Stadium this afternoon, and if your phone sounds a siren at 2pm tomorrow, that's just the new AusAlert system being tested, not an emergency.",
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
