import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const textosCaso = z.object({
  categoria: z.string(),
  subtitulo: z.string(),
  ubicacion: z.string(),
  producto: z.string(),
  resultadoDescripcion: z.string(),
  resultadoCorto: z.string().optional(),
  descripcion: z.string(),
});

const casos = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/casos' }),
  schema: z.object({
    index: z.string(),
    categoria: z.string(),
    categoriaSlug: z.string(),
    titulo: z.string(),
    subtitulo: z.string(),
    ubicacion: z.string(),
    producto: z.string(),
    resultadoPrefijo: z.string().default(''),
    resultadoValor: z.number(),
    resultadoDecimales: z.number().default(0),
    resultadoSufijo: z.string().default(''),
    resultadoDescripcion: z.string(),
    resultadoCorto: z.string().optional(),
    progreso: z.number(),
    descripcion: z.string(),
    imagen: z.string().optional(),
    mapa: z.string().optional(),
    lat: z.number().optional(),
    lng: z.number().optional(),
    destacado: z.boolean().default(false),
    // Textos traducidos (opcional): si falta un idioma, esa versión del caso no se genera
    traducciones: z.object({ en: textosCaso.optional(), ca: textosCaso.optional() }).optional(),
  }),
});

export const collections = { casos };
