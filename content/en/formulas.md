---
title: Formula mode
description: The math keyboard that shows up in formula fields, with the gallery of structures and the formula drawing.
---

In fields the app marked for formulas, Teclado360 swaps the text keyboard for the math keyboard. You build the
formula and it appears drawn as in a textbook while you type. In ordinary fields, nothing changes: the text keyboard
gets no new keys.

## The screens

| Screen | What it has |
|---|---|
| **123** | Numbers, x and n, fractions, powers (□², □ⁿ), roots, parentheses, absolute value, π, e, ∞, ≤ and ≥ |
| **f(x)** | sen, cos, tg, log, ln, limit, Σ, ∫, derivative, quantifiers, sets, arrows, vector and angle |
| **abc** | Letters, for variables and names |
| **αβγ** | Greek letters, lowercase and uppercase |
| **□⁄□…** | The gallery of structures |

The last row is the same on every screen: **←** and **→** move the cursor, **⇥** goes to the next blank and **↵**
delivers the formula. Keys with a dot in the corner have more options: hold to see them (on **=**, for example, ≠,
≈, ≡, ≅ and ∼).

The function names follow Brazilian notation (sen, tg); in English, sin and tan are on the same keys, by holding them.

## Gallery of structures

The **□⁄□…** key opens the gallery, organized like Word's equation ribbon: fraction, script, radical, integral, large
operator, delimiters, function, accent, limit and log, operator and matrix. Each structure appears drawn, the way it
will look. Tap one and it goes into the formula with blanks (□) for you to fill in.

## Blanks and what you already typed

- A structure takes along what is to the left of the cursor when it makes sense: typing **12** and tapping **□/□**
  puts 12 in the numerator and the cursor in the denominator.
- **⇥** moves to the next blank. Typing in a selected blank fills it.
- **⌫** deletes to the left; at the start of a structure, it takes the structure apart and keeps what was inside.

## Typed shortcuts

Type the word and it becomes the symbol:

| Type | Becomes |
|---|---|
| `sqrt` or `raiz` | √ |
| `pi` | π |
| `alpha`, `beta`, `theta`, `delta`… | α, β, θ, δ… |
| `infty` | ∞ |
| `sin`, `cos`, `tan`, `log`, `ln` | the functions |
| `<=`, `>=`, `!=`, `+-`, `->` | ≤, ≥, ≠, ±, → |

A shortcut that can still grow waits for the word to end: **cos** only becomes cosine when you type something else,
because it could still become **cossec**.

## Tap on the formula

Tap anywhere on the drawn formula to put the cursor there. On the top half of a fraction, the cursor goes to the
numerator; on a matrix cell, to the cell. Tapping a parenthesis puts the cursor outside it, and tapping a blank
selects it.

## Matrices and systems

With the cursor in a matrix or a system, you can insert a row above or below, a column to the left or right, and
delete the row or the column, as in Word. New cells come with a blank. The last row and column stay; to delete the
whole matrix, use **⌫**. A system has at most 2 columns, and matrices, 10.

## What goes into the field

The app chooses the format when it marks the field:

- **Readable text (Unicode):** x²+1, ½, √2. It works anywhere.
- **LaTeX:** `x^2+1`, `\frac{1}{2}`, `\sqrt{2}`. It is the format of Gabarito360 and Editor360.

## Read aloud

Every formula has a reading for the screen reader, in Brazilian Portuguese: x² + 1 is read "x ao quadrado mais 1"
("x squared plus 1").
