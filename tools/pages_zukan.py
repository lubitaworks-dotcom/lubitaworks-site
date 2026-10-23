"""敵キャラ図鑑: /zukan/（最新階層）と /zukan/{N}/（第N階層）。1ページ＝1階層＝7体で固定。"""
import parts
import zukan_data
from lib import breadcrumb, page


def _href(n, latest_no):
    return "/zukan/" if n == latest_no else f"/zukan/{n}/"


def _pager(nos, cur, latest_no):
    """階層が7以下は全部。8以上は、現在地の前後2つ＋先頭・末尾を出し、間は「…」で省略。"""
    if len(nos) <= 7:
        shown = nos
    else:
        keep = {nos[0], nos[-1]} | {n for n in nos if abs(n - cur) <= 2}
        shown = [n for n in nos if n in keep]
    items, prev = [], None
    if cur != nos[0]:
        items.append(f'<a class="step" href="{_href(cur - 1, latest_no)}" aria-label="前の階層">&lt;</a>')
    for n in shown:
        if prev is not None and n - prev > 1:
            items.append('<span class="gap" aria-hidden="true">…</span>')
        items.append('<span class="cur" aria-current="page">%d</span>' % n if n == cur else f'<a href="{_href(n, latest_no)}">{n}</a>')
        prev = n
    if cur != nos[-1]:
        items.append(f'<a class="step" href="{_href(cur + 1, latest_no)}" aria-label="次の階層">&gt;</a>')
    return f'  <nav class="pager" aria-label="階層（ページ）">{"".join(items)}</nav>'


def _body(f, nos, latest_no):
    return f"""<section class="blk" style="padding-top:8px">
  <div class="tag">[ 02 ] ENEMY FILE</div>
{parts.zhead(parts.ZUKAN_LEAD)}
  <div class="cards">
{parts.floor_cards(f)}
  </div>
{_pager(nos, f["floor"], latest_no)}
  <div class="pager-note">第{f["floor"]}階層「{f["name"]}」を表示中。ページ番号＝階層（1ページ7体で固定）。</div>
{parts.follow_band()}
</section>"""


def build():
    floors = zukan_data.load()
    zukan_data.sync_images(floors)
    latest = zukan_data.latest_floor(floors)
    floors = zukan_data.visible(floors)
    nos = [f["floor"] for f in floors]
    out = {}
    for f in floors:
        is_latest = f["floor"] == latest["floor"]
        path = _href(f["floor"], latest["floor"])
        crumb = breadcrumb(("zukan", None if is_latest else "/zukan/"), *(() if is_latest else ((f"第{f['floor']}階層", None),)))
        out[path] = page(title=f"敵キャラ図鑑 第{f['floor']}階層「{f['name']}」", path=path, crumb=crumb,
                         desc="ルビタの敵キャラ図鑑。電脳の世界にひそむ敵キャラを、毎朝Xに1体ずつ紹介し、ここに図鑑として残しています。",
                         body=_body(f, nos, latest["floor"]))
    return out
