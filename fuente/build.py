#!/usr/bin/env python3
"""Monta la web “YukTech avanza en los ODS” a partir de src/index.html."""
import hashlib
import re
from pathlib import Path

RAIZ = Path(__file__).parent
SRC = RAIZ / "src"
SITIO = RAIZ / "site"

TITULO = "YukTech avanza en los ODS"
DESCRIPCION = ("Trabajo de Sostenibilidad (UD3): qué Objetivos de Desarrollo Sostenible impulsa YukTech, SL "
               "con lo que ya hace y qué acciones podría añadir hasta 2030.")
EQUIPO = "Marcos Ramos, Gonzalo Redondo, Jaime Ramos y Victor Cerveros"

REPARTO = [
    ("1", "Marcos Ramos", "Actuaciones 1 a 4", [("hoy", "1. Lo que ya hace")]),
    ("2", "Gonzalo Redondo", "Actuaciones 5 a 7 y balance", [("hoy", "1. Lo que ya hace"), ("balance", "2. Balance")]),
    ("3", "Jaime Ramos", "Acciones para los ODS que ya trabaja", [("reforzar", "3. Reforzar")]),
    ("4", "Victor Cerveros", "ODS nuevos, hoja de ruta y conclusión", [("ampliar", "4. Ampliar"), ("ruta", "5. Hoja de ruta")]),
]

UNSPLASH = "https://images.unsplash.com/"
FOTOS = {
    "equipo": ("photo-1622675363311-3e1904dc1885", "Mapbox",
               "https://unsplash.com/photos/four-people-all-on-laptops-two-men-and-two-women-listen-to-person-talking-in-a-board-meeting-ZT5v0puBjZI",
               "Cuatro personas con sus portátiles escuchan a quien habla en una reunión."),
    "formacion": ("photo-1723987135977-ae935608939e", "Anastassia Anufrieva",
                  "https://unsplash.com/photos/a-group-of-people-sitting-at-a-table-with-computers--JUlfa5fAIg",
                  "Un grupo de personas trabaja con ordenadores alrededor de una mesa."),
    "solar": ("photo-1707247111552-aaf74241058b", "Chirayu Trivedi",
              "https://unsplash.com/photos/a-large-amount-of-solar-panels-on-the-roof-of-a-building-twOIx6I35tk",
              "Muchas placas solares sobre la cubierta de un edificio."),
}

FUENTES = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900"
           "&amp;family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,700;1,400&amp;display=swap")

ODS = {
    1: ("Fin de la pobreza", "Fin de la pobreza", "#E5243B"),
    2: ("Hambre cero", "Hambre cero", "#DDA63A"),
    3: ("Salud y bienestar", "Salud y bienestar", "#4C9F38"),
    4: ("Educación de calidad", "Educación de calidad", "#C5192D"),
    5: ("Igualdad de género", "Igualdad de género", "#FF3A21"),
    6: ("Agua limpia y saneamiento", "Agua limpia", "#26BDE2"),
    7: ("Energía asequible y no contaminante", "Energía limpia", "#FCC30B"),
    8: ("Trabajo decente y crecimiento económico", "Trabajo decente", "#A21942"),
    9: ("Industria, innovación e infraestructura", "Industria e innovación", "#FD6925"),
    10: ("Reducción de las desigualdades", "Menos desigualdad", "#DD1367"),
    11: ("Ciudades y comunidades sostenibles", "Ciudades sostenibles", "#FD9D24"),
    12: ("Producción y consumo responsables", "Consumo responsable", "#BF8B2E"),
    13: ("Acción por el clima", "Acción por el clima", "#3F7E44"),
    14: ("Vida submarina", "Vida submarina", "#0A97D9"),
    15: ("Vida de ecosistemas terrestres", "Vida terrestre", "#56C02B"),
    16: ("Paz, justicia e instituciones sólidas", "Paz y justicia", "#00689D"),
    17: ("Alianzas para lograr los objetivos", "Alianzas", "#19486A"),
}
CLAROS = {2, 6, 7, 9, 11, 15}
ESTADO = {1: "hoy", 3: "hoy", 4: "hoy", 5: "hoy", 8: "hoy", 9: "hoy", 10: "hoy", 17: "hoy",
          7: "propuesta", 11: "propuesta", 12: "propuesta", 13: "propuesta", 16: "propuesta",
          2: "fuera", 6: "fuera", 14: "fuera", 15: "fuera"}
DESTINO = {"hoy": "#hoy", "propuesta": "#ampliar", "fuera": "#fuera"}
TEXTO_ESTADO = {"hoy": ("ya contribuye", "✓ Hoy"), "propuesta": ("propuesta nuestra", "+ Propuesta"),
                "fuera": ("fuera de su alcance", "Fuera")}
COSTE = {"bajo": (1, 2, "Bajo"), "medio": (2, 1, "Medio"), "alto": (3, 0, "Alto")}

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{fuentes}" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{fuentes}"></noscript>
<link rel="stylesheet" href="assets/estilos.css?v={v}">
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
<nav class="barra" aria-label="Apartados del trabajo">
  <div class="barra__dentro">
    <a class="barra__marca" href="#inicio"><span class="barra__logo" aria-hidden="true"></span>YukTech <em>· ODS</em></a>
    <button class="barra__boton" type="button" aria-expanded="false" aria-controls="barra-lista">Apartados</button>
    <ol class="barra__lista" id="barra-lista">
{nav}
    </ol>
  </div>
