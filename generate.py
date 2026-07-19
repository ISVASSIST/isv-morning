#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 20 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 20 Jul (BOM)
    "{{WEATHER_1}}": "MON 20 · ☀️❄️ Morning frost near the hills, then mostly sunny · 5–16°C",
    "{{WEATHER_2}}": "TUE 21 · 🌫️⛅ Morning fog near the hills, partly cloudy · 6–15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "WED 22 · 🌦️ Showers likely, possible small hail (SE suburbs) · 7–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 23 · 🌦️ Showers likely, hail chance (SE suburbs) · 6–14°C",
    "{{WEATHER_5}}": "FRI 24 · ☁️ Cloudy, medium chance of showers · 6–14°C",
    "{{WEATHER_ALERT}}": "⚠ MORNING FROST TODAY, FOG TUESDAY · SHOWERS & POSSIBLE HAIL WED–FRI · NO SEVERE WARNINGS ACTIVE",

    # World
    "{{WORLD_1_FLAG}}": "🇯🇴🇮🇶 IRAN WAR · EIGHTH STRAIGHT NIGHT · NUCLEAR PLANT AND KUWAIT HIT AGAIN",
    "{{WORLD_1_HEADLINE}}": "US Strikes Iran for an Eighth Consecutive Night as Washington Mourns Troops Killed in Jordan and Tehran Hits an Under-Construction Nuclear Plant",
    "{{WORLD_1_SUMMARY}}": "US forces carried out a fresh wave of strikes on Iranian military infrastructure overnight, avenging two soldiers killed and one still missing after Friday's Iranian attack on a base in Jordan, with a further service member killed in Iraq on Saturday. Iran responded by striking an under-construction nuclear power plant and hitting Kuwait's power and desalination network for the second time in two days, while its foreign ministry declared the ceasefire memorandum 'suspended' — no large tanker has broadcast a crossing of the Strait of Hormuz since 15 July, a chokepoint that normally carries a fifth of the world's oil.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/liveblog/2026/7/19/iran-war-live-us-launches-new-strikes-trump-mourns-killed-soldiers",

    "{{WORLD_2_FLAG}}": "🇺🇸🇬🇧 MIAMI · TATE BROTHERS ARRESTED · NEW UK RAPE AND TRAFFICKING CHARGES",
    "{{WORLD_2_HEADLINE}}": "Andrew and Tristan Tate Arrested in Miami as the UK Crown Prosecution Service Files a Fresh Wave of Rape and Trafficking Charges",
    "{{WORLD_2_SUMMARY}}": "US Marshals took the influencer brothers into custody in Miami on Saturday, acting on a UK extradition request that now includes seven additional counts of rape and three of arranging or facilitating sex trafficking against Andrew, and two counts of rape and a trafficking count against Tristan, covering alleged offences dating back to 2010. Both men, who built vast followings selling business and 'masculinity' content to young men, are awaiting an extradition hearing while denying all charges through their lawyers.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/7/19/tate-brothers-arrested-in-miami-as-uk-adds-rape-trafficking-charges",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL SUPPLY · 174 STATIONS DRY NATIONWIDE · INDEPENDENTS HIT HARDEST",
    "{{ECON_1_HEADLINE}}": "174 Australian Petrol Stations Are Reporting Outages as Hormuz Disruption and the Excise Restoration Squeeze Bowsers at Once",
    "{{ECON_1_SUMMARY}}": "Live tracking shows 174 service stations around the country — 237 individual fuel-type outages — currently out of at least one fuel type, with independent operators making up 63% of affected sites versus 37% for the major chains, and NSW and SA the worst-hit states. It's less a national shortage than a logistics squeeze — tanker delivery backlogs and import-terminal disruption layered on top of the 16c/L excise restoration that landed 1 July — but for a business running utes and compressors on diesel, it's another reason to keep the tank topped up rather than running to empty.",
    "{{ECON_1_URL}}": "https://petrolpulse.com.au/fuel-shortage",

    "{{ECON_2_FLAG}}": "🧾 ATO CRACKDOWN · $35.9B SMALL BUSINESS DEBT · GARNISHEES AND CREDIT REPORTING RAMP UP",
    "{{ECON_2_HEADLINE}}": "The Australian National Audit Office Finds Small Business Owes $35.9 Billion in Unpaid Tax, and the ATO Is Coming for It Harder",
    "{{ECON_2_SUMMARY}}": "A new ANAO report shows collectable small business tax debt has ballooned 118% since 2018-19 to $35.9 billion — two-thirds of everything owed to the ATO nationally — and the Tax Office is responding with more garnishee notices, Director Penalty Notices and disclosure of overdue debts to credit reporting agencies. None of this changes what you owe, but it does change how fast the ATO will come looking for it — worth a proactive call to your bookkeeper if a BAS or two has slipped behind.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔍 GOOGLE · AI MODE GOES ACTIONABLE · SEARCH NOW BOOKS AND BUYS FOR YOU",
    "{{TECH_1_HEADLINE}}": "Google Expands AI Mode in Search So It Can Take Actions Through Instacart, Canva and YouTube Music, Not Just Answer Questions",
    "{{TECH_1_SUMMARY}}": "Google has widened its AI Mode search feature for US users so that, instead of just summarising an answer, it can now complete tasks directly through partner apps — building a shopping cart on Instacart or generating a design in Canva from inside the search results. It's a small US rollout for now, but it's the clearest sign yet that search is shifting from 'find the answer' to 'do the task' — worth watching for when a similar action-taking search shows up on whatever tools your own business quoting or scheduling runs through.",
    "{{TECH_1_URL}}": "https://www.buildfastwithai.com/blogs/ai-news-today-july-18-2026",

    "{{TECH_2_FLAG}}": "💸 AI PRICING · THREE FLAGSHIPS IN 24 HOURS · TOKEN COSTS COLLAPSE",
    "{{TECH_2_HEADLINE}}": "A New AI Price War Just Pushed Flagship Model Costs Down to a Sixth of What They Were, as Grok 4.5, GPT-5.6 and Meta's Muse Spark All Launched Within a Day of Each Other",
    "{{TECH_2_SUMMARY}}": "SpaceX AI's Grok 4.5, OpenAI's cut-price GPT-5.6 'Luna' tier and Meta's Muse Spark 1.1 all shipped within 24 hours of one another this month, dragging output token costs down to roughly $4-6 per million compared with $25-50 for last year's flagships. For a small business dabbling in AI tools for quoting, emails or admin, the practical upshot is the same capability is quietly getting cheaper every few months — worth revisiting whatever you dismissed as 'too expensive' six months ago.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇺🇸🏭 SPARTANBURG · FIGURE'S BMW PILOT WRAPS · 90,000 PARTS, 1.2 MILLION STEPS",
    "{{ROBOT_1_HEADLINE}}": "Figure AI Wraps an Eleven-Month Humanoid Pilot at BMW's Spartanburg Plant, Having Loaded 90,000 Sheet-Metal Parts Without a Sick Day",
    "{{ROBOT_1_SUMMARY}}": "Figure AI's Figure 02 robot has completed an eleven-month pilot on BMW's Spartanburg production line, logging more than 1,250 operating hours, loading over 90,000 sheet-metal parts and clocking roughly 1.2 million steps while supporting production of more than 30,000 BMW X3s — one of a genuinely small handful of humanoid deployments doing real, documented, repetitive factory work rather than a demo reel. BMW is now folding lessons from the pilot into an expanded rollout of the newer Figure 03 model.",
    "{{ROBOT_1_URL}}": "https://www.technology.org/2026/07/18/humanoid-robots-in-2026-what-is-actually-deployed/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Government Adopts 35 of 54 Recommendations From Its Islamophobia Envoy, Including $41.9 Million for Mosque and School Security",
    "{{AUS_1_SUMMARY}}": "The Albanese government has formally responded to special envoy Aftab Malik's report on Islamophobia, adopting 35 of his 54 recommendations, including education campaigns to counter misinformation and $41.9 million to boost security at mosques, Islamic schools and other Muslim faith-based institutions. Malik's calls for an independent review of counter-terrorism laws and a commission of inquiry into Islamophobia and anti-Arab racism went unanswered, ten months after his report first landed on the government's desk.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/government-response-islamophobia-report-aftab-malik-2026/25cw8s7z9",

    "{{AUS_2_HEADLINE}}": "ACMA Pursues Telstra for Tens of Millions in Fines Over Its Nationwide Network Outage",
    "{{AUS_2_SUMMARY}}": "The Australian Communications and Media Authority told a Senate inquiry it is pursuing civil penalties that could run into the tens of millions of dollars against Telstra over last week's nationwide outage, which knocked out calls, texts and data for customers across the country. For any small business that leans on a single telco for eftpos, alarm monitoring or booking calls, it's a reminder that 'my carrier is down' is no longer a rare excuse — worth knowing your backup before it happens to you.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Police Investigate Fatal Monbulk Collision as Search Continues for Missing Ghin Ghin Kayaker",
    "{{VIC_1_SUMMARY}}": "A man has died following a head-on collision in Monbulk in Melbourne's outer east this morning, while police continue searching the Goulburn River near Ghin Ghin for a man who reportedly overturned in a kayak yesterday. A sober start to the week — worth taking it easy on wet or fog-affected roads this morning before conditions clear.",

    # Science
    "{{SCI_1_FLAG}}": "🦖☄️ PALAEONTOLOGY · DINO-KILLING ASTEROID ID'D · A RARE 'ODDBALL' FROM THE OUTER SOLAR SYSTEM",
    "{{SCI_1_HEADLINE}}": "Scientists Identify the Exact Rare Meteorite Type That Killed the Dinosaurs, and It Wasn't What Anyone Expected",
    "{{SCI_1_SUMMARY}}": "By analysing nickel isotopes preserved in debris from the Chicxulub impact, researchers from UBC, Paris, Brussels and Vienna have identified the dinosaur-killing asteroid as a rare CO chondrite — a class making up only a sliver of the roughly 5% of meteorites that are carbonaceous, likely originating from the outer solar system near Jupiter. Its low sulphur and carbon content suggests the mass extinction 66 million years ago was driven more by planet-cooling dust thrown into the atmosphere than by climate-wrecking gases baked into the rock itself, reshaping a decades-old assumption about exactly how the impact killed everything it did.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The ATO's Debt Recovery Just Got Personal — How AI Can Keep Your Books Off the $35.9 Billion Naughty List",
    "{{INSIGHT_BODY}}": "The tax office isn't just sending reminder letters anymore — garnishee notices straight to your bank, Director Penalty Notices, and disclosure of overdue debts to credit reporting agencies are all now standard tools once a BAS or two slips behind. AI-powered bookkeeping apps that reconcile daily and flag a looming shortfall weeks out, rather than at lodgement time, cost a fraction of what a garnishee notice or a damaged credit file will — the businesses landing in that $35.9 billion pile overwhelmingly aren't the ones dodging tax, they're the ones who lost track of cash flow one quarter at a time.",

    # Fun Facts
    "{{FACT_1}}": "The Great Emu War of 1932 saw the Australian Army deploy machine guns against emus in Western Australia to protect wheat crops from the birds — the emus won, and the failed operation is still taught as a textbook case of underestimating the enemy.",

    "{{FACT_2}}": "The 'over or under' toilet paper debate has an actual paper trail — Seth Wheeler's original 1891 patent diagram clearly shows the roll hanging over the front, which hasn't stopped the argument running for 135 years since.",

    "{{FACT_3}}": "The word 'algorithm' comes from the 9th-century Persian mathematician Muhammad ibn Musa al-Khwarizmi, whose Latinised name gave us 'algorithm' directly and whose book title, Kitab al-Jabr, gave us 'algebra' as a bonus.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the joiner refuse to trust a client's tape measure on a custom cabinet job?",
    "{{JOKE_PUNCHLINE}}": "Because 'near enough' has ruined more kitchens than bad timber ever has.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Little by little, one travels far.\"",
    "{{CLOSING_ATTR}}": "— J.R.R. Tolkien",
    "{{CLOSING_MESSAGE}}": "Monday starts frosty and sunny in Carrum Downs — 5–16°C — with fog settling in tomorrow and showers not due back until Wednesday, so it's a good window to get outdoor jobs done before the weather turns. Spain and Argentina's World Cup final wrapped up the tournament overnight, the Iran war ground into an eighth consecutive night of strikes, and the working week starts with the ATO tightening its grip on overdue debt — as good a Monday as any to get the books in order before anyone comes looking.",
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
