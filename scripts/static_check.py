# -*- coding: utf-8 -*-
"""req-prompt-eval 静态检查器（轻档核心）

零模型调用，纯文本匹配计分。做什么：
  1. 模糊词密度 —— 拿词表搜「更好/友好/尽量」这类没定死的词，按每千字计数
  2. 验收判据存在率 —— 逐条看有没有「怎么算对」的说法（预期/返回/不超过/达到…）
  3. 未定死标记 —— 搜「待定/TBD/视情况」这类留白挂牌
  4. 结构检查 —— 完成定义 / 范围边界 / 质量门 三类话在不在

它不理解语义，只认字面。语义判断（真细致还是画大饼）交给中档的模型裁判。

用法：
  python static_check.py <文件> [--scenario auto|prd|prompt] [--json]
                          [--ledger 台账.jsonl] [--tag "改动备注"]

输出：人读评分卡（默认）或 JSON（--json）。给 --ledger 则追加一行到分数台账。
"""

import argparse
import datetime
import json
import pathlib
import re
import sys

# ---------- 词表（场景无关的通用核心） ----------

# 模糊词：说出来但没定死的表述
VAGUE_ZH = [
    "更好", "更优", "较好", "友好", "好用", "合理", "适当", "尽量", "尽可能",
    "尽快", "美观", "流畅", "出色", "优秀", "良好", "显著", "高效", "灵活",
    "完善", "健壮", "顺滑", "人性化", "智能化", "不错的", "满意", "友好性",
    "用户体验好", "性能好", "足够好", "若干", "部分情况下", "必要时", "视情况而定",
]
VAGUE_EN = [
    "good", "nice", "better", "fast", "robust", "user-friendly",
    "reasonable", "appropriate", "efficient", "smooth", "flexible",
    "as needed", "if necessary", "etc.",
]

# 未定死标记：留白的显式挂牌（出现即登记进未定死清单，不算隐式留白）
UNDECIDED = [
    "待定", "TBD", "TODO", "待补充", "后续补充", "另行约定", "另行商定",
    "视情况", "酌情", "开发定", "开发自行", "不确定", "暂不", "占位",
]

# 验收判据痕迹：「怎么算对」的说法（注意：纯义务词「应当/应该」不算——
# 「用户应当能够下单」没有说怎么核对，不算有判据）
ACCEPT_MARKS = [
    "预期", "应该返回", "返回", "输出为", "输出格式", "通过标准",
    "验收", "算对", "不低于", "不超过", "至少", "至多", "达到", "等于",
    "包含", "格式为", "视为通过", "判定为", "计为", "成功率",
]

# 结构检查三组
STRUCT_DONE = [   # 完成定义：什么算做完
    "完成定义", "完成标准", "交付物", "产出为", "输出格式", "产出物",
    "definition of done", "DoD",
]
STRUCT_SCOPE = [  # 范围边界：不做什么
    "不包含", "不做", "不在本", "超出范围", "范围外", "禁止", "不允许",
    "不得", "除外", "不负责", "边界",
]
STRUCT_GATE = [   # 质量门：交出去之前自检
    "自检", "检查清单", "核对", "校验", "确认无误", "自查", "验证一遍",
    "复核", "checklist",
]

ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.、)])\s+\S")


def split_items(text):
    """把文本切成条目。

    规则：列表行（-/数字）按行切；没有列表时先按空行分段，
    段内每行都以句号类标点结尾（需求/提词常见的一行一条）就按行切；
    Markdown 标题行不计为条目。
    """
    lines = text.splitlines()
    items, buf = [], []
    has_list = any(ITEM_RE.match(l) for l in lines)
    para_end = re.compile(r"[。！？；;.!]\s*$")
    for line in lines:
        if line.lstrip().startswith("#"):
            continue
        if has_list and ITEM_RE.match(line):
            if buf:
                items.append("\n".join(buf))
            buf = [line]
        elif has_list:
            if buf:
                buf.append(line)
        else:
            if not line.strip():
                if buf:
                    items.append("\n".join(buf))
                buf = []
            else:
                buf.append(line)
    if buf:
        items.append("\n".join(buf))

    out = []
    for it in items:
        ls = [l for l in it.splitlines() if l.strip()]
        if len(ls) > 1 and all(para_end.search(l) for l in ls):
            out.extend(ls)          # 一行一条的写法，逐行切
        else:
            out.append(it)
    return [i for i in out if i.strip()]


def find_hits(patterns, text):
    """返回命中的 (词, 次数) 列表。中文按子串数，英文按词边界。"""
    hits = []
    low = text.lower()
    for p in patterns:
        if re.fullmatch(r"[a-zA-Z\s.-]+", p):
            n = len(re.findall(r"\b" + re.escape(p.lower()) + r"\b", low))
        else:
            n = text.count(p)
        if n:
            hits.append((p, n))
    return hits


