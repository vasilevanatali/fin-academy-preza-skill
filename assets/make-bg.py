#!/usr/bin/env python3
"""
Перебакать фоновые подложки под цвет референса.
Использование:
  python3 make-bg.py [accent_hex] [second_hex] [base_hex]
  по умолчанию: accent=#A8E84A (лайм), second=#64FEBE (бирюза), base=#0A0C09 (почти чёрный)
Создаёт bg-corner.webp и bg-center.webp рядом со скриптом.
Фон тёмный, со свечением в углу — текст остаётся читаемым.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter

W, H = 1280, 720


def hx(s, d):
    s = (s or "").lstrip("#")
    if len(s) != 6:
        return d
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def scaled(rgb, k):
    return tuple(max(0, min(255, int(c * k))) for c in rgb)


def bake(name, focal, second, lime, teal, base, strength=0.30):
    base_im = Image.new("RGB", (W, H), base)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    fx, fy = focal; r = 520
    g.ellipse([fx - r, fy - r, fx + r, fy + r], fill=lime)
    sx, sy = second; r2 = 430
    g.ellipse([sx - r2, sy - r2, sx + r2, sy + r2], fill=teal)
    glow = glow.filter(ImageFilter.GaussianBlur(165))
    out = Image.blend(base_im, Image.blend(base_im, glow, 1.0), strength)
    # контур-текстура (едва заметная)
    lines = Image.new("L", (W, H), 0); ld = ImageDraw.Draw(lines)
    for i in range(6, 40):
        rr = i * 36
        ld.ellipse([fx - rr, fy - rr * 0.72, fx + rr, fy + rr * 0.72], outline=16, width=2)
    lines = lines.filter(ImageFilter.GaussianBlur(0.7))
    tint = Image.new("RGB", (W, H), scaled(lime, 1.3))
    out = Image.composite(Image.blend(out, tint, 0.06), out, lines)
    # виньетка
    vin = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vin).ellipse([-180, -140, W + 180, H + 140], fill=255)
    vin = vin.filter(ImageFilter.GaussianBlur(150))
    out = Image.composite(out, Image.new("RGB", (W, H), scaled(base, 0.5)), vin)
    out.save(name, quality=86, method=6)
    print("  ✓", name)


def main():
    a = sys.argv[1:]
    accent = hx(a[0] if len(a) > 0 else "", (168, 232, 74))
    second = hx(a[1] if len(a) > 1 else "", (100, 254, 190))
    base = hx(a[2] if len(a) > 2 else "", (10, 12, 9))
    lime_glow = scaled(accent, 0.70)   # приглушаем, чтобы фон оставался тёмным
    teal_glow = scaled(second, 0.38)
    here = os.path.dirname(os.path.abspath(__file__))
    bake(os.path.join(here, "bg-corner.webp"), (W * 1.02, H * -0.05), (W * -0.05, H * 1.05),
         lime_glow, teal_glow, base)
    bake(os.path.join(here, "bg-center.webp"), (W * 0.5, H * 1.18), (W * 0.5, H * -0.18),
         lime_glow, teal_glow, base)
    print("Фоны перебачены под цвет:", accent, second)


if __name__ == "__main__":
    main()
