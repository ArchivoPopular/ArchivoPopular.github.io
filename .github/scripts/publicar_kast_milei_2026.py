from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, re, html, subprocess

root = Path('.')
slug = 'kast-milei-zurdos-golpe-2026'
title = 'Milei llamó “zurdos mugrosos” a la izquierda y reivindicó el Chile posterior al golpe: Kast evitó condenarlo'
summary = 'El presidente chileno dijo que él no habría utilizado esa expresión, pero se negó a comentar las palabras de Javier Milei. El argentino había celebrado el “derrocamiento” de Salvador Allende y presentado el período posterior como una etapa de estabilidad y crecimiento.'
category = 'América Latina · Memoria y ultraderecha'
date_iso = '2026-09-07T16:43:00-03:00'
date_display = '7 SEP 2026'
place = 'Santiago · Chile'
image_rel = 'assets/news/kast-milei-presidencia-chile-2026.jpg'
social_rel = 'assets/social/archivo-popular-kast-milei-zurdos-golpe-2026-master.png'
article_rel = f'noticias/{slug}.html'
url = f'https://archivopopular.github.io/{article_rel}'
photo_credit = 'Presidencia de la República de Chile · Archivo, 3 de setiembre de 2026'
photo_source = 'https://prensa.presidencia.cl/fotografia.aspx?id=339732'

# Foto oficial descargada previamente desde la galería de Presidencia de Chile.
photo = root / 'fotos-kast-milei' / '_dsc7150.jpg'
if not photo.exists():
    candidates = list((root / 'fotos-kast-milei').glob('*.jpg'))
    if not candidates:
        raise FileNotFoundError('No se encontró la galería oficial descargada')
    photo = candidates[0]

src = Image.open(photo).convert('RGB')
# Imagen web
web = src.copy()
if web.width > 1600:
    h = round(web.height * 1600 / web.width)
    web = web.resize((1600, h), Image.Resampling.LANCZOS)
out = root / image_rel
out.parent.mkdir(parents=True, exist_ok=True)
web.save(out, quality=93, optimize=True)

