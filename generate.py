#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 16 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 16 Jul (BOM)
    "{{WEATHER_1}}": "THU 16 · ☁️ Cloudy, slight shower · 6–14°C",
    "{{WEATHER_2}}": "FRI 17 · 🌧️➡️☀️ Showers early, clearing · 5–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 18 · 🌫️☀️ Morning fog, sunny · 8–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SUN 19 · ❄️☀️ Frosty start, mostly sunny · 8–15°C",
    "{{WEATHER_5}}": "MON 20 · ❄️🌤️ Frosty patches, breezy · 9–15°C",
    "{{WEATHER_ALERT}}": "⚠ FROST & FOG RETURNING SAT–MON MORNINGS · NO SEVERE WARNINGS ACTIVE",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷⚓ STRAIT OF HORMUZ · US STRIKES IRAN AGAIN · NAVAL BLOCKADE REINSTATED",
    "{{WORLD_1_HEADLINE}}": "US Launches Fresh Strikes on Iran as Strait of Hormuz Standoff Escalates",
    "{{WORLD_1_SUMMARY}}": "US forces carried out a fresh, roughly 90-minute wave of strikes on Iranian military targets near the Strait of Hormuz overnight, with CENTCOM saying the goal is to stop Iran threatening tankers transiting the strait. Iran says at least seven of its troops were killed and 260 people wounded, and its foreign ministry insists there are 'no plans for negotiations.' The US has also reimposed a naval blockade of Iranian ports, with daily tanker traffic through the strait down to a handful of vessels from the usual 18-22.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/liveblog/2026/7/15/live-trump-says-strikes-on-iran-will-continue-until-i-say",

    "{{WORLD_2_FLAG}}": "🇨🇩🏥 DR CONGO · EBOLA OUTBREAK TOPS 700 DEATHS · OUTPACING CONTACT TRACING",
    "{{WORLD_2_HEADLINE}}": "Ebola Outbreak in Eastern Congo Passes 700 Deaths as It Outruns Contact Tracing",
    "{{WORLD_2_SUMMARY}}": "Confirmed deaths from the Bundibugyo strain of Ebola in the Democratic Republic of Congo have passed 700, with more than 1,900 people infected across three provinces since the outbreak was first detected in May. The WHO says 80% of new cases can't be traced back to a known chain of transmission, and many victims are dying in their communities without ever reaching a clinic — there's still no approved vaccine or treatment for this particular strain.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/07/15/g-s1-133630/ebola-congo-deaths",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ OIL SHOCK · BRENT TOPS US$85 · GULF EXPORTS CUT ROUGHLY IN HALF",
    "{{ECON_1_HEADLINE}}": "Oil Surges Past US$85 a Barrel as Iran Conflict Threatens a Fresh Bowser Hit",
    "{{ECON_1_SUMMARY}}": "Brent crude climbed above $85 a barrel overnight, its third straight day of gains, after the latest US strikes on Iran and the reinstated naval blockade near the Strait of Hormuz. Gulf oil exports have fallen to roughly half their normal volume over the past week, and Goldman Sachs has floated Brent topping $110 by the fourth quarter if the disruption drags on — worth watching closely given how quickly bowser prices have already moved this year.",
    "{{ECON_1_URL}}": "https://www.cnbc.com/2026/07/15/oil-prices-today-brent-wti-hormuz-blockade.html",

    "{{ECON_2_FLAG}}": "📊 SENTIMENT · CONSUMER CONFIDENCE UP 4.1% · RELIEF MAY BE SHORT-LIVED",
    "{{ECON_2_HEADLINE}}": "Consumer Sentiment Lifts as Fuel Prices Ease — Just Before the Latest Oil Spike",
    "{{ECON_2_SUMMARY}}": "The Westpac-Melbourne Institute Consumer Sentiment Index jumped 4.1% to 83.9 in July, though it remains in the bottom 10% of readings in the survey's 50-year history. The lift was driven largely by relief at the bowser, with average pump prices easing to around $1.60 a litre during the survey week — before the fresh Middle East-driven oil spike above hit, which suggests any confidence gains could prove short-lived.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🇨🇳🤖 REGULATION · CHINA'S NEW AI LAW · HUMANLIKE CHATBOTS PULLED",
    "{{TECH_1_HEADLINE}}": "China's New AI Companion Law Forces ByteDance and Alibaba to Shut Down Humanlike Chatbots",
    "{{TECH_1_SUMMARY}}": "China's first dedicated rules for AI services that simulate human personality and emotional connection took effect today, and ByteDance's Doubao and Alibaba's Qwen have already disabled their custom companion-agent features to comply, following Tencent's Yuanbao two weeks ago. The rules require anti-addiction systems, age verification for under-14s and an always-available exit option — a preview of the kind of AI chatbot regulation now being debated in the US and Australia.",
    "{{TECH_1_URL}}": "https://www.techtimes.com/articles/320525/20260715/china-ai-companion-law-takes-effect-doubao-qwen-shut-down-millions-lose-chat-data.htm",

    "{{TECH_2_FLAG}}": "🎨 SOFTWARE · CANVA CODE 2.0 · FREE AI WEBSITE BUILDER FOR EVERYONE",
    "{{TECH_2_HEADLINE}}": "Canva Launches Code 2.0, Giving Every User — Even Free Accounts — an AI Website Builder",
    "{{TECH_2_SUMMARY}}": "Canva has rolled out Code 2.0, letting any of its 265 million monthly users build a working website or app from a plain-language prompt, including everyone on the free tier. Unlike code-first rivals, Canva is betting the real bottleneck for small businesses isn't generating code but making the result look professional — you can drag in your own photos and branding and tweak it without touching a line of code.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🐕🤖 LOGISTICS · BOSTON DYNAMICS · SPOT TAKES ON THE 'PORCH GAP'",
    "{{ROBOT_1_HEADLINE}}": "Boston Dynamics Trials Its Spot Robot for Last-Mile Doorstep Deliveries",
    "{{ROBOT_1_SUMMARY}}": "Boston Dynamics is piloting a new job for its robot dog Spot — solving what it calls the 'porch gap,' the last stretch of a delivery where drivers lose time and strain their bodies navigating stairs, gravel and curbs. A driver loads parcels onto a rig on Spot's back, and the robot walks itself up to the door and back to the van, with Boston Dynamics already talking to logistics companies about scaling it up to around 200 packages a day per driver-robot team.",
    "{{ROBOT_1_URL}}": "https://bostondynamics.com/blog/bridging-the-porch-gap/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Labor Pitches Housing Tax Reform to Young Australians Locked Out of the Market",
    "{{AUS_1_SUMMARY}}": "Treasurer Jim Chalmers, PM Anthony Albanese and Finance Minister Katy Gallagher have put out a pitch aimed squarely at young Australians shut out of the housing market, flagging changes to capital gains tax discounts and negative gearing on investment properties. The government argues these investor tax breaks have given property investors an unfair edge over first-home buyers, and is framing the move as 'levelling the playing field' ahead of budget changes.",
    "{{AUS_1_URL}}": "https://www.newcastleherald.com.au/story/9244354/last-minute-budget-pitch-to-level-field-for-young/",

    "{{AUS_2_HEADLINE}}": "Fortescue Ordered to Pay Yindjibarndi People $150 Million in Landmark Native Title Case",
    "{{AUS_2_SUMMARY}}": "The Federal Court has finalised orders requiring mining giant Fortescue to pay roughly $150.3 million to the Yindjibarndi Aboriginal Corporation for mining on their WA Pilbara land since 2012 — the largest native title compensation order in Australian history. The orders cover four open-pit mines, a railway and waste dumps spread across more than 135 square kilometres of Yindjibarndi country, with the community noting it's still well short of the roughly $1.8 billion originally sought.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Liberal MP Moira Deeming Withdraws Court Case Over Disendorsement Push",
    "{{VIC_1_SUMMARY}}": "Upper house Liberal MP Moira Deeming has withdrawn the Supreme Court injunction she'd taken out to delay her party's push to disendorse her, after submitting a formal statement and mediation proposal to the party's State Executive. The dispute traces back to her allegation that former Victorian Liberal leader Matthew Guy put her in a headlock in May, which Victoria Police found no CCTV evidence for — the party's move to strip her preselection for November's state election is still live.",

    # Science
    "{{SCI_1_FLAG}}": "🔭 ASTRONOMY · HIDDEN DEAD STARS · FOUR WHITE DWARFS UNMASKED NEXT DOOR",
    "{{SCI_1_HEADLINE}}": "Astronomers Find Four 'Invisible' Dead Stars Hiding in Our Cosmic Backyard",
    "{{SCI_1_SUMMARY}}": "Using Hubble's ultraviolet vision, astronomers have unmasked four white dwarfs — the dense, burnt-out cores of long-dead stars — hiding in plain sight next to brighter companion stars, including one just 25 light-years from Earth that took nearly three decades to confirm. The trick was watching the brighter star wobble as an unseen object tugged it back and forth, then using UV light to fish the much fainter white dwarf's glow out of the glare — all four sit within 65 light-years of us, hinting our stellar neighbourhood may be hiding plenty more.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Website Doesn't Need a Developer Anymore — Canva's New AI Builder Proves It",
    "{{INSIGHT_BODY}}": "Canva just rolled out Code 2.0, letting any of its 265 million users type a plain-language prompt and get a working website or app — including everyone on the free tier, not just paying subscribers. For a trades business that's been putting off a proper website, or paying a developer a few hundred dollars for basic changes, this closes that gap: drag in your own job photos and branding, tweak the layout, and publish without touching a line of code. It won't replace a serious custom build, but for a one-page quote-and-contact site or a landing page for a new service line, it might be the cheapest 20 minutes you spend on the business this month.",

    # Fun Facts
    "{{FACT_1}}": "Corrosion quietly costs the global economy an estimated US$2.5 trillion a year — more than 3% of world GDP — and industry bodies estimate 15-20% of that could be prevented with coatings and protective treatments that already exist today.",

    "{{FACT_2}}": "Sega picked blue for Sonic the Hedgehog specifically because it matched the company's own logo, and chose a hedgehog because its spiky defence read as 'attitude' next to Nintendo's plumber.",

    "{{FACT_3}}": "A bottle of champagne holds roughly three times the pressure of a car tyre — about 90 psi — which is why an improperly aimed cork can travel more than 20 metres at speeds close to 50 km/h.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the handyman start bringing two toolboxes to every job?",
    "{{JOKE_PUNCHLINE}}": "One for the tools, one for all the 'quick, five-minute' favours that always turn into a full afternoon.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Do not be embarrassed by your failures, learn from them and start again.\"",
    "{{CLOSING_ATTR}}": "— Richard Branson",
    "{{CLOSING_MESSAGE}}": "It's a cool, mostly cloudy Thursday in Carrum Downs, 6-14°C with just a slim chance of a shower — dry enough to get outside work done before frostier mornings roll in over the weekend. Oil's back above US$85 a barrel overnight as the Iran standoff escalates, so if fuel felt a touch cheaper this week, don't bank on that lasting — worth another look at your surcharge line before it bites again.",
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
