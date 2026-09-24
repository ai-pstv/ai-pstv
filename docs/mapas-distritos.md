# Mapas de distritos del hero

Los heros de la home (ES, CA y EN) incluyen un panel animado con un **mapa de distritos** de una ciudad, en el que se ilumina una zona cada vuelta. Este documento explica de dónde salen esos mapas, cómo se generan, dónde están y cómo se cambian.

## Qué ciudad usa cada versión

| Versión | Página | Ciudad | Distritos | Archivo |
|---|---|---|---|---|
| Español | `src/pages/index.astro` | Madrid | 21 | `public/images/hero/mapa-madrid.svg` |
| Catalán | `src/pages/ca/index.astro` | Barcelona | 10 | `public/images/hero/mapa-barcelona.svg` |
| Inglés | `src/pages/en/index.astro` | Málaga | 11 | `public/images/hero/mapa-malaga.svg` |

## Fuentes de datos y licencias

Los datos son **abiertos y oficiales** de cada ayuntamiento. Se descargan automáticamente al ejecutar el script.

| Ciudad | Fuente | Formato | Licencia / condiciones |
|---|---|---|---|
| Madrid | [Geoportal del Ayuntamiento de Madrid](https://geoportal.madrid.es/fsdescargas/IDEAM_WBGEOPORTAL/LIMITES_ADMINISTRATIVOS/Distritos/TopoJSON/Distritos.json), parte del portal [datos.madrid.es](https://datos.madrid.es/dataset/300497-0-distritos-municipales-madrid) | TopoJSON | Datos abiertos del Ayuntamiento. Incluye el ajuste de límites de 2020 |
| Barcelona | [Open Data BCN](https://opendata-ajuntament.barcelona.cat/) (Ajuntament de Barcelona), a través de la copia en GeoJSON de [martgnz/bcn-geodata](https://github.com/martgnz/bcn-geodata) | GeoJSON | Datos abiertos del Ajuntament. **Se descargan de una copia de terceros**, no directamente del portal |
| Málaga | [Datos abiertos del Ayuntamiento de Málaga](https://datosabiertos.malaga.eu/dataset/sistema-de-informacion-cartografica-distrito-municipal), "Sistema de Información Cartográfica - Distrito Municipal" | GeoJSON (EPSG:4326) | **CC BY 4.0**: exige atribución |

### Atribución

El pie de página (`src/components/Footer.astro`) tiene preparada una línea de créditos con enlaces a cada portal, traducida a los tres idiomas. **Ahora mismo está oculta**: se controla con la constante `SHOW_MAP_CREDITS` (a `false`); poniéndola a `true` aparece en todas las páginas.

- ES: *Mapas: datos abiertos de los Ayuntamientos de Madrid, Barcelona y Málaga (CC BY 4.0).*
- CA: *Mapes: dades obertes dels Ajuntaments de Madrid, Barcelona i Màlaga (CC BY 4.0).*
- EN: *Maps: open data from the city councils of Madrid, Barcelona and Málaga (CC BY 4.0).*

> **Importante antes de publicar en producción:** la licencia CC BY 4.0 de los datos de Málaga exige atribución, así que conviene activar la línea de créditos (o mencionar la fuente en otro sitio visible, por ejemplo en el aviso legal). Además, revisar las condiciones de reutilización exactas de los portales de Madrid y Barcelona, y confirmar que la atribución cubre sus condiciones.

## Cómo son los SVG generados

Cada mapa es un único SVG con **una pieza por distrito**:

```svg
<svg viewBox="0 0 435.6 508.7" role="img" aria-label="Distritos de Madrid">
  <g id="distritos">
    <path id="chamberi" class="distrito" data-nombre="Chamberí" d="M…Z"/>
    <path id="salamanca" class="distrito" data-nombre="Salamanca" d="M…Z"/>
    …
  </g>
</svg>
```

- El `id` es el nombre del distrito normalizado (minúsculas, sin tildes, con guiones): `chamberi`, `fuencarral-el-pardo`, `sarria-sant-gervasi`, `carretera-de-cadiz`…
- `data-nombre` guarda el nombre real con tildes, que es el que se muestra en el hero.
- **No llevan estilos**: el color, el brillo y las animaciones los pone el componente por CSS.
- Las piezas están **encogidas de forma uniforme** para dejar una pequeña rendija entre vecinas. Así no hay bordes duplicados (los datos originales no siempre encajan exactamente y, dibujando el borde de cada distrito, se veían líneas dobles).
- Los contornos están simplificados para que cada SVG pese entre 15 y 25 KB.

## Cómo se generan (script)

El script está en [`scripts/generar-mapas.py`](../scripts/generar-mapas.py). Descarga los datos, los proyecta a un plano, deja la rendija entre distritos, simplifica los contornos y escribe los SVG. Necesita Python 3 y la librería `shapely`.

```bash
python3 -m venv .venv-mapas
.venv-mapas/bin/pip install shapely

# Regenerar las tres ciudades
.venv-mapas/bin/python scripts/generar-mapas.py madrid barcelona malaga

# Más separación entre distritos (por defecto ~3 unidades)
.venv-mapas/bin/python scripts/generar-mapas.py malaga --rendija 4

# Contornos más o menos simplificados (por defecto 0.25)
.venv-mapas/bin/python scripts/generar-mapas.py madrid --simplificar 0.4

# Escribir en otra carpeta para comparar antes de sustituir
.venv-mapas/bin/python scripts/generar-mapas.py madrid --salida /tmp/prueba
```

Los datos descargados se guardan en `.cache-mapas/` para no repetir la descarga. Esa carpeta y `.venv-mapas/` están en `.gitignore`.

El script reproduce **exactamente** los tres SVG publicados (se comprobó comparando byte a byte).

### Añadir otra ciudad

1. Localizar los distritos de la ciudad en su portal de datos abiertos, en **GeoJSON con coordenadas WGS84 (EPSG:4326)** o en TopoJSON.
2. Añadir una entrada nueva al diccionario `CIUDADES` de `scripts/generar-mapas.py` con la URL, el formato, el campo del nombre y del orden, el tamaño y la rendija. Si los nombres vienen en mayúsculas o sin tildes, rellenar `nombres` con el mapeo al nombre correcto.
3. Ejecutar el script con la nueva ciudad y revisar el resultado abriendo el SVG en el navegador.
4. Añadir la fuente a la línea de atribución del pie (`Footer.astro`) y a este documento.

## Cómo se usan en la web

El componente [`src/components/HeroMapFlow.astro`](../src/components/HeroMapFlow.astro) lee el SVG al compilar y **lo incrusta en el HTML** de cada página, por lo que el navegador no descarga el archivo aparte y no hay peticiones extra.

Cada página lo invoca con su ciudad, sus zonas y sus textos:

```astro
<HeroMapFlow
  map="mapa-barcelona"
  city="BARCELONA"
  zoneSlugs={['eixample', 'gracia', 'sarria-sant-gervasi', 'sant-marti']}
  copy={heroFlowCopy}
/>
```

- `zoneSlugs`: las zonas por las que rota el hero, cada una durante una vuelta del flujo (~5,4 s). Vale cualquier `id` del SVG. Por defecto (Madrid): Chamberí, Fuencarral - El Pardo, Salamanca y Moncloa - Aravaca.
- `copy`: los textos de las tarjetas y de la terminal. `{zona}` se sustituye por el nombre del distrito activo.
- **Interruptor reversible**: en cada página hay una constante `HERO_FLOW_TEST`. Poniéndola a `false` desaparece el panel y el hero vuelve al diseño centrado original.
- El panel solo se muestra en pantallas de más de 1100 px de ancho; en tablet y móvil está oculto (pendiente de diseñar una versión móvil).

## Archivos del proyecto relacionados

```
docs/mapas-distritos.md              este documento
scripts/generar-mapas.py             generador de los SVG
public/images/hero/mapa-madrid.svg
public/images/hero/mapa-barcelona.svg
public/images/hero/mapa-malaga.svg
public/images/hero/distritos.svg     original de Illustrator (sin uso; se puede borrar)
public/images/hero/hero.png          imagen de prueba (sin uso; se puede borrar)
src/components/HeroMapFlow.astro     panel animado que usa los mapas
src/components/Footer.astro          línea de atribución de los mapas
```

## Consideraciones

- **Rendimiento**: los tres mapas juntos suman unos 54 KB y solo se incrusta el de la versión de cada página. El panel no se carga en móvil.
- **Precisión**: para cerrar huecos y dejar la rendija, las piezas se han encogido y simplificado. Sirven para ilustrar, no son un mapa cartográfico exacto.
- **Málaga**: el distrito Centro es muy pequeño frente a los periféricos (Campanillas, Puerto de la Torre…), por lo que iluminado se ve como un punto. Conviene alternarlo con zonas grandes.
