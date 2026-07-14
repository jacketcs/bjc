# Quarto features used by `bjc`

This site is built with [Quarto](https://quarto.org/). Most page bodies are
plain Markdown, but the project leans on a number of Quarto-specific features
(and four custom extensions) to do things Markdown alone can't. This document
catalogs them so editors know what's available and what the non-Markdown syntax
in the `.qmd` files means.

> Quick orientation: configuration lives in `_quarto.yml` and `_variables.yml`;
> custom behavior lives in `_extensions/`; a page skeleton lives in
> `_templates/lab_temp.qmd`.

## 1. Project / website configuration (`_quarto.yml`)

The whole thing is a Quarto **website project** (`project.type: website`), which
gives features you never get from standalone Markdown:

- **Navbar and docked sidebars** — the top "Labs / Resources" menus and the
  per-unit docked sidebars are generated from `website.navbar` and
  `website.sidebar`. Sidebar contents are auto-built from directory listings
  (e.g. `contents: unit-1`).
- **Site-wide search** (`navbar.search: true`), **reader mode**, and
  **page navigation** (prev/next links via `page-navigation: true`).
- **Shared page footer** with the BJC/CC-BY-NC-SA attribution.
- **Theming via SCSS** — `theme: { light: bjc.scss, dark: [bjc-dark.scss, bjc.scss] }`.
  Light/dark theming and Sass compilation are Quarto features; the custom
  fenced-div classes (see §5) are styled in `bjc.scss`.
- **Selective rendering** — `render: ["!*.md", "*.qmd"]` so `.md` docs (like this
  file and `COMPARISON.md`) are *not* rendered into the site; only `.qmd` is.
- **`resources`** globs (`/llab/`, `/prog/`, `/img/`, `/data/`) copy
  non-`.qmd` assets into the output.
- **HTML format options** applied site-wide: `toc: true`, Bootstrap
  `grid` widths, `callout-appearance: minimal`,
  `link-external-newwindow: true`, a `revealjs` `slide-format` so any page
  can become slides, and a site-wide `pagetitle` (`"{{< metatext subtitle >}}"`)
  for the browser tab title (see §2).
- **`include-in-header`** injects the BJC lab-runner script
  (`/llab/loader.js`) into every page — this is what renders the embedded
  Snap! block images.
- **Pandoc filters** are registered globally: `gifffer` and `checkpoint`
  (see §3).

## 2. Metadata shortcodes and the browser tab title

- **`{{< meta … >}}`** pulls from a page's own front matter. The site-wide
  `pagetitle` in `_quarto.yml` (`"{{< metatext subtitle >}}"`) sets the browser
  tab title from the page's subtitle; Quarto then appends the website `title`
  (`JacketCS CSP`) itself, so a tab reads `Unit 1, Lab 1, Page 2 – JacketCS CSP`
  — the brand comes from `website.title`, *not* from the `pagetitle` string, so
  it isn't doubled. (`metatext` is the custom shortcode that strips inline HTML,
  e.g. the `<em>` italicizing the `!` in "Snap!", for the plain-text `<title>`;
  see §3.)
- The subtitle only makes a good tab title on numbered lab pages, which have a
  distinctive subtitle (`"Unit N, Lab M, Page K"`). Every other page — index
  pages, `create-task/`, posts, standalone resource pages, and the
  `optional-projects`/`project` pages with a generic, non-unique subtitle like
  `"Unit N Optional Project"` — instead sets an explicit
  `pagetitle: "{{< metatext title >}}"` so the tab shows the unique page title.
  Which pages carry this override is generated and enforced by `fix-titles.py`
  (see §7), not maintained by hand.

`{{< meta >}}` (and the custom `{{< metatext >}}`) don't exist in plain
Markdown; they are Quarto shortcodes resolved at render time.

## 3. Custom extensions (`_extensions/`)

Four local extensions ship with the repo:

### `checkpoint` — the `checkpoint` shortcode (most-used custom feature, ~49 uses)

`{{< checkpoint id="<google-form-id>" text="..." >}}` expands (via
`_extensions/checkpoint/checkpoint.lua`) into a Bootstrap **modal dialog**
containing an embedded Google Form `<iframe>`, triggered by a red button. This
is how the converted curriculum replaced many of BJC's inline multiple-choice
self-checks. Plain Markdown cannot generate the button + modal + iframe markup.

