#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Thursday, 29 October 2026',
'{{WEATHER_1}}': 'THU 29 OCT · ☁️ Cloudy · 12–19°C',
'{{WEATHER_2}}': 'FRI 30 OCT · ☀️ Clear to partly cloudy, dry · 9–25°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'SAT 31 OCT · 🌧️ Showers, possible storm, 10–15 mm · 16–22°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'SUN 1 NOV · 🌥️ Mostly cloudy, a shower or two · 12–19°C',
'{{WEATHER_5}}': 'MON 2 NOV · 🌥️ Forecast not confirmed, check BoM',
'{{WEATHER_ALERT}}': "Friday is the standout: dry, clear and up to 25°C, so that is the day for exterior coating and blasting work. Saturday looks wet with possible storms. These come from commercial Melbourne forecasts (WillyWeather and Elders), not a Carrum Downs-specific BoM page, and they vary a little between sources, so check BoM before committing to outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 US · IRAN',
'{{WORLD_1_HEADLINE}}': "US Reportedly Preparing to Renew Strikes on Iran After the November Midterms",
'{{WORLD_1_SUMMARY}}': "CNBC ties Wednesday's rise in crude to reports that Washington could resume strikes once the midterms are over, with the Strait of Hormuz still largely shut to commercial shipping. This is a report of preparations, not a confirmed decision, and ING analysts say prices could ease if no new strikes come.",
'{{WORLD_1_URL}}': 'https://www.cnbc.com/2026/10/28/oil-price-today-wti-brent-hormuz.html',
'{{WORLD_2_FLAG}}': '🌍 ISRAEL',
'{{WORLD_2_HEADLINE}}': "Israel's Election Produces No Clear Winner Between the Netanyahu and Eisenkot Blocs",
'{{WORLD_2_SUMMARY}}': "Headline coverage points to a deadlock, which usually means weeks of coalition bargaining. I only saw news-homepage snippets and couldn't open a full article, so treat the detail as unverified until more outlets confirm.",
'{{WORLD_2_URL}}': 'https://www.aljazeera.com/',
'{{ECON_1_FLAG}}': '🇦🇺 INFLATION · RBA',
'{{ECON_1_HEADLINE}}': 'Inflation Jumps to 4.3% in September, Making a November RBA Rate Hike Near-Certain',
'{{ECON_1_SUMMARY}}': "The ABS says CPI rose 4.3% in the year to September, up from 4.0% in August, with automotive fuel up 23.6% over the year and housing up 5.2%. Markets now put the odds of a 25-basis-point hike on 3 November at around 85–90%, which would lift the cash rate from 4.60% to 4.85%. Check your variable-rate loans and equipment finance.",
'{{ECON_1_URL}}': 'https://www.abc.net.au/news/2026-10-28/inflation-september-cpi-ahead-of-november-interest-rate-call/107317382',
'{{ECON_2_FLAG}}': '🛢️ OIL · BRENT',
'{{ECON_2_HEADLINE}}': 'Brent Climbs to About US$115 as Hormuz Stays Largely Shut',
'{{ECON_2_SUMMARY}}': "CNBC had Brent futures up 1.3% at US$115.36 on Wednesday, after settling at US$117 on Friday. Fuel was already one of the biggest drivers of September's inflation print, so diesel costs are likely to stay a live issue when pricing longer jobs.",
'{{TECH_1_FLAG}}': '🤖 AI · MARKETING',
'{{TECH_1_HEADLINE}}': "Sprinklr Opens Beta of Six AI Marketing Agents",
'{{TECH_1_SUMMARY}}': "Sprinklr opened a beta of six marketing AI agents on 27 October. It is an enterprise-focused vendor, so it is more a sign of where social media and customer-reply automation is heading than something a small trades business will use directly. Based on an aggregator roundup, not Sprinklr's own announcement.",
'{{TECH_1_URL}}': 'https://aiagentstore.ai/ai-agent-news/this-week',
'{{TECH_2_FLAG}}': '🤖 AI · AGENTS',
'{{TECH_2_HEADLINE}}': "Anthropic's Claude Duet Proactive Agent Preview Targets Small Business Owners",
'{{TECH_2_SUMMARY}}': "Reports describe a research-preview agent that works in the background across email, calendar and invoicing and checks with you before irreversible actions. It launched around 21 October, so it is older than 48 hours, and access is limited to Pro and Max subscribers in the US with a waitlist, so it's not yet usable here.",
'{{ROBOT_1_FLAG}}': '🤖 INSPECTION ROBOTS',
'{{ROBOT_1_HEADLINE}}': "ANYbotics Begins Delivering ANYmal X, a Legged Inspection Robot for Explosive Atmospheres",
'{{ROBOT_1_SUMMARY}}': "The Robot Report says ANYbotics launched customer deliveries of its four-legged inspection robot certified for hazardous zones such as oil, gas and chemical plants. The exact publication date wasn't shown in my search, but it sat among the 27 October items. Useful as a sign that robots are taking over dangerous inspection work in industrial sites.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/anybotics-begins-delivering-anymal-x-legged-robot-explosive-atmospheres/',
'{{AUS_1_HEADLINE}}': "ABC Tells One Nation to Remove Cartoon Depicting Bluey Running Over a Politician",
'{{AUS_1_SUMMARY}}': "ABC managing director Hugh Marks told Senate estimates the use of the character was an intellectual property infringement and a 'shocking' use of Australia's most loved character. The ABC has since formally asked One Nation to take the cartoons down.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-10-28/brk-bluey-senate-estimates-one-nation-cartoon/107317644',
'{{AUS_2_HEADLINE}}': "Only 1,430 Invitations Sent So Far to 50,000+ People Eligible for Centrelink Compensation",
'{{AUS_2_SUMMARY}}': "Officials told Senate estimates that just 1,430 invitations have gone out, though the government has identified more than 50,000 people as potentially eligible over incorrect payment cancellations. From a search summary of ABC's Wednesday coverage.",
'{{VIC_1_HEADLINE}}': "Coalition Surges to 55–45 Lead in Victorian Newspoll a Month Before the Election",
'{{VIC_1_SUMMARY}}': "The Conversation reports the Coalition ahead 55–45 on a two-party basis, and Labor has trailed by at least 52–48 in all recent polls. Premier Ben Carroll and Opposition Leader Jess Wilson are both pitching payroll tax relief ahead of the 28 November election. I saw the summary only, and the poll's exact date was unclear.",
'{{SCI_1_FLAG}}': '🔬 HEALTH',
'{{SCI_1_HEADLINE}}': "A Single Sauna Session Sends Immune Cells Surging Through Your Body",
'{{SCI_1_SUMMARY}}': "A University of Eastern Finland study found a 30-minute sauna session temporarily raises white blood cell counts in the bloodstream, a response that resembles the immune boost seen during exercise. ScienceDaily, 28 October.",
'{{INSIGHT_TITLE}}': "Let AI Turn Your Rough Site Notes Into a Clean Variation Request",
'{{INSIGHT_BODY}}': "Extra work found mid-job is where small trades quietly lose money, usually because the change was agreed verbally and never written down. After the conversation, type or voice-record rough notes on what changed, why, and the extra time and materials, then ask an AI tool to turn them into a short, polite variation request with a clear price line for the customer to approve. Check the figures and wording yourself before sending, and keep customer personal details out of the tool. It takes two minutes and protects your margin.",
'{{FACT_1}}': "A single sauna session can temporarily raise the number of white blood cells circulating in your bloodstream, a response similar to what happens during exercise.",
'{{FACT_2}}': "Australia's September inflation rate of 4.3% was driven in large part by automotive fuel, which rose 23.6% over the year.",
'{{FACT_3}}': "ANYbotics' ANYmal X inspection robot is certified under IECEx and ATEX standards for use in Zone 1 explosive atmospheres, where an ordinary spark could be dangerous.",
'{{JOKE_SETUP}}': "Why did the shopfitter get invited to every planning meeting?",
'{{JOKE_PUNCHLINE}}': '"He was the only one who ever measured twice and still showed up with a spare."',
'{{CLOSING_QUOTE}}': '"What gets measured gets managed."',
'{{CLOSING_ATTR}}': '— Peter Drucker',
'{{CLOSING_MESSAGE}}': "Thursday is cloudy and mild, and Friday looks like the best day of the week: dry, clear and up to 25°C. Get exterior jobs lined up for Friday before Saturday's showers arrive, and keep an eye on Tuesday's RBA decision.",
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
