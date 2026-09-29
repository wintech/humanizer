---
name: pattern-catalog
description: 24-pattern catalog of AI writing tells, loaded by humanizer SKILL.md Step 3
attribution:
  - Patterns 1-24, examples, and pattern structure originate from blader/humanizer
    (MIT licensed, Copyright (c) 2025 Siqi Chen), ultimately derived from Wikipedia's
    "Signs of AI writing" page (WikiProject AI Cleanup, CC BY-SA).
  - Pattern 7 (AI vocabulary) refined in humanizer v2.4.0 by F. Novak — research-validated
    vs context-dependent split based on Kobak et al. 2024.
  - Pattern 25 (Uniform Sentence Rhythm) added in humanizer v2.4.0 by F. Novak — based on
    Computational Linguistics 2025 survey identifying sentence-length variance as the top
    stylometric discriminator beyond perplexity.
  - Removed in v2.4.0: original pattern 25 "Hyphenated Word Pair Overuse" — no empirical
    support and produced grammatically worse output.
  - Pattern 26 (Unicode Typography and Invisible Characters) added — covers mandatory
    substitutions (em dash, en dash, curly quotes, true ellipsis, non-breaking/zero-width
    spaces) and decorative symbol replacements (arrows, special bullets, math operators in
    prose). Mandatory subset enforced in SKILL.md Step 4.
---

# Pattern catalog

Loaded by SKILL.md Step 3 (pattern scan). Apply at intensity determined by Step 1 context
calibration. Cluster of 3+ focal vocabulary matches in a paragraph = high signal; isolated
single matches usually not.

## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.


### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.


### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.


### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.


### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.


### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.


## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**Research-validated focal words** (Kobak et al. 2024; PubMed Z-score >3.5 in 2024 vs. pre-ChatGPT baseline): *delve, underscore, tapestry, intricate/intricacies, showcase, meticulous, boast, commendable, surpass, unlocking, pivotal, enduring, garner, fostering, testament, vibrant, align with*

**Context-dependent tells** (flag only when co-occurring with at least one other pattern from this skill — these words are normal English on their own): *Additionally, crucial, emphasizing, enhance, interplay, landscape* (as abstract noun)

**Deliberately not flagged:** *key, valuable, highlight* — generic English; flagging them homogenizes legitimate writing and produces over-zealous edits.

**Problem:** These words appear far more frequently in post-2023 text and tend to co-occur. A single instance proves nothing; clustering of three or more from the focal list in a paragraph is a stronger signal.

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.


### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.


### 9. Negative Parallelisms

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.


### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.


### 11. Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty code causing excessive synonym substitution.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.


### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.


## STYLE PATTERNS

### 13. Em Dash Overuse

**Problem:** LLMs use em dashes (—) more than humans, mimicking "punchy" sales writing.

**Before:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.


### 14. Overuse of Boldface

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.


### 15. Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.


### 16. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships


### 17. Emojis

**Problem:** AI chatbots often decorate headings or bullet points with emojis.

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.


### 18. Curly Quotes and Smart Apostrophes

**Problem:** ChatGPT and most LLMs output typographic Unicode quotes and apostrophes by default. These are invisible in rendered HTML but detectable in raw text and differ from what humans type on keyboards.

**Characters to replace (mandatory — see Step 4):**
- `“` (U+201C) and `”` (U+201D) → `"` straight double quote
- `‘` (U+2018) and `’` (U+2019) → `'` straight single quote / apostrophe

**Before:**
> He said “the project is on track” but others disagreed. It’s the team’s call.

**After:**
> He said "the project is on track" but others disagreed. It's the team's call.


## COMMUNICATION PATTERNS

### 19. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.


### 20. Knowledge-Cutoff Disclaimers

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Problem:** AI disclaimers about incomplete information get left in text.

**Before:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.


### 21. Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language.

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.


## FILLER AND HEDGING

### 22. Filler Phrases

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"


### 23. Excessive Hedging

**Problem:** Over-qualifying statements.

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.


### 24. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> The company plans to open two more locations next year.


### 26. Unicode Typography and Invisible Characters

