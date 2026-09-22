#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Wednesday, 23 September 2026",

    # Weather — Carrum Downs / Melbourne bayside, 5-day from Wed 23 Sep
    "{{WEATHER_1}}": "WED 23 SEP · ☀️ Sunny, patchy morning frost inland · 8–17°C",
    "{{WEATHER_2}}": "THU 24 SEP · ☀️ Sunny, light winds · 8–21°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "FRI 25 SEP · ☀️ Mostly sunny, warming up · 11–24°C",
    "{{WEATHER_3_CLASS}}": "",
    "{{WEATHER_4}}": "SAT 26 SEP · ⛅ Partly cloudy, slight shower chance · 13–25°C",
    "{{WEATHER_5}}": "SUN 27 SEP · ⛅ Partly cloudy, mild · 14–23°C",
    "{{WEATHER_ALERT}}": "A sharp, clear frost this morning burns off fast — dry and warming steadily through the week to a 25°C Saturday before easing into the weekend.",

    # World
    "{{WORLD_1_FLAG}}": "🇾🇪 YEMEN · HOUTHIS PUSH TO SEIZE STRATEGIC HIGHLANDS AS TRUMP OFFERS NO MILITARY PLEDGE",
    "{{WORLD_1_HEADLINE}}": "Houthis Push to Seize Yemen's Kahboub Highlands, Threatening to Cut the Red Sea Coast Off Completely",
    "{{WORLD_1_SUMMARY}}": "Five Yemeni military sources told Reuters the Iran-aligned Houthis, who seized Yemen's Red Sea coast earlier this month, are now pushing to take the Kahboub Mountains separating that coast from the last government-held areas in the south — Yemen's Saudi-backed president called Trump on Sunday asking for US military help, but two sources say Trump stopped short of any direct pledge of support.",
    "{{WORLD_1_URL}}": "https://www.irishtimes.com/world/middle-east/2026/09/21/houthis-try-to-seize-control-of-yemen-highlands/",

    "{{WORLD_2_FLAG}}": "🇫🇷 UNITED NATIONS · MACRON USES HIS FINAL UN SPEECH AS FRANCE'S PRESIDENT TO BLAST GAZA DIPLOMACY",
    "{{WORLD_2_HEADLINE}}": "Macron Calls Gaza a 'Spectacle That Shames Us All' in His Last Address to the UN General Assembly",
    "{{WORLD_2_SUMMARY}}": "French President Emmanuel Macron told the UN General Assembly that a declared peace in Gaza has not translated into humanitarian deliveries, calling the disconnect 'a spectacle that shames us all' and criticising rising settler violence in the West Bank, as world leaders gathered in New York for the UN's annual diplomatic week.",
    "{{WORLD_2_URL}}": "https://www.timesofisrael.com/liveblog_entry/at-un-macron-says-gaza-is-a-spectacle-that-shames-us-all",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · ACCC DATA SHOWS DIESEL NOW 91C/L HIGHER THAN BEFORE THE MIDDLE EAST CONFLICT BEGAN",
    "{{ECON_1_HEADLINE}}": "ACCC Confirms Diesel Is Running 91 Cents a Litre Above Pre-War Levels as Houthi Red Sea Gains Keep Oil Elevated",
    "{{ECON_1_SUMMARY}}": "The ACCC's latest weekly fuel price monitoring shows national petrol prices sitting 53 cents a litre higher and diesel 91 cents a litre higher than they were in February, before the Middle East conflict pushed oil above $100 a barrel — with the Houthis' advance toward Yemen's Red Sea coast this week keeping pressure on international benchmarks, it's worth building a bit more buffer into any quote that relies on a full tank or a generator running all day.",
    "{{ECON_1_URL}}": "https://www.accc.gov.au/about-us/publications/weekly-fuel-price-monitoring-update",

    "{{ECON_2_FLAG}}": "📊 RATES WATCH · MARKETS NOW PRICE A 93% CHANCE OF A HIKE, WITH ANZ TIPPING A SECOND MOVE BY CHRISTMAS",
    "{{ECON_2_HEADLINE}}": "ANZ Goes Further Than the Other Big Four, Now Forecasting Two Rate Hikes to 4.85% by Year's End",
    "{{ECON_2_SUMMARY}}": "With markets now pricing a 93% probability of Monday's expected quarter-point rise to 4.60%, ANZ has gone a step further than CBA, NAB and Westpac, factoring in a second hike in November that would take the cash rate to 4.85% by Christmas — governor Michele Bullock's recent comments to a parliamentary committee that upside inflation risks are 'materialising' are exactly the kind of signal that makes it worth locking in finance or fixed pricing sooner rather than later.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "💸 AI PRICING · OPENAI QUIETLY MAKES ITS FLAGSHIP INTELLIGENCE CHEAPER AND MORE ACCESSIBLE",
    "{{TECH_1_HEADLINE}}": "OpenAI Launches GPT-6 Sol and Luna — Same Family as Its Flagship Model, Built to Cost Less to Run",
    "{{TECH_1_SUMMARY}}": "Just over a week after unveiling its most powerful model yet, GPT-6 Astra, OpenAI has released two lighter siblings — Sol and Luna — extending the same GPT-6 generation at a lower price point rather than chasing pure benchmark performance, framing it as making the latest generation of AI 'more efficient and accessible' for everyday use rather than just frontier research.",
    "{{TECH_1_URL}}": "https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/",

    "{{TECH_2_FLAG}}": "🎓 AI SKILLS · OPENAI EXPANDS ITS FREE TRAINING HUB WITH ROLE-BASED COURSES FOR NON-DEVELOPERS TOO",
    "{{TECH_2_HEADLINE}}": "OpenAI Academy Adds Role-Based Courses and Badges Aimed at Business Leaders, Not Just Developers",
    "{{TECH_2_SUMMARY}}": "OpenAI has expanded its free OpenAI Academy training hub with new role-based learning paths for developers, business leaders, educators and students, adding course assessments and badges to its existing 'Apply AI at Work' series — a genuinely no-cost way to get a handle on practical AI skills without wading through developer documentation first.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 PHYSICAL AI · NVIDIA'S LATEST ROBOTICS SOFTWARE STACK IS ALREADY POWERING HUMANOID AND INDUSTRIAL ARMS FROM FOUR ROBOT MAKERS",
    "{{ROBOT_1_HEADLINE}}": "NVIDIA Releases Isaac ROS 5.0, the Toolkit Four Robotics Companies Are Already Using to Build Faster Robots",
    "{{ROBOT_1_SUMMARY}}": "Announced at the ROSCon robotics conference in Toronto, NVIDIA's Isaac ROS 5.0 is a GPU-accelerated software package for the open-source Robot Operating System that companies including Intrinsic, Mentee Robotics, EKUMEN and Flexiv are already using to build and deploy robots faster, adding new 'agentic' workflows that let robots reason about tasks rather than just follow fixed scripted motions.",
    "{{ROBOT_1_URL}}": "https://www.therobotreport.com/isaac-ros-5-0-brings-ai-agents-robotics-development-says-nvidia/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Joins 20 Nations Calling for a UN Body to Keep AI Under Human Control",
    "{{AUS_1_SUMMARY}}": "Australia signed a joint statement with Germany, Canada, South Africa, the UAE and 16 other countries this week calling for mandatory safety testing, independent evaluations and a potential global oversight body for frontier AI models — notably, the US and China, the two countries actually racing to build the most powerful systems, did not join, and are expected to discuss AI directly when Trump and Xi meet at the White House on Thursday.",
    "{{AUS_1_URL}}": "https://www.aljazeera.com/economy/2026/9/22/20-countries-propose-global-oversight-body-to-manage-ai-dangers",

    "{{AUS_2_HEADLINE}}": "ASIC Warns Australia's Private Credit Boom Is Running on Borrowed Time",
    "{{AUS_2_SUMMARY}}": "ASIC commissioner Simone Constant has warned the fast-growing private credit sector that 'the clock is ticking' on poor lending practices, flagging concerns about valuation and disclosure standards in a corner of finance that's ballooned as banks pull back from riskier business lending — a sector many small operators now rely on when a big four bank says no to equipment or vehicle finance.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Twenty New Emergency Beds at the Royal Children's Hospital Sit Empty — No Funding to Staff Them",
    "{{VIC_1_SUMMARY}}": "A $50 million expansion of Victoria's flagship children's hospital is structurally complete, but the 20 new emergency department beds it delivered can't take patients because no funding was allocated to staff them, with the health service now exploring shifting nurses from elsewhere in the hospital — a reminder that a finished build is often the easy half of any big project.",

    # Science
    "{{SCI_1_FLAG}}": "🔥 EXTREMOPHILES · A NEWLY NAMED SPECIES JUST REDREW THE UPPER TEMPERATURE LIMIT FOR COMPLEX LIFE",
    "{{SCI_1_HEADLINE}}": "Scientists Name a 'Fire Amoeba' That Divides Normally at 63°C, Smashing the Previous Heat Record for Complex Life",
    "{{SCI_1_SUMMARY}}": "Researchers who spent three years sampling geothermal streams in California's Cascade Range have named a new species, Incendiamoeba cascadensis, after finding it not just surviving but actively dividing at 63°C — five degrees past the previous known ceiling for any eukaryote, the broad category of organisms with a nucleus that includes everything from amoebas to humans — and recovering even after brief exposure to 70°C.",

    # Business insight
    "{{INSIGHT_TITLE}}": "OpenAI's New Sol and Luna Models Just Made AI Noticeably Cheaper — A Good Moment to Try It If You Haven't",
    "{{INSIGHT_BODY}}": "OpenAI released two new models this week — GPT-6 Sol and Luna — built to be faster and more efficient than its flagship Astra model, extending the same GPT-6 intelligence at a lower running cost. For a business your size that's never needed the most powerful (and most expensive) AI on the market, this is exactly the sweet spot: cheap enough to run through your quoting, scheduling or customer emails every day without the bill creeping up, without you having to know or care which model is doing the work behind the scenes.",

    # Fun facts
    "{{FACT_1}}": "The United Nations General Assembly has held its September leaders' week in the same New York hall since it opened in 1952, with heads of state still speaking from the same green marble rostrum installed then — meaning Macron's Gaza speech this week was delivered from the same podium generations of leaders have used for over seven decades.",
    "{{FACT_2}}": "Until this week, the record for heat tolerance in a eukaryote — any organism with a nucleus, from amoebas to humans — sat at around 60°C; the newly described 'fire amoeba', found in hot springs in California's Cascade Range, pushed that ceiling to 63°C and was seen dividing normally at that temperature, redrawing the line scientists use to define the upper limit of complex life.",
    "{{FACT_3}}": "The Reserve Bank of Australia has only set policy through a single published 'cash rate target' since 1990 — before that it leaned on direct controls over how much banks could lend rather than one headline number the whole country watches, which is part of why Monday's expected move to 4.60% gets so much more airtime than similar tightening cycles once did.",

    # Joke
    "{{JOKE_SETUP}}": "A locksmith was asked how his small business always managed to start a job on time, even when a client lost the only key an hour before the appointment.",
    "{{JOKE_PUNCHLINE}}": "He said he'd never been late once — he just let himself in.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The best time to plant a tree was 20 years ago. The second best time is now.\"",
    "{{CLOSING_ATTR}}": "— Chinese Proverb",
    "{{CLOSING_MESSAGE}}": "It's Wednesday, and Carrum Downs wakes up to a sharp, clear frost that burns off fast into a sunny day — good conditions for locking in outdoor coating and blasting work before the weekend's possible showers roll through. With diesel still sitting 91c/L above pre-conflict levels and the RBA all but certain to move on Monday, it's a week to get quotes out the door at today's numbers rather than next week's.",
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
