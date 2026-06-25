#!/usr/bin/env python3
"""Update indexes for the root-date-file archive.

Rules:
- Daily files live in repository root as YYYY-MM-DD.md.
- README.md contains a latest-news block between markers.
- index/YYYY.md and index/YYYY-MM.md are generated from root date files.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE_FILE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")
README_START = "<!-- news-index:start -->"
README_END = "<!-- news-index:end -->"


def find_day_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.glob("*.md"):
        if DATE_FILE_RE.match(path.name):
            files.append(path)
    return sorted(files, reverse=True)


def extract_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def replace_between_markers(text: str, start: str, end: str, replacement: str) -> str:
    if start not in text or end not in text:
        return text
    before = text.split(start, 1)[0]
    after = text.split(end, 1)[1]
    return f"{before}{start}\n{replacement}\n{end}{after}"


def update_readme(day_files: list[Path]) -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        return

    latest = day_files[:10]
    if latest:
        replacement = "\n".join(f"- [{extract_title(path)}]({path.name})" for path in latest)
    else:
        replacement = "- 暂无"

    text = readme.read_text(encoding="utf-8")
    new_text = replace_between_markers(text, README_START, README_END, replacement)
    readme.write_text(new_text, encoding="utf-8")


def update_month_indexes(day_files: list[Path]) -> None:
    index_dir = ROOT / "index"
    index_dir.mkdir(exist_ok=True)

    grouped: dict[str, dict[str, list[Path]]] = defaultdict(lambda: defaultdict(list))
    for path in day_files:
        match = DATE_FILE_RE.match(path.name)
        if not match:
            continue
        year, month, _day = match.groups()
        grouped[year][month].append(path)

    for year, months in grouped.items():
        month_lines = [f"# {year} 年简报索引", "", "## 月份", ""]
        for month in sorted(months):
            month_lines.append(f"- [{year} 年 {int(month)} 月]({year}-{month}.md)")
        month_lines.extend(["", "## 规则", "", "- 每日文件保存在仓库根目录，例如 `../YYYY-MM-DD.md`。", "- 月份索引只做跳转，不存放正文。", ""])
        (index_dir / f"{year}.md").write_text("\n".join(month_lines), encoding="utf-8")

        for month, paths in months.items():
            rows = [
                f"# {year} 年 {int(month)} 月简报索引",
                "",
                "## 每日文件",
                "",
                "| 日期 | 当天文件 | 标题 |",
                "|---|---|---|",
            ]
            for path in sorted(paths, reverse=True):
                date = path.stem
                rows.append(f"| {date} | [查看](../{path.name}) | {extract_title(path)} |")
            rows.extend(["", "## 说明", "", "- 8:30 主简报、10:30 喝水提醒、15:30 下午补充都应写入同一个根目录日期文件。", "- 运行 `python scripts/update_index.py` 可刷新 README 和月份索引。", ""])
            (index_dir / f"{year}-{month}.md").write_text("\n".join(rows), encoding="utf-8")


def main() -> None:
    day_files = find_day_files()
    update_readme(day_files)
    update_month_indexes(day_files)
    print(f"Updated indexes from {len(day_files)} root date file(s).")


if __name__ == "__main__":
    main()
