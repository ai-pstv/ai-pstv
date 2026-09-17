# Memoria del proyecto +CercaTV

Documento vivo para registrar las decisiones confirmadas sobre la nueva web. Debe actualizarse cuando cambie el alcance, la arquitectura o la estrategia.

Última actualización: 13 de septiembre de 2026.

## 1. Objetivo principal

La web debe estar enfocada desde el inicio al posicionamiento:

- SEO: posicionamiento en buscadores tradicionales como Google y Bing.
- GEO: visibilidad y capacidad de ser citada o utilizada como fuente por buscadores y asistentes basados en inteligencia artificial.
- Conversión: conseguir solicitudes de empresas interesadas en estudiar una campaña.
- Captación de agencias: facilitar información específica y la descarga del Media Kit.
- Idiomas: la web debe estar disponible en español e inglés desde su arquitectura inicial.

La web no será una single page. Debe ser multipágina para responder a diferentes intenciones de búsqueda mediante URLs específicas.

La web debe concebirse como un sistema vivo y extensible. Tiene que poder recibir nuevos datos, copys, imágenes, páginas, sectores, casos, idiomas e integraciones sin reconstruir su arquitectura ni duplicar trabajo. Las ampliaciones habituales deben resolverse añadiendo contenido estructurado o configurando conectores, no modificando manualmente cada página.

## 2. Tecnología confirmada

- Frontend: Astro.
- Estilos: variables globales o design tokens para colores, tipografía, tamaños, espaciados y componentes.
- Formularios: endpoints PHP en el hosting existente.
- Datos de formularios: MySQL.
- Casos de éxito y contenidos estructurados: Astro Content Collections o sistema equivalente basado en archivos.
- Gestión editorial: principalmente mediante Codex o Claude.
- Historial y recuperación de cambios: Git.
- Publicación: compilación de Astro y despliegue de los archivos generados.

La web debe estar diseñada para administrarse mediante peticiones en lenguaje natural a Codex o Claude. El equipo aportará principalmente copys, datos e imágenes; el asistente se encargará de transformarlos en contenido estructurado, colocarlos en las plantillas, validar el resultado y preparar una vista previa.

No se comprarán Elementor Pro ni ACF Pro mientras WordPress no forme parte de la arquitectura definitiva.

Principios técnicos de extensibilidad:

- Separar contenido, presentación, formularios e integraciones.
- Crear páginas a partir de esquemas y plantillas reutilizables.
- Validar automáticamente todos los contenidos antes de compilar.
- Permitir añadir campos nuevos de forma controlada y compatible.
- Mantener una única fuente para theme, navegación, idiomas y configuración SEO.
- Evitar información repetida manualmente en diferentes páginas.
- Relacionar automáticamente sectores, casos, preguntas y contenidos relacionados.
- Encapsular CRM, correo y base de datos detrás de una capa de integración sustituible.
- Mantener compatibilidad hacia atrás cuando evolucionen los esquemas de contenido.
- Registrar cambios y permitir recuperación mediante Git.

## 3. Arquitectura SEO inicial

```text
/
├── /publicidad-television-hiperlocal
├── /segmentacion-por-codigo-postal
├── /como-funciona
├── /atresmedia
├── /sectores
│   ├── /sectores/clinicas
│   ├── /sectores/restauracion
│   ├── /sectores/automocion
│   ├── /sectores/retail
│   ├── /sectores/franquicias
│   ├── /sectores/educacion
│   └── /sectores/servicios
├── /casos-de-exito
│   └── /casos-de-exito/[slug]
├── /agencias
├── /preguntas-frecuentes
└── /contacto
```

Esta arquitectura es una propuesta inicial. Las URLs definitivas deben validarse con investigación de palabras clave, intención de búsqueda y disponibilidad de contenido suficiente.

### Arquitectura internacional

- Español será el idioma principal y utilizará las URLs raíz.
- Inglés utilizará el prefijo `/en/`.
- La versión inglesa será una base editorial; cada página SEO tendrá su propia versión inglesa cuando su traducción esté aprobada.
- Cada idioma tendrá títulos, descripciones, encabezados, slugs y textos adaptados a su intención de búsqueda; no se hará una traducción literal automática sin revisión.
- Se implementarán etiquetas `hreflang` entre las versiones española e inglesa, además de canonical propio para cada URL.
- El sitemap incluirá las páginas de ambos idiomas.

Estado actual:

- La home inglesa base está disponible en `/en/`.
- El selector ES/EN enlaza las versiones existentes de la home.
- Al cambiar de idioma se conserva el módulo equivalente que el usuario está leyendo, no una posición exacta de píxeles.
- La etiqueta `hreflang` está incluida en la home inglesa; queda por completar de forma simétrica en la home española y automatizarla para todas las páginas futuras.

