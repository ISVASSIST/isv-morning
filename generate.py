#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Monday, 23 November 2026',
'{{WEATHER_1}}': 'MON 23 NOV · 🌥️ Cloudy and cooler, about 13-22°C, chance of an early shower',
'{{WEATHER_2}}': 'TUE 24 NOV · ☀️ Cool and mostly sunny, about 9-17°C, the coldest day of the week',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'WED 25 NOV · 🌤️ Warming up, partly cloudy, top of about 25-26°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'THU 26 NOV · ⛅ Warm, mid-20s, chance of an afternoon storm',
'{{WEATHER_5}}': 'FRI 27 NOV · 🌦️ Warm and humid, high 20s, showers or a storm possible later',
'{{WEATHER_ALERT}}': "After Sunday's heat and storms, the week starts cooler. Monday should be cloudy with a top in the low 20s and the chance of a shower early, then Tuesday is the cold one, starting near 9°C and only reaching about 17°C, but mostly sunny and dry. Wednesday warms back up to the mid-20s. Thursday and Friday stay warm, but some forecasts show afternoon storms both days, so plan any outdoor coating work for Tuesday and Wednesday and keep an eye on the radar later in the week. Please note that the forecast sites don't agree by a few degrees this week, so check the BoM forecast for Carrum Downs before you lock in an outdoor job.",
'{{WORLD_1_FLAG}}': '🌍 TURKEY · COP31',
'{{WORLD_1_HEADLINE}}': 'COP31 Climate Summit Collapses With No Final Deal',
'{{WORLD_1_SUMMARY}}': "The COP31 climate talks in Antalya, Turkey, ended on Sunday without a final agreement. The summit's president told delegates the proposed \"Antalya Pact\" had failed. The main fight was over fossil fuels. The final draft left out any direct mention of phasing out coal, oil and gas, and the EU, the UK and small island nations wouldn't accept it. Climate finance was the other dealbreaker, according to Australia's Chris Bowen, who helped lead the negotiations. The talks ran more than 44 hours past their scheduled Friday finish, the longest ever. A few smaller decisions survived, and the 2023 Dubai agreement to transition away from fossil fuels still stands.",
'{{WORLD_1_URL}}': 'https://www.npr.org/2026/11/22/nx-s1-6046195/cop31-climate-talks-close-disappointment',
'{{WORLD_2_FLAG}}': '🇮🇷 MIDDLE EAST · SHIPPING',
'{{WORLD_2_HEADLINE}}': 'More Tankers Hit in the Strait of Hormuz as Iran Tightens Its Grip',
'{{WORLD_2_SUMMARY}}': "British maritime authorities say two tankers were hit by unidentified projectiles near Oman, while Iran keeps restricting shipping through the Strait of Hormuz. Iran's navy also says an oil tanker caught fire after hitting a naval mine east of the strait. Those mine claims haven't been independently verified. The US has blockaded Iranian ports and is escorting tankers through the waterway. Iran says it would reopen the strait if the US accepts its conditions. About a fifth of the world's oil normally passes through Hormuz, so any flare-up there can push fuel prices back up.",
'{{WORLD_2_URL}}': 'https://www.aljazeera.com/news/2026/11/21/tankers-hit-in-strait-of-hormuz-as-iran-tightens-grip-on-shipping',
'{{ECON_1_FLAG}}': '🏬 RETAIL · INSOLVENCY',
'{{ECON_1_HEADLINE}}': 'General Pants Collapses as Retail Payment Defaults Hit Their Worst Level Since 2016',
'{{ECON_1_SUMMARY}}': "Fashion chain General Pants Co has gone into voluntary administration, with about 500 jobs at risk. Its 35 stores and online shop are still trading for now. It follows David Jones, which is closing stores and cutting more than 1,500 jobs. CreditorWatch says retail payment defaults are up 43% on a year ago, the worst level since 2016. ASIC recorded more than 12,000 administrator and liquidator appointments in the first 10 months of the year. For a small business, the lesson is to keep a close eye on who owes you money. Chase overdue invoices early and ask for deposits on bigger jobs.",
'{{ECON_1_URL}}': 'https://www.canberratimes.com.au/story/9394529/general-pants-collapse-fuels-retail-crisis-fears/',
'{{ECON_2_FLAG}}': '⛽ FUEL',
'{{ECON_2_HEADLINE}}': 'Wholesale Fuel Prices Kept Falling All Last Week, but Hormuz Is Still a Risk',
'{{ECON_2_SUMMARY}}': "The Australian Institute of Petroleum's terminal gate prices fell every day from Monday 16 to Friday 20 November in every capital city. Pump prices usually follow a few days later, so diesel and petrol should keep easing early this week. The ACCC's last five-city figures had average diesel at 266.4 cents a litre, down 9.4 cents on the week. The risk is the Strait of Hormuz, where more tankers were hit over the weekend. If that pushes global oil prices up, the drop could stall. If you've been putting off filling the work vehicles, the next few days look like a good time.",
'{{TECH_1_FLAG}}': '📞 AI · YOUR PHONE',
'{{TECH_1_HEADLINE}}': "Google's Gemini Can Now Ring Businesses on a Customer's Behalf",
'{{TECH_1_SUMMARY}}': "Google has built its Duplex calling technology into Gemini, so the AI can now phone a business for a user, for example to check opening hours, availability or a price. Every call starts by saying it's an automated system calling from Google. Businesses that don't want these calls can switch them off in their Google Business Profile: go to business.google.com, then More, Business Profile settings and Advanced settings. You can also say \"Please stop calling my business\" during a call. Availability differs by country, so it may not reach Australia straight away. It's worth deciding now whether you'd rather take these calls or block them.",
'{{TECH_1_URL}}': 'https://research.google/blog/how-google-duplex-evolved-to-also-call-businesses-for-you-in-gemini/',
'{{TECH_2_FLAG}}': '🧾 AI · BOOKKEEPING',
'{{TECH_2_HEADLINE}}': 'ChatGPT Adds Plugins Aimed at Small Business Sales and Accounts',
'{{TECH_2_SUMMARY}}': "OpenAI has released a batch of business plugins for ChatGPT, including a Sales plugin and more than 30 new or updated partner plugins. Small-business roundups also report a new Accounting plugin that helps prepare invoice entries, reconcile records and draft month-end reports. Separately, OpenAI's \"Businesses in ChatGPT\" beta lets companies claim and verify their business and add details like products and prices. Exact features and availability in Australia may differ, so check the settings in your own account. The practical upside is that routine bookwork could move into a tool you might already pay for.",
'{{ROBOT_1_FLAG}}': '🏗️ CONSTRUCTION ROBOTICS',
'{{ROBOT_1_HEADLINE}}': 'Humanoid Robots on the Jobsite Will Bring New Safety Risks, Industry Warns',
'{{ROBOT_1_SUMMARY}}': "A Roofing Magazine piece published on 22 November looks at what happens when humanoid robots like Tesla's Optimus start turning up on building sites. It warns that a robot that moves a load unexpectedly or reacts badly to changing site conditions could seriously injure someone. It also raises unanswered questions about insurance and who's liable when a robot causes an accident. Industry experts expect robots to start with material handling, staging and maintenance work long before they take on production work on a real jobsite. McKinsey has suggested large-scale use of humanoids on construction sites may still be about a decade away. For now, the safety rules for robots on site are still being worked out.",
'{{ROBOT_1_URL}}': 'https://roofingmagazine.com/optimus-on-the-jobsite-humanoid-robots-and-the-next-generation-of-construction-risk/',
'{{AUS_1_HEADLINE}}': 'Penny Wong to Name AI as a Major National Security Challenge',
'{{AUS_1_SUMMARY}}': "Foreign Minister Penny Wong will give a major foreign policy speech to Parliament this week that treats artificial intelligence as a \"major foreign policy and national security challenge\". The speech is called \"Securing Australia's future in a changing world\". She's expected to warn that AI is giving foreign actors new tools to disrupt democracies, with examples of Iran and Russia using deepfakes and fake articles to sway public opinion. The government is also working on mandatory AI safety standards and plans to legislate national AI rules in 2027. The speech follows warnings from Australia's spy chief about foreign interference in building AI data centres.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-22/federal-politics-penny-wong-foreign-policy-ai-threat/107414236',
'{{AUS_2_HEADLINE}}': 'Spirit of Tasmania Ferries Ordered Off Autopilot While Steering Faults Are Probed',
'{{AUS_2_SUMMARY}}': "The ABC reports that the Australian Maritime Safety Authority has ordered TT-Line to stop using autopilot on any part of the new Spirit of Tasmania ferries' Bass Strait crossings while it investigates steering problems on one of the ships. It follows two incidents. On 24 October, Spirit of Tasmania V's autopilot couldn't stop a turn. On 5 November, Spirit of Tasmania IV's steering wheel didn't respond when the crew switched from autopilot to manual. An inspection in Geelong found a fault in the steering console's mechanical and electrical systems. The ATSB is also investigating. Until it's sorted, crews will have to steer the crossings manually.",
'{{VIC_1_HEADLINE}}': 'Five Teenagers Arrested After Fatal Stabbing in Melbourne CBD',
'{{VIC_1_SUMMARY}}': "Victoria Police are investigating three separate stabbings across Melbourne in less than eight hours over the weekend. A 21-year-old man died after he was allegedly stabbed in the CBD, and five teenagers have been arrested over his death. Police are still looking for a suspect after a separate stabbing in Bourke Street Mall. A third person was stabbed in Broadmeadows, in the city's north. Police haven't said the three attacks are linked. It comes in the final week before Saturday's state election.",
'{{SCI_1_FLAG}}': '🔭 SPACE',
'{{SCI_1_HEADLINE}}': 'Webb Telescope Finds a Black Hole That Grew Faster Than Its Own Galaxy',
'{{SCI_1_SUMMARY}}': "Astronomers using the James Webb Space Telescope have found what may be an \"overmassive\" black hole in a young galaxy called MARTA-3887, seen as it was in the early universe. The black hole's mass is about 2.3% of the mass of all the galaxy's stars, which is roughly 100 times more than we'd expect from galaxies nearby. That suggests the black hole grew faster than the galaxy built its stars. The team, led by Mirko Curti of Italy's INAF, used several lines of evidence. The work is still a preprint and hasn't been peer reviewed yet. Phys.org covered it on 22 November.",
'{{INSIGHT_TITLE}}': 'When an AI Rings Your Business for a Quote, Make Sure It Hears the Right Answer',
'{{INSIGHT_BODY}}': "AI assistants like Gemini are starting to phone businesses on customers' behalf to check hours, availability and prices. That means the first call about a job might come from a computer, not a person. Before that happens, decide how you want to handle it. Write a short script for whoever answers the phone: what services you offer, your usual lead time, whether you do site visits, and that quotes are only given after you've seen the job. Then make sure your Google Business Profile matches the script, with correct hours, services, service area and a phone number that's actually answered. If you'd rather not deal with robot callers, you can switch them off in the profile's Advanced settings. Either way, never give a firm price over the phone to an AI. Offer to send a written quote instead, so you keep control of the paperwork.",
'{{FACT_1}}': "The 1956 Melbourne Olympics opened at the MCG on 22 November 1956, 70 years ago yesterday, making them the first Games held in the Southern Hemisphere. Australia's strict animal quarantine rules meant the equestrian events had to be held in Stockholm, Sweden, months earlier.",
'{{FACT_2}}': "COP31 in Antalya ran more than 44 hours past its scheduled finish, breaking the record set by COP25 in Madrid in 2019 for the longest climate summit.",
'{{FACT_3}}': "A red giant in the Andromeda galaxy nicknamed \"Big Bao\" is estimated to be about 350 times wider than the Sun and 18,000 times brighter, and astronomers watched it erupt after a smaller companion star spiralled into it.",
'{{JOKE_SETUP}}': "Why did the plasterer turn off the election ads on Monday morning?",
'{{JOKE_PUNCHLINE}}': "He'd seen enough people patching over cracks and hoping nobody checks before the final coat.",
'{{CLOSING_QUOTE}}': '"Quality is never an accident; it is always the result of intelligent effort."',
'{{CLOSING_ATTR}}': '— John Ruskin',
'{{CLOSING_MESSAGE}}': "It's Monday, and the week starts cooler after Sunday's storms. Tuesday is the chilly one but it should be dry, and Wednesday is the pick of the week for outdoor work before storms become a chance again from Thursday. Fuel should keep easing for a few more days, the state election is on Saturday, and with another big retailer in administration, it's a good week to chase any overdue invoices. Have a good week.",
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
