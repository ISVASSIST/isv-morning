#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Thursday, 09 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Thu 9 Jul (BOM)
    "{{WEATHER_1}}": "THU 9 · 🌫️ Morning fog & frost patches, clearing to sun · 4–14°C",
    "{{WEATHER_2}}": "FRI 10 · 🌤️ Frosty start, mostly sunny · 5–16°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SAT 11 · 🌧️ Showers building, windy · 8–15°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "SUN 12 · 🌦️ Showers likely · 7–11°C",
    "{{WEATHER_5}}": "MON 13 · 🌦️ Showers likely · 11–13°C",
    "{{WEATHER_ALERT}}": "⚠ FROSTY, FOGGY MORNINGS THU–FRI · GUSTY N'LY WINDS & SHOWERS FROM SATURDAY AFTERNOON",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 US · IRAN · CEASEFIRE COLLAPSES, NATO SUMMIT RATTLED",
    "{{WORLD_1_HEADLINE}}": "Trump Declares the US–Iran Ceasefire \"Over\" After Overnight Strikes, Oil Markets Jolt",
    "{{WORLD_1_SUMMARY}}": "Speaking at the NATO summit in Ankara, President Trump said of the fragile ceasefire \"for me, I think it's over,\" after the US struck dozens of targets along the Iranian coast overnight and Iran said it retaliated against US military sites in Bahrain and Kuwait. Crude oil jumped more than 5% and Wall Street sold off on the news — a reminder that the Strait of Hormuz remains a live risk to global fuel prices even after weeks of relative calm.",
    "{{WORLD_1_URL}}": "https://www.washingtonpost.com/world/2026/07/08/trump-declares-ceasefire-with-iran-has-ended/",

    "{{WORLD_2_FLAG}}": "🥇 OLYMPICS · GEOPOLITICS · IOC LIFTS RUSSIA SUSPENSION",
    "{{WORLD_2_HEADLINE}}": "IOC Provisionally Lifts Its Suspension on the Russian Olympic Committee",
    "{{WORLD_2_SUMMARY}}": "The International Olympic Committee has provisionally reinstated the Russian Olympic Committee, opening a path for Russian athletes to return to full competition from the 2028 Los Angeles Games, though the ban on the Russian flag and anthem remains in place for now. Ukraine has called the move \"premature,\" arguing it rewards Moscow while the war continues.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/07/08/g-s1-132480/russia-olympics-ioc-decision",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ OIL SHOCK · FUEL COSTS · BOWSER RISES TIPPED WITHIN DAYS",
    "{{ECON_1_HEADLINE}}": "Oil Jumps Nearly 6% as Iran Ceasefire Collapse Reignites Fuel Price Risk",
    "{{ECON_1_SUMMARY}}": "Brent crude spiked toward the high US$70s a barrel after the US-Iran ceasefire fell apart, with the Dow shedding over 500 points on the news — and the NRMA is warning Australian bowser prices are likely to start climbing again within 7 to 10 days as the higher global crude price works its way through. Worth watching closely if you're running a fleet of utes, vans or a diesel compressor, since it comes right on top of this month's fuel excise cut stepping down.",
    "{{ECON_1_URL}}": "https://www.barchart.com/story/news/3176179/oil-prices-jump-nearly-6-after-trump-says-ceasefire-with-iran-is-over",

    "{{ECON_2_FLAG}}": "📉 ASX · MARKETS · SHARES PARE LOSSES, DOLLAR SLIPS",
    "{{ECON_2_HEADLINE}}": "ASX Claws Back Early Losses After Sharp Open on Iran Tensions, Aussie Dollar Dips",
    "{{ECON_2_SUMMARY}}": "The ASX200 fell as much as 1.4% in early trade before recovering through the afternoon to close just 0.2% lower at 8,785.1 points, while the Australian dollar edged down to 69.40 US cents, as investors weighed the overnight escalation between the US and Iran against hopes it stays contained. It's a sign markets still expect the disruption to be short-lived — but a jumpy few weeks are likely for anyone watching fuel and import costs.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🇨🇳 AI COSTS · CHINESE MODELS · US LAWMAKERS PROBE ENTERPRISE SHIFT",
    "{{TECH_1_HEADLINE}}": "US Lawmakers Probe Surge in American Companies Running Chinese AI Models",
    "{{TECH_1_SUMMARY}}": "CNBC reports that 30–46% of enterprise AI token usage at US firms now flows through Chinese open-weight models like Zhipu's GLM 5.2 and Moonshot's Kimi, which run 60–90% cheaper than equivalent Anthropic or OpenAI models — Coinbase says switching cut its AI bill in half. The practical takeaway for any business now paying for AI tools: which model sits behind the app is fast becoming as real a cost lever as your electricity provider.",
    "{{TECH_1_URL}}": "https://www.cnbc.com/2026/07/08/chinese-ai-models-probe-us-lawmakers.html",

    "{{TECH_2_FLAG}}": "🤖 OPENAI · GPT-5.6 · CLEARS US GOVERNMENT REVIEW FOR FULL LAUNCH",
    "{{TECH_2_HEADLINE}}": "OpenAI's GPT-5.6 Clears Government Review, Launches Today for General Availability",
    "{{TECH_2_SUMMARY}}": "GPT-5.6 goes from a restricted preview held to roughly 20 government-approved partners to broad public rollout today, after weeks of delay under a new US frontier-AI oversight regime. It's a sign the model was genuinely strong enough to warrant the scrutiny — worth a look if you're using GPT for quoting, admin or customer-facing chat once it's live in your existing plan.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 ROBOTICS · EX-TESLA OPTIMUS SCIENTIST LAUNCHES EUROPEAN HUMANOID",
    "{{ROBOT_1_HEADLINE}}": "Ex-Tesla Optimus Scientist Unveils \"Northstar\", a Lightweight European Humanoid Robot",
    "{{ROBOT_1_SUMMARY}}": "Rémi Cadène, formerly of Tesla's Optimus program, has unveiled Northstar at the Machina Summit — a 40kg humanoid built by his startup UMA that uses \"real-time learning\" to pick up new tasks from demonstration rather than manual programming. Around 50 potential customers in logistics, manufacturing and healthcare are already in talks for pilots — another sign the industry is racing to solve the training-data bottleneck, not just build lighter hardware.",
    "{{ROBOT_1_URL}}": "https://www.bloomberg.com/news/articles/2026-07-07/ex-tesla-scientist-unveils-plans-for-european-humanoid-robot",

    # Australia
    "{{AUS_1_HEADLINE}}": "Nationwide Telstra Outage Halts Trains, Hits Triple Zero Calls and EFTPOS",
    "{{AUS_1_SUMMARY}}": "A network node synchronisation fault knocked out Telstra mobile and internet services nationwide, suspending V/Line regional trains in Victoria, disabling EFTPOS and EV charging terminals in places, and disrupting some Triple Zero emergency calls. It's a blunt reminder of how much everyday business — payments, phones, scheduling — now leans on a single telco network staying up.",
    "{{AUS_1_URL}}": "https://www.theregister.com/networks/2026/07/08/telstra_outage_downs_000_calls_trains_payment_systems/",

    "{{AUS_2_HEADLINE}}": "China Conducts Submarine Ballistic Missile Test Near the Solomon Islands, Australia Objects",
    "{{AUS_2_SUMMARY}}": "China test-fired a submarine-launched ballistic missile that landed in the Pacific between Tonga and Nauru, roughly 1,000km from the Solomon Islands, with Prime Minister Albanese calling it \"a destabilising act\" carried out without advance notice. Japan, New Zealand and Taiwan have echoed the criticism, adding to a tense week of regional military signalling.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "V/Line Trains Stay Suspended Into Thursday Morning After Telstra Outage",
    "{{VIC_1_SUMMARY}}": "Regional train services including the Warrnambool line remain halted this morning after Wednesday's Telstra outage took down the network's signalling communications from about 5am, with V/Line saying services wouldn't resume until at least mid-morning. Worth a heads-up if you've got staff or deliveries relying on regional rail today.",

    # Science
    "{{SCI_1_FLAG}}": "🐝 ECOLOGY · BUMBLEBEES ABSORB FAR MORE TOXIC METAL THAN HONEYBEES",
    "{{SCI_1_HEADLINE}}": "Bumblebees Absorb Up to Seven Times More Toxic Heavy Metal Than Honeybees in the Same Area",
    "{{SCI_1_SUMMARY}}": "University of Cambridge researchers measured arsenic, cadmium, lead and other heavy metals in bees and pollen across Cambridgeshire apiaries and found bumblebees carry far higher contamination than honeybees foraging the same patch — likely because they forage closer to the nest from fewer plant species and their hairier bodies trap more polluted dust. It helps explain why bumblebee colonies are proving more vulnerable to decline than honeybee hives even in identical environments.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "When Telstra Goes Dark, Does Your Business?",
    "{{INSIGHT_BODY}}": "Yesterday's nationwide Telstra outage grounded regional trains, knocked out some Triple Zero calls, and killed EFTPOS terminals for hours — a blunt reminder that even the smartest AI quoting tool, scheduling app or cloud accounting system is only as good as the network sitting underneath it. For a trades business, real resilience isn't about adding more AI — it's a low-tech fallback that still works when the smart tools go quiet: a paper docket book in the ute, an offline day sheet, a backup SIM on a different carrier, a way to take payment that doesn't need a live terminal. The businesses that shrugged off yesterday's outage weren't the most tech-savvy ones — they were the ones who'd tested their fallback before they needed it.",

    # Fun Facts
    "{{FACT_1}}": "The first computer mouse, built in 1964 by Bill English at Stanford Research Institute from Douglas Engelbart's design, was a hand-carved block of pine with two perpendicular metal wheels and one button — it got its name because the trailing cord looked like a tail.",

    "{{FACT_2}}": "Instant ramen was invented after its creator, Momofuku Ando, noticed that hot frying oil drew moisture out of tempura batter — he adapted that dehydration trick to preserve noodles for long storage, launching the first packet of Chikin Ramen in Japan in 1958.",

    "{{FACT_3}}": "Australia's Dingo Fence is the longest fence on Earth at 5,614 kilometres, running from southern Queensland to the Nullarbor cliffs on the Great Australian Bight to keep dingoes off sheep country — more than twice the length of the Great Barrier Reef.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the blacksmith never worry about a slow month?",
    "{{JOKE_PUNCHLINE}}": "He knew how to strike while the iron — and the invoices — were hot.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"There are no secrets to success. It is the result of preparation, hard work, and learning from failure.\"",
    "{{CLOSING_ATTR}}": "— Colin Powell",
    "{{CLOSING_MESSAGE}}": "It's a frosty, foggy start across Carrum Downs this Thursday, clearing to a mild afternoon — dry through Friday before showers and a stiff northerly build in from Saturday, so it's worth getting any exposed prep work done while it's still calm. Keep an eye on the bowser too: with the Iran ceasefire back off and oil already jumping, the NRMA's flagging fuel prices could start climbing again within the week.",
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
