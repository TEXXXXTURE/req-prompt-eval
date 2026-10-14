# A 路调研：AIGC 生图/生视频提示词的分类体系与控制维度

> 用途：为 `req-prompt-eval` skill 的「经典 AIGC 生图/生视频」场景判据包提供文献依据。
> 方法：公开网络多源检索（学术论文 + 官方文档 + 社区 wiki/教程 + 中文资料），交叉比对，逐条标注来源 URL。
> 采集日期：2026-10-14。抓取说明：部分站点（arxiv 正文页、stable-diffusion-art、runway academy、GitHub raw）直连抓取被拦截（返回 "Blocked: URL targets a private or internal network address"），改用搜索引擎返回的页面正文摘要作为依据；下文凡引用此类来源者均已注明。

---

## 0. 一个关键前提：存在「两套分类轴」，不要混为一谈

调研中最重要的一条元结论：**公开领域对提示词的「分类」实际上沿两条不同的轴展开，两者术语相近但切分逻辑完全不同**，设计判据包时必须先选定用哪条轴（或明确两轴并用）：

- **轴 A — 语义槽位轴（Semantic-slot axis）**：把提示词按「画面由哪些可见要素构成」切分——主体 / 场景 / 风格 / 光照 / 构图 / 镜头 / 色彩 / 画质。这是**实践指南**（Midjourney 官方、SD 教程、视频官方 prompt guide）的主流切法，也是负责人所说「动作的、场景的、画质杂乱的」这类直觉对应的轴。
- **轴 B — 修饰符功能轴（Modifier-function axis）**：把提示词按「每个词对模型起什么作用」切分——主体词 / 风格修饰 / 画质增强词 / 重复词 / 魔法词 / 图像提示。这是**学术分类**（Oppenlaender 2022）的切法，它不按画面内容分类，而按「这个 token 在干什么」分类。

来源分歧点：学术分类里根本没有「动作」「场景」「镜头」这些类目（它把场景并入「主体词 subject term」）；而实践指南里也基本不提「重复词」「魔法词」。做评测器时，**画面质量判据宜用轴 A 的槽位缺失/冲突来打分，而「画质杂乱」这类问题在轴 A、轴 B 里都有对应出口**（轴 A 是「画质/负面词」槽，轴 B 是「quality booster」+「negative prompt」机制）。

---

## ① 分类体系汇总表（类目 / 子类 / 作用 / 典型词例 / 来源）

下表以**轴 A（语义槽位）**为主干整合多源，括号内为各源采用的不同叫法。

