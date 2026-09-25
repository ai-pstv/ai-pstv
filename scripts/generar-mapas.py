#!/usr/bin/env python3
"""
Genera los mapas SVG de distritos que usa el hero (public/images/hero/mapa-<ciudad>.svg)
a partir de los datos abiertos oficiales de cada ayuntamiento.

Cada distrito sale como una pieza independiente (<path id="..." class="distrito">) encogida
de forma uniforme para dejar una rendija entre vecinos (sin bordes duplicados).

Uso:
    python3 -m venv .venv-mapas && .venv-mapas/bin/pip install shapely
    .venv-mapas/bin/python scripts/generar-mapas.py madrid barcelona malaga
    .venv-mapas/bin/python scripts/generar-mapas.py malaga --rendija 4   # más separación

Opciones:
    --rendija N     separación entre distritos en unidades del SVG (por defecto, la de cada ciudad)
    --simplificar N tolerancia de simplificación de contornos (por defecto 0.25)
    --salida DIR    carpeta de salida (por defecto public/images/hero)

Fuentes y licencias (mencionar la fuente en la web, ver el pie de página):
    fuenlabrada-cp  Códigos postales de Fuenlabrada, de la carpeta local 'Mapas ciudades' (origen y licencia por confirmar)
    fuenlabrada  OpenStreetMap (ODbL), límite municipal, para el mapa de un caso
    madrid     Ayuntamiento de Madrid, Geoportal - Distritos (TopoJSON)
    barcelona  Ajuntament de Barcelona, Open Data BCN - Districtes (vía martgnz/bcn-geodata)
    malaga     Ayuntamiento de Málaga, Datos abiertos - Distrito Municipal (CC BY 4.0)
"""
import argparse
import json
import math
import os
import re
import sys
import unicodedata
import urllib.request

from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CIUDADES = {
    'madrid': {
        'url': 'https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/LIMITES_ADMINISTRATIVOS/Distritos/TopoJSON/Distritos.json',
        'formato': 'topojson',
        'campo_nombre': 'NOMBRE',
        'campo_orden': 'COD_DIS',
        'escala': 1500.0,       # unidades por grado de latitud (fija, para no alterar el mapa ya publicado)
        'rendija': 3.5,
        'aria': 'Distritos de Madrid',
        'nombres': {},
    },
    'barcelona': {
        'url': 'https://raw.githubusercontent.com/martgnz/bcn-geodata/master/districtes/districtes.geojson',
        'formato': 'geojson',
        'campo_nombre': 'NOM',
        'campo_orden': 'CODI_UA',
        'tamano': 508.0,        # tamaño de la dimensión mayor, en unidades del SVG
        'rendija': 3.0,
        'aria': 'Districtes de Barcelona',
        'nombres': {},
    },
    'malaga': {
        'url': 'https://datosabiertos.malaga.eu/recursos/urbanismoEInfraestructura/planimetria/callejero/da_cartografiaDistritoMunicipal-4326.geojson',
        'formato': 'geojson',
        'campo_nombre': 'NOMBRE',
        'campo_orden': 'NUMERO',
        'tamano': 520.0,
        'rendija': 3.0,
        'aria': 'Distritos de Málaga',
        # El dato viene en mayúsculas y sin tildes
        'nombres': {
            'CHURRIANA': 'Churriana', 'CARRETERA DE CADIZ': 'Carretera de Cádiz',
            'TEATINOS-UNIVERSIDAD': 'Teatinos-Universidad', 'CRUZ DE HUMILLADERO': 'Cruz de Humilladero',
            'BAILEN-MIRAFLORES': 'Bailén-Miraflores', 'PALMA-PALMILLA': 'Palma-Palmilla',
            'CIUDAD JARDIN': 'Ciudad Jardín', 'ESTE': 'Este', 'CENTRO': 'Centro',
            'PUERTO DE LA TORRE': 'Puerto de la Torre', 'CAMPANILLAS': 'Campanillas',
        },
    },
    # Municipio completo (mapa de un caso de éxito): un único polígono, límite de OpenStreetMap (ODbL)
    'fuenlabrada': {
        'url': 'https://nominatim.openstreetmap.org/search?q=Fuenlabrada,Madrid&format=geojson&polygon_geojson=1&polygon_threshold=0.0002&limit=1&featuretype=city',
        'formato': 'geojson',
        'nombre_fijo': 'Fuenlabrada',
        'tamano': 300.0,
        'rendija': 0.0,
        'aria': 'Mapa de Fuenlabrada',
        'carpeta': os.path.join('public', 'images', 'casos'),
        'nombres': {},
    },
    # Códigos postales de un municipio, desde la carpeta local "Mapas ciudades" (un polígono por código postal)
    'fuenlabrada-cp': {
        'archivo': os.path.join('Mapas ciudades', 'geojson', 'MADRID.geojson'),
        'formato': 'geojson',
        'filtro': ('CODIGO_INE', 28058),
        'campo_nombre': 'COD_POSTAL',
        'campo_orden': 'COD_POSTAL',
        'prefijo_id': 'cp-',
        'tamano': 300.0,
        'rendija': 1.2,
        'aria': 'Códigos postales de Fuenlabrada',
        'carpeta': os.path.join('public', 'images', 'casos'),
        'nombres': {},
    },
}