Ejemplo:

```text
/publicidad-television-hiperlocal
/en/hyperlocal-tv-advertising

/sectores/clinicas
/en/sectors/clinics

/casos-de-exito/[slug]
/en/case-studies/[slug]
```

## 4. Menú principal propuesto

- Inicio.
- Publicidad hiperlocal.
- Cómo funciona.
- Sectores.
- Casos de éxito.
- Agencias.
- Botón destacado: Estudiar mi campaña.

### Header V1

- Logotipo oficial compuesto de Atresmedia +CercaTV.
- Navegación de escritorio: Inicio, Publicidad hiperlocal, Cómo funciona, Sectores, Casos de éxito y Agencias.
- Selector de idioma visible: ES/EN.
- CTA destacado: Estudiar mi campaña.
- Header fijo durante el desplazamiento.
- En móvil, la navegación se presenta en un panel desplegable con selector de idioma y CTA.
- Incluye un selector claro/oscuro reversible para comparar ambos acabados visuales. La elección se conserva en el navegador del usuario.
- No incluye buscador, teléfono ni megamenú; solo se añadirán si se confirma una necesidad.
- El selector ES/EN navega entre las versiones existentes y conserva el bloque equivalente durante el cambio.

No todas las páginas SEO deben aparecer en el menú principal. Las páginas secundarias podrán enlazarse desde contenidos relacionados, sectores, casos de éxito y footer.

## 5. Principios SEO

- Cada página debe responder a una intención de búsqueda concreta.
- No se crearán páginas vacías, duplicadas o con contenido superficial solo para aumentar el número de URLs.
- Cada URL debe tener título, descripción, encabezado principal y contenido propios.
- Los enlaces internos deben conectar servicios, sectores, preguntas y casos relacionados.
- Los casos de éxito deben reforzar las páginas de sector correspondientes.
- Las páginas deben incluir datos estructurados cuando sean aplicables.
- La web debe generar sitemap XML, robots.txt y URLs canónicas.
- Las páginas bilingües deben enlazarse mediante `hreflang` y selector de idioma.
- Las redirecciones deben gestionarse cuando cambie una URL.
- Imágenes optimizadas, descriptivas y con texto alternativo útil.
- Rendimiento, accesibilidad y experiencia móvil forman parte del SEO.

## 6. Principios GEO

- Explicar de forma clara qué es +CercaTV, qué ofrece, para quién sirve y dónde opera.
- Utilizar afirmaciones concretas y verificables, evitando textos comerciales vagos.
- Estructurar las respuestas con encabezados, listas, tablas y preguntas frecuentes cuando ayuden a comprender el contenido.
- Identificar claramente empresa, servicio, cobertura, relación con Atresmedia y datos de contacto.
- Publicar casos con contexto, metodología, fechas y resultados verificables.
- Mantener coherencia entre páginas y actualizar información obsoleta.
- Preparar contenido que pueda responder directamente preguntas reales de clientes y agencias.
- Incluir autoría, fechas de publicación o actualización y fuentes cuando corresponda.

## 7. Formularios

Solo se han confirmado dos formularios:

### Estudiar mi campaña

Un único formulario reutilizado desde los distintos botones de conversión de la web.

### Descargar Media Kit

Formulario específico de la página de agencias.

Flujo técnico previsto:

1. Astro muestra y valida inicialmente el formulario.
2. PHP vuelve a validar la información en el servidor.
3. Los datos se guardan en MySQL.
4. Se envía una notificación al equipo.
5. El usuario recibe una confirmación o acceso al Media Kit.

Los formularios deben incluir protección CSRF, medidas contra spam, limitación de envíos, consultas preparadas, consentimiento legal y política de conservación de datos.

## 8. Casos de éxito

Los casos funcionarán de forma parecida a un Custom Post Type de WordPress, pero estarán gestionados como contenido estructurado en Astro.

Campos iniciales:

- Título.
- Slug.
- Cliente o marca.
- Familia o sector.
- Subfamilia.
- Localidad o zona.
- Objetivo.
- Solución aplicada.
- Resultado principal.
- Métricas adicionales.
- Testimonio.
- Imagen o logotipo.
- Canales utilizados.
- Destacado: sí/no.
- Fecha.
- Estado: borrador o publicado.

Los casos podrán aparecer en:

- Su ficha individual.
- El archivo general de casos.
- La página del sector correspondiente.
- Zonas de resultados destacados cuando `destacado` sea verdadero.

