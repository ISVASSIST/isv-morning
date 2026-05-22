#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 23 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 23 May (BOM forecast)
    "{{WEATHER_1}}": "SAT 23 · ⛅ P/Cloudy · 18°C",
    "{{WEATHER_2}}": "SUN 24 · ☀ Mostly sunny · 19°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 25 · 🌧 Showers likely · 17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 26 · 🌧 Showers · 17°C",
    "{{WEATHER_5}}": "WED 27 · ⛅ P/Cloudy · 15°C",
    "{{WEATHER_ALERT}}": "☔ RAIN FROM MONDAY",

    # World
    "{{WORLD_1_FLAG}}": "🇷🇺 RUSSIA · NUCLEAR DRILLS",
    "{{WORLD_1_HEADLINE}}": "Russia Delivers Nuclear Warheads to Belarus as Putin and Lukashenko Personally Monitor Massive Joint Exercises",
    "{{WORLD_1_SUMMARY}}": "Russia conducted its largest tactical and strategic nuclear force exercises in years from 19–21 May, deploying nuclear munitions to field storage facilities in Belarus as part of joint drills involving 64,000 personnel and 7,800 pieces of equipment — including 200 missile launchers, 73 surface ships, and 13 submarines. Russian President Putin and Belarusian President Lukashenko monitored the event via video conference, the first time both leaders have directly participated in a joint nuclear exercise. Live firings included a Yars ballistic missile and a Zircon hypersonic missile. NATO allies expressed serious concern, Ukraine upgraded its air defence posture, and the drills were launched with minimal advance notice to Western partners — a combination European governments are treating as deliberate escalation signalling at a time when diplomatic channels remain strained.",
    "{{WORLD_1_URL}}": "https://www.euronews.com/my-europe/2026/05/21/russia-delivers-nuclear-warheads-to-belarus-as-nato-tensions-spike",

    "{{WORLD_2_FLAG}}": "🏥 WHO · PUBLIC HEALTH",
    "{{WORLD_2_HEADLINE}}": "WHO Declares Global Health Emergency Over Ebola Outbreak in DRC and Uganda — 650+ Suspected Cases, No Approved Vaccine",
    "{{WORLD_2_SUMMARY}}": "The World Health Organization declared a Public Health Emergency of International Concern over an Ebola outbreak caused by the Bundibugyo virus strain in the Democratic Republic of Congo's Ituri Province, which has now spread to Uganda with confirmed cases in Kampala. Over 650 suspected cases and 160 suspected deaths have been reported, with the true scale likely larger given detection challenges in the region. Unlike the more widely known Ebola-Zaire strains, there are currently no approved vaccines or therapeutics for Bundibugyo, significantly complicating the international response. WHO, CDC, and ECDC are coordinating emergency deployments. The 2014–16 West Africa outbreak killed over 11,000 people before containment — early response speed is critical.",
    "{{WORLD_2_URL}}": "https://www.who.int/emergencies/disease-outbreak-news/item/2026-DON602",

    # Economics
    "{{ECON_1_FLAG}}": "📊 ABS · LABOUR FORCE",
    "{{ECON_1_HEADLINE}}": "Australian Unemployment Jumps to 4.5% in April — Highest Since 2021 as Employment Falls Unexpectedly",
    "{{ECON_1_SUMMARY}}": "The Australian Bureau of Statistics Labour Force survey for April 2026 delivered a significant shock: employment fell by 18,600 to 14.74 million — the first monthly decline in five months — defying market forecasts for a 17,500 gain. The unemployment rate rose to 4.5%, the highest level since November 2021, and youth unemployment surged 0.9 percentage points to 11.1%. The RBA's May Statement on Monetary Policy, released Thursday, projects inflation peaking at 4.8% in the June quarter and rate cuts not arriving until at least mid-2027. For trades businesses, deteriorating employment conditions typically signal reduced consumer confidence on discretionary spend — though maintenance, protective coatings, and compliance-driven industrial work hold more resilient than new construction and fit-out pipelines.",
    "{{ECON_1_URL}}": "https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release",

    "{{ECON_2_FLAG}}": "⛽ FUEL PRICES · ACCC",
    "{{ECON_2_HEADLINE}}": "ACCC Weekly Update: Retail Diesel Down 28%, Petrol Down 29% — Fuel Excise Cut Delivers Relief Until June 30",
    "{{ECON_2_SUMMARY}}": "The ACCC's weekly fuel price monitoring update published Friday 22 May confirms retail diesel is down 28% and petrol down 29% across Australia's five largest cities compared to the crisis peak. The federal government's temporary fuel excise reduction of 32 cents per litre — running from 1 April to 30 June 2026 — is driving a material portion of the relief, alongside easing international crude prices as Strait of Hormuz routes partially reopen. For any trades or fleet operator with bulk tank capacity: the excise cut expires 30 June. The next five weeks are your window to pre-purchase at lower input costs before prices likely step back up.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 OPENAI · GPT-5.5",
    "{{TECH_1_HEADLINE}}": "OpenAI Launches GPT-5.5 With Full Agentic Capabilities — Multi-Step Task Automation Live, 4 Million Weekly Codex Users",
    "{{TECH_1_SUMMARY}}": "OpenAI has released GPT-5.5, its most capable agentic model to date, designed to execute complex multi-step tasks across software environments without constant user prompting — planning, using tools, checking its own work, and pushing through ambiguity autonomously. Codex, OpenAI's coding and automation agent built on GPT-5.5, now counts 4 million weekly active users. The practical shift: GPT-5.5 moves AI from a capable tool you direct step by step to a capable delegate you hand a goal to. For trades businesses, this means a single prompt can now initiate a multi-stage admin sequence — generate a quote, check schedule availability, draft a follow-up message, and log the outcome — without micromanagement at every step.",
    "{{TECH_1_URL}}": "https://openai.com/index/introducing-gpt-5-5/",

    "{{TECH_2_FLAG}}": "🔐 FIVE EYES · AI GUIDANCE",
    "{{TECH_2_HEADLINE}}": "Australia Joins Five Eyes in Releasing Agentic AI Risk Guidance — Businesses Warned on Five Critical Threat Categories",
    "{{TECH_2_SUMMARY}}": "The cybersecurity agencies of Australia, the US, UK, Canada, and New Zealand jointly released guidance titled 'Careful Adoption of Agentic AI Services,' identifying five risk categories as AI systems gain autonomous capability: supply chain compromise of AI tools, prompt injection attacks, excessive permission grants to AI agents, inadequate audit trails, and over-reliance on AI outputs without human verification. The guidance provides best-practice frameworks across the full AI lifecycle. For any business now using AI for quoting, scheduling, or document generation, the sections on permissions management and human-in-the-loop validation are the most immediately relevant.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤝 UK ROBOTICS · BOSCH",
    "{{ROBOT_1_HEADLINE}}": "UK's Humanoid Secures Bosch Partnership for Scaled HMND 01 Production — Bosch Logistics Becomes First Major Commercial Deployment",
    "{{ROBOT_1_SUMMARY}}": "UK AI and robotics company Humanoid announced a commercial partnership with manufacturing giant Bosch on 22 May to scale production of its HMND 01 humanoid robot, following a successful proof of concept in March 2026 where HMND 01 robots autonomously transferred boxes from conveyors to trolleys in Bosch's logistics facility in Bühl, Germany, without human supervision. The partnership follows Humanoid's earlier agreement to deploy up to 2,000 robots in Schaeffler's global factory network. Bosch is one of the world's largest industrial and logistics operators — a supply relationship at that scale is not a pilot programme, it is a commercial platform. Barclays Research, also publishing this week, estimates the humanoid robot market will reach $200 billion by 2035, with the sector compressing its timeline from demonstration to contracted deployment faster than almost any previous automation technology.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/05/22/humanoid-secures-partnership-with-manufacturing-giant-bosch-following-a-successful-proof-of-concept/101720/",

    # Australia
    "{{AUS_1_HEADLINE}}": "ABS April Labour Force: Employment Falls 18,600, Unemployment Hits 4.5% — Highest Since November 2021",
    "{{AUS_1_SUMMARY}}": "The ABS confirmed Australia's unemployment rate rose to 4.5% in April — the highest level since November 2021 — after employment unexpectedly fell 18,600 in the month, defying forecasts. Youth unemployment jumped to 11.1%. The data confirms that three consecutive RBA rate hikes, the Budget's property investor changes, and 5% inflation are beginning to translate into real labour market softening. The RBA's May Statement on Monetary Policy projects unemployment rising further to 4.7% by 2028. For trades businesses, the practical signal is to watch forward bookings and quote conversion rates carefully — residential discretionary spend will soften before industrial and maintenance work does.",
    "{{AUS_1_URL}}": "https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release",

    "{{AUS_2_HEADLINE}}": "RBA May Statement on Monetary Policy: Inflation to Peak 4.8% in June Quarter, Rate Cuts Off the Table Until Mid-2027",
    "{{AUS_2_SUMMARY}}": "The Reserve Bank's May 2026 Statement on Monetary Policy confirmed headline inflation is expected to peak at 4.8% in the June quarter with underlying inflation remaining above 3% until mid-2027 and unemployment forecast to reach 4.7% by 2028. The bank stated explicitly that the labour market will operate with 'a little spare capacity' over the forecast period — signalling it is not in a hurry to cut rates. For trades businesses financing equipment, vehicles, or working capital at variable rates: borrowing costs are not coming down meaningfully for at least 12 to 18 months.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Public School Teachers Win Up to 32.4% Pay Rise Over Four Years in Landmark AEU Deal",
    "{{VIC_1_SUMMARY}}": "The Australian Education Union and the Victorian state government reached an in-principle agreement this week for the largest public school pay deal in decades — between 28.3% and 32.4% rises over four years for teachers, and 39% for early childhood educators. An experienced teacher's salary rises from $118,063 to $151,419 by 2029, with the first 12% increase landing October 2026. For trades businesses working in school precincts, landmark enterprise agreement settlements historically precede increased government capital spending on school infrastructure and maintenance — as staffing budget certainty tends to unlock longer-term capital planning cycles.",

    # Science
    "{{SCI_1_FLAG}}": "🧬 BIOLOGY · MIT",
    "{{SCI_1_HEADLINE}}": "MIT Scientists Discover Single Amino Acid That Triggers Intestinal Repair — Could Transform Recovery After Cancer Treatment",
    "{{SCI_1_SUMMARY}}": "Researchers at MIT have identified cysteine — an amino acid naturally present in meat, dairy, beans, and nuts — as a potent trigger for intestinal stem cell repair. In mice exposed to the radiation damage common in cancer treatment, a cysteine-rich diet activated immune cells that released healing signals, prompting stem cells to rebuild damaged intestinal tissue. The discovery points toward a dietary intervention that could significantly reduce recovery time after chemotherapy, bowel surgery, or radiation treatment without requiring new pharmaceutical compounds. Researchers believe the same cysteine-activation mechanism is likely active in humans. Published in ScienceDaily, 21 May 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Small Trades Businesses Are Leaving Government Grants on the Table — AI Can Help You Claim Them",
    "{{INSIGHT_BODY}}": "There are dozens of active state and federal grant programs that small trades businesses are technically eligible for right now — apprenticeship incentives, energy efficiency upgrades, digital transformation grants, clean energy rebates, export assistance, and more. Most operators never apply, not because they're ineligible, but because researching programs, establishing eligibility, writing applications, and assembling supporting documentation on top of running actual jobs is genuinely difficult. AI changes that equation significantly. A well-structured prompt to Claude or ChatGPT — outlining your business size, industry code, annual turnover, headcount, and what you'd use the funding for — will return a shortlist of relevant programs in minutes and can draft a complete application in under 30 minutes. Business.gov.au's grants finder and Business Victoria's register are both publicly searchable and updated regularly. If your business hasn't received a grant in the past 12 months, there's a real possibility you're eligible for something you haven't yet claimed. Saturday is the right day to spend 20 minutes finding out.",

    # Fun Facts
    "{{FACT_1}}": "The first product ever scanned by a commercial barcode reader was a pack of Wrigley's Juicy Fruit chewing gum, sold at a Marsh Supermarkets store in Troy, Ohio, on 26 June 1974. The gum sold for 67 cents. That transaction was the first successful use of the Universal Product Code in a retail checkout — and the original pack is now on display at the Smithsonian Institution's National Museum of American History in Washington, D.C.",

    "{{FACT_2}}": "The pistol shrimp can snap its claw so fast it generates a cavitation bubble that collapses at temperatures briefly reaching around 4,000°C — comparable to the surface of the sun — producing a shockwave at approximately 200 decibels, louder than a gunshot at close range. The snap travels faster than a speeding bullet and is powerful enough to stun or kill small prey. It is one of the loudest sounds produced by any living animal relative to its body size.",

    "{{FACT_3}}": "Minecraft is the best-selling video game of all time with over 300 million copies sold across all platforms. Creator Markus 'Notch' Persson wrote the first playable version in just six days in May 2009, taking inspiration from Dwarf Fortress and Infiniminer. Microsoft acquired Mojang in 2014 for US$2.5 billion. The game now has more than 140 million monthly active players and generates roughly US$1 billion in annual revenue — all from a project that began as a six-day experiment.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the demolition contractor win the business award?",
    "{{JOKE_PUNCHLINE}}": "He really knew how to bring the house down.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The best time to plant a tree was 20 years ago. The second best time is now.”",
    "{{CLOSING_ATTR}}": "— Chinese Proverb",
    "{{CLOSING_MESSAGE}}": "Saturday morning in Carrum Downs — partly cloudy today with a high around 18°C, and Sunday looks even cleaner at 19°C. If there's outdoor prep, coating, or site work that needs doing this weekend, you've got a solid two-day window before showers roll back in Monday and hold through Tuesday. This week carried a heavy economic load: unemployment is at 4.5% and rising, the RBA confirmed rate cuts aren't expected until mid-2027, inflation is heading for a 4.8% peak in June, and the Federal Budget's negative gearing changes are now live. For a maintenance-focused trades business like ISV, the read is reasonably constructive — owners of existing buildings and industrial stock don't stop maintaining and protecting it just because property investors are stepping back. The fuel excise cut is still running and diesel is down nearly 30%; if you have bulk tank capacity, the next five weeks are your window. Enjoy the weekend, Liall.",
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
