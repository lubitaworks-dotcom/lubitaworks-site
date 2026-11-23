"""ページをまたいで使うHTML部品（トップ・図鑑・アプリ詳細）。構造とクラス名は handoff の叩き台に合わせてある。"""
import datetime
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


def pickup(apps):
    """トップの「注目アプリ」枠。apps.json で pickup を持つアプリだけ（無ければ空）。画像はアプリ詳細の1枚目（表紙）。"""
    out = []
    for a in apps:
        p = a.get("pickup")
        if not p:
            continue
        pts = "".join(f"<li>{e(x)}</li>" for x in p.get("points", []))
        out.append(f"""<section id="pickup" class="blk">
  <div class="tag">[ {e(p.get("label", "PICK UP"))} ] APP</div>
  <div class="pick win">
    <div class="win-bar dot"><i></i><i></i><i></i><span>{e(a["slug"])}.app</span></div>
    <div class="pick-body">
      <div class="pick-txt">
        <div class="ident">
          <img src="/assets/img/icons/{a["slug"]}.png" alt="{e(a["name"])}のアイコン" width="72" height="72">
          <div><h2 class="hh">{e(a["name"])}</h2><span class="muted dot" style="font-size:14px">{platforms(a)}</span></div>
        </div>
        <p class="lead">{e(a["tagline"])}</p>
        <p class="muted" style="margin:0">{e(p.get("lead", ""))}</p>
        <ul class="pick-pts">{pts}</ul>
        <div class="store">
          <a href="https://apps.apple.com/jp/app/id{a["apple_id"]}"><img src="/assets/img/badges/appstore-ja.svg" alt="App Storeでダウンロード" width="141" height="52"></a>
          <a class="btn line" href="/apps/{a["slug"]}/">&gt; 詳しく見る</a>
        </div>
      </div>
      <a class="pick-shot" href="/apps/{a["slug"]}/"><img src="/assets/img/apps/{a["slug"]}/shot1.webp" alt="{e(a["shots"][0]["alt"]) if a.get("shots") else ""}" width="440" height="952" loading="lazy"></a>
    </div>
  </div>
</section>""")
    return "\n\n".join(out)


def devlog(apps, stickers=(), limit=10):
    """NEWS（アプリの更新＋LINEスタンプの発売）を日付の新しい順に。日付が確認できていない項目は載せない。
    スタンプは stickers.json の release_date があるものだけ（公開表示にするときに発売日を入れる）。"""
    # 同じ日付なら、スタンプ（先に並べる）→アプリの更新の順（日付だけで時刻は持たないため、sort は安定ソートで先に入れた方が上）
    # 海外限定版（region あり）は、日本では買えないので、見出しに国名を明記し、注記を添える
    items = [(s["release_date"],
               f'<span class="t"><a href="/stickers/#{s["slug"]}">LINEスタンプ{region_tag(s)}</a></span>',
               (f'「{e(s["name"])}」を{REGIONS[s["region"]]["name"]}で発売（{s["count"]}個入り。日本では購入できません）'
                if s.get("region") else f'「{e(s["name"])}」を発売（{s["count"]}個入り）'))
              for s in stickers if s.get("release_date")]
    items += [(d["date"], f'<span class="t">{e(a["name"])} {e(d["version"])}</span>', e(d["note"]))
             for a in apps for d in a.get("devlog", []) if d.get("date")]
    items.sort(key=lambda x: x[0], reverse=True)
    return "\n".join(f'    <div><span class="d">[{dt}]</span>{label}<span>{note}</span></div>'
                     for dt, label, note in items[:limit])


# 海外限定版。stickers.json の region に入れるコード。販売国はこの1か国のみ（日本では購入できない）
REGIONS = {
    "TW": {"name": "台湾", "lang": "zh-Hant", "price_unit": "NT$"},
    "TH": {"name": "タイ", "lang": "th", "price_unit": "฿"},
}


