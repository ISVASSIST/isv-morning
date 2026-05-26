#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 27 May 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 27 May (BOM forecast)
    "{{WEATHER_1}}": "WED 27 · 🌧 Showers · 14°C",
    "{{WEATHER_2}}": "THU 28 · ☁️ Cloudy · 13°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 29 · 🌦 Showers · 14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 30 · 🌤 Sunny spells · 16°C",
    "{{WEATHER_5}}": "SUN 31 · ☁️ Cloudy · 13°C",
    "{{WEATHER_ALERT}}": "❄ LOWS TO 7°C — WINTER CLOSING IN",

    # World
    "{{WORLD_1_FLAG}}": "🕌 SAUDI ARABIA · HAJJ 2026",
    "{{WORLD_1_HEADLINE}}": "Two Million Pilgrims Reach Hajj's Sacred Peak at Mount Arafat — 47°C Heat Tests Saudi Emergency Services",
    "{{WORLD_1_SUMMARY}}": "Nearly two million Muslim pilgrims from more than 150 countries gathered on the plains of Mount Arafat in western Saudi Arabia yesterday — the spiritual climax of the annual Hajj. Saudi authorities deployed 25 field hospitals and more than 25,000 health workers as temperatures at the holy sites reached 47°C. The Al Mashair Metro ran approximately 2,000 train journeys on the day, moving more than two million passengers — the world's largest single-day transit operation by passenger volume. The Hajj concludes with Eid al-Adha today, with pilgrims completing the symbolic stoning at Mina before the final circumambulation of the Kaaba in Mecca. This year's gathering is among the most technically coordinated in the pilgrimage's 1,400-year history.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/gallery/2026/5/26/hajj-pilgrims-gather-at-mount-arafat-under-scorching-desert-sun",

    "{{WORLD_2_FLAG}}": "🇮🇷🇺🇸 IRAN · NUCLEAR DEAL",
    "{{WORLD_2_HEADLINE}}": "Trump Says US-Iran Nuclear Deal Is \"Close\" — Tehran Dismisses Core Demand as a \"Fantasy\"",
    "{{WORLD_2_SUMMARY}}": "President Trump said yesterday both sides were close to finalising a nuclear agreement involving strong inspections, but Iranian Foreign Minister Araghchi said he was uncertain whether a deal was imminent. Supreme Leader Khamenei's senior advisor dismissed Trump's demand for control over Iran's nuclear program as a fantasy. The US military conducted self-defence strikes in southern Iran on 25 May even as back-channel talks continued — a deliberate pressure strategy according to analysts. The US-Israel-Iran conflict, now in its third month since coordinated strikes on 28 February, continues to drive oil price volatility. Australia's April fuel excise cut was partly a direct response to the oil shock that followed the conflict's opening phase.",
    "{{WORLD_2_URL}}": "https://www.cnn.com/2026/05/24/middleeast/iran-us-proposed-deal-wwk-intl",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AUSTRALIA · FUEL PRICES",
    "{{ECON_1_HEADLINE}}": "Diesel Down 30%, Petrol Down 28% — ACCC Confirms Excise Relief Is Working, But Closes June 30",
    "{{ECON_1_SUMMARY}}": "The ACCC's weekly fuel price monitoring update as at 20 May confirmed Australian retail diesel is down approximately 30% and petrol down 28% across the five major capitals since the government halved fuel excise from 52.6 to 26.3 cents per litre on April 1. The measure costs the budget $2.9 billion and runs until June 30 only. Middle East conflict risk remains the primary upside price threat the ACCC is watching weekly. For trades operators running fleets or heavy equipment, 34 days remain on this relief window — a practical moment to schedule fuel-intensive jobs and front-load procurement before the excise rate reverts on July 1.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "🇦🇺 BUDGET 2026-27",
    "{{ECON_2_HEADLINE}}": "497 Nuisance Tariffs Scrapped From July 1 — Tyres, Air Conditioners and Bitumen Among Items Getting Cheaper",
    "{{ECON_2_SUMMARY}}": "A quietly significant measure in the 2026-27 Federal Budget will abolish 497 tariffs from July 1, streamlining approximately $23 billion in annual trade flows. Items freed from import duties include tyres, air conditioners, bitumen, wine glasses, and margarine — several of which are inputs or consumables relevant to trades operations. For businesses that import tools, components, or materials currently subject to these duties, July 1 is a practical procurement planning date. The same budget also locks in the permanent $20,000 instant asset write-off for businesses with turnover under $10 million, plus a new $1,000 instant work-related tax deduction for all workers — both effective July 1.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🔐 ANTHROPIC · CYBERSECURITY",
    "{{TECH_1_HEADLINE}}": "Anthropic's Claude Mythos Finds 10,000+ Zero-Day Flaws in Every Major OS and Browser — Patching Is Now the Bottleneck",
    "{{TECH_1_SUMMARY}}": "An update to Anthropic's Project Glasswing published yesterday revealed Claude Mythos Preview has identified more than 10,000 high- and critical-severity software vulnerabilities across every major operating system and browser — including a 27-year-old flaw in OpenBSD and a 16-year-old bug in FFmpeg that had survived all prior human review and automated scanning. Findings were shared with AWS, Apple, Cisco, Google, Microsoft, NVIDIA, and the Linux Foundation. But only 97 vulnerabilities have been patched upstream despite 1,596 verified reports — exposing volunteer open-source maintainer capacity as the critical constraint in the AI-enabled security era. The finding is the strongest evidence yet of AI performing superhuman code review, and the patching lag it has created is a live risk in enterprise and government systems.",
    "{{TECH_1_URL}}": "https://www.helpnetsecurity.com/2026/05/26/anthropic-project-glasswing-update/",

    "{{TECH_2_FLAG}}": "🌐 GOOGLE · AI AGENTS",
    "{{TECH_2_HEADLINE}}": "Google's New AI Agents Shop the Whole Internet For You — Universal Cart and Gemini Omni Among I/O 2026 Rollouts",
    "{{TECH_2_SUMMARY}}": "Google I/O 2026 this month unveiled Gemini Omni — a multimodal AI model generating video, image, and text output from any input type — alongside a suite of AI agents now rolling out across Google products. The most practically significant for business is Universal Cart: an AI agent that searches across multiple retailers, compares prices, and completes purchases across different websites simultaneously without manual checkout. Gemini Spark is a new personalised daily AI briefing and task agent in the Gemini app. Together these signal Google's shift from search engine to AI-first operating system — and place AI-completed purchases in mainstream consumer tech within months. For any small business selling products online, AI agents will soon be the primary buying interface your customers use.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 HYUNDAI · ATLAS ROBOT",
    "{{ROBOT_1_HEADLINE}}": "Hyundai Accelerates Atlas Humanoid Mass Production — New AI Factory Division Targets 30,000 Units Per Year by 2028",
    "{{ROBOT_1_SUMMARY}}": "Hyundai Motor Group announced this week it is accelerating mass production of its Atlas humanoid robot and creating dedicated software-defined factory and robotics divisions to fast-track industrial deployment. The group — which owns Boston Dynamics (acquired 2021) — is targeting 30,000 Atlas units per year by 2028, beginning with parts sequencing tasks before scaling to component assembly by 2030. Atlas is designed for repetitive, heavy, and complex operations across Hyundai's global factory network. When a manufacturer of Hyundai's scale commits publicly to 30,000 humanoid units per year, it validates the economics of industrial humanoids more powerfully than any startup announcement — and it compresses the timeline for the technology reaching wider industrial sectors.",
    "{{ROBOT_1_URL}}": "https://www.upi.com/Top_News/World-News/2026/05/25/motor-group-humanoid-robot-software-defined-factory/7101779760033/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Leave Florida for LA Today as World Cup Final Countdown Reaches Three Weeks",
    "{{AUS_1_SUMMARY}}": "The Socceroos are heading from Sarasota, Florida to Los Angeles today as their FIFA World Cup 2026 preparation camp enters its final phase. Coach Tony Popovic will name the official 26-player squad on June 1, after a pre-tournament friendly against Mexico at Pasadena's Rose Bowl on May 30. Australia faces Türkiye in Vancouver on June 13, the USA in Seattle on June 19, and Paraguay in the San Francisco Bay Area on June 25 — all in Group D. Eight players were released from the extended training squad this week. Australia hasn't progressed past the round of 16 since 2006 — Group D offers a realistic path.",
    "{{AUS_1_URL}}": "https://socceroos.com.au/news/commbank-socceroos-commence-fifa-world-cup-2026tm-pre-camp-sarasota-florida",

    "{{AUS_2_HEADLINE}}": "Australia's Worst Diphtheria Outbreak in Decades — 194 Cases in 2026, Mostly Indigenous Communities, Possible First Death Since 2018",
    "{{AUS_2_SUMMARY}}": "Federal Health Minister Mark Butler has described the current diphtheria outbreak as Australia's worst in decades, with 194 infections notified in 2026 as of May 11. The outbreak predominantly affects Aboriginal and Torres Strait Islander communities — 93.8% of cases — concentrated in the Northern Territory (60%) and Western Australia (37%). Unlike pre-2020 patterns when diphtheria was typically travel-imported, this outbreak is mostly locally acquired. Authorities are awaiting autopsy results on a potential diphtheria-related death in the NT; if confirmed, it would be Australia's first fatal case since 2018. The scale of the outbreak is prompting urgent calls for improved vaccination programs in remote communities.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne's Free Public Transport Ends This Sunday — Half-Price $5.70/Day Fares Start Monday June 1",
    "{{VIC_1_SUMMARY}}": "Victoria's free public transport period across all metropolitan and regional trains, trams, and buses ends this Sunday May 31. From Monday June 1, fares halve across the state: a full daily fare drops from $11.40 to $5.70 anywhere in Victoria, saving the average commuter an estimated $850 across the six-month half-price period to January 2027. The Victorian Budget 2026-27 also delivers a 20% car registration reduction worth up to $186 per vehicle. For trades businesses with staff commuting into or around the Carrum Downs area from different suburbs, it's worth flagging the change before Monday so no one hits the gate expecting free travel.",

    # Science
    "{{SCI_1_FLAG}}": "🧠 NEUROSCIENCE · TEXAS A&M",
    "{{SCI_1_HEADLINE}}": "Two-Dose Nasal Spray Reverses Brain Aging in Mice — Memory and Cognitive Function Restored for Months",
    "{{SCI_1_SUMMARY}}": "Researchers at Texas A&M University have developed a nasal spray that reverses key markers of brain aging after just two doses, published on ScienceDaily yesterday. The spray contains microscopic particles derived from neural stem cells that bypass the blood-brain barrier via the nasal route, delivering microRNA sequences that switch off inflammatory signals in aging brain tissue and boost cellular energy supply. Mice equivalent in age to 60-year-old humans showed significantly reduced brain inflammation and improved memory and cognitive function within weeks, with benefits persisting for months. The Texas A&M team is filing a patent and working toward a human-applicable formulation for eventual clinical trials. The key practical advance is the delivery mechanism — nasal administration is far more accessible than injection-based therapies.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Why the Best Tradies in 2026 Are Treating AI Like a Business Partner, Not a Search Engine",
    "{{INSIGHT_BODY}}": "There's a meaningful difference between asking AI a question and working through a problem with it. Most operators who've tried AI tools and found them underwhelming were using them the first way — querying for answers, expecting a search engine. The ones pulling ahead are using them the second way: feeding context, asking for analysis, pushing back on the output, and iterating. That shift changes everything. When you paste a quote scope into Claude and ask it to pressure-test the margin, flag missed scope items, and suggest where a competitor might undercut you — you're not doing a search. You're working through a business problem with a collaborator that has read more quotes and contracts than any person you'll ever hire. For a trades operator running lean, that's like having a silent business partner who's available at 10pm, has no ego, and remembers everything you've told it about your business this session. The threshold for getting real value is simple: bring your actual work, not test questions. Operators who've made that shift report the biggest change isn't any single output — it's that business decisions start feeling deliberate rather than reactive.",

    # Fun Facts
    "{{FACT_1}}": "The world's oldest known lock and key dates back around 4,000 years to the ancient Assyrian city of Nineveh (present-day Iraq). The mechanism was entirely wooden — a large key lifted a row of wooden pins to allow a bolt to slide. The Romans later miniaturised the concept into iron locks with bronze keys small enough to wear as rings, so valuables could be locked away while the owner bathed at the public baths.",

    "{{FACT_2}}": "Pac-Man was originally released in Japan in 1980 under the name Puck-Man — but when Namco licensed the game for North American release, the name was deliberately changed because operators feared vandals would scratch the letter P into something offensive. The four ghosts — Blinky, Pinky, Inky, and Clyde — each follow distinctly different AI pursuit algorithms: Blinky directly chases the player, Pinky tries to ambush four squares ahead, Inky uses a complex offset calculation, and Clyde switches randomly between chasing and retreating.",

    "{{FACT_3}}": "The Hubble Space Telescope launched in 1990 with a catastrophic flaw: its 2.4-metre primary mirror had been ground to the wrong curvature by just 2.2 micrometres — roughly 1/50th the width of a human hair. Every image it returned was blurry. NASA astronauts corrected the error in orbit in December 1993 by installing custom corrective optics. Hubble went on to directly contribute to more than 18,000 peer-reviewed scientific publications and helped establish that the expansion of the universe is accelerating.",

    # Joke
    "{{JOKE_SETUP}}": "My plumber told me the job would be a quick fix.",
    "{{JOKE_PUNCHLINE}}": "That was two weeks ago. I've started naming the puddles.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Two roads diverged in a wood, and I — I took the one less travelled by, and that has made all the difference.”",
    "{{CLOSING_ATTR}}": "— Robert Frost",
    "{{CLOSING_MESSAGE}}": "Wednesday 27 May — showers this morning and winter firmly closing in, with lows dropping to 7°C through the week. Free public transport ends this Sunday, so enjoy the last few days before the $5.70 daily fare kicks in from Monday. The Anthropic zero-day story in tech today is worth a full read — 10,000 software vulnerabilities found by AI in weeks is a genuinely significant development for anyone running digital infrastructure. The Socceroos leave Florida for LA today with the squad announcement in five days — Group D is winnable. Fuel excise relief closes in 34 days: schedule heavy diesel work now while the saving still applies. Have a good hump day, Liall.",
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
