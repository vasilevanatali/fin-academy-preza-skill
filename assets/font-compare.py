#!/usr/bin/env python3
"""
Сравнить шрифты-кандидаты с референсом ГЛАЗАМИ, а не угадывать имя вслепую.
Распознать шрифт по картинке на 100% нельзя, поэтому процесс такой:
  1) назвать 3-5 похожих шрифтов с Google Fonts (по форме букв с референса);
  2) этот скрипт рисует их образцы в один лист одинаковым текстом;
  3) открыть лист рядом с референсом и выбрать совпадающий;
  4) поставить выбранный локально через fetch-font.py.

  python3 font-compare.py "Montserrat,Manrope,Unbounded,Onest" [--text "Свой образец"] [--out fonts-compare.png]

Бесплатно, без ключей (Google Fonts отдаёт ttf). Нужен Pillow: pip install pillow.
"""
import sys, os, re, subprocess, tempfile

# текст-образец: кириллица (заглавные+строчные) + латиница + цифры — видно характер букв
DEF_TITLE = "Финансовый Директор"
DEF_BODY = "Мастер CFO · 2026 · АаБбВвГгДд · AaBbCcGg · 0123456789"


def fetch_ttf(family):
    """Скачать у Google Fonts ttf для заголовка (жирный) и текста (обычный).
    Возвращает (title_ttf_path, body_ttf_path) или (None, None)."""
    fam = family.strip().replace(" ", "+")
    url = f"https://fonts.googleapis.com/css2?family={fam}:wght@400;500;700;800&display=swap"
    # БЕЗ современного UA — тогда Google отдаёт ttf (а не woff2), его читает Pillow
    css = subprocess.run(["curl", "-s", url], capture_output=True, text=True).stdout
    if "@font-face" not in css:
        return None, None
    faces = []  # (weight:int, is_cyr:bool, url)
    for blk in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
        wt = re.search(r"font-weight:\s*(\d+)", blk)
        ur = re.search(r"unicode-range:\s*([^;]+);", blk)
        src = re.search(r"url\((https://[^)]+\.ttf)\)", blk)
        if not (wt and src):
            continue
        is_cyr = bool(ur and "0400" in ur.group(1))
        faces.append((int(wt.group(1)), is_cyr, src.group(1)))
    if not faces:
        return None, None
    # предпочитаем кириллические начертания (для русского образца); иначе латиница
    cyr = [f for f in faces if f[1]]
    use = cyr or faces
    title = max(use, key=lambda f: f[0])      # самый жирный — на заголовок
    body = min(use, key=lambda f: abs(f[0] - 400))  # ближе к 400 — на текст
    paths = []
    for tag, face in (("title", title), ("body", body)):
        fd, p = tempfile.mkstemp(suffix=f"-{tag}.ttf")
        os.close(fd)
        rc = subprocess.run(["curl", "-s", face[2], "-o", p], capture_output=True).returncode
        paths.append(p if rc == 0 and os.path.getsize(p) > 2000 else None)
    return paths[0], paths[1]


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("--"):
        sys.exit(__doc__)
    families = [f.strip() for f in re.split(r"[,;]", a[0]) if f.strip()]
    title_txt = a[a.index("--text") + 1] if "--text" in a else DEF_TITLE
    body_txt = a[a.index("--body") + 1] if "--body" in a else DEF_BODY
    out = a[a.index("--out") + 1] if "--out" in a else "fonts-compare.png"

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Нужен Pillow: pip install pillow")

    W, ROW, PAD = 1180, 196, 40
    H = 96 + ROW * len(families) + PAD
    img = Image.new("RGB", (W, H), "#f6f6f2")
    d = ImageDraw.Draw(img)

    def sysfont(size):
        for p in ("/System/Library/Fonts/Supplemental/Arial.ttf",
                  "/Library/Fonts/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"):
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        return ImageFont.load_default()

    d.text((PAD, 30), "Сравни каждую пару с РЕФЕРЕНСОМ и выбери совпадающую по форме букв",
           fill="#14140f", font=sysfont(26))
    d.line((PAD, 84, W - PAD, 84), fill="#d2d2c8", width=2)

    y = 96
    for fam in families:
        tp, bp = fetch_ttf(fam)
        d.text((PAD, y + 6), fam, fill="#8a8a80", font=sysfont(22))
        if tp:
            try:
                d.text((PAD, y + 40), title_txt, fill="#14140f", font=ImageFont.truetype(tp, 58))
                d.text((PAD, y + 120), body_txt, fill="#3a3a32",
                       font=ImageFont.truetype(bp or tp, 26))
            except Exception as e:
                d.text((PAD, y + 60), f"(ошибка рендера: {e})", fill="#b00", font=sysfont(20))
        else:
            d.text((PAD, y + 60), "(не удалось скачать — проверь имя на fonts.google.com)",
                   fill="#b00", font=sysfont(22))
        for p in (tp, bp):
            if p and os.path.exists(p):
                os.unlink(p)
        d.line((PAD, y + ROW - 16, W - PAD, y + ROW - 16), fill="#e2e2da", width=1)
        y += ROW

    img.save(out)
    print(f"✓ Лист сравнения: {out} ({len(families)} шрифтов)")
    print("  Открой его рядом с референсом, выбери совпадающую пару и поставь её:")
    print('  python3 fetch-font.py "<Заголовочный>" --weights 700,800')


if __name__ == "__main__":
    main()
