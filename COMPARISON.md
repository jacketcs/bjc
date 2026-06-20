# Comparison: `bjc` (Quarto) vs. `bjc-r` (upstream HTML)

This document compares this repository (`bjc`) against the upstream
[`bjc-r`](https://github.com/bjc-edc/bjc-r) repository it was derived from.
The goal is to record **what is missing** and **what changed substantively**,
ignoring pure markup/formatting differences (HTML → Markdown, tabs, whitespace,
`<h2>` → title frontmatter, etc.) that are an expected part of the conversion.

> **Sources compared**
>
> - `bjc` (this repo, the `compare` worktree) — a Quarto website, 198 `.qmd` files.
> - `bjc-r`: `/Users/peter/hacks/bjc-r` — the full upstream curriculum repo (HTML + Ruby/Jekyll tooling).

## 1. The big picture

`bjc-r` is the complete Beauty and Joy of Computing curriculum repository: the
high-school AP CSP course, a middle-school course (`sparks/`), Spanish
translations, teaching guides, performance tasks, social-context readings, and
all the lab-runner infrastructure.

`bjc` is a **focused Quarto rebuild of just the AP CSP "programming" course,
Units 1–6**, plus its Snap! starter code and images. It is not a full mirror —
it deliberately reproduces one slice of `bjc-r` in a new toolchain. As a result:

- The **per-page instructional prose for Units 1–6 is largely carried over
  faithfully.** Most pages match the source paragraph-for-paragraph.
- **Large supporting/peripheral sections of `bjc-r` are dropped entirely**
  (see §2).
- A consistent set of **systematic edits** was applied during conversion (see §3).
- Some **new content was authored** that has no upstream source (see §6).

## 2. Whole sections of `bjc-r` NOT present in `bjc`

These exist in `bjc-r` and have no counterpart in `bjc` at all.

### 2.1 Other courses / large content trees

- **Middle-school course** — `sparks/` (≈873 files). Entirely absent.
- **Topic-based labs** — `topic/` (≈149 files). Absent.
- **Standalone "course" pages** — `course/` (17 files). Absent.
- **`eir/`, `mini/`, `teacher/`, `teachers/`** stub/landing dirs. Absent.

### 2.2 Curriculum sections under `cur/` (outside Units 1–6)

- **Unit 7 — Recursion** (`cur/programming/7-recursion`, 11 English pages). Not converted.
- **Unit 8 — Recursive Reporters** (`cur/programming/8-recursive-reporters`, 17 English pages). Not converted.
- **Unit 3.5 — Team Programming Project / T1PP** (`cur/programming/3.5-T1PP`, 6 pages). Not converted as a unit. *(Note: this is distinct from the per-unit `lab-*.5` pages that DO exist in `bjc` — those are new, see §6.)*
- **`cur/social-context/`** — readings (apps, areas, concerns, future, history, misc). Absent.
- **`cur/teaching-guide/`** — full teacher guides for every unit (U1–U8, AP, T1PP). Absent.
- **`cur/solutions-assessments/`** — solution/assessment pages for Units 1–8. Absent.
- **`cur/performance-tasks/`** — partly carried over: the AP Create Task became `create-task/` in `bjc` (see §6); the Explore Task and other performance-task pages were not.

### 2.3 Per-unit reference pages (dropped for every unit)

For **every** Unit 1–6, the three standalone unit-level reference pages were dropped:

- `unit-N-self-check.html`
- `unit-N-vocab.html` (the glossary page; inline `vocab`/`vocabFullWidth` callouts *within* lab pages were kept)
- `unit-N-exam-reference.html` (Units 1, 2, 3, 5 had these)

Also dropped: the per-unit standalone `assessment-dataN.html` banks (Units 2, 3, 5, 6).

### 2.4 Spanish translations

Every page in `bjc-r` has a parallel `*.es.html` translation. **None** were
carried over. `bjc` is English-only.

### 2.5 Archived / draft material (expected drops)

`old/`, `semi-old/`, `very old/`, `future/`, `unused-new-stuff/`, `*-old`,
and `*-draft` files throughout `bjc-r` were not converted. These are superseded
drafts; dropping them is almost certainly intentional and not a content loss.

## 3. Systematic (cross-cutting) changes in the converted units

These patterns recur across most or all of Units 1–6:

- **AP-standard tags stripped.** Inline `ap-standard` labels (e.g. `AAP-1.B.1`,
  `CRD-2.C`, `DAT-*`) were removed throughout.
- **Inline multiple-choice self-check questions removed**, frequently replaced
  by a Google-Form `{{< checkpoint >}}` shortcode. The question text, answer
  options, and per-answer feedback are lost when this happens. This is the
  single largest category of substantive content loss within converted pages.
  *(Handling is inconsistent — a few pages instead re-encoded the MCQs into
  Quarto `::: {.assessment-data}` blocks, preserving them; see Units 3 and 6.)*
- **"What would this look like in Python?" collapsible hints removed** (most visible in Unit 1).
- **Author-to-author editorial comments dropped** (e.g. `--MF, 7/4/20` notes) — generally a good cleanup.
- **New navigation landing pages added** — each unit has an `index.qmd`, and most labs have a `lab-N/index.qmd`. These have no upstream equivalent.

## 4. Per-unit detail

### Unit 1 — Introduction (`1-introduction`)

**Missing pages**

- `3-drawing/7-programming-journal.html` — "Keeping a Programming Journal" dropped entirely.
- `6-optional-projects/1b-sprite-line-art-hints.html` and `1c-sprite-line-art-interactive.html` — dropped (hint images + embedded answer iframe lost).
- `6-optional-projects/2-row-of-houses.html` — relocated & redesigned into a new `lab-3.5` (see below).
- Self-check, vocab, exam-reference: dropped (see §2.3).

**Reordered / renamed / added**

- **Lab 1 pages 1 & 2 swapped**: source "Start Your First Snap App" / "Creating a Snap Account" → converted "Creating a Snap Account" / "Start Your First Snap App". The new page 1 was also substantially rewritten (account creation/login content replacing the old "Saving Snap! Projects" A/B/C options).
- `3b-pong-hints.html` was **inlined** into `optional-projects/3-pong.qmd` as a collapsible block (preserved, not lost).
- New `project/index.qmd` "Project: eCard" (no source counterpart).
- New `lab-3.5` "Row of Houses" — redesigned from the optional project: `repeat until` (draw-to-edge) task replaced with a fixed-count `repeat`; the "how does repeat until keep the sprite off the edge?" question removed; new exercises + checkpoints added.

**Notable substantive content changes**

- **Lab 4 (Privacy) drifted the most** — appears rebuilt from a newer revision: privacy-law section rewritten (added CCPA/CPRA, COPPA, GDPR), tracking-tool discussion modernized (uBlock Origin, Privacy Badger, device fingerprinting, behavioral biometrics); Facebook→Meta/Instagram; several MCQs dropped.
- **"At Work" biography boxes dropped**: Edith Windsor (L2p3), Tim Cook (L4p2), Rana el Kaliouby (L4p4). *(Diana Macias in L5p1 was kept.)*
- L5p1: leader-follower animation GIF dropped.
- Several student dialogue names changed (Morgan/Omar/Jasmine → Alphie/Gamal/Betsy).

**Minor conversion bugs flagged**: duplicated endnote in `lab-2/1-pair-programming.qmd`; stray unclosed `</ul>` in `lab-4/1-your-image-in-the-cloud.qmd`.

### Unit 2 — Complexity / "Abstraction" (`2-complexity`)

> Note: the converted unit titles itself "Unit 2: Abstraction" though the source dir is `2-complexity`.

**Missing pages**

- `1-variables-games/6-keeping-a-journal.html` — dropped.
- `6-optional-projects/3-mastermind.html` — Mastermind project dropped.
- `2-data-structures-art/assessment-data2.html` and `functional-programming.html` — dropped.
- Self-check, vocab, exam-reference: dropped.

**Reordered / renamed / added**

- New `lab-2.5/index.qmd` "Flashcards" — **newly authored**, no HTML source (uses real assets `prog/2-complexity/U2L2-5-Flashcards.xml`).
- New `project/index.qmd` "Project: Survey" — **newly authored**, no HTML source.

**Notable substantive content changes**

- **Biographical boxes removed**: Jerry Lawson (L1p3), Reshma Saujani (L2p2).
- L2p1 (shopping list): meaning change — source had students *create* the global variable; the qmd says it "has already been created for you." A new "take it further" section (5 activities + video) was added.
- L1p5: new YouTube video embed added.
- L2p2: new "take it further" content added.
- L4p2 (math predicates): Google Trends / Web-API extended example removed.
- Many inline MCQs removed/commented (≈30 `multiplechoice` blocks in source).

**Minor flag**: image path `min-of-3-and--4-reporting.png` (double dash) in L4p3 — verify the asset exists.

### Unit 3 — Lists (`3-lists`)

**Missing pages — largest structural losses of any unit**

- **Entire `5-work/` lab dropped** (3 pages: past-and-future, working-conditions, working-remotely). There is no `lab-5` in the conversion.
- **Entire `investigations/` directory dropped** (5 pages: chords, display-word, exaggerate, longest-word, processing-a-sentence).
- `2-contact-list/assessment-data3.html` dropped.
- Self-check, vocab, exam-reference: dropped.

**Reordered / renamed / added**

- New `lab-3.5` "Monty Hall Simulator" project (`montyHall.qmd` + `index.qmd`, image, Snap! starter link) — **net-new, no source anywhere**.
- `4-robots-ai/4-breakthroughs-possibilities.html` → `lab-4/4-recent-developments.qmd` (renamed; prose essentially unchanged, just retitled and an author note removed).

**Notable substantive content changes**

- Mostly faithful prose. Inconsistent self-check handling: the MCQ on `lab-2/1-build-the-list` was **dropped**, while the self-checks on `lab-2/5-mapping-over-list` were **kept** (re-encoded as `.assessment-data` blocks).

### Unit 4 — The Internet (`4-internet`)

**Missing pages — several whole sections dropped**

- **`X-gps-data/`** (3 pages: GPS coordinates / interpreting / analyzing). Dropped.
- **`Y-innovations/`** (3 pages: identifying issues / address the issue / unintended consequences). Dropped.
- **`new/`** (2 pages: Cloud Computing, Intro to Internet APIs). Dropped.
- **`optional-projects/`** (5 pages incl. Binary Timer, TCP, writing-html). Dropped.
- **`old-search-internet/`** (2 live pages: how-searching-works, design-your-own). Dropped.
- `5b-binary-alternate.html` dropped — but this is an internal author discussion doc, not a student page (no real loss).
- Self-check, vocab: dropped. *(Page-level inline MCQ self-checks within labs were kept here.)*

**Reordered / renamed / added**

- New Unit 4 Project "Binary Converter" in `unit_4_prpj/index.qmd` — does not exist upstream (and is distinct from the source's "Binary Timer" optional project).
- **Likely artifact to clean up**: the unit contains BOTH `unit_4_prpj/` (the real project dir) and `unit_4_project` (a stray **1-byte** file — a lone newline). The `prpj` spelling also looks like a typo for `project`.

**Notable substantive content changes**

- The four core labs (1–4, 24 pages) are otherwise a faithful conversion — vocab boxes, "For You To Do"/"If There Is Time", hints, "At Work" bios, and inline MCQ self-checks all carried over.
- **One regression**: `lab-3/3-censorship.qmd` "For You To Do #4" reverts to an **older resource** than the source — converted points to a 2015 Business Insider infographic; the source uses a 2024 Freedom House internet-censorship map. Worth fixing.
- Cosmetic artifacts: stray empty `****` in `lab-4/3-representing-numbers.qmd`; a dropped paren in `lab-3/7-collaboration.qmd`.

### Unit 5 — Algorithms (`5-algorithms`)

**Missing pages — whole sections dropped**

- **`7-other-programming-languages/`** entire section (3 pages: sequential languages, primitives in other sequential languages, non-sequential languages — ≈8,800 words). Dropped.
- **`mutation/`** entire section (3 pages: mutate-vars, swap-list-values, swap-two-list-values). Dropped.
- **`optional-projects/`** (tic-tac-toe computer player). Dropped.
- `3-turning-data-information/assessment-data5.html` (≈2,000 words). Dropped.
- Self-check, vocab, exam-reference: dropped.

**Reordered / renamed / added**

- Labs 1–6 map cleanly; all 25 core lab pages converted. New per-lab and unit `index.qmd` landing pages.

**Notable substantive content changes**

- The recurring loss is **AP-practice MCQ blocks (with data tables and per-answer feedback) replaced by Google-Form checkpoints**:
  - `lab-3/2-self-check.qmd` — largest single loss (837 → 132 words): all 4 MCQs removed (bird-tracking, pattern searching, ride-hailing trends, music-download table).
  - `lab-1/5-categorizing-algorithms.qmd` — dropped the "computer time by town size" data-table question + explanations.
  - `lab-1/6-heuristics.qmd` — dropped the "where is a heuristic appropriate?" MCQ.
- Otherwise prose is faithful (spot-checks match paragraph-for-paragraph). `lab-1/1-sorted-lists.qmd` adds an embedded YouTube video.

### Unit 6 — How Computers Work (`6-computers`)

**Missing pages**

- **`optional-projects/`** (2-adder, binary-adder, weather-app "Teacher's Choice" project). Dropped.
- `2-history-impact/assessment-data6.html` dropped as a standalone page.
- Self-check, vocab: dropped.
- Binary assets (`ComputerComponents.docx/.pdf`, `MooresLawDiagram.xlsx`) not carried over.

**Reordered / renamed / added**

- New `project/project.qmd` "Unit 6 Project: Educational Game" — **net-new** (by "Ms. Chang and Ms. O'Keefe"); a Snap! game-design project. Not derived from the dropped optional projects. Cross-links to `/unit-2/lab-2/2-quizzes.qmd`.
- New per-lab and unit `index.qmd` pages.

**Notable substantive content changes** (this unit is otherwise a high-fidelity conversion, even preserving teacher TODO comments as raw blocks)

- `lab-1/06-digital-architecture` — **Ada Lovelace passage rewritten/expanded** with new hedging ("…although it's almost certain that Babbage himself wrote several example programs…"; "Whether or not she was truly the first programmer…"); renamed "Augusta Ada King-Noel, Countess of Lovelace." (Built from a newer revision.)
- `lab-2/2-moore` — **factual correction**: "3TB of memory (3 billion MB)" → "3 million MB".
- `lab-2/1-timeline` — added "Answer this on the Google Form" to questions; new "this timeline is outdated" note; cross-link changed from "Unit 4, Lab 3 (A Hierarchy of Open Protocols)" → "Unit 4, Lab 1 (What Is the Internet?)".
- `lab-1/09-digital-logic-gates` — MCQ self-checks **preserved**, re-encoded as structured `.assessment-data` blocks (content intact, format changed).

## 5. Supporting assets and infrastructure

- **`prog/` (Snap! starter code, `.xml`)** — carried over nearly intact (258 files vs. 286 upstream). The upstream **`prog/python/`** subdir was dropped (consistent with the Python-hint removal in §3); other subdirs match.
- **`img/`** — carried over heavily (≈4,300 files).
- **`llab/` (lab-runner / loader)** — a trimmed version is present (loader.js, renderContent.js, script, lib, docs); upstream's `build/`, `css/`, `fonts/`, `html/`, `img/` subdirs were dropped.
- **`data/`** — present (9 files).
- **Cheat sheets** — `snap-cheat-sheet.qmd` (from `cur/snap-cheat-sheet.html`) and a new `costume-cheatsheet.qmd`.
- **Upstream Ruby/Jekyll tooling dropped** (expected — different toolchain): `Gemfile`, `Gemfile.lock`, `.rspec`, `utilities/` (59 files incl. build-tools), `docs/` (28 files), `.htaccess`, `robots.txt`, the `index_*.html` variants, `pd.html`, etc. Replaced by Quarto config (`_quarto.yml`, `_extensions/`, `_templates/`, `.github/workflows`, SCSS themes).

## 6. AP CSP standards (CED) mapping

`bjc-r` maps the College Board Course and Exam Description (the `CRD-1.B.2` /
`DAT-1.D.4` identifiers) to the curriculum in several places. None of these were
carried into `bjc` during the initial conversion:

- **`cur/teaching-guide/resources/standards-map.html`** — the canonical
  crosswalk, "Mapping from AP CSP Standards to BJC." Organized by the five Big
  Ideas (CRD, DAT, AAP, CSN, IOC), it maps **397 distinct CED IDs** down to the
  Essential-Knowledge level and links each to the exact page/problem/vocab box
  where it is taught.
- **Inline `ap-standard` tags** embedded next to content in ~137 source lab
  pages (the reverse direction). These were **systematically stripped** during
  conversion (see §3), so the per-page annotation that `standards-map.html`
  indexes no longer exists in `bjc`.
- **`cur/teaching-guide/AP/ap-standards.html`** — an *older* mapping to the
  pre-2020 framework (Big Ideas / Learning Objectives / old EK numbering, not
  the current CRD/DAT IDs). Historical only.
- **Per-unit `unit-N-exam-reference.html`** (Units 1, 2, 3, 5) and
  **`cur/teaching-guide/U4/assessment/u4-Internet@APStandards.pdf`** — also dropped.

### Ported into `bjc`: `standards-map.qmd`

This repo now contains a Quarto conversion of the standards map at
**`standards-map.qmd`** (registered in the Resources navbar menu), generated by
**`convert_standards_map.py`** (re-runnable if upstream changes). The script
parses the source HTML, rewrites every link to the new site paths, and verifies
each target exists. Conversion results:

- **415** EK/LO links resolved directly to converted `.qmd` pages.
- **1** link fixed via an explicit rename map: Unit 1 Lab 1's swapped pages
  (`1-start-your-first-snap-app` → `/unit-1/lab-1/2-start-your-first-snap-app.qmd`).
- **28** AP **Create Task** links redirected to this site's `/create-task/`
  section (the Create Task guide was rewritten and does not map page-for-page;
  the descriptive text — e.g. "Page 3, problem 2" — is retained so the location
  is still findable). A `callout-note` on the page explains this.
- **2** links left **unresolved** and rendered as plain text (no link), both
  pointing at the dropped Unit 3 `5-work/` lab (IOC-1.A → "Unit 3, Lab 5,
  Pages 1–2"). These are dead because that lab was not converted (see §4, Unit 3).

Note: the upstream map does not reference any **Unit 6** (`6-computers`) pages,
so the converted map has no Unit 6 links either — that is a property of the
source, not a conversion gap.

## 7. New content authored in `bjc` (no upstream source)

- **Per-unit individual projects**: U1 "eCard", U2 "Survey", U3 "Monty Hall Simulator", U4 "Binary Converter", U6 "Educational Game" (the `lab-*.5`, `project/`, and `unit_4_prpj/` dirs). These are new and reference real Snap! assets, but they are not conversions of any upstream page.
- **U2 `lab-2.5` "Flashcards"** — newly authored.
- **`create-task/`** — AP Create Performance Task guide (program-code, video, PPR, resources, submitting), adapted from `cur/performance-tasks/AP-create-task`.
- **`posts/`** — a Quarto blog: announcements + "CITN" (Computing in the News) entries with templates. New to this repo.
- **Unit/lab `index.qmd` landing pages** throughout.
- **`costume-cheatsheet.qmd`**.

## 8. Items worth a second look (potential bugs / regressions)

1. **`unit-4/unit_4_project`** — stray 1-byte file alongside `unit_4_prpj/`; likely accidental. Also `prpj` looks like a typo for `project`.
2. **`unit-4/lab-3/3-censorship.qmd`** — uses a 2015 censorship resource where the upstream source had a newer (2024) one — a content regression.
3. **Inconsistent self-check handling** — some MCQs were dropped, some converted to Google-Form checkpoints, some re-encoded as `.assessment-data` blocks. If the assessments matter pedagogically, the dropped ones (esp. Unit 5 `lab-3/2-self-check`, Unit 5 `lab-1/5` & `6`, Unit 3 `lab-2/1`) are real losses.
4. **Dropped whole sections that may have been wanted**: U3 `5-work/` lab and `investigations/`; U4 `X-gps-data`/`Y-innovations`/`new`; U5 `7-other-programming-languages`/`mutation`. Confirm these were intentional cuts vs. oversights.
5. **Minor markup artifacts**: duplicated endnote (U1 L2p1), unclosed `</ul>` (U1 L4p1), empty `****` (U4 L4p3), double-dash image filename (U2 L4p3) — verify these render correctly.
6. **No Spanish, no Units 7–8, no teaching guides / solutions** — fine if the scope is "the English student-facing AP CSP course," but a significant reduction from upstream if a fuller mirror was intended.
