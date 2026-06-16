#!/usr/bin/env python3
"""
Авто-аудит дека: находит косяки вёрстки ДО сдачи, чтобы не ловить их глазами.
  python3 check.py <index.html>

Проверяет каждый слайд (1280x720):
- переполнение (контент вылезает за слайд),
- пустой низ (текст вверху, низ пустой — надо наполнить/центрировать),
- разъехавшиеся заголовки (строк больше задуманного — уменьшить кегль),
- битые/не загрузившиеся картинки,
- прозрачные слои (rgba/полупрозрачный градиент — риск мерцания PDF в Acrobat),
- наезд элементов за границу слайда.

Возвращает список проблемных слайдов. Код выхода != 0, если есть косяки
(удобно для цикла «починил → перепроверил» и для make-pdf.sh).

Нужен playwright: pip install playwright (использует системный Chrome, отдельный
браузер качать не обязательно).
"""
import sys, os

AUDIT_JS = r"""
(opts) => {
  const H = 720, out = [];
  const slides = [...document.querySelectorAll('.slide')];
  slides.forEach((s, i) => {
    const p = [];
    const center = s.classList.contains('slide--center') || s.classList.contains('slide--cover');
    if (s.scrollHeight - s.clientHeight > opts.overflow)
      p.push('переполнение +' + (s.scrollHeight - s.clientHeight) + 'px — контент вылезает за слайд');
    if (!center) {
      const kids = [...s.children];
      if (kids.length) {
        const top = s.getBoundingClientRect().top; let maxB = 0, minT = H;
        kids.forEach(k => { const r = k.getBoundingClientRect(); maxB = Math.max(maxB, r.bottom - top); minT = Math.min(minT, r.top - top); });
        const freeBottom = H - maxB, freeTop = minT;
        // косяк = низ заметно пустее верха (контент прижат вверх), а не центрированный с равными полями
        if (freeBottom > opts.freeBottom && freeBottom > freeTop * opts.freeRatio)
          p.push('низ пустой ~' + Math.round(freeBottom) + 'px при отступе сверху ' + Math.round(freeTop) + 'px — контент смещён вверх, центрировать или наполнить');
      }
    }
    s.querySelectorAll('h1.title, h2.title').forEach(h => {
      const lh = parseFloat(getComputedStyle(h).lineHeight) || 1;
      const lines = Math.round(h.getBoundingClientRect().height / lh);
      const br = (h.innerHTML.match(/<br/g) || []).length;
      if ((br > 0 && lines > br + 1) || (br === 0 && lines >= opts.headMaxLines))
        p.push('заголовок «' + h.textContent.trim().replace(/\s+/g, ' ').slice(0, 28) + '» на ' + lines + ' строк — разъехался, уменьшить кегль');
    });
    s.querySelectorAll('img').forEach(im => {
      if (im.complete && im.naturalWidth === 0) p.push('битая картинка: ' + im.getAttribute('src'));
    });
    let transp = 0;
    [s, ...s.querySelectorAll('.card, .mc, [style*=background], [style*=rgba]')].forEach(e => {
      const cs = getComputedStyle(e);
      if (/rgba\([^)]+,\s*0?\.\d+\s*\)/.test(cs.backgroundColor)) transp++;
      if (/gradient/.test(cs.backgroundImage) && /(rgba|transparent)/.test(cs.backgroundImage)) transp++;
    });
    if (transp > 0) p.push('прозрачные слои (' + transp + ') — риск мерцания PDF в Acrobat, сделать сплошными');
    if (p.length) out.push({ slide: i + 1, problems: p });
  });
  return { total: slides.length, issues: out };
}
"""


def main():
    import argparse
    ap = argparse.ArgumentParser(
        description="Авто-аудит вёрстки дека (слайды 1280x720). Код выхода !=0 при косяках.")
    ap.add_argument("path", help="index.html деком")
    ap.add_argument("--overflow", type=float, default=2,
                    help="порог переполнения за край, px (по умолч. 2)")
    ap.add_argument("--free-bottom", type=float, default=220, dest="free_bottom",
                    help="пустой низ от скольких px считать косяком (220)")
    ap.add_argument("--free-ratio", type=float, default=1.6, dest="free_ratio",
                    help="во сколько раз низ пустее верха = косяк, а не центровка (1.6)")
    ap.add_argument("--head-max-lines", type=int, default=4, dest="head_max_lines",
                    help="заголовок без <br> от скольких строк считать разъехавшимся (4)")
    ap.add_argument("--quiet", action="store_true", help="печатать только итоговую строку")
    args = ap.parse_args()

    path = os.path.abspath(args.path)
    if not os.path.exists(path):
        sys.exit("Файл не найден: " + path)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Нужен playwright: pip install playwright")
    opts = {"overflow": args.overflow, "freeBottom": args.free_bottom,
            "freeRatio": args.free_ratio, "headMaxLines": args.head_max_lines}
    with sync_playwright() as pw:
        try:
            b = pw.chromium.launch(channel="chrome", headless=True)
        except Exception:
            b = pw.chromium.launch(headless=True)  # fallback на встроенный chromium
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto("file://" + path, wait_until="networkidle")
        pg.wait_for_timeout(400)
        res = pg.evaluate(AUDIT_JS, opts)
        b.close()
    issues = res["issues"]
    print(f"Слайдов: {res['total']}, проблемных: {len(issues)}")
    if not issues:
        print("✓ Косяков не найдено.")
        return
    if not args.quiet:
        for it in issues:
            print(f"\nСлайд {it['slide']}:")
            for pr in it["problems"]:
                print("  •", pr)
    print(f"\nИтого {len(issues)} слайд(ов) с косяками — починить и прогнать check.py снова.")
    sys.exit(1)


if __name__ == "__main__":
    main()
