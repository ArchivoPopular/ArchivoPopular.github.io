from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, re, subprocess, requests, time

ROOT = Path('.')
ID = 'paro-nacional-universidades-argentina-financiamiento-2026'
ARTICLE_REL = f'noticias/{ID}.html'
ARTICLE_URL = f'https://archivopopular.github.io/{ARTICLE_REL}'
NEWS_IMG_REL = 'assets/news/paro-universitario-argentina-uba-mayo-2026.jpg'
SOCIAL_REL = 'assets/social/archivo-popular-paro-universitario-argentina-2026-master.png'
PHOTO_URL = 'https://www.uba.ar/storage/tm5fees8bvjJGNXfUgH9Od9zlZYpDM3uGL6bnVbd.jpg'
TITLE = 'Universidades argentinas paran en todo el país por salarios y financiamiento y preparan una quinta Marcha Federal'
SUMMARY = 'Docentes y nodocentes realizan este martes un paro nacional de 24 horas tras rechazar la oferta oficial. Reclaman el cumplimiento de la Ley 27.795, recomposición salarial, actualización de becas y más presupuesto; el Frente Sindical prepara una quinta Marcha Federal para octubre.'
CATEGORY = 'América Latina · Universidad pública y trabajo'
DATE_ISO = '2026-09-08T10:42:00-03:00'
DATE_DISPLAY = '8 SEP 2026'
PLACE = 'Argentina'
ALT = 'Movilización en defensa de la universidad pública durante la Marcha Federal Universitaria de mayo de 2026 en Buenos Aires'
CREDIT = 'Universidad de Buenos Aires · Archivo, 12 de mayo de 2026'

def get_with_retries(url, tries=5):
    last = None
    for i in range(tries):
        try:
            r = requests.get(url, timeout=45, headers={'User-Agent':'Mozilla/5.0 ArchivoPopular/1.0'})
            r.raise_for_status()
            return r
        except Exception as e:
            last = e
            time.sleep(3*(i+1))
    raise last

def cover_crop(im, size, focal=(0.5,0.5)):
    im = im.convert('RGB')
    tw, th = size
    scale = max(tw/im.width, th/im.height)
    nw, nh = round(im.width*scale), round(im.height*scale)
    im = im.resize((nw,nh), Image.Resampling.LANCZOS)
    fx, fy = focal
    left = int((nw-tw)*fx)
    top = int((nh-th)*fy)
    left = max(0,min(left,nw-tw)); top=max(0,min(top,nh-th))
    return im.crop((left,top,left+tw,top+th))

def draw_spaced(draw, xy, text, font, fill, spacing=0, anchor='la'):
    x,y=xy
    widths=[font.getlength(ch) for ch in text]
    total=sum(widths)+spacing*(len(text)-1)
    if anchor in ('ra','rm','rs'):
        x -= total
    elif anchor in ('ma','mm','ms'):
        x -= total/2
    for ch,w in zip(text,widths):
        draw.text((x,y), ch, font=font, fill=fill, anchor='la')
        x += w + spacing

