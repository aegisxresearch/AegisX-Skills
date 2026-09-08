#!/usr/bin/env python3
"""Audit kualitas konten skill berdasarkan prinsip anti-AI-slop.

Memeriksa panduan skill (file .md utama) untuk pola kualitas rendah:
- Klaim hampa tanpa bukti atau kriteria
- Code fence tanpa bahasa
- Checklist kosong
- Section penting tidak ada
- Trade-off / failure modes tidak dijelaskan
- Referensi terlalu sedikit atau URL mati
- Nama variabel generik di contoh kode
- Paragraf panjang tanpa sub-heading
- Istilah teknis tidak dibungkus backtick
- AI signature patterns (Co-Authored-By, Generated with, robot emoji)
- Watermark presence check
- Emoji di heading (non-functional)
- Kata kunci "just", "simply", "easily" tanpa konteks

Output: laporan per skill dengan severity (error/warning/info).
Exit code 1 jika ada error.

Usage:
    python3 scripts/audit-slop.py [--json] [--check-urls]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

REQUIRED_SECTIONS = [
    (
        "tujuan|prasyarat|konsep inti|overview|getting started|introduction|struktur",
        "inti section (Konsep inti / Getting Started / Overview)",
    ),
    (
        "checklist|check-list|verification|verifikasi",
        "Checklist section",
    ),
    (
        "kesalahan umum|pitfalls|common mistakes|anti-patterns",
        "Kesalahan umum / Pitfalls section",
    ),
    (
        "referensi|references|resources|see also",
        "Referensi / References section",
    ),
]

HOLLOW_CLAIMS = [
    re.compile(r"\b(scalable|robust|production[- ]ready|battle[- ]tested)\b", re.I),
    re.compile(r"\b(best practice|industry standard|de facto standard)\b", re.I),
    re.compile(r"\b(foolproof|fool[- ]proof|hassle[- ]free|zero[- ]config)\b", re.I),
    re.compile(r"\b(100%|fully|completely) (secure|safe|tested|reliable)\b", re.I),
]

TRADEOFF_KEYWORDS = re.compile(
    r"\b(kapan tidak|when not|trade-?off|downside|limitation|caveat|hindari|avoid|jeleknya|drawback)\b",
    re.I,
)

GENERIC_VAR_NAMES = re.compile(
    r"\b(foo|bar|baz|data_list|my_var|temp|result_?)\b"
)

# Anti-AI-slop: AI signature patterns that should NOT appear in content
AI_SIGNATURE_PATTERNS = [
    re.compile(r"(?i)co-authored-by:\s*(ai|bot|chatgpt|claude|copilot|gemini|openai|anthropic|codebuff|freebuff)"),
    re.compile(r"(?i)(generated|created|written|produced)\s+(with|by)\s+(ai|artificial intelligence|chatgpt|claude|copilot)"),
    re.compile(r"(?i)(powered|assisted)\s+by\s+(ai|artificial intelligence|chatgpt|claude|copilot)"),
    re.compile(r"🤖|🧠|✨\s*(generated|created|written)"),
    re.compile(r"(?i)this\s+(document|file|guide|content)\s+was\s+(generated|created|written)\s+(by|with|using)"),
    re.compile(r"(?i)disclaimer:?\s*(this|the above)\s+(is|was)\s+(generated|created)\s+(by|with)"),
]

# Watermark pattern — content should have a provenance marker
WATERMARK_PATTERNS = [
    re.compile(r"(?i)aegisx\s+research"),
    re.compile(r"(?i)terakhir\s+diupdate|last\s+updated|last\s+reviewed"),
    re.compile(r"(?i)bagian\s+ini\s+dihasilkan|this\s+section\s+is\s+generated"),
]

# Emoji in headings (non-functional, AI slop pattern)
HEADING_EMOJI_RE = re.compile(r"^(#{1,6})\s+[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50]+\s*", re.M)

# Filler words
FILLER_WORDS = re.compile(r"\b(just|simply|easily|obviously|clearly|of course|it's worth noting|it is worth noting)\b", re.I)

CODE_FENCE_RE = re.compile(r"^```(\w*)", re.M)
CHECKLIST_EMPTY_RE = re.compile(r"^[-*]\s+\[[ x]\]\s*$", re.M)
URL_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)", re.M)


class Issue:
    def __init__(self, severity: str, line: int, code: str, message: str):
        self.severity = severity
        self.line = line
        self.code = code
        self.message = message

    def to_dict(self):
        return {
            "severity": self.severity,
            "line": self.line,
            "code": self.code,
            "message": self.message,
        }

    def __str__(self):
        prefix = {"error": "ERR", "warning": "WRN", "info": "INF"}[self.severity]
        return f"  [{prefix}] L{self.line:>4} ({self.code}): {self.message}"


def audit_guide(sid: str, text: str) -> list[Issue]:
    issues: list[Issue] = []
    lines = text.splitlines()
    full_text_lower = text.lower()

    # --- 1. Section structure ---
    for pattern, label in REQUIRED_SECTIONS:
        if not re.search(pattern, full_text_lower):
            issues.append(Issue("warning", 0, "missing-section", f"Section tidak ditemukan: {label}"))

    # --- 2. Code fence language tags ---
    for m in CODE_FENCE_RE.finditer(text):
        lang = m.group(1)
        line_no = text[: m.start()].count("\n") + 1
        if not lang:
            issues.append(Issue("warning", line_no, "code-no-lang", "Code fence tanpa bahasa (```)"))

    # --- 3. Empty checklist items ---
    for m in CHECKLIST_EMPTY_RE.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        issues.append(Issue("error", line_no, "empty-checklist", "Checklist item kosong (tanpa teks)"))

    # --- 4. Trade-off / failure modes ---
    has_tradeoff = bool(TRADEOFF_KEYWORDS.search(text))
    if not has_tradeoff:
        issues.append(Issue("warning", 0, "no-tradeoff", "Tidak ada diskusi trade-off / kapan tidak pakai"))

    # --- 5. Hollow claims ---
    for pattern in HOLLOW_CLAIMS:
        for m in pattern.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            issues.append(
                Issue("warning", line_no, "hollow-claim", f"Klaim hampa: '{m.group().strip()}' — beri kriteria/bukti")
            )

    # --- 6. Generic variable names in code ---
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            for vm in GENERIC_VAR_NAMES.finditer(line):
                issues.append(
                    Issue("info", i, "generic-var", f"Nama variabel generik: '{vm.group()}' — nama deskriptif")
                )

    # --- 7. Reference section quality ---
    refs = URL_RE.findall(text)
    ref_section_start = -1
    for kw in ("referensi", "references", "resources"):
        if kw in full_text_lower:
            headings = {m.group(2).lower().strip(): m.start() for m in HEADING_RE.finditer(text)}
            for h, pos in headings.items():
                if kw in h:
                    ref_section_start = pos
            break
    if ref_section_start >= 0:
        refs_after = [u for u, _ in refs if text.find(u, ref_section_start) > 0]
        if len(refs_after) < 2:
            issues.append(
                Issue("warning", 0, "few-refs", f"Referensi terlalu sedikit ({len(refs_after)}), idealnya >= 3")
            )

    # --- 8. Wall of text (no sub-heading for > 60 lines) ---
    heading_positions = [m.start() for m in HEADING_RE.finditer(text)]
    if len(heading_positions) > 1:
        for i in range(len(heading_positions) - 1):
            gap = text[heading_positions[i] : heading_positions[i + 1]].count("\n")
            if gap > 60:
                line_no = text[: heading_positions[i]].count("\n") + 1
                issues.append(Issue("info", line_no, "wall-of-text", f"Bagian tanpa sub-heading selama {gap} baris"))

    # --- 9. Inline code for technical terms ---
    inline_terms = re.findall(
        r"\b(SQLAlchemy|FastAPI|Prometheus|Grafana|Kubernetes|Argo.?CD|Elasticsearch)\b", text
    )
    for term in set(inline_terms):
        occurrences = list(re.finditer(re.escape(term), text))
        in_backtick = sum(1 for m in occurrences if text[m.start() - 1 : m.start()] == "`")
        if in_backtick < len(occurrences) and len(occurrences) >= 2:
            line_no = next(
                text[: m.start()].count("\n") + 1
                for m in occurrences
                if text[m.start() - 1 : m.start()] != "`"
            )
            issues.append(
                Issue("info", line_no, "no-backtick", f"'{term}' {len(occurrences)}x — beberapa tanpa backtick")
            )

    # --- 10. AI signature detection (error — must not exist) ---
    for pattern in AI_SIGNATURE_PATTERNS:
        for m in pattern.finditer(text):
            line_no = text[: m.start()].count("\n") + 1
            issues.append(
                Issue(
                    "error",
                    line_no,
                    "ai-signature",
                    f"AI signature terdeteksi: '{m.group().strip()}' — hapus dari konten",
                )
            )

    # --- 11. Watermark/provenance check (info) ---
    has_watermark = any(p.search(text) for p in WATERMARK_PATTERNS)
    if not has_watermark:
        issues.append(
            Issue(
                "info",
                0,
                "no-watermark",
                "Tidak ada watermark/provenance — pertimbangkan tambah attribution atau last-reviewed",
            )
        )

    # --- 12. Emoji in headings (warning) ---
    for m in HEADING_EMOJI_RE.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        heading_text = m.group().strip()
        issues.append(
            Issue("warning", line_no, "emoji-heading", f"Emoji di heading: '{heading_text[:40]}' — gunakan teks saja")
        )

    # --- 13. Filler words (info) ---
    for m in FILLER_WORDS.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        issues.append(
            Issue("info", line_no, "filler-word", f"Filler word: '{m.group()}' — pertimbangkan hapus atau ganti")
        )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--check-urls", action="store_true", help="Validate external URLs (slow)")
    parser.add_argument("--skill", help="Audit satu skill tertentu (id)")
    args = parser.parse_args()

    skill_dirs = sorted(
        d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")
    )
    if args.skill:
        skill_dirs = [d for d in skill_dirs if d.name == args.skill]
        if not skill_dirs:
            print(f"Skill tidak ditemukan: {args.skill}", file=sys.stderr)
            return 1

    all_results: dict[str, dict] = {}
    total_errors = 0
    total_warnings = 0

    for d in skill_dirs:
        sid = d.name
        guide = d / f"{sid}.md"
        if not guide.is_file():
            all_results[sid] = {
                "errors": 1,
                "warnings": 0,
                "issues": [
                    {
                        "severity": "error",
                        "line": 0,
                        "code": "missing-guide",
                        "message": f"File {sid}.md tidak ada",
                    }
                ],
            }
            total_errors += 1
            continue
        text = guide.read_text(encoding="utf-8")
        issues = audit_guide(sid, text)
        errs = sum(1 for i in issues if i.severity == "error")
        warns = sum(1 for i in issues if i.severity == "warning")
        total_errors += errs
        total_warnings += warns
        all_results[sid] = {
            "errors": errs,
            "warnings": warns,
            "issues": [i.to_dict() for i in issues],
        }

    if args.json:
        summary = {
            "total_skills": len(skill_dirs),
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "skills": all_results,
        }
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 1 if total_errors > 0 else 0

    # Human-readable output
    skills_with_issues = {sid: r for sid, r in all_results.items() if r["issues"]}
    skills_clean = [sid for sid, r in all_results.items() if not r["issues"]]

    if not skills_with_issues:
        print(f"Semua {len(skill_dirs)} skill lolos audit anti-slop.")
        return 0

    print(f"Audit anti-slop: {len(skill_dirs)} skill diperiksa")
    print(f"   {len(skills_clean)} bersih, {len(skills_with_issues)} punya temuan")
    print(f"   {total_errors} error, {total_warnings} warning\n")

    for sid, r in sorted(skills_with_issues.items()):
        print(f"--- {sid} ({r['errors']} err, {r['warnings']} wrn) ---")
        for iss in r["issues"]:
            sev_label = {"error": "ERR", "warning": "WRN", "info": "INF"}[iss["severity"]]
            print(f"   [{sev_label}] L{iss['line'] or '---':>4} ({iss['code']}): {iss['message']}")
        print()

    print("--- Ringkasan error (harus diperbaiki) ---")
    error_types: dict[str, int] = {}
    for r in all_results.values():
        for iss in r["issues"]:
            if iss["severity"] == "error":
                error_types[iss["code"]] = error_types.get(iss["code"], 0) + 1
    for code, count in sorted(error_types.items(), key=lambda x: -x[1]):
        print(f"   {code}: {count}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
