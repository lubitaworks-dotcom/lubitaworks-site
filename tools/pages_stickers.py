"""LINEスタンプ: /stickers/。データは tools/data/stickers.json（visible のものだけ載せる）。"""
from html import escape as e

import parts
from lib import breadcrumb, page

AUTHOR = "https://line.me/S/shop/sticker/author/6779143"


def _set(x):
    if x.get("line_url"):
        go = f'<a class="btn" href="{e(x["line_url"])}">&gt; LINEストアで見る</a>'
    else:
        go = '<span class="muted">LINEストアのリンクは準備中です。</span>'
    return f"""  <article class="stk" id="{x["slug"]}">
    <div class="top">
      <div class="art"><img src="/assets/img/stickers/{x["slug"]}-main.webp" alt="{e(x["name"])}のメイン画像" width="240" height="240" loading="lazy"></div>
      <div class="info">
        <h2 class="hh"><span>{parts.nb(x["name"])}</span></h2>
        <div class="chips dot"><span>{"動く " if x.get("animated") else ""}{x["count"]}個</span><span>¥{x["price"]}</span><span>{e(x["chara"])}</span></div>
        <p class="muted" style="margin:0">{e(x["blurb"])}</p>
        <div>{go}</div>
      </div>
    </div>
    <p class="shcap dot">▼ 全{x["count"]}個{"（一覧は1コマ目。動きはLINEストアで見られます）" if x.get("animated") else "（LINEストアで拡大して見られます）"}</p>
    <div class="sheet"><img src="/assets/img/stickers/{x["slug"]}-sheet.webp" alt="{e(x["alt"])}" width="960" height="{240 * ((x["count"] + 3) // 4) if x.get("animated") else 832}" loading="lazy"></div>
  </article>"""


def build():
    sets = parts.load_stickers()
    body = f"""<section class="blk" style="padding-top:8px">
  <div class="tag">[ 01 ] LINE STICKER</div>
{parts.zhead(parts.STICKER_LEAD, "LINEスタンプ", "rubita_happy_20", "にっこりするルビタ")}
{chr(10).join(_set(x) for x in sets)}
  <div><a class="btn line dot" href="{AUTHOR}">&gt; 作者ページ（LINEストア）</a></div>
  <p class="muted" style="font-size:14px;margin:0">スタンプの絵は、画像生成AIを使って制作しています。価格はLINEストアの表示が優先されます。</p>
</section>"""
    return {"/stickers/": page(title="LINEスタンプ", path="/stickers/", crumb=breadcrumb(("stickers", None)),
                               og_image="/assets/img/og-stickers.png",
                               desc="LUBITA WORKSのLINEスタンプ。ルビタ図鑑のモンスターが、ドット絵のスタンプになりました。", body=body)}