</nav>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie"><div class="pie__dentro"><p>Trabajo de clase de {equipo}. Sostenibilidad, UD3. Tablero y gráficos de elaboración propia con los colores oficiales de los ODS; fotos de Unsplash.</p><p><a href="#inicio">Volver arriba</a></p></div></footer>
<script src="assets/sitio.js?v={v}" defer></script>
</body>
</html>
"""


def foto(clave, pie):
    ident, autor, pagina, alt = FOTOS[clave]
    urls = [(f"{UNSPLASH}{ident}?auto=format&amp;fit=crop&amp;w={a}&amp;h={a * 9 // 16}&amp;q=70", a) for a in (720, 1440)]
    srcset = ", ".join(f"{u} {a}w" for u, a in urls)
    carga = 'loading="lazy"'
    return (f'<figure class="foto"><img data-foto src="{urls[-1][0]}" srcset="{srcset}" sizes="(max-width: 72rem) 92vw, 68rem" '
            f'width="1440" height="810" alt="{alt}" {carga} decoding="async">'
            f'<figcaption>{pie}. <span>Foto: <a href="{pagina}">{autor}</a>, Unsplash.</span></figcaption></figure>')


def encargo(nombre, corto=False):
    if corto:
        return f"<strong>{nombre}</strong>"
    return f"Se encarga <strong>{nombre}</strong>"


def reparto():
    filas = "".join(f'<tr><th scope="row">{nombre}</th><td>{parte}</td><td>{", ".join(f"<a href=\"#{i}\">{t}</a>" for i, t in secc)}</td></tr>'
                    for n, nombre, parte, secc in REPARTO)
    return ('<div class="tabla"><table><thead><tr><th scope="col">Integrante</th><th scope="col">Parte</th>'
            '<th scope="col">Secciones</th></tr></thead><tbody>' + filas + "</tbody></table></div>")


def creditos():
    filas = "".join(f'<li>{autor}. <a href="{pagina}">{alt.rstrip(".")}</a>. Unsplash, licencia libre.</li>' for _, autor, pagina, alt in FOTOS.values())
    return '<h3 class="h-sub">Fotografías</h3><ul class="refs refs--fotos">' + filas + "</ul>"




def tinta(n):
    return "#1d1d1b" if n in CLAROS else "#ffffff"


def luminancia(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def comprobar_contrastes():
    print("ODS  color    tinta    ratio")
    for n, (_, _, color) in ODS.items():
        r = contraste(color, tinta(n))
        aviso = "" if r >= 3 else "  AVISO <3:1"
        print(f"{n:>3}  {color}  {tinta(n)}  {r:5.2f}{aviso}")


def estilo(n):
    return f"--c:{ODS[n][2]};--t:{tinta(n)}"


def tablero():
    lis = []
    for n, (largo, corto, color) in ODS.items():
        e = ESTADO[n]
        txt, marca = TEXTO_ESTADO[e]
        lis.append(f'<li class="tile tile--{e}" style="{estilo(n)}"><a href="{DESTINO[e]}" aria-label="ODS {n}, {largo}: {txt}">'
                   f'<span class="tile__n">{n}</span><span class="tile__nombre">{corto}</span>'
                   f'<span class="tile__estado">{marca}</span></a></li>')
    hoy = sum(1 for v in ESTADO.values() if v == "hoy")
    prop = sum(1 for v in ESTADO.values() if v == "propuesta")
    lis.append(f'<li class="tablero__resumen"><p><strong>{hoy}</strong> ODS hoy</p>'
               f'<p><strong>+{prop}</strong> con nuestras propuestas</p></li>')
    return '<ol class="tablero">' + "".join(lis) + "</ol>"


def leyenda():
    return ('<span class="ley ley--hoy">Ya contribuye</span> <span class="ley ley--propuesta">Propuesta nuestra</span> '
            '<span class="ley ley--fuera">Fuera de su alcance</span>')


def ods_chip(n):
    n = int(n)
    return f'<span class="ods" style="{estilo(n)}" title="ODS {n}: {ODS[n][0]}"><b>{n}</b>{ODS[n][1]}</span>'


def ods_corto(n):
    n = int(n)
    return f'<span class="ods-n" style="{estilo(n)}" title="ODS {n}: {ODS[n][0]}"><span class="vh">ODS </span>{n}</span>'


X = {"d": ("d", "Directa"), "i": ("i", "Indirecta"), "-": ("n", "Sin relación")}


def marca_x(k):
    c, t = X[k]
    return f'<span class="x x--{c}" title="{t}"><span class="vh">{t}</span></span>'


def coste(k):
    a, o, t = COSTE[k]
    return (f'<span class="coste coste--{k}"><span class="coste__e" aria-hidden="true">{"€" * a}'
            f'<span class="coste__off">{"€" * o}</span></span>{t}</span>')


def color_propuestas(html):
    def una(m):
        art = m.group(0)
        c = re.search(r"--c:(#[0-9A-Fa-f]{6})", art)
        if not c:
            return art
        return art.replace("<article", f'<article style="--c1:{c.group(1)}"', 1)
    return re.sub(r'<article class="propuesta[^"]*">.*?</article>', una, html, flags=re.S)


def macros(cuerpo):
    cuerpo = re.sub(r"\{\{foto:([a-z]+)\|([^}]+)\}\}", lambda m: foto(m.group(1), m.group(2)), cuerpo)
    cuerpo = re.sub(r"\{\{encargo-corto:([^}]+)\}\}", lambda m: encargo(m.group(1), True), cuerpo)
    cuerpo = re.sub(r"\{\{encargo:([^}]+)\}\}", lambda m: encargo(m.group(1)), cuerpo)
    cuerpo = cuerpo.replace("{{reparto}}", reparto()).replace("{{creditos}}", creditos())
    cuerpo = cuerpo.replace("{{tablero}}", tablero()).replace("{{leyenda}}", leyenda())
    cuerpo = re.sub(r"\{\{ods-corto:(\d+)\}\}", lambda m: ods_corto(m.group(1)), cuerpo)
    cuerpo = re.sub(r"\{\{ods:(\d+)\}\}", lambda m: ods_chip(m.group(1)), cuerpo)
    cuerpo = re.sub(r"\{\{x:(d|i|-)\}\}", lambda m: marca_x(m.group(1)), cuerpo)
    cuerpo = re.sub(r"\{\{coste:(bajo|medio|alto)\}\}", lambda m: coste(m.group(1)), cuerpo)
    return color_propuestas(cuerpo)


def espacios_duros(cuerpo):
    cuerpo = re.sub(r"(\d) %", r"\1&nbsp;%", cuerpo)
    cuerpo = re.sub(r"(\d) °C", r"\1&nbsp;°C", cuerpo)
    cuerpo = re.sub(r"(\d) €", r"\1&nbsp;€", cuerpo)
    return cuerpo


def limpiar_texto(fragmento):
    fragmento = re.sub(r'<span class="supuesto">.*?</span>', "", fragmento, flags=re.S)
    return re.sub(r"<[^>]+>", "", fragmento).strip().replace('"', "&quot;")


def apilar_tabla(m):
    tabla = m.group(0)
    cab = re.search(r"<thead>(.*?)</thead>", tabla, flags=re.S)
    if not cab:
        return tabla
    etiquetas = [limpiar_texto(t) for t in re.findall(r"<th[^>]*>(.*?)</th>", cab.group(1), flags=re.S)]

    def fila(mf):
        pos = iter(range(len(etiquetas)))
        def celda(mc):
            i = next(pos, None)
            if i is None:
                return mc.group(0)
            return f'<{mc.group(1)} data-et="{etiquetas[i]}"{mc.group(2)}>'
        return re.sub(r"<(th|td)((?:\s[^>]*)?)>", celda, mf.group(0))

    cuerpo = re.search(r"<tbody>.*?</tbody>", tabla, flags=re.S)
    nuevo = re.sub(r"<tr>.*?</tr>", fila, cuerpo.group(0), flags=re.S)
    return tabla.replace(cuerpo.group(0), nuevo)


def apilable(html):
    return re.sub(r'<div class="tabla(?!--matriz)[^"]*">\s*<table>.*?</table>', apilar_tabla, html, flags=re.S)


def navegacion(cuerpo):
    filas = []
    for ident, nombre, n in re.findall(r'<section class="[^"]*" id="([^"]+)" data-etapa="([^"]+)" data-n="([^"]+)"', cuerpo):
        filas.append(f'      <li><a href="#{ident}"><span>{n}</span>{nombre}</a></li>')
    return "\n".join(filas)


def version():
    h = hashlib.sha1()
    for nombre in ("estilos.css", "sitio.js"):
        h.update((SITIO / "assets" / nombre).read_bytes())
    return h.hexdigest()[:8]


def version():
    h = hashlib.sha1()
    for nombre in ("estilos.css", "sitio.js"):
        h.update((SITIO / "assets" / nombre).read_bytes())
    return h.hexdigest()[:8]


def main():
    comprobar_contrastes()
    cuerpo = (SRC / "index.html").read_text(encoding="utf-8")
    cuerpo = macros(cuerpo)
    cuerpo = espacios_duros(cuerpo)
    cuerpo = apilable(cuerpo)
    html = PLANTILLA.format(titulo=TITULO, descripcion=DESCRIPCION, fuentes=FUENTES, v=version(),
                            nav=navegacion(cuerpo), cuerpo=cuerpo.rstrip(), equipo=EQUIPO)
    if "{{" in html:
        i = html.index("{{")
        raise SystemExit("Macro sin resolver: " + html[i:i + 80])
    (SITIO / "index.html").write_text(html, encoding="utf-8")
    (SITIO / ".nojekyll").write_text("", encoding="utf-8")
    print("ok index.html", len(html))


if __name__ == "__main__":
    main()
