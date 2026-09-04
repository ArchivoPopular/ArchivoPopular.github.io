from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen
import json, re, html, subprocess

ROOT = Path(__file__).resolve().parents[1]
TMP = Path('/tmp/frigorifico-tacuarembo.jpg')

CURRENT = 'https://www.cronista.com/resizer/v2/I6T4QLTEAVFGPN4TCY6WND65JU.jpg?auth=182c6c09f7821ddc5d2673acccb9dd4048ff949ef9bb9bdfe16d5181d9616190&height=450&quality=70&smart=true&width=800'
ARCHIVE = 'https://www.gub.uy/presidencia/sites/presidencia/files/styles/documento/public/imagenes/noticias/WhatsApp%20Image%202026-04-23%20at%2015.03.10.jpeg?itok=nSEjtus9'


def download(url: str, target: Path):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 ArchivoPopular/1.0'})
    with urlopen(req, timeout=30) as r:
        data = r.read()
    target.write_bytes(data)
    Image.open(target).verify()


try:
    download(CURRENT, TMP)
    photo_credit = 'El Cronista · 4 de setiembre de 2026'
    photo_short = 'El Cronista'
except Exception as e:
    print('Foto actual no disponible, se usa archivo oficial:', e)
    download(ARCHIVE, TMP)
    photo_credit = 'Presidencia de la República · Archivo, 23 de abril de 2026'
    photo_short = 'Presidencia de la República · Archivo'

