"""
File: tools/build.py
Purpose: builds the Teclado360 website for GitHub Pages into site/: the landing page and the documentation, in
Brazilian Portuguese (root) and English (en/). Documentation pages come from content/<language>/*.md (pandoc, a build
tool, turns them into HTML); the formula pictures come from assets/kernel.json, drawn by the real kernel
(tools/kernel_assets.js). The pages load nothing from other sites.

Usage: python3 -I tools/build.py

Copyright (c) 2026 Lucas Matos e Souza. All rights reserved.
"""
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
KERNEL = json.loads((ROOT / "assets" / "kernel.json").read_text(encoding="utf-8"))
YEAR = "2026"
DOMAIN = "teclado360.app"

DOCS = ["instalar", "digitar", "formulas", "desenvolvedores"]
LEGAL = ["licenca", "privacidade", "terceiros"]

T = {
    "pt": {
        "lang": "pt-BR", "other": "en", "other_label": "English", "other_short": "EN",
        "home": "Apresentação", "docs": "Documentação", "privacy": "Privacidade",
        "skip": "Pular para o conteúdo", "theme_dark": "Tema escuro", "theme_light": "Tema claro",
        "docs_group": "Usar o Teclado360", "legal_group": "Licenças e privacidade", "menu": "Páginas da documentação",
        "footer_rights": f"© {YEAR} Lucas Matos e Souza. Todos os direitos reservados.",
        "footer_links": [("documentacao.html", "Documentação"), ("licenca.html", "Licença de uso"),
                         ("privacidade.html", "Privacidade"), ("terceiros.html", "Componentes de terceiros")],
        "docs_title": "Documentação", "docs_desc": "Como instalar, digitar, montar fórmulas e integrar o Teclado360.",
        "site_desc": "Teclado para Android com acentos à mão, digitar deslizando e um modo fórmula que desenha a "
                     "equação enquanto você digita. Funciona sem internet e sem anúncios.",
    },
    "en": {
        "lang": "en", "other": "pt", "other_label": "Português", "other_short": "PT",
        "home": "Overview", "docs": "Documentation", "privacy": "Privacy",
        "skip": "Skip to content", "theme_dark": "Dark theme", "theme_light": "Light theme",
        "docs_group": "Using Teclado360", "legal_group": "Licenses and privacy", "menu": "Documentation pages",
        "footer_rights": f"© {YEAR} Lucas Matos e Souza. All rights reserved.",
        "footer_links": [("documentacao.html", "Documentation"), ("licenca.html", "License agreement"),
                         ("privacidade.html", "Privacy"), ("terceiros.html", "Third-party components")],
        "docs_title": "Documentation", "docs_desc": "How to install Teclado360, type, build formulas and integrate it.",
        "site_desc": "An Android keyboard with accents at hand, swipe typing and a formula mode that draws the "
                     "equation as you type. Works without internet and without ads.",
    },
}

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="1" y="3" width="30" height="26" rx="7" fill="var(--marca)"/>'
        '<g fill="var(--marca-texto)"><rect x="6" y="9" width="4" height="4" rx="1"/><rect x="14" y="9" width="4" height="4" rx="1"/>'
        '<rect x="22" y="9" width="4" height="4" rx="1"/><rect x="9" y="19" width="14" height="4" rx="1.5"/></g></svg>')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='1' y='3' width='30' "
           "height='26' rx='7' fill='%235B21B6'/%3E%3Cg fill='%23fff'%3E%3Crect x='6' y='9' width='4' height='4' rx='1'/%3E%3Crect "
           "x='14' y='9' width='4' height='4' rx='1'/%3E%3Crect x='22' y='9' width='4' height='4' rx='1'/%3E%3Crect x='9' y='19' "
           "width='14' height='4' rx='1.5'/%3E%3C/g%3E%3C/svg%3E")

# Theme: read before drawing, so the page does not flash; the choice stays only in this browser.
THEME_HEAD = ("<script>try{if(localStorage.getItem('t360-site-tema')==='escuro'){document.documentElement.setAttribute('data-tema','escuro')}}"
              "catch(e){}</script>")
