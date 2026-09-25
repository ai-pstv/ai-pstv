# Ideas y funcionalidades para la web de +CercaTV

Documento de trabajo: qué tiene la web hoy, qué le falta y qué podría llevar para pasar de ser una web informativa a un área donde consultar, calcular y gestionar. Nada de lo marcado como "idea" está decidido ni construido.

## Contexto del negocio

+CercaTV vende **publicidad en televisión segmentada por zona** (código postal, barrio o ciudad) en los canales de Atresmedia, pensada para **negocios locales** que no pueden pagar una campaña nacional. Puntos que deben guiar cualquier decisión:

- **Accesible:** el mensaje es que la TV ya no es solo para grandes marcas.
- **Público objetivo:** negocios con una zona de influencia (concesionarios, clínicas, franquicias, retail, hostelería).
- **Prueba real:** casos de éxito verdaderos como argumento principal.
- Los formularios se guardan en **Pipedrive** mediante PHP propio (no con formularios embebidos).

## Qué hay ya

| Pieza | Estado |
|---|---|
| Home en español, inglés y catalán, con hero animado de mapa (Madrid, Málaga, Barcelona) | Hecho (textos de EN/CA por revisar) |
| Casos de éxito: archivo con filtros y página de detalle con mapa + terminal de datos | Hecho; solo Motor Dye traducido a EN/CA |
| Preguntas frecuentes con categorías, buscador, JSON-LD (SEO/GEO) y hero con buscador animado | Hecho (contenido real por completar) |
| Modo claro/oscuro, selector de idioma, aviso de acceso para la fase de pruebas | Hecho |
| Generador de mapas SVG por zonas (proyecto aparte en `Desarrollo AI/mapas`) | Hecho |
| Tablet y móvil de la FAQ y de los paneles animados | Pendiente |

## Páginas que faltan (ya enlazadas en el menú)

- Quiénes somos
- +Cerca Media
- Exclusividad con Atresmedia
- Soluciones
- Contacto y formulario de campaña (con Pipedrive)
- Aviso legal, privacidad y cookies (necesarios antes del lanzamiento)
- Traducción a inglés y catalán del resto de páginas

## Ideas por objetivo

### 1. Captar clientes nuevos

| Idea | Qué es | Depende de |
|---|---|---|
| **Comprobador de cobertura** | El visitante escribe código postal o ciudad y ve en un mapa si llegáis y qué zonas puede elegir | Lista real de zonas disponibles (Atresmedia) |
| **Simulador de campaña** | Elige zona y duración y obtiene una estimación de hogares alcanzados y una horquilla de precio | Datos de audiencia y tarifas |
| **Páginas por ciudad** | "Publicidad en TV en Sevilla", "en Málaga"…, cada una con su mapa, casos y preguntas | Mapas por ciudad (proyecto de mapas) |
| **Agente de IA** | Responde dudas con el contenido de las preguntas frecuentes y recoge el contacto | Contenido de FAQ completo |
| **Solicitud de campaña guiada** | Formulario paso a paso (zona, sector, objetivo, presupuesto) que crea el negocio en Pipedrive | Campos de Pipedrive |
| **Plantillas de anuncio** | Galería de formatos sencillos para quien no tiene spot | Material creativo |

### 2. Enseñar prueba y confianza

- Más casos de éxito reales, con mapa de la zona, resultado y, si es posible, vídeo del anuncio.
- Filtros de casos por sector y por provincia.
- Testimonios cortos de clientes.
- Página de "cómo se mide" con un ejemplo real de informe.
- Mapa público de cobertura con datos agregados (por provincia, sin identificar clientes).

### 3. Clientes actuales (área privada)

- **Área de cliente con acceso:** ver campañas activas y pasadas, zonas, fechas, resultados y facturas.
- **Aprobación de creatividades** sin correos de ida y vuelta.
- **Informe de campaña automático:** página o PDF con el mapa de la zona, el periodo y los resultados, generado desde el CRM.
- **Solicitar renovación o ampliar zona** desde el propio panel.

### 4. Ayuda a los comerciales (uso interno)

Objetivo: que el comercial llegue mejor preparado a la reunión, convenza más y envíe la propuesta antes. Es un área de la web pensada para el equipo, con acceso restringido.

**Antes de la reunión**

| Idea | Qué es | Depende de |
|---|---|---|
| **Ficha del prospecto con mapa** | El comercial escribe el negocio y su dirección y sale una hoja con su zona dibujada, casos de éxito de su sector y qué se le puede ofrecer | Mapas por ciudad; casos etiquetados por sector |
| **Buscador de casos parecidos** | Filtra por sector y ciudad para encontrar un cliente comparable, el argumento que más convence | Casos de éxito con sector y ubicación |