# Placa 2160x2700 con geometría de la plantilla de Archivo Popular.
W, H, PH = 2160, 2700, 1590
scale = max(W/src.width, PH/src.height)
rs = src.resize((round(src.width*scale), round(src.height*scale)), Image.Resampling.LANCZOS)
left = max(0, (rs.width-W)//2)
top = max(0, (rs.height-PH)//2)
photo_crop = rs.crop((left, top, left+W, top+PH))
plate = Image.new('RGB', (W, H), '#F3F0E9')
plate.paste(photo_crop, (0,0))
d = ImageDraw.Draw(plate)
# sombra superior para logo
for y in range(520):
    a = max(0, 0.70*(1-y/520))
    shade = Image.new('RGB', (W,1), (0,0,0))
    if a > 0:
        base = plate.crop((0,y,W,y+1))
        plate.paste(Image.blend(base, shade, a), (0,y))
# crédito
d.rectangle((120,1510,1510,1590), fill='#FFFFFF')
font_bold = '/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf'
font_reg = '/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf'
credit_font = ImageFont.truetype(font_bold, 32)
d.text((154,1538), 'FOTO DE ARCHIVO: PRESIDENCIA DE LA REPÚBLICA DE CHILE', font=credit_font, fill='#090909')
# bloque titular
d.rectangle((0,1590,2160,2576), fill='#090909')
d.rectangle((0,1590,2160,1602), fill='#E30613')
head = ImageFont.truetype(font_bold,150)
lines = ['MILEI LLAMÓ “ZURDOS', 'MUGROSOS” A LA', 'IZQUIERDA: KAST', 'EVITÓ CONDENARLO']
ys = [1782,1954,2126,2298]
for line,y in zip(lines,ys):
    d.text((120,y), line, font=head, fill='#FFFFFF', anchor='ls')
info = ImageFont.truetype(font_bold,48)
d.text((120,2510), '7 DE SETIEMBRE DE 2026', font=info, fill='#E30613', anchor='ls')
d.text((2040,2510), 'SANTIAGO · CHILE', font=info, fill='#BEBAB2', anchor='rs')
# footer
d.rectangle((0,2576,2160,2700), fill='#FFFFFF')
d.rectangle((0,2576,620,2700), fill='#E30613')
footer_font = ImageFont.truetype(font_bold,58)
d.text((310,2657), 'NOTICIA', font=footer_font, fill='#FFFFFF', anchor='mm')
handle_font = ImageFont.truetype(font_bold,62)
d.text((2040,2657), '@archivopopular', font=handle_font, fill='#090909', anchor='rs')
# logo exacto
logo = Image.open(root/'logo.png').convert('RGBA').resize((560,181), Image.Resampling.LANCZOS)
plate_rgba = plate.convert('RGBA')
plate_rgba.alpha_composite(logo, (800,42))
social = root / social_rel
social.parent.mkdir(parents=True, exist_ok=True)
plate_rgba.convert('RGB').save(social, quality=96)

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
<main id="contenido" class="page-main"><article class="wrapper article-shell"><header class="article-header"><p class="eyebrow">{category}</p><p class="story-meta"><span>7 DE SETIEMBRE DE 2026 · 16:43</span><span>{place}</span><span>Archivo Popular</span></p><h1>{title}</h1><p class="article-deck">{summary}</p></header>
<figure class="article-figure"><img src="../{image_rel}" alt="José Antonio Kast y Javier Milei durante una reunión en el Palacio de La Moneda" width="1600" loading="eager"><figcaption>José Antonio Kast y Javier Milei durante una reunión de trabajo en La Moneda. Foto de archivo: Presidencia de la República de Chile · 3 de setiembre de 2026.</figcaption></figure>
<div class="article-body">
<p>El presidente de Chile, José Antonio Kast, evitó este lunes condenar las expresiones de Javier Milei contra la izquierda durante el Foro Madrid realizado en Santiago. Consultado específicamente por el uso de la expresión “zurdos mugrosos”, Kast respondió: “Yo no lo habría dicho, pero no voy a comentar las palabras que emitió Javier Milei”.</p>
<p>Las declaraciones del mandatario argentino habían provocado críticas en Chile desde la oposición y también reparos dentro del oficialismo. Durante su intervención del 3 de setiembre, Milei volvió a plantear una confrontación ideológica abierta contra la izquierda y habló del “cáncer de la izquierda”, además de utilizar el insulto que luego motivó la consulta a Kast.</p>
<p>El punto más sensible de su discurso estuvo relacionado con la historia chilena. Milei afirmó que “tras el derrocamiento del comunista Allende, Chile entró en un período de estabilidad y crecimiento que se extendió por más de 40 años”. Su formulación presentó el quiebre institucional de 1973 como el inicio de una etapa positiva sin detenerse en la dictadura de Augusto Pinochet y las graves violaciones a los derechos humanos cometidas por el régimen.</p>
<p>El Partido Socialista chileno y dirigentes de la oposición cuestionaron públicamente las palabras de Milei y exigieron una respuesta del gobierno. También aparecieron críticas desde sectores de Chile Vamos, que consideraron inconveniente que un mandatario extranjero utilizara suelo chileno para intervenir de esa manera en una discusión vinculada a la memoria del golpe de Estado.</p>
<p>Kast optó por marcar una distancia limitada. Dijo que él no habría empleado el insulto, pero rechazó profundizar sobre las palabras del presidente argentino y sostuvo que el Foro Madrid era un encuentro de carácter privado con connotación pública. La respuesta evitó transformar el episodio en un choque abierto entre dos gobiernos que mantienen una estrecha sintonía política.</p>
<p>La relación entre Kast y Milei ha sido presentada por ambos como parte de un nuevo eje de derechas en América Latina. Los dos participaron en la Carta de Madrid y comparten una agenda de confrontación con fuerzas progresistas y de izquierda. Esa proximidad explica parte del debate abierto en Chile sobre cuánto debe pesar la afinidad ideológica cuando aparecen declaraciones referidas a la historia política y a la memoria democrática del país.</p>
<p>El episodio ocurre, además, a pocos días de un nuevo aniversario del golpe de Estado del 11 de setiembre de 1973. La discusión sobre Allende, Pinochet y las responsabilidades de la dictadura sigue siendo uno de los principales puntos de disputa de la política chilena, y las declaraciones de Milei volvieron a colocar ese pasado en el centro del debate regional.</p>
</div>
<aside class="article-aside" aria-labelledby="fuentes"><h2 id="fuentes">Fuentes consultadas</h2><ul class="source-list">
<li><a href="https://elpais.com/chile/2026-09-07/kast-yo-no-habria-dicho-lo-de-zurdos-mugrosos-pero-no-voy-a-comentar-las-palabras-de-javier-milei.html" rel="noopener" target="_blank">EL PAÍS Chile · respuesta de Kast</a></li>
<li><a href="https://www.cooperativa.cl/noticias/site/artic/20260904/pags-amp/20260904143641.html" rel="noopener" target="_blank">Cooperativa · declaraciones de Milei y reacciones</a></li>
<li><a href="https://www.biobiochile.cl/noticias/internacional/america-latina/2026/09/03/el-comunista-allende-y-zurdos-mugrosos-las-incendiarias-frases-de-javier-milei-en-el-foro-madrid.shtml" rel="noopener" target="_blank">BioBioChile · discurso de Milei</a></li>
<li><a href="{photo_source}" rel="noopener" target="_blank">Presidencia de la República de Chile · galería fotográfica oficial</a></li>
</ul></aside></article></main>
<footer class="site-footer"><div class="wrapper footer-grid"><div class="footer-brand"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"><p>Noticias políticas, memoria y fotografía desde Uruguay con una mirada popular y latinoamericana.</p></div><div class="footer-column"><h2>Secciones</h2><ul><li><a href="../noticias.html">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia de las izquierdas</a></li><li><a href="../fotografos.html">Nuestros fotógrafos</a></li></ul></div><div class="footer-column"><h2>Seguinos</h2><ul><li><a href="https://www.instagram.com/archivopopular/" rel="me noopener" target="_blank">Instagram</a></li><li><a href="https://www.facebook.com/profile.php?id=61560610077791" rel="noopener" target="_blank">Facebook</a></li><li><a href="https://www.tiktok.com/@archivopopular" rel="noopener" target="_blank">TikTok</a></li></ul></div></div><div class="wrapper footer-bottom"><span>Archivo Popular © <span data-current-year>2026</span></span><span>Montevideo, Uruguay</span></div></footer><script src="../site.js?v=20260828-1" defer></script>
</body></html>'''
article_path = root / article_rel
article_path.parent.mkdir(parents=True, exist_ok=True)
article_path.write_text(article, encoding='utf-8')

# Noticias dinámicas
news_path = root/'data/noticias.json'
news = json.loads(news_path.read_text(encoding='utf-8'))
news = [n for n in news if n.get('id') != slug]
item = {
    'id': slug,
    'title': title,
    'summary': summary,
    'category': category,
    'date': date_iso,
    'dateDisplay': date_display,
    'place': place,
    'image': image_rel,
    'imageAlt': 'José Antonio Kast y Javier Milei durante una reunión en el Palacio de La Moneda',
    'photoCredit': photo_credit,
    'url': article_rel
}
news.insert(0,item)
news_path.write_text(json.dumps(news, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

# Fallback del home
index_path = root/'index.html'
idx = index_path.read_text(encoding='utf-8')
hero = f'''<article class="lead-story" data-latest-story aria-live="polite">
      <figure><img src="{image_rel}" alt="José Antonio Kast y Javier Milei durante una reunión en La Moneda" width="1600"><figcaption class="photo-credit">Foto: {photo_credit}</figcaption></figure>
      <div class="lead-copy"><p class="story-meta"><span>{date_display}</span><span>{place}</span></p><h1 id="ultima-noticia">{title}</h1><p class="summary">{summary}</p><a class="story-link" href="{article_rel}">Leer la noticia completa</a></div>
    </article>'''
idx = re.sub(r'<article class="lead-story" data-latest-story aria-live="polite">.*?</article>', hero, idx, count=1, flags=re.S)
idx = re.sub(r'<meta property="og:image" content="[^"]+">', f'<meta property="og:image" content="https://archivopopular.github.io/{image_rel}">', idx, count=1)
index_path.write_text(idx, encoding='utf-8')

# Fallback de noticias: insertar tarjeta si no existe
noticias_path = root/'noticias.html'
nt = noticias_path.read_text(encoding='utf-8')
if article_rel not in nt:
    card = f'''\n          <a class="news-card" href="{article_rel}"><figure><img src="{image_rel}" alt="José Antonio Kast y Javier Milei durante una reunión en La Moneda" width="658" height="425" loading="lazy"></figure><div class="news-card__body"><p class="eyebrow">{category}</p><h2>{title}</h2><p>{summary}</p><p class="story-meta"><span>{date_display}</span><span>{place}</span></p></div></a>'''
    nt = re.sub(r'(<div class="news-grid" data-news-grid[^>]*>)', r'\1'+card, nt, count=1)
    noticias_path.write_text(nt, encoding='utf-8')

# Feed
feed_path = root/'feed.xml'
feed = feed_path.read_text(encoding='utf-8')
if url not in feed:
    item_xml = f'''\n    <item><title>{html.escape(title)}</title><link>{url}</link><guid>{url}</guid><pubDate>Mon, 07 Sep 2026 19:43:00 GMT</pubDate><description>{html.escape(summary)}</description></item>'''
    feed = feed.replace('<item>', item_xml+'\n    <item>', 1)
feed = re.sub(r'<lastBuildDate>.*?</lastBuildDate>', '<lastBuildDate>Mon, 07 Sep 2026 19:43:00 GMT</lastBuildDate>', feed, count=1)
feed_path.write_text(feed, encoding='utf-8')

# Sitemap
sitemap_path = root/'sitemap.xml'
sm = sitemap_path.read_text(encoding='utf-8')
if url not in sm:
    sm = sm.replace('</urlset>', f'  <url><loc>{url}</loc><lastmod>2026-09-07</lastmod></url>\n</urlset>')
sitemap_path.write_text(sm, encoding='utf-8')

# Buscador
if (root/'scripts/generar-buscador.mjs').exists():
    subprocess.run(['node','scripts/generar-buscador.mjs'], check=True)

print(article_rel)
print(image_rel)
print(social_rel)
