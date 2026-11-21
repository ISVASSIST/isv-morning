#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Sunday, 22 November 2026',
'{{WEATHER_1}}': 'SUN 22 NOV · ⛈️ Hot and windy, 16-31°C, then afternoon and evening storms, possibly severe',
'{{WEATHER_2}}': 'MON 23 NOV · 🌦️ Cooler, about 21-23°C, chance of a morning storm or shower',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'TUE 24 NOV · 🌧️ Cool and showery, about 16-18°C, the coldest day of the week',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'WED 25 NOV · ☀️ Sunny, cold start near 9°C, top of about 25°C',
'{{WEATHER_5}}': 'THU 26 NOV · 🌤️ Mostly fine and warm, about 24-26°C',
'{{WEATHER_ALERT}}': "Today is the day to watch. The BoM forecast for Melbourne has Sunday reaching about 31°C on strong northerly winds, then a cold front bringing a 90% chance of showers and thunderstorms in the late afternoon and evening. Those storms could be severe, with damaging winds and large hail, and the Bureau has flagged damaging winds for parts of Victoria as the front moves through. Rain totals are only 1 to 10mm, so wind and hail are the bigger risk. Tie down or bring in anything loose in the yard before lunch, and check the BoM warnings page this morning. Monday and Tuesday are much cooler, with Tuesday topping out at only about 17°C. Wednesday and Thursday warm back up to the mid-20s with mostly fine weather, which makes them the best days this week for outdoor coating work.",
'{{WORLD_1_FLAG}}': '🇫🇮 FINLAND · BALTIC SEA',
'{{WORLD_1_HEADLINE}}': 'Drone Strike Sets a Russian Cargo Ship on Fire in the Gulf of Finland',
'{{WORLD_1_SUMMARY}}': "Finland says a drone attack hit a Russian cargo ship in international waters in the eastern Gulf of Finland on Saturday. The ship, the Sparta II, caught fire and drifted toward Finnish waters before anchoring, and its crew was evacuated. Finland told NATO straight away and put temporary air and sea restrictions over the area. It also says a Russian helicopter may have entered Finnish airspace while responding. A Russian regional governor said two drones hit the Kaliningrad-bound ship. Nobody has officially claimed the attack. The ship is under Ukrainian and US sanctions.",
'{{WORLD_1_URL}}': 'https://www.france24.com/en/europe/20261121-drone-attack-sets-russian-cargo-ship-ablaze-in-gulf-of-finland',
'{{WORLD_2_FLAG}}': '🌍 TURKEY · COP31',
'{{WORLD_2_HEADLINE}}': 'Climate Talks Run Into Overtime After Fossil Fuels Are Dropped From the Draft Deal',
'{{WORLD_2_SUMMARY}}': "The COP31 climate summit in Antalya, Turkey, was meant to finish on Friday but ran into Saturday without a final agreement. The main fight is over fossil fuels. The latest draft removed every mention of them, including the COP28 wording about \"transitioning away\" from coal, oil and gas. Panama said it would formally object to any deal without that language, and a bloc of countries from Europe, Africa, Latin America and the Pacific is pushing for it to go back in. Turkey, as host, argues that electrification already implies moving away from fossil fuels. Climate finance is the other big sticking point.",
'{{WORLD_2_URL}}': 'https://www.pbs.org/newshour/world/climate-talks-in-overtime-as-nations-wrestle-with-response-to-worsening-global-warming',
'{{ECON_1_FLAG}}': '⛽ FUEL',
'{{ECON_1_HEADLINE}}': 'Melbourne Wholesale Diesel Keeps Sliding, Down to About 243 Cents',
'{{ECON_1_SUMMARY}}': "The Australian Institute of Petroleum's terminal gate prices show wholesale diesel in Melbourne at about 242.9 cents a litre on Friday 20 November, down from 247.1 cents on Monday. Wholesale prices were forecast to ease every day this week. That's the price servos pay before their margin, so pump prices usually follow a few days later. The ACCC says diesel doesn't follow the regular weekly price cycle that petrol does, so the drop should come through gradually. If you're filling up the work vehicles this week, it may pay to top up rather than fill, and watch for a cheaper price later in the week.",
'{{ECON_1_URL}}': 'https://aip.com.au/pricing/terminal-gate-prices/',
'{{ECON_2_FLAG}}': '🛍️ RETAIL',
'{{ECON_2_HEADLINE}}': 'Nearly 1,700 David Jones Staff Handed Redundancy Notices Before Christmas',
'{{ECON_2_SUMMARY}}': "David Jones served redundancy notices on 1,689 employees on Friday. Their jobs will end on 30 December. The department store chain went into voluntary administration earlier this month and is closing 19 of its 38 stores across Australia and New Zealand. Only about 10% of affected staff are expected to get redeployment offers. The SDA union says casual staff don't get redundancy pay, and permanent staff may have to wait until the administration ends. For small businesses that supply or service big retailers, it's a reminder to keep a close eye on what you're owed when a customer goes into administration.",
'{{TECH_1_FLAG}}': '🧮 AI · MATHS',
'{{TECH_1_HEADLINE}}': 'Anthropic Researcher Says He and Claude Have Proved the Riemann Hypothesis',
'{{TECH_1_SUMMARY}}': "Levent Alpöge, a mathematician at Anthropic, says he used the Claude AI to produce a proof of the Riemann hypothesis, a famous maths problem first posed in 1859 that carries a US$1 million prize. He has released a four-page note and a version written in Lean, a computer language that lets other experts check the proof step by step. He hasn't published a full written argument yet, and he says it would be extremely long. The claim hasn't been verified. Cornell mathematician Steven Strogatz said, \"If it holds up, it's an extremely big deal.\" Either way, it shows how far AI tools have come on hard, careful reasoning.",
'{{TECH_1_URL}}': 'https://phys.org/news/2026-11-anthropic-claude-math-greatest-riddle.html',
'{{TECH_2_FLAG}}': '🎨 AI · TOOLS',
'{{TECH_2_HEADLINE}}': 'Canva Adds a Switch to Turn Off Its Generative AI Features',
'{{TECH_2_SUMMARY}}': "Canva now lets Free and Pro users turn off its generative AI tools. Go to Settings, then Permissions, and switch off \"Enable generative AI features\". That disables tools like Magic Write, Magic Design and Magic Expand. Everyday helpers like the Background Remover stay on. A separate setting cuts down how many AI-generated templates and images show up in search. On Teams and Business accounts, the admin controls it. AI stays on by default, so nothing changes unless you turn it off. It's handy if you want flyers and quote templates built only from your own photos and logos.",
'{{ROBOT_1_FLAG}}': '🏭 AUTOMATION',
'{{ROBOT_1_HEADLINE}}': 'GM Reportedly Targets 20% More Factory Automation by 2028',
'{{ROBOT_1_SUMMARY}}': "General Motors is reportedly aiming to increase robotics and automation in its factories by about 20% by 2028, citing rising factory and manufacturing costs, according to Reuters reporting covered by Robotics 24/7. GM is also building and integrating its own robots at its plant in Kokomo, Indiana, which makes car electronics such as engine control modules. GM hasn't confirmed the target publicly. It's another sign that big manufacturers are turning to robots because labour and production costs keep rising, not only to chase new technology.",
'{{ROBOT_1_URL}}': 'https://robotics247.com/article/gm-targets-20-increase-in-robotics-and-factory-automation-by-2028',
'{{AUS_1_HEADLINE}}': 'Top End Shaken as a Magnitude 6.8 Earthquake Hits East Timor',
'{{AUS_1_SUMMARY}}': "A magnitude 6.8 earthquake struck about 100km north-east of Lospalos in East Timor at about 7:15pm Darwin time on Saturday. It was about 130 to 140km deep. People across Darwin, Katherine and other parts of the Top End felt it, and some Darwin residents said it was the strongest shaking they'd felt in the city. Geoscience Australia received hundreds of felt reports. No damage or injuries had been reported in Australia. It's the second strong quake felt in the Top End this week, after a magnitude 6.6 in the Banda Sea on Tuesday.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-21/top-end-nt-shaken-as-major-earthquake-hits-east-timor/107413134',
'{{AUS_2_HEADLINE}}': 'Cricket Australia Backs Pat Cummins as Test Captain Amid Sandpapergate Fallout',
'{{AUS_2_SUMMARY}}': "The Cricket Australia board has given Pat Cummins its \"unanimous support\" to stay on as men's Test captain. The 2018 ball-tampering scandal in South Africa has come back into the spotlight after Cameron Bancroft published a 4,000-word account and Usman Khawaja suggested more players knew about it than the three who were punished. Interim chair David Boon and chief executive Todd Greenberg met Cummins in Sydney on Friday. Boon said the board \"unequivocally\" rejects any suggestion Cummins' integrity has been compromised. CA has ruled out reopening the 2018 investigation, but will hold an independent forum, which Bancroft and former coach Darren Lehmann have said they'll join.",
'{{VIC_1_HEADLINE}}': 'One Week Out, Experts Tip a Heavy Labor Loss at the State Election',
'{{VIC_1_SUMMARY}}': "Victoria goes to the polls next Saturday, 28 November, and political experts quoted by the ABC expect a heavy defeat for Labor. Some say Premier Ben Carroll, who has held Niddrie for 14 years, could even lose his own seat, which would make him the first sitting premier to do so in about 80 years. Carroll replaced Jacinta Allan earlier this year and says Labor can still win. These are predictions, not results, and campaigns can shift in the final week. Early voting continues through the week if you want to get your vote done before Saturday.",
'{{SCI_1_FLAG}}': '🔋 BATTERIES',
'{{SCI_1_HEADLINE}}': 'Scientists Build a Rechargeable Battery That Uses Vitamin B12',
'{{SCI_1_SUMMARY}}': "Researchers at the University of Córdoba in Spain have built a rechargeable zinc-air battery that uses vitamin B12 as a catalyst. The vitamin isn't the fuel. It helps drive the chemical reactions when the battery charges and discharges, thanks to the cobalt atom at its centre. Because B12 dissolves in water, the team attached it to tiny carbon nanotubes to keep it in place. The prototype lasted up to 250 charge cycles. It's still early lab work, but it shows a cheap, natural molecule could one day replace expensive metals in batteries. ScienceDaily covered the study on 20 November.",
'{{INSIGHT_TITLE}}': 'After a Storm, Let AI Turn Your Damage Photos Into a Claim-Ready Report',
'{{INSIGHT_BODY}}': "If today's storms do any damage to the shed, the yard or a job in progress, how quickly you document it can decide how smoothly your insurance claim goes. Before you clean anything up, walk around and take photos and short videos of every bit of damage, with something in the shot for scale. Then upload them to ChatGPT, Claude or Gemini and ask it to write a damage report: a list of each item, where it is, what's wrong with it, and the date and time it happened. Add the BoM warning for the day and ask it to draft a short, factual email to your insurer or broker. Check every detail yourself before you send it, and don't let the AI guess at costs or causes. Keep the original photos in a folder you own.",
'{{FACT_1}}': "Vitamin B12 is the only vitamin with a metal atom at its core: a single atom of cobalt, which is why its chemical name is cobalamin.",
'{{FACT_2}}': "The Riemann hypothesis was first put forward by German mathematician Bernhard Riemann in 1859, and it is one of the seven Millennium Prize Problems, each worth US$1 million.",
'{{FACT_3}}': "The magnitude 6.8 earthquake felt in Darwin on Saturday started about 130 to 140 kilometres underground, which is one reason its shaking spread so far.",
'{{JOKE_SETUP}}': "Why wouldn't the land surveyor predict next Saturday's election result?",
'{{JOKE_PUNCHLINE}}': "He never calls anything until he's checked the levels twice and the margins are pegged.",
'{{CLOSING_QUOTE}}': '"It is not enough to be busy; so are the ants. The question is: what are we busy about?"',
'{{CLOSING_ATTR}}': '— Henry David Thoreau',
'{{CLOSING_MESSAGE}}': "It's Sunday, and it's going to be a hot, windy one before storms roll through this afternoon and evening. Get anything loose in the yard tied down or under cover this morning, then enjoy the rest of the day indoors. Diesel is still easing, the election is six days away, and Wednesday and Thursday look like the best days for outdoor work this week. Have a good Sunday.",
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
