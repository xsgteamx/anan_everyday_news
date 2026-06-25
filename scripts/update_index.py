#!/usr/bin/env python3
"""Update README and archive indexes for the HTML homepage workflow.

Rules:
- Current page is root index.html.
- Archived pages live in archive/YYYY/MM/YYYY-MM-DD.html.
- index/YYYY.md and index/YYYY-MM.md are lightweight navigation files.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_RE = re.compile(r"^archive/(\d{4})/(\d{2})/(\d{4}-\d{2}-\d{2})\.html$")
README_START = "<!-- archive-index:start -->"
README_END = "<!-- archive-index:end -->"


def archive_pages() -> list[Path]:
    pages = []
    for path in ROOT.glob("archive/*/*/*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if ARCHIVE_RE.match(rel):
            pages.append(path)
    return sorted(pages, reverse=True)


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    title_match = re.search(r"<title>(.*?)</title>", text, flags=re.S)
    if title_match:
        return re.sub(r"\s+", " ", title_match.group(1)).strip()
    h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.S)
    if h1_match:
        return re.sub(r"<.*?>", "", h1_match.group(1)).strip()
    return path.stem


def replace_between_markers(text: str, replacement: str) -> str:
    if README_START not in text or README_END not in text:
        return text
    before = text.split(README_START, 1)[0]
    after = text.split(README_END, 1)[1]
    return f"{before}{README_START}\n{replacement}\n{README_END}{after}"


def update_readme(pages: list[Path]) -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        return
    latest = pages[:10]
    replacement = "\n".join(f"- [{path.stem}]({path.relative_to(ROOT).as_posix()})" for path in latest) if latest else "- 暂无归档"
    text = readme.read_text(encoding="utf-8")
    readme.write_text(replace_between_markers(text, replacement), encoding="utf-8")


def update_indexes(pages: list[Path]) -> None:
    index_dir = ROOT / "index"
    index_dir.mkdir(exist_ok=True)

    grouped: dict[str, dict[str, list[Path]]] = defaultdict(lambda: defaultdict(list))
    for path in pages:
        match = ARCHIVE_RE.match(path.relative_to(ROOT).as_posix())
        if not match:
            continue
        year, month, _date = match.groups()
        grouped[year][month].append(path)

    for year, months in grouped.items():
        year_lines = [f"# {year} 年归档索引", "", "## 月份", ""]
        for month in sorted(months):
            year_lines.append(f"- [{year} 年 {int(month)} 月]({year}-{month}.md)")
        year_lines.append("")
        (index_dir / f"{year}.md").write_text("\n".join(year_lines), encoding="utf-8")

        for month, month_pages in months.items():
            rows = [
                f"# {year} 年 {int(month)} 月归档索引",
                "",
                "## 历史页面",
                "",
                "| 日期 | 页面 | 标题 |",
                "|---|---|---|",
            ]
            for page in sorted(month_pages, reverse=True):
                rel = page.relative_to(ROOT).as_posix()
                rows.append(f"| {page.stem} | [查看](../{rel}) | {extract_title(page)} |")
            rows.append("")
            (index_dir / f"{year}-{month}.md").write_text("\n".join(rows), encoding="utf-8")


def main() -> None:
    pages = archive_pages()
    update_readme(pages)
    update_indexes(pages)
    print(f"Updated indexes from {len(pages)} archived HTML page(s).")


if __name__ == "__main__":
    main()
