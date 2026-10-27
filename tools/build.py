"""静的サイトのビルド。使い方: python tools/build.py

1. pages_*.py が返すページを、リポジトリ直下（公開ルート）へ書き出す
2. 書き出したHTML・CSS・データに出てくる文字だけで、フォントをサブセット化して assets/fonts/*.woff2 に出力する
標準ライブラリ＋fonttools＋brotli（フォントのサブセット化のみ）。
"""
import importlib
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

# フォント原本（OFL。リポジトリには入れず、無ければ取得する）
FONT_SRC = Path(os.environ.get("LUBITA_FONT_SRC", r"C:\dev\fonts_src"))
GF = "https://raw.githubusercontent.com/google/fonts/main/ofl"
FONTS = {  # 出力名: (原本ファイル, 取得URL)
    "ArchivoBlack": ("ArchivoBlack-Regular.ttf", f"{GF}/archivoblack/ArchivoBlack-Regular.ttf"),
    "DotGothic16": ("DotGothic16-Regular.ttf", f"{GF}/dotgothic16/DotGothic16-Regular.ttf"),
    "ZenKakuGothicNew-500": ("ZenKakuGothicNew-Medium.ttf", f"{GF}/zenkakugothicnew/ZenKakuGothicNew-Medium.ttf"),
    "ZenKakuGothicNew-700": ("ZenKakuGothicNew-Bold.ttf", f"{GF}/zenkakugothicnew/ZenKakuGothicNew-Bold.ttf"),
    "ZenKakuGothicNew-900": ("ZenKakuGothicNew-Black.ttf", f"{GF}/zenkakugothicnew/ZenKakuGothicNew-Black.ttf"),
}
# 常に含める文字: ASCII・ひらがな・カタカナ・全角記号。新しい文字は build のたびに自動で追加される
BASE_RANGES = [(0x20, 0x7E), (0x3000, 0x303F), (0x3041, 0x3096), (0x30A0, 0x30FF), (0xFF01, 0xFF5E), (0x2190, 0x2193), (0x25A0, 0x25CF), (0x2605, 0x2606)]
# 公開物の走査から外すもの
GENERATED_DIRS = ["apps", "zukan", "stickers"]  # build が全部作り直すディレクトリ（手で置かない）
SKIP_DIRS = {".git", "tools", "assets"}


def write_pages():
    """tools/pages_*.py の build() が {公開パス: HTML} を返す。公開パスは '/apps/x/' か '/404.html' の形。"""
    written = []
    for d in GENERATED_DIRS:  # 前回の生成物を消す（階層が減る・名前が変わったときに古いHTMLを残さない）
        shutil.rmtree(ROOT / d, ignore_errors=True)
    for mod_path in sorted(TOOLS.glob("pages_*.py")):
        mod = importlib.import_module(mod_path.stem)
        for url_path, html in mod.build().items():
            out = ROOT / (url_path.lstrip("/") + ("index.html" if url_path.endswith("/") else ""))
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8", newline="\n")
            written.append(out)
    return written


def write_seo(written):
    """sitemap.xml と robots.txt。404 は載せない。privacy は既存ページなので、あるものだけ載せる。"""
    from lib import SITE
    urls = ["/" if p == ROOT / "index.html" else "/" + p.parent.relative_to(ROOT).as_posix() + "/"
            for p in written if p.name == "index.html"]
    urls += ["/privacy/" + d.name + "/" for d in sorted((ROOT / "privacy").glob("*/")) if (d / "index.html").exists()]
    nl = chr(10)
    rows = "".join(f"  <url><loc>{SITE}{u}</loc></url>{nl}" for u in sorted(set(urls)))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>' + nl
           + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + nl + rows + "</urlset>" + nl)
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8", newline=nl)
    robots = f"User-agent: *{nl}Allow: /{nl}{nl}Sitemap: {SITE}/sitemap.xml{nl}"
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8", newline=nl)


def collect_chars():
    chars = set()
    for lo, hi in BASE_RANGES:
        chars.update(chr(c) for c in range(lo, hi + 1))
    sources = [ROOT / "assets/css/site.css"]
    for p in ROOT.rglob("*.html"):
        if not set(p.relative_to(ROOT).parts[:-1]) & SKIP_DIRS:
            sources.append(p)
    sources += list((TOOLS / "data").glob("*.json"))
    for p in sources:
        chars.update(p.read_text(encoding="utf-8"))
    chars.discard("\n")
    return "".join(sorted(chars))


def subset_fonts():
    from fontTools import subset
    text = collect_chars()
    out_dir = ROOT / "assets/fonts"
    out_dir.mkdir(parents=True, exist_ok=True)
    FONT_SRC.mkdir(parents=True, exist_ok=True)
    for name, (src_name, url) in FONTS.items():
        src = FONT_SRC / src_name
        if not src.exists():
            print(f"download {src_name}")
            urllib.request.urlretrieve(url, src)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]  # ライセンス表記を残す
        font = subset.load_font(str(src), opts)
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(font)
        dst = out_dir / f"{name}.woff2"
        subset.save_font(font, str(dst), opts)
        print(f"{dst.name}: {dst.stat().st_size / 1024:.0f} KB ({len(text)} chars)")


def main():
    pages = write_pages()
    write_seo(pages)
    print(f"{len(pages)} pages")
    subset_fonts()


if __name__ == "__main__":
    main()