| 类目 | 子类 | 作用 | 典型词例（中/英） | 来源 |
|---|---|---|---|---|
| **主体 Subject** | 人物/动物/物体/地点；外观、材质、服饰、表情、年龄 | 画面核心锚点；Anchor，缺它则模型自由发挥 | 一位饱经风霜的渔夫 / a weathered fisherman; 加州猫 / a calico cat | Midjourney 官方 Prompt Basics（subject/environment/lighting/color/composition）https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics ；stable-diffusion-art（8 类之「Subject」）https://stable-diffusion-art.com/prompt-guide/ ；Oppenlaender 2022（subject term，唯一「必需」类）http://arxiv.org/pdf/2204.13988v2 |
| **动作/姿态 Action & Pose** | 单个动作、表情、肢体语言、mid-action 动词 | 控制「正在发生什么」；视频里是最难也最关键的槽 | 慢慢地一手一手收网 / slowly hauls a wet rope hand over hand; mid-stride, dynamic motion blur; 一个动作/镜 | imagetoprompt（token order 第 5 位 Action/pose）https://www.imagetoprompt.dev/blog/stable-diffusion-prompt-guide/ ；Luma（Ray 系列公式：Subject+Mid-Action Verb...）https://opten.space/en/models/luma-ray ；Runway 官方（Subject action）https://academy.runwayml.com/guides/prompting-guide |
| **场景/环境 Scene & Environment** | 地点、时间、天气、大气、背景处理（清晰/虚化/极简）、道具 | 给主体上下文；决定光照与氛围的联动词 | 薄雾笼罩的山顶日出 / on a misty mountain peak at sunrise; 石港，晨雾 / a stone harbor, morning mist | Midjourney 官方（Environment）；openjourney SD 指南（Environment and Setting）https://www.openjourney.art/blog/stable-diffusion-prompts ；navosagent 中文（环境与场景层）https://www.navosagent.ai/zh/blog/ai-image-prompting-guide |
| **风格/媒介 Style & Medium** | 艺术运动、流派、媒介（油画/水彩/3D/摄影）、年代、艺术家引用 | 设定「latent 分布簇」；一个词就能大幅改观 | 油画/水彩插画/电影感照片 / oil painting, watercolor illustration, cinematic photograph, cyberpunk, art nouveau; by Greg Rutkowski | stable-diffusion-art（Medium + Style 两类）；Oppenlaender（style modifier）；veed SD3（7 元之 Style）https://www.veed.io/learn/stable-diffusion-3-prompts |
| **镜头/构图 Camera & Composition** | 景别（极远/远/中/特写）、角度（低/高/鸟瞰/荷兰角）、镜头（24/50/85mm、微距、鱼眼、移轴）、景深、构图法（三分法/居中/负空间） | 决定空间关系与「能不能用」；摄影真实感的最大杠杆之一 | 85mm f/1.4、浅景深、低角度 / 85mm lens, shallow depth of field, low angle, rule of thirds, bird's-eye view | Midjourney 官方（Composition）；uisdc 中文景别全表（极远景→极特写+特殊镜头）https://www.uisdc.com/aigc-61 ；imagetoprompt（Camera/technical） |
| **光照 Lighting** | 光源类型（自然/人工）、方向（正/侧/逆/顶）、光质（硬/软/漫射/体积光）、色温、光比；经典布光（伦勃朗/蝶形/分割/剪影） | 被多源公认为「最高杠杆槽」，直接决定质感与情绪 | 黄金时段逆光、柔光箱、体积光、霓虹反射 / golden hour, softbox, rim light, volumetric lighting, chiaroscuro; 暖色背光+冷色轮廓 | aigeartools（Lighting 为最高杠杆槽）https://aigeartools.com/midjourney-prompts ；stable-diffusion-art（Lighting）；navosagent（光线与氛围层+伦勃朗比例） |
| **色彩/调色 Color & Palette** | 色相倾向、饱和/去饱和、单色、互补色、胶片调色、hex 色值 | 影响整体色调关系与统一度 | 去饱和莫兰迪色 / desaturated pastel, muted, monochromatic, warm amber palette, Kodak Portra 400 | Midjourney 官方（Color）；navosagent 中文（调色板层）；Runway 实测（加 "desaturated pastel colors" 可保色彩一致）https://www.youtube.com/watch?v=rm-5TvlL8uU |
| **质感/材质 Texture & Material** | 表面材质、纹理、胶片颗粒、次表面散射、材质名 | 提升真实感/绘画质感；对视频还能掩盖闪烁瑕疵 | 拉丝铝、哑光陶瓷、细颗粒 / brushed aluminum, matte ceramic, film grain, subsurface scattering | vegueai SD 指南（Material）https://vogueai.net/blog/stable-diffusion-prompt-guide ；domer.io Luma（Texture 第六变量）https://domer.io/blog/luma-dream-machine-ai-video-workflow-guide |
| **画质增强词 Quality Boosters** | 分辨率、精细度、锐度、评价性夸张词 | 提高细节/锐度（是否有用存在大量分歧，见④） | masterpiece, best quality, highly detailed, 8K, sharp focus, trending on artstation | Oppenlaender（quality booster）；imagetoprompt（Quality tokens 置于最前）；stable-diffusion-art |
| **画质问题/负面词 Quality-Control & Negative** | 伪影类（模糊/噪点/jpeg 压缩/畸形手）、杂乱背景类、水印文字类、风格冲突类 | 排除不想要的；负责人所说「针对画质杂乱内容的」核心所在 | 模糊、多余手指、水印、杂乱背景 / blurry, extra fingers, watermark, busy/cluttered background | multic.com（负面词按「Quality & Artifact Prevention」「Content Control」分类，含 busy background/cluttered/distracting）https://www.multic.com/guides/negative-prompts-ai-art/ ；aiphotogenerator（质量/解剖/水印三大类）https://www.aiphotogenerator.net/blog/2026/02/negative-prompts-stable-diffusion-guide |
| **技术参数/输出约束 Parameters** | 宽高比、模型版本、stylize、chaos、seed、时长、分辨率 | 渲染开关，非画面语义 | --ar 16:9 --style raw --s 50（MJ）；(word:1.5)（SD）；--motion 1/2/3 | memons.ai MJ cheat sheet https://memons.ai/midjourney-prompt-cheat-sheet ；Midjourney 官方参数文档；veed SD3（Technical parameters） |
| **参考图/一致性 Reference & Consistency** | 图像提示、style ref、character ref、首/尾帧 | 锁定风格或主体，跨张跨镜一致 | --sref / --cref / --cw（MJ）；keyframes start/end（Luma）；reference image（Sora/Veo） | MJ cheat sheet；memons.ai Luma cheat sheet https://memons.ai/luma-prompt-cheat-sheet ；openai Sora skill prompting.md https://github.com/openai/skills/blob/82d2c5b4/skills/.curated/sora/references/prompting.md |
| **文字/画面内文本 Text-in-image** | 引号包裹的可见文案 | 控制图内文字（多数模型仍不可靠） | "Sign reading 'Open for Business'" | veed SD3（第七元 Text integration，SD3 需双引号）；Sora 2 有 Dialogue 块 |

