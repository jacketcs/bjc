# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## What this is

A Quarto website hosting the BJC (Beauty and Joy of Computing) AP CSP curriculum
for Berkeley High School, published at bjc.jacketcs.net. Content was converted
from the original bjc-r HTML curriculum (see `conversion-notes.md`), so many
pages still contain raw HTML mixed into Markdown — prefer Markdown syntax for
new content unless HTML is required for a feature.

## Commands

```bash
quarto preview   # live-reload dev server (port 1000, per _quarto.yml)
quarto render    # one-time full render
```

Two informational CI checks run on pull requests and pushes to `main`:
`.github/workflows/check-titles.yml` runs `python3 fix-titles.py --check` (see
the frontmatter conventions below), and `.github/workflows/check-divs.yml` runs
`python3 format-divs.py --check` (see the fenced-div convention below). Both are
independent of the deploy workflow, so a failure shows a red X but does not stop
publishing. There are no other tests or linters.

Deployment is automatic: pushing to `main` triggers
`.github/workflows/main.yml`, which renders with a pinned Quarto version (check
the workflow for the exact version) and publishes to the `gh-pages` branch. Use
the same Quarto version locally to match the live site. `Dockerfile.yolo`
installs exactly that version on top of the yolo base image (keep its
`QUARTO_VERSION` in sync with the workflow); apply it with `yolo config
--dockerfile ./Dockerfile.yolo` so every container has `quarto` preinstalled.

## Structure and conventions

- **Only `.qmd` files are rendered** (enforced by the `render:` rules in `_quarto.yml`). `.md` files are reserved for documentation and are excluded from the site.

- Curriculum content lives in `unit-1/` … `unit-6/` and `create-task/`, each
  wired into the navbar and sidebar in `_quarto.yml`. Units contain `lab-N/`
  folders of numbered pages (`1-foo.qmd`, `2-bar.qmd`, …) plus an `index.qmd`.
  Quarto orders the auto-generated sidebar by the `order:` frontmatter field, or,
  when `order` is absent, by filename — so numbered pages carry no `order`
  (their filename number already sorts them; the one lab that reaches double
  digits, `unit-6/lab-1/`, is zero-padded `01-`…`10-` so filename sort stays
  numeric). `index.qmd` files and any page whose `order` differs from its
  filename number (e.g. `create-task/`) keep their explicit `order`.

- Page frontmatter follows `_templates/lab_temp.qmd`: `title` (e.g. `"Page 2:
  Programming a Game"`) and `subtitle` (e.g. `"Unit 1, Lab 2, Page 3"` — the
  site-wide `pagetitle` in `_quarto.yml` builds the browser tab title from it).
  On lab pages the `Page N:` title prefix and the whole subtitle are derived
  from the file path and must match it. Quarto reads the title for the
  sidebar/navbar from raw frontmatter *before* any Lua filter runs, so these
  strings are baked into the frontmatter rather than computed at render time.
  **`fix-titles.py` is the generator**: it rewrites the derivable parts
  (preserving the human-authored part of each title), drops redundant `order`
  fields, and normalizes subtitles. It also **manages `pagetitle`**: lab pages
  (distinctive subtitle) get none and rely on the global one, while every other
  page gets an explicit `pagetitle: "{{< metatext title >}}"` so its tab is
  titled from the page title rather than an absent or generic subtitle. It also
  zero-pads numbered filenames to a consistent per-directory width when a lab
  reaches double digits (`1-foo.qmd` → `01-foo.qmd`) and rewrites the internal
  links that pointed at any renamed file, so filename-based ordering stays
  numeric. Run `python3 fix-titles.py` after adding or renaming lab pages;
  `python3 fix-titles.py --check` reports drift without writing and is what CI
  runs.

- Content is styled with fenced divs using BJC-specific classes defined in
  `bjc.scss`/`bjc-dark.scss`: `learn`, `forYouToDo`, `ifTime`, `dialogue`,
  `takeItFurther`, `takeNote`, `endnote`, `narrower`, `narrowblue`,
  `narrowpurple`, `time`. Nest divs by adding colons: top-level divs get three
  colons (`:::`) and each level of nesting adds one more (`::::` one level in,
  `:::::` two levels in, …). `format-divs.py` normalizes this automatically —
  it rewrites only the colon counts (preserving indentation and attributes),
  skips code blocks and HTML comments, and refuses to touch a file whose fences
  don't balance. Run `python3 format-divs.py` after editing divs; `--check`
  reports drift and `--diff` previews without writing.

- Announcements and CITN posts go in `posts/`.

## Custom Lua extensions (`_extensions/`)

These run on every page (declared in `_quarto.yml`):

- **gifffer** — click-to-play GIFs; opt in per page with `gifffer: true` in
  frontmatter.

- **checkpoint** — embeds a Google Form via shortcode: `{{< checkpoint id="..." >}}`.

- **metatext** — `{{< metatext KEY >}}` emits the plain-text (HTML-stripped)
  value of a frontmatter field; used to build every `pagetitle` so inline HTML
  in a title (e.g. `Snap<em>!</em>`) doesn't leak into the browser tab.

The **glossary** extension is unused. Each extension has a README and `example.qmd`.

## Snap! integration

- `llab/loader.js` is injected into every page's header and dynamically loads
  `llab/script/library.js` and `llab/script/curriculum.js`. On page load,
  `llab.secondarySetUp()` (curriculum.js) rewrites any `<a class="run">` link
  via `llab.getSnapRunURL()` (library.js) so its href opens the linked project
  XML in the Snap! web IDE. Fragile detail: `getSnapRunURL` skips hrefs that
  don't contain the current hostname, and only works because Quarto's own
  `quarto-nav.js` happens to absolutize every anchor href first.
  `llab.hostDomain` is hardcoded to `https://bjc.jacketcs.net`, so run links
  point at production XML even during `quarto preview`.

- `llab/renderContent.js` contains near-identical run-link logic but is dead
  code — nothing loads it.

- Snap! starter project XML files go in `prog/`, organized by topic/unit
  folders. Reference them with absolute paths, e.g. `<a
  href="/prog/1-introduction/U1L1-ClickAlonzo.xml" class="run">`.

- `img/`, `data/`, `llab/`, and `prog/` are copied verbatim as site resources;
  reference them with absolute paths (`/img/...`).
