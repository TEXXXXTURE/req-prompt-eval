# -*- coding: utf-8 -*-
"""req-prompt-eval · AIGC 补充检查器（轻档，配套 v0.1.1 判据包）

与 `static_check.py`（核心，需求向）并列的第二把轻档尺子：核心脚本的词表是需求向的，
拿到生图/生视频提示词上几乎空转（E 自测报告 §5.1：12 条用例 11 条同分 33.3）。
本脚本只做 AIGC 专属、可程序判的检查，**不改核心脚本**（判据包 §一说明 + E·6.2 纪律）。

词表与判据来源（不在脚本里发明词，全部指向判据包）：
  空词六类典型词        → references/判据包-AIGC生图视频.md §7.1（B·§2.6 六类 slop）
  AIGC 模糊词白名单      → 同 §7.4（v0.1.1 新增，修 E·5.2 的 T2 误扣）
  负面词四类 / 行卫生     → 同 §7.2 + 主干 11.6（硬规则）
  景别 / 运镜 / 角度词表  → 同 §7.3（B 已词典化，供 4.1 / 4.2 复核）
  参数误入正文（分档项）  → §一分项 + §六 12.2（冲突 C4，本版只报不扣）
  占位符未填（硬失败）    → 主干 13.0（v0.1.1 新增，对应 B·§2.6 硬失败「空占位符未填」）
  对象类型判别（前置）    → §零·A（v0.1.1 新增：成品 / 方法论模板 / 跨模态）

它不理解语义，只认字面。判「写得好不好」交给中档裁判；本脚本只回答
「有没有空词 / 有没有占位符没填 / 参数混进正文没有 / 负面块卫生不卫生 / 这是不是提示词」。

用法：
  python aigc_check.py <文件> [--json]

输出：人读 AIGC 卡（默认）或 JSON（--json）。返回码恒为 0（除文件不存在）。
"""

import argparse
import json
import pathlib
import re
import sys

# ======================================================================
# 词表（§7.1 空词六类典型词 —— 字面直搬，不扩写）
# ======================================================================

# --- 1 类：空评价词 ---
EMPTY_EVAL = [
    "cinematic", "epic", "stunning", "beautiful", "dynamic", "professional",
    "amazing", "gorgeous", "breathtaking", "impressive", "flawless", "incredible",
]
# --- 2 类：搬运图像模型 token ---
EMPTY_TOKENS = [
    "8k", "32k uhd", "masterpiece", "best quality", "highly detailed", "sharp focus",
    "trending on artstation", "ultra detailed", "uhd", "4k", "hyperdetailed",
    "最佳品质", "高清", "细节丰富", "超高清", "超高分辨率",
]
# --- 5 类：形容词堆叠（同义三连，表内两条）---
SYNONYM_TRIPLES = [
    ("beautiful", "stunning", "gorgeous"),
    ("dramatic", "intense", "powerful"),
]
# class 5 表内词的**单用**也算空词（§7.1 锚点行：`dramatic cinematic noir vibes` 里的 `dramatic`）
EMPTY_EVAL_EXTRA = ["dramatic", "intense", "powerful"]
# --- 6 类：感受后缀词（含中文专属空词表，§7.1 末）---
FEELING_SUFFIX = [
    "电影感", "氛围感", "高级感", "大片感", "质感",
    "vibey", "vibes",   # vibes = vibey 的名词形（§7.1 锚点行）
    "雰囲気のある", "감성적인", "atmosférico", "атмосферный",
]
# 3 类（标签沙拉）只报不判：逗号串无动词 —— 专业写法里也有大量合法逗号串，
# 字面判会误伤（T10 `shot on Kodak Portra 400, soft pastel tones, …`），故只计数提示。

# ======================================================================
# 词表（§7.4 AIGC 模糊词白名单 —— 算模糊词密度前先剔除）
# ======================================================================

VAGUE_WHITELIST = [
    "smooth", "natural", "soft", "clean", "warm", "cool", "sharp",
    "平滑", "自然", "柔和", "干净", "暖", "冷",
]

