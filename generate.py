#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 02 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 2 Sep (BOM)
    "{{WEATHER_1}}": "WED 2 SEP · 🌦️ Shower or two easing by late morning, breezy nor'wester · 12–18°C",
    "{{WEATHER_2}}": "THU 3 SEP · 🌧️ Cloudy, high chance of showers morning and arvo, blustery nor'wester · 10–17°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 4 SEP · 🌧️ Partly cloudy, very high chance of showers later in the day · 11–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 5 SEP · ⛅ Partly cloudy, high chance of a shower · 8–18°C",
    "{{WEATHER_5}}": "SUN 6 SEP · ☁️ Cloudy, medium chance of a shower later in the day · 13–17°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula — a damaging winds warning covers the alpine ranges only. Expect a showery, blustery run through the week before it eases into a cloudier, calmer weekend.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 STRAIT OF HORMUZ · TRUMP VOWS TO 'HIT' IRAN HARDER AFTER FRESH CLASHES",
    "{{WORLD_1_HEADLINE}}": "Trump Warns Iran of a 'Much Harder' Strike as US-Iran Clashes Resume Near the Strait of Hormuz",
    "{{WORLD_1_SUMMARY}}": "US Central Command struck Iranian minelaying forces near the Strait of Hormuz over the weekend, and Iran's Revolutionary Guard retaliated with missile strikes on US bases in Jordan, which said it intercepted at least eight of them; Trump warned Monday that Iran would be hit 'at a much harder and higher level' if it strikes again, rattling oil markets already on edge over the shipping chokepoint.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/9/1/hit-them-hard-does-trump-have-another-new-iran-strategy-can-it-work",

    "{{WORLD_2_FLAG}}": "🌏 BISHKEK · SCO SUMMIT WRAPS WITH NEW TRADE AND LOGISTICS PACT",
    "{{WORLD_2_HEADLINE}}": "Shanghai Cooperation Organisation Summit Closes With 13 New Agreements, Including a Five-Year Logistics Plan",
    "{{WORLD_2_SUMMARY}}": "Leaders from China, Russia, India, Pakistan and Central Asian states wrapped the 26th SCO summit in Bishkek with the 'Bishkek Declaration' and 13 outcome agreements, including a 2026–2030 plan to build out regional ports and logistics hubs and the adoption of English as an official SCO language, as the bloc's chairmanship passes to Pakistan.",
    "{{WORLD_2_URL}}": "https://aninews.in/news/world/asia/sco-summit-yields-13-outcome-agreements-spanning-counter-terrorism-climate-action-and-digital-cooperation20260901180249/",

    # Economics
    "{{ECON_1_FLAG}}": "📉 ASX · OIL SURGE ON US-IRAN TENSIONS WEIGHS ON TECH STOCKS",
    "{{ECON_1_HEADLINE}}": "ASX Edges Lower as Renewed US-Iran Conflict Sends Oil Above US$91 a Barrel",
    "{{ECON_1_SUMMARY}}": "The ASX 200 closed down about 0.1% at 9,066 points on Tuesday, with energy stocks the standout gainer (+1.2%) while tech and consumer discretionary shares dropped 1.4–1.7%, as Brent crude climbed above US$91 a barrel on fears the US-Iran clashes near the Strait of Hormuz could disrupt Middle East oil supply.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-09-01/asx-markets-business-live-news-house-prices-fall/107100764",

    "{{ECON_2_FLAG}}": "⛽ FUEL · MELBOURNE BOWSER PRICES CLIMBING AS OIL SURGES",
    "{{ECON_2_HEADLINE}}": "Melbourne Petrol Heads Into the Rising Leg of the Cycle Just as Oil Jumps on Middle East Tensions",
    "{{ECON_2_SUMMARY}}": "Victoria's average unleaded price sat at 196.8 cents a litre on Tuesday (national average 205.3 cents, diesel 253.3 cents), with Melbourne now in the rising leg of its local price cycle — a climb likely to get a further push from Brent crude's jump above US$91 a barrel on the fresh US-Iran clashes.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🛒 SCAMS · ACCC WARNS AI IS SUPERCHARGING FAKE ONLINE STORES",
    "{{TECH_1_HEADLINE}}": "ACCC Warns Generative AI Is Making Fake 'Ghost Store' Scams Impersonating Real Businesses Harder to Spot",
    "{{TECH_1_SUMMARY}}": "The ACCC says scammers are now using generative AI to spin up professional-looking fake online stores in minutes — complete with AI-generated product photos, descriptions and fake reviews — often impersonating real Australian businesses, warning shoppers 'can no longer rely on appearance alone.' Worth knowing if your business has a website or social presence someone could convincingly clone.",
    "{{TECH_1_URL}}": "https://www.smartcompany.com.au/artificial-intelligence/accc-warns-ai-ghost-stores-online-shopping/",

    "{{TECH_2_FLAG}}": "📊 AI ADOPTION · TREASURY SAYS AUSSIE BUSINESS AI USE IS 'WIDE BUT SHALLOW'",
    "{{TECH_2_HEADLINE}}": "Treasury Warns Australian Businesses' AI Adoption Is 'Widespread But Shallow'",
    "{{TECH_2_SUMMARY}}": "Advice to Treasurer Jim Chalmers found roughly two-thirds of Australian businesses report some AI use, but fewer than one in ten report 'significant' adoption — meaning the economy risks missing AI's productivity upside unless businesses move past basic chatbot use into real operational change.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🐕 PHYSICAL AI · US HOMELAND SECURITY EYES ROBOT DOGS FOR HAZARD WORK",
    "{{ROBOT_1_HEADLINE}}": "US Homeland Security Plans to Buy Boston Dynamics' Spot Robots for Hazardous-Site Inspection",
    "{{ROBOT_1_SUMMARY}}": "A Department of Homeland Security funding document shows US authorities want to spend up to $2 million on Boston Dynamics' four-legged Spot robots, fitted with cameras and hazardous-gas sensors, for remote inspection and hazard assessment in high-risk environments rather than direct enforcement — with a formal tender expected around 4 September.",
    "{{ROBOT_1_URL}}": "https://www.wbur.org/news/2026/08/31/ice-robot-dogs-immigration-enforcement-boston-dynamics",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australian Government Bond Yields Hit a 15-Year High Amid Global Debt Sell-Off",
    "{{AUS_1_SUMMARY}}": "The yield on Australia's benchmark 10-year government bond jumped as much as 10 basis points to 5.19% on Tuesday, its highest level since July 2011, as a deepening global bond sell-off on inflation fears pushed yields higher in Japan, Britain and the US in tandem.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-09-01/australian-government-10-year-bond-hits-15-year-high/107103096",

    "{{AUS_2_HEADLINE}}": "Missing Australian Found Alive Six Days After Deadly Nepal-Tibet Border Floods",
    "{{AUS_2_SUMMARY}}": "One of 43 Australians reported missing after the catastrophic Nepal-Tibet border floods has been found alive in Tibet, with DFAT confirming contact on Tuesday morning — the second Australian located safe in recent days, bringing the number still missing down to 42.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne's First 'Kindred People' Festival Opens Today, Putting First Nations Culture Centre Stage",
    "{{VIC_1_SUMMARY}}": "A new Indigenous-led festival of First Nations arts, culture and knowledge kicks off today across Monash University's campuses, running through Sunday with music, theatre, dance and a dedicated two-day knowledge-sharing program — organisers hope it becomes a biennial fixture on Melbourne's cultural calendar.",

    # Science
    "{{SCI_1_FLAG}}": "🚀 SPACE STATION · SIXTH-EVER ALL-FEMALE SPACEWALK COMPLETED",
    "{{SCI_1_HEADLINE}}": "NASA and ESA Astronauts Complete Only the Sixth All-Female Spacewalk in History",
    "{{SCI_1_SUMMARY}}": "NASA's Jessica Meir and ESA's Sophie Adenot spent about 6.5 hours outside the International Space Station on Tuesday, replacing a docking-navigation mirror on the Harmony module, running cable and camera swaps, and prepping the Alpha Magnetic Spectrometer for future maintenance — Meir's seventh career spacewalk, moving her into third place all-time among NASA women spacewalkers.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Government Bond Yields Just Hit a 15-Year High — Here's What It Means If You're Financing a Ute or a Compressor",
    "{{INSIGHT_BODY}}": "Australia's benchmark 10-year bond yield jumped to 5.19% on Tuesday, its highest level since 2011, as a global bond sell-off on inflation fears pushes borrowing costs up in lockstep from Tokyo to London. Bond yields aren't your equipment loan rate, but they're the base rate lenders build on — when they climb this fast, business finance and lease rates tend to follow within weeks, not months. If you've been putting off financing a new compressor, blast pot or ute, it's worth getting a quote locked in now rather than waiting for a 'better time' that a global bond sell-off is currently working against. Worth a call to your broker this week rather than next.",

    # Fun facts
    "{{FACT_1}}": "The retractable, spring-return tape measure was patented in 1868 by Connecticut clockmaker Alvin J. Fellows, who adapted a clock-spring mechanism into a pocket-sized metal case, replacing the folding wooden rulers tradesmen had carried for generations.",
    "{{FACT_2}}": "Space Invaders was such a hit in Japan after its 1978 release that arcades reportedly drained the country's supply of 100-yen coins, prompting the Japanese Mint to roughly quadruple production of the coin that year.",
    "{{FACT_3}}": "The word 'salary' traces back to the Latin salarium, the allowance Roman soldiers were paid partly to cover salt — one of the ancient world's most valuable commodities, prized for preserving food long before refrigeration existed.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pest controller's small business always have healthy cash flow?",
    "{{JOKE_PUNCHLINE}}": "Because he never let a late payment nest for long.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The secret of getting ahead is getting started.\"",
    "{{CLOSING_ATTR}}": "— Mark Twain",
    "{{CLOSING_MESSAGE}}": "It's hump day in Carrum Downs, with a shower or two easing off by late morning before a breezy nor'wester takes over — a decent window to get outdoor jobs done early. Over in Melbourne's south-east, the inaugural Kindred People festival kicks off today at Monash, a bit of good local news in a week otherwise dominated by rising bond yields and climbing bowser prices.",
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
