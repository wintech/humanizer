---
name: humanizer
version: 3.0.0
description: Use when editing or reviewing text that may sound AI-generated, robotic, or sterile — especially before publishing persona content, marketing copy, or LLM-assisted drafts. Grounded in detection research (Kobak et al. 2024, COLING 2025) and Wikipedia's WikiProject AI Cleanup. Modular: SKILL.md is the orchestrator; specific patterns and language overlays live in references/. English-tuned by default; load language-overlay-<lang>.md for other languages.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# Humanizer: Remove AI Writing Patterns

This skill is an orchestrator. The 24-pattern catalog and language-specific overlays live in `references/`. Each step below loads the references it needs.

## What research shows

Detection studies (Kobak et al. 2024, COLING 2025, Computational Linguistics 2025 survey) identify five high-signal markers:

1. **Vocabulary frequency shifts** — *delve, underscore, tapestry, intricate, showcase, meticulous, boast, commendable, surpass, unlocking, pivotal* spiked sharply post-2022 (Z>3.5 in 2024).
2. **Sentence-length uniformity** — top stylometric discriminator beyond perplexity. Humans cluster at extremes; LLMs cluster at moderate length.
3. **Em-dash frequency** — GPT-4.1 uses ~3.28× human baseline (blog research, Freeburg, reported via McGill OSS 2025). GPT-5.1 suppresses by default.
4. **Narrower vocabulary, synonym cycling** — LLMs have higher repetition penalty.
5. **Lower emotional range** — fewer question/exclamation marks, more formal register.

**Caveats (read before flagging anything):**

- **No single marker is proof.** Many experienced human writers use em dashes heavily. Vocabulary tells need *frequency*, not single occurrences.
- **ESL bias.** Non-native English writers naturally produce lower-perplexity, more uniform text. Apply judgment.
- **Models adapt.** Detection markers move with model versions. Combine markers, do not rely on any one.
- **Language scope.** Default catalog is English-tuned. Load `references/language-overlay-<lang>.md` for other languages.

## Workflow

The workflow has nine steps (0 through 8). Steps load references on demand.

### Step 0 — Over-edit gate

If the text already reads naturally — sentence variance present, no vocabulary clusters, no significance inflation — run Steps 0.5 and 0.6 anyway (they are mechanical and always apply), then declare clean and stop. Reflexive editing produces homogenized output, which is its own AI tell. Single-pattern issues get a single-pattern fix; do not rewrite the rest "for consistency."

### Step 0.5 — Encoding Pre-flight

**Run before everything else, including Step 4 typography replacements.**

Scan the input for mojibake — characters that were stored or transmitted with a mismatched charset (commonly UTF-8 bytes read as Windows-1252/Latin-1). Fix them to correct Unicode first. Step 0.6 will then convert the resulting Unicode typographic characters (em dash, curly quotes, etc.) to plain ASCII as normal.

**Mojibake substitution table — apply in order (longer sequences first):**

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
| `Ã¢` | `â` | U+00E2 |
| `Ã®` | `î` | U+00EE |
| `Ã´` | `ô` | U+00F4 |
| `Ã»` | `û` | U+00FB |
| `Ã§` | `ç` | U+00E7 |
| `Ã‰` | `É` | U+00C9 |
| `Ã€` | `À` | U+00C0 |

**Also fix these less-visible patterns:**

| Pattern | Issue | Fix |
|---|---|---|
| `"` + `"` (U+201C) adjacent to a digit | Range dash stored as ASCII quote + curly quote | Replace the pair with `–` (en dash) |
| `"` + `"` (U+201D) adjacent to a digit | Same, right-quote variant | Replace with `–` |

**Decision rule:** If no mojibake found, skip and continue to Step 0.6. If found, fix all occurrences, note count in the output summary, then continue.

### Step 0.6 — Hidden watermark character scan (mandatory)

**Run on every input, after Step 0.5 and before Step 1.** Invisible and typographic characters are a common watermark / AI-provenance signal. You cannot reliably see them by reading, so always use the script — never eyeball it.

