"""プライバシーポリシー /privacy/{slug}/ ×6。URLは変えない。

本文（<main> の中身）は tools/data/privacy/{slug}.html に原文のまま置き、ここでは枠（ヘッダー・フッター・装飾）だけを
新デザインにする。ポリシーの文面を改定するときは、そのHTMLを直す（改定は必ずユーザー確認のうえで）。
"""
import json
from pathlib import Path

from lib import breadcrumb, page

DATA = Path(__file__).resolve().parent / "data" / "privacy"


def build():
    meta = json.loads((DATA / "meta.json").read_text(encoding="utf-8"))
    out = {}
    for slug, m in meta.items():
        inner = (DATA / f"{slug}.html").read_text(encoding="utf-8").rstrip("\n")
        body = f'<section class="blk" style="padding-top:8px">\n<article class="policy">\n{inner}\n</article>\n</section>'
        path = f"/privacy/{slug}/"
        out[path] = page(title=m["title"], desc=m["desc"], path=path, body=body,
                         crumb=breadcrumb(("apps", "/#apps"), (slug, f"/apps/{slug}/"), ("privacy", None)))
    return out
