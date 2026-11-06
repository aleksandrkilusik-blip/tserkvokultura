# Церквокультура | Подкаст про віру, суспільство та культуру

Статичний сайт подкасту: чистий HTML + один CSS-файл, без фреймворків і збирачів. JS — кілька рядків у кінці `index.html` (поява блоків під час прокрутки й запуск відео після кліку).

```
404.html                сторінка «не знайдено»
scripts/update_episodes.py  оновлення випусків з YouTube (запускає .github/workflows/update-episodes.yml)
index.html              єдина сторінка: обкладинка, про подкаст, 3 картки, останні випуски
assets/css/style.css    усі стилі; кольори — CSS-змінні в :root
assets/img/hero.jpg     фото обкладинки (1920×1280)
assets/img/og-default.jpg  прев'ю для Telegram і соцмереж
assets/img/logo-wordmark.png  логотип-напис (білий, прозорий фон) — заголовок сторінки
assets/img/logo-icon.png      значок «О» (білий, прозорий фон) — у шапці
assets/img/favicon-64.png, apple-touch-icon.png  іконки вкладки й телефона
```

## Публікація на GitHub Pages

Settings → Pages → Build and deployment → Source: **Deploy from a branch** → гілка **main**, папка **/ (root)** → Save.
Сайт: `https://aleksandrkilusik-blip.github.io/tserkvokultura/`. Усі посилання відносні, тому підшлях `/tserkvokultura/` працює.

## Випуски оновлюються автоматично

Блок «Останні випуски» в `index.html` (між мітками `<!-- EPISODES:START -->` і `<!-- EPISODES:END -->`) заповнює скрипт `scripts/update_episodes.py`. **Вручну цей блок не редагуйте** — наступний запуск його перезапише.

- `.github/workflows/update-episodes.yml` запускає скрипт кожні 6 годин.
- Скрипт читає публічну RSS-стрічку каналу [@church_and_culture](https://www.youtube.com/@church_and_culture) (без API-ключа), пропускає Shorts і бере 3 найновіші відео: обкладинка, назва, дата.
- Якщо є зміни — бот комітить `index.html`, і GitHub Pages сам публікує сайт.
- Запустити одразу: вкладка **Actions** → «Оновити випуски з YouTube» → **Run workflow**.
- Налаштування — у workflow: `EPISODE_COUNT` (скільки випусків), `CHANNEL_ID` (UC…, якщо колись не вдасться визначити канал за назвою).
- GitHub вимикає розклад, якщо в репозиторії 60 днів немає активності. Тоді прийде лист — увімкніть workflow у вкладці Actions однією кнопкою.

Перевірити скрипт локально на збереженій стрічці: `python3 scripts/update_episodes.py --feed feed.xml`.

## Кеш браузера

Стилі підключені як `style.css?v=1`. Після змін у `assets/css/style.css` збільште номер (`?v=2` …), інакше браузери можуть показувати старий CSS.

## Перегляд локально

```
cd ..   # тека, де лежить tserkvokultura
python3 -m http.server 8000
# відкрийте http://localhost:8000/tserkvokultura/
```

Сайт перенесено зі сторінки `tserkvokultura.html` репозиторію `ukraine-for-christ`. Картка подкасту на сторінці «Ресурси» основного сайту веде сюди.