THEME_BUTTON_JS = """<script>
(function () {
  var b = document.getElementById('tema');
  if (!b) { return; }
  function label() { var d = document.documentElement.getAttribute('data-tema') === 'escuro'; b.textContent = d ? b.dataset.claro : b.dataset.escuro; b.setAttribute('aria-pressed', d ? 'true' : 'false'); }
  label();
  b.addEventListener('click', function () {
    var d = document.documentElement.getAttribute('data-tema') === 'escuro';
    if (d) { document.documentElement.removeAttribute('data-tema'); } else { document.documentElement.setAttribute('data-tema', 'escuro'); }
    try { localStorage.setItem('t360-site-tema', d ? 'claro' : 'escuro'); } catch (e) {}
    label();
  });
})();
</script>"""


def page(lang, slug, title, description, body, current):
    t = T[lang]
    base = "" if lang == "pt" else "../"
    assets = f"{base}assets/"
    other_href = (f"en/{slug}.html" if lang == "pt" else f"../{slug}.html")
    nav = [("index", t["home"]), ("documentacao", t["docs"]), ("privacidade", t["privacy"])]
    nav_html = "".join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s == current else ""}>{label}</a>' for s, label in nav)
    footer = "".join(f'<a href="{h}">{label}</a>' for h, label in t["footer_links"])
    full_title = "Teclado360" if slug == "index" else f"{title} | Teclado360"
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#F7F6FA">
<link rel="icon" href="{FAVICON}">
<link rel="alternate" hreflang="{T[t['other']]['lang']}" href="{other_href}">
{THEME_HEAD}
<link rel="stylesheet" href="{assets}site.css">
</head>
<body>
<a class="pular" href="#conteudo">{t['skip']}</a>
<header class="topo"><div class="topo-dentro">
<a class="marca" href="index.html">{LOGO}Teclado360</a>
<nav aria-label="{t['docs']}">{nav_html}</nav>
<div class="acoes">
<a class="botao-topo" href="{other_href}" hreflang="{T[t['other']]['lang']}" lang="{T[t['other']]['lang']}" aria-label="{t['other_label']}">{t['other_short']}</a>
<button class="botao-topo" id="tema" type="button" data-escuro="{t['theme_dark']}" data-claro="{t['theme_light']}">{t['theme_dark']}</button>
</div>
</div></header>
<main id="conteudo">
{body}
</main>
<footer class="rodape"><div class="dentro">{footer}<span class="direitos">{t['footer_rights']}</span></div></footer>
{THEME_BUTTON_JS}
</body>
</html>
"""


def markdown(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    meta = dict(re.findall(r"^(\w+): (.*)$", m.group(1), re.M))
    body = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none"], input=m.group(2), capture_output=True,
                          text=True, check=True).stdout
    # fields the owner still has to fill in stand out
    body = re.sub(r"\[([A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9][A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 ,\-]+)\]", r'<mark class="preencher">[\1]</mark>', body)
    return meta, body


def doc_nav(lang, current):
    t = T[lang]
    titles = {s: markdown(ROOT / "content" / lang / f"{s}.md")[0]["title"] for s in DOCS + LEGAL}
    item = lambda s: f'<li><a href="{s}.html"{" aria-current=\"page\"" if s == current else ""}>{html.escape(titles[s])}</a></li>'
    return (f'<nav class="doc-nav" aria-label="{t["docs"]}"><details class="doc-menu" open><summary>{t["menu"]}</summary>'
            f'<h2>{t["docs_group"]}</h2><ul>'
            f'<li><a href="documentacao.html"{" aria-current=\"page\"" if current == "documentacao" else ""}>{t["docs_title"]}</a></li>'
            f'{"".join(item(s) for s in DOCS)}</ul><h2>{t["legal_group"]}</h2><ul>{"".join(item(s) for s in LEGAL)}</ul></details></nav>'
            "<script>try{if(matchMedia('(max-width: 900px)').matches){document.querySelector('.doc-menu').removeAttribute('open')}}catch(e){}</script>")


def build_docs(lang, out):
    for slug in DOCS + LEGAL:
        meta, body = markdown(ROOT / "content" / lang / f"{slug}.md")
        content = (f'<div class="doc">{doc_nav(lang, slug)}<article class="doc-corpo"><h1>{html.escape(meta["title"])}</h1>'
                   f'<p class="descricao">{html.escape(meta["description"])}</p>{body}</article></div>')
        current = "privacidade" if slug == "privacidade" else "documentacao"
        (out / f"{slug}.html").write_text(page(lang, slug, meta["title"], meta["description"], content, current), encoding="utf-8")
    t = T[lang]
    cards = []
    for slug in DOCS + LEGAL:
        meta, _ = markdown(ROOT / "content" / lang / f"{slug}.md")
        cards.append(f'<li><a href="{slug}.html"><b>{html.escape(meta["title"])}</b><span>{html.escape(meta["description"])}</span></a></li>')
    content = (f'<div class="doc">{doc_nav(lang, "documentacao")}<article class="doc-corpo"><h1>{t["docs_title"]}</h1>'
               f'<p class="descricao">{t["docs_desc"]}</p><ul class="indice">{"".join(cards)}</ul></article></div>')
    (out / "documentacao.html").write_text(page(lang, "documentacao", t["docs_title"], t["docs_desc"], content, "documentacao"),
                                           encoding="utf-8")


def keyboard_html(rows):
    out = []
    for i, row in enumerate(rows):
        keys = "".join(
            f'<span class="k{" fn" if k["fn"] else ""}{" segura" if k["hold"] else ""}" data-k="{html.escape(k["label"])}" '
            f'style="flex-grow:{k["width"]}">{html.escape(k["label"])}</span>' for k in row)
        out.append(f'<div class="linha{" abas" if i == 0 else ""}">{keys}</div>')
    return "".join(out)


GALLERY_EN = {
    "Fração empilhada": "Stacked fraction", "Raiz com índice": "Root with index", "Integral de superfície": "Surface integral",
    "Somatório com limites": "Sum with limits", "Sistema ou função por partes": "System or piecewise function",
    "Vetor AB": "Vector AB", "Limite": "Limit", "Matriz entre colchetes": "Matrix in brackets",
}

LANDING = {
    "pt": {
        "h1": "O teclado que escreve Matemática.",
        "lead": "Acentos à mão, digitar deslizando e um modo fórmula que desenha a equação enquanto você digita. "
                "Para celular e tablet Android, sem internet e sem anúncios.",
        "cta1": ("formulas.html", "Ver o modo fórmula"), "cta2": ("instalar.html", "Instalar e ativar"),
        "status": "<b>Versão 1.0 em preparação</b> para Android.",
        "device_label": "Resposta", "device_alt": "A fórmula de Bhaskara sendo montada no modo fórmula, uma tecla por vez, "
                                                  "com o desenho feito pelo próprio Teclado360.",
        "s2_title": "Para texto, o teclado de sempre, mais esperto.",
        "s2_lead": "Letras na ordem de sempre e os símbolos de Matemática e ciências perto da mão. Nada troca sozinho: "
                   "o texto só muda quando você toca.",
        "photos": [
            ("celular-balao.webp", "Segurando o a: o balão mostra os acentos.", "Acentos no balão",
             "Segure a letra e escolha: á à â ã, é ê, ó ô õ, ç."),
            ("celular-deslize-rastro.webp", "Deslizando “tem” depois de “A prova”.", "Digitar deslizando",
             "Passe o dedo pelas letras sem soltar. Um rastro mostra o caminho."),
            ("celular-sugestoes.webp", "Digitando “matem”: matemática no meio.", "Linha de sugestões",
             "Três lugares fixos: acento certo, palavra completa, tecla vizinha."),
        ],
        "photos_note": "Telas da versão web do Teclado360. O aplicativo Android segue o mesmo desenho.",
        "s3_title": "Fórmulas desenhadas como no livro.",
        "s3_lead": "Nos campos marcados para fórmulas, o Teclado360 vira um teclado de Matemática. Cada estrutura da "
                   "galeria abaixo foi desenhada pelo próprio teclado.",
        "points": [
            ("Galeria de estruturas", "Frações, raízes, integrais, somatórios, matrizes e sistemas, organizados como na faixa de equações do Word."),
            ("Toque na fórmula", "Toque em qualquer ponto do desenho para pôr o cursor ali: no numerador, numa célula, depois de um parêntese."),
            ("LaTeX ou texto legível", "O campo recebe LaTeX, para o Gabarito360 e o Editor360, ou texto como x²+1, que vai para qualquer lugar."),
        ],
        "s4_title": "O que você digita fica no seu aparelho.",
        "promises": [
            ("Sem internet", "O aplicativo não pede acesso à internet. Nada do que você digita é enviado."),
            ("Sem anúncios e sem rastreamento", "Nenhuma biblioteca de terceiros, nenhuma análise de uso."),
            ("Aprende só no aparelho", "As palavras que o teclado aprende ficam com você, e você apaga quando quiser."),
            ("Senha é senha", "Em campos de senha e privados, sem sugestões, sem deslize e sem aprender nada."),
        ],
        "privacy_link": ("privacidade.html", "Ler a política de privacidade"),
        "s5_title": "Onde funciona",
        "where": [
            ("Android, celular e tablet", "Em qualquer aplicativo, como teclado do sistema.", "Versão 1.0, em breve", False),
            ("Gabarito360 e Editor360", "Na própria página, sem instalar nada.", "Em teste", True),
            ("iPhone e iPad", "Como teclado do sistema.", "Depois da 1.0", False),
        ],
        "faq_title": "Perguntas",
        "faq": [
            ("Precisa de internet?", "Não. O Teclado360 funciona inteiro no aparelho, inclusive as sugestões e o desenho das fórmulas."),
            ("Quanto custa?", "O aplicativo é pago uma vez, na loja. O preço aparece na página do aplicativo no lançamento, e as atualizações não custam nada a mais."),
            ("E se eu me arrepender da compra?", "Você pode desistir em até 7 dias e receber o valor de volta, pela loja ou pelo nosso atendimento. Veja a <a href=\"licenca.html\">licença de uso</a>."),
            ("Funciona em qualquer aplicativo?", "Sim, como qualquer teclado. O modo fórmula aparece só nos campos que o aplicativo marcar para fórmulas; nos outros, você tem o teclado de texto com os símbolos à mão."),
            ("Meu aplicativo pode oferecer o modo fórmula?", "Pode. Basta marcar o campo, como explica a página <a href=\"desenvolvedores.html\">para quem desenvolve aplicativos</a>."),
        ],
        "final_title": "Comece pela documentação.",
        "final_cta": ("documentacao.html", "Abrir a documentação"),
    },
    "en": {
        "h1": "The keyboard that writes math.",
        "lead": "Accents at hand, swipe typing and a formula mode that draws the equation as you type. "
                "For Android phones and tablets, without internet and without ads.",
        "cta1": ("formulas.html", "See formula mode"), "cta2": ("instalar.html", "Install and turn on"),
        "status": "<b>Version 1.0 in preparation</b> for Android.",
        "device_label": "Answer", "device_alt": "The quadratic formula being built in formula mode, one key at a time, "
                                                "drawn by Teclado360 itself.",
        "s2_title": "For text, the keyboard you know, smarter.",
        "s2_lead": "Letters in the usual order, with math and science symbols close at hand. Nothing changes on its own: "
                   "the text only changes when you tap.",
        "photos": [
            ("celular-balao.webp", "Holding a: the bubble shows the accents.", "Accents in a bubble",
             "Hold the letter and pick: á à â ã, é ê, ó ô õ, ç."),
            ("celular-deslize-rastro.webp", "Swiping “tem” after “A prova”.", "Swipe to type",
             "Slide your finger across the letters without lifting it. A trail shows the path."),
            ("celular-sugestoes.webp", "Typing “matem”: matemática in the middle.", "Suggestion row",
             "Three fixed slots: the right accent, the whole word, the neighboring key."),
        ],
        "photos_note": "Screens of the Teclado360 web version, in Portuguese. The Android app follows the same design.",
        "s3_title": "Formulas drawn as in a textbook.",
        "s3_lead": "In fields marked for formulas, Teclado360 becomes a math keyboard. Every structure in the gallery "
                   "below was drawn by the keyboard itself.",
        "points": [
            ("Gallery of structures", "Fractions, roots, integrals, sums, matrices and systems, organized like Word's equation ribbon."),
            ("Tap on the formula", "Tap anywhere on the drawing to put the cursor there: in the numerator, in a cell, after a parenthesis."),
            ("LaTeX or readable text", "The field receives LaTeX, for Gabarito360 and Editor360, or text like x²+1 that works anywhere."),
        ],
        "s4_title": "What you type stays on your device.",
        "promises": [
            ("No internet", "The app does not ask for internet access. Nothing you type is sent anywhere."),
            ("No ads, no tracking", "No third-party libraries, no usage analytics."),
            ("Learns only on the device", "The words the keyboard learns stay with you, and you erase them whenever you want."),
            ("A password is a password", "In password and private fields: no suggestions, no swiping, no learning."),
        ],
        "privacy_link": ("privacidade.html", "Read the privacy policy"),
        "s5_title": "Where it works",
        "where": [
            ("Android phones and tablets", "In any app, as the system keyboard.", "Version 1.0, coming soon", False),
            ("Gabarito360 and Editor360", "Right in the page, with nothing to install.", "In testing", True),
            ("iPhone and iPad", "As the system keyboard.", "After 1.0", False),
        ],
        "faq_title": "Questions",
        "faq": [
            ("Does it need internet?", "No. Teclado360 runs entirely on the device, including suggestions and formula drawing."),
            ("How much does it cost?", "The app is a one-time purchase in the store. The price appears on the app's page at launch, and updates cost nothing extra."),
            ("What if I change my mind?", "You can withdraw within 7 days and get your money back, through the store or our support. See the <a href=\"licenca.html\">license agreement</a>."),
            ("Does it work in any app?", "Yes, like any keyboard. Formula mode shows up only in fields the app marks for formulas; elsewhere you get the text keyboard with symbols at hand."),
            ("Can my app offer formula mode?", "Yes. Just mark the field, as the page <a href=\"desenvolvedores.html\">for app developers</a> explains."),
        ],
        "final_title": "Start with the documentation.",
        "final_cta": ("documentacao.html", "Open the documentation"),
    },
}

# Which tab to light up for a key that is not on the numeric screen (as a person would switch screens).
TAB_OF = {"a": "abc", "b": "abc", "c": "abc", "±": "f(x)"}


def build_landing(lang, out):
    c = LANDING[lang]
    base = "" if lang == "pt" else "../"
    final = KERNEL["frames"][-1]["svg"]
    frames = [{"k": f["key"], "t": TAB_OF.get(f["key"]), "svg": f["svg"]} for f in KERNEL["frames"]]
    gallery = "".join(
        f'<figure>{g["svg"]}<figcaption>{html.escape(g["name"] if lang == "pt" else GALLERY_EN[g["name"]])}</figcaption></figure>'
        for g in KERNEL["gallery"])
    photos = "".join(
        f'<figure><img src="{base}assets/img/{img}" alt="{html.escape(alt)}" width="824" height="680" loading="lazy">'
        f'<h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></figure>' for img, alt, h, p in c["photos"])
    points = "".join(f'<div><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for h, p in c["points"])
    promises = "".join(f'<li><b>{html.escape(h)}</b><span>{html.escape(p)}</span></li>' for h, p in c["promises"])
    where = "".join(
        f'<tr><th scope="row">{html.escape(a)}</th><td>{html.escape(b)}</td><td><span class="selo{" ok" if ok else ""}">{html.escape(s)}</span></td></tr>'
        for a, b, s, ok in c["where"])
    faq = "".join(f'<details><summary>{html.escape(q)}</summary><p>{a}</p></details>' for q, a in c["faq"])
    body = f"""
