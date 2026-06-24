#!/usr/bin/env python3
"""Check basic archive file conventions.

Current checks:
- placeholder only

Future checks:
- verify daily files use YYYY-MM-DD.md
- verify daily/YYYY/MM path matches file date
- verify afternoon/YYYY/MM path matches file date
- report missing month index files
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    print("check_files.py is a placeholder. Implement file convention checks when needed.")


if __name__ == "__main__":
    main()