**补充：参考结构顺序（多源给出的「推荐 token 顺序」）**

- stable-diffusion-art：Subject → Medium → Style → Art-sharing website → Resolution → Additional details → Color → Lighting。
- flywithai：Viewing Angle → Subject → Details → Medium → Style → Artist/Render → Lighting → Resolution/Focus。https://flywithai.co/prompt-guide
- imagetoprompt（SD）：Quality tokens → Medium/format → Subject → Subject details → Action/pose → Setting/environment → Lighting → Style/artist → Camera/technical。
- KDhimananda 五块法（2026）：[Subject] + [Medium/Style] + [Lighting/Color] + [Composition] + [Technical Parameters]。https://khimananda.com/blog/prompting-for-ai-image-generation
- navosagent（中文六要素）：[主题] + [风格与媒介] + [光线与氛围] + [构图与拍摄角度] + [色彩搭配] + [质量调整]。
- 夫子AI（中文六要素，Grok Imagine 实测）：主体 → 动作/姿态/表情 → 场景/环境 → 风格 → 构图/镜头 → 光影/氛围/色彩 → 用途约束。https://www.fuziai.com/136.html

**学术分类（轴 B，Oppenlaender 2022，arxiv:2204.13988）六类修饰符 + 五步法**

| 修饰符类型 | 功能 | 例 | 来源 |
|---|---|---|---|
| Subject term 主体词 | 指明主体（唯一必需） | "a landscape," "an old car in a meadow" | arxiv:2204.13988 |
| Image prompt 图像提示 | 用参考图提供主体/风格视觉目标 | 附一张参考图 URL | 同上 |
| Style modifier 风格修饰 | 指向艺术风格/媒介/流派/艺术家 | "oil painting," "cubist," "by Francisco Goya" | 同上 |
| Quality booster 画质增强词 | 纯提审美抛光/细节 | "trending on artstation," "8k," "masterpiece" | 同上 |
| Repeating term 重复词（solidifier 固化词） | 重复或同义改述以强化关联 | "space whale. a whale in space" | 同上 |
| Magic term 魔法词 | 加入语义远距词以制造不可预测变化 | "control the soul" | 同上 |

