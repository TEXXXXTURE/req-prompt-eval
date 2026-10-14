# -*- coding: utf-8 -*-
"""阈值校准跑批（v0.2）：把 research/E3-校准样本/ 全部样本喂给 aigc_check.analyze()，
两档各跑一遍，逐项算「分开率」并落盘 JSON。

用法：python research/E3-校准样本/_calibrate.py --tag v02
输出：research/E3-校准样本/_calib_<tag>.json
"""
import argparse
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = ROOT / "E3-校准样本"

# 脚本层可判的期望类别（其余为「脚本层不判 / 探针」，单列，不进分开率分母）
SCRIPT_JUDGEABLE_NEG = [
    "N01", "N02", "N03", "N04", "N05", "N06", "N07", "N08", "N09", "N10",
    "N11", "N13", "N14", "N21", "N25",
]
# 脚本层不判的反例：13.2 语义污染 / 13.5 越权 属待验证「只计不判」；
# 8.1 多镜头无锁定块属裁判项 → 不进脚本层分开率，报告里单列。
NOT_SCRIPT_NEG = [
    "N15", "N16", "N17", "N18", "N20",
]
# 探针样本（结构性 / 档位边界 / 裁判项 / 参数矛盾）——两个方向都不算对错，只记录读数。
PROBES = ["N12", "N19", "N22", "N23", "N24", "N26", "N27", "N28"]
TYPE_ONLY_POS = ["P07", "P08"]          # 对象类型样本（方法论 / 跨模态），判「不打分」
# 平台语料正例：只在平台档期望高分；进阶档把它们判低**正是档位差异本身**（D·③-C1）
PLATFORM_CORPUS_POS = ["P20", "P22"]


def load_module(tag):
    p = REPO / "scripts" / "aigc_check.py"
    spec = importlib.util.spec_from_file_location(f"aigc_check_{tag}", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def wants():
    d = {}
    for line in (OUT / "_index.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        if not line.strip():
            continue
        name, want, _ = line.split("\t")
        d[name] = want
    return d


def run_tier(m, tier):
    rows = []
    for folder in ("正例", "反例"):
        for f in sorted((OUT / folder).glob("*.txt")):
            r = m.analyze(f.read_text(encoding="utf-8"), tier=tier)
            neg = r["负面行卫生"]
            rows.append({
                "样本": f.name,
                "期望": wants().get(f.name, "?"),
                "目录": folder,
                "字符数": r["字符数"],
                "对象类型": r["对象类型"].split("→")[0].strip(),
                "强信号": r["对象类型依据"]["方法论强信号"],
                "弱信号": r["对象类型依据"]["方法论弱信号"],
                "跨模态": r["对象类型依据"]["跨模态特征词"],
                "占位符": r["占位符未填"]["处数"],
                "硬失败": r["占位符未填"]["硬失败"],
                "反模式分": next(v for k, v in r["分项"].items() if k.startswith("反模式")),
                "空词数": r["空词"]["总数"],
                "空词密度": r["空词"]["每千字"],
                "负面项数": neg["最大项数"],
                "负面评级": neg["评级"],
                "负面卫生分": neg["卫生分"],
                "硬规则命中": neg.get("硬规则命中"),
                "槽痕分": r["槽痕迹"]["命中数"],
                "参数混入": len(r["参数"]["疑似混入散文"]),
                "参数矛盾": len(r["参数"]["矛盾"]),
                "素材型判定": r["参考素材型身份锁定"]["判定"],
                "主分": r["主分"],
                "参考栏static": (r["参考栏_static"] or {}).get("总分"),
                "判定": r["判定"],
            })
    return rows


def text_lines(f):
    return f.read_text(encoding="utf-8").splitlines()


def separation(rows, tier):
    """分开率：
      正例（含对象类型样本「不打分」）主分 ≥70 记分对；平台语料正例在进阶档判低算「档位差异」不计错；
      脚本层可判反例主分 <70 记分对；探针与脚本层不判样本不进分母。"""
    ok, bad = [], []
    for r in rows:
        rid = r["样本"][:3]
        if rid in PROBES:
            continue
        if rid in TYPE_ONLY_POS:
            (ok if r["主分"] is None else bad).append(r["样本"])
            continue
        if r["期望"] == "pos":
            if tier == "advanced" and rid in PLATFORM_CORPUS_POS:
                continue                      # 档位差异，两个方向都不算错
            (ok if (r["主分"] is not None and r["主分"] >= 70) else bad).append(r["样本"])
        elif r["期望"] == "neg" and rid in SCRIPT_JUDGEABLE_NEG:
            (ok if (r["主分"] is not None and r["主分"] < 70) else bad).append(r["样本"])
    return ok, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="run")
    args = ap.parse_args()
    m = load_module(args.tag)

    all_rows, summary = {}, {}
    for tier in ("platform", "advanced"):
        rows = run_tier(m, tier)
        all_rows[tier] = rows
        ok, bad = separation(rows, tier)
        pos = [r for r in rows if r["期望"] == "pos" and r["样本"][:3] not in TYPE_ONLY_POS
               and not (tier == "advanced" and r["样本"][:3] in PLATFORM_CORPUS_POS)]
        neg = [r for r in rows if r["样本"][:3] in SCRIPT_JUDGEABLE_NEG]
        probes = [r for r in rows if r["样本"][:3] in PROBES or r["样本"][:3] in NOT_SCRIPT_NEG]
        summary[tier] = {
            "正例数(脚本层可判)": len(pos),
            "反例数(脚本层可判)": len(neg),
            "探针+脚本层不判": len(probes),
            "分开数": len(ok), "未分开": len(bad), "未分开样本": bad,
            "分开率": (f"{len(ok)}/{len(ok)+len(bad)} = "
                    f"{round(len(ok)/(len(ok)+len(bad))*100,1)}%"),
            "正例主分区": [min([r["主分"] for r in pos if r["主分"] is not None], default=None),
                       max([r["主分"] for r in pos if r["主分"] is not None], default=None)],
            "反例主分区": [min([r["主分"] for r in neg if r["主分"] is not None], default=None),
                       max([r["主分"] for r in neg if r["主分"] is not None], default=None)],
        }

    (OUT / f"_calib_{args.tag}.json").write_text(
        json.dumps({"summary": summary, "tiers": all_rows}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    for tier in ("platform", "advanced"):
        print(f"\n===== 档位 = {tier} =====")
        hdr = ("样本", "期望", "对象类型", "强/弱", "占位", "反模式分", "空词密度",
               "负面项", "负评级", "卫生分", "硬规则", "槽", "混入", "矛盾", "素材型", "主分", "参考栏", "判定")
        print(" | ".join(hdr))
        for r in all_rows[tier]:
            print(" | ".join(str(x) for x in (
                r["样本"], r["期望"], r["对象类型"], f"{r['强信号']}/{r['弱信号']}", r["占位符"],
                r["反模式分"], r["空词密度"], r["负面项数"], r["负面评级"],
                r["负面卫生分"], r["硬规则命中"], r["槽痕分"], r["参数混入"], r["参数矛盾"],
                r["素材型判定"], r["主分"], r["参考栏static"], r["判定"])))
        print(json.dumps(summary[tier], ensure_ascii=False))


if __name__ == "__main__":
    main()
