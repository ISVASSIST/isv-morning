#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 15 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 15 May (BOM forecast issued 8:50pm Thu 14 May)
    "{{WEATHER_1}}": "Fri 15 May · Clear & Cool · 15°C",
    "{{WEATHER_2}}": "Sat 16 May · Sunny · 17°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "Sun 17 May · Partly Cloudy · 16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "Mon 18 May · Rain Likely · 14°C",
    "{{WEATHER_5}}": "Tue 19 May · Showers · 13°C",
    "{{WEATHER_ALERT}}": "☀️ SUNNY WEEKEND — RAIN MON",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸🇨🇳 US–CHINA SUMMIT",
    "{{WORLD_1_HEADLINE}}": "Xi Issues Stark Taiwan Warning as Trump-Xi Beijing Summit Nears Conclusion",
    "{{WORLD_1_SUMMARY}}": "On day two of President Trump's landmark Beijing visit, President Xi Jinping issued his sharpest public statement on Taiwan in years — warning the US and China 'will have clashes and even conflicts' if Taiwan is mishandled, calling it 'the most important issue' in the bilateral relationship. The two leaders agreed in principle to a 'constructive relationship of strategic stability' and discussed trade deals covering Boeing aircraft, US agricultural goods, rare earth access, and Nvidia chip export rules. No formal communiqué was released, but analysts describe the summit as stabilising — the US-China trade truce is expected to extend.",
    "{{WORLD_1_URL}}": "https://www.cnbc.com/2026/05/14/trump-xi-summit-beijing-takeaway-taiwan-trade-iran-war-strategic-relations-.html",

    "{{WORLD_2_FLAG}}": "🇷🇺🇺🇦 RUSSIA–UKRAINE",
    "{{WORLD_2_HEADLINE}}": "Russia Launches Biggest Two-Day Aerial Assault on Ukraine Since War Began — Kyiv Declares Day of Mourning",
    "{{WORLD_2_SUMMARY}}": "Russia fired more than 1,560 drones and 56 ballistic missiles across Ukraine in a two-day bombardment — described by Ukrainian officials as the largest aerial attack since the war started. Kyiv bore the worst damage with at least 12 killed and 57 injured, apartment buildings collapsed in the Darnytskyi district and fires breaking out across multiple suburbs. Kharkiv, Poltava, and Zaporizhzhia were also struck. The mayor of Kyiv declared a day of mourning. The timing — coinciding with the Trump-Xi summit — was widely noted as a deliberate signal.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/05/14/g-s1-121998/russia-hits-kyiv-with-drones-and-ballistic-missiles",

    # Economics
    "{{ECON_1_FLAG}}": "📊 INFLATION",
    "{{ECON_1_HEADLINE}}": "Australia's Annual Inflation Eases to 4.3% as Global Fuel Pressures Begin to Moderate",
    "{{ECON_1_SUMMARY}}": "Australia's CPI data for May 2026 shows annual inflation easing to 4.3%, down from 4.6% in March — the first clear sign the recent energy-driven surge may be peaking. Headline CPI rose 0.8% in the month, with easing diesel and petrol prices providing early relief after the April crisis. However, housing, insurance, and services costs remain stubbornly elevated, and economists warn that when the government's 26-cent fuel excise cut expires June 30, any bounce in pump prices could push inflation back up. The Reserve Bank is watching closely before any rate move.",
    "{{ECON_1_URL}}": "https://www.ibtimes.com.au/australia-inflation-eases-slightly-43-may-2026-fuel-pressures-begin-moderate-1868689",

    "{{ECON_2_FLAG}}": "📉 RBA WATCH",
    "{{ECON_2_HEADLINE}}": "Economists Divided on RBA Rate Path as Budget Stimulus Clouds the Inflation Picture",
    "{{ECON_2_SUMMARY}}": "With Tuesday's Federal Budget delivering expanded infrastructure spending, an extended instant asset write-off, and housing support measures, Australian economists are reassessing the RBA's rate-cut timeline. Several analysts argue the stimulus adds meaningful demand to an economy already running near full employment, potentially keeping inflation above the 2–3% target band longer. Markets had priced in a 65% chance of an August rate cut before the budget; that figure has since softened. For small businesses carrying floating-rate debt or planning equipment investment, the message is: don't count on relief before late 2026.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 BAIDU CREATE 2026",
    "{{TECH_1_HEADLINE}}": "Baidu CEO Declares the Model Race Is Over — AI's Next Era Is the Agent Race, and 'Super Individuals' Are Coming",
    "{{TECH_1_SUMMARY}}": "At Baidu's annual Create 2026 conference in Beijing on Thursday, CEO Robin Li outlined a fundamental shift in AI competition: large model development is largely settled, he argued, and the real battle is now for who builds the best autonomous AI agents. Baidu unveiled DuMate — a general-purpose agent handling customer service, data analysis, and content creation — and Miaoda, a code-generation agent that writes roughly 90% of its own code. Li introduced the concept of 'super individuals': one person, empowered by AI agents, doing the commercial output of an entire team. 'What made AI go viral was not the model, but the application,' he said.",
    "{{TECH_1_URL}}": "https://technode.com/2026/05/14/baidu-create-2026-ceo-says-ai-is-moving-from-model-competition-to-ai-agent-era-foresees-rise-of-super-individuals/",

    "{{TECH_2_FLAG}}": "🔔 PROACTIVE AI",
    "{{TECH_2_HEADLINE}}": "Anthropic, OpenAI and Google All Launch 'Proactive AI' Features This Week — Your Assistant Now Acts Without Being Asked",
    "{{TECH_2_SUMMARY}}": "In a remarkable convergence, all three of the world's leading AI labs — Anthropic, OpenAI, and Google — announced proactive AI features within days of each other this week. Anthropic's Claude Orbit, OpenAI's ChatGPT Pulse, and Google's Gemini Proactive Assistance will all monitor connected apps — reading your calendar, email, and project tools — and surface actions, draft responses, and flag priorities automatically without waiting for a prompt. The shift marks AI moving from a tool you query to an agent working on your behalf. For small businesses with Gmail, Slack, or Xero connected, the integration window is opening now.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏭 WAREHOUSE AUTOMATION — USA",
    "{{ROBOT_1_HEADLINE}}": "Symbotic's AI Robots Process 2.23 Billion Cases in 2025 — Autonomous Fleet Travels 200 Million Miles",
    "{{ROBOT_1_SUMMARY}}": "Symbotic has announced that its fleet of SymBot autonomous mobile robots processed more than 2.23 billion warehouse cases in 2025 — while collectively travelling over 200 million miles through distribution centres, placing them among the most-travelled autonomous vehicle fleets in the world. Per-bot efficiency improved 9% in cases handled and 20% in miles travelled year-on-year, driven by AI-optimised routing and pick sequencing. Symbotic operates across Walmart and major US retail networks, with a $22.7 billion deployment backlog signalling demand far outpacing current capacity.",
    "{{ROBOT_1_URL}}": "https://roboticsandautomationnews.com/2026/05/13/symbotic-surpasses-2-billion-cases-processed-as-demand-for-physical-ai-accelerates/101444/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Budget Migration Overhaul: Trades Retained on Priority Shortage List as Points Test Tightened for Other Fields",
    "{{AUS_1_SUMMARY}}": "The 2026-27 Federal Budget includes significant reforms to Australia's permanent skilled migration program — recalibrating the points test to favour candidates with confirmed job offers in critical shortage occupations, while tightening caps in over-subscribed professional fields. For the trades sector, the key outcome is that high-demand trade occupations remain on the priority skills shortage list, meaning businesses struggling to recruit locally can still access sponsored skilled visas and state nomination pathways. The reforms target migration more precisely toward genuine labour market gaps.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/federal-budget-migration-program-changes/mg2awxk1k",

    "{{AUS_2_HEADLINE}}": "Trump and Xi Agree Strait of Hormuz Must Stay Open — A Result Australia Was Watching Closely",
    "{{AUS_2_SUMMARY}}": "As part of the Trump-Xi summit conclusions, both leaders agreed the Strait of Hormuz must remain open to global energy flows — a development watched carefully in Canberra. Australia imports a significant share of its refined fuel via Persian Gulf routes; the April diesel crisis made global energy security a domestic priority. Trump pushed for reduced militarisation of the strait while Xi signalled China's intent to purchase more US oil. If the agreement holds, it offers a path toward easing fuel supply pressure — though analysts note geopolitical agreements in the region have a poor recent track record.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "NBA House Lands in Melbourne Today — Official Playoffs Fan Hub at The Timber Yard Through Sunday",
    "{{VIC_1_SUMMARY}}": "The NBA brings its official fan experience hub to Melbourne for the first time during the 2026 Playoffs, with NBA House opening today at The Timber Yard in Port Melbourne and running through Sunday 17 May. The free-entry event blends live game viewing, gaming zones, music, and pop culture activations — part of the NBA's accelerating push into Australian markets as domestic viewership hits record levels. Open 10am to 10pm daily.",

    # Science
    "{{SCI_1_FLAG}}": "🦑 MARINE SCIENCE — WESTERN AUSTRALIA",
    "{{SCI_1_HEADLINE}}": "Giant Squid Confirmed in WA Waters for the First Time — Deep-Sea eDNA Study Reveals Hidden World Off Ningaloo",
    "{{SCI_1_SUMMARY}}": "Scientists from the Western Australian Museum, aboard the Schmidt Ocean Institute's R/V Falkor, have confirmed the first-ever recorded presence of the giant squid (Architeuthis dux) in Western Australian waters — detected via environmental DNA (eDNA) collected from deep submarine canyons near the Ningaloo Coast. Researchers collected over 1,000 water samples from depths up to 4,510 metres across the Cape Range and Cloates canyons, identifying 226 species including the sleeper shark, faceless cusk eel, rare deep-diving whales, and dozens of species never previously recorded in WA waters. The study was published in Environmental DNA, May 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI-Assisted Cash Flow Forecasting: The Tool Keeping Small Trades Businesses Solvent Through Volatile Times",
    "{{INSIGHT_BODY}}": "For a trades business like ISV, cash flow is the oxygen of the operation — but it's also the thing that gets crunched hardest when jobs slow, clients pay late, or material costs jump without warning. Most small operators are still managing cash flow the same way they always have: an eye on the bank balance and a gut feeling about what's coming in. AI-assisted cash flow forecasting tools — now built into platforms like Xero, MYOB, and QuickBooks — can model upcoming inflows and outflows based on your job schedule, invoice history, and known expenses, and flag potential shortfalls weeks before they hit. At the current pace of economic volatility — fuel still elevated, interest rates uncertain, inflation only now easing — knowing your cash position six weeks out isn't just useful. It's the difference between making a confident call on a new hire or a piece of equipment, or having no choice at all.",

    # Fun Facts
    "{{FACT_1}}": "Portland cement — the binding agent in virtually all modern concrete — accounts for around 8% of global CO₂ emissions, making the construction materials industry one of the planet's largest industrial emitters. Researchers are developing geopolymer cements using industrial slag and fly ash that could cut those emissions by up to 80% at comparable performance and cost — potentially the most consequential materials science shift in construction since Portland cement was patented in 1824.",
    "{{FACT_2}}": "Capsaicin — the compound that makes chillies hot — has no taste or smell whatsoever. It works purely by binding to heat and pain receptors in your mouth (called TRPV1), triggering the same nerve signals as a genuine burn at around 43°C. Water does almost nothing to help because capsaicin is oil-soluble; dairy products work far better because casein proteins physically break the capsaicin–receptor bond. This is why milk, yoghurt, or ice cream beat beer or water every time.",
    "{{FACT_3}}": "Colossus — the world's first programmable digital computer, built at Bletchley Park in 1943 to crack Nazi Lorenz cipher traffic — was deliberately destroyed after World War II on Winston Churchill's direct orders to protect the secret of British codebreaking capability. Its existence remained officially classified until 1975 — a full 30 years after the war ended. Veterans and historians rebuilt a fully functional replica from scratch in 2008 using surviving photographs, partial circuit diagrams, and the memories of the engineers who built the original.",

    # Joke
    "{{JOKE_SETUP}}": "Why do refrigeration mechanics always win arguments?",
    "{{JOKE_PUNCHLINE}}": "They know exactly how to keep their cool.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Do not go where the path may lead, go instead where there is no path and leave a trail.\"",
    "{{CLOSING_ATTR}}": "Ralph Waldo Emerson",
    "{{CLOSING_MESSAGE}}": "Friday in Carrum Downs and the polar blast is done — clear skies this morning and a sunny Saturday ahead before rain returns Monday. It's been a heavy week of news: the federal budget, the Trump-Xi summit wrapping up in Beijing, and Russia's biggest aerial assault on Ukraine since the war began. On the brighter side, inflation is finally turning the corner and the weekend is yours. NBA House is on in Melbourne this weekend if you're after something to do Saturday. Have a good one, Liall.",
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
