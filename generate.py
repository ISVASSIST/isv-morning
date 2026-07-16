#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 17 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 17 Jul (BOM)
    "{{WEATHER_1}}": "FRI 17 · ☁️🌧️ Cloudy, shower or two · 8–15°C",
    "{{WEATHER_2}}": "SAT 18 · 🌫️🌦️ Morning fog, shower developing · 8–14°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "SUN 19 · 🌫️☀️ Morning fog, then sunny · 6–14°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "MON 20 · ❄️🌫️☀️ Frost & fog patches, mostly sunny · 5–14°C",
    "{{WEATHER_5}}": "TUE 21 · 🌦️ Shower or two, cooler · 6–12°C",
    "{{WEATHER_ALERT}}": "⚠ FROST & FOG PATCHES MON MORNING · NO SEVERE WARNINGS ACTIVE",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷⚓ STRAIT OF HORMUZ · US STRIKES CONTINUE FIFTH DAY · TANKER HIT NEAR EXPORT TERMINAL",
    "{{WORLD_1_HEADLINE}}": "US Strikes Iran for a Fifth Straight Day, Hits Tanker Trying to Skirt Blockade",
    "{{WORLD_1_SUMMARY}}": "US forces struck Iranian military targets for a fifth consecutive night and hit a sanctioned oil tanker attempting to evade the naval blockade near Iran's main export terminal. Iran has fired on US bases in Kuwait and Jordan in response, its health ministry says at least 35 people have been killed and over 300 injured in the latest strikes, and India has now barred its seafarers from sailing through the Strait of Hormuz altogether. A regional ceasefire agreed in April unravelled within weeks, and talks over the strait's long-term administration remain stalled.",
    "{{WORLD_1_URL}}": "https://www.cnn.com/2026/07/16/world/live-news/iran-war-trump",

    "{{WORLD_2_FLAG}}": "🇬🇧🏛️ WESTMINSTER · LABOUR LEADERSHIP CONTEST CLOSES · BURNHAM SET TO BE PM BY TOMORROW",
    "{{WORLD_2_HEADLINE}}": "Andy Burnham Set to Become UK's Seventh PM in a Decade as Leadership Contest Closes",
    "{{WORLD_2_SUMMARY}}": "Nominations for the UK Labour leadership closed today with Andy Burnham the only candidate to secure enough support, meaning the former Greater Manchester mayor could be sworn in as prime minister as early as tomorrow. He inherits the job after Keir Starmer's resignation last month, becoming Britain's seventh PM in ten years — a turnover rate not seen in nearly two centuries.",
    "{{WORLD_2_URL}}": "https://www.pbs.org/newshour/world/andy-burnham-prepares-for-a-uk-labour-leadership-contest-that-may-be-a-coronation",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ AT THE BOWSER · EXCISE RELIEF HALVED · PRICES CLIMBING ACROSS EVERY CAPITAL",
    "{{ECON_1_HEADLINE}}": "Petrol Prices Jump as Fuel Excise Discount Is Halved and Middle East Conflict Drags On",
    "{{ECON_1_SUMMARY}}": "The federal government's temporary fuel excise cut dropped from 32 cents to 16 cents a litre on July 1, and combined with the ongoing Iran conflict it's pushed capital-city unleaded to a national average of 170.1 cents a litre and diesel to 191.9 cents — both up sharply on last month. The relief scheme is due to expire August 2, and with Brent still sitting near US$85 a barrel, there's little sign of the bowser easing off before then.",
    "{{ECON_1_URL}}": "https://www.ibtimes.com.au/rising-petrol-prices-australia-causes-consumer-tips-1872184",

    "{{ECON_2_FLAG}}": "💱 CURRENCY · AUD NEAR 3-MONTH LOW · SAFE-HAVEN DEMAND FROM HORMUZ CRISIS",
    "{{ECON_2_HEADLINE}}": "Australian Dollar Slides Near Three-Month Lows as Middle East Tensions Boost the Greenback",
    "{{ECON_2_SUMMARY}}": "The Aussie dollar has been grinding lower against the US dollar this week as the Strait of Hormuz standoff drives money into safe-haven currencies, with Trump's reinstated naval blockade and talk of a 20% 'security levy' on cargo transiting the strait adding to the uncertainty. A weaker dollar makes imported tools, materials and equipment more expensive just as fuel costs are already climbing — a double hit worth factoring into any big purchases this quarter.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · GEMINI 3.5 PRO LAUNCHES TODAY · GOOGLE'S BIGGEST MODEL YET",
    "{{TECH_1_HEADLINE}}": "Google's Gemini 3.5 Pro Goes Live Today With a Reported 2-Million-Token Context Window",
    "{{TECH_1_SUMMARY}}": "Google DeepMind's next flagship model is set for general release today after a ground-up architectural rebuild, reportedly bringing a 2-million-token context window and a new 'Deep Think' reasoning mode. It lands the same week Shanghai's World AI Conference opens with Xi Jinping attending in person — a reminder of just how fast the ground is shifting under every AI tool your business already relies on.",
    "{{TECH_1_URL}}": "https://www.techtimes.com/articles/320308/20260713/gemini-35-pro-targets-july-17-after-full-rebuild-every-spec-remains-unconfirmed.htm",

    "{{TECH_2_FLAG}}": "💼 AI IMPLEMENTATION · ANTHROPIC & BLACKSTONE · $1.5B BET ON 'DOING', NOT JUST BUILDING",
    "{{TECH_2_HEADLINE}}": "Anthropic and Blackstone Launch $1.5B Venture Betting the Real AI Money Is in Implementation",
    "{{TECH_2_SUMMARY}}": "Anthropic has teamed up with Blackstone, Goldman Sachs and other major investors to launch a $1.5 billion venture called Ode with Anthropic, built entirely around helping businesses actually deploy AI rather than just build the models. It's a signal from the top of the industry that the next big opportunity isn't a smarter chatbot — it's the unglamorous work of getting existing tools properly wired into how a business actually runs, which is exactly the gap most small operators are sitting in right now.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇨🇳🦾 FACTORY FLOOR · XIAOMI HUMANOID · 98% SUCCESS RATE ON PRODUCTION LINE",
    "{{ROBOT_1_HEADLINE}}": "Xiaomi's Humanoid Robot Hits 98% Success Sorting Parts on a Live Car Production Line",
    "{{ROBOT_1_SUMMARY}}": "Xiaomi CEO Lei Jun shared uncut footage of the company's humanoid robot continuously sorting centre console side covers on an EV assembly line, with the company reporting a 98% task success rate in testing. Xiaomi hasn't set a commercial launch date but says it plans to deploy 'a large number' of the robots across its own factories within five years — another data point in just how fast humanoid robots are moving from lab demos to actual repetitive shift work.",
    "{{ROBOT_1_URL}}": "https://technode.com/2026/07/15/xiaomi-updates-progress-on-humanoid-robots-in-auto-factory-achieves-98-success-rate-in-some-tasks/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Landmark Aboriginal Land Deal Protects an Area Two-Thirds the Size of Tasmania",
    "{{AUS_1_SUMMARY}}": "A new Indigenous Protected Area covering more than 47,000 square kilometres of the Simpson Desert has been signed with Traditional Owners at the remote Uluperte homelands in the NT's southeast, managed by the Central Land Council. The deal pushes a quarter of Australia's landmass under some form of conservation agreement, meeting a major national environmental target, with traditional custodians saying it will help protect sacred sites and manage fire and feral animals.",
    "{{AUS_1_URL}}": "https://www.newcastleherald.com.au/story/9311611/aboriginal-conservation-deal-boosts-environmental-goals/",

    "{{AUS_2_HEADLINE}}": "Cyberattack on Major GP Network Exposes Medical Records of Patients Across Three Cities",
    "{{AUS_2_SUMMARY}}": "Partnered Health, which runs more than 60 medical and skin cancer clinics including sites in Sydney, Melbourne and Canberra, has confirmed a data breach at 21 of its clinics exposing patient names, Medicare numbers, and consultation and treatment records. The group has gone to the NSW Supreme Court seeking an injunction to stop the stolen data being used or published — a reminder that any business holding customer records, tradies included, is a target worth locking down properly.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria Set to Scrap Group Voting Tickets Before November's State Election",
    "{{VIC_1_SUMMARY}}": "The Allan government has introduced legislation to abolish group voting tickets for the Legislative Council, ending the practice that let so-called 'preference whisperers' broker preference deals behind closed doors. Victoria was the last state still using the system — from November's election, upper house voters will number their own preferences above the line instead.",

    # Science
    "{{SCI_1_FLAG}}": "🔬 SKIN SCIENCE · HIDDEN COLLAGEN DAMAGE · CAUGHT BEFORE IT'S VISIBLE",
    "{{SCI_1_HEADLINE}}": "New Optical Scanner Spots Skin Damage Years Before Wrinkles Ever Show",
    "{{SCI_1_SUMMARY}}": "Researchers at Hiroshima University have combined advanced optical imaging with chiroptical spectroscopy to detect collagen breaking down at a molecular level — long before any visible signs of skin damage appear under a standard microscope. The technique picks up the earliest stage of deterioration, when collagen's internal twisted structure starts to unravel, well before the fibres themselves visibly break apart — a find with obvious spin-off potential for anyone whose job means a lot of UV exposure.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "A Health Network Just Got Hacked — Is Your Client List Any Safer?",
    "{{INSIGHT_BODY}}": "Partnered Health's breach this week exposed the personal and medical details of patients across 21 clinics — a reminder that any business sitting on a folder of customer names, addresses and payment details is a target, not just big corporates. Most small trades operators keep quotes, invoices and site photos scattered across emails, a phone and maybe a shared drive, often with no real access control. AI-powered job management tools can actually tighten this up rather than add risk: centralising client records behind a single login, flagging unusual access, and making it trivial to see exactly who touched what and when. It won't stop every attack, but it closes the easiest door — the one where 'security' is just hoping nobody looks.",

    # Fun Facts
    "{{FACT_1}}": "The modern spray gun traces back to a paint sprayer patented by Joseph Binks in 1887, built to whitewash the cavernous interior of the Chicago Board of Trade Building overnight — the same compressed-air mechanism still powers airless sprayers on job sites today.",

    "{{FACT_2}}": "Kangaroos and emus can't walk backwards, which is part of the reason both appear on Australia's coat of arms — chosen to represent a nation that only ever moves forward.",

    "{{FACT_3}}": "The word 'freelance' originally meant a mercenary knight — literally a 'free lance' available for hire — and wasn't used in its modern sense until Sir Walter Scott coined it figuratively in his 1820 novel Ivanhoe.",

    # Joke
    "{{JOKE_SETUP}}": "A tradie's bookkeeper asked if his customer database was properly backed up and password protected.",
    "{{JOKE_PUNCHLINE}}": "He said, 'Course it is — it's in a manila folder, and nobody's ever going to guess THAT password.'",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The men who have succeeded are men who have chosen one line and stuck to it.\"",
    "{{CLOSING_ATTR}}": "— Andrew Carnegie",
    "{{CLOSING_MESSAGE}}": "It's a cool, showery start to Friday in Carrum Downs, 8-15°C with a shower or two easing later — a decent window to knock over outdoor jobs before the fog and frost roll back in over the weekend. Fuel excise relief just got halved and Brent's still sitting near US$85, so if you haven't updated your surcharge line since June, today's the day — and if Gemini 3.5 Pro actually drops as promised, it's worth five minutes over your coffee to see what's changed.",
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
