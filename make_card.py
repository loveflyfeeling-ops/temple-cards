# -*- coding: utf-8 -*-
"""廟口故事／神明聖誕圖卡 1080x1350（FB 4:5）。
用法：python3 make_card.py "標題（可用\\n換行）" "副標一句" 編號 輸出.png [標章文字]
標章文字預設「廟口故事」；神明生日用「神明聖誕」。"""
import sys, glob
from PIL import Image, ImageDraw, ImageFont
title, sub, no, out = sys.argv[1].replace("\\n", "\n"), sys.argv[2], sys.argv[3], sys.argv[4]
badge = sys.argv[5] if len(sys.argv) > 5 else "廟口故事"
W, H = 1080, 1350
RED, GOLD, INK, CREAM, GREY = (179,38,30), (212,160,23), (26,26,26), (245,239,230), (130,130,130)
cands = ["/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc", "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"] + glob.glob("/usr/share/fonts/**/*CJK*.tt*", recursive=True) + glob.glob("/usr/share/fonts/**/*wqy*.tt*", recursive=True)
def F(sz):
    for p in cands:
        try: return ImageFont.truetype(p, sz, index=0)
        except Exception: pass
    raise SystemExit("no CJK font: apt-get install -y fonts-noto-cjk")
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
for x0 in (40, W - 40):                       # 兩側細紅邊，取代整面紋理（檔案小）
    d.rectangle([x0 - 6, 40, x0 + 6, H - 40], fill=(60, 22, 18))
# 外框（雙線，金）
d.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=4)
d.rectangle([58, 58, W - 58, H - 58], outline=(90, 70, 20), width=2)
# 上方品牌
d.text((W / 2, 140), "台灣廟口研究所", font=F(40), fill=GOLD, anchor="mm")
d.rectangle([W / 2 - 70, 176, W / 2 + 70, 181], fill=RED)
# 紅色印章「廟口故事」
label = f"{badge} No.{no}"
bw = d.textlength(label, font=F(42)) / 2 + 40
d.rounded_rectangle([W / 2 - bw, 230, W / 2 + bw, 310], radius=14, fill=RED)
d.text((W / 2, 270), label, font=F(42), fill=CREAM, anchor="mm")
# 標題（自動縮字，最多兩行）
lines = title.split("\n")[:2]
size = 150
while size > 60 and max(d.textlength(l, font=F(size)) for l in lines) > W - 180:
    size -= 6
lh = size * 1.18
y0 = 640 - lh * (len(lines) - 1) / 2
for i, l in enumerate(lines):
    d.text((W / 2, y0 + i * lh), l, font=F(size), fill=CREAM, anchor="mm")
# 副標（金色，自動縮字）
ss = 54
while ss > 30 and d.textlength(sub, font=F(ss)) > W - 200:
    ss -= 2
d.text((W / 2, 900), sub, font=F(ss), fill=GOLD, anchor="mm")
# 分隔＋免責
d.line([W / 2 - 200, 1080, W / 2 + 200, 1080], fill=(80, 80, 80), width=2)
d.text((W / 2, 1140), "民俗文化分享 · 各地說法不一 · 切勿過度迷信", font=F(30), fill=GREY, anchor="mm")
d.text((W / 2, 1220), "FB｜台灣廟口研究所", font=F(34), fill=(170, 170, 170), anchor="mm")
img.convert("P", palette=Image.ADAPTIVE, colors=32).save(out, optimize=True)  # PNG 32 色，約 30–60KB
print("saved", out)
