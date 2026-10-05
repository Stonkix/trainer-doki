"""Массовая конвертация PNG -> WebP (lossless, не шире 1920 px) для сценариев ЭПД
и правка ссылок в HTML.

Какие сценарии затрагиваются: все страницы, до которых можно дойти по ссылкам
от astraldocs/epd.html (1С, веб-кабинет, мобильное приложение), и только
картинки из images/, которые эти страницы реально используют.

Исходные PNG берутся из astraldocs/images/ или, если их там уже нет, из
png_originals/ (папка вне сайта). Сами PNG скрипт не удаляет и не меняет.
Повторный запуск безопасен.

Запуск:
    py png_to_webp.py --dry-run   # только показать, что будет сделано
    py png_to_webp.py             # сконвертировать (только новое/устаревшее) и поправить HTML
    py png_to_webp.py --force     # пересоздать все WebP
"""
import os
import re
import sys

from PIL import Image

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.join(ROOT_DIR, "astraldocs")
PNG_BACKUP_DIR = os.path.join(ROOT_DIR, "png_originals")
ENTRY = "epd.html"
MAX_WIDTH = 1920

LINK_RE = re.compile(
    r"""href\s*=\s*['"]\./?([\w\-.]+\.html)['"]"""
    r"""|"action":\s*"([\w\-.]+\.html)\""""
    r"""|location\.href\s*=\s*['"]\./?([\w\-.]+\.html)['"]"""
)
IMG_RE = re.compile(r"""images/[^'")\s]+\.(?:png|webp)""")


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def collect_pages():
    seen, queue = set(), [ENTRY]
    while queue:
        page = queue.pop()
        if page in seen or page == "index.html":
            continue
        path = os.path.join(SITE_DIR, page)
        if not os.path.exists(path):
            continue
        seen.add(page)
        for groups in LINK_RE.findall(read(path)):
            queue.extend(g for g in groups if g)
    return sorted(seen)


def save_webp(src, dst):
    im = Image.open(src)
    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", lossless=True, method=6)


def find_png(rel_png):
    for base in (SITE_DIR, os.path.join(ROOT_DIR, "png_originals")):
        path = os.path.join(base, os.path.relpath(rel_png, "images") if base != SITE_DIR else rel_png)
        if os.path.exists(path):
            return path
    return None


def main():
    dry = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    pages = collect_pages()

    page_images = {}
    for page in pages:
        found = {os.path.splitext(p)[0] for p in IMG_RE.findall(read(os.path.join(SITE_DIR, page)))}
        if found:
            page_images[page] = found
    images = sorted(set().union(*page_images.values()))

    old_total = new_total = 0
    for stem in images:  # stem вида images/t2_1c_1
        dst = os.path.join(SITE_DIR, stem + ".webp")
        src = find_png(stem + ".png")
        if src and (force or not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src)):
            if not dry:
                save_webp(src, dst)
        elif not os.path.exists(dst):
            print(f"! нет ни PNG, ни WebP: {stem}")
            continue
        if src and os.path.exists(dst):
            old_total += os.path.getsize(src)
            new_total += os.path.getsize(dst)
            print(f"{stem}: {os.path.getsize(src) // 1024} KB -> {os.path.getsize(dst) // 1024} KB")

    changed = 0
    for page in page_images:
        path = os.path.join(SITE_DIR, page)
        text = read(path)
        new = IMG_RE.sub(lambda m: os.path.splitext(m.group(0))[0] + ".webp", text)
        if new != text:
            changed += 1
            if not dry:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(new)

    mb = 1024 * 1024
    print(f"\nСтраниц ЭПД: {len(pages)}, картинок: {len(images)}, HTML изменено: {changed}")
    if old_total:
        print(f"PNG {old_total / mb:.1f} MB -> WebP {new_total / mb:.1f} MB "
              f"({100 - new_total * 100 / old_total:.0f}% меньше)")
    if dry:
        print("(dry-run: ничего не записано)")


if __name__ == "__main__":
    main()