def count_all(patterns, text):
    return sum(n for _, n in find_hits(patterns, text))


def analyze(text, scenario):
    chars = len(re.sub(r"\s", "", text))
    items = split_items(text)

    vague_hits = find_hits(VAGUE_ZH, text) + find_hits(VAGUE_EN, text)
    vague_total = sum(n for _, n in vague_hits)
    density = vague_total / chars * 1000 if chars else 0.0

    undecided_hits = find_hits(UNDECIDED, text)
    undecided_total = sum(n for _, n in undecided_hits)

    accept_items = 0
    for it in items:
        if count_all(ACCEPT_MARKS, it) > 0:
            accept_items += 1
    accept_rate = accept_items / len(items) * 100 if items else 0.0

    struct = {
        "完成定义": count_all(STRUCT_DONE, text) > 0,
        "范围边界": count_all(STRUCT_SCOPE, text) > 0,
        "质量门": count_all(STRUCT_GATE, text) > 0,
    }
    struct_score = sum(struct.values()) / 3 * 100

    # 计分：每维 0-100
    vague_score = max(0.0, 100.0 - density * 10)   # 每千字 10 个模糊词即归零
    scores = {
        "可验收率": round(accept_rate, 1),
        "模糊词分": round(vague_score, 1),
        "结构分": round(struct_score, 1),
    }
    total = round(sum(scores.values()) / len(scores), 1)

    return {
        "scenario": scenario,
        "字符数": chars,
        "条目数": len(items),
        "计数": {
            "模糊词总数": vague_total,
            "模糊词明细": dict(vague_hits),
            "每千字模糊词": round(density, 2),
            "未定死标记": undecided_total,
            "未定死明细": dict(undecided_hits),
            "含验收判据条目": accept_items,
        },
        "结构检查": struct,
        "分项": scores,
        "总分": total,
    }


def print_card(path, r):
    print(f"== req-prompt-eval 静态评分卡（轻档）==")
    print(f"对象: {path}  场景: {r['scenario']}")
    print(f"字符 {r['字符数']} ｜ 条目 {r['条目数']}")
    print(f"模糊词 {r['计数']['模糊词总数']} 个（每千字 {r['计数']['每千字模糊词']}）"
          f" ｜ 未定死挂牌 {r['计数']['未定死标记']} 处"
          f" ｜ 含判据条目 {r['计数']['含验收判据条目']}/{r['条目数']}")
    s = " ｜ ".join(f"{k} {v}" for k, v in r["结构检查"].items())
    print(f"结构检查（{r['scenario'] == 'prompt' and '提词向' or '通用'}）: {s}")
    print("---")
    for k, v in r["分项"].items():
        print(f"{k}: {v}")
    print(f"总分: {r['总分']}")
    if r["计数"]["模糊词明细"]:
        top = sorted(r["计数"]["模糊词明细"].items(), key=lambda x: -x[1])[:8]
        print("模糊词 top: " + "、".join(f"{w}×{n}" for w, n in top))
    if r["计数"]["未定死明细"]:
        print("未定死标记: " + "、".join(r["计数"]["未定死明细"].keys()))
    print("（本卡只给判断不给改写；中档裁判与多跑对比见 SKILL.md）")


def main():
    ap = argparse.ArgumentParser(description="需求/提示词静态检查（轻档）")
    ap.add_argument("file", help="被测文件（Markdown 或纯文本）")
    ap.add_argument("--scenario", choices=["auto", "prd", "prompt"], default="auto",
                    help="场景：prd=需求文档向 prompt=提词向 auto=按内容猜")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    ap.add_argument("--ledger", help="分数台账路径（JSONL，追加一行）")
    ap.add_argument("--tag", default="", help="台账备注：本次改动了什么")
    args = ap.parse_args()

    p = pathlib.Path(args.file)
    if not p.is_file():
        sys.exit(f"文件不存在: {p}")
    text = p.read_text(encoding="utf-8")

    scenario = args.scenario
    if scenario == "auto":
        # 需求文档向的信号：条目里多是「系统应当」类表述
        shalls = len(re.findall(r"应当|应支持|需支持|系统应", text))
        scenario = "prd" if shalls >= 3 else "prompt"

    r = analyze(text, scenario)
    result = {"file": str(p), "时间": datetime.datetime.now().isoformat(timespec="seconds"),
              **r}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_card(str(p), r)

    if args.ledger:
        lp = pathlib.Path(args.ledger)
        lp.parent.mkdir(parents=True, exist_ok=True)
        with lp.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"时间": result["时间"], "对象": str(p),
                                "场景": scenario, "档位": "轻",
                                "分项": r["分项"], "总分": r["总分"],
                                "备注": args.tag}, ensure_ascii=False) + "\n")
        if not args.json:
            print(f"台账已追加: {lp}")


if __name__ == "__main__":
    main()