# 核心脚本 `static_check.py` 的通用模糊词表（此处镜像一份，**只为算白名单差额**：
# 「模糊词（AIGC 口径）」= 核心表命中 − 白名单命中；核心脚本本身不改）。
CORE_VAGUE_ZH = [
    "更好", "更优", "较好", "友好", "好用", "合理", "适当", "尽量", "尽可能",
    "尽快", "美观", "流畅", "出色", "优秀", "良好", "显著", "高效", "灵活",
    "完善", "健壮", "顺滑", "人性化", "智能化", "不错的", "满意", "友好性",
    "用户体验好", "性能好", "足够好", "若干", "部分情况下", "必要时", "视情况而定",
]
CORE_VAGUE_EN = [
    "good", "nice", "better", "fast", "robust", "user-friendly",
    "reasonable", "appropriate", "efficient", "smooth", "flexible",
    "as needed", "if necessary", "etc.",
]

# ======================================================================
# 词表（§7.3 景别 / 运镜 / 角度 —— 供槽痕迹判定）
# ======================================================================

SHOT_SIZE = (r"(?:extreme\s+close-?up|close-?up|medium\s+close-?up|medium\s+full|"
             r"medium\s+shot|two-?shot|over-?the-?shoulder|full\s+shot|wide\s+shot|"
             r"extreme\s+wide|pov|point\s+of\s+view|"
             r"大特写|特写|近景|中近景|中景|中全景|全景|远景|大远景|双人镜头|过肩镜头|主观视角)")
CAMERA_MOVE = (r"(?:push-?\s?in|pull-?\s?back|pullback|dolly(?:\s+(?:in|out|left|right))?|truck|"
               r"whip\s+pan|pan\s+(?:left|right)|tilt|zoom|crane\s+(?:up|down)|orbit|"
               r"follow\s+shot|handheld|steadicam|"
               r"推近|推进|拉远|横移|摇镜|升降|环绕|跟拍|手持|变焦|甩镜)")
CAMERA_ANGLE = r"(?:low\s+angle|high\s+angle|bird'?s[\s-]eye|dutch\s+angle|低角度|高角度|鸟瞰|荷兰角)"

# ======================================================================
# 11 个槽痕迹探测（「提示词该有的槽写没写」——字面层，不判质量）
# ======================================================================

SLOTS = [
    ("主体", re.compile(r"(?<!no\s)\b(hero|character|product|subject|artist|protagonist|"
                        r"woman|man|girl|boy|person|people|model)\b|"
                        r"原创角色|主角|主体|角色|人物|渔夫|咖啡师", re.I)),
    ("动作", re.compile(r"\b(walks?|walked|rotates?|pushes?|lifts?|places?|reach(?:es|ing)|"
                        r"pauses?|reassembl\w*|drops?|turns?\s+away|finishes?|wakes?|runs?|"
                        r"opens?|touches?|stands?|steps?\s+forward)\b|"
                        r"放下|站在|停在|推进|转动|缓慢|打开|触碰|抬起", re.I)),
    ("场景", re.compile(r"\b(chamber|studio|office|corridor|street|scene|setting|backdrop|"
                        r"shelf|room|cliff|window|hall|alley|forest|desk)\b|"
                        r"走廊|室内|场景|背景|环境|走廊|屋顶|海边|街道", re.I)),
    ("镜头", re.compile(SHOT_SIZE + "|" + CAMERA_MOVE + "|" + CAMERA_ANGLE, re.I)),
    ("光照", re.compile(r"\b(lighting|light\s+from|lights?\b|key\s+light|backlight|rim\s+light|"
                        r"tungsten|daylight|dawn|dusk|neon|practical|sunlight|window\s+light)\b|"
                        r"灯光|光源|顶灯|雨光|打光|晨光|逆光", re.I)),
    ("材质", re.compile(r"\b(material|texture|matte|brushed|satin|gloss\w*|clay|ceramic|sheen|"
                        r"reflection|reflective|stone|fabric|metal\w*|glass)\b|"
                        r"材质|质感|镜面|反光|湿|粗糙|光滑", re.I)),
    ("风格", re.compile(r"\b(style|palette|colou?rs?|pastel|tone[s]?|grade|cel-?shading|"
                        r"watercolor|oil\s+painting|cyberpunk|noir|anime|3d\s+cartoon|render)\b|"
                        r"风格|调色|色调|色彩|画风", re.I)),
    ("时序", re.compile(r"\d{1,3}\s*-\s*\d{1,3}\s*s\b|"
                        r"\b(cut\s+to|shot\s+\d|scene\s+\d|stage\s+\d)\b|"
                        r"镜头\s*\d|分镜|第\s*\d\s*段", re.I)),
    ("声音", re.compile(r"\b(audio|sound|dialogue|ambience|ambient|score|music|voiceover|"
                        r"hum|rustling|echo(?:es)?)\b|声音|对白|配乐|音效|音乐|环境声", re.I)),
    ("画质锁定", re.compile(r"\b(visual\s+control|remain\s+unchanged|stays?\s+consistent|"
                            r"keep\s+\w+\s+consistent|preservation|film\s+grain|kodak|portra|"
                            r"anamorphic|\d{2,3}\s?mm|65mm|stable\s+identity|physically\s+plausible)\b|"
                            r"保持一致|保持不变|锁定|稳定主体", re.I)),
    ("参数", re.compile(r"\d{1,3}\s*:\s*\d{1,3}|--[a-z]+|\b\d{1,4}\s?fps\b|"
                        r"(?<![\d-])\b\d{1,4}\s?s\b|\bseed\b|aspect", re.I)),
]

