# -*- coding: utf-8 -*-
"""req-prompt-eval · AIGC 补充检查器（轻档，配套 **v0.2** 判据包）

与 `static_check.py`（核心，需求向）并列的第二把轻档尺子：核心脚本的词表是需求向的，
拿到生图/生视频提示词上几乎空转（E 自测报告 §5.1：12 条用例 11 条同分 33.3）。
本脚本只做 AIGC 专属、可程序判的检查，**不改核心脚本**（判据包 §一说明 + E·6.2 纪律）。

【v0.2 合分口径（负责人已定，判据包§一 + SKILL.md 同步）】
  AIGC 场景以**本脚本的「主分」为主分**；`static_check.py` 的总分**降为参考栏**
  （它的词表是需求向的，对生图/生视频提示词几乎不命中，只作体检记录，不参与排序）。
  卡面把「主分」与「参考栏」分开标，两者不平均、不加权。

【v0.2 档位开关（判据包§六 6.1）】
  `--tier advanced|platform`（默认 platform）
    advanced = 进阶档（物理描写派）  ：空词不豁免、密度曲线更严
    platform = 平台档（国内厂商预设派）：厂商官方词表原词视为平台语料，不计空词
  档位差异**只**由「空词豁免 + 空词密度曲线」产生（这是 D·③-C1 的冲突面），
  其余分档项（2.2 / 5.2 / 6.1 / 8.2 / 12.2）在卡面「分档栏」里报两档判定。
  这样同一提示词两档的分差**可解释**：`阿里 8K 例在平台档不扣、进阶档扣`。

【主分口径（v0.2 重定，含校准依据）】
  主分 = mean(适用项)：
    1. 反模式分（13.1，含 10.3 子分）—— tier 豁免 + 分档曲线（见阈值校准表）
    2. 负面卫生分（硬规则 11.6）—— 仅在有负面槽时适用
    3. 参数分（12.1/12.2）—— 仅有参数时适用；参数自相矛盾 = 0，否则 100
    4. 情绪可拍摄分（2.2，分档）—— 仅在出现情绪词时适用
  硬闸：
    · 13.0 占位符未填（硬失败）→ 主分 0、判「不通过」
    · 11.6 卫生不合格（旧失败专名 / >15 项长清单）→ 主分帽 34（硬规则「违反即扣」）
  退出主分的项（v0.2 决定，勘误记录见校准报告）：
    · **槽痕分** → 进「体检栏」。理由：槽痕分是「槽写没写」的字面计数，短提示词
      （中文紧凑例、胶片片段）天然低分、长模板天然高分，留在主分会让正反例无法分开
      （E2 报告 §六-7 已建议「槽痕分只做体检、不做判据」）。
    · **2.2/5.2/6.1/8.2/12.2 的「内联 vs 分离」面** → 分档栏；只有拿到净正反例锚点的
      分档项才进主分（2.2 有 N14↔P03/P13；12.2-矛盾 有 N12↔P25）。

词表与判据来源（不在脚本里发明词，全部指向判据包）：
  空词六类典型词        → references/判据包-AIGC生图视频.md §7.1（B·§2.6 六类 slop）
  AIGC 模糊词白名单      → 同 §7.4（v0.1.1 新增，修 E·5.2 的 T2 误扣）
  负面词四类 / 行卫生     → 同 §7.2 + 主干 11.6（硬规则）
  景别 / 运镜 / 角度词表  → 同 §7.3（B 已词典化，供 4.1 / 4.2 复核）
  参数误入正文（分档项）  → §一分项 + §六 12.2（冲突 C4）
  占位符未填（硬失败）    → 主干 13.0（对应 B·§2.6 硬失败「空占位符未填」）
  对象类型判别（前置）    → §零·A（成品 / 方法论模板 / 跨模态）
  参考素材型身份锁定      → 主干 1.2 双口径 + 1.3（v0.2 修 E·5.7；B-素材原文 L10547）
  平台语料豁免表          → C·§3.1（火山 `高清，细节丰富，电影质感，色彩自然，光影柔和`；
                            阿里 `8K`/`32k UHD`/`最佳品质`/`超高清`）+ D·③-C1
  档位规则与阈值校准      → research/E3-v02校准报告.md（正反例各 ≥20 条实测）

它不理解语义，只认字面。判「写得好不好」交给中档裁判；本脚本只回答
「有没有空词 / 有没有占位符没填 / 参数混进正文没有 / 负面块卫生不卫生 / 这是不是提示词」。

用法：
  python aigc_check.py <文件> [--tier advanced|platform] [--json] [--no-static]

输出：人读 AIGC 卡（默认）或 JSON（--json）。返回码恒为 0（除文件不存在）。
"""

import argparse
import importlib.util
import json
import pathlib
import re
import sys

VERSION = "v0.2"

# ======================================================================
# 阈值校准表（v0.2，全部由 research/E3-校准样本/ 实测得出）
# 每项写「旧值 → 新值」与支撑数据，改阈值必须能指回这里。
# ======================================================================

# ① 对象类型判别线（旧：方法论特征词计数 ≥3 → 新：强信号「框架词」≥2）
#    校准数据：真实方法论样本 T06 旧计数 4（正确触发）；构造探针 N28 旧计数 5（误触发）。
#    拆成强信号/弱信号后：T06 强=3 触发；N28 强=0、弱=5 不触发。
META_STRONG_THRESHOLD = 2

# ② 跨模态线（计数 ≥3 保留；但修 `udio` 误匹配 `studio`/`Audio` 的字面 bug）
CROSSMODAL_THRESHOLD = 3

# ③ 负面卫卫生三档（旧：≤8 / 9–12 / >12 → 新：≤8 / 9–15 / >15；旧专名痕迹 → 直接不合格）
NEG_OK_MAX_ITEMS = 8
NEG_LONG_MAX_ITEMS = 15

