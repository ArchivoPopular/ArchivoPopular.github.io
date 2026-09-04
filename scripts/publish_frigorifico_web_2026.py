from pathlib import Path
from datetime import datetime, timezone
import json, re, html, subprocess

ROOT = Path(__file__).resolve().parents[1]
slug = 'frigorifico-tacuarembo-1300-seguro-paro-2026'
article_rel = f'noticias/{slug}.html'
site_url = f'https://archivopopular.github.io/{article_rel}'
image_rel = 'assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg'
title = '1.300 trabajadores en seguro de paro: Frigorífico Tacuarembó paraliza su actividad'
summary = ('De los 1.700 empleados de la planta, alrededor de 1.300 quedarán amparados por el seguro de desempleo. '
           'La reestructura mantiene sobre la mesa 150 puestos de trabajo, rebajas salariales y tercerizaciones, mientras el sindicato rechaza que el ajuste recaiga sobre la plantilla.')
category = 'Trabajo · Industria frigorífica'
place = 'Tacuarembó · Uruguay'
iso = '2026-09-04T14:58:00-03:00'
rss_date = 'Fri, 04 Sep 2026 17:58:00 GMT'
photo_credit = 'Subrayado · 3 de setiembre de 2026'

article = f'''<!doctype html>
<html lang="es-UY">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#090909">
  <meta name="description" content="{html.escape(summary, quote=True)}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(summary, quote=True)}">
  <meta property="og:image" content="https://archivopopular.github.io/{image_rel}">
  <meta property="article:published_time" content="{iso}">
  <link rel="canonical" href="{site_url}">
  <link rel="stylesheet" href="../styles.css?v=20260828-1">
  <title>{html.escape(title)} | Archivo Popular</title>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": {json.dumps(title, ensure_ascii=False)},
    "datePublished": "{iso}",
    "dateModified": "{iso}",
    "inLanguage": "es-UY",
    "image": ["https://archivopopular.github.io/{image_rel}"],
    "author": {{"@type": "Organization", "name": "Archivo Popular"}},
    "publisher": {{"@type": "Organization", "name": "Archivo Popular", "url": "https://archivopopular.github.io/"}},
    "mainEntityOfPage": "{site_url}"
  }}
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
        <p class="eyebrow">{category}</p>
        <p class="story-meta"><span>4 DE SETIEMBRE DE 2026 · 14:58</span><span>{place}</span><span>Archivo Popular</span></p>
        <h1>{title}</h1>
        <p class="article-deck">{summary}</p>
      </header>

      <figure class="article-figure">
        <img src="../{image_rel}" alt="Frigorífico Tacuarembó durante el conflicto laboral de setiembre de 2026" width="658" height="425">
        <figcaption>Imagen del conflicto en el Frigorífico Tacuarembó. Foto: {photo_credit}.</figcaption>
      </figure>

      <div class="article-body">
        <p>El Frigorífico Tacuarembó se encamina a una paralización prácticamente total de su actividad y alrededor de 1.300 trabajadores, sobre una plantilla de 1.700, quedarán amparados por el seguro de desempleo. A los cerca de 750 operarios que ya habían ingresado al seguro de paro se sumarán unos 550 más.</p>

        <p>La reestructura planteada por la empresa incluye la reducción de 150 puestos de trabajo, cambios en el sistema de producción y la tercerización de algunos servicios. Según la Asociación de Obreros y Empleados del Frigorífico Tacuarembó, los cambios salariales propuestos podrían implicar rebajas de entre 40% y 45% en determinados componentes de la remuneración.</p>

        <p>El sindicato rechazó los despidos arbitrarios y la rebaja salarial y presentó una contrapropuesta para discutir alternativas que permitan sostener la actividad sin descargar el costo de la reestructura sobre los trabajadores. La Federación Obrera de la Industria de la Carne respaldó el rechazo gremial.</p>

        <p>La empresa ha vinculado la baja de actividad a las dificultades del mercado chino y a la menor disponibilidad de ganado para faena. Desde el sindicato cuestionan que la situación financiera justifique el paquete de ajustes y recuerdan que la planta se mantiene entre las de mayor nivel de faena del país. Esa última valoración corresponde a la representación sindical y forma parte de una negociación todavía abierta.</p>

        <p>El contraste con lo ocurrido hace apenas cuatro meses es fuerte. El 23 de abril, MBRF inauguró una ampliación de la planta por unos 70 millones de dólares e incorporó 570 trabajadores, llevando el total de empleos directos en Tacuarembó a 1.700. En aquel momento, el gobierno presentó la inversión como una señal positiva para el empleo y la producción.</p>

        <p>Ahora, la mayor parte de esa plantilla quedará temporalmente fuera de actividad. La negociación entre empresa, sindicato y Ministerio de Trabajo continúa abierta y deberá definir qué ocurre con los puestos incluidos en la reestructura, las tercerizaciones y los cambios salariales.</p>
      </div>

      <aside class="article-aside" aria-labelledby="fuentes">
        <h2 id="fuentes">Fuentes consultadas</h2>
        <ul class="source-list">
          <li><a href="https://www.cronista.com/uruguay/economia-uy/frigorifico-tacuarembo-detendra-totalmente-su-actividad-desde-el-proximo-martes/" rel="noopener" target="_blank">El Cronista Uruguay · 1.300 trabajadores en seguro de paro y paralización</a></li>
          <li><a href="https://www.tardaguila.uy/ganaderia/mbrf-dejara-de-faenar-en-tacuarembo-y-la-caballada-tambien-saldra-de-actividad" rel="noopener" target="_blank">Tardáguila · Cese de faena y alcance sobre la plantilla</a></li>
          <li><a href="https://www.subrayado.com.uy/trabajadores-del-frigorifico-tacuarembo-presentaron-contrapropuesta-no-al-despido-arbitrario-ni-la-rebaja-salarial-n1017236" rel="noopener" target="_blank">Subrayado · Posición y contrapropuesta del sindicato</a></li>
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
(ROOT / article_rel).write_text(article, encoding='utf-8')

news_path = ROOT / 'data/noticias.json'
data = json.loads(news_path.read_text(encoding='utf-8'))
data = [item for item in data if item.get('id') != slug]
data.insert(0, {
    'id': slug,
    'title': title,
    'summary': summary,
    'category': category,
    'date': iso,
    'dateDisplay': '4 SEP 2026',
    'place': place,
    'image': image_rel,
    'imageAlt': 'Frigorífico Tacuarembó durante el conflicto laboral de setiembre de 2026',
    'photoCredit': photo_credit,
    'url': article_rel
})
news_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

index_path = ROOT / 'index.html'
idx = index_path.read_text(encoding='utf-8')
idx = re.sub(r'<meta property="og:image" content="[^"]+">', f'<meta property="og:image" content="https://archivopopular.github.io/{image_rel}">', idx, count=1)
hero = f'''<article class="lead-story" data-latest-story aria-live="polite">
      <figure>
        <img src="{image_rel}" alt="Frigorífico Tacuarembó durante el conflicto laboral de setiembre de 2026" width="658" height="425">
        <figcaption class="photo-credit">Foto: {photo_credit}</figcaption>
      </figure>
      <div class="lead-copy">
        <p class="story-meta"><span>4 SEP 2026</span><span>{place}</span></p>
        <h1 id="ultima-noticia">{title}</h1>
        <p class="summary">{summary}</p>
        <a class="story-link" href="{article_rel}">Leer la noticia completa</a>
      </div>
    </article>'''
idx = re.sub(r'<article class="lead-story" data-latest-story aria-live="polite">.*?</article>', hero, idx, count=1, flags=re.S)
index_path.write_text(idx, encoding='utf-8')

noticias_path = ROOT / 'noticias.html'
nt = noticias_path.read_text(encoding='utf-8')
if article_rel not in nt:
    card = f'''\n          <a class="news-card" href="{article_rel}">
            <figure><img src="{image_rel}" alt="Frigorífico Tacuarembó durante el conflicto laboral de setiembre de 2026" width="658" height="425"></figure>
            <div class="news-card__body"><p class="eyebrow">{category}</p><h2>{title}</h2><p>{summary}</p><p class="story-meta"><span>4 SEP 2026</span><span>{place}</span></p></div>
          </a>'''
    marker = '<div class="news-grid" data-news-grid aria-live="polite">'
    nt = nt.replace(marker, marker + card, 1)
noticias_path.write_text(nt, encoding='utf-8')

feed_path = ROOT / 'feed.xml'
feed = feed_path.read_text(encoding='utf-8')
feed = re.sub(r'<lastBuildDate>.*?</lastBuildDate>', f'<lastBuildDate>{rss_date}</lastBuildDate>', feed, count=1)
if site_url not in feed:
    item = f'''\n    <item>
      <title>{html.escape(title)}</title>
      <link>{site_url}</link>
      <guid isPermaLink="true">{site_url}</guid>
      <pubDate>{rss_date}</pubDate>
      <description>{html.escape(summary)}</description>
    </item>'''
    pos = feed.find('<item>')
    feed = feed[:pos] + item + '\n    ' + feed[pos:]
feed_path.write_text(feed, encoding='utf-8')

sitemap_path = ROOT / 'sitemap.xml'
sm = sitemap_path.read_text(encoding='utf-8')
if site_url not in sm:
    line = f'  <url><loc>{site_url}</loc><lastmod>2026-09-04</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    marker = '  <url><loc>https://archivopopular.github.io/noticias/orsi-violencia-genero-hecho-aislado-2026.html</loc>'
    pos = sm.find(marker)
    sm = sm[:pos] + line + sm[pos:] if pos != -1 else sm.replace('</urlset>', line + '</urlset>')
sitemap_path.write_text(sm, encoding='utf-8')

subprocess.run(['node', str(ROOT / 'scripts/generar-buscador.mjs')], cwd=ROOT, check=True)
print(site_url)
