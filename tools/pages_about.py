"""このサイトについて /about/。運営者情報（屋号のみ）・画像の扱い・免責・フォント・商標。"""
from lib import MAIL, X_URL, analytics_token, breadcrumb, page

# アクセス解析を入れたときだけ表示する説明。Cloudflare公式FAQで確認できた範囲だけを書く
# （「Cookieを使わない」「個人を特定しない」等は、公式の記載を確認できていないので書かない）。
ANALYTICS = """
    <h3>アクセス解析について</h3>
    <ul>
      <li>このサイトでは、閲覧数などの傾向を把握するために、Cloudflare Web Analytics でアクセス状況を集計しています。ページの閲覧数、流入元、国、端末の種類などを、サイト全体の集計として見ています。</li>
      <li>解析のために、お使いのブラウザは Cloudflare のサーバー（static.cloudflareinsights.com、cloudflareinsights.com）と通信します。</li>
      <li>Cloudflare は、Web Analytics について「個々の訪問者を追跡しない」と説明しています（Cloudflare ダッシュボードの表示）。当サイトでも、広告やプロフィール作成のための追跡は行っていません。</li>
    </ul>
"""


def build():
    analytics = ANALYTICS if analytics_token() else ""
    body = f"""<section class="blk" style="padding-top:8px">
  <div class="tag">[ 05 ] ABOUT</div>
  <h2 class="hh">このサイトについて</h2>

  <div class="about">
    <h3>運営者情報</h3>
    <ul>
      <li>屋号：LUBITA WORKS（ルビタワークス）</li>
      <li>お問い合わせ：<a href="mailto:{MAIL}">{MAIL}</a></li>
      <li>公式X：<a href="{X_URL}">@LUBITAWORKS</a></li>
      <li>販売業者の表示：<a href="/tokushoho/">特定商取引法に基づく表記</a></li>
    </ul>

    <h3>このサイトの画像・文章について</h3>
    <ul>
      <li>アプリのアイコン・画面写真は、LUBITA WORKS が制作したものです。</li>
      <li>「ルビタ」のドット絵は、LUBITA WORKS が制作したオリジナルキャラクターです。</li>
      <li>「敵キャラ図鑑」のイラストは、画像生成AIで生成した画像を、LUBITA WORKS が選定・調整して掲載しています。</li>
      <li>画像・文章の無断での転載・再配布はご遠慮ください。</li>
      <li>画像・文章の引用や、SNS・ブログでのご紹介は歓迎です。出典として、サイト名またはURLを添えてください。</li>
    </ul>

    <h3>リンクについて</h3>
    <ul>
      <li>このサイトへのリンクは、自由にどうぞ。ご連絡は不要です。</li>
    </ul>

    <h3>免責</h3>
    <ul>
      <li>掲載している情報は、できる限り正確を心がけていますが、内容を保証するものではありません。アプリの機能・価格・対応状況は、変更されることがあります。最新の情報は、各ストアのページをご確認ください。</li>
      <li>アプリの利用に関する詳細は、各アプリのプライバシーポリシーをご覧ください（<a href="/support/">サポート</a>からご確認いただけます）。</li>
    </ul>

{analytics}
    <h3>使用しているフォント</h3>
    <ul>
      <li>Archivo Black、DotGothic16、Zen Kaku Gothic New（いずれも SIL Open Font License 1.1）。ライセンス文は <a href="/assets/fonts/OFL.txt">OFL.txt</a> をご覧ください。</li>
    </ul>

    <h3>商標</h3>
    <ul>
      <li>App Store は Apple Inc. のサービスマークです。Google Play は Google LLC の商標です。X は X Corp. の商標です。</li>
    </ul>
  </div>
</section>"""
    return {"/about/": page(title="このサイトについて", path="/about/", crumb=breadcrumb(("about", None)),
                            desc="LUBITA WORKS の運営者情報、画像・文章の扱い、免責、使用しているフォントについて。", body=body)}
