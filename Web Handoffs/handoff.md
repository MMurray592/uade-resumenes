# Handoff — Portal de Resúmenes UADE

**Última actualización:** 2026-06-21
**Web:** https://mmurray592.github.io/uade-resumenes/
**Carpeta:** `~/UADE-Web/Resúmenes Interactivos (HTML)/`

---

## Cómo funciona el portal (importante leer antes de tocar nada)

- `index.html` es **generado**, no se edita a mano. Lo arma `build_portal.py`.
- `build_portal.py` recorre las carpetas de materias (`Derivados/`, `Finanzas Corporativas/`,
  `Adm. de Portafolios/`), lee cada resumen `.html` y lo **incrusta** dentro del portal como
  `srcdoc` de un `<iframe>` (una pestaña por resumen, agrupadas por materia).
- Por eso: **si editás un resumen, tenés que regenerar el portal** con
  `python3 build_portal.py`, sino el cambio no aparece en `index.html`.

```
~/UADE-Web/Resúmenes Interactivos (HTML)/
├── index.html              <- GENERADO (no editar a mano)
├── build_portal.py         <- template + lógica del portal (header, scroll, botón ↑)
├── Derivados/              <- resúmenes fuente
├── Finanzas Corporativas/
├── Adm. de Portafolios/
└── handoff.md              <- este archivo
```

**Deploy:** la carpeta se publica vía git push → GitHub Pages (launchd + deploy.sh).
Después de cualquier cambio: regenerar el portal y hacer `git push`.

---

## Cambios hechos en esta sesión (2026-06-21)

### 1. Scroll del header del portal: de aparecer/desaparecer → estático + botón ↑
**Dónde:** `build_portal.py` (bloque `<script>`, funciones `setTopbar` / `watchScroll` / `goTop`).

- **Antes:** el header del portal (título + materias + pestañas) aparecía al subir y
  desaparecía al bajar, según la dirección del scroll. Resultaba molesto: con un desliz
  mínimo hacia arriba ya reaparecía.
- **Ahora:**
  - Se esconde cuando bajás (`scrollY > 140`) y **se queda quieto** — ya no reacciona a la
    dirección del scroll.
  - Vuelve a mostrarse solo cuando llegás arriba del todo (`scrollY <= 20`).
  - Se agregó un **botón flotante ↑** (`#toTop`, abajo a la derecha). Al tocarlo, scrollea
    el resumen activo arriba del todo y trae el header de vuelta. El botón solo se ve
    cuando el header está escondido.
- Se eliminó la lógica que movía los sub-headers `sticky` internos de cada resumen: ahora
  quedan fijos de forma natural, sin saltos.

### 2. Header del portal más chico
**Dónde:** `build_portal.py` (CSS: `header`, `.title`, `.subtitle`, `.subjects`, `.subj`, `.tab`).

- Título 1.35rem → 1.05rem · subtítulo .88rem → .74rem · padding superior 16px → 8px.
- Pastillas de materias y pestañas con menos padding y fuente.

### 3. Headers internos de cada resumen más chicos (los 6 archivos)
**Dónde:** archivos fuente de cada resumen (NO en build_portal.py).

| Archivos | Antes | Ahora |
|---|---|---|
| Derivados (2 apuntes) + Portafolios (2) | título 1.45rem, padding 28px, pestañas 8px/.88rem | título 1.1rem, padding 14px, pestañas 6px/.82rem |
| Derivados — Fórmulas | título 1.6rem, subtítulo .95rem | título 1.15rem, subtítulo .78rem |
| Finanzas Corporativas | h1 22px, sub 13.5px | h1 17px, sub 12px |

Después de editar los resúmenes se regeneró `index.html` con `build_portal.py`.

---

## Cómo previsualizar localmente

```
cd "~/UADE-Web/Resúmenes Interactivos (HTML)"
python3 -m http.server 8000
# abrir http://localhost:8000/index.html
```

---

## Pendientes / ideas a futuro
- Ajustar tamaño/posición del botón ↑ o ponerle texto ("Menú") si se quiere.
- Afinar el umbral de scroll (`140` / `20` en `watchScroll`) si se siente muy temprano/tarde.
