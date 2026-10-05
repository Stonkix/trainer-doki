"""Сжатие шрифта TTF -> WOFF2 без изменения глифов (все символы и оси сохраняются).

Нужны пакеты: pip install fonttools brotli
Запуск: py ttf_to_woff2.py [путь/к/шрифту.ttf]
"""
import os
import sys

from fontTools.ttLib import TTFont

DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "astraldocs", "assets", "fonts", "Montserrat-VariableFont_wght.ttf")

src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
dst = os.path.splitext(src)[0] + ".woff2"
font = TTFont(src)
font.flavor = "woff2"
font.save(dst)
print(f"{os.path.basename(src)}: {os.path.getsize(src) // 1024} KB -> "
      f"{os.path.basename(dst)}: {os.path.getsize(dst) // 1024} KB")