# 占位符未填（主干 13.0）
PLACEHOLDER_PATTERNS = [
    re.compile(r"<[^<>\n]{1,80}>"),        # <subject> / <one primary action or event>
    re.compile(r"\$\{[^}\n]{1,60}\}"),     # ${subject}
    re.compile(r"\[\s*占位\s*\]"),
    re.compile(r"\bXXX+\b"),
    re.compile(r"待填"),
    re.compile(r"\bTODO\b", re.I),
    re.compile(r"\bTBD\b", re.I),
]
# 占位符落在主干槽上（判定硬失败要「集中在主干槽」）
SPINE_SLOT_HINT = re.compile(
    r"(subject|primary event|initial state|end state|video type|story summary|camera|"
    r"grade|audio|character|prop)", re.I)

# 负面槽行头（§7.2 / 主干 11.x）
NEG_HEAD_RE = re.compile(
    r"^\s*(?:[-*•]\s*)?(negative|avoid|exclude|excluded|负面|避免|排除|禁止)\b",
    re.I)
# 旧失败专名痕迹（11.6 不通过项之一）
OLD_FAIL_MARK = re.compile(r"上次|上一版|那张图|之前那版|last\s+time|previous\s+version")

# 参数误入正文（§一 + §六 12.2 分档项，只报不扣）
PARAM_TOKEN = re.compile(
    r"--[a-z]+|(?<![\d:.-])\b\d{1,3}\s*:\s*\d{1,3}\b|\b\d{1,4}\s?fps\b|"
    r"(?<![\d-])\b\d{1,4}\s?s\b|\b\d{3,4}\s?x\s?\d{3,4}\b|\b(?:4k|8k|32k\s?uhd)\b|"
    r"\bseed\b|--ar|--s\b|--no\b", re.I)

# 对象类型判别（§零·A）
META_METHOD = re.compile(
    r"模板|公式|你可以|示例|以下|用于默认|区分规则|不强制|写法|方法|规范|指南|填空|"
    r"请按|建议|命名|槽位|"
    r"\[Generation\s+Goal\]|\[Stage\s+\d\]|APPLIES\s+TO\s+EVERY\s+SHOT|Maintain\s+Consistency|"
    r"Initial\s+state:|Primary\s+event:|End\s+state:|template|framework|you\s+can|guide",
    re.I)
META_CROSSMODAL = re.compile(
    r"style\s+of\s+music|instrumentation|tempo|bpm|key\s*:|lyrics|\[verse|\[chorus|\[intro|"
    r"\[pre-chorus|chord|soundfont|suno|udio\b|spotify|"
    r"和弦|歌词|编曲|人声|混音|旋律|"
    r"\bdef\s|\bimport\s|\bclass\s|\bfunction\s|\breturn\s|代码|函数|脚本",
    re.I)


def find_hits(patterns, text):
    """返回命中的 (词, 次数)。中文按子串数，英文按词边界。"""
    hits = []
    low = text.lower()
    for p in patterns:
        if re.fullmatch(r"[a-zA-Z\s.-]+", p):
            n = len(re.findall(r"\b" + re.escape(p.lower()) + r"\b", low))
        else:
            n = text.lower().count(p.lower())
        if n:
            hits.append((p, n))
    return hits


def visible(text):
    return len(re.sub(r"\s", "", text))


_DUR_RE = re.compile(r"^(\d{1,4})\s?s$", re.I)


