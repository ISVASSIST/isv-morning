#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 09 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 9 Jun
    # Cool winter week; showers Wednesday, clearing to fine weekend
    "{{WEATHER_1}}": "TUE 9 · ⛅ Partly Cloudy · 11–15°C",
    "{{WEATHER_2}}": "WED 10 · 🌧 Showers · 12–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 11 · ⛅ Mostly Cloudy · 8–16°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "FRI 12 · 🌤 Clearing · 10–17°C",
    "{{WEATHER_5}}": "SAT 13 · ☀️ Fine · 10–19°C",
    "{{WEATHER_ALERT}}": "⚽ WORLD CUP OPENS THURSDAY",

    # World
    "{{WORLD_1_FLAG}}": "🇵🇭 ASIA-PACIFIC · PHILIPPINES",
    "{{WORLD_1_HEADLINE}}": "Magnitude 7.8 Earthquake Kills at Least 35 in Southern Philippines, Triggering Tsunami",
    "{{WORLD_1_SUMMARY}}": "A powerful offshore earthquake struck Mindanao on Monday, collapsing buildings in General Santos City and triggering a one-metre tsunami that swept coastal communities in Sarangani province. Landslides killed at least 13, bringing the total death toll to 35 with more than 200 injured. Tsunami warnings have been lifted but search and rescue teams continue working through the rubble of the hard-hit south.",
    "{{WORLD_1_URL}}": "https://www.aljazeera.com/news/2026/6/8/tsunami-warnings-issued-after-8-2-magnitude-earthquake-off-philippines",

    "{{WORLD_2_FLAG}}": "🇨🇳 CHINA · NORTH KOREA",
    "{{WORLD_2_HEADLINE}}": "Xi Jinping in Pyongyang for First State Visit in Seven Years — Calls for Deeper Strategic Ties With Kim",
    "{{WORLD_2_SUMMARY}}": "Chinese President Xi Jinping arrived in North Korea on Monday for a two-day state visit — his first trip to Pyongyang since 2019 — calling for 'powerful momentum' in China-North Korea ties. The visit marks the 65th anniversary of their mutual defence treaty, but analysts say Beijing's real objective is reasserting influence over Kim Jong Un as Pyongyang's military alignment with Russia deepens and US-led denuclearisation talks remain stalled.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/2026/6/8/chinas-xi-jinping-arrives-in-north-korea-on-rare-state-visit",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL PRICES · AUS",
    "{{ECON_1_HEADLINE}}": "Fuel Prices Set to Jump 26–29c/L on July 1 as Government Confirms No Excise Extension",
    "{{ECON_1_SUMMARY}}": "The federal government's temporary halving of the fuel excise — which has kept petrol and diesel prices down by 26–29 cents a litre since April 1 — expires June 30 with no extension confirmed despite ongoing Middle East oil supply pressures. From July 1, an 80-litre diesel fill costs roughly $22 more. For trades businesses running vehicle fleets, this arrives on the same date as the Fair Work annual wage adjustment — a combined cost hit that demands immediate repricing before the new financial year.",
    "{{ECON_1_URL}}": "https://www.sbs.com.au/news/article/government-to-reassess-fuel-excise-extension-as-reserves-swell-july-cutoff-nears/ixy1ok945",

    "{{ECON_2_FLAG}}": "🏦 INTEREST RATES · AUS",
    "{{ECON_2_HEADLINE}}": "RBA Decision One Week Away — Markets Split on a Fourth 2026 Rate Rise or Pause at 4.35%",
    "{{ECON_2_SUMMARY}}": "The Reserve Bank meets next Tuesday June 16, with the cash rate at 4.35% after three consecutive hikes this year. Westpac economists predict another 25bp rise; CBA and independent economist Saul Eslake tip a pause as the RBA waits for evidence that inflation is easing. Headline CPI is forecast to peak at 4.8% in the June quarter, keeping variable-rate business lending and equipment finance expensive heading into the new financial year.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🍎 USA · APPLE WWDC 2026",
    "{{TECH_1_HEADLINE}}": "Apple Launches 'Siri AI' at WWDC 2026 — A Rebuilt Conversational Assistant With Agency Across All Your Apps",
    "{{TECH_1_SUMMARY}}": "Apple's WWDC 2026 keynote on Monday unveiled 'Siri AI' — a completely rebuilt Siri capable of multi-turn conversations, real-time web knowledge, and system-wide agency: autonomously changing passwords, pulling context from photos, and acting as an AI agent from the Dynamic Island. iOS 27, macOS Golden Gate, and all platform updates were announced. Public beta arrives July; full release September alongside iPhone 18. For iPhone-using small business operators, a phone-based assistant that can draft, book, and execute tasks without switching apps is arriving this year.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/06/08/apple-wwdc-2026-live-updates.html",

    "{{TECH_2_FLAG}}": "📊 AI MARKET · JUNE 2026",
    "{{TECH_2_HEADLINE}}": "ChatGPT's Market Share Falls to 54.7% as Claude Records 306% Growth in a Single Quarter",
    "{{TECH_2_SUMMARY}}": "The June 2026 Momentic report shows ChatGPT's share of global AI web visits has dropped from 76.5% in early 2025 to 54.7%, while Google Gemini climbs to 27.4% (up 104% in six months) and Claude has grown 306% in a single quarter. The AI assistant market is fragmenting fast — the practical implication for small businesses is to build workflows around tasks, not around a single brand, as the capability gap between the leading tools continues to narrow.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🤖 GLOBAL · HUMANOID MARKET",
    "{{ROBOT_1_HEADLINE}}": "Bank of America: 90,000 Humanoid Robots to Ship in 2026 — Factory Payback Period Now Just Six Months",
    "{{ROBOT_1_SUMMARY}}": "Fresh analysis from KraneShares citing Bank of America data puts global humanoid robot shipments on track for 90,000 units in 2026, rising steeply to 1.2 million per year by 2030. The tipping point: in high-utilisation industrial environments, the investment payback period has already compressed to six months — transforming humanoid robotics from 'strategic experiment' to standard capital expenditure. Factory deployments from Figure AI, Boston Dynamics Atlas, and Chinese manufacturers are now scaling under standing commercial orders, not pilot contracts.",
    "{{ROBOT_1_URL}}": "https://kraneshares.com/humanoid-robotics-in-2026-the-race-from-pilot-to-platform/",

    # Australia
    "{{AUS_1_HEADLINE}}": "World Cup Opens Thursday — Socceroos Face Türkiye in Vancouver on June 14",
    "{{AUS_1_SUMMARY}}": "The 2026 FIFA World Cup begins this Thursday June 11 in Mexico City, with Australia's Socceroos kicking off their Group D campaign against Türkiye in Vancouver on June 14. Coach Tony Popovic's 26-man squad features Mat Ryan and Mathew Leckie heading to a record-equalling fourth World Cup alongside 17 first-timers. Australia also faces co-hosts USA on June 20 and Paraguay June 26 in the 48-team, three-nation tournament — the biggest in history.",
    "{{AUS_1_URL}}": "https://footballaustralia.com.au/news/commbank-socceroos-squad-named-fifa-world-cup-2026tm",

    "{{AUS_2_HEADLINE}}": "Income Tax Rate Drops to 15% on July 1 — But Fuel Excise Snapback Will Offset Much of the Relief",
    "{{AUS_2_SUMMARY}}": "From July 1, the 16% income tax bracket drops to 15% under the 2026-27 federal budget — worth up to $268 annually for eligible workers, with a further cut to 14% from July 2027. For trades business owners, however, the relief lands on the same date as the fuel excise restoration, adding roughly $22–$28 per large tank fill. The $20,000 instant asset write-off for small businesses is now permanent — relevant for equipment purchases in the new financial year.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Sunbury Line Suspended This Saturday and Sunday — Bus Replacements as Metro Tunnel Works Ramp Up",
    "{{VIC_1_SUMMARY}}": "Commuters on the Sunbury train line face full service suspension this Saturday June 13 and Sunday June 14 for Metro Tunnel construction works, with bus replacements operating throughout. A second weekend suspension is planned for June 27–28. Separately, half-price public transport fares remain in place for all Victorian passengers until at least the end of 2026.",

    # Science
    "{{SCI_1_FLAG}}": "🐨 AUSTRALIA · ECOLOGY",
    "{{SCI_1_HEADLINE}}": "South Australia's Koala Boom May End in Mass Starvation — Population Has Outgrown Its Food Supply",
    "{{SCI_1_SUMMARY}}": "South Australia's koala population in the Mount Lofty Ranges has grown to an estimated 22,000–26,000 animals — roughly 10% of Australia's total — in numbers the ecosystem can no longer safely support. Researchers warn that without targeted fertility management, overbrowsing will strip the eucalyptus forests koalas depend on, triggering widespread starvation and habitat collapse. The study recommends sterilising around 22% of adult females annually to hold the population below a sustainable threshold. Published ScienceDaily, 6 June 2026.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "The July 1 Double Hit Is Three Weeks Away — Use AI This Week to Find Out Which Jobs Will Bleed Margin",
    "{{INSIGHT_BODY}}": "In three weeks, two cost increases land on the same date: the annual Fair Work wage adjustment and the full restoration of the 52.6 cents-per-litre fuel excise, which halved in April and will not be extended. For a small trades business with two employees and two work vehicles covering around 1,000 kilometres per week, this combined hit can add $800–$1,200 to monthly outgoings overnight — without a single new cost decision being made. The businesses that absorb this cleanly are already repricing. AI makes the analysis fast: paste your last quarter of job data into Claude or ChatGPT, describe the incoming cost changes, and ask it to identify which job types or service areas will become unprofitable at current rates. Then ask it to draft revised rate cards and a short client note explaining the adjustment. Twenty minutes this week is worth more than a month of margin scrambling in July.",

    # Fun Facts
    "{{FACT_1}}": "When inflation in Germany's Weimar Republic peaked in November 1923, the exchange rate hit 4.2 trillion marks per US dollar — a loaf of bread cost 200 billion marks. Workers were paid twice daily so they could spend wages before afternoon prices rose further, and people carted cash in wheelbarrows to buy groceries. The crisis ended when Germany introduced the Rentenmark, exchanged at one new mark per one trillion old. Economists cite the collapse as a key factor in the political instability that followed through the 1930s.",

    "{{FACT_2}}": "Egg whites foam when whipped because the proteins — ovalbumin and ovomucin — are denatured by the mechanical force and align at the air-water interface, trapping bubbles in a stable structure. A single drop of egg yolk or oil destroys the foam entirely: fat coats the protein ends before they can bond, preventing the structure from forming. This is why pastry chefs are precise about bowl and whisk cleanliness — a trace of fat on the equipment is enough to prevent meringue from forming, no matter how long you whip.",

    "{{FACT_3}}": "The PlayStation was famously rejected by Nintendo before Sony built it themselves. A 1991 deal for a CD-ROM add-on for the Super Nintendo collapsed after Nintendo changed contract terms without warning, leaving Sony with a nearly complete console platform. Sony launched the PlayStation in 1994, and it went on to become the best-selling console brand in history. Over 600 million PlayStation consoles have been sold across all generations — with Nintendo's perceived slight arguably the most commercially costly partnership breakdown in the history of technology.",

    # Joke
    "{{JOKE_SETUP}}": "Asked an AI to help write a quote for a tricky new commercial client.",
    "{{JOKE_PUNCHLINE}}": "It asked: 'Do you want the price that wins the job, the price that makes money, or the special one that tries both?' First time a computer's made me feel genuinely understood.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Act as if what you do makes a difference. It does.”",
    "{{CLOSING_ATTR}}": "— William James",
    "{{CLOSING_MESSAGE}}": "It's a cool Tuesday morning in Carrum Downs — winter proper now, with showers expected Wednesday and a fine weekend coming. Apple's Siri rebuild landed overnight and it looks like the most significant iPhone shift in years. The FIFA World Cup opens Thursday in Mexico City, and the Socceroos kick off five days from now on June 14 — worth setting an alarm. The fuel excise clock is ticking: three weeks to July 1, and the cost structure changes whether the repricing is ready or not. Have a good day, Liall.",
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