### `metatext` — plain-text metadata for `pagetitle`

`{{< metatext KEY >}}` (via `_extensions/metatext/metatext.lua`) emits the
plain-text value of a front-matter field, like `{{< meta KEY >}}` but with any
inline HTML stripped. It exists because a few titles carry HTML — e.g.
`"Snap<em>!</em> Cheat Sheet"`, where the `<em>` italicizes the `!` for the
navbar/sidebar. The HTML `<title>` element can't render tags, so interpolating
the raw title leaks a literal `Snap<em>!</em>` into the browser tab.
`pandoc.utils.stringify` drops raw-HTML inlines while keeping their text, so
`metatext` yields `Snap!`. Every `pagetitle` in the site is built with
`metatext` (the site-wide one in `_quarto.yml` and the per-page overrides that
`fix-titles.py` maintains). It contributes a shortcode (not a filter), so it's
auto-discovered and not in the `filters:` list.

### `gifffer` — play/pause for animated GIFs

A page opts in with **`gifffer: true`** in its front matter (~37 pages). The
`gifffer.lua` filter then attaches the `gifffer.min.js` script and
`bjc-gifffer.css` as HTML dependencies *only on those pages*, so animated GIFs
get a click-to-play control instead of autoplaying. (Conditional, per-page asset
injection driven by front matter is a Quarto/Lua-filter capability.)

### `titling` — removed (replaced by `fix-titles.py`)

An earlier `titling` extension tried to derive "Unit N, Lab N, Page N" text from
a page's path via Lua. But Quarto reads each page's sidebar/navbar title from
raw frontmatter *before* any Lua filter runs, so the filter could never affect
the sidebar — it was effectively a no-op. It was removed and replaced by
**`fix-titles.py`**, a Python generator that bakes the derivable title/subtitle
prefixes into each page's frontmatter on disk and drops redundant `order` fields
(see §7 and `CLAUDE.md`).

### `glossary` — vocabulary scaffolding

`vocabulary.lua` is a (currently minimal) filter that hooks `vocab` / `vocabBig`
divs. It's wired up as an extension but does little today; the visible vocab
styling comes from the fenced-div classes in §5.

> Note: `_quarto.yml`'s `filters:` list names only `gifffer` and `checkpoint`.
> The `glossary` filter is not in the active list, so it's effectively dormant.

## 4. Built-in shortcodes

- **`{{< video … >}}`** (~8 uses) — embeds YouTube videos responsively, e.g.
  `{{< video https://youtu.be/8rfDb0A7XsA >}}`. A Quarto built-in.

## 5. Fenced divs with custom classes (Pandoc/Quarto extension)

The single biggest "beyond Markdown" feature is **fenced `:::` divs**. Plain
Markdown has no block-container syntax; Pandoc/Quarto add `::: {.class}` … `:::`,
which compiles to `<div class="class">`. The curriculum uses a large vocabulary
of project-specific classes (styled in `bjc.scss`), the most common being:

| Class | Purpose (approx.) |
|---|---|
| `learn` | red "On this page, you'll learn…" intro box |
| `forYouToDo` | green "For you to do" task box |
| `ifTime` | optional "if there's time" task |
| `takeNote` / `endnote` / `sidenote` / `sidenoteBig` | call-out notes & asides |
| `takeItFurther` / `takeItTeaser` / `takeItTeased` | extension activities |
| `vocab` / `vocabBig` / `vocabFullWidth` | vocabulary definition boxes |
| `ap-standard` | the CED standard tag callout (e.g. `DAT-1.D.1`) |
| `dialogue` / `stagedir` | scripted student dialogue |
| `atwork` / `atworkFullWidth` | "computing at work" profile boxes |
| `newProject` / `saveAs` | project-start / save-as instructions |
| `narrower` / `narrowblue` / `narrowpurple` | width/color variants |

These are not Quarto built-ins — they're custom classes given meaning by the
SCSS theme. Editors compose them with `::: learn` … `:::` blocks.

### Structured assessment divs

A QTI-flavored assessment structure is expressed as **nested attributed fenced
divs** (~38 `assessment-data` blocks), e.g.:

