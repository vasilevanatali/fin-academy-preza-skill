#!/usr/bin/env python3
"""
Анализ референса дизайна -> ПОЛНАЯ палитра для презентации (под светлую и тёмную тему).
Подаёшь картинку-референс (скрин чужого слайда, мудборд, лого, сайт), получаешь готовый
блок :root ЦЕЛИКОМ: фон, текст, 2 акцента, карточки, границы, подложки. Для СВЕТЛОГО
референса всё пересчитывается автоматически (белые карточки, видимые границы, тёмная
подложка отключается, текст тёмный) — руками править не нужно.

  python3 palette.py reference.png
  python3 palette.py reference.jpg --colors 8

Дальше: вставить выданный :root ЦЕЛИКОМ в theme.css, перепечь фон под акценты
(make-bg.py "#АКЦЕНТ" "#ВТОРОЙ"), иконки в стиле/цвете референса (references/icon-styles.md).
"""
import sys, colorsys
from collections import Counter


def load(path, side=240):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((side, side))
    return im


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def sat(c):
    h, s, v = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return s


def hx(c):
    return "#%02X%02X%02X" % tuple(int(v) for v in c)


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def clusters(im, n):
    """Кластеры цветов (median cut) с долей площади: [((r,g,b), frac), ...] по убыванию доли.
    Median cut даёт перцептивно ровные группы — устойчивее к шуму/градиентам, чем счёт точных пикселей."""
    q = im.quantize(colors=n, method=0)  # 0 = MEDIANCUT
    pal = q.getpalette()
    cl = [((pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2]), cnt) for cnt, i in q.getcolors(256)]
    total = sum(cnt for _, cnt in cl) or 1
    cl.sort(key=lambda t: -t[1])
    return q, [(c, cnt / total) for c, cnt in cl]


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("--"):
        sys.exit(__doc__)
    path = a[0]
    ncol = int(a[a.index("--colors") + 1]) if "--colors" in a else 6
    im = load(path)
    q, cl = clusters(im, 16)
    qrgb = q.convert("RGB")

    # фон = доминирующий КЛАСТЕР по краям (рамка 12%) — устойчиво к шуму и градиенту
    w, h = im.size
    m = max(2, int(min(w, h) * 0.12))
    edge = Counter()
    for y in range(h):
        for x in range(w):
            if x < m or x >= w - m or y < m or y >= h - m:
                edge[qrgb.getpixel((x, y))] += 1
    edge_total = sum(edge.values()) or 1
    edge_share = {col: cnt / edge_total for col, cnt in edge.items()}
    # фон = крупнейший по площади кластер, который заметен на краях (объединяем оба сигнала,
    # иначе угловое свечение/виньетка на краю подменяет базовый фон)
    bg = next((col for col, _ in cl if edge_share.get(col, 0) > 0.10), cl[0][0])
    dark = lum(bg) < 128
    text = (245, 245, 245) if dark else (20, 22, 25)

    # акценты = насыщенные кластеры, далёкие от фона, с НЕмизерной площадью (отсекаем шум).
    # score = насыщенность × вес площади (^0.25): яркость главная, но случайный пиксель не пройдёт.
    cand = []
    for col, frac in cl:
        if frac < 0.012 or not (dist(col, bg) > 90 and sat(col) > 0.25):
            continue
        cand.append((sat(col) * (frac ** 0.25), col))
    cand.sort(key=lambda t: -t[0])
    picks = [c for _, c in cand]
    a1 = picks[0] if picks else (163, 221, 69)
    a2 = next((c for c in picks[1:] if dist(c, a1) > 80), None)
    if a2 is None:  # вторая заметная не нашлась — берём фирменную пару, отличную от a1
        a2 = (100, 254, 190) if dist((100, 254, 190), a1) > 80 else (163, 221, 69)

    print(f"Референс: {path}")
    print(f"Фон: {hx(bg)}  ({'тёмный' if dark else 'светлый'})")
    print(f"Текст: {hx(text)}")
    print(f"Акцент 1: {hx(a1)}")
    print(f"Акцент 2: {hx(a2)}")
    print("Топ палитры:", "  ".join(hx(c) for c, _ in cl[:ncol]))
    print()
    # полный набор переменных под тему — для светлого референса всё пересчитывается
    # автоматически (карточки светлые, границы видимые, тёмная подложка отключается)
    shift = lambda c, d: tuple(min(255, max(0, v + d)) for v in c)
    bg2 = shift(bg, 12 if dark else -10)
    card = shift(bg, 11) if dark else (255, 255, 255)
    hair = shift(bg, 26) if dark else shift(bg, -32)
    ink = (255, 255, 255) if lum(a1) < 140 else (10, 12, 9)  # текст на акцентной плашке
    muted = (185, 194, 181) if dark else (107, 107, 96)
    corner = 'url("bg-corner.webp")' if dark else "none"
    center = 'url("bg-center.webp")' if dark else "none"

    print(f"--- вставить ЦЕЛИКОМ в :root theme.css ({'тёмная' if dark else 'СВЕТЛАЯ'} тема) ---")
    print(f"  --bg: {hx(bg)};")
    print(f"  --bg-2: {hx(bg2)};")
    print(f"  --lime: {hx(a1)};   /* главный акцент с референса */")
    print(f"  --teal: {hx(a2)};   /* второй акцент */")
    print(f"  --white: {hx(text)};   /* основной текст ({'светлый' if dark else 'тёмный'}) */")
    print(f"  --ink: {hx(ink)};   /* текст на акцентной плашке/кнопке */")
    print(f"  --muted: {hx(muted)};")
    print(f"  --card-dark: {hx(card)};   /* карточка */")
    print(f"  --hair: {hx(hair)};   /* граница */")
    print(f"  --bg-corner: {corner};")
    print(f"  --bg-center: {center};")
    if not dark:
        print("  /* СВЕТЛАЯ тема: подложки отключены (none), карточки белые. В slide-templates")
        print("     тёмные плашки-выводы (#171d0e и т.п.) заменить на светлые контрастные. */")
    print()
    print("Дальше:")
    print(f'  python3 make-bg.py "{hx(a1)}" "{hx(a2)}"        # перепечь фон-свечение под цвет')
    print(f'  python3 gen-3d.py <concept> --color "({hx(a1)})"  # иконки в цвете референса')
    print("Шрифт/настроение/стиль иконок с референса оценить глазами (см. SKILL.md, раздел про референс).")


if __name__ == "__main__":
    main()
