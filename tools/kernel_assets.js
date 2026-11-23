/**
 * File: tools/kernel_assets.js
 * Purpose: renders the site's formula pictures with the real Teclado360 kernel (t360.wasm), so every drawing on the
 * site is what the keyboard draws: the hero sequence (the quadratic formula being typed, one frame per key), a few
 * gallery structures and the formula keyboard's numeric screen. Writes assets/kernel.json.
 * Usage: node tools/kernel_assets.js PATH/TO/teclado360-kernel
 *
 * Copyright (c) 2026 Lucas Matos e Souza. All rights reserved.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const kernelDir = path.resolve(process.argv[2]);
const Kernel = require(path.join(kernelDir, 'web/t360-kernel.js'));
const Drawing = require(path.join(kernelDir, 'web/t360-drawing.js'));

(async () => {
  const k = await Kernel.load(fs.readFileSync(path.join(kernelDir, 'target/wasm32-unknown-unknown/release/t360.wasm')), { language: 'pt-BR', formula_size: 46 });
  const formulaOf = (r) => r.actions.find((a) => a.action === 'formula').formula;
  const svg = (d, color) => Drawing.svg(d, { color: color || 'currentColor', placeholderColor: 'currentColor', cursorColor: 'var(--marca)', margin: 6 });

  // hero: x = (−b ± √(b² − 4ac)) / 2a, key by key, as a person types it
  let r = k.request({ op: 'focus', field: { type: 'text', mark: 'formula' }, before: '', after: '' });
  const layout = k.request({ op: 'layout' }).layout;
  const keys = layout.layers.flatMap((l) => l.rows.flat());
  const key = (label) => { const t = keys.find((x) => x.label === label); if (!t) throw new Error('no key ' + label); return t.id; };
  const tap = (label) => formulaOf(k.request({ op: 'tap', id: key(label), before: '', after: '' }));
  const frames = [];
  const push = (f, label) => frames.push({ key: label, svg: svg(f.drawing), latex: f.output });
  const steps = ['x', '=', '□/□', '−', 'b', '±', '√□', 'b', '□²', '−', '4', 'a', 'c', '⇥', '2', 'a'];
  for (const s of steps) {
    // letters and ± are on other screens: switch the way a person would
    const screen = (s === 'b' || s === 'c' || s === 'a') ? 'abc' : (s === '±') ? 'f(x)' : '123';
    k.request({ op: 'tap', id: key(screen), before: '', after: '' });
    push(tap(s), s);
  }

  // gallery: a few structures, drawn by the kernel
  const gallery = k.request({ op: 'gallery', size: 34 }).gallery;
  const wanted = ['Fração empilhada', 'Raiz com índice', 'Integral de superfície', 'Somatório com limites', 'Matriz entre colchetes', 'Sistema ou função por partes', 'Limite', 'Vetor AB'];
  const picked = [];
  for (const g of gallery.groups || gallery) {
    for (const it of (g.items || [])) {
      if (wanted.includes(it.name)) picked.push({ name: it.name, svg: svg(it.drawing) });
    }
  }

  // the formula keyboard's numeric screen, as the kernel lays it out
  const numeric = layout.layers.find((l) => l.id === 'numeric');
  const rows = numeric.rows.map((row) => row.map((t) => ({ label: t.label, width: t.width, fn: !!t.is_function, hold: (t.hold || []).length > 0 })));
  fs.writeFileSync(path.join(__dirname, '..', 'assets', 'kernel.json'), JSON.stringify({ frames, gallery: picked, keyboard: rows }, null, 1));
  console.log('ok', frames.length, 'frames,', picked.length, 'gallery items,', rows.length, 'keyboard rows; final:', frames[frames.length - 1].latex);
  k.destroy();
})().catch((e) => { console.error(e); process.exit(1); });