1. Save the text to a file in the scratchpad (skip if it is already a file).
2. Scan: `python ~/.claude/skills/humanizer/scripts/hidden_chars.py <file>` — prints each character found (code point, name, count, line:col). Exit 0 = clean.
3. If anything is found, fix: `python ~/.claude/skills/humanizer/scripts/hidden_chars.py <file> --fix` — rewrites the file and confirms `0 left`. Continue editing from the fixed file.
4. Report in the output summary: `Hidden characters: N found and fixed (U+200B x3, U+00A0 x2, ...)` or `Hidden characters: none`.

What the script handles:

| Class | Characters | Fix |
|---|---|---|
| Zero-width / invisible | U+200B, U+200C, U+2060, U+FEFF (BOM), U+00AD soft hyphen, U+180E, U+034F, U+2061-2064 | removed |
| Bidi controls | U+200E, U+200F, U+061C, U+202A-202E, U+2066-2069 | removed |
| Unicode tag chars (ASCII smuggling) | U+E0000-E007F | removed |
| ZWJ + variation selectors | U+200D, U+FE00-FE0F | removed, **except** inside emoji sequences (kept) |
| Non-breaking / odd spaces | U+00A0, U+202F, U+2000-200A, U+205F, U+3000, U+1680 | regular space |
| Line / paragraph separators | U+2028, U+2029 | newline |
| Curly quotes, primes | U+201C-201F, U+2033 / U+2018-201B, U+2032 | `"` / `'` |
| Em dash, horizontal bar | U+2014, U+2015 | ` - ` (spaced hyphen) |
| En dash | U+2013 | `-` between digits (ranges), else ` - ` |
| Other hyphens, minus | U+2010, U+2011, U+2012, U+2212 | `-` |
| Ellipsis | U+2026 | `...` |
| ASCII `--` used as a dash | `word -- word`, `word--word` (skips code, `--flags`, `<!-- -->`, `---` rules) | `-` between digits, else ` - ` |

Voice exception: if Step 2 finds the writer deliberately uses em dashes, the fix still runs here; restore them by hand only when the user asks.

**Final re-scan:** rewrites in Steps 4-7 can reintroduce curly quotes and dashes. Run the scan again on the final version before delivering it. It must exit 0.

### Step 1 — Diagnose

Before editing, establish four things:

1. **Language.** If non-English, load `references/language-overlay-<lang>.md`. Currently available: `slovak`. Other languages: catalog applies as starting hypothesis, with caveats.
2. **Content type.** Technical / marketing / personal / regulatory / educational / mixed.
3. **Length.** Short (<300 words) / medium (300-1500) / long (>1500).
4. **Input purity.** If input might be hybrid (human draft + AI polish), load `references/hybrid-input.md` and tag each paragraph HUMAN / MIXED / AI before editing.

Then load `references/context-calibration.md` to determine which patterns to apply and at what intensity for this content type × length combination.

### Step 2 — Identify target voice

Ask if not told: which persona, brand, or author? Voice signatures take precedence over the pattern catalog. If the writer's natural voice uses a flagged pattern (em dashes for an essayist, "key" as a verb for an engineer, long sentences with semicolons), leave it. Goal: make the text sound like its writer with AI-isms gone — not standardize voice across personas.

**ESL note (bidirectional):** if the writer is a non-native English speaker, treat low burstiness and limited vocabulary as ESL features, not AI tells. Be more conservative.

### Step 2.5 — Stop-slop pre-clean (mandatory)

Invoke the `stop-slop` skill on the input **before** the catalog scan, so downstream steps work on pre-cleaned prose.

Apply Quick Checks: adverbs, passive voice, inanimate-actor verbs ("the complaint becomes a fix"), Wh- openers, "here's what/this/that" throat-clearing, "not X, it's Y" contrasts, three-same-length sentence runs, em dashes, vague declaratives, narrator-from-a-distance, meta-joiners ("the rest of this essay…").

Score 5 dimensions (Directness / Rhythm / Trust / Authenticity / Density), 1-10 each. **If total < 35/50, revise once and re-score.** Cap at one revise.

Conflict rule: if a stop-slop fix would erase a Step 2 voice signature (essayist em dash, persona-specific cadence, technical jargon required by role), keep the voice signature.