五步流程：**define（主体词/图像提示）→ modify（风格修饰/画质增强）→ solidify（重复词）→ vary（魔法词）→ mix/exclude（权重混合与排除）**。来源同上；英文学术源交叉验证见 aiwiki.ai https://aiwiki.ai/wiki/prompt_engineering_for_image_generation 与 emergentmind.com https://emergentmind.com/topics/artprompt 。
> 注：Oppenlaender 原文为 six types，个别二手转述（如 grokipedia）把类目名写成 "medium modifiers / artist modifiers / technical modifiers"，与原文 "image prompts / repetitions / magic terms" 不一致，属**转述讹误**，以原文（arxiv 2204.13988）为准。

---

## ② 生视频特有维度

视频在图像槽位之上叠加**「运动 + 时序」**这一整条轴。多源高度一致地把视频提示词拆成「视觉组件 + 运动组件」两组：

**Runway 官方（Gen-4.5）的分类最权威**：https://academy.runwayml.com/guides/prompting-guide
- 视觉组件（Visual components）：Subject appearance（主体外观）、Environment（环境）、Lighting（光照）、Composition/Framing（构图取景）、Style（风格）。
- 运动组件（Motion components）：Subject action（主体动作）、Environmental motion（环境运动）、Camera motion（运镜）、Motion style & timing（运动风格与节奏）、Direction & speed（方向与速度）。
- 官方建议结构：`[Camera] shot of [a subject/object] [action] in [environment]. [Supporting component descriptions]`；图生视频则 `The camera [motion] as the subject [action].`
- **时序控制**：Sequential prompting（`X occurs, then Y occurs. Finally, Z occurs.`）与**时间戳**（`[00:01] X occurs. [00:03] Y occurs.`）；时间戳建议与自然语言并用。

**运镜（Camera movement）——视频第一控制维度，母语词表跨源一致**
- Luma 运镜表：dolly in/out、truck left/right、crane up/down、pedestal up/down、orbit / arc around、tracking shot、handheld push-in、pull back、whip pan、overhead top-down、static/locked-off。https://memons.ai/luma-prompt-cheat-sheet
- 通用运镜词表（awesome-prompts / shotblock）：水平 pan/truck；垂直 tilt/boom/crane；纵深 dolly/zoom；复合 tracking/whip pan/handheld/gimbal；修饰 slow/fast/steady/shaky/floating/rapid。https://raw.githubusercontent.com/ai-boost/awesome-prompts/main/prompts/video_gen_prompting.txt
- **铁律（多源一致）**：**一个镜头 = 一个运镜 + 一个主体动作**；叠加两个运镜几乎必然失败。来源：Runway 官方、Sora 2 官方、Luma（opten.space）、artlist。

**首/尾帧（Keyframes）**
- Luma：设 start frame + end frame，模型在两端之间插值（interpolate），是「控制镜头起止最干净的方法」；且**只需描述帧之间的 CHANGE，不要重述静态元素**。https://opten.space/en/models/luma-ray-2 ；https://memons.ai/luma-prompt-cheat-sheet
- Sora 2：用 input image 锚定第一帧，prompt 描述「接下来发生什么」；无参考图时可先生成一张再作 input_reference。https://github.com/openai/skills/blob/82d2c5b4/skills/.curated/sora/references/prompting.md
- Runway：可用参考图作**尾帧**（last frame），让模型倒推填充，用于精确控制终点。

**一致性控制（Consistency）**
- 角色一致：MJ `--cref` + `--cw`；Luma "Character Reference"；Sora 用 character ID（建议每次生成 ≤2 个角色）；Veo 用参考图。
- 风格一致：MJ `--sref` + `--sw`；跨镜复用同一段固定描述（"storyboard bible" 式复用）。https://domer.io/blog/luma-dream-machine-prompt-guide
- 环境/角色锚定：把固定的环境块、角色块**逐字复用**到每个 prompt，只改动作与运镜。

