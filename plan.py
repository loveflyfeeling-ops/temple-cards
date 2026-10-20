# -*- coding: utf-8 -*-
"""今天要發什麼？ 用法：python3 plan.py [YYYY-MM-DD]（省略＝今天 Asia/Taipei）
規則：農曆日期在 DEITY 表內 → 發「神明聖誕」；否則發廟口主題（只用非神明日計數，主題不會被跳過）。
需要：pip install lunardate"""
import sys, datetime
from lunardate import LunarDate

START = datetime.date(2026, 10, 21)          # 廟口故事 No.1

TOPICS = [
    "廟口石獅子為什麼一公一母、怎麼分", "廟門門神：秦叔寶、尉遲恭與其他門神", "擲筊的由來與聖筊、笑筊、陰筊",
    "進廟「龍邊進、虎邊出」的規矩", "金紙怎麼分：壽金、刈金、福金", "媽祖遶境為什麼大家要鑽轎腳",
    "為什麼廟口總有小吃攤（廟埕與市集）", "安太歲的由來與意義", "平安符的由來與保存習俗",
    "拜拜為什麼常用三炷香", "廟頂上的剪黏與交趾陶", "虎爺為什麼在供桌底下",
    "中元普渡與放水燈", "籤詩怎麼看、為什麼要解籤", "東港迎王與王船祭",
    "台東炸寒單", "鹽水蜂炮的由來", "城隍廟的算盤與「你來了」匾額",
    "月老與紅線", "文昌帝君與考生拜拜", "關公為什麼紅臉",
    "註生娘娘與婆姐", "八家將", "宋江陣",
    "廟埕：古早的社區中心", "拜拜供品的常見禁忌（如芭樂、番茄的說法）", "爐主怎麼選：擲筊選爐主",
    "還願與謝籤", "土地公廟為什麼那麼多", "廟裡的香爐與「過爐」",
]

# 農曆 (月, 日): 神明（每天只放一位主角；同日多位用「、」）
DEITY = {
    (1, 1): "彌勒尊佛佛辰", (1, 6): "清水祖師聖誕", (1, 9): "玉皇上帝萬壽（天公生）", (1, 15): "上元天官大帝聖誕",
    (2, 2): "福德正神千秋（土地公生）", (2, 3): "文昌帝君聖誕", (2, 15): "太上老君聖誕", (2, 19): "觀世音菩薩聖誕",
    (3, 3): "玄天上帝萬壽", (3, 15): "保生大帝聖誕", (3, 20): "註生娘娘千秋", (3, 23): "天上聖母（媽祖）聖誕",
    (3, 28): "東嶽大帝聖誕",
    (4, 8): "釋迦牟尼佛聖誕", (4, 14): "孚佑帝君（呂洞賓）聖誕", (4, 26): "神農大帝聖誕、南鯤鯓李府千歲千秋",
    (5, 13): "霞海城隍爺、關平太子聖誕",
    (6, 6): "虎爺聖誕", (6, 19): "觀世音菩薩得道紀念日", (6, 24): "關聖帝君聖誕",
    (7, 7): "七星娘娘（七娘媽）聖誕", (7, 15): "中元地官大帝聖誕", (7, 30): "地藏王菩薩聖誕",
    (8, 3): "九天司命灶君千秋", (8, 15): "月下老人、太陰星君聖誕", (8, 22): "廣澤尊王千秋", (8, 27): "至聖先師孔子聖誕",
    (9, 9): "中壇元帥（三太子）聖誕", (9, 13): "孟婆尊神千秋", (9, 15): "女媧娘娘萬壽、五府千歲吳三王聖誕",
    (9, 18): "倉聖先師千秋", (9, 19): "觀世音菩薩出家紀念日", (9, 28): "五顯大帝聖誕",
    (10, 5): "達摩祖師聖誕", (10, 15): "下元水官大帝聖誕", (10, 18): "地母至尊千秋", (10, 22): "青山靈安尊王千秋",
    (11, 11): "太乙救苦天尊聖誕", (11, 17): "阿彌陀佛聖誕",
    (12, 8): "釋迦牟尼佛成道日", (12, 16): "福德正神千秋（尾牙）",
}
CN = "〇一二三四五六七八九十"


def lunar_cn(m, d):
    mm = "正" if m == 1 else ("臘" if m == 12 else ("十一" if m == 11 else ("十" if m == 10 else CN[m])))
    if d <= 10:
        dd = "初" + ("十" if d == 10 else CN[d])
    elif d < 20:
        dd = "十" + CN[d - 10]
    elif d == 20:
        dd = "二十"
    elif d < 30:
        dd = "廿" + CN[d - 20]
    else:
        dd = "三十"
    return f"農曆{mm}月{dd}"


def deity_of(day):
    ld = LunarDate.fromSolarDate(day.year, day.month, day.day)
    if getattr(ld, "isLeapMonth", False):
        return None, ld
    return DEITY.get((ld.month, ld.day)), ld


def plan(day):
    no = (day - START).days + 1
    name, ld = deity_of(day)
    if name:
        return {"date": str(day), "no": no, "kind": "神明聖誕", "deity": name,
                "lunar": lunar_cn(ld.month, ld.day)}
    k = sum(1 for i in range((day - START).days)
            if not deity_of(START + datetime.timedelta(days=i))[0])
    return {"date": str(day), "no": no, "kind": "廟口故事", "topic": TOPICS[k % len(TOPICS)],
            "lunar": lunar_cn(ld.month, ld.day)}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        today = datetime.date.fromisoformat(sys.argv[1])
    else:
        today = (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).date()
    import json, warnings
    warnings.filterwarnings("ignore")
    print(json.dumps(plan(today), ensure_ascii=False))
