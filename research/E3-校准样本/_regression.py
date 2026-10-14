# -*- coding: utf-8 -*-
"""v0.2 回归：12 条 E-用例原文 × 两档，复跑并落盘（供 E3 报告§回归节引用）。"""
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = ROOT.parent
spec = importlib.util.spec_from_file_location("ac", REPO / "scripts" / "aigc_check.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

rows = []
for f in sorted((ROOT / "E-用例").glob("T*.txt")):
    text = f.read_text(encoding="utf-8")
    rec = {"用例": f.stem}
    for tier in ("platform", "advanced"):
        r = m.analyze(text, tier=tier)
        rec[tier] = {"主分": r["主分"], "判定": r["判定"], "对象类型": r["对象类型"].split("→")[0].strip(),
                     "分项": r["分项"], "空词密度": r["空词"]["每千字"],
                     "负面评级": r["负面行卫生"]["评级"], "素材型": r["参考素材型身份锁定"]["判定"],
                     "参考栏static": (r["参考栏_static"] or {}).get("总分")}
    rows.append(rec)

(ROOT / "E3-校准样本" / "_regression_12.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

hdr = ("用例", "平台主分", "平台判定", "进阶主分", "进阶判定", "对象类型",
       "空词密度", "负面评级", "素材型判定", "参考栏")
print(" | ".join(hdr))
for r in rows:
    p, a = r["platform"], r["advanced"]
    print(" | ".join(str(x) for x in (
        r["用例"], p["主分"], p["判定"], a["主分"], a["判定"], p["对象类型"],
        p["空词密度"], p["负面评级"], p["素材型"], p["参考栏static"])))