def _is_decade(tok):
    """`\d+s` 有两种意思：时长（10s / 15s）与年代（`80s Japanese`）。
    只有 ≤ 60 秒才算时长参数，其余当年代写作放过（避免 T11 的 `80s Japanese` 误报）。"""
    m = _DUR_RE.match(tok.strip())
    return bool(m) and int(m.group(1)) > 60


def iter_lines(text):
    return text.splitlines()


def is_neg_head(line):
    return bool(NEG_HEAD_RE.match(line))


def collect_neg_blocks(text):
    """负面槽 = 以 negative/Avoid/负面… 起头的行，加上紧随其后的续行（非空、非新槽/新标题）。"""
    lines = iter_lines(text)
    blocks, cur = [], None
    for ln in lines:
        if is_neg_head(ln):
            if cur:
                blocks.append(cur)
            cur = [ln]
        elif cur is not None:
            s = ln.strip()
            if not s:
                blocks.append(cur)
                cur = None
            elif s.startswith("#") or (s.startswith("[") and s.endswith("]")):
                blocks.append(cur)
                cur = None
            else:
                cur.append(ln)
    if cur:
        blocks.append(cur)
    return blocks


def neg_item_count(block_text):
    """负面项数：按逗号 / 顿号 / 分号 / 斜杠切，去掉行头标签。"""
    body = NEG_HEAD_RE.sub("", block_text)          # 去「Avoid:」标签
    body = re.sub(r"^\s*[:：]\s*", "", body)
    parts = [p.strip() for p in re.split(r"[,，、;；/]", body)]
    return len([p for p in parts if p])


def strip_neg_lines(text):
    """去掉负面槽行（负面不该算进正向槽痕迹与正向空词）。"""
    keep = []
    for ln in iter_lines(text):
        if is_neg_head(ln):
            continue
        keep.append(ln)
    return "\n".join(keep)


