from pathlib import Path
import json, re

root = Path(__file__).resolve().parents[1]
slug = 'frigorifico-tacuarembo-1300-seguro-paro-2026'
article_rel = f'noticias/{slug}.html'
url = f'https://archivopopular.github.io/{article_rel}'

story = {
    'id': slug,
    'title': '1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad',
    'summary': 'La planta sumará a unos 550 trabajadores al seguro de desempleo y cerca de 1.300 de sus 1.700 funcionarios quedarán amparados. La reestructura mantiene abierta una disputa por puestos de trabajo, salarios y tercerizaciones.',
    'category': 'Trabajo · Industria frigorífica',
    'date': '2026-09-04T14:52:00-03:00',
    'dateDisplay': '4 SEP 2026',
    'place': 'Tacuarembó · Uruguay',
    'image': 'assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg',
    'imageAlt': 'Operarios durante la actividad del Frigorífico Tacuarembó en el contexto del conflicto laboral de setiembre de 2026',
    'photoCredit': 'Subrayado · 3 de setiembre de 2026',
    'url': article_rel,
}

# Datos dinámicos de noticias.
data_path = root / 'data/noticias.json'
stories = json.loads(data_path.read_text(encoding='utf-8'))
stories = [item for item in stories if item.get('id') != slug]
stories.insert(0, story)
data_path.write_text(json.dumps(stories, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

article = '''<!doctype html>
<html lang="es-UY">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#090909">
  <meta name="description" content="La planta sumará a unos 550 trabajadores al seguro de desempleo y cerca de 1.300 de sus 1.700 funcionarios quedarán amparados. La reestructura mantiene abierta una disputa por puestos, salarios y tercerizaciones.">
  <meta property="og:type" content="article">
  <meta property="og:title" content="1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad">
  <meta property="og:description" content="Cerca de 1.300 de los 1.700 trabajadores de la planta quedarán bajo seguro de desempleo en medio de una reestructura laboral.">
  <meta property="og:image" content="https://archivopopular.github.io/assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg">
  <meta property="article:published_time" content="2026-09-04T14:52:00-03:00">
  <link rel="canonical" href="https://archivopopular.github.io/noticias/frigorifico-tacuarembo-1300-seguro-paro-2026.html">
  <link rel="stylesheet" href="../styles.css?v=20260828-1">
  <title>1.300 trabajadores en seguro de paro en Frigorífico Tacuarembó | Archivo Popular</title>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": "1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad",
    "datePublished": "2026-09-04T14:52:00-03:00",
    "dateModified": "2026-09-04T14:52:00-03:00",
    "inLanguage": "es-UY",
    "image": ["https://archivopopular.github.io/assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg"],
    "author": {"@type": "Organization", "name": "Archivo Popular"},
    "publisher": {"@type": "Organization", "name": "Archivo Popular", "url": "https://archivopopular.github.io/"},
    "mainEntityOfPage": "https://archivopopular.github.io/noticias/frigorifico-tacuarembo-1300-seguro-paro-2026.html"
  }
  </script>
</head>
<body>
  <a class="skip-link" href="#contenido">Saltar al contenido</a>
  <header class="site-header">
    <div class="wrapper topline"><span>Montevideo · Uruguay · Desde 2023</span><span>Noticias, memoria y fotografía</span></div>
    <div class="wrapper brandbar">
      <a class="brand" href="../index.html" aria-label="Archivo Popular, inicio"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"></a>
      <nav class="site-nav" aria-label="Navegación principal" data-open="false">
        <ul><li><a href="../index.html">Inicio</a></li><li><a href="../noticias.html" aria-current="page">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia</a></li><li><a href="../fotografos.html">Fotógrafos</a></li><li><a href="../index.html#nosotros">Nosotros</a></li></ul>
      </nav>
      <button class="menu-button" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </header>

  <main id="contenido" class="page-main">
    <article class="wrapper article-shell">
      <header class="article-header">
        <p class="eyebrow">Trabajo · Industria frigorífica</p>
        <p class="story-meta"><span>4 DE SETIEMBRE DE 2026 · 14:52</span><span>Tacuarembó · Uruguay</span><span>Archivo Popular</span></p>
        <h1>1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad</h1>
        <p class="article-deck">La planta sumará a unos 550 trabajadores al seguro de desempleo y cerca de 1.300 de sus 1.700 funcionarios quedarán amparados. La reestructura mantiene abierta una disputa por puestos de trabajo, salarios y tercerizaciones.</p>
      </header>

      <figure class="article-figure">
        <img src="../assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg" alt="Operarios durante la actividad del Frigorífico Tacuarembó en el contexto del conflicto laboral de setiembre de 2026" width="658" height="425">
        <figcaption>Actividad en el Frigorífico Tacuarembó. Foto: Subrayado · 3 de setiembre de 2026.</figcaption>
      </figure>

      <div class="article-body">
        <p>El Frigorífico Tacuarembó llevará a cerca de 1.300 el número de trabajadores amparados por el seguro de desempleo, sobre una plantilla de alrededor de 1.700 personas. La empresa incorporará a unos 550 funcionarios más a la medida y la planta quedará prácticamente paralizada desde el martes 8 de setiembre.</p>

        <p>La nueva tanda se suma a los cerca de 750 trabajadores que ya habían ingresado al seguro de paro a comienzos de mes. Tardáguila informó además que la planta dejará de faenar desde este sábado. La actividad restante quedará reducida a tareas puntuales y de mantenimiento.</p>

        <p>La empresa vinculó la caída de actividad a la situación del mercado chino y a las dificultades para sostener el ritmo de faena. En paralelo, la reestructura discutida con el sindicato incluye una reducción de unos 150 puestos de trabajo, cambios salariales y la tercerización de determinados servicios. Dirigentes de Foica han señalado que dentro de esos 150 egresos podrían incluirse causales jubilatorias o retiros voluntarios, por lo que no todos implicarían necesariamente despidos directos.</p>

        <p>La Asociación de Obreros y Empleados del Frigorífico Tacuarembó rechazó que la reestructura se descargue sobre el empleo y los salarios. Su presidente, Hugo Gálvez, dijo a Subrayado que el cambio salarial planteado podría significar reducciones de entre 40% y 45% para sectores afectados, y sostuvo que el gremio está dispuesto a discutir mecanismos de eficiencia sin aceptar despidos arbitrarios ni una rebaja de ingresos.</p>

        <p>El escenario contrasta con la expansión anunciada apenas cuatro meses atrás. En abril, MBRF inauguró una ampliación de la planta e incorporó 570 trabajadores, llevando el empleo directo en esa unidad a unas 1.700 personas. Presidencia presentó entonces la inversión como una señal favorable para el empleo y la actividad industrial en Tacuarembó.</p>

        <p>La negociación continuará en el Ministerio de Trabajo. Mientras tanto, la mayoría de la plantilla quedará bajo seguro de desempleo y vuelve al centro del debate una pregunta habitual frente a las reestructuras empresariales: cuánto del ajuste termina recayendo sobre quienes viven de su salario.</p>
      </div>

      <aside class="article-aside" aria-labelledby="fuentes">
        <h2 id="fuentes">Fuentes consultadas</h2>
        <ul class="source-list">
          <li><a href="https://www.cronista.com/uruguay/economia-uy/frigorifico-tacuarembo-detendra-totalmente-su-actividad-desde-el-proximo-martes/" rel="noopener" target="_blank">El Cronista · Paralización y 1.300 trabajadores en seguro de paro</a></li>
          <li><a href="https://www.subrayado.com.uy/trabajadores-del-frigorifico-tacuarembo-presentaron-contrapropuesta-no-al-despido-arbitrario-ni-la-rebaja-salarial-n1017236" rel="noopener" target="_blank">Subrayado · Posición del sindicato y discusión salarial</a></li>
          <li><a href="https://www.tardaguila.uy/ganaderia/mbrf-dejara-de-faenar-en-tacuarembo-y-la-caballada-tambien-saldra-de-actividad" rel="noopener" target="_blank">Tardáguila · Alcance de la paralización y posición de Foica</a></li>
          <li><a href="https://www.gub.uy/presidencia/comunicacion/noticias/orsi-frigorifico-tacuarembo-inversiones-empleo" rel="noopener" target="_blank">Presidencia · Ampliación de abril e incorporación de 570 trabajadores</a></li>
        </ul>
      </aside>
    </article>
  </main>

  <footer class="site-footer">
    <div class="wrapper footer-grid">
      <div class="footer-brand"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"><p>Noticias políticas, memoria y fotografía desde Uruguay con una mirada popular y latinoamericana.</p></div>
      <div class="footer-column"><h2>Secciones</h2><ul><li><a href="../noticias.html">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia de las izquierdas</a></li><li><a href="../fotografos.html">Nuestros fotógrafos</a></li></ul></div>
      <div class="footer-column"><h2>Seguinos</h2><ul><li><a href="https://www.instagram.com/archivopopular/" rel="me noopener" target="_blank">Instagram</a></li><li><a href="https://www.facebook.com/profile.php?id=61560610077791" rel="noopener" target="_blank">Facebook</a></li><li><a href="https://www.tiktok.com/@archivopopular" rel="noopener" target="_blank">TikTok</a></li></ul></div>
    </div>
    <div class="wrapper footer-bottom"><span>Archivo Popular © <span data-current-year>2026</span></span><span>Montevideo, Uruguay</span></div>
  </footer>
  <script src="../site.js?v=20260828-1" defer></script>
</body>
</html>
'''
(root / article_rel).write_text(article, encoding='utf-8')

# Portada: actualizar imagen social y fallback de última noticia.
index_path = root / 'index.html'
index = index_path.read_text(encoding='utf-8')
index = re.sub(
    r'<meta property="og:image" content="[^"]+">',
    '<meta property="og:image" content="https://archivopopular.github.io/assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg">',
    index,
    count=1,
)
lead = '''<article class="lead-story" data-latest-story aria-live="polite">
      <figure>
        <img src="assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg" alt="Operarios durante la actividad del Frigorífico Tacuarembó en el contexto del conflicto laboral de setiembre de 2026" width="658" height="425">
        <figcaption class="photo-credit">Foto: Subrayado · 3 de setiembre de 2026</figcaption>
      </figure>
      <div class="lead-copy">
        <p class="story-meta"><span>4 SEP 2026</span><span>Tacuarembó · Uruguay</span></p>
        <h1 id="ultima-noticia">1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad</h1>
        <p class="summary">La planta sumará a unos 550 trabajadores al seguro de desempleo y cerca de 1.300 de sus 1.700 funcionarios quedarán amparados. La reestructura mantiene abierta una disputa por puestos, salarios y tercerizaciones.</p>
        <a class="story-link" href="noticias/frigorifico-tacuarembo-1300-seguro-paro-2026.html">Leer la noticia completa</a>
      </div>
    </article>'''
index = re.sub(r'<article class="lead-story" data-latest-story aria-live="polite">[\s\S]*?</article>', lead, index, count=1)
index_path.write_text(index, encoding='utf-8')

# Listado de noticias: fallback estático.
noticias_path = root / 'noticias.html'
noticias = noticias_path.read_text(encoding='utf-8')
if article_rel not in noticias:
    card = '''          <a class="news-card" href="noticias/frigorifico-tacuarembo-1300-seguro-paro-2026.html">
            <figure><img src="assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg" alt="Operarios durante la actividad del Frigorífico Tacuarembó en el contexto del conflicto laboral de setiembre de 2026" width="658" height="425"></figure>
            <div class="news-card__body"><p class="eyebrow">Trabajo · Industria frigorífica</p><h2>1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad</h2><p>La planta sumará a unos 550 trabajadores al seguro de desempleo y cerca de 1.300 de sus 1.700 funcionarios quedarán amparados.</p><p class="story-meta"><span>4 SEP 2026</span><span>Tacuarembó · Uruguay</span></p></div>
          </a>\n'''
    marker = '<div class="news-grid" data-news-grid aria-live="polite">\n'
    noticias = noticias.replace(marker, marker + card, 1)
noticias_path.write_text(noticias, encoding='utf-8')

# RSS.
feed_path = root / 'feed.xml'
feed = feed_path.read_text(encoding='utf-8')
feed = re.sub(r'<lastBuildDate>.*?</lastBuildDate>', '<lastBuildDate>Fri, 04 Sep 2026 17:52:00 GMT</lastBuildDate>', feed, count=1)
if url not in feed:
    item = '''    <item>
      <title>1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad</title>
      <link>https://archivopopular.github.io/noticias/frigorifico-tacuarembo-1300-seguro-paro-2026.html</link>
      <guid isPermaLink="true">https://archivopopular.github.io/noticias/frigorifico-tacuarembo-1300-seguro-paro-2026.html</guid>
      <pubDate>Fri, 04 Sep 2026 17:52:00 GMT</pubDate>
      <description>La planta sumará a unos 550 trabajadores al seguro de desempleo y cerca de 1.300 de sus 1.700 funcionarios quedarán amparados.</description>
    </item>\n'''
    feed = feed.replace('    <item>\n', item + '    <item>\n', 1)
feed_path.write_text(feed, encoding='utf-8')

# Sitemap.
sitemap_path = root / 'sitemap.xml'
sitemap = sitemap_path.read_text(encoding='utf-8')
if url not in sitemap:
    entry = '  <url><loc>https://archivopopular.github.io/noticias/frigorifico-tacuarembo-1300-seguro-paro-2026.html</loc><lastmod>2026-09-04</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    anchor = '  <url><loc>https://archivopopular.github.io/noticias/orsi-violencia-genero-hecho-aislado-2026.html</loc>'
    sitemap = sitemap.replace(anchor, entry + anchor, 1)
sitemap_path.write_text(sitemap, encoding='utf-8')

print(article_rel)
