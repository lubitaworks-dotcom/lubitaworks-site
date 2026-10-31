"""LINEスタンプ: /stickers/。データは tools/data/stickers.json（visible のものだけ載せる）。"""
from html import escape as e

import parts
from lib import breadcrumb, page

AUTHOR = "https://line.me/S/shop/sticker/author/6779143"


def _set(x):
    reg = parts.REGIONS[x["region"]] if x.get("region") else None   # 海外限定版（日本では購入できない）
    if x.get("line_url"):
        label = f'{reg["name"]}のLINEストアで見る' if reg else "LINEストアで見る"
        go = f'<a class="btn" href="{e(x["line_url"])}">&gt; {label}</a>'
        if reg:
            go += f'<p class="muted" style="font-size:14px;margin:8px 0 0">日本から開くと、見られない場合があります。</p>'
    else:
        go = '<span class="muted">LINEストアのリンクは準備中です。</span>'
    price = e(x["price_label"]) if x.get("price_label") else f'¥{x["price"]}'
    chips = (f'<span>{"動く " if x.get("animated") else ""}{x["count"]}個</span><span>{price}</span>'
             f'<span>{e(x["chara"])}</span>' + (f'<span>{reg["name"]}限定</span>' if reg else ""))
    # 現地語のスタンプ名（LINEでの登録名）は、あれば日本語名の下に添える（言語を指定して、正しいフォントで表示させる）
    local = (f'\n        <p class="muted" lang="{reg["lang"]}" style="margin:0;font-weight:700">{e(x["name_local"])}</p>'
             if reg and x.get("name_local") else "")
    return f"""  <article class="stk" id="{x["slug"]}">
    <div class="top">
      <div class="art"><img src="/assets/img/stickers/{x["slug"]}-main.webp" alt="{e(x["name"])}のメイン画像" width="240" height="240" loading="lazy"></div>
      <div class="info">
        <h2 class="hh"><span>{parts.nb(x["name"])}</span></h2>{local}
        <div class="chips dot">{chips}</div>
        <p class="muted" style="margin:0">{e(x["blurb"])}</p>
        <div>{go}</div>
      </div>
    </div>
    <p class="shcap dot">▼ 全{x["count"]}個{"（一覧は1コマ目。動きはLINEストアで見られます）" if x.get("animated") else "（LINEストアで拡大して見られます）"}</p>
    <div class="sheet"><img src="/assets/img/stickers/{x["slug"]}-sheet.webp" alt="{e(x["alt"])}" width="960" height="{(240 if x.get("animated") else 208) * ((x["count"] + 3) // 4)}" loading="lazy"></div>
  </article>"""


def build():
    sets = parts.load_stickers()
    jp, overseas = parts.jp_stickers(sets), parts.overseas_stickers(sets)
    # 海外限定版は、日本向けの下に、別の見出しで載せる（日本では購入できないことを明記）
    names = "・".join(dict.fromkeys(parts.REGIONS[x["region"]]["name"] for x in overseas))
    overseas_html = f"""
  <h2 class="hh" id="overseas" style="margin-top:24px">海外限定版（{names}）</h2>
  <p class="muted" style="margin:0">次のスタンプは、{names}のLINEストアだけで販売しています。<b>日本のLINEストアでは購入できません</b>。</p>
{chr(10).join(_set(x) for x in overseas)}""" if overseas else ""
    body = f"""<section class="blk" style="padding-top:8px">
  <div class="tag">[ 01 ] LINE STICKER</div>
{parts.zhead(parts.STICKER_LEAD, "LINEスタンプ", "rubita_happy_20", "にっこりするルビタ")}
{chr(10).join(_set(x) for x in jp)}{overseas_html}
  <div><a class="btn line dot" href="{AUTHOR}">&gt; 作者ページ（LINEストア）</a></div>
  <p class="muted" style="font-size:14px;margin:0">スタンプの絵は、画像生成AIを使って制作しています。価格はLINEストアの表示が優先されます。</p>
</section>"""
    return {"/stickers/": page(title="LINEスタンプ", path="/stickers/", crumb=breadcrumb(("stickers", None)),
                               og_image="/assets/img/og-stickers.png",
                               desc="LUBITA WORKSのLINEスタンプ。ルビタ図鑑のモンスターが、ドット絵のスタンプになりました。", body=body)}
