#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 21 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 21 Aug (BOM)
    "{{WEATHER_1}}": "FRI 21 · ☁️ Cloudy, chance of a shower · 9–16°C",
    "{{WEATHER_2}}": "SAT 22 · 🌦️ Showers, morning and afternoon · 9–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 23 · 🌧️ Partly cloudy, light rain · 7–12°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 24 · ☁️ Cloudy, isolated shower · 7–14°C",
    "{{WEATHER_5}}": "TUE 25 · 🌦️ Patchy rain clearing · 8–14°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or Carrum Downs — Wednesday's damaging wind warning has eased — but with showers likely Saturday and Sunday, Monday or Tuesday is the better window for any exterior coating or blasting work that needs a dry surface",

    # World
    "{{WORLD_1_FLAG}}": "🇨🇳 CHINA · EVERGRANDE FOUNDER SENTENCED TO LIFE",
    "{{WORLD_1_HEADLINE}}": "Evergrande Founder Hui Ka Yan Jailed for Life",
    "{{WORLD_1_SUMMARY}}": "A Shenzhen court sentenced Hui Ka Yan, founder of collapsed property giant China Evergrande, to life imprisonment for fraud, embezzlement and bribery, confiscating all his personal property. Evergrande and its main operating unit were separately fined roughly $1.31 billion and 7 billion yuan, among the largest corporate penalties ever handed down in a Chinese criminal case, closing out the fallout from the firm's 2021 collapse under more than $300 billion in liabilities.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/08/20/nx-s1-5939335/chinese-sentence-founder-evergrande",

    "{{WORLD_2_FLAG}}": "🇺🇦 UKRAINE · RUSSIA SHIFTS ENERGY WAR TOWARD WINTER",
    "{{WORLD_2_HEADLINE}}": "Ukraine Races to Winter-Proof Its Power Grid as Strikes Continue",
    "{{WORLD_2_SUMMARY}}": "With Russian strikes hitting Naftogaz facilities and power substations through summer, Ukraine has begun an unusually early push to build smaller distributed power sources and shield its grid, fearing a repeat of last winter's crippling bombardment campaign. Kyiv residents sheltered in metro stations during fresh overnight strikes this week as officials warned the \"energy war\" is entering its next phase.",
    "{{WORLD_2_URL}}": "https://www.washingtontimes.com/news/2026/aug/20/ukraine-braces-winter-russia-shifts-energy-war-heat-water/",

    # Economics
    "{{ECON_1_FLAG}}": "⛽🇦🇺 FUEL PRICES · EXCISE BACK TO FULL RATE",
    "{{ECON_1_HEADLINE}}": "Bowser Prices Stay Elevated as Fuel Excise Returns in Full",
    "{{ECON_1_SUMMARY}}": "Since the temporary fuel excise cut fully expired on 2 August, the excise has sat back at 53.7 cents a litre, and the ACCC's latest monitoring shows average retail petrol and diesel prices across Australia's five biggest cities running well above the discounted levels of a few weeks ago. Victoria currently has among the cheapest average unleaded prices of any state, but every business running a ute or van is still feeling the pinch at the pump.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📉🇦🇺 JOBS MARKET · UNEMPLOYMENT AT POST-COVID HIGH",
    "{{ECON_2_HEADLINE}}": "Unemployment Climbs to 4.5%, the Highest Since the Pandemic",
    "{{ECON_2_SUMMARY}}": "ABS figures released yesterday show Australia's seasonally adjusted unemployment rate rose to 4.5% in July, with 691,500 people now out of work as part-time roles fell faster than full-time hiring could offset. Economists say the softer labour market makes a further RBA rate rise in September less likely, which is at least one less cost pressure for small business owners carrying loans on plant or a ute.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI COMMERCE · GOOGLE'S AI NOW CALLS SHOPS FOR YOU",
    "{{TECH_1_HEADLINE}}": "Google Launches \"Let Google Call\" — AI Agents That Ring Local Stores",
    "{{TECH_1_SUMMARY}}": "Google's new feature uses its Gemini-powered voice agent to phone nearby stores on a shopper's behalf, check stock and pricing, then text back a summary — the AI is required to identify itself as an automated caller, and businesses can opt out. It's paired with an \"agentic checkout\" tool that can complete a purchase via Google Pay once the shopper approves, pushing AI further into everyday retail transactions.",
    "{{TECH_1_URL}}": "https://www.techbuzz.ai/articles/google-unleashes-shopping-ai-bots-that-call-stores-and-buy-for-you",

    "{{TECH_2_FLAG}}": "💾 AI CHIPS · GOOGLE-MARVELL MEGA-DEAL",
    "{{TECH_2_HEADLINE}}": "Marvell Hands Google a $12.2 Billion Stake Option in AI Chip Deal",
    "{{TECH_2_SUMMARY}}": "Chipmaker Marvell has given Google the right to buy up to $12.2 billion of its shares, tied to Google's purchases of custom AI inference, storage and networking chips — a deal that could be worth roughly $120 billion in revenue for Marvell through 2033 and sent its stock up more than 11% overnight, underlining how much money is now flowing into the physical infrastructure behind everyday AI tools.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 ROBOTICS · BEIJING'S ROBOT GAMES OPEN THIS WEEKEND",
    "{{ROBOT_1_HEADLINE}}": "Beijing Gears Up for the World Humanoid Robot Games",
    "{{ROBOT_1_SUMMARY}}": "Beijing is putting the finishing touches on the second World Humanoid Robot Games, opening 22 August at the National Speed Skating Oval with a reported 2,056 robots from 666 teams — sharply up on last year — competing across more than 30 events testing agility, manipulation and autonomy. Household service robots have been doing trial runs around the city this week ahead of the Games, a sign of how fast the sector is moving from lab demos to public competition.",
    "{{ROBOT_1_URL}}": "https://news.cgtn.com/news/2026-08-19/Household-robots-gear-up-for-World-Humanoid-Robot-Games-2026-1PJMzWOxAbK/p.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Fortescue Produces First Hot Metal at Pilbara Green Iron Plant",
    "{{AUS_1_SUMMARY}}": "Fortescue's $75 million Christmas Creek pilot plant has produced its first molten metal using a renewable-powered furnace instead of coking coal, a milestone toward commercial \"green iron\" production in the Pilbara. The plant is expected to eventually produce more than 1,500 tonnes a year as the company works to prove cheap green power can make low-carbon steelmaking commercially viable.",
    "{{AUS_1_URL}}": "https://www.miningweekly.com/article/fortescue-produces-first-hot-metal-towards-green-iron-production-in-australia-2026-08-19",

    "{{AUS_2_HEADLINE}}": "Drones Breach Restricted Airspace at RAAF Base Williamtown Again",
    "{{AUS_2_SUMMARY}}": "Police have confirmed drones breached restricted airspace around RAAF Base Williamtown — home to most of Australia's F-35A fighter jets — for the second time in a month, following a similar incursion in July. Investigators are working with the ADF to identify who is operating the drones; Australia's most sensitive defence sites logged 147 such breaches last financial year, more than double the year before.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Launches $50m Royal Commission Into Construction Sector Corruption",
    "{{VIC_1_SUMMARY}}": "Premier Ben Carroll has appointed former SA chief justice Christopher Kourakis to lead a royal commission investigating corruption, criminality and misconduct on major projects within Victoria's Big Build program, with a final report due within 12 months. For local trades and subcontractors it's a clear signal that scrutiny of contracts, paperwork and project oversight across the construction sector is about to get a lot tighter.",

    # Science
    "{{SCI_1_FLAG}}": "☕ HEALTH SCIENCE · YOUR COFFEE HABIT, EXPLAINED",
    "{{SCI_1_HEADLINE}}": "Coffee Drinkers Have Less Body Fat, More Muscle and Distinct Hormones, Study Finds",
    "{{SCI_1_SUMMARY}}": "Analysing more than 2,264 people in Finland's Northern Finland Birth Cohort, University of Oulu researchers found that despite similar BMI, the heaviest coffee drinkers carried about 6% less visceral fat and had the highest skeletal muscle mass, along with distinct sex-hormone patterns and lower levels of amino acids linked to insulin resistance. It's an observational study, so it can't prove coffee causes the effect — but it adds to a growing pile of evidence that habitual coffee drinking tracks with healthier metabolism.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Google's AI Agents Are Now Calling Local Businesses — Is Yours Ready to Pick Up?",
    "{{INSIGHT_BODY}}": "Google's new \"Let Google Call\" feature has quietly started ringing local businesses on customers' behalf, using an AI voice agent to check stock, pricing and availability before texting the customer a summary. For a trades business like ISV, that cuts both ways: a caller from an unfamiliar number identifying itself as an automated Google agent isn't a scam to hang up on, it's a genuine lead worth a straight answer — and the businesses that respond clearly and quickly will win the booking before a human ever gets involved. It's also worth flipping around: the same kind of AI calling agent can be pointed at your own supplier list to chase stock and pricing on abrasives, coatings and consumables without anyone on your team losing an afternoon on hold.",

    # Fun facts
    "{{FACT_1}}": "Melbourne's CBD grid, surveyed by Robert Hoddle in 1837, has main streets 99 feet (30 metres) wide — Hoddle fought off the Governor's order to narrow them to 66 feet, arguing wide streets were needed so bullock drays hauling goods through town wouldn't block horse-drawn traffic making turns.",
    "{{FACT_2}}": "The world's first video game to display graphics on a screen was OXO, a version of noughts-and-crosses built in 1952 by Alexander Douglas on Cambridge's EDSAC computer as part of his PhD thesis — players entered moves with a rotary telephone dial and played against a genuinely artificially intelligent opponent, two decades before Pong.",
    "{{FACT_3}}": "The idea that a business's reputation and customer relationships are a saleable asset in their own right — what accountants now call \"goodwill\" — was cemented in British law by an 1896 House of Lords case, Trego v Hunt, involving a dispute between two Victorian-era varnish manufacturers.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the portable toilet hire business never worry about a cash flow problem?",
    "{{JOKE_PUNCHLINE}}": "Because business was always flush.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Discipline is the bridge between goals and accomplishment.\"",
    "{{CLOSING_ATTR}}": "— Jim Rohn",
    "{{CLOSING_MESSAGE}}": "A showery start to the weekend in Carrum Downs means it's worth locking in any exterior coating work before Saturday's rain rolls in, then eyeing Monday or Tuesday for the next dry run. Between Victoria's new construction Royal Commission and Google's AI now cold-calling shops on customers' behalf, it's a week that's a good reminder to keep your own paperwork and phone manner just as sharp as your tools.",
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
