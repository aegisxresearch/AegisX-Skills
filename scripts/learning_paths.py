#!/usr/bin/env python3
"""Single source of truth untuk Jalur Belajar (learning paths).

Definisi jalur memakai skill ID dari manifest sehingga jam total
bisa dihitung ulang otomatis. Dua output dari satu sumber:
1. README.md — section Jalur Belajar + tabel badge per jalur
2. docs/learning-paths.md — halaman situs dokumentasi

Aturan perhitungan:
- Jam per skill diambil dari difficulty_hours di manifest.
- Skill alternatif (dipisah "atau") dihitung sebagai rentang:
  total minimum memakai opsi terpendek, total maksimum opsi terpanjang.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "skills" / "manifest.json"


@dataclass
class PathStep:
    """Satu langkah dalam jalur: satu skill atau alternatif beberapa skill."""

    options: list[str]  # skill IDs; >1 berarti alternatif ("atau")


@dataclass
class LearningPath:
    key: str
    title: str
    audience: str
    steps: list[PathStep] = field(default_factory=list)


PATHS: list[LearningPath] = [
    LearningPath(
        key="web-fullstack",
        title="Web Full-Stack",
        audience="Engineer yang membangun aplikasi web end-to-end: dari desain API sampai deploy dan monitoring.",
        steps=[
            PathStep(["system-design-architect"]),
            PathStep(["api-design-patterns"]),
            PathStep(["auth-implementation-guide"]),
            PathStep(["postgresql-master"]),
            PathStep(["postgresql-query-tuning"]),
            PathStep(["react-nextjs-patterns"]),
            PathStep(["design-system-builder"]),
            PathStep(["accessibility-wcag"]),
            PathStep(["frontend-testing-playbook"]),
            PathStep(["api-observability"]),
            PathStep(["docker-production-checklist"]),
            PathStep(["ci-cd-production"]),
            PathStep(["github-actions-workflows"]),
        ],
    ),
    LearningPath(
        key="ai-ml",
        title="AI/ML Pipeline",
        audience="Engineer yang membangun aplikasi LLM atau pipeline ML produksi.",
        steps=[
            PathStep(["data-engineering-pipelines"]),
            PathStep(["rag-pipeline-architect", "llm-application-engineering"]),
            PathStep(["ml-evaluation-mlops"]),
            PathStep(["api-observability"]),
            PathStep(["opentelemetry-tracing"]),
            PathStep(["cybersecurity-fundamentals"]),
        ],
    ),
    LearningPath(
        key="platform-infra",
        title="Platform & Infra",
        audience="Engineer yang mengelola infrastruktur, cluster, dan pipeline deployment.",
        steps=[
            PathStep(["threat-modeling-stride"]),
            PathStep(["secrets-management"]),
            PathStep(["terraform-infrastructure"]),
            PathStep(["kubernetes-production"]),
            PathStep(["gitops-kubernetes"]),
            PathStep(["ci-cd-production"]),
            PathStep(["github-actions-workflows"]),
            PathStep(["sast-dependency-scanning"]),
            PathStep(["supply-chain-security"]),
            PathStep(["incident-response-sre"]),
        ],
    ),
    LearningPath(
        key="security",
        title="Security Engineer",
        audience="Engineer yang fokus pada keamanan aplikasi dan infrastruktur.",
        steps=[
            PathStep(["threat-modeling-stride"]),
            PathStep(["cybersecurity-fundamentals"]),
            PathStep(["auth-implementation-guide"]),
            PathStep(["api-security-hardening"]),
            PathStep(["sast-dependency-scanning"]),
            PathStep(["security-testing-dast-sast"]),
            PathStep(["zero-trust-application-security"]),
            PathStep(["gdpr-data-privacy"]),
        ],
    ),
    LearningPath(
        key="observability-sre",
        title="Observability & SRE",
        audience="Engineer yang menjaga reliability: metrik, tracing, alerting, dan respons insiden.",
        steps=[
            PathStep(["api-observability"]),
            PathStep(["opentelemetry-tracing"]),
            PathStep(["observability-prometheus-grafana"]),
            PathStep(["prometheus-alerting-slo"]),
            PathStep(["kubernetes-production"]),
            PathStep(["incident-response-sre"]),
        ],
    ),
    LearningPath(
        key="mobile",
        title="Mobile",
        audience="Engineer yang membangun aplikasi mobile produksi.",
        steps=[
            PathStep(["react-native-expo", "flutter-development"]),
            PathStep(["pwa-offline-first"]),
            PathStep(["api-security-hardening"]),
            PathStep(["api-observability"]),
            PathStep(["ci-cd-production"]),
        ],
    ),
]


def load_hours() -> dict[str, int]:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {s["id"]: s.get("difficulty_hours", 0) for s in manifest["skills"]}


def path_hours(path: LearningPath, hours: dict[str, int]) -> tuple[int, int]:
    """Return (min, max) total jam untuk jalur."""
    total_min = 0
    total_max = 0
    for step in path.steps:
        option_hours = [hours.get(sid, 0) for sid in step.options]
        total_min += min(option_hours)
        total_max += max(option_hours)
    return total_min, total_max


def path_skill_count(path: LearningPath) -> int:
    return sum(len(step.options) for step in path.steps)


def render_step(step: PathStep, hours: dict[str, int], link: bool) -> str:
    """Render satu langkah; link hanya untuk README (relative path)."""
    names = []
    for sid in step.options:
        h = hours.get(sid, 0)
        label = f"{sid} ({h}h)"
        if link:
            names.append(f"[{label}](./skills/{sid}/)")
        else:
            names.append(label)
    return " atau ".join(names)


def gh_slug(title: str) -> str:
    """GitHub-compatible heading anchor slug."""
    s = title.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)  # hapus tanda baca termasuk & dan /
    return s.replace(" ", "-")


def render_readme_section(hours: dict[str, int]) -> str:
    """Section Jalur Belajar lengkap untuk README (dengan badge table)."""
    lines = [
        "## Jalur Belajar",
        "",
        "Setiap jalur menunjukkan urutan skill yang sebaiknya dipelajari.",
        "Estimasi jam dihitung otomatis dari `difficulty_hours` di manifest",
        "oleh `scripts/learning_paths.py` — jangan mengedit bagian ini manual.",
        "",
        "| Jalur | Skill | Durasi |",
        "|-------|-------|--------|",
    ]
    for path in PATHS:
        lo, hi = path_hours(path, hours)
        dur = f"{lo}-{hi} jam" if lo != hi else f"{lo} jam"
        anchor = gh_slug(path.title)
        lines.append(
            f"| [{path.title}](#{anchor}) | {path_skill_count(path)} skill | {dur} |"
        )
    lines.append("")

    for path in PATHS:
        lo, hi = path_hours(path, hours)
        dur = f"{lo}-{hi} jam" if lo != hi else f"{lo} jam"
        anchor = gh_slug(path.title)
        lines.append(f"### {path.title}")
        lines.append("")
        lines.append(f"{path.audience}")
        lines.append("")
        lines.append("```text")
        rendered = [render_step(step, hours, link=False) for step in path.steps]
        # Wrap menjadi baris ~72 karakter
        current = ""
        for item in rendered:
            piece = f"-> {item}" if current else item
            if len(current) + len(piece) + 3 > 72 and current:
                lines.append(current)
                current = piece
            else:
                current = f"{current} -> {item}" if current else item
        if current:
            lines.append(current)
        lines.append(f"Total: ~{dur}")
        lines.append("```")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_docs_page(hours: dict[str, int]) -> str:
    """Halaman learning paths untuk situs MkDocs."""
    lines = [
        "# Jalur Belajar",
        "",
        "Enam jalur belajar terstruktur. Jam per skill dihitung dari",
        "`difficulty_hours` di manifest; urutan mengikuti dependencies.",
        "",
        "| Jalur | Skill | Durasi |",
        "|-------|-------|--------|",
    ]
    for path in PATHS:
        lo, hi = path_hours(path, hours)
        dur = f"{lo}-{hi} jam" if lo != hi else f"{lo} jam"
        lines.append(f"| [{path.title}](#{path.key}) | {path_skill_count(path)} skill | {dur} |")
    lines.append("")

    for path in PATHS:
        lo, hi = path_hours(path, hours)
        dur = f"{lo}-{hi} jam" if lo != hi else f"{lo} jam"
        lines.append(f"## {path.title}")
        lines.append("")
        lines.append(path.audience)
        lines.append("")
        lines.append("| # | Skill | Jam |")
        lines.append("|---|-------|-----|")
        for i, step in enumerate(path.steps, 1):
            for sid in step.options:
                h = hours.get(sid, 0)
                lines.append(
                    f"| {i} | [`{sid}`](./skills/{sid}/README.md) | {h} |"
                )
        lines.append(f"| | **Total** | **~{dur}** |")
        lines.append("")

    lines += [
        "---",
        "",
        '<div class="watermark">',
        "<em>Dokumentasi engineering yang ditulis oleh engineer, untuk engineer.</em>",
        "<br>",
        "<small>AegisX Research | "
        "[GitHub](https://github.com/aegisxresearch) | "
        "Konten ini bukan hasil AI generation.</small>",
        "</div>",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    h = load_hours()
    print(render_readme_section(h))
