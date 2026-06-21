#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruye 'index.html' (el Portal de Resúmenes de UADE) a partir de los
archivos .html organizados en SUBCARPETAS POR MATERIA dentro de esta carpeta.

    Resúmenes Interactivos (HTML)/
    ├── build_portal.py
    ├── index.html              <- generado
    ├── Derivados/
    │   ├── Apunte 1er Parcial — U1-U4.html
    │   └── ...
    └── Finanzas Corporativas/
        └── Teoría — U2-U3-U4 (2do Parcial).html

Cada subcarpeta es una MATERIA (un "pill" en la fila superior). Cada .html
adentro es una PESTAÑA de esa materia. Los archivos que usan variables de
color indefinidas (tema "claro") reciben una hoja de estilos que los
normaliza al tema oscuro del portal.

Uso:  python3 build_portal.py
"""
import html, re, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent

# Archivos/carpetas que NO son contenido
EXCLUDE_FILES = {"index.html"}
EXCLUDE_DIR_PREFIXES = (".",)   # .git, etc.

# Un color por materia (en orden de aparición)
PALETTE = ["#4fa3e8", "#3dbf8a", "#e8a83d", "#d4537e", "#9b87f5", "#e86f51"]

# Hoja de estilos que normaliza archivos de "tema claro" (variables --color-* indefinidas)
FIX_CSS = """<style id="portal-restyle">
:root{--bg:#0f0f0f;--bg2:#1a1a1a;--bg3:#242424;--bg4:#2e2e2e;--text:#e8e8e8;--text2:#a0a0a0;--text3:#777;--border:#2e2e2e;--border2:#3a3a3a;
--color-background-primary:#1a1a1a;--color-background-secondary:#242424;--color-background-tertiary:#2e2e2e;
--color-border-secondary:#3a3a3a;--color-border-tertiary:#2e2e2e;
--color-text-primary:#e8e8e8;--color-text-secondary:#a0a0a0;--color-text-tertiary:#777;
--font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
--font-mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
--border-radius-md:7px;--border-radius-lg:10px;--unit-color:#378ADD;}
body{background:#161616!important;color:var(--text);line-height:1.6;font-size:15px;max-width:1000px;margin:0 auto;padding:24px 16px}
.nav{position:sticky;top:0;background:#161616;padding:10px 0;z-index:10;border-bottom:1px solid var(--border);margin-bottom:24px;gap:8px}
.nav-btn{background:var(--bg2);border:1px solid var(--border2);color:var(--text2);padding:9px 16px;border-radius:8px;font-size:.9rem;font-weight:600;transition:all .15s}
.nav-btn:hover{background:var(--bg3);color:var(--text)}
.nav-btn.active{background:var(--unit-color);border-color:var(--unit-color);color:#fff}
.unit-header{padding:16px 18px;border-radius:12px;margin-bottom:18px;border:1px solid var(--border2);border-left:4px solid var(--unit-color);background:linear-gradient(135deg,color-mix(in srgb,var(--unit-color) 15%,transparent),transparent)}
.unit-header h3{font-size:1.25rem;font-weight:700;color:var(--text)}
.unit-header p{color:var(--text2);font-size:.9rem;margin-top:4px}
.section{background:var(--bg2);border:1px solid var(--border);border-radius:10px;margin-bottom:10px;overflow:hidden}
.sec-head{padding:14px 16px;gap:12px;background:var(--bg2);transition:background .15s}
.sec-head:hover{background:var(--bg3)}
.sec-head h4{font-size:1rem;font-weight:600;color:var(--text)}
.sec-tag{font-size:.7rem;font-weight:600;padding:3px 9px;border-radius:20px;background:var(--bg4);color:var(--text2);border:none}
.arrow{color:var(--text3);font-size:.8rem}
.sec-body{padding:4px 18px 18px 18px;border-top:1px solid var(--border);background:var(--bg2)}
.sec-body p{color:var(--text);font-size:.95rem;margin-bottom:10px}
.sec-body strong{color:var(--text);font-weight:600}
.concept{background:var(--bg3);border:1px solid var(--border2);border-radius:8px;padding:12px 14px;margin:12px 0}
.concept-title{color:#fff;font-weight:700;font-size:.92rem;margin-bottom:4px}
.concept p{color:var(--text2);font-size:.92rem}
.vs-grid{background:var(--border2);border:1px solid var(--border2);border-radius:8px;margin:14px 0}
.vs-cell{background:var(--bg2);padding:10px 13px;font-size:.88rem;color:var(--text)}
.vs-header{background:var(--bg4);font-weight:700;color:#fff;text-align:center;font-size:.85rem}
.formula{background:#0b0b0b;border:1px solid var(--border2);border-radius:8px;padding:10px 14px;margin:12px 0;font-family:"SF Mono",Menlo,Consolas,monospace;color:#d6e9ff;font-size:.9rem}
.tag-list{gap:6px;margin-top:8px}
.tag{font-size:.7rem;font-weight:600;padding:3px 9px;border-radius:20px;background:var(--bg4);color:var(--text2);border:none}
ul{color:var(--text);padding-left:20px}
ul li{color:var(--text);margin-bottom:6px}
ul li strong{color:var(--text);font-weight:600}
</style>"""


def needs_fix(content: str) -> bool:
    """True si el archivo usa variables --color-* sin definirlas (tema claro)."""
    return ("var(--color-" in content) and ("--color-text-primary:" not in content)


def inject_fix(content: str) -> str:
    if 'id="portal-restyle"' in content:
        return content
    if "</body>" in content:
        return content.replace("</body>", FIX_CSS + "\n</body>", 1)
    return content + FIX_CSS


def meta_from_filename(stem: str):
    """Devuelve (label, sub, unit_start, type_rank) a partir del nombre del archivo."""
    parts = re.split(r"\s+[—-]\s+", stem, maxsplit=1)
    head = parts[0].strip()
    rest = parts[1].strip() if len(parts) > 1 else ""
    low = head.lower()
    if "fórmula" in low or "formula" in low:
        tipo, trank = "Fórmulas", 1
    elif "teó" in low or "teo" in low:
        tipo, trank = "Teoría", 0
    else:
        tipo, trank = head, 0
    # unidades y subtítulo
    msub = re.search(r"\(([^)]*)\)", rest)
    sub = msub.group(1).strip() if msub else ""
    units = re.sub(r"\([^)]*\)", "", rest).strip() if rest else ""
    units = units.replace("-", "–")
    # número de unidad inicial para ordenar
    mnum = re.search(r"[Uu]\s*(\d+)", units)
    unit_start = int(mnum.group(1)) if mnum else 99
    label = f"{tipo} · {units}".strip(" ·") if units else tipo
    return label, sub, unit_start, trank


def collect_subjects():
    """Devuelve [(materia, [archivos ordenados]), ...] ordenado por nombre de materia."""
    subjects = []
    for d in sorted(HERE.iterdir(), key=lambda p: p.name.lower()):
        if not d.is_dir():
            continue
        if any(d.name.startswith(pre) for pre in EXCLUDE_DIR_PREFIXES):
            continue
        files = [p for p in d.rglob("*.html") if p.name not in EXCLUDE_FILES]
        if not files:
            continue

        def key(p):
            _, _, us, tr = meta_from_filename(p.stem)
            return (us, tr, p.name)

        subjects.append((d.name, sorted(files, key=key)))
    return subjects


def build():
    subjects = collect_subjects()
    if not subjects:
        print("No hay subcarpetas de materia con archivos .html.", file=sys.stderr)
        return None

    pills, tabs, panels = [], [], []
    panel_i = 0
    for si, (materia, files) in enumerate(subjects):
        color = PALETTE[si % len(PALETTE)]
        active_subj = " active" if si == 0 else ""
        pills.append(
            f'<button class="subj{active_subj}" data-subj="{si}" style="--c:{color}">'
            f'<span class="sdot"></span>{html.escape(materia)} '
            f'<span class="scount">{len(files)}</span></button>'
        )
        for j, p in enumerate(files):
            content = p.read_text(encoding="utf-8")
            if needs_fix(content):
                content = inject_fix(content)
            esc = html.escape(content, quote=True)
            label, sub, _, _ = meta_from_filename(p.stem)
            # primera pestaña de la primera materia = activa
            active = " active" if (si == 0 and j == 0) else ""
            hide = "" if si == 0 else ";display:none"
            subhtml = f"<i>{html.escape(sub)}</i>" if sub else ""
            tabs.append(
                f'<button class="tab{active}" data-i="{panel_i}" data-subj="{si}" '
                f'style="--c:{color}{hide}">'
                f'<span class="tdot"></span><span><b>{html.escape(label)}</b>{subhtml}</span></button>'
            )
            panels.append(
                f'<iframe class="panel{active}" data-i="{panel_i}" srcdoc="{esc}" loading="lazy"></iframe>'
            )
            panel_i += 1

    out = PORTAL_TEMPLATE.format(
        pills="\n".join(pills), tabs="\n".join(tabs), panels="\n".join(panels)
    )
    dest = HERE / "index.html"
    dest.write_text(out, encoding="utf-8")
    total = sum(len(f) for _, f in subjects)
    print(f"OK · index.html generado · {len(subjects)} materias, {total} pestañas:")
    for materia, files in subjects:
        print(f"   {materia}:")
        for p in files:
            print("      -", p.name)
    return dest


PORTAL_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>UADE · Resúmenes Interactivos</title>
<style>
:root{{--bg:#0f0f0f;--bg2:#1a1a1a;--bg3:#242424;--text:#e8e8e8;--text2:#a0a0a0;--text3:#666;--border:#2e2e2e;--border2:#3a3a3a;}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;display:flex;flex-direction:column;height:100vh}}
#topbar{{flex-shrink:0;transition:margin-top .28s ease;will-change:margin-top}}
header{{padding:16px 20px 0}}
.title{{font-size:1.35rem;font-weight:700;display:flex;align-items:center;gap:10px}}
.title .badge{{font-size:.62rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--bg3);color:var(--text2);padding:4px 9px;border-radius:6px;border:1px solid var(--border2)}}
.subtitle{{color:var(--text2);font-size:.88rem;margin:5px 0 12px}}
.subjects{{display:flex;gap:8px;flex-wrap:wrap;padding:0 20px 12px}}
.subj{{display:flex;align-items:center;gap:8px;background:var(--bg2);border:1px solid var(--border2);color:var(--text2);padding:7px 14px;border-radius:20px;cursor:pointer;font-size:.85rem;font-weight:600;transition:all .15s}}
.subj:hover{{background:var(--bg3);color:var(--text)}}
.subj .sdot{{width:9px;height:9px;border-radius:50%;background:var(--c);flex-shrink:0}}
.subj .scount{{font-size:.7rem;background:var(--bg4,#2e2e2e);color:var(--text3);padding:1px 7px;border-radius:10px}}
.subj.active{{background:color-mix(in srgb,var(--c) 18%,var(--bg2));border-color:var(--c);color:#fff}}
.subj.active .scount{{background:color-mix(in srgb,var(--c) 30%,transparent);color:#fff}}
.tabs{{display:flex;gap:8px;flex-wrap:wrap;padding:0 20px;border-bottom:1px solid var(--border)}}
.tab{{display:flex;align-items:center;gap:9px;background:var(--bg2);border:1px solid var(--border2);border-bottom:none;color:var(--text2);padding:10px 16px;border-radius:9px 9px 0 0;cursor:pointer;font-size:.9rem;transition:all .15s;margin-bottom:-1px}}
.tab:hover{{background:var(--bg3);color:var(--text)}}
.tab b{{font-weight:600;display:block;font-size:.9rem;line-height:1.2}}
.tab i{{font-style:normal;font-size:.74rem;color:var(--text3)}}
.tab .tdot{{width:10px;height:10px;border-radius:50%;background:var(--c);flex-shrink:0}}
.tab.active{{background:var(--bg);color:var(--text);border-color:var(--border);border-bottom:1px solid var(--bg)}}
.tab.active i{{color:var(--text2)}}
.panels{{flex:1;position:relative;background:var(--bg)}}
.panel{{display:none;position:absolute;inset:0;width:100%;height:100%;border:none;background:var(--bg)}}
.panel.active{{display:block}}
@media(max-width:640px){{.tab i{{display:none}}.title{{font-size:1.1rem}}}}
</style>
</head>
<body>
<div id="topbar">
<header>
  <div class="title">📚 UADE — Resúmenes Interactivos</div>
  <div class="subtitle">Elegí una materia y después un resumen · Teoría y fórmulas de todas las unidades</div>
</header>
<nav class="subjects">
{pills}
</nav>
<nav class="tabs">
{tabs}
</nav>
</div>
<main class="panels">
{panels}
</main>
<script>
const subjPills=[...document.querySelectorAll('.subj')];
const tabs=[...document.querySelectorAll('.tab')];
const panels=[...document.querySelectorAll('.panel')];
const topbar=document.getElementById('topbar');
let topbarHidden=false;
let quietUntil=0;
function setTopbar(hide){{
  if(hide===topbarHidden)return;
  topbarHidden=hide;
  topbar.style.marginTop=hide?(-topbar.offsetHeight-2)+'px':'0px';
  quietUntil=Date.now()+450;
}}
function stickiesOf(doc){{
  if(!doc.__stickies){{
    try{{
      doc.__stickies=[...doc.querySelectorAll('body *')].filter(el=>{{
        const s=doc.defaultView.getComputedStyle(el);
        return s.position==='sticky'&&(parseFloat(s.top)||0)<80;
      }});
      doc.__stickies.forEach(el=>{{
        el.style.transition='transform .28s ease';
        el.style.willChange='transform';
      }});
    }}catch(e){{doc.__stickies=[];}}
  }}
  return doc.__stickies;
}}
function setStickies(doc,hide){{
  stickiesOf(doc).forEach(el=>{{el.style.transform=hide?'translateY(-120%)':'none';}});
}}
const hookedDocs=[];
function watchScroll(win){{
  const doc=win.document;
  hookedDocs.push(doc);
  let lastY=win.scrollY||0;
  win.addEventListener('scroll',()=>{{
    if(win.document!==doc)return;
    const y=win.scrollY;
    if(Date.now()<quietUntil){{lastY=y;return;}}
    const dy=y-lastY;
    lastY=y;
    if(y<=20){{setTopbar(false);setStickies(doc,false);return;}}
    if(dy>5){{setTopbar(true);setStickies(doc,true);}}
    else if(dy<-5){{setTopbar(false);setStickies(doc,false);}}
  }},{{passive:true}});
}}
function hookPanel(f){{
  try{{
    const d=f.contentDocument;
    if(!d||d.__scrollHooked)return;
    d.__scrollHooked=true;
    watchScroll(f.contentWindow);
  }}catch(e){{}}
}}
panels.forEach(f=>f.addEventListener('load',()=>hookPanel(f)));
panels.forEach(hookPanel);
setInterval(()=>panels.forEach(hookPanel),1000);
function selectTab(i){{
  tabs.forEach(x=>x.classList.toggle('active',x.dataset.i===i));
  panels.forEach(p=>p.classList.toggle('active',p.dataset.i===i));
  setTopbar(false);
  hookedDocs.forEach(d=>setStickies(d,false));
  try{{localStorage.setItem('uade-tab',i);}}catch(e){{}}
}}
function selectSubj(s){{
  subjPills.forEach(p=>p.classList.toggle('active',p.dataset.subj===s));
  tabs.forEach(t=>t.style.display=(t.dataset.subj===s)?'':'none');
  const first=tabs.find(t=>t.dataset.subj===s);
  if(first)selectTab(first.dataset.i);
}}
subjPills.forEach(p=>p.addEventListener('click',()=>selectSubj(p.dataset.subj)));
tabs.forEach(t=>t.addEventListener('click',()=>selectTab(t.dataset.i)));
</script>
</body>
</html>"""


if __name__ == "__main__":
    build()