**运动幅度/节奏**
- Luma「secondary motion（次级运动）」是让视频「活」的关键：风吹发丝、扬尘、水面涟漪、蒸汽、衣摆飘动。https://opten.space/en/models/luma-ray
- 表述时态：Luma 用**现在进行时**（running 而非 begins to run），模型不理解未来时/动作序列。
- 时长与指令遵循度负相关：模型在**较短片段**中更可靠遵循指令；Sora 建议 4s 两段拼接可能优于单条 8s。

**跨模型视频提示词结构（shotblock 研究文档汇总，含官方源交叉引用）** https://raw.githubusercontent.com/shanghaicellcenter/shotblock/master/docs/research/ai-prompt-conventions.md
- Veo 3.1（官方）：[Cinematography] + [Subject] + [Action] + [Context] + [Style & Ambiance]
- Kling 2.x：Subject + 主体描述 + movement + scene + scene 描述 +（camera language + lighting + atmosphere）；Kling 有**独立 negative-prompt 字段**。
- Luma Ray2（官方 learning hub）：Main subject → Action → Details → Scene → Style → Camera → Reinforcer
- Sora 2（OpenAI cookbook）：prose 场景描述 + 标注块（Cinematography / Camera shot / Mood / Actions / Dialogue）
- Runway Gen-4：图像承载「外观」，文本 prompt **几乎只描述运动**。
- 跨模型共识顺序：[1 景别+角度] → [2 主体+动作] → [3 场景] → [4 运镜] → [5 镜头光学] → [6 光照] → [7 风格/胶片/情绪]。

---

## ③ 负面词（Negative Prompt）体系

负面词按用途可分为**四个子类**（多源可交叉印证）：

| 子类 | 作用 | 典型词例（中/英） | 来源 |
|---|---|---|---|
| **A. 画质/伪影类** | 抑制模糊、噪点、压缩伪影、过曝欠曝 | lowres, worst quality, low quality, blurry, jpeg artifacts, grainy, noisy, pixelated, oversaturated / 低分辨率、模糊、噪点、过曝 | aiphotogenerator（质量类）；multic（Quality & Artifact Prevention） |
| **B. 内容/结构类**（含"杂乱背景"） | 抑制不想要的物体、畸形解剖、多余主体、**杂乱/拥挤背景** | extra fingers, fused fingers, bad anatomy, multiple subjects, duplicate; **busy background, cluttered, distracting background, messy, chaotic, noisy background** / 杂乱背景、拥挤、重复主体 | multic（Content Control 明确列 busy/cluttered/distracting background）；openjourney（messy background）；vogueai（cluttered background） |
| **C. 风格/媒介类** | 排除与目标风格冲突的渲染方式 | cartoon, anime, illustration, 3d render, CGI（要写实时）；photorealistic（要插画时） | imagetoprompt（photography-specific negatives）；aiphotogenerator（unwanted styles） |
| **D. 水印/文字/署名类** | 去掉水印、签名、logo、乱码文字 | watermark, text, signature, logo, username, copyright, error | stable-diffusion-art；AUTOMATIC1111 社区通用负面块 https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/2803 |

**视频特有负面子类（图像工具不存在）** —— 这是判据包里「视频场景」必须单列的一类：

| 子类 | 典型词例 | 来源 |
|---|---|---|
| 时序闪烁/频闪 | flickering, strobing, temporal inconsistency, frame jitter, flashing lights | buzzy.now Seedance 2.5 https://www.buzzy.now/blog/seedance-2-5-negative-prompts |
| 运动模糊/拖影 | motion blur, smearing, ghosting, trailing artifacts | 同上 |
| 形变/融化 | morphing, warping, melting, shape-shifting, object deformation | 同上；videoai.me Kling https://videoai.me/blog/kling-ai-negative-prompts |
| 运镜失控 | no camera drift, no handheld movement, no sudden zooms, unstable camera | artlist（Kling/Veo/Wan）https://artlist.io/blog/negative-prompts-ai-video/ |
| 面部漂移 | facial warping, changing facial features, warping fingers, jittery eyes | artlist；videoai.me |
| 音频失配（带音模型） | audio desync, garbled speech, overlapping voices, mouth not matching words, no background music, no copyright watermark | videoai.me；invideo https://invideo.io/faq/how-do-negative-prompts-work-in-ai-video-generation-and/ |

