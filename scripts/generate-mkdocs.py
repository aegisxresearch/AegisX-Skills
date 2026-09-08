#!/usr/bin/env python3
"""Generator situs MkDocs dari skills/manifest.json.

Strategi:
1. Menyinkronkan markdown skill + manifest.json ke `docs/skills/` dan
   menyalin `CONTRIBUTING.md` ke `docs/`. `docs/` adalah artefak build
   (gitignored), jadi `skills/` tetap satu-satunya source of truth.
2. Menghasilkan `docs/index.md` — halaman home yang menautkan overview
   dan guide tiap skill.
3. Menghasilkan `mkdocs.yml` dengan `docs_dir: docs` (direktori anak dari
   config, sesuai aturan MkDocs 1.6+).

Idempotent: file tidak ditulis ulang jika isinya sama.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
DOCS_DIR = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
INDEX_PATH = DOCS_DIR / "index.md"

LEVEL_DISPLAY = {
    "beginner": "Beginner",
    "beginner-intermediate": "Beginner–Intermediate",
    "intermediate": "Intermediate",
    "intermediate-advanced": "Intermediate–Advanced",
    "advanced": "Advanced",
    "beginner-advanced": "Beginner–Advanced",
}


def _copy_if_changed(src: Path, dst: Path) -> bool:
    if dst.is_file() and dst.read_bytes() == src.read_bytes():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def sync_docs() -> list[str]:
    """Salin markdown skill, manifest, dan CONTRIBUTING ke docs/. Kembalikan file yang berubah."""
    changed: list[str] = []

    for src in sorted((ROOT / "skills").rglob("*.md")):
        rel = src.relative_to(ROOT / "skills")
        if _copy_if_changed(src, DOCS_DIR / "skills" / rel):
            changed.append(f"docs/skills/{rel}")

    manifest_src = ROOT / "skills" / "manifest.json"
    if _copy_if_changed(manifest_src, DOCS_DIR / "skills" / "manifest.json"):
        changed.append("docs/skills/manifest.json")

    if _copy_if_changed(ROOT / "CONTRIBUTING.md", DOCS_DIR / "CONTRIBUTING.md"):
        changed.append("docs/CONTRIBUTING.md")

    return changed


def build_mkdocs(manifest: dict) -> str:
    categories = manifest.get("categories", {})
    skills = manifest.get("skills", [])

    by_category: dict[str, list[dict]] = {}
    for skill in skills:
        by_category.setdefault(skill.get("category", ""), []).append(skill)
    for key in by_category:
        by_category[key].sort(key=lambda s: s.get("id", ""))

    nav = ["  - Home: index.md"]
    for cat_key, cat_title in categories.items():
        cat_skills = by_category.get(cat_key)
        if not cat_skills:
            continue
        nav.append(f"  - {cat_title}:")
        for skill in cat_skills:
            sid = skill["id"]
            nav.append(f"      - {sid}: skills/{sid}/README.md")
            nav.append(f"      - {sid} — Panduan Lengkap: skills/{sid}/{sid}.md")
    nav.append("  - Kontribusi: CONTRIBUTING.md")

    return f"""\
site_name: AegisX Skills Collection
site_description: "Panduan engineering: backend, frontend, AI, data, DevOps, security."
site_url: https://aegisxresearch.github.io/AegisX-Skills/
repo_url: https://github.com/aegisxresearch/AegisX-Skills
docs_dir: docs
site_dir: site
theme:
  name: material
  features:
    - navigation.sections
    - navigation.expand
    - content.code.copy
    - toc.integrate
  palette:
    scheme: slate
    primary: indigo
    accent: indigo
markdown_extensions:
  - admonition
  - toc:
      permalink: true
  - pymdownx.superfences
nav:
{chr(10).join(nav)}
"""


def build_index(manifest: dict) -> str:
    categories = manifest.get("categories", {})
    skills = manifest.get("skills", [])

    by_category: dict[str, list[dict]] = {}
    for skill in skills:
        by_category.setdefault(skill.get("category", ""), []).append(skill)
    for key in by_category:
        by_category[key].sort(key=lambda s: s.get("id", ""))

    lines = [
        "# 🚀 AegisX Skills Collection",
        "",
        "Kumpulan panduan engineering terstruktur: Backend API, Frontend, AI/ML, "
        "Database, DevOps, Cloud, dan Security.",
        "",
        "> Dokumen ini dihasilkan secara otomatis dari "
        "[`skills/manifest.json`](./skills/manifest.json). Jangan mengedit secara manual.",
        "",
    ]

    for cat_key, cat_title in categories.items():
        cat_skills = by_category.get(cat_key)
        if not cat_skills:
            continue
        lines.append(f"## {cat_title}")
        lines.append("")
        lines.append("| Skill | Level | Deskripsi |")
        lines.append("|-------|-------|-----------|")
        for skill in cat_skills:
            sid = skill["id"]
            level = LEVEL_DISPLAY.get(skill.get("level", ""), skill.get("level", ""))
            links = (
                f"[overview](./skills/{sid}/README.md) · "
                f"[panduan](./skills/{sid}/{sid}.md)"
            )
            lines.append(f"| **{sid}** ({links}) | {level} | {skill.get('summary', '')} |")
        lines.append("")

    lines += [
        "---",
        "",
        "## Kontribusi",
        "",
        "Lihat [CONTRIBUTING.md](./CONTRIBUTING.md).",
        "Situs ini dibangun otomatis dari `manifest.json` oleh GitHub Actions.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _write_if_changed(path: Path, content: str) -> bool:
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    if not MANIFEST_PATH.is_file():
        print(f"❌ Manifest tidak ditemukan: {MANIFEST_PATH}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    synced = sync_docs()
    mkdocs_changed = _write_if_changed(MKDOCS_YML, build_mkdocs(manifest))
    index_changed = _write_if_changed(INDEX_PATH, build_index(manifest))

    count = len(manifest.get("skills", []))
    if synced or mkdocs_changed or index_changed:
        print(
            f"✅ docs/ disinkronkan ({len(synced)} file), "
            f"mkdocs.yml {('diperbarui' if mkdocs_changed else 'sama')}, "
            f"index.md {('diperbarui' if index_changed else 'sama')} — {count} skill."
        )
    else:
        print(f"✅ docs/, mkdocs.yml, dan index.md sudah sinkron — {count} skill.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
