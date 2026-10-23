"""守るもの（既存URL・設定ファイル）が壊れていないか確認する。使い方: python tools/check_protected.py
- app-ads.txt、CNAME、.nojekyll は「最後のコミットから1バイトも変わっていない」こと
- /privacy/{アプリ名}/ ×6 は存在し、本文が tools/data/privacy/{アプリ名}.html（原稿）と一致していること（URLと本文を守る）
- 404.html は存在すること（見た目の作り直しは可）
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ["gensyu-log", "plants-biyori", "oyatsu-log", "medaka-biyori", "hakko-biyori", "zettai-lock"]
IMMUTABLE = ["app-ads.txt", "CNAME", ".nojekyll"]
PRIVACY = [f"privacy/{a}/index.html" for a in APPS]
MUST_EXIST = IMMUTABLE + PRIVACY + ["404.html"]

ng = []
for rel in MUST_EXIST:
    if not (ROOT / rel).is_file():
        ng.append(f"なくなっている: {rel}")
diff = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", *IMMUTABLE], cwd=ROOT, capture_output=True, text=True).stdout.split()
ng += [f"変更されている: {p}" for p in diff]
for a in APPS:
    page_file = ROOT / f"privacy/{a}/index.html"
    src = (ROOT / f"tools/data/privacy/{a}.html").read_text(encoding="utf-8").rstrip(chr(10))
    if page_file.is_file() and src not in page_file.read_text(encoding="utf-8"):
        ng.append(f"privacy の本文が原稿と一致しない: {a}")
cname = (ROOT / "CNAME").read_bytes()
if cname != b"lubitaworks.com":
    ng.append(f"CNAME が想定と違う: {cname!r}")

if ng:
    print("NG\n" + "\n".join(ng))
    sys.exit(1)
print(f"OK: 保護対象 {len(MUST_EXIST)} 件は無事")
