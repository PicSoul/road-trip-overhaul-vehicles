"""Draws the mod icon (mod/mod_icon.jpg, 276x162 - the size the game and the Workshop uploader require)
and the Steam Workshop preview image (assets/workshop_preview.jpg, 640x360).

    python tools/make_icon.py      (needs Pillow)
"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = r"C:\Windows\Fonts\bahnschrift.ttf"
ORANGE = (242, 140, 40)
WHITE = (240, 240, 236)


def font(size, style):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(style)
    return f


def draw(w, h, scale):
    s = scale * 4  # supersample for smooth edges
    W, H = w * s // scale, h * s // scale
    img = Image.new("RGB", (W, H))
    px = ImageDraw.Draw(img)
    # dusk sky fading into asphalt
    for y in range(H):
        t = y / H
        c = tuple(int(a + (b - a) * t) for a, b in zip((38, 44, 56), (14, 15, 18)))
        px.line([(0, y), (W, y)], fill=c)
    # road in perspective toward a vanishing point
    vx, vy = W * 0.5, H * 0.42
    px.polygon([(vx - W * 0.01, vy), (vx + W * 0.01, vy), (W * 0.98, H), (W * 0.02, H)], fill=(28, 29, 33))
    for side in (-1, 1):
        px.line([(vx + side * W * 0.01, vy), (W * 0.5 + side * W * 0.48, H)], fill=(200, 200, 190), width=max(2, s // 2))
    # centre dashes
    for i in range(7):
        a, b = (i / 7) ** 1.8, ((i + 0.5) / 7) ** 1.8
        y1, y2 = vy + (H - vy) * a, vy + (H - vy) * b
        hw1, hw2 = W * 0.004 * (1 + a * 3), W * 0.004 * (1 + b * 3)
        px.polygon([(vx - hw1, y1), (vx + hw1, y1), (vx + hw2, y2), (vx - hw2, y2)], fill=ORANGE)
    img = img.filter(ImageFilter.GaussianBlur(s * 0.6))
    # darken behind the text
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle([0, 0, W, int(H * 0.62)], fill=150)
    shade = shade.filter(ImageFilter.GaussianBlur(H * 0.08))
    img = Image.composite(Image.new("RGB", (W, H), (8, 9, 11)), img, shade)
    px = ImageDraw.Draw(img)

    def centred(text, f, y, fill):
        x0, y0, x1, y1 = px.textbbox((0, 0), text, font=f)
        px.text(((W - (x1 - x0)) / 2 - x0, y - y0), text, font=f, fill=fill)
        return y + (y1 - y0)

    y = centred("ROAD TRIP", font(int(H * 0.15), "Bold"), H * 0.07, WHITE)
    y = centred("OVERHAUL", font(int(H * 0.27), "Bold"), y + H * 0.035, ORANGE)
    # subtitle band
    band = font(int(H * 0.11), "SemiBold")
    x0, y0, x1, y1 = px.textbbox((0, 0), "VEHICLE TUNING", font=band)
    bw, bh, by = (x1 - x0) + W * 0.08, (y1 - y0) + H * 0.06, y + H * 0.06
    px.rectangle([(W - bw) / 2, by, (W + bw) / 2, by + bh], fill=ORANGE)
    centred("VEHICLE TUNING", band, by + H * 0.03, (20, 20, 22))
    return img.resize((w, h), Image.LANCZOS)


def main():
    os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)
    icon = os.path.join(HERE, "mod", "mod_icon.jpg")
    draw(276, 162, 1).save(icon, quality=92)
    draw(640, 360, 1).save(os.path.join(HERE, "assets", "workshop_preview.jpg"), quality=92)
    print("wrote", icon, "and assets/workshop_preview.jpg")


if __name__ == "__main__":
    main()
