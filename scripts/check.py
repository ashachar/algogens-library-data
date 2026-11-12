#!/usr/bin/env python3
"""Validate AlgoGens Library entries against the schemas in schema/.

Standard library only, so it runs anywhere Python 3.9+ runs.

Usage:
  python3 scripts/check.py                 # check every file in cards/ and tools/
  python3 scripts/check.py FILE [FILE...]  # check named files
  python3 scripts/check.py --self-test     # valid fixtures must pass, invalid fixtures must fail

Which schema applies: files under cards/ use card.schema.json, files under tools/ use
tool.schema.json. Test fixtures pick the schema from their name prefix (card-*.json, tool-*.json).
Exit code 0 means every checked file is valid.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = {name: json.loads((ROOT / "schema" / f"{name}.schema.json").read_text()) for name in ("card", "tool")}
TYPES = {
    "object": dict, "array": list, "string": str, "null": type(None),
    "integer": int, "number": (int, float), "boolean": bool,
}


def validate(value, schema, path="$"):
    """Return a list of error strings for the JSON Schema subset the library schemas use."""
    errors = []
    if "anyOf" in schema:
        if not any(not validate(value, option, path) for option in schema["anyOf"]):
            errors.append(f"{path}: does not match any allowed form")
        return errors
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
    expected = schema.get("type")
    if expected:
        ok = isinstance(value, TYPES[expected])
        if expected in ("integer", "number") and isinstance(value, bool):
            ok = False
        if not ok:
            return errors + [f"{path}: expected {expected}, got {type(value).__name__}"]
    if isinstance(value, str):
        if len(value.strip()) < schema.get("minLength", 0):
            errors.append(f"{path}: must not be empty")
        # fullmatch-style: "$" in Python also matches before a final newline, so reject newlines in patterned values.
        if "pattern" in schema and ("\n" in value or not re.search(schema["pattern"], value)):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} is below {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} is above {schema['maximum']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: needs at least {schema['minItems']} item(s)")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True) for v in value}) != len(value):
            errors.append(f"{path}: items must be unique")
        for i, item in enumerate(value):
            errors += validate(item, schema.get("items", {}), f"{path}[{i}]")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required field '{key}'")
        for key, item in value.items():
            if key in props:
                errors += validate(item, props[key], f"{path}.{key}")
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unknown field {key[:60]!r}")
    return errors


def kind_of(path: Path) -> str | None:
    resolved = path.resolve()
    parts = resolved.relative_to(ROOT).parts if resolved.is_relative_to(ROOT) else ()
    if parts[:1] == ("cards",):
        return "card"
    if parts[:1] == ("tools",):
        return "tool"
    for name in SCHEMAS:
        if path.name.startswith(f"{name}-"):
            return name
    return None


def check_file(path: Path, known_slugs: set[str]) -> list[str]:
    kind = kind_of(path)
    if kind is None:
        return [f"{path}: cannot tell if this is a card or a tool (put it in cards/ or tools/)"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: not valid JSON ({exc})"]
    errors = validate(data, SCHEMAS[kind])
    in_dataset = path.resolve().parent.name in ("cards", "tools")
    if in_dataset and isinstance(data, dict) and data.get("slug") != path.stem:
        errors.append(f"$.slug: {data.get('slug')!r} must equal the file name '{path.stem}'")
    if kind == "card" and isinstance(data, dict) and data.get("parent") and known_slugs:
        if data["parent"] not in known_slugs:
            errors.append(f"$.parent: {data['parent']!r} is not a card slug in cards/")
    return [f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {e}" for e in errors]


def card_slugs() -> set[str]:
    return {p.stem for p in (ROOT / "cards").glob("*.json")}


def run(paths: list[Path]) -> int:
    slugs = card_slugs()
    errors = [e for p in paths for e in check_file(p, slugs)]
    for e in errors:
        print(e)
    print(f"checked {len(paths)} file(s): {'FAIL, ' + str(len(errors)) + ' error(s)' if errors else 'all valid'}")
    return 1 if errors else 0


def self_test() -> int:
    slugs = card_slugs()
    failures = 0
    for p in sorted((ROOT / "tests/fixtures/valid").glob("*.json")):
        errs = check_file(p, slugs)
        status = "ok  " if not errs else "FAIL"
        failures += bool(errs)
        print(f"{status} valid fixture passes: {p.name}" + "".join(f"\n       {e}" for e in errs))
    for p in sorted((ROOT / "tests/fixtures/invalid").glob("*.json")):
        errs = check_file(p, slugs)
        status = "ok  " if errs else "FAIL"
        failures += not errs
        print(f"{status} invalid fixture is rejected: {p.name}" + (f" ({errs[0].split(': ', 1)[1]})" if errs else ""))
    print("self-test:", "FAIL" if failures else "all fixtures behaved as expected")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return self_test()
    if argv:
        return run([Path(a) for a in argv])
    return run(sorted((ROOT / "cards").glob("*.json")) + sorted((ROOT / "tools").glob("*.json")))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
