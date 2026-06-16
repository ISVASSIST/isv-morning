#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 17 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Wed 17 Jun
    # BOM forecast: Wed clear/light winds; Thu frost risk/patchy fog; Fri–Sun showers & northerlies
    "{{WEATHER_1}}": "WED 17 · ☀️ Clear · 14°C",
    "{{WEATHER_2}}": "THU 18 · 🌥 Frost risk · 10°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 19 · 🌧 Showers · 12°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SAT 20 · 🌦 Shower risk · 13°C",
    "{{WEATHER_5}}": "SUN 21 · 🌧 Showers · 13°C",
    "{{WEATHER_ALERT}}": "⚠ FROST RISK THU AM · SHOWERS & N'LY WINDS FRI–SUN",

    # World
    "{{WORLD_1_FLAG}}": "🌐 G7 · Évian",
    "{{WORLD_1_HEADLINE}}": "G7 Leaders Issue AI for Prosperity Statement — Summit Closes in France With First-Ever Commitment to SME AI Adoption",
    "{{WORLD_1_SUMMARY}}": "The 52nd G7 Summit wrapped up today in Évian-les-Bains, France, with leaders releasing a joint communiqué that includes a landmark AI for Prosperity statement — the first formal G7 commitment to actively support AI adoption by small and medium-sized enterprises. On critical minerals, nations agreed to standards-based market mechanisms to reduce Chinese supply chain dependency, though the US blocked France's proposed permanent Critical Minerals Secretariat. The summit also addressed Ukraine, the West Asia peace process, and global trade imbalances. For Australian businesses, the practical consequence is that rules governing AI tools, data localisation, and cross-border AI liability are now being set at G7 level — Australia typically aligns with those frameworks within 12 to 18 months.",
    "{{WORLD_1_URL}}": "https://www.consilium.europa.eu/en/meetings/international-summit/2026/06/15-17/",

    "{{WORLD_2_FLAG}}": "🌐 Ukraine · Kyiv",
    "{{WORLD_2_HEADLINE}}": "Russia Intensifies Aerial Strikes on Ukrainian Cities as Ground Advance Stalls — UNESCO Condemns Kyiv Monastery Attack",
    "{{WORLD_2_SUMMARY}}": "Russia stepped up aerial bombardment of Ukrainian cities this week as battlefield ground advances slowed, with European defence officials assessing the escalation as a signal of growing military and economic pressure on Moscow. A Russian strike damaged the Kyiv Pechersk Lavra monastery — a UNESCO World Heritage site — drawing international condemnation. On the diplomatic front, Hungary dropped its objection to formal EU accession talks for Ukraine, while remaining opposed to the fast-track process Kyiv is seeking as a security guarantee against future aggression. The Ukraine conflict has received less international attention this week, overshadowed by the G7 summit and the pending US-Iran signing.",
    "{{WORLD_2_URL}}": "https://www.npr.org/sections/world/",

    # Economics
    "{{ECON_1_FLAG}}": "🏦 RBA · June 2026",
    "{{ECON_1_HEADLINE}}": "RBA Holds at 4.35% — Unanimous Decision, But Rules Out Near-Term Cuts With Hawkish Language",
    "{{ECON_1_SUMMARY}}": "The Reserve Bank of Australia held the cash rate at 4.35% at its June board meeting yesterday, with Governor Michele Bullock confirming the unanimous decision at a 3:30pm AEST press conference. The tone was notably hawkish: the RBA stated it will 'do what it considers necessary, including increasing the cash rate further if required' — a line that pushed back against expectations of a near-term cut. Major banks still expect an August reduction is possible if June CPI data comes in soft, but nothing is guaranteed. For trades businesses carrying variable rate commercial debt, the message is direct: plan FY2027 at current rates. Don't build a cash flow forecast that depends on a rate cut arriving on schedule.",
    "{{ECON_1_URL}}": "https://www.rba.gov.au/monetary-policy/int-rate-decisions/",

    "{{ECON_2_FLAG}}": "📋 ATO · EOFY",
    "{{ECON_2_HEADLINE}}": "13 Days to EOFY — Three June 30 Deadlines Every Small Business Needs to Act On Now",
    "{{ECON_2_SUMMARY}}": "The ATO has published its 30-page small business EOFY guide flagging three simultaneous June 30 deadlines. First: the $20,000 instant asset write-off — available to businesses with aggregated turnover under $10 million — closes June 30 and reverts to $1,000 from July 1. Any plant, tools, or equipment costing up to $20,000 that is purchased and in use before June 30 qualifies. Second: the ATO's Small Business Superannuation Clearing House shuts permanently on June 30 — businesses using it must migrate to another platform now. Third: trust income distributions must be formally documented before June 30 or risk being taxed at the highest marginal rate. All three deadlines hit simultaneously. Act this week.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🌐 G7 · AI for SMEs",
    "{{TECH_1_HEADLINE}}": "G7 AI for Prosperity Statement — Governments Formally Commit to Removing Barriers to AI Adoption for Small Business",
    "{{TECH_1_SUMMARY}}": "The G7 Évian communiqué released today contains the first formal commitment by world leaders to support AI adoption specifically for small and medium-sized enterprises. The AI for Prosperity statement calls on member governments to identify and remove policy barriers to SME AI uptake, share best practice on AI training, and ensure small businesses are not disadvantaged by data governance rules designed primarily for large platforms. For Australian small business, the practical effect unfolds over 12 to 18 months: expect updated AI procurement guidance, possible tax incentives for AI tools, and regulatory frameworks calibrated for SME capacity rather than big-tech compliance budgets. The direction is now unambiguous — AI for small business is no longer a fringe policy topic.",
    "{{TECH_1_URL}}": "https://www.consilium.europa.eu/en/meetings/international-summit/2026/06/15-17/",

    "{{TECH_2_FLAG}}": "🔬 AI Research",
    "{{TECH_2_HEADLINE}}": "New Study: Top AI Models Degrade Sharply on Complex Multi-Step Tasks — Exactly the Work Businesses Need Most",
    "{{TECH_2_SUMMARY}}": "A study published this week gave leading AI language models a sustained attention test — identifying and tracking specific information across increasingly long and complex inputs — and found a consistent pattern: accuracy was high on short, simple tasks but degraded sharply as length and complexity grew. The finding is directly relevant to anyone using AI for business tasks involving long documents, multi-step analysis, or extended reasoning. The practical takeaway: break complex tasks into shorter, focused segments rather than sending everything in one prompt. Reviewing a 50-page subcontractor agreement? Five sequential, targeted prompts will consistently outperform one large instruction. AI works best when you work with its limitations, not around them.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 Automate 2026 · Chicago",
    "{{ROBOT_1_HEADLINE}}": "America's Biggest Automation Show Opens in Chicago Next Week — NVIDIA Sponsors a Dedicated Humanoid Robot Pavilion in an Industry First",
    "{{ROBOT_1_SUMMARY}}": "Automate 2026 — North America's largest robotics and automation trade show — opens at Chicago's McCormick Place on June 22, with over 1,000 exhibitors across 450,000 square feet and an anticipated 50,000 attendees. In a first for the show, NVIDIA is sponsoring a dedicated Humanoid Robot Pavilion on the show floor with live working robot demonstrations and a presentation theatre for exhibitor talks throughout the four-day event. The NVIDIA pavilion matters because its Isaac Sim and GR00T AI platforms have become the de facto software infrastructure for humanoid robot development globally. For the trades and industrial services sector, Automate is where the technology pipeline gets set — products debuted there typically reach Tier 1 industrial clients within 18 months.",
    "{{ROBOT_1_URL}}": "https://www.automateshow.com/education-networking/humanoid-robot-pavilion",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Top Group D — Australia Eyes Decisive USA Clash in Seattle on Saturday Morning",
    "{{AUS_1_SUMMARY}}": "Following their 2–0 win over Türkiye in Vancouver on June 14, Australia sit top of FIFA World Cup 2026 Group D with 3 points. The Socceroos face USA in Seattle on Saturday June 20 — kickoff 5:00am AEST — in the pivotal group-stage match. The US enter with home crowd support and heavy expectation, but Australia have momentum, a clean sheet, and the psychological edge of an opening-game statement win. A victory or draw in Seattle would virtually guarantee a round of 16 berth. The match is live on SBS and SBS On Demand. Coach Tony Popovic's squad is in preparation camp in Seattle this week.",
    "{{AUS_1_URL}}": "https://socceroos.com.au/match/usa-v-australia-fifa-world-cuptm-2026-20-06-2026/22278774",

    "{{AUS_2_HEADLINE}}": "NDIS Shake-Up Proceeds — 160,000 Participants Face Eligibility Review as Thriving Kids Launches July 1",
    "{{AUS_2_SUMMARY}}": "The federal government is pressing ahead with NDIS reforms targeting a reduction from 760,000 participants to 600,000 by 2030, despite fierce pushback at Senate inquiry hearings this week. The centrepiece change redirects children under eight with developmental delays to a new Thriving Kids early intervention programme launching July 1. Disability advocates and specialist medical groups have warned the eligibility changes will cause direct harm. The government argues scheme growth — adding approximately 40,000 participants per year at an average plan cost of $31,000 — is fiscally unsustainable. The Senate inquiry continues with further submissions this week.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Permanent Pill Testing Service in Fitzroy Hits Six-Month Milestone — 2,300 Samples Tested, Hours Extended Through June",
    "{{VIC_1_SUMMARY}}": "Victoria's first fixed-site pill testing service at 95 Brunswick Street Fitzroy has reached its six-month mark, having tested more than 2,300 drug samples and engaged over 1,300 people in harm reduction conversations. The free, confidential, and legal service — part of the state government's strategy to combat fentanyl and synthetic opioid contamination — has extended its Thursday and Friday hours through the end of June to meet demand. It operates Thursdays 12pm–4pm, Fridays 3pm–7pm, and Saturdays 1pm–7pm. Victoria is Australia's second state to offer a permanent fixed-site testing service after South Australia.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 Chemistry · ScienceDaily",
    "{{SCI_1_HEADLINE}}": "Scientists Identify How Ultraviolet Light Destroys 'Forever Chemicals' — No Added Chemicals Required",
    "{{SCI_1_SUMMARY}}": "Researchers have published a significant breakthrough in PFAS 'forever chemical' remediation: hydrogen radicals generated when water is exposed to intense ultraviolet light are the key agent in breaking down PFAS molecules. Published in Environmental Science & Technology in mid-June 2026, the study found that under high-energy UV at wavelengths below 300nm, hydrogen radicals progressively strip fluorine atoms from PFAS compounds, degrading them into less persistent substances — without requiring chemical reagents. PFAS contamination is widespread across Australian industrial sites, military facilities, and several metropolitan water catchment areas including sites near Melbourne. This mechanism could underpin scalable treatment systems that are significantly cheaper than current chemical-intensive approaches.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Help You Brief a New Client in 60 Seconds — Before You Even Take the Call",
    "{{INSIGHT_BODY}}": "Most trades business owners spend the first 15 minutes of a new client call figuring out whether the job is even worth quoting. That is time you don't have when you're running a crew. AI can front-load that filter. Before your next quote call, paste the client's initial contact form, email, or referral note into Claude or ChatGPT and ask it to generate a 60-second brief: who they probably are, what the job likely involves based on the description, three questions you should ask before agreeing to quote, and two red flags to watch for — scope creep, absent decision-maker, unrealistic timeline. The whole exercise takes 90 seconds and gives you a mental framework before you pick up the phone rather than winging it. Over a year, that habit quietly filters out the clients who were never going to be profitable. It also makes you sound more prepared than almost anyone else they're calling — which matters when you're competing on reputation, not just price.",

    # Fun Facts
    "{{FACT_1}}": "Water expands by approximately 9 percent when it freezes — which is why pipes burst during frost events, why potholes open in roads after cold nights, and why Victorian water authorities use flexible expansion joints in mains infrastructure. The expansion force is strong enough to split solid granite boulders on exposed mountainsides over repeated freeze-thaw cycles. It's the same physics that drove the shift away from rigid cast iron in building services pipe systems.",

    "{{FACT_2}}": "The Great Wall of China is not visible from space with the naked eye — a fact confirmed by China's first astronaut, Yang Liwei, who specifically looked for it during the 2003 Shenzhou 5 mission and reported he could not see it. The wall is typically only 4 to 9 metres wide, far below the resolution of the human eye at orbital altitude. The myth appears to have originated in a 1932 Ripley's Believe It or Not column, was repeated so widely it became accepted as fact, and persisted in school textbooks for decades after it was debunked.",

    "{{FACT_3}}": "The word 'plumber' comes from the Latin plumbum, meaning lead. Roman plumbers worked with lead pipes, and that origin is preserved today in the chemical symbol for lead — Pb — and in the name of the trade itself. Lead plumbing was standard practice across the Roman Empire and remained common in European and Australian buildings well into the 20th century, until research confirmed lead's toxicity. The job title survived the pipe material by roughly two thousand years.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the floor sander always win at poker?",
    "{{JOKE_PUNCHLINE}}": "He knew exactly when to strip it back — and when to put on a silky smooth finish.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The journey of a thousand miles begins with a single step.”",
    "{{CLOSING_ATTR}}": "— Lao Tzu",
    "{{CLOSING_MESSAGE}}": "It's a clear Wednesday in Carrum Downs — the best weather day in the next five. Frost risk arrives Thursday morning, then showers and northerlies through Friday to Sunday, so plan site access accordingly. The RBA held at 4.35% yesterday with a hawkish tone — no cuts guaranteed for FY2027, so price accordingly. The G7 wrapped in France today with a formal AI for SME commitment that will shape Australian policy over the next 18 months. Thirteen days to EOFY: the $20K write-off closes June 30, the ATO Super Clearing House closes June 30, and the Socceroos face the USA in Seattle at 5am Saturday. A lot happening this week, Liall. One step at a time.",
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