def region_tag(s):
    """見出しに足す「（台湾限定）」。日本向け（region なし）は空。"""
    return f'（{REGIONS[s["region"]]["name"]}限定）' if s.get("region") else ""


def load_stickers():
    """公開するスタンプセット（visible のもの。日本向けと海外限定版の両方）。"""
    d = json.loads((DATA / "stickers.json").read_text(encoding="utf-8"))
    out = [x for x in d if x.get("visible")]
    for x in out:  # 設定の取り違え（未知の国コード・価格表示の抜け）は、ビルドで止める
        if x.get("region") and x["region"] not in REGIONS:
            raise ValueError(f'stickers.json: {x["slug"]} の region が不明: {x["region"]}')
        if x.get("region") and not x.get("price_label"):
            raise ValueError(f'stickers.json: {x["slug"]} は海外限定版なので price_label（例: "NT$30"）が必要')
    # 新しい販売開始日が上（日付が同じなら、あとから追加した方が上。release_date の無いものは一番下）
    return sorted(reversed(out), key=lambda x: x.get("release_date") or "", reverse=True)


def jp_stickers(sets):
    return [x for x in sets if not x.get("region")]


def overseas_stickers(sets):
    return [x for x in sets if x.get("region")]


NEWB = '<b class="new">NEW</b>'
NEW_DAYS = 7   # 販売開始から何日間、NEWを付けるか


def is_new(x):
    """販売開始日（release_date）から NEW_DAYS 日以内なら True。日本時間で数える（毎朝の自動ビルドで自然に外れる）。"""
    if not x.get("release_date"):
        return False
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).date()
    return 0 <= (today - datetime.date.fromisoformat(x["release_date"])).days <= NEW_DAYS


def nb(name):
    """名前を、カタカナ・漢字・ひらがな・【…】のかたまりに分け、かたまりの途中では折り返さない（「ス/タンプ」「オ/ノマトペ」を防ぐ）。
    1つのかたまりが長すぎて列を押し広げないよう、全体は nowrap にしない。"""
    out = []
    for tok in re.findall(r"【[^】]*】|[ァ-ヶー]+|[一-龠々]+|[ぁ-ん]+|.", name):
        out.append(f'<span style="white-space:nowrap">{e(tok)}</span>' if len(tok) >= 2 else e(tok))
    return "".join(out)


def sticker_toc(sets):
    """スタンプページ先頭の目次。シリーズごとに、各セットへジャンプするチップを並べる（JS不要）。
    シリーズ・短い名前は stickers.json の series / short（無ければ chara / name）。海外限定版は別の行にまとめる。"""
    rows = {}
    for x in sets:   # sets は新しい順。シリーズの行も、最新のセットがあるものが上
        key = f'海外限定版（{"・".join(dict.fromkeys(REGIONS[y["region"]]["name"] for y in sets if y.get("region")))}）' if x.get("region") else x.get("series") or x["chara"]
        rows.setdefault(key, []).append(x)
    out = []
    for label, items in rows.items():
        chips = "".join(
            f'<a href="#{x["slug"]}">{"<b>動く</b>" if x.get("animated") else ""}{e(x.get("short") or x["name"])}{NEWB if is_new(x) else ""}</a>' for x in items)
        out.append(f'    <div class="srow"><span class="lb dot">{e(label)}</span><span class="cs">{chips}</span></div>')
    return f'''  <nav class="stoc" aria-label="スタンプのシリーズ">
    <p class="muted dot">シリーズから探す（全{len(sets)}セット）</p>
{chr(10).join(out)}
  </nav>'''


def sticker_cards(sets):
    return chr(10).join(
        f'    <a class="card" href="/stickers/#{x["slug"]}" style="text-decoration:none"><span class="cap dot">LINE STICKER / {x["count"]}{NEWB if is_new(x) else ""}</span>'
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


STICKER_LEAD = "ドット絵のモンスターから、色で気分が伝わる丸顔まで。毎日のあいさつや返事に使えるスタンプが、いろいろそろったよ！"
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