Load on demand from `~/.claude/skills/stop-slop/`: `SKILL.md`, `references/phrases.md`, `references/structures.md`, `references/examples.md`.

### Step 3 — Scan for patterns

Load `references/pattern-catalog.md`. Apply patterns at the intensity from Step 1's context calibration. Cluster of 3+ focal vocabulary matches in a paragraph = high signal; isolated single matches usually are not.

### Step 4 — Rewrite problematic sections

Replace AI-isms with natural alternatives that fit Step 2's target voice. Preserve meaning and facts. Do not invent details (names, statistics, citations) to sound "more human" — that creates a different problem.

**Mandatory typography replacements** (already applied mechanically in Step 0.6; the table stays as the rule for any text you write here — do not type these characters into rewrites):

| Character | Unicode | Replace with | Reason |
|-----------|---------|--------------|--------|
| Em dash `—` | U+2014 | ` - ` (spaced hyphen) | Pattern 13; GPT-4.1 ~3.28× human baseline |
| En dash `–` | U+2013 | `-` (hyphen) or ` - ` | Pattern 13; also overused by AI |
| Curly double open `"` | U+201C | `"` straight | Pattern 18; ChatGPT default output |
| Curly double close `"` | U+201D | `"` straight | Pattern 18; ChatGPT default output |
| Curly single open `'` | U+2018 | `'` straight | Pattern 18 |
| Curly single close `'` | U+2019 | `'` straight | Pattern 18 |
| True ellipsis `…` | U+2026 | `...` three dots | Pattern 26; AI typography tell |
| Non-breaking space | U+00A0 | regular space | Pattern 26; invisible, causes encoding issues |
| Zero-width space | U+200B | remove entirely | Pattern 26; invisible, corrupts pasted text |

No exceptions on these. Full list of handled characters: Step 0.6.

### Step 5 — Transition coherence check

Load `references/transition-coherence.md`. After surgical edits, re-read paragraphs end-to-end. Fix broken connective tissue: orphaned pronouns, dangling transition words, broken antecedents, abandoned list rhythms.

### Step 6 — Add soul where flat

Load `references/soul-toolkit.md`. Apply only where the text reads flat AND the target voice from Step 2 permits. Not every text needs soul injection — regulatory disclosures don't.

### Step 7 — Anti-AI audit — cap at two passes

Prompt: "What makes the below so obviously AI generated?" Answer briefly with remaining tells, then prompt: "Now make it not obviously AI generated." and revise. **Stop after this pass.** Further iteration produces homogenized "humanized" slop.

### Step 8 — Detector lens (optional, Option C fallback)

Load `references/detector-lens.md`. Run stylometric self-check. **Only fix if failure points to a real quality issue, not a detector quirk.** If burstiness is low because the writer is non-native English with naturally uniform rhythm, ship it. Voice quality beats detector compliance.

## Output Format

Provide:

1. Draft humanized version
2. "What makes the below so obviously AI generated?" — brief bullets
3. Final version (revised after the audit)
4. Brief summary of changes made (optional)
5. Hidden-character result from Step 0.6 (count per character, or "none") and confirmation the final re-scan exited 0

## Reference dependencies

| Reference | Loaded at | Source / Author |
|---|---|---|
| `references/pattern-catalog.md` | Step 3 | Wikipedia/blader (MIT, attributed) + F. Novak v2.4.0 contributions |
| `references/transition-coherence.md` | Step 5 | F. Novak (MIT) |
| `references/soul-toolkit.md` | Step 6 | F. Novak (MIT) |
| `references/context-calibration.md` | End of Step 1 | F. Novak (MIT) |
| `references/hybrid-input.md` | End of Step 1 (if hybrid suspected) | F. Novak (MIT) |
| `references/detector-lens.md` | Step 8 (optional) | F. Novak (MIT) |
| `references/language-overlay-slovak.md` | Step 1 (if Slovak) | F. Novak (MIT) |
| `stop-slop` skill (`~/.claude/skills/stop-slop/`) | Step 2.5 (mandatory pre-clean) | Hardik Pandya (MIT) |

See `NOTICE` for full attribution. See `LICENSE` (MIT, Siqi Chen © 2025).
