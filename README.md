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

The live website uses [Quarto Version 1.3.353](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.3.353). So you may want to download this version to see the same visual content as the live version. (We can change the version in `.github/workflows/main.yml`)


When authoring the website, you'll want to use the

```
quarto preview
```

in the terminal

If you just want a single time render, you can use

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

