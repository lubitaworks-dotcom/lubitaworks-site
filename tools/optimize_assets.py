"""公開用に画像を縮小する（原本は秘書室・実験室のまま。リポジトリには縮小版だけ入れる）。
使い方: python tools/optimize_assets.py
- アイコン: 実験室 handoff の角丸PNG（透過）-> 192px PNG（表示は最大96px。2倍）
- 画面イメージ: 秘書室の {アプリ名}_AppStore素材 の ios_ss_* -> 幅440px の webp（表示は最大220px。2倍）
"""
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
import os

# 原本の場所（ローカル専用の素材置き場）。環境変数で指定する
LAB = Path(os.environ["LUBITA_LAB_ASSETS"])      # 実験室/会社サイト_デザイン検証/handoff/assets
STORE = Path(os.environ["LUBITA_STORE_ROOT"])    # 秘書室（{アプリ名}_AppStore素材 がある場所）
ICON_SRC = {"gensyu-log": "gensyu_log", "oyatsu-log": "oyatsu_log", "plants-biyori": "plants_biyori",
            "medaka-biyori": "medaka_biyori", "hakko-biyori": "hakko_biyori", "zettai-lock": "zettai_lock"}
STORE_DIR = {"gensyu-log": "減酒ログ", "oyatsu-log": "おやつログ", "plants-biyori": "プランツびより",
             "medaka-biyori": "めだかびより", "hakko-biyori": "発酵びより", "zettai-lock": "絶対ロック"}


def icons():
    out = ROOT / "assets/img/icons"
    out.mkdir(parents=True, exist_ok=True)
    for slug, stem in ICON_SRC.items():
        im = Image.open(LAB / f"{stem}_rounded.png").convert("RGBA").resize((192, 192), Image.LANCZOS)
        im.save(out / f"{slug}.png", optimize=True)
        print("icon", slug, (out / f"{slug}.png").stat().st_size // 1024, "KB")


def shots():
    apps = json.loads((ROOT / "tools/data/apps.json").read_text(encoding="utf-8"))
    for a in apps:
        out = ROOT / "assets/img/apps" / a["slug"]
        out.mkdir(parents=True, exist_ok=True)
        for i, s in enumerate(a["shots"], 1):
            im = Image.open(STORE / f"{STORE_DIR[a['slug']]}_AppStore素材" / s["file"]).convert("RGB")
            im = im.resize((440, round(im.height * 440 / im.width)), Image.LANCZOS)
            dst = out / f"shot{i}.webp"
            im.save(dst, "WEBP", quality=82, method=6)
            print("shot", a["slug"], i, dst.stat().st_size // 1024, "KB")


def favicons():
    """ルビタ（通常）のドット絵 20x20 から favicon 一式を作る。"""
    src = Image.open(ROOT / "assets/img/rubita_normal_20.png").convert("RGBA")
    big = src.resize((640, 640), Image.NEAREST)
    big.resize((64, 64), Image.NEAREST).save(ROOT / "assets/img/favicon-64.png", optimize=True)
    big.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    # iOSのホーム画面用: paper地に少し余白を付ける
    tile = Image.new("RGBA", (180, 180), (245, 246, 241, 255))
    tile.alpha_composite(src.resize((140, 140), Image.NEAREST), (20, 20))
    tile.convert("RGB").save(ROOT / "assets/img/apple-touch-icon.png", optimize=True)


def og():
    """SNS共有用 1200x630。paper地にロゴ（ink）とルビタ。"""
    img = Image.new("RGB", (1200, 630), (245, 246, 241))
    logo = Image.open(STORE / "SNS素材" / "lockup_transparent_ink.png").convert("RGBA")
    logo = logo.resize((880, round(logo.height * 880 / logo.width)), Image.LANCZOS)
    img.paste(logo, ((1200 - logo.width) // 2, 150), logo)
    r = Image.open(ROOT / "assets/img/rubita_normal_20.png").convert("RGBA").resize((160, 160), Image.NEAREST)
    img.paste(r, ((1200 - 160) // 2, 360), r)
    img.save(ROOT / "assets/img/og.png", optimize=True)


if __name__ == "__main__":
    icons()
    favicons()
    og()
    if (ROOT / "tools/data/apps.json").exists():
        shots()