def descargar(ciudad, cfg):
    if 'archivo' in cfg:
        with open(os.path.join(RAIZ, cfg['archivo']), encoding='utf-8') as f:
            return json.load(f)
    cache = os.path.join(RAIZ, '.cache-mapas')
    os.makedirs(cache, exist_ok=True)
    destino = os.path.join(cache, f'{ciudad}.json')
    if not os.path.exists(destino):
        print(f'  descargando {cfg["url"]}')
        peticion = urllib.request.Request(cfg['url'], headers={'User-Agent': 'cercatv-mapas/1.0'})
        with urllib.request.urlopen(peticion) as r, open(destino, 'wb') as f:
            f.write(r.read())
    with open(destino, encoding='utf-8') as f:
        return json.load(f)


def slug(texto):
    t = unicodedata.normalize('NFD', texto)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def distritos_topojson(data, cfg):
    """TopoJSON: arcos codificados en deltas; las fronteras compartidas son exactamente iguales."""
    sx, sy = data['transform']['scale']
    tx, ty = data['transform']['translate']
    arcos = []
    for a in data['arcs']:
        x = y = 0
        pts = []
        for dx, dy in a:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))   # (lon, lat)
        arcos.append(pts)

    def arco(i):
        return arcos[i] if i >= 0 else arcos[~i][::-1]

    def anillo(indices):
        pts = []
        for i in indices:
            a = arco(i)
            pts += a if not pts else a[1:]
        return pts

    salida = []
    objeto = next(iter(data['objects'].values()))
    for g in objeto['geometries']:
        anillos = [anillo(r) for r in g['arcs']]
        salida.append((g['properties'][cfg['campo_nombre']], int(g['properties'][cfg['campo_orden']]), [(anillos[0], anillos[1:])]))
    return salida


def distritos_geojson(data, cfg):
    salida = []
    for f in data['features']:
        if 'filtro' in cfg and f['properties'].get(cfg['filtro'][0]) != cfg['filtro'][1]:
            continue
        geom = f['geometry']
        poligonos = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
        partes = [([(c[0], c[1]) for c in p[0]], [[(c[0], c[1]) for c in r] for r in p[1:]]) for p in poligonos]
        props = f['properties']
        if 'nombre_fijo' in cfg:
            salida.append((cfg['nombre_fijo'], 1, partes))
            continue
        salida.append((str(props[cfg['campo_nombre']]).strip(), int(props[cfg['campo_orden']]), partes))
    return salida


