from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, re, html, subprocess

root=Path('.')
slug='kast-milei-zurdos-mugrosos-golpe-chile-2026'
title='Kast evitó condenar a Milei tras llamar “zurdos mugrosos” a la izquierda y reivindicar el Chile posterior al golpe de 1973'
summary='El presidente chileno dijo que él no habría usado esa expresión, pero rechazó comentar o condenar las palabras de Javier Milei. Días antes, el mandatario argentino había insultado a la izquierda y elogiado el período que siguió al derrocamiento de Salvador Allende.'
category='América Latina · Memoria y extrema derecha'
date_iso='2026-09-07T15:48:00-03:00'
date_display='7 SEP 2026'
place='Santiago · Chile'
article_rel=f'noticias/{slug}.html'
image_rel='assets/news/kast-milei-presidencia-chile-2026.jpg'
social_rel='assets/social/archivo-popular-kast-milei-zurdos-golpe-2026-master.png'
url=f'https://archivopopular.github.io/{article_rel}'
photo_credit='Presidencia de la República de Chile · Archivo, 3 de septiembre de 2026'
image_alt='José Antonio Kast y Javier Milei se saludan durante la visita del presidente argentino al Palacio de La Moneda'

src=Image.open('/tmp/gallery/_dsc7150.jpg').convert('RGB')
out_img=root/image_rel
out_img.parent.mkdir(parents=True,exist_ok=True)
w=1600; h=round(src.height*w/src.width)
src.resize((w,h),Image.Resampling.LANCZOS).save(out_img,quality=92,optimize=True)

W,H,PH=2160,2700,1590
plate=Image.new('RGB',(W,H),'#F3F0E9')
scale=max(W/src.width, PH/src.height)
rs=src.resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.LANCZOS)
left=(rs.width-W)//2; top=max(0,(rs.height-PH)//2)
plate.paste(rs.crop((left,top,left+W,top+PH)),(0,0))
plate=plate.convert('RGBA')
shade=Image.new('RGBA',(W,520),(0,0,0,0)); px=shade.load()
for y in range(520):
    t=y/519
    a=int(255*0.70*(1-t/0.72)) if t<=0.72 else 0
    for x in range(W): px[x,y]=(0,0,0,a)
plate.alpha_composite(shade,(0,0))
logo=Image.open(root/'logo.png').convert('RGBA').resize((560,181),Image.Resampling.LANCZOS)
plate.alpha_composite(logo,(800,42))
d=ImageDraw.Draw(plate)
font_b='/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf'
credit_font=ImageFont.truetype(font_b,32)
head_font=ImageFont.truetype(font_b,150)
date_font=ImageFont.truetype(font_b,48)
loc_font=ImageFont.truetype(font_b,48)
label_font=ImageFont.truetype(font_b,58)
handle_font=ImageFont.truetype(font_b,62)

def draw_spaced(draw,xy,text,font,fill,spacing=0,anchor='ls'):
    x,y=xy
    if anchor=='rs':
        total=sum(draw.textlength(ch,font=font) for ch in text)+spacing*(len(text)-1)
        x-=total
    for ch in text:
        draw.text((x,y),ch,font=font,fill=fill,anchor='ls')
        x+=draw.textlength(ch,font=font)+spacing

credit='FOTO DE ARCHIVO: PRESIDENCIA DE LA REPÚBLICA DE CHILE'
credit_w=int(sum(d.textlength(ch,font=credit_font)+3 for ch in credit)-3)+68
credit_w=min(1920,max(540,credit_w))
d.rectangle((120,1510,120+credit_w,1590),fill='#FFFFFF')
draw_spaced(d,(154,1562),credit,credit_font,'#090909',3)
d.rectangle((0,1590,W,2576),fill='#090909')
d.rectangle((0,1590,W,1602),fill='#E30613')
lines=['MILEI LLAMÓ “ZURDOS','MUGROSOS” A LA','IZQUIERDA: KAST','EVITÓ CONDENARLO']
for line,y in zip(lines,[1782,1954,2126,2298]):
    draw_spaced(d,(120,y),line,head_font,'#FFFFFF',-2)
draw_spaced(d,(120,2510),'7 DE SETIEMBRE DE 2026',date_font,'#E30613',2.5)
draw_spaced(d,(2040,2510),'SANTIAGO · CHILE',loc_font,'#BEBAB2',2,anchor='rs')
d.rectangle((0,2576,W,2700),fill='#FFFFFF')
d.rectangle((0,2576,620,2700),fill='#E30613')
d.text((310,2657),'NOTICIA',font=label_font,fill='#FFFFFF',anchor='mm')
draw_spaced(d,(2040,2657),'@archivopopular',handle_font,'#090909',2,anchor='rs')
out_social=root/social_rel
out_social.parent.mkdir(parents=True,exist_ok=True)
plate.convert('RGB').save(out_social,quality=96)

