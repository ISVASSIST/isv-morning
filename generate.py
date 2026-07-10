#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 11 July 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 11 Jul (BOM)
    "{{WEATHER_1}}": "SAT 11 · 🌫️ Patchy fog, mostly dry · 5–14°C",
    "{{WEATHER_2}}": "SUN 12 · ❄️ Frost & fog, sunny arvo · 3–15°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "MON 13 · 🌧️ Showers, windy · 9–14°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 14 · 🌧️ Showers, windy N'ly · 8–15°C",
    "{{WEATHER_5}}": "WED 15 · ⛅ Partly cloudy, cooler · 9–14°C",
    "{{WEATHER_ALERT}}": "⚠ FROST WARNING FOR VICTORIA SUNDAY MORNING · SHOWERS & GUSTY WINDS RETURN MONDAY",

    # World
    "{{WORLD_1_FLAG}}": "🇮🇷🇺🇸 IRAN · US · FRAGILE PAUSE AFTER TWO DAYS OF STRIKES",
    "{{WORLD_1_HEADLINE}}": "US-Iran Fighting Appears to Pause After Two Days of Fresh Strikes, Talks Set to Continue",
    "{{WORLD_1_SUMMARY}}": "After the US hit roughly 170 targets across Iran over 48 hours of renewed strikes, both sides appear to have stepped back from the brink, with President Trump confirming Washington will continue talks with Tehran even as he insists the earlier ceasefire is officially \"over.\" Qatari negotiators have travelled to Iran to help restart diplomacy, with a US official saying strikes were deliberately paced to leave room for a deal.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/07/10/g-s1-132943/up-first-newsletter-iran-us-tps-haitians-syrians-eac-gaza-israel-hamas",

    "{{WORLD_2_FLAG}}": "🇮🇱🇵🇸 GAZA · CEASEFIRE · ISRAEL NOW HOLDS 70% OF TERRITORY",
    "{{WORLD_2_HEADLINE}}": "Nine Months Into Its Ceasefire, Israel Now Controls Nearly 70% of Gaza",
    "{{WORLD_2_SUMMARY}}": "New mapping shows Israeli forces have steadily expanded their zone of control since the October 2025 ceasefire, from around half of Gaza to almost 70% today, with the UN estimating 200 Palestinians killed near the shifting lines since the truce began. President Trump's peace plan, which calls for a full Israeli withdrawal and Hamas disarmament, remains stalled nine months on.",
    "{{WORLD_2_URL}}": "https://www.npr.org/2026/07/10/nx-s1-5887357/israel-gaza-war-trump-ceasefire-military-control",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL WATCH · SMES · 51% NOW CALL FUEL A MAJOR COST STRAIN",
    "{{ECON_1_HEADLINE}}": "Fuel Costs Bite Harder for Australian Small Businesses as Excise Relief Winds Back",
    "{{ECON_1_SUMMARY}}": "MYOB's latest Business Monitor shows 51% of small businesses now cite fuel as a major source of financial strain, more than double the 25% recorded last November, as the government's temporary excise relief steps down from 32c to 16c a litre this month before disappearing entirely from 2 August. Heavy vehicle operators face a further hit as the road user charge partially returns — worth building a bit of buffer into any quote with a ute, van or compressor on the road.",
    "{{ECON_1_URL}}": "https://smbtech.au/news/fuel-cost-concerns-for-australian-smes-as-relief-is-pulled-back/",

    "{{ECON_2_FLAG}}": "📈 ASX · MARKETS · FOUR-DAY SLIDE SNAPPED",
    "{{ECON_2_HEADLINE}}": "ASX 200 Snaps Four-Day Losing Streak, Closing Friday Up 0.5% at 8,806 Points",
    "{{ECON_2_SUMMARY}}": "Australian shares rebounded on Friday as banks and miners rallied behind a stronger Wall Street lead, even as renewed Iran-US strikes kept oil markets jittery. The benchmark still finished the week 0.4% lower overall — a reminder that volatility from the Middle East is filtering through to local portfolios and borrowing costs alike.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 OPENAI · CHATGPT WORK · AGENTS THAT FINISH THE JOB",
    "{{TECH_1_HEADLINE}}": "OpenAI Launches ChatGPT Work, an Agent That Delivers Finished Docs and Spreadsheets, Not Just Chat",
    "{{TECH_1_SUMMARY}}": "OpenAI's new ChatGPT Work agent, powered by the newly public GPT-5.6 model, takes a plain-English goal, gathers the context it needs, and hands back a finished spreadsheet, document or simple web app rather than just a conversation — with Codex now folded into the same desktop app for coding tasks. For a small business it's effectively a first-draft admin assistant: point it at a job note or invoice backlog and let it produce the paperwork while you check the final version.",
    "{{TECH_1_URL}}": "https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026",

    "{{TECH_2_FLAG}}": "⚡ AI MODELS · GROK 4.5 · CHEAPER AND FASTER — NOT ALWAYS RIGHT",
    "{{TECH_2_HEADLINE}}": "Grok 4.5 Lands With a Big Efficiency Claim, But Independent Testers Flag a Hallucination Spike",
    "{{TECH_2_SUMMARY}}": "SpaceXAI's new Grok 4.5 model reportedly uses 60% fewer tokens than rivals to solve the same benchmark tasks, at around 31 cents a task — a genuine cost win for anyone running AI-heavy admin at volume. But independent analysis firm Artificial Analysis also found its hallucination rate more than doubled versus the previous version, a useful reminder to double-check anything AI-generated before it goes out to a client.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🎨 ROBOTICS · COATINGS · NO-CODE PAINT COBOTS ENTER SPRAY BOOTHS",
    "{{ROBOT_1_HEADLINE}}": "No-Code 'Cobot Painter' Brings Explosion-Proof Robotic Spraying to Industrial Paint Booths",
    "{{ROBOT_1_SUMMARY}}": "Hirebotics' new Cobot Painter, built on FANUC's CRX-10iA/L Paint arm, is designed to run in solvent-heavy spray environments with an explosion-proof rating and no robotics programming required — part of a broader wave of eight-degree-of-freedom robotic arms reaching into tighter, more awkward industrial spaces. It's an early sign that robotic coating and finishing work, long considered too fiddly to automate, is starting to become commercially viable.",
    "{{ROBOT_1_URL}}": "https://www.marketscale.com/industries/industrial-iot/physical-ai-converges-on-the-warehouse-floor-five-operational-moves-shaping-industrial-robotics-in-mid-2026",

    # Australia
    "{{AUS_1_HEADLINE}}": "Australia Confirms First Bird Flu Case in a Native (Non-Migratory) Seabird",
    "{{AUS_1_SUMMARY}}": "Agriculture Minister Julie Collins confirmed H5N1 bird flu has been found for the first time in an Australian-born seabird, in the coastal town of Robe in South Australia, rather than a migratory bird — raising concern the virus may now be circulating locally rather than only arriving from overseas. Authorities say there's still no sign of spread into poultry and the risk to human health remains low.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/article/first-case-of-bird-flu-detected-in-local-wildlife/lx38jrhxh",

    "{{AUS_2_HEADLINE}}": "SA Police Rule Out Telstra Outage as Cause of Death, After Senator's Claim Sparked Alarm",
    "{{AUS_2_SUMMARY}}": "South Australian police have confirmed a woman's death this week was not linked to Wednesday's Telstra outage, despite an earlier claim from a Liberal senator that a Triple Zero call had failed to connect — the neighbour's calls for help actually went through on both counts. Communications Minister Anika Wells said it was a relief no deaths were linked to the outage, though the scare underlines how quickly a network failure can spiral into fear for small operators who rely on mobile coverage to run their business.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Tens of Thousands Turn Out for Modi's Docklands Rally as Protesters Gather Outside",
    "{{VIC_1_SUMMARY}}": "Close to 30,000 people packed Docklands Stadium to see Indian PM Narendra Modi appear alongside Anthony Albanese and Premier Jacinta Allan on his third visit to Australia, while two separate protest groups — one over human rights concerns, another far-right — demonstrated outside. Worth allowing extra travel time if you're working anywhere near the Docklands precinct this weekend as the visit wraps up.",

    # Science
    "{{SCI_1_FLAG}}": "🕷️ ZOOLOGY · CONVERGENT EVOLUTION · A SMILEY FACE 7,000 MILES FROM HOME",
    "{{SCI_1_HEADLINE}}": "New 'Happy-Face' Spider Species Found in the Himalayas — 7,000 Miles From Its Only Known Hawaiian Relative",
    "{{SCI_1_SUMMARY}}": "Researchers surveying ants in the mountains of Uttarakhand, India stumbled on a spider bearing the same grinning face pattern as Hawaii's famous happy-face spider, and DNA testing confirmed it evolved the resemblance completely independently rather than being a relative. Both species also turned up on ginger plants an ocean apart, a coincidence scientists say raises fresh questions about how such specific, cartoonish markings evolve twice in unrelated corners of the planet.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "ChatGPT Just Learned to Finish the Job, Not Just Chat About It — Here's What That Means for Your Paperwork",
    "{{INSIGHT_BODY}}": "OpenAI's new ChatGPT Work agent doesn't just answer questions — point it at a goal and it goes away, gathers what it needs, and comes back with a finished spreadsheet, document or simple web page rather than a wall of text to tidy up yourself. For a small trades business that's a genuinely different kind of tool: instead of drafting a quote letter and editing it into shape, you could hand it your job notes and photos and get back something close to client-ready. It won't replace your judgement on pricing or scope, but it can cut the time between finishing a job and getting the paperwork out the door — which is exactly the kind of admin most tradies would rather not be doing at 9pm.",

    # Fun Facts
    "{{FACT_1}}": "The household wrench as we picture it today — with an adjustable jaw — was patented in 1922 by world heavyweight boxing champion Jack Johnson, who filed it under his own name while touring as an entertainer.",

    "{{FACT_2}}": "Carrum Downs takes its name from the Bunurong word 'Karrum Karrum', meaning boomerang — the shape early Kulin peoples saw in the long, curved sweep of sandy coastline visible from Oliver's Hill in Frankston, long before the swampland was drained for farming in the early 1900s.",

    "{{FACT_3}}": "The humble can opener wasn't invented until 1858 — 48 years after the tin can itself. Until then, soldiers and settlers were advised to open cans with a bayonet, a hammer and chisel, or whatever was on hand.",

    # Joke
    "{{JOKE_SETUP}}": "Why did the asphalt contractor never lose his cool on a tricky job?",
    "{{JOKE_PUNCHLINE}}": "He always knew how to smooth things over.",

    # Closing
    "{{CLOSING_QUOTE}}": "\"The only impossible journey is the one you never begin.\"",
    "{{CLOSING_ATTR}}": "— Tony Robbins",
    "{{CLOSING_MESSAGE}}": "It's a foggy, still start to the weekend in Carrum Downs, clearing to a mild top of 14°C with no frost until tomorrow morning — a solid window to get outdoor jobs ticked off before showers and wind return Monday. With the ASX clawing back Friday's losses and Modi's Melbourne visit wrapping up nearby, it's a good quiet Saturday to get ahead before things pick up again next week.",
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
