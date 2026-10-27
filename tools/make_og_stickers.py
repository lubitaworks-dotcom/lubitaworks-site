"""LINEスタンプ用のOGP画像（1200x630）を作る。使い方: python tools/make_og_stickers.py
原本のスタンプ画像は環境変数 LUBITA_STICKER_ROOT（既定は休憩室の 図鑑/書き出し）。"""
import io
import os
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("LUBITA_STICKER_ROOT", r"c:\Users\tashi\OneDrive\Desktop\LUBITA WORKS\休憩室\LINEスタンプ試作\図鑑\書き出し"))
PAPER, INK, TEAL, SHADOW, AMBER = (245, 246, 241), (28, 36, 34), (14, 124, 116), (60, 199, 183), (138, 95, 20)


def font(name, size):
    f = TTFont(ROOT / "assets/fonts" / name)
    f.flavor = None
    b = io.BytesIO(); f.save(b); b.seek(0)
    return ImageFont.truetype(b, size)


def card(im, x, y, size, d, canvas):
    d.rectangle([x + 10, y + 10, x + size + 10, y + size + 10], fill=SHADOW)
    d.rectangle([x, y, x + size, y + size], fill=PAPER, outline=TEAL, width=4)
    a = im.resize((size - 8, size - 8), Image.LANCZOS)
    canvas.paste(a, (x + 4, y + 4), a)


def main():
    c = Image.new("RGB", (1200, 630), PAPER)
    d = ImageDraw.Draw(c)
    for gx in range(0, 1200, 24):
        d.line([gx, 0, gx, 630], fill=(236, 240, 235))
    for gy in range(0, 630, 24):
        d.line([0, gy, 1200, gy], fill=(236, 240, 235))
    d.text((64, 56), "LUBITA WORKS_", font=font("ArchivoBlack.woff2", 34), fill=INK)
    d.text((64, 200), "LINEスタンプ", font=font("ZenKakuGothicNew-900.woff2", 84), fill=INK)
    d.text((64, 320), "ルビタ図鑑のモンスターが", font=font("ZenKakuGothicNew-700.woff2", 34), fill=INK)
    d.text((64, 368), "ドット絵のスタンプになったよ", font=font("ZenKakuGothicNew-700.woff2", 34), fill=INK)
    d.text((64, 470), "各16個  ¥190", font=font("DotGothic16.woff2", 36), fill=AMBER)
    for (folder, x, y) in [("ヒツジ", 700, 80), ("ヤドカリ", 880, 300)]:
        im = Image.open(SRC / folder / "main.png").convert("RGBA")
        card(im, x, y, 230, d, c)
    out = ROOT / "assets/img/og-stickers.png"
    c.save(out, optimize=True)
    print(out, out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
