"""敵キャラ図鑑のデータ層。出典は lubita-x-autopost/monsters/（private。クローンを読む）。

- 未解放キャラの名前・絵は、公開リポジトリに一切出さない（LOCKED は番号だけ）。
- 解放 = 投稿ログ（monsters/logs/posted.jsonl）に載ったNo.。Xの投稿と同期させるため。
- ローカル確認用: 環境変数 LUBITA_PREVIEW_DATE=YYYY-MM-DD を付けると、投稿ログではなく
  schedule.md の日付がその日以前のものを解放扱いにする（本番ビルドでは付けない）。
"""
import json
import os
import re
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
MONSTERS = Path(os.environ.get("LUBITA_MONSTERS", r"C:\dev\lubita-x-autopost\monsters"))
IMG_OUT = ROOT / "assets" / "img" / "zukan"
PER_FLOOR = 7
CARD_PX = 560  # 表示は最大約255px。2倍＋余裕


def _schedule():
    """schedule.md の表 -> {No: {"date": 'YYYY-MM-DD', "ok": bool}}"""
    rows = {}
    for line in (MONSTERS / "schedule.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*([^|]*?)\s*\|", line)
        if m:
            rows[int(m.group(2))] = {"date": m.group(1), "ok": m.group(3) == "済"}
    return rows


def _posted_nos():
    log = MONSTERS / "logs" / "posted.jsonl"
    nos = set()
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                if rec.get("status") in ("posted", "posted_text_only") and rec.get("no"):
                    nos.add(int(rec["no"]))
    return nos


def load():
    """階層ごとの表示データを返す: [{floor, name, boss, unlocked, total, cards:[...]}] を階層番号順に。"""
    sched = _schedule()
    preview = os.environ.get("LUBITA_PREVIEW_DATE")
    if preview:
        unlocked = {n for n, r in sched.items() if r["ok"] and r["date"] <= preview}
    else:
        unlocked = _posted_nos()

    mons = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((MONSTERS / "data").glob("*.json"))]
    floors = {}
    for m in mons:
        f = floors.setdefault(m["floor"], {"floor": m["floor"], "name": m["floor_name"], "mons": []})
        f["mons"].append(m)

    out, latest_no = [], max(unlocked, default=0)
    for fno in sorted(floors):
        f = floors[fno]
        f["mons"].sort(key=lambda m: m["no"])
        boss = next((m for m in f["mons"] if m["rank"] == 5), None)
        cards = []
        for m in f["mons"]:
            u = m["no"] in unlocked
            cards.append({"no": m["no"], "unlocked": u, "name": m["name"] if u else None,
                          "alt": m["alt"] if u else None, "new": u and m["no"] == latest_no,
                          "src": MONSTERS / m["image"]})
        out.append({"floor": fno, "name": f["name"],
                    "boss": boss["name"] if boss and boss["no"] in unlocked else None,
                    "unlocked": sum(c["unlocked"] for c in cards), "total": PER_FLOOR, "cards": cards})
    return out


def latest_floor(floors):
    """最新階層 = 解放済みが1体でもある最大の階層。無ければ第1階層。"""
    got = [f for f in floors if f["unlocked"]]
    return got[-1] if got else floors[0]


def visible(floors):
    """公開する階層 = 解放済みが1体でもある階層＋最新階層（未開始の階層は名前も出さない）。"""
    latest = latest_floor(floors)
    return [f for f in floors if f["unlocked"] or f is latest]


def sync_images(floors):
    """解放済みの絵だけを assets/img/zukan/NNN.webp に書き出す（古いものは消す）。"""
    if IMG_OUT.exists():
        shutil.rmtree(IMG_OUT)
    IMG_OUT.mkdir(parents=True)
    for f in floors:
        for c in f["cards"]:
            if c["unlocked"]:
                im = Image.open(c["src"]).convert("RGB").resize((CARD_PX, CARD_PX), Image.LANCZOS)
                im.save(IMG_OUT / f"{c['no']:03d}.webp", "WEBP", lossless=True, method=6)