**负面词使用机制**
- 机制上负面词 = 同一条 guidance 的反号：把采样从「负面条件预测」外推离开（classifier-free guidance 方向的负向）。来源：Oppenlaender（负权重 "heart:-1"）；giveupinternet 记录 https://www.giveupinternet.com/w/negative-prompt
- 语法差异：SD 系 `(word:1.5)` 提高、`[word]` 降低、负面框放排除词；MJ 用 `--no text, watermark`；Kling/Veo API 有独立 negativePrompt 字段；Luma 部分模型**无负面框**（见④）。

---

## ④ 各来源之间的共识与分歧（不一致点逐一标注）

### 强共识（≥3 源且无明显冲突）
1. **主体优先、必需**：所有源都把 Subject 列为第一/唯一必需槽。
2. **光照是最高杠杆槽之一**：Midjourney 官方列入核心、aigeartools 称之为「single highest-leverage slot」、navosagent 列为「最关键且最易被忽略」。
3. **视频 = 视觉组件 + 运动组件**，且**一个镜头一个运镜 + 一个动作**：Runway 官方、Sora 2 官方、Luma、artlist 一致。
4. **首/尾帧插值与一致性引用**是视频控制标配（Luma keyframes、MJ --cref/--sref、Sora character ID）。
5. **负面词分「画质/内容/风格/水印」四类**，且**视频另有时序/形变类负面词**。

### 显式分歧（要标出来）
| # | 分歧点 | 各源立场 | 来源 |
|---|---|---|---|
| D1 | **类目数量与切法不一致** | MJ 官方 5 类（主体/环境/光照/色彩/构图）；flywithai 8 项；veed SD3 7 元；stable-diffusion-art 8 类；学术 6 类（但为功能轴,非槽位轴） | docs.midjourney.com；flywithai.co；veed.io；stable-diffusion-art.com；arxiv:2204.13988 |
| D2 | **画质增强词（quality booster）放前还是放后** | imagetoprompt 主张 **quality tokens 放最前**；stable-diffusion-art、openjourney 主张 **quality boosters 放最后** | imagetoprompt.dev vs stable-diffusion-art.com/openjourney.art |
| D3 | **顺序到底重不重要** | Runway 官方：**"structure and order are far less important than clearly conveying an idea"**；而 MJ 系（keenable/aigeartools/saneprompts）称 **"order matters, earlier words weighted more heavily"** | academy.runwayml.com vs aigeartools.com/memons.ai |
| D4 | **负面词该长还是该短** | SD1.5 传统：长负面清单（"indispensable"）；SDXL/SD3.5/qwe：**短、聚焦更好**，长清单反而更差甚至降质；Luma Ray2：**"positive only"，负面提示反效果** | aiphotogenerator.net；qwe.edu.pl；opten.space/en/models/luma-ray-2 |
| D5 | **"masterpiece/best quality" 等夸张词是否有用** | 老教程（SD1.5）当必备；vogueai 明言 **"some older workflows used quality tags heavily, but clear subject/lighting/composition matter more"**；qwe 指抽象词（"ugly"）模型无对应概念 | stable-diffusion-art.com vs vogueai.net / qwe.edu.pl |
| D6 | **权重语法是否通用** | SD 系 `(word:1.5)` 在 A1111/Forge/Fooocus/Invoke/ComfyUI 通用；但 **MJ 用 `::`**、**NovelAI 用 `{}`**、**DALL·E/Flux/Ideogram/Imagen 根本不支持权重语法**（写了只当字面括号）；ComfyUI/NightCafe 部分不支持 A1111 括号 | generativelabs.com/insights/prompt-syntax-for-stable-diffusion-faq |
| D7 | **视频 prompt 用自然语言 vs 关键词标签** | Runway/Luma/Sora 主张**自然句**（Luma 明说 "no brackets, no director syntax"）；Veo/Kling 容忍逗号分隔片段 | shotblock ai-prompt-conventions.md |

