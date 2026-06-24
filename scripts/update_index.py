#!/usr/bin/env python3
"""Update archive indexes for anan_everyday_news.

This script is intentionally lightweight for now.
Future behavior:
- scan daily/YYYY/MM/*.md and afternoon/YYYY/MM/*.md
- update README.md latest links
- update index/YYYY-MM.md tables
- optionally update topic index files
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    print("update_index.py is a placeholder. Implement index generation when the archive has daily files.")


if __name__ == "__main__":
    main()
