#!/usr/bin/env python3
"""Read template.html, replace placeholders with today's content, write to index.html."""

import re

replacements = {
    "{{DATE}}": "Saturday, 27 June 2026",

    # Weather — Carrum Downs VIC, 5-day from Sat 27 Jun
    # Cold winter Saturday; partly cloudy today, showers building Sunday–Monday
    "{{WEATHER_1}}": "SAT 27 · 🌤 Partly cloudy · 7–13°C",
    "{{WEATHER_2}}": "SUN 28 · 🌧 Showers likely · 7–12°C",
    "{{WEATHER_2_CLASS}}": "rain",
    "{{WEATHER_3}}": "MON 29 · 🌦 Rainy · 6–12°C",
    "{{WEATHER_3_CLASS}}": "rain",
    "{{WEATHER_4}}": "TUE 30 · ⛅ Mostly cloudy · 8–14°C",
    "{{WEATHER_5}}": "WED 1 · 🌤 Fine and cold · 9–15°C",
    "{{WEATHER_ALERT}}": "⚠ SHOWERS SUN–MON · EOFY TUE 30",

    # World
    "{{WORLD_1_FLAG}}": "🇻🇪 VENEZUELA · EARTHQUAKE",
    "{{WORLD_1_HEADLINE}}": "Twin Earthquakes Kill Over 900 in Venezuela — Strongest in 125 Years as Rescue Teams Race to Find Survivors",
    "{{WORLD_1_SUMMARY}}": "Two powerful earthquakes — magnitude 7.5 and 7.2 — struck western Venezuela within minutes of each other on June 24, killing at least 920 people and injuring more than 3,000 across states west of Caracas. At least 172 people remain trapped under collapsed buildings as rescue teams from the United States, Mexico, and neighbouring nations work against a closing search-and-rescue window. The 7.5-magnitude quake is the strongest to strike Venezuela since a similarly catastrophic event in 1900. Venezuela's president declared a national state of emergency across the hardest-hit states. The country was already under severe economic stress before the disaster, complicating the international relief effort. Global aid organisations have been slow to mobilise due to existing diplomatic tensions with the Venezuelan government.",
    "{{WORLD_1_URL}}": "https://www.npr.org/2026/06/26/nx-s1-5870651/venezuela-earthquakes-caracas",

    "{{WORLD_2_FLAG}}": "🇮🇷 IRAN · HORMUZ · SHIPPING",
    "{{WORLD_2_HEADLINE}}": "Iran Strikes Singapore Cargo Ship in Strait of Hormuz, Pausing UN Evacuation of Stranded Vessels",
    "{{WORLD_2_SUMMARY}}": "Iranian forces struck the Singapore-flagged cargo ship 'Ever Lovely' with a drone as it exited the Strait of Hormuz on June 25, damaging the bridge and temporarily halting a United Nations-backed operation to evacuate vessels stranded in the Persian Gulf. The United States confirmed Iran's IRGC was responsible. The attack came weeks after the US and Iran signed a memorandum of understanding to reopen the corridor — the world's most critical oil shipping chokepoint — and directly undermines that agreement. Oil markets edged higher as the incident renewed fears about Hormuz disruption. Iran and the US are in dispute over whether ships must seek Iranian permission before transiting versus using the Omani coastline route.",
    "{{WORLD_2_URL}}": "https://www.cbsnews.com/live-updates/us-iran-war-trump-strait-of-hormuz-oil-prices/",

    # Economics
    "{{ECON_1_FLAG}}": "📊 PMI · AUSTRALIA · JUNE 2026",
    "{{ECON_1_HEADLINE}}": "Australia's Services PMI Holds Below 50 at 49.9 in June — New Orders Fall for Fourth Straight Month",
    "{{ECON_1_SUMMARY}}": "Australia's S&P Global Services PMI came in at 49.9 for June 2026 — up from May's 48.7 but still below the expansion line, signalling ongoing contraction in private sector services activity. New orders fell for a fourth consecutive month as businesses flagged weak domestic demand, cost pressure, and post-election policy uncertainty. Employment rose modestly in June after falling in May, but outstanding work backlogs declined at the fastest pace in two and a half years. The composite PMI (services plus manufacturing) also remained below 50 at 49.8. For small trades operators, the PMI data confirms what many are already experiencing: cautious clients, slower decision cycles, and a market that is moving but not racing heading into the new financial year.",
    "{{ECON_1_URL}}": "https://www.pmi.spglobal.com/Public/Home/PressRelease/bebd268873ef4650ade93d2cd6f35367",

    "{{ECON_2_FLAG}}": "📅 EOFY · JULY 1 · FIVE CHANGES",
    "{{ECON_2_HEADLINE}}": "Five Cost Changes Hit Australian Small Business Simultaneously on July 1 — Wages, Super, Fuel, and Energy All Move at Once",
    "{{ECON_2_SUMMARY}}": "Tuesday July 1 is the most concentrated single-day cost event for Australian small business in years. The national minimum wage rises 3.75% to $24.10 per hour (award rates vary by industry). Compulsory superannuation climbs from 11.5% to 12%. Payday super begins — super must now be paid with each payslip, not quarterly, changing cash flow timing immediately. The full fuel excise returns — petrol and diesel up approximately 29 cents per litre. Regulated electricity tariffs rise across several states. For trades businesses that price labour into quotes and run diesel plant, every one of these increases is a direct margin risk. If your July rates have not been reviewed this weekend, Tuesday hits harder than it should.",

    # Tech / AI
    "{{TECH_1_FLAG}}": "🤖 AI · OPENAI · GPT-5.6",
    "{{TECH_1_HEADLINE}}": "OpenAI Launches GPT-5.6 Preview With 1.5 Million Token Context Window and Three-Tier Model Family",
    "{{TECH_1_SUMMARY}}": "OpenAI began a limited partner rollout of GPT-5.6 on June 26, introducing three model tiers: Sol for complex, agentic tasks; Terra for everyday use; and Luna for high-volume, low-cost applications. The headline capability is a 1.5 million token context window — enough to load an entire year of emails, contracts, job files, or compliance documents into a single AI session and have the model reason across all of it simultaneously. Coding performance and front-end code generation are significantly improved. A broader public release is expected within weeks. For small business users, the practical change is immediate: you can now give an AI tool your complete project history, quote history, or client correspondence without manually selecting what to include.",
    "{{TECH_1_URL}}": "https://www.buildfastwithai.com/blogs/ai-news-today-june-26-2026",

    "{{TECH_2_FLAG}}": "💸 AI · DEEPSEEK · PRICING",
    "{{TECH_2_HEADLINE}}": "DeepSeek Makes 75% Price Cut Permanent — Undercutting GPT-5.5 by Over 5x as Global AI Cost Floor Collapses",
    "{{TECH_2_SUMMARY}}": "Chinese AI firm DeepSeek has made its May 2026 promotional 75% price reduction on its V4-Pro model permanent, locking in costs that undercut OpenAI's GPT-5.5 by more than 5x on input tokens and 17x on output. The move continues the dramatic collapse in AI API pricing that began in late 2024. For small businesses, the practical effect arrives via the tools they already subscribe to: quoting software, job management platforms, accounting apps, and scheduling tools built on these models are seeing their AI running costs fall sharply — and the most competitive vendors will pass those savings through to subscribers across 2026 and 2027.",

    # Robotics
    "{{ROBOT_1_FLAG}}": "🇩🇪 GERMANY · HUMANOIDS · INDUSTRY",
    "{{ROBOT_1_HEADLINE}}": "German Industry Demands Faster Humanoid Robot Adoption — 82% Call for China-Style Government Subsidies",
    "{{ROBOT_1_SUMMARY}}": "The 2026 automatica Trend Index, surveying 100 German industrial executives and automation decision-makers, found that 82% believe Germany should increase subsidies for humanoid robotics development to match China's government-backed approach. Despite Germany ranking third globally in industrial robot density — 449 robots per 10,000 employees, behind South Korea and Singapore — 68% of firms are still running pilot programs rather than full commercial deployment. The survey, published June 26, shows European manufacturers watching China's Unitree, AgiBot, and Honor ecosystems scale into production and growing increasingly anxious about the competitive gap. The global robotics market reached $38 billion in 2026, a 34% year-on-year increase.",
    "{{ROBOT_1_URL}}": "https://www.roboticstomorrow.com/news/2026/06/26/german-economy-calls-for-faster-humanoid-robotics-adoption/26778/",

    # Australia
    "{{AUS_1_HEADLINE}}": "Socceroos Through to World Cup Round of 32 After Gritty 0-0 Draw With Paraguay",
    "{{AUS_1_SUMMARY}}": "Australia secured a place in the 2026 FIFA World Cup knockout stage with a goalless draw against Paraguay at Levi's Stadium in San Francisco on Friday night AEST. The Socceroos finish second in Group D on four points after three group matches. Australia will face a Group C opponent in the round of 32, to be confirmed once today's other group results conclude. It is one of Australia's strongest World Cup group stage performances, going unbeaten across three matches. The Socceroos will now prepare for a knockout match expected in the coming days.",
    "{{AUS_1_URL}}": "https://www.sbs.com.au/news/live-blog/australia-v-paraguay-world-cup-live-score-updates/6y6tfs4pg",

    "{{AUS_2_HEADLINE}}": "AFP to Formally Investigate Abuse Allegations Against Israeli Forces by Australian Gaza Flotilla Activists",
    "{{AUS_2_SUMMARY}}": "The Australian Federal Police will formally investigate allegations that Israeli forces sexually assaulted and tortured Australian citizens detained during the Global Sumud Flotilla incident in May 2026. Eleven Australians were among nearly 400 activists intercepted by Israeli forces while attempting to deliver aid to Gaza. Several Australian women alleged rape and torture during detention. Israel's ambassador to Australia has criticised the AFP investigation as a 'mistake.' The case represents one of Australia's most serious direct diplomatic confrontations with Israel during the ongoing conflict. The investigation's outcome could carry significant bilateral consequences.",

    # Victoria
    "{{VIC_1_HEADLINE}}": "Victoria's Half-Price Public Transport Continues to End of 2026 as Federation Square Fondue Chalet Closes Today",
    "{{VIC_1_SUMMARY}}": "The Victorian Government's half-price public transport fares — which replaced a free PT promotion earlier this year — continue on all metropolitan trains, trams, and buses through the remainder of 2026 as a cost-of-living measure. Melbourne's daily public transport patronage has held above pre-COVID levels across the promotion period. Separately, the popular Federation Square Fondue Chalet closes today after a seven-week winter season that drew record visitors. If you are heading into the city this weekend to follow the Socceroos result or catch a winter event, the half-price fare still applies.",

    # Science
    "{{SCI_1_FLAG}}": "🪐 ASTROBIOLOGY · VENUS · PANSPERMIA",
    "{{SCI_1_HEADLINE}}": "Earth May Have Been Seeding Venus With Microbial Life for Billions of Years, New Study Finds",
    "{{SCI_1_SUMMARY}}": "A study published this week by researchers at Johns Hopkins University Applied Physics Laboratory proposes that asteroid impacts on Earth have been launching rock fragments carrying hardy microbes into space for billions of years — and that some may have reached Venus's cloud layers. The team estimates around 100 viable microbial cells could arrive at Venus each year, and that hundreds of billions of rock fragments may have made the journey over geological timescales. The finding does not claim life currently exists on Venus, but it raises the statistical probability that if life ever existed on early Earth, some of it had a viable pathway to another world. The research contributes to the growing field of panspermia — the hypothesis that life can travel between planets aboard asteroid debris.",

    # Business Insight
    "{{INSIGHT_TITLE}}": "How AI Can Turn Your Job Site Photos Into Professional Documentation — Without Writing a Word",
    "{{INSIGHT_BODY}}": "If you run a blasting and coatings business, job photos are usually abundant — before shots, progress shots, final coverage checks, substrate condition records — but they rarely turn into anything formally documented. AI tools like Claude and GPT-4o can now look at your site photos and generate structured reports: substrate condition notes, coating system records, surface profile observations, completion sign-offs, and client-facing before-and-after summaries. The process takes minutes, requires no writing skill, and produces a document you can send directly to a client or attach to your compliance file. Start with one job this weekend: take ten photos, open a free AI tool, upload them, and ask for a job completion report. A good AI will ask clarifying questions — what system was applied, what the DFT readings were, what surface profile was achieved — and structure the answers into a clean document. That document is then both a client deliverable and a compliance record. Photographic documentation that used to sit invisibly in your camera roll becomes a professional output and a point of difference from operators who still hand over nothing in writing.",

    # Fun Facts
    "{{FACT_1}}": "The twin earthquakes that struck Venezuela on June 24, 2026 — magnitude 7.5 and 7.2 within minutes of each other — are the strongest to hit the country since a catastrophic quake levelled Caracas in 1900, killing an estimated 10,000 to 30,000 people. At the time, that death toll represented more than 10% of Venezuela's entire population. The 1900 earthquake effectively destroyed the city and forced a complete rebuild of the Venezuelan capital.",

    "{{FACT_2}}": "3I/ATLAS — discovered in 2025 and only the third interstellar object ever confirmed to enter our solar system — was scanned for alien radio signals by SETI's Allen Telescope Array for more than seven hours in June 2026. Researchers sifted through 74 million narrowband signals. Every single one traced back to technology on Earth's surface or in Earth orbit. The first two interstellar visitors were 'Oumuamua (2017), which remains unexplained due to its strange non-gravitational acceleration, and Borisov (2019), which behaved like a normal comet.",

    "{{FACT_3}}": "Germany has 449 industrial robots per 10,000 manufacturing employees — the third highest robot density on Earth after South Korea (1,012) and Singapore (770). Australia has approximately 87 robots per 10,000 manufacturing workers — roughly one-fifth the German rate and one-twelfth the South Korean rate. The global average is 162. For context: in trades and field services, where conditions change job-to-job, meaningful robot deployment still lags well behind fixed-location manufacturing by at least a decade.",

    # Joke
    "{{JOKE_SETUP}}": "Why does the concreter never lose an argument?",
    "{{JOKE_PUNCHLINE}}": "Once he sets his position, nobody can move him.",

    # Closing
    "{{CLOSING_QUOTE}}": "“Success usually comes to those who are too busy to be looking for it.”",
    "{{CLOSING_ATTR}}": "— Henry David Thoreau",
    "{{CLOSING_MESSAGE}}": "Happy Saturday, Liall. The Socceroos punched through to the World Cup round of 32 overnight — a gritty nil-all with Paraguay and they are through. Carrum Downs is looking at a partly cloudy winter Saturday morning, decent enough to get a few things done before showers build on Sunday and Monday. Four days until the new financial year: wages, super, fuel excise, and electricity prices all change simultaneously on Tuesday. If your July rates have not been reviewed yet, this weekend is the window before it costs you on the first job of FY2027. On the science front: Earth has apparently been launching microbial hitchhikers toward Venus for billions of years via asteroid impacts. Venus might be less alone than it looks. Make it a good Saturday.",
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
