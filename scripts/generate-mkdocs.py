#!/usr/bin/env python3
"""Generator konfigurasi MkDocs dan halaman home dari skills/manifest.json.

Menghasilkan:
1. `mkdocs.yml` — nav dikelompokkan per kategori dari manifest.
2. `docs_index.md` — halaman home yang menautkan overview dan guide tiap skill.

Idempotent: tidak menulis file jika isinya sama dengan yang sudah ada.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
MKDOCS_YML = ROOT / "mkdocs.yml"
INDEX_PATH = ROOT / "docs_index.md"

LEVEL_DISPLAY = {
    "beginner": "Beginner",
    "beginner-intermediate": "Beginner–Intermediate",
    "intermediate": "Intermediate",
    "intermediate-advanced": "Intermediate–Advanced",
    "advanced": "Advanced",
    "beginner-advanced": "Beginner–Advanced",
}

EXCLUDE_DOCS = [
    "/.github/",
    "/.freebuff/",
    "/.venv/",
    "/scripts/",
    "/site/",
    "/AGENTS.md",
    "/LICENSE",
    "/requirements-docs.txt",
    "/ruff.toml",
    "/mkdocs.yml",
]


def _indent(lines: list[str], spaces: int = 2) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line for line in lines) + "\n"


def build_mkdocs(manifest: dict, index_name: str) -> str:
    categories = manifest.get("categories", {})
    skills = manifest.get("skills", [])

    by_category: dict[str, list[dict]] = {}
    for skill in skills:
        by_category.setdefault(skill.get("category", ""), []).append(skill)
    for key in by_category:
        by_category[key].sort(key=lambda s: s.get("id", ""))

    nav = ["  - Home: docs_index.md"]
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
site_description: "Kumpulan panduan engineering terstruktur: backend, frontend, AI/ML, database, DevOps, dan security."
site_url: https://aegisxresearch.github.io/AegisX-Skills/
repo_url: https://github.com/aegisxresearch/AegisX-Skills
docs_dir: .
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
exclude_docs: |
{_indent(EXCLUDE_DOCS)}markdown_extensions:
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
        "[`skills/manifest.json`](./skills/manifest.json). "
        "Jangan mengedit secara manual.",
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
        "Lihat [CONTRIBUTING.md](./CONTRIBUTING.md). ",
        "Situs ini dibangun otomatis dari `manifest.json` oleh GitHub Actions.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def write_if_changed(path: Path, content: str) -> bool:
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    if not MANIFEST_PATH.is_file():
        print(f"❌ Manifest tidak ditemukan: {MANIFEST_PATH}", file=sys.stderr)
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    mkdocs_changed = write_if_changed(MKDOCS_YML, build_mkdocs(manifest, "docs_index.md"))
    index_changed = write_if_changed(INDEX_PATH, build_index(manifest))

    count = len(manifest.get("skills", []))
    if mkdocs_changed or index_changed:
        print(f"✅ mkdocs.yml / docs_index.md diperbarui — {count} skill dari manifest.")
    else:
        print("✅ mkdocs.yml / docs_index.md sudah sinkron, tidak ada perubahan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())