<section class="faixa" aria-labelledby="titulo"><div class="dentro abertura">
  <div>
    <h1 id="titulo">{html.escape(c['h1'])}</h1>
    <p class="lead">{html.escape(c['lead'])}</p>
    <div class="botoes"><a class="tecla-botao principal" href="{c['cta1'][0]}">{c['cta1'][1]}</a><a class="tecla-botao" href="{c['cta2'][0]}">{c['cta2'][1]}</a></div>
    <p class="situacao">{c['status']}</p>
  </div>
  <div class="aparelho">
    <p class="campo-rotulo"><span>{c['device_label']}</span><code id="latex" aria-hidden="true"></code></p>
    <div class="campo-formula" id="formula" role="img" aria-label="{html.escape(c['device_alt'])}">{final}</div>
    <div class="teclado" aria-hidden="true">{keyboard_html(KERNEL['keyboard'])}</div>
  </div>
</div></section>

<section class="faixa bandeja" aria-labelledby="s2"><div class="dentro">
  <h2 class="secao-titulo" id="s2">{html.escape(c['s2_title'])}</h2>
  <p class="secao-lead">{html.escape(c['s2_lead'])}</p>
  <div class="fotos">{photos}</div>
  <p class="nota-fotos">{html.escape(c['photos_note'])}</p>
