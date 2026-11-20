#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
'{{DATE}}': 'Saturday, 21 November 2026',
'{{WEATHER_1}}': 'SAT 21 NOV · 🌦️ Warm and humid, possible showers, 18-25°C, gusty northerlies turning northwest',
'{{WEATHER_2}}': 'SUN 22 NOV · ⛈️ Hot, near 31°C, then afternoon storms, possibly severe',
'{{WEATHER_2_CLASS}}': 'rain',
'{{WEATHER_3}}': 'MON 23 NOV · 🌦️ Cooler, about 23°C, chance of a morning storm and showers',
'{{WEATHER_3_CLASS}}': 'rain',
'{{WEATHER_4}}': 'TUE 24 NOV · 🌧️ Showery and cool, about 18°C',
'{{WEATHER_5}}': 'WED 25 NOV · ☁️ Outlook not firm yet, check the BoM closer to the day',
'{{WEATHER_ALERT}}': "Sunday is the day to watch. The BoM's Melbourne forecast has Sunday reaching about 31°C on strong northerly winds of 30 to 45km/h, then a cold front bringing showers and a chance of thunderstorms in the late afternoon and evening. Those storms could be severe, with damaging winds and large hail. Today (Saturday) is warm and humid at about 25°C with a 50% chance of a shower, and northerly winds strengthening to about 40km/h before turning northwest this afternoon. Monday is cooler at about 23°C with a chance of a morning storm, and Tuesday looks showery and cool. If anything is curing outside this weekend, get it under cover before Sunday afternoon, and check the BoM warnings page on Sunday morning.",
'{{WORLD_1_FLAG}}': '⚖️ NETHERLANDS · ICJ',
'{{WORLD_1_HEADLINE}}': 'World Court Finds Myanmar Committed Genocide Against the Rohingya',
'{{WORLD_1_SUMMARY}}': "The International Court of Justice in The Hague ruled on Thursday that Myanmar committed genocide against the Rohingya during its military's 2016-2017 \"clearance operations\". Human Rights Watch says it's the first time the court has found a country responsible for committing genocide. The judges voted nine to six. The court also found Myanmar failed to prevent and punish genocide, and ordered it to investigate and prosecute those responsible, including military commanders, and to compensate victims. Myanmar has two years to report back. The ruling is final and binding, but the court has no way to enforce it, so rights groups are now calling for sanctions.",
'{{WORLD_1_URL}}': 'https://www.hrw.org/news/2026/11/19/world-court-finds-myanmar-committed-rohingya-genocide',
'{{WORLD_2_FLAG}}': '🇷🇺 RUSSIA · UKRAINE',
'{{WORLD_2_HEADLINE}}': 'Putin Invites Europeans to Moscow but Rules Out a Ceasefire',
'{{WORLD_2_SUMMARY}}': "Vladimir Putin says Russia has invited European representatives to Moscow to set out their position on Ukraine. He said Russia would then decide how to continue talks with Kyiv. The Kremlin hasn't said which leaders were invited, and Putin made no promise that Europe would get a formal role in any peace deal. Speaking in Shenzhen, he also rejected Ukraine's call for a ceasefire before winter. The invitation came as leaders from more than 30 countries met in Berlin on Thursday. Germany's Friedrich Merz said Europe is ready to talk, but only with Europe and Ukraine at the table.",
'{{WORLD_2_URL}}': 'https://www.irishtimes.com/world/europe/2026/11/20/putin-invites-european-leaders-to-moscow-for-peace-talks-as-russia-pounds-kyiv/',
'{{ECON_1_FLAG}}': '⛽ FUEL',
'{{ECON_1_HEADLINE}}': 'Diesel Falls Another 8 Cents a Litre in the Big Cities',
'{{ECON_1_SUMMARY}}': "Average diesel in Australia's five biggest cities fell 8.1 cents in a week to 258.3 cents a litre on 18 November, according to a summary of the ACCC's latest weekly fuel report. Average petrol was 207.8 cents. Prices fell in every capital and in more than 190 regional towns as international fuel prices kept easing. Wholesale prices dropped too, so there may be a bit more relief to come. Diesel is still well above where it was in February, though, so keep an eye on the terminal gate price and fill up when your local servo is at the bottom of its cycle.",
'{{ECON_1_URL}}': 'https://www.indexbox.io/blog/australian-fuel-prices-fall-across-capital-cities-and-regions-in-november-2026/',
'{{ECON_2_FLAG}}': '📋 RED TAPE',
'{{ECON_2_HEADLINE}}': 'Productivity Commission Calls for Less Business Reporting',
'{{ECON_2_SUMMARY}}': "The Productivity Commission's interim report on business reporting, released this week, says some non-financial reporting rules should be scaled back or redesigned to cut compliance costs. One example is the scheme that makes large businesses report twice a year on how fast they pay small suppliers. The commission found payment times have improved only slightly since it began. It also warned that extending climate reporting to medium-sized businesses would add a big compliance load. For small trades, the payment-times finding matters most. Don't assume big customers will pay on time just because they have to report it.",
'{{TECH_1_FLAG}}': '📈 AI · MARKETS',
'{{TECH_1_HEADLINE}}': 'Anthropic Lists on Nasdaq in a Record IPO',
'{{TECH_1_SUMMARY}}': "Anthropic, the company that makes the Claude AI assistant, started trading on the Nasdaq on Thursday under the ticker ANT. It priced its shares at US$83, above its planned range, and raised about US$81 billion, overtaking SpaceX's June float as the biggest IPO on record. Shares opened about 34% higher, then closed the first day at US$97.17, up 17%. They fell about 9% in early trading on Friday as some investors took profits. For anyone using Claude at work, nothing changes overnight. The listing shows how much money is now behind the AI tools small businesses are starting to rely on.",
'{{TECH_1_URL}}': 'https://www.forbes.com/sites/fionariley/2026/11/19/anthropic-ipo-live-stock-closes-day-at-97-up-more-than-17/',
'{{TECH_2_FLAG}}': '🤝 AI · POLICY',
'{{TECH_2_HEADLINE}}': 'Australia and China Agree to Set Up Regular AI Talks',
'{{TECH_2_SUMMARY}}': "After Anthony Albanese met Premier Li Qiang in Beijing on Friday, the two countries agreed to set up a regular dialogue on artificial intelligence. A joint statement from Beijing says the talks will cover AI safety, governance and how the technology is used. It comes only days after Australia signed a separate agreement with the US, partly aimed at reducing reliance on China for critical technology. There's no direct change for businesses yet. But the rules on which AI tools and hardware can be used here will be shaped by both of those agreements.",
'{{ROBOT_1_FLAG}}': '🦾 HUMANOIDS',
'{{ROBOT_1_HEADLINE}}': 'Foundation Unveils Phantom MKII, a Humanoid Built for Heavy, Dirty Work',
'{{ROBOT_1_SUMMARY}}': "US company Foundation Future Industries has unveiled the Phantom MKII, its second-generation humanoid robot, aimed at heavy industry and defence. The company says it can carry about 90kg while walking, work in rain, snow and dust, and run for about six hours on a charge. Its new Cortex II software is designed to learn tasks by watching people do them. Tech Times notes the claims haven't been independently tested, and no waterproof rating or battery size has been given. Foundation plans to start production in early 2027.",
'{{ROBOT_1_URL}}': 'https://www.techtimes.com/articles/331061/20261119/humanoid-robot-debut-phantom-mkii-claims-200-pound-walking-payload-no-independent-test.htm',
'{{AUS_1_HEADLINE}}': "Xi Hails a 'Complete Turnaround' in Relations With Australia",
'{{AUS_1_SUMMARY}}': "Xi Jinping told Anthony Albanese at APEC in Shenzhen on Friday that relations between China and Australia had seen a \"complete turnaround\" over the past four years, despite their differences. It was the pair's fifth meeting. Xi agreed to make 2027 the Australia-China Year of Tourism. Albanese said the relationship delivers prosperity for both countries and stressed the value of frank conversations. He then went to Beijing for talks with Premier Li Qiang and a CEO roundtable. Reports say there was no real progress on beef quotas.",
'{{AUS_1_URL}}': 'https://www.abc.net.au/news/2026-11-20/albanese-to-meet-xi-for-trade/107406222',
'{{AUS_2_HEADLINE}}': 'US Sanctions Comanchero Bikie Bosses in an Australian First',
'{{AUS_2_SUMMARY}}': "The US has placed sanctions on Comanchero bikie gang president Allan Meehan and associate Marco Coffen, as part of its wider crackdown on Mexican drug cartels. The AFP says it's the first time an Australian-based crime gang has been sanctioned this way. Australia doesn't enforce US sanctions. But American companies operating here, including banks, may not be able to process transactions for the two men. The AFP's Stephen Nutt said police hope it makes joining or dealing with the gang less attractive.",
'{{VIC_1_HEADLINE}}': 'Two Men Charged Over Stolen Melbourne Cups, and a Fourth Cup Is Missing',
'{{VIC_1_SUMMARY}}': "Victoria Police have charged two men over the theft of racing trophies from Flemington and Caulfield racecourses. Three of Makybe Diva's Melbourne Cups were taken from a display cabinet at Flemington, and the 1948 Caulfield Cup was taken from Caulfield after several break-ins between 4 and 11 November. In court this week it was revealed a fourth Melbourne Cup had also been stolen. A 39-year-old Elsternwick man and a 36-year-old Mount Waverley man have been charged, and both are due back in court in February. The cups haven't been found.",
'{{SCI_1_FLAG}}': '🌊 DEEP SEA',
'{{SCI_1_HEADLINE}}': 'A Strange Bacterium Lives Beneath the Skin of Deep-Sea Sea Pigs',
'{{SCI_1_SUMMARY}}': "Sea pigs are small, plump relatives of sea cucumbers that walk along the deep ocean floor. University of Tokyo researchers have found a new bacterium living in the layers beneath their skin. In some samples it made up more than 70% of all the bacterial DNA found there. They've named it Candidatus Abyssoplasma scotoplanesicola. Its genome is tiny, and it seems to rely on its host for amino acids, fats and minerals. What the sea pig gets in return is still a mystery. The study is in ISME Host Microbe.",
'{{INSIGHT_TITLE}}': 'Before You Take On a Big New Customer, Ask AI to Check Their Credit Signals',
'{{INSIGHT_BODY}}': "The Productivity Commission found big businesses are paying small suppliers only a little faster than before. A large new account can look great on paper and still leave you waiting 60 days or more. Before you quote a big job for a customer you haven't worked with, ask ChatGPT, Claude or Gemini to research them. Get it to look for recent news, any administration or liquidation notices, court cases, reviews from other subcontractors and their published payment terms. Then ask it to sum up the risk in plain English and suggest sensible terms, like a deposit or progress payments. It takes about ten minutes. Check anything serious yourself on ASIC Connect before you rely on it.",
'{{FACT_1}}': "The International Court of Justice's Myanmar ruling this week is the first time the court has found a country responsible for committing genocide.",
'{{FACT_2}}': "The bacterium living beneath the skin of deep-sea sea pigs has a genome of just 649,000 DNA bases, and about a quarter of it goes to building surface proteins.",
'{{FACT_3}}': "Anthropic's IPO raised about US$81 billion, overtaking SpaceX's US$75 billion float in June as the largest IPO on record.",
'{{JOKE_SETUP}}': "Why don't roofers trust a 31-degree Sunday forecast?",
'{{JOKE_PUNCHLINE}}': "They know that what goes up usually comes down, and in Melbourne it comes down as hail.",
'{{CLOSING_QUOTE}}': '"The best way to find out if you can trust somebody is to trust them."',
'{{CLOSING_ATTR}}': '— Ernest Hemingway',
'{{CLOSING_MESSAGE}}': "It's Saturday, and early voting centres for the state election are open today, but they're closed tomorrow. If you want to get your vote done before next Saturday, today's a good chance. Sunday is the one to plan around: hot and windy, then possible severe storms, so tie down and cover anything in the yard tonight. Diesel is still coming down, which helps. Enjoy the weekend.",
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
