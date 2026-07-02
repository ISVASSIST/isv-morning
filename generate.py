#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 03 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 3 Jul
    "{{WEATHER_1}}": "FRI 3 · 🌧 Showers, windy · 9–14°C",
    "{{WEATHER_2}}": "SAT 4 · 🌧 Showers, cooler · 8–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 5 · ⛅ Early shower, clearing · 9–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 6 · ☀️ Sunny, frosty start · 3–15°C",
    "{{WEATHER_5}}": "TUE 7 · ☀️ Mostly sunny · 5–16°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS TODAY & TOMORROW · MIN WAGE RISES TO $26.44/HR THIS WEEK",

    # World
    "{{WORLD_1_FLAG}}": "🇻🇦 VATICAN CITY · SCHISM · BISHOPS EXCOMMUNICATED",
    "{{WORLD_1_HEADLINE}}": "Vatican Declares Traditionalist Society of St. Pius X in Schism, Excommunicates Its Bishops",
    "{{WORLD_1_SUMMARY}}": "The Vatican formally excommunicated the four bishops the breakaway Society of St. Pius X consecrated without papal consent on July 1 in Écône, Switzerland, plus two more who took part in the ceremony, declaring the ultra-traditionalist society itself in schism. Priests belonging to the group are now deemed excommunicated too, with the Vatican warning that sacraments they perform — including confession and marriage — are invalid, and that the faithful attending SSPX Masses risk excommunication themselves. It's the most decisive Vatican action against the group since Pope Benedict XVI lifted an earlier excommunication in 2009, closing off nearly two decades of cautious rapprochement.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/07/02/nx-s1-5878916/vatican-society-of-st-pius-x-in-schism",

    "{{WORLD_2_FLAG}}": "🇺🇸 UNITED STATES · TRADE · USMCA NOT RENEWED",
    "{{WORLD_2_HEADLINE}}": "Trump Refuses to Renew USMCA, Toppling a Pillar of North American Trade Stability",
    "{{WORLD_2_SUMMARY}}": "Six years to the day after the US-Mexico-Canada trade deal took effect, the Trump administration confirmed this week it won't renew it in its current form, instead opening a decade of amendment negotiations that could see Washington strike separate bilateral deals with Mexico and Canada. The pact stays technically in force but now faces annual reviews that could reopen major provisions at any time, injecting fresh uncertainty into roughly $2 trillion of North American trade — the kind of upstream disruption that tends to work its way into global shipping costs and, eventually, the price of imported gear and materials everywhere, including here.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/business/economy/trump-usmca-renewal-tariffs-trade-rcna352594",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL PRICES · DIESEL NATIONAL AVERAGE · $1.97/L",
    "{{ECON_1_HEADLINE}}": "National Diesel Average Hits 197.1 Cents a Litre as the Halved Fuel Excise Discount Bites",
    "{{ECON_1_SUMMARY}}": "The latest pricing data puts Australia's national average diesel price at 197.1 cents a litre this week, with Victoria still the cheapest state to fill up at an average 185.6 cents a litre. It's the first full week of pricing since the fuel excise discount halved from 32 cents to 16 cents a litre on July 1, and retailers are progressively passing the difference through — worth checking against whatever number you last budgeted a tank of diesel at.",
    "{{ECON_1_URL}}": "https://gdp.com.au/petrol-prices",

    "{{ECON_2_FLAG}}": "💰 FAIR WORK COMMISSION · MINIMUM WAGE · UP 6% THIS WEEK",
    "{{ECON_2_HEADLINE}}": "National Minimum Wage Rises 6% to $26.44 an Hour From This Week's First Full Pay Cycle",
    "{{ECON_2_SUMMARY}}": "The Fair Work Commission's 6% increase to the National Minimum Wage takes effect from the first full pay period after July 1, lifting the weekly minimum to $1,004.90 (award wages rise 4.75%), flowing through to around 2.7 million workers. For any small trades business with award-reliant staff, it's worth double-checking payroll has applied the new rates before the next pay run rather than after — the increase applies automatically regardless of when you get around to updating the numbers.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 GOOGLE · SEARCH · GEMINI 3.5 FLASH NOW DEFAULT",
    "{{TECH_1_HEADLINE}}": "Google Makes Gemini 3.5 Flash the Default Model Behind AI Mode in Search, Starting This Week",
    "{{TECH_1_SUMMARY}}": "From July 2, Google has swapped in Gemini 3.5 Flash as the default model behind AI Mode in Search globally, promising flagship-level reasoning on coding and complex queries at the speed of its lighter-weight Flash tier. For anyone using Google to research suppliers, compare prices or draft a quick job scope, it means the AI answers sitting above the normal search results just got noticeably sharper without anyone needing to opt into anything.",
    "{{TECH_1_URL}}": "https://blog.google/products-and-platforms/products/search/search-io-2026/",

    "{{TECH_2_FLAG}}": "🤖 OPENAI · GOVERNANCE · 5% GOVERNMENT STAKE PROPOSED",
    "{{TECH_2_HEADLINE}}": "OpenAI Reportedly Proposes Giving the US Government a 5% Stake in the Company",
    "{{TECH_2_SUMMARY}}": "OpenAI executives, including CEO Sam Altman, have opened preliminary talks about handing Washington a 5% ownership stake, as part of a wider arrangement that would see the government hold a slice of each major US AI developer, the Financial Times reports. It's a sign of how tightly AI policy and national politics are becoming intertwined at the top of the industry — worth watching less for the direct impact on a small trades business and more for what it signals about how the tools you rely on daily might eventually be regulated.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · IFR · NEW GLOBAL PRESIDENT ELECTED",
    "{{ROBOT_1_HEADLINE}}": "Jane Heffner of Teradyne Robotics Elected New President of the International Federation of Robotics",
    "{{ROBOT_1_SUMMARY}}": "The IFR — the peak global body tracking and setting direction for the industrial robotics industry — has elected Jane Heffner, Teradyne Robotics' Global Vice President of Channel Communication, as its new president, taking over the rotating role from Takayuki Ito of Fanuc. It's a leadership call rather than a factory deployment, but it lands the same week IFR data confirms global industrial robot installations hit an all-time high of US$16.7 billion — a reminder that the automation wave reshaping factories overseas is being steered by decisions being made right now.",
    "{{ROBOT_1_URL}}": "https://ifr.org/ifr-press-releases/news/jane-heffner-is-new-president-of-ifr",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australian Home Prices Post Biggest Monthly Fall in Three and a Half Years as New Financial Year Opens Weak",
    "{{AUS_1_SUMMARY}}": "National home values fell 0.4% in June — the steepest monthly drop since December 2022 — with Sydney down 1.2% and Melbourne not far behind, as the ASX 200 also opened the new financial year down 0.6%. Analysts point to three RBA rate rises since February, energy price pressure from the Middle East conflict, and tightened tax concessions for property investors as the drivers — a reminder that a cooler housing market flows through to how confident clients feel about spending on the next job.",
    "{{AUS_1_URL}}": "https://thenightly.com.au/australia/property-australian-home-prices-suffer-biggest-monthly-fall-since-december-2022-c-22511628",

    "{{AUS_2_HEADLINE}}": "Labor MP Tells Antisemitism Royal Commission His Office Was Vandalised, He's Had 10,000+ Abusive Messages",
    "{{AUS_2_SUMMARY}}": "Melbourne federal MP Josh Burns testified this week at the Royal Commission on Antisemitism and Social Cohesion's Sydney hearing block, describing social media platforms as 'arenas of hate' and detailing the toll of sustained online abuse and a vandalised electorate office. The commission's hearings run through to July 10, examining how online platforms amplify hateful content — a live conversation for any business owner who's had to decide how to handle a nasty comment thread.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Docklands' Firelight Festival Lights Up Melbourne's Waterfront This Weekend, July 3–5",
    "{{VIC_1_SUMMARY}}": "Fire performers, fire pits, live music and winter market stalls take over Docklands from tonight through Sunday as part of the Firelight Festival, part of the city's push to keep the waterfront lively through the cooler months. If you're headed into the city this weekend and want to make the most of Melbourne's winter rather than hide from it, it's free to attend and runs into the evening each night.",

    # Science
    "{{SCI_1_FLAG}}": "🪐 ASTRONOMY · HOBBY-EBERLY & NEID TELESCOPES",
    "{{SCI_1_HEADLINE}}": "Astronomers Confirm a Potentially Habitable Super-Earth Just 25 Light-Years From Us",
    "{{SCI_1_SUMMARY}}": "US astronomers have confirmed and refined the properties of GJ 3378b, a rocky super-Earth about 2.3 times Earth's mass orbiting a faint red dwarf star every 21.45 days, sitting squarely in its star's habitable zone and receiving roughly 90% of the sunlight Earth gets. It's one of the closest potentially habitable worlds ever found, though it sits right on the 'cosmic shoreline' — the edge of the zone where a star's radiation can strip away a planet's atmosphere entirely — so whether it could actually host liquid water remains an open question the next generation of telescopes will need to settle.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Google Just Made AI the Default Way People Search — Is Your Business Still Findable?",
    "{{INSIGHT_BODY}}": "As of this week, Google is showing AI-generated answers above the normal blue links for everyone, by default, worldwide — which means a growing share of people looking for 'blasting and coatings near me' or 'industrial paint stripping Melbourne' never scroll down to a traditional listing at all. The AI answer is built from whatever text it can find and trust, so a website full of vague slogans and no specifics gets skipped over in favour of a competitor whose site plainly states what they do, where, and for whom. A genuinely useful move this week: ask an AI tool to read your own website and answer 'what does this business actually do, and would I trust it with my job?' as if it were a stranger — then fix whatever it couldn't answer clearly. Fifteen minutes now is cheaper than slowly going invisible to searches you can't see happening.",

    # Fun Facts
    "{{FACT_1}}": "The Sydney Opera House was budgeted at $7 million and scheduled to take four years — it ended up costing $102 million and taking fourteen years to finish, yet it's now one of the most photographed buildings on Earth and has long since paid for itself many times over in tourism.",

    "{{FACT_2}}": "Red dwarf stars — small, dim and cool compared to our Sun — make up roughly 75% of all stars in the Milky Way, which is why most of the nearby 'potentially habitable' exoplanets found so far, including one confirmed again just this week, orbit stars nothing like our own.",

    "{{FACT_3}}": "The PlayStation 2, launched in 2000, remains the best-selling video game console ever made at over 155 million units sold worldwide — more than the PS3, PS4, original Xbox and Xbox 360 combined.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the locksmith's apprentice get promoted after just three months on the job?",
    "{{JOKE_PUNCHLINE}}": "Turns out he was the only one on the team who'd never once locked the van, the office, or himself out.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Life isn't about waiting for the storm to pass, it's about learning to dance in the rain.”",
    "{{CLOSING_ATTR}}": "— Vivian Greene",
    "{{CLOSING_MESSAGE}}": "It's Friday, and the showers rolling through Carrum Downs today and tomorrow make a fair excuse to get the admin pile sorted before Monday's frosty, sunny start. This is the first full week of the new $26.44 minimum wage and a diesel bill that's crept up with the halved fuel excise — worth a quick look at both before you quote the next job. If you're in the city this weekend, Docklands' Firelight Festival kicks off tonight through Sunday, fire pits and all — as good a reason as any to get out once the tools are down.",
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
