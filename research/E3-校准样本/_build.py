# -*- coding: utf-8 -*-
"""构建 v0.2 阈值校准样本集（正例 ≥20 / 反例 ≥20）。

来源纪律：
  - 正例 P01–P06 / P07 / P08 直接复制 research/E-用例/ 的既有用例（原文未改写）。
  - P09–P24 取自 research/B-素材原文.md 与 research/C-大厂预设与提示词资料.md 的原词整段
    （出处行号写进文件名注释，不改写）。
  - 反例 N01–N04 为既有用例原文；N05 起为**构造反例**（按 B·§2.6 六类 slop / 七类污染 /
    硬失败清单的词例拼装），文件首行写「【构造】」标记，正文标出词例来源。
  - 每个文件首行写：# 期望=<pos|neg> ｜ 来源=... ｜ 说明=...
"""
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]      # research/
REPO = ROOT.parent
CASE = ROOT / "E-用例"
OUT = ROOT / "E3-校准样本"
POS = OUT / "正例"
NEG = OUT / "反例"

for d in (POS, NEG):
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------- 正例
POS_FILES = {}

# P01–P06 复制既有用例（原文不改写）
COPIES = {
    "P01_visionone_A_电影冒险.txt": "T01_visionone_A_电影冒险.txt",
    "P02_visionone_H_产品展示.txt": "T02_visionone_H_产品展示.txt",
    "P03_visionone_I_含对白短剧.txt": "T03_visionone_I_含对白短剧.txt",
    "P04_seedance25_陶瓷杯Example.txt": "T04_seedance25_陶瓷杯Example.txt",
    "P05_seedance_examples_zh_Character_drama.txt": "T09_seedance_examples_zh_Character_drama.txt",
    "P06_filmPreset_Kodak_Portra_400.txt": "T10_filmPreset_Kodak_Portra_400.txt",
    "P07_V017_九方面输出模板.txt": "T06_V017_九方面输出模板.txt",
    "P08_suno_Style_of_Music块.txt": "T11_suno_Style_of_Music块.txt",
}
for dst, src in COPIES.items():
    shutil.copyfile(CASE / src, POS / dst)