Codex o Claude podrán crear y editar casos siguiendo el esquema, pero la publicación deberá pasar primero por revisión humana y vista previa.

## 8.1. Flujo editorial asistido por IA

El equipo no debería necesitar editar código para nutrir la web.

Flujo previsto:

1. El equipo entrega a Codex o Claude el copy, datos, imágenes y página de destino.
2. El asistente comprueba si falta información obligatoria.
3. Clasifica el contenido: página, sector, caso de éxito, pregunta frecuente, testimonio u otro tipo definido.
4. Adapta el material al esquema correspondiente sin inventar cifras, clientes, afirmaciones o resultados.
5. Genera la versión española y, cuando se solicite, prepara la adaptación inglesa para revisión.
6. Optimiza nombres de archivo, formatos, dimensiones, texto alternativo y metadatos de las imágenes.
7. Crea o actualiza los archivos de contenido sin alterar las plantillas ni el theme salvo petición expresa.
8. Ejecuta validaciones de estructura, enlaces, compilación, SEO y accesibilidad.
9. Abre una vista previa y resume exactamente qué ha cambiado.
10. Solo publica después de recibir aprobación humana explícita.

Peticiones de ejemplo:

```text
Crea un caso de éxito para Clínica Norte con este copy y estas imágenes.
Relaciónalo con Clínicas > Salud dental y déjalo como borrador destacado.
```

```text
Actualiza la página de agencias con este nuevo Media Kit y prepara también la versión inglesa.
No publiques todavía; abre una vista previa.
```

```text
Añade estas tres preguntas a la página de publicidad hiperlocal y genera los datos estructurados correspondientes.
```

Reglas de seguridad editorial:

- Codex o Claude no deben publicar automáticamente por defecto.
- Nunca deben inventar resultados, testimonios, clientes, cobertura o cifras comerciales.
- Las imágenes originales deben conservarse y las versiones optimizadas guardarse por separado.
- Los cambios deben quedar registrados en Git y poder revertirse.
- El contenido generado debe validarse contra esquemas antes de compilar.
- Las credenciales de hosting, correo o base de datos no se guardarán en contenidos ni en el repositorio.

## 9. Identidad visual

- Marca: Atresmedia +CercaTV.
- Color corporativo: `#CB7721`.
- Colores principales: naranja, negro y blanco.
- Tipografía principal: Gotham Pro alojada localmente en formatos WOFF2. La licencia web ha sido confirmada por el responsable del proyecto el 12 de septiembre de 2026.
- La web no debe depender de Google Fonts ni de otros servicios externos para cargar tipografías.
- El naranja debe utilizarse como acento y guía visual.
- El logotipo debe respetar sus versiones y zona de seguridad.
- Todos los componentes deben consumir variables globales del theme.
- En mobile, los textos deben evitar una presencia exagerada o "gritada". La escala tipográfica debe mantener impacto, pero priorizar lectura cómoda, jerarquía clara y sensación editorial.
- La versión mobile debe tener ajustes propios de tamaño, interlineado y espaciado; no debe ser una reducción directa de la escala desktop.

Fuente actual de los tokens visuales: `src/styles/tokens.css`.

## 10. Material disponible

- Manual de identidad corporativa de +CercaTV.
- Wireframe inicial de la landing.
- Logotipos de canales de Atresmedia.
- Correo de aclaraciones sobre páginas, casos administrables, formularios y licencias.

## 11. Decisiones pendientes

- Investigación de palabras clave y arquitectura SEO definitiva.
- Investigación de palabras clave independiente para español e inglés.
- Confirmar si todos los contenidos estarán disponibles en ambos idiomas desde el lanzamiento.
- Definir quién traducirá y quién aprobará los textos en inglés.
- Alcance geográfico exacto y posibles páginas por ubicación.
- Menú definitivo.
- Contenido específico de cada página.
- Familias y subfamilias iniciales.
- Primeros casos de éxito.
- Campos definitivos de los formularios.
- Correo receptor de las solicitudes.
- Uso o no de CRM y Calendly.
- Funcionamiento exacto de la descarga del Media Kit.
- Textos legales, privacidad y cookies.
- Sistema de despliegue y acceso al hosting.
- Flujo exacto de aprobación antes de publicar contenido generado por IA.

## 12. Regla de mantenimiento

Cuando se tome una decisión importante:

1. Actualizar este documento.
2. Indicar qué queda confirmado y qué continúa pendiente.
3. No guardar contraseñas, tokens, credenciales ni datos personales.
4. Mantener separados los hechos confirmados de las propuestas.
