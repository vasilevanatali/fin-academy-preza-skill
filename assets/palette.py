#!/usr/bin/env python3
"""
Анализ референса дизайна -> палитра для презентации.
Подаёшь картинку-референс (скрин чужого слайда, мудборд, лого, сайт), получаешь:
фон (тёмный/светлый), цвет текста, 2 акцента + готовый блок :root для theme.css.

  python3 palette.py reference.png
  python3 palette.py reference.jpg --colors 8

Дальше: подставить выданные --bg/--accent/--accent2 в :root theme.css, перепечь фон
(make-bg.py "#АКЦЕНТ" "#ВТОРОЙ") и генерить иконки в цвете акцента (gen-3d.py --color ...).
"""
import sys, colorsys
from collections import Counter


def load(path, side=240):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((side, side))
    return im


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.5882 * c[2]


def sat(c):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return s


def hx(c):
    return "#%02X%02X%02X" % c


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("--"):
        sys.exit(__doc__)
    path = a[0]
    ncol = int(a[a.index("--colors") + 1]) if "--colors" in a else 6
    im = load(path)
    px = list(im.getdata())

    # фон = доминирующий цвет по краям (рамка 10%)
    w, h = im.size
    edge = []
    m = max(2, int(min(w, h) * 0.10))
    for y in range(h):
        for x in range(w):
            if x < m or x > w - m or y < m or y > h - m:
                edge.append(im.getpixel((x, y)))
    bg = Counter(edge).most_common(1)[0][0]
    dark = lum(bg) < 128
    text = (245, 245, 245) if dark else (20, 22, 25)

    # палитра: квантование
    q = im.quantize(colors=12, method=2).convert("RGB")
    common = Counter(q.getdata()).most_common(12)
    # акценты = самые насыщенные и заметные, не похожие на фон
    def far_from_bg(c):
        return abs(c[0] - bg[0]) + abs(c[1] - bg[1]) + abs(c[2] - bg[2]) > 90
    accents = sorted([c for c, _ in common if sat(c) > 0.35 and far_from_bg(c)],
                     key=lambda c: -sat(c))
    if not accents:
        accents = [c for c, _ in common if far_from_bg(c)]
    a1 = accents[0] if accents else (163, 221, 69)
    a2 = next((c for c in accents[1:] if abs(c[0] - a1[0]) + abs(c[1] - a1[1]) + abs(c[2] - a1[2]) > 80), a1)

    print(f"Референс: {path}")
    print(f"Фон: {hx(bg)}  ({'тёмный' if dark else 'светлый'})")
    print(f"Текст: {hx(text)}")
    print(f"Акцент 1: {hx(a1)}")
    print(f"Акцент 2: {hx(a2)}")
    print("Вся палитра:", "  ".join(hx(c) for c, _ in common[:ncol]))
    print()
    print("--- вставить в :root theme.css ---")
    print(f"  --bg: {hx(bg)};")
    print(f"  --bg-2: {hx(tuple(min(255, v + (12 if dark else -12)) for v in bg))};")
    print(f"  --white: {hx(text)};")
    print(f"  --lime: {hx(a1)};   /* главный акцент с референса */")
    print(f"  --teal: {hx(a2)};   /* второй акцент */")
    print()
    print("Дальше:")
    print(f'  python3 make-bg.py "{hx(a1)}" "{hx(a2)}"        # перепечь фон-свечение под цвет')
    print(f'  python3 gen-3d.py <concept> --color "({hx(a1)})"  # иконки в цвете референса')
    print("Шрифт/настроение/стиль иконок с референса оценить глазами (см. SKILL.md, раздел про референс).")


if __name__ == "__main__":
    main()