def generar(ciudad, rendija=None, simplificar=0.25, salida=None):
    cfg = CIUDADES[ciudad]
    rendija = cfg['rendija'] if rendija is None else rendija
    print(f'{ciudad}:')
    data = descargar(ciudad, cfg)
    crudos = distritos_topojson(data, cfg) if cfg['formato'] == 'topojson' else distritos_geojson(data, cfg)

    # Si varios polígonos comparten nombre (p. ej. un código postal en dos trozos), se unen en una sola pieza
    unidos = {}
    for nombre, orden, partes in crudos:
        if nombre in unidos:
            unidos[nombre][2].extend(partes)
        else:
            unidos[nombre] = (nombre, orden, list(partes))
    crudos = list(unidos.values())

    todos = [c for _, _, partes in crudos for ext, huecos in partes for c in ext]
    lat0 = sum(p[1] for p in todos) / len(todos)
    coslat = math.cos(math.radians(40.42 if ciudad == 'madrid' else lat0))
    if 'escala' in cfg:
        escala = cfg['escala']
    else:
        ancho = (max(p[0] for p in todos) - min(p[0] for p in todos)) * coslat
        alto = max(p[1] for p in todos) - min(p[1] for p in todos)
        escala = cfg['tamano'] / max(ancho, alto)

    def proy(anillo):
        return [(x * coslat * escala, -y * escala) for x, y in anillo]

    piezas = []
    for nombre, orden, partes in crudos:
        polis = []
        for ext, huecos in partes:
            p = Polygon(proy(ext), [proy(h) for h in huecos])
            polis.append(p if p.is_valid else p.buffer(0))
        nombre = cfg['nombres'].get(nombre, nombre)
        piezas.append((nombre, orden, unary_union(polis)))
    piezas.sort(key=lambda x: x[1])

    minx, miny, maxx, maxy = unary_union([p for _, _, p in piezas]).bounds

    def fmt(coords):
        return ' '.join(f'{x - minx + 6:.1f} {y - miny + 6:.1f}' for x, y in coords)

    def d_de(geom):
        if geom.is_empty:
            return ''
        partes = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
        out = []
        for p in partes:
            if p.area < 0.5:
                continue
            out.append('M' + fmt(list(p.exterior.coords)[:-1]) + 'Z')
            for h in p.interiors:
                out.append('M' + fmt(list(h.coords)[:-1]) + 'Z')
        return ''.join(out)

    ancho = maxx - minx + 12
    alto = maxy - miny + 12
    lineas = ['<?xml version="1.0" encoding="UTF-8"?>',
              f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.1f} {alto:.1f}" role="img" aria-label="{cfg["aria"]}">',
              '  <g id="distritos">']
    for nombre, _, geom in piezas:
        q = geom.buffer(-rendija / 2, quad_segs=3, join_style='round').simplify(simplificar)
        lineas.append(f'    <path id="{cfg.get("prefijo_id", "")}{slug(nombre)}" class="distrito" data-nombre="{nombre}" d="{d_de(q)}"/>')
    lineas += ['  </g>', '</svg>']

    carpeta = salida or os.path.join(RAIZ, cfg.get('carpeta', os.path.join('public', 'images', 'hero')))
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, f'mapa-{ciudad}.svg')
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')
    print(f'  {os.path.relpath(ruta, RAIZ)}  viewBox 0 0 {ancho:.1f} {alto:.1f}  {os.path.getsize(ruta)} bytes  {len(piezas)} distritos')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Genera los mapas SVG de distritos del hero.')
    ap.add_argument('ciudades', nargs='+', choices=sorted(CIUDADES))
    ap.add_argument('--rendija', type=float)
    ap.add_argument('--simplificar', type=float, default=0.25)
    ap.add_argument('--salida')
    a = ap.parse_args()
    for c in a.ciudades:
        generar(c, a.rendija, a.simplificar, a.salida)