def logo_fit(src, box=(560,181)):
    im=Image.open(src).convert('RGBA')
    im.thumbnail(box, Image.Resampling.LANCZOS)
    out=Image.new('RGBA', box, (0,0,0,0))
    out.alpha_composite(im, ((box[0]-im.width)//2,(box[1]-im.height)//2))
    return out

Path(NEWS_IMG_REL).parent.mkdir(parents=True, exist_ok=True)
r = get_with_retries(PHOTO_URL)
Path(NEWS_IMG_REL).write_bytes(r.content)
photo = Image.open(NEWS_IMG_REL).convert('RGB')

W,H=2160,2700
canvas=Image.new('RGB',(W,H),'black')
canvas.paste(cover_crop(photo,(2160,1590), focal=(0.5,0.48)),(0,0))
shade=Image.new('RGBA',(W,520),(0,0,0,0)); sd=ImageDraw.Draw(shade)
for y in range(520):
    a=int(175*(1-y/519))
    sd.line((0,y,W,y), fill=(0,0,0,a))
canvas=Image.alpha_composite(canvas.convert('RGBA'), Image.new('RGBA',(W,H),(0,0,0,0)))
canvas.alpha_composite(shade,(0,0))
logo_path=Path('logo.png')
if logo_path.exists():
    canvas.alpha_composite(logo_fit(logo_path),(800,42))
D=ImageDraw.Draw(canvas)
D.rectangle((0,1590,2160,2576), fill=(0,0,0,255))
D.rectangle((0,1590,2160,1602), fill=(227,6,19,255))
font_bold='/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf'
f_credit=ImageFont.truetype(font_bold,32)
credit='FOTO DE ARCHIVO: UNIVERSIDAD DE BUENOS AIRES'
credit_w=sum(f_credit.getlength(ch) for ch in credit)+3*(len(credit)-1)
tab_w=int(min(1850,max(840,credit_w+70)))
D.rectangle((120,1510,120+tab_w,1590), fill=(255,255,255,255))
draw_spaced(D,(154,1562),credit,f_credit,(0,0,0,255),spacing=3,anchor='ls')
f_head=ImageFont.truetype(font_bold,150)
lines=['UNIVERSIDADES EN PARO','EN TODA ARGENTINA','POR SALARIOS Y CONTRA','EL AJUSTE DE MILEI']
for i,line in enumerate(lines):
    draw_spaced(D,(120,1782+i*172),line,f_head,(255,255,255,255),spacing=-2,anchor='ls')
f_meta=ImageFont.truetype(font_bold,48)
draw_spaced(D,(120,2510),'8 DE SETIEMBRE DE 2026',f_meta,(227,6,19,255),spacing=2.5,anchor='ls')
draw_spaced(D,(2040,2510),'ARGENTINA',f_meta,(190,186,178,255),spacing=2,anchor='rs')
D.rectangle((0,2576,2160,2700), fill=(255,255,255,255))
D.rectangle((0,2576,620,2700), fill=(227,6,19,255))
f_not=ImageFont.truetype(font_bold,58); f_handle=ImageFont.truetype(font_bold,62)
draw_spaced(D,(310,2657),'NOTICIA',f_not,(255,255,255,255),spacing=5,anchor='ms')
draw_spaced(D,(2040,2657),'@archivopopular',f_handle,(0,0,0,255),spacing=2,anchor='rs')
Path(SOCIAL_REL).parent.mkdir(parents=True, exist_ok=True)
canvas.convert('RGB').save(SOCIAL_REL, quality=96)

article = f'''<!doctype html>
<html lang="es-UY">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#090909">
<meta name="description" content="{SUMMARY}">
<meta property="og:type" content="article"><meta property="og:title" content="{TITLE}"><meta property="og:description" content="{SUMMARY}"><meta property="og:image" content="https://archivopopular.github.io/{NEWS_IMG_REL}">
<meta property="article:published_time" content="{DATE_ISO}"><link rel="canonical" href="{ARTICLE_URL}"><link rel="stylesheet" href="../styles.css?v=20260828-1">
<title>{TITLE} | Archivo Popular</title>
</head><body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header"><div class="wrapper topline"><span>Montevideo · Uruguay · Desde 2023</span><span>Noticias, memoria y fotografía</span></div><div class="wrapper brandbar"><a class="brand" href="../index.html" aria-label="Archivo Popular, inicio"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"></a><nav class="site-nav" aria-label="Navegación principal" data-open="false"><ul><li><a href="../index.html">Inicio</a></li><li><a href="../noticias.html" aria-current="page">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia</a></li><li><a href="../fotografos.html">Fotógrafos</a></li><li><a href="../index.html#nosotros">Nosotros</a></li></ul></nav><button class="menu-button" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span><span></span><span></span></button></div></header>
<main id="contenido" class="page-main"><article class="wrapper article-shell"><header class="article-header"><p class="eyebrow">{CATEGORY}</p><p class="story-meta"><span>8 DE SETIEMBRE DE 2026 · 10:42</span><span>{PLACE}</span><span>Archivo Popular</span></p><h1>{TITLE}</h1><p class="article-deck">{SUMMARY}</p></header>
<figure class="article-figure"><img src="../{NEWS_IMG_REL}" alt="{ALT}" width="1600" loading="eager"><figcaption>Marcha Federal Universitaria del 12 de mayo de 2026 en Buenos Aires. Foto de archivo: Universidad de Buenos Aires.</figcaption></figure>
<div class="article-body">
<p>Las universidades nacionales de Argentina atraviesan este martes 8 de setiembre un paro de 24 horas convocado por el Frente Sindical de las Universidades Nacionales. La medida reúne a federaciones docentes y nodocentes de todo el país y vuelve a colocar en el centro del conflicto el financiamiento del sistema público, los salarios y la aplicación de la Ley 27.795.</p>
<p>El paro fue resuelto después de la reunión paritaria del 1.º de setiembre. El Ministerio de Capital Humano informó oficialmente que presentó una propuesta de aumento del 6% para el bimestre, con un 3% correspondiente a setiembre. Las organizaciones sindicales consideraron insuficiente la oferta y reclamaron una recomposición que recupere la pérdida acumulada del poder adquisitivo.</p>
<p>Entre las organizaciones que impulsan el plan de lucha están CONADU, CONADU Histórica, FEDUN, CTERA, FAGDUT, UDA y FATUN. Además de la discusión salarial, el frente exige la aplicación efectiva de la Ley de Financiamiento Universitario, la actualización de las becas Progresar y Manuel Belgrano y recursos que garanticen el funcionamiento de las universidades nacionales.</p>
<p>La Ley 27.795 fue sancionada en agosto de 2025 y publicada en el Boletín Oficial en octubre de ese año. Su objetivo declarado es garantizar la protección y el sostenimiento del financiamiento de la educación universitaria pública en todo el territorio argentino. El conflicto persiste porque universidades y gremios sostienen que varias de sus disposiciones no fueron ejecutadas en los términos previstos.</p>
<p>La disputa ya llegó a la Justicia. El 1.º de setiembre, el juez federal Martín Cormick hizo lugar a una medida cautelar presentada por la Universidad de Buenos Aires y ordenó al Poder Ejecutivo ejecutar de forma inmediata partidas previstas en la ley para funcionamiento, recomposición salarial, becas e investigación respecto de la UBA. En el expediente principal también rechazó el pedido oficial de levantar la cautelar que mantiene abierta la discusión por el cumplimiento de la norma.</p>
<p>El Gobierno, por su parte, sostiene que continúa negociando con las federaciones y presentó la pauta del 6% bimestral como una nueva instancia de la paritaria. Los gremios responden que el problema excede un incremento puntual y que el deterioro salarial y presupuestario acumulado exige una recomposición más amplia.</p>
<p>La protesta de este martes es parte de un calendario que seguirá durante septiembre. El Frente Sindical convocó una jornada nacional de clases públicas para el 15 de setiembre y un acto frente al área educativa del Gobierno nacional para el 17. Además, anunció que trabaja en una quinta Marcha Federal Universitaria para la primera semana de octubre.</p>
<p>La última gran movilización federal, realizada el 12 de mayo, reunió a cientos de miles de personas en Buenos Aires y tuvo réplicas en todo el país. La UBA informó entonces que el reclamo central fue el cumplimiento de la ley y la recomposición de salarios docentes y nodocentes. Cuatro meses después, el conflicto continúa abierto y vuelve a paralizar este martes buena parte del sistema universitario nacional.</p>
</div>
<aside class="article-aside" aria-labelledby="fuentes"><h2 id="fuentes">Fuentes consultadas</h2><ul class="source-list">
<li><a href="https://adiuc.org.ar/2026/09/04/paro-total/" rel="noopener" target="_blank">ADIUC · convocatoria del Frente Sindical Universitario</a></li>
<li><a href="https://www.argentina.gob.ar/noticias/el-ministerio-de-capital-humano-recibio-los-representantes-de-las-federaciones-gremiales" rel="noopener" target="_blank">Ministerio de Capital Humano · propuesta paritaria del 1.º de setiembre</a></li>
<li><a href="https://www.argentina.gob.ar/normativa/nacional/ley-27795-419006" rel="noopener" target="_blank">Argentina.gob.ar · Ley 27.795 de Financiamiento Universitario</a></li>
<li><a href="https://noticiasargentinas.com/politica/judiciales/reves-para-el-gobierno--la-justicia-acepto-una-cautelar-de-la-uba-por-la-ley-de-financiamiento-universitario_a6a972c581e20ad033b413280" rel="noopener" target="_blank">Noticias Argentinas · cautelar a favor de la UBA</a></li>
<li><a href="https://www.uba.ar/ubanoticias/noticias/1124" rel="noopener" target="_blank">Universidad de Buenos Aires · Marcha Federal del 12 de mayo y fotografía de archivo</a></li>
</ul></aside></article></main>
<footer class="site-footer"><div class="wrapper footer-grid"><div class="footer-brand"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"><p>Noticias políticas, memoria y fotografía desde Uruguay con una mirada popular y latinoamericana.</p></div><div class="footer-column"><h2>Secciones</h2><ul><li><a href="../noticias.html">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia de las izquierdas</a></li><li><a href="../fotografos.html">Nuestros fotógrafos</a></li></ul></div><div class="footer-column"><h2>Seguinos</h2><ul><li><a href="https://www.instagram.com/archivopopular/" rel="me noopener" target="_blank">Instagram</a></li><li><a href="https://www.facebook.com/profile.php?id=61560610077791" rel="noopener" target="_blank">Facebook</a></li><li><a href="https://www.tiktok.com/@archivopopular" rel="noopener" target="_blank">TikTok</a></li></ul></div></div><div class="wrapper footer-bottom"><span>Archivo Popular © <span data-current-year>2026</span></span><span>Montevideo, Uruguay</span></div></footer><script src="../site.js?v=20260828-1" defer></script>
</body></html>'''
Path(ARTICLE_REL).parent.mkdir(parents=True, exist_ok=True)
Path(ARTICLE_REL).write_text(article, encoding='utf-8')

p=Path('data/noticias.json')
news=json.loads(p.read_text(encoding='utf-8'))
old_latest=news[0] if news else None
news=[n for n in news if n.get('id') != ID]
new_item={'id':ID,'title':TITLE,'summary':SUMMARY,'category':CATEGORY,'date':DATE_ISO,'dateDisplay':DATE_DISPLAY,'place':PLACE,'image':NEWS_IMG_REL,'imageAlt':ALT,'photoCredit':CREDIT,'url':ARTICLE_REL}
news.insert(0,new_item)
p.write_text(json.dumps(news,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

idx=Path('index.html'); s=idx.read_text(encoding='utf-8')
s=re.sub(r'<meta property="og:image" content="[^"]+">', f'<meta property="og:image" content="https://archivopopular.github.io/{NEWS_IMG_REL}">', s, count=1)
lead=f'''<article class="lead-story" data-latest-story aria-live="polite">\n      <figure><img src="{NEWS_IMG_REL}" alt="{ALT}" width="1600"><figcaption class="photo-credit">Foto: {CREDIT}</figcaption></figure>\n      <div class="lead-copy"><p class="story-meta"><span>{DATE_DISPLAY}</span><span>{PLACE}</span></p><h1 id="ultima-noticia">{TITLE}</h1><p class="summary">{SUMMARY}</p><a class="story-link" href="{ARTICLE_REL}">Leer la noticia completa</a></div>\n    </article>'''
s=re.sub(r'<article class="lead-story" data-latest-story aria-live="polite">.*?</article>',lead,s,count=1,flags=re.S)
if old_latest and old_latest.get('url') and old_latest['url'] not in s.split('data-home-news-grid',1)[-1][:2500]:
    oldcard=f'''\n          <a class="news-card" href="{old_latest['url']}"><figure><img src="{old_latest['image']}" alt="{old_latest['imageAlt']}" width="658" height="425" loading="lazy"></figure><div class="news-card__body"><p class="eyebrow">{old_latest['category']}</p><h2>{old_latest['title']}</h2><p>{old_latest['summary']}</p><p class="story-meta"><span>{old_latest['dateDisplay']}</span><span>{old_latest['place']}</span></p></div></a>'''
    s=s.replace('<div class="news-grid" data-home-news-grid aria-live="polite">','<div class="news-grid" data-home-news-grid aria-live="polite">'+oldcard,1)
idx.write_text(s,encoding='utf-8')

np=Path('noticias.html'); ns=np.read_text(encoding='utf-8')
card=f'''\n          <a class="news-card" href="{ARTICLE_REL}"><figure><img src="{NEWS_IMG_REL}" alt="{ALT}" width="658" height="425" loading="lazy"></figure><div class="news-card__body"><p class="eyebrow">{CATEGORY}</p><h2>{TITLE}</h2><p>{SUMMARY}</p><p class="story-meta"><span>{DATE_DISPLAY}</span><span>{PLACE}</span></p></div></a>'''
if ARTICLE_REL not in ns:
    ns=ns.replace('<div class="news-grid" data-news-grid aria-live="polite">','<div class="news-grid" data-news-grid aria-live="polite">'+card,1)
np.write_text(ns,encoding='utf-8')

fp=Path('feed.xml'); fs=fp.read_text(encoding='utf-8')
fs=re.sub(r'<lastBuildDate>.*?</lastBuildDate>','<lastBuildDate>Tue, 08 Sep 2026 13:42:00 GMT</lastBuildDate>',fs,count=1)
item=f'''\n    <item><title>{TITLE}</title><link>{ARTICLE_URL}</link><guid>{ARTICLE_URL}</guid><pubDate>Tue, 08 Sep 2026 13:42:00 GMT</pubDate><description>{SUMMARY}</description></item>'''
if ARTICLE_URL not in fs:
    m=re.search(r'</lastBuildDate>',fs)
    if m: fs=fs[:m.end()]+item+fs[m.end():]
fp.write_text(fs,encoding='utf-8')

sp=Path('sitemap.xml'); ss=sp.read_text(encoding='utf-8')
ss=re.sub(r'(<loc>https://archivopopular.github.io/</loc>\s*<lastmod>)[^<]+',r'\g<1>2026-09-08',ss,count=1)
ss=re.sub(r'(<loc>https://archivopopular.github.io/noticias.html</loc>\s*<lastmod>)[^<]+',r'\g<1>2026-09-08',ss,count=1)
urlentry=f'''\n  <url><loc>{ARTICLE_URL}</loc><lastmod>2026-09-08</lastmod></url>'''
if ARTICLE_URL not in ss:
    ss=ss.replace('</urlset>',urlentry+'\n</urlset>',1)
sp.write_text(ss,encoding='utf-8')
subprocess.run(['node','scripts/generar-buscador.mjs'],check=True)
print('OK', ARTICLE_REL, SOCIAL_REL)
