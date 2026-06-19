#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 20 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 20 Jun
    # Showers today, clearing for solstice Sunday, shower risk Mon, partly cloudy Tue/Wed
    "{{WEATHER_1}}": "SAT 20 · 🌧 Showers · 15°C",
    "{{WEATHER_2}}": "SUN 21 · ⛅ Clearing · 16°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 22 · 🌦 Shower risk · 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 23 · ⛅ Partly cloudy · 14°C",
    "{{WEATHER_5}}": "WED 24 · ⛅ Partly cloudy · 15°C",
    "{{WEATHER_ALERT}}": "⚠ WINTER SOLSTICE TOMORROW SUN 21 JUN · EOFY 10 DAYS AWAY",

    # World
    "{{WORLD_1_FLAG}}": "🌐 Ukraine · Russia",
    "{{WORLD_1_HEADLINE}}": "Ukraine Strikes Moscow Oil Refinery in Its Largest Single-Night Drone Attack of the War",
    "{{WORLD_1_SUMMARY}}": "Ukraine launched 555 drones overnight — its largest single-night long-range attack since Russia's full-scale invasion began — targeting the Kapotnya oil refinery in southeast Moscow, a Gazprom subsidiary set ablaze for the second time in a week. Russia's air defences intercepted almost 200 drones approaching the capital; debris struck houses, a fitness centre and a large shopping mall whose roof caught fire. President Zelenskyy called the strikes 'a fully justified response to Russian attacks on our cities and communities.' Russia's defence ministry threatened escalation. The attack signals a significant intensification of Ukraine's long-range campaign as both sides await US diplomatic engagement on a ceasefire framework.",
    "{{WORLD_1_URL}}": "https://www.nbcnews.com/world/russia/moscow-refinery-attack-ukrainian-drones-hit-kapotnya-russia-trump-war-rcna350665",

    "{{WORLD_2_FLAG}}": "🌐 US · Iran",
    "{{WORLD_2_HEADLINE}}": "US and Iran Sign 60-Day Ceasefire Extension in Geneva — Strait of Hormuz Reopens and Nuclear Talks Begin",
    "{{WORLD_2_SUMMARY}}": "The United States and Iran formalised a 60-day ceasefire extension at a signing ceremony in Geneva on June 19, a significant diplomatic milestone following months of conflict that disrupted global oil supplies through the Strait of Hormuz. Both sides agreed to lift their maritime blockades, reopening the Strait to international shipping. Iran has pledged to never acquire nuclear weapons and will engage in technical negotiations on its enriched uranium stockpile in exchange for access to frozen assets and sanctions relief. If the framework holds, analysts expect a meaningful easing of global energy costs — which have been feeding directly into Australian fuel prices since the conflict escalated earlier this year.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/06/15/nx-s1-5858590/us-iran-deal-updates",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ Fuel · Australia",
    "{{ECON_1_HEADLINE}}": "The 32-Cent Fuel Excise Cut Expires June 30 — Australian Business Fuel Costs Are About to Jump",
    "{{ECON_1_SUMMARY}}": "The Australian Government's temporary fuel excise reduction of 32 cents per litre — which has held retail diesel prices roughly 38% lower than they would otherwise be since April 1 — expires on June 30. From July 1, the full excise rate returns on the same day as the minimum wage rise and the Payday Super changes. For a trades business running diesel vehicles and equipment in Carrum Downs, every kilometre driven from July 1 is more expensive overnight. The practical move before June 30: review any client contracts with escalation clauses, confirm fuel card arrangements, and price the full post-excise fuel cost into every FY2027 quote submitted this month.",
    "{{ECON_1_URL}}": "https://davidrosenbaum.com.au/australia-fuel-price/",

    "{{ECON_2_FLAG}}": "📊 EOFY · Retail",
    "{{ECON_2_HEADLINE}}": "EOFY Spending Tracks $10.7 Billion Nationally — Final 10 Days Deliver the Deepest Discounts on Tools and Equipment",
    "{{ECON_2_SUMMARY}}": "The Australian Retail Council is tracking $10.7 billion in EOFY spending nationally, with the final two weeks consistently producing the deepest discounts on technology, tools, equipment and plant as retailers compete to clear stock before June 30. For a trades business, this is the window to purchase eligible assets under the $20,000 instant asset write-off — but only if the asset is purchased, installed and ready for use before June 30. Ten days remain: if there is equipment you were planning to buy in July anyway, purchasing it this week may produce both the EOFY discount and a tax deduction in this financial year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 Anthropic · IPO",
    "{{TECH_1_HEADLINE}}": "Anthropic Overtakes OpenAI as World's Most Valuable AI Startup — $965 Billion Valuation and Confidential IPO Filed",
    "{{TECH_1_SUMMARY}}": "Anthropic — the company behind the Claude AI model that powers this briefing — surpassed OpenAI as the world's most valuable AI startup after raising $65 billion in Series H funding at a $965 billion post-money valuation, with a confidential IPO filing targeting October 2026 on NASDAQ. Annual recurring revenue now stands at approximately $47 billion, five times its December 2025 level. The scale of investment confirms sustained, accelerating AI development through 2026 and beyond. For small business: the AI tools available today are materially less capable than what will be standard in 12 to 18 months. The case for building the habit now — while costs are low and the learning curve is short — has never been more direct.",
    "{{TECH_1_URL}}": "https://finance.yahoo.com/markets/stocks/articles/anthropic-hits-965-billion-valuation-104626610.html",

    "{{TECH_2_FLAG}}": "🤖 AI Agents · 2026",
    "{{TECH_2_HEADLINE}}": "AI Shifts From Chatbot to Autopilot — Agents Now Completing Full Business Workflows Without Human Prompting",
    "{{TECH_2_SUMMARY}}": "June 2026 marks a visible inflection in enterprise AI: the shift from conversational tools to agentic systems that plan, execute and close multi-step tasks autonomously. Google, OpenAI, Anthropic and Microsoft are all shipping production-grade agent systems capable of handling quoting workflows, supplier communications, scheduling and invoice follow-up as full sequences — without needing to be re-prompted at each step. For a trades business, the practical implication is that AI is no longer just a faster way to write an email. The next generation of tools is being built to manage the entire admin loop while you are on the tools — end to end, without babysitting.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 Automate 2026 · Chicago",
    "{{ROBOT_1_HEADLINE}}": "World's Largest Robotics Show Opens Monday — Humanoid Robot Forum to Define the Direction of Physical AI Through 2027",
    "{{ROBOT_1_SUMMARY}}": "North America's largest robotics and automation event, Automate 2026, opens at McCormick Place in Chicago this Monday June 22 with more than 50,000 attendees and 1,000 exhibitors. At its centrepiece is the inaugural Humanoid Robot Forum (June 23–24) — a dedicated two-day program examining the real-world economics of humanoid deployment: six-month payback periods in high-utilisation factories, workforce integration models, and the physical AI software stacks enabling robots to train entirely in simulation before entering production floors. Events like Automate tend to set the commercial agenda for industrial robotics investment over the following 12 to 24 months.",
    "{{ROBOT_1_URL}}": "https://www.automateshow.com/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Fall 2-1 to USA in Seattle — Haji Wright Brace Ends Australia's Perfect World Cup Start",
    "{{AUS_1_SUMMARY}}": "Australia suffered a narrow 2-1 defeat to the United States at Lumen Field in Seattle in a fiercely contested World Cup Group D clash overnight (5am AEST). Jordan Bos put the Socceroos ahead in the first half, but Haji Wright's brace — assisted by Cristian Roldan — turned the match for the USA. Christian Pulisic was injured, clouding the US outlook for future games. Australia remains on three points in Group D and is still alive for knockout qualification, but will need a result against Turkey in their final group game. The team fought hard in one of the loudest and most hostile stadium environments in North American sport.",
    "{{AUS_1_URL}}": "https://www.aol.com/article/haji-wright-delivers-as-usmnt-beats-australia-2-1-but-christian-pulisics-injury-clouds-win-030458529.html",

    "{{AUS_2_HEADLINE}}": "July 1 Triple Whammy: Wage Rise, Payday Super and Fuel Excise All Hit Australian Businesses on the Same Morning",
    "{{AUS_2_SUMMARY}}": "Australian small business operators face a rare convergence of three simultaneous cost increases from July 1: the minimum wage rise under the Fair Work Commission's annual wage review; the commencement of Payday Super, shifting superannuation from quarterly to within seven business days of each pay run; and the return of the full fuel excise as the temporary 32-cent reduction expires. For a trades business with staff on award rates running diesel vehicles, all three operating cost increases arrive on the same morning. Any quote currently being priced for work completing after July 1 needs to absorb all three before it is sent.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Marks Winter Solstice Weekend — Street Parties, Sound Baths and Planetarium Shows Across the City Tonight",
    "{{VIC_1_SUMMARY}}": "Melbourne is hosting a cluster of winter solstice events this weekend: the Courthouse Hotel's Winter Solstice Street Party takes over Errol Street in North Melbourne tonight; Abbotsford Convent is running a special sound bath led by LA-based vocalist Odeya Nini; Scienceworks After Dark features a Planetarium show on the astronomy of the solstice; and the Sorrento Solstice Festival runs all afternoon and evening on the Mornington Peninsula. Winter solstice falls tomorrow, Sunday June 21 — the Southern Hemisphere's shortest day — after which Melbourne gains approximately one to two minutes of daylight each day through to the December summer solstice.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 Biology · Science",
    "{{SCI_1_HEADLINE}}": "Scientists Switch On Mammalian Regeneration — Ability to Regrow Bone and Joints Is Not Lost, Just Switched Off",
    "{{SCI_1_SUMMARY}}": "A multi-institution study led by Dr Ken Muneoka of Texas A&M University — in collaboration with Tulane, Stanford, Arizona State University and the Ludwig Boltzmann Institute for Traumatology in Vienna — published this week in the journal Science overturns the long-held assumption that mammals lost the regenerative abilities of salamanders and other simpler animals. The study shows the ability is not absent in mammals: it is switched off. Using a sequenced two-stage growth factor protocol — FGF2 followed by BMP2 — the team redirected the body's normal healing response away from scar formation and toward full regrowth of bone, joint cartilage, ligaments and tendons after amputation in animal studies, without any external stem cell transplants. The researchers believe the same dormant pathway exists in humans.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Ten Days to EOFY — The AI Checklist That Closes the Financial Year Without the Last-Minute Scramble",
    "{{INSIGHT_BODY}}": "With ten days remaining before June 30, the gap between a clean financial year-end and a chaotic one is almost always the same thing: preparation done on the last Saturday versus panic on June 27. Here is what AI can help you action today. First, outstanding invoices: export your unpaid invoice list and run a prompt asking your AI to draft tailored follow-up messages for each one, adjusting tone for how old the debt is and the size of the amount. That single Saturday hour can chase a month of debtors. Second, the instant write-off window: ask your AI to identify any planned tool, equipment or technology purchases you were going to make in July — then calculate whether buying them this week at current EOFY discounts would produce both a tax deduction and a price saving versus buying post-discount in the new financial year. Third, FY2027 rate card: the triple cost hit on July 1 — wage rise, Payday Super and fuel excise — means rates quoted in the last three months may be underpriced for work completing after July 1. Run your current labour rate and fuel inputs through an AI and ask it to calculate the compounded impact of all three changes. Fourth, job records: EOFY is the moment to have AI turn outstanding site notes, photos and WhatsApp messages into completion reports while the jobs are still fresh. The businesses that arrive at July 1 in control are the ones that treated this Saturday as a half-day of admin, not a day off.",

    # Fun Facts
    "{{FACT_1}}": "The word 'solstice' derives from the Latin sol (sun) and sistere (to stand still) — because at this moment the sun appears to pause at its extreme point before reversing direction. Tomorrow's winter solstice (June 21) is the Southern Hemisphere's shortest day of the year. From Sunday, Melbourne gains approximately one to two minutes of daylight each day until the summer solstice in December, when the sun sets around 8:45pm.",

    "{{FACT_2}}": "Australia produces approximately 95% of the world's supply of gem-quality opals. The largest opal ever found — the 'Olympic Australis' — was unearthed at Coober Pedy, South Australia in 1956 and weighs 17,000 carats (3.4 kilograms). The most celebrated black opal, the 'Virgin Rainbow' from Lightning Ridge NSW, glows in the dark due to its fluorescence and is valued at approximately AUD $1 million.",

    "{{FACT_3}}": "The Concorde supersonic jet carried passengers from London to New York in 3.5 hours but consumed approximately 25,700 litres of fuel per hour — around 17 times more per passenger than a modern Boeing 787 Dreamliner. At cruising speed of Mach 2.02 (2,179 km/h), aerodynamic heating caused the aluminium fuselage to expand by up to 30 centimetres in flight, so engineers deliberately left gaps in the airframe to accommodate the thermal expansion.",

    # Joke
    "{{JOKE_SETUP}}": "Why do the best tradies always schedule their biggest jobs for a cold Saturday morning in winter?",
    "{{JOKE_PUNCHLINE}}": "No traffic, no school zones, and everyone else is sleeping off the World Cup. You own the whole job site.",

    # Closing
    "{{CLOSING_QUOTE}}": "“However long the night, the dawn will break.”",
    "{{CLOSING_ATTR}}": "— African Proverb",
    "{{CLOSING_MESSAGE}}": "The Socceroos went down 2-1 to the USA overnight — Jordan Bos gave Australia the lead before Haji Wright's brace sealed it for the home side at Lumen Field. Still three points in Group D, still alive, and the Turkey game becomes everything. It's a cold, wet Saturday in Carrum Downs, and tomorrow is winter solstice — the longest night of the year, after which the days start getting longer again. Ten days to EOFY: fuel excise expires June 30, Payday Super starts July 1, the wage rise lands the same morning. If there's a better use of a rainy Saturday morning than getting ahead of all three, it's hard to think of one. However long the night. Go the Socceroos, Liall.",
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