# P09 Vision-One B 延展（B-素材原文 L11633–L11643，原文整段）
POS_FILES["P09_visionone_B_延展已有视频.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L11633–L11643（templates.ts id 'B'，原文） ｜ 说明=成品提示词·延展型
Extend @video1 by 5s. Keep continuity of character identity, outfit, camera direction, and lighting.
0-2s (new segment): continue current motion seamlessly without jump cut.
2-5s (new segment): introduce one escalation action and resolve naturally.
Camera: same lens feel and movement language as @video1.
Audio: continue ambience; add subtle transition swell only at climax.
negative: no watermark, no logo.
"""

# P10 Vision-One J 一镜到底 + 多图航点（L11766–L11781）
POS_FILES["P10_visionone_J_一镜到底多图航点.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L11766–L11781（id 'J'，原文） ｜ 说明=参考素材职责·每图各自绑定用途
16:9 widescreen, 15s, espionage thriller style, continuous one-take tracking shot, no cuts, rainy evening, neon-reflected wet streets, suspenseful atmosphere
@image1 as first frame: protagonist in a dark coat walks forward, camera follows from the front at full-body framing
0-5s: steady front-tracking shot, passersby occasionally obscure the protagonist, rain droplets on lens edge, shallow depth of field on subject
6-10s: protagonist turns a corner past the building from @image2, camera pans to follow, a mysterious figure referencing @image3 is spotted lurking at the corner edge watching
11-15s: camera continues forward past the figure, protagonist approaches and enters the building from @image4, camera holds on the entrance as door closes, rain intensifies
Single continuous camera movement throughout, no cuts, no montage
negative: no watermark, no subtitles, no on-screen text, no jump cuts, no freeze frames
"""

# P11 Vision-One K 多段拼接（L11785–L11800）
POS_FILES["P11_visionone_K_多段拼接交接帧.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L11785–L11800（id 'K'，原文） ｜ 说明=段间连续 / 交接帧
## 第 1 段（0-15 秒）—— 正常生成
16:9 widescreen, 15s, fantasy cinematic, aerial establishing shot
0-5s: top-down view of swirling cloud sea over mountain peaks, camera slowly pushes down through cloud layer
6-10s: reveal a sword master standing on a cliff edge, back to camera, robes billowing, dark energy rising on the horizon
11-15s: sword master slowly turns to face camera, draws glowing blade, eyes determined, low voice: "It begins.", hold on a clean front-facing composition

交接帧：剑师正面中景，发光长剑出鞘，身后山脉，前方乌云翻涌

## 第 2 段（15-30 秒）—— 视频延展
Extend @video1 by 15s. Preserve character identity, outfit, lighting, and camera style.
0-5s: continuing from the sword master's stance, dozens of shadow creatures emerge from the dark clouds and charge forward, sword master leaps to meet them
6-10s: aerial combat sequence, blade trails cut through shadow forms that dissolve into ash particles, orbiting camera with dynamic tracking
11-15s: sword master lands gracefully, sheathes blade, residual golden particles drift in the air, camera slow push-in on profile against clearing sky, score fades to wind ambience
negative: no watermark, no on-screen text
"""

# P12 Vision-One D（L11662–L11671）
POS_FILES["P12_visionone_D_IP安全生物对战.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L11662–L11671（id 'D'，原文） ｜ 说明=纯文本·IP 安全 negative
vertical 9:16, 10s, 24fps, family-friendly original cartoon fantasy duel in a sunset forest clearing, vibrant cinematic lighting, expressive faces, smooth animation, high detail
Creature A: a tiny storm-rabbit with glowing cyan antlers and soft cloud-like fur, emits harmless spark particles
Creature B: a mini lava-iguana with crystal scales, ember freckles, and a floating flame orb above its tail
0-3s: dramatic stare-down, swirling leaves, warm sun rays through trees, slow push-in
3-7s: playful high-speed exchange, zigzag spark sprint versus curved ember spin, dynamic tracking camera, readable motion, clean silhouettes
7-10s: both land safely, smile, and perform a friendly team pose on two rocks under a glowing orange-pink sky, uplifting finish
negative: no existing franchise characters, no brand references, no logos, no watermark, no subtitles, no on-screen text, no violence, no injuries
"""

# P13 Vision-One E（L11676–L11685）
POS_FILES["P13_visionone_E_IP安全科幻英雄.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L11676–L11685（id 'E'，原文） ｜ 说明=角色昵称行 + 三段节拍
vertical 9:16, duration 10s, 24fps, original sci-fi hero short, cinematic city atmosphere after rain, reflective glass towers, cool blue and silver palette, family-friendly action tone, custom powered exo-suit with smooth ceramic panels, hex-light energy core, magnetic boots, forearm thrusters, expressive body language, polished animation quality
Main character nickname: Alloy Sentinel
Support character nickname: Orbit Mentor
0-3s: Alloy Sentinel stands on a high rooftop, suit systems boot sequence, hex-core pulses softly, vapor vents from shoulder ports, camera rises from boots to helmet in a dramatic reveal
3-7s: controlled flight through narrow skyline corridor, short lateral boosts, spiral climb around a tower, Orbit Mentor appears as a distant ally drone giving guidance lights, dynamic tracking camera, readable motion, crisp reflections
7-10s: Alloy Sentinel lands safely on a skybridge, energy core shifts from bright to calm glow, Orbit Mentor drone hovers at shoulder height, both face sunrise over the city, hopeful heroic ending
negative: no Marvel, no Iron Man, no Tony Stark, no Avengers, no arc reactor, no franchise references, no logos, no recognizable character likeness, no watermark, no subtitles, no on-screen text
"""

# P14 Vision-One F（L11690–L11699）
POS_FILES["P14_visionone_F_玩偶舞蹈动画.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L11690–L11699（id 'F'，原文） ｜ 说明=全素材参考·最长 negative
9:16 vertical, 10s, stylized toy dance animation in a clean studio set, one original vinyl-style toy figure performing an upbeat hip-hop routine, playful and family-friendly tone, smooth animation, clean silhouette readability, soft cinematic lighting, simple gradient backdrop, energetic music-video framing
0-3s: toy enters center frame in a neutral stance, subtle head nod and shoulder groove, camera slow push-in from full-body to medium shot
3-7s: main dance combo with clear toy-friendly movement, side step, heel-toe shuffle, arm wave, chest bounce, controlled half-turn, rhythmic camera drift, stable limb motion
7-10s: final combo, short forward glide, hand-point to camera, confident freeze pose, slight camera tilt and gentle punch-in for final beat
negative: no real person likeness, no celebrity likeness, no branded toy, no logos, no trademark symbols, no text on clothing, no watermark, no subtitles, no violent gestures, no broken joints, no extra limbs, no deformed hands, no flicker, no blur, no face distortion
"""

# P15 中文 Product I2V（L7639 原文）
POS_FILES["P15_zh_Product_I2V.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L7639（seedance 安全示例原文） ｜ 说明=参考素材型·写「用什么+不用什么」
[Image1]为产品参考，严格保持logo、标签、瓶身形状和颜色不变。镜头缓慢推进到标签特写；左侧暖光扫过玻璃，水珠沿瓶身下滑，背景保持暗色静止。声音：轻微环境声，结尾一声清脆玻璃音。
"""

# P16 中文 First/last frame（L7655 原文）
POS_FILES["P16_zh_First_last_frame.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L7655（seedance 安全示例原文） ｜ 说明=首尾帧·@图N 指代
@图1为首帧，@图2为尾帧。保持同一原创角色、服装和房间布局，角色从椅子上缓慢站起，走到窗边并停在尾帧姿势。动作连续自然，不跳切，不改变脸部、衣服或房间结构。镜头固定中景，仅轻微推镜。声音：安静室内环境声。
"""

# P17 中文 Camera-reference R2V（L7667 原文）
POS_FILES["P17_zh_Camera_reference_R2V.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L7667（seedance 安全示例原文） ｜ 说明=参考素材型·「仅参考 X，不复制 Y」
@图1锁定原创角色造型和服装，@视频1仅参考运镜节奏和侧向跟拍方式，不复制人物、场景或品牌。角色在雨夜街道从画面左侧跑入，停在路灯下回头。镜头横向稳定跟拍，最后固定中景。冷色雨光，地面反射霓虹。声音：雨声、脚步声，无配乐。
"""

# P18 中文 Action（L7661 原文）
POS_FILES["P18_zh_Action.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L7661（seedance 安全示例原文） ｜ 说明=中文紧凑成品·动作/光/声齐全
原创快递员在雨夜屋顶奔跑，跃过一道狭窄缝隙，落地后单膝撑住并冲向即将关闭的铁门。低机位手持跟拍，冷色屋顶灯和湿地反光。声音：急促呼吸、雨声、铁门提示音。
"""

# P19 火山 Seedance 2.5 案例句（C·3.1 原词整段）
POS_FILES["P19_火山25_案例_色温调色胶片.txt"] = """# 期望=pos ｜ 来源=C-大厂预设与提示词资料.md §3.1 火山 Seedance 2.5（案例原词） ｜ 说明=平台档·色温+比例+焦段+胶片
白平衡 4000K，青橙（teal-and-amber）调色，35mm，浅景深，胶片颗粒，弥漫的海雾，黄金时刻光晕。海雾中的灯塔 keeper 缓慢推灯，光柱扫过海面，镜头缓慢横移。
"""

# P20 火山 Seedance 2.0 画质模板案例句（C·3.1 原词）
POS_FILES["P20_火山20_画质模板案例.txt"] = """# 期望=pos ｜ 来源=C-大厂预设与提示词资料.md §3.1 火山 Seedance 2.0（实战案例句尾原词） ｜ 说明=平台档·厂商画质词模板正面使用
全程画面高清电影纪实风，色调温暖，光影柔和；人物面部稳定不变形，动作自然流畅，无卡顿无闪烁；环境音效与 @音频1 自然融合。原创人物在清晨巷口推车出摊，蒸笼热气升起，镜头缓慢跟拍。
"""

# P21 阿里百炼 文生图示例（C·3.4(b) 原句）
POS_FILES["P21_阿里_网球女运动员.txt"] = """# 期望=pos ｜ 来源=C-大厂预设与提示词资料.md §3.4(b) 阿里百炼原句 ｜ 说明=平台档·主体+静态特征+风格
网球女运动员，短发，白色网球服，黑色短裤，侧身回球，3D卡通风格。
"""

# P22 阿里百炼 折纸熊猫示例（C·3.4(b) 原句，含「最佳品质」）
POS_FILES["P22_阿里_折纸熊猫_最佳品质.txt"] = """# 期望=pos ｜ 来源=C-大厂预设与提示词资料.md §3.4(b) 阿里百炼原句 ｜ 说明=平台档·厂商语料「最佳品质」正面使用（C1 反例侧）
折纸杰作，牛皮纸材质的熊猫，森林背景，中景，极简主义，背光，最佳品质。
"""

# P23 im2 正向行 + 窄负面块（B-素材原文 L2630 + L2645 区，原词）
POS_FILES["P23_im2_窄负面块7项.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L2630、L2645 区（im2-clean-image 原文） ｜ 说明=负面卫生·窄块 7 项（B·§2.5「一条紧凑行优先」正锚点）
clean rendering, clear focal/support/quiet detail hierarchy, selective focal detail, broad calm masses, realistic detail only, natural texture only, controlled material rendering, clean gradients, soft diffused lighting, controlled highlights, subtle reflections only, matte or natural surfaces
Avoid: ghost texture, latent artifacts, hidden watermark-like marks, repeated micro-pattern noise, muddy shadows, noisy bokeh, pasted-on texture.
"""

# P24 emotion-prompt「开心」条（B-素材原文 L1072–L1089 原词）
POS_FILES["P24_emotion_开心条_可拍摄线索.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L1076–L1086（emotion-prompt 原文） ｜ 说明=2.2 情绪可拍摄化·生理线索（进阶档正例）
嘴部: 颧大肌收缩→嘴角向外上方牵引，上唇展平，可露上齿6-8颗；
      口轮匝肌松弛→双唇自然分开
眼部: 眼轮匝肌外侧纤维收缩→外眼角辐射状细纹，眼裂缩窄呈弯月状；
      下眼睑因眶部眼轮匝肌收缩上提
眉额: 额肌完全放松→额头平滑无纹；皱眉肌无收缩→眉间距正常
视线: 注视点直接锁定对象面部，眼动灵活，视线跳跃轻快不粘滞
"""

# P25 构造·参数独立行正例
POS_FILES["P25_构造_参数独立行正例.txt"] = """# 期望=pos ｜ 来源=【构造】按 B·§可先行落地 12.1 写法拼装（B-素材原文 12.1 词例 `--ar 16:9 --s 50`） ｜ 说明=12.2 独立参数行判定线正锚点
--ar 16:9 --s 50 --seed 12345

中景，一位饱经风霜的渔夫站在薄雾笼罩的码头，缓慢抬起渔网，目光停在远处灯塔。
warm practical key from frame left, cool blue rim；湿木板的反射，粗糙缆绳的纤维。
slow push-in from medium shot to close-up。
"""

# P26 构造·调色板比例正例（B-素材原文 L9948 原词句）
POS_FILES["P26_构造_调色板比例_60_30_10.txt"] = """# 期望=pos ｜ 来源=B-素材原文 L9948 原词句（`60% 暖赭石色，30% 深炭灰色，10% 铁锈红色`） ｜ 说明=5.2 进阶档正例·比例
60% 暖赭石色，30% 深炭灰色，10% 铁锈红色，保持 60/30/10。中景，陶艺师在工作室摆正一只浅蓝陶杯，柔和晨光从窗口进入，湿粘土有细腻光泽。镜头缓慢推近杯壁釉面纹理。
"""

for name, body in POS_FILES.items():
    (POS / name).write_text(body, encoding="utf-8")

NEG_FILES = {}

NEG_COPIES = {
    "N01_antislop_空词句.txt": "T07_antislop_空词句.txt",
    "N02_lira_否定slop_反例.txt": "T08_lira_否定slop_反例.txt",
    "N03_im2_长负面块19项.txt": "T12_im2_clean_image_Avoid长负面块.txt",
    "N04_占位符未填模板.txt": "T05_锁定观感块_Stage模板_未填.txt",
}
for dst, src in NEG_COPIES.items():
    shutil.copyfile(CASE / src, NEG / dst)

NEG_FILES["N05_构造_空词堆叠.txt"] = """# 期望=neg ｜ 来源=【构造】按 B·§2.6 六类 slop 第 1/2/6 类词例拼装 ｜ 说明=空词密度最高档
cinematic, epic, stunning, masterpiece, best quality, 8K, 32k UHD, highly detailed, trending on ArtStation, 电影感, 氛围感, 高级感, 大片感, 质感
"""

NEG_FILES["N06_构造_同义三连.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 六类 slop 第 5 类原词表 ｜ 说明=形容词堆叠（同义三连）
beautiful, stunning, gorgeous, dramatic, intense, powerful
"""

NEG_FILES["N07_构造_标签沙拉.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 六类 slop 第 3 类原词例 ｜ 说明=标签沙拉（逗号堆关键词，无动词无时间轴）
noir, rain, neon, moody, 4k, ultra detailed, dramatic lightning, dark alley, mysterious figure, cinematic grade, high contrast, sharp focus
"""

NEG_FILES["N08_构造_否定slop写正向.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 六类 slop 第 4 类原词例 ｜ 说明=否定 slop 散落正向正文
一位原创角色站在空旷街道中央，中景，暖色路灯。no blur, no artifacts, no extra fingers, no watermark
"""

NEG_FILES["N09_构造_负面旧失败记忆.txt"] = """# 期望=neg ｜ 来源=【构造】B-素材原文 L2612「Do not name old failed props…」规则 ｜ 说明=负面卫生·旧失败专名
一位原创角色站在空旷街道中央，中景，暖色路灯。镜头缓慢推近。
Avoid: 上次那张图里的蓝色杯子, 上一版的红色帽子, 之前那版的雨伞
"""

NEG_FILES["N10_构造_否定堆叠.txt"] = """# 期望=neg ｜ 来源=【构造】B-素材原文 L9930「不是卡通，不是动漫…」 ｜ 说明=否定堆叠（召唤被禁概念）
不是卡通，不是动漫，不是3D渲染，不要塑料感。原创角色，中景，站在走廊。
"""

NEG_FILES["N11_构造_参数混入散文.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 硬失败「把生成参数写进正文」（lira 规则 4） ｜ 说明=12.2 进阶档反例·参数混在散文句内
一个 4K 分辨率的 16:9 横画幅镜头里，9:16 vertical 的竖构图被裁切，时长 10s，帧率 24fps，男主站在雨夜街头缓慢回头，画面保持 --ar 16:9 的构图比例与 cinematic 调性。
"""

NEG_FILES["N12_构造_参数自相矛盾.txt"] = """# 期望=probe（参数矛盾检测探针） ｜ 来源=【构造】判据包 12.1 不通过项「参数自相矛盾」 ｜ 说明=12.1 反例
9:16 vertical, 16:9 widescreen, 10s, 4:3, 24fps, 30fps
"""

NEG_FILES["N13_构造_全空评价.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 六类 slop 第 1/6 类 + B·§2.4 中文空词表 ｜ 说明=零实词·全抽象评价
画面很美，光影很合适，构图很好，非常有质感，高级感拉满，氛围感很好，很有电影感。
"""

NEG_FILES["N14_构造_情绪词无外化.txt"] = """# 期望=neg ｜ 来源=【构造】D·S9「情绪必须可拍摄化」反例 ｜ 说明=抽象情绪词无线索
女主坐在桌前，非常生气，又很悲伤，内心极度激动，情绪复杂难以言说。中景。
"""

NEG_FILES["N15_构造_越权承诺.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 硬失败「无支撑的能力承诺（frame-accurate）」 ｜ 说明=13.5 越权承诺（本版只计不判，记录用）
请生成 frame-accurate 的视频，要求帧级精确、pixel-perfect 像素级一致，每一帧都要精确复刻参考图的每一根发丝。中景。
"""

NEG_FILES["N16_构造_语义污染内部泄漏.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 七类污染之「内部控制泄漏」 ｜ 说明=上一个/之前那版/本段/继续保持
上一个版本里我们用过中景，之前那版的光线不对，本段继续保持上一版的运镜，工作流注释：待补。
"""

NEG_FILES["N17_构造_冲突语义锚.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 七类污染之「冲突语义锚」 ｜ 说明=克制×爆发 / 锁定构图×完全不同视角
画面要极度克制安静，同时充满爆发式的能量；锁定固定构图，同时换一个完全不同的视角重拍。中景。
"""

NEG_FILES["N18_构造_标签负载污染.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 七类污染之「标签负载污染」 ｜ 说明=压迫感/史诗感/动态镜头 靠标签代可见证据
压迫感、史诗感、动态镜头、呼吸感、张力感。原创角色站在废墟上。
"""

NEG_FILES["N19_构造_边角占位符2处.txt"] = """# 期望=probe（结构面验证：不应硬失败） ｜ 来源=【构造】按 13.0「1–2 处边角占位符 → 记未定死清单，不硬失败」 ｜ 说明=占位符不应触发硬失败
中景，一位饱经风霜的渔夫站在薄雾笼罩的码头，缓慢抬起渔网。光源方向待填，镜头焦段 TODO。声音：远处海鸥。
"""

NEG_FILES["N20_构造_多镜头无锁定块.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 硬失败「多镜头无锁定观感块 / 每段多于一个主变化」 ｜ 说明=8.1/8.3 反例
镜头1：角色跑进房间，同时打开窗户又扔出信封，还顺手拉上窗帘。
镜头2：角色坐着，然后站起，又坐下，再次站起。
镜头3：画面结束。
"""

NEG_FILES["N21_构造_负面23项.txt"] = """# 期望=neg ｜ 来源=【构造】B-素材原文 L2624 长块（19 项）扩到 23 项 ｜ 说明=负面卫生·不合格档边界（>12）
一名陶艺师在工作室摆正浅蓝陶杯，柔和晨光从窗口进入，湿粘土有细腻光泽，中景。
Avoid: dirty texture buildup, random micro-pattern noise, hidden watermark-like marks, ghost texture, latent artifacts, muddy shadows, noisy bokeh, low-contrast residual textures, over-sharpened grime, uniform plastic gloss, pasted-on texture, milky reflections, clipped highlights, crushed blacks, dirty AO halos, malformed anatomy when people are present, stray text, logo, signature, username, copyright, error, blurry
"""

NEG_FILES["N22_构造_负面10项.txt"] = """# 期望=probe（档位边界，脚本层不判低） ｜ 来源=【构造】负面项数 10（落偏长档） ｜ 说明=负面卫生档位边界样本
一名陶艺师在工作室摆正浅蓝陶杯，柔和晨光从窗口进入，湿粘土有细腻光泽，中景。
Avoid: dirty texture buildup, random micro-pattern noise, ghost texture, latent artifacts, muddy shadows, noisy bokeh, pasted-on texture, milky reflections, clipped highlights, crushed blacks
"""

NEG_FILES["N23_构造_负面8项.txt"] = """# 期望=probe（卫生合格侧边界） ｜ 来源=【构造】负面项数 8 ｜ 说明=负面卫生档位边界样本（≤8 合格）
一名陶艺师在工作室摆正浅蓝陶杯，柔和晨光从窗口进入，湿粘土有细腻光泽，中景。
Avoid: dirty texture buildup, random micro-pattern noise, ghost texture, latent artifacts, muddy shadows, noisy bokeh, pasted-on texture, milky reflections
"""

NEG_FILES["N24_构造_负面13项.txt"] = """# 期望=probe（档位边界，脚本层不判低） ｜ 来源=【构造】负面项数 13 ｜ 说明=负面卫生档位边界样本（>12 不合格）
一名陶艺师在工作室摆正浅蓝陶杯，柔和晨光从窗口进入，湿粘土有细腻光泽，中景。
Avoid: dirty texture buildup, random micro-pattern noise, ghost texture, latent artifacts, muddy shadows, noisy bokeh, pasted-on texture, milky reflections, clipped highlights, crushed blacks, over-sharpened grime, uniform plastic gloss, dirty AO halos
"""

NEG_FILES["N25_构造_跨语言感受后缀.txt"] = """# 期望=neg ｜ 来源=【构造】B·§2.6 六类 slop 第 6 类跨语言词表 ｜ 说明=感受后缀（多语言）
vibey, 雰囲気のある, 감성적인, atmosférico, атмосферный
"""

NEG_FILES["N26_构造_参考素材型缺排除项.txt"] = """# 期望=probe（裁判项：1.3 判不通过，脚本只报不扣） ｜ 来源=【构造】按 1.3 不通过项 + B-素材原文 L10552「@Images 1 through 4 define four characters respectively.」 ｜ 说明=参考素材型·无用/不用声明（E·5.7 修复后的判法）
@Image 1 defines the character's appearance. @Image 2 defines the character's outfit.
一位原创角色站在雨夜街头，缓慢回头。中景，冷色雨光。声音：雨声，无配乐。
"""

NEG_FILES["N27_构造_参数混入散文短.txt"] = """# 期望=probe（进阶档反例；平台档允许内联） ｜ 来源=【构造】12.2 独立参数行判定线反锚点 ｜ 说明=参数与描述同一句、比例低
中景，陶艺师摆正陶杯，10s 的镜头里 9:16 竖构图，24fps，缓慢推近，暖光，wet clay sheen。
"""

NEG_FILES["N28_构造_方法论词误伤探针.txt"] = """# 期望=探针（构造）｜ 来源=【构造】用于校准对象类型判别线（方法论特征词计数） ｜ 说明=正常提示词里出现少量「建议/示例/方法」类词，不应被判方法论模板
建议使用中景，示例动作是缓慢抬手；这个方法能保住构图。请按上面写法填你的主体。
"""

for name, body in NEG_FILES.items():
    (NEG / name).write_text(body, encoding="utf-8")

index_rows = []
# 正例：复制件 + 构造件统一处理后写 index
_write_pos_index = []
for name in COPIES:
    src = COPIES[name]
    (POS / name).write_text((POS / name).read_text(encoding="utf-8"), encoding="utf-8")
    _write_pos_index.append((name, "期望=pos ｜ 来源=research/E-用例/" + src + "（原文复制，未改写）"))
for name, body in POS_FILES.items():
    lines = body.split("\n")
    header = lines[0].lstrip("# ").strip()
    (POS / name).write_text("\n".join(lines[1:]).lstrip("\n"), encoding="utf-8")
    _write_pos_index.append((name, header))

_neg_index = []
for name in NEG_COPIES:
    src = NEG_COPIES[name]
    _neg_index.append((name, "期望=neg ｜ 来源=research/E-用例/" + src + "（原文复制，未改写）"))
for name, body in NEG_FILES.items():
    lines = body.split("\n")
    header = lines[0].lstrip("# ").strip()
    (NEG / name).write_text("\n".join(lines[1:]).lstrip("\n"), encoding="utf-8")
    _neg_index.append((name, header))

with (OUT / "_index.tsv").open("w", encoding="utf-8") as f:
    f.write("样本\t期望\t来源与说明\n")
    for name, header in _write_pos_index + _neg_index:
        want = "pos" if "期望=pos" in header else ("neg" if "期望=neg" in header else "probe")
        f.write(f"{name}\t{want}\t{header}\n")

print("正例", len(list(POS.glob('*.txt'))), "反例", len(list(NEG.glob('*.txt'))),
      "index", (OUT / '_index.tsv').exists())
