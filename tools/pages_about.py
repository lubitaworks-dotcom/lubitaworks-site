"""このサイトについて /about/。運営者情報（屋号のみ）・画像の扱い・免責・フォント・商標。"""
from lib import MAIL, X_URL, breadcrumb, page


def build():
    body = f"""<section class="blk" style="padding-top:8px">
  <div class="tag">[ 05 ] ABOUT</div>
  <h2 class="hh">このサイトについて</h2>

  <div class="about">
    <h3>運営者情報</h3>
    <ul>
      <li>屋号：LUBITA WORKS</li>
      <li>お問い合わせ：<a href="mailto:{MAIL}">{MAIL}</a></li>
      <li>公式X：<a href="{X_URL}">@LUBITAWORKS</a></li>
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
