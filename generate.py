#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 28 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 28 Aug (BOM)
    "{{WEATHER_1}}": "FRI 28 · ☁️ Cloudy, slight chance of a shower · 9–15°C",
    "{{WEATHER_2}}": "SAT 29 · ⛈️ Showers, chance of a thunderstorm, windy · 10–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 30 · 🌧️ Cold front crosses, showers easing PM · 8–13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 31 · ⛅ Clearing, sunny spells · 7–15°C",
    "{{WEATHER_5}}": "TUE 1 SEP · ☀️ Mostly sunny and mild · 8–16°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula. A trough moves over the bays tonight ahead of a cold front crossing Bass Strait Sunday — today's your cleanest outdoor blasting and coating window before Saturday turns showery and windy.",

    # World
    "{{WORLD_1_FLAG}}": "🇳🇵 NEPAL–TIBET · GLACIAL FLOOD LEAVES 1,500 MISSING",
    "{{WORLD_1_HEADLINE}}": "Nearly 1,500 Missing After Glacial Flood Sweeps Nepal-Tibet Border Villages",
    "{{WORLD_1_SUMMARY}}": "A glacial collapse triggered flash floods that swept away entire villages on the Nepal-Tibet border, killing at least 270 people in Nepal with hundreds more dead or missing on the Chinese side; officials say 644 foreign nationals — including 35 Australians — remain unaccounted for, many of them Hindu pilgrims travelling to Kailash Mansarovar.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/27/nx-s1-5946309/nepal-tibet-deadly-floods",

    "{{WORLD_2_FLAG}}": "🇮🇱 GAZA · US CEASEFIRE ENVOY CRITICISES ISRAELI STRIKES",
    "{{WORLD_2_HEADLINE}}": "Trump's Own Gaza Ceasefire Envoy Criticises Israel Over Renewed Strikes",
    "{{WORLD_2_SUMMARY}}": "Nikolay Mladenov, the official leading President Trump's Gaza ceasefire plan, told the UN Security Council that near-daily Israeli strikes since the truce began have killed around 1,200 people in the enclave, warning of a choice between a rebuilt Gaza or \"the next war already on the horizon.\"",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/08/27/g-s1-140400/israel-gaza-ceasefire",

    # Economics
    "{{ECON_1_FLAG}}": "📈 RATES · CBA JOINS NAB IN TIPPING A RATE HIKE",
    "{{ECON_1_HEADLINE}}": "CBA Flips to Forecasting a Rate Hike as Fuel-Driven Inflation Bites",
    "{{ECON_1_SUMMARY}}": "CBA reversed its call on Thursday and now expects the RBA to lift the cash rate to 4.60% in November, joining NAB (which tips a September move) after July's inflation print showed core price pressure holding firm even as fuel and excise costs keep climbing — bad news for any small business carrying equipment finance or a business loan.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-08-27/asx-markets-business-news-live-updates-thursday-27-august/107083084",

    "{{ECON_2_FLAG}}": "🛒 SPENDING · HOUSEHOLD SPEND HITS FASTEST GROWTH IN 3 YEARS",
    "{{ECON_2_HEADLINE}}": "Household Spending Grows at Fastest Pace in Three Years, Adding to Rate Pressure",
    "{{ECON_2_SUMMARY}}": "ABS figures show household spending rose 1.1% in July — a third straight monthly rise and 7% higher than a year ago, the fastest annual growth since June 2023 — which economists say gives the RBA more room to justify a rate rise, even as small operators are still absorbing higher fuel and finance costs.",
    "{{ECON_2_URL}}": "https://www.savings.com.au/news/household-spending-growth-hits-fastest-pace-in-3-years",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🛡️ AI SECURITY · 100+ FIRMS INCLUDING ANTHROPIC AND OPENAI SIGN CYBER PACT",
    "{{TECH_1_HEADLINE}}": "OpenAI, Anthropic, Google and 100+ Companies Call for Joint Defence Against AI Cyber Threats",
    "{{TECH_1_SUMMARY}}": "More than a hundred tech, cybersecurity and financial firms — including OpenAI, Anthropic, Google, Microsoft, CrowdStrike and Okta — signed an open letter urging governments and industry to coordinate on defending against AI-enabled cyber attacks, warning such attacks \"will become far more widespread and sophisticated\" as models grow more capable.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/08/27/openai-anthropic-google-and-100-other-companies-call-for-action-to-defend-against-rogue-ai/",

    "{{TECH_2_FLAG}}": "💬 AI TOOLS · GOOGLE'S CHEAPEST GEMINI YET TARGETS BUSINESS TASKS",
    "{{TECH_2_HEADLINE}}": "Google Launches Gemini 3.7 Flash With Business-Automation Pricing",
    "{{TECH_2_SUMMARY}}": "Google introduced Gemini 3.7 Flash, pitched at coding, document work and everyday business automation, with introductory pricing of $0.75 per million input tokens and $3.75 per million output tokens through the end of 2026 — a further sign the cost of running practical AI tools for admin work keeps falling.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 HUMANOID ROBOTS · FIGURE AI PASSES 1,000 COMMERCIAL UNITS",
    "{{ROBOT_1_HEADLINE}}": "Figure AI, Not Tesla, Now Leads US Humanoid Robot Production, Analysts Say",
    "{{ROBOT_1_SUMMARY}}": "Figure AI has become the first US company to pass 1,000 commercially deployed humanoid robots, building its Figure 03 model at roughly one per hour at its BotQ facility, while Tesla's Optimus Gen 3 is still in a low-volume production ramp — a sign the practical, working-hours-logged robots are pulling ahead of the hype.",
    "{{ROBOT_1_URL}}": "https://www.benzinga.com/trading-ideas/long-ideas/26/08/61407174/tesla-not-leading-humanoid-robotics-figure-ai-is",

    # Australia
    "{{AUS_1_HEADLINE}}": "Voluntary Assisted Dying Becomes Legal Nationwide as NT Parliament Passes Bill",
    "{{AUS_1_SUMMARY}}": "The Northern Territory parliament passed voluntary assisted dying laws in a conscience vote on Thursday night, making the practice legal in every Australian state and territory for the first time since the federal government overturned the NT's original 1995 law.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-27/nt-to-pass-voluntary-assisted-dying-bill-in-parliament/107087354",

    "{{AUS_2_HEADLINE}}": "Household Spending Posts Fastest Annual Growth Since 2023",
    "{{AUS_2_SUMMARY}}": "New ABS data shows Australians opened their wallets further in July, with spending on recreation, food, and hotels and cafes driving a third consecutive monthly rise — a sign of resilience in consumer demand even as trades businesses juggle higher fuel and finance costs.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Auditor-General Reveals Victoria Hid a Secret Levy on Every Public Transport Fare",
    "{{VIC_1_SUMMARY}}": "A Victorian Auditor-General report found the state government quietly added an undisclosed 1% annual levy to public transport fares since 2025 to help fund the Suburban Rail Loop, raising $6.5 million so far without ever telling commuters — Premier Ben Carroll has now vowed to scrap it and apologised for the lack of transparency.",

    # Science
    "{{SCI_1_FLAG}}": "🚀 MATERIALS SCIENCE · AI CRACKS A NASA ALLOY IN 40 TRIES, NOT MILLIONS",
    "{{SCI_1_HEADLINE}}": "AI Searches 100 Million Options to Find a Cheaper Way to 3D-Print a NASA Rocket Alloy",
    "{{SCI_1_SUMMARY}}": "Washington State University researchers used an AI model to sift through more than 100 million possible 3D-printing settings for GRCop-42, a heat-resistant copper alloy NASA developed for rocket engines, narrowing it to just 40 real-world trials and finding six settings that work on ordinary commercial printers — cutting what would have been months of trial and error down to weeks.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Two of the Big Four Now Expect a Rate Hike — Here's How AI Cash-Flow Forecasting Can Buy You a Buffer",
    "{{INSIGHT_BODY}}": "NAB and now CBA are both tipping the RBA to raise rates again this year, after July's inflation data showed fuel and core costs still running hot. For a small trades business carrying equipment finance or a ute loan, that's a real hit to the bottom line if it lands unplanned. Cheap AI-linked forecasting tools, built into most modern accounting packages, can now model \"what if rates rise 0.25% in September\" against your actual job pipeline in seconds — giving you a genuine buffer to decide on that new compressor or hire before the banks decide for you.",

    # Fun facts
    "{{FACT_1}}": "Every vehicle sold in Australia since the mid-2000s carries an OBD-II diagnostic port, originally mandated in the US back in 1996 purely for emissions testing — the same port that now lets a $50 Bluetooth dongle and a phone app read fault codes that used to need a dealer-only scan tool costing thousands.",
    "{{FACT_2}}": "The air fryer sitting on an estimated one in three Australian kitchen benches isn't new technology — Philips only patented the countertop version in 2010, but it's really a compact version of the rapid-air convection ovens commercial kitchens have used since the 1950s.",
    "{{FACT_3}}": "Dry ice blasting — firing frozen CO2 pellets at surfaces to strip coatings and contamination — was developed by NASA's Marshall Space Flight Center in the 1980s to clean rocket engine components, and leaves no secondary waste because the pellets sublimate straight back into gas on impact.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the generator technician's small business never lose power, even during a state-wide blackout?",
    "{{JOKE_PUNCHLINE}}": "Because he'd already sold himself a backup plan.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"A goal without a plan is just a wish.\"",
    "{{CLOSING_ATTR}}": "— Antoine de Saint-Exupéry",
    "{{CLOSING_MESSAGE}}": "It's a cloudy but calm Friday in Carrum Downs before Saturday turns showery and windy with a cold front through Sunday, so today's genuinely your best outdoor window this week. With two of the big banks now tipping a rate rise and fuel costs still climbing, it's a fair day to run the numbers on anything you're financing before conditions — on site or in the economy — get less forgiving.",
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
