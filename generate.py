#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 15 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 15 Jun
    # Fog early Mon; showers Tue–Thu; easing Fri
    "{{WEATHER_1}}": "MON 15 · ⛅ Fog early · 17°C",
    "{{WEATHER_2}}": "TUE 16 · 🌧 Showers · 18°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 17 · 🌧 Shower risk · 13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 18 · 🌧 Heavy showers · 13°C",
    "{{WEATHER_5}}": "FRI 19 · ⛅ Easing · 12°C",
    "{{WEATHER_ALERT}}": "⚠ FOG MON AM · SHOWERS TUE–THU",

    # World
    "{{WORLD_1_FLAG}}": "🌐 Iran · US",
    "{{WORLD_1_HEADLINE}}": "Trump Says US-Iran Ceasefire Deal Close to Finalisation — Qatari Negotiators Fly to Tehran as Strait of Hormuz Reopening Looms",
    "{{WORLD_1_SUMMARY}}": "US President Donald Trump announced on June 14 that a ceasefire deal with Iran was ready to be signed, with Qatari negotiators flying directly to Tehran to finalise an agreement that has been months in the making. The proposed deal would see Iran reopen the Strait of Hormuz immediately — a critical global oil chokepoint — while the US simultaneously lifts its naval blockade of Iranian ports. A 60-day negotiating window would then follow to work toward a formal permanent settlement. Iran's government cast some doubt on the exact timing and disputed reported details of the draft, but both Washington and its mediators from Pakistan and Qatar signalled the framework was largely agreed. A successful reopening of the Strait would directly ease global oil supply pressure and could soften crude prices into July — relevant for every Australian diesel fleet operator watching June 30.",
    "{{WORLD_1_URL}}": "https://www.rferl.org/a/iran-war-us-hormuz-oil-blockade-gulf-israel/33640284.html",

    "{{WORLD_2_FLAG}}": "⚽ World Cup 2026 · Group C",
    "{{WORLD_2_HEADLINE}}": "Scotland End 36-Year World Cup Win Drought — McGinn's Deflected Strike Beats Haiti in Boston as Socceroos Also Triumph",
    "{{WORLD_2_SUMMARY}}": "Scotland claimed their first World Cup victory since 1990 with a hard-fought 1-0 win over Haiti at Gillette Stadium in Boston on June 14, ending a 28-year absence from the tournament and snapping a 36-year winning drought. Captain John McGinn's deflected strike in the second half separated the sides in Group C — where Scotland also face Morocco and Brazil. Earlier the same day, Australia beat Türkiye 2-0 in Vancouver with goals from Nestory Irankunda and Connor Metcalfe, and goalkeeper Patrick Beach produced eight saves against a side with 72% possession and 30 shots. A remarkable day for football nations that have waited a generation for World Cup success.",
    "{{WORLD_2_URL}}": "https://www.espn.com/soccer/story/_/id/49058587/world-cup-2026-today-blog-14-06-2026-live-updates-news-fixtures-schedule-results-scotland-win-brazil-morocco-draw",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ Fuel Watch · 15 Days",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Cut Expires in Exactly 15 Days — Diesel Set to Jump 26+ Cents Per Litre at Midnight July 1",
    "{{ECON_1_SUMMARY}}": "The federal government's halved fuel excise — saving diesel operators approximately 26.3 cents per litre since April 1 — expires at midnight on June 30, exactly 15 days from today. The full excise of 52.6 cents per litre returns from July 1, adding roughly 28 to 30 cents to the bowser price once GST and margins are factored in. Current Australian diesel sits around $2.05 per litre; expect that to climb above $2.30 from the first of July unless international crude prices fall significantly. Any job quoted at today's fuel rates for work scheduled in July or later needs its numbers reviewed before June 30. Watch the Iran deal news above — a Strait of Hormuz reopening this week could bring some crude price relief and soften the July spike slightly.",
    "{{ECON_1_URL}}": "https://fueldaddy.com.au/blog/fuel-excise-cut-2026/",

    "{{ECON_2_FLAG}}": "🏦 RBA · Meets Today",
    "{{ECON_2_HEADLINE}}": "RBA Two-Day Meeting Opens Today — Decision at 2:30pm AEST Tomorrow; Hold Expected at 4.35%, Eyes on August Cut Signal",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank of Australia's June board meeting begins today with the monetary policy decision due at 2:30pm AEST on Tuesday June 16. The consensus across the big four banks is a hold at 4.35%, but the language of the post-decision statement will be closely watched. CBA and NAB have both removed further rate hike forecasts, with some economists now flagging an August cut as possible if the Iran ceasefire stabilises oil prices and June inflation data comes in subdued. For trades businesses carrying variable-rate equipment finance or business credit lines, tomorrow's RBA statement could be the clearest forward signal yet on when cost-of-debt relief is coming.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💻 AI · Open Source",
    "{{TECH_1_HEADLINE}}": "Moonshot AI Open-Sources Kimi K2.7-Code — Free 1-Trillion-Parameter Coding Model Cuts Processing Cost by 30% and Beats Rivals on Tool Use",
    "{{TECH_1_SUMMARY}}": "Chinese AI company Moonshot AI released Kimi K2.7-Code on June 12, publishing the full model weights to Hugging Face under a Modified MIT Licence that permits free commercial use. The model runs 1 trillion parameters total with 32 billion active at any time via a Mixture-of-Experts architecture, achieves a 31.5% benchmark improvement on coding tasks over its predecessor, and burns 30% fewer compute tokens per answer. For small businesses and trades operators, the practical implication is that frontier AI coding capabilities are now available at zero cost to anyone willing to use open-source tools. The race to the bottom on AI pricing continues to accelerate — what cost thousands per month two years ago is increasingly free today.",
    "{{TECH_1_URL}}": "https://www.digitalapplied.com/blog/kimi-k2-7-code-release-open-source-coding-model",

    "{{TECH_2_FLAG}}": "🤖 AI · Models",
    "{{TECH_2_HEADLINE}}": "MiniMax M3 Cuts AI Processing Cost to One-Twentieth — 1M-Token Context Window Now Runs at 9x the Speed",
    "{{TECH_2_SUMMARY}}": "China's MiniMax released its M3 model with a Sparse Attention architecture that reduces per-token compute requirements to just one-twentieth of conventional models, with 9x faster input processing and 15x faster output for one-million-token context windows. In practical terms, this is an AI that can read an entire year of business documents, job records, invoices and emails in a single query — and do it vastly faster and cheaper than six months ago. Long-context AI models are becoming the infrastructure layer for business intelligence tools; as these capabilities become cheaper, the door opens for trades businesses to feed full financial years of operational data into AI analysis at minimal cost.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 Boston Dynamics · DeepMind",
    "{{ROBOT_1_HEADLINE}}": "Boston Dynamics' Electric Atlas Humanoid Ships First Units to Google DeepMind — AI Foundation Model Integration Moves From Lab to Live Robot",
    "{{ROBOT_1_SUMMARY}}": "The first production units of Boston Dynamics' electric Atlas humanoid robot are now shipping to Google DeepMind in June 2026, as part of an active partnership to integrate DeepMind's AI foundation models directly into Atlas's cognitive systems. The arrangement goes beyond standard robotics: DeepMind's models are designed to give Atlas real-time reasoning and adaptive decision-making so the robot can handle unstructured tasks without pre-programmed instructions. Units are also shipping in parallel to Hyundai's Robotics Metaplant Application Center, with all 2026 Atlas production already fully committed. The convergence of frontier AI with advanced physical robotics — in live industrial settings — marks a qualitative shift in what robots can be asked to do. What Boston Dynamics and DeepMind are building together today, mass-market manufacturers will be selling in five years.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/boston-dynamics-google-reunite-on-next-gen-atlas-humanoid/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Stun Turkey 2-0 in World Cup Opener — Irankunda and Metcalfe Goals, Beach Makes Eight Saves",
    "{{AUS_1_SUMMARY}}": "Australia opened their 2026 FIFA World Cup campaign with a composed 2-0 victory over Türkiye at BC Place in Vancouver on June 14 — their fifth win in World Cup history. Nestory Irankunda struck in the 27th minute and Connor Metcalfe sealed the result in the 75th, while goalkeeper Patrick Beach produced eight saves against a Turkish side that dominated with 72% possession and 30 shots. Coach Tony Popovic's disciplined defensive setup was widely praised after what was considered a significant upset. Australia next faces hosts USA on June 20 in Group D — the result that will define whether the Socceroos can realistically reach the knockout stage for the first time since 2006.",
    "{{AUS_1_URL}}": "https://www.skysports.com/football/news/12098/13552630/world-cup-2026-australia-2-0-turkey-socceroos-make-winning-start-to-group-d-campaign-in-vancouver",

    "{{AUS_2_HEADLINE}}": "NDIS Minister Defends Plan to Cut 160,000 Participants — People With Disability Warn Reforms Risk Lives",
    "{{AUS_2_SUMMARY}}": "NDIS Minister Mark Butler is defending proposed reforms that would reduce scheme participant numbers from 760,000 to 600,000 by 2030, with cuts to social and community participation funding beginning as early as July 1. Disability advocates warned the changes were life-threatening; the government argues growth rates are unsustainable and has proposed diverting under-8s with developmental delays or autism to a new program called Thriving Kids. The debate has been among the most charged of the current parliamentary term, with specialist medical associations joining advocates in opposing the eligibility tightening.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Yarra Valley Winter Wine Festival Running Now Through June 27 — 15 Days of Wine, Fire and Feasts an Hour From Carrum Downs",
    "{{VIC_1_SUMMARY}}": "The Yarra Valley Winter Wine Festival is midway through its 15-day run, continuing until June 27 across wineries and restaurants throughout the valley. The festival features prix-fixe cellar door menus, chef-driven collaborative dinners, and fireside wine tastings that typically sell out quickly in the middle weeks. About an hour from Carrum Downs via the Eastern Freeway to Lilydale, it is one of Victoria's most accessible wine region escapes in winter. Several participating venues still have midweek bookings available — worth a look if a Wednesday evening off the tools is on the cards this week.",

    # Science
    "{{SCI_1_FLAG}}": "🔭 Astrophysics · New Theory",
    "{{SCI_1_HEADLINE}}": "Dying Stars May Spawn New Universes Instead of Black Holes — Gravastar Theory Gets Fresh Theoretical Support",
    "{{SCI_1_SUMMARY}}": "A new theoretical study published in Physical Review D and reported by ScienceDaily on June 14 proposes that when a massive star collapses, it might not form a singularity hidden behind an event horizon. Instead, dark energy building inside the collapsing core could push back against gravity and trigger the expansion of a miniature new universe inside the dying star — creating an exotic object called a gravastar — rather than crushing everything to an infinite point. The theory, from researchers at Goethe University Frankfurt, offers a potential resolution to one of physics' most uncomfortable gaps: existing mathematics breaks down entirely at a black hole singularity, meaning the known laws of physics literally cannot describe what happens there. Gravastars would look identical to black holes from the outside — but have a completely different interior, and no singularity at all.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Build a Price Escalation Clause Into Every FY2027 Quote — AI Can Write One in 90 Seconds",
    "{{INSIGHT_BODY}}": "The combination of the full fuel excise reversion on July 1, the minimum wage rise on July 1, and ongoing material cost pressures means any fixed-price job quoted in June for work starting in August or later is already carrying hidden margin risk. A price escalation clause — sometimes called a rise-and-fall clause — protects you by linking the final invoice to verified movement in specific input costs, typically fuel, labour, and materials. Without one, you absorb all the inflation risk; with one, your client shares it proportionally. AI can draft a clear, professional price escalation clause in under two minutes from a simple prompt: ‘Draft a rise-and-fall clause for a construction subcontract in Victoria, Australia, referencing CPI, diesel fuel index, and Fair Work minimum wage movements.’ The result is not a legal document — your accountant or solicitor should review it once — but it gives you a professional working framework to customise and include with every future quote. With 15 days until July 1, this week is exactly the right time to build that clause into your standard quote template before the cost shock lands.",

    # Fun Facts
    "{{FACT_1}}": "Playing a musical instrument in later life measurably slows brain ageing. A four-year study of older adults found that those who continued practising an instrument maintained their memory performance and showed significantly less age-related brain shrinkage compared to those who had stopped playing. The effect was consistent across multiple instruments and musical backgrounds. Musical engagement is emerging as one of the most effective cognitive protection tools available to older adults — and it appears the key variable is active practice, not passive listening.",

    "{{FACT_2}}": "MetLife Stadium in East Rutherford, New Jersey — host of the 2026 FIFA World Cup Final on July 19 — is the only stadium in the NFL where two rival teams permanently share the same venue as their home ground. The New York Giants and New York Jets both call MetLife home, yet the stadium carries neither team's name. When the venue opened in 2010, the two clubs failed to agree on a shared naming compromise, resulting in the building being sold to corporate sponsors while both teams play their home schedules there. At 82,500 capacity, it is also the largest venue in the 2026 World Cup.",

    "{{FACT_3}}": "Standard computer mice were originally called \"X-Y Position Indicators for a Display System\" when Douglas Engelbart invented the device at Stanford Research Institute in 1964. The nickname \"mouse\" was informal engineering shorthand — the cord trailing from the back resembled a tail — and stuck so completely that Engelbart himself began using it in formal documentation. The world's first public demonstration of a computer mouse, along with video conferencing, hypertext, and collaborative real-time editing, occurred at what became known as \"The Mother of All Demos\" in San Francisco on December 9, 1968.",

    # Joke
    "{{JOKE_SETUP}}": "Why do irrigation contractors never stress about Monday mornings?",
    "{{JOKE_PUNCHLINE}}": "They set everything up to run automatically over the weekend.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Believe you can and you’re halfway there.”",
    "{{CLOSING_ATTR}}": "— Theodore Roosevelt",
    "{{CLOSING_MESSAGE}}": "The week starts on a high — the Socceroos put in one of their best World Cup performances in years yesterday, and the Strait of Hormuz could reopen before the week is out if the Iran deal closes, which would be the most welcome news for diesel prices since April. Monday opens with fog on the Mornington Peninsula, clearing to a partly cloudy 17°C today before rain arrives from Tuesday through Thursday — so anything worth doing outside is worth front-loading this morning. The RBA decision lands tomorrow at 2:30pm AEST: hold is expected, but the language matters for anyone carrying variable-rate debt. Fifteen days to EOFY and the fuel excise expiry, Liall — the week to act is this one.",
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
