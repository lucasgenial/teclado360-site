---
title: For app developers
description: How to mark a field in your app for formula mode and how the keyboard reads other fields.
---

Any Android app works with Teclado360 without changing anything. This page is for those who want to offer the math
keyboard in a field of their own app, or want the keyboard to get each field's type right.

## Mark a field for formulas

Formula mode only shows up in the fields you mark. On Android, use `privateImeOptions`:

```xml
<EditText
    android:id="@+id/answer"
    android:inputType="text"
    android:privateImeOptions="app.teclado360.formula" />
```

| Value | What the field receives |
|---|---|
| `app.teclado360.formula` | LaTeX: `x^2+1`, `\frac{1}{2}` |
| `app.teclado360.formula-unicode` | Readable text: `x²+1`, `½` |

People without Teclado360 see the field with their own keyboard, with no side effects.

When it opens a field that already has a formula, the keyboard starts from it: a LaTeX field with `\sqrt{2}` opens
with the root drawn and the cursor at the end.

## How the keyboard reads other fields

Teclado360 follows what the field already tells the system:

| In the field | The keyboard |
|---|---|
| A number, decimal or phone `inputType` | Opens the numeric keyboard (phone with +) |
| An e-mail or web address `inputType` | Brings @, the dot and the keys these fields use; no swiping |
| A password `inputType`, or the `IME_FLAG_NO_PERSONALIZED_LEARNING` option | Treats it as private: no suggestions, no swiping and no learning |
| `imeOptions` (`actionNext`, `actionDone`, `actionSearch`, `actionGo`, `actionSend`) | Shows the right action on ↵ |

## iPhone and iPad

The iOS app comes after version 1.0. On iOS, the system does not pass marks like `privateImeOptions` to an installed
keyboard; how to offer formula mode on those devices will be published here with the app.

## Using Teclado360 inside other products

The Teclado360 engine and the web version, which runs inside the page, are private: only Gabarito360 and the products
of its ecosystem may use them. For other uses, write to suporte@teclado360.app.
