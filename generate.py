#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 22 October 2026',
'{{WEATHER_1}}': 'THU 22 OCT · ☀️ Sunny and hot for spring · ~30°C',
'{{WEATHER_2}}': 'FRI 23 OCT · ☀️ Hot, gusty northerlies · ~30°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SAT 24 OCT · 🌧️ Showers building ahead of a cold front · ~24°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SUN 25 OCT · 🌥️ Much cooler · ~16°C',
'{{WEATHER_5}}': 'MON 26 OCT · 🌥️ Cool · ~15°C',
'{{WEATHER_ALERT}}': "Melbourne is forecast to hit 30°C on both Thursday and Friday, its first 30s since March, so plan water, shade and early starts. A cold front brings showers Saturday and a drop to the mid-teens by Sunday. Forecasts vary between sources, so check BoM before committing to outdoor jobs.",
'{{WORLD_1_FLAG}}': '🌍 IRAN WAR',
'{{WORLD_1_HEADLINE}}': "Pakistan's Army Chief Lands in Tehran as Iran Says No Talks With Washington Until Its Demands Are Met",
'{{WORLD_1_SUMMARY}}': "Field Marshal Asim Munir met President Pezeshkian and the foreign minister on 20 October, his fifth Iran trip since the April ceasefire. Iran reportedly refuses to ship enriched uranium out and wants oil sanctions lifted first, and says renewed fighting with the US is possible. No deal means Hormuz stays tight and fuel stays dear.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/10/20/pakistan-army-chief-in-tehran-can-diplomacy-prevent-new-us-iran-fighting',
'{{WORLD_2_FLAG}}': '📰 US SECURITY',
'{{WORLD_2_HEADLINE}}': 'FBI Releases 38 Pages of Interview Notes From Durham Probe Into CIA Torture of 9/11 Detainees',
'{{WORLD_2_SUMMARY}}': "Just Security's 21 October roundup says the release followed a FOIA lawsuit. The same edition leads with the Iran war. I only saw the summary, so check the full edition for detail.",
'{{WORLD_2_URL}}': 'https://www.justsecurity.org/161515/early-edition-october-21-2026/',
'{{ECON_1_FLAG}}': '⛽ FUEL · OIL',
'{{ECON_1_HEADLINE}}': 'Brent Settles Near US$108.79 After Touching a Five-Month High of US$111.99 on Houthi Attacks on Saudi Infrastructure',
'{{ECON_1_SUMMARY}}': "Market reports on 21 October show oil still well above US$100 with Hormuz unresolved and US-Iran mediation stalling. Quotes varied between US$107 and US$111 through the day. Diesel at the bowser follows with a lag, so verify current prices before quoting jobs.",
'{{ECON_1_URL}}': 'https://www.mitrade.com/au/insights/daily-market-outlook/news-today/market-news-today-australia-261021',
'{{ECON_2_FLAG}}': '📈 MARKETS · AUD',
'{{ECON_2_HEADLINE}}': 'ASX 200 Edges Up 0.16% to 8,831 as NextDC Shares Plunge About 40% Over Data Centre Opposition; Aussie Dollar Holds Near 70 US Cents',
'{{ECON_2_SUMMARY}}': "ABC's 21 October markets blog has the local market steady and the dollar around 70 US cents. A stronger dollar helps a little with imported consumables and equipment costs. NextDC's fall reflects community opposition to one of Victoria's largest data centres.",
'{{TECH_1_FLAG}}': '🛡️ AI · SECURITY',
'{{TECH_1_HEADLINE}}': "Microsoft Adds Controls for Rogue AI Agents That Limit What an Agent Can Do as Its Risk Rises",
'{{TECH_1_SUMMARY}}': "SiliconANGLE reports on 19 October that Microsoft's new controls shrink an agent's permissions as its assessed risk climbs. Enterprise-focused, but the principle applies to any trade business: give AI tools the least access they need, and keep customer and bank details out of them.",
'{{TECH_1_URL}}': 'https://siliconangle.com/2026/10/19/microsoft-targets-the-agentic-insider-with-new-controls-for-rogue-ai-agents/',
'{{TECH_2_FLAG}}': '🎙️ AI · MEETINGS',
'{{TECH_2_HEADLINE}}': "Otter.ai Raises US$320M for Its AI Meeting Assistant; DeepSeek Open-Sources Its DeepInfer Inference Framework",
'{{TECH_2_SUMMARY}}': "SiliconANGLE reported both on 20 October. Meeting and call transcription tools are among the easiest AI wins for a small business, such as site walks and customer calls turned into written notes. Open-sourcing inference code tends to push AI running costs down over time.",
'{{ROBOT_1_FLAG}}': '🤖 ROBOTICS · HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': "AGCO to Deploy Agility Robotics' Digit Humanoid in a Kansas Factory as Agility Heads Toward a SPAC Listing",
'{{ROBOT_1_SUMMARY}}': "The Robot Report, 21 October. Another farm-machinery maker puts a humanoid on a real production floor while Agility moves toward going public through a merger with Churchill Capital, after Digit was deployed at nine customer sites. Still early scale, but real factory work is where it counts.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/agco-to-deploy-agility-digit-humanoid-in-kansas-factory/',
'{{AUS_1_HEADLINE}}': "Helen Haines Has Lost Both Legs, Husband Says, as Accused Driver Brendan Nugent Appears in Wangaratta Court",
'{{AUS_1_SUMMARY}}': "The independent MP for Indi remains in the Alfred Hospital after Monday's attack outside her Wangaratta office. Nugent, 43, is charged with dangerous driving causing serious injury, intentionally causing serious injury and causing harm to a Commonwealth public official. He did not apply for bail, and a committal hearing is set for 4 February. Reports differed on the extent of her injuries earlier in the day.",
'{{AUS_1_URL}}': 'https://abc.net.au/news/2026-10-21/helen-haines-attack-live-updates-brendan-nugent-court-hearing/107290276',
'{{AUS_2_HEADLINE}}': 'NextDC Shares Tank About 40% After Returning to Trade Amid Community Opposition to a Major Victorian Data Centre',
'{{AUS_2_SUMMARY}}': "ABC's 21 October markets blog covers the sell-off. It shows how local opposition to energy- and land-hungry AI infrastructure is now moving share prices.",
'{{VIC_1_HEADLINE}}': "Questions Over Whether the Victorian Election Campaign Will Change After the Haines Attack",
'{{VIC_1_SUMMARY}}': "ABC Victoria's 21 October coverage asks how the campaign will look and feel after the attack. Separately, Victoria's teaching watchdog has raided an alternative primary school in Fitzroy over abuse allegations.",
'{{SCI_1_FLAG}}': '🧬 MEDICINE',
'{{SCI_1_HEADLINE}}': "Scientists Find a Natural Compound That Kills Dangerous C. difficile Gut Bacteria Without Wiping Out the Good Ones",
'{{SCI_1_SUMMARY}}': "Helmholtz Centre for Infection Research, via ScienceDaily around 20 October. The compound targets C. difficile while sparing beneficial gut microbes in early tests, which matters because current antibiotics often wreck the whole gut. Early-stage work, not yet a treatment.",
'{{INSIGHT_TITLE}}': 'Give AI the Least Access It Needs: Keep Customer and Bank Details Out of Chat Tools',
'{{INSIGHT_BODY}}': "Microsoft is adding controls this week to limit rogue AI agents, a sign that even big vendors worry about tools with too much access. Small trades can apply the same idea for free. Paste in job descriptions, quote wording and site notes, but leave out customer phone numbers, bank details and logins. Use a separate login for AI tools, avoid giving any assistant direct access to your accounting or banking, and review anything it drafts before it goes out. Start with drafting and summarising, where a mistake is easy to catch.",
'{{FACT_1}}': "Brent crude briefly hit a five-month high of US$111.99 a barrel on Tuesday before settling lower.",
'{{FACT_2}}': "Agility Robotics' Digit has been deployed at nine customer sites, according to The Robot Report.",
'{{FACT_3}}': "IDC estimated first-half 2026 humanoid robot shipments at around 25,000 units, with China accounting for 77.9% of them.",
'{{JOKE_SETUP}}': "Why did the plumber always get the tough jobs?",
'{{JOKE_PUNCHLINE}}': '"Because he never let a little pressure get to him."',
'{{CLOSING_QUOTE}}': '"A stitch in time saves nine."',
'{{CLOSING_ATTR}}': '— English Proverb',
'{{CLOSING_MESSAGE}}': "It's Thursday and the first 30-degree day since March, so water, shade and early starts on site. Tomorrow is just as hot with gusty winds, then a cold front on Saturday. Get the outdoor work done while it's dry.",
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
