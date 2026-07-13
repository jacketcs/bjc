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

There are no tests or linters. Deployment is automatic: pushing to `main`
triggers `.github/workflows/main.yml`, which renders with a pinned Quarto
version (check the workflow for the exact version) and publishes to the
`gh-pages` branch. Use the same Quarto version locally to match the live site.

## Structure and conventions

- **Only `.qmd` files are rendered** (enforced by the `render:` rules in `_quarto.yml`). `.md` files are reserved for documentation and are excluded from the site.

- Curriculum content lives in `unit-1/` … `unit-6/` and `create-task/`, each
  wired into the navbar and sidebar in `_quarto.yml`. Units contain `lab-N/`
  folders of numbered pages (`1-foo.qmd`, `2-bar.qmd`, …) plus an `index.qmd`;
  sidebar order comes from the `order:` frontmatter field.

- Page frontmatter follows `_templates/lab_temp.qmd`: `title` (e.g. `"Page 2:
  Programming a Game"`), `subtitle` (e.g. `"Unit 1, Lab 2, Page 3"` — used in
  the browser page title via `pagetitle` in `_quarto.yml`), and `order`.

- Content is styled with fenced divs using BJC-specific classes defined in
  `bjc.scss`/`bjc-dark.scss`: `learn`, `forYouToDo`, `ifTime`, `dialogue`,
  `takeItFurther`, `takeNote`, `endnote`, `narrower`, `narrowblue`,
  `narrowpurple`, `time`. Nest divs by adding colons (`::::` outside, `:::`
  inside).

- Announcements and CITN posts go in `posts/`.

## Custom Lua extensions (`_extensions/`)

Three filters run on every page (declared in `_quarto.yml`):

- **titling** — Lua functions that derive "Unit X, Lab Y, Page Z" strings from
  the file path (path parsing assumes the `unit-N/lab-N/N-name.qmd` layout, so
  keep that naming).

- **gifffer** — click-to-play GIFs; opt in per page with `gifffer: true` in
  frontmatter.

- **checkpoint** — embeds a Google Form via shortcode: `{{< checkpoint id="..." >}}`.

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
