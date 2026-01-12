# ATLEAST GIVE CREDITS IF YOU STEALING :(((((((((((((((((((((((((((((((((((((
# ELSE NO FURTHER PUBLIC THUMBNAIL UPDATES

import random, logging, os, re, aiofiles, aiohttp, traceback
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from py_yt import VideosSearch

logging.basicConfig(level=logging.INFO)

def truncate_short(text, limit=18):
    text = text.upper()
    return text[:limit] + "…" if len(text) > limit else text

def nature_gradient(w, h):
    top = (90, 150, 130)
    bottom = (25, 70, 45)
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = int(top[0] + (bottom[0]-top[0]) * y/h)
        g = int(top[1] + (bottom[1]-top[1]) * y/h)
        b = int(top[2] + (bottom[2]-top[2]) * y/h)
        draw.line([(0,y),(w,y)], fill=(r,g,b))
    return img.convert("RGBA")

# 🎵 MUSIC SYMBOL (TOP CENTER)
def draw_music_symbol(img):
    draw = ImageDraw.Draw(img)
    cx = img.width // 2
    cy = 55

    # shadow
    draw.ellipse((cx-22, cy-22, cx+22, cy+22), fill=(0,0,0,120))
    draw.rectangle((cx+8, cy-28, cx+14, cy+10), fill=(0,0,0,120))

    # main circle
    draw.ellipse((cx-20, cy-20, cx+20, cy+20), fill=(245,245,245))
    draw.rectangle((cx+10, cy-26, cx+14, cy+6), fill=(245,245,245))
    draw.ellipse((cx+8, cy+6, cx+22, cy+18), fill=(245,245,245))

    return img

# ✨ BORDER COLOR GRADING
def add_premium_border(img):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    colors = [(90,200,160),(120,180,255),(160,120,255)]

    for i in range(4):
        c = colors[i % len(colors)]
        draw.rectangle((i, i, w-i-1, h-i-1), outline=c)

    return img

async def gen_thumb(videoid):
    try:
        out = f"cache/{videoid}_v9.png"
        if os.path.isfile(out):
            return out

        data = (await VideosSearch(f"https://youtube.com/watch?v={videoid}",1).next())["result"][0]
        title = truncate_short(re.sub("\W+"," ",data["title"]))
        duration = data.get("duration","Live")
        thumb = data["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as s:
            async with s.get(thumb) as r:
                raw = await r.read()

        raw_path = f"cache/{videoid}_raw.png"
        async with aiofiles.open(raw_path,"wb") as f:
            await f.write(raw)

        fg = Image.open(raw_path).convert("RGBA")
        fg.thumbnail((900,520), Image.LANCZOS)

        bg = nature_gradient(1280,720).filter(ImageFilter.GaussianBlur(8))

        # 🎵 top music symbol
        bg = draw_music_symbol(bg)

        draw = ImageDraw.Draw(bg)
        x = (1280 - fg.width)//2
        y = 95

        shadow = fg.copy().filter(ImageFilter.GaussianBlur(20))
        bg.paste(shadow,(x+12,y+12),shadow)
        bg.paste(fg,(x,y),fg)

        title_font = ImageFont.truetype("AviaxMusic/assets/font3.ttf", 44)
        text_w = draw.textlength(title, font=title_font)
        draw.text(((1280-text_w)//2+2, y+fg.height+27),
                  title, font=title_font, fill=(0,0,0))
        draw.text(((1280-text_w)//2, y+fg.height+25),
                  title, font=title_font, fill=(245,245,245))

        icon = Image.open("AviaxMusic/assets/play_icons.png").resize((70,70))
        bg.paste(icon,(x-90,y+fg.height+15),icon)
        bg.paste(icon,(x+fg.width+20,y+fg.height+15),icon)

        small = ImageFont.truetype("AviaxMusic/assets/font2.ttf", 26)
        draw.text((1050,660), duration, font=small, fill=(230,230,230))

        # ✨ premium border
        bg = add_premium_border(bg)

        os.remove(raw_path)
        bg.save(out, "PNG", quality=95)
        return out

    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        return None