</div></section>

<section class="faixa" aria-labelledby="s3"><div class="dentro">
  <h2 class="secao-titulo" id="s3">{html.escape(c['s3_title'])}</h2>
  <p class="secao-lead">{html.escape(c['s3_lead'])}</p>
  <div class="galeria">{gallery}</div>
  <div class="pontos">{points}</div>
</div></section>

<section class="faixa bandeja" aria-labelledby="s4"><div class="dentro">
  <h2 class="secao-titulo" id="s4">{html.escape(c['s4_title'])}</h2>
  <ul class="promessas">{promises}</ul>
  <p><a href="{c['privacy_link'][0]}">{c['privacy_link'][1]}</a></p>
</div></section>

<section class="faixa" aria-labelledby="s5"><div class="dentro">
  <h2 class="secao-titulo" id="s5">{html.escape(c['s5_title'])}</h2>
  <table class="onde">{where}</table>
</div></section>

<section class="faixa bandeja" aria-labelledby="s6"><div class="dentro">
  <h2 class="secao-titulo" id="s6">{html.escape(c['faq_title'])}</h2>
  <div class="perguntas">{faq}</div>
  <p style="margin-top:36px"><a class="tecla-botao principal" href="{c['final_cta'][0]}">{c['final_cta'][1]}</a></p>
