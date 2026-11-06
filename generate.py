#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 07 November 2026',
'{{WEATHER_1}}': 'SAT 7 NOV · ⛈️ Showers, 90% chance of rain, possible small hail and early-afternoon thunderstorm · about 9-15°C',
'{{WEATHER_2}}': 'SUN 8 NOV · ☁️ Cloudy, only a 10% chance of rain · about 17°C',
'{{WEATHER_2_CLASS}}': '',
'{{WEATHER_3}}': 'MON 9 NOV · 🌤️ Forecast not confirmed in my sources, check BoM',
'{{WEATHER_3_CLASS}}': '',
'{{WEATHER_4}}': 'TUE 10 NOV · 🌤️ Forecast not confirmed in my sources, check BoM',
'{{WEATHER_5}}': 'WED 11 NOV · 🌧️ Showers expected to return (Wed-Thu)',
'{{WEATHER_ALERT}}': "Today is the wet one: showers are very likely, with possible small hail and a chance of an early-afternoon thunderstorm. Sunday looks much drier. These figures are for Melbourne from BoM-sourced search results, not a Carrum Downs page, and I couldn't confirm Monday and Tuesday, so check BoM before scheduling outdoor work.",
'{{WORLD_1_FLAG}}': '🌍 UKRAINE',
'{{WORLD_1_HEADLINE}}': "Trump Says a Russia-Ukraine Deal Is 'Very Close' After Meeting Putin's Envoy",
'{{WORLD_1_SUMMARY}}': "Al Jazeera reports Trump met Russian envoy Kirill Dmitriev at the White House on 6 November and gave no specifics. A temporary local ceasefire around Oleshky allowed nearly 800 civilians to be evacuated. Russian strikes continue, so treat 'very close' as a claim, not a done deal.",
'{{WORLD_1_URL}}': 'https://www.aljazeera.com/news/2026/11/6/trump-met-russian-envoy-after-he-appeared-with-melania-trump-and-ukrainians',
'{{WORLD_2_FLAG}}': '🌍 MIDDLE EAST',
'{{WORLD_2_HEADLINE}}': 'Iran Says Two More Tankers Hit Mines and a US Drone Was Shot Down Near Hormuz',
'{{WORLD_2_SUMMARY}}': "Al Jazeera's 6 November live blog carries the Revolutionary Guard's claims about tanker fires and a downed US MQ-1 drone, while Trump weighs a deal against new strikes. These are Iranian official statements and casualty and incident counts differ between outlets.",
'{{WORLD_2_URL}}': 'https://www.aljazeera.com/news/liveblog/2026/11/6/iran-war-live-trump-warns-us-may-have-to-destroy-rest-of-iran',
'{{ECON_1_FLAG}}': '⛽ FUEL',
'{{ECON_1_HEADLINE}}': 'Melbourne Wholesale Diesel Down About 7.6c in Six Days, Unleaded Down Over 8c',
'{{ECON_1_SUMMARY}}': "AIP terminal gate averages for Melbourne show diesel falling from 267.8 to 260.2 cents a litre and unleaded from 225.0 to 216.9 between 30 October and 5 November. Wholesale doesn't always flow straight to the bowser, and I saw these via a search summary of the AIP page.",
'{{ECON_1_URL}}': 'https://aip.com.au/pricing/terminal-gate-prices/',
'{{ECON_2_FLAG}}': '🛢️ OIL',
'{{ECON_2_HEADLINE}}': 'Oil Prices Rebound Slightly After a Post-Midterm Plunge as More Ships Are Attacked in the Gulf',
'{{ECON_2_SUMMARY}}': "CBS News live coverage reports crude edging back up after a sharp fall following the US midterms, with more ships attacked in the Persian Gulf. Oil is the main driver of our diesel price, so it's worth watching. I only saw the headline summary.",
'{{TECH_1_FLAG}}': '🤖 AI · TENCENT',
'{{TECH_1_HEADLINE}}': 'Tencent Announces Hy4 Model With Visual Understanding and Computer-Use Skills',
'{{TECH_1_SUMMARY}}': "An AI release tracker says Tencent announced Hy4 on 4 November, adding image understanding and the ability to operate a computer, with weights and system cards due in coming days. This comes from an aggregator, not Tencent, so it's unconfirmed.",
'{{TECH_1_URL}}': 'https://www.nocode.mba/ai-release-tracker/2026/11',
'{{TECH_2_FLAG}}': '🤖 AI · DEEPSEEK',
'{{TECH_2_HEADLINE}}': 'DeepSeek Reportedly Releases V4 Flash Update',
'{{TECH_2_SUMMARY}}': "A tracker lists deepseek-v4-flash-0731 as released on 5 November. I found no independent coverage or official announcement, and no major-lab agent launch in the last 48 hours, so treat this as unverified.",
'{{ROBOT_1_FLAG}}': '🤖 HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': 'Shareholders Approve US$2.5B Agility Robotics Humanoid SPAC Deal',
'{{ROBOT_1_SUMMARY}}': "The Robot Report says Churchill Capital XI shareholders approved the deal, expected to bring in about US$465 million gross, and a 5 November piece covers its first day on the market. I only saw headlines and summaries, not the full articles.",
'{{ROBOT_1_URL}}': 'https://www.therobotreport.com/',
'{{AUS_1_HEADLINE}}': 'Man Jailed for Seven Years Over Albury Crash That Killed a Premature Baby',
'{{AUS_1_SUMMARY}}': "ABC reports Andrew Dean Robson, 35, was sentenced on 6 November over a 2025 crash that caused a pregnant teenager to lose her baby. He will be eligible for parole in under three years.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-06/man-jailed-for-albury-crash-premature-baby-death/107355348',
'{{AUS_2_HEADLINE}}': 'Productivity Commission Releases Interim Findings on Making Business More Dynamic',
'{{AUS_2_SUMMARY}}': "ABC's politics page reports the inquiry was directed not to consider tax or industrial relations. Relevant to small operators, but I only saw the headline, so check the full report for details.",
'{{VIC_1_HEADLINE}}': 'Victorian Election Campaign Underway as Nominations Stay Open to Monday',
'{{VIC_1_SUMMARY}}': "Candidate nominations opened on 4 November and close at noon on Monday 9 November. Early voting begins 18 November, ahead of polling day on Saturday 28 November. This is from a campaign-start report, not a fresh 6 November story.",
'{{SCI_1_FLAG}}': '🧠 HEALTH',
'{{SCI_1_HEADLINE}}': 'Low-Dose Anti-Ageing Drug Boosts Brain Blood Flow in People at Higher Alzheimer\'s Risk',
'{{SCI_1_SUMMARY}}': "A small pilot trial of four weeks of low-dose rapamycin in healthy middle-aged APOE4 carriers found improved brain blood flow, strongest in women. Published in the Journal of Cerebral Blood Flow & Metabolism and reported by ScienceDaily on 5 November. It's a small early study, not a treatment.",
'{{INSIGHT_TITLE}}': 'Let AI Turn Your Messy Voicemails Into a Monday Callback List',
'{{INSIGHT_BODY}}': "Missed calls piling up over the week are lost jobs. Paste your voicemail transcripts or scribbled message notes into an AI tool and ask for a callback list ranked by urgency, with a one-line summary of what each person wants and a suggested reply. Check names and numbers yourself, because it can mishear. It takes five minutes and means the first thing you do Monday is ring the people most likely to book work.",
'{{FACT_1}}': "A new ISO standard, ISO 21423:2026, is meant to let mobile robots from different vendors communicate and coordinate in the same site, according to The Robot Report on 3 November.",
'{{FACT_2}}': "Victorian candidate nominations close at noon on Monday 9 November, and early voting begins on Wednesday 18 November.",
'{{FACT_3}}': "A temporary local ceasefire around Oleshky in Ukraine's Kherson region allowed nearly 800 civilians to be evacuated, according to Al Jazeera.",
'{{JOKE_SETUP}}': "Why did the tiler's apprentice get told off for being too cheerful on a wet Saturday?",
'{{JOKE_PUNCHLINE}}': '"Because he kept saying the day was a wash, and the boss said that was the only thing he was meant to be grouting about."',
'{{CLOSING_QUOTE}}': '"Into each life some rain must fall."',
'{{CLOSING_ATTR}}': '— Henry Wadsworth Longfellow',
'{{CLOSING_MESSAGE}}': "It's a wet Saturday with possible hail and a thunderstorm, so keep gear dry and stay off ladders and roofs. Sunday looks calmer, a good day to rest and line up Monday.",
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
