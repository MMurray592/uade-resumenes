# Handoff — Portal de Resúmenes UADE

**Última actualización:** 2026-08-24
**Web:** https://mmurray592.github.io/uade-resumenes/
**Repo:** https://github.com/MMurray592/uade-resumenes
**Carpeta:** `~/UADE-Web/Resúmenes Interactivos (HTML)/`

---

## Cómo funciona el portal (importante leer antes de tocar nada)

- `index.html` es **generado**, no se edita a mano. Lo arma `build_portal.py`.
- `build_portal.py` recorre las carpetas de materias (`Adm. de Portafolios/`, `Derivados/`,
  `Derivados II/`, `Finanzas Corporativas/`), lee cada resumen `.html` y lo **incrusta** dentro
  del portal como `srcdoc` de un `<iframe>` (una pestaña por resumen, agrupadas por materia).
- Por eso: **si editás un resumen, tenés que regenerar el portal** con
  `python3 build_portal.py`, sino el cambio no aparece en `index.html`.

```
~/UADE-Web/Resúmenes Interactivos (HTML)/
├── index.html              <- GENERADO (no editar a mano)
├── build_portal.py         <- template + lógica del portal (header, scroll, botón ↑)
├── Adm. de Portafolios/    <- resúmenes fuente
├── Derivados/              <- Derivados I (U1–U8)
├── Derivados II/           <- Ingeniería Financiera II
├── Finanzas Corporativas/
└── Web Handoffs/
    └── handoff.md          <- este archivo
```

**Deploy:** la carpeta se publica vía `git push` → GitHub Pages.
Después de cualquier cambio: regenerar el portal y hacer `git push`.

### Convención de nombres de archivo

`build_portal.py` parsea el nombre con `meta_from_filename()` y de ahí saca la etiqueta de la
pestaña. El patrón es:

```
Tipo — Unidades (Subtítulo).html
```

| Parte | Qué hace | Ejemplo |
|---|---|---|
| `Tipo` | Texto antes del `—`. Si contiene "teo/teó" → **Teoría**; si contiene "formula/fórmula" → **Fórmulas**; si no, se usa tal cual | `Teoría`, `Apunte 1er Parcial` |
| `Unidades` | Va al label de la pestaña; los `-` se pasan a `–`. El primer `U<n>` define el orden | `U1-U2` → `U1–U2` |
| `(Subtítulo)` | Opcional, sale como línea chica debajo del label | `(Estrategias y Griegas)` |

El separador puede ser `—` o `-`, pero **con espacios alrededor**.

---

## Cambios hechos en esta sesión (2026-08-24)

### 1. Materia nueva: Derivados II

Se agregó la carpeta `Derivados II/` con el primer resumen de la materia:
`Teoría — U1-U2 (Estrategias y Griegas).html`.

Cubre las 4 clases dictadas hasta la fecha, 58 subtemas:

| Pestaña interna | Contenido | Subtemas |
|---|---|---|
| 00 · La materia | Objetivos, las 7 unidades, bibliografía, fechas de parciales | 4 |
| 01 · Mecánica de opciones | Derivados, actores, moneyness, OCC, márgenes Reg-T, open interest, operatoria BYMA | 29 |
| 02 · Estrategias (U1) | Covered call, collar, paridad put-call, verticales, box, mariposas, calendarios, straddles/strangles | 16 |
| 03 · Letras griegas (U2) | Delta hedging, gamma, theta, rho, vega, tabla de signos | 9 |

**Fuentes:** PPTs de cátedra de Instrumentos Financieros Derivados II (UADE, 2C 2026,
Lic. Santiago Ranucci, comisión jueves). Solo contenido teórico — sin ejercicios ni desarrollos
numéricos.

### 2. Efectos secundarios del alta a tener en cuenta

- **`build_portal.py` asigna colores por orden alfabético de carpeta** (`PALETTE`, índice de
  aparición). Al insertarse `Derivados II` en la tercera posición, Finanzas Corporativas pasó de
  la tercera a la cuarta y **cambió de color**. Es solo estético.
- El archivo nuevo **no necesita `FIX_CSS`**: trae su propio tema oscuro con variables `--bg*` /
  `--text*` definidas, así que `needs_fix()` devuelve `False` y no se le inyecta el restyle de
  tema claro.

### 3. Nota sobre notación en la fuente de Letras Griegas

La PPT de la cátedra usa `τ` para theta y `υ` para vega, y en la tabla de signos rotula vega
como `σ`. Hull usa `Θ` y `ν`. El resumen reproduce el contenido de la cátedra pero deja la
aclaración en el subtema 3.1, para no arrastrar la confusión al estudiar.

---

## Cambios hechos en la sesión anterior (2026-06-21)

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
cd ~/UADE-Web/"Resúmenes Interactivos (HTML)"
python3 -m http.server 8000
# abrir http://localhost:8000/index.html
```

---

## Pendientes / ideas a futuro
- Ajustar tamaño/posición del botón ↑ o ponerle texto ("Menú") si se quiere.
- Afinar el umbral de scroll (`140` / `20` en `watchScroll`) si se siente muy temprano/tarde.
- Derivados II: sumar Fórmulas y el integrador cuando avancen las unidades 3 a 7.
- Si el orden alfabético de materias deja de servir, agregar un orden explícito en
  `collect_subjects()` en vez de depender del nombre de carpeta.