**Problem:** AI outputs substitute Unicode typographic characters for plain ASCII equivalents. Some are invisible (non-breaking space, zero-width space) and cause encoding or layout bugs. Others are visible but signal AI generation.

**Step 0.5 — Mojibake pre-flight (run FIRST, before Step 4):**

Mojibake happens when UTF-8 text is read with a mismatched charset (most often Windows-1252/Latin-1). Fix these corrupted sequences to correct Unicode first — Step 4 will then normalize them to plain ASCII.

| Corrupted sequence | Correct character | Unicode |
|---|---|---|
| `â€"` | `–` | U+2013 en dash |
| `â€"` | `—` | U+2014 em dash |
| `â€™` | `'` | U+2019 right single quote |
| `â€˜` | `'` | U+2018 left single quote |
| `â€œ` | `"` | U+201C left double quote |
| `â€` | `"` | U+201D right double quote |
| `â€¢` | `•` | U+2022 bullet |
| `Â·` | `·` | U+00B7 middle dot |
| `Â ` | ` ` | regular space (double-encoded NBSP) |
| `Ã©` | `é` | U+00E9 |
| `Ã¨` | `è` | U+00E8 |
| `Ã ` | `à` | U+00E0 |
| `Ã§` | `ç` | U+00E7 |
| `Ã‰` | `É` | U+00C9 |

Also fix digit-adjacent quote pairs used as range dashes:
- `"` (U+201C) immediately after a digit → `–` (en dash)
- `"` (U+201D) immediately after a digit → `–` (en dash)

**Mandatory substitutions (see Step 4 — run after mojibake pre-flight):**

| AI Output | Unicode | Plain replacement |
|-----------|---------|-------------------|
| `—` em dash | U+2014 | ` - ` spaced hyphen |
| `–` en dash | U+2013 | `-` or ` - ` |
| `…` true ellipsis | U+2026 | `...` |
| `"` `"` curly doubles | U+201C/D | `"` |
| `'` `'` curly singles | U+2018/9 | `'` |
| non-breaking space | U+00A0 | regular space |
| zero-width space | U+200B | remove |

**Decorative symbols in prose (fix when not in code or data):**

| Symbol | Context | Fix |
|--------|---------|-----|
| `→` (U+2192) | Used as "to" or "leads to" in prose | spell it out or use `->` |
| `×` (U+00D7) | Used as "x" multiplier in prose | use "x" or "by" |
| `•` `◦` `▪` special bullets | Non-standard list markers | use plain `-` or `*` |
| `✓` `✅` checkmarks | Decorative in prose | remove or reword |
| `©` `®` `™` | Not part of a legal/brand requirement | remove |
| `½` `¼` `¾` fractions | Non-code prose | spell out or use `/` |
| `≈` `≠` `≤` `≥` | Non-math prose | spell out ("about", "is not", "at most") |

**Before:**
> The process → better results — it's that simple. Cost savings: ≈30% × current spend.

**After:**
> The process leads to better results. Cost savings are roughly 30% of current spend.

### 25. Uniform Sentence Rhythm

**Words to watch:** N/A — this is structural, not lexical.

**Problem:** Sentence-length variance is one of the strongest empirical discriminators between human and LLM text (Computational Linguistics 2025 survey; Pangram Labs 2024). LLMs cluster around moderate length (15–25 words) and rarely deviate. Humans cluster at extremes — short punchy sentences, then long winding ones with multiple clauses.

**Diagnostic:** If five consecutive sentences fall within ±5 words of each other, you have a rhythm problem. Read it aloud. If your breath pattern stays the same the whole way through, the rhythm is flat.

**Before (uniform 18–22 words):**
> The product launched in March after eighteen months of development work. The team had been iterating on the core feature set since the previous summer. Early customer feedback has been generally positive across most segments. Sales performance exceeded the initial internal forecast for the first quarter. The roadmap for the next six months focuses on enterprise readiness.

**After (variance restored):**
> The product launched in March. Eighteen months of work behind it, three rewrites, one team change — and it landed. Sales beat the forecast, not by a small margin. Customers like it, mostly. The next six months are about enterprise readiness, which is the boring word for what we actually need: SSO, audit logs, and people who pick up the phone.

---
