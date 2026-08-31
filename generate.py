#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 01 September 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 1 Sep (BOM)
    "{{WEATHER_1}}": "TUE 1 SEP · 🌬️ Mostly sunny, very windy, high chance of a shower late · 8–15°C",
    "{{WEATHER_2}}": "WED 2 SEP · 🌧️ Cloudy, high chance of showers, most likely morning · 9–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 3 SEP · 🌧️ Showers, easing later, blustery nor'wester · 8–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 4 SEP · ⛅ Partly cloudy, isolated shower, cooler · 7–14°C",
    "{{WEATHER_5}}": "SAT 5 SEP · ☀️ Mostly sunny, light winds, settling down · 7–15°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or the Mornington Peninsula. Spring's first week is arriving with a proper blast of northerly wind and showers rather than sunshine, easing back to calmer, drier conditions by the weekend.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 STRAIT OF HORMUZ · US AND IRAN TRADE STRIKES, OIL SURGES",
    "{{WORLD_1_HEADLINE}}": "US Strikes Iranian Launchers Near Strait of Hormuz, Iran Retaliates, Ending Weeks of Calm",
    "{{WORLD_1_SUMMARY}}": "US forces struck two Iranian rocket launchers on Larak Island on Sunday after spotting Revolutionary Guard units preparing to fire mines into the Strait of Hormuz, and Iran struck back early Monday — the first exchange of attacks in a month, sending Brent crude up more than 3% to above $90 a barrel and reviving fears of a fresh squeeze on global fuel supply.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/08/30/politics/us-iran-strikes-larak-island",

    "{{WORLD_2_FLAG}}": "🇳🇵 NEPAL-TIBET · FLOOD DEATH TOLL TOPS 900, 4,700+ MISSING",
    "{{WORLD_2_HEADLINE}}": "Nepal-Tibet Flood Death Toll Surpasses 900 as More Than 4,700 Remain Missing",
    "{{WORLD_2_SUMMARY}}": "The toll from the Himalayan flash floods that struck the Nepal-Tibet border ten days ago has climbed past 900, with 903 confirmed dead in Nepal alone and more than 4,700 still missing; four more Australians were identified among the missing on Monday as rescue efforts along the Trishuli River continue.",
    "{{WORLD_2_URL}}": "https://abcnews.com/International/nepal-tibet-flood-death-toll-surpasses-900-officials/story?id=136081207",

    # Economics
    "{{ECON_1_FLAG}}": "📉 ASX · STAR ENTERTAINMENT LOSS DEEPENS MARKET SLIDE",
    "{{ECON_1_HEADLINE}}": "ASX Closes Lower as Star Entertainment's $307 Million Loss Raises Fresh Doubts Over Its Survival",
    "{{ECON_1_SUMMARY}}": "The S&P/ASX 200 slipped 0.18% to 9,076 points on Monday, weighed down by losses in the gold, metals and mining sectors and a subdued lead from Wall Street, as casino operator Star Entertainment posted a $307 million annual loss that has analysts openly questioning whether the company can keep trading.",
    "{{ECON_1_URL}}": "https://www.abc.net.au/news/2026-08-31/asx-markets-business-live-news-wall-street-slides/107095734",

    "{{ECON_2_FLAG}}": "⛽ FUEL · OIL JUMPS ON HORMUZ STRIKES, BOWSER RISES LOOM",
    "{{ECON_2_HEADLINE}}": "Oil Prices Jump After Fresh US-Iran Strikes, Setting Up Another Round of Bowser Pain This Week",
    "{{ECON_2_SUMMARY}}": "Brent crude rose more than 3% to above $90 a barrel after Sunday's exchange of strikes near the Strait of Hormuz, adding fresh upward pressure on a diesel price already sitting around $2.30 a litre nationally and Melbourne unleaded near 207 cents a litre — bad timing for any business still absorbing last month's full return of the fuel excise.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI FOR SMBs · CASHFREE'S 'RELAY' AUTOMATES PAYMENT CHASING",
    "{{TECH_1_HEADLINE}}": "Cashfree Launches 'Relay', an AI Agent That Chases Late Payments and Runs Payment Admin for Small Businesses",
    "{{TECH_1_SUMMARY}}": "Payments platform Cashfree has taken its AI 'Super Agent' Relay from beta to general availability, letting small businesses describe in plain language what they want handled — retrying failed payments, chasing abandoned invoices, confirming orders, filing disputes before deadlines — with Cashfree citing an average small business spending 60 hours a week on payment admin that Relay aims to cut to under 45 minutes.",
    "{{TECH_1_URL}}": "https://ibsintelligence.com/ibsi-news/cashfrees-relay-brings-ai-agents-to-smb-payment-operations/",

    "{{TECH_2_FLAG}}": "🍎 APPLE · JOHN TERNUS TAKES OVER AS CEO TODAY, AI STRATEGY IN FOCUS",
    "{{TECH_2_HEADLINE}}": "Tim Cook Steps Aside as Apple CEO Today, Handing John Ternus a Company Under Pressure to Fix Its AI Strategy",
    "{{TECH_2_SUMMARY}}": "Apple's leadership change takes effect today, with hardware chief John Ternus becoming CEO and Tim Cook moving to executive chairman — a transition announced back in April that now lands squarely on Ternus's desk just as Apple races to catch up on Siri and Apple Intelligence after a string of delays.",
    "{{TECH_2_URL}}": "https://www.apple.com/newsroom/2026/04/tim-cook-to-become-apple-executive-chairman-john-ternus-to-become-apple-ceo/",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🧹 PHYSICAL AI · HUMANOID MAKER BUYS ITS WAY INTO CLEANING ROBOTS",
    "{{ROBOT_1_HEADLINE}}": "Humanoid Robot Maker NEURA Robotics Acquires Cleaning Specialist ADLATUS, Fresh Off a €1.2 Billion Raise",
    "{{ROBOT_1_SUMMARY}}": "German humanoid developer NEURA Robotics has bought Ulm-based ADLATUS Robotics outright, folding its autonomous cleaning machines into NEURA's 'physical AI' platform weeks after closing a €1.2 billion funding round — a sign the humanoid robotics boom is starting to reach the unglamorous, everyday equipment that keeps commercial floors and factories running.",
    "{{ROBOT_1_URL}}": "https://tech.eu/2026/08/24/neura-robotics-acquires-adlatus-to-bring-physical-ai-to-autonomous-cleaning",

    # Australia
    "{{AUS_1_HEADLINE}}": "Federal Government Unveils 'Right to Erasure' in Sweeping Draft Privacy Law Overhaul",
    "{{AUS_1_SUMMARY}}": "The Attorney-General has released draft privacy reforms including a 'right to erasure' letting people demand large platforms delete their personal data, alongside a new IDLock identity-verification tool coming to MyGov from 2027; the erasure right applies only to platforms with $500 million-plus revenue or 2.5 million monthly users, with submissions open until 18 September.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-31/attorney-general-says-no-ban-on-smart-glasses-draft-privacy-laws/107097852",

    "{{AUS_2_HEADLINE}}": "One Nation Wins First-Ever WA Lower House Seat in Secret Harbour By-Election Upset",
    "{{AUS_2_SUMMARY}}": "One Nation's Luke Herdegen has claimed the traditionally safe Labor seat of Secret Harbour with 42.3% of the vote, the party's first lower house win in Western Australian history, in a result analysts say reflects growing voter frustration with the major parties in outer-suburban seats.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Opens Australia's First Offshore Wind Auction, Chasing Power for 1.5 Million Homes",
    "{{VIC_1_SUMMARY}}": "Energy Minister Jaclyn Symes has opened bidding for the state's first 2 gigawatts of offshore wind off the Gippsland coast, with contracts assessed on cost, deliverability and benefits for local workers and businesses, and expected to be awarded in 2028 — a long runway, but one that could eventually mean cheaper, more secure power for energy-hungry trades and manufacturers.",

    # Science
    "{{SCI_1_FLAG}}": "🐍 BIOLOGY · WHY SNAKE EMBRYOS ALWAYS COIL THE SAME WAY",
    "{{SCI_1_HEADLINE}}": "Scientists Finally Explain Why Snake Embryos Almost Always Coil to the Right",
    "{{SCI_1_SUMMARY}}": "Examining more than 800 embryo images, a UBC-led team found the coiling direction comes down to simple mechanics — the body elongates faster than the shorter gut can keep pace, and the yolk sitting on the embryo's left side pushes the curling body to curve right; published in Current Biology on 31 August, the finding helps explain how snakes build one of the animal kingdom's most extreme body plans.",

    # Business insight
    "{{INSIGHT_TITLE}}": "Canberra's New 'Right to Erasure' Privacy Law Is Aimed at Big Tech — But the Habit It's Asking For Applies to You Too",
    "{{INSIGHT_BODY}}": "The draft privacy reforms unveiled yesterday technically only bite platforms with $500 million-plus in revenue, so no trades business needs to panic about compliance. But the 'right to erasure' reflects where community expectations are heading on personal data, and most small operators are sitting on more of it than they realise — customer phone numbers and addresses in a phone, before-and-after job photos with someone's house in the background, quotes with names and details saved in an AI tool. It costs nothing to start being deliberate about it now: know what you're storing, delete what you don't need, and ask any AI tool you use where customer data actually goes. Getting ahead of a habit is a lot cheaper than retrofitting one after a law forces the issue.",

    # Fun facts
    "{{FACT_1}}": "Laminated safety glass was discovered by accident in 1903, when French chemist Édouard Bénédictus dropped a glass flask coated in dried collagen film and found it had cracked into a spiderweb pattern instead of shattering — he later recalled a newspaper report about car accident injuries from broken windscreens and patented the idea within weeks.",
    "{{FACT_2}}": "The traffic cone — the 'witches hat' on every job site — was patented in 1943 by Los Angeles street painter Charles D. Scanlon, who made it from rubber specifically so cars could drive over it without damage, unlike the wooden markers it replaced.",
    "{{FACT_3}}": "Despite producing only a sliver of the world's diamonds by volume, Western Australia's Argyle mine supplied more than 90% of the world's pink diamonds before it closed in 2020 — prices for the rare stones have kept climbing ever since, as none of the handful of mines still operating produce them in meaningful numbers.",

    # Joke
    "{{JOKE_SETUP}}": "A young auto electrician was asked how he always found a fault in a car's wiring faster than anyone else in town.",
    "{{JOKE_PUNCHLINE}}": "He said the trick was never chasing the spark — always tracing it back to where the current started.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Do the difficult things while they are easy and do the great things while they are small.\"",
    "{{CLOSING_ATTR}}": "— Lao Tzu",
    "{{CLOSING_MESSAGE}}": "It's the first day of spring in Carrum Downs, and it's arriving with a proper blast of northerly wind and showers rather than sunshine — a fair excuse to get any indoor quoting or admin done before conditions ease by the weekend. With oil prices jumping on fresh Middle East strikes and the diesel bill already elevated, it's worth locking in any fuel-sensitive quotes now rather than waiting for the bowser to catch up.",
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
