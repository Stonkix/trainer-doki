"""Предзагрузка следующего шага тренажёра.

В <head> каждой страницы шага вставляется блок между маркерами
<!-- prefetch-next --> ... <!-- /prefetch-next -->:
  * <link rel="prefetch"> на HTML и картинку следующего шага (кнопка «вперёд» и
    все переходы из clickZones, если их несколько - предзагружаются все);
  * запасной вариант для браузеров без поддержки prefetch (Safari/iOS):
    после загрузки страницы картинка подгружается через new Image().

Блок идемпотентен: повторный запуск заменяет его, а не дублирует.
Обычные HTTP-запросы к уже существующим статическим файлам, серверной части нет.

Запуск для всех страниц ЭПД:
    py add_prefetch.py            # вставить/обновить
    py add_prefetch.py --remove   # убрать блок со всех страниц ЭПД
"""
import json
import os
import re
import sys

import png_to_webp as site

START, END = "<!-- prefetch-next -->", "<!-- /prefetch-next -->"
BLOCK_RE = re.compile(r"[ \t]*" + re.escape(START) + r".*?" + re.escape(END) + r"\r?\n?", re.S)
NAV_RE = re.compile(r"""window\.location\.href\s*=?\s*'\.?/?([\w\-.]+\.html)'""")
ZONES_RE = re.compile(r"const clickZones = (\[.*?\]);\r?\n")
IMG_RE = re.compile(r"""<img src="\./(images/[^"]+)" id="step-img\"""")
SKIP = {"index.html", "end.html", "end_mobile.html", "epd.html"}


def page_path(name):
    return os.path.join(site.SITE_DIR, name)


def next_pages(html):
    """Страницы, на которые можно уйти с этого шага, по порядку и без повторов."""
    found = list(NAV_RE.findall(html))
    m = ZONES_RE.search(html)
    if m:
        found += [z.get("action", "") for z in json.loads(m.group(1))]
    result = []
    for name in found:
        if name and name not in SKIP and name not in result and os.path.exists(page_path(name)):
            result.append(name)
    return result


def image_of(name):
    m = IMG_RE.search(site.read(page_path(name)))
    return m.group(1) if m else None


def build_block(targets):
    lines = [START]
    images = []
    for name in targets:
        lines.append(f'    <link rel="prefetch" href="./{name}">')
        img = image_of(name)
        if img:
            images.append(img)
            lines.append(f'    <link rel="prefetch" href="./{img}" as="image">')
    if images:
        arr = json.dumps(["./" + i for i in images])
        lines.append(
            "    <script>if(!document.createElement('link').relList.supports('prefetch')){"
            "addEventListener('load',function(){" + arr + ".forEach(function(s){new Image().src=s;});});}</script>"
        )
    lines.append("    " + END)
    return "\n".join(lines)


def process_page(name, remove=False):
    """Возвращает True, если файл изменён."""
    path = page_path(name)
    html = site.read(path)
    clean = BLOCK_RE.sub("", html)
    targets = [] if remove else next_pages(clean)
    if targets:
        nl = "\r\n" if "\r\n" in clean else "\n"
        block = build_block(targets).replace("\n", nl) + nl
        if "</head>" not in clean:
            return False
        new = clean.replace("</head>", block + "</head>", 1)
    else:
        new = clean
    if new == html:
        return False
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new)
    return True


def process_pages(names, remove=False):
    return sum(process_page(n, remove) for n in names)


if __name__ == "__main__":
    remove = "--remove" in sys.argv
    pages = [p for p in site.collect_pages() if p != site.ENTRY]
    changed = process_pages(pages, remove)
    print(f"Страниц ЭПД: {len(pages)}, изменено: {changed}" + (" (блок удалён)" if remove else ""))