now = datetime.now(ZoneInfo('America/Montevideo')).replace(second=0, microsecond=0)
iso = now.isoformat()
hhmm = now.strftime('%H:%M')
rss_date = now.astimezone(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

slug = 'frigorifico-tacuarembo-1300-seguro-paro-2026'
article_rel = f'noticias/{slug}.html'
site_url = f'https://archivopopular.github.io/{article_rel}'
image_rel = 'assets/news/frigorifico-tacuarembo-seguro-paro-2026.jpg'
social_rel = 'assets/social/archivo-popular-frigorifico-tacuarembo-seguro-paro-2026-master.png'
title = '1.300 trabajadores quedarán en seguro de paro en Frigorífico Tacuarembó'
summary = ('De una plantilla de 1.700 personas, alrededor de 1.300 quedarán amparadas por el seguro de desempleo. '
           'La reestructura mantiene sobre la mesa 150 egresos, cambios salariales y tercerizaciones, mientras el sindicato rechaza que el ajuste recaiga sobre los trabajadores.')
category = 'Trabajo · Industria frigorífica'
place = 'Tacuarembó · Uruguay'

src = Image.open(TMP).convert('RGB')
out_news = ROOT / image_rel
out_news.parent.mkdir(parents=True, exist_ok=True)
web_img = src.copy()
if web_img.width < 1200:
    scale = 1200 / web_img.width
    web_img = web_img.resize((1200, round(web_img.height * scale)), Image.Resampling.LANCZOS)
web_img.save(out_news, 'JPEG', quality=91, optimize=True)

# Placa master 2160x2700, misma jerarquía de la plantilla habitual.
W, H = 2160, 2700
PHOTO_H = 1590
BLACK_Y = 1602
FOOTER_Y = 2576
canvas = Image.new('RGB', (W, H), '#080808')
im = src.copy()
scale = max(W / im.width, PHOTO_H / im.height)
im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
left = max(0, (im.width - W) // 2)
top = max(0, (im.height - PHOTO_H) // 2)
photo = im.crop((left, top, left + W, top + PHOTO_H))
canvas.paste(photo, (0, 0))
d = ImageDraw.Draw(canvas)

overlay = Image.new('RGBA', (W, 400), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(400):
    a = int(75 * (1 - y / 400))
    od.line((0, y, W, y), fill=(0, 0, 0, max(0, a)))
canvas.paste(overlay, (0, 0), overlay)

logo = Image.open(ROOT / 'logo.png').convert('RGBA')
target_w = 600
target_h = round(logo.height * target_w / logo.width)
logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
canvas.paste(logo, ((W - target_w) // 2, 45), logo)

font_path_bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_credit = ImageFont.truetype(font_path_bold, 38)
credit_text = f'FOTO: {photo_short.upper()}'
bbox = d.textbbox((0, 0), credit_text, font=font_credit)
cw = bbox[2] - bbox[0] + 44
ch = 74
cx, cy = 118, PHOTO_H - ch
d.rectangle((cx, cy, cx + cw, cy + ch), fill='white')
d.text((cx + 22, cy + 16), credit_text, font=font_credit, fill='#111111')

d.rectangle((0, PHOTO_H, W, BLACK_Y), fill='#ed0712')
d.rectangle((0, BLACK_Y, W, FOOTER_Y), fill='#080808')
d.rectangle((0, FOOTER_Y, W, H), fill='white')
red_w = 620
d.rectangle((0, FOOTER_Y, red_w, H), fill='#ed0712')


def fit_font(text, max_width, start=142, min_size=72):
    for s in range(start, min_size - 1, -2):
        f = ImageFont.truetype(font_path_bold, s)
        if d.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
    return ImageFont.truetype(font_path_bold, min_size)


lines = [
    '1.300 TRABAJADORES',
    'QUEDARÁN EN',
    'SEGURO DE PARO',
    'EN FRIGORÍFICO',
    'TACUAREMBÓ',
]
x, y, maxw = 118, 1712, 1924
for i, line in enumerate(lines):
    f = fit_font(line, maxw, 150 if i == 0 else 142, 92)
    d.text((x, y), line, font=f, fill='white', stroke_width=1, stroke_fill='white')
    bb = d.textbbox((x, y), line, font=f)
    y = bb[3] + 24

font_meta = ImageFont.truetype(font_path_bold, 48)
date_text = '4 DE SETIEMBRE DE 2026'
place_text = 'TACUAREMBÓ · URUGUAY'
meta_y = 2486
d.text((118, meta_y), date_text, font=font_meta, fill='#f00d1a')
pb = d.textbbox((0, 0), place_text, font=font_meta)
d.text((W - 118 - (pb[2] - pb[0]), meta_y), place_text, font=font_meta, fill='#bdbdbd')

footer_font = ImageFont.truetype(font_path_bold, 60)
d.text((176, FOOTER_Y + 30), 'NOTICIA', font=footer_font, fill='white')
handle = '@archivopopular'
hb = d.textbbox((0, 0), handle, font=footer_font)
hx = red_w + (W - red_w - (hb[2] - hb[0])) // 2
d.text((hx, FOOTER_Y + 30), handle, font=footer_font, fill='#111111')

out_social = ROOT / social_rel
out_social.parent.mkdir(parents=True, exist_ok=True)
canvas.save(out_social, 'PNG', optimize=True)

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
        <p class="story-meta"><span>4 DE SETIEMBRE DE 2026 · {hhmm}</span><span>{place}</span><span>Archivo Popular</span></p>
        <h1>{title}</h1>
        <p class="article-deck">{summary}</p>
      </header>

      <figure class="article-figure">
        <img src="../{image_rel}" alt="Frigorífico Tacuarembó durante la actual crisis laboral" width="1200">
        <figcaption>Frigorífico Tacuarembó. Foto: {photo_credit}.</figcaption>
      </figure>

      <div class="article-body">
        <p>El Frigorífico Tacuarembó se encamina a una paralización prácticamente total de su actividad y alrededor de 1.300 trabajadores, sobre una plantilla de 1.700, quedarán amparados por el seguro de desempleo. La medida amplía el alcance de una crisis que ya había enviado a cerca de 750 personas al seguro de paro a comienzos de setiembre y que ahora incorpora a unos 550 trabajadores más.</p>

        <p>La empresa comunicó una reestructura que incluye la reducción de 150 puestos de trabajo, cambios en el sistema de producción y la tercerización de algunos servicios. Según dirigentes sindicales de la Asociación de Obreros y Empleados del Frigorífico Tacuarembó, los cambios salariales planteados podrían significar recortes de entre 40% y 45% en determinados componentes de la remuneración.</p>

        <p>El sindicato rechazó los despidos arbitrarios y la rebaja salarial, y presentó una contrapropuesta para discutir alternativas que permitan sostener la actividad sin trasladar el costo de la reestructura a los trabajadores. La Federación Obrera de la Industria de la Carne también respaldó el rechazo gremial.</p>

        <p>La empresa vinculó la baja de actividad a dificultades del mercado chino y a la menor disponibilidad de ganado para faena. Los trabajadores, en cambio, cuestionan que la situación financiera justifique el paquete de ajustes y recuerdan que la planta se mantiene entre las de mayor nivel de faena del país. Esa valoración corresponde al sindicato y forma parte de una negociación todavía abierta.</p>

        <p>El contraste con lo ocurrido hace apenas cuatro meses es marcado. El 23 de abril, MBRF inauguró una ampliación de la planta por unos 70 millones de dólares e incorporó 570 trabajadores, llevando el total de empleos directos en Tacuarembó a 1.700. En aquel momento, el gobierno destacó la inversión y la generación de puestos de trabajo.</p>

        <p>Ahora, la mayor parte de esa plantilla quedará temporalmente fuera de actividad. La próxima etapa de la negociación entre empresa, sindicato y Ministerio de Trabajo deberá definir qué ocurre con los 150 puestos incluidos en la reestructura, las tercerizaciones y los cambios salariales propuestos.</p>
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
data = [x for x in data if x.get('id') != slug]
data.insert(0, {
    'id': slug,
    'title': title,
    'summary': summary,
    'category': category,
    'date': iso,
    'dateDisplay': '4 SEP 2026',
    'place': place,
    'image': image_rel,
    'imageAlt': 'Frigorífico Tacuarembó durante la actual crisis laboral',
    'photoCredit': photo_credit,
    'url': article_rel,
})
news_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

index_path = ROOT / 'index.html'
idx = index_path.read_text(encoding='utf-8')
idx = re.sub(r'<meta property="og:image" content="[^"]+">', f'<meta property="og:image" content="https://archivopopular.github.io/{image_rel}">', idx, count=1)
hero = f'''<article class="lead-story" data-latest-story aria-live="polite">
      <figure>
        <img src="{image_rel}" alt="Frigorífico Tacuarembó durante la actual crisis laboral" width="1200">
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
            <figure><img src="{image_rel}" alt="Frigorífico Tacuarembó durante la actual crisis laboral" width="1200"></figure>
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

site_path = ROOT / 'sitemap.xml'
sm = site_path.read_text(encoding='utf-8')
if site_url not in sm:
    line = f'  <url><loc>{site_url}</loc><lastmod>2026-09-04</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
    marker = '  <url><loc>https://archivopopular.github.io/noticias/orsi-violencia-genero-hecho-aislado-2026.html</loc>'
    p = sm.find(marker)
    sm = sm[:p] + line + sm[p:] if p != -1 else sm.replace('</urlset>', line + '</urlset>')
site_path.write_text(sm, encoding='utf-8')

subprocess.run(['node', str(ROOT / 'scripts/generar-buscador.mjs')], cwd=ROOT, check=True)
print('PUBLICADO:', site_url)
print('PLACA:', social_rel)
print('FOTO:', photo_credit)
