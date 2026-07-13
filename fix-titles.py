#!/usr/bin/env python3
"""Normalize curriculum page titles, subtitles, and `order` frontmatter.

Titles and subtitles on curriculum pages follow a strict convention that is
fully derivable from the file's path:

    unit-N/lab-M/K-name.qmd   title:    "Page K: <human title>"
                              subtitle: "Unit N, Lab M, Page K"
    unit-N/lab-M/index.qmd    title:    "Lab M: <human title>"
                              subtitle: "Unit N, Lab M"

The Quarto sidebar/navbar reads each page's title from its raw frontmatter
before any Lua filter runs, so the derived parts (the "Page K:" / "Lab M:"
prefix and the whole subtitle) have to be baked into the frontmatter on disk
rather than computed at render time. This script is the generator: it rewrites
the derivable parts while preserving the human-authored part of the title.

It also drops the `order:` field wherever it is redundant with the filename
(basename `K-...` and `order == K`), because Quarto orders auto-sidebar
contents by filename when `order` is absent. `index.qmd` and files like
create-task's `1-program-code.qmd` (order 100) keep their `order`.

Usage:
    python3 fix-titles.py           # fix files in place
    python3 fix-titles.py --check   # report needed changes, write nothing,
                                     # exit 1 if any file is out of date (CI)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# unit-N/lab-M/K-name.qmd  (K may be zero-padded, e.g. 01-abstraction.qmd)
NUMBERED = re.compile(r"^unit-(\d+)/lab-(\d+)/(\d+)-[^/]+\.qmd$")
# unit-N/lab-M/index.qmd   (integer labs only; half-labs like lab-3.5 are skipped)
LAB_INDEX = re.compile(r"^unit-(\d+)/lab-(\d+)/index\.qmd$")

# Leading generated prefixes to strip before recomputing, so the script is
# idempotent and never double-prefixes ("Page 4: Page 4: ...").
STRIP_PREFIX = re.compile(r"^\s*(?:Page|Lab)\s+[\d.]+:\s*")


def derive(relpath):
    """Return (expected_title, expected_subtitle) for an in-scope file, or None."""
    m = NUMBERED.match(relpath)
    if m:
        unit, lab, page = int(m[1]), int(m[2]), int(m[3])
        return f"Page {page}: {{human}}", f"Unit {unit}, Lab {lab}, Page {page}"
    m = LAB_INDEX.match(relpath)
    if m:
        unit, lab = int(m[1]), int(m[2])
        return f"Lab {lab}: {{human}}", f"Unit {unit}, Lab {lab}"
    return None


def unquote(value):
    """Strip one layer of surrounding matching quotes from a YAML scalar."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def order_is_redundant(relpath, order_value):
    """True when `order` just repeats the filename's leading number."""
    base = relpath.rsplit("/", 1)[-1]
    m = re.match(r"^(\d+)-", base)
    ov = order_value.strip()
    return bool(m) and ov.isdigit() and int(ov) == int(m[1])


def process(path):
    """Return (new_text, list_of_change_descriptions) for a file."""
    relpath = path.relative_to(ROOT).as_posix()
    spec = derive(relpath)
    title_tmpl, want_subtitle = spec if spec else (None, None)

    text = path.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?\n)---\n", text, re.S)
    if not fm:
        return None, []
    body_start = fm.end()
    fm_lines = fm.group(1).splitlines()

    changes = []
    out_lines = []
    saw_subtitle = False
    title_idx = None

    for line in fm_lines:
        key = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        name = key.group(1) if key else None

        # Title/subtitle are only rewritten on convention-following lab pages.
        if spec and name == "title":
            human = STRIP_PREFIX.sub("", unquote(key.group(2))).strip()
            want = title_tmpl.format(human=human)
            new_line = f'title: "{want}"'
            if new_line != line:
                changes.append(f"title -> {want!r}")
            out_lines.append(new_line)
            title_idx = len(out_lines) - 1

        elif spec and name == "subtitle":
            saw_subtitle = True
            new_line = f'subtitle: "{want_subtitle}"'
            if new_line != line:
                changes.append(f"subtitle -> {want_subtitle!r}")
            out_lines.append(new_line)

        # Redundant `order` is dropped everywhere, convention or not.
        elif name == "order" and order_is_redundant(relpath, key.group(2)):
            changes.append(f"drop order ({key.group(2).strip()})")
            # skip line

        else:
            out_lines.append(line)

    if spec and not saw_subtitle and title_idx is not None:
        out_lines.insert(title_idx + 1, f'subtitle: "{want_subtitle}"')
        changes.append(f"add subtitle {want_subtitle!r}")

    if not changes:
        return None, []

    new_text = "---\n" + "\n".join(out_lines) + "\n---\n" + text[body_start:]
    return new_text, changes


def main():
    check = "--check" in sys.argv[1:]
    files = sorted(
        p for p in ROOT.glob("**/*.qmd")
        if not p.relative_to(ROOT).as_posix().startswith(
            ("_extensions/", "_site/", "_templates/")
        )
    )
    changed = 0
    for path in files:
        new_text, changes = process(path)
        if not changes:
            continue
        changed += 1
        rel = path.relative_to(ROOT).as_posix()
        print(f"{rel}")
        for c in changes:
            print(f"    {c}")
        if not check:
            path.write_text(new_text, encoding="utf-8")

    if changed == 0:
        print("All titles up to date.")
        return 0
    if check:
        print(f"\n{changed} file(s) need updating. Run without --check to fix.")
        return 1
    print(f"\nFixed {changed} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
