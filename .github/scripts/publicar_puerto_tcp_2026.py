from pathlib import Path
from PIL import Image
import urllib.request, json, re, html, subprocess

root = Path('.')
slug = 'paro-puerto-tcp-estabilidad-esencialidad-2026'
title = 'Nuevo paro en el puerto: el sindicato reclama estabilidad y la oposición pide declarar la esencialidad'
summary = 'TCP-Nelsury detuvo las actividades desde las 10:00 mientras reclama garantías de estabilidad laboral y jornales. La terminal sostiene que su propuesta es definitiva y Javier García pidió al Poder Ejecutivo declarar la esencialidad.'
category = 'Trabajo · Puerto de Montevideo'
date_iso = '2026-09-07T15:48:00-03:00'
date_display = '7 SEP 2026'
place = 'Puerto de Montevideo · Uruguay'
image_rel = 'assets/news/puerto-montevideo-presidencia-2024.jpg'
social_rel = 'assets/social/archivo-popular-paro-puerto-tcp-2026-master.png'
article_rel = f'noticias/{slug}.html'
url = f'https://archivopopular.github.io/{article_rel}'
image_alt = 'Terminal de contenedores del Puerto de Montevideo durante una recorrida oficial en 2024'
photo_credit = 'Presidencia de la República · Archivo, 5 de febrero de 2024'
photo_url = 'https://medios.presidencia.gub.uy/tav_portal/2024/noticias/AL_953/fgr_01.jpg'

