---
title: Para quem desenvolve aplicativos
description: Como marcar um campo do seu aplicativo para o modo fórmula e como o teclado lê os outros campos.
---

Qualquer aplicativo Android funciona com o Teclado360 sem mudar nada. Esta página é para quem quer oferecer o teclado
de Matemática num campo do próprio aplicativo, ou quer que o teclado acerte o tipo de cada campo.

## Marcar um campo para fórmulas

O modo fórmula só aparece nos campos que você marcar. No Android, use `privateImeOptions`:

```xml
<EditText
    android:id="@+id/resposta"
    android:inputType="text"
    android:privateImeOptions="app.teclado360.formula" />
```

| Valor | O que o campo recebe |
|---|---|
| `app.teclado360.formula` | LaTeX: `x^2+1`, `\frac{1}{2}` |
| `app.teclado360.formula-unicode` | Texto legível: `x²+1`, `½` |

Quem não tem o Teclado360 instalado vê o campo com o próprio teclado, sem nenhum efeito colateral.

Ao abrir um campo que já tem uma fórmula, o teclado parte dela: um campo LaTeX com `\sqrt{2}` abre com a raiz
desenhada e o cursor no fim.

## Como o teclado lê os outros campos

O Teclado360 segue o que o campo já diz ao sistema:

| No campo | O teclado |
|---|---|
| `inputType` de número, decimal ou telefone | Abre o teclado numérico (telefone com +) |
| `inputType` de e-mail ou endereço da web | Traz @, ponto e as teclas desses campos; sem deslize |
| `inputType` de senha, ou a opção `IME_FLAG_NO_PERSONALIZED_LEARNING` | Trata como campo privado: sem sugestões, sem deslize e sem aprender palavras |
| `imeOptions` (`actionNext`, `actionDone`, `actionSearch`, `actionGo`, `actionSend`) | Mostra no ↵ a ação certa |

## iPhone e iPad

O aplicativo para iOS chega depois da versão 1.0. No iOS, o sistema não repassa marcas como `privateImeOptions` ao
teclado instalado; a forma de oferecer o modo fórmula nesses aparelhos será publicada aqui com o aplicativo.

## Uso do Teclado360 dentro de outros produtos

O motor do Teclado360 e a versão web, que roda dentro da página, são privados: só o Gabarito360 e os produtos do
ecossistema dele podem usá-los. Para outros usos, escreva para suporte@teclado360.app.
