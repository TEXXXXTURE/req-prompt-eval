# -*- coding: utf-8 -*-
"""v0.1.1 基线分开率（同一规则，用于与 v0.2 对照）。
读 _calib_baseline.json（v0.1.1 脚本跑出的旧数据）与 _calib_v02.json。"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent

SCRIPT_JUDGEABLE_NEG = ["N01", "N02", "N03", "N04", "N05", "N06", "N07", "N08",
                        "N09", "N10", "N11", "N13", "N14", "N21", "N25"]
PROBES = ["N12", "N19", "N22", "N23", "N24", "N26", "N27", "N28"]
TYPE_ONLY_POS = ["P07", "P08"]
PLATFORM_CORPUS_POS = ["P20", "P22"]


def rate(rows, field, tier):
    ok, bad = [], []
    for r in rows:
        rid = r["样本"][:3]
        if rid in PROBES:
            continue
        if rid in TYPE_ONLY_POS:
            (ok if r.get(field) is None else bad).append(r["样本"])
            continue
        if r["期望"] == "pos":
            if tier == "advanced" and rid in PLATFORM_CORPUS_POS:
                continue
            (ok if (r.get(field) is not None and r[field] >= 70) else bad).append(r["样本"])
        elif r["期望"] == "neg" and rid in SCRIPT_JUDGEABLE_NEG:
            (ok if (r.get(field) is not None and r[field] < 70) else bad).append(r["样本"])
    return ok, bad


base = json.loads((OUT / "_calib_baseline.json").read_text(encoding="utf-8"))
v02 = json.loads((OUT / "_calib_v02.json").read_text(encoding="utf-8"))

for label, rows, field, tier in [
        ("v0.1.1（旧口径：总分含槽痕分）", base["rows"], "总分", "platform"),
        ("v0.2 · 平台档", v02["tiers"]["platform"], "主分", "platform"),
        ("v0.2 · 进阶档", v02["tiers"]["advanced"], "主分", "advanced"),
]:
    ok, bad = rate(rows, field, tier)
    print(f"{label}: 分开 {len(ok)}/{len(ok)+len(bad)} = "
          f"{round(len(ok)/(len(ok)+len(bad))*100,1)}%   未分开={bad}")
