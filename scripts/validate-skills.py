#!/usr/bin/env python3
"""Validator untuk AegisX Skills Collection.

Memeriksa:
1. Setiap direktori skills/ memiliki README.md dan <nama-skill>.md
2. Manifest skills/manifest.json sinkron dengan direktori aktual
3. Metadata manifest valid (id unik, kategori terdaftar, level/status dikenal)
4. File overview/guide pada manifest benar-benar ada
5. Tidak ada placeholder terlarang (TODO/PLACEHOLDER) di file skill
6. Tidak ada karakter kontrol (NUL)
7. Link lokal Markdown di skill menunjuk ke file yang ada
8. README utama menautkan semua skill (katalog sinkron)

Exit code 0 jika semua lolos, 1 jika ada temuan.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MANIFEST_PATH = SKILLS_DIR / "manifest.json"
README_PATH = ROOT / "README.md"
AGENTS_PATH = ROOT / "AGENTS.md"

VALID_LEVELS = {
    "beginner",
    "beginner-intermediate",
    "intermediate",
    "intermediate-advanced",
    "advanced",
    "beginner-advanced",
}
VALID_STATUSES = {
    "planned",
    "draft",
    "maintained",
    "needs-review",
    "deprecated",
    "archived",
}
FORBIDDEN_PATTERNS = [
    re.compile(r"TODO\s*:\s*implement later", re.IGNORECASE),
    re.compile(r"\bPLACEHOLDER\b"),
    re.compile(r"\bFIXME\b"),
]
LOCAL_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]*)\)")
ANCHOR_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # --- 1. Struktur direktori skill -------------------------------------
    skill_dirs = sorted(
        d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")
    )
    for d in skill_dirs:
        guide = d / f"{d.name}.md"
        if not (d / "README.md").is_file():
            errors.append(f"[struktur] {d.name}: README.md tidak ada")
        if not guide.is_file():
            errors.append(f"[struktur] {d.name}: {d.name}.md tidak ada")

    # --- 2. Manifest sinkron dengan direktori ------------------------------
    if not MANIFEST_PATH.is_file():
        errors.append("[manifest] skills/manifest.json tidak ditemukan")
        manifest = {"skills": [], "categories": {}}
    else:
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"[manifest] JSON tidak valid: {exc}")
            manifest = {"skills": [], "categories": {}}

    manifest_ids = {s.get("id") for s in manifest.get("skills", []) if isinstance(s, dict)}
    dir_ids = {d.name for d in skill_dirs}

    for missing in sorted(dir_ids - manifest_ids):
        errors.append(f"[manifest] direktori {missing}/ tidak ada di manifest")
    for extra in sorted(manifest_ids - dir_ids):
        errors.append(f"[manifest] id {extra} di manifest tanpa direktori")

    # --- 3. Validasi metadata manifest --------------------------------------
    categories = set(manifest.get("categories", {}).keys())

    interval = manifest.get("review_interval_days")
    if not isinstance(interval, int) or interval <= 0:
        errors.append(
            f"[manifest] review_interval_days harus bilangan bulat positif, got {interval!r}"
        )

    seen_ids: set[str] = set()
    for entry in manifest.get("skills", []):
        if not isinstance(entry, dict):
            errors.append("[manifest] entri skill bukan objek")
            continue
        sid = entry.get("id")
        if not sid:
            errors.append("[manifest] entri skill tanpa id")
            continue
        if sid in seen_ids:
            errors.append(f"[manifest] id duplikat: {sid}")
        seen_ids.add(sid)

        if entry.get("category") not in categories:
            errors.append(
                f"[manifest] {sid}: kategori '{entry.get('category')}' tidak terdaftar"
            )
        if entry.get("level") not in VALID_LEVELS:
            errors.append(
                f"[manifest] {sid}: level tidak dikenal '{entry.get('level')}'"
            )
        if entry.get("status") not in VALID_STATUSES:
            errors.append(
                f"[manifest] {sid}: status tidak dikenal '{entry.get('status')}'"
            )

        for field in ("overview", "guide"):
            path = entry.get(field)
            if not path:
                errors.append(f"[manifest] {sid}: field '{field}' kosong")
            elif not (ROOT / path).is_file():
                errors.append(f"[manifest] {sid}: {field} menunjuk file tidak ada: {path}")

        last_reviewed = entry.get("last_reviewed")
        if not last_reviewed:
            errors.append(f"[manifest] {sid}: field 'last_reviewed' kosong")
        else:
            try:
                datetime.strptime(last_reviewed, "%Y-%m-%d")
            except ValueError:
                errors.append(
                    f"[manifest] {sid}: last_reviewed bukan tanggal ISO (YYYY-MM-DD): {last_reviewed}"
                )

    # --- 4. Placeholder dan karakter kontrol di file skill ------------------
    md_files = sorted(SKILLS_DIR.rglob("*.md"))
    for f in md_files:
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"[encoding] {f}: bukan UTF-8 valid")
            continue
        if "\x00" in text:
            errors.append(f"[kontrol] {f}: mengandung karakter NUL")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"[placeholder] {f}: cocok dengan {pattern.pattern}")

    for path in (README_PATH, AGENTS_PATH):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "\x00" in text:
            errors.append(f"[kontrol] {path.name}: mengandung karakter NUL")

    # --- 5. Link lokal Markdown di dalam skill -------------------------------
    for f in md_files:
        rel = f.relative_to(ROOT)
        text = f.read_text(encoding="utf-8")
        for match in LOCAL_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if "://" in target:
                continue
            if "#" in target:
                target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (f.parent / target).resolve()
            if not resolved.is_file():
                errors.append(f"[link] {rel}: target tidak ada -> {target}")

    # --- 6. README utama menautkan semua skill --------------------------------
    if README_PATH.is_file():
        readme_text = README_PATH.read_text(encoding="utf-8")
        for d in skill_dirs:
            if f"./skills/{d.name}/" not in readme_text:
                errors.append(f"[katalog] README.md tidak menautkan ./skills/{d.name}/")

        # Pastikan jumlah total yang diklaim sesuai manifest
        claim = re.search(r"Kumpulan \*\*(\d+) skills\*\*", readme_text)
        if claim:
            expected = len(skill_dirs)
            if int(claim.group(1)) != expected:
                errors.append(
                    f"[katalog] README.md mengklaim {claim.group(1)} skills, "
                    f"aktual {expected}"
                )

    # --- Laporan -----------------------------------------------------------------
    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"❌ Validasi gagal — {len(errors)} masalah:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"✅ Validasi sukses — {len(skill_dirs)} skill, {len(md_files)} file Markdown, manifest sinkron.")
    return 0


if __name__ == "__main__":
    sys.exit(main())