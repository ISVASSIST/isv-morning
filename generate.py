#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 17 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 17 May
    "{{WEATHER_1}}": "SUN 17 · ⛅ 19°C",
    "{{WEATHER_2}}": "MON 18 · 🌧️ 13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 19 · 🌦️ 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 20 · ⛅ 17°C",
    "{{WEATHER_5}}": "THU 21 · ☀️ 18°C",
    "{{WEATHER_ALERT}}": "COOL CHANGE TODAY",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇦 UKRAINE",
    "{{WORLD_1_HEADLINE}}": "Russia's Biggest Aerial Barrage Kills 24 in Kyiv Apartment Block — Zelenskyy Leads Day of Mourning",
    "{{WORLD_1_SUMMARY}}": "A Russian missile strike on Thursday night flattened a nine-storey apartment building in Kyiv's Darnytskyi district, killing 24 people including three children. It was part of Russia's largest two-day aerial assault of the war — more than 1,560 drones fired in 48 hours. Ukrainian President Zelenskyy visited the rubble, laid red roses, and led an official day of mourning with flags at half-mast across the city of three million. Western diplomats arrived in solidarity as rescue workers continued searching the ruins.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/05/15/nx-s1-5823388/death-toll-in-attack-on-kyiv-apartment-building-now-stands-at-24",

    "{{WORLD_2_FLAG}}": "⛽ HORMUZ",
    "{{WORLD_2_HEADLINE}}": "Ship Seized Near UAE, Another Sunk — Strait of Hormuz Tensions Reignite Despite Trump-Xi Commitment",
    "{{WORLD_2_SUMMARY}}": "A vessel anchored northeast of the UAE port of Fujairah was seized by unauthorised personnel Thursday and steered toward Iranian waters, while an Indian-flagged cargo ship sank near Oman after an attack sparked an onboard fire — all 14 crew rescued by Oman's coast guard. The UK Maritime Trade Operations authority confirmed both incidents, which occurred even as Trump was finalising a Hormuz shipping commitment with Xi in Beijing. The seizures raise immediate questions about whether any diplomatic agreement can hold while active interventions continue in the waterway.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/05/15/g-s1-122203/tensions-flare-near-strait-of-hormuz",

    # Economics
    "{{ECON_1_FLAG}}": "💼 SUPER",
    "{{ECON_1_HEADLINE}}": "Payday Super Kicks In From 1 July — Small Trades Now Have Six Weeks to Sort Out Payroll",
    "{{ECON_1_SUMMARY}}": "From 1 July 2026, employers must pay superannuation on payday rather than quarterly — a reform that fundamentally rewrites cash flow timing for every business running payroll. Industry modelling puts the average working capital adjustment at approximately $124,000 per employer as payments shift from periodic lump sums to continuous real-time obligations. The ATO's Small Business Superannuation Clearing House closes on 30 June, meaning any business still using it must migrate to a new platform in the next six weeks. CPA Australia is urging operators to act now to avoid a July 1 compliance shock.",
    "{{ECON_1_URL}}": "https://www.smallbusiness.nsw.gov.au/news-podcasts/news/payday-superannuation-what-small-businesses-need-to-know-ahead-of-1-july-2026",

    "{{ECON_2_FLAG}}": "🏠 BUDGET",
    "{{ECON_2_HEADLINE}}": "Budget 2026 Limits Negative Gearing to New Builds — Tradie Investors Need to Check Grandfathering Rules",
    "{{ECON_2_SUMMARY}}": "From 1 July 2027, residential investment properties purchased after 7:30pm on Budget night (12 May 2026) can only claim losses against rental income or property capital gains — not against wage or business income — unless the property is a new build. The 50% capital gains discount is replaced by a minimum 30% tax on inflation-adjusted gains, with existing holdings grandfathered under old rules. For tradespeople who own established investment properties, the change is significant and worth a conversation with your accountant before your next property decision.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📊 AI INDEX",
    "{{TECH_1_HEADLINE}}": "Generative AI Hit 53% Global Adoption in Three Years — Faster Than the PC or the Internet",
    "{{TECH_1_SUMMARY}}": "Stanford's 2026 AI Index confirms generative AI has reached majority global adoption faster than any comparable technology in history — 53% of the world's population within three years, versus roughly 15-18 years for the personal computer and 10 years for the internet. Enterprise adoption reached 88%. The report also flags a transparency risk: disclosure scores among the world's major AI developers dropped from 58 to 40, meaning tools are more powerful but their workings are less openly documented. AI workforce disruption has moved from prediction to documented reality — hitting young workers first.",
    "{{TECH_1_URL}}": "https://hai.stanford.edu/news/inside-the-ai-index-12-takeaways-from-the-2026-report",

    "{{TECH_2_FLAG}}": "🚢 AI AGENTS",
    "{{TECH_2_HEADLINE}}": "Virgin Voyages Scaled From 50 to 1,500 AI Agents in Four Months — and Then Posted Record Sales",
    "{{TECH_2_SUMMARY}}": "A case study presented at NVIDIA's GTC 2026 conference shows how fast agentic AI is moving from pilot to production: cruise operator Virgin Voyages expanded from 50 AI agents to more than 1,500 in just four months. Content production time fell 60%, promotional output doubled, and the months following deployment were the company's best sales period on record. The example is one of many from the GTC enterprise track showing AI now delivering measurable operational gains — not future potential, but documented present results.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 FIGURE AI",
    "{{ROBOT_1_HEADLINE}}": "Figure AI Robots Sort 88,000 Packages in 72-Hour Nonstop Livestream — Zero Human Intervention",
    "{{ROBOT_1_SUMMARY}}": "Figure AI's three Helix-02 humanoid robots — named Bob, Frank, and Gary by the hundreds of thousands of livestream viewers — sorted 88,000 packages over 72 continuous hours this week with no teleoperation and zero human interventions. The robots processed barcoded packages on conveyor belts at speeds CEO Brett Adcock says match human worker performance. The milestone drew viral attention as viewers watched the robots work through the night without breaks, errors, or restarts. It stands as one of the most significant public demonstrations of autonomous humanoid deployment in a real industrial setting to date.",
    "{{ROBOT_1_URL}}": "https://interestingengineering.com/ai-robotics/figure-ai-humanoids-24-hour-autonomous-run",

    # Australia
    "{{AUS_1_HEADLINE}}": "Budget Commits $53 Billion Extra to Defence — Australia to Reach 3% GDP Military Spending by 2033",
    "{{AUS_1_SUMMARY}}": "Australia's 2026-27 budget commits $53 billion in additional defence funding over the next decade, lifting military expenditure from around 2% to 3% of GDP by 2033 — the nation's largest peacetime defence commitment. The move reflects bipartisan recognition of Indo-Pacific strategic risk and sustained pressure from AUKUS and Five Eyes partners. For trades and construction businesses, sustained large-scale defence investment typically generates maintenance, upgrade, and facilities expansion contracts — particularly across South Australia, Queensland, and Western Australia.",
    "{{AUS_1_URL}}": "https://www.commbank.com.au/articles/newsroom/2026/05/2026-federal-budget-analysis-australian-economy.html",

    "{{AUS_2_HEADLINE}}": "Labor Holds Stafford By-Election — But LNP Swing Signals Budget Isn't Landing Everywhere",
    "{{AUS_2_SUMMARY}}": "Luke Richmond retained the Queensland state seat of Stafford for Labor in Saturday's by-election, but a notable swing toward the LNP has political analysts watching closely. With the next federal election within 18 months, the Stafford result is being read in Canberra as an early signal of how the Budget is landing in suburban electorates. National polling shows mixed favourability on the housing tax and payday superannuation announcements.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Art Book Fair Closes Today at NGV — Design Week Continues Through Sunday 24 May",
    "{{VIC_1_SUMMARY}}": "The Melbourne Art Book Fair — flagship event of Melbourne Design Week's 10th birthday edition — wraps up today at NGV International's Great Hall after three days of local and international publishers, typography installations, and design talks. Melbourne Design Week continues through Sunday 24 May with more than 400 events citywide, including exhibitions, keynote talks, and workshops. Entry to the majority of events is free. Full program at designweek.melbourne.",

    # Science
    "{{SCI_1_FLAG}}": "🦴 PALAEOANTHROPOLOGY",
    "{{SCI_1_HEADLINE}}": "Ethiopian Fossils Confirm Early Humans and a Previously Unknown Ancestor Shared the Same Ground 2.6 Million Years Ago",
    "{{SCI_1_SUMMARY}}": "A major fossil study published this week confirms that early Homo and a previously unknown Australopithecus species coexisted at the Ledi-Geraru site in Ethiopia's Afar region between 2.6 and 2.8 million years ago. Rather than a linear ape-to-human progression, the evidence now points to at least four distinct hominin lineages living simultaneously in eastern Africa during this critical period — a crowded, branching evolutionary tree. The find was led by an international team including researchers from the University of Chicago and University of Arkansas, and rewrites the first chapter of human evolution.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Every Job Is a Data Point — How AI Is Helping Trades Build Smarter Estimating Engines",
    "{{INSIGHT_BODY}}": "Every quote you have sent, every job you have finished, and every cost variation you have absorbed is information most trades businesses throw away once the invoice closes. AI tools can now ingest that job history — from invoices, job notes, time records, and supplier costs — and build a continuously improving cost model specific to your operation. Over time, your estimates stop being educated guesses and start being data-driven forecasts calibrated to your actual margins, crew output rates, and real supplier pricing. The result is not just more accurate quotes — it is the ability to spot the jobs that consistently underperform before you have committed to them. Start small: export your last 50 closed jobs into a spreadsheet and ask an AI tool what patterns it finds in your margin variation. The answer will likely surprise you.",

    # Fun Facts
    "{{FACT_1}}": "Oxford University is older than the Aztec Empire. Teaching has been recorded at Oxford since 1096, and the university was well established by 1167 — more than 260 years before the Aztec Empire was founded in 1428. When Aztec engineers were laying the first stones of Tenochtitlán, Oxford had already been producing graduates for two centuries.",
    "{{FACT_2}}": "Crows can recognise individual human faces, hold grudges for years against people who have wronged them, and teach their offspring to do the same. University of Washington field experiments confirmed it: crows repeatedly dive-bombed specific researchers who had handled them — even when those researchers wore completely different clothing — while ignoring nearby strangers. The behaviour spread socially through family groups across multiple seasons.",
    "{{FACT_3}}": "Tetris was created by Soviet computer engineer Alexey Pajitnov in 1984 while working at the Soviet Academy of Sciences in Moscow — making it the first software to be legally exported from the USSR to the West. Pajitnov received no royalties for 12 years: all proceeds went to the Soviet government. Licensing rights finally reverted to him in 1996, by which point Tetris had already sold over 35 million copies on Game Boy alone.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the waterproofer always have the last word in every site meeting?",
    "{{JOKE_PUNCHLINE}}": "No matter what came up, he had it covered.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Don't judge each day by the harvest you reap but by the seeds that you plant.\"",
    "{{CLOSING_ATTR}}": "Robert Louis Stevenson",
    "{{CLOSING_MESSAGE}}": "Sunday morning in Carrum Downs — partly cloudy at 19°C today before a cold wet change pushes through overnight into Monday's 13°C. Melbourne Design Week runs through the 24th if you are heading into the city this week. Eurovision wrapped in Vienna last night — worth a check if you are curious who won. It has been a big week: a budget, a summit, a Kyiv mourning day, and 88,000 packages sorted by robots without a coffee break. The world keeps moving even on Sundays. Enjoy the quiet while it lasts, Liall.",
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