article=f'''<!doctype html>
<html lang="es-UY">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#090909">
<meta name="description" content="{html.escape(summary,quote=True)}">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title,quote=True)}"><meta property="og:description" content="{html.escape(summary,quote=True)}"><meta property="og:image" content="https://archivopopular.github.io/{image_rel}">
<meta property="article:published_time" content="{date_iso}"><link rel="canonical" href="{url}"><link rel="stylesheet" href="../styles.css?v=20260828-1">
<title>{html.escape(title)} | Archivo Popular</title>
</head><body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>
<header class="site-header"><div class="wrapper topline"><span>Montevideo · Uruguay · Desde 2023</span><span>Noticias, memoria y fotografía</span></div><div class="wrapper brandbar"><a class="brand" href="../index.html" aria-label="Archivo Popular, inicio"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"></a><nav class="site-nav" aria-label="Navegación principal" data-open="false"><ul><li><a href="../index.html">Inicio</a></li><li><a href="../noticias.html" aria-current="page">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia</a></li><li><a href="../fotografos.html">Fotógrafos</a></li><li><a href="../index.html#nosotros">Nosotros</a></li></ul></nav><button class="menu-button" type="button" aria-label="Abrir menú" aria-expanded="false"><span></span><span></span><span></span></button></div></header>
<main id="contenido" class="page-main"><article class="wrapper article-shell"><header class="article-header"><p class="eyebrow">{category}</p><p class="story-meta"><span>7 DE SETIEMBRE DE 2026 · 15:48</span><span>{place}</span><span>Archivo Popular</span></p><h1>{title}</h1><p class="article-deck">{summary}</p></header>
<figure class="article-figure"><img src="../{image_rel}" alt="{image_alt}" width="1600" loading="eager"><figcaption>José Antonio Kast y Javier Milei durante la visita del mandatario argentino a La Moneda. Foto de archivo: Presidencia de la República de Chile · 3 de septiembre de 2026.</figcaption></figure>
<div class="article-body">
<p>El presidente de Chile, José Antonio Kast, evitó este lunes condenar las declaraciones que Javier Milei realizó días antes en el Foro Madrid de Santiago, donde el mandatario argentino llamó “zurdos mugrosos” a sectores de izquierda y reivindicó el período que siguió al derrocamiento de Salvador Allende en 1973.</p>
<p>Consultado en una entrevista con Radio ADN, Kast marcó una distancia limitada respecto del lenguaje utilizado por su aliado. Dijo que él “no lo habría dicho”, pero agregó que no iba a comentar las palabras de Milei. También sostuvo que no acostumbra pronunciarse sobre expresiones de otras personas en actos que considera privados, aunque el Foro Madrid tuvo presencia de prensa y participación pública de dirigentes internacionales.</p>
<p>Las palabras que originaron la polémica habían sido pronunciadas por Milei el 3 de septiembre, durante la apertura del V Encuentro Regional de Foro Madrid. Allí afirmó que el “mejor antídoto” contra los “zurdos mugrosos negadores de la realidad” eran los datos y presentó a Chile como un ejemplo de la llamada “batalla cultural” de la derecha.</p>
<p>En el mismo discurso, Milei se refirió a Salvador Allende como “el comunista Allende” y sostuvo que, tras su “derrocamiento”, Chile ingresó en un período de estabilidad y crecimiento que, según él, se extendió durante más de cuatro décadas. Esa formulación fue interpretada por partidos de izquierda chilenos como una reivindicación del golpe de Estado de 1973 y del período dictatorial que siguió.</p>
<p>El 11 de septiembre de 1973 las Fuerzas Armadas y de Orden de Chile, encabezadas por Augusto Pinochet, derrocaron al gobierno constitucional de Allende. El golpe abrió una dictadura que se extendió durante 17 años. El Instituto Nacional de Derechos Humanos de Chile recuerda que durante ese período se cometieron violaciones sistemáticas a los derechos humanos, incluidas ejecuciones, desapariciones forzadas y torturas.</p>
<p>El Partido Socialista de Chile fue uno de los sectores que reaccionó con mayor dureza. La formación sostuvo que no se trataba de una simple diferencia ideológica y cuestionó que un presidente extranjero utilizara insultos contra quienes piensan distinto y presentara positivamente el quiebre institucional de 1973. Otros dirigentes opositores también reclamaron una condena explícita del gobierno.</p>
<p>La primera respuesta del Ejecutivo chileno ya había evitado entrar en el fondo de las declaraciones. El ministro del Interior, Claudio Alvarado, señaló que el gobierno no se transformaría en “comentarista” de expresiones emitidas en un foro particular. La respuesta de Kast de este lunes mantuvo esa línea: reconoció que él no habría utilizado el insulto, pero rechazó emitir una condena política.</p>
<p>El episodio expone la cercanía política entre ambos presidentes y, al mismo tiempo, los límites que esa alianza impone a La Moneda cuando las intervenciones de Milei se proyectan sobre debates especialmente sensibles para la memoria democrática chilena. Kast y Milei mantuvieron una reunión de trabajo en el Palacio de La Moneda el mismo 3 de septiembre, en el marco de la visita del presidente argentino.</p>
<p>El Foro Madrid es una plataforma política vinculada a la Fundación Disenso, creada por el partido español Vox, y reúne a dirigentes y organizaciones de la derecha y la ultraderecha iberoamericana. En Santiago, Milei volvió a plantear una confrontación internacional contra la izquierda y Kast participó tanto de actividades del encuentro como de la agenda bilateral con Argentina.</p>
<p>La discusión no termina en el vocabulario utilizado. El punto más sensible es la lectura política del golpe de 1973 y de la dictadura posterior. Para los sectores que cuestionaron a Milei, presentar aquel período principalmente como una etapa de estabilidad económica omite el quiebre democrático y las violaciones de derechos humanos acreditadas por las instituciones chilenas. Kast, por ahora, eligió no entrar en esa controversia.</p>
</div>
<aside class="article-aside" aria-labelledby="fuentes"><h2 id="fuentes">Fuentes consultadas</h2><ul class="source-list">
<li><a href="https://elpais.com/chile/2026-09-07/kast-yo-no-habria-dicho-lo-de-zurdos-mugrosos-pero-no-voy-a-comentar-las-palabras-de-javier-milei.html" rel="noopener" target="_blank">El País Chile · respuesta de Kast del 7 de septiembre</a></li>
<li><a href="https://www.latercera.com/politica/noticia/milei-abre-foro-madrid-con-dura-critica-al-18-o-y-destaca-a-kast-chile-ha-vuelto-a-apostar-por-las-ideas-de-la-libertad/" rel="noopener" target="_blank">La Tercera · discurso de Milei en Foro Madrid</a></li>
<li><a href="https://www.emol.com/noticias/Nacional/2026/09/03/1210463/oposicion-dichos-milei-foro-madrid.html" rel="noopener" target="_blank">Emol · reacciones de la izquierda chilena</a></li>
<li><a href="https://ciudadano.indh.cl/11-de-septiembre/" rel="noopener" target="_blank">INDH Chile · golpe de Estado, dictadura y memoria</a></li>
<li><a href="https://prensa.presidencia.cl/fotografia.aspx?id=339732" rel="noopener" target="_blank">Presidencia de la República de Chile · fotografía oficial</a></li>
<li><a href="https://prensa.presidencia.cl/comunicado.aspx?id=339750" rel="noopener" target="_blank">Presidencia de Chile · participación de Kast en Foro Madrid</a></li>
</ul></aside></article></main>
<footer class="site-footer"><div class="wrapper footer-grid"><div class="footer-brand"><img src="../logo.png" alt="Archivo Popular" width="2269" height="713"><p>Noticias políticas, memoria y fotografía desde Uruguay con una mirada popular y latinoamericana.</p></div><div class="footer-column"><h2>Secciones</h2><ul><li><a href="../noticias.html">Noticias</a></li><li><a href="../personajes.html">Archivo político</a></li><li><a href="../historia.html">Historia de las izquierdas</a></li><li><a href="../fotografos.html">Nuestros fotógrafos</a></li></ul></div><div class="footer-column"><h2>Seguinos</h2><ul><li><a href="https://www.instagram.com/archivopopular/" rel="me noopener" target="_blank">Instagram</a></li><li><a href="https://www.facebook.com/profile.php?id=61560610077791" rel="noopener" target="_blank">Facebook</a></li><li><a href="https://www.tiktok.com/@archivopopular" rel="noopener" target="_blank">TikTok</a></li></ul></div></div><div class="wrapper footer-bottom"><span>Archivo Popular © <span data-current-year>2026</span></span><span>Montevideo, Uruguay</span></div></footer><script src="../site.js?v=20260828-1" defer></script>
</body></html>'''
article_path=root/article_rel
article_path.parent.mkdir(parents=True,exist_ok=True)
article_path.write_text(article,encoding='utf-8')

