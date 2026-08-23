#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Monday, 24 August 2026",

    # Weather — Carrum Downs VIC, 5-day from Mon 24 Aug (BOM)
    "{{WEATHER_1}}": "MON 24 · ☁️ Cloudy, showers most likely evening · 6–18°C",
    "{{WEATHER_2}}": "TUE 25 · 🌧️ Cloudy, very high chance of showers · 10–16°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "WED 26 · ☁️ Cloudy, showers most likely morning · 11–17°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "THU 27 · ⛅ Partly cloudy, slight chance of a shower · 10–17°C",
    "{{WEATHER_5}}": "FRI 28 · ⛅ Partly cloudy · 9–17°C",
    "{{WEATHER_ALERT}}": "No severe weather warnings are current for Melbourne metro or Carrum Downs, though a flood watch remains in place for the Ovens and King Rivers in Victoria's north-east. Tuesday is shaping up as the wettest day of the run, with showers building back in from this evening — today's daylight hours and Thursday/Friday are the better dry windows for any outdoor coating or blasting work.",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷 IRAN · TEHRAN DISMISSES 'DESPERATE' NEW U.S. SANCTIONS",
    "{{WORLD_1_HEADLINE}}": "Iran Dismisses Trump's New Sanctions as a Sign of 'Desperation,' Pakistan Sends Army Chief to Mediate",
    "{{WORLD_1_SUMMARY}}": "Iran's foreign minister said Sunday that Washington's looming new sanctions package — described by the US Treasury Secretary as \"the toughest sanctions in history\" — is a sign the US has failed to defeat Tehran militarily and will fail economically too. Pakistan's army chief is due in Tehran today as a mediator, a reminder the Middle East standoff behind this year's oil price swings is still nowhere near resolved.",
    "{{WORLD_1_URL}}": "https://www.nbcnews.com/world/iran/iran-says-desperate-new-sanctions-will-fail-mediator-pakistan-sends-ar-rcna593979",

    "{{WORLD_2_FLAG}}": "🌪️ HAWAII · TROPICAL STORM BEARS DOWN ON BIG ISLAND",
    "{{WORLD_2_HEADLINE}}": "Tropical Storm Moke Threatens Hawaii's Big Island With Up to 15 Inches of Rain",
    "{{WORLD_2_SUMMARY}}": "Hawaii's Big Island is opening shelters and urging residents in flood-prone areas to leave early as Tropical Storm Moke tracks in with forecast rainfall of 5 to 15 inches — just a week after Hurricane Lala's deadly flooding and landslides battered the same island. A stark reminder that back-to-back extreme weather events are becoming the norm, not the exception, in a lot of places right now.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/08/23/nx-s1-5941769/tropical-storm-moke-hawaii",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL · MELBOURNE PRICES SPAN 183c TO 300c TODAY",
    "{{ECON_1_HEADLINE}}": "Melbourne Petrol Prices Range From 183.5c to Over 300c a Litre This Morning",
    "{{ECON_1_SUMMARY}}": "Live pricing across Melbourne's 1,172 stations today shows unleaded ranging from 183.5c/L at the cheapest (Preston) to over 300c/L at the priciest, averaging 201.5c/L — a reminder that shopping around before you fill the ute can be worth $50-plus on a single tank. Tuesday to Thursday is typically the cheapest stretch of Melbourne's price cycle, though the Middle East conflict has been disrupting the usual pattern since February.",
    "{{ECON_1_URL}}": "https://petrolmate.com.au/city/vic/melbourne",

    "{{ECON_2_FLAG}}": "🏦 BANKING · BENDIGO BANK REPORTS AS ASX SLIDES",
    "{{ECON_2_HEADLINE}}": "Bendigo Bank Reports Full-Year Results Today After ASX's Second Straight Losing Week",
    "{{ECON_2_SUMMARY}}": "The ASX 200 closed out Friday down for a second consecutive week, weighed by high oil prices, jittery US bond markets and a sell-off in the big banks tied to housing gloom — with three of the big four already flagging double-digit drops in new home loan applications since May's budget. Bendigo Bank's results today will be watched for whether regional lenders are feeling the same squeeze, worth a glance if you're comparing business finance rates.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "📢 AI ADVERTISING · CHATGPT ADS LAND IN EUROPE TODAY",
    "{{TECH_1_HEADLINE}}": "OpenAI Rolls Out ChatGPT Ads to 31 European Markets Today",
    "{{TECH_1_SUMMARY}}": "OpenAI's ad business — which launched as a US pilot in February and has since rolled out to Australia, the UK, Canada and others — expands to 31 European countries today, six months in. Ads only ever show to Free and Go tier users, never Plus or Pro, and contextual (non-personalised) ads don't require consent under GDPR — a preview of how disclosure and consent rules are likely to keep tightening around AI tools generally, not just chat ads.",
    "{{TECH_1_URL}}": "https://openai.com/index/chatgpt-ads-expands-across-europe/",

    "{{TECH_2_FLAG}}": "💰 AI PRICING · FLAGSHIP MODELS GET CHEAPER AGAIN",
    "{{TECH_2_HEADLINE}}": "OpenAI Cuts Its Flagship Model Price Over 20%, Google Halves Gemini Flash Pricing",
    "{{TECH_2_SUMMARY}}": "OpenAI trimmed benchmark pricing on its top-tier GPT-5.6 Sol model by more than 20% this weekend — the first cut to its flagship since July — while Google's new Gemini 3.7 Flash landed at roughly half the price of its predecessor. Competition between the big AI labs keeps pushing the cost of using these tools down, which is good news if you're paying monthly for an AI assistant to help with quotes or admin.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🏃 HUMANOID ROBOTS · SPRINT WORLD RECORD SET IN BEIJING",
    "{{ROBOT_1_HEADLINE}}": "Chinese Humanoid Robot Beats Usain Bolt's 100m World Record at Beijing Games",
    "{{ROBOT_1_SUMMARY}}": "Tiangong Ultra ran 100 metres in 9.39 seconds at the opening of the second World Humanoid Robot Games in Beijing, beating Bolt's 9.58-second record from 2009 — a huge leap from the same robot's 21.5-second time at last year's inaugural games. Runner-up robot Lightning also beat Bolt's mark at 9.47 seconds, though not every competitor had a clean run — one reportedly crashed hard into the safety barrier at full speed, so even world-record pace still comes with its share of on-the-job stumbles.",
    "{{ROBOT_1_URL}}": "https://www.abc.net.au/news/2026-08-22/the-robot-that-can-beat-usain-bolt/107067592",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Confirms First Bird Flu Case in a Mammal After Fur Seal Found in SA",
    "{{AUS_1_SUMMARY}}": "A long-nosed fur seal found at Beachport on SA's south-east coast has tested positive for H5N1 bird flu, Australia's first confirmed case in a mammal, as authorities also brace for the strain to hit sea lion breeding colonies following mass seabird deaths nearby.",
    "{{AUS_1_URL}}": "https://www.abc.net.au/news/2026-08-23/australias-first-bird-flu-case-in-mammal-confirmed-in-sa/107068380",

    "{{AUS_2_HEADLINE}}": "$17m Robot Upgrade Halves Casual Workforce, Doubles Output at WA Avocado Shed",
    "{{AUS_2_SUMMARY}}": "One of WA's largest avocado packing sheds has installed nine Japanese-made robots at its Manjimup facility, cutting its casual workforce roughly in half while doubling output — driven by high labour costs and uncertainty over overseas worker schemes rather than any grand automation strategy.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Can the Coalition Really Win Government Back at November's Victorian Election?",
    "{{VIC_1_SUMMARY}}": "With the poll now under 100 days away, the Coalition under Jess Wilson is optimistic about retaking government, while new Premier Ben Carroll's Labor is bracing to lose traditionally safe western and north-western Melbourne seats like Sunbury, Sydenham, Melton and Yan Yean to One Nation or the Coalition.",

    # Science
    "{{SCI_1_FLAG}}": "🕳️ ASTROPHYSICS · WHY SOME STARS KEEP SURVIVING BLACK HOLES",
    "{{SCI_1_HEADLINE}}": "Astronomers Find Stars That Keep Surviving Repeated Brushes With Supermassive Black Holes",
    "{{SCI_1_SUMMARY}}": "Some stars orbit so close to supermassive black holes that they get partially torn apart on every pass, producing a flare of light each time — and researchers now think stars that were already spinning extremely fast before capture explain both how they got trapped in such tight orbits and why those repeat flares mysteriously fade a little more with each pass.",

    # Business insight
    "{{INSIGHT_TITLE}}": "The Big Four Are Fighting for Loans Again — What a New 'Mortgage War' Means for Your Equipment Finance",
    "{{INSIGHT_BODY}}": "NAB, ANZ, Westpac and CommBank have all reported sharp pull-backs in new home loan applications since May's federal budget — down as much as 20% at Westpac — and banking analysts are calling it the start of a fresh 'mortgage war' as lenders compete harder to keep volumes up. That same competitive pressure typically flows through to business and equipment finance within a few months, as banks look for growth wherever they can find it. If your ute, compressor or blast pot finance is coming up for renewal, or you've been sitting on the same commercial loan rate for a couple of years, this is a reasonable window to ask an AI-assisted comparison tool (or your broker) to run the numbers again — a rate that looked competitive in a tighter lending market may not be the best on offer once the banks start chasing business again.",

    # Fun facts
    "{{FACT_1}}": "The Sony PlayStation 2 has sold more than 155 million units since its 2000 launch, making it the best-selling games console of all time — more than any single console from any generation since, including today's.",
    "{{FACT_2}}": "Baking soda and baking powder aren't interchangeable: baking powder already contains its own acid, while baking soda needs an acidic ingredient like buttermilk or vinegar to activate — swap one for the other and you can end up with a dense, bitter result.",
    "{{FACT_3}}": "The Sydney Harbour Bridge was held together with more than six million hand-driven rivets — a riveting gang could drive around 700 a shift, each one heated in a coke fire, thrown red-hot through the air, and caught in a cone before it was hammered into place.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the retaining wall builder become such a reliable small business owner?",
    "{{JOKE_PUNCHLINE}}": "He never let anything slide — least of all an unpaid invoice.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"He that will not sail till all dangers are over must never put to sea.\"",
    "{{CLOSING_ATTR}}": "— Thomas Fuller",
    "{{CLOSING_MESSAGE}}": "It's a cloudy start to the week in Carrum Downs with showers building back in this evening, so today's daylight hours are your best bet for anything outdoors before Tuesday turns into the wet day of the run. With the ASX just closing out a second rough week and the big banks jostling harder for loans, it's also a decent Monday to check whether your own finance rates are still competitive — and if you need a break from the numbers, the World Humanoid Robot Games are still running in Beijing through Wednesday.",
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
