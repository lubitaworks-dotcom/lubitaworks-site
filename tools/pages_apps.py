"""アプリ詳細 /apps/{slug}/ ×6。データは tools/data/apps.json。"""
from html import escape as e

import parts
from lib import MAIL, breadcrumb, page


def _body(a, apps):
    chips = "<span>iOS</span>" + ("<span>Android</span>" if a.get("play_pkg") else "")
    store = f'<a href="https://apps.apple.com/jp/app/id{a["apple_id"]}">App Store で見る</a>'
    if a.get("play_pkg"):
        store += f'\n      <a href="https://play.google.com/store/apps/details?id={a["play_pkg"]}">Google Play で見る</a>'
    shots = "\n".join(
        f'    <div class="shot"><div class="win-bar dot"><i></i><i></i><i></i><span>shot_{i:02d}</span></div>'
        f'<img src="/assets/img/apps/{a["slug"]}/shot{i}.webp" alt="{e(s["alt"])}" width="440" height="952" loading="lazy"></div>'
        for i, s in enumerate(a["shots"], 1))
    feats = "\n".join(
        f'    <div><span class="n dot">FEATURE {i:02d}</span><b>{e(f["title"])}</b><span class="s">{e(f["body"])}</span></div>'
        for i, f in enumerate(a["features"], 1))
    others = "\n".join(
        f'    <a href="/apps/{o["slug"]}/"><img src="/assets/img/icons/{o["slug"]}.png" alt="" width="80" height="80" loading="lazy">{e(o["name"])}</a>'
        for o in apps if o["slug"] != a["slug"])
    return f"""<section class="hero">
  <div class="l">
    <div class="ident">
      <img src="/assets/img/icons/{a["slug"]}.png" alt="{e(a["name"])}のアイコン" width="96" height="96">
      <div>
        <h1>{e(a["name"])}</h1>
        <div class="chips dot">{chips}</div>
      </div>
    </div>
    <p class="lead">{e(a["tagline"])}</p>
    <p class="muted" style="margin:0;max-width:540px">{e(a["blurb"])}</p>
    <div class="store">
      {store}
    </div>
  </div>
  <div class="r">
    <div class="bubble">ここが、このアプリのポイントだよ！</div>
    <div class="rubita-frame s"><img src="/assets/img/rubita_happy_20.png" alt="にっこりするルビタ"></div>
  </div>
</section>

<section class="blk" style="padding-top:0">
  <h2 class="hh">画面イメージ</h2>
  <div class="shots" tabindex="0" aria-label="スクリーンショット（横にスクロール）">
{shots}
  </div>
</section>

<section class="blk" style="padding-top:0">
  <h2 class="hh">できること</h2>
  <div class="feat">
{feats}
  </div>
</section>

<section class="blk" style="padding-top:0">
  <div class="support">
    <div><b style="color:var(--hd)">サポート・規約</b><br><span class="muted" style="font-size:14px">お困りのときは、メールでお問い合わせください。</span></div>
    <div style="display:flex;flex-wrap:wrap;gap:8px 28px;font-weight:700;font-size:15px">
      <a href="/privacy/{a["slug"]}/">プライバシーポリシー</a>
      <a href="mailto:{MAIL}">{MAIL}</a>
    </div>
  </div>
</section>

<section class="blk" style="padding-top:0">
  <h2 class="hh">ほかのアプリ</h2>
  <div class="others">
{others}
  </div>
</section>"""


def build():
    apps = parts.load_apps()
    out = {}
    for a in apps:
        path = f"/apps/{a['slug']}/"
        crumb = breadcrumb(("apps", "/#apps"), (a["slug"], None))
        out[path] = page(title=a["name"], path=path, crumb=crumb,
                         desc=f"{a['name']}（{a['tagline']}）。{a['blurb']}", body=_body(a, apps))
    return out
