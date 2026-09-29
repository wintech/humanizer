#!/usr/bin/env python3
"""Scan text for hidden watermark / AI-typography characters and optionally fix them.

Usage:
  python hidden_chars.py FILE            # report only (exit 1 if anything found)
  python hidden_chars.py FILE --fix      # rewrite FILE in place, then report what changed
  python hidden_chars.py - --fix < in    # read stdin, write cleaned text to stdout

Covers: zero-width / invisible chars, bidi controls, Unicode tag chars, stray variation
selectors, non-breaking and odd-width spaces, curly quotes, typographic dashes, ellipsis,
and ASCII "--" used as a dash ("word -- word", "word--word").
Emoji sequences keep their ZWJ (U+200D) and variation selectors. The "--" check skips
code (fenced blocks and inline backticks), CLI flags (--fix), HTML comments and "---" rules.
"""
import re
import sys
import unicodedata
from collections import Counter

# Removed entirely (invisible, carry no meaning in prose).
REMOVE = {
    0x200B, 0x200C, 0x2060, 0xFEFF, 0x00AD, 0x180E, 0x034F,
    0x200E, 0x200F, 0x061C,
    *range(0x202A, 0x202F), *range(0x2066, 0x206A),
    *range(0x2061, 0x2065),
    *range(0xE0000, 0xE0080),  # Unicode tag characters (ASCII smuggling)
}
# Kept only inside emoji sequences, removed elsewhere.
EMOJI_JOINERS = {0x200D, *range(0xFE00, 0xFE10)}
SPACES = {0x00A0, 0x1680, *range(0x2000, 0x200B), 0x202F, 0x205F, 0x3000}
LINE_BREAKS = {0x2028, 0x2029}
SIMPLE = {
    0x201C: '"', 0x201D: '"', 0x201E: '"', 0x201F: '"', 0x2033: '"',
    0x2018: "'", 0x2019: "'", 0x201A: "'", 0x201B: "'", 0x2032: "'",
    0x2010: "-", 0x2011: "-", 0x2012: "-", 0x2212: "-",
    0x2026: "...",
}
EM_DASHES = "—―"
EN_DASH = "–"
FLAGGED = REMOVE | EMOJI_JOINERS | SPACES | LINE_BREAKS | set(SIMPLE) | {0x2013, 0x2014, 0x2015}

# ASCII "--" standing in for an em dash: spaced ("a -- b") or tight between words ("a--b").
# Not matched: "---" rules, "<!--" / "-->", CLI flags ("--fix").
DOUBLE_HYPHEN = "--"
DOUBLE_HYPHEN_RE = re.compile(
    r"(?<=[^\s<!-]) +--(?![->]) +(?=\S)"
    r"|(?<=[A-Za-z0-9.,;:)\]\"'])--(?=[A-Za-z0-9(\[\"'])")
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)


def is_emoji(ch):
    cp = ord(ch)
    return cp >= 0x1F000 or 0x2600 <= cp <= 0x27BF or 0x2300 <= cp <= 0x23FF


def is_emoji_joiner(text, i):
    return ord(text[i]) in EMOJI_JOINERS and i > 0 and (
        is_emoji(text[i - 1]) or ord(text[i - 1]) in EMOJI_JOINERS)


def fix(text):
    out = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        if cp in REMOVE:
            continue
        if cp in EMOJI_JOINERS:
            if is_emoji_joiner(text, i):
                out.append(ch)
            continue
        if cp in SPACES:
            out.append(" ")
        elif cp in LINE_BREAKS:
            out.append("\n")
        elif cp in SIMPLE:
            out.append(SIMPLE[cp])
        else:
            out.append(ch)
    text = "".join(out)
    # En dash in numeric ranges -> hyphen; other dashes -> spaced hyphen.
    text = re.sub(rf"(?<=\d)\s*{EN_DASH}\s*(?=\d)", "-", text)
    text = re.sub(rf"[ \t]*[{EM_DASHES}{EN_DASH}][ \t]*", " - ", text)
    for start, end in reversed(double_hyphen_spans(text)):
        is_range = text[start - 1].isdigit() and text[end:end + 1].isdigit()
        text = text[:start] + ("-" if is_range else " - ") + text[end:]
    return text


def double_hyphen_spans(text):
    """Spans of ASCII "--" used as a dash, outside code."""
    code = [m.span() for m in CODE_RE.finditer(text)]
    return [m.span() for m in DOUBLE_HYPHEN_RE.finditer(text)
            if not any(s <= m.start() < e for s, e in code)]


def scan(text):
    """Return Counter of flagged code points and first few line:col locations each."""
    counts, where = Counter(), {}
    ln, col = 1, 0
    for i, ch in enumerate(text):
        col += 1
        if ch == "\n":
            ln, col = ln + 1, 0
        if ord(ch) in FLAGGED and not is_emoji_joiner(text, i):
            counts[ch] += 1
            where.setdefault(ch, [])
            if len(where[ch]) < 5:
                where[ch].append(f"{ln}:{col}")
    for start, _ in double_hyphen_spans(text):
        counts[DOUBLE_HYPHEN] += 1
        where.setdefault(DOUBLE_HYPHEN, [])
        if len(where[DOUBLE_HYPHEN]) < 5:
            line_start = text.rfind("\n", 0, start) + 1
            where[DOUBLE_HYPHEN].append(f"{text.count(chr(10), 0, start) + 1}:{start - line_start + 1}")
    return counts, where


def report(counts, where, stream):
    if not counts:
        print("hidden-chars: clean (0 found)", file=stream)
        return
    print(f"hidden-chars: {sum(counts.values())} found", file=stream)
    for ch, n in counts.most_common():
        if ch == DOUBLE_HYPHEN:
            code, name = "  --  ", "ASCII DOUBLE HYPHEN AS DASH"
        else:
            code, name = f"U+{ord(ch):04X}", unicodedata.name(ch, "UNKNOWN")
        print(f"  {code} {name:<32} x{n:<4} at {', '.join(where[ch])}", file=stream)


def main():
    args = [a for a in sys.argv[1:] if a != "--fix"]
    do_fix = "--fix" in sys.argv
    if len(args) != 1:
        sys.exit(__doc__)
    path = args[0]
    if path == "-":
        sys.stdin.reconfigure(encoding="utf-8")
        text = sys.stdin.read()
    else:
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()

    counts, where = scan(text)
    report(counts, where, sys.stderr)
    if not do_fix:
        sys.exit(1 if counts else 0)

    cleaned = fix(text)
    if path == "-":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(cleaned)
    else:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(cleaned)
    left, _ = scan(cleaned)
    print(f"hidden-chars: fixed; {sum(left.values())} left", file=sys.stderr)


if __name__ == "__main__":
    main()
