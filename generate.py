#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 07 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 07 Aug (BOM)
    "{{WEATHER_1}}": "FRI 07 · 🌦️ Windy, showers likely later · 8–15°C",
    "{{WEATHER_2}}": "SAT 08 · 🌧️ High chance of showers, wetter in the hills · 8–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 09 · 🌬️ Windy with a shower or two · 9–16°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 10 · ⛅ Partly cloudy, drier stretch · 7–15°C",
    "{{WEATHER_5}}": "TUE 11 · ☀️ Mostly sunny, cooler start · 6–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings current for Melbourne / Carrum Downs",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦🇷🇺 UKRAINE · RUSSIAN BARRAGE KILLS 17 IN KYIV REGION, NO MISSILES INTERCEPTED",
    "{{WORLD_1_HEADLINE}}": "Russian Missile and Drone Barrage Kills 17 in Kyiv Region as Air Defences Come Up Empty",
    "{{WORLD_1_SUMMARY}}": "A huge overnight barrage of 24 ballistic missiles, four Zircon/Onyx missiles and 115 drones hit Kyiv and its surrounding region, killing 17 and wounding 44 — Ukraine's air force says none of the missiles were intercepted, with warehouses, a brewery and a rail station among the targets. President Zelenskyy says allies have supplied only a third of the promised Patriot interceptors this year, keeping the war's energy and shipping risk elevated for anyone watching global fuel costs.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/08/05/europe/russia-ukraine-kyiv-attack-intl-hnk",

    "{{WORLD_2_FLAG}}": "🇮🇱🇵🇸 GAZA · ISRAEL REJECTS KEY TERMS OF TRUMP-BACKED HAMAS DISARMAMENT PLAN",
    "{{WORLD_2_HEADLINE}}": "Israel Pushes Back on Trump's Hamas Disarmament Plan as Gaza Ceasefire Wobbles",
    "{{WORLD_2_SUMMARY}}": "Days after Trump's 15-point disarmament roadmap was unveiled, Israel has told the White House it has 'serious security concerns,' judging Hamas intends to store rather than surrender its weapons — while Hamas insists it never agreed to full disarmament. It's the latest sign the ceasefire remains fragile, with no resolution yet in sight.",
    "{{WORLD_2_URL}}": "https://foreignpolicy.com/2026/08/06/hamas-disarmament-deal-netanyahu-israel-gaza/",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺⛽ FUEL · CAPITAL CITY PRICES UP 42.1C/L AS EXCISE CUT ENDS, ACCC WARNS OF $100M FINES",
    "{{ECON_1_HEADLINE}}": "Capital City Fuel Prices Jump 42.1 Cents a Litre as the ACCC Puts Servos on Notice",
    "{{ECON_1_SUMMARY}}": "With excise relief fully wound back from 3 August, the ACCC's latest monitoring shows capital city pump prices up 42.1c/L, and Treasurer Jim Chalmers has asked the regulator to watch retailers closely — servos and suppliers now face fines up to $100 million per offence for price gouging. Worth comparing a couple of servos near your sites this week rather than assuming yesterday's cheapest is still today's.",
    "{{ECON_1_URL}}": "https://www.indexbox.io/blog/accc-fuel-report-prices-rise-as-fuel-excise-cut-expires/",

    "{{ECON_2_FLAG}}": "🇦🇺🏦 RATES · RBA'S BIG AUGUST CALL LANDS TUESDAY, HOLD AT 4.35% THE FIRM FAVOURITE",
    "{{ECON_2_HEADLINE}}": "All Four Big Banks Expect the RBA to Hold at 4.35% Next Tuesday — But It's Not a Sure Thing",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank's rate call lands Tuesday 11 August alongside its full quarterly forecasts, and CBA, NAB, ANZ and Westpac all expect a hold after June's inflation came in softer than expected — though markets still price a 20–30% chance of a surprise hike. Worth holding off on any big loan or equipment finance decisions until the dust settles early next week.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI TOOLS · META LAUNCHES 'MUSE CODE' TO TAKE ON CLAUDE CODE AND OPENAI CODEX",
    "{{TECH_1_HEADLINE}}": "Meta Launches Muse Code, a Terminal AI Agent Built to Handle Whole Codebases",
    "{{TECH_1_SUMMARY}}": "Meta's new Muse Code agent can plan, write and validate code changes across large repositories in one sitting, launching in beta with a pay-as-you-go tier and a cheaper 'contributor' tier for developers who let Meta train on their data. It's another sign the AI coding-agent race is now a genuine three-way fight between Meta, Anthropic and OpenAI — good news for anyone hoping today's AI tool prices keep falling.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/08/05/meta-launches-muse-code-an-ai-agent-for-large-code-bases/",

    "{{TECH_2_FLAG}}": "💻 HARDWARE · AI-DRIVEN MEMORY CHIP SHORTAGE IS PUSHING UP PC AND LAPTOP PRICES",
    "{{TECH_2_HEADLINE}}": "AI Data Centres Are Eating So Much Memory That HP, Asus and Acer Are Turning to Chinese Chips",
    "{{TECH_2_SUMMARY}}": "AI data-centre buildouts are set to consume 70% of the world's memory chip production this year, tripling DRAM costs in 18 months and pushing memory to 40–60% of a PC's total cost — forcing HP, Asus and Acer to start using Chinese CXMT chips in some models sold outside the US. If a work laptop or tablet is due for replacement, it's worth budgeting for a higher price tag than last time.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳🦾 ROBOTICS · UNITREE PRICES ITS $904M SHANGHAI IPO, DEEPSEEK TAKES A STAKE",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robot Maker Unitree Prices Its $904 Million Shanghai IPO as DeepSeek Takes a Stake",
    "{{ROBOT_1_SUMMARY}}": "Unitree priced its STAR Market listing at 150.80 yuan a share, raising about $904 million in what will be mainland China's first publicly traded humanoid robot maker — with AI startup DeepSeek buying a 2.31% stake and agreeing to jointly develop AI models for the robots. Another marker of humanoid robotics shifting from prototype hype into real, capital-market-priced mass production.",
    "{{ROBOT_1_URL}}": "https://www.bloomberg.com/news/articles/2026-08-06/china-s-unitree-seeks-904-million-in-first-mainland-robotic-ipo",

    # Australia
    "{{AUS_1_HEADLINE}}": "Royal Commission Into Antisemitism Opens Its Eighth Hearing Block in Sydney",
    "{{AUS_1_SUMMARY}}": "The Royal Commission on Antisemitism and Social Cohesion, set up after the Bondi Beach terror attack, is running Sydney hearings from 5–14 August, with Commissioner Virginia Bell examining evidence as the inquiry builds toward its December final report.",
    "{{AUS_1_URL}}": "https://asc.royalcommission.gov.au/hearings",

    "{{AUS_2_HEADLINE}}": "Home Prices Keep Falling Nationally as Inflation Drops to Pre-War Levels",
    "{{AUS_2_SUMMARY}}": "Home prices are falling across most of the country as the housing downturn continues, with the Treasurer welcoming inflation numbers that have now dropped back to levels last seen before the Middle East conflict — a mixed bag of cheaper cost-of-living pressure alongside a cooling property market.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "CFA Chief Officer Jason Heffernan Announces He's Stepping Down",
    "{{VIC_1_SUMMARY}}": "Chief Officer Jason Heffernan AFSM has told the CFA Board and Victorian Government he's stepping down, staying on until November to give the organisation time to recruit before the 2026/27 fire season — the news lands as Victorian crews remain deployed overseas supporting Canada's fire response.",

    # Science
    "{{SCI_1_FLAG}}": "🧬 BIOLOGY · FERTILISATION MAY DEPEND ON SPERM TEAMWORK, NOT JUST A SOLO RACE",
    "{{SCI_1_HEADLINE}}": "Forget the Sperm Race — New Research Says Fertilisation May Depend on Teamwork",
    "{{SCI_1_SUMMARY}}": "Evolutionary biologists from Syracuse, Siena and Szeged universities find that in many species, sperm don't compete purely as individuals — they cooperate in coordinated groups to reach and fertilise an egg, upending the simple 'fastest swimmer wins' model taught for decades. A reminder that even well-worn science can turn out to be more of a team sport than assumed.",

    # Business insight
    "{{INSIGHT_TITLE}}": "AI's Memory Chip Shortage Is About to Make Your Next Laptop Cost More",
    "{{INSIGHT_BODY}}": "AI data centres are now soaking up such a huge share of the world's memory chip supply that DRAM costs have tripled in eighteen months, and memory alone now makes up 40-60% of what a PC actually costs to build — enough that even HP, Asus and Acer are turning to Chinese-made chips to keep prices in check. For a small operation running quoting apps, job photos and admin off a laptop or tablet, it's a nudge to replace ageing gear sooner rather than later, or at least budget for a noticeably bigger bill next time one dies. It's also a neat reminder that the AI tools making your paperwork faster are, indirectly, one of the reasons the hardware underneath it all keeps getting dearer.",

    # Fun facts
    "{{FACT_1}}": "The tape measure tradies carry today traces back to a single 1868 patent — American Alvin J. Fellows was first to combine a concave-convex steel blade with a spring-loaded case, letting the tape hold itself rigid when extended instead of flopping over like the cloth and wooden folding rules that came before it.",
    "{{FACT_2}}": "The Leaning Tower of Pisa tilts because it was built on soft, uneven subsoil just three metres down — engineers didn't stabilise it until 1990–2001, when they removed 38 cubic metres of soil from underneath the north side to reduce the lean from 5.5 to under 4 degrees, deliberately stopping short of making it perfectly straight.",
    "{{FACT_3}}": "The jackhammer's ancestor was a steam-powered rock drill patented in 1849 by Massachusetts engineer Jonathan Couch — designed to bore through granite for one of the era's first mechanised tunnelling projects, decades before compressed air made the tool portable enough for a job site.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the solar installer's small business never have a bad month?",
    "{{JOKE_PUNCHLINE}}": "Because he always made sure the outlook stayed bright, rain or shine.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Energy and persistence conquer all things.\"",
    "{{CLOSING_ATTR}}": "— Benjamin Franklin",
    "{{CLOSING_MESSAGE}}": "It's a windy, showery start to Friday in Carrum Downs, with the wet stretch easing into a drier, sunnier run by Monday and Tuesday. Fuel prices are now fully reflecting the excise increase, so factor the higher bowser price into this week's job costings, and keep Tuesday 11 August marked for the RBA's rate call before committing to any big equipment finance.",
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