def analyze(text):
    chars = visible(text)
    lines = iter_lines(text)
    positive = strip_neg_lines(text)                # 正向正文（不含负面槽行）

    # ---------- 1. 占位符未填（13.0 硬失败） ----------
    ph_hits = []
    for pat in PLACEHOLDER_PATTERNS:
        for m in pat.finditer(text):
            ph_hits.append(m.group(0))
    ph_spine = sum(1 for h in ph_hits if SPINE_SLOT_HINT.search(h))
    hard_placeholder = bool(ph_hits) and (len(ph_hits) >= 5 or ph_spine >= 3)

    # ---------- 2. 空词六类 ----------
    empty = []
    for w, n in find_hits(EMPTY_EVAL, positive):
        empty.append(("1 空评价词", w, n))
    for w, n in find_hits(EMPTY_EVAL_EXTRA, positive):
        empty.append(("5 形容词堆叠·单用", w, n))
    for w, n in find_hits(EMPTY_TOKENS, positive):
        empty.append(("2 搬运 token", w, n))
    # 3 类 标签沙拉：只报不判
    salad_lines = []
    for ln in lines:
        if is_neg_head(ln) or not ln.strip():
            continue
        toks = [t.strip() for t in re.split(r"[,，]", ln) if t.strip()]
        if len(toks) >= 6 and not re.search(
                r"\b(is|are|was|were|has|have|walks|rotates|pushes|lifts|places|"
                r"打开|放下|站在|停在|推进)\b", ln, re.I):
            salad_lines.append(ln.strip())
    # 4 类 否定 slop：`no X` / `不要X` 写在正向正文里（非负面槽行）
    neg_slop = re.findall(r"(?<![\w-])no\s+[a-z][a-z\s-]{1,20}", positive, re.I) \
        + re.findall(r"不要[^\s，。；]{1,10}|不是[^\s，。；]{1,10}", positive)
    for w in neg_slop:
        empty.append(("4 否定 slop", w.strip(), 1))
    # 5 类 同义三连
    for tri in SYNONYM_TRIPLES:
        if all(re.search(r"\b" + w + r"\b", positive, re.I) for w in tri):
            empty.append(("5 形容词堆叠", "/".join(tri), 1))
    # 6 类 感受后缀词
    for w, n in find_hits(FEELING_SUFFIX, positive):
        empty.append(("6 感受后缀词", w, n))

    empty_total = sum(n for _, _, n in empty)
    empty_density = empty_total / chars * 1000 if chars else 0.0
    empty_score = max(0.0, 100.0 - empty_density * 10)

    # ---------- 3. 参数误入正文（分档项：只报不扣） ----------
    param_hits, param_inline = [], []
    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            continue
        toks = [t for t in PARAM_TOKEN.findall(ln) if not _is_decade(t)]
        if not toks:
            continue
        segs = max(1, len([s for s in re.split(r"[,，;；]", ln) if s.strip()]))
        param_hits.append({"行": i, "命中": toks})
        if len(toks) / segs < 0.6:                 # 参数不是独立行 → 混在散文里
            param_inline.append({"行": i, "命中": toks, "原文": ln.strip()[:90]})

    # ---------- 4. 负面行卫生（硬规则 11.6） ----------
    blocks = collect_neg_blocks(text)
    neg_info = {"负面行数": len(blocks)}
    if blocks:
        counts = [neg_item_count("\n".join(b)) for b in blocks]
        max_items = max(counts)
        longest = max(len(re.sub(r"\s", "", "\n".join(b))) for b in blocks)
        old_marks = OLD_FAIL_MARK.findall(text)
        if max_items <= 8:
            grade, hygiene = "合格（紧凑行）", 100.0
        elif max_items <= 12:
            grade, hygiene = "偏长（建议压缩）", 60.0
        else:
            grade, hygiene = "不合格（长清单）", 0.0
        if old_marks:
            hygiene = max(0.0, hygiene - 20.0 * len(old_marks))
        neg_info.update({"每块项数": counts, "最大项数": max_items,
                         "最长块字符数": longest, "旧专名痕迹": old_marks,
                         "评级": grade, "卫生分": hygiene})
    else:
        neg_info.update({"每块项数": [], "最大项数": 0, "最长块字符数": 0,
                         "旧专名痕迹": [], "评级": "不适用（无负面槽）",
                         "卫生分": None})

    # ---------- 5. 槽痕迹（11 槽） ----------
    slot_hits = [name for name, pat in SLOTS if pat.search(positive)]
    slot_missing = [name for name, _ in SLOTS if name not in slot_hits]
    slot_score = len(slot_hits) / len(SLOTS) * 100

    # ---------- 6. 对象类型判别（§零·A） ----------
    meta_n = len(META_METHOD.findall(text))
    cross_n = len(META_CROSSMODAL.findall(text))
    if hard_placeholder:
        obj_type = "疑似占位符模板（未填）→ 硬失败优先"
    elif cross_n >= 3:
        obj_type = "疑似跨模态（音乐/声音/代码）→ 不打分，另立包"
    elif meta_n >= 3:
        obj_type = "疑似方法论模板（教人写词，不是成品词）→ 不打分"
    else:
        obj_type = "成品提示词 → 正常打分"

    # ---------- 7. 模糊词（AIGC 口径 = 核心表 − §7.4 白名单） ----------
    core_hits = find_hits(CORE_VAGUE_ZH, text) + find_hits(CORE_VAGUE_EN, text)
    core_total = sum(n for _, n in core_hits)
    wl_total = sum(n for _, n in find_hits(VAGUE_WHITELIST, text))
    aigc_vague = max(0, core_total - wl_total)
    aigc_density = aigc_vague / chars * 1000 if chars else 0.0
    aigc_vague_score = max(0.0, 100.0 - aigc_density * 10)

    # ---------- 汇总判定 ----------
    scored = {"空词分": round(empty_score, 1), "槽痕分": round(slot_score, 1)}
    if neg_info["卫生分"] is not None:
        scored["负面卫生分"] = round(neg_info["卫生分"], 1)
    unscored = dict(scored)          # 不打分时留参考，不进总分

    if hard_placeholder:
        verdict = f"不通过（硬失败：占位符未填 {len(ph_hits)} 处）"
        total = 0.0
        scoreable = False
    elif obj_type.startswith("疑似跨模态") or obj_type.startswith("疑似方法论"):
        verdict = "不打分（对象类型非成品提示词）"
        total = None
        scoreable = False
    else:
        total = round(sum(scored.values()) / len(scored), 1)
        scoreable = True
        verdict = "偏低" if total < 50 else ("中" if total < 75 else "中高/高")
    if not scoreable:
        scored = {}                  # 不打分：分项不进卡面，只留「未计分参考」

    return {
        "字符数": chars,
        "对象类型": obj_type,
        "对象类型依据": {"方法论特征词": meta_n, "跨模态特征词": cross_n},
        "占位符未填": {"硬失败": hard_placeholder, "处数": len(ph_hits),
                       "落在主干槽": ph_spine, "例": ph_hits[:6]},
        "空词": {"总数": empty_total, "每千字": round(empty_density, 2),
                 "明细": [{"类": c, "词": w, "次数": n} for c, w, n in empty]},
        "标签沙拉行": salad_lines,
        "参数误入正文": {"疑似混入散文": param_inline, "全部参数行": param_hits,
                         "口径": "分档项（§六 12.2，冲突 C4）——只报不扣"},
        "负面行卫生": neg_info,
        "槽痕迹": {"命中": slot_hits, "缺失": slot_missing,
                   "命中数": len(slot_hits), "总槽数": len(SLOTS)},
        "模糊词AIGC口径": {"核心表命中": core_total, "白名单剔除": wl_total,
                           "修后": aigc_vague, "每千字": round(aigc_density, 2),
                           "修后分": round(aigc_vague_score, 1)},
        "分项": scored,
        "未计分参考": unscored,
        "总分": total,
        "可打分": scoreable,
        "判定": verdict,
    }