item={'id':slug,'title':title,'summary':summary,'category':category,'date':date_iso,'dateDisplay':date_display,'place':place,'image':image_rel,'imageAlt':image_alt,'photoCredit':photo_credit,'url':article_rel}
ndata=root/'data/noticias.json'
news=json.loads(ndata.read_text(encoding='utf-8'))
news=[n for n in news if n.get('id')!=slug]
news.insert(0,item)
ndata.write_text(json.dumps(news,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

idx=root/'index.html'; t=idx.read_text(encoding='utf-8')
t=re.sub(r'<meta property="og:image" content="[^"]+">',f'<meta property="og:image" content="https://archivopopular.github.io/{image_rel}">',t,count=1)
hero=f'''<article class="lead-story" data-latest-story aria-live="polite">
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
t=re.sub(r'<article class="lead-story" data-latest-story aria-live="polite">.*?</article>',hero,t,count=1,flags=re.S)
port_url='noticias/paro-puerto-tcp-estabilidad-esencialidad-2026.html'
m=re.search(r'<div class="news-grid" data-home-news-grid aria-live="polite">(.*?)</div>\s*</div>\s*</section>',t,re.S)
if m and port_url not in m.group(1):
    card='''\n          <a class="news-card" href="noticias/paro-puerto-tcp-estabilidad-esencialidad-2026.html"><figure><img src="assets/news/puerto-montevideo-presidencia-2024.jpg" alt="Terminal de contenedores del Puerto de Montevideo durante una recorrida oficial en 2024" width="658" height="425" loading="lazy"></figure><div class="news-card__body"><p class="eyebrow">Trabajo · Puerto de Montevideo</p><h2>Nuevo paro en el puerto: el sindicato reclama estabilidad y la oposición pide declarar la esencialidad</h2><p>TCP-Nelsury detuvo las actividades mientras reclama garantías de estabilidad laboral y jornales.</p><p class="story-meta"><span>7 SEP 2026</span><span>Puerto de Montevideo · Uruguay</span></p></div></a>'''
    t=t.replace('<div class="news-grid" data-home-news-grid aria-live="polite">','<div class="news-grid" data-home-news-grid aria-live="polite">'+card,1)
idx.write_text(t,encoding='utf-8')

np=root/'noticias.html'; nt=np.read_text(encoding='utf-8')
if article_rel not in nt:
    card=f'''\n          <a class="news-card" href="{article_rel}"><figure><img src="{image_rel}" alt="{image_alt}" width="658" height="425" loading="lazy"></figure><div class="news-card__body"><p class="eyebrow">{category}</p><h2>{title}</h2><p>{summary}</p><p class="story-meta"><span>{date_display}</span><span>{place}</span></p></div></a>'''
    nt=nt.replace('<div class="news-grid" data-news-grid aria-live="polite">','<div class="news-grid" data-news-grid aria-live="polite">'+card,1)
np.write_text(nt,encoding='utf-8')

fp=root/'feed.xml'; ft=fp.read_text(encoding='utf-8')
ft=re.sub(r'<lastBuildDate>.*?</lastBuildDate>','<lastBuildDate>Sun, 07 Sep 2026 18:48:00 GMT</lastBuildDate>',ft,count=1)
if url not in ft:
    feed_item=f'''\n    <item>\n      <title>{html.escape(title)}</title>\n      <link>{url}</link>\n      <guid>{url}</guid>\n      <pubDate>Sun, 07 Sep 2026 18:48:00 GMT</pubDate>\n      <description>{html.escape(summary)}</description>\n    </item>'''
    pos=ft.find('<item>')
    if pos!=-1: ft=ft[:pos]+feed_item+'\n    '+ft[pos:]
    else: ft=ft.replace('</channel>',feed_item+'\n  </channel>')
fp.write_text(ft,encoding='utf-8')

sp=root/'sitemap.xml'; st=sp.read_text(encoding='utf-8')
st=re.sub(r'(<loc>https://archivopopular.github.io/</loc>\s*<lastmod>)[^<]+',r'\g<1>2026-09-07',st,count=1)
st=re.sub(r'(<loc>https://archivopopular.github.io/noticias.html</loc>\s*<lastmod>)[^<]+',r'\g<1>2026-09-07',st,count=1)
if url not in st:
    st=st.replace('</urlset>',f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-09-07</lastmod>\n  </url>\n</urlset>')
sp.write_text(st,encoding='utf-8')

subprocess.run(['node','scripts/generar-buscador.mjs'],check=True)
print(article_rel)
print(image_rel)
print(social_rel)
