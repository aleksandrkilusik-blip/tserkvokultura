#!/usr/bin/env python3
"""Оновлює блок «Останні випуски» в index.html з RSS-стрічки YouTube-каналу.

Запускається з GitHub Actions (.github/workflows/update-episodes.yml).
Лише стандартна бібліотека Python, без ключів і залежностей.

  python3 scripts/update_episodes.py            # оновити index.html
  python3 scripts/update_episodes.py --feed F   # взяти RSS із локального файлу (для перевірки)
"""
import argparse
import html
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

HANDLE = os.environ.get("CHANNEL_HANDLE", "church_and_culture")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")  # UC…; якщо порожньо — визначаємо за @handle
COUNT = int(os.environ.get("EPISODE_COUNT", "3"))
INDEX = os.path.join(os.path.dirname(__file__), "..", "index.html")
START = re.compile(r"(<!-- EPISODES:START[^>]*-->\n)(.*?)(<!-- EPISODES:END -->)", re.S)
UA = {"User-Agent": "Mozilla/5.0 (tserkvokultura site updater)", "Accept-Language": "uk,en;q=0.8"}
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}
MONTHS = ["січня", "лютого", "березня", "квітня", "травня", "червня",
          "липня", "серпня", "вересня", "жовтня", "листопада", "грудня"]


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def resolve_channel_id():
    if CHANNEL_ID:
        return CHANNEL_ID
    page = get(f"https://www.youtube.com/@{HANDLE}")
    m = re.search(r'"(?:externalId|channelId)":"(UC[\w-]{22})"', page) or \
        re.search(r'youtube\.com/channel/(UC[\w-]{22})', page)
    if not m:
        sys.exit(f"Не вдалося визначити channel_id для @{HANDLE}. Задайте CHANNEL_ID у workflow.")
    return m.group(1)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def is_short(video_id):
    """Shorts відкриваються за /shorts/ID (200); звичайне відео звідти перенаправляється (3xx)."""
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(f"https://www.youtube.com/shorts/{video_id}", headers=UA, method="HEAD")
    try:
        return opener.open(req, timeout=20).status == 200
    except urllib.error.HTTPError as e:
        return False  # 3xx (звичайне відео) або інша помилка
    except Exception:
        return False  # не змогли перевірити — краще показати, ніж загубити випуск


def parse(feed_xml):
    root = ET.fromstring(feed_xml)
    items = []
    for e in root.findall("a:entry", NS):
        vid = e.findtext("yt:videoId", namespaces=NS)
        title = (e.findtext("a:title", namespaces=NS) or "").strip()
        published = e.findtext("a:published", namespaces=NS) or ""
        if vid:
            items.append({"id": vid, "title": title, "date": published[:10]})
    items.sort(key=lambda x: x["date"], reverse=True)
    return items


def ua_date(iso):
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def render(items):
    out = []
    for i, it in enumerate(items):
        t = html.escape(it["title"], quote=True)
        out.append(
            f'      <div class="rv episode" style="--d:{(i % 3) * 120}ms">\n'
            f'        <button class="yt" type="button" data-yt="{it["id"]}" data-yt-title="{t}" aria-label="Відтворити випуск «{t}»">\n'
            f'          <img src="https://i.ytimg.com/vi/{it["id"]}/hqdefault.jpg" width="480" height="360" alt="" loading="lazy"><span class="play" aria-hidden="true"></span>\n'
            f'        </button>\n'
            f'        <div>\n'
            f'          <p class="episode-meta"><time datetime="{it["date"]}">{ua_date(it["date"])}</time></p>\n'
            f'          <p class="episode-title">{t}</p>\n'
            f'        </div>\n'
            f'      </div>\n')
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", help="локальний RSS-файл замість завантаження")
    ap.add_argument("--no-shorts-check", action="store_true")
    args = ap.parse_args()

    if args.feed:
        feed = open(args.feed, encoding="utf-8").read()
    else:
        cid = resolve_channel_id()
        print(f"channel_id: {cid}")
        feed = get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")

    picked = []
    for it in parse(feed):
        if not args.no_shorts_check and not args.feed and is_short(it["id"]):
            print(f"пропускаю Shorts: {it['id']} {it['title']}")
            continue
        picked.append(it)
        if len(picked) == COUNT:
            break
    if not picked:
        sys.exit("У стрічці немає відео — index.html не змінюю.")

    page = open(INDEX, encoding="utf-8").read()
    if not START.search(page):
        sys.exit("У index.html немає міток EPISODES:START / EPISODES:END.")
    new = START.sub(lambda m: m.group(1) + render(picked) + m.group(3), page, count=1)
    if new == page:
        print("Нових випусків немає.")
        return
    open(INDEX, "w", encoding="utf-8").write(new)
    for it in picked:
        print(f"{it['date']}  {it['id']}  {it['title']}")
    print("index.html оновлено.")


if __name__ == "__main__":
    main()
