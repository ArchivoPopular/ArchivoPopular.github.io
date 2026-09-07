from pathlib import Path
from PIL import Image
import json, re, html, subprocess, urllib.request

root = Path('.')
slug = 'uruguayos-eeuu-decreto-lacalle-deportaciones-2026'
title = 'Uruguayos en EE.UU. advierten que un decreto de Lacalle los expone a detenciones y deportaciones'
summary = ('Representantes de uruguayos en el exterior pidieron a Yamandú Orsi revisar el Decreto 281/022, '
           'que exige antecedentes penales del país de residencia para tramitar pasaportes en el exterior. '
           'Aseguran que en Estados Unidos el requisito puede exponer a personas a detenciones o deportaciones.')
category = 'Política nacional · Uruguayos en el exterior'
date_iso = '2026-09-07T10:24:00-03:00'
date_display = '7 SEP 2026'
place = 'Montevideo · Uruguay'
image_rel = 'assets/news/orsi-torre-ejecutiva-ignacio-turell-2026-09-04.jpg'
social_rel = 'assets/social/archivo-popular-uruguayos-eeuu-decreto-lacalle-2026-master.png'
article_rel = f'noticias/{slug}.html'
url = f'https://archivopopular.github.io/{article_rel}'
image_alt = 'Yamandú Orsi en la Torre Ejecutiva durante una reunión del 4 de setiembre de 2026'
photo_credit = 'Ignacio Turell / Presidencia de la República · Archivo, 4 de setiembre de 2026'

