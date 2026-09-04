from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
source = Path('/tmp/frigorifico-tacuarembo-subrayado.jpg')
news_img = root / 'assets/news/frigorifico-tacuarembo-conflicto-subrayado-2026.jpg'
social_img = root / 'assets/social/archivo-popular-frigorifico-tacuarembo-1300-seguro-paro-2026-master.png'
root_copy = root / 'archivo-popular-frigorifico-tacuarembo-1300-seguro-paro-2026-master.png'
news_img.parent.mkdir(parents=True, exist_ok=True)
social_img.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(source, news_img)

W, H = 2160, 2700
PHOTO_H = 1590
RED_H = 12
BLACK_TOP = PHOTO_H + RED_H
FOOTER_Y = 2576
RED = '#E30613'
BLACK = '#050505'
WHITE = '#FFFFFF'
GRAY = '#C8C5C2'

src = Image.open(source).convert('RGB')
scale = max(W / src.width, PHOTO_H / src.height)
resized = src.resize((round(src.width * scale), round(src.height * scale)), Image.Resampling.LANCZOS)
left = max(0, (resized.width - W) // 2)
top = max(0, (resized.height - PHOTO_H) // 2)
photo = resized.crop((left, top, left + W, top + PHOTO_H))

canvas = Image.new('RGBA', (W, H), (5, 5, 5, 255))
canvas.paste(photo.convert('RGBA'), (0, 0))

# Protección oscura suave detrás del logo.
overlay = Image.new('RGBA', (W, 350), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(350):
    alpha = int(105 * (1 - y / 350))
    od.line((0, y, W, y), fill=(0, 0, 0, alpha))
canvas.alpha_composite(overlay, (0, 0))

# Logo original de Archivo Popular.
logo = Image.open(root / 'logo.png').convert('RGBA')
target_w = 610
target_h = round(logo.height * target_w / logo.width)
logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
canvas.alpha_composite(logo, ((W - target_w) // 2, 42))

d = ImageDraw.Draw(canvas)
d.rectangle((0, PHOTO_H, W, PHOTO_H + RED_H - 1), fill=RED)
d.rectangle((0, BLACK_TOP, W, FOOTER_Y - 1), fill=BLACK)
d.rectangle((0, FOOTER_Y, W, H), fill=WHITE)
d.rectangle((0, FOOTER_Y, 620, H), fill=RED)

bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font_credit = ImageFont.truetype(bold, 34)
font_head = ImageFont.truetype(bold, 106)
font_meta = ImageFont.truetype(bold, 43)
font_footer = ImageFont.truetype(bold, 48)
font_handle = ImageFont.truetype(bold, 50)

credit = 'FOTO: SUBRAYADO'
cb = d.textbbox((0, 0), credit, font=font_credit)
cw = cb[2] - cb[0]
ch = cb[3] - cb[1]
cx, cy = 120, PHOTO_H - 78
d.rectangle((cx, cy, cx + cw + 42, PHOTO_H), fill=WHITE)
d.text((cx + 21, cy + (78 - ch) // 2 - cb[1]), credit, font=font_credit, fill='#111111')

headline = [
    '1.300 TRABAJADORES',
    'EN SEGURO DE PARO:',
    'FRIGORÍFICO TACUAREMBÓ',
    'PARALIZA SU ACTIVIDAD',
]
x, y = 120, 1715
for line in headline:
    d.text((x, y), line, font=font_head, fill=WHITE)
    box = d.textbbox((x, y), line, font=font_head)
    y = box[3] + 25

meta_y = 2470
date = '4 DE SETIEMBRE DE 2026'
place = 'TACUAREMBÓ · URUGUAY'
d.text((120, meta_y), date, font=font_meta, fill=RED)
pb = d.textbbox((0, 0), place, font=font_meta)
d.text((W - 120 - (pb[2] - pb[0]), meta_y), place, font=font_meta, fill=GRAY)

d.text((176, 2606), 'NOTICIA', font=font_footer, fill=WHITE)
handle = '@archivopopular'
hb = d.textbbox((0, 0), handle, font=font_handle)
d.text((W - 120 - (hb[2] - hb[0]), 2602), handle, font=font_handle, fill='#111111')

canvas.convert('RGB').save(social_img, 'PNG', optimize=True)
shutil.copy2(social_img, root_copy)
print(social_img)
print(news_img)
