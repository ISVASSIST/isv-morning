#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Sunday, 14 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sun 14 Jun
    # Partly cloudy today with fog risk; heavy rain Mon; easing Tue-Thu
    "{{WEATHER_1}}": "SUN 14 · ⛅ Fog/cloudy · 14°C",
    "{{WEATHER_2}}": "MON 15 · 🌧 Rain heavy · 13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "TUE 16 · ⛅ Easing · 12°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "WED 17 · ⛅ Shower PM · 13°C",
    "{{WEATHER_5}}": "THU 18 · 🌤 Partly cloudy · 13°C",
    "{{WEATHER_ALERT}}": "⚠ FOG SUN AM · HEAVY RAIN MON",

    # World
    "{{WORLD_1_FLAG}}": "🇰🇷 South Korea",
    "{{WORLD_1_HEADLINE}}": "Ousted South Korean President Yoon Sentenced to 30 More Years Over North Korea Drone Plot",
    "{{WORLD_1_SUMMARY}}": "A Seoul court handed former President Yoon Suk Yeol an additional 30-year prison sentence — stacked on top of a life term he received in February — after finding him guilty of conspiring to order propaganda drones over Pyongyang in October 2024 to provoke a North Korean military response and manufacture a justification for martial law. His former Defence Minister received the same term. Yoon, 65, is now serving what amounts to a permanent sentence across two separate convictions for two separate acts of abuse of power and treason.",
    "{{WORLD_1_URL}}": "https://www.foxnews.com/world/former-south-korean-president-yoon-suk-yeol-sentenced-30-years-over-north-korea-drone-flights",

    "{{WORLD_2_FLAG}}": "🇬🇧 UK · Belfast",
    "{{WORLD_2_HEADLINE}}": "Riots Erupt Across Belfast for Second Night as Far-Right Groups Exploit Stabbing — Elon Musk Accused of Stoking Unrest",
    "{{WORLD_2_SUMMARY}}": "Violent anti-immigrant protests spread across Belfast for a second consecutive night after a brutal knife attack sparked far-right mobilisation. Masked men set fires and hurled bricks and bottles at police; the Northern Ireland Fire and Rescue Service responded to 62 incidents in a single evening. Elon Musk drew fierce condemnation after sharing posts on X amplifying the violence. Northern Ireland First Minister Michelle O'Neill called it 'disgusting cowardice' and a government minister labelled the riots 'racist thuggery.' Northern Ireland police deployed water cannons and made multiple arrests.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/world/united-kingdom/belfast-riots-elon-musk-anti-immigrant-violence-stabbing-rcna349384",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ Fuel Watch · 16 Days",
    "{{ECON_1_HEADLINE}}": "Australia's Fuel Excise Cut Expires June 30 — Diesel Jumps 26 Cents Per Litre Overnight Into FY2027",
    "{{ECON_1_SUMMARY}}": "The federal government's temporary halving of the fuel excise — saving diesel operators approximately 26.3 cents per litre since April 1 — expires at midnight on June 30, the same moment FY2027 begins. For trades businesses running diesel fleets, the cost jump is immediate and unavoidable. Any job quoted at current fuel rates but starting in July needs its margins reviewed now. With 16 days remaining, this week is the window to re-run job costings, adjust fleet allowances, and update any standard rates that were built on the reduced excise assumption.",
    "{{ECON_1_URL}}": "https://wealthworks.com.au/blog/fuel-excise-cut-april-2026-how-it-works-petrol-diesel-savings-australia",

    "{{ECON_2_FLAG}}": "🏦 RBA · Tuesday",
    "{{ECON_2_HEADLINE}}": "RBA Meets Tuesday — First Rate Cut Tipped for August If Ceasefire Holds and Inflation Eases",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank meets on Tuesday June 16 with a near-unanimous market consensus for a hold at 4.35%. But with CBA and NAB both removing rate hike forecasts, and some economists now tipping a cut as early as August if the US-Iran ceasefire stabilises oil prices through July, the post-decision statement will carry significant weight. For small businesses carrying variable-rate equipment loans or business credit, a cut this quarter would be the first meaningful debt relief since 2022. Watch the RBA's language on Tuesday afternoon — it will be the clearest signal yet on whether the rate peak is confirmed.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · Workforce",
    "{{TECH_1_HEADLINE}}": "Snap Cuts 1,000 Jobs as AI Writes 65% of Its New Code — Follows Meta's 8,000-Job AI Pivot Last Month",
    "{{TECH_1_SUMMARY}}": "Snapchat parent Snap axed approximately 1,000 employees — 16% of its global workforce — directly citing AI generating the majority of new code and taking over operations roles. CEO Evan Spiegel confirmed AI now produces more than 65% of all new code written at Snap, with the restructuring projected to save over $500 million annually. This follows Meta's 8,000-role reduction last month, also AI-driven. Two of the world's largest social platforms have now formally replaced headcount with AI rather than supplementing it — and the structural shift is spreading beyond tech into every sector where repetitive skilled work can be automated.",
    "{{TECH_1_URL}}": "https://www.crescendo.ai/news/latest-ai-news-and-updates",

    "{{TECH_2_FLAG}}": "📊 AI · Commerce",
    "{{TECH_2_HEADLINE}}": "Adobe: AI-Generated Traffic to Retail Sites Up 393% — Converts to Sales 42% Better Than Other Channels",
    "{{TECH_2_SUMMARY}}": "Adobe Digital Insights Q1 2026 data shows AI-driven referral traffic to US retail websites surged 393% year-on-year, and that traffic converted to sales 42% more effectively than traffic from search, social, or email. Customers are increasingly discovering businesses through AI assistants rather than Google. For small trades operators with online quote forms or booking pages, the implication is clear: businesses optimised for AI discovery are picking up a disproportionate share of new enquiries without any additional marketing spend.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 Robotics · IPO",
    "{{ROBOT_1_HEADLINE}}": "EngineAI Files Confidentially for Hong Kong IPO as New Shenzhen Factory Ships First T800 Humanoid Robots",
    "{{ROBOT_1_SUMMARY}}": "Shenzhen-based EngineAI filed confidentially for a Hong Kong stock exchange listing on June 12, engaging China International Capital Corp and Citic Securities as underwriters. Founded in 2023 and valued above $1.5 billion after a Series B in April, EngineAI opened a 12,000 square metre Shenzhen factory on June 1 and began shipping its T800 humanoid robot — with a production line targeting 10,000 units per year. If completed, the IPO would mark one of the first publicly listed pure-play humanoid robotics companies globally, a milestone expected to unlock significant new institutional capital for the sector.",
    "{{ROBOT_1_URL}}": "https://blog.mean.ceo/robotics-news-june-2026/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Face Türkiye in 2026 World Cup Opener Today — Kick-Off 2pm AEST From Vancouver",
    "{{AUS_1_SUMMARY}}": "Australia begins their 2026 FIFA World Cup campaign at BC Place in Vancouver against Türkiye today at 2pm AEST — a rare civilised viewing hour for Australian fans. Coach Tony Popovic's squad includes captain Mathew Ryan and veteran Mathew Leckie, both set to equal Tim Cahill's record of four World Cup appearances. Group D also includes hosts USA (June 20) and Paraguay (June 26). With the expanded 48-team format and a realistic path through the group stage, this is arguably Australia's strongest World Cup position since the 2006 Germany campaign.",
    "{{AUS_1_URL}}": "https://socceroos.com.au/news/match-preview-australia-v-turkiye-fifa-world-cup-2026tm",

    "{{AUS_2_HEADLINE}}": "Fair Work Commission Hears INPEX Ichthys LNG Strike Application — NT Gas Supply Under Watch",
    "{{AUS_2_SUMMARY}}": "The Fair Work Commission held a hearing Friday on INPEX's application regarding protected industrial action at the Ichthys LNG facility in Darwin. A disruption to the facility could tighten domestic east-coast gas supply at an already sensitive time — with Middle East tensions keeping energy markets volatile and the fuel excise relief expiring June 30. Energy-intensive businesses and logistics operators are watching the outcome closely for any flow-on to input costs in Q1 FY2027.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Free World Cup Live Screenings at Bunjil Place Narre Warren — Every Match on Outdoor Screen Through July 19",
    "{{VIC_1_SUMMARY}}": "Bunjil Place in Narre Warren — ten kilometres from Carrum Downs — is screening every 2026 FIFA World Cup match live and free on its outdoor screen through the tournament final on July 19. The Socceroos' opener against Türkiye kicks off this afternoon at 2pm. With 104 matches scheduled across 48 teams, there is live football on virtually every day through mid-July. A worthwhile way to catch the big games without a pub cover charge — check the Bunjil Place website for session times and weather contingencies.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 Physics · Neutrinos",
    "{{SCI_1_HEADLINE}}": "China's Giant JUNO Observatory Publishes First Results in Nature — Neutrino Measurements 1.6× More Precise Than All Previous Experiments Combined",
    "{{SCI_1_SUMMARY}}": "The Jiangmen Underground Neutrino Observatory (JUNO) — a 20,000-tonne liquid scintillator sphere buried 700 metres underground in southern China — published its first physics result as the cover article in Nature on June 10, with ScienceDaily coverage on June 12. Using just 59 days of data collected in late 2025, JUNO improved precision on two key neutrino oscillation parameters by a factor of 1.6 over the best combined results from decades of prior global experiments. Neutrinos are the universe's most abundant particles after photons; pinning down their mass hierarchy could help resolve why matter came to dominate over antimatter — and ultimately why the universe exists at all.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Two Weeks to EOFY: How AI Can Digitise Your Paper Trail Before June 30",
    "{{INSIGHT_BODY}}": "With June 30 exactly sixteen days away, most small trades businesses have job cards, photo receipts, delivery dockets, and handwritten materials notes scattered across the ute, a desk drawer, and three different email threads — and the accountant needs all of it. AI document tools can now photograph a paper job card, extract the key details, create a searchable digital record, and categorise it for tax purposes in under 60 seconds per document. Running a weekly AI sweep through your phone's camera roll — photos of receipts, supplier dockets, purchase orders — can compress three hours of bookkeeping prep into thirty minutes. Here is the practical approach: open Claude or ChatGPT on your phone right now, photograph a pile of paper documents, and ask the AI to extract the date, supplier, amount, and job reference from each one. Paste the results into a spreadsheet and you have a clean, dated transaction log your accountant can use without chasing you. The accountant deadline is not June 30 — it is the fortnight before June 30, when they need time to process everything. Starting today means you hand over clean records, not a shoebox. That difference alone can save two to four hours of billable accounting time at the end of the year.",

    # Fun Facts
    "{{FACT_1}}": "The Great Ocean Road was carved through 243 kilometres of Victoria's rugged southwest coastline by 3,000 returned World War I soldiers between 1919 and 1932, using picks, shovels, and gelignite — no heavy machinery was used. It took thirteen years to complete and is officially classified as the world's largest war memorial. The soldiers received only basic wages, contributing their labour as a tribute to Australian servicemen lost in the war.",

    "{{FACT_2}}": "Earth's magnetic north pole does not sit at the geographic North Pole — it is currently drifting toward Siberia at roughly 50 kilometres per year and has moved more than 2,300 kilometres since systematic records began in 1831. In some parts of Australia, this magnetic declination means a compass points up to 12 degrees away from true geographic north. It is why professional surveyors always reference true north coordinates rather than magnetic bearings, and why navigational charts carry a declination correction value.",

    "{{FACT_3}}": "Graphene — a single atom-thick sheet of carbon atoms first isolated in 2004 by Andre Geim and Konstantin Novoselov at Manchester University — is approximately 200 times stronger than steel by weight and conducts electricity better than copper at room temperature. The pair received the 2010 Nobel Prize in Physics for the discovery. A graphene sheet large enough to cover a football field would weigh less than four grams.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the site supervisor always make the best scrambled eggs?",
    "{{JOKE_PUNCHLINE}}": "Because he knew exactly when to pull them off the heat — leave it one minute too long and you've got a rework.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Even if you’re on the right track, you’ll get run over if you just sit there.”",
    "{{CLOSING_ATTR}}": "— Will Rogers",
    "{{CLOSING_MESSAGE}}": "The Socceroos kick off at 2pm AEST this afternoon — Turkey in Vancouver, a rare civilised-hour World Cup match for Australian viewing. Carrum Downs has partly cloudy skies today with a fog risk this morning, but heavy rain is forecast for Monday so anything worth doing outdoors is worth doing today. Sixteen days to the end of the financial year, and the fuel excise cut disappears at midnight on June 30 regardless of what happens in Tehran. A Sunday spent on your paper trail and your July job pricing could save you a very stressful first week of FY2027, Liall.",
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
