#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 29 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 29 May (BOM forecast)
    "{{WEATHER_1}}": "FRI 29 · 🌦 Showers · 17°C",
    "{{WEATHER_2}}": "SAT 30 · 🌧 Rain likely · 18°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 31 · 🌫 Fog/Cloudy · 15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 1 JUN · ☁️ Cloudy/fog · 14°C",
    "{{WEATHER_5}}": "TUE 2 JUN · 🌧 Rain likely · 16°C",
    "{{WEATHER_ALERT}}": "⚠ WET WEEKEND — RAIN SAT–SUN",

    # World
    "{{WORLD_1_FLAG}}": "🌊 USA · INDUSTRIAL DISASTER",
    "{{WORLD_1_HEADLINE}}": "Chemical Tank Implosion at Washington State Paper Mill Kills 2, 9 Still Unrecovered",
    "{{WORLD_1_SUMMARY}}": "A 600,000-gallon white liquor chemical tank imploded at the Nippon Dynawave Packaging facility in Longview, Washington on Tuesday, killing at least two workers and leaving nine others unrecovered — potentially the deadliest industrial accident in Washington state history. Recovery efforts are hampered by ongoing structural instability around the ruptured tank. White liquor is a caustic chemical used to break down wood into paper pulp. Crews are working to dilute it to safe levels before discharge into the Columbia River, which is being monitored for contamination. Seven others are hospitalised. Cause under investigation.",
    "{{WORLD_1_URL}}": "https://www.cbsnews.com/news/washington-paper-mill-chemical-tank-explosion-deaths/",

    "{{WORLD_2_FLAG}}": "🇮🇷🇮🇱 MIDDLE EAST · ESCALATION",
    "{{WORLD_2_HEADLINE}}": "Israel Launches 100 Airstrikes on Lebanon in 10 Minutes — Iran Calls US Actions a Gross Ceasefire Violation",
    "{{WORLD_2_SUMMARY}}": "Israel launched Operation Eternal Darkness — 100 airstrikes across Lebanon in 10 minutes — killing at least 11 people including civilians in the Bekaa Valley, despite the April 17 US-brokered ceasefire. Iran's foreign ministry separately accused the US of 'piracy' for attacking Iranian commercial vessels, calling the strikes a 'gross violation' of ceasefire terms. Israel maintains the ceasefire never applied to Lebanon; Iran and Pakistani mediators say it did. Prospects for a broader peace deal — which would reopen the Strait of Hormuz and potentially ease global fuel prices — have deteriorated sharply this week.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/05/26/nx-s1-5834840/iran-lebanon-updates",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AUSTRALIA · FUEL",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Cut Has Slashed Diesel 30%, Petrol 28% — But June 30 Reversal Is 32 Days Away",
    "{{ECON_1_SUMMARY}}": "The Federal Government's temporary 32c/litre fuel excise halving has cut diesel approximately 30% and petrol 28% across Australia's five major cities since April 1, according to ACCC weekly monitoring. For a trades business running two diesel vans at 50,000km each annually, the excise reversal on June 30 — when excise reverts from 26.3c to 52.6c per litre — represents roughly $2,600–$3,200 in additional annual fuel cost landing in 32 days. Any job being quoted now for delivery in July or August needs to incorporate the post-excise fuel rate, or the margin disappears before the job is finished.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📉 ECONOMY · CONSUMER SPENDING",
    "{{ECON_2_HEADLINE}}": "Australian Household Spending Falls in April — First Drop in Four Months as RBA Rate Hikes Bite",
    "{{ECON_2_SUMMARY}}": "New data released Thursday showed Australian household spending fell in April for the first time in four months, confirming that three RBA rate hikes in 2026 — pushing the cash rate to 4.35% — are beginning to compress consumer demand. The ASX 200 fell 1.4% to 8,593 on the data, its lowest close in a week. CBA economists forecast growth to slow below trend through 2026 as borrowing costs and living expenses continue to weigh. For trades businesses with residential renovation exposure, softening consumer spending is the earliest leading indicator of a pipeline tightening — the second-half pipeline needs watching closely.",
    "{{ECON_2_URL}}": "",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📱 META · AI PLATFORMS",
    "{{TECH_1_HEADLINE}}": "Meta Launches Paid Subscriptions for Instagram, Facebook and WhatsApp — Business AI Tools Bundled In",
    "{{TECH_1_SUMMARY}}": "Meta officially launched consumer and business subscription tiers for all three core platforms on May 27 — Instagram Plus ($3.99/mo), Facebook Plus ($3.99/mo) and WhatsApp Plus ($2.99/mo) — with AI-enhanced features including analytics, creative tools, expanded messaging and AI interaction. The launch marks the first time Meta's platforms are monetised directly through subscriptions at scale alongside advertising. Business tiers include WhatsApp AI for customer communications and Facebook business analytics — tools directly applicable to trades operators who rely on these platforms for quoting, client follow-up and marketing. The free tier remains available, but the AI capability gap between free and paid is widening.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/05/27/meta-officially-launches-instagram-facebook-and-whatsapp-subscriptions-with-more-to-come-including-ai-plans/",

    "{{TECH_2_FLAG}}": "🛒 AI · BUSINESS DISCOVERY",
    "{{TECH_2_HEADLINE}}": "AI-Driven Traffic to Business Websites Up 393% Year-on-Year — and Converts 42% Better Than Paid Search",
    "{{TECH_2_SUMMARY}}": "Q1 2026 data shows AI-generated referral traffic to retail and business websites grew 393% year-on-year, and visitors arriving via AI tools — conversational search, shopping assistants, AI recommendations — convert into sales at a 42% higher rate than traffic from paid search or email campaigns. The data confirms a structural shift: AI-sourced customer discovery rewards well-structured, accurate business information and strong review profiles over traditional keyword tactics. For trades operators, this means your Google Business profile, service descriptions and review volume are now commercially more important than ever — AI tools use them as the primary source when matching customers to service providers.",
    "{{TECH_2_URL}}": "",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🧠 BCI · PHYSICAL ROBOTICS",
    "{{ROBOT_1_HEADLINE}}": "Neuralink User Closes 2026 Robotics Summit With Live Brain-Controlled Demo — 5,000 Developers Give Standing Ovation",
    "{{ROBOT_1_SUMMARY}}": "Noland Arbaugh — the world's first Neuralink brain-computer interface user — delivered the closing demonstration at the 2026 Robotics Summit & Expo in Boston on May 28, controlling digital interfaces in real-time using only neural implant signals — drawing a standing ovation from 5,000+ robotics developers. Arbaugh was paralysed in a diving accident; his Neuralink implant translates neural signals into cursor and interface commands. The demonstration closed a summit (May 27–28) themed around the convergence of AI, BCI, and physical robotic systems toward machines that execute human intent without explicit programming. Amazon Vulcan — the touch-sensing warehouse robot — was named Robot of the Year.",
    "{{ROBOT_1_URL}}": "https://www.techtimes.com/articles/317330/20260528/robotics-summit-2026-wraps-neuralink-users-live-demo-closes-boston-show.htm",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Sues 3M for $1.43 Billion in Largest-Ever Government Claim — PFAS Contamination at 28 Defence Bases",
    "{{AUS_1_SUMMARY}}": "The Australian government lodged legal action against 3M on May 28 seeking A$2 billion ($1.43B USD) in damages over PFAS 'forever chemical' contamination at 28 defence bases — the largest claim ever filed by the Australian government. The Defence Department has already spent A$1.3B on remediation including A$408M in community legal settlements, treated 200,000 tonnes of contaminated soil, and processed 13 billion litres of water. 3M allegedly misrepresented the safety of its firefighting foam and withheld environmental risk data for decades. 3M says it never manufactured PFAS in Australia and ceased local sales around 20 years ago.",
    "{{AUS_1_URL}}": "https://www.cnn.com/2026/05/28/business/australia-3m-legal-action-intl-hnk",

    "{{AUS_2_HEADLINE}}": "Chalmers Tables Negative Gearing and CGT Reform Legislation — Investor Rules Change From 2027-28",
    "{{AUS_2_SUMMARY}}": "Treasurer Jim Chalmers this week introduced legislation implementing two major budget measures: negative gearing limited to new residential builds only from 2027-28 (existing investments grandfathered), and the 50% CGT discount replaced with inflation-indexed gains taxed at a minimum 30% rate from July 2027. The reforms are projected to raise tens of billions over the decade and shift investor incentives toward new construction. For trades operators in renovation and upgrade work, the shift in investor behaviour toward new builds — rather than existing property improvement — is worth tracking as a medium-term pipeline signal.",
    "{{AUS_2_URL}}": "",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Suburban Rail Loop East TBMs Arrive in Melbourne — Major Tunnelling Begins in 2026, Six Stations by 2035",
    "{{VIC_1_SUMMARY}}": "Tunnel boring machines have arrived in Melbourne for the Suburban Rail Loop East project, with major tunnelling due to begin in 2026 on the 26km twin-tunnel alignment delivering six new underground stations: Cheltenham, Clayton, Monash, Glen Waverley, Burwood and Box Hill. At Clayton — the future transport super-hub connecting Cranbourne, Pakenham and Gippsland lines — 500+ metres of diaphragm walls are installed and station box excavation is commencing. SRL East is Australia's largest current infrastructure project. For trades operators in Melbourne's southeastern suburbs, it represents a substantial and growing civil, structural, services and protective coatings pipeline running through to 2035.",
    "{{VIC_1_URL}}": "",

    # Science
    "{{SCI_1_FLAG}}": "🧬 NEUROSCIENCE · PARKINSON'S",
    "{{SCI_1_HEADLINE}}": "Scientists Identify the Brain Protein That Spreads Parkinson's Disease — Blocking It With Antibodies Stops the Cascade",
    "{{SCI_1_SUMMARY}}": "Penn Medicine researchers discovered that GPNMB — a protein released by the brain's own immune cells (microglia) in response to neuron damage — acts as a carrier enabling Parkinson's disease pathology to spread between neurons. The mechanism: GPNMB facilitates uptake of toxic alpha-synuclein protein clumps into healthy neurons, propagating the disease. Antibodies blocking GPNMB halted this cascade in laboratory experiments. Critically, the team validated the mechanism in 1,675 human brain samples from Penn's Brain Bank — people carrying variants linked to higher GPNMB production showed significantly more widespread damage at death. Published in Neuron (ScienceDaily, 27 May 2026). No drug currently slows Parkinson's progression; this could change that.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "EOFY Is 32 Days Away — Here's How AI Can Close Your Financial Year Without the Scramble",
    "{{INSIGHT_BODY}}": "By June 30, every completed job needs to be invoiced, every receipt categorised, and every deductible asset purchase documented. For most small trades operators, EOFY becomes a four-week sprint driven by deadline anxiety rather than a methodical process — and that costs money, either in missed deductions or in accountant time spent chasing documentation. AI can change that, but only if you start now. Concretely: use an AI tool to draft a deductions checklist from your transaction history; have it write follow-up messages for every outstanding invoice over 30 days (the conversations most operators avoid); ask it to identify equipment, tools or vehicle purchases this financial year that qualify for the $20,000 instant asset write-off; and use it to convert completed job notes into a billable-hours summary your accountant can use without ringing you. Two time-sensitive items this year: the fuel excise cut reverts June 30, so fuel-related deductions at the lower net cost should be captured now; and the ATO is scrutinising work-related expenses in trades, so documentation quality matters. That 20-minute AI session today could easily be worth $2,000 in additional deductions and saved accountant hours. Start the week you still have time.",

    # Fun Facts
    "{{FACT_1}}": "The number zero — fundamental to every trade invoice, bank balance and computer operation — wasn't accepted in European commerce until the 12th century. Hindu mathematician Brahmagupta defined zero's arithmetic rules in 628 AD. When Arabic traders brought the system west, Florence actively banned zero from commercial bookkeeping in 1299, viewing it as dangerous and deceptive. It took until the Renaissance for European merchants to fully adopt it.",

    "{{FACT_2}}": "Canberra became Australia's capital as a deliberate compromise between Sydney and Melbourne, both of which refused to cede the title to the other. The Australian Constitution mandated the capital be in New South Wales but at least 100 miles from Sydney — a condition so specifically awkward it guaranteed a greenfield site would be selected. The winner was a sheep and cattle station in the Monaro tablelands, purpose-built into a planned city from 1913.",

    "{{FACT_3}}": "The world's most accurate timekeepers — optical lattice clocks — would gain or lose less than one second over 300 billion years, longer than the current age of the universe. They are sensitive enough to measure the difference in the rate of time between the floor and a desk, because gravity causes time to run fractionally slower closer to a mass — a direct consequence of Einstein's general relativity, now measurable at centimetre scale in a laboratory.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the hydraulic mechanic never panic when things went wrong on site?",
    "{{JOKE_PUNCHLINE}}": "He knew how to handle everything under pressure.",

    # Closing
    "{{CLOSING_QUOTE}}": "“I find that the harder I work, the more luck I seem to have.”",
    "{{CLOSING_ATTR}}": "— Thomas Jefferson",
    "{{CLOSING_MESSAGE}}": "Friday 29 May — end of the working week in Carrum Downs, with a shower or two possible today and a wetter weekend on the way. Rain is forecast from Saturday afternoon into Sunday, so any outdoor work planned for the weekend is better moved to today. Household spending data released yesterday points to real cracks in consumer confidence — worth keeping an eye on the renovation pipeline over the next quarter. EOFY is 32 days away and the fuel excise reversal is ticking down; today's economics section has the numbers you need before you quote another job for post-July delivery. The Longview paper mill implosion in Washington is a sobering reminder of why chemical storage risk matters — 11 workers still unaccounted for three days in. Have a great Friday, Liall.",
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
