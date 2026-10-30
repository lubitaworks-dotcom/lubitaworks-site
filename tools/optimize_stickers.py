"""LINEスタンプの公開用画像を作る（原本は休憩室。リポジトリには縮小版だけ入れる）。
使い方: python tools/optimize_stickers.py
- main: 240×240のメイン画像 -> 240px webp
- sheet: 16枚を4×4に並べた一覧（paper色の地に載せる。ライト・ダークとも同じ見え方） -> 幅960px webp
原本の場所は環境変数 LUBITA_STICKER_ROOT（既定は休憩室の 図鑑/書き出し）。
"""
import json
import os
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(os.environ.get("LUBITA_STICKER_ROOT", r"c:\Users\tashi\OneDrive\Desktop\LUBITA WORKS\休憩室\LINEスタンプ試作\図鑑\書き出し"))
PAPER = (245, 246, 241)   # site.css の .card .art と同じ
CELL = (240, 208)


def build(slug, folder):
    out = ROOT / "assets/img/stickers"
    out.mkdir(parents=True, exist_ok=True)
    m = Image.open(SRC / folder / "main.png").convert("RGBA")
    base = Image.new("RGB", m.size, PAPER)   # メインは透過なので、paper色の地に載せる
    base.paste(m, (0, 0), m)
    base.save(out / f"{slug}-main.webp", quality=90)
    sheet = Image.new("RGB", (CELL[0] * 4, CELL[1] * 4), PAPER)
    for i in range(16):
        im = Image.open(SRC / folder / f"{i + 1:02d}.png").convert("RGBA")
        im = im.resize(CELL, Image.LANCZOS)
        sheet.paste(im, ((i % 4) * CELL[0], (i // 4) * CELL[1]), im)
    sheet.save(out / f"{slug}-sheet.webp", quality=88)
    print(slug, (out / f"{slug}-sheet.webp").stat().st_size // 1024, "KB")


def build_animated(slug, folder, count, export="5_提出用"):
    """動くスタンプ: 提出用の APNG。メインは動くwebp、一覧は各スタンプの1コマ目（正方形セル、4列）。"""
    from PIL import ImageSequence
    d = SRC.parent / folder / export
    out = ROOT / "assets/img/stickers"
    out.mkdir(parents=True, exist_ok=True)

    def on_paper(fr, size):
        fr = fr.convert("RGBA")
        k = min(size[0] / fr.width, size[1] / fr.height)   # 切り詰め版は横長・縦長があるので、縦横比を保って中央に置く
        fr = fr.resize((max(1, round(fr.width * k)), max(1, round(fr.height * k))), Image.LANCZOS)
        base = Image.new("RGB", size, PAPER)
        base.paste(fr, ((size[0] - fr.width) // 2, (size[1] - fr.height) // 2), fr)
        return base

    m = Image.open(d / "main.png")
    frames = [on_paper(f, (240, 240)) for f in ImageSequence.Iterator(m)]
    dur = m.info.get("duration", 100)
    frames[0].save(out / f"{slug}-main.webp", save_all=True, append_images=frames[1:], duration=dur, loop=0, quality=80)
    rows = (count + 3) // 4
    sheet = Image.new("RGB", (960, 240 * rows), PAPER)
    for i in range(count):
        im = Image.open(d / "stickers" / f"{i + 1:02d}.png")
        im.seek(0)
        sheet.paste(on_paper(im, (240, 240)), ((i % 4) * 240, (i // 4) * 240))
    sheet.save(out / f"{slug}-sheet.webp", quality=88)
    print(slug, (out / f"{slug}-main.webp").stat().st_size // 1024, "KB main,", (out / f"{slug}-sheet.webp").stat().st_size // 1024, "KB sheet")


if __name__ == "__main__":
    data = json.loads((ROOT / "tools/data/stickers.json").read_text(encoding="utf-8"))
    for s in data:
        if s.get("animated"):
            build_animated(s["slug"], s["folder"], s["count"], s.get("export", "5_提出用"))
        else:
            build(s["slug"], s["folder"])
