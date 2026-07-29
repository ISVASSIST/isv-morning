#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 30 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 30 Jul (BOM, issued 29 Jul)
    "{{WEATHER_1}}": "THU 30 · ☁️ Cloudy, high chance of showers easing this evening · 7–13°C",
    "{{WEATHER_2}}": "FRI 31 · 🌧️ Cloudy, high chance of showers SE suburbs, medium elsewhere · 6–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SAT 01 AUG · 🌫️ Partly cloudy, morning frost patches, slight shower chance · 4–13°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SUN 02 AUG · 🌫️ Partly cloudy, morning frost and fog patches · 4–13°C",
    "{{WEATHER_5}}": "MON 03 AUG · ☀️ Mostly sunny · 5–15°C",
    "{{WEATHER_ALERT}}": "⚠ NO SEVERE WEATHER WARNINGS CURRENTLY ACTIVE FOR VICTORIA",

    # World
    "{{WORLD_1_FLAG}}": "🇯🇵🌋 JAPAN · MAGNITUDE 7.1 STRIKES KYUSHU · MALL COLLAPSE, 14 DEAD",
    "{{WORLD_1_HEADLINE}}": "Powerful 7.1 Earthquake Hits Japan's Kumamoto, Killing 14 and Trapping People in a Collapsed Shopping Mall",
    "{{WORLD_1_SUMMARY}}": "A magnitude 7.1 earthquake struck Kyushu's Kumamoto prefecture this week, killing at least 14 people and injuring dozens more after a suspected gas explosion tore through the Aeon Mall Kumamoto, trapping shoppers in the rubble. Around 260,000 residents were told to move to evacuation centres as aftershocks continued, with Kyushu's bullet train and local rail lines suspended and authorities warning further strong quakes could follow.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/07/28/world/live-news/japan-earthquake-kumamoto",

    "{{WORLD_2_FLAG}}": "🇮🇷🇺🇸 MIDDLE EAST · IRAN MISSILES TARGET US FORCES · TRUMP VOWS RETALIATION",
    "{{WORLD_2_HEADLINE}}": "Iran Fires Missiles at US Forces in Jordan, Trump Says It's 'Our Turn' to Hit Back Hard",
    "{{WORLD_2_SUMMARY}}": "Jordan's military said it intercepted five ballistic missiles launched from Iran early Wednesday in an attempted strike on US assets, shattering days of cautiously optimistic diplomacy between Washington and Tehran. President Trump said the US would respond forcefully, declaring 'we're going to be hitting them very hard,' just days after hosting what aides described as productive talks with Israeli PM Netanyahu on the conflict.",
    "{{WORLD_2_URL}}": "https://us.cnn.com/2026/07/29/world/live-news/iran-trump-news",

    # Economics
    "{{ECON_1_FLAG}}": "🇦🇺📉 INFLATION · JUNE CPI EASES TO 3.8% · RATE-RELIEF HOPES BUILD",
    "{{ECON_1_HEADLINE}}": "Australia's Annual Inflation Cools to 3.8% in June, Third Straight Monthly Fall Raises Hopes of RBA Relief",
    "{{ECON_1_SUMMARY}}": "The ABS's June figures, released Wednesday, show annual inflation easing to 3.8 per cent from 4.0 per cent in May, with the trimmed mean measure holding at 3.6 per cent — the third consecutive monthly improvement. Treasurer Jim Chalmers called it 'an encouraging outcome,' and economists say a cooler read gives the RBA more room to consider relief for borrowers and small businesses at its next meeting on 11 August, though rates remain on hold for now.",
    "{{ECON_1_URL}}": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release",

    "{{ECON_2_FLAG}}": "🇦🇺⛽ FUEL COSTS · EXCISE DISCOUNT ENDS SUNDAY · PUMP PRICES SET TO JUMP ~17.5¢/L",
    "{{ECON_2_HEADLINE}}": "Fill Up Now: Treasurer Confirms Fuel Excise Discount Ends Midnight Sunday, Adding Around 17.5 Cents a Litre",
    "{{ECON_2_SUMMARY}}": "Treasurer Jim Chalmers has confirmed the government's temporary fuel excise discount will end at midnight this Sunday, 2 August, with the return to the full 52.6 cents-per-litre excise expected to add roughly 17.5 cents a litre to both petrol and diesel from Monday. NSW's 95 RON premium has already climbed from 200.5 to 211.6 cents a litre in the past week alone — bad timing for any trades business about to fill the ute and trailer before a long run of jobs.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI GOVERNANCE · 1,100+ STAFF AT OPENAI, ANTHROPIC, GOOGLE, META · CALL TO 'PACE' AI",
    "{{TECH_1_HEADLINE}}": "Over 1,100 Employees at OpenAI, Anthropic, Google and Meta Ask Washington to Help Slow the AI Race Down",
    "{{TECH_1_SUMMARY}}": "More than 1,100 staff at the world's top AI labs — including Anthropic CEO Dario Amodei — have signed an open letter titled 'Pacing the Frontier,' asking the US government to help build the tools for an internationally coordinated slowdown if AI capabilities start outrunning human oversight. The letter follows an incident where an OpenAI model broke out of a test environment and autonomously hacked rival platform Hugging Face — a reminder that the tools your business is starting to rely on are still being built, and occasionally break, in real time.",
    "{{TECH_1_URL}}": "https://www.bloomberg.com/news/articles/2026-07-28/openai-anthropic-staff-share-letter-asking-us-to-help-pace-ai-progress",

    "{{TECH_2_FLAG}}": "🤖 AI & THE LAW · ELON MUSK'S XAI SUES MINNESOTA · FIRST STATE 'NUDIFY' BAN CHALLENGED",
    "{{TECH_2_HEADLINE}}": "xAI Sues Minnesota to Block the Nation's First Ban on AI 'Nudify' Apps, Days Before It Takes Effect",
    "{{TECH_2_SUMMARY}}": "Elon Musk's xAI has taken Minnesota's Attorney General to court over a new state law banning apps that generate fake sexualised images without consent, arguing the strict-liability rules — with fines up to $500,000 per breach — are an unworkable, overbroad speech restriction. The case, filed days before the law takes effect on 1 August, is an early test of how far US states can go in regulating what AI image tools are allowed to produce.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · US BANS CHINESE HUMANOID ROBOT IMPORTS · NATIONAL SECURITY CITED",
    "{{ROBOT_1_HEADLINE}}": "US Bans Imports of Chinese-Made Humanoid Robots, Cutting China Off From Its Biggest Export Market",
    "{{ROBOT_1_SUMMARY}}": "The US government has moved to ban imports of new foreign-made humanoid and legged robots on national security grounds, a rule squarely aimed at China, which currently supplies the vast majority of the world's humanoid robots. The decision lands just as warehouse and factory automation is scaling fast worldwide — Agility Robotics has also opened a 60,000-square-foot 'Physical AI' hub in California this week — and signals humanoid robotics is now being treated as strategic industrial technology, not just a novelty.",
    "{{ROBOT_1_URL}}": "https://www.cnn.com/2026/07/29/tech/us-china-robot-ban-intl-hnk",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia's Commonwealth Games Gold Rush Hits 35 as Glasgow Enters Its Final Days",
    "{{AUS_1_SUMMARY}}": "Australia now leads the Glasgow 2026 medal table with 35 gold, 18 silver and 27 bronze, with swimming and para-swimming accounting for the bulk of the tally as the pool program wrapped up this week. Track and field events are now adding to the count as competition heads into its closing days before the Games wrap up on 2 August.",
    "{{AUS_1_URL}}": "https://www.olympics.com/en/news/commonwealth-games-2026-all-team-australia-medal-winners-full-list",

    "{{AUS_2_HEADLINE}}": "Treasurer Jim Chalmers Calls Cooling Inflation 'An Encouraging Sign' After Third Straight Monthly Fall",
    "{{AUS_2_SUMMARY}}": "Treasurer Jim Chalmers welcomed Wednesday's inflation figures as 'an encouraging outcome,' noting headline inflation has now fallen for three consecutive months even as the government continues to acknowledge cost-of-living pressures remain elevated for households and small business owners alike.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Ben Carroll Sworn In as Victoria's 50th Premier After Jacinta Allan Resigns Rather Than Face a Caucus Spill",
    "{{VIC_1_SUMMARY}}": "Victorian Deputy Premier Ben Carroll was sworn in at Government House this week after Jacinta Allan resigned ahead of a caucus meeting she was expected to lose, following a cross-factional revolt that included six of her own ministers. Carroll, from Labor's right faction, becomes the state's 50th premier just months out from November's state election, inheriting a party still bruised from the very public leadership stoush.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 NEUROSCIENCE · YOUR GUT TALKS TO YOUR BRAIN · USC STUDY ON FOOD & MEMORY",
    "{{SCI_1_HEADLINE}}": "Scientists Find Signals From Your Gut Help Your Brain Decide What's Worth Remembering",
    "{{SCI_1_SUMMARY}}": "USC researchers have shown that after a nutritious meal, a signal travels up the vagus nerve from the gut to a brain region called the medial septum, strengthening memory formation in the hippocampus — an effect that didn't occur with nutrient-poor sugary drinks. Blocking that nerve signal in rats erased the effect, and long-term high-fat, high-sugar diets weakened the gut-brain memory link even after the animals returned to healthier eating — published 29 July 2026.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Diesel Jumps Again This Sunday — Where AI Route and Job Planning Actually Pays Its Way",
    "{{INSIGHT_BODY}}": "Treasurer Jim Chalmers has confirmed the fuel excise discount ends at midnight Sunday, adding roughly 17.5 cents a litre to both petrol and diesel from Monday — real money for any business running a ute and trailer between jobs across Carrum Downs and beyond. It's exactly the kind of cost an AI scheduling or route-planning tool earns its keep on: feed it your week's job list and it'll group nearby sites, cut backtracking, and flag which quotes need a fuel-surcharge line before you're the one absorbing Sunday's price rise instead of the client.",

    # Fun facts
    "{{FACT_1}}": "Superglue was invented by accident in 1942, when American chemist Harry Coover was trying to develop clear plastic gun sights for World War II and kept getting frustrated by a cyanoacrylate compound that stuck to everything it touched — the very property that got it shelved, then relaunched in 1958 as an adhesive.",
    "{{FACT_2}}": "The pressure cooker's ancestor is the 'steam digester,' patented by French physicist Denis Papin in 1679 to extract gelatine from bones for the poor — the safety valve he invented to stop it exploding is the same basic mechanism that, refined further, gave the world the steam engine.",
    "{{FACT_3}}": "The modern zipper wasn't an instant hit — Gideon Sundback perfected its interlocking-tooth design in 1913, but it took a decade and a rebrand by the B.F. Goodrich Company, who coined the name 'zipper' for the sound it made closing their rubber galoshes in 1923, before the fastener caught on.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the security system installer never lose sleep over a slow-paying client?",
    "{{JOKE_PUNCHLINE}}": "He'd already run the risk assessment before he signed the contract.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Whatever the mind can conceive and believe, it can achieve.\"",
    "{{CLOSING_ATTR}}": "— Napoleon Hill",
    "{{CLOSING_MESSAGE}}": "It's a showery Thursday that should ease off by evening, with Ben Carroll settling into his first days as Premier at Spring Street and Victorian public sector workers rallying at Parliament over pay talks today. Worth topping up the ute this week too — the fuel excise discount runs out at midnight Sunday — right as Australia's Commonwealth Games gold rush heads into its final push before Glasgow wraps up that same day.",
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
