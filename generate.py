#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 30 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 30 May (BOM forecast)
    "{{WEATHER_1}}": "SAT 30 · 🌧 Showers · 16°C",
    "{{WEATHER_2}}": "SUN 31 · 🌧 Showers · 15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 1 JUN · 🌧 Showers · 15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 2 JUN · ⛈ Heavy showers · 16°C",
    "{{WEATHER_5}}": "WED 3 JUN · 🌧 Cloudy/Showers · 14°C",
    "{{WEATHER_ALERT}}": "⚠ WET WEEK — SHOWERS DAILY SAT–WED",

    # World
    "{{WORLD_1_FLAG}}": "🕊️ USA / IRAN · DIPLOMACY",
    "{{WORLD_1_HEADLINE}}": "US and Iran Reach 60-Day Ceasefire Extension Deal — Trump Weighing Final Approval",
    "{{WORLD_1_SUMMARY}}": "US and Iranian negotiators agreed in principle on a 60-day memorandum of understanding to extend their ceasefire and begin formal nuclear talks — but Trump said he needs 'a couple of days to think about it' before giving final approval. The deal, reported by Bloomberg and Al Jazeera on May 29, would push the truce through late July. Trump's stated conditions include Iran permanently abandoning nuclear weapons development, surrendering enriched uranium stocks, and the Strait of Hormuz reopening to unrestricted commercial shipping. Iran's semi-official media says the text hasn't been fully finalised. If approved, the deal would significantly ease the global shipping disruption that has been driving above-average fuel costs — with Brent crude already dropping around 4% this week on deal optimism.",
    "{{WORLD_1_URL}}": "https://www.bloomberg.com/news/articles/2026-05-29/us-iran-reach-deal-on-extended-ceasefire-pending-trump-approval",

    "{{WORLD_2_FLAG}}": "🇺🇸 USA · GAS SAFETY",
    "{{WORLD_2_HEADLINE}}": "Natural Gas Explosion Destroys Dallas Apartment Building — 3 Dead Including Child, 5 Injured",
    "{{WORLD_2_SUMMARY}}": "A natural gas explosion destroyed The Clyde apartment complex in Oak Cliff, Dallas on May 28, killing at least three people — including a child — and hospitalising five others. Atmos Energy confirmed that an external construction crew had struck a buried gas main before the blast; no active construction permits were on file for the site. The 20-unit building was fully engulfed within minutes, debris scattered across neighbouring properties. The NTSB has dispatched investigators. Third-party construction crews striking underground utilities — gas, water, electrical — is the leading preventable cause of infrastructure incidents in Australian and US cities alike, and a hazard every trades operator working near buried services must actively manage.",
    "{{WORLD_2_URL}}": "https://www.nbcnews.com/news/us-news/dallas-gas-explosion-apartment-rcna347419",

    # Economics
    "{{ECON_1_FLAG}}": "💰 AUSTRALIA · INTEREST RATES",
    "{{ECON_1_HEADLINE}}": "Banks Split on RBA's June 16 Decision — Westpac Tips Two More Hikes to 4.85%, CBA Calls Pause",
    "{{ECON_1_SUMMARY}}": "Following May's third consecutive RBA rate rise — cash rate now at 4.35% — Australia's major banks have diverged sharply on what happens next. Westpac economists forecast two further 25bp hikes in June and August, taking the cash rate to 4.85%, while ANZ, CBA and NAB are all predicting a pause. The next decision falls on Tuesday June 16. The RBA's May statement left the door explicitly open to further moves, citing inflation concerns from elevated fuel and commodity prices. For trades operators with variable-rate equipment loans, overdrafts or vehicle finance, the gap between the forecast scenarios is real money — a further 50bp rise pushes most variable business lending rates above 8.5%. Anyone drawing on a credit line or refinancing in the next 60 days should model the upside rate scenario, not just the central case.",
    "{{ECON_1_URL}}": "https://www.commbank.com.au/articles/newsroom/2026/05/rba-may-interest-rates-decision.html",

    "{{ECON_2_FLAG}}": "⛽ GLOBAL · FUEL",
    "{{ECON_2_HEADLINE}}": "Brent Crude Drops 4% on US-Iran Deal Optimism — But Australia's June 30 Excise Reversal Is Still Locked In",
    "{{ECON_2_SUMMARY}}": "Oil markets softened around 4% this week as traders priced in a higher probability of the Strait of Hormuz reopening under a US-Iran ceasefire extension. Brent crude retreated toward $85/barrel from recent highs above $90, and Singapore wholesale diesel — the benchmark for Australian terminal gate pricing — edged fractionally lower. However, the Australian Government's temporary fuel excise halving expires unconditionally on June 30 regardless of any Iran deal outcome, reverting from 26.3c to 52.6c per litre. That is a 26.3c rise landing on every diesel vehicle in your fleet from July 1. Any job being quoted today for post-June-30 delivery should already be using post-excise fuel rates in the cost model — or the margin evaporates before the job is finished.",
    "{{ECON_2_URL}}": "",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💹 AI · IPO",
    "{{TECH_1_HEADLINE}}": "OpenAI Files Confidential IPO at Up to $1 Trillion Valuation — $25B Revenue, Losing $1.22 for Every Dollar Earned",
    "{{TECH_1_SUMMARY}}": "OpenAI filed a confidential S-1 IPO prospectus with the US SEC on May 22, targeting a September 2026 public listing at a valuation of $852 billion to $1 trillion — potentially the largest tech IPO in history, led by Goldman Sachs and Morgan Stanley. Revenue hit $25 billion annualised by March 2026, from 50 million consumer subscribers and 9 million business users, with enterprise representing more than 40% of revenue. Despite the headline numbers, the filing confirms OpenAI is losing $1.22 for every $1.00 earned — burning capital on compute, talent and safety research at a rate analysts say will require $207 billion in further funding by 2030. For small business operators using OpenAI tools today: the AI you're paying for is still heavily cross-subsidised by investor capital. When pricing normalises toward profitability, operators who have built genuine workflows now will be best placed to absorb the shift.",
    "{{TECH_1_URL}}": "https://enterprisedna.co/resources/news/openai-ipo-confidential-filing-may-2026/",

    "{{TECH_2_FLAG}}": "🤖 AI · TOOLS",
    "{{TECH_2_HEADLINE}}": "Google Releases Gemini 3.1 Flash-Lite — 2.5× Faster, $0.25 Per Million Tokens — AI Cost Curve Steepens",
    "{{TECH_2_SUMMARY}}": "Google released Gemini 3.1 Flash-Lite this week — delivering 2.5× faster response times and 45% better output generation at just $0.25 per million input tokens. The release continues a structural trend: AI processing cost is falling roughly 10× every 12 months, driven by chip improvements, model compression and competition between Google, Anthropic and OpenAI. For small trades operators building AI workflows — quoting assistants, review responders, job note summarisers — purpose-built tools are approaching the cost of a coffee per month. The entry barrier is effectively gone. The competitive gap between operators using AI daily and those who aren't is now about workflow and habit — not cost.",
    "{{TECH_2_URL}}": "",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 ROBOTICS · SUMMIT",
    "{{ROBOT_1_HEADLINE}}": "Humanoids Summit Tokyo Closes — Chinese Robots Dominate as Japan's Industry Faces Its Sharpest Rivalry Yet",
    "{{ROBOT_1_SUMMARY}}": "The inaugural Asia edition of the Humanoids Summit Tokyo closed on May 29 at the Takanawa Gateway Convention Center, drawing 2,000 attendees from 30 countries and over 300 companies. Chinese humanoid robot manufacturers — Unitree, AgiBot and UBTECH — dominated the exhibition floor and commanded the largest crowds, with Japanese media noting the stark contrast with Japan's own industry, which pioneered humanoid robotics research but is now racing to commercialise at comparable pace. Speakers from Google DeepMind and Osaka University's Hiroshi Ishiguro addressed the convergence of large language models, computer vision and physical robotics. The summit's move to Asia signals that the next five years of humanoid deployment will be shaped as much in Beijing, Seoul and Tokyo as in Silicon Valley.",
    "{{ROBOT_1_URL}}": "https://www.japantimes.co.jp/business/2026/05/28/tech/tokyo-humanoid-summit/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Melbourne Home Values Post First Monthly Fall in Four Months as RBA Hikes Compound",
    "{{AUS_1_SUMMARY}}": "Capital city housing markets recorded broadly lower prices in May 2026, with Melbourne posting its first monthly decline in four months — reflecting the cumulative impact of three RBA rate hikes this year. The national median house price rose 0.9% in the March quarter but conditions have since stalled. Victoria's Housing Industry Association data shows building approvals outpacing actual construction starts by nearly 22,000 dwellings, with labour shortages and financing difficulties holding back new supply. For trades operators with residential renovation and improvement exposure, softening property values tend to suppress discretionary upgrade spend — the second-half pipeline is the indicator to watch closely over coming weeks.",
    "{{AUS_1_URL}}": "https://www.commbank.com.au/articles/newsroom/2026/05/rba-may-interest-rates-decision.html",

    "{{AUS_2_HEADLINE}}": "Federal Budget's $722.8M Apprenticeship Package — $10K Incentives for New Housing Construction Tradies Now Active",
    "{{AUS_2_SUMMARY}}": "The 2026 Federal Budget's $722.8 million apprenticeship package includes $10,000 incentive payments for new apprentices entering housing construction trades, paid in instalments over the life of the apprenticeship. An additional $85.2 million fast-tracks skills assessments for overseas-trained tradies, with the Government targeting a reduction in processing time of up to six months. For established trades businesses, both measures signal increasing labour supply over the next 24–36 months. Operators who hire an apprentice now can access both the employer incentive payments and the streamlined assessment system for overseas workers already in their network — worth checking directly with the Department of Employment before the financial year closes.",
    "{{AUS_2_URL}}": "",

    # Victoria
    "{{VIC_1_HEADLINE}}": "City of Melbourne Budget 2026-27 — 13 New Parks, Community Safety Officers Doubled, State Pipeline Hits $21.4B",
    "{{VIC_1_SUMMARY}}": "Melbourne City Council's draft 2026-27 budget delivers 13 new or upgraded parks across the municipality and doubles Community Safety Officers from 11 to 22. The City budget sits within a broader $21.4 billion Victorian state infrastructure investment program for 2025-26, which includes the Suburban Rail Loop East, North East Link tunnelling, and accelerated housing supply projects across Melbourne's growth corridors. For southeast Melbourne trades operators, the SRL East 26km underground alignment — connecting Cheltenham, Clayton, Monash, Glen Waverley, Burwood and Box Hill — continues to represent a long-tail civil, services, and protective coatings pipeline running through to at least 2035.",
    "{{VIC_1_URL}}": "",

    # Science
    "{{SCI_1_FLAG}}": "🌌 ASTRONOMY · ASTROBIOLOGY",
    "{{SCI_1_HEADLINE}}": "Moons of Rogue Planets Could Sustain Life for 4.3 Billion Years — No Star Required",
    "{{SCI_1_SUMMARY}}": "Researchers from Ludwig Maximilian University of Munich and the Max Planck Institute for Extraterrestrial Physics published findings on May 28 showing that moons orbiting free-floating 'rogue' planets — ejected from their star systems into deep space — could maintain liquid water oceans and support life for up to 4.3 billion years. Two mechanisms sustain warmth: tidal heating (the gravitational stretch-and-squeeze of an elliptical orbit generates internal friction), and dense hydrogen atmospheres (which trap residual heat at temperatures far below normal habitability thresholds). The moons could even experience wet-dry cycles — the chemistry thought to have initiated life on Earth — driven by tidal forces rather than sunlight. With the Milky Way estimated to contain billions of rogue planets, many potentially with moons, the research dramatically expands the candidate locations for extraterrestrial life beyond solar systems entirely.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Most Valuable Saturday Morning Habit: The 15-Minute AI Business Review",
    "{{INSIGHT_BODY}}": "Saturday morning is the best time most small trades operators never use. The week's jobs are still fresh, the weekend hasn't started, and there's fifteen quiet minutes before anyone needs anything. Here's what a focused AI-assisted review looks like in practice: Tell an AI tool — Claude, ChatGPT, Gemini — the three jobs completed this week and the rough margin on each, then ask it which was most profitable and why. Pull up your outstanding quotes and ask it to draft a follow-up message for anything older than five days. Check next week's schedule and ask the AI to flag any resourcing gaps or scheduling conflicts. That's four prompts — fifteen minutes. What most operators find surprises them: they have no clear picture of which job type is actually most profitable, because nobody's had time to look. The AI doesn't do the analysis for you — but it frames the question you've been avoiding, and that question is usually the one that moves the business. Start this Saturday, while the week's data is fresh.",

    # Fun Facts
    "{{FACT_1}}": "The deepest point on Earth is Challenger Deep in the Mariana Trench (western Pacific) — 10,935 metres below sea level, deep enough to fully submerge Mount Everest with over a kilometre to spare. Pressure at that depth reaches approximately 1,086 bar — roughly 1,000 times atmospheric pressure. A standard 200-litre steel drum dropped in would be crushed to roughly the size of a soup can within seconds of reaching the bottom.",

    "{{FACT_2}}": "Bubble Wrap was accidentally invented in 1957 by engineers Alfred Fielding and Marc Chavannes, who were originally attempting to design textured plastic wallpaper. When the wallpaper concept flopped commercially, they pivoted to packaging — IBM was an early adopter, using it to ship the IBM 1401 computer in 1959. Today, Sealed Air Corporation (the company Fielding and Chavannes founded) produces enough Bubble Wrap each year to wrap the Earth roughly 10 times.",

    "{{FACT_3}}": "The Aurora Australis (Southern Lights) is regularly visible from Melbourne and the Mornington Peninsula during periods of high solar activity — and 2025-2026 sits near the peak of Solar Cycle 25's maximum. The phenomenon occurs when charged solar particles collide with oxygen atoms in the ionosphere at 100–300 km altitude, producing characteristic green glows; nitrogen produces blue and purple. On strong nights, the aurora has been photographed from Victoria's southeastern coastline, including beaches around the Mornington Peninsula and south Gippsland — looking south toward Antarctica.",

    # Joke
    "{{JOKE_SETUP}}": "Why do crane operators make the best friends?",
    "{{JOKE_PUNCHLINE}}": "They'll always lift you up when you're feeling low — and they know exactly when you've hit the safe working load.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The future belongs to those who believe in the beauty of their dreams.”",
    "{{CLOSING_ATTR}}": "— Eleanor Roosevelt",
    "{{CLOSING_MESSAGE}}": "Saturday, 30 May 2026 — wet start to the weekend in Carrum Downs, with showers likely this afternoon and running daily through to Wednesday. If there's outdoor work on today, the morning window is your best bet. The US-Iran ceasefire deal is the big one to watch this weekend: if Trump signs off, the Strait of Hormuz reopens, oil eases further, and Australia's fuel cost picture improves heading into July — but the June 30 excise reversal is locked in regardless. The week's robotics news out of Tokyo confirmed what the production numbers have been showing for months: China has moved from observer to dominant force in humanoid deployment. Worth staying across as automation costs come down toward trades-relevant territory. Enjoy your Saturday, Liall.",
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
