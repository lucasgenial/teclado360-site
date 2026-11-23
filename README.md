# Teclado360 website

The public website for Teclado360, served by GitHub Pages at [teclado360.app](https://teclado360.app): the landing page and the documentation, in Brazilian Portuguese (root) and English (`en/`).

- `content/pt/` and `content/en/`: documentation pages in Markdown.
- `assets/`: styles, images, fonts and `kernel.json` (formula pictures drawn by the real kernel).
- `tools/build.py`: builds the site into `site/` (needs pandoc). Run `python3 -I tools/build.py`.
- `tools/kernel_assets.js`: regenerates `assets/kernel.json` from a kernel checkout: `node tools/kernel_assets.js PATH/TO/teclado360-kernel`.
- `site/`: the built website that GitHub Pages serves.

Copyright (c) 2026 Lucas Matos e Souza. All rights reserved.
