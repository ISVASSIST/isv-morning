#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 30 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 30 Jun
    "{{WEATHER_1}}": "TUE 30 EOFY · 🌧 Rain likely · 10–14°C",
    "{{WEATHER_2}}": "WED 1 JUL · ☁ Cold start · 8–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 2 · ⛅ Partly cloudy · 9–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 3 · 🌤 Cool and dry · 10–14°C",
    "{{WEATHER_5}}": "SAT 4 · 🌤 Fine and mild · 11–15°C",
    "{{WEATHER_ALERT}}": "⚠ RAIN THIS AFTERNOON · EOFY ENDS MIDNIGHT",

    # World
    "{{WORLD_1_FLAG}}": "🌐 IRAN · STRAIT OF HORMUZ · VESSEL ATTACKED",
    "{{WORLD_1_HEADLINE}}": "Iran Fires on Singapore-Flagged Tanker in Strait of Hormuz as US Accuses Tehran of Direct Attack on Shipping",
    "{{WORLD_1_SUMMARY}}": "A Singapore-flagged vessel was struck in the Strait of Hormuz overnight, with US officials directly accusing Iran of firing on the ship — though Iranian officials have not claimed responsibility. The incident follows President Trump's accusation that Iran had violated its nuclear framework agreement, and Tehran's subsequent threat to halt negotiations entirely. The Strait carries roughly 20% of all globally traded oil; any sustained disruption would spike diesel prices worldwide within weeks. Australian importers and fuel-dependent trades operators would feel the impact quickly — particularly relevant given today marks the end of the Australian government's fuel excise reduction.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/",

    "{{WORLD_2_FLAG}}": "🇰🇷 SOUTH KOREA · TREASON VERDICT · 30 YEARS",
    "{{WORLD_2_HEADLINE}}": "Former South Korean President Yoon Suk Yeol Found Guilty of Treason — Sentenced to 30 Years on Top of Existing Life Sentence",
    "{{WORLD_2_SUMMARY}}": "South Korea's court handed down its verdict on June 29, finding former President Yoon Suk Yeol guilty of treason and abuse of power after his December 2025 attempt to declare emergency martial law and order military drones flown into North Korean territory. Yoon was sentenced to 30 years imprisonment, added to an existing life sentence. The verdict closes a period of severe political instability in one of East Asia's key economies and a major Australian trade and security partner — a South Korea back under stable democratic governance matters for the regional security environment that shapes Australian defence and export settings.",
    "{{WORLD_2_URL}}": "https://www.bbc.com/news/world-asia",

    # Economics
    "{{ECON_1_FLAG}}": "🗓️ EOFY TODAY · SBSCH CLOSES MIDNIGHT",
    "{{ECON_1_HEADLINE}}": "Small Business Super Clearing House Closes Tonight — 200,000 Businesses Must Have Alternative Systems Ready Before Tomorrow's First Pay Run",
    "{{ECON_1_SUMMARY}}": "The Small Business Superannuation Clearing House (SBSCH) shuts permanently at 11:59pm tonight as Payday Super takes effect from July 1. More than 200,000 Australian small businesses have been using the free ATO service to pay employee super contributions quarterly — that process ends today. From tomorrow, super must be paid within 7 business days of every payroll run, and businesses need payroll software with an integrated clearing house. If you haven't migrated yet, download your SBSCH transaction history today — it becomes inaccessible after midnight. Payroll providers including Xero, MYOB and Employment Hero offer compliant solutions, but the system must be set up before Wednesday's first pay run.",
    "{{ECON_1_URL}}": "https://www.smallbusiness.nsw.gov.au/news-podcasts/news/closure-of-the-small-business-superannuation-clearing-house-ahead-of-payday-super",

    "{{ECON_2_FLAG}}": "💰 SUPER CAP RISES · PAYDAY SUPER LIVE · FROM TOMORROW",
    "{{ECON_2_HEADLINE}}": "Super Concessional Cap Rises to $32,500 From July 1 — And Every Future Pay Run Now Triggers Super Within 7 Business Days",
    "{{ECON_2_SUMMARY}}": "Two superannuation changes arrive simultaneously at midnight: the annual concessional contribution cap rises from $30,000 to $32,500, and Payday Super begins — meaning super is paid alongside wages, not quarterly. For self-employed tradies, tonight is the last chance to make a personal concessional super contribution under the old $30,000 cap and claim the deduction in FY2026 returns — your fund must receive the transfer before 11:59pm. For employers: any wages paid from Wednesday must trigger a super payment within 7 business days. The ATO will apply penalties for late super from the very first payroll run — the informal grace period that existed under the old quarterly system is gone.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 ANTHROPIC · FABLE 5 · EXPORT BAN UPDATE",
    "{{TECH_1_HEADLINE}}": "Anthropic's Most Powerful AI Model Has Been Offline for 15 Days — Expected Back Within Days as Pentagon and NSA Negotiations Progress",
    "{{TECH_1_SUMMARY}}": "The Trump administration's export control directive — issued June 12 citing a potential jailbreak of Fable 5 — forced Anthropic to disable both Fable 5 and Mythos 5 globally, including for non-US customers. Axios reported June 27 that the situation is nearing resolution: Commerce Secretary Lutnick's letter cleared Mythos 5 for approximately 100 US institutions, with Pentagon and NSA sign-off on Fable 5 still outstanding as of June 28. For Australian businesses using Claude-based AI tools: no disruption has been reported to Australian accounts, as the export ban specifically targeted foreign nationals accessing the models — not downstream products sold through Anthropic's API. The episode underscores the risk of over-dependence on any single AI provider in an increasingly regulated global environment.",
    "{{TECH_1_URL}}": "https://www.anthropic.com/news/fable-mythos-access",

    "{{TECH_2_FLAG}}": "⚖️ COLORADO · AI CONSUMER LAW · EFFECTIVE TODAY",
    "{{TECH_2_HEADLINE}}": "World's First Comprehensive State AI Consumer Protection Law Takes Effect Today in Colorado — Australia's Regulators Are Watching Closely",
    "{{TECH_2_SUMMARY}}": "Colorado's Consumer Protections for Artificial Intelligence Act takes effect June 30, 2026 — the first comprehensive consumer-facing AI law in the world, requiring AI developers and deployers to disclose when consumers interact with AI systems and provide meaningful appeal rights for high-stakes AI decisions covering employment, housing, healthcare and financial services. While it applies to Colorado-based businesses and customers, Australia's ACCC and the Department of Industry's AI safety review have been closely tracking the Colorado framework as a likely template for domestic regulation. For trades businesses using AI tools for quoting, scheduling or client communication: start documenting what AI systems you use. That habit is heading to Australia.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 CHINA · MORGAN STANLEY · 50,000 HUMANOIDS 2026",
    "{{ROBOT_1_HEADLINE}}": "Morgan Stanley Doubles China's 2026 Humanoid Robot Forecast to 50,000 Units — Early Commercialisation Phase Has Officially Arrived",
    "{{ROBOT_1_SUMMARY}}": "Morgan Stanley published an updated market analysis this week doubling its 2026 forecast for Chinese humanoid robot shipments from 28,000 to 50,000 units — itself already a doubling from an earlier estimate of 14,000. The bank cites a single $1 billion State Grid order (8,500+ robots for power grid maintenance), accelerating factory deployments, and policy support under China's 15th Five-Year Plan. Morgan Stanley projects China's humanoid robot market reaching $2 billion this year and $15 billion by 2030, with annual shipments of 446,000 units by decade end. The numbers confirm the shift: humanoid robots are no longer a technology development story — they are a manufacturing and workforce story. The timeline for meaningful penetration of Australian industrial labour markets has moved materially forward.",
    "{{ROBOT_1_URL}}": "https://www.cnbc.com/2026/06/24/morgan-stanley-china-humanoid-robot-market-forecast.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Face Egypt in World Cup Round of 32 — Confirmed for Saturday July 4 at 4am AEST in Arlington, Texas",
    "{{AUS_1_SUMMARY}}": "Australia's World Cup knockout stage opponent is confirmed: Egypt, after a dramatic Group G finale in which Belgium beat New Zealand 5–1 to edge the Pharaohs on goal difference. The Socceroos finished second in Group D behind co-hosts the USA. It's the first meeting between the two nations at a FIFA World Cup. Kick-off is 4:00am AEST Saturday with free-to-air coverage on SBS and SBS On Demand from 3:00am. If you're setting the alarm, set two.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/fifa-world-cup-2026-socceroos-round-of-32-opponent/76wwjel32",

    "{{AUS_2_HEADLINE}}": "Last Hours to Top Up Super at the FY2026 Cap — Concessional Limit Resets at Midnight as EOFY Clock Runs Down",
    "{{AUS_2_SUMMARY}}": "June 30 is the final opportunity to make concessional superannuation contributions under the FY2026 cap of $30,000. From midnight, the cap resets to $32,500 for FY2027. Self-employed tradies and business owners with spare cash who haven't maximised their concessional contributions can still make a personal deductible contribution today — your fund must receive the transfer before close of business to guarantee it's received in time. Check your year-to-date total against your $30,000 cap before acting. Over-contributing incurs tax penalties, so confirm with your accountant if you're close to the limit.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Free Public Transport Scheme Ends Tonight — Half-Price Fares Continue Across Melbourne and Regional Network Through to December 2026",
    "{{VIC_1_SUMMARY}}": "The State Government's free public transport program closes tonight after its run as a cost-of-living measure. From tomorrow, fares apply across Melbourne trains, trams and buses — though the government has committed to maintaining half-price fares through to December 2026. For trades operators or employees using PT for site travel, MYKI cards must be charged from tomorrow to avoid tap-on penalties. Full fares don't return until 2027.",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ QUANTUM PHYSICS · FRACTIONAL FERMI SEA · NEW STATE OF MATTER",
    "{{SCI_1_HEADLINE}}": "Physicists Create a Brand-New Quantum State Called the 'Fractional Fermi Sea' — Goes Beyond Every Established Theory of Quantum Materials",
    "{{SCI_1_SUMMARY}}": "A team at the University of Innsbruck, working with CNRS theorists, has demonstrated that ultracold cesium atoms under one-dimensional confinement can be driven into a completely new quantum state — the 'fractional Fermi sea' — by cycling particle interactions. This exotic critical phase falls entirely outside the Tomonaga-Luttinger liquid theory that has been the backbone of quantum materials science for decades. Published June 29 in Physical Review Letters, the discovery opens new pathways for quantum simulation. Discoveries of entirely new phases of matter have a solid history of enabling future technology — superconductivity was found in 1911 and now underpins MRI machines and quantum computers. This one is earlier on that journey.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The Last Hours of FY2026: How to Use AI to Close Every Open Loop Before Midnight",
    "{{INSIGHT_BODY}}": "Today is June 30 — the financial year is over at midnight, and whatever hasn't been actioned before then doesn't count for FY2026. Most trades businesses have at least three or four loose ends still unresolved: an invoice that went out but was never followed up, a supplier credit that was promised but never processed, a piece of plant that was meant to be claimed but never made it into the bookkeeping system. AI won't file your tax return, but it will help you surface and close every one of those items in under an hour. Start with this prompt: 'I run a small trades business and today is the last day of the financial year. List every item I should check or action before midnight — outstanding invoices, supplier credits, asset purchases, personal super contributions, receipts to digitise, and anything I might have forgotten.' Work through the list with your accountant on call for anything that needs a decision. The businesses that come out of EOFY ahead aren't just the ones that prepared — they're the ones who made one final push on the day itself.",

    # Fun Facts
    "{{FACT_1}}": "WD-40 was invented on the 40th attempt — the name is not a brand invention but a literal record: the first 39 formulas failed. Rocket Chemical Company in San Diego developed it in 1953 to protect the outer skin of the Atlas Space Missile from rust and corrosion using a water displacement formula. Workers started smuggling cans home from the factory floor, which is how the company discovered its consumer appeal. The original formula has never been patented — deliberately — to stop competitors from simply reading the patent documentation and reverse-engineering it.",

    "{{FACT_2}}": "Quicksand doesn't suck you under — it's actually denser than the human body, so in real quicksand you'd sink roughly to waist depth and float there, not disappear. The genuine danger is becoming immobilised while a tide rises, or dehydrating if you can't work free. Real quicksand forms at riverbanks, beaches and coastal areas when water-saturated sand loses its load-bearing strength — it's genuinely common in parts of New Zealand's west coast and northern Australia. The quicksand-as-death-trap trope was so popular in 1960s cinema that it appeared in nearly three per cent of all films released that decade.",

    "{{FACT_3}}": "The Sydney Harbour Bridge has been painted approximately 16 times since it opened in 1932, using around 30,000 litres of paint per full coat. A complete repaint is estimated to take roughly 10 years of continuous work — meaning there is always a painting crew somewhere on the structure. The original 1932 zinc phosphate primer coat is still intact in sections and continues to protect the steel after more than 90 years, making it one of the most successful long-term applications of industrial protective coating in Australian engineering history.",

    # Joke
    "{{JOKE_SETUP}}": "How does a trades business owner know the financial year has officially ended?",
    "{{JOKE_PUNCHLINE}}": "The job they quoted in March finally gets approved — the day after June 30.",

    # Closing
    "{{CLOSING_QUOTE}}": "“A good plan today is better than a perfect plan tomorrow.”",
    "{{CLOSING_ATTR}}": "— Publilius Syrus, Roman writer, 1st century BC",
    "{{CLOSING_MESSAGE}}": "It's the last day of FY2026 — rain is expected this afternoon in Carrum Downs, which makes it a solid office day for closing the books rather than heading to site. Tonight at midnight: the SBSCH closes, the financial year ends, and July 1 brings the minimum wage at $26.44/hr, super at 12%, and Payday Super live from the first payroll run. On the brighter side, the Socceroos take on Egypt this Saturday at 4am AEST — get the SBS app ready and the alarm set for 3am. Keep one eye on the Strait of Hormuz situation today: if it escalates, diesel prices won't wait for the next monthly reporting cycle to move. Make the last hours of FY2026 count, Liall.",
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
