#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Sunday, 15 November 2026',
'{{WEATHER_1}}': 'SUN 15 NOV · ⛅ Mostly dry, partly cloudy, about 12-17°C',
'{{WEATHER_2}}': 'MON 16 NOV · 🌦️ Cloudy, a slight chance of an early shower, about 10-16°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'TUE 17 NOV · 🌤️ Partly cloudy, mostly dry, about 9-18°C',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'WED 18 NOV · 🌤️ Partly cloudy and warmer, about 10-20°C',
'{{WEATHER_5}}': 'THU 19 NOV · ⛅ Mild, likely dry, about 11-21°C',
'{{WEATHER_ALERT}}': "Monday might start with a shower, then it should be dry and warming from Tuesday. Wednesday and Thursday look like the best days for outdoor coating. These are Melbourne figures from search summaries of BoM, Weather25 and timeanddate, and they didn't all agree. Friday's not covered, and none of this is a Carrum Downs forecast, so check BoM before booking outdoor work.",
'{{WORLD_1_FLAG}}': '🌏 US · CHINA · RUSSIA',
'{{WORLD_1_HEADLINE}}': 'White House Confirms Trump, Xi and Putin Will Meet in Shenzhen Next Week',
'{{WORLD_1_SUMMARY}}': "The White House said on Friday that Trump will hold a first-ever three-way meeting with Xi Jinping and Vladimir Putin on the sidelines of the APEC summit in Shenzhen, which runs 18-19 November. Officials say nuclear arms reduction and the Iran conflict are the main topics, and they don't expect a formal arms deal. Washington says Ukraine won't be raised by Trump, but a Kremlin aide says Putin plans to raise it.",
'{{WORLD_1_URL}}': 'https://www.euronews.com/2026/11/14/trump-xi-and-putin-to-meet-in-china-white-house-says',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'Turkey and Qatar Sign a Mutual Defence Pact in Istanbul',
'{{WORLD_2_SUMMARY}}': "President Erdogan and Qatar's Emir Sheikh Tamim signed a mutual defence agreement on Friday, one of five deals agreed at the 12th meeting of their High Strategic Committee. It covers expanded joint military exercises, defence-industry cooperation and training. The other deals cover education, consumer protection and conflict resolution. It's not yet clear how the defence commitments would work in practice. The pact comes as the Gulf stays tense over the Iran war and shipping through Hormuz.",
'{{WORLD_2_URL}}': 'https://gulfnews.com/world/mena/us-israel-iran-war-turkey-qatar-sign-defence-pact-as-trump-warns-tehran-hormuz-risks-persist-1.500745854',
'{{ECON_1_FLAG}}': '🛢️ OIL',
'{{ECON_1_HEADLINE}}': 'Brent Closes the Week at US$95.84, Its Second Weekly Fall in a Row',
'{{ECON_1_SUMMARY}}': "Brent crude settled at US$95.84 a barrel on Friday, almost unchanged on the day but down 2.5% for the week, from US$98.32 the Friday before. US crude (WTI) closed at US$88.56. Traders are weighing a growing global supply surplus against continuing risk around Hormuz and the Gulf. If it holds, lower crude should keep easing wholesale diesel over the next few weeks.",
'{{ECON_1_URL}}': 'https://energynow.com/2026/11/oil-prices-fall-for-second-straight-week-as-global-supply-surplus-emerges-wti-closes-at-88-56-brent-at-95-84/',
'{{ECON_2_FLAG}}': '🧾 SMALL BUSINESS',
'{{ECON_2_HEADLINE}}': 'Small Businesses Start Passing On Costs After Rate Rises, Fuel and the Surcharge Ban',
'{{ECON_2_SUMMARY}}': "Reporting updated on 14 November says a fifth interest rate rise, plus the fuel and supply-chain effects of the Middle East war, are pushing smaller operators to lift prices, especially those who were absorbing card fees after the surcharge ban. A Small Flat White tracker found 17% of cafés lifted prices after the ban started on 1 October, by an average of 49 cents. Check whether your quote rates still cover fuel and card fees.",
'{{TECH_1_FLAG}}': '🔐 AI · SECURITY',
'{{TECH_1_HEADLINE}}': 'Notion AI Chat Transcripts Exposed in a Breach at AI Supplier Fireworks',
'{{TECH_1_SUMMARY}}': "Notion says AI chats sent to its supplier Fireworks AI for its Insights feature were exposed in a cyberattack, affecting fewer than 1% of workspaces. Notion has switched off Insights. It's telling affected customers to treat the data as exposed and to change any passwords or keys they pasted into Notion AI. The lesson for any business: whatever you type into an AI tool can pass through other companies' servers.",
'{{TECH_1_URL}}': 'https://www.esecurityplanet.com/threats/news-fireworks-ai-second-breach-notion-chat-transcripts/',
'{{TECH_2_FLAG}}': '💻 TECH · CHIPS',
'{{TECH_2_HEADLINE}}': 'Nvidia Fallout Widens as US Senators Want Jensen Huang to Testify',
'{{TECH_2_SUMMARY}}': "A US Senate committee wants Jensen Huang and Commerce Secretary Howard Lutnick to give evidence, according to AI news roundups on 13 November. South Korea's science minister says Nvidia has confirmed it will still supply the 260,000 GPUs it promised for Korean AI data centres. Reports also name Arm CEO Rene Haas as a possible successor, but nothing about the succession is confirmed. I only saw search summaries and newsletter roundups.",
'{{ROBOT_1_FLAG}}': '🦾 ROBOTICS',
'{{ROBOT_1_HEADLINE}}': 'FF Robotics Says It Needs Around 830 More Robot Sales in Two Months to Hit Its 2026 Target',
'{{ROBOT_1_SUMMARY}}': "Faraday Future's robotics spin-off, FF EAI Robotics (Nasdaq: FFR), reported third-quarter results on 13 November and kept its target of about 2,000 robots shipped in 2026, sold at a positive gross margin per unit. It shipped 817 units to the end of September, then a record 351 in October, for 1,168 in total. That means it needs about 832 more in November and December. It hasn't broken down revenue by robot type.",
'{{ROBOT_1_URL}}': 'https://manilatimes.net/2026/11/13/tmt-newswire/pr-newswire/ff-eai-robotics-ecosystem-ffr-announces-2026-q3-results-with-approximately-23-million-in-cumulative-revenue-for-acquired-robotics-business/2469191',
'{{AUS_1_HEADLINE}}': "Coalition Preferences One Nation Ahead of Labor in Victoria, a Move Analysts Say Could Set a National Precedent",
'{{AUS_1_SUMMARY}}': "Opposition Leader Jess Wilson has confirmed the Victorian Liberals and Nationals will mostly put One Nation ahead of Labor on how-to-vote cards for the 28 November election. Labor, the Greens and the Victorian Socialists will be last by default, with decisions made seat by seat. Wilson has ruled out a formal deal. Labor's Anthony Carbines says Labor will put One Nation last. Coverage says the move could set a precedent for other states and federally.",
'{{AUS_1_URL}}': 'https://www.newcastleherald.com.au/story/9388668/one-nation-preference-deal-could-set-national-precedent/',
'{{AUS_2_HEADLINE}}': 'Carlton and Sydney Win Through to the AFLW Preliminary Finals',
'{{AUS_2_SUMMARY}}': "Carlton beat Hawthorn by five points in Saturday's AFLW semi-final, with Darcy Vescio kicking two goals in their 100th game. Sydney beat Geelong in the other semi-final, putting the Swans into their first preliminary final. The Blues and the Swans now play for spots in the grand final.",
'{{VIC_1_HEADLINE}}': 'Early Voting Opens Wednesday as the Victorian Campaign Enters Its Last Fortnight',
'{{VIC_1_SUMMARY}}': "Early voting centres open across Victoria on Wednesday 18 November, ahead of the 28 November election. Premier Ben Carroll is campaigning on a $30 weekly public transport fare cap, 20 new dental centres and winding back Labor's 2023 land tax increases. Jess Wilson's Coalition has promised to repeal the Treaty within 100 days and to strengthen workplace protection orders. Recent polling has the Coalition in front.",
'{{SCI_1_FLAG}}': '💊 MEDICINE',
'{{SCI_1_HEADLINE}}': 'Stopping Statins After 70 Looks Safe in the Short Term, but Heart Risk Creeps Up Later',
'{{SCI_1_SUMMARY}}': "The STREAM trial followed about 1,900 adults aged 70 and over who took statins only for prevention, with no previous heart attack or stroke. It was published in the New England Journal of Medicine. At two years, stopping was no worse than continuing for heart attacks, strokes or death, and quality of life, muscle pain and falls didn't differ. By four years, though, heart events were a little higher in the group that stopped. The lead author says it doesn't support a general rule to stop. Talk to your GP before changing any medication.",
'{{INSIGHT_TITLE}}': 'Before You Paste Anything Into an AI Tool, Strip Out the Passwords and Bank Details',
'{{INSIGHT_BODY}}': "The Notion breach is a reminder that anything you type into an AI tool can pass through other companies' servers. Make one simple rule for the business: no passwords, bank details, tax file numbers or customer home addresses go into ChatGPT, Claude, Copilot or any other AI tool. Swap them for placeholders like [CUSTOMER] or [SITE] before you paste a quote, email or invoice in. You can even ask the AI to remind you to remove sensitive details first. It takes ten seconds a job, and it means a breach at someone else's company doesn't become your problem.",
'{{FACT_1}}': "Turkey and Qatar signed five agreements at the 12th meeting of their High Strategic Committee in Istanbul, including a mutual defence pact.",
'{{FACT_2}}': "Robot start-up Rhoda AI says its robots can learn a new task from as little as ten hours of remote-control demonstration, after pretraining on hundreds of millions of videos.",
'{{FACT_3}}': "FF EAI Robotics shipped a record 351 robots in October 2026, beating its previous monthly high of 265 set in September.",
'{{JOKE_SETUP}}': "Why did the gasfitter take a proper Sunday off?",
'{{JOKE_PUNCHLINE}}': '"After six days of fixing leaks, he\'d earned the chance to let off some steam."',
'{{CLOSING_QUOTE}}': '"Rest when you\'re weary. Refresh and renew yourself, your body, your mind, your spirit. Then get back to work."',
'{{CLOSING_ATTR}}': '— Ralph Marston',
'{{CLOSING_MESSAGE}}': "It's a mostly dry, mild Sunday, so take a proper break. Oil eased again this week. Early voting opens on Wednesday, and Wednesday and Thursday look like the best coating days of the week. Spend five minutes setting a 'what not to paste into AI' rule for the crew. Enjoy the rest of the weekend.",
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
