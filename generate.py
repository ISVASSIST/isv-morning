#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 31 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 31 May (BOM forecast)
    "{{WEATHER_1}}": "SUN 31 · 🌧 Showers · 15°C",
    "{{WEATHER_2}}": "MON 1 JUN · 🌧 Showers · 14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 2 JUN · ⛈ Heavy rain · 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "WED 3 JUN · ☁ Cloudy · 13°C",
    "{{WEATHER_5}}": "THU 4 JUN · ⛅ Partly cloudy · 13°C",
    "{{WEATHER_ALERT}}": "⚠ WET START TO JUNE — SHOWERS DAILY SUN–TUE",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇱 ISRAEL · LEBANON",
    "{{WORLD_1_HEADLINE}}": "Israeli Ground Forces Cross Lebanon's Litani River — Netanyahu Declares Offensive Expanding",
    "{{WORLD_1_SUMMARY}}": "Israeli Prime Minister Benjamin Netanyahu confirmed Friday that Israeli ground forces have crossed Lebanon's Litani River — the boundary long treated as the effective limit of Israeli operations in southern Lebanon. 'Our forces have crossed the Litani and advanced to controlling positions,' Netanyahu said, adding that operations were active across Beirut, the Bekaa Valley and the entire front. The advance comes despite a ceasefire agreed April 16 and a 45-day extension signed May 15 — both of which have failed to halt the fighting. Since the original ceasefire, UNICEF reports 55 children killed and 212 injured in Lebanon. Israeli and Lebanese military officials met at the Pentagon this week to discuss implementation, as the diplomatic and military tracks continue to run in opposite directions.",
    "{{WORLD_1_URL}}": "https://www.cbc.ca/news/world/israel-lebanon-litani-river-9.7216696",

    "{{WORLD_2_FLAG}}": "🇸🇬 SINGAPORE · SECURITY FORUM",
    "{{WORLD_2_HEADLINE}}": "Hegseth at Shangri-La Dialogue: US Firms Line on Taiwan and China as Beijing Skips Forum for Second Year",
    "{{WORLD_2_SUMMARY}}": "US Secretary of Defense Pete Hegseth delivered the keynote at the 2026 Shangri-La Dialogue in Singapore on Saturday — the region's premier annual defence forum — setting out US policy on China, Taiwan, the South China Sea, Iran, and AI rivalry. The address was the first detailed public statement of US Indo-Pacific posture since Trump and Xi agreed to reset relations at their May summit in Beijing. Analysts noted Hegseth struck a firmer tone on Taiwan while softening economic competition language. China's Defence Minister Dong Jun declined to attend for the second consecutive year. For businesses operating across Indo-Pacific supply chains, the direction of US-China policy post-Beijing reset will be a key variable shaping trade costs through the second half of 2026.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/5/30/what-hegseths-comments-at-shangri-la-dialogue-say-about-us-foreign-policy",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AUSTRALIA · FUEL COSTS",
    "{{ECON_1_HEADLINE}}": "ACCC: Diesel Down 30% Since April Excise Cut — But the 26.3c/L Reversal Is Locked In for July 1",
    "{{ECON_1_SUMMARY}}": "The ACCC's May 22 weekly fuel monitoring update confirmed that the April 1 fuel excise halving has reduced retail diesel prices around 30% and petrol 28% across Australia's five major cities. The relief is real but time-limited: on June 30, the excise unconditionally reverts from 26.3c to 52.6c per litre — a 26.3c increase landing on every diesel vehicle from July 1. A trades business running three vehicles averaging 80L per fill twice weekly faces roughly $630 in additional monthly fuel cost from that date. Any quote being written today for work scheduled after June 30 needs to use post-excise fuel rates — not current pump prices. The current price is temporary. The July bill is not.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "💰 AUSTRALIA · FEDERAL BUDGET",
    "{{ECON_2_HEADLINE}}": "Budget 2026-27: $20K Instant Asset Write-Off Now Permanent — Loss Carry-Back Also Unlocked for Small Business",
    "{{ECON_2_SUMMARY}}": "Two meaningful small business wins from the 2026-27 Federal Budget take effect from 1 July 2026. The $20,000 instant asset write-off is now permanently legislated for businesses with turnover under $10 million — ending years of annual extensions and giving certainty to equipment purchase planning. Separately, companies with global turnover under $1 billion can carry a tax loss back against tax paid in the previous two years, improving cash flow in lean periods. For trades operators buying vehicles, compressors, spray equipment or scaffolding, the permanent write-off removes the annual timing risk. The budget also confirmed CGT small business concessions are maintained, while the broader 50% CGT discount is being replaced with inflation-adjusted indexation for gains from July 2027.",
    "{{ECON_2_URL}}": "https://business.gov.au/news/budget-2026-27",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · GOOGLE I/O",
    "{{TECH_1_HEADLINE}}": "Google Launches Gemini 3.5 Flash and Gemini Spark: AI That Acts on Your Behalf, Not Just Answers Questions",
    "{{TECH_1_SUMMARY}}": "Google's I/O 2026 keynote confirmed the shift from AI-as-chatbot to AI-as-agent. Gemini 3.5 Flash combines fast output with what Google calls 'frontier intelligence with action' — the model can execute multi-step tasks, not just generate text. Gemini Spark goes further: a 24/7 AI agent that reasons across your connected apps — calendar, email, documents, contacts — and takes actions on your behalf under your direction. Google also rebuilt its Search box for the first time in 25 years, now accepting images, files, videos and open browser tabs as simultaneous inputs. The practical shift for small business operators: AI tools are moving from 'help me draft this' to 'do this for me' — and the operators building AI habits now will be ahead of those still waiting to start.",
    "{{TECH_1_URL}}": "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/",

    "{{TECH_2_FLAG}}": "🔐 AI · SECURITY",
    "{{TECH_2_HEADLINE}}": "Intelligence Agencies Warn: AI Agents Can Be Hijacked — Five Key Risk Categories for Business Operators",
    "{{TECH_2_SUMMARY}}": "Cybersecurity and intelligence agencies from the US, UK, Australia and allies jointly released 'Careful Adoption of Agentic AI Services,' identifying five risk categories unique to AI agents that take actions: prompt injection (malicious instructions hidden in web content), excessive permissions granted to the agent, supply chain compromise in the AI toolchain, insufficient human oversight of AI-initiated actions, and insecure memory and data handling. The practical rule for small business operators using AI to send emails, respond to reviews, or process customer requests: keep human checkpoints on any AI action involving money, customer data, or outgoing communications. The automation benefit is real — the oversight layer is essential.",
    "{{TECH_2_URL}}": "",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 USA · MANUFACTURING",
    "{{ROBOT_1_HEADLINE}}": "Hyundai Orders 25,000 Electric Atlas Robots From Boston Dynamics — Largest Humanoid Deployment Commitment in History",
    "{{ROBOT_1_SUMMARY}}": "Hyundai Motor Group has placed an order for 25,000 Electric Atlas humanoid robots from Boston Dynamics to deploy across its US manufacturing facilities — the largest single humanoid unit commitment in manufacturing history. A May 18 technical demonstration showed Atlas lifting and carrying 45kg loads using reinforcement learning, compressing millions of hours of simulated practice into weeks of real-world training. Hyundai has simultaneously established a dedicated robotics parts procurement division and a software-defined factory promotion division to support the rollout, with full automotive line deployment targeted from 2028. At current humanoid pricing of $25,000–$37,000 per unit, the 25,000-unit order represents a capital commitment of $625M–$925M. That scale confirms humanoid robots in structured manufacturing have crossed the threshold from pilot programme to industrial platform — and the pace is accelerating.",
    "{{ROBOT_1_URL}}": "https://www.koreaherald.com/article/10756187",

    # Australia
    "{{AUS_1_HEADLINE}}": "Federal Budget 2026-27: CGT 50% Discount Abolished From July 2027 — Small Business Concessions Preserved",
    "{{AUS_1_SUMMARY}}": "The 2026-27 Federal Budget replaces the 50% capital gains tax discount with inflation-adjusted indexation for gains realised from 1 July 2027, with a minimum 30% effective rate on realised gains. The change affects investment property, shares and business asset disposals for individuals and trusts. Crucially, the Government confirmed existing CGT small business concessions are fully preserved — meaning sale of a business or active business asset under SBE thresholds remains eligible for rollover and retirement exemptions. Property investors and self-funded retirees face the largest impact. Trades business owners planning an exit or asset sale should be reviewing disposal timing with their accountant now — before July 2027.",
    "{{AUS_1_URL}}": "https://budget.gov.au/content/04-tax-reform.htm",

    "{{AUS_2_HEADLINE}}": "Cost of Living Survey: One in Eight Australian Adults Skipping Meals as Inflation Remains Above Target",
    "{{AUS_2_SUMMARY}}": "A recent ACOSS survey found one in eight Australian adults reporting they skipped meals due to financial pressure, with food insecurity highest among renters, households with children, and casual workers. Inflation remains above the RBA's 2–3% target band, driven by fuel, rent and food costs. While the April fuel excise cut provided temporary relief, the core cost-of-living squeeze is suppressing discretionary spending — including home maintenance and trades work. Operators with a residential customer base should expect continued price sensitivity through the second half of 2026.",
    "{{AUS_2_URL}}": "",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Free Public Transport Ends Tonight — Half-Price Fares Begin Tomorrow on All Metro and Regional Services",
    "{{VIC_1_SUMMARY}}": "Free public transport across Victoria ends at midnight tonight (Sunday 31 May), with half-price fares taking effect Monday 1 June 2026 and running through to 1 January 2027. The maximum full-fare daily cap drops from $11.40 to $5.70; concession fares fall from $5.70 to $2.85. All metro trains, trams, buses and regional V/Line coaches are included; SkyBus and ferries are excluded. Tap on as usual — the system calculates the half price automatically. For trades businesses with staff commuting by public transport to job sites, the transition is seamless. Victoria has committed approximately $432 million to fund the half-price period.",
    "{{VIC_1_URL}}": "",

    # Science
    "{{SCI_1_FLAG}}": "⚛️ QUANTUM · BREAKTHROUGH",
    "{{SCI_1_HEADLINE}}": "Stanford Engineers Build Room-Temperature Quantum Device Using 'Twisted Light' — Quantum Computing Out of the Freezer",
    "{{SCI_1_SUMMARY}}": "Researchers at Stanford University have developed a nanoscale quantum device that operates at room temperature by using 'twisted light' — photons that move forward while rotating, like a corkscrew — to entangle quantum states between light and electrons. The device pairs a patterned silicon nanostructure with a thin layer of molybdenum diselenide, a two-dimensional semiconductor. When twisted photons strike the material, their rotational spin transfers to electrons within it, creating the entanglement that quantum communication and computing depend on. Most quantum systems today require cooling to near absolute zero (−459°F), making them large and extremely expensive. This breakthrough, published in Nature Communications and reported May 28, opens a pathway toward miniaturised quantum devices — with near-term applications in quantum-secured communications and, over the longer term, compact quantum processors.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The Job Debrief Habit: How AI Turns Every Completed Job Into a Sharper Quote",
    "{{INSIGHT_BODY}}": "Most trades operators are excellent at doing work and getting to the next job. Very few have a system for capturing what they learned on the last one. Here's a habit that costs five minutes and compounds over time: at the end of every completed job, open an AI tool — Claude, ChatGPT, Gemini — and give it three sentences: what the job was, what took longer than quoted, and what you'd price differently next time. Then ask it to turn those three inputs into a one-paragraph note to your future self for the next quote of that type. Over three months, you'll build a reference library of job-specific lessons that reflect your actual operations, not a generic pricing guide. Most estimating errors aren't math errors — they're memory errors. A five-minute AI-assisted debrief, captured and retrievable, is the cheapest estimating improvement you'll ever make.",

    # Fun Facts
    "{{FACT_1}}": "Starbucks entered Australia in 2000 with plans for 150+ stores — and closed 61 of its 84 locations in a single day in July 2008. The chain had underestimated a local café culture built on espresso and barista craft since the Italian migration wave of the 1950s, where independent operators set quality standards the chain couldn't match. It remains one of the most documented examples of a major global brand being outcompeted on their home ground by small operators who knew their customers better.",

    "{{FACT_2}}": "A teaspoon of material from a neutron star would weigh approximately 10 million tonnes on Earth — roughly the same as all of humanity compressed into a space the size of a sugar cube. Neutron stars are the collapsed remnants of massive stars that have exploded as supernovae; their gravity is so extreme that protons and electrons are crushed together into neutrons. A typical neutron star packs 1.4 times the mass of our Sun into a sphere just 20 kilometres across — smaller than the distance across Melbourne's CBD.",

    "{{FACT_3}}": "The original Nintendo Game Boy (1989) had 8 kilobytes of RAM and a processor running at 4.19 megahertz — slower than a 1970s pocket calculator, and about 8,000 times less memory than a modern smartwatch. Its designers deliberately chose weaker hardware to extend battery life and keep the price low. That trade-off turned out to be exactly right: the Game Boy sold 118 million units across its lifespan and defined portable gaming for a generation.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the chef get promoted to head of the kitchen?",
    "{{JOKE_PUNCHLINE}}": "He always raised the steaks — and his margins never fell below medium.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Whether you think you can, or you think you can’t — you’re right.”",
    "{{CLOSING_ATTR}}": "— Henry Ford",
    "{{CLOSING_MESSAGE}}": "Sunday, 31 May 2026 — last day of the month, and the last day of free public transport across Victoria. Half-price fares kick in on metro trains, trams and buses from tomorrow morning, so if any of your team commutes by PT, they'll notice the tap-on cost changing. Showers are likely in the southeast suburbs today — Carrum Downs is squarely in that band — so outdoor work this morning is marginal at best. The June 30 fuel excise cliff is now exactly 30 days away: if you haven't updated post-June-30 fuel rates in your quoting template yet, this Sunday morning — with no job pressure — is the right time to do it. Enjoy your Sunday, Liall.",
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