photo_url = 'https://medios.presidencia.gub.uy/tav_portal/2026/noticias/AP_745/_DSC9943.jpg'
req = urllib.request.Request(photo_url, headers={'User-Agent':'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=60) as r:
    Path('/tmp/orsi.jpg').write_bytes(r.read())

src = Image.open('/tmp/orsi.jpg').convert('RGB')
target_w = 1600
if src.width > target_w:
    h = round(src.height * target_w / src.width)
    src_web = src.resize((target_w, h), Image.Resampling.LANCZOS)
else:
    src_web = src
out = root / image_rel
out.parent.mkdir(parents=True, exist_ok=True)
src_web.save(out, quality=92, optimize=True)

W, PH = 2160, 1590
scale = max(W/src.width, PH/src.height)
resized = src.resize((round(src.width*scale), round(src.height*scale)), Image.Resampling.LANCZOS)
left = max(0, (resized.width-W)//2)
top = max(0, (resized.height-PH)//2)
crop = resized.crop((left, top, left+W, top+PH))
crop.save('/tmp/photo-crop.jpg', quality=96)

photo_uri = Path('/tmp/photo-crop.jpg').resolve().as_uri()
svg = f'''<svg width="2160" height="2700" viewBox="0 0 2160 2700" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="topShade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000000" stop-opacity="0.70"/><stop offset="0.72" stop-color="#000000" stop-opacity="0"/></linearGradient></defs>
<rect width="2160" height="2700" fill="#F3F0E9"/>
<image x="0" y="0" width="2160" height="1590" href="{photo_uri}" preserveAspectRatio="xMidYMid slice"/>
<rect x="0" y="0" width="2160" height="520" fill="url(#topShade)"/>
<rect x="120" y="1510" width="1390" height="80" fill="#FFFFFF"/>
<text x="154" y="1562" fill="#090909" font-family="Nimbus Sans" font-size="32" font-weight="700" letter-spacing="3">FOTO DE ARCHIVO: IGNACIO TURELL / PRESIDENCIA</text>
<rect x="0" y="1590" width="2160" height="986" fill="#090909"/>
<rect x="0" y="1590" width="2160" height="12" fill="#E30613"/>
<text x="120" y="1782" fill="#FFFFFF" font-family="Nimbus Sans" font-size="150" font-weight="700" letter-spacing="-2">
<tspan x="120" dy="0">URUGUAYOS EN EE.UU.</tspan>
<tspan x="120" dy="172">ADVIERTEN QUE DECRETO</tspan>
<tspan x="120" dy="172">DE LACALLE LOS EXPONE</tspan>
<tspan x="120" dy="172">A DEPORTACIONES</tspan>
</text>
<text x="120" y="2510" fill="#E30613" font-family="Nimbus Sans" font-size="48" font-weight="700" letter-spacing="2.5">7 DE SETIEMBRE DE 2026</text>
<text x="2040" y="2510" text-anchor="end" fill="#BEBAB2" font-family="Nimbus Sans" font-size="48" font-weight="600" letter-spacing="2">MONTEVIDEO · URUGUAY</text>
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
logo = Image.open(root/'logo.png').convert('RGBA')
logo.thumbnail((560,181), Image.Resampling.LANCZOS)
box_x, box_y, box_w, box_h = 800, 42, 560, 181
x = box_x + (box_w-logo.width)//2
y = box_y + (box_h-logo.height)//2
plate.alpha_composite(logo, (x,y))
plate.convert('RGB').save(social)

body_paragraphs = [
'Representantes de uruguayos residentes en el exterior pidieron al presidente Yamandú Orsi que reconsidere el Decreto 281/022, aprobado durante el gobierno de Luis Lacalle Pou, por entender que una de sus exigencias para tramitar pasaportes fuera del país puede dejar a compatriotas expuestos a detenciones o deportaciones, especialmente en Estados Unidos.',
'El decreto, promulgado el 31 de agosto de 2022 y firmado por Lacalle Pou junto a los entonces ministros Luis Alberto Heber y Francisco Bustillo, modificó el reglamento de expedición de pasaportes. Entre otros cambios, estableció que los mayores de edad que gestionen el documento en el exterior deben acreditar sus antecedentes judiciales en Uruguay y presentar un certificado de carencia de antecedentes del país donde residen.',
'La norma prevé una alternativa cuando las autoridades del país de residencia no expiden ese certificado o existe una “justa causa de impedimento”: en esos casos pueden comparecer dos testigos ante el funcionario consular. Sin embargo, los firmantes sostienen que, en la práctica, la exigencia incorporó nuevas cargas burocráticas, costos y riesgos para quienes viven fuera del país.',
'La carta fue firmada por uruguayos radicados en distintos puntos de Estados Unidos y también en Dinamarca, España, Argentina e Italia. El planteo reclama volver al régimen del Decreto 129/014 y abrir una instancia de diálogo con las comunidades uruguayas en el exterior.',
'El foco de la denuncia está puesto en Estados Unidos. Según los firmantes, solicitar allí el certificado de antecedentes puede obligar a personas con una situación migratoria irregular a ponerse en contacto con autoridades y exponerlas a controles migratorios. La carta afirma que ya se constataron “numerosos casos” de detenciones o deportaciones vinculados a este problema.',
'Archivo Popular no encontró, al momento de esta publicación, una estadística oficial que permita establecer cuántas deportaciones fueron provocadas específicamente por el trámite exigido por el Decreto 281/022. La relación causal entre el requisito y casos concretos de deportación corresponde, por ahora, a la denuncia formulada por los representantes de la diáspora.',
'El contexto migratorio estadounidense sí muestra un endurecimiento verificable. Cancillería informó que durante 2025 y hasta el 6 de enero de 2026 se registraron aproximadamente 100 deportaciones de uruguayos desde Estados Unidos, una cifra superior a las de los años anteriores. A fines de 2024, el gobierno estadounidense había comunicado a Uruguay que 365 compatriotas tenían órdenes de deportación.',
'El cambio normativo de 2022 ocurrió después de la polémica por el pasaporte entregado al narcotraficante Sebastián Marset mientras estaba detenido en Dubái. En aquel momento, el gobierno sostuvo que la reglamentación vigente no impedía la emisión del documento por antecedentes registrados en otros países. El Decreto 281/022 amplió luego las exigencias vinculadas a antecedentes y requisitorias internacionales.',
'La discusión enfrenta dos objetivos que no son necesariamente incompatibles: reforzar la seguridad en la expedición de documentos y garantizar que los ciudadanos uruguayos puedan acceder a su pasaporte sin quedar sometidos a riesgos desproporcionados. Los firmantes cuestionan que la respuesta a las fallas que quedaron expuestas por el caso Marset haya trasladado nuevas dificultades a miles de uruguayos en el exterior.',
'Hasta el cierre de esta nota no se había difundido una respuesta pública del Poder Ejecutivo a la carta. La definición ahora queda en manos del gobierno de Orsi, que deberá decidir si mantiene el régimen actual, introduce excepciones o modifica el decreto.'
]
body_html = '\n'.join(f'<p>{html.escape(p)}</p>' for p in body_paragraphs)

sources = [
('El País · carta de la diáspora y reclamo al presidente Orsi','https://www.elpais.com.uy/informacion/politica/diaspora-de-uruguayos-alerta-que-decreto-de-lacalle-genera-deportaciones-en-ee-uu'),
('Uypress · reclamo de uruguayos en el exterior','https://www.uypress.net/Actualidad/EEUU-Uruguayos-en-el-exterior-piden-a-Orsi-cambiar-decreto-que-advierten-los-expone-a-detenciones-y-deportaciones-uc155958'),
('IMPO · Decreto 281/022','https://www.impo.com.uy/bases/decretos/281-2022'),
('El País · deportaciones de uruguayos desde Estados Unidos en 2025','https://www.elpais.com.uy/que-pasa/en-un-ano-estados-unidos-deporto-a-100-uruguayos-cifras-record-en-2025-y-como-es-empezar-de-cero-en-uruguay'),
('Montevideo Portal · contexto del cambio normativo tras el caso Marset','https://www.montevideo.com.uy/Noticias/A-raiz-del-caso-Marset-Gobierno-modifico-requisito-de-antecedentes-para-emitir-pasaportes-uc831571'),
('Presidencia · fotografía de archivo y términos de uso','https://www.gub.uy/presidencia/comunicacion/publicaciones/presidente-orsi-recibio-referentes-politicos')
]
source_items = '\n'.join(f'<li><a href="{u}" rel="noopener" target="_blank">{html.escape(n)}</a></li>' for n,u in sources)

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
<main id="contenido" class="page-main"><article class="wrapper article-shell"><header class="article-header"><p class="eyebrow">{category}</p><p class="story-meta"><span>7 DE SETIEMBRE DE 2026 · 10:24</span><span>{place}</span><span>Archivo Popular</span></p><h1>{html.escape(title)}</h1><p class="article-deck">{html.escape(summary)}</p></header>
<figure class="article-figure"><img src="../{image_rel}" alt="{html.escape(image_alt, quote=True)}" width="1600" loading="eager"><figcaption>Yamandú Orsi durante una reunión en la Torre Ejecutiva. Foto de archivo: Ignacio Turell / Presidencia de la República · 4 de setiembre de 2026. La imagen no corresponde a la entrega de la carta.</figcaption></figure>
<div class="article-body">
{body_html}
</div>
<aside class="article-aside" aria-labelledby="fuentes"><h2 id="fuentes">Fuentes consultadas</h2><ul class="source-list">
{source_items}
</ul></aside></article></main>
<footer class="site-footer"><div class="wrapper footer-grid"><div class="footer-brand"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"><p>Noticias políticas, memoria y fotografía desde Uruguay con una mirada popular y latinoamericana.</p></div><div class="footer-column"><h2>Secciones</h2><ul><li><a href="../noticias.html">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia de las izquierdas</a></li><li><a href="../fotografos.html">Nuestros fotógrafos</a></li></ul></div><div class="footer-column"><h2>Seguinos</h2><ul><li><a href="https://www.instagram.com/archivopopular/" rel="me noopener" target="_blank">Instagram</a></li><li><a href="https://www.facebook.com/profile.php?id=61560610077791" rel="noopener" target="_blank">Facebook</a></li><li><a href="https://www.tiktok.com/@archivopopular" rel="noopener" target="_blank">TikTok</a></li></ul></div></div><div class="wrapper footer-bottom"><span>Archivo Popular © <span data-current-year>2026</span></span><span>Montevideo, Uruguay</span></div></footer><script src="../site.js?v=20260828-1" defer></script>
</body></html>'''
article_path = root / article_rel
article_path.parent.mkdir(parents=True, exist_ok=True)
article_path.write_text(article, encoding='utf-8')

data_path = root/'data/noticias.json'
data = json.loads(data_path.read_text(encoding='utf-8'))
data = [x for x in data if x.get('id') != slug]
data.insert(0,{
    'id':slug,'title':title,'summary':summary,'category':category,'date':date_iso,
    'dateDisplay':date_display,'place':place,'image':image_rel,'imageAlt':image_alt,
    'photoCredit':photo_credit,'url':article_rel
})
data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

index_path = root/'index.html'
idx = index_path.read_text(encoding='utf-8')
idx = re.sub(r'<meta property="og:image" content="[^"]+">', f'<meta property="og:image" content="https://archivopopular.github.io/{image_rel}">', idx, count=1)
lead = f'''<article class="lead-story" data-latest-story aria-live="polite">
      <figure>
        <img src="{image_rel}" alt="{html.escape(image_alt, quote=True)}" width="658" height="425">
        <figcaption class="photo-credit">Foto: {html.escape(photo_credit)}</figcaption>
      </figure>
      <div class="lead-copy">
        <p class="story-meta"><span>{date_display}</span><span>{place}</span></p>
        <h1 id="ultima-noticia">{html.escape(title)}</h1>
        <p class="summary">{html.escape(summary)}</p>
        <a class="story-link" href="{article_rel}">Leer la noticia completa</a>
      </div>
    </article>'''
idx = re.sub(r'<article class="lead-story" data-latest-story aria-live="polite">.*?</article>', lead, idx, count=1, flags=re.S)
index_path.write_text(idx, encoding='utf-8')

news_path = root/'noticias.html'
news = news_path.read_text(encoding='utf-8')
if article_rel not in news:
    card = f'''\n          <a class="news-card" href="{article_rel}">\n            <figure><img src="{image_rel}" alt="{html.escape(image_alt, quote=True)}" width="1600"></figure>\n            <div class="news-card__body"><p class="eyebrow">{category}</p><h2>{html.escape(title)}</h2><p>{html.escape(summary)}</p><p class="story-meta"><span>{date_display}</span><span>{place}</span></p></div>\n          </a>'''
    marker = '<div class="news-grid" data-news-grid aria-live="polite">'
    news = news.replace(marker, marker+card, 1)
news_path.write_text(news, encoding='utf-8')

feed_path = root/'feed.xml'
feed = feed_path.read_text(encoding='utf-8')
feed = re.sub(r'<lastBuildDate>.*?</lastBuildDate>', '<lastBuildDate>Mon, 07 Sep 2026 13:24:00 GMT</lastBuildDate>', feed, count=1)
if url not in feed:
    item = f'''\n    <item>\n      <title>{html.escape(title)}</title>\n      <link>{url}</link>\n      <guid isPermaLink="true">{url}</guid>\n      <pubDate>Mon, 07 Sep 2026 13:24:00 GMT</pubDate>\n      <description>{html.escape(summary)}</description>\n    </item>'''
    pos = feed.find('</lastBuildDate>')
    if pos != -1:
        pos += len('</lastBuildDate>')
        feed = feed[:pos] + item + feed[pos:]
feed_path.write_text(feed, encoding='utf-8')

sitemap_path = root/'sitemap.xml'
sitemap = sitemap_path.read_text(encoding='utf-8')
if url not in sitemap:
    entry = f'\n  <url><loc>{url}</loc><lastmod>2026-09-07</lastmod></url>\n'
    sitemap = sitemap.replace('</urlset>', entry+'</urlset>')
sitemap_path.write_text(sitemap, encoding='utf-8')

if (root/'scripts/generar-buscador.mjs').exists():
    subprocess.run(['node','scripts/generar-buscador.mjs'], check=True)

assert Image.open(social).size == (2160,2700)
assert article_path.exists() and out.exists()
print('READY', article_rel, social_rel)
