# Эталонная коллекция стилей иконок для презентаций

Палитра трендовых стилей иконок 2026 — чтобы скилл не был заперт в одном «3D-глянец-лайм», а мог
собрать иконографику в стиле любого референса. Для каждого стиля: вид, настроение, когда брать,
**промпт-рецепт** для `gen-3d.py --prompt`, как распознать стиль на референсе, и визуальный эталон
в `assets/objects/styles/`.

## Как пользоваться (режим «по референсу»)

1. Открыть референс и сверить иконки с эталонами ниже (`objects/styles/*.png`) — определить стиль.
2. Взять промпт-рецепт нужного стиля, подставить свой объект вместо `<объект>` и цвет под палитру:
   ```bash
   python3 gen-3d.py --prompt "<рецепт с вашим объектом>" --color "(#АКЦЕНТ)" --out objects/<имя>.png
   ```
   (`gen-3d.py` сам вырежет фон в прозрачность и запечёт свечение; для сырого образца — флаг `--raw`).
3. Стиль иконок держать ЕДИНЫМ во всём деке — не смешивать (clay + line на одном слайде = разнобой).

Все эталоны сгенерированы своим бесплатным генератором (Pollinations), без чужих файлов и лицензий.

---

## 1. 3D-глянец / multi-material (фирменный дефолт)

- **Вид:** объёмный глянцевый объект, стеклянно-жидкий материал, блики, объёмное свечение, премиум.
- **Настроение:** дорого, технологично, ярко. **Аудитория:** бизнес, AI, премиум-продукты.
- **Когда брать:** тёмный фон, продающие и технологичные деки (дефолт школы — на лайме).
- **Рецепт:** `trendy 3D glossy <объект> icon, glass-like liquid material, high-gloss, soft volumetric glow, specular highlights and reflections, isometric three-quarter angle, octane render, premium, isolated on solid black background`
- **Распознать:** сильные блики, отражения, объём, «мокрая» поверхность, свечение по контуру.
- **Эталон:** `objects/styles/glossy.png`

## 2. Soft 3D / Claymorphism (один из главных трендов 2026)

- **Вид:** мягкий «пластилиновый» 3D, матовый, пухлые скруглённые формы, пастель, мягкий свет.
- **Настроение:** дружелюбно, тепло, игриво, доступно. **Аудитория:** обучение, массовый продукт, детское/новички.
- **Когда брать:** светлый/пастельный фон, дружелюбные деки, курсы для начинающих.
- **Рецепт:** `soft 3D clay <объект> icon, matte plasticine claymorphism, puffy rounded soft edges, pastel colors, soft studio lighting, cute, isolated on solid black background`
- **Распознать:** нет бликов-стекла, матовая «резиновая» поверхность, толстые скруглённые края, пастель.
- **Эталон:** `objects/styles/clay.png`

## 3. Glassmorphism (frosted glass)

- **Вид:** матовое полупрозрачное стекло, размытие, тонкая светлая граница, лёгкое преломление.
- **Настроение:** премиум, чисто, современно. **Аудитория:** финтех, продуктивность, финансы (релевантно школе).
- **Когда брать:** фон с лёгким градиентом/фото, премиальные финансовые деки.
- **Рецепт:** `glassmorphism <объект> icon, frosted translucent glass, soft blur, subtle light border, gentle refraction, premium fintech app style, on a soft gradient background`
- **Распознать:** сквозь объект просвечивает фон, матовое стекло, тонкая белая окантовка, блюр.
- **Эталон:** `objects/styles/glass.png`

## 4. Gradient / mesh (самый частый в app-иконках)

- **Вид:** сочный плавный градиент-меш, глянцевая заливка, насыщенные цвета.
- **Настроение:** энергично, современно, digital. **Аудитория:** SaaS, app, маркетинг.
- **Когда брать:** и тёмный, и светлый фон; динамичные продуктовые деки.
- **Рецепт:** `vibrant gradient <объект> icon, smooth mesh gradient fill, glossy, saturated colors, modern iOS app icon style, isolated on solid black background`
- **Распознать:** плавный переход двух-трёх ярких цветов внутри объекта, без сложного 3D-объёма.
- **Эталон:** `objects/styles/gradient.png`

## 5. Isometric (2.5D)

- **Вид:** изометрическая проекция, аккуратная векторная сцена, мягкие тени, «инфографика».
- **Настроение:** структурно, технично, аналитично. **Аудитория:** B2B, аналитика, процессы, схемы.
- **Когда брать:** деки про системы/процессы/архитектуру, инфографика.
- **Рецепт:** `isometric <объект> icon, 2.5D clean vector illustration, soft long shadows, tech infographic style, isolated on solid black background`
- **Распознать:** объект под углом ~30°, параллельные грани (не перспектива), плоские грани с лёгкой тенью.
- **Эталон:** `objects/styles/isometric.png`

## 6. Flat / hyper-minimal

- **Вид:** плоский, два-три цвета, простые геометрические формы, без объёма и градиента.
- **Настроение:** строго, чисто, корпоративно. **Аудитория:** корпоратив, госструктуры, строгий B2B.
- **Когда брать:** светлый/однотонный фон, минималистичные строгие деки.
- **Рецепт:** `flat minimal <объект> icon, two-tone, simple geometric shapes, no gradients, no shadows, modern corporate flat design, isolated on solid black background`
- **Распознать:** ровные заливки без объёма/теней, один-два цвета, геометрическая простота.
- **Эталон:** `objects/styles/flat.png`

## 7. Line / outline

- **Вид:** тонкие контурные линии, без заливки, минимум деталей.
- **Настроение:** лёгко, воздушно, премиально-сдержанно. **Аудитория:** премиум-минимализм, лонгриды, светлые деки.
- **Когда брать:** очень светлый фон, много текста, спокойные деки; как мелкие акценты.
- **Рецепт:** `thin line outline <объект> icon, single continuous stroke, minimalist lineart, even monochrome lines, no fill, isolated on solid black background`
- **Распознать:** только контур, одинаковая толщина линии, нет заливки и объёма.
- **Эталон:** `objects/styles/line.png`

## 8. Fluent 3D / sticker / emoji

- **Вид:** милый объёмный «стикер», глянцево-пухлый, мягкие скругления (как Microsoft Fluent / Apple emoji).
- **Настроение:** дружелюбно, неформально, эмоционально. **Аудитория:** обучение, чат-продукты, контент, соцсети.
- **Когда брать:** дружелюбные образовательные и контентные деки, эмодзи-настроение.
- **Рецепт:** `cute 3D sticker <объект> icon, Microsoft Fluent emoji style, glossy puffy, soft rounded, playful, vivid, isolated on solid black background`
- **Распознать:** «эмодзи-объём», очень скруглённые формы, лёгкий глянец, мультяшно-милый вид.
- **Эталон:** `objects/styles/fluent.png`

---

## Тренды (источники)

Подбор стилей сверен с обзорами иконографики 2026: soft 3D и claymorphism, glassmorphism для
finance/productivity, градиенты как самый частый подход, сосуществование isometric/flat/line,
Fluent-3D эмодзи для образовательных продуктов.

- Envato — Icon design trends 2026: https://elements.envato.com/learn/icon-design-trends
- IconikAI — App Icon Trends 2026: https://www.iconikai.com/blog/app-icon-design-trends-2026
- Medium (Arini A.) — 2026 Iconography strategic guide: https://medium.com/@ariniwrites/a-strategic-guide-to-2026-iconography-trends-how-to-choose-the-right-visual-style-for-your-73833baf2394
