---
title: Third-party components
description: What comes from other authors inside Teclado360, with each one's license.
---

Teclado360 is written by us, without third-party libraries. Some data, fonts and the languages' standard libraries
come from other authors and follow the licenses below, which take precedence over the [License agreement](licenca.html)
for those components.

| Component | Where | License | Authors |
|---|---|---|---|
| G360 Matematica font (regular, bold, letters, sets, sizes 1 and 2), derived from the KaTeX fonts, with new G360 family glyphs (∯ and ∰) | Formula drawing | SIL Open Font License 1.1 | Design Science, Inc. (2009-2010) and Khan Academy (2014-2018), in the original fonts with the reserved name KaTeX; modifications by Lucas Matos e Souza (2026) |
| KaTeX font metrics (height, depth, width) | Keyboard engine | MIT | Khan Academy and other contributors (2013-2020) |
| Portuguese and English word lists (FrequencyWords, OpenSubtitles 2018 subtitles), filtered by the LibreOffice dictionary | Suggestions and swiping | CC BY-SA 4.0 | Hermit Dave |
| Blocked words list (List of Dirty, Naughty, Obscene and Otherwise Bad Words) | Blocking profanity in suggestions | CC BY 4.0 | The list's authors |
| Rust standard library | Keyboard engine | MIT or Apache 2.0, at your option | The Rust Project Developers |
| Kotlin standard library | Android app | Apache 2.0 | JetBrains s.r.o. and contributors |

The word lists ship as a separate file inside the app and remain under CC BY-SA 4.0: you may copy and adapt them
under that license, which does not extend to the rest of the app.

The G360 Matematica font may be used, studied, modified and redistributed under the SIL Open Font License 1.1, but it
may not be sold by itself. The font parameters of Donald Knuth's Computer Modern, used in the drawing, are published
numerical values.

## License texts

- SIL Open Font License 1.1: [openfontlicense.org](https://openfontlicense.org)
- MIT (KaTeX): [github.com/KaTeX/KaTeX/blob/main/LICENSE](https://github.com/KaTeX/KaTeX/blob/main/LICENSE)
- CC BY-SA 4.0: [creativecommons.org/licenses/by-sa/4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- CC BY 4.0: [creativecommons.org/licenses/by/4.0](https://creativecommons.org/licenses/by/4.0/)
- Rust (MIT and Apache 2.0): [github.com/rust-lang/rust/blob/master/COPYRIGHT](https://github.com/rust-lang/rust/blob/master/COPYRIGHT)
- Apache 2.0 (Kotlin): [www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)

The app carries a copy of each of these texts, on the "About and licenses" screen.
