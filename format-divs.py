#!/usr/bin/env python3
"""Normalize the colon counts on nested Pandoc/Quarto fenced divs.

Top-level divs get three colons (`:::`); each level of nesting adds one
more colon (`::::`, `:::::`, …).  Pandoc closes the innermost open div on
*any* bare colon fence regardless of its length, so colon count is purely
cosmetic — but a consistent "outer few, inner many" scheme keeps deeply
nested content (see e.g. unit-4/lab-2/2-caesar-cipher.qmd) readable and
makes an accidental premature close obvious.

Only the colon *count* is ever rewritten.  Leading whitespace (which is
semantically significant when a div lives inside a Markdown list item) and
the attribute text after the colons are preserved verbatim.  Fenced code
blocks (``` / ~~~), `<!-- HTML comments -->`, and YAML frontmatter are
skipped so colons appearing there are left alone.  (These BJC pages were
converted from HTML and routinely have whole div-laden sections commented
out — see e.g. unit-2/lab-4/1-mod-operator.qmd lines 218-379.)

A file is only rewritten if its fences balance as a stack; an unbalanced
file is reported and left untouched, so this script can never turn a
merely-ugly file into a broken one.

Usage:
    python3 format-divs.py [PATH ...]     # rewrite in place (default: all *.qmd)
    python3 format-divs.py --check [PATH ...]   # report drift, write nothing
    python3 format-divs.py --diff  [PATH ...]   # show unified diffs, write nothing

Exit status is non-zero if any file needs changes (--check/--diff) or if any
file has unbalanced fences.
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

# A fenced-div line: optional indent, >=3 colons, then the rest of the line.
FENCE_RE = re.compile(r"^([ \t]*)(:{3,})(.*)$")
# A code fence: optional indent, >=3 backticks or tildes, then an info string.
CODE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")


class UnbalancedError(Exception):
    """Raised when a file's div fences don't form a balanced stack."""


def comment_state_after(line, in_comment):
    """Return whether we are inside an HTML comment at the end of `line`.

    HTML comments don't nest, so this is a simple open/close scan that also
    copes with several `<!--`/`-->` pairs on a single line.
    """
    i = 0
    while i < len(line):
        if not in_comment:
            j = line.find("<!--", i)
            if j < 0:
                break
            in_comment = True
            i = j + 4
        else:
            j = line.find("-->", i)
            if j < 0:
                break
            in_comment = False
            i = j + 3
    return in_comment


def reformat(text):
    """Return the reformatted text for one file's contents.

    Raises UnbalancedError (with a human-readable message) if the fences
    don't balance, in which case the caller should leave the file alone.
    """
    newline = "\n"
    had_trailing_newline = text.endswith("\n")
    lines = text.split("\n")
    if had_trailing_newline:
        # split() leaves a trailing "" we don't want to iterate as a line
        lines = lines[:-1]

    out = []
    stack = []           # colon counts of the currently-open divs
    in_code = False
    code_fence = None    # (char, length) of the open code fence
    in_comment = False   # inside an <!-- HTML comment --> spanning lines
    idx = 0

    # Skip a leading YAML frontmatter block untouched.
    if lines and lines[0].strip() == "---":
        out.append(lines[0])
        idx = 1
        while idx < len(lines) and lines[idx].strip() != "---":
            out.append(lines[idx])
            idx += 1
        if idx < len(lines):           # closing ---
            out.append(lines[idx])
            idx += 1

    for lineno in range(idx, len(lines)):
        line = lines[lineno]

        # Inside a multi-line HTML comment: pass through, watch for its close.
        if in_comment:
            in_comment = comment_state_after(line, True)
            out.append(line)
            continue

        code_m = CODE_RE.match(line)
        if code_m:
            fence = code_m.group(2)
            char, length, info = fence[0], len(fence), code_m.group(3)
            if not in_code:
                in_code = True
                code_fence = (char, length)
            elif char == code_fence[0] and length >= code_fence[1] and info.strip() == "":
                in_code = False
                code_fence = None
            out.append(line)
            continue

        if in_code:
            out.append(line)
            continue

        # A line containing comment markers is prose, not a fence (a real
        # fence line never contains `<!--`).  Track a comment that stays open.
        if "<!--" in line:
            in_comment = comment_state_after(line, False)
            out.append(line)
            continue

        fence_m = FENCE_RE.match(line)
        if not fence_m:
            out.append(line)
            continue

        indent, _colons, rest = fence_m.group(1), fence_m.group(2), fence_m.group(3)

        if rest.strip() == "":
            # Closing fence: reuse the count assigned to its matching open.
            if not stack:
                raise UnbalancedError(
                    f"line {lineno + 1}: closing fence with no open div")
            count = stack.pop()
            out.append(f"{indent}{':' * count}")
        else:
            # Opening fence: three colons at the top, +1 per nesting level.
            count = 3 + len(stack)
            stack.append(count)
            out.append(f"{indent}{':' * count}{rest}")

    if in_code:
        raise UnbalancedError("unterminated fenced code block")
    if in_comment:
        raise UnbalancedError("unterminated HTML comment")
    if stack:
        raise UnbalancedError(f"{len(stack)} div fence(s) left unclosed")

    result = newline.join(out)
    if had_trailing_newline:
        result += newline
    return result


def iter_target_files(paths):
    """Yield the .qmd files implied by the command-line PATH arguments."""
    if not paths:
        paths = [Path(".")]
    for p in paths:
        p = Path(p)
        if p.is_dir():
            yield from sorted(p.rglob("*.qmd"))
        else:
            yield p


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="report files that would change; write nothing")
    mode.add_argument("--diff", action="store_true",
                      help="print a unified diff for each file; write nothing")
    parser.add_argument("paths", nargs="*",
                        help="files or directories (default: all *.qmd below cwd)")
    args = parser.parse_args(argv)

    changed = []
    errors = []

    for path in iter_target_files(args.paths):
        original = path.read_text(encoding="utf-8")
        try:
            updated = reformat(original)
        except UnbalancedError as exc:
            errors.append((path, str(exc)))
            continue

        if updated == original:
            continue
        changed.append(path)

        if args.diff:
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=str(path), tofile=str(path))
            sys.stdout.writelines(diff)
        elif not args.check:
            path.write_text(updated, encoding="utf-8")

    for path, msg in errors:
        print(f"UNBALANCED  {path}: {msg}", file=sys.stderr)

    verb = "would reformat" if (args.check or args.diff) else "reformatted"
    for path in changed:
        print(f"{verb}  {path}")

    if errors:
        print(f"\n{len(errors)} file(s) have unbalanced fences and were skipped.",
              file=sys.stderr)
    if changed:
        print(f"{len(changed)} file(s) {verb}.")
    if not changed and not errors:
        print("All fenced divs already consistently formatted.")

    # Non-zero exit if there's drift (check/diff) or any unbalanced file.
    if errors:
        return 2
    if changed and (args.check or args.diff):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
