"""共通部品。ページ生成（build.py）から使う。クラス名は assets/css/site.css と同じ。"""
import datetime
import json
from html import escape
from pathlib import Path

SITE = "https://lubitaworks.com"
X_URL = "https://x.com/LUBITAWORKS"
MAIL = "info@lubitaworks.com"
FIRST_YEAR = 2026


def analytics_token():
    """Cloudflare Web Analytics のビーコントークン（未設定なら None＝解析スクリプトを入れない）。"""
    p = Path(__file__).resolve().parent / "data" / "analytics.json"
    return json.loads(p.read_text(encoding="utf-8")).get("cloudflare_web_analytics_token") if p.exists() else None


def _beacon():
    t = analytics_token()
    if not t:
        return ""
    attr = json.dumps({"token": t})
    return ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            f"data-cf-beacon='{attr}'></script>" + chr(10))


def _years():
    y = datetime.date.today().year
    return str(FIRST_YEAR) if y <= FIRST_YEAR else f"{FIRST_YEAR}–{y}"


def page(*, title, desc, path, body, crumb=""):
    """共通のヘッド・ヘッダー・フッターで包んだHTMLを返す。path は '/apps/gensyu-log/' の形。"""
    full_title = "LUBITA WORKS" if title == "" else f"{title} | LUBITA WORKS"
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/assets/img/favicon-64.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<div class="wrap">

<header class="site">
  <a class="logo" href="/">LUBITA WORKS<span class="cur" aria-hidden="true">_</span></a>
  <nav class="site" aria-label="メイン">
    <a href="/#apps">/apps</a><a href="/zukan/">/zukan</a><a href="/#log">/log</a><a href="{X_URL}">/x</a>
  </nav>
</header>
{crumb}
{body}

<img class="motif" src="/assets/img/sakurajima_motif_teal.png" alt="" aria-hidden="true">
<footer class="site">
  <span>© {_years()} LUBITA WORKS</span>
  <span class="fl"><a href="/about/">このサイトについて</a><a href="/support/">サポート</a><a href="/tokushoho/">特定商取引法に基づく表記</a></span>
  <span>お問い合わせ：<a href="mailto:{MAIL}">{MAIL}</a></span>
</footer>
<p class="legal">App Store は Apple Inc. のサービスマークです。Google Play は Google LLC の商標です。X は X Corp. の商標です。</p>

</div>
{_beacon()}</body>
</html>
"""


def breadcrumb(*parts):
    """parts は (表示, href or None) の並び。先頭に top を付ける。"""
    items = ['<a href="/">top</a>']
    for label, href in parts:
        items.append(f'<a href="{href}">{escape(label)}</a>' if href else escape(label))
    return f'<div class="crumb">{" / ".join(items)}</div>'
