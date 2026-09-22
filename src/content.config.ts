import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

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
    progreso: z.number(),
    descripcion: z.string(),
    imagen: z.string().optional(),
    destacado: z.boolean().default(false),
  }),
});

export const collections = { casos };
