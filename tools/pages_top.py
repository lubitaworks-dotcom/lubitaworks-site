"""トップページ。"""
import json

import parts
import zukan_data
from lib import SITE, X_URL, page


def build():
    apps = parts.load_apps()
    floors = zukan_data.load()
    zukan_data.sync_images(floors)
    latest = zukan_data.latest_floor(floors)
    started = any(f["unlocked"] for f in floors)
    tag = "[ 02 ] ENEMY FILE — 毎朝1体" if started else "[ 02 ] ENEMY FILE — 10/26 スタート"

    body = f"""<section id="top" class="hero-top">
  <div class="win">
    <div class="win-bar dot"><i></i><i></i><i></i><span>rubita@lubitaworks:~</span></div>
    <div class="win-body dot">
      <div class="muted">&gt; hello</div>
      <h1><span class="ph">暮らしにそっと寄りそう、</span><br><span class="ph">小さなアプリをつくっています。</span></h1>
      <div class="say"><img class="say-r" src="/assets/img/rubita_normal_20.png" alt="ルビタ"><div class="muted">&gt; ぼくはルビタ。ここの案内役だよ。まずはアプリを見てみる？</div></div>
      <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:12px">
        <a class="btn" href="#apps">&gt; アプリを見る</a>
        <a class="btn line" href="{X_URL}">&gt; 公式X</a>
      </div>
    </div>
  </div>
  <div class="rubita-wrap"><div class="rubita-frame"><img src="/assets/img/rubita_normal_20.png" alt="ロボのキャラクター「ルビタ」"></div></div>
</section>

<section id="apps" class="blk">
  <div class="tag">[ 01 ] APPS — {len(apps)} files found</div>
  <div class="list">
{parts.app_rows(apps)}
  </div>
</section>

<section id="zukan" class="blk">
  <div class="tag">{tag}</div>
{parts.zhead(parts.ZUKAN_LEAD)}
  <div class="cards">
{parts.floor_cards(latest)}
  </div>
  <a class="btn dot more" href="/zukan/">&gt; 全階層を見る</a>
{parts.follow_band()}
</section>

<section id="log" class="blk">
  <div class="tag">[ 03 ] DEV LOG</div>
  <div class="log dot">
{parts.devlog(apps)}
  </div>
</section>"""

    # 構造化データ: サイト名の別名（カナ・ひらがな）をGoogleに伝える。表示には出ない
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "LUBITA WORKS",
         "alternateName": ["ルビタワークス", "るびたわーくす"], "inLanguage": "ja"},
        {"@type": "Organization", "@id": f"{SITE}/#org", "url": f"{SITE}/", "name": "LUBITA WORKS",
         "alternateName": ["ルビタワークス", "るびたわーくす"], "sameAs": [X_URL]},
    ]}
    head_extra = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>\n"
    return {"/": page(title="", path="/", body=body, head_extra=head_extra,
                      desc="LUBITA WORKS（ルビタワークス）— 暮らしにそっと寄りそう、小さなアプリをつくっています。")}