### 抓取失败记录（如实标注）
- `arxiv.org/html/2204.13988v3`、`stable-diffusion-art.com/prompt-guide/`、`academy.runwayml.com/guides/prompting-guide`、`raw.githubusercontent.com/.../ai-prompt-conventions.md`、`blog.athina.ai/...` 直连抽取被平台拦截（错误信息：`Blocked: URL targets a private or internal network address`）。上述来源的**具体内容均来自搜索引擎返回的页面正文片段**（即页面真实内容的索引快照），URL 可复核；未能拿到完整正文的页面已尽量用多个镜像/二手源交叉验证。
- 未发现需要付费墙或登录才能核验的关键结论。

---

## ⑤ 可信度自评

### 多源一致的强结论（可作为判据包硬规则）
1. **主体必填 + 光照高杠杆 + 视频一镜一运镜一动作**：论文（Oppenlaender）与三大厂商官方文档（Midjourney/Runway/Sora）与中文教程独立收敛 —— 强。
2. **视频提示词 = 视觉组件 + 运动组件 + 时序/关键帧**：Runway 官方表 + Sora 官方模板 + Luma 官方 hub + shotblock 汇总，四源一致 —— 强。
3. **负面词四分类 + 视频时序/形变负面子类**：multic/aiphotogenerator（图像）+ buzzy.now/videoai.me/artlist（视频）多源一致 —— 强。
4. **一致性控制靠引用（--cref/--sref/keyframes/character ID）**：MJ 官方 + Luma 官方 + Sora 官方 —— 强。

### 单源孤证（谨慎采用、标为可选规则）
- **"quality tokens 放最前"**（imagetoprompt.dev 单源，且与主流"放最后"相左）。
- **"50–150 词是单镜头最佳长度"**（仅 shotblock 汇总文档给出，Veo/Sora 原话未直接核实）。
- **Kling 3.0 的 "audio desync / tonal shift between cuts"** 之类具体词例（主要来自 videoai.me 单源营销博客）。
- **Seedance 2.5 的「5 类缺陷 → 负面词」对照表**（buzzy.now 单源，虽结构清晰但无第二源印证其词表有效性）。

### 最可疑的一条
**「负面提示词长度越长越好（社区版通用长负面清单）」** —— 这是流传最广却最可疑的说法。反证来自三处独立来源：qwe 指出 SDXL 用长负面清单**反而更差**、抽象词（"ugly"）模型无对应概念；aiphotogenerator 指 SDXL/SD3.5 应**缩短**负面词；Luma Ray2 甚至是**positive-only**。giveupinternet 的社区「勘误」条目也直言「负面词修好了手」是**把模型自身的进步误当成技巧**（"correlation was mistaken for craft"）。→ 判据包**不应把「负面词清单很长」当作加分项**，而应看负面词是否「具体、可见、按失败模式分类」。

### 对判据包设计的直接建议（供后续计划参考）
- 采用**轴 A 槽位**做打分骨架（主体/动作/场景/风格/镜头/光照/色彩/画质/负面/参数/一致性/文字），**轴 B 功能**用于「画质增强词是否堆砌空转」这类反模式判定。
- 视频场景单列一组判据：运镜唯一性、主体动作唯一性、时序/时间戳、关键帧/引用一致性、次级运动是否存在、时序类负面词是否覆盖。
- 权重/顺序类规则**做成「模型相关」开关**（SD/MJ/自然语言系三档），不要把 SD 语法当普适规则（见 D6）。

---

