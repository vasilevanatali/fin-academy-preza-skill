# Установка скилла Fin-Academy Preza

Скилл собирает презентации в фирменном тёмно-лаймовом стиле школы «Финансовый директор · Мастер CFO»
или по вашему референсу — прямо в Claude Code или Codex. Бесплатно, без API-ключей.

Один и тот же скилл работает в обоих инструментах (общий формат Agent Skills, файл `SKILL.md`).
Отличается только папка, куда его положить.

---

## Что нужно один раз

- Установлен **Claude Code** или **OpenAI Codex**.
- **Python 3** и две библиотеки для генератора картинок:
  ```bash
  pip3 install pillow numpy
  ```
- Установлен **git** (обычно уже есть на Mac/Linux; на Windows — Git for Windows).

---

## Claude Code

```bash
# 1. папка личных скиллов (создастся, если её нет)
mkdir -p ~/.claude/skills

# 2. скачать скилл
cd ~/.claude/skills
git clone https://github.com/vasilevanatali/fin-academy-preza-skill.git fin-academy-preza

# 3. проверить, что файл на месте
ls ~/.claude/skills/fin-academy-preza/SKILL.md
```

Перезапустите Claude Code. Проверка: в чате спросите **«какие скиллы доступны?»** — в списке должен
быть `fin-academy-preza`. Или просто напишите «свёрстай презентацию про …» — скилл подхватится сам.

---

## OpenAI Codex

> Важно: у Codex личная папка скиллов — `~/.agents/skills/` (НЕ `~/.codex/`).

```bash
# 1. папка скиллов Codex
mkdir -p ~/.agents/skills

# 2. скачать тот же скилл
cd ~/.agents/skills
git clone https://github.com/vasilevanatali/fin-academy-preza-skill.git fin-academy-preza

# 3. проверить
ls ~/.agents/skills/fin-academy-preza/SKILL.md
```

Проверка: команда **`/skills`** в Codex (скилл в списке) или вызов **`$fin-academy-preza`**.

**Если уже поставили в Claude Code** — можно не клонировать второй раз, а сделать ссылку:

```bash
mkdir -p ~/.agents/skills
ln -s ~/.claude/skills/fin-academy-preza ~/.agents/skills/fin-academy-preza
```

---

## Как пользоваться

- **Преза в фирменном стиле:** «Сделай презентацию на 10 слайдов про бюджетирование в нашем стиле».
- **По референсу (любой стиль):** приложите картинку-образец (скрин чужого слайда, мудборд, сайт)
  и напишите «свёрстай презу в этом стиле» — скилл возьмёт палитру, фон, шрифт и настроение с неё.
- **Сгенерить иконку** (бесплатно, без ключа):
  ```bash
  python3 ~/.claude/skills/fin-academy-preza/assets/gen-3d.py rocket
  python3 ~/.claude/skills/fin-academy-preza/assets/gen-3d.py chart --color "vibrant blue (#3B82F6)"
  ```
- **Палитра из референса:**
  ```bash
  python3 ~/.claude/skills/fin-academy-preza/assets/palette.py референс.png
  ```

---

## Что внутри

| Файл                               | Зачем                                                                |
| ---------------------------------- | -------------------------------------------------------------------- |
| `SKILL.md`                         | как агент собирает презу, два режима (фирменный / по референсу)      |
| `references/design-system.md`      | палитра, шрифты, сетка, типы слайдов                                 |
| `references/slide-layout-rules.md` | чеклист вёрстки (что не обрезать, не оставлять пустым, выравнивание) |
| `assets/theme.css`                 | тема, палитра в `:root`                                              |
| `assets/slide-templates.html`      | готовые блоки слайдов                                                |
| `assets/gen-3d.py`                 | генератор 3D-объектов (бесплатный Pollinations.ai)                   |
| `assets/palette.py`                | анализ палитры из референса                                          |
| `assets/objects/`                  | библиотека готовых 3D-иконок                                         |
| `assets/fonts/`, `bg-*.webp`       | локальные шрифты и фоны (чтобы PDF не мерцал)                        |

Готовый дек собирается в HTML и печатается в PDF 16:9 через headless Chrome (`assets/make-pdf.sh`).

---

## Частые вопросы

- **Платно ли?** Нет. Картинки генерит бесплатный Pollinations.ai без регистрации и ключей.
- **Генератор не ответил с первого раза.** Это публичный бесплатный сервис, бывает занят — повторите
  команду (можно добавить `--seed 12`).
- **Нет Pillow/numpy.** `pip3 install pillow numpy`.
- **Скилл не виден.** Проверьте, что `SKILL.md` лежит прямо в папке скилла, и перезапустите инструмент.
