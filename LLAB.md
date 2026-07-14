# LLAB.md

An investigation of the `llab/` JavaScript and how it's actually used on this
site. `llab/` is a self-contained copy of the upstream "Lightweight Labs"
framework (from [`bjc-r`](https://github.com/beautyjoy/bjc-r/)) dropped into
this Quarto site. Most of it is vestigial; only three code paths run against
this site's content.

## How it's wired in

`llab/` connects to the site in exactly two places in `_quarto.yml`:

- `resources: - "/llab/"` (line 10) copies the whole directory to the site verbatim.

- `include-in-header` (line 98) injects `<script src="/llab/loader.js">` into **every** rendered page.

`loader.js` is the only entry point. It defines a global `llab` object with a
hardcoded config (`rootURL` = `/`, `install_directory` = `llab/`), then loads
the rest of the scripts in three dependency-gated stages, polling
`stage_complete_functions` every 2 ms:

- **Stage 0:** `lib/jquery.min.js`, `script/library.js`, `script/quiz/multiplechoice.js`

- **Stage 1:** `script/curriculum.js`, `script/course.js`, `script/topic.js`

- **Stage 2:** `script/quiz.js`

Each script sets a `llab.loaded[...]` flag; the gates wait on those.
(`lib/sha1.js` "for brainstorm" is commented out and never loaded.)

## The three live features

Everything hangs off `$(document).ready` handlers in the loaded scripts. Only
three of them do anything on this site's content.

### 1. Snap! "run" link rewriting — the primary feature

`curriculum.js` → `llab.secondarySetUp()` finds every `<a class="run">` and
rewrites its `href` through `llab.getSnapRunURL()` (in `library.js`) so the link
opens the linked project XML inside the Snap! web IDE, in a new tab.

- **Used:** 31 `class="run"` links across 29 files, all pointing at `/prog/.../*.xml`.

- **Fragile mechanics (both real):**

    - `getSnapRunURL` bails out unless the href contains
      `window.location.hostname`. A raw `/prog/…` path *doesn't* — it only works
      because Quarto's own `quarto-nav.js` absolutizes every anchor to
      `https://bjc.jacketcs.net/prog/…` **before** `secondarySetUp` runs.
      Ordering-dependent.

    - `llab.hostDomain` is hardcoded to `https://bjc.jacketcs.net`, so even under
      `quarto preview` the run links point at **production** XML, not your local
      copy.

### 2. Collapsible "optional content" — heavily used

Also in `secondarySetUp`: it finds `div.ifTime`, `div.takeItFurther`, and
`div.takeItTeased`, wrapping each in a Bootstrap collapse toggle button labeled
"If There Is Time…" / "Take It Further…". Add class `show` to a div to expand it
by default.

- **Used:** `ifTime` in 49 files, `takeItFurther` in 46, `takeItTeased` in 4 — written as bare fences (`::: ifTime`, `::: takeItFurther`).

- These classes are *also* styled by `bjc.scss`, so they're a joint SCSS-styling + JS-behavior feature.

### 3. Multiple-choice self-check quizzes — used, and it genuinely works

`quiz.js` → `buildQuestions()` scans `div.assessment-data`, dispatches by
`type`, and `multiplechoice.js` (the `MC` class) builds an interactive Bootstrap
card with Check Answer / Try Again, per-choice feedback, and correct/incorrect
styling.

- **Used:** 21 files, 38 questions, all `type="multiplechoice"`.

- **The subtle part:** `multiplechoice.js` reads `data-`-prefixed, lowercased
  attributes (`data-responseidentifier`, `data-shuffle`, `data-maxchoices`,
  `data-identifier`) while the `.qmd` authors write them unprefixed
  (`responseidentifier="ri1"`, `shuffle="false"`, …). Pandoc's HTML5 writer
  **auto-prefixes** custom fenced-div attributes with `data-` (and lowercases
  them), so `responseidentifier` → `data-responseidentifier`, etc. The markup
  matches the JS by accident of Pandoc's behavior. `type` stays unprefixed,
  which is also exactly what `quiz.js` reads. The quizzes are functional — but
  this is an undocumented, fragile dependency on Pandoc's attribute handling.

## Loaded but inert on this site

These scripts load on every page but their `document.ready` handlers find
nothing to act on:

- **`course.js`** (`editURLs`) — only does work when the page path is under
  `/course/` and contains `.topic_container` / `.topic_link` elements. This site
  has none (0 uses); it's a no-op.

- **`topic.js`** — a whole `.topic` file parser (`renderFull`), but its handler
  only fires on URLs containing `topic.html` or `empty-topic-page.html`, which
  don't exist here. Entirely dormant. It's also the *only* caller of
  `library.js`'s `setUpDevComments`, so that never runs either.

## Fully dead code (never loaded at all)

- **`renderContent.js`** — a near-duplicate of the run-link + collapsible logic.
  Nothing references it; the only script tag anywhere is `loader.js`. Dead. (Its
  `getSnapRunURL` even uses a *different, better* internal-link test —
  `indexOf('http')==0` — that wouldn't need the quarto-nav absolutizing trick.)

- **`script/glossary.js`** — not in any loader stage; unused.

- **`lib/sha1.js`** — commented out in the loader.

## Dead branches inside live files

- **`js-run` handling** (`curriculum.js`, `renderContent.js`) — 0 `js-run` elements in content.

- **`inline-multiplechoice` / `IMC`** (`quiz.js:8-9`) — dispatches to
  `new IMC(...)`, but `IMC` is **never defined anywhere**. Would throw a
  ReferenceError if used; no content uses it, so it never fires.

- **Dev-comment toggle** (`library.js`: `toggleDevComments`,
  `setUpDevComments`, `canShowDevComments`) — only invoked from the dormant
  `topic.js`. The 11 `.todo`/`.comment`/`.commentBig` boxes in content
  (7 + 3 + 1) are simply hidden by `bjc.scss` (`display: none`), never toggled by
  llab.

- **Most of `library.js`'s utilities** — cookies, `merge`, `any`/`all`/`which`,
  `truncate`, `spanTag`, plus `curriculum.js`'s `addFrame`, `additionalSetup`,
  `isCurriculum`, `thisPageNum` — none are called by the three live features. The
  only parts of `library.js` that matter here are `getSnapRunURL`, the
  `llab.selectors`/`strings`/`fragments` constants, and `getAttributesForElement`
  (used by the inert `course.js`).

## Bottom line

Of the ~15 files in `llab/`, this site actively exercises **three code paths**:
run-link rewriting and collapsible content (both in `curriculum.js`, calling
into `library.js`), and multiple-choice quizzes (`quiz.js` +
`multiplechoice.js`). Everything else — `renderContent.js`, `glossary.js`,
`topic.js`, `course.js`, `sha1.js`, and the topic/course/glossary config in
`loader.js` — is vestigial framework machinery carried over from upstream
`llab`'s directory-driven "topic/course" model, which this Quarto site replaced
with its own navbar/sidebar and never uses.

Two things worth flagging if anyone touches this:

- The quizzes silently depend on Pandoc's `data-` attribute prefixing.

- The run links silently depend on `quarto-nav.js` absolutizing hrefs first, plus a production-hardcoded `hostDomain`.

Both work today but neither is obvious from the code.
