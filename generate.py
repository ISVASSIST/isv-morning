#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 01 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 1 Jul
    "{{WEATHER_1}}": "WED 1 · 🌤 Patchy frost, then sun · 2–17°C",
    "{{WEATHER_2}}": "THU 2 · 🌧 Rain, windy · 7–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "FRI 3 · 🌧 Rain continues · 6–12°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 4 · 🌦 Showers easing · 6–11°C",
    "{{WEATHER_5}}": "SUN 5 · 🌧 Showers, cool · 6–12°C",
    "{{WEATHER_ALERT}}": "⚠ RAIN ARRIVES THURSDAY · DAY ONE OF FY2027",

    # World
    "{{WORLD_1_FLAG}}": "🇻🇪 VENEZUELA · EARTHQUAKE · DEATH TOLL NEARS 2,000",
    "{{WORLD_1_HEADLINE}}": "Venezuela's Earthquake Death Toll Climbs Past 1,900 a Week On, With Tens of Thousands Still Missing",
    "{{WORLD_1_SUMMARY}}": "The death toll from the magnitude 7.2 and 7.5 earthquakes that struck near Caracas on June 24 has risen to 1,943, with more than 10,500 injured and over 46,000 people still reported missing, according to Venezuelan officials. Rescue teams are still pulling survivors from rubble a week on, though hope is fading as the search drags into its second week. The US Geological Survey's automated PAGER system has warned the final toll could climb far higher once the true scale of destruction in informal housing areas is known — a sobering reminder of how slowly the rebuild after a 30-second tremor actually happens.",
    "{{WORLD_1_URL}}": "https://www.nbcnews.com/world/venezuela/venezuela-earthquake-latest-death-toll-missing-rescues-la-guaira-rcna352179",

    "{{WORLD_2_FLAG}}": "🌐 IRAN · STRAIT OF HORMUZ · TALKS STALLED",
    "{{WORLD_2_HEADLINE}}": "Iran Refuses to Resume Ceasefire Talks Until US Meets Lebanon Conditions, Leaving Gulf Shipping in Limbo",
    "{{WORLD_2_SUMMARY}}": "Iran's Foreign Ministry said on June 30 it won't return to the negotiating table with Washington until the US implements clauses of their interim memorandum of understanding relating to Lebanon — nearly five months into the conflict. Maritime traffic through the Strait of Hormuz, which carries roughly 20% of the world's traded oil, slowed sharply again after weekend attacks on shipping, including a strike on a Qatari tanker that drew a US military response. A 60-day waiver allowing Iran to sell oil internationally remains in place under the June 17 interim deal, but the standoff means shippers and insurers are still pricing in serious risk — exactly the kind of disruption that flows through to diesel prices at home.",
    "{{WORLD_2_URL}}": "https://www.rferl.org/a/iran-war-us-hormuz-oil-blockade-gulf-israel/33640284.html",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL EXCISE · RELIEF EXTENDED · FROM TODAY",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Cut Extended to August — Petrol and Diesel Stay 16c/Litre Cheaper, Truckies Get Matching Road Charge Relief",
    "{{ECON_1_SUMMARY}}": "The federal government has extended its fuel excise relief for another month, keeping petrol and diesel 16 cents per litre cheaper than normal from today through to August 2, saving the average motorist around $11 a tank. The Heavy Vehicle Road User Charge has also been cut by 16 cents for the same period — a direct saving for any trades business running a ute, van or truck fleet. The relief has cost the federal budget close to $3 billion in foregone revenue since it began, and there's no commitment yet on what happens after August 2 — worth factoring into any fuel budgeting you do for the new financial year.",
    "{{ECON_1_URL}}": "https://www.pm.gov.au/media/additional-fuel-excise-relief-month-july",

    "{{ECON_2_FLAG}}": "💰 WAGES · MINIMUM WAGE RISES · EFFECTIVE TODAY",
    "{{ECON_2_HEADLINE}}": "National Minimum Wage Rises 4.75% to $26.44 an Hour From Today, While the $20,000 Instant Asset Write-Off Becomes Permanent",
    "{{ECON_2_SUMMARY}}": "The Fair Work Commission's 4.75% increase to award and minimum wages takes effect today, lifting the National Minimum Wage to $1,004.90 a week, or $26.44 an hour — a $56.90 weekly increase for any award-reliant staff. The Commission acknowledged the rise falls short of a genuine real wage increase given inflation running near 4.8%. On the other side of the ledger, the $20,000 instant asset write-off for small businesses with turnover under $10 million is now a permanent fixture rather than an annual budget announcement, and businesses that made a loss can carry it back to claim a refund against tax paid in the previous two years. Worth running both numbers through your FY2027 pricing today, not next quarter.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 ANTHROPIC · ENTERPRISE AI · GLOBANT ALLIANCE",
    "{{TECH_1_HEADLINE}}": "Globant Signs Multi-Year Alliance With Anthropic, Rolling Out Claude-Powered 'AI Pods' to 28,500 Staff",
    "{{TECH_1_SUMMARY}}": "IT services giant Globant announced a multi-year alliance with Anthropic on June 30, becoming a Preferred Services Partner in the Claude Partner Network and giving all 28,500 of its staff access to Claude along with Anthropic's certification training. The centrepiece is a new line of Claude-powered 'AI Pods' — specialised, agent-run service units already adopted by 40% of Globant's top 20 accounts — targeting tasks like content localisation, real-time booking and customer concierge work. It's another sign the AI conversation in big business has shifted from 'should we use it' to 'which parts of the job can an agent now run end-to-end' — the same question worth asking about your own quoting, scheduling and follow-up admin.",
    "{{TECH_1_URL}}": "https://www.stocktitan.net/news/GLOB/globant-announces-an-alliance-with-anthropic-to-redefine-enterprise-nyiuasjucqlb.html",

    "{{TECH_2_FLAG}}": "⚙️ GOOGLE · GEMINI 3.5 PRO · DELAYED TO JULY",
    "{{TECH_2_HEADLINE}}": "Google's Gemini 3.5 Pro Misses Its June Deadline as Anthropic's Fable 5 Nears Full Return From Export Suspension",
    "{{TECH_2_SUMMARY}}": "Google's flagship Gemini 3.5 Pro model has slipped past its promised June general-availability date and is now expected sometime in July, with the company citing unresolved token-efficiency issues and the fallout from several senior researchers departing for OpenAI and Anthropic. Meanwhile, Anthropic's most capable model, Claude Fable 5, remains suspended for general users under the US export control directive issued in mid-June, though reporting suggests Pentagon and NSA sign-off is close. For Australian businesses relying on frontier AI tools day to day, the practical takeaway is the same one that applies to suppliers and subcontractors: build in a backup, because even the biggest players are missing their own deadlines right now.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 CHINA · HUMANOID ROBOTS · RENTAL MARKET REALITY CHECK",
    "{{ROBOT_1_HEADLINE}}": "China's Booming Humanoid Robot Rental Market Is Exposing How Far the Technology Still Has to Go",
    "{{ROBOT_1_SUMMARY}}": "With more than 153,000 robot rental businesses now operating across China and the sector tipped to hit $1.5 billion by year's end, CNN's on-the-ground reporting this week found a less polished reality behind the viral videos: rows of humanoid robots performing single repetitive tasks — sorting packages, scooping popcorn — each guided by a human operator with a handheld controller standing right next to it. Even UBTECH, one of China's largest humanoid makers, admits its most advanced models hit only around 80% of human productivity, and only on narrow tasks like box stacking. Genuine industrial deployment still accounts for less than 10% of sales. The six-month payback headlines are real for a handful of tightly scoped jobs — but full autonomy on a messy job site remains some way off yet.",
    "{{ROBOT_1_URL}}": "https://edition.cnn.com/2026/06/30/tech/china-humanoid-robot-ai-rental-intl-hnk-dst",

    # Australia
    "{{AUS_1_HEADLINE}}": "Government to Double Social Media Fines to $99 Million After Admitting the Under-16s Ban Isn't Working",
    "{{AUS_1_SUMMARY}}": "The federal government will introduce legislation this week doubling the maximum fine for platforms like Facebook, Instagram, Snapchat and TikTok that fail to keep Australian children off their services, after eSafety found seven in ten under-16s who held accounts when the ban began in December still have them. Communications Minister Anika Wells put the blame squarely on the platforms' resistance to enforcing the age checks properly.",
    "{{AUS_1_URL}}": "https://www.npr.org/2026/06/29/nx-s1-5874576/australia-fines-child-social-media-accounts",

    "{{AUS_2_HEADLINE}}": "What Else Changes From Today: Lowest Tax Bracket Cut to 15%, $1,000 No-Receipts Deduction, Free Electricity Trial Begins",
    "{{AUS_2_SUMMARY}}": "Alongside the wage and super changes, the lowest marginal tax rate drops from 16% to 15% on income between $18,201 and $45,000 from today, and a new $1,000 instant deduction for work-related expenses replaces the old $300 receipt-free limit for FY2027 returns. Eligible households in NSW, South Australia and south-east Queensland can also opt into three hours of free electricity a day under the new Solar Sharer Offer.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Free Public Transport Officially Ends in Victoria — Half-Price Fares Now Locked In Through to January 2027",
    "{{VIC_1_SUMMARY}}": "Victoria's free public transport trial, which ran from March 31 to May 31 before a one-month extension, has now fully transitioned to half-price fares — a full daily MYKI fare across the state costs $5.70 instead of $11.40, with concession fares at $2.85. The discount runs to January 1, 2027 and covers trains, trams, buses and regional coaches, though not SkyBus or ferries. Separately, the Bureau has confirmed El Niño has officially returned to the state, pointing to a warmer, drier-than-average winter and spring across Victoria.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 NEUROSCIENCE · MENTAL HEALTH · CREATINE REVIEW",
    "{{SCI_1_HEADLINE}}": "New Review of Five Clinical Trials Finds Creatine May Ease Depression — But the Evidence Is Still a Coin Flip",
    "{{SCI_1_SUMMARY}}": "A new systematic review published this week examined five randomised clinical trials testing creatine supplementation as an add-on treatment for depression. Two trials, both in women with major depressive disorder, found creatine alongside standard treatment produced a meaningfully greater reduction in symptoms than therapy plus a placebo. The other three found no real benefit at all. Researchers say the overall effect is, at best, small to moderate and possibly trivial — international psychiatric bodies are recommending against using it as a depression treatment until better data comes in. A useful reminder that 'a study found' and 'this works' are two very different sentences.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Public Liability Renewal Season: How AI Can Stop You Sleepwalking Into a Bad Auto-Renewal",
    "{{INSIGHT_BODY}}": "Most trades insurance — public liability, contract works, tool cover — renews around the new financial year, and most of it auto-renews unless you actively intervene. The problem is most operators don't have time to read a 40-page Product Disclosure Statement against last year's, so the policy just rolls over, price increase and all, often with coverage that no longer matches the work you're actually doing now versus when you first took it out. AI is well suited to exactly this kind of unglamorous document comparison. Try this: photograph or scan both your current PDS and the renewal notice, then ask an AI tool to 'compare these two insurance documents and list every difference in coverage, exclusions, and price, in plain English.' It won't replace a broker for anything complex, but it will tell you in two minutes whether what's about to auto-renew on your card still covers what you're actually doing on site — before the payment goes through, not after a claim gets knocked back.",

    # Fun Facts
    "{{FACT_1}}": "The Compagnie Parisienne de l'Air Comprimé built the world's first citywide compressed-air power network in Paris from 1888, piping high-pressure air through tunnels to drive machinery, clocks and even small motors across the city — for several decades, parts of Paris ran on air pressure before they ran on electricity.",

    "{{FACT_2}}": "San Francisco's Boudin Bakery has kept the same sourdough starter alive and in continuous use since the California Gold Rush in 1849 — meaning the wild yeast culture in today's loaf is, genetically, more than 175 years old and has never been allowed to die out.",

    "{{FACT_3}}": "When AlphaGo played its famous 'Move 37' against world champion Lee Sedol in 2016, commentators initially thought the AI had made a mistake — it was so far outside conventional human strategy. It's now taught in professional Go academies as a genuine turning point in the game, not a glitch.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the signwriter never lose an argument with a difficult client?",
    "{{JOKE_PUNCHLINE}}": "Because he always made sure to get everything in writing — literally.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The secret of change is to focus all of your energy not on fighting the old, but on building the new.”",
    "{{CLOSING_ATTR}}": "— Socrates",
    "{{CLOSING_MESSAGE}}": "It's July 1 — day one of FY2027. The new minimum wage, Payday Super and the permanent $20K instant write-off all land today, while the fuel excise cut keeps the bowser 16 cents cheaper through to August. Rain moves into Carrum Downs from tomorrow and sticks around the whole weekend, so if there's an outdoor job that can move forward today, today's the day to do it. The Socceroos kick off against Egypt at 4am AEST on Saturday — set the alarm if you're keen. Whatever's still sitting in last year's column, leave it there: new quarter, new numbers, Liall.",
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