req = urllib.request.Request(photo_url, headers={'User-Agent':'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=30) as r:
    raw = r.read()
Path('/tmp/port.jpg').write_bytes(raw)

im = Image.open('/tmp/port.jpg').convert('RGB')
if im.width > 1600:
    h = round(im.height * 1600 / im.width)
    im = im.resize((1600, h), Image.Resampling.LANCZOS)
out = root / image_rel
out.parent.mkdir(parents=True, exist_ok=True)
im.save(out, quality=92, optimize=True)

src = Image.open('/tmp/port.jpg').convert('RGB')
W, PH = 2160, 1590
scale = max(W/src.width, PH/src.height)
rs = src.resize((round(src.width*scale), round(src.height*scale)), Image.Resampling.LANCZOS)
left = max(0, (rs.width-W)//2)
top = max(0, (rs.height-PH)//2)
crop = rs.crop((left, top, left+W, top+PH))
crop.save('/tmp/port-crop.jpg', quality=96)

photo_uri = Path('/tmp/port-crop.jpg').resolve().as_uri()
svg = f'''<svg width="2160" height="2700" viewBox="0 0 2160 2700" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="topShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000000" stop-opacity="0.70"/><stop offset="0.72" stop-color="#000000" stop-opacity="0"/></linearGradient></defs>
<rect width="2160" height="2700" fill="#F3F0E9"/>
<image x="0" y="0" width="2160" height="1590" href="{photo_uri}" preserveAspectRatio="xMidYMid slice"/>
<rect x="0" y="0" width="2160" height="520" fill="url(#topShade)"/>
<rect x="120" y="1510" width="1320" height="80" fill="#FFFFFF"/>
<text x="154" y="1562" fill="#090909" font-family="Nimbus Sans" font-size="32" font-weight="700" letter-spacing="3">FOTO DE ARCHIVO: PRESIDENCIA DE LA REPÚBLICA</text>
<rect x="0" y="1590" width="2160" height="986" fill="#090909"/>
<rect x="0" y="1590" width="2160" height="12" fill="#E30613"/>
<text x="120" y="1782" fill="#FFFFFF" font-family="Nimbus Sans" font-size="150" font-weight="700" letter-spacing="-2">
<tspan x="120" dy="0">NUEVO PARO EN EL PUERTO</tspan>
<tspan x="120" dy="172">SINDICATO RECLAMA</tspan>
<tspan x="120" dy="172">GARANTÍAS Y OPOSICIÓN</tspan>
<tspan x="120" dy="172">PIDE ESENCIALIDAD</tspan>
</text>
<text x="120" y="2510" fill="#E30613" font-family="Nimbus Sans" font-size="48" font-weight="700" letter-spacing="2.5">7 DE SETIEMBRE DE 2026</text>
<text x="2040" y="2510" text-anchor="end" fill="#BEBAB2" font-family="Nimbus Sans" font-size="48" font-weight="600" letter-spacing="2">PUERTO DE MONTEVIDEO · URUGUAY</text>
<rect x="0" y="2576" width="2160" height="124" fill="#FFFFFF"/>
<rect x="0" y="2576" width="620" height="124" fill="#E30613"/>
<text x="310" y="2657" text-anchor="middle" fill="#FFFFFF" font-family="Nimbus Sans" font-size="58" font-weight="700" letter-spacing="5">NOTICIA</text>
<text x="2040" y="2657" text-anchor="end" fill="#090909" font-family="Nimbus Sans" font-size="62" font-weight="700" letter-spacing="2">@archivopopular</text>
</svg>'''
Path('/tmp/plate.svg').write_text(svg, encoding='utf-8')
social = root / social_rel
social.parent.mkdir(parents=True, exist_ok=True)
subprocess.run(['rsvg-convert','-w','2160','-h','2700','-o',str(social),'/tmp/plate.svg'], check=True)
plate = Image.open(social).convert('RGBA')
logo = Image.open(root/'logo.png').convert('RGBA').resize((560,181), Image.Resampling.LANCZOS)
plate.alpha_composite(logo, (800,42))
plate.convert('RGB').save(social, quality=96)

article = f'''<!doctype html>
<html lang="es-UY">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#090909">
<meta name="description" content="{html.escape(summary, quote=True)}">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title, quote=True)}"><meta property="og:description" content="{html.escape(summary, quote=True)}"><meta property="og:image" content="https://archivopopular.github.io/{image_rel}">
<meta property="article:published_time" content="{date_iso}"><link rel="canonical" href="{url}"><link rel="stylesheet" href="../styles.css?v=20260828-1">
<title>{html.escape(title)} | Archivo Popular</title>
</head><body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header"><div class="wrapper topline"><span>Montevideo · Uruguay · Desde 2023</span><span>Noticias, memoria y fotografía</span></div><div class="wrapper brandbar"><a class="brand" href="../index.html" aria-label="Archivo Popular, inicio"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"></a><nav class="site-nav" aria-label="Navegación principal" data-open="false"><ul><li><a href="../index.html">Inicio</a></li><li><a href="../noticias.html" aria-current="page">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia</a></li><li><a href="../fotografos.html">Fotógrafos</a></li><li><a href="../index.html#nosotros">Nosotros</a></li></ul></nav><button class="menu-button" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span><span></span><span></span></button></div></header>
<main id="contenido" class="page-main"><article class="wrapper article-shell"><header class="article-header"><p class="eyebrow">{category}</p><p class="story-meta"><span>7 DE SETIEMBRE DE 2026 · 15:48</span><span>{place}</span><span>Archivo Popular</span></p><h1>{title}</h1><p class="article-deck">{summary}</p></header>
<figure class="article-figure"><img src="../{image_rel}" alt="{image_alt}" width="1600" loading="eager"><figcaption>Terminal de contenedores del Puerto de Montevideo durante una recorrida oficial. Foto de archivo: Presidencia de la República · 5 de febrero de 2024.</figcaption></figure>
<div class="article-body">
<p>El sindicato de trabajadores de Terminal Cuenca del Plata (TCP-Nelsury) detuvo este lunes las actividades desde las 10:00 en la principal terminal especializada en contenedores del Puerto de Montevideo. La medida se produce en medio de un conflicto por la renovación del convenio colectivo y fue acompañada por reuniones sectoriales y una asamblea general definida por el gremio como “grave y urgente”.</p>
<p>Durante el paro funciona una guardia gremial mínima. Esa decisión mantiene abiertos los accesos y permite una operativa limitada en el muelle, aunque la terminal no trabaja con normalidad. Al cierre de esta nota no se había comunicado oficialmente un horario de retorno pleno a las actividades.</p>
<p>El núcleo del conflicto está en la negociación del nuevo convenio colectivo. Desde el sindicato señalaron que buscan retomar la negociación tripartita con la empresa y el Ministerio de Trabajo y Seguridad Social. Entre sus principales planteos están la estabilidad laboral y la garantía de una cantidad de jornales, dos aspectos que el gremio considera centrales para cerrar un acuerdo de cinco años.</p>
<p>Terminal Cuenca del Plata sostiene que su propuesta ya incorporó sucesivas mejoras y que quedó formulada “en términos definitivos”. La empresa afirma que no existen posibilidades de introducir nuevas modificaciones, aunque dice mantener disposición a explicar el contenido de la oferta. También rechazó las acusaciones sindicales de falta de buena fe o negativa a negociar.</p>
<p>El conflicto se arrastra desde el vencimiento del convenio colectivo, el 31 de mayo. En los últimos meses se sucedieron asambleas y paralizaciones que afectaron la operativa de buques y camiones. Luego del paro sorpresivo del sábado 5, TCP advirtió que evalúa acciones administrativas y legales si continúan medidas que, a su entender, generen perjuicios a la terminal.</p>
<p>La discusión escaló además al terreno político. El senador del Partido Nacional Javier García pidió este lunes que el Poder Ejecutivo declare la esencialidad del trabajo en el puerto. Sostuvo que las medidas sindicales están provocando un daño al país y calificó la situación como un “boicot”. Esas expresiones corresponden al dirigente opositor y no a una resolución del gobierno.</p>
<p>García aseguró además que en los primeros ocho meses del año los paros acumularon alrededor de un mes de inactividad. Archivo Popular no encontró, al momento de esta publicación, una cifra oficial independiente que permita confirmar ese cálculo exacto. La actividad portuaria, de todas formas, viene registrando interrupciones reiteradas por el conflicto.</p>
<p>La posibilidad de declarar la esencialidad ya había aparecido durante etapas anteriores de la negociación. El gobierno de Yamandú Orsi optó hasta ahora por sostener la mediación del Ministerio de Trabajo y buscar una salida tripartita. La medida es especialmente sensible por tratarse de un conflicto sindical en una infraestructura clave para el comercio exterior.</p>
<p>TCP es una sociedad público-privada: Nelsury, vinculada al grupo belga Katoen Natie, posee el 80% de las acciones y la Administración Nacional de Puertos el 20% restante. Esa estructura coloca al Estado no solo como mediador laboral, sino también como accionista minoritario de la terminal.</p>
<p>El punto inmediato será conocer qué resolvió la asamblea sindical de este lunes y si se reabre una instancia formal de negociación. Mientras tanto, la terminal continúa bajo una operativa restringida y el conflicto vuelve a instalar la discusión sobre los límites de las medidas sindicales, las obligaciones empresariales y el papel del Estado.</p>
</div>
<aside class="article-aside" aria-labelledby="fuentes"><h2 id="fuentes">Fuentes consultadas</h2><ul class="source-list">
<li><a href="https://www.montevideo.com.uy/Noticias/Hay-nuevo-paro-en-el-puerto-y-TCP-respondio-a-quienes-le-atribuyen-falta-de-buena-fe--uc974389" rel="noopener" target="_blank">Montevideo Portal · paro y posición de TCP</a></li>
<li><a href="https://altamarnews.uy/sindicato-de-tcp-detuvo-actividades-y-reclama-reanudar-negociacion-por-convenio/" rel="noopener" target="_blank">Altamar News · reclamos sindicales y negociación</a></li>
<li><a href="https://www.subrayado.com.uy/nuevo-paro-la-terminal-cuenca-del-plata-guardia-gremial-la-oposicion-pide-que-se-declare-la-esencialidad-n1017469/amp" rel="noopener" target="_blank">Subrayado · paro, guardia gremial y pedido de esencialidad</a></li>
<li><a href="https://www.telenoche.com.uy/nacionales/javier-garcia-pedira-la-esencialidad-el-puerto-o-gobiernan-los-sindicatos-o-gobierna-la-soberania-n5404368" rel="noopener" target="_blank">Telenoche · declaraciones de Javier García</a></li>
<li><a href="https://www.gub.uy/presidencia/comunicacion/fotos/obras-puerto-montevideo" rel="noopener" target="_blank">Presidencia de la República · fotografía de archivo</a></li>
<li><a href="https://www.gub.uy/presidencia/sites/presidencia/files/2021-04/cons_min_433.pdf" rel="noopener" target="_blank">Presidencia · estructura accionaria de TCP</a></li>
</ul></aside></article></main>
<footer class="site-footer"><div class="wrapper footer-grid"><div class="footer-brand"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"><p>Noticias políticas, memoria y fotografía desde Uruguay con una mirada popular y latinoamericana.</p></div><div class="footer-column"><h2>Secciones</h2><ul><li><a href="../noticias.html">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia de las izquierdas</a></li><li><a href="../fotografos.html">Nuestros fotógrafos</a></li></ul></div><div class="footer-column"><h2>Seguinos</h2><ul><li><a href="https://www.instagram.com/archivopopular/" rel="me noopener" target="_blank">Instagram</a></li><li><a href="https://www.facebook.com/profile.php?id=61560610077791" rel="noopener" target="_blank">Facebook</a></li><li><a href="https://www.tiktok.com/@archivopopular" rel="noopener" target="_blank">TikTok</a></li></ul></div></div><div class="wrapper footer-bottom"><span>Archivo Popular © <span data-current-year>2026</span></span><span>Montevideo, Uruguay</span></div></footer><script src="../site.js?v=20260828-1" defer></script>
</body></html>'''
article_path = root / article_rel
article_path.parent.mkdir(parents=True, exist_ok=True)
article_path.write_text(article, encoding='utf-8')

data_path = root/'data/noticias.json'
data = json.loads(data_path.read_text(encoding='utf-8'))
data = [x for x in data if x.get('id') != slug]
data.insert(0, {'id': slug, 'title': title, 'summary': summary, 'category': category, 'date': date_iso, 'dateDisplay': date_display, 'place': place, 'image': image_rel, 'imageAlt': image_alt, 'photoCredit': photo_credit, 'url': article_rel})
data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

index_path = root/'index.html'
idx = index_path.read_text(encoding='utf-8')
idx = re.sub(r'<meta property="og:image" content="[^"]+">', f'<meta property="og:image" content="https://archivopopular.github.io/{image_rel}">', idx, count=1)
lead = f'''<article class="lead-story" data-latest-story aria-live="polite">
      <figure>
        <img src="{image_rel}" alt="{image_alt}" width="1600">
        <figcaption class="photo-credit">Foto: {photo_credit}</figcaption>
      </figure>
      <div class="lead-copy">
        <p class="story-meta"><span>{date_display}</span><span>{place}</span></p>
        <h1 id="ultima-noticia">{title}</h1>
        <p class="summary">{summary}</p>
        <a class="story-link" href="{article_rel}">Leer la noticia completa</a>
      </div>
    </article>'''
idx = re.sub(r'<article class="lead-story" data-latest-story aria-live="polite">.*?</article>', lead, idx, count=1, flags=re.S)
index_path.write_text(idx, encoding='utf-8')

news_path = root/'noticias.html'
news = news_path.read_text(encoding='utf-8')
card = f'''\n          <a class="news-card" href="{article_rel}">
            <figure><img src="{image_rel}" alt="{image_alt}" width="1600"></figure>
            <div class="news-card__body"><p class="eyebrow">{category}</p><h2>{title}</h2><p>{summary}</p><p class="story-meta"><span>{date_display}</span><span>{place}</span></p></div>
          </a>'''
marker = '<div class="news-grid" data-news-grid aria-live="polite">'
if article_rel not in news:
    news = news.replace(marker, marker+card, 1)
news_path.write_text(news, encoding='utf-8')

feed_path = root/'feed.xml'
feed = feed_path.read_text(encoding='utf-8')
feed = re.sub(r'<lastBuildDate>.*?</lastBuildDate>', '<lastBuildDate>Mon, 07 Sep 2026 18:48:00 GMT</lastBuildDate>', feed, count=1)
item = f'''\n    <item>\n      <title>{html.escape(title)}</title>\n      <link>{url}</link>\n      <guid isPermaLink="true">{url}</guid>\n      <pubDate>Mon, 07 Sep 2026 18:48:00 GMT</pubDate>\n      <description>{html.escape(summary)}</description>\n    </item>'''
if url not in feed:
    feed = feed.replace('</channel>', item+'\n  </channel>', 1)
feed_path.write_text(feed, encoding='utf-8')

sitemap_path = root/'sitemap.xml'
sitemap = sitemap_path.read_text(encoding='utf-8')
entry = f'''\n  <url><loc>{url}</loc><lastmod>2026-09-07</lastmod></url>'''
if url not in sitemap:
    sitemap = sitemap.replace('</urlset>', entry+'\n</urlset>', 1)
sitemap = re.sub(r'(<loc>https://archivopopular.github.io/</loc>\s*<lastmod>)[^<]+', r'\g<1>2026-09-07', sitemap, count=1)
sitemap = re.sub(r'(<loc>https://archivopopular.github.io/noticias.html</loc>\s*<lastmod>)[^<]+', r'\g<1>2026-09-07', sitemap, count=1)
sitemap_path.write_text(sitemap, encoding='utf-8')

subprocess.run(['node','scripts/generar-buscador.mjs'], check=True)
print(article_rel)
print(image_rel)
print(social_rel)
