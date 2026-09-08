#!/usr/bin/env python3
"""Pemeriksa jadwal review skill berdasarkan skills/manifest.json.

Skill dianggap perlu review jika `last_reviewed` lebih lama dari
`review_interval_days` (default 180). Berguna untuk CI: jika ada skill
yang perlu review, keluar kode 1 (atau menulis issue body ke --output).

Output:
- stdout: daftar skill yang perlu review (jika ada).
- GITHUB_OUTPUT: due=true/false agar workflow bisa mengambil keputusan.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
DEFAULT_INTERVAL_DAYS = 180


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Tulis body issue markdown ke file (jika ada skill yang perlu review).",
    )
    parser.add_argument(
        "--interval-days",
        type=int,
        default=None,
        help=f"Override interval review (default dari manifest: {DEFAULT_INTERVAL_DAYS}).",
    )
    args = parser.parse_args()

    if not MANIFEST_PATH.is_file():
        print(f"❌ Manifest tidak ditemukan: {MANIFEST_PATH}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    interval = args.interval_days or manifest.get("review_interval_days", DEFAULT_INTERVAL_DAYS)
    today = date.today()

    due: list[tuple[str, str, str]] = []
    for skill in manifest.get("skills", []):
        sid = skill.get("id", "?")
        last_reviewed_raw = skill.get("last_reviewed")
        try:
            last_reviewed = parse_date(last_reviewed_raw)
        except (TypeError, ValueError):
            due.append((sid, last_reviewed_raw or "missing", "metadata tidak valid"))
            continue
        days = (today - last_reviewed).days
        if days > interval:
            due.append((sid, str(last_reviewed), f"{days} hari lalu (interval {interval} hari)"))

    due.sort()
    if due:
        print(f"⚠️  {len(due)} skill melewati interval review ({interval} hari):")
        for sid, last, detail in due:
            print(f"  - {sid}: last_reviewed={last} ({detail})")
        body = (
            "## Skill perlu review\n\n"
            "Skill berikut melewati interval review. "
            "Perbarui `last_reviewed` di `skills/manifest.json` setelah konten direview "
            "(atau ubah `status` menjadi `needs-review`/`deprecated`).\n\n"
            "| Skill | last_reviewed | Catatan |\n"
            "|-------|---------------|---------|\n"
        )
        for sid, last, detail in due:
            body += f"| `{sid}` | {last} | {detail} |\n"
        if args.output:
            Path(args.output).write_text(body, encoding="utf-8")
        _emit_github_output("due", "true")
        return 1

    print(f"✅ Semua {len(manifest.get('skills', []))} skill masih dalam interval review.")
    _emit_github_output("due", "false")
    return 0


def _emit_github_output(key: str, value: str) -> None:
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"{key}={value}\n")


if __name__ == "__main__":
    sys.exit(main())