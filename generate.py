#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

replacements = {
    "{{DATE}}": "Wednesday, 30 April 2026",

    # Weather — Carrum Downs 5-day from Wednesday 30 April
    "{{WEATHER_1}}": "Wed 15° Showers",
    "{{WEATHER_2}}": "Thu 13° Rain",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Fri 15° Cloudy",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Sat 17° P/Cloudy",
    "{{WEATHER_5}}": "Sun 18° Sunny",
    "{{WEATHER_ALERT}}": "Rain gear advised",

    # World
    "{{WORLD_1_FLAG}}": "🌍 MIDDLE EAST",
    "{{WORLD_1_HEADLINE}}": "US Dismisses Iran&#8217;s Hormuz Offer as Trump Claims Tehran in &#8220;State of Collapse&#8221;",
    "{{WORLD_1_SUMMARY}}": "Iran has proposed reopening the Strait of Hormuz in exchange for ending the war and lifting the US naval blockade &#8212; without requiring nuclear concessions upfront. The White House is reportedly cool on the deal, and Trump posted Tuesday claiming Iran was in a &#8220;state of collapse,&#8221; as global oil prices hit fresh highs above $140 per barrel.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/4/28/whats-in-irans-latest-proposal-and-how-has-the-us-responded",

    "{{WORLD_2_FLAG}}": "🇺🇸 UNITED STATES",
    "{{WORLD_2_HEADLINE}}": "Federal Reserve Holds Rates Steady for Third Straight Meeting as Powell Chairs His Final Session",
    "{{WORLD_2_SUMMARY}}": "The US Federal Reserve kept its benchmark rate at 3.5&#8211;3.75% at today&#8217;s meeting &#8212; its third consecutive pause &#8212; as Chair Jerome Powell, in what analysts expect to be his final press conference, cited rising energy costs and inflation as reasons to hold. One cut is still pencilled in for 2026, but markets are pricing in fewer.",
    "{{WORLD_2_URL}}": "https://finance.yahoo.com/news/live/fed-meeting-live-updates-federal-reserve-holds-rates-steady-forecasts-1-rate-cut-in-2026-180216872.html",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 FUEL PRICES",
    "{{ECON_1_HEADLINE}}": "ACCC: Diesel Down 15 Cents Since Excise Cut, But Trades Businesses Still Paying Well Above Pre-Crisis Prices",
    "{{ECON_1_SUMMARY}}": "The ACCC&#8217;s weekly fuel monitoring confirms diesel prices have fallen around 15 cents per litre following the government&#8217;s April excise cut &#8212; but at roughly $1.85/litre, costs remain significantly higher than pre-crisis levels. The relief runs to 30 June; if the Strait of Hormuz stays closed beyond that date, prices could bounce back sharply.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🇦🇺 INTEREST RATES",
    "{{ECON_2_HEADLINE}}": "Economists Tip RBA to Hike Rates Again at Tuesday&#8217;s Board Meeting &#8212; More Pressure on Small Business",
    "{{ECON_2_SUMMARY}}": "NAB and Westpac are forecasting a 25 basis point rate hike when the RBA board meets on 5 May, which would push the cash rate to its highest point since 2008. Businesses already stretched by fuel costs may face higher repayments on loans, overdrafts, and vehicle finance just as operating overheads remain elevated.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 OPENAI &#8212; 23 APRIL",
    "{{TECH_1_HEADLINE}}": "OpenAI&#8217;s GPT-5.5 Can Now Run Your Whole Workflow &#8212; Not Just Answer Questions",
    "{{TECH_1_SUMMARY}}": "OpenAI&#8217;s latest model marks a shift from &#8220;AI that answers&#8221; to &#8220;AI that gets things done.&#8221; GPT-5.5 handles multi-step jobs &#8212; browsing the web, writing code, drafting documents, filling spreadsheets, and operating software &#8212; until the task is complete. Priced at roughly half the per-task cost of earlier frontier models, it&#8217;s increasingly accessible for small businesses looking to automate back-office work.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/04/23/openai-chatgpt-gpt-5-5-ai-model-superapp/",

    "{{TECH_2_FLAG}}": "🤖 AI AGENTS &#8212; 22 APRIL",
    "{{TECH_2_HEADLINE}}": "OpenAI and Google Both Launched Business AI Agent Platforms on the Same Day &#8212; The Race Just Accelerated",
    "{{TECH_2_SUMMARY}}": "On 22 April, OpenAI unveiled ChatGPT Workspace Agents and Google launched its Gemini Enterprise Agent Platform within hours of each other. Both systems are designed to autonomously handle entire business workflows &#8212; scheduling, reporting, customer communications &#8212; shifting AI from a tool you query into one that works independently.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 HUMANOID ROBOTS",
    "{{ROBOT_1_HEADLINE}}": "Figure AI&#8217;s Humanoid Robot is Doubling Monthly Deliveries &#8212; 240 Units Shipped in April Alone",
    "{{ROBOT_1_SUMMARY}}": "Figure AI has delivered an estimated 240 of its humanoid factory robots in April 2026 &#8212; double March&#8217;s output and more than the company&#8217;s entire 2025 total. The robots are heading to manufacturing partners for materials handling, assembly, and logistics. The rapid scaling is being cited as evidence that industrial humanoid robotics has crossed from pilots into genuine production deployment.",
    "{{ROBOT_1_URL}}": "https://sg.finance.yahoo.com/news/figure-doubling-humanoid-robot-deliveries-213145204.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Victoria&#8217;s Free Public Transport Ends Today &#8212; But Fares Stay Free Through May, Then Half-Price Until Year&#8217;s End",
    "{{AUS_1_SUMMARY}}": "Today marks the last day of the original free fare period &#8212; and the Victorian government has confirmed trains, trams and buses will remain free throughout May before transitioning to half-price fares for the rest of 2026. The policy, triggered by the fuel price emergency, has been credited with reducing car trips and easing cost-of-living pressure across the state.",
    "{{AUS_1_URL}}": "https://www.melbourning.com.au/2026/04/19/free-public-transport-in-victoria-is-extended-throughout-may-and-will-then-be-half-price-for-rest-of-2026/",

    "{{AUS_2_HEADLINE}}": "EV Sales Nearly Double Year-on-Year as Fuel Shock Drives Australians Towards Electric Vehicles",
    "{{AUS_2_SUMMARY}}": "Electric vehicles accounted for 14.6% of all Australian car sales in March 2026 &#8212; nearly double the rate from March 2025 &#8212; as petrol above $2.30/litre made the economics of EV ownership compelling. Used EV prices have risen 10&#8211;20% and stock is now turning over in weeks rather than months.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne&#8217;s Southbank Underpass to Become 5,000sqm Public Park with Skate Rink and Bouldering Wall",
    "{{VIC_1_SUMMARY}}": "The City of Melbourne has announced plans to transform a long-disused concrete underpass in Southbank into a vibrant 5,000 square metre public space featuring a roller rink, skate park, bouldering wall, and basketball courts. The project is part of the city&#8217;s broader strategy to activate underutilised urban spaces and improve safety and amenity across Melbourne&#8217;s inner city.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ QUANTUM PHYSICS &#8212; JAPAN",
    "{{SCI_1_HEADLINE}}": "Scientists Catch Antimatter &#8220;Atom&#8221; Behaving as a Quantum Wave &#8212; A World First",
    "{{SCI_1_SUMMARY}}": "Researchers from Tokyo University of Science have observed positronium &#8212; an exotic &#8220;atom&#8221; formed by an electron and its antimatter mirror, a positron &#8212; diffract and interfere like a quantum wave. Published 28 April, the breakthrough confirms that matter-antimatter systems obey the same strange quantum laws as ordinary atoms, and opens the door to the first direct tests of how gravity affects antimatter.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Protecting Your Margins When Costs Spike: How AI Pricing Tools Help Tradies Stay Profitable",
    "{{INSIGHT_BODY}}": "With diesel still above $1.85 per litre and another RBA rate hike expected next week, margins on fixed-price contracts are being squeezed from every direction. A growing number of trades businesses are turning to AI-assisted pricing tools &#8212; built into platforms like ServiceM8, Simpro, and Buildxact &#8212; to dynamically factor in current fuel costs, labour rates, and material prices at quoting time, rather than relying on static price lists that are months out of date. The key advantage isn&#8217;t just speed; these tools can flag when a quote is likely to lose money before you submit it, giving you the chance to adjust scope, add a fuel surcharge, or walk away from the job. In a market where every contract needs to cover escalating overheads, getting the numbers right upfront isn&#8217;t a nice-to-have &#8212; it&#8217;s the difference between a busy year and a costly one.",

    # Fun Facts
    "{{FACT_1}}": "Positronium &#8212; the antimatter &#8220;atom&#8221; at the centre of this week&#8217;s quantum physics breakthrough &#8212; has a lifespan of just 142 nanoseconds in its most stable form. That&#8217;s less than two ten-millionths of a second, yet long enough for Japanese researchers to fire it at a sheet of graphene and watch it diffract like a beam of light.",
    "{{FACT_2}}": "Australia&#8217;s National Electricity Market (NEM) spans over 5,000 kilometres from Far North Queensland to South Australia, making it the world&#8217;s longest single synchronous interconnected power system &#8212; a vital but vulnerable piece of national infrastructure in an era of rising energy costs and grid stress.",
    "{{FACT_3}}": "In the first quarter of 2026 alone, global AI investment hit a record $267 billion in venture deal value &#8212; more than double the previous quarterly record. That single quarter&#8217;s AI funding is larger than the entire GDP of New Zealand.",

    # Joke
    "{{JOKE_SETUP}}": "What do you call a plumber who shows up on time, finishes the job, and charges what he quoted?",
    "{{JOKE_PUNCHLINE}}": "A myth.",

    # Closing
    "{{CLOSING_QUOTE}}": "&#8220;The man who moves a mountain begins by carrying away small stones.&#8221;",
    "{{CLOSING_ATTR}}": "&#8212; Confucius",
    "{{CLOSING_MESSAGE}}": "Today is the last day of Victoria&#8217;s free public transport era &#8212; from tomorrow it stays free through May, then halves for the rest of the year. The Fed held steady overnight, which is one less headache, but the RBA clock is ticking toward next Tuesday. It&#8217;s mid-week on the tools. Keep moving.",
}

with open("template.html", "r", encoding="utf-8") as f:
    html = f.read()

for placeholder, value in replacements.items():
    html = html.replace(placeholder, value)

# Verify no placeholders remain
import re
remaining = re.findall(r"\{\{[A-Z_0-9]+\}\}", html)
if remaining:
    print(f"WARNING: Unreplaced placeholders: {remaining}")
else:
    print("All placeholders replaced successfully.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html written successfully.")
