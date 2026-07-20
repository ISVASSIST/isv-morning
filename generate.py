#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Tuesday, 21 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Tue 21 Jul (BOM)
    "{{WEATHER_1}}": "TUE 21 · 🌫️⛅ Morning fog near the hills, partly cloudy · 6–15°C",
    "{{WEATHER_2}}": "WED 22 · 🌦️ Showers likely, possible small hail (SE suburbs) · 7–15°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "THU 23 · 🌦️ Showers likely, hail chance (SE suburbs) · 6–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "FRI 24 · ☁️ Cloudy, medium chance of showers · 6–14°C",
    "{{WEATHER_5}}": "SAT 25 · ⛅ Partly cloudy, shower chance easing · 7–14°C",
    "{{WEATHER_ALERT}}": "⚠ MORNING FOG TODAY · SHOWERS & POSSIBLE HAIL WED–THU · NO SEVERE WARNINGS ACTIVE",

    # World
    "{{WORLD_1_FLAG}}": "🇬🇧 UK POLITICS · SEVENTH PM IN A DECADE · BURNHAM VOWS 'CIRCUIT BREAKER'",
    "{{WORLD_1_HEADLINE}}": "Andy Burnham Becomes Britain's Seventh Prime Minister in a Decade, Pledging a 'Circuit Breaker' for a Country Trump Just Called a 'Poverty-Stricken Disaster'",
    "{{WORLD_1_SUMMARY}}": "King Charles III formally invited the former Greater Manchester mayor to form a government on Monday after Keir Starmer's resignation, making the once-rejected Labour leadership contender the UK's 59th prime minister. In his first speech as PM, Burnham promised to 'regain our stability' and build a 'new political model and a new economic model' for Britain — a tall order given six changes of prime minister in the past decade and a fresh broadside from Donald Trump calling the country a 'poverty-stricken disaster' within hours of the handover.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/07/20/world/live-news/andy-burnham-uk-prime-minister-intl",

    "{{WORLD_2_FLAG}}": "🇮🇷🇺🇸 IRAN WAR · NINTH STRAIGHT NIGHT · KHAMENEI CALLS CEASEFIRE 'WORTHLESS'",
    "{{WORLD_2_HEADLINE}}": "US Completes a Ninth Consecutive Night of Strikes on Iran as Khamenei Declares the Ceasefire Deal 'Worthless and Invalid'",
    "{{WORLD_2_SUMMARY}}": "US Central Command struck Iranian command centres, air defence and coastal surveillance sites, missile and drone facilities and communications networks overnight, the ninth straight night of bombing since the ceasefire memorandum collapsed. Iran's Supreme Leader dismissed Trump's signature on the deal as worthless, while a mediator-floated 10-day pause has so far gone nowhere — no relief yet for the Strait of Hormuz shipping lane that normally carries a fifth of the world's oil.",
    "{{WORLD_2_URL}}": "https://www.aljazeera.com/news/liveblog/2026/7/20/iran-war-live-us-military-carries-out-another-wave-of-strikes-on-iran",

    # Economics
    "{{ECON_1_FLAG}}": "🛢️ OIL & ASX · CRUDE AT 5-WEEK HIGH · ENERGY STOCKS UP, AUD SOFTENS",
    "{{ECON_1_HEADLINE}}": "Crude Oil Steadies Near a Five-Week High as the Iran War Drags On, Pushing ASX Energy Stocks Up and the Aussie Dollar Down",
    "{{ECON_1_SUMMARY}}": "Brent crude held around US$82.50 a barrel on Monday, its highest in five weeks, as the Strait of Hormuz standoff keeps a risk premium baked into every oil price. The ASX 200 Energy Index jumped nearly 2% on the news while the Australian dollar slipped to around 69.8 US cents — a combination that tends to flow through to the bowser here within days, so worth filling up before rather than after the next price cycle turns.",
    "{{ECON_1_URL}}": "https://www.marketindex.com.au/news/asx-200-live-today-monday-20th-july",

    "{{ECON_2_FLAG}}": "⛽ FUEL EXCISE · RELIEF ENDS AUGUST 2 · ANOTHER PRICE JUMP LOOMS",
    "{{ECON_2_HEADLINE}}": "Australia's Temporary Fuel Excise Relief Is Set to Expire on August 2, With Analysts Warning of a Further 40¢-a-Litre Jump at the Bowser",
    "{{ECON_2_SUMMARY}}": "The halved 16-cent excise discount introduced during the Middle East conflict runs out in less than two weeks, and with crude still elevated from the Iran war, analysts are flagging another sharp jump on top of the rises already banked since 1 July — potentially adding upwards of $24 to a 60-litre tank. Fuel reserves are at a record high, which is the one piece of good news, but for a business running utes and compressors on diesel it's worth locking in fuel budgets now rather than after August 2.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🌏 SHANGHAI · WORLD AI CONFERENCE CLOSES · 29-NATION AI BLOC LAUNCHED",
    "{{TECH_1_HEADLINE}}": "China Wraps Up the World AI Conference in Shanghai by Launching a 29-Country AI Cooperation Body, With Xi Jinping Delivering His First-Ever Keynote on the Technology",
    "{{TECH_1_SUMMARY}}": "The four-day World AI Conference in Shanghai closed this week with the formal launch of the World Artificial Intelligence Cooperation Organization, founding-signed by 29 countries including Pakistan, Russia and Kazakhstan and aimed at setting shared rules for AI development outside the US-led frontier labs. It's a reminder that AI governance is now firmly a geopolitical contest, not just a technology race — worth watching for how it eventually shapes which AI tools and data rules end up available here.",
    "{{TECH_1_URL}}": "https://www.aljazeera.com/news/2026/7/17/chinas-xi-jinping-launches-new-ai-alliance-what-is-it",

    "{{TECH_2_FLAG}}": "🇨🇳 OPEN AI MODELS · KIMI K3 TOPS CODING CHARTS · FREE WEIGHTS JULY 27",
    "{{TECH_2_HEADLINE}}": "A Chinese Open-Source Model Just Beat Claude and GPT at Coding, and American Labs Are Publicly Reassessing How Big Their Lead Really Is",
    "{{TECH_2_SUMMARY}}": "Moonshot AI's Kimi K3 — a 2.8-trillion-parameter model and the largest open-weight system released to date — has topped LMArena's Frontend Code leaderboard ahead of Claude and GPT-5.6, with free weights due for public release on July 27. For a business paying by the token for AI tools, the bigger story than the benchmark result is the pattern: genuinely capable open models are now landing within weeks of the best closed ones, and that competition keeps pushing prices for everyday AI tools down.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳🤖 WAIC SHANGHAI · UNITREE'S RIDEABLE 'MECHA' ROBOT · TRANSFORMS MID-STRIDE",
    "{{ROBOT_1_HEADLINE}}": "Unitree Unveils the GD01, a Rideable 500kg Robot That Transforms Between Two Legs and Four Like a Real-Life Transformer",
    "{{ROBOT_1_SUMMARY}}": "Chinese robotics maker Unitree showed off its GD01 at the World AI Conference in Shanghai this week — a 2.7-metre, 500kg piloted machine with an open cockpit that folds its legs and shifts its centre of gravity to switch between bipedal and quadrupedal movement in a few seconds, priced from 3.9 million yuan (about A$830,000) and now in production. It's closer to a manned vehicle than a factory tool for now, but it's a sharp reminder of how fast the physical hardware side of robotics is moving well beyond the warehouse-picking robots doing the actual paid work.",
    "{{ROBOT_1_URL}}": "https://www.globaltimes.cn/page/202607/1365826.shtml",

    # Australia
    "{{AUS_1_HEADLINE}}": "New Report Finds 99% of Asylum Seekers on Nauru Can't Afford Enough Food on Their $260 Fortnightly Allowance",
    "{{AUS_1_SUMMARY}}": "A report titled 'Hungry for Freedom', based on interviews with 78 of the roughly 91 people still living under Australia's regional processing arrangements on Nauru, found 99% couldn't afford enough food and 82% lacked easy access to free, clean drinking water, thirteen years after Australia resumed offshore processing on the island.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/nauru-community-detainees-say-australian-support-impossible-to-live-on/i9ubiu9nk",

    "{{AUS_2_HEADLINE}}": "The Hunter Valley's Coal Capital Is Being Rewired for Batteries as Liddell Power Station's Chimneys Come Down for Good",
    "{{AUS_2_SUMMARY}}": "Muswellbrook's skyline lost its 169-metre coal chimneys to a controlled demolition this year, with a grid-scale battery now rising on the same site and set to switch on within weeks — one of Australia's clearest signs yet that the energy transition has moved from policy to poured concrete.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victorian Liberal MP Moira Deeming Ousted as Candidate After Refusing to Apologise Over a 'Headlock' Allegation Against Matthew Guy",
    "{{VIC_1_SUMMARY}}": "The Liberal Party's state executive has revoked Deeming's preselection for the November state election after she refused to apologise to former leader Matthew Guy, following a Supreme Court challenge she later withdrew and a police review that found no offence had occurred — another distraction for a Coalition currently leading Labor in the polls, four months out from the vote.",

    # Science
    "{{SCI_1_FLAG}}": "💻 PHYSICS · ORDINARY LAPTOP BEATS 'QUANTUM-ONLY' PROBLEM · SUPREMACY CLAIM SHAKEN",
    "{{SCI_1_HEADLINE}}": "An Ordinary Laptop Just Solved a Problem That Was Supposed to Require a Quantum Computer",
    "{{SCI_1_SUMMARY}}": "Physicists at the Flatiron Institute and Boston University compressed the overwhelming wave function of hundreds of entangled qubits using decades-old tensor-network mathematics, letting a conventional computer simulate a quantum system previously held up as proof of 'quantum supremacy' — with results matching both theory and an actual quantum computer's output. It's the second such reversal this year, and a useful reminder that a claimed technological leap isn't always as permanent as the headline made it sound.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "Your Bookkeeping Software Just Became an AI Coworker — What Xero's 'JAX' Means for a One-Person Office",
    "{{INSIGHT_BODY}}": "Xero's AI financial agent, JAX (Just Ask Xero), now plugs straight into Microsoft 365, meaning a business owner can type a plain-English question about cash position, overdue invoices or upcoming BAS liability into a Word or Outlook sidebar and get a straight answer pulled live from the books — no logging into a separate portal, no waiting for the bookkeeper to run a report. For a one-person back office trying to run a trades business off the side of a ute, that's the real value of this wave of AI tools: not a chatbot for chatting, but the numbers finally coming to you instead of the other way around.",

    # Fun Facts
    "{{FACT_1}}": "Bitcoin's pseudonymous creator, Satoshi Nakamoto, mined an estimated 1.1 million bitcoin back in 2009 — worth tens of billions of dollars today — and has never moved a single coin or been identified.",

    "{{FACT_2}}": "Mario wasn't always a plumber — in the original 1981 arcade game Donkey Kong he was a carpenter named 'Jumpman', and only became a plumber two years later when Nintendo gave him his own game, Mario Bros., set in New York's sewers.",

    "{{FACT_3}}": "Onions make you cry because cutting them releases an enzyme that produces a gas called syn-propanethial-S-oxide, which drifts up to your eyes and reacts with moisture to form a mild sulfuric acid — your tears are a defence reflex to flush it back out.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the pest controller's small business always come out on top at tax time?",
    "{{JOKE_PUNCHLINE}}": "Because he was the only tradie in town who'd already found every hidden problem before it cost him a cent.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"It is never too late to be what you might have been.\"",
    "{{CLOSING_ATTR}}": "— George Eliot",
    "{{CLOSING_MESSAGE}}": "Tuesday brings fog near the hills before it burns off to partly cloudy skies in Carrum Downs — 6–15°C — with showers and a chance of small hail moving in from Wednesday, so it's a good day to get outdoor work locked in early. Britain woke up to its seventh prime minister in a decade, the Iran war ground into a ninth night of strikes with oil prices creeping back up, and Victorian state politics served up its own drama with Moira Deeming's preselection axed — a reminder that the news cycle doesn't take a day off, even when the fog hasn't lifted yet.",
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