# ④ 独立参数行判定线（旧：命中数/分句数 < 0.6 记为混入散文 →
#    新：**去掉参数 token 后该行剩余可见字符 ≤ 15** 才算独立参数行）
#    校准数据：独立参数行样本 P25 剩余 7 字 → 独立；散文混入样本 N11 剩余 70、
#    N27 剩余 41、官方模板行 P01 剩余 108 → 混入。旧口径在 N11 上给 1.17（误判为独立行）。
PARAM_LINE_MAX_REST = 15

# ⑤ 空词 / 反模式密度扣分曲线（旧：max(0, 100 − 密度×10) → 新：分档台阶，两档不同）
#    校准数据（每千字空词数）：正例最高 3.9（P12）／4.7（P07 方法论，不打分）；
#    反例最低 20.8（N11）。5–20 之间无样本 → 台阶段落在此区间，正反例各留 1 档余量。
EMPTY_CURVE_ADV = [(2, 100.0), (5, 85.0), (10, 60.0), (20, 30.0)]   # 进阶档
EMPTY_CURVE_PLAT = [(3, 100.0), (6, 85.0), (12, 60.0), (20, 30.0)]  # 平台档（更宽一档）

# 硬闸
HARD_RULE_CAP = 34.0     # 11.6 卫生不合格（硬规则）→ 主分帽
MIN_ITEM_STEP = 1.0

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
    "最佳品质", "高清", "细节丰富", "超高清", "超高分辨率", "超高清晰度",
]
# --- 平台语料豁免表（C·§3.1 厂商官方词表原词；仅**平台档**生效）---
#     D·③-C1：阿里官方示例正面使用 `8K / 32k UHD / 最佳品质`，火山给 `高清，细节丰富，
#     电影质感，色彩自然，光影柔和` 模板 → 平台档视为平台语料，不计空词。
PLATFORM_CORPORA = [
    "32k超高清", "32k uhd", "超高清晰度", "超高分辨率", "超高清", "高清相机",
    "高清", "细节丰富", "最佳品质", "电影质感", "色彩自然", "光影柔和", "色调温暖",
    "8k", "uhd", "4k",
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
# 分档子类（§六 6.1）用词表 —— 2.2 / 5.2 / 6.1 / 8.2 / 12.2
# ======================================================================

# 2.2 情绪可拍摄化：抽象情绪词（须外化为生理/姿态线索）
EMOTION_WORDS = [
    "情绪", "情感", "开心", "快乐", "高兴", "生气", "愤怒", "愤怒", "悲伤", "难过", "委屈",
    "紧张", "焦虑", "激动", "兴奋", "害怕", "恐惧", "惊讶", "惊喜", "厌恶", "困惑",
    "骄傲", "失落", "冷漠", "无奈", "失望", "羡慕", "嫉妒", "平静", "压抑", "崩溃",
    "tense", "angry", "sad", "anxious", "joyful", "fearful", "nervous", "upset",
    "emotionally charged", "distressed", "ecstatic", "desperate", "cold and firm",
    "determined", "playful", "suspenseful", "tense expression", "tension",
]
# 可拍摄线索（眼动/眉张力/嘴形/呼吸/视线/手部/姿态 —— B·§2.5）
SHOOTABLE_CUES = [
    "视线", "眼神", "眼光", "眼", "眉", "嘴", "唇", "鼻", "下颌", "下巴",
    "肩", "手", "指", "呼吸", "胸腔", "躯干", "重心", "肌", "颤抖", "姿态",
    "身体", "面部", "表情", "目光", "姿势",
    "gaze", "eyebrow", "lip", "breath", "hand", "finger", "shoulder", "posture",
    "body language", "jaw", "trembl", "blink", "chin", "expression", "gesture", "stance",
]

# 5.2 色温 / 调色板比例
COLOR_TEMP = r"(?:\d{3,4}\s*K\b|色温|白平衡|kelvin)"
PALETTE_RATIO = r"(?:\d{1,3}\s*%[^。\n]{0,6}\d{1,3}\s*%|\d{1,3}\s*[/／]\s*\d{1,3}\s*[/／]\s*\d{1,3})"
PLATFORM_TONE_WORDS = [
    "色调温暖", "光影柔和", "暖色调", "冷色调", "青橙", "teal-and-amber", "黄金时刻",
    "冷色", "暖色", "低饱和", "高饱和", "反差", "胶片颗粒",
]

# 6.1 材质 / 纹理 / 表面响应
MATERIAL_WORDS = [
    "材质", "纹理", "表面", "磨砂", "哑光", "釉", "陶瓷", "木", "金属", "玻璃", "石",
    "布", "皮革", "纸", "粘土", "纤维", "漆",
    "material", "texture", "matte", "brushed", "satin", "gloss", "clay", "ceramic",
    "fabric", "metal", "glass", "stone", "paper", "leather",
]
MATERIAL_RESPONSE = [
    "反光", "反射", "光泽", "倒影", "高光", "颗粒", "阴影",
    "sheen", "reflection", "reflective", "specular", "grain", "highlight", "gloss",
]

# 8.2 时间戳 / 时间预算
TIMECODE = r"\d{1,3}(?:\.\d)?\s*-\s*\d{1,3}(?:\.\d)?\s*s\b"
SHOT_INDEX = r"(?:镜头\s*\d|分镜|第\s*\d\s*段|shot\s*\d|scene\s*\d|stage\s*\d|\[Stage\s*\d)"
OVER_PRECISE_TIME = r"(?:精确|framing\s+at|at\s+exactly)[^。\n]{0,8}?\d{1,3}(?:\.\d+)?\s*(?:秒|s\b)"

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
OLD_FAIL_MARK = re.compile(r"上次|上一版|上版|那张图|之前那版|之前那版|旧版|last\s+time|previous\s+version")

# 参数 token（§一 + §六 12.2 分档项）
PARAM_TOKEN = re.compile(
    r"--[a-z]+|(?<![\d:.-])\b\d{1,3}\s*:\s*\d{1,3}\b|\b\d{1,4}\s?fps\b|"
    r"(?<![\d-])\b\d{1,4}\s?s\b|\b\d{3,4}\s?x\s?\d{3,4}\b|\b(?:4k|8k|32k\s?uhd)\b|"
    r"\bseed\b|--ar|--s\b|--no\b", re.I)
# v0.2：进「参数分 / 独立参数行判定」只用**严格参数语法**（`--flag`、宽高比、时长、fps、seed）。
# 裸分辨率词（`4K / 8K / 32k UHD`）虽然 §一也把它们列为「参数误入正文」的正则，
# 但它们同时是空词六类第 2 类（搬运图像模型 token）——两处都算会把同一处稀释两次，
# 校准样本 N05（纯空词堆叠）因此拿到「参数分 100」把主分从 0 抬到 50。故：
#   · 空词层（13.1）照 §7.1 计 class 2；
#   · 参数层只认严格语法，裸分辨率词仍进「全部参数行」报告栏（只报）。
PARAM_TOKEN_STRICT = re.compile(
    r"--[a-z]+|(?<![\d:.-])\b\d{1,3}\s*:\s*\d{1,3}\b|\b\d{1,4}\s?fps\b|"
    r"(?<![\d-])\b\d{1,4}\s?s\b|\b\d{3,4}\s?x\s?\d{3,4}\b|\bseed\b", re.I)
ASPECT_TOKEN = re.compile(r"\b\d{1,3}\s*[:：]\s*\d{1,3}\b")
FPS_TOKEN = re.compile(r"\b\d{1,4}\s?fps\b", re.I)

# 对象类型判别（§零·A，v0.2 拆强/弱信号）
META_METHOD_STRONG = re.compile(
    r"模板|公式|槽位|填空|区分规则|不强制|用于默认|规范|指南|"
    r"\[Generation\s+Goal\]|\[Stage\s+\d\]|APPLIES\s+TO\s+EVERY\s+SHOT|"
    r"Maintain\s+Consistency|Initial\s+state:|Primary\s+event:|End\s+state:|"
    r"\btemplate\b|\bframework\b|\bguide\b", re.I)
META_METHOD_WEAK = re.compile(
    r"以下|建议|示例|你可以|请按|写法|方法|命名|\byou\s+can\b|\bexample\b", re.I)
META_CROSSMODAL = re.compile(
    r"style\s+of\s+music|instrumentation|\btempo\b|\bbpm\b|\bkey\s*:|lyrics|\[verse|\[chorus|\[intro|"
    r"\[pre-chorus|chord|soundfont|\bsuno\b|\budio\b|spotify|"
    r"和弦|歌词|编曲|人声|混音|旋律|"
    r"\bdef\s|\bimport\s|\bclass\s|\bfunction\s|\breturn\s|代码|函数|脚本", re.I)

# 参考素材指代（修 E·5.7：素材承担身份时 1.2 不再按散文静态特征判）
ASSET_REF = re.compile(
    r"(?:\[\s*Image\s*\d\s*\]|\[\s*Video\s*\d\s*\]|\[\s*Audio\s*\d\s*\]|"
    r"\{\{\s*Image\s*\d\s*\}\}|\{\{\s*Video\s*\d\s*\}\}|\{\{\s*Audio\s*\d\s*\}\}|"
    r"@\s*(?:图|图片|视频|音频)\s*\d|@\s*[Ii]mage\s*\d|@\s*[Vv]ideo\s*\d|@\s*[Aa]udio\s*\d|"
    r"@image\d|@video\d|@audio\d)", re.I)
ASSET_USE_DECL = re.compile(
    r"(?:为[^\n。；]{0,12}参考|用于[^\n。；]{0,20}|参考[^\n。；]{0,10}的|作为[^\n。；]{0,8}"
    r"(?:首帧|尾帧|参考)|为\s*(?:首帧|尾帧)|锁定[^\n。；]{0,12}|严格保持|保持不变|"
    r"保持[^\n。；]{0,12}不变|延展|延长|继承|沿用|融合|配合|锁住|保持|"
    r"\bdefines\b|\bas\s+first\s+frame\b|\bas\s+last\s+frame\b|\bpreserve\b|\breference\b|"
    r"\bextend\b|\bcontinue\b|\bfollow\b|\block\b)", re.I)
ASSET_EXCLUDE_DECL = re.compile(
    r"(?:不采用|不使用|不用|不复制|不要用|不引入|不含|不改变|不出现|不跳切|"
    r"仅参考|只参考|仅保留|只保留|"
    r"\bdo\s+not\s+use\b|\bwithout\b|\bonly\b|\bnot\s+copy\b|"
    r"\bno\s+(?:jump\s+)?cuts\b|\bno\s+montage\b)", re.I)


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


def strip_platform_corpora(text):
    """平台档：先把厂商官方词表原词从文本里摘掉，再跑空词表（D·③-C1）。"""
    out = text
    for w in sorted(PLATFORM_CORPORA, key=len, reverse=True):
        out = re.sub(re.escape(w), " ", out, flags=re.I)
    return out


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


def curve_score(density, curve):
    """分档台阶曲线：density ≤ 台阶上限 → 该档分数，超出则归零档。"""
    for limit, score in curve:
        if density <= limit:
            return score
    return 0.0


# ----------------------------------------------------------------------
# 分档子类判定（§六 6.1 的 7 项，两档各自算）
# ----------------------------------------------------------------------

def judge_22(text):
    """2.2 情绪可拍摄化（分档）。返回 (进阶档, 平台档, 依据)。"""
    emo = find_hits(EMOTION_WORDS, text)
    cues = find_hits(SHOOTABLE_CUES, text)
    emo_n = sum(n for _, n in emo)
    cue_n = sum(n for _, n in cues)
    if emo_n == 0:
        return ("不适用（无情绪词）", "不适用（无情绪词）", "未出现抽象情绪词")
    if cue_n == 0:
        return ("不通过（情绪词无线索）", "不通过（情绪词无外化）", f"情绪词 {emo_n} 处、可拍摄线索 0")
    if cue_n >= 5:
        adv = "不通过（线索 >4，清点整张脸）"
    elif cue_n == 1:
        adv = "部分通过（仅 1 条线索，建议 2–4）"
    else:
        adv = "通过（2–4 条线索）"
    pla = "通过（有外化线索即可）"
    return (adv, pla, f"情绪词 {emo_n} 处、可拍摄线索 {cue_n} 条")


def judge_52(text):
    """5.2 色温 / 调色板比例（分档）。"""
    has_temp = bool(re.search(COLOR_TEMP, text, re.I))
    has_ratio = bool(re.search(PALETTE_RATIO, text))
    platform_tone = find_hits(PLATFORM_TONE_WORDS, text)
    tone_n = sum(n for _, n in platform_tone)
    if has_temp and has_ratio:
        return ("通过（色温 + 比例）", "通过", f"色温命中 + 比例命中")
    if has_temp and not has_ratio:
        return ("部分通过（有色温，缺调色板比例）", "通过",
                "有色温但无 60/30/10 类比例")
    if has_ratio and not has_temp:
        return ("部分通过（有比例，缺色温）", "通过", "有比例但无色温值")
    if tone_n:
        return ("不通过（只有色调词，无温度值 / 无比例）", "通过（平台色调词表内）",
                f"平台色调词 {tone_n} 处，无温度值 / 无比例")
    return ("不通过（未提色彩倾向）", "不通过（未提色彩倾向）", "色彩槽缺失")


def judge_61(text):
    """6.1 材质 / 纹理 / 表面响应（分档）。"""
    mats = find_hits(MATERIAL_WORDS, text)
    resp = find_hits(MATERIAL_RESPONSE, text)
    mat_n = sum(n for _, n in mats)
    resp_n = sum(n for _, n in resp)
    if mat_n and resp_n:
        return ("通过（物理材质名 + 光响应）", "通过", f"材质 {mat_n} 处 + 响应 {resp_n} 处")
    if mat_n and not resp_n:
        return ("部分通过（有材质名，无光响应配对）", "通过",
                "有材质名但未写它带来的可见后果（B「命名必带可见后果」）")
    if resp_n and not mat_n:
        return ("部分通过（有表面响应，无材质名）", "通过", "只有光响应词")
    return ("不通过（无材质槽）", "不通过（无材质槽）", "材质槽缺失")


def judge_82(text):
    """8.2 时间戳 / 时间预算粒度（分档，冲突 C2）。"""
    codes = re.findall(TIMECODE, text)
    shots = re.findall(SHOT_INDEX, text, re.I)
    over = re.findall(OVER_PRECISE_TIME, text)
    # 区间连续性（只对 `a-b s` 数值对判重叠）
    pairs = []
    for m in re.finditer(r"(\d{1,3}(?:\.\d)?)\s*-\s*(\d{1,3}(?:\.\d)?)\s*s\b", text):
        pairs.append((float(m.group(1)), float(m.group(2))))
    overlap = any(pairs[i][1] > pairs[i + 1][0] for i in range(len(pairs) - 1))
    if pairs and overlap:
        return ("不通过（区间重叠）", "不通过（区间重叠）", f"时间区间 {pairs} 有重叠")
    if codes:
        adv = "通过（连续时间预算）"
        pla = "通过（该平台响应时间戳）"
        return (adv, pla, f"时间码 {len(codes)} 处：{'、'.join(codes[:6])}")
    if shots:
        return ("不通过（用镜头序号代替时码，进阶档要求时间预算）",
                "通过（Seedance 2.0 只响应镜头序号，允许序号替代）",
                f"镜号/分镜标记 {len(shots)} 处：{'、'.join(dict.fromkeys(shots))[:60]}")
    if over:
        return ("不通过（对精确时间硬承诺）", "不通过（文档明确对精确时间支持不稳定）",
                f"越权时间承诺：{'、'.join(over[:3])}")
    if len(text.strip().splitlines()) > 3:
        return ("不通过（多段却无时间分段）", "部分通过（可用镜号，但此处两者皆无）",
                "既无时码也无镜号")
    return ("不适用（单段散文写法）", "不适用（单段散文写法）", "单段、无时序需求")


def judge_122(text):
    """12.2 参数与散文分离纪律（分档，冲突 C4）。返回 (adv, pla, sep, mixed, contradiction)。"""
    lines = [l for l in text.splitlines() if l.strip()]
    inline, sep, contra = [], [], []
    aspects, fps = [], []
    for i, ln in enumerate(lines, 1):
        toks = [t for t in PARAM_TOKEN_STRICT.findall(ln) if not _is_decade(t)]
        if toks:
            rest = len(re.sub(r"\s", "", PARAM_TOKEN_STRICT.sub("", ln)))
            if rest > PARAM_LINE_MAX_REST:
                inline.append({"行": i, "命中": toks, "去参数后剩余字": rest})
            else:
                sep.append({"行": i, "命中": toks, "去参数后剩余字": rest})
        aspects += ASPECT_TOKEN.findall(ln)
        fps += [t.lower() for t in FPS_TOKEN.findall(ln)]
    if len(set(aspects)) > 1:
        contra.append(f"宽高比互斥：{'/'.join(sorted(set(aspects)))}")
    if len(set(fps)) > 1:
        contra.append(f"帧率互斥：{'/'.join(sorted(set(fps)))}")
    if not (inline or sep):
        return ("不适用（无参数）", "不适用（无参数）", sep, inline, contra)
    if contra:
        return ("不通过（参数自相矛盾）", "不通过（参数自相矛盾）", sep, inline, contra)
    if inline:
        return ("不通过（参数写进散文正文）", "通过（该平台允许内联参数）", sep, inline, contra)
    return ("通过（参数独立成行 / 独立块）", "通过（参数独立成行 / 独立块）", sep, inline, contra)


def score_22(adv_v, pla_v, adv):
    """2.2 分档计分：进阶档要 2–4 条线索；平台档有外化线索即可。"""
    if adv_v.startswith("不适用"):
        return None
    if adv:
        if adv_v.startswith("通过"):
            return 100.0
        if adv_v.startswith("部分"):
            return 60.0
        return 0.0
    return 100.0 if pla_v.startswith("通过") else 0.0


def analyze(text, tier="platform"):
    if tier not in ("advanced", "platform"):
        raise ValueError("tier 只接受 advanced / platform")
    adv = (tier == "advanced")
    chars = visible(text)
    lines = iter_lines(text)
    positive = strip_neg_lines(text)                # 正向正文（不含负面槽行）
    positive_scored = positive if adv else strip_platform_corpora(positive)

    # ---------- 1. 占位符未填（13.0 硬失败） ----------
    ph_hits = []
    for pat in PLACEHOLDER_PATTERNS:
        for m in pat.finditer(text):
            ph_hits.append(m.group(0))
    ph_spine = sum(1 for h in ph_hits if SPINE_SLOT_HINT.search(h))
    hard_placeholder = bool(ph_hits) and (len(ph_hits) >= 5 or ph_spine >= 3)

    # ---------- 2. 空词六类（两档各算一遍；tier 只影响 class 2 豁免） ----------
    def empty_hits(src):
        out = []
        for w, n in find_hits(EMPTY_EVAL, src):
            out.append(("1 空评价词", w, n))
        for w, n in find_hits(EMPTY_EVAL_EXTRA, src):
            out.append(("5 形容词堆叠·单用", w, n))
        for w, n in find_hits(EMPTY_TOKENS, src):
            out.append(("2 搬运 token", w, n))
        neg_slop = re.findall(r"(?<![\w-])no\s+[a-z][a-z\s-]{1,20}", src, re.I) \
            + re.findall(r"不要[^\s，。；]{1,10}|不是[^\s，。；]{1,10}", src)
        for w in neg_slop:
            out.append(("4 否定 slop", w.strip(), 1))
        for tri in SYNONYM_TRIPLES:
            if all(re.search(r"\b" + w + r"\b", src, re.I) for w in tri):
                out.append(("5 形容词堆叠", "/".join(tri), 1))
        for w, n in find_hits(FEELING_SUFFIX, src):
            out.append(("6 感受后缀词", w, n))
        return out

    empty = empty_hits(positive_scored)
    empty_total = sum(n for _, _, n in empty)
    empty_density = empty_total / chars * 1000 if chars else 0.0
    curve = EMPTY_CURVE_ADV if adv else EMPTY_CURVE_PLAT
    empty_score = curve_score(empty_density, curve)

    # 10.3 子分：只看空评价词 / 搬运 token / 感受后缀（抽象评价词三类）
    eval_total = sum(n for c, _, n in empty if c.startswith(("1 ", "2 ", "6 ")))
    eval_density = eval_total / chars * 1000 if chars else 0.0
    eval_score = curve_score(eval_density, curve)

    # 另一档的同口径读数（分档栏要同时给出两档数字）
    def metrics_for(t):
        src = positive if t == "advanced" else strip_platform_corpora(positive)
        hits = empty_hits(src)
        tot = sum(n for _, _, n in hits)
        den = tot / chars * 1000 if chars else 0.0
        cv = EMPTY_CURVE_ADV if t == "advanced" else EMPTY_CURVE_PLAT
        ev = sum(n for c, _, n in hits if c.startswith(("1 ", "2 ", "6 ")))
        evd = ev / chars * 1000 if chars else 0.0
        return {"total": tot, "density": den, "score": curve_score(den, cv),
                "eval": ev, "eval_density": evd, "eval_score": curve_score(evd, cv)}

    other = metrics_for("platform" if adv else "advanced")

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

    # ---------- 3. 参数（12.1 / 12.2 分档） ----------
    adv_122, pla_122, param_sep, param_inline, param_contra = judge_122(text)
    param_hits = [{"行": x["行"], "命中": x["命中"]} for x in (param_sep + param_inline)]
    # 报告栏（只报）：§一 的宽口径「参数误入正文」正则（含裸 4K/8K）
    param_all_wide = []
    for i, ln in enumerate(lines, 1):
        toks = [t for t in PARAM_TOKEN.findall(ln) if not _is_decade(t)]
        if toks:
            param_all_wide.append({"行": i, "命中": toks})
    has_param = bool(param_sep or param_inline)
    if not has_param:
        param_score = None
    elif param_contra:
        param_score = 0.0
    else:
        param_score = 100.0

    # ---------- 4. 负面行卫生（硬规则 11.6，v0.2 校准：≤8 / 9–15 / >15） ----------
    blocks = collect_neg_blocks(text)
    neg_info = {"负面行数": len(blocks)}
    neg_fail_hard = False
    if blocks:
        counts = [neg_item_count("\n".join(b)) for b in blocks]
        max_items = max(counts)
        longest = max(len(re.sub(r"\s", "", "\n".join(b))) for b in blocks)
        old_marks = OLD_FAIL_MARK.findall(text)
        if old_marks:
            grade, hygiene, neg_fail_hard = "不合格（含旧失败专名）", 0.0, True
        elif max_items <= NEG_OK_MAX_ITEMS:
            grade, hygiene = "合格（紧凑行）", 100.0
        elif max_items <= NEG_LONG_MAX_ITEMS:
            grade, hygiene = "偏长（建议压缩）", 60.0
        else:
            grade, hygiene, neg_fail_hard = "不合格（长清单）", 0.0, True
        neg_info.update({"每块项数": counts, "最大项数": max_items,
                         "最长块字符数": longest, "旧专名痕迹": old_marks,
                         "评级": grade, "卫生分": hygiene, "硬规则命中": neg_fail_hard})
    else:
        neg_info.update({"每块项数": [], "最大项数": 0, "最长块字符数": 0,
                         "旧专名痕迹": [], "评级": "不适用（无负面槽）",
                         "卫生分": None, "硬规则命中": False})

    # ---------- 5. 槽痕迹（11 槽，体检栏） ----------
    slot_hits = [name for name, pat in SLOTS if pat.search(positive)]
    slot_missing = [name for name, _ in SLOTS if name not in slot_hits]
    slot_score = len(slot_hits) / len(SLOTS) * 100
    # 主干槽缺失警示（**不进主分**）：轻档主分只答「有无空词 / 卫生 / 参数」，
    # 「缺主体/动作/场景」的后果必须走中档逐条判据（E2·§五-4、§六-7）。
    spine_missing = [s for s in ("主体", "动作", "场景") if s in slot_missing]
    spine_warn = (f"主干槽缺失 {'、'.join(spine_missing)} → 主分不可当成「成品质量分」，"
                  f"须走中档逐条判据" if spine_missing else None)

    # ---------- 6. 对象类型判别（§零·A，v0.2 强/弱信号拆分） ----------
    meta_strong = len(META_METHOD_STRONG.findall(text))
    meta_weak = len(META_METHOD_WEAK.findall(text))
    cross_n = len(META_CROSSMODAL.findall(text))
    if hard_placeholder:
        obj_type = "疑似占位符模板（未填）→ 硬失败优先"
    elif cross_n >= CROSSMODAL_THRESHOLD:
        obj_type = "疑似跨模态（音乐/声音/代码）→ 不打分，另立包"
    elif meta_strong >= META_STRONG_THRESHOLD:
        obj_type = "疑似方法论模板（教人写词，不是成品词）→ 不打分"
    else:
        obj_type = "成品提示词 → 正常打分"

    # ---------- 7. 参考素材型身份锁定（v0.2 修 E·5.7） ----------
    refs = ASSET_REF.findall(text)
    use_decl = ASSET_USE_DECL.findall(text)
    exclude_decl = ASSET_EXCLUDE_DECL.findall(text)
    if refs:
        if use_decl and exclude_decl:
            ref_verdict = "通过（用什么 + 不用什么齐）"
        elif use_decl:
            ref_verdict = "部分（写了『用什么』，缺『不用什么』）"
        else:
            ref_verdict = "不通过（有指代，未声明用途）"
        ref_note = ("身份由参考素材承担 → 1.2 不再按散文静态特征判（并入 1.3 素材职责）；"
                    "本项为裁判项，脚本只报不扣")
    else:
        ref_verdict = "不适用（无素材指代）"
        ref_note = "无参考素材，1.2 按散文静态特征判"

    # ---------- 8. 模糊词（AIGC 口径 = 核心表 − §7.4 白名单） ----------
    core_hits = find_hits(CORE_VAGUE_ZH, text) + find_hits(CORE_VAGUE_EN, text)
    core_total = sum(n for _, n in core_hits)
    wl_total = sum(n for _, n in find_hits(VAGUE_WHITELIST, text))
    aigc_vague = max(0, core_total - wl_total)
    aigc_density = aigc_vague / chars * 1000 if chars else 0.0
    aigc_vague_score = max(0.0, 100.0 - aigc_density * 10)

    # ---------- 9. 分档栏（7 项，两档各自判定） ----------
    adv_22, pla_22, ev22 = judge_22(text)
    adv_52, pla_52, ev52 = judge_52(text)
    adv_61, pla_61, ev61 = judge_61(text)
    adv_82, pla_82, ev82 = judge_82(text)
    tier_axis = [
        {"子类": "2.2 情绪可拍摄化", "进阶档": adv_22, "平台档": pla_22, "依据": ev22,
         "进主分": adv_22.startswith("不适用") is False},
        {"子类": "5.2 色温/调色板比例", "进阶档": adv_52, "平台档": pla_52, "依据": ev52,
         "进主分": False},
        {"子类": "6.1 材质/纹理/表面响应", "进阶档": adv_61, "平台档": pla_61, "依据": ev61,
         "进主分": False},
        {"子类": "8.2 时间戳/时间预算粒度", "进阶档": adv_82, "平台档": pla_82, "依据": ev82,
         "进主分": False},
        {"子类": "10.3 抽象评价词检测",
         "进阶档": (f"空词分 {eval_score:.1f}（不豁免）" if adv
                 else f"空词分 {other['eval_score']:.1f}（不豁免）"),
         "平台档": (f"空词分 {other['eval_score']:.1f}（厂商语料豁免后）" if adv
                 else f"空词分 {eval_score:.1f}（厂商语料豁免后）"),
         "依据": f"抽象评价词三类命中 {eval_total} 处，密度 {eval_density:.2f}/千字；"
                 f"另一档密度 {other['eval_density']:.2f}/千字", "进主分": True},
        {"子类": "12.2 参数与散文分离纪律", "进阶档": adv_122, "平台档": pla_122,
         "依据": (f"独立参数行 {len(param_sep)}、散文混入 {len(param_inline)}"
                  + (f"、矛盾 {param_contra}" if param_contra else "")),
         "进主分": "矛盾进主分；内联面只报不扣"},
        {"子类": "13.1 空词/标签沙拉/形容词堆叠",
         "进阶档": (f"反模式分 {empty_score:.1f}" if adv else f"反模式分 {other['score']:.1f}"),
         "平台档": (f"反模式分 {other['score']:.1f}" if adv else f"反模式分 {empty_score:.1f}"),
         "依据": f"六类命中 {empty_total} 处，密度 {empty_density:.2f}/千字，"
                 f"曲线档位 {EMPTY_CURVE_ADV if adv else EMPTY_CURVE_PLAT}", "进主分": True},
    ]

    # ---------- 汇总判定（v0.2 主分口径） ----------
    scored, n_a = {}, []
    scored["反模式分(13.1)"] = round(empty_score, 1)
    if neg_info["卫生分"] is not None:
        scored["负面卫生分(11.6)"] = round(neg_info["卫生分"], 1)
    else:
        n_a.append("负面卫生（无负面槽）")
    if param_score is not None:
        scored["参数分(12.1/12.2)"] = round(param_score, 1)
    else:
        n_a.append("参数（无参数）")
    if not adv_22.startswith("不适用"):
        scored["情绪可拍摄分(2.2)"] = score_22(adv_22, pla_22, adv)
    else:
        n_a.append("情绪（无情绪词）")

    caps = []
    if hard_placeholder:
        verdict = f"不通过（硬失败：占位符未填 {len(ph_hits)} 处）"
        total, scoreable = 0.0, False
    elif obj_type.startswith("疑似跨模态") or obj_type.startswith("疑似方法论"):
        verdict = "不打分（对象类型非成品提示词）"
        total, scoreable = None, False
    else:
        scoreable = True
        raw = sum(scored.values()) / len(scored)
        total = raw
        if neg_fail_hard:
            total = min(raw, HARD_RULE_CAP)
            caps.append(f"硬规则 11.6 命中 → 主分帽 {HARD_RULE_CAP}")
        total = round(total, 1)
        verdict = "偏低" if total < 50 else ("中" if total < 75 else "中高/高")
    tier_name = "进阶档（物理描写派）" if adv else "平台档（国内厂商预设派）"

    # ---------- 10. 参考栏：static_check（v0.2：降为参考栏，不进主分） ----------
    static_ref = run_static_ref(text)

    return {
        "档位": tier_name,
        "版本": VERSION,
        "字符数": chars,
        "对象类型": obj_type,
        "对象类型依据": {"方法论强信号": meta_strong, "方法论弱信号": meta_weak,
                         "跨模态特征词": cross_n,
                         "判据线": f"强信号 ≥{META_STRONG_THRESHOLD}（弱信号不触发）"},
        "占位符未填": {"硬失败": hard_placeholder, "处数": len(ph_hits),
                       "落在主干槽": ph_spine, "例": ph_hits[:6]},
        "空词": {"总数": empty_total, "每千字": round(empty_density, 2),
                 "明细": [{"类": c, "词": w, "次数": n} for c, w, n in empty],
                 "豁免": ("无（进阶档）" if adv else f"平台语料 {len(PLATFORM_CORPORA)} 词已摘除")},
        "标签沙拉行": salad_lines,
        "参数": {"独立参数行": param_sep, "疑似混入散文": param_inline,
                 "矛盾": param_contra, "全部参数行": param_hits,
                 "宽口径报告_含裸分辨率词": param_all_wide,
                 "判定线": f"去参数后剩余可见字符 ≤{PARAM_LINE_MAX_REST} 视为独立行",
                 "口径": "分档项（§六 12.2，冲突 C4）：内联只报；矛盾进主分"},
        "参数误入正文": {"疑似混入散文": param_inline, "全部参数行": param_all_wide,
                         "口径": "分档项（§六 12.2，冲突 C4）——只报不扣"},
        "负面行卫生": neg_info,
        "槽痕迹": {"命中": slot_hits, "缺失": slot_missing,
                   "命中数": len(slot_hits), "总槽数": len(SLOTS),
                   "主干槽缺失警示": spine_warn,
                   "口径": "体检栏：只答「槽写没写」；v0.2 起不进主分（E2·§六-7）"},
        "参考素材型身份锁定": {"指代命中": refs[:8], "指代数": len(refs),
                               "用途声明": bool(use_decl), "排除声明": bool(exclude_decl),
                               "判定": ref_verdict, "口径": ref_note},
        "模糊词AIGC口径": {"核心表命中": core_total, "白名单剔除": wl_total,
                           "修后": aigc_vague, "每千字": round(aigc_density, 2),
                           "修后分": round(aigc_vague_score, 1)},
        "分档栏": tier_axis,
        "分项": scored,
        "不适用项": n_a,
        "硬闸": caps,
        "主分": total,
        "参考栏_static": static_ref,
        "可打分": scoreable,
        "判定": verdict,
    }


def run_static_ref(text):
    """参考栏：跑核心脚本 static_check.py（只作参考，不进主分）。"""
    p = pathlib.Path(__file__).with_name("static_check.py")
    if not p.is_file():
        return {"可用": False, "原因": "同目录未找到 static_check.py"}
    try:
        spec = importlib.util.spec_from_file_location("static_check_ref", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        shalls = len(re.findall(r"应当|应支持|需支持|系统应", text))
        scenario = "prd" if shalls >= 3 else "prompt"
        r = m.analyze(text, scenario)
        return {"可用": True, "总分": r["总分"], "分项": r["分项"], "场景": scenario,
                "口径": "核心脚本词表是需求向的 → AIGC 场景只作参考栏，不进主分、不参与排序"}
    except Exception as e:                                  # 出任何异常都不能拖垮主分
        return {"可用": False, "原因": f"{type(e).__name__}: {e}"}


def print_card(path, r):
    print(f"== req-prompt-eval AIGC 卡（轻档·{r['版本']} 判据包 ｜ {r['档位']}）==")
    print(f"对象: {path}")
    print(f"字符 {r['字符数']} ｜ 对象类型: {r['对象类型']}")
    d = r["对象类型依据"]
    print(f"  类型依据: 方法论强信号 {d['方法论强信号']} ｜ 弱信号 {d['方法论弱信号']} "
          f"｜ 跨模态 {d['跨模态特征词']} ｜ 判据线 {d['判据线']}")
    if r["占位符未填"]["硬失败"]:
        p = r["占位符未填"]
        print(f"!! 占位符未填（主干 13.0 硬失败）: {p['处数']} 处，其中落在主干槽 {p['落在主干槽']} 处")
        print(f"   例: {'、'.join(p['例'])}")
    else:
        print("占位符未填: 否（{} 处）".format(r["占位符未填"]["处数"]))
    e = r["空词"]
    print(f"空词: {e['总数']} 个（每千字 {e['每千字']}）｜ 豁免: {e['豁免']}")
    for it in e["明细"][:10]:
        print(f"  - [{it['类']}] {it['词']}×{it['次数']}")
    if r["标签沙拉行"]:
        print(f"标签沙拉候选（只报）: {len(r['标签沙拉行'])} 行")
    pm = r["参数"]
    print(f"参数（分档项 12.2）: 独立行 {len(pm['独立参数行'])} ｜ "
          f"混入散文 {len(pm['疑似混入散文'])} ｜ 矛盾 {len(pm['矛盾'])} ｜ {pm['判定线']}")
    for it in pm["疑似混入散文"][:5]:
        print(f"  - L{it['行']}: {'、'.join(it['命中'])} ｜ 去参数后剩 {it['去参数后剩余字']} 字")
    for c in pm["矛盾"]:
        print(f"  !! {c}")
    n = r["负面行卫生"]
    print(f"负面行卫生（硬规则 11.6）: 负面行 {n['负面行数']} ｜ 最大项数 {n['最大项数']} ｜ "
          f"最长 {n['最长块字符数']} 字 ｜ {n['评级']}"
          + (" ｜ **硬规则命中**" if n.get("硬规则命中") else ""))
    if n["旧专名痕迹"]:
        print(f"  旧失败专名痕迹: {'、'.join(n['旧专名痕迹'])}")
    s = r["槽痕迹"]
    print(f"槽痕迹（体检栏，不进主分）: {s['命中数']}/{s['总槽数']} ｜ "
          f"缺失: {'、'.join(s['缺失']) or '无'}")
    ra = r["参考素材型身份锁定"]
    print(f"参考素材型身份锁定（修 E·5.7）: {ra['判定']}"
          + (f" ｜ 指代 {ra['指代数']} 处：{'、'.join(ra['指代命中'][:4])}" if ra["指代数"] else ""))
    v = r["模糊词AIGC口径"]
    print(f"模糊词（AIGC 口径 = 核心表 {v['核心表命中']} − 白名单 {v['白名单剔除']}）"
          f": {v['修后']} 个（每千字 {v['每千字']}）")
    print("--- 分档栏（7 项双开关：进阶档 / 平台档）---")
    for it in r["分档栏"]:
        mark = "★进主分" if it["进主分"] else "·报告"
        print(f"  [{it['子类']}] {mark}")
        print(f"      进阶档: {it['进阶档']}")
        print(f"      平台档: {it['平台档']}")
    print("---")
    for k, val in r["分项"].items():
        print(f"{k}: {val}")
    if r["不适用项"]:
        print(f"不适用（不计入主分）: {'、'.join(r['不适用项'])}")
    if r["硬闸"]:
        for c in r["硬闸"]:
            print(f"硬闸: {c}")
    sr = r["参考栏_static"]
    print("== 主分 / 参考栏 ==")
    print(f"主分（aigc_check · {r['档位']}）: "
          f"{'—（不打分）' if r['主分'] is None else r['主分']}")
    if sr.get("可用"):
        print(f"参考栏（static_check · 只作参考，不进主分）: {sr['总分']}  分项 {sr['分项']}")
    else:
        print(f"参考栏（static_check）: 不可用（{sr.get('原因')}）")
    print(f"判定: {r['判定']}")
    print("（本卡只给判断不给改写；对象类型非成品的记「不打分」，中档裁判见判据包§五）")


def main():
    ap = argparse.ArgumentParser(description=f"AIGC 提示词补充检查（轻档，配套 {VERSION} 判据包）")
    ap.add_argument("file", help="被测文件（提示词原文，Markdown 或纯文本）")
    ap.add_argument("--tier", choices=["advanced", "platform"], default="platform",
                    help="档位开关：advanced=进阶档（物理描写派）"
                         " platform=平台档（国内厂商预设派，默认）")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    ap.add_argument("--no-static", action="store_true", help="不算参考栏（不跑 static_check）")
    args = ap.parse_args()

    p = pathlib.Path(args.file)
    if not p.is_file():
        sys.exit(f"文件不存在: {p}")
    text = p.read_text(encoding="utf-8")

    r = analyze(text, tier=args.tier)
    if args.no_static:
        r["参考栏_static"] = {"可用": False, "原因": "--no-static"}
    result = {"file": str(p), **r}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_card(str(p), r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
