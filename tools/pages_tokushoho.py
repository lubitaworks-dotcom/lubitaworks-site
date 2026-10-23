"""特定商取引法に基づく表記 /tokushoho/。

方針（2026-10-23ユーザー決定）: 氏名は表示し、住所・電話番号は「請求があれば遅滞なく開示」とする。
調査: 秘書室/進行管理/会社サイト_特商法表記_調査.md。返品・返金は、当方の独自ルールを決めていないため、各ストアの規定に従う旨だけを書く。
"""
from lib import MAIL, breadcrumb, page

ROWS = [
    ("販売業者", "田代 雄作（屋号：LUBITA WORKS〔ルビタワークス〕）"),
    ("運営責任者", "田代 雄作"),
    ("所在地", "請求があれば、遅滞なく開示します。"),
    ("電話番号", "請求があれば、遅滞なく開示します。"),
    ("お問い合わせ", f'<a href="mailto:{MAIL}">{MAIL}</a>（所在地・電話番号のご請求も、こちらのメールで受け付けます。）'),
    ("販売価格", "各アプリのApp Store・Google Playのページおよび購入画面に表示される金額（消費税込み）です。"),
    ("商品代金以外の必要料金", "アプリのダウンロード・利用時の通信料は、お客様のご負担となります。"),
    ("支払方法・支払時期", "App Store・Google Playの決済方法に従います。支払時期は、各ストアの規定によります。"),
    ("提供時期", "購入手続きの完了後、ただちにご利用いただけます。"),
    ("返品・返金・キャンセル", "各ストア（Apple・Google）の規定に従います。お手続きは、購入されたストアの窓口へお願いします。"),
    ("動作環境", "各アプリのApp Store・Google Playのページに記載しています。"),
]


def build():
    rows = "\n".join(f"      <tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in ROWS)
    body = f"""<section class="blk" style="padding-top:8px">
  <div class="tag">[ 06 ] LEGAL</div>
  <h2 class="hh">特定商取引法に基づく表記</h2>
  <div class="about">
    <p class="muted" style="margin:16px 0 8px">LUBITA WORKS のアプリ内課金（買い切り）に関する表記です。</p>
    <table class="tbl">
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
</section>"""
    return {"/tokushoho/": page(title="特定商取引法に基づく表記", path="/tokushoho/", crumb=breadcrumb(("tokushoho", None)),
                                desc="LUBITA WORKS の特定商取引法に基づく表記。アプリ内課金（買い切り）の販売条件について。", body=body)}
