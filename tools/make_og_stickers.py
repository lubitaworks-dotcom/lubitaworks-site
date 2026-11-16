"""LINEスタンプ用のOGP画像（1200x630）を作る。使い方: python tools/make_og_stickers.py [出力先]
2026-11-17〜: 「色で伝わる！丸顔の漢字一文字」シリーズをメインにした絵柄（3枚）。
原本のスタンプ画像は環境変数 LUBITA_KANJI_ROOT（既定は休憩室の 漢字スタンプ）。
動く版の画像は1コマ目を使う。"""
import io
import os
import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("LUBITA_KANJI_ROOT", r"c:\Users\tashi\OneDrive\Desktop\LUBITA WORKS\休憩室\LINEスタンプ試作\漢字スタンプ"))
PAPER, INK, TEAL, SHADOW, AMBER = (245, 246, 241), (28, 36, 34), (14, 124, 116), (60, 199, 183), (138, 95, 20)

# (素材の相対パス, カードの左上x, y)。左上から右下へ、少し重ねて並べる
CARDS = [
    ("申請用/静止画40/main.png", 640, 50),                    # 推（静止画のメイン）
    ("動く版/気持ち編/4_申請用/stickers/03.png", 790, 215),    # 草（気持ち編）
    ("動く版/日常編/4_申請用/stickers/main.png", 940, 380),    # 祝（返事・日常編のメイン）
]
CARD_SIZE = 200


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
    d.text((64, 320), "色で伝わる！丸顔の漢字一文字", font=font("ZenKakuGothicNew-700.woff2", 34), fill=INK)
    d.text((64, 368), "気分で体の色が変わるよ", font=font("ZenKakuGothicNew-700.woff2", 34), fill=INK)
    d.text((64, 470), "静止画 ¥190　動く ¥250", font=font("DotGothic16.woff2", 36), fill=AMBER)
    for (rel, x, y) in CARDS:
        im = Image.open(SRC / rel)
        im.seek(0)
        card(im.convert("RGBA"), x, y, CARD_SIZE, d, c)
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "assets/img/og-stickers.png"
    c.save(out, optimize=True)
    print(out, out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
