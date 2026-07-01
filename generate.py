#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 02 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 2 Jul
    "{{WEATHER_1}}": "THU 2 · 🌧 Showers, windy · 10–15°C",
    "{{WEATHER_2}}": "FRI 3 · 🌧 Showers continue · 10–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 4 · ☔ Shower or two · 9–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 5 · ⛅ Isolated early shower · 9–14°C",
    "{{WEATHER_5}}": "MON 6 · ☀️ Sunny, frosty start · 5–14°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS TODAY & FRIDAY · PUMP PRICES RISE THIS WEEK",

    # World
    "{{WORLD_1_FLAG}}": "🇿🇦 SOUTH AFRICA · UNREST · 900+ ARRESTED",
    "{{WORLD_1_HEADLINE}}": "Over 900 Arrested as Anti-Migrant Protests Sweep South Africa in the Country's Largest Unrest Since 2008",
    "{{WORLD_1_SUMMARY}}": "South African police confirmed more than 900 arrests after nationwide anti-migrant protests over June 30 and July 1, the largest coordinated action of its kind since 2008. Of 120 organised marches, 108 stayed peaceful while about a dozen tipped into looting, prompting the military to be placed on standby and troops sent to back up police in Johannesburg's Hillbrow area. The protests followed a citizen-set 'deadline' for undocumented migrants to leave, sending thousands scrambling to consulates and shelters — a reminder that economic anxiety finds a target everywhere, not just here.",
    "{{WORLD_1_URL}}": "https://www.nbcnews.com/world/africa/south-africa-arrests-nationwide-anti-migrant-protests-rcna352529",

    "{{WORLD_2_FLAG}}": "🌐 MIDDLE EAST · STRAIT OF HORMUZ · SHIPPING WORKAROUND",
    "{{WORLD_2_HEADLINE}}": "US and Gulf Allies Quietly Build a Workaround Shipping Route as Iran Keeps Squeezing the Strait of Hormuz",
    "{{WORLD_2_SUMMARY}}": "Four months after the US-Israel strikes on Iran, Tehran's Revolutionary Guard is still harassing shipping through the Strait of Hormuz, so Washington and Gulf partners — Oman chief among them — are quietly assembling an alternative southern corridor to keep oil and gas moving. The strait normally carries around a quarter of the world's seaborne oil trade, so every week of disruption keeps upward pressure on global energy prices. It's the slow-burn story sitting underneath every fuel price rise this year, including the one at the local bowser this week.",
    "{{WORLD_2_URL}}": "https://www.foxnews.com/politics/iran-fights-keep-grip-hormuz-us-gulf-allies-carve-new-shipping-route",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL EXCISE · DISCOUNT HALVES · BOWSER PRICES RISE",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Discount Halves From July 1 — Petrol and Diesel Set to Rise Up to 16c a Litre This Week",
    "{{ECON_1_SUMMARY}}": "The temporary fuel excise relief that's kept pump prices in check since April was cut in half, from 32 cents a litre to 16 cents a litre, on July 1, running through to August 2 — and retailers are already passing the difference on. NRMA and AIP pricing data show regular unleaded and diesel both edging up as much as 16 cents a litre across capital cities this week, with Sydney unleaded already averaging above 150c/L before the rise fully flows through nationally. For any trades business running a ute, van or truck fleet, it's worth re-checking fuel budgets now rather than after the next full tank — the discount still applies, it's just half what it was a fortnight ago.",
    "{{ECON_1_URL}}": "https://www.pm.gov.au/media/additional-fuel-excise-relief-month-july",

    "{{ECON_2_FLAG}}": "💰 PAYDAY SUPER · NEW COMPLIANCE RULE · STARTS THIS WEEK",
    "{{ECON_2_HEADLINE}}": "Payday Super Is Now Law — Employers Must Pay Super Within 7 Days of Every Payday, Not Quarterly",
    "{{ECON_2_SUMMARY}}": "From the first payday on or after July 1, every Australian employer is legally required to pay superannuation guarantee contributions within seven business days of paying wages, replacing the old quarterly cycle. The Fair Work Ombudsman has signalled a light touch on genuine first-time mistakes, but the change is real: it tightens cash flow timing for any small business used to holding onto super contributions for weeks before the old quarterly due date, so it's worth checking your payroll software has actually switched over rather than assuming it has.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 MICROSOFT · COPILOT · SMALL BUSINESS PLANS LIVE",
    "{{TECH_1_HEADLINE}}": "Microsoft Bakes Copilot Directly Into Its Small Business 365 Plans From This Week",
    "{{TECH_1_SUMMARY}}": "Microsoft 365 Business Standard and Business Premium with Copilot went generally available this week, building AI directly into Word, Excel, PowerPoint and Outlook rather than selling it as a separate add-on. A new 'Work IQ' feature lets the AI pull real context from a business's own emails, files and calendar instead of answering generically, and the plans now connect to more than 1,000 external tools including accounting software. For any small operator already paying for Microsoft 365, it's a sign the AI layer is quietly becoming standard-issue rather than a premium extra.",
    "{{TECH_1_URL}}": "https://www.microsoft.com/en-us/microsoft-365/blog/2026/05/28/introducing-microsoft-365-business-with-copilot-the-new-standard-for-small-business/",

    "{{TECH_2_FLAG}}": "🤖 ANTHROPIC · CLAUDE SONNET 5 · NOW THE FREE DEFAULT",
    "{{TECH_2_HEADLINE}}": "Claude Sonnet 5 Becomes the Default Free AI Model for Every User, No Upgrade Required",
    "{{TECH_2_SUMMARY}}": "Anthropic made its newest model, Claude Sonnet 5, the automatic default for every Free and Pro user on Claude.ai this week, rather than gating it behind a paid tier. The company says it closes in on flagship-level performance for everyday tasks like drafting, summarising and research at a fraction of the running cost of top-tier models — good news for any small business using AI chat tools for quotes, emails and admin without paying for the most expensive plan.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 CHINA · AGIBOT · PRODUCTION SCALE",
    "{{ROBOT_1_HEADLINE}}": "AGIBOT's 15,000th Robot Rolls Off the Line as Chinese Manufacturers Shift From Prototyping to Mass Production",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics maker AGIBOT marked its 15,000th unit rolling off the production line in the past week — an industrial-grade embodied-AI robot built for factory work. The production curve is the real story: it took roughly a year to go from 1,000 to 5,000 units, then just three months to jump from 5,000 to 10,000, and now on to 15,000. It's a Chinese factory milestone rather than an Australian one, but it's a clear signal of how fast the humanoid and industrial robot supply chain is scaling once a manufacturer moves past the prototype stage.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/agibot-produces-15000th-robot-marking-milestone-embodied-ai-deployment/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia's New Anti-Price-Gouging Law for Supermarkets Takes Effect",
    "{{AUS_1_SUMMARY}}": "From July 1, it's illegal for supermarkets with over $30 billion in annual revenue — in practice, just Coles and Woolworths — to charge prices that are 'significantly excessive' relative to their cost of supply, with fines up to $10 million enforced by the ACCC. Legal experts are already flagging that 'significantly excessive' is a hard test to prove in court, so don't expect grocery bills to fall overnight.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/australia-price-gouging-laws-grocery-bills-explained/2jakzlnvp",

    "{{AUS_2_HEADLINE}}": "BAE Systems Begins Delivery on Australia's Largest-Ever Defence Export Deal",
    "{{AUS_2_SUMMARY}}": "BAE Systems Australia formally began delivery work this week under a $2.5 billion government-to-government deal exporting Australia's Over-the-Horizon Radar technology to Canada for an Arctic early-warning system. Built on the proven JORN radar network, the deal supports around 300 high-value technical jobs locally — a reminder that Australian-made 'boring' infrastructure tech still punches above its weight overseas.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Bans Forced NDAs in Workplace Sexual Harassment Settlements, a First for Australia",
    "{{VIC_1_SUMMARY}}": "From this week, Victorian employers can no longer make a worker sign a non-disclosure agreement as a condition of settling a workplace sexual harassment complaint — under the new law, an NDA is only valid if the complainant asks for one themselves, after being clearly told their rights. It's the first law of its kind in Australia, and any Victorian employer with staff should flag it with whoever handles HR, because the old 'sign this and it goes away' approach is no longer lawful.",

    # Science
    "{{SCI_1_FLAG}}": "🧬 SYNTHETIC BIOLOGY · UNIVERSITY OF MINNESOTA",
    "{{SCI_1_HEADLINE}}": "Scientists Build the First Fully Synthetic Cell With a Complete Life Cycle",
    "{{SCI_1_SUMMARY}}": "Researchers at the University of Minnesota have built a synthetic cell, nicknamed 'SpudCell,' assembled entirely from non-living chemical components rather than modified from an existing organism. It can feed itself, grow by fusing with lipid droplets, replicate its roughly 90-kilobase genome, and divide into daughter cells for about five generations, even showing early signs of natural selection as its genetic makeup shifts across generations. Lead researcher Kate Adamala wryly calls it 'an incredibly wimpy organism' — it basically just eats and occasionally reproduces — but as a proof of concept for how primitive life might bootstrap itself from basic chemistry, it's a genuine landmark.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Victoria Just Banned Forced NDAs in Harassment Settlements — How AI Can Get Your Policies Compliant Before It Costs You",
    "{{INSIGHT_BODY}}": "Most small trades businesses haven't looked at their workplace complaint-handling policy since the day it was first drafted, and Victoria's new ban on forced NDAs in sexual harassment settlements means that document is now out of date whether you've ever had a complaint or not. The rule itself is simple — you can no longer make an NDA a condition of settling a complaint — but the practical fallout is a policy and process update most operators don't have a template for. This is a genuinely good use for AI: feed it your existing workplace policy or induction pack and ask it to 'flag every clause that conflicts with Victoria's ban on forced NDAs in sexual harassment settlements and draft compliant replacement wording.' It won't replace a proper employment lawyer if a real complaint ever lands, but it will get you from 'haven't looked at this in years' to 'basically compliant' in about twenty minutes — twenty minutes better than finding out the hard way.",

    # Fun Facts
    "{{FACT_1}}": "Welding is roughly 5,000 years old — Sumerian metalworkers in Mesopotamia were hard-soldering bronze for swords around 3000 BC, while Egyptian smiths of the same era forge-welded sponge iron by hammering heated metal together over charcoal, long before anyone thought to weld a steel frame.",

    "{{FACT_2}}": "Compressed air at just 12 psi — a tenth of what comes out of a standard workshop air line — is enough to blow an eye out of its socket if aimed at the face, and at 40 psi from close range it can rupture an eardrum. It's why 'never point it at yourself or anyone else' is rule number one around any air compressor.",

    "{{FACT_3}}": "Brain freeze is your body defending its favourite organ — the stabbing headache from wolfing down ice cream too fast happens because sudden cold against the roof of your mouth makes blood vessels feeding the brain rapidly constrict and rebound, a reflex your body shares with its response to actual head trauma. It's harmless, but it's technically your skull's alarm system firing a false positive.",

    # Joke
    "{{JOKE_SETUP}}": "A small business owner asked her AI assistant to draft a follow-up email chasing an overdue invoice.",
    "{{JOKE_PUNCHLINE}}": "The AI came back with three drafts — polite, firm, and 'unhinged 2am energy' — and she realised the hardest part of running the business was picking which version of herself to send.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Indomitable perseverance in a business, properly understood, always ensures ultimate success.”",
    "{{CLOSING_ATTR}}": "— Cyrus McCormick",
    "{{CLOSING_MESSAGE}}": "It's day two of FY2027, and the fuel excise cut just halved — expect a few extra cents at the pump this week, alongside the first Payday Super pay cycle for anyone paid today. Showers roll through Carrum Downs today and tomorrow before a proper wet weekend, so if there's an indoor job or a quoting pile that's been waiting on you, today's a good day for it. Whatever new-financial-year admin is still sitting open, it's only day two — plenty of time to close it out properly instead of rushing it.",
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
