#!/usr/bin/env python3
"""Generator situs MkDocs dari skills/manifest.json.

Strategi:
1. Menyinkronkan markdown skill + manifest.json ke `docs/skills/`, menyalin
   `CONTRIBUTING.md` ke `docs/`, dan menyalin aset brand dari `assets/`
   ke `docs/assets/`. `docs/` adalah artefak build (gitignored), jadi
   `skills/` dan `assets/` tetap source of truth.
2. Menghasilkan `docs/index.md` — halaman home dengan hero, statistik,
   kartu kategori, jalur belajar, dan FAQ.
3. Menghasilkan `mkdocs.yml` dengan `docs_dir: docs`, tema Material
   berkustom (logo, font, palette, extra CSS).

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
ASSETS_DIR = ROOT / "assets"
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

CAT_ICONS = {
    "backend-api": "⚙️",
    "ai-ml": "🤖",
    "frontend": "🎨",
    "database-data": "🗄️",
    "architecture-reliability": "🏛️",
    "devops-cloud": "☁️",
    "security": "🔐",
    "anti-slop-quality": "🛡️",
    "programming-workflow": "💻",
    "mobile": "📱",
}


def _copy_if_changed(src: Path, dst: Path) -> bool:
    if dst.is_file() and dst.read_bytes() == src.read_bytes():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def sync_docs() -> list[str]:
    """Salin markdown skill, manifest, CONTRIBUTING, dan aset brand ke docs/."""
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

    if ASSETS_DIR.is_dir():
        for src in sorted(ASSETS_DIR.rglob("*")):
            if src.is_file():
                rel = src.relative_to(ASSETS_DIR)
                if _copy_if_changed(src, DOCS_DIR / "assets" / rel):
                    changed.append(f"docs/assets/{rel}")

    return changed


def _group_by_category(manifest: dict) -> dict[str, list[dict]]:
    by_category: dict[str, list[dict]] = {}
    for skill in manifest.get("skills", []):
        by_category.setdefault(skill.get("category", ""), []).append(skill)
    for key in by_category:
        by_category[key].sort(key=lambda s: s.get("id", ""))
    return by_category


def build_mkdocs(manifest: dict) -> str:
    categories = manifest.get("categories", {})
    by_category = _group_by_category(manifest)

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
  logo: assets/logo.png
  favicon: assets/favicon.png
  icon:
    repo: fontawesome/brands/github
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.sections
    - navigation.expand
    - navigation.top
    - content.code.copy
    - toc.integrate
    - search.highlight
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: amber
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: amber
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
extra_css:
  - assets/extra.css
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/aegisxresearch
markdown_extensions:
  - admonition
  - toc:
      permalink: true
  - pymdownx.superfences
  - pymdownx.details
nav:
{chr(10).join(nav)}
"""


def _cat_card(cat_key: str, cat_title: str, count: int) -> str:
    icon = CAT_ICONS.get(cat_key, "📘")
    return (
        f'<a class="cat-card" href="#kategori-{cat_key}">'
        f'<span class="cat-icon">{icon}</span>'
        f"<strong>{cat_title}</strong>"
        f'<span class="cat-count">{count} skill</span></a>'
    )


def build_index(manifest: dict) -> str:
    categories = manifest.get("categories", {})
    by_category = _group_by_category(manifest)
    total = len(manifest.get("skills", []))

    lines = [
        "# AegisX Skills Collection",
        "",
        "<div class=\"hero\">",
        "<img class=\"hero-logo\" src=\"./assets/logo.png\" alt=\"AegisX\">",
        "<h1>AegisX Skills Collection</h1>",
        f"<p>Kumpulan <strong>{total} panduan engineering terstruktur</strong> untuk "
        "programmer, software engineer, DevOps, security, dan ML engineer.</p>",
        "<p class=\"hero-cta\">",
        '<a class="md-button md-button--primary" href="#daftar-skill">Jelajahi Skill</a>',
        '<a class="md-button" href="#jalur-belajar">Jalur Belajar</a>',
        "</p>",
        "</div>",
        "",
        "> Dokumen ini dihasilkan secara otomatis dari "
        "[`skills/manifest.json`](./skills/manifest.json). Jangan mengedit secara manual.",
        "",
        "## Statistik",
        "",
        "| Metrik | Nilai |",
        "|--------|-------|",
        f"| Total skill | {total} |",
        f"| Kategori | {len(categories)} |",
        f"| Backend API | {len(by_category.get('backend-api', []))} |",
        f"| Frontend | {len(by_category.get('frontend', []))} |",
        f"| Mobile | {len(by_category.get('mobile', []))} |",
        f"| AI/ML | {len(by_category.get('ai-ml', []))} |",
        f"| Database/Data | {len(by_category.get('database-data', []))} |",
        f"| DevOps/Cloud | {len(by_category.get('devops-cloud', []))} |",
        f"| Security | {len(by_category.get('security', []))} |",
        "",
        "## Daftar Skill per Kategori",
        "",
        '<h2 id="daftar-skill" hidden></h2>',
        "<div class=\"cat-grid\">",
    ]
    for cat_key, cat_title in categories.items():
        count = len(by_category.get(cat_key, []))
        if count:
            lines.append(_cat_card(cat_key, cat_title, count))
    lines.append("</div>")

    for cat_key, cat_title in categories.items():
        cat_skills = by_category.get(cat_key)
        if not cat_skills:
            continue
        lines.append(f'<h2 id="kategori-{cat_key}">{cat_title}</h2>')
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
        '<h2 id="jalur-belajar">Jalur Belajar</h2>',
        "",
        "**Aplikasi web:** System Design → API Design → Authentication → "
        "PostgreSQL/Prisma → React/Next.js → Testing → Observability → CI/CD",
        "",
        "**Aplikasi AI:** Data Engineering → RAG/LLM Application → Evaluation/MLOps "
        "→ API Observability → Security",
        "",
        "**Aplikasi mobile:** React Native/Expo atau Flutter → Offline & state → "
        "Push → API Security → Store Release",
        "",
        "---",
        "",
        "## FAQ",
        "",
        "**Apakah contoh kode siap dipakai produksi?**\\n",
        "Contoh diberi label jujur (`runnable`, `illustrative`, `pseudo-code`) dan "
        "harus disesuaikan dengan stack serta threat model Anda.",
        "",
        "**Bagaimana menambahkan skill baru?**\\n",
        "Buat folder `skills/<nama-skill>/` (README + panduan), daftarkan di "
        "`skills/manifest.json`, lalu jalankan `scripts/generate-readme.py` dan "
        "`scripts/validate-skills.py`.",
        "",
        "**Bagaimana CI menjaga kualitas?**\\n",
        "Workflow Skills Validation memeriksa struktur, metadata, link, dan sinkronisasi "
        "katalog; workflow Docs membangun situs secara strict dan deploy ke GitHub Pages.",
        "",
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