## 附：本报告引用来源清单（去重）

学术：
- Oppenlaender 2022, A Taxonomy of Prompt Modifiers for Text-To-Image Generation — http://arxiv.org/pdf/2204.13988v2 ；https://arxiv.org/html/2204.13988v3
- 转述/交叉验证：https://aiwiki.ai/wiki/prompt_engineering_for_image_generation ；https://emergentmind.com/topics/artprompt ；https://blog.athina.ai/a-taxonomy-of-prompt-modifiers-for-text-to-image-generation ；https://vidregen.com/blog/prompt-engineering-taxonomy
- Columbia CHI2022 Design Guidelines for Prompt Engineering T2I — https://www.cs.columbia.edu/~chilton/web/my_publications/LiuPromptsAIGenArt_CHI2022.pdf

官方文档：
- Midjourney Prompt Basics — https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics
- Runway Prompting Guide (Gen-4.5) — https://academy.runwayml.com/guides/prompting-guide ；https://help.runwayml.com/hc/en-us/articles/47313737321107-Text-to-Video-Prompting-Guide
- Sora 2 Prompting Guide — https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide.md ；https://github.com/openai/skills/blob/82d2c5b4/skills/.curated/sora/references/prompting.md
- HuggingFace Diffusers weighted prompts — https://huggingface.co/docs/diffusers/main/en/using-diffusers/weighted_prompts

社区/教程（英）：
- https://stable-diffusion-art.com/prompt-guide/ ；https://www.openjourney.art/blog/stable-diffusion-prompts ；https://www.imagetoprompt.dev/blog/stable-diffusion-prompt-guide/ ；https://flywithai.co/prompt-guide ；https://www.veed.io/learn/stable-diffusion-3-prompts ；https://vogueai.net/blog/stable-diffusion-prompt-guide ；https://www.generativelabs.com/insights/prompt-syntax-for-stable-diffusion-faq ；https://education.civitai.com/civitais-prompt-crafting-guide-part-2-intermediate/ ；https://www.qwe.edu.pl/tutorial/negative-prompts-stable-diffusion/ ；https://www.aiphotogenerator.net/blog/2026/02/negative-prompts-stable-diffusion-guide ；https://www.multic.com/guides/negative-prompts-ai-art/ ；https://memons.ai/midjourney-prompt-cheat-sheet ；https://memons.ai/luma-prompt-cheat-sheet ；https://opten.space/en/models/luma-ray ；https://opten.space/en/models/luma-ray-2 ；https://domer.io/blog/luma-dream-machine-prompt-guide ；https://domer.io/blog/luma-dream-machine-ai-video-workflow-guide ；https://aigeartools.com/midjourney-prompts ；https://artlist.io/blog/negative-prompts-ai-video/ ；https://videoai.me/blog/kling-ai-negative-prompts ；https://www.buzzy.now/blog/seedance-2-5-negative-prompts ；https://invideo.io/faq/how-do-negative-prompts-work-in-ai-video-generation-and/ ；https://raw.githubusercontent.com/shanghaicellcenter/shotblock/master/docs/research/ai-prompt-conventions.md ；https://raw.githubusercontent.com/ai-boost/awesome-prompts/main/prompts/video_gen_prompting.txt

中文资料：
- Sora 2 提示词指南（中文转译）— https://ciliy.com/news/1
- AI 图片提示词指南（六要素公式）— https://www.navosagent.ai/zh/blog/ai-image-prompting-guide
- 提示词工程第4讲：图片提示词（Grok Imagine，六要素）— https://www.fuziai.com/136.html
- 13 个 AI 摄影景别提示词（优设网）— https://www.uisdc.com/aigc-61
- ComfyUI 教程：AI 绘画提示词构成 — https://k.sina.cn/article_7879848900_1d5acf3c401902s8q8.html
- ComfyUI 实战：正负提示词与权重控制（五层语义结构）— https://zhuanlan.zhihu.com/p/1974213340822778903
