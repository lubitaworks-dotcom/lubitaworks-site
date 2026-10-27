"""ページをまたいで使うHTML部品（トップ・図鑑・アプリ詳細）。構造とクラス名は handoff の叩き台に合わせてある。"""
import json
import re
from html import escape as e
from pathlib import Path

from lib import X_URL

DATA = Path(__file__).resolve().parent / "data"


def load_apps():
    return json.loads((DATA / "apps.json").read_text(encoding="utf-8"))


def platforms(app):
    return "iOS / Android" if app.get("play_pkg") else "iOS"


def app_rows(apps):
    rows = []
    for i, a in enumerate(apps, 1):
        rows.append(
            f'    <a class="row dot" href="/apps/{a["slug"]}/"><span class="no">{i:02d}</span>'
            f'<img class="ic" src="/assets/img/icons/{a["slug"]}.png" alt="" width="48" height="48" loading="lazy">'
            f'<span class="txt" style="font-family:\'Zen Kaku Gothic New\',sans-serif"><b>{e(a["name"])}</b><small>{e(a["tagline"])}</small></span>'
            f'<span class="pf">{platforms(a)}</span><span class="go">&gt; open</span></a>')
    return "\n".join(rows)


def devlog(apps, limit=5):
    """各アプリの開発ログを日付の新しい順に。日付が確認できていない項目は載せない。"""
    items = [(d["date"], a["name"], d["version"], d["note"]) for a in apps for d in a.get("devlog", []) if d.get("date")]
    items.sort(reverse=True)
    return "\n".join(
        f'    <div><span class="d">[{dt}]</span><span class="t">{e(n)} {e(v)}</span><span>{e(note)}</span></div>'
        for dt, n, v, note in items[:limit])


def load_stickers():
    """公開するスタンプセット（visible のもの）。"""
    d = json.loads((DATA / "stickers.json").read_text(encoding="utf-8"))
    return [x for x in d if x.get("visible")]


def nb(name):
    """末尾の「（返事）スタンプ」を1かたまりにして、「ス/タンプ」のような途中折り返しを防ぐ。"""
    m = re.search(r"(返事)?スタンプ$", name)
    if not m:
        return e(name)
    return e(name[:m.start()]) + f'<span style="white-space:nowrap">{e(m.group(0))}</span>'


def sticker_cards(sets):
    return chr(10).join(
        f'    <a class="card" href="/stickers/#{x["slug"]}" style="text-decoration:none"><span class="cap dot">LINE STICKER / {x["count"]}</span>'
        f'<div class="art"><img src="/assets/img/stickers/{x["slug"]}-main.webp" alt="{e(x["name"])}のメイン画像" width="240" height="240" loading="lazy"></div>'
        f'<span class="nm">{nb(x["name"])}</span></a>' for x in sets)


def zhead(sub, title="敵キャラ図鑑", img="rubita_surprised_20", alt="おどろくルビタ"):
    return f"""  <div class="zhead">
    <div class="rubita-frame s"><img src="/assets/img/{img}.png" alt="{alt}"></div>
    <div class="t">
      <h2 class="hh">{title}</h2>
      <p class="muted">{e(sub)}</p>
    </div>
  </div>"""


STICKER_LEAD = "ルビタ図鑑のモンスターが、LINEスタンプになったよ！ドット絵で、毎日のあいさつや返事に使えるんだ。"
ZUKAN_LEAD = "電脳の世界にひそむ敵キャラが、毎朝Xに1体ずつ出てくるよ。出会った全員を、ここに図鑑として残していくね！"


def floor_cards(f):
    """階層タイル＋7体のカード（未解放は LOCKED）。"""
    pct = round(f["unlocked"] / f["total"] * 100)
    boss = e(f["boss"]) if f["boss"] else "？？？"
    out = [f'''    <div class="floor-tile"><div><div class="no">FLOOR {f["floor"]:02d} / DUNGEON</div><div class="fl">第{f["floor"]}階層</div><div class="sub">「{e(f["name"])}」</div></div>
      <div class="boss"><span class="lb">BOSS ★5</span><span class="bn">{boss}</span></div><div class="files">FILES {f["unlocked"]} / {f["total"]} 体</div><div class="bar" aria-hidden="true"><i style="width:{pct}%"></i></div></div>''']
    for c in f["cards"]:
        if c["unlocked"]:
            new = '<b class="new">NEW</b>' if c["new"] else ""
            out.append(f'    <div class="card"><span class="cap dot">FILE No.{c["no"]:03d}{new}</span><div class="art"><img src="/assets/img/zukan/{c["no"]:03d}.webp" alt="{e(c["alt"])}" width="560" height="560" loading="lazy"></div><span class="nm">{e(c["name"])}</span></div>')
        else:
            out.append(f'    <div class="card lock"><span class="cap dot">FILE No.{c["no"]:03d}</span><div class="art" aria-label="未解放">LOCKED</div><span class="nm">？？？</span></div>')
    return "\n".join(out)


def follow_band():
    return f"""  <div class="follow" id="x">
    <div class="bar dot"><i></i><i></i><i></i><span>&gt; follow @LUBITAWORKS</span></div>
    <div class="body">
      <div class="talk">
        <div class="rubita-frame s"><img src="/assets/img/rubita_wink_20.png" alt="ウインクするルビタ"></div>
        <div class="msg"><span class="who">@LUBITAWORKS</span><span class="muted">今日の新種は、Xでチェックしてね！</span></div>
      </div>
      <a class="btn am dot" href="{X_URL}" style="font-size:16px">&gt; open X</a>
    </div>
  </div>"""
