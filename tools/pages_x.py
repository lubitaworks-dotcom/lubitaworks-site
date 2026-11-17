"""Xからの流入を測るための転送ページ /x/ ほか。

Cloudflare Web Analytics は URL の「?」以降（utm_source など）を記録しないので、
Xのプロフィール・投稿に貼るURLを、パスが違うこのページにして、アクセス数で数える。
開くと約1秒で本来のページへ移る（その間に解析のスクリプトが送信される）。
検索には載せない（noindex・sitemap対象外）。
"""
from html import escape

from lib import SITE, page

# (このサイトのパス, 転送先, 使い道)
ROUTES = [
    ("/x/", "/", "Xのプロフィールのウェブサイト欄・固定ポスト"),
    ("/x/stickers/", "/stickers/", "Xのスタンプ告知ポスト"),
    ("/x/zukan/", "/zukan/", "Xの敵キャラ図鑑のポスト"),
]


def _redirect(path, to):
    head = (
        '<meta name="robots" content="noindex,follow">\n'
        f'<meta http-equiv="refresh" content="1;url={escape(to)}">\n'
        f"<script>setTimeout(function(){{location.replace({to!r})}},700)</script>\n"
    )
    body = f"""<section class="blk" style="padding-top:32px">
  <div class="win">
    <div class="win-bar dot"><i></i><i></i><i></i><span>rubita@lubitaworks:~</span></div>
    <div class="win-body dot">
      <div class="muted">&gt; ようこそ。ページを開いています…</div>
      <div style="margin-top:12px"><a class="btn" href="{escape(to)}">&gt; 開かないときはこちら</a></div>
    </div>
  </div>
</section>"""
    p = page(title="", path=to, desc="LUBITA WORKS（ルビタワークス）のサイトへ移動します。",
             body=body, head_extra=head)
    # canonical は転送先のまま（page(path=to) で設定済み）。ページ名だけ元のパスに合わせる必要はない
    return p


def build():
    return {src: _redirect(src, to) for src, to, _ in ROUTES}
