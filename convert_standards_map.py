#!/usr/bin/env python3
"""Convert bjc-r's cur/teaching-guide/resources/standards-map.html into a
Quarto .qmd page for this site, rewriting every lab link to its new path and
flagging any link whose target no longer exists in the converted site.

Run from the bjc (Quarto) repo root:
    python3 convert_standards_map.py
"""
import os
import re
import sys
from bs4 import BeautifulSoup, NavigableString, Tag

SRC = "/Users/peter/hacks/bjc-r/cur/teaching-guide/resources/standards-map.html"
ROOT = os.path.dirname(os.path.abspath(__file__))  # bjc repo root
OUT = os.path.join(ROOT, "standards-map.qmd")

UNIT_MAP = {
    "1-introduction": "unit-1",
    "2-complexity": "unit-2",
    "3-lists": "unit-3",
    "4-internet": "unit-4",
    "5-algorithms": "unit-5",
    "6-computers": "unit-6",
}

# Explicit overrides for pages renamed/reordered during the conversion.
# Keys are the original source path (without /bjc-r/ prefix, without query).
RENAME = {
    # Unit 1 Lab 1 pages 1 & 2 were swapped in the conversion.
    "cur/programming/1-introduction/1-building-an-app/1-start-your-first-snap-app.html":
        "/unit-1/lab-1/2-start-your-first-snap-app.qmd",
    "cur/programming/1-introduction/1-building-an-app/2-creating-a-snap-account.html":
        "/unit-1/lab-1/1-creating-a-snap-account.qmd",
    # Unit 3 Lab 4 page 4 renamed.
    "cur/programming/3-lists/4-robots-ai/4-breakthroughs-possibilities.html":
        "/unit-3/lab-4/4-recent-developments.qmd",
}

stats = {"resolved": 0, "renamed": 0, "createtask": 0, "unresolved": 0}
unresolved = []   # (id-ish label, source path, visible text)
createtask = set()


def target_exists(qmd_path):
    return os.path.isfile(os.path.join(ROOT, qmd_path.lstrip("/")))


def map_href(href, label, vis_text):
    """Return a rewritten /...qmd path, or None if it can't be resolved."""
    src = href.split("?")[0]
    if src.startswith("/bjc-r/"):
        src = src[len("/bjc-r/"):]

    # AP Create Task: bjc has a rewritten guide; point at its section index.
    if src.startswith("cur/performance-tasks/create-task/"):
        createtask.add(src)
        stats["createtask"] += 1
        return "/create-task/"

    if src in RENAME:
        dest = RENAME[src]
        if target_exists(dest):
            stats["renamed"] += 1
            return dest
        unresolved.append((label, src, vis_text))
        stats["unresolved"] += 1
        return None

    m = re.match(r"cur/programming/([^/]+)/([^/]+)/(.+)\.html$", src)
    if m:
        unit_dir, lab_dir, page = m.groups()
        unit = UNIT_MAP.get(unit_dir)
        lab_num = re.match(r"(\d+)", lab_dir)
        if unit and lab_num:
            dest = f"/{unit}/lab-{lab_num.group(1)}/{page}.qmd"
            if target_exists(dest):
                stats["resolved"] += 1
                return dest
    unresolved.append((label, src, vis_text))
    stats["unresolved"] += 1
    return None


def render_inline(node, current_id):
    """Render the mixed text/<a> content of an <li> (excluding nested <ul>)."""
    out = []
    for child in node.children:
        if isinstance(child, NavigableString):
            out.append(re.sub(r"\s+", " ", str(child)))
        elif isinstance(child, Tag):
            if child.name == "ul":
                continue  # handled separately
            if child.name == "strong":
                out.append(f"**{child.get_text().strip()}**")
            elif child.name == "a":
                text = re.sub(r"\s+", " ", child.get_text()).strip()
                dest = map_href(child.get("href", ""), current_id, text)
                if dest:
                    out.append(f"[{text}]({dest})")
                else:
                    out.append(text)  # leave as plain text if unresolved
            else:
                out.append(re.sub(r"\s+", " ", child.get_text()))
    s = "".join(out)
    s = re.sub(r"[ \t]+", " ", s).strip()
    s = s.replace(" ,", ",").replace(" ;", ";").replace(" .", ".")
    return s


def li_id(li):
    strong = li.find("strong", recursive=False)
    if strong:
        return strong.get_text().strip().rstrip(":")
    # nested EK <li> start with text like "CRD-1.A.1:"
    txt = li.get_text(" ", strip=True)
    m = re.match(r"([A-Z]{3}-[0-9.]+)", txt)
    return m.group(1) if m else "?"


def render_list(ul, depth, lines):
    indent = "    " * depth
    for li in ul.find_all("li", recursive=False):
        cid = li_id(li)
        text = render_inline(li, cid)
        lines.append(f"{indent}- {text}")
        nested = li.find("ul", recursive=False)
        if nested:
            render_list(nested, depth + 1, lines)


def main():
    with open(SRC, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    body = soup.body
    lines = []
    # Front matter
    lines.append("---")
    lines.append('title: "AP CSP Standards Map"')
    lines.append('pagetitle: "{{< meta title >}} | {{< var title-fix >}}"')
    lines.append('subtitle: "Where each College Board CED standard is covered in BJC"')
    lines.append("order: 20")
    lines.append("---")
    lines.append("")
    lines.append(
        "This page maps the College Board "
        "[AP Computer Science Principles Course and Exam Description]"
        "(https://apcentral.collegeboard.org/courses/ap-computer-science-principles/course) "
        "(CED) learning objectives and essential-knowledge statements to the place "
        "they are covered in this curriculum. It is adapted from the BJC "
        "*Standards Map*.")
    lines.append("")
    lines.append(
        "::: callout-note\n"
        "Links to the AP **Create Task** point to this site's "
        "[Create Task](/create-task/) section, which is a rewritten guide and does "
        "not map page-for-page to the original. See the description text for the "
        "specific location.\n:::")
    lines.append("")

    # Quick-nav row
    cats = []
    for h3 in body.find_all("h3"):
        a = h3.find("a")
        if a and a.get("name"):
            cats.append(a["name"])
    if cats:
        lines.append(" · ".join(f"[{c}](#{c})" for c in cats))
        lines.append("")

    # Walk the big-idea / category structure in document order.
    for el in body.children:
        if not isinstance(el, Tag):
            continue
        if el.name == "h2":
            txt = el.get_text().strip()
            if txt.startswith("Big Idea"):
                lines.append(f"# {txt}")
                lines.append("")
        elif el.name == "h3":
            a = el.find("a")
            anchor = a["name"] if a and a.get("name") else el.get_text().strip()
            label = el.get_text().strip()
            lines.append(f"## {label} {{#{anchor}}}")
            lines.append("")
        elif el.name == "div":
            ul = el.find("ul", recursive=False)
            if ul:
                render_list(ul, 0, lines)
                lines.append("")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # Report
    print(f"Wrote {OUT}")
    print(f"Link resolution: {stats}")
    if createtask:
        print("\nCreate-Task source pages redirected to /create-task/ :")
        for s in sorted(createtask):
            print(f"  - {s}")
    if unresolved:
        print(f"\nUNRESOLVED links ({len(unresolved)}) — rendered as plain text:")
        for label, src, text in unresolved:
            print(f"  - {label}: {src}  (\"{text}\")")


if __name__ == "__main__":
    main()
