# Fin-Academy Preza

Скилл для **Claude Code** и **OpenAI Codex**: собирает презентации в фирменном тёмно-лаймовом
стиле онлайн-школы «Финансовый директор · Мастер CFO» **или по вашему референсу**.
Формат HTML+CSS → PDF 16:9. Бесплатно, без API-ключей.

## Два режима

- **Фирменный стиль школы** — тёмный фон + кислотный лайм, готовая библиотека 3D-иконок.
- **По референсу** — даёте картинку-образец (скрин слайда, мудборд, сайт, лого), и скилл берёт
  с неё палитру, фон, шрифт, стиль иконок и настроение. Не зациклен на одном стиле.

## Установка

Claude Code → `~/.claude/skills/`, Codex → `~/.agents/skills/`.
Полная пошаговая инструкция для обоих: **[INSTALL.md](INSTALL.md)**.

Коротко (Claude Code):

```bash
mkdir -p ~/.claude/skills && cd ~/.claude/skills
git clone https://github.com/vasilevanatali/fin-academy-preza-skill.git fin-academy-preza
pip3 install pillow numpy   # для генератора картинок
```

Перезапустить Claude Code. Дальше: «свёрстай презентацию про … в нашем стиле» или приложить
референс и сказать «собери в этом стиле».

## Бесплатный генератор картинок

3D-иконки генерятся через бесплатный **Pollinations.ai** (без ключей и регистрации). Скрипт
`gen-3d.py` рисует объект и сам убирает фон в прозрачность + запекает фирменное свечение.

```bash
python3 assets/gen-3d.py rocket
python3 assets/gen-3d.py chart --color "vibrant blue (#3B82F6)"
python3 assets/palette.py reference.png    # палитра из референса
```

## Что внутри

- `SKILL.md` — как агент собирает презу (оба режима).
- `references/design-system.md` — палитра, шрифты, сетка, типы слайдов.
- `references/slide-layout-rules.md` — чеклист вёрстки (что не обрезать, не оставлять пустым, выравнивание, как избегать мерцания PDF).
- `assets/theme.css`, `fonts/`, `bg-*.webp` — тема, локальные шрифты, фоны.
- `assets/objects/` — библиотека 3D-иконок + `manifest.json` (подбор по смыслу слайда).
- `assets/gen-3d.py`, `palette.py`, `make-bg.py`, `make-pdf.sh` — генерация объектов, палитры, фонов и сборка PDF.

## Онлайн-школа «Финансовый директор · Мастер CFO»

Учим финансистов и финдиректоров работать с нейросетями.

- Телеграм-канал: **https://t.me/findir_pro**
- AI для финансистов: **https://t.me/ai_finansist**
- MAX: **https://max.ru/findir_pro**
- Сайт: **https://fin-academy.pro**

## Лицензия

Код — MIT, используйте свободно. Шрифт Montserrat — OFL.
