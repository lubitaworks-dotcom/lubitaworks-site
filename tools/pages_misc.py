"""サポート /support/ と 404。"""
from html import escape as e

import parts
from lib import MAIL, breadcrumb, page


def _support():
    apps = parts.load_apps()
    policies = "\n".join(
        f'      <a href="/privacy/{a["slug"]}/">{e(a["name"])}</a>' for a in apps)
    body = f"""<section class="blk" style="padding-top:8px">
  <div class="tag">[ 04 ] SUPPORT</div>
  <div class="zhead">
    <div class="rubita-frame s"><img src="/assets/img/rubita_happy_20.png" alt="にっこりするルビタ"></div>
    <div class="t">
      <h2 class="hh">サポート</h2>
      <p class="muted">アプリのご質問・ご要望・不具合のご連絡は、メールでお問い合わせください。件名か本文に、アプリの名前を添えていただけると助かります。</p>
    </div>
  </div>
  <div class="support">
    <div><b style="color:var(--hd)">お問い合わせ</b><br><span class="muted" style="font-size:14px">メールアドレス</span></div>
    <div style="display:flex;flex-wrap:wrap;gap:8px 28px;font-weight:700;font-size:15px">
      <a href="mailto:{MAIL}">{MAIL}</a>
    </div>
  </div>
  <h2 class="hh" style="margin-top:12px">プライバシーポリシー</h2>
  <div class="support">
    <div style="display:flex;flex-wrap:wrap;gap:8px 28px;font-weight:700;font-size:15px">
{policies}
    </div>
  </div>
</section>"""
    return page(title="サポート", path="/support/", crumb=breadcrumb(("support", None)),
                desc="LUBITA WORKS のアプリに関するお問い合わせ先と、各アプリのプライバシーポリシーへのリンクです。", body=body)


def _not_found():
    body = """<section class="blk" style="padding-top:32px">
  <div class="win">
    <div class="win-bar dot"><i></i><i></i><i></i><span>rubita@lubitaworks:~</span></div>
    <div class="win-body dot">
      <div class="muted">&gt; open ?</div>
      <h1><span class="ph">ページが見つかりません</span></h1>
      <div class="say"><img class="say-r" src="/assets/img/rubita_surprised_20.png" alt="ルビタ"><div class="muted">&gt; あれれ、迷子になっちゃった？ トップに戻ろう。</div></div>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:12px">
        <a class="btn" href="/">&gt; トップへ戻る</a>
      </div>
    </div>
  </div>
</section>"""
    return page(title="ページが見つかりません", path="/404.html", desc="お探しのページは見つかりませんでした。", body=body)


def build():
    return {"/support/": _support(), "/404.html": _not_found()}
