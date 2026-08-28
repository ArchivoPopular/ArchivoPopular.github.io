# Archivo Popular

Sitio estático de Archivo Popular publicado con GitHub Pages.

## Publicar una noticia

Cada publicación nueva requiere cuatro piezas:

1. Imagen optimizada en `assets/news/`.
2. Artículo HTML dentro de `noticias/`, con título, fecha, lugar, crédito fotográfico y fuentes.
3. Entrada al comienzo de `data/noticias.json`; el inicio y el archivo de noticias se actualizan desde ese archivo.
4. Actualización de `sitemap.xml`, `feed.xml` y de los metadatos Open Graph del inicio.
5. Regeneración del índice del buscador con `node scripts/generar-buscador.mjs`.

Las noticias deben conservar la línea editorial y el sistema de verificación de Archivo Popular: hechos separados de interpretación, al menos dos fuentes confiables, fotografía acreditada y enlaces directos a la documentación utilizada.

No deben almacenarse claves de servicios ni credenciales dentro del repositorio.

## Buscador

El buscador usa `data/buscador.json` para consultar el texto completo de las noticias, las historias, el archivo político, los perfiles de fotógrafos y la información institucional. La búsqueda funciona sin servicios externos, distingue relevancia y no se ve afectada por mayúsculas o tildes.

Después de agregar o modificar contenido indexable, ejecutar:

```sh
node scripts/generar-buscador.mjs
```

Como respaldo, el navegador también incorpora cualquier noticia nueva presente en `data/noticias.json`, aunque el índice principal todavía no se haya regenerado.
