#!/usr/bin/env bash
# Рендерит HTML-деком в PDF через headless Google Chrome.
# Использование:
#   ./make-pdf.sh [input.html] [output.pdf]
# По умолчанию: input=slide-templates.html, output=<input>.pdf
# Требует: python3 + Google Chrome (macOS).

set -e
cd "$(dirname "$0")"

IN="${1:-slide-templates.html}"
OUT="${2:-${IN%.html}.pdf}"
PORT="${PORT:-8769}"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -f "$CHROME" ] || { echo "✗ Google Chrome не найден в /Applications/"; exit 1; }
[ -f "$IN" ] || { echo "✗ Нет файла $IN"; exit 1; }

KILL=0
if ! lsof -ti:"$PORT" >/dev/null 2>&1; then
  python3 -m http.server "$PORT" >/dev/null 2>&1 &
  SPID=$!; KILL=1
  for i in 1 2 3 4 5 6; do curl -s "http://localhost:$PORT/$IN" >/dev/null 2>&1 && break; sleep 0.5; done
fi

echo "→ Рендерю $IN → $OUT…"
"$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --no-pdf-header-footer --print-to-pdf="$OUT" --virtual-time-budget=30000 \
  "http://localhost:$PORT/$IN" 2>/dev/null

[ "$KILL" = 1 ] && kill "$SPID" 2>/dev/null || true

if [ -f "$OUT" ]; then echo "✓ Готово: $OUT ($(du -h "$OUT" | awk '{print $1}'))"; else
  echo "✗ PDF не создался. Открой $IN в Chrome и ⌘P."; exit 1; fi