**Durante la reunión**

| Idea | Qué es | Depende de |
|---|---|---|
| **Simulador en pantalla** | El cliente elige su zona en el mapa y se ve lo que alcanzaría y una horquilla de inversión | Datos fiables de audiencia y tarifas (Atresmedia) |
| **Demo del hero personalizada** | La animación de la home se adapta a la ciudad del cliente para que vea "tu anuncio solo en tu zona" | Mapa de la ciudad |

**Después de la reunión**

| Idea | Qué es | Depende de |
|---|---|---|
| **Propuesta automática** | PDF o enlace con mapa, zona, fechas e inversión, generado en minutos | Plantilla de propuesta; tarifas |
| **Seguimiento en Pipedrive** | Aviso cuando el cliente abre la propuesta y recordatorios para retomar el contacto | Integración con Pipedrive |

**Para dirigir el esfuerzo**

| Idea | Qué es | Depende de |
|---|---|---|
| **Panel de clientes en mapa** | España por provincias, coloreada por número de clientes; al pulsar una provincia, lista de clientes y campañas del CRM; se puede bajar a municipios, distritos y puntos | Datos de ubicación y campaña en Pipedrive |
| **Buscador de huecos** | Zonas sin clientes de un sector concreto, para saber a dónde ir a vender | Panel anterior |
| **Ranking de zonas y sectores** | Dónde se cierra más, para poner el foco | Histórico de negocios en Pipedrive |
| **Cuadro de mando** | Campañas, inversión y resultados | Datos de campaña en Pipedrive |

**Por dónde empezar:** la ficha del prospecto con mapa y la propuesta automática, porque ayudan más y no dependen de datos de Atresmedia. El simulador y el panel de clientes van después. Antes de construir, conviene preguntar a los comerciales qué les hace perder más tiempo y qué preguntas de los clientes no saben responder.

**Notas técnicas**
- Los datos del CRM no pasan por la web pública: se leen desde un servidor que guarda la clave de Pipedrive (ya hay PHP para los formularios).
- Los mapas con clientes en puntos son solo de uso interno, con acceso protegido.
- Primer paso barato: una demo del panel con una exportación de Pipedrive (nombre o anonimizado, provincia, sector, campaña, fechas, inversión, estado, resultado).

### 5. Contenido y posicionamiento

- Blog o guías: "cómo anunciarse en TV con poco presupuesto", "TV local vs. redes sociales".
- Glosario (HbbTV, segmentación, GRP…).
- Datos estructurados (ya hay FAQ y migas de pan; se puede ampliar a organización, servicio y casos).
- Páginas por sector: "publicidad en TV para clínicas", "para concesionarios"…

## Prioridad sugerida

1. **Terminar lo básico antes del lanzamiento:** páginas que faltan, formulario con Pipedrive, textos legales, revisión de EN/CA y versión móvil.
2. **Comprobador de cobertura** y **páginas por ciudad:** mayor utilidad para quien llega a la web y aprovechan los mapas.
3. **Ayuda a los comerciales:** ficha del prospecto con mapa y propuesta automática; después el panel de clientes en mapa (primero como demo con una exportación de Pipedrive).
4. **Área de cliente e informes automáticos:** es lo más grande, y lo que convierte la web en una herramienta diaria.
5. **Simulador de campaña** cuando haya datos fiables de audiencia y precios.

## Requisitos y decisiones abiertas

- **Zonas y audiencias reales:** confirmar con Atresmedia qué se puede ofrecer y dónde. Sin eso, el comprobador y el simulador prometerían cosas que no se pueden cumplir.
- **Datos del CRM:** revisar qué campos de ubicación y de campaña están rellenos en Pipedrive antes de construir paneles.
- **Servidor:** las funciones con datos vivos (área de cliente, paneles) necesitan una parte de servidor. La web actual es estática y ya usa PHP para los formularios, que se puede aprovechar.
- **Privacidad (RGPD):** en la web pública, solo datos agregados o con permiso del cliente; los mapas con puntos por cliente, solo de uso interno.
- **Atribución de mapas:** activar `SHOW_MAP_CREDITS` en el pie antes del lanzamiento (Málaga: CC BY 4.0; Fuenlabrada: OpenStreetMap, ODbL).
- **Dominio definitivo:** quitar `noindex`, la base `/ai-web` y el acceso con contraseña al lanzar.
- **Fuentes oficiales de los mapas:** Barcelona usa una copia de terceros y Fuenlabrada, OpenStreetMap; se pueden sustituir por fuentes oficiales cuando convenga (ver `docs/mapas-distritos.md`).
