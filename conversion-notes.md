# Things to convert files

Just some things I did to convert the source bjc-r `.html` files to `.qmd` format

## 1. Find all giffer containing files

i.e. find all files that have

``` html
<script type="text/javascript" src="/bjc-r/utilities/gifffer.min.js"></script>
<script type="text/javascript">window.onload = function() {Gifffer();}</script>
<link rel="stylesheet" type="text/css" href="/bjc-r/css/bjc-gifffer.css">
```

and add a `gifffer: true` after the `</h2>` tag

## 2. Delete all tabs

Match all `\t` with regex and replace all with nothing

## 3. Delete initial html heading code

Match:

``` regex
<!DOCTYPE html>[\s\S\n]*?<h2>
```

Replace with 

``` md
---
title: "
```

Match: `</h2>`

Replace with: 

```
"
subtitle: "Unit , Lab , Page "
order:
editor: 
    markdown: 
        wrap: 72
```

## 4. Other changes

Change all `<h3>` to `##`, delete closing `</h3>`
Change all `<h4>` to `###`, delete closing `</h4>`
Change all `<h5>` to `##`, delete closing `</h5>`

## 5. bash commands to change .html to .qmd

``` bash
find /mnt/c/users/equil/projects/bjc -type f -name "unit-*.html
" -exec bash -c 'mv "$1" "${1%.html}.qmd"' _ {} \;

find ./  -type f -path "*/unit-*/lab-*.html" -exec bash -c 'mv
"$1" "${1%.html}.qmd"' _ {} \;
```

