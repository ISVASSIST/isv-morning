#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Friday, 26 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Fri 26 Jun
    # Cold winter Friday; mostly dry today, showers building Sunday into EOFY week
    "{{WEATHER_1}}": "FRI 26 · ☁ Mostly cloudy · 7–11°C",
    "{{WEATHER_2}}": "SAT 27 · 🌤 Partly cloudy · 6–12°C",
    "{{WEATHER_2_CLASS}}": "",
    "{{WEATHER_3}}": "SUN 28 · 🌧 Showers likely · 6–13°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "MON 29 · 🌦 Showers · 10–14°C",
    "{{WEATHER_5}}": "TUE 30 · ⛅ Cloudy · 11–15°C",
    "{{WEATHER_ALERT}}": "⚠ WEEKEND SHOWERS · EOFY TUE 30",

    # World
    "{{WORLD_1_FLAG}}": "🇺🇸 USA · SUPREME COURT · IMMIGRATION",
    "{{WORLD_1_HEADLINE}}": "US Supreme Court Blocks Border Asylum Claims and Strips Legal Shield From Long-Term TPS Residents",
    "{{WORLD_1_SUMMARY}}": "The United States Supreme Court handed the Trump administration two landmark immigration victories on Thursday. In the first ruling, the court held that migrants physically turned away at the US border cannot apply for asylum — eliminating a key legal pathway that had allowed removed individuals to file claims from inside the country. In the second, nationals holding Temporary Protected Status — many of whom have lived lawfully in the United States for decades due to wars or natural disasters in their home countries — were blocked from seeking judicial protection against deportation. Together, the decisions significantly expand executive authority over immigration enforcement and signal the court's willingness to defer to administration policy over established legal protections. The rulings are expected to accelerate deportation proceedings for hundreds of thousands of people, with downstream effects on remittance economies across Latin America and Southeast Asia.",
    "{{WORLD_1_URL}}": "https://www.foxnews.com/politics/supreme-court-hands-trump-two-major-immigration-victories",

    "{{WORLD_2_FLAG}}": "🦠 DRC · EBOLA · EUROPE",
    "{{WORLD_2_HEADLINE}}": "Ebola Reaches France as DRC Outbreak Surpasses 1,100 Cases — Second Largest on Record, No Vaccine Available",
    "{{WORLD_2_SUMMARY}}": "The Ebola outbreak caused by the Bundibugyo virus in the Democratic Republic of Congo has become the second-largest on record, with 1,118 confirmed cases and 291 confirmed deaths as of June 24. The outbreak is spreading faster than any previous Ebola event on record. France confirmed an imported case on June 24 — only the second European case this outbreak, following a US citizen medically evacuated to Germany in May. The Bundibugyo strain has no approved vaccine or specific antiviral treatment, making containment through isolation and contact tracing the only tools available. The WHO flagged one month in that the international response remains insufficient relative to case growth. There are no current cases in Australia. The Department of Health is monitoring the situation.",
    "{{WORLD_2_URL}}": "https://www.who.int/emergencies/situations/ebola-outbreak---drc-2026",

    # Economics
    "{{ECON_1_FLAG}}": "⛽ FUEL EXCISE · CONFIRMED · JULY 1",
    "{{ECON_1_HEADLINE}}": "Fuel Excise Cut Confirmed Halved From Monday — Diesel Expected to Jump Above $2.10/L From July 1",
    "{{ECON_1_SUMMARY}}": "The federal government confirmed on June 23 that the 32 cent per litre fuel excise discount — in place since April 1 — will be halved to 16 cents per litre from Monday June 30, with partial relief continuing until August 2. Diesel pump prices are expected to climb from approximately $1.97/L today to above $2.10/L next week. For trades operators running diesel plant and commercial vehicles in Carrum Downs, the increase arrives alongside the minimum wage rise and the new payday super payment obligation — all effective July 1. The ACCC's June 19 monitoring update showed Melbourne unleaded averaging 163.9c/L and Melbourne diesel at 197.3c/L — both figures set to move up from Monday. Update your July job rates this weekend.",
    "{{ECON_1_URL}}": "https://www.carsguide.com.au/car-news/fuel-prices-in-australia-will-increase-again-as-fuel-excise-discount-slashed-from-june-30",

    "{{ECON_2_FLAG}}": "📊 ABS · CPI · AUSTRALIA",
    "{{ECON_2_HEADLINE}}": "Australian Annual CPI Falls to 4.0% in May — Trimmed Mean Holds at 3.6% as Housing and Transport Drive Costs",
    "{{ECON_2_SUMMARY}}": "The Australian Bureau of Statistics released May 2026 inflation data showing headline CPI of 4.0% annual — down from 4.2% in April — but the underlying trimmed mean rate edged up to 3.6%, well above the RBA's 2–3% target band. Housing costs rose 6.5% year-on-year, food and non-alcoholic beverages 3.3%, and transport 3.3%. For trades businesses, the data reinforces a stubbornly elevated cost environment heading into the new financial year: even as headline inflation eases, the categories that most directly hit operating costs — rent, fuel, and vehicle running — remain elevated. The June 2026 CPI release is scheduled for July 29.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI POLICY · WHITE HOUSE · USA",
    "{{TECH_1_HEADLINE}}": "White House Signs New AI Innovation and Security Executive Order — Federal AI Adoption Mandated, Competitive Stance Accelerated",
    "{{TECH_1_SUMMARY}}": "President Trump signed a new executive order titled 'Promoting Advanced Artificial Intelligence Innovation and Security' in June 2026, directing federal agencies to accelerate AI adoption across government operations and establish tighter security standards for national security AI applications. The order frames US AI leadership as a national security imperative, loosens some Biden-era constraints on AI development, and dramatically expands federal AI procurement. For Australian small business operators, the downstream effect is practical: the AI tools they use daily — Claude, ChatGPT, Gemini — are developing faster in capability and enterprise feature depth because of accelerating US government and commercial demand, and those improvements flow through to every paying subscriber worldwide.",
    "{{TECH_1_URL}}": "https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/",

    "{{TECH_2_FLAG}}": "📱 SHOPIFY · GOOGLE · SMALL BUSINESS AI",
    "{{TECH_2_HEADLINE}}": "Shopify Embeds Google's Imagen 3 Into Its Platform — AI Product Photography Now Available to 5 Million Merchants",
    "{{TECH_2_SUMMARY}}": "Shopify has integrated Google's Imagen 3 AI image generation directly into its merchant tools, giving more than five million small business users access to AI-generated product photography from inside their store dashboard — no photographer, no studio. The integration reflects a broader 2026 shift: enterprise-grade AI capabilities are being bundled into the SaaS tools small businesses already use and pay for, rather than requiring separate AI subscriptions. The same pattern is now visible in accounting software, quoting tools, and job management platforms. AI is no longer an optional add-on — it is becoming a default feature of every business tool you already run.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🦾 NVIDIA · DOOSAN · PHYSICAL AI",
    "{{ROBOT_1_HEADLINE}}": "NVIDIA and Doosan Group Deepen Physical AI Collaboration — Autonomous Industrial Equipment Moves Toward Commercial Reality",
    "{{ROBOT_1_SUMMARY}}": "NVIDIA and South Korea's Doosan Group have expanded their physical AI collaboration, combining NVIDIA's Jetson-based accelerated computing stack with Doosan's industrial automation and heavy equipment capabilities across construction, energy, and manufacturing sectors. The partnership targets autonomous operation of real-world industrial machinery — the category the industry now calls 'physical AI' to distinguish AI that acts in the three-dimensional world from AI that processes text or images in the cloud. The Doosan deal is part of a broader wave of industrial equipment manufacturers — including Caterpillar, ABB, and FANUC — all building their autonomous system pipelines on the same NVIDIA hardware and training infrastructure. The gap between today's pilot programs and commercially autonomous site operations is narrowing faster than most operators expect.",
    "{{ROBOT_1_URL}}": "https://blogs.nvidia.com/blog/nvidia-and-doosan-group-physical-ai/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Auction Clearance Rates Fall to 47.4% Nationally — Lowest Since COVID-19 as Negative Gearing Uncertainty Weighs on Market",
    "{{AUS_1_SUMMARY}}": "The combined capital city auction clearance rate fell to 47.4% for the week ending June 22 — the weakest result since April 2020 during the COVID-19 lockdowns. In Melbourne, the clearance rate was 51.9%, down 13.5 percentage points from the same week in 2025 when two in three auctioned homes sold. Sydney was at 47.2%. More than half of properties going to auction nationally are now passing in. Analysts point to a combination of RBA rate pressure, cost-of-living stress on buyer confidence, and growing uncertainty around the federal government's proposed changes to negative gearing and capital gains tax concessions.",
    "{{AUS_1_URL}}": "https://www.cotality.com/au/press-releases/final-clearance-rates-week-ending-14-june-2026",

    "{{AUS_2_HEADLINE}}": "Socceroos Face Paraguay at Noon Today — World Cup Last 16 Spot on the Line at Levi's Stadium",
    "{{AUS_2_SUMMARY}}": "Australia and Paraguay meet in their final Group D match at the 2026 FIFA World Cup at noon AEST today, Friday June 26, at Levi's Stadium in Santa Clara, California. A win or draw sends the Socceroos through to the Round of 32. Australia sit second in Group D on three points — level with Paraguay but ahead on goal difference — after beating Türkiye 2–0 and losing 2–0 to the USA. Live and free on SBS and SBS On Demand. Melbourne live sites at Federation Square and AAMI Park open from 11:30am.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Melbourne Fans Converge on Federation Square and AAMI Park for Today's Socceroos World Cup Decider",
    "{{VIC_1_SUMMARY}}": "Federation Square and AAMI Park are hosting free public live sites for today's Socceroos vs Paraguay World Cup decider, with gates open from 11:30am AEST for the noon kick-off. Security screening is in place at both venues and early arrival is recommended — capacity is limited. It is a cold 11°C morning across the city. The Queen Victoria Market Winter Night Market continues tonight from 5pm — fire pits, food trucks, and live music if there is something to celebrate after the final whistle.",

    # Science
    "{{SCI_1_FLAG}}": "⚛ QUANTUM PHYSICS · PHOTON SPLITTING",
    "{{SCI_1_HEADLINE}}": "Physicists Try to Split a Single Photon — and Instead Summon an Infinite Quantum Swarm of Particles",
    "{{SCI_1_SUMMARY}}": "A team of physicists attempting to divide a single photon using a fast optical shutter discovered something far stranger than expected: the process does not produce two smaller photons. Instead, it generates a quantum superposition of infinitely many photon states — a mixture ranging from zero to arbitrarily many particles, produced by quantum field fluctuations triggered by the shutter disturbance. The probability of each particle-count outcome depends on how quickly the shutter closes; only as shutter speed approaches infinite fastness does the expected count become truly infinite. Published in Physical Review Letters this month, the result exposes a genuine limitation in the 'photon as discrete particle' model used to describe light — revealing that in quantum field theory, a particle is always a simplified description of a more complex and stranger underlying field state.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Help You Build a Job Cost Template That Catches Every Billable Item Before You Send the Invoice",
    "{{INSIGHT_BODY}}": "Most undercharging in trades businesses does not happen because rates are wrong — it happens because billable time and cost gets missed between site and invoice. A blasting and coatings crew that spent 45 minutes setting up exclusion zones, ordered additional material for a larger-than-expected substrate, and made an unscheduled supply run for consumables often ends up with only two lines on the invoice: labour hours and product. Everything else gets absorbed as overhead or forgotten between site clean-up and desktop. AI can help you fix this systematically. Describe your most recently completed job to Claude or a similar tool — what actually happened, step by step, from leaving the yard to site clean-up — and ask it to build a job cost template: every category of time, every cost type, with short prompts to fill in at job completion rather than from memory two days later. Then run the same exercise across your last three jobs and ask the AI to flag what consistently appears in your verbal description that does not appear in your invoices. That gap is your margin leak. Adjusting the capture process is often more impactful than adjusting your hourly rate — because every unrecorded hour and missed consumable was earned on site and lost at the desk.",

    # Fun Facts
    "{{FACT_1}}": "Voyager 1 — launched in September 1977 — is the most distant human-made object ever built, now more than 24 billion kilometres from Earth. Its radio signals, travelling at the speed of light, take over 22 hours to reach us. The probe still transmits data at just 160 bits per second — slower than a 1980s modem — powered by a plutonium radioisotope thermoelectric generator that NASA expects will keep the spacecraft operational until approximately 2036, nearly 60 years after launch.",

    "{{FACT_2}}": "The Trans-Australian Railway across the Nullarbor Plain runs 478 kilometres in a perfectly straight line — the longest uninterrupted straight stretch of railway track on Earth. Completed in 1917 and surveyed entirely by hand before GPS or laser alignment existed, it crosses one of the world's largest karst limestone plateaux. The name Nullarbor comes from Latin — nullus arbor, meaning no tree — and the treeless plain stretches over 1,100 kilometres across southern Australia.",

    "{{FACT_3}}": "The original 1980 Pac-Man arcade game has a famous kill screen at Level 256. An integer overflow in the game's level counter corrupts the right half of the screen with scrambled tiles and random data, making the stage impossible to complete. Namco's programmers never imagined anyone would reach it — the counter was only designed to handle values up to 255. Reaching Level 256 became a legendary milestone in competitive arcade history, and the corrupted split-screen remains one of gaming's most iconic unintended features.",

    # Joke
    "{{JOKE_SETUP}}": "I looked into getting a humanoid robot to help with site preparation.",
    "{{JOKE_PUNCHLINE}}": "Turns out they need an OH&S induction, a site-specific SWMS, and apparently they clock overtime after eight hours. I'll stick with the apprentice.",

    # Closing
    "{{CLOSING_QUOTE}}": "“The key is not the will to win. Everybody has that. It is the will to prepare to win that is important.”",
    "{{CLOSING_ATTR}}": "— Bobby Knight",
    "{{CLOSING_MESSAGE}}": "Cold and overcast this Friday morning in Carrum Downs — around 11°C with a layer of winter cloud that should thin through the afternoon. The Socceroos kick off against Paraguay at noon on SBS — a win or draw sends Australia into the World Cup Round of 32, and Federation Square will be full from 11:30. On the economics front: the fuel excise cut is confirmed halved from Monday, meaning diesel pushes above $2.10/L from July 1 — the same day the wage rise and payday super rules change. If your July rates are not updated yet, this weekend is the window to fix that. The Ebola outbreak in the DRC has crossed 1,100 cases and reached France — no Australian impact at this point, but one to watch. On the science desk: physicists tried to split a single photon and instead discovered an infinite quantum swarm. Some problems you try to simplify turn out to contain infinities. Have a strong Friday, Liall — and go the Socceroos.",
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
