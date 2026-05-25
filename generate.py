#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 26 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 26 May (BOM forecast)
    "{{WEATHER_1}}": "TUE 26 · 🌧 Showers · 14°C",
    "{{WEATHER_2}}": "WED 27 · 🌧 Showers · 13°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 28 · 🌦 Showers · 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 29 · 🌦 Showers · 14°C",
    "{{WEATHER_5}}": "SAT 30 · 🌥 Cloudy · 14°C",
    "{{WEATHER_ALERT}}": "⛈ T-STORM RISK TONIGHT",

    # World
    "{{WORLD_1_FLAG}}": "🇷🇺🇺🇦 RUSSIA · UKRAINE",
    "{{WORLD_1_HEADLINE}}": "Russia Fires Hypersonic Oreshnik Missile at Kyiv in War's Largest Overnight Barrage — 4 Dead, ~100 Injured",
    "{{WORLD_1_SUMMARY}}": "Russian forces launched the largest single-night combined attack of the full-scale war on 23–24 May, deploying 600 drones and 90 missiles against Kyiv and surrounding regions. Among the weapons was an Oreshnik hypersonic ballistic missile — capable of carrying nuclear warheads and only the third use of this system during the conflict — which struck Bila Tserkva, roughly 80 km south of the capital. At least 4 people were killed and approximately 100 injured across the city. Ukrainian air defences intercepted most drones and more than half the missiles, but around 30 residential buildings in Kyiv were damaged or destroyed, marking the highest location count of any single night since the war began. President Zelensky called for international consequences and European NATO allies condemned the strike as a deliberate escalation aimed at breaking civilian resolve.",
    "{{WORLD_1_URL}}": "https://kyivindependent.com/russian-attack-may-24-2026/",

    "{{WORLD_2_FLAG}}": "🇨🇩🇺🇬 AFRICA · HEALTH EMERGENCY",
    "{{WORLD_2_HEADLINE}}": "WHO Declares Ebola Outbreak in Central Africa a Global Health Emergency — No Approved Vaccine for This Strain",
    "{{WORLD_2_SUMMARY}}": "The World Health Organisation declared the Ebola Bundibugyo virus outbreak in the Democratic Republic of Congo and Uganda a Public Health Emergency of International Concern on 17 May, with Africa CDC issuing a continental security alert on 18 May. As of 24 May, confirmed cases have spread across three provinces in eastern DRC — Ituri, Nord-Kivu, and Sud-Kivu — with five cases confirmed in Uganda's capital Kampala. Critically, there is no approved vaccine or treatment for the Bundibugyo strain, which is genetically distinct from the Zaire strain targeted by existing vaccines. Emergency committee recommendations issued on 22 May call for urgent travel and trade screening measures and expanded surveillance across the 10 countries considered at elevated risk. The WHO has deployed rapid response teams, but the outbreak is operating in territory affected by active armed conflict and humanitarian crisis.",
    "{{WORLD_2_URL}}": "https://www.who.int/news/item/22-05-2026-first-meeting-of-the-ihr-emergency-committee-regarding-the-epidemic-of-ebola-bundibugyo-virus-disease-in-the-democratic-republic-of-the-congo-and-uganda-2026-temporary-recommendations",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 AUSTRALIA · INTEREST RATES",
    "{{ECON_1_HEADLINE}}": "RBA Lifts Cash Rate to 4.35% in Third Straight Hike — Small Business Borrowing Costs Now at 12-Year High",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank of Australia's monetary policy board voted 8-1 in May to raise the official cash rate by 25 basis points to 4.35 per cent — the third consecutive meeting with a rate increase. Inflation reached 4.6 per cent annually in the March quarter and is forecast to peak at 4.8 per cent in June, well above the RBA's 2–3 per cent target band. The bank cited the prolonged Middle East conflict as a key upside risk to energy prices and inflation expectations. CBA economists' base case holds rates at 4.35 per cent through 2026, with potential cuts only emerging in 2027 if conditions improve. For trades operators with equipment finance, overdraft facilities, or business credit lines, borrowing costs are the highest since 2012 — layered on top of existing fuel, wage, and materials pressures building through the year.",
    "{{ECON_1_URL}}": "https://www.commbank.com.au/articles/newsroom/2026/05/rba-may-interest-rates-decision.html",

    "{{ECON_2_FLAG}}": "💰 AUSTRALIA · FEDERAL BUDGET",
    "{{ECON_2_HEADLINE}}": "Budget 2026-27: $20K Instant Asset Write-Off Now Permanent — And Fuel Excise Relief Runs Until June 30",
    "{{ECON_2_SUMMARY}}": "The 2026-27 Federal Budget delivered on 12 May permanently legislated the $20,000 instant asset write-off for businesses with turnover up to $10 million — ending years of annual uncertainty for small trades operators making equipment and vehicle decisions. The same budget extended fuel excise relief worth $2.9 billion, halving the rate from 52.6 to 26.3 cents per litre until 30 June 2026. The headline deficit is projected at $31.5 billion in 2026-27, and the heavy vehicle road user charge has been reduced to zero. GDP growth is forecast to slow to 1.75 per cent in 2026-27. With 35 days remaining on the fuel relief window, now is the time to review any large plant, vehicle, or equipment purchases — both the write-off and lower fuel costs are working in your favour simultaneously.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💰 AI · INVESTMENT",
    "{{TECH_1_HEADLINE}}": "Anthropic Set to Close $30 Billion Round This Week — $900B+ Valuation Would Make It World's Most Valuable AI Startup",
    "{{TECH_1_SUMMARY}}": "Anthropic is expected to close a $30 billion-plus investment round at a valuation exceeding $900 billion as early as this week, vaulting ahead of OpenAI's $852 billion valuation to become the world's most valuable private AI company. The round is co-led by Sequoia Capital, Dragoneer, Altimeter Capital, and Greenoaks Capital Partners, with each firm contributing roughly $2 billion. The raise coincides with Anthropic projecting $10.9 billion in Q2 revenue — the first quarter in which it expects to record an operating profit. For context, $900 billion places Anthropic ahead of every company on the ASX and larger than the combined market cap of Australia's four major banks. The numbers illustrate how completely AI has moved from experimental research into commercial-scale business in under five years.",
    "{{TECH_1_URL}}": "https://www.bloomberg.com/news/articles/2026-05-22/anthropic-to-close-over-30-billion-round-as-soon-as-next-week",

    "{{TECH_2_FLAG}}": "🔍 GOOGLE · AI SEARCH",
    "{{TECH_2_HEADLINE}}": "Google Confirms Gemini Will Power Next-Generation Siri — Apple-Google AI Deal Redraws the Smartphone Landscape",
    "{{TECH_2_SUMMARY}}": "Google Cloud CEO Thomas Kurian confirmed this week at Google Cloud Next '26 in Las Vegas that Google's Gemini AI will power a new, more personalised version of Siri launching in Apple's iOS 27 and macOS 27 later in 2026. The partnership — internally referred to as Apple Intelligence Extensions — allows users to select third-party AI providers including Anthropic and Google to handle text generation, editing, and image tasks across Apple devices. This marks the most significant reordering of the AI assistant landscape since ChatGPT's launch: the two biggest tech ecosystems in the world are now pooling AI infrastructure rather than competing head-to-head at the model level. For small businesses, it means AI-powered answers to customer questions will become a default feature of every phone, not an optional app.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 USA · ROBOTICS SUMMIT",
    "{{ROBOT_1_HEADLINE}}": "2026 Robotics Summit Opens in Boston This Week — Amazon's Touch-Sensing Vulcan Robot Named Robot of the Year",
    "{{ROBOT_1_SUMMARY}}": "The 2026 Robotics Summit and Expo opens tomorrow (Wednesday) at the Boston Convention Center, bringing together more than 6,000 engineers, developers, and executives from aerospace, healthcare, logistics, and manufacturing. The headline accolade goes to Amazon's Vulcan — the first industrial robot to incorporate a genuine sense of touch, named Robot of the Year by Robotics Business Review. Vulcan is already operational at Amazon's Spokane warehouse, handling around 75 per cent of all items at human-comparable speed and running 20 hours per day, with expansion to additional US and German facilities planned for 2026. The summit's logistics track will spotlight the wider shift in warehouse automation: AI-guided picking systems are now showing measurable payback periods of 6–12 months in high-utilisation deployments, compressing the economics of automation for mid-size operators.",
    "{{ROBOT_1_URL}}": "https://www.roboticssummit.com/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Second Fatal Shark Attack in a Fortnight — Man Killed at Kennedy Shoal off Northeast Queensland",
    "{{AUS_1_SUMMARY}}": "A man died following a shark attack at Kennedy Shoal off northeast Queensland on Sunday 24 May, the second fatal shark incident in Australia in less than two weeks after a 38-year-old died near Perth on 16 May. A commercial fishing operator at the scene told media that sharks had become noticeably more common and aggressive along the coastline, attributing the change to restrictions on catching large sharks introduced in recent years. Queensland's shark monitoring program deploys drumlines and nets at selected beaches, but remote offshore shoal areas remain unprotected. The two fatalities in quick succession have renewed calls for a review of large shark management policy in Queensland and Western Australia.",
    "{{AUS_1_URL}}": "https://www.aljazeera.com/news/2026/5/24/man-dies-in-northeast-australia-after-shark-attack",

    "{{AUS_2_HEADLINE}}": "Socceroos Begin World Cup Final Preparations in Florida — Squad Named 1 June, Tournament Opens 11 June",
    "{{AUS_2_SUMMARY}}": "Australia's national football squad has assembled in Sarasota, Florida for its final preparation camp ahead of the FIFA World Cup 2026. Coach Tony Popovic is working with an extended squad before naming the official 26-player group on 1 June. Australia draws Group D alongside Türkiye, the United States, and Paraguay — opening play against Türkiye in Vancouver on 14 June (AEST), facing co-hosts the USA in Seattle on 19 June, and closing the group stage against Paraguay in Santa Clara on 25 June. A pre-tournament friendly against Mexico in Los Angeles is scheduled for 30 May. The tournament itself kicks off on 11 June with the opening match in Mexico City.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Tunnel Boring Machines Assembled at Burwood as Melbourne's Suburban Rail Loop East Prepares to Dig",
    "{{VIC_1_SUMMARY}}": "Victoria's Big Build confirmed in its May 2026 construction update that tunnel boring machines have arrived and are being assembled at the Burwood launch site for Suburban Rail Loop East, with tunnelling toward Glen Waverley expected to begin later this year. The SRL East project — connecting Cheltenham to Box Hill with 13 fully automated train stations — received an additional $3.8 billion in federal funding in the May budget, bringing total Commonwealth contribution to $6 billion. When complete in 2035, the line will provide Carrum Downs and Frankston corridor residents with orbital connections to Deakin University, Monash Clayton, and Box Hill without requiring a CBD interchange.",

    # Science
    "{{SCI_1_FLAG}}": "🐙 MARINE BIOLOGY · GALÁPAGOS",
    "{{SCI_1_HEADLINE}}": "Golf Ball-Sized Blue Octopus Spotted Near Galápagos in 2015 Confirmed as Entirely New Species — Microeledone galapagensis",
    "{{SCI_1_SUMMARY}}": "Scientists have formally described a tiny blue octopus first filmed during a 2015 deep-sea expedition near the Galápagos Islands as an entirely new species, naming it Microeledone galapagensis — published in the journal Zootaxa and covered by ScienceDaily on 25 May 2026. About the size of a golf ball, the creature was observed by a remotely operated vehicle at roughly 1,773 metres (5,800 feet) below the surface near Darwin Island, during a mission run in partnership with the Charles Darwin Foundation and the Galápagos National Park Directorate. The formal description marks the first time lead researcher Janet Voight — who has spent more than 40 years studying octopus evolution — has officially led the naming of a new species. The discovery is a reminder of how little science has catalogued in the deep ocean: less than 25 per cent of the global seafloor has been mapped in high resolution.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "AI Can Score Your Quotes Before You Send Them — And the Results May Surprise You",
    "{{INSIGHT_BODY}}": "Most quotes leave the business with a guess baked in — not a deliberate margin, not a competitive calculation, just the estimator's experience and a feeling about the job. For small trades operators, that guess compounds across dozens of quotes a month. AI changes that equation without adding overhead. Before your next quote goes out, paste the full scope, your materials cost, your labour hours, and the client context into Claude or ChatGPT. Then ask it directly: does the margin in this quote make sense for the risk and scope? Is there anything in the scope I haven't priced? How does this compare to what a competitor might charge for this type of job in this suburb? You will get a structured second opinion in 60 seconds — not a replacement for your judgement, but a lens that catches gaps your experience has learned to assume away. The most common finding: quotes that underestimate complexity on the labour side, not the materials side. The second most common: scope that doesn't account for access conditions or site staging. Catching one of those per week on a mid-sized job reshapes the profitability of your whole month. The habit takes five minutes per quote. It compounds.",

    # Fun Facts
    "{{FACT_1}}": "In certain conditions, hot water can freeze faster than cold water — a counterintuitive phenomenon known as the Mpemba effect, named after Tanzanian student Erasto Mpemba, who noticed it while making ice cream in 1963 and was dismissed by his teacher. The effect was confirmed experimentally after Mpemba later co-authored a paper with a University of Dar es Salaam physicist. The underlying mechanism is still debated, with proposed explanations including differences in convection patterns, dissolved gas content, and the structure of hydrogen bond networks in hot versus cold water samples.",

    "{{FACT_2}}": "Reinforced concrete — the material underpinning almost every modern building, bridge, and industrial structure — was not invented by an engineer or architect. It was patented in 1867 by a French gardener named Joseph Monier, who was trying to make stronger flower pots by embedding iron mesh in cement. He extended the idea to tanks, pipes, and eventually bridges. His patents were acquired by German engineers in the 1880s, who developed the structural theory behind the material and built the first large reinforced concrete structures in Europe.",

    "{{FACT_3}}": "The Moon is moving away from Earth at approximately 3.8 centimetres per year — a rate confirmed by laser ranging measurements using retroreflectors placed on the lunar surface during the Apollo missions. About 1.5 billion years ago the Moon was close enough that a day on Earth lasted only 18 hours. In roughly 600 million years, the Moon will have receded far enough that its apparent size in the sky will be too small to completely cover the Sun, making total solar eclipses impossible. The drift is caused by tidal interactions that continuously transfer rotational energy from Earth to the Moon's orbit.",

    # Joke
    "{{JOKE_SETUP}}": "Why do fire sprinkler installers make terrible poker players?",
    "{{JOKE_PUNCHLINE}}": "Because the moment things heat up, they blow their hand.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Motivation is what gets you started. Habit is what keeps you going.”",
    "{{CLOSING_ATTR}}": "— Jim Ryun",
    "{{CLOSING_MESSAGE}}": "Tuesday 26 May — showers again today with a thunderstorm risk tonight, so plan outdoor work accordingly. The Russia-Ukraine conflict escalated sharply at the weekend with the largest single-night barrage of the full-scale war, including an Oreshnik hypersonic missile strike — a reminder that geopolitical tension continues to feed the energy prices that affect your operating costs here. On the economic front, the RBA's third straight rate rise to 4.35 per cent and the Budget's permanent $20K write-off are the two pressure points and opportunities to have clear in mind right now — especially with fuel excise relief closing in 35 days. Down the road, the Robotics Summit opens in Boston tomorrow with 6,000+ industry people and a wave of announcements expected through the week. And if you haven't already, today's insight on AI-scoring your quotes before they go out is worth five minutes. Have a sharp one, Liall.",
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
