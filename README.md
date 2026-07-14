# BJC for Berkeley High School AP Computer Science Principles

Check it out at [bjc.jacketcs.net](https://bjc.jacketcs.net)

This is a work in progress. 

## Editing

The website uses [Quarto](https://quarto.org/docs/guide/), utilizing Markdown to create a bootstrap themed website. Most things that you will want to edit are in the `unit-*` folders.

You can also create individual posts for CITN or general announcements with the files in the `posts/` files.

**This project is set up to only render `.qmd` files**. `.md` files should be reserved for documentation.

### Snap Starter Codes

Add them to the `prog/` folder.

## Building the website

The site is built with [Quarto](https://quarto.org/). The live site is rendered with a **pinned** Quarto version so everyone sees the same output — currently **1.9.38**. The source of truth for the version is `version:` in `.github/workflows/main.yml`; use that same version locally so your preview matches the deployed site.

### Installing Quarto on a Mac

Pick one:

- **Match the live version (recommended).** Download the macOS installer `quarto-1.9.38-macos.pkg` from the [v1.9.38 release page](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.9.38) and open it. (If the workflow pins a different version, grab that one instead.)

- **Homebrew (installs the latest).** Run `brew install --cask quarto`. This is quick, but Homebrew tracks the newest release, which may not match the pinned version above.

Confirm it installed:

```
quarto --version
```

### Previewing while you edit

For a live-reloading dev server — it rebuilds as you save and opens on port 1000 (set in `_quarto.yml`):

```
quarto preview
```

### One-time render

To build the whole site once (output goes to `_site/`):

```
quarto render
```

## Disclaimer

The code, styling, curriculum, and text on this website is adapted from The Beauty and Joy of Computing by University of California, Berkeley and Education Development Center, Inc. which is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

## License

[CC BY-NC-SA 4.0][cc]

![CC_IMG][cc_img]

[cc]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[cc_img]: https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png

