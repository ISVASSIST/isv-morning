#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Tuesday, 03 November 2026',
'{{WEATHER_1}}': 'TUE 3 NOV · Forecast not confirmed, check BoM',
'{{WEATHER_2}}': 'WED 4 NOV · 🌧️ Rain likely, about 6mm · highs around 14-18°C',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'THU 5 NOV · 🌦️ Light drizzle · 10 to 16°C',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'FRI 6 NOV · 🌧️ Showers · 10 to 20°C',
'{{WEATHER_5}}': 'SAT 7 NOV · 🌦️ Drizzle, cool · about 11 to 13°C',
'{{WEATHER_ALERT}}': "A cool, showery stretch looks likely through Wednesday to Saturday, with Wednesday and Friday the wetter days. These are greater Melbourne figures from two third-party forecast sites that disagree on detail, not a Carrum Downs BoM page, and I couldn't confirm Tuesday's forecast at all. Check BoM before planning outdoor coatings work.",
'{{WORLD_1_FLAG}}': '🌍 IRAN',
'{{WORLD_1_HEADLINE}}': "Draft Proposal to End US-Iran War Circulates After Doha Talks",
'{{WORLD_1_SUMMARY}}': "Iranian negotiators left the Qatar-mediated talks on Sunday and a draft proposal was reportedly circulating on Monday, though an official said the departure wasn't a breakdown and a follow-up meeting is possible. Iran says no final deal can start unless the US blockade ends. Details of the draft haven't been released.",
'{{WORLD_1_URL}}': 'https://www.tbsnews.net/worldbiz/middle-east/iranians-have-left-doha-talks-draft-proposal-us-deal-being-circulated-official',
'{{WORLD_2_FLAG}}': '🌍 USA',
'{{WORLD_2_HEADLINE}}': "Trump Says 'the Hammer' Is Still on the Table as Iran Talks and US Midterms Collide",
'{{WORLD_2_SUMMARY}}': "Fox News live coverage on 2 November reports Trump saying military options remain even as talks continue, with the US vote close. Reports say he indicated no new attacks before the vote. This is a live-blog summary of a fast-moving story, so check the source for updates.",
'{{WORLD_2_URL}}': 'https://www.foxnews.com/live-news/iran-war-news-trump-midterms-peace-deal-israel-november-2',
'{{ECON_1_FLAG}}': '🛢️ OIL · BRENT',
'{{ECON_1_HEADLINE}}': 'Oil Drops Over 4% as Iran Draft Proposal Eases Supply Fears',
'{{ECON_1_SUMMARY}}': "Brent fell on Monday to roughly US$108.50, though sources quote slightly different figures and timings. It had climbed 13.6% in October to above US$113. Any relief at the Australian bowser lags crude by a week or two, so don't bank on cheaper diesel yet.",
'{{ECON_1_URL}}': 'https://oilprice.com/Latest-Energy-News/World-News/Oil-Prices-Plunge-as-Draft-Proposal-to-End-U.S.-Iran-War-is-Circulated.html',
'{{ECON_2_FLAG}}': '🏦 RBA',
'{{ECON_2_HEADLINE}}': 'RBA Decision Due Today at 2:30pm AEDT, Cash Rate Currently 4.60%',
'{{ECON_2_SUMMARY}}': "The cash rate sits at 4.60% after a September rise, the fourth hike this year. Forecasts conflict, with some previews tipping another rise to 4.85% and older market odds favouring no change, so I can't say which way it goes. If you have variable equipment finance or an overdraft, check your repayments after the announcement.",
'{{TECH_1_FLAG}}': '🤖 AI · SMALL BIZ',
'{{TECH_1_HEADLINE}}': "BDC Launches Mission AI to Help Small Businesses Find Where AI Pays Off",
'{{TECH_1_SUMMARY}}': "Canada's business bank says its study found 30% of small firms use generative AI and that those firms are 24% more productive. It's a Canadian program, but the finding about where small firms gain is worth a read. Announced 2 November.",
'{{TECH_1_URL}}': 'https://betakit.com/bdc-launches-two-entrepreneur-led-ai-programs-to-make-small-businesses-and-itself-more-productive/',
'{{TECH_2_FLAG}}': '🤖 AI · AGENTS',
'{{TECH_2_HEADLINE}}': "OpenAI Reportedly Launches Always-On 'Dots' Agents for Paid Business Tiers",
'{{TECH_2_SUMMARY}}': "One roundup says Dots launched for Pro and Business Premium, but sources conflict on which regions are excluded, including the UK and EU. This comes from a vendor newsletter rather than OpenAI itself, so check OpenAI's help centre before relying on it in Australia.",
'{{ROBOT_1_FLAG}}': '🤖 OPTIMUS',
'{{ROBOT_1_HEADLINE}}': "Tesla Optimus Early Production Reported at Fremont, Customer Shipments Not Until Late 2027",
'{{ROBOT_1_SUMMARY}}': "TheStreet reports early Optimus production has started at Fremont, with Musk saying the line could eventually reach a million units a year, but that would take a year or longer. It's a single secondary report, so treat the timelines as claims rather than confirmed output. 2 November.",
'{{ROBOT_1_URL}}': 'https://thestreet.com/investing/elon-musk-incredible-news-micron-stock-investors-humanoid-robot-memory-needs',
'{{AUS_1_HEADLINE}}': "Government Rejects Calls to Means-Test EV and Home Battery Schemes",
'{{AUS_1_SUMMARY}}': "The government says it can't prepare for the next fuel crisis while running deficits, so the subsidies stay open to everyone for now. Reported in the ABC's 2 November federal politics live blog.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-02/federal-politics-live-blog-albanese-chogm-nov-2/107334912',
'{{AUS_2_HEADLINE}}': "Joint Commonwealth-NSW Gun Buyback Opens After Bondi Beach Attack",
'{{AUS_2_SUMMARY}}': "The scheme started on 2 November and lets people hand in firearms for payment. Also on the agenda, Albanese is in the Caribbean for CHOGM, where the Coalition has criticised the timing. Details from search summaries of ABC reporting.",
'{{VIC_1_HEADLINE}}': "Victorian Election Set for 28 November, With Writs Due to Be Issued Today",
'{{VIC_1_SUMMARY}}': "The Parliament of Victoria site lists 3 November as the writ issue date for the 28 November state election. Premier Ben Carroll took over from Jacinta Allan in July. I couldn't find a more specific Victorian news story from the last 48 hours, so this is the best confirmed item.",
'{{SCI_1_FLAG}}': '🔭 HUBBLE',
'{{SCI_1_HEADLINE}}': "Hubble Finds Missing Oxygen in Nearby Dwarf Galaxies, Blown Out by Supernova Winds",
'{{SCI_1_SUMMARY}}': "Data from 37 nearby dwarf galaxies suggests supernova-driven winds strip out more oxygen than current models predict. Published in The Astrophysical Journal, with NASA dating the release to 2 November.",
'{{INSIGHT_TITLE}}': "Let AI Build Your Job Checklist Before You Price the Next Quote",
'{{INSIGHT_BODY}}': "Underpriced jobs usually come from a forgotten step, not a bad hourly rate. Describe the job to an AI tool and ask it to list every stage, consumable, access need and clean-up task, then compare that list with your last quote. Tick off what you actually do and ignore the rest. Keep your own final say on price, and with costs moving as fast as they are, a thorough checklist is cheap insurance.",
'{{FACT_1}}': "Victoria's next state election is on Saturday 28 November 2026, with writs due to be issued on 3 November, according to the Parliament of Victoria.",
'{{FACT_2}}': "The RBA's cash rate is 4.60% after a 25 basis point rise on 29 September, the fourth hike of 2026.",
'{{FACT_3}}': "Canada's BDC says small businesses using generative AI are 24 percent more productive than those that don't, though only 30 percent of them use it.",
'{{JOKE_SETUP}}': "Why did the carpenter refuse to bet on the Cup?",
'{{JOKE_PUNCHLINE}}': '"He only backs things he has measured twice, and no horse ever turned up with a tape measure."',
'{{CLOSING_QUOTE}}': '"Hope is not a strategy."',
'{{CLOSING_ATTR}}': '— Traditional saying',
'{{CLOSING_MESSAGE}}': "The RBA announces its rate decision at 2:30pm today, so have a look at your finance repayments afterwards. With rain tipped from Wednesday, get any outdoor coating work and site prep done today if you can.",
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
