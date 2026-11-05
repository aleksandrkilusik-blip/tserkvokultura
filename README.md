# Церквокультура | Подкаст про віру, суспільство та культуру

Статичний сайт подкасту: чистий HTML + один CSS-файл, без фреймворків і збирачів. JS — кілька рядків у кінці `index.html` (поява блоків під час прокрутки й запуск відео після кліку).

```
index.html              єдина сторінка: обкладинка, про подкаст, 3 картки, останні випуски
assets/css/style.css    усі стилі; кольори — CSS-змінні в :root
assets/img/hero.jpg     фото обкладинки (1920×1280)
assets/img/og-default.jpg  прев'ю для Telegram і соцмереж
assets/img/favicon.svg  іконка вкладки
```

## Публікація на GitHub Pages

Settings → Pages → Build and deployment → Source: **Deploy from a branch** → гілка **main**, папка **/ (root)** → Save.
Сайт: `https://aleksandrkilusik-blip.github.io/tserkvokultura/`. Усі посилання відносні, тому підшлях `/tserkvokultura/` працює.

## Як додати новий випуск

Випуски лежать у `<div class="episodes">` у `index.html`, **новіші зверху**.

1. Скопіюйте перший блок `<div class="rv episode">…</div>` і вставте його першим.
2. Замініть ID відео (частина після `watch?v=` або `youtu.be/`) у двох місцях: `data-yt="…"` і `src="https://i.ytimg.com/vi/…/hqdefault.jpg"`.
3. Оновіть `data-yt-title` і `aria-label` — назва випуску.
4. На сторінці показуємо 3 останні випуски: найстаріший блок видаліть. Повний список — на YouTube-каналі.
5. Перерахуйте `style="--d:…"` по колонках: 0ms, 120ms, 240ms.

Під обкладинкою можна додати підпис (стилі вже є):

```html
<div>
  <p class="episode-meta">Випуск N · <time datetime="YYYY-MM-DD">D місяця YYYY</time></p>
  <p class="episode-title">Ім'я гостя: «Назва»</p>
  <p class="episode-note">1–2 речення про розмову.</p>
</div>
```

## Кеш браузера

Стилі підключені як `style.css?v=1`. Після змін у `assets/css/style.css` збільште номер (`?v=2` …), інакше браузери можуть показувати старий CSS.

## Перегляд локально

```
cd ..   # тека, де лежить tserkvokultura
python3 -m http.server 8000
# відкрийте http://localhost:8000/tserkvokultura/
```

Сайт перенесено зі сторінки `tserkvokultura.html` репозиторію `ukraine-for-christ`. Картка подкасту на сторінці «Ресурси» основного сайту веде сюди.
