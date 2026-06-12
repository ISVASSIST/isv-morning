#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 13 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 13 Jun
    # Rain and northerly winds Sat–Sun, clearing from Monday
    "{{WEATHER_1}}": "SAT 13 · 🌧 Rain · 13–16°C",
    "{{WEATHER_2}}": "SUN 14 · 🌧 Showers · 9–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 15 · ⛅ Clearing · 7–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "TUE 16 · ☁ Cloudy · 7–12°C",
    "{{WEATHER_5}}": "WED 17 · 🌤 Partly Cloudy · 5–12°C",
    "{{WEATHER_ALERT}}": "⚠ HEAVY RAIN & N WINDS TO 40KM/H SAT–SUN",

    # World
    "{{WORLD_1_FLAG}}": "🌐 MIDDLE EAST · CEASEFIRE",
    "{{WORLD_1_HEADLINE}}": "Iran-US Ceasefire Holds as Negotiators Say They Are '75% There' — But Tehran Insists Nothing Is Signed",
    "{{WORLD_1_SUMMARY}}": "The 60-day US-Iran ceasefire entered its second day as Trump declared the deal 'approved' and cancelled planned strikes. Pakistani PM Sharif posted that peace 'has never been this close,' citing direct involvement from Witkoff, Rubio, and Iranian President Pezeshkian. However, Iran's Foreign Minister Araqchi maintained no agreement had been formally concluded — with Tehran insisting on retaining uranium enrichment rights and control of Hormuz shipping. Negotiators say they are '75 percent there.' For Australian businesses, a genuine deal would release oil market pressure and push fuel prices back toward pre-crisis levels within weeks — but every false signal in this conflict has been followed by escalation. Watch the weekend carefully.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/liveblog/2026/6/12/iran-war-live-trump-claims-tehran-deal-approved-cancels-new-strikes",

    "{{WORLD_2_FLAG}}": "🇬🇧 UK · POLITICS",
    "{{WORLD_2_HEADLINE}}": "UK Defence Secretary John Healey Resigns Over Military Funding Shortfall — Sixth Starmer Minister Out in a Month",
    "{{WORLD_2_SUMMARY}}": "John Healey and Armed Forces Minister Al Carns quit on June 11 after Chancellor Rachel Reeves refused to increase defence spending beyond £12 billion — far short of the £18 billion Healey sought to meet rising NATO obligations. Healey said the settlement 'falls well short of what the nation needs at this dangerous time,' citing rising Russian and global threats. He became the sixth Starmer minister to resign in a single month and the 19th to leave government since Labour took power in July 2024. Dan Jarvis was immediately appointed Secretary of State for Defence.",
    "{{WORLD_2_URL}}": "https://www.cbsnews.com/news/united-kingdom-defense-chief-john-healey-resigns-military-funding-nato/",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺 ATO · JULY 1",
    "{{ECON_1_HEADLINE}}": "ATO Confirms Fuel Tax Credit Rates Revert to Full on July 1 — 17 Days to Review Your BAS and Job Pricing",
    "{{ECON_1_SUMMARY}}": "The ATO has confirmed fuel tax credit rates will revert to full indexed levels from July 1, 2026, when the temporary fuel excise halving expires. Businesses that have been claiming credits at the reduced April 1 rates need to update their records and recalculate cost models before the end of the financial year. For trades operators, the practical impact is immediate: any job priced on current fuel costs needs to be reviewed before quotes are finalised for work starting in July. The Q4 FY2026 BAS (April–June) will reflect the reduced excise, but FY2027 Q1 activity will be calculated at the full rate — meaning the difference will be visible in your first quarterly BAS lodgement next October.",
    "{{ECON_1_URL}}": "https://www.ato.gov.au/businesses-and-organisations/business-bulletins-newsroom/fuel-tax-credit-rates-changed-from-1-april-2026",

    "{{ECON_2_FLAG}}": "🏦 RBA · RATES",
    "{{ECON_2_HEADLINE}}": "RBA Cash Rate Decision Due Tuesday June 16 — Hold at 4.35% Expected With Easing Bias Emerging",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank of Australia meets on Tuesday June 16, with both CBA and NAB now removing forecasts for further rate hikes. The market consensus is a hold at 4.35%, with some economists projecting the first cut could come as early as August if inflation continues to ease. The easing of Middle East oil pressure — if the ceasefire holds — would be a significant disinflationary input. For small businesses, Tuesday's meeting and post-decision statement will be the clearest signal yet of whether the RBA sees the current rate as the peak or whether any upside risk remains.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · WORKFORCE",
    "{{TECH_1_HEADLINE}}": "Snap Cuts 1,000 Jobs as AI Now Writes 65% of Its New Code — Tech Layoff Wave Reshapes What Human Work Means",
    "{{TECH_1_SUMMARY}}": "Snapchat parent Snap axed approximately 1,000 employees — 16% of its workforce — and closed over 300 open roles, directly citing AI replacing coding and operations work. CEO Evan Spiegel confirmed AI now generates more than 65% of all new code written at Snap. The cuts are expected to deliver over $500 million in annualised savings by H2 2026. This follows Meta's 8,000-job reduction last month, also AI-driven. The pattern is accelerating: major platforms are running leaner by embedding AI into the work itself — not just using AI as a productivity aid, but as a replacement for headcount. The question for every business now is not whether AI will change staffing decisions, but how fast.",
    "{{TECH_1_URL}}": "https://www.foxbusiness.com/markets/snapchat-parent-company-cuts-1000-jobs-major-ai-driven-workforce-restructuring",

    "{{TECH_2_FLAG}}": "💼 AI · META",
    "{{TECH_2_HEADLINE}}": "Meta Cuts 8,000 Jobs in AI Pivot — Thousands More Reassigned to AI-Focused Roles as Platform Restructures Around Intelligence",
    "{{TECH_2_SUMMARY}}": "Meta has reduced its global headcount by roughly 10% — approximately 8,000 roles — while simultaneously reassigning thousands more employees to AI-focused teams. An additional 600 staff in Meta's own AI division were separately cut in a push for leaner decision-making. Taken together with Snap's restructuring this week, two of the world's largest social platforms have now formally declared that AI is replacing generalist roles, not supplementing them. For trades and small business owners, the signal is that the gap between AI-enabled businesses and those still running on manual processes is widening faster than most economic forecasts predicted.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳 CHINA · POLICY",
    "{{ROBOT_1_HEADLINE}}": "China's Government Issues National Directive: Humanoid Robots Must Achieve 'Routine Deployment' Across Industry by End of 2026",
    "{{ROBOT_1_SUMMARY}}": "China's Ministry of Industry and Information Technology (MIIT) and the State-owned Assets Supervision and Administration Commission (SASAC) have jointly launched the 2026 Humanoid Robot and Embodied AI Real-Scene Training Action. The directive mandates that humanoid robots complete application verification and achieve 'routine deployment' across industrial manufacturing, public services, and specialised operations by December 2026 — targeting thousand-unit deployments across more than 100 validated real-world scenarios. Implementation plans are due from enterprises by the end of this month. It is the most comprehensive state-backed robot industrialisation mandate ever issued globally, underpinning China's position as the world's most aggressive humanoid robotics scaler at the government level.",
    "{{ROBOT_1_URL}}": "https://pandaily.com/miit-sasac-humanoid-robot-real-scene-training-2026-jun2026",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Face Türkiye Tomorrow in World Cup Opener — Australia Kicks Off at 2pm AEST from Vancouver",
    "{{AUS_1_SUMMARY}}": "Australia begins their 2026 FIFA World Cup campaign tomorrow, Sunday June 14, at 2:00pm AEST at BC Place in Vancouver against Türkiye — a watchable afternoon kick-off for Australian fans. Coach Tony Popovic's 26-man squad includes 17 first-time World Cup players alongside veterans Mathew Ryan (captain) and Mathew Leckie, both set to equal Tim Cahill's record of four World Cup squads. Group D also includes the USA (June 20 at 5am AEST) and Paraguay (June 26). With the expanded 48-team format, Australia has a more realistic path through the group stage than in any previous World Cup.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/socceroos-australia-world-cup-2026-explained/5w41ackgb",

    "{{AUS_2_HEADLINE}}": "Fair Work Commission Hears INPEX Ichthys LNG Strike Application — NT Energy Supply in Focus",
    "{{AUS_2_SUMMARY}}": "The Fair Work Commission held a hearing Friday on INPEX's application regarding protected industrial action at the Ichthys LNG facility in Darwin. An adverse outcome could affect LNG export volumes and domestic east-coast gas supply at an already sensitive time — with the energy market under pressure from the Middle East conflict and the fuel excise relief expiring June 30. The outcome will be watched closely by energy-intensive businesses and logistics operators tracking input costs into Q1 FY2027.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "FIFA World Cup Live Screenings Begin Today at Bunjil Place — Every Match Free on the Outdoor Screen Through July 19",
    "{{VIC_1_SUMMARY}}": "Bunjil Place in Narre Warren — 10 kilometres from Carrum Downs — is screening every 2026 FIFA World Cup match live on its outdoor screen through July 19. The Socceroos' Group D opener against Türkiye tomorrow at 2pm AEST is the first marquee fixture. The NGV's Cartier: Winter Masterpieces, which opened Thursday, also continues its run through October 4 at NGV International on St Kilda Road. A packed Melbourne winter program — between the football and one of the biggest gallery exhibitions ever staged in Australia, there is no shortage of reasons to head out once the rain eases.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 BIOLOGY · AGEING",
    "{{SCI_1_HEADLINE}}": "Scientists Identify the Hidden Trigger of Cellular Aging — and Show a Dietary Molecule Can Reverse It",
    "{{SCI_1_SUMMARY}}": "Researchers at Germany's Leibniz Institute on Aging have pinpointed the decline of phosphatidylcholine — a key membrane lipid — as a primary driver of age-related mitochondrial dysfunction and cellular energy loss. As organisms age, phosphatidylcholine synthesis drops, disrupting the mitochondrial membrane network that powers cells. The study, published in Nature Communications on June 10, showed that restoring phosphatidylcholine through diet reversed mitochondrial decline in nematode models and rejuvenated energy networks in human cell cultures. The finding opens a potential dietary path to slow one of the most fundamental cellular processes underlying the ageing of every living organism.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Why Your Plant and Equipment Is Your Most Underpriced Line Item — and How AI Can Fix It This Weekend",
    "{{INSIGHT_BODY}}": "Most small trades operators price labour and materials with reasonable care, but plant and equipment — the ute, trailer, compressor, generator, specialty gear — typically gets a round number that has not been revisited since fuel, insurance premiums, and replacement costs were a third of what they are now. The result is that every job quietly subsidises your equipment at margins you have never consciously set. Here is where AI earns its keep in a single Saturday morning session. Open Claude or ChatGPT and list every piece of plant you regularly deploy: what you paid for it, current insurance and registration, fuel cost per week, and expected replacement timeline. Ask the AI to calculate a realistic per-hour and per-day cost for each item at your current utilisation rate. Then compare that figure to what you are actually charging or including in quotes. Most operators find they are undercharging on equipment by 20 to 40 percent — particularly on specialty gear used infrequently, where there is no visible 'market rate' to anchor against. That gap, recovered consistently across a full year of quoting, can represent five to ten thousand dollars in recovered margin without changing a single hour of work or a single job. It is not glamorous analysis. But it is the kind of thing that makes your next financial year materially different from this one, and it takes less time than watching the pre-match commentary tonight.",

    # Fun Facts
    "{{FACT_1}}": "The human nose can identify approximately one trillion distinct odours — roughly 500 times more than previous estimates suggested. Smell is the only sense with a direct neural pathway to the brain's memory and emotion centres, the hippocampus and amygdala, which is why a single familiar scent can trigger a vivid, emotionally charged memory from decades earlier far more powerfully than any image or sound.",

    "{{FACT_2}}": "The Panama Canal's lock system uses no pumps whatsoever — every ship is raised and lowered entirely by gravity, using freshwater from Gatun Lake above sea level. Each vessel passage drains approximately 197 million litres of fresh water into the ocean. Completed in 1914 after a decade of construction by 75,000 workers, the canal saves ships roughly 15,000 kilometres compared to sailing around Cape Horn at the southern tip of South America.",

    "{{FACT_3}}": "The world's largest known bacterium, Thiomargarita magnifica, was discovered in Caribbean mangroves in 2022 and can grow up to two centimetres long — large enough to see with the naked eye. It rewrote biology textbooks: unlike all other bacteria, it stores its DNA inside a membrane-bound organelle, a feature previously thought exclusive to complex cells. A single specimen can contain up to 700,000 times more DNA than a typical bacterium.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the bricklayer never need a calculator on site?",
    "{{JOKE_PUNCHLINE}}": "He always knew when the job was about to hit a wall.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Simplicity is the ultimate sophistication.”",
    "{{CLOSING_ATTR}}": "— Leonardo da Vinci",
    "{{CLOSING_MESSAGE}}": "A rainy Saturday in Carrum Downs — northerly winds up to 40 km/h and rain likely through the morning, easing this evening. The Socceroos kick off their World Cup campaign tomorrow at 2pm AEST against Türkiye in Vancouver — a civilised Saturday arvo watch if you can get your quotes and your plant costing sorted first. The Iran ceasefire is at a delicate moment: if the Strait of Hormuz reopens properly over the weekend, you will see it at the bowser within a fortnight. But the fuel excise relief still ends on June 30 regardless. Use the wet morning well, Liall — the week ahead has the RBA on Tuesday, World Cup at all hours, and 17 days to get your July pricing right.",
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
