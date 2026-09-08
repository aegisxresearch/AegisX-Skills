#!/usr/bin/env python3
"""Generator katalog README.md dari skills/manifest.json.

Menghasilkan ulang bagian daftar skill (di antara marker
<!-- CATALOG_START --> dan <!-- CATALOG_END -->) pada README.md.
Bagian lain README (badges, intro, jalur belajar, kontribusi, lisensi)
tidak diubah. Menulis ulang README hanya jika output berbeda.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_paths import load_hours, render_readme_section

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
README_PATH = ROOT / "README.md"

START_MARKER = "<!-- CATALOG_START -->"
END_MARKER = "<!-- CATALOG_END -->"
PATHS_START_MARKER = "<!-- PATHS_START -->"
PATHS_END_MARKER = "<!-- PATHS_END -->"

LEVEL_DISPLAY = {
    "beginner": "Beginner",
    "beginner-intermediate": "Beginner–Intermediate",
    "intermediate": "Intermediate",
    "intermediate-advanced": "Intermediate–Advanced",
    "advanced": "Advanced",
    "beginner-advanced": "Beginner–Advanced",
}


def build_catalog(manifest: dict) -> str:
    categories = manifest.get("categories", {})
    skills = manifest.get("skills", [])

    # Kelompokkan skill per kategori, pertahankan urutan kategori dari manifest.
    by_category: dict[str, list[dict]] = {}
    for skill in skills:
        by_category.setdefault(skill.get("category", ""), []).append(skill)
    for key in by_category:
        by_category[key].sort(key=lambda s: s.get("id", ""))

    lines = [
        "## Daftar Skills",
        "",
        "Katalog ini dihasilkan secara otomatis dari "
        "[`skills/manifest.json`](./skills/manifest.json) oleh "
        "[`scripts/generate-readme.py`](./scripts/generate-readme.py). "
        "Jangan mengedit bagian ini secara manual.",
        "",
    ]

    for cat_key, cat_title in categories.items():
        cat_skills = by_category.get(cat_key)
        if not cat_skills:
            continue
        lines.append(f"### {cat_title}")
        lines.append("")
        lines.append("| Skill | Level | Deskripsi |")
        lines.append("|-------|-------|-----------|")
        for skill in cat_skills:
            sid = skill["id"]
            level = LEVEL_DISPLAY.get(skill.get("level", ""), skill.get("level", ""))
            lines.append(
                f"| [`{sid}`](./skills/{sid}/) | {level} | {skill.get('summary', '')} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    if not MANIFEST_PATH.is_file():
        print(f"❌ Manifest tidak ditemukan: {MANIFEST_PATH}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    readme = README_PATH.read_text(encoding="utf-8")
    if START_MARKER not in readme or END_MARKER not in readme:
        print(
            "❌ Marker katalog tidak ditemukan di README.md. "
            "Tambahkan <!-- CATALOG_START --> dan <!-- CATALOG_END -->.",
            file=sys.stderr,
        )
        return 1

    start_idx = readme.index(START_MARKER)
    end_idx = readme.index(END_MARKER) + len(END_MARKER)

    catalog = build_catalog(manifest)
    new_readme = (
        readme[:start_idx] + START_MARKER + "\n\n" + catalog + END_MARKER + readme[end_idx:]
    )

    # Regenerate Jalur Belajar section from learning_paths module
    hours = load_hours()
    paths_section = render_readme_section(hours)
    if PATHS_START_MARKER in new_readme and PATHS_END_MARKER in new_readme:
        p_start = new_readme.index(PATHS_START_MARKER)
        p_end = new_readme.index(PATHS_END_MARKER) + len(PATHS_END_MARKER)
        paths_block = PATHS_START_MARKER + "\n\n" + paths_section + PATHS_END_MARKER
        new_readme = new_readme[:p_start] + paths_block + new_readme[p_end:]

    if new_readme == readme:
        print("✅ Katalog README sudah sinkron, tidak ada perubahan.")
        return 0

    README_PATH.write_text(new_readme, encoding="utf-8")
    count = len(manifest.get("skills", []))
    print(f"✅ Katalog README diperbarui — {count} skill dari manifest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
