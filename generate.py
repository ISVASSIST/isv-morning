#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 03 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 03 Aug (BOM)
    "{{WEATHER_1}}": "MON 03 · 🌧️ Showers, easing this evening · 8–15°C",
    "{{WEATHER_2}}": "TUE 04 · 🌧️ Showers, most likely SE suburbs · 5–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 05 · 🌦️ Isolated shower, chance easing · 6–13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 06 · 🌦️ Shower or two, morning/arvo · 6–13°C",
    "{{WEATHER_5}}": "FRI 07 · ⛅ Partly cloudy, drier · 6–14°C",
    "{{WEATHER_ALERT}}": "⚠ SEVERE WEATHER WARNING CURRENT FOR DAMAGING WINDS · GIPPSLAND, ALPINE & SW VIC (NOT METRO MELBOURNE)",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇱🇵🇸 GAZA · ISRAELI STRIKES KILL NINE DESPITE HAMAS SIGNING ONTO US-BACKED DISARMAMENT DEAL",
    "{{WORLD_1_HEADLINE}}": "Israeli Strikes Kill Nine in Gaza as a Senior Minister Vows Attacks Won't Stop Despite Hamas's Disarmament Deal",
    "{{WORLD_1_SUMMARY}}": "A senior Israeli minister says strikes on Gaza will continue even after Hamas signed onto a US-backed disarmament plan brokered through Trump's Board of Peace, with Sunday's strikes on Gaza City, Deir al-Balah and Khan Younis marking the deadliest day there in weeks. It's a reminder that a signed deal on paper doesn't automatically mean the fighting stops on the ground.",
    "{{WORLD_1_URL}}": "https://www.timesofisrael.com/senior-minister-says-israel-not-halting-attacks-in-gaza-as-9-said-killed-in-idf-strikes",

    "{{WORLD_2_FLAG}}": "🇮🇷🇺🇸 IRAN · TRUMP SAYS HE'S CALLING OFF A PLANNED STRIKE, CITING 'RAPID' PROGRESS TOWARD A DEAL",
    "{{WORLD_2_HEADLINE}}": "Trump Says He's Cancelling a Planned Strike on Iran, Citing Rapid Progress Toward a Deal",
    "{{WORLD_2_SUMMARY}}": "President Trump said he's calling off a planned attack on Iran contingent on both sides 'rapidly' reaching an agreement, pointing to progress on reopening the Strait of Hormuz after days of threatening fresh strikes. A step back from the brink is good news for oil markets generally, given roughly a fifth of the world's traded oil passes through that strait.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/08/02/world/live-news/iran-war-trump",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺⛽ FUEL · EXCISE DISCOUNT HAS OFFICIALLY ENDED TODAY · PETROL AND DIESEL BOTH RISING NATIONWIDE",
    "{{ECON_1_HEADLINE}}": "The Fuel Excise Discount Has Officially Ended Today, With Petrol and Diesel Prices Rising Nationwide",
    "{{ECON_1_SUMMARY}}": "From today the remaining fuel excise discount is gone and the excise rate itself has risen to 53.7 cents a litre with an added CPI-linked adjustment on top, pushing unleaded up by as much as 16 cents a litre on a price that had already climbed more than 34 cents a litre since June. Diesel was already averaging around 231 cents a litre before today's change, so it's worth shopping around for the cheapest servo near your sites this week.",
    "{{ECON_1_URL}}": "https://www.indexbox.io/blog/accc-fuel-report-prices-rise-as-fuel-excise-cut-expires/",

    "{{ECON_2_FLAG}}": "🇦🇺🏦 INTEREST RATES · ALL FOUR MAJOR BANKS NOW EXPECT THE RBA TO HOLD RATES STEADY THIS MONTH",
    "{{ECON_2_HEADLINE}}": "All Four Major Banks Now Agree the RBA Will Hold Interest Rates Steady at Its August Meeting",
    "{{ECON_2_SUMMARY}}": "With the RBA's next call due August 11, Westpac has joined CommBank, NAB and ANZ in expecting the cash rate to stay on hold, with most economists now pushing any further relief out to 2027. If you've been banking on a rate cut to ease loan repayments on the ute or plant finance, it's worth planning as if that relief isn't coming this year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🇪🇺🤖 AI REGULATION · EU TRANSPARENCY RULES FOR AI SYSTEMS OFFICIALLY START TODAY",
    "{{TECH_1_HEADLINE}}": "New EU Rules Requiring AI Systems to Disclose Themselves to Users Officially Start Today",
    "{{TECH_1_SUMMARY}}": "From today, the European Commission's AI Act transparency obligations require chatbots to identify themselves as AI, deepfakes to be labelled, and AI-generated content to carry machine-readable marks, with fines of up to €15 million for non-compliance. It doesn't apply directly to an Australian trades business, but it's a clear signal of where AI disclosure expectations are heading globally — worth getting ahead of before a client asks.",
    "{{TECH_1_URL}}": "https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august",

    "{{TECH_2_FLAG}}": "🎥 AI TOOLS · GOOGLE GIVING AWAY 10 FREE AI-GENERATED VIDEOS IN GEMINI — OFFER ENDS TOMORROW",
    "{{TECH_2_HEADLINE}}": "Google Is Giving Away 10 Free AI-Generated Videos Through Gemini, but the Offer Ends Tomorrow",
    "{{TECH_2_SUMMARY}}": "Gemini users without a paid Google AI plan can generate, edit and remix up to ten videos at no cost using Gemini's Veo-powered 'Omni' tool until 11:59pm PT tomorrow, August 4. It's a genuinely free way to knock out a few before/after job clips or a quick social post for the business before the trial window closes.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · TEXAS STARTUP PERSONA AI SHARES REAL WELDING TEST FOOTAGE FOR ITS SHIPYARD HUMANOID",
    "{{ROBOT_1_HEADLINE}}": "Persona AI Shares Real-World Welding Test Footage From Its Heavy-Duty Shipyard Humanoid Robot",
    "{{ROBOT_1_SUMMARY}}": "Houston-based Persona AI has released footage of its Gen 1 humanoid being teleoperated through a genuine welding job in an industrial fabrication shop, part of the data-gathering push behind its HD Hyundai shipyard deployment and a steel-fabrication pilot in Louisiana. It's a reminder that a lot of the humanoid robotics push is now landing squarely in heavy industry — welding, grinding and structural fabrication — the exact kind of physical trade work AI was supposed to leave alone the longest.",
    "{{ROBOT_1_URL}}": "https://mikekalil.com/blog/persona-ai-humanoid-robot-welder/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Census Night Is Just Over a Week Away, With Every Person in Australia Counted on 11 August",
    "{{AUS_1_SUMMARY}}": "The 2026 Census falls on Tuesday 11 August, with around 30,000 ABS field staff deployed to make sure everyone — including people experiencing homelessness or in hospital — gets counted, and login letters landing in letterboxes now. This year's count is also the first to ask Australians aged 16 and over about sexual orientation and gender, and allows up to four ancestries to be listed instead of two.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/census-2026-guide-when-is-census-night-and-everything-you-need-to-know/7grekdcbf",

    "{{AUS_2_HEADLINE}}": "One in Five Australians Are Now Delaying a Doctor's Visit Purely Because of Cost, New Report Finds",
    "{{AUS_2_SUMMARY}}": "Finder's 2026 Health Report found one in five Australians are putting off GP visits due to cost, with dental, physio and preventative scans among the first things people cut, and 1.5 million Australians now cancelling private health cover altogether. A sobering number worth keeping in mind if you're weighing up staff health benefits or just your own next check-up.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne's West Gets Its First New Tram in Over a Decade as the City's $1.85 Billion Fleet Overhaul Begins",
    "{{VIC_1_SUMMARY}}": "The first of 100 new Dandenong-built G Class trams has rolled into the newly opened Maidstone Tram Depot, carrying roughly double the passengers of the old fleet and marking the start of Victoria's biggest tram rollout in years. Good news if any of your crews rely on the tram network to get between city-fringe jobs.",

    # Science
    "{{SCI_1_FLAG}}": "🥩 NUTRITION SCIENCE · MAJOR REVIEW OF 350+ STUDIES FINDS EATING LESS PROTEIN MAY ACTUALLY SLOW AGING",
    "{{SCI_1_HEADLINE}}": "A Major Review of More Than 350 Studies Finds Eating Less Protein Could Slow Aging, Not Speed It Up",
    "{{SCI_1_SUMMARY}}": "A sweeping Cell Press review published this month found current high-protein guidance may be overselling what most people actually need, with the ideal intake depending heavily on age and activity level rather than a single blanket number. Handy context next time a supplement ad tells you more protein is automatically better.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The EU Just Made AI Disclosure Compulsory — Should Your Quotes Say When AI Helped Write Them?",
    "{{INSIGHT_BODY}}": "From today, new European rules require businesses to tell customers when they're dealing with an AI system or AI-generated content — a rule that doesn't apply directly to a Carrum Downs trades business, but points at where client expectations are heading. If you're using AI to draft quotes, follow-up emails or job reports, a simple line like 'drafted with AI assistance, reviewed by [name]' costs nothing and can actually build trust rather than undermine it — most clients care less that AI was involved and more that a human checked the numbers before it landed in their inbox. Worth building into your templates now, before a client asks first.",

    # Fun facts
    "{{FACT_1}}": "The 'black box' flight recorder fitted to every commercial aircraft today was invented by an Australian, David Warren, working at Melbourne's Aeronautical Research Laboratories in the 1950s — partly driven by the loss of his own father in a 1934 plane crash. The real units are painted bright orange, not black, purely so wreckage search teams can actually spot them.",
    "{{FACT_2}}": "Ned Kelly's famous suit of armour wasn't custom-forged steel plate — bush blacksmiths hammered it together from stolen plough mouldboards in 1880, and the finished set weighed around 44 kilograms. It stopped dozens of police bullets at Glenrowan, but Kelly's unprotected legs were what finally brought him down.",
    "{{FACT_3}}": "The 'flat white' — one of Australia's biggest coffee exports — has a genuinely disputed birthplace between Sydney and Wellington, but one of the earliest documented menu listings was at Sydney's Moors Espresso Bar back in 1985, decades before the drink caught on in London and New York.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the line marking contractor's small business never run over budget?",
    "{{JOKE_PUNCHLINE}}": "He'd already drawn the line on what he was prepared to spend.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Strive not to be a success, but rather to be of value.\"",
    "{{CLOSING_ATTR}}": "— Albert Einstein",
    "{{CLOSING_MESSAGE}}": "It's a showery start to the week in Carrum Downs, with today's rain expected to ease by this evening before a cooler, drier stretch moves in — a good excuse to keep indoor jobs on the board this morning. Fuel officially got more expensive nationwide from today with the excise discount gone, so budget for it on your next tank if you didn't fill up over the weekend. And keep an eye on the Middle East this week — Trump's talk of calling off a strike on Iran is a good sign for oil prices staying steady rather than spiking.",
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
