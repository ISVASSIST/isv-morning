#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 10 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 10 Jul (BOM)
    "{{WEATHER_1}}": "FRI 10 · 🌦️ Frosty start, showers easing · 7–13°C",
    "{{WEATHER_2}}": "SAT 11 · 🌫️ Patchy fog, mostly dry · 5–14°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SUN 12 · ❄️ Frost & fog, sunny arvo · 3–15°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 13 · 🌧️ Showers, windy · 9–14°C",
    "{{WEATHER_5}}": "TUE 14 · 🌧️ Showers, windy N'ly · 8–15°C",
    "{{WEATHER_ALERT}}": "⚠ FROST WARNING FOR VICTORIA THIS MORNING · SHOWERS & GUSTY N'LY WINDS RETURN MONDAY",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 US · IRAN · FRESH OVERNIGHT STRIKES, CEASEFIRE IN TATTERS",
    "{{WORLD_1_HEADLINE}}": "US and Iran Trade Fresh Strikes for a Second Night After Trump Declares Ceasefire \"Over\"",
    "{{WORLD_1_SUMMARY}}": "US forces hit around 90 targets across Iran overnight, including sites near the Strait of Hormuz, while Iran retaliated with drone and missile strikes on US bases in Kuwait, Bahrain and Qatar. Trump, capping the NATO summit in Ankara, called further negotiation with Tehran \"a waste of time\" — keeping the three-week-old ceasefire effectively dead and oil markets on edge.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/07/08/nx-s1-5883929/trump-nato-iran-strikes-press-conference",

    "{{WORLD_2_FLAG}}": "🇬🇧 UK · POLITICS · LABOUR LEADERSHIP RACE OPENS",
    "{{WORLD_2_HEADLINE}}": "Nominations Open in UK Labour Leadership Race, With Andy Burnham the Likely Only Candidate",
    "{{WORLD_2_SUMMARY}}": "Nominations opened Thursday in the contest to replace Keir Starmer as UK prime minister, with former Health Secretary Wes Streeting dropping his own bid to back Andy Burnham. If no rival candidate reaches the 81-MP threshold by 16 July, Burnham will be crowned Labour leader — and PM in waiting — unopposed at a special conference on 17 July.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/7/9/uk-labour-leadership-nominations-begin-whos-running-and-how-it-works",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · EXCISE RELIEF HALVED AS OIL SWINGS ON IRAN",
    "{{ECON_1_HEADLINE}}": "Bowser Prices Under Pressure From Both Sides as Excise Relief Halves and Oil Whipsaws on Iran",
    "{{ECON_1_SUMMARY}}": "Australia's fuel excise discount dropped from 32c to 16c a litre on 1 July, pushing capital-city petrol to around 158cpl and diesel to 179cpl even before this week's Iran-driven oil volatility, which has seen Brent swing between roughly $76 and $79 a barrel in a single session. Worth building a bit of buffer into quotes with a ute, van or diesel compressor on the books over winter.",
    "{{ECON_1_URL}}": "https://www.mynrma.com.au/open-road/news/2026/fuel-excise-update",

    "{{ECON_2_FLAG}}": "📉 ASX · MARKETS · FOURTH STRAIGHT RED SESSION",
    "{{ECON_2_HEADLINE}}": "ASX 200 Falls for a Fourth Day Running as Iran Tensions and a Downgraded Growth Outlook Bite",
    "{{ECON_2_SUMMARY}}": "The ASX200 slipped 0.26% to close at 8,762.5 points on Thursday, its fourth consecutive red session, after the IMF trimmed its 2026 Australian growth forecast citing energy prices and geopolitics. Gold eased for a third day to around US$4,080 an ounce, while a handful of small-cap debuts, including a 13% first-day pop for FDC Consolidated, offered a rare bright spot.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 OPENAI · GPT-5.6 · SOL, TERRA & LUNA GO FULLY PUBLIC",
    "{{TECH_1_HEADLINE}}": "OpenAI's GPT-5.6 Lineup Clears Government Security Review, Launches to Everyone",
    "{{TECH_1_SUMMARY}}": "GPT-5.6 Sol, Terra and Luna rolled out broadly across ChatGPT, the API and Codex on Thursday, ending a 12-day window where access to the flagship Sol model was limited to roughly 20 government-vetted partners under a new White House cybersecurity review. Terra and Luna are priced well below the outgoing GPT-5.5 lineup, which is worth a look if you're using ChatGPT for quoting, admin or customer replies and want the same quality for less.",
    "{{TECH_1_URL}}": "https://www.techtimes.com/articles/319979/20260709/gpt-56-goes-public-after-12-day-white-house-gate-tests-voluntary-ai-framework.htm",

    "{{TECH_2_FLAG}}": "📊 AI ADOPTION · SMALL BUSINESS · UPTAKE NEARLY DOUBLES",
    "{{TECH_2_HEADLINE}}": "NAB Data Shows Regular AI Use Among Australian Small Businesses Nearly Doubled in 18 Months",
    "{{TECH_2_SUMMARY}}": "Regular AI use among Australian SMEs climbed from 40% in mid-2024 to 69% in January 2026, with daily use more than tripling to 28%, and 79% of users reporting a real productivity gain. The biggest thing still holding businesses back isn't cost — it's not knowing where to start and worrying about getting it wrong.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 MEDICAL ROBOTICS · WORLD FIRST · HUMANOID ROBOTS PERFORM LIVE SURGERY",
    "{{ROBOT_1_HEADLINE}}": "Teleoperated Humanoid Robots Complete Two Live Surgeries in UC San Diego World-First Trial",
    "{{ROBOT_1_SUMMARY}}": "Researchers at UC San Diego used two Unitree G1 humanoid robots, controlled entirely by human operators via motion capture and foot pedals, to perform a gallbladder removal and a second procedure with no direct human hands in the operating field — coordinating both arms to hold tissue with one hand while cutting with the other. It's an early but striking sign that humanoid hardware is starting to move from warehouses and factory floors into far more delicate, high-stakes work.",
    "{{ROBOT_1_URL}}": "https://today.ucsd.edu/story/surgeons-use-teleoperated-humanoid-robots-to-perform-live-surgery-a-world-first",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Strikes Landmark Uranium Export Deal With India During Modi's Melbourne Visit",
    "{{AUS_1_SUMMARY}}": "Australia has agreed to sell uranium to India for peaceful power generation, signed during a Melbourne visit by Prime Minister Narendra Modi that also produced new agreements on critical minerals, defence, technology and a planned space-tracking terminal on the Cocos Islands. It's Australia's latest move to diversify trade away from its heavy reliance on China.",
    "{{AUS_1_URL}}": "https://www.aljazeera.com/news/2026/7/9/australia-india-strike-deal-on-uranium-exports-during-pm-modis-visit",

    "{{AUS_2_HEADLINE}}": "RBA Holds Cash Rate Steady as It Weighs the Oil Shock Against Slowing Growth",
    "{{AUS_2_SUMMARY}}": "The Reserve Bank left the cash rate unchanged this week, judging it appropriate to sit tight while it assesses the impact of three earlier rate rises alongside the Iran-driven oil supply disruption, with consumer spending growth already slowing and housing prices falling in some capital cities. The board meets again on 11 August.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "NAIDOC Week Wraps Up With Free Federation Square Concert Today",
    "{{VIC_1_SUMMARY}}": "Christine Anu headlines a free NAIDOC in the City concert at Federation Square from midday today, alongside a Koorie Heritage Trust market and workshops — a good excuse for a lunchtime detour into the city if you're doing a job nearby.",

    # Science
    "{{SCI_1_FLAG}}": "🌳 ECOLOGY · CARBON CYCLE · CLIMATE MODELS MAY BE OVERSTATING FOREST CARBON STORAGE",
    "{{SCI_1_HEADLINE}}": "Oak Trees Keep Absorbing Carbon for Months After They Stop Growing, Study Finds",
    "{{SCI_1_SUMMARY}}": "Researchers tracking oak trees at 137 US sites found that up to 36% of a tree's annual carbon uptake happens after its growth for the season has already stopped, breaking the long-standing assumption that more photosynthesis simply means more wood. Published in Science Advances, the finding suggests climate models may be overestimating how much carbon forests can actually lock away as wood in a warming world.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "4 in 10 Aussie Small Businesses Are Already Using AI Daily — Are You?",
    "{{INSIGHT_BODY}}": "New NAB data shows regular AI use among Australian small businesses has climbed from 40% to 69% in eighteen months, with daily use more than tripling — and 79% of those using it say it's genuinely lifted productivity, not just added another app to juggle. The businesses still sitting on the sidelines usually aren't held back by cost; they're held back by not knowing where to start. The fix isn't a big rollout — it's picking one repetitive task this week, a quote template, a job note, a follow-up email, and letting AI take the first draft while you keep the final say.",

    # Fun Facts
    "{{FACT_1}}": "The world's first hydraulic press was patented by British engineer Joseph Bramah in 1795, built on Blaise Pascal's principle that pressure in a sealed fluid transmits equally in all directions — the same basic idea behind every hydraulic jack, lift and ram used on a job site today.",

    "{{FACT_2}}": "The Eiffel Tower was held together by roughly 2.5 million rivets, each one driven by a four-man team: one to heat it red-hot, one to hold it, one to shape the head, and one to hammer it home — with crews placing up to 22,000 rivets a week at the peak of construction in 1889.",

    "{{FACT_3}}": "Australia became the first country in the world to switch entirely to polymer banknotes, a project run by the CSIRO, the Reserve Bank and the University of Melbourne that began in 1968 and produced its first note — a $10 bicentennial commemorative — in January 1988.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pool builder's small business never run dry?",
    "{{JOKE_PUNCHLINE}}": "He always kept a healthy reserve — and made sure it was a deep one.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"Well done is better than well said.\"",
    "{{CLOSING_ATTR}}": "— Benjamin Franklin",
    "{{CLOSING_MESSAGE}}": "It's a frosty start under this morning's Victorian frost warning, but Carrum Downs clears through the day to a mild top of 13°C, with a calmer, mostly dry weekend ahead before showers return Monday — a solid window to get outdoor jobs ticked off. Keep half an eye on the bowser too, with the fuel excise relief just halved and oil still swinging on the Iran standoff, a few more cents a litre wouldn't be a shock this week.",
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
