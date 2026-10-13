#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 14 October 2026',
'{{WEATHER_1}}': 'WED 14 OCT · ☁️ Cloudy, 10% chance of rain · 9–16°C',
'{{WEATHER_2}}': 'THU 15 OCT · ⛅ Partly cloudy, 5% chance of rain · 6–21°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'FRI 16 OCT · outlook not confirmed',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'SAT 17 OCT · outlook not confirmed',
'{{WEATHER_5}}': 'SUN 18 OCT · outlook not confirmed',
'{{WEATHER_ALERT}}': 'Cloudy but dry today, then Thursday looks like the pick of the week at around 21°C with only a 5% chance of rain. Figures come from a Bureau of Meteorology Melbourne page that may be a day or two old, so Carrum Downs could differ, and Friday to Sunday could not be confirmed. Check the BoM app before committing to outdoor jobs.',
'{{WORLD_1_FLAG}}': '🌊 BLACK SEA · SHIPS HIT',
'{{WORLD_1_HEADLINE}}': 'Bulgaria Says Drones Struck Two Ships Off Its Coast, With Eleven Sailors Still Missing',
'{{WORLD_1_SUMMARY}}': 'Bulgaria\'s prime minister said the drones hit two vessels off the Bulgarian coast, and eleven sailors remain unaccounted for. Reported in the 13 October Just Security roundup, which credits wire services. Attacks on shipping like this tend to push up freight and fuel costs.',
'{{WORLD_1_URL}}': 'https://www.justsecurity.org/160525/early-edition-october-13-2026/',
'{{WORLD_2_FLAG}}': '⛪ VATICAN · POPE LEO XIV',
'{{WORLD_2_HEADLINE}}': 'Vatican Says Pope Leo XIV\'s Lung Nodule Surgery Was Completed Successfully',
'{{WORLD_2_SUMMARY}}': 'The Vatican reported on 13 October that the operation went well. I only saw the headline in a live blog, so details on his recovery are not confirmed.',
'{{WORLD_2_URL}}': 'https://www.timesofisrael.com/liveblog-october-13-2026/',
'{{ECON_1_FLAG}}': '🛢️ OIL · RUSSIAN DIESEL',
'{{ECON_1_HEADLINE}}': 'Oil Prices Fall After the US Eases Restrictions on Russian Diesel Supplies',
'{{ECON_1_SUMMARY}}': 'Oil slipped on Tuesday after Washington relaxed limits on Russian diesel, though supply is still tight with Gulf disruptions and Riyadh\'s airport reportedly still closed. Falling global diesel can eventually help local pump prices, but it is not guaranteed.',
'{{ECON_1_URL}}': 'https://thestreet.com/stock-market-today/stock-market-today-dow-jones-sp-500-nasdaq-updates-oct-13-2026',
'{{ECON_2_FLAG}}': '⛽ DIESEL · NAB WARNING',
'{{ECON_2_HEADLINE}}': 'Australian Diesel Averages 224 Cents a Litre as NAB Models a Severe $4 Scenario',
'{{ECON_2_SUMMARY}}': 'The Australian Institute of Petroleum put the national average diesel price at 224 cents a litre in the week ending 1 October. NAB says wholesale diesel topping $4 is a severe scenario, not its base case. This is older than 48 hours, so check your fuel card pricing before quoting.',
'{{TECH_1_FLAG}}': '🧠 AI · GOOGLE GEMINI',
'{{TECH_1_HEADLINE}}': 'Google Reportedly Makes Gemini 4 Argon Broadly Available With Low Launch API Pricing',
'{{TECH_1_SUMMARY}}': 'Reports dated 13 October say the model is open to more users at a promotional $2 input and $10 output per million tokens, rising later to about $4 and $20. Some sources say access is still limited, so confirm with Google before building anything on it.',
'{{TECH_1_URL}}': 'https://venturebeat.com/technology/google-makes-gemini-4-argon-broadly-available-with-limited-time-low-api-pricing-of-2-10-per-1m-token',
'{{TECH_2_FLAG}}': '🤖 AI · META',
'{{TECH_2_HEADLINE}}': 'Meta Lists Muse Wonder 1.0 as Its Newest Model, Released 12 October',
'{{TECH_2_SUMMARY}}': 'A model-release tracker lists Muse Wonder 1.0 as the latest launch. I could not find details on what it does or costs, so treat this as an unconfirmed headline for now.',
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS · PHYSICAL AI',
'{{ROBOT_1_HEADLINE}}': 'Humanoid Robots Will Report to Work Soon as Physical AI\'s "ChatGPT Moment" Arrives, Says Ex-Boston Dynamics CEO',
'{{ROBOT_1_SUMMARY}}': 'KED Global published the headline on 12 October from a Korean HR forum. I only saw the headline, and others in the industry, including Unitree\'s founder, say the breakthrough has not arrived yet, so treat the timing as opinion.',
'{{ROBOT_1_URL}}': 'https://kedglobal.com/global-hr-forum-2026/newsView/ked202610120019',
'{{AUS_1_HEADLINE}}': 'Lukewarm Liberal Response to Josh Frydenberg\'s Potential Return to Politics',
'{{AUS_1_SUMMARY}}': 'ABC reported on 13 October that the party room response was cool after Frydenberg said on 60 Minutes that he has not closed the door, while attacking Angus Taylor\'s leadership. He says the next election is 18 months away.',
'{{AUS_1_URL}}': 'https://abc.net.au/news/2026-10-13/liberal-party-josh-frydenberg-politics-kooyong-return/107260102',
'{{AUS_2_HEADLINE}}': 'RBA Sits at 4.60% After Its Fourth Hike This Year, With August Inflation at 4.0%',
'{{AUS_2_SUMMARY}}': 'Background rather than breaking news: the 29 September hike and August CPI keep pressure on small business borrowing and costs, with trimmed mean at 3.6%. This is older than 48 hours.',
'{{VIC_1_HEADLINE}}': 'Wilson Rules Out a GST Increase as Carroll Calls the Idea a "Ridiculous Proposition"',
'{{VIC_1_SUMMARY}}': 'ABC reports the GST debate on 13 October, about six weeks out from the 28 November state election, with cost of living central to the campaign. I only saw the summary, so check the full story.',
'{{SCI_1_FLAG}}': '🦖 PALAEONTOLOGY · FOSSILS',
'{{SCI_1_HEADLINE}}': '97-Million-Year-Old Fossils Reveal the Earliest Known Animal "GPS"',
'{{SCI_1_SUMMARY}}': 'This is a headline I saw listed on a science news site, and I could not confirm the publication date or the details of the study, so check the source before sharing it.',
'{{INSIGHT_TITLE}}': 'Photograph Every Job Before and After: Your Best Training Data for Any AI Tool',
'{{INSIGHT_BODY}}': 'Most AI tools get useful only when they have your own examples to learn from. Start a simple habit now: take a dated before and after photo of every job, name it with the client, the surface and the spec, and keep it in one folder. In six months you will have a library that can illustrate quotes, settle disputes about condition, train new staff and feed any tool that estimates from photos. It costs nothing, takes two minutes a job, and makes you ready when the tools improve.',
'{{FACT_1}}': 'Around 80 to 90 percent of the world\'s goods by volume travel by sea, which is why a couple of drone-hit ships can ripple through fuel and freight prices.',
'{{FACT_2}}': 'Rudolf Diesel\'s engine ran on peanut oil when it was shown at the 1900 Paris World\'s Fair, years before it became tied to petroleum.',
'{{FACT_3}}': 'Bananas are naturally slightly radioactive because they contain potassium-40, though you would need to eat millions at once for it to matter.',
'{{JOKE_SETUP}}': 'Why did the roofer\'s bookkeeper never worry about a tax audit?',
'{{JOKE_PUNCHLINE}}': '"Because everything on the books was already covered."',
'{{CLOSING_QUOTE}}': '"Do one thing every day that scares you."',
'{{CLOSING_ATTR}}': '— Eleanor Roosevelt',
'{{CLOSING_MESSAGE}}': "It's Wednesday 14 October, cloudy but dry in Carrum Downs, so it's a decent day to get outdoor work moving. Thursday looks sunnier and warmer at around 21°C, so line up your best outdoor job for then. With diesel still in the news, check your fuel pricing before you quote anything big this week.",
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
