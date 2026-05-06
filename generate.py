#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 07 May 2026",

    # Weather — Carrum Downs VIC, 5-day outlook from Thu 7 May
    "{{WEATHER_1}}": "Thu 7 May · Showers · 12°C",
    "{{WEATHER_2}}": "Fri 8 May · Rain · 12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "Sat 9 May · Partly cloudy · 15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Sun 10 May · Partly cloudy · 14°C",
    "{{WEATHER_5}}": "Mon 11 May · Showers · 16°C",
    "{{WEATHER_ALERT}}": "⚠ Wet Thu–Fri · clearing Sat",

    # World
    "{{WORLD_1_FLAG}}": "🌐 MIDDLE EAST",
    "{{WORLD_1_HEADLINE}}": "Trump Pauses Hormuz Escorts as US–Iran Peace Talks Gain Ground",
    "{{WORLD_1_SUMMARY}}": "President Trump has halted the US Navy escort operation through the Strait of Hormuz, citing 'great progress' in negotiations with Iran mediated by Pakistan. Talks now cover freedom of navigation, Iran's nuclear programme, sanctions, and long-term peace. Iran's Foreign Ministry says it continues to exchange diplomatic messages via Islamabad but has not yet issued a formal response to Washington's latest proposal.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/5/6/has-the-us-accepted-irans-demand-to-settle-hormuz-first-nuclear-later",

    "{{WORLD_2_FLAG}}": "🇸🇾 INTERNATIONAL SECURITY",
    "{{WORLD_2_HEADLINE}}": "IS Group Families Repatriated to Australia After Years in Syrian Detention",
    "{{WORLD_2_SUMMARY}}": "Four women and nine children connected to IS fighters have arrived in Australia after years held in Syria's al-Roj camp. The Labor government says it played no role in organising the repatriation and that monitoring arrangements are already in place. The move follows years of legal pressure from families and human rights advocates.",
    "{{WORLD_2_URL}}": "https://www.sbs.com.au/news/podcast-episode/families-linked-to-is-group-fighters-returning-to-australia-midday-news-bulletin-6-may-2026/dmc0tq29z",

    # Economics
    "{{ECON_1_FLAG}}": "📋 FEDERAL BUDGET",
    "{{ECON_1_HEADLINE}}": "Federal Budget on 12 May — What Small Business Is Watching For",
    "{{ECON_1_SUMMARY}}": "Treasurer Chalmers delivers the federal budget in five days with a stated focus on restraint rather than large-scale stimulus. Expected measures include cost-of-living relief for households, an earned income offset for lower earners, and targeted support for energy costs. Small businesses are watching closely for any changes to instant asset write-off thresholds, fuel-related relief, and whether the excise cut beyond June 30 gets extended.",
    "{{ECON_1_URL}}": "https://www.smartcompany.com.au/federal-budget-2026/federal-budget-what-we-know-businesses-2026-fuel-negative-gearing-capital-gains/",

    "{{ECON_2_FLAG}}": "⛽ FUEL PRICES",
    "{{ECON_2_HEADLINE}}": "Petrol at 181c/L, Diesel at 246c/L — Excise Cut Expires June 30",
    "{{ECON_2_SUMMARY}}": "National average petrol sits at 181.3 cents per litre and diesel at 245.9 cents per litre this week. The government's fuel excise cut — halved to 26.3 cents — expires June 30. With Hormuz tensions still unresolved, a post-July price snapback is a real risk. Any jobs or contracts running past July should factor in a fuel cost contingency right now.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💰 AI INVESTMENT",
    "{{TECH_1_HEADLINE}}": "Google Commits Up to $40 Billion to Anthropic in Landmark AI Deal",
    "{{TECH_1_SUMMARY}}": "Google is investing $10 billion immediately into Anthropic — maker of the Claude AI — at a $350 billion valuation, with up to $30 billion more tied to performance targets. Anthropic has also committed to spend $200 billion on Google Cloud over five years, cementing Google as its primary compute partner. The deal mirrors a separate Amazon agreement, and signals that the big AI labs are locking in infrastructure partnerships for the decade ahead.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/04/24/google-to-invest-up-to-40b-in-anthropic-in-cash-and-compute/",

    "{{TECH_2_FLAG}}": "📉 AI & WORKFORCE",
    "{{TECH_2_HEADLINE}}": "Snap Cuts 1,000 Jobs — CEO Credits AI for Letting Smaller Teams Match Previous Output",
    "{{TECH_2_SUMMARY}}": "Snap CEO Evan Spiegel announced the layoff of approximately 1,000 employees, explicitly citing 'rapid advancements in artificial intelligence' that allow smaller teams to deliver the same work. The move signals what is becoming a structural shift across the tech sector: AI is not just a product — it is actively reshaping how many people a business needs to operate.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 HUMANOID PRODUCTION",
    "{{ROBOT_1_HEADLINE}}": "1X Opens America's First Vertically Integrated Humanoid Robot Factory in California",
    "{{ROBOT_1_SUMMARY}}": "Norwegian robotics firm 1X has opened its NEO Factory in Hayward, California — a 58,000 sq ft facility producing up to 10,000 general-purpose NEO home robots in 2026, scaling to 100,000 by 2027. First customer deliveries are planned for this year. Early-access pre-orders sold out within five days of launch, and every NEO rolls off the line powered by NVIDIA's Jetson Thor chip.",
    "{{ROBOT_1_URL}}": "https://www.globenewswire.com/news-release/2026/04/30/3285118/0/en/1x-opens-neo-factory-in-hayward-ca-americas-first-vertically-integrated-humanoid-robot-factory-with-consumer-shipments-planned-for-2026.html",

    # Australia
    "{{AUS_1_HEADLINE}}": "RBA Rate Now 4.35% — What Yesterday's Hike Means for Business Borrowers",
    "{{AUS_1_SUMMARY}}": "The day after the RBA's third 2026 rate hike, CBA economists say the bank now has room to pause — but Westpac still forecasts further rises in June and August. For small businesses on variable-rate equipment finance or business loans, the increase flows through within weeks. The key action item: review your loan structure before rates move again.",
    "{{AUS_1_URL}}": "https://www.commbank.com.au/articles/newsroom/2026/05/rba-may-interest-rates-cba-economists-analysis.html",

    "{{AUS_2_HEADLINE}}": "Royal Commission on Antisemitism Hears Jewish Families Fear for Children's Safety",
    "{{AUS_2_SUMMARY}}": "The Royal Commission on Antisemitism and Social Cohesion heard from Jewish parents who say they fear for their children's safety following the Bondi terror attack, with accounts of racial slurs and antisemitic abuse at schools and sporting venues. The commission is examining community safety, social cohesion, and the legal framework for addressing hate-based harm.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "South Side Festival Kicks Off in Frankston Tomorrow — Ten Nights of Arts and Culture",
    "{{VIC_1_SUMMARY}}": "The South Side Festival launches in Frankston from 8–17 May 2026, bringing ten nights of theatre, circus, dance, light installations, and community events. Neon Fields transforms Beauty Park into a glowing wonderland this weekend (8–10 May). Frankston is right next door — a solid option if you're looking for something on with the family this Saturday.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 CANCER TREATMENT · UK",
    "{{SCI_1_HEADLINE}}": "Nine-Week Immunotherapy Before Surgery Keeps Bowel Cancer Patients Relapse-Free for Nearly 3 Years",
    "{{SCI_1_SUMMARY}}": "A UK-led trial (NEOPRISM-CRC) gave 32 patients with stage 2–3 colorectal cancer nine weeks of pembrolizumab immunotherapy before surgery — replacing the usual post-surgery chemotherapy. After 33 months of follow-up, not one patient has relapsed. Standard care sees roughly 25% of similar patients relapse within three years. Results were presented at the American Association for Cancer Research annual meeting in San Diego.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How a Daily 10-Minute AI Debrief Can Save Your Business Thousands Each Year",
    "{{INSIGHT_BODY}}": "At the end of a long day on site, the last thing you want is more admin. But five to ten minutes dictating a site summary into an AI tool — what was done, what is outstanding, any variations or extra charges — can automatically generate job notes, update your quote, flag uncharged extras, and draft a client message. Over a year, tradespeople who build this habit typically recover thousands in missed charges and cut after-hours paperwork by hours each week. The entry point is low: voice memos on your phone, dropped into an AI, with a simple prompt to structure the debrief. It turns the drive home into productive time without a single minute of typing.",

    # Fun Facts
    "{{FACT_1}}": "Flamingos are born white — they turn pink from the carotenoid pigments in the brine shrimp and algae they eat. A flamingo kept away from its natural diet will gradually fade back to white, which is why zoos add special carotenoid supplements to their food.",
    "{{FACT_2}}": "Sound travels through steel approximately 15 times faster than through air — 5,120 m/s versus 343 m/s. Early railway workers would press an ear to the track to detect approaching trains long before the noise reached them through the air.",
    "{{FACT_3}}": "The smell of rain — petrichor — can be detected by the human nose at concentrations as low as 0.4 parts per trillion. The scent comes from geosmin, a compound released by soil bacteria when raindrops hit dry earth and kick microscopic particles into the air.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the glazier always win every negotiation?",
    "{{JOKE_PUNCHLINE}}": "He made his position perfectly clear.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\"",
    "{{CLOSING_ATTR}}": "Winston Churchill",
    "{{CLOSING_MESSAGE}}": "Cool and showery in Carrum Downs today — 12°C with rain expected through Friday before it clears for the weekend. Yesterday's RBA hike to 4.35% is now the new baseline, so if you have variable-rate finance, today is a good day to run the numbers. The federal budget lands in five days — know your margins before Chalmers sets the tone. Have a strong Thursday, Liall.",
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
