#!/usr/bin/env python3
"""Validate the optional JSON entry in a "Submit your system or tool" issue.

Reads the issue body from the ISSUE_BODY environment variable (or a file path argument).
Exit codes: 0 valid, 1 invalid, 2 no JSON entry given.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check  # noqa: E402


def section(body: str, heading: str) -> str:
    match = re.search(rf"^###\s+{re.escape(heading)}\s*$(.*?)(?=^###\s|\Z)", body, re.S | re.M)
    return match.group(1).strip() if match else ""


def main(argv: list[str]) -> int:
    body = Path(argv[0]).read_text() if argv else os.environ.get("ISSUE_BODY", "")
    kind = "tool" if "tool" in section(body, "Entry type").lower() else "card"
    entry = section(body, "JSON entry (optional)")
    fenced = re.search(r"```(?:json)?\s*(.*?)```", entry, re.S)
    text = (fenced.group(1) if fenced else entry).strip()
    if not text or text == "_No response_":
        print("No JSON entry given.")
        return 2
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"The JSON entry is not valid JSON: {exc}")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"{kind}-submission.json"
        path.write_text(json.dumps(data))
        errors = check.check_file(path, check.card_slugs())
    if errors:
        print(f"Checked as a {kind}:")
        for e in errors:
            print(e.split(": ", 1)[1])
        return 1
    print(f"Checked as a {kind}: valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