```markdown
::: {.assessment-data type="multiplechoice" identifier="…" maxchoices="1" responseidentifier="resp1" shuffle="false"}
::: prompt
Which statements are true about this list?
:::
::: {.choice identifier="c1"}
::: text
…
:::
::: feedback
…
:::
:::
:::
```

This uses Pandoc's **attributed div** syntax (`{.class key="value"}`) — arbitrary
key/value attributes on a div, which plain Markdown can't express. Related
classes: `prompt`, `choice`, `text`, `feedback`, `correctResponse`,
`responseDeclaration`.

## 6. Bootstrap integration

Because the HTML format is Bootstrap-based, pages use Bootstrap directly:

- **Grid layout** — `::: {.grid}` with `::: {.g-col-6}` / `g-col-xxl-4` columns,
  and utility classes like `.float-end`, `.ms-4` on divs/images.
- **Collapsible content / modals** — `data-bs-toggle` is used on ~73 pages.
  Hints are commonly written as a link plus a **`::: {#some-id .collapse}`** div
  (Bootstrap collapse), and the `checkpoint` shortcode emits a Bootstrap modal.
- A built-in **`callout-note`** is used once; mostly the project prefers its own
  `learn`/`takeNote`-style boxes over Quarto's standard callouts.

## 7. Front matter conventions

Per-page YAML front matter drives several behaviors beyond a Markdown title:

- **`title`**, **`subtitle`** (e.g. `"Unit 4, Lab 4, Page 6"`), and **`order`**.
  On lab pages the `Page N:` / `Lab N:` title prefix and the whole subtitle are
  derived from the file path and generated by **`fix-titles.py`**. `order`
  controls sidebar/listing sequence but is kept only where it isn't redundant
  with the filename number (~42 files), since Quarto orders auto-sidebar
  contents by filename when `order` is absent.
- **`pagetitle`** — a per-page override of the site-wide HTML `<title>`, set on
  the pages whose subtitle would make a poor tab title (absent or shared); it
  builds the title from `{{< metatext title >}}` instead of `subtitle`.
  `fix-titles.py` generates and enforces this: lab pages (distinctive subtitle)
  must have *no* `pagetitle`; every other page must carry exactly
  `pagetitle: "{{< metatext title >}}"` (see §2 and the `metatext` extension in
  §3).
- **`gifffer: true`** — opts a page into the GIF player (see §3).
- **`format:`** — per-page format overrides where needed (e.g.
  `unit-4/lab-4/5-binary.qmd` sets `html-table-processing: none`).
- **`include-in-header`** — page-local `<style>`/script injection (e.g. the home
  page hides its `h1` title this way).
- **Blog/listing fields** — `draft`, `description`, `date`, `date-modified`,
  `author`, `categories` are used by the posts section (see §8).

## 8. Listing pages and the blog (`posts/`)

`posts/index.qmd` uses Quarto's **listing** feature
(`listing:` with `contents`, `categories: true`, `sort`, `sort-ui`,
`filter-ui`, `page-layout: full`) to auto-generate an index of announcements and
"Computing in the News" entries. Categories come from per-folder
**`_metadata.yml`** files (`posts/announcements/_metadata.yml`,
`posts/citn/_metadata.yml`), which apply shared front matter to every post in a
directory — a Quarto directory-metadata feature. Drafts are hidden with
`draft: true`. Listing pages, directory metadata, and draft handling are all
Quarto-only.

## 9. Templates

`_templates/lab_temp.qmd` is a starter skeleton (not rendered into the site)
documenting the front-matter shape and the common `:::` classes for authors
creating a new lab page.

---

### Summary — what's "beyond Markdown" here

1. Website project: navbar, sidebars, search, page-nav, footer, SCSS theming.
2. Shortcodes: `{{< meta >}}`, `{{< video >}}`, and the custom
   `{{< checkpoint >}}` / `{{< metatext >}}`.
3. Four local extensions (`checkpoint`, `metatext`, `gifffer`, `glossary`) = Lua
   filters/shortcodes + bundled JS/CSS (`titling` was removed in favor of
   `fix-titles.py`).
4. Fenced divs with custom classes, including attributed divs for assessments.
5. Bootstrap grid, collapse, and modals.
6. Behavior-driving front matter (`order`, `gifffer`, `pagetitle`, `format`,
   `include-in-header`).
7. Listing pages + directory `_metadata.yml` for the posts/blog section.
