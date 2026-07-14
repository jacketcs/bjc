# Metatext Extension

Provides a `metatext` shortcode that emits the **plain-text** value of a
front-matter field.

## Using

```
{{< metatext KEY >}}
```

It behaves like Quarto's built-in `{{< meta KEY >}}`, except any inline HTML or
markdown formatting in the field is stripped (via `pandoc.utils.stringify`).

## Why

Some page titles contain HTML so a character renders a particular way in the
navbar/sidebar — e.g. `title: "Snap<em>!</em> Cheat Sheet"`, where `<em>`
italicizes the `!` in "Snap!". The HTML `<title>` element can only hold text, so
interpolating the raw title into `pagetitle` leaks a literal `Snap<em>!</em>`
into the browser tab. `metatext` yields `Snap!` instead.

That is exactly how this site uses it: every `pagetitle` is built with
`metatext` rather than `meta` — the site-wide one in `_quarto.yml` and the
per-page overrides in front matter:

```yaml
pagetitle: "{{< metatext title >}} | {{< var title-fix >}}"
```
