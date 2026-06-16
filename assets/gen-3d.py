#!/usr/bin/env python3
"""
Генератор фирменных 3D-объектов для презентаций.
Движок — БЕСПЛАТНЫЙ Pollinations.ai (Flux), без ключей и регистрации.

Использование:
  python3 gen-3d.py <concept> [--color "acid lime-green (#A8E84A)"] [--out path.png]
  python3 gen-3d.py --all            # сгенерить всю стартовую библиотеку в ./objects/
  python3 gen-3d.py --prompt "свой промпт" --out my.png

Объект генерится на чёрном фоне, постобработка убирает фон в прозрачность по яркости
и запекает фирменное свечение + тень. Никаких токенов и прокси не нужно — отдать команде
можно как есть.
"""
import sys, os, re, subprocess, tempfile, urllib.parse

DEFAULT_COLOR = "vibrant acid lime-green (#A8E84A)"

# Библиотека частых объектов: concept -> что рисуем
LIBRARY = {
    "exclamation": "exclamation mark",
    "question":    "question mark",
    "gift":        "gift box with a ribbon bow",
    "rocket":      "rocket / launch",
    "target":      "dartboard target with an arrow in the bullseye",
    "brain":       "human brain (AI / thinking)",
    "lightbulb":   "glowing light bulb (idea)",
    "chart":       "rising bar chart with an upward arrow",
    "trophy":      "winner trophy cup",
    "check":       "checkmark inside a circle",
    "cross":       "cross / X mark inside a circle",
    "magnet":      "horseshoe magnet (lead magnet)",
    "coins":       "stack of coins with a russian ruble sign",
    "robot":       "friendly robot head (AI assistant)",
    "document":    "document / file sheet with folded corner",
    "chat":        "rounded chat speech bubble",
}

# Объект на ЧИСТО ЧЁРНОМ фоне (его потом вырезаем по яркости в прозрачность)
STYLE = ("A single trendy 3D glossy {color} {thing} icon, studio product render, "
         "smooth glass-like material, soft volumetric neon glow, specular highlights and "
         "reflections, slight isometric three-quarter angle, modern premium 3D icon, clean, "
         "centered, isolated on a pure solid black background #000000, high detail, octane render style")

POLLINATIONS = "https://image.pollinations.ai/prompt/{p}?width=1024&height=1024&nologo=true&model=flux&seed={seed}"


def fetch(prompt, out, seed=7):
    """Скачать картинку с Pollinations (бесплатно, без ключа). True/False."""
    url = POLLINATIONS.format(p=urllib.parse.quote(prompt), seed=seed)
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    rc = subprocess.run(["curl", "-sL", url, "-o", out, "--max-time", "120"],
                        capture_output=True).returncode
    if rc != 0 or not os.path.exists(out) or os.path.getsize(out) < 2000:
        return False
    return True


def glow_from_color(color, default=(168, 232, 74)):
    """RGB свечения из строки --color (первый #RRGGBB). Нет hex -> лайм."""
    m = re.search(r'#([0-9a-fA-F]{6})', color or "")
    if not m:
        return default
    h = m.group(1)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def postprocess(path, maxside=720, glow=(168, 232, 74)):
    """Убрать чёрный фон в прозрачность по яркости, обрезать, ужать,
    ЗАПЕЧЬ свечение+тень в PNG (без CSS-фильтра -> PDF не растрируется)."""
    try:
        import numpy as np
        from PIL import Image, ImageFilter
        im = Image.open(path).convert("RGBA")
        arr = np.array(im).astype("float")
        lum = arr[:, :, :3].max(axis=2)
        # фон (lum < ~18) -> прозрачный, объект/свечение (> ~48) -> непрозрачный, плавно
        alpha = np.clip((lum - 18.0) / 30.0 * 255.0, 0, 255)
        arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)
        im = Image.fromarray(arr.astype("uint8"))
        bb = im.split()[3].getbbox()
        if bb:
            im = im.crop(bb)
        if max(im.size) > maxside:
            k = maxside / max(im.size)
            im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
        w, h = im.size
        pad = int(max(w, h) * 0.28)
        W, H = w + pad * 2, h + pad * 2
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        a = im.split()[3]
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        halo.paste(glow + (140,), (pad, pad), a)
        halo = halo.filter(ImageFilter.GaussianBlur(int(max(w, h) * 0.10)))
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 150), (pad + int(w * 0.02), pad + int(h * 0.06)), a)
        shadow = shadow.filter(ImageFilter.GaussianBlur(int(max(w, h) * 0.05)))
        canvas = Image.alpha_composite(canvas, shadow)
        canvas = Image.alpha_composite(canvas, halo)
        canvas.alpha_composite(im, (pad, pad))
        canvas.save(path, optimize=True)
    except Exception as e:
        print("  (постобработка пропущена:", e, "— объект остаётся на чёрном фоне)")


def generate(prompt, out, glow=(168, 232, 74), seed=7):
    if not fetch(prompt, out, seed):
        print("  ✗ Pollinations не ответил, попробуйте ещё раз (другой --seed)")
        return False
    postprocess(out, glow=glow)
    print("  ✓", out)
    return True


def main():
    a = sys.argv[1:]
    color = a[a.index("--color") + 1] if "--color" in a else DEFAULT_COLOR
    glow = glow_from_color(color)
    here = os.path.dirname(os.path.abspath(__file__))

    if "--all" in a:
        outdir = os.path.join(here, "objects")
        done = 0
        for i, (concept, thing) in enumerate(LIBRARY.items()):
            out = os.path.join(outdir, concept + ".png")
            if os.path.exists(out):
                print("  •", concept, "уже есть"); done += 1; continue
            print("→", concept)
            if generate(STYLE.format(color=color, thing=thing), out, glow, seed=7 + i):
                done += 1
        print(f"Готово: {done}/{len(LIBRARY)} объектов в {outdir}")
        return

    if "--prompt" in a:
        prompt = a[a.index("--prompt") + 1]
        out = a[a.index("--out") + 1] if "--out" in a else "object.png"
        generate(prompt, out, glow); return

    if not a or a[0].startswith("--"):
        sys.exit(__doc__)
    concept = a[0]
    thing = LIBRARY.get(concept, concept)
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(here, "objects", concept + ".png")
    generate(STYLE.format(color=color, thing=thing), out, glow)


if __name__ == "__main__":
    main()
