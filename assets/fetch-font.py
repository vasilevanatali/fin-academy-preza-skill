#!/usr/bin/env python3
"""
Скачать шрифт с Google Fonts ЛОКАЛЬНО (woff2, латиница + кириллица) и подключить в деке.
Бесплатно, без ключей. Нужно, когда дизайн собирается ПО РЕФЕРЕНСУ: агент распознал
по картинке шрифтовую пару (заголовок + текст), а этот скрипт ставит шрифты локально,
чтобы PDF не мерцал (НЕ Google Fonts по сети).

  python3 fetch-font.py "Unbounded" --weights 400,700,800,900
  python3 fetch-font.py "Inter" --weights 400,500,600,700 --out-dir <деком>/fonts --css <деком>/fonts.css

По умолчанию кладёт в ./fonts и дописывает ./fonts.css. Дальше в theme.css поменять
font-family на скачанный шрифт. Для пары запустить дважды (заголовочный и текстовый).
"""
import sys, os, re, subprocess, urllib.parse

# современный UA — иначе Google отдаёт ttf вместо woff2
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def curl(url, binary=False, out=None):
    args = ["curl", "-s", "-A", UA, url]
    if out:
        args += ["-o", out]
        return subprocess.run(args, capture_output=True).returncode == 0
    return subprocess.run(args, capture_output=True, text=True).stdout


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("--"):
        sys.exit(__doc__)
    family = a[0]
    weights = (a[a.index("--weights") + 1] if "--weights" in a else "400,500,700,800").split(",")
    out_dir = a[a.index("--out-dir") + 1] if "--out-dir" in a else "fonts"
    css_path = a[a.index("--css") + 1] if "--css" in a else "fonts.css"
    os.makedirs(out_dir, exist_ok=True)

    fam_q = urllib.parse.quote(family)
    url = f"https://fonts.googleapis.com/css2?family={fam_q}:wght@{';'.join(weights)}&display=block"
    css = curl(url)
    if "@font-face" not in css:
        sys.exit(f"✗ Google Fonts не вернул '{family}'. Проверьте точное имя на fonts.google.com")

    # разобрать @font-face блоки: weight, style, url woff2, unicode-range
    blocks = re.findall(r"@font-face\s*\{(.*?)\}", css, re.S)
    out_css = []
    seen = set()
    n = 0
    slug = re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")
    for b in blocks:
        wt = re.search(r"font-weight:\s*(\d+)", b)
        st = re.search(r"font-style:\s*(\w+)", b)
        ur = re.search(r"unicode-range:\s*([^;]+);", b)
        src = re.search(r"url\(([^)]+\.woff2)\)", b)
        if not (wt and src):
            continue
        wt, st = wt.group(1), (st.group(1) if st else "normal")
        # берём только latin и cyrillic подмножества (по наличию кода в unicode-range)
        urng = ur.group(1) if ur else ""
        subset = "cyr" if "0400" in urng else ("lat" if "0000" in urng or "0100" in urng else None)
        if subset is None:
            continue
        key = (wt, st, subset)
        if key in seen:
            continue
        seen.add(key)
        fname = f"{slug}-{subset}-{wt}-{st}.woff2"
        if curl(src.group(1), out=os.path.join(out_dir, fname)):
            n += 1
            base = os.path.basename(out_dir.rstrip("/"))
            rel = f"{base}/{fname}" if base in ("fonts",) else f"fonts/{fname}"
            out_css.append(
                f"@font-face{{font-family:'{family}';font-style:{st};font-weight:{wt};"
                f"font-display:block;src:url('{rel}') format('woff2');"
                f"unicode-range:{urng.strip()};}}")

    if not n:
        sys.exit("✗ не удалось скачать ни одного woff2")
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(f"\n/* {family} (Google Fonts, локально) */\n" + "\n".join(out_css) + "\n")
    print(f"✓ {family}: скачано {n} начертаний в {out_dir}/, @font-face дописаны в {css_path}")
    print(f"  Теперь в theme.css: font-family: \"{family}\", sans-serif;")


if __name__ == "__main__":
    main()
