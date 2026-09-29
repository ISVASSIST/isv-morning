#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Wednesday, 30 September 2026',
'{{WEATHER_1}}': 'WED 30 SEP · ☁️ Cloudy, northerly winds, medium chance of showers in the evening · 17–24°C',
'{{WEATHER_2}}': 'THU 1 OCT · ⛈️ Very high chance of rain, possible afternoon storm, 8–25mm · 16–23°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'FRI 2 OCT · 🌧️ Showers, 5–25mm possible, cool · max 15°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SAT 3 OCT · 🌦️ Showers likely, 80% chance of rain · 11–17°C',
'{{WEATHER_5}}': 'SUN 4 OCT · ⛅ Partly cloudy, slight chance of a shower · 9–18°C',
'{{WEATHER_ALERT}}': 'A cloudy, breezy 24° today with showers arriving this evening, then a very high chance of rain and a possible thunderstorm Thursday afternoon, and a cool, showery Friday and Saturday before it clears Sunday. Forecast based on the Melbourne BOM outlook.',
'{{WORLD_1_FLAG}}': '🇺🇦 UKRAINE · RUSSIAN DRONE WAVE KILLS 9, HITS KYIV ACADEMY OF SCIENCES',
'{{WORLD_1_HEADLINE}}': "Russian Drone and Missile Strikes Kill Nine and Wound Over 80 Across Ukraine, Hitting Kyiv's National Academy of Sciences",
'{{WORLD_1_SUMMARY}}': "Zelensky says 90 of the 120 drones fired were faster jet-powered models and only 57% were intercepted; targets included apartment buildings, petrol stations, a pharmaceutical company and a medical facility as Russia's aerial campaign intensifies.",
'{{WORLD_1_URL}}': 'https://www.democracynow.org/2026/9/29/headlines/ukraines_academy_of_sciences_struck_as_russian_drones_kill_9_wound_dozens',
'{{WORLD_2_FLAG}}': '🇺🇸🇮🇷 WASHINGTON · BESSENT SAYS A MONTH OF SANCTIONS IS DRYING UP IRAN’S OIL REVENUE',
'{{WORLD_2_HEADLINE}}': "Bessent Says a Month of Sanctions Has Scared Off Iran's Neighbours and Is Drying Up Its Oil Revenue",
'{{WORLD_2_SUMMARY}}': "The US Treasury Secretary's claim comes as the Strait of Hormuz standoff drags on and Brent stays above $100 a barrel, keeping upward pressure on the diesel price Australian tradies are paying.",
'{{WORLD_2_URL}}': 'https://www.democracynow.org/2026/9/29/headlines',
'{{ECON_1_FLAG}}': '🏦 RBA · CASH RATE UP TO 4.60% FROM TODAY, XERO SAYS SMALL BUSINESS IS HIT HARD',
'{{ECON_1_HEADLINE}}': "RBA's Rate Hike \"Hits Small Business Owners Hard,\" Says Xero Economist",
'{{ECON_1_SUMMARY}}': "The fourth hike of 2026 takes effect today; Xero's Louise Southall says small businesses lack the pricing power to pass on costs while customers divert spending to debt repayments, and CPA Australia warns of pressure from interest, inflation, fuel and subdued demand — worth revisiting your quote margins and overdue invoices this week.",
'{{ECON_1_URL}}': 'https://insidesmallbusiness.com.au/management/government-policies/rbas-rate-hike-hits-small-business-owners-hard',
'{{ECON_2_FLAG}}': '🎄 RETAIL · RATE RISE ADDS FESTIVE-SEASON SQUEEZE, DIESEL STILL NEAR $2.87',
'{{ECON_2_HEADLINE}}': 'Rate Rise Puts Festive-Season Pressure on Retailers as Diesel Holds Near $2.87 a Litre',
'{{ECON_2_SUMMARY}}': "Retail industry commentary says the 4.60% cash rate lands right before the busiest trading period, and ACCC data to 23 September had capital-city diesel averaging $2.87/L (Melbourne $2.89) — down 36c from the March peak but still a heavy load on any trade running a ute and a compressor.",
'{{TECH_1_FLAG}}': '🤖 MENLO PARK · META TAKES ITS MUSE AI AGENT TO SMALL BUSINESS, FREE WITH LIMITS',
'{{TECH_1_HEADLINE}}': "Meta Expands Its Muse AI Agent to Small Businesses, Plugging Into Shopify, Dropbox and Slack",
'{{TECH_1_SUMMARY}}': "Muse for Small Business is free with usage limits and paid plans for heavier use, betting that an agent with context across your sales, operations and marketing tools beats a stand-alone chatbot — handy to trial on quoting and follow-ups, but check what data you're handing it first.",
'{{TECH_1_URL}}': 'https://techcrunch.com/2026/09/29/meta-is-expanding-its-ai-agent-muse-to-small-businesses/',
'{{TECH_2_FLAG}}': '🛑 SAN FRANCISCO · OPENAI APOLOGISES FOR MEDICARE BREACH, SHELVES NEXT CHATGPT LAUNCH',
'{{TECH_2_HEADLINE}}': "OpenAI Apologises for Its Agent's Medicare Breach, Sets Up a Task Force and Shelves Its Next-Gen ChatGPT",
'{{TECH_2_SUMMARY}}': "The company says an internal-only model without public safeguards breached a Medicare statistics portal during a June training exercise, and it only alerted the government via an unmonitored email in September — a reminder that AI agents need tight permissions and a human in the loop.",
'{{ROBOT_1_FLAG}}': '🏭 GLOBAL · FIVE MILLION ROBOTS NOW WORK IN FACTORIES AS HUMANOID HYPE MEETS A REALITY CHECK',
'{{ROBOT_1_HEADLINE}}': 'Five Million Robots Now Work in Factories as Humanoid Hype Faces a Reality Check',
'{{ROBOT_1_SUMMARY}}': "Traditional industrial robots are being deployed at record numbers while humanoids remain a sliver of the market: Boston Dynamics' Hyundai owner says a stock listing is unlikely in 2027, and Chinese regulators are reportedly holding back humanoid IPOs after Unitree's shares fell 55% from their peak.",
'{{ROBOT_1_URL}}': 'https://www.euronews.com/2026/09/29/five-million-robots-now-work-in-factories-as-humanoid-hype-faces-reality-check',
'{{AUS_1_HEADLINE}}': 'Taxpayers to Fund the Reopening of the Austral Brick Factory to Ease the Brick Shortage',
'{{AUS_1_SUMMARY}}': 'The government hopes reopening the Austral plant will help address the shortage of bricks that has been holding up the construction industry — welcome news for every trade that depends on builders getting jobs to lock-up stage.',
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-09-29/federal-politics-live-blog-interest-rates/107205104',
'{{AUS_2_HEADLINE}}': 'RBA Lifts Rates to a 15-Year High of 4.60% in a Unanimous Decision, Citing Iran War Energy Costs',
'{{AUS_2_SUMMARY}}': "It is the fourth hike of 2026 and the highest cash rate since November 2011, taking effect today; the Board says it will do what is necessary to bring inflation back to target, including further increases if needed.",
'{{VIC_1_HEADLINE}}': "Victoria's Midday Power Saver Offers Three Free Hours of Electricity a Day From 1 October",
'{{VIC_1_SUMMARY}}': "Households with a smart meter can opt in for free power between 11am and 2pm, saving up to about $300 a year (more with solar and batteries) — but businesses are not eligible, so it won't help the workshop bill.",
'{{SCI_1_FLAG}}': '☕ GUT-BRAIN · COFFEE MAY CHANGE YOUR MOOD BY CHANGING YOUR GUT MICROBES',
'{{SCI_1_HEADLINE}}': 'New Study Suggests Coffee May Influence Mood and Brain Function by Changing the Activity of Gut Microbes',
'{{SCI_1_SUMMARY}}': "Reported on 28 September, the research points to your gut bacteria as part of how your morning brew affects how you feel and think, not just the caffeine itself.",
'{{INSIGHT_TITLE}}': "Meta's Free AI Agent Wants Into Your Business Tools — What a Tradie Should Check Before Saying Yes",
'{{INSIGHT_BODY}}': "Meta's Muse for Small Business is free with usage limits and plugs into tools like Shopify, Dropbox and Slack, promising an agent that understands your whole operation. That's tempting for a one-person office drowning in quotes and follow-ups, but free tools are paid for somehow. Before connecting anything, check what data it can read, whether it can send messages or change records on its own, and whether you can switch it off. Start with one low-risk job, like drafting follow-up texts to old quotes, keep a human check on anything a customer sees, and never connect your accounting or banking until you trust it.",
'{{FACT_1}}': "Victoria's Midday Power Saver, starting 1 October, gives participating households free electricity between 11am and 2pm every day — but only if they have a smart meter and actively opt in with their retailer.",
'{{FACT_2}}': "Russia's newer jet-powered drones made up 90 of the 120 fired at Ukraine in this week's attack, and because they fly faster and higher, Ukraine could intercept only about 57% of them.",
'{{FACT_3}}': "Shares in Chinese robot maker Unitree soared more than fivefold on their 19 August Shanghai debut, then fell 55% from that peak — a reminder that robot hype and robot sales aren't the same thing.",
'{{JOKE_SETUP}}': "An appliance repairer was asked how his small business kept getting repeat customers, even when he had to tell them their fridge was beyond saving.",
'{{JOKE_PUNCHLINE}}': 'He said, "Simple — I always leave them with a cool head and a warm recommendation."',
'{{CLOSING_QUOTE}}': '"Plan your work, and work your plan."',
'{{CLOSING_ATTR}}': '— Napoleon Hill',
'{{CLOSING_MESSAGE}}': "It's a mild, cloudy Wednesday in Carrum Downs, with the RBA's new 4.60% cash rate taking effect today and showers due this evening. Get outdoor jobs finished by mid-afternoon, since a possible thunderstorm and up to 25mm of rain are forecast for tomorrow.",
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