def print_card(path, r):
    print("== req-prompt-eval AIGC 卡（轻档·v0.1.1 判据包）==")
    print(f"对象: {path}")
    print(f"字符 {r['字符数']} ｜ 对象类型: {r['对象类型']}")
    d = r["对象类型依据"]
    print(f"  类型依据: 方法论特征词 {d['方法论特征词']} ｜ 跨模态特征词 {d['跨模态特征词']}")
    if r["占位符未填"]["硬失败"]:
        p = r["占位符未填"]
        print(f"!! 占位符未填（主干 13.0 硬失败）: {p['处数']} 处，其中落在主干槽 {p['落在主干槽']} 处")
        print(f"   例: {'、'.join(p['例'])}")
    else:
        print("占位符未填: 否（{} 处）".format(r["占位符未填"]["处数"]))
    e = r["空词"]
    print(f"空词: {e['总数']} 个（每千字 {e['每千字']}）")
    for it in e["明细"][:10]:
        print(f"  - [{it['类']}] {it['词']}×{it['次数']}")
    if r["标签沙拉行"]:
        print(f"标签沙拉候选（只报）: {len(r['标签沙拉行'])} 行")
    pi = r["参数误入正文"]["疑似混入散文"]
    print(f"参数误入正文（分档项，只报不扣）: {len(pi)} 行")
    for it in pi[:5]:
        print(f"  - L{it['行']}: {'、'.join(it['命中'])} ｜ {it['原文']}")
    n = r["负面行卫生"]
    line = (f"负面行卫生（硬规则 11.6）: 负面行 {n['负面行数']} ｜ "
            f"最大项数 {n['最大项数']} ｜ 最长 {n['最长块字符数']} 字 ｜ {n['评级']}")
    print(line)
    if n["旧专名痕迹"]:
        print(f"  旧失败专名痕迹: {'、'.join(n['旧专名痕迹'])}")
    s = r["槽痕迹"]
    print(f"槽痕迹: {s['命中数']}/{s['总槽数']} ｜ 缺失: {'、'.join(s['缺失']) or '无'}")
    v = r["模糊词AIGC口径"]
    print(f"模糊词（AIGC 口径 = 核心表 {v['核心表命中']} − 白名单 {v['白名单剔除']}）"
          f": {v['修后']} 个（每千字 {v['每千字']}）")
    print("---")
    for k, val in r["分项"].items():
        print(f"{k}: {val}")
    print(f"总分: {'—（不打分）' if r['总分'] is None else r['总分']}")
    print(f"判定: {r['判定']}")
    print("（本卡只给判断不给改写；对象类型非成品的记「不打分」，中档裁判见判据包§五）")


def main():
    ap = argparse.ArgumentParser(description="AIGC 提示词补充检查（轻档，配套 v0.1.1 判据包）")
    ap.add_argument("file", help="被测文件（提示词原文，Markdown 或纯文本）")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    args = ap.parse_args()

    p = pathlib.Path(args.file)
    if not p.is_file():
        sys.exit(f"文件不存在: {p}")
    text = p.read_text(encoding="utf-8")

    r = analyze(text)
    result = {"file": str(p), **r}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_card(str(p), r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