</div></section>

<script type="application/json" id="quadros">{json.dumps(frames, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>
(function () {{
  // One moment of motion: the formula being typed, key by key. With reduced motion, only the finished formula.
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{ return; }}
  var quadros = JSON.parse(document.getElementById('quadros').textContent);
  var campo = document.getElementById('formula');
  var teclas = Array.prototype.slice.call(document.querySelectorAll('.teclado .k'));
  var i = 0, timer = null;
  function acha(rotulo) {{ for (var j = 0; j < teclas.length; j++) {{ if (teclas[j].getAttribute('data-k') === rotulo) {{ return teclas[j]; }} }} return null; }}
  function passo() {{
    teclas.forEach(function (t) {{ t.classList.remove('tocada'); }});
    var q = quadros[i];
    campo.innerHTML = q.svg;
    var t = acha(q.t || q.k);
    if (t) {{ t.classList.add('tocada'); }}
    i = (i + 1) % quadros.length;
    timer = setTimeout(passo, i === 0 ? 3200 : 520);
  }}
  var visivel = true;
  if ('IntersectionObserver' in window) {{
    new IntersectionObserver(function (e) {{
      visivel = e[0].isIntersecting;
      if (visivel && !timer) {{ passo(); }} else if (!visivel && timer) {{ clearTimeout(timer); timer = null; }}
    }}).observe(campo);
  }} else {{ passo(); }}
}})();
</script>"""
    (out / "index.html").write_text(page(lang, "index", "Teclado360", T[lang]["site_desc"], body, "index"), encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "en").mkdir(parents=True)
    shutil.copytree(ROOT / "assets", OUT / "assets", ignore=shutil.ignore_patterns("kernel.json"))
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    # own domain (K-21): GitHub Pages serves the site at this address once the DNS points to it
    (OUT / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
    for lang, out in (("pt", OUT), ("en", OUT / "en")):
        build_docs(lang, out)
        build_landing(lang, out)
    print("ok", sum(1 for _ in OUT.rglob("*.html")), "pages in", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
