# B · MOKE AIGC（mokeaigc.com）素材采集与写法分析

- 采集时间：2026-10-14（UTC+08:00）
- 采集者：Hermes 子 Agent（第 2 路调研）
- 采集方式：原生 curl（Windows 版）抓 HTML + Python 正则去标签；站点公开 JSON API 直取；GitHub 公开 API / raw 直取。**全程未登录、未注册、未授权任何账号，未执行站点上的任何脚本。**
- 素材原文全文：见同目录 `B-素材原文.md`（每个条目带来源 URL 与本地缓存文件名，便于复核）
- 本地缓存（复核用）：`C:/Users/A/.moke-scratch/`（站点页面、API JSON、GitHub 原始文件）

## 0. 采集总览

| # | 素材域 | 入口 | 性质 | 条数 |
|---|--------|------|------|------|
| A | 站点 SkillHub 目录 | `https://www.mokeaigc.com/api/skills?publicPage=skills&sort=downloads&page=1..8&limit=24` | 公开 JSON（无需登录） | 183 条元数据 |
| B | 站点 Skill 正文（SKILL.md） | `https://www.mokeaigc.com/api/skills/{namespace}/{slug}` → `item.parsed_metadata_json.body` | 公开 JSON，含**完整 SKILL.md 正文** | 42 份（合计 493,515 字符 / 620 KB UTF-8，落盘为 42 个 .md） |
| C | 站点公开页面文案 | `/`、`/skill.html`、`/mcp.html`、`/today.html` | HTML（公开） | 4 页，含提示词库用法示意与 agent 指令模板 |
| D | GitHub `MOKEAIGC/MOKE-Vision-One` | `components/seedance/templates.ts` 等 | 开源仓库源码 | 11 条成品视频提示词 + 80 条术语 + 29 条胶片片段 + 3 条元提示 + 1 套氛围规则 |
| E | GitHub `MOKEAIGC/MOKEAIGC-work-V017` | `MOKEAIGC-work V017 .md` / `MOKEAIGC-work V09 .md` | 开源仓库 Markdown | 2 份世界观构建 Skill 全文 |
| — | **可引用素材条目合计** | | | **88 条**（分解见 §①） |

**关键发现（决定了采集路径）**：站点「提示词库」（`/cinematique.html`）、`/videos.html`、`/tutorial.html`、`/film-stills/` **均需登录**（HTTP 302 → `/auth/login?returnTo=...`，跳转后落回 `www.mokeaigc.ai/` 首页），首页底部亦明示「提示词库等受保护内容需要登录；MCP 需要单独授权」。因此提示词库**正文抓不到**；但站点把大量方法论沉淀成了 Skill，而 Skill 详情 API **完全公开**（含 SKILL.md 全文），这是本次素材的主干来源。GitHub 组织 `MOKEAIGC` 补上了成品提示词与词库。

---

## ① 采集清单

### 1.A 站点 SkillHub 目录（183 条，公开 JSON）

- 来源：`https://www.mokeaigc.com/api/skills?publicPage=skills&sort=downloads&page={1..8}&limit=24&includeSections=1`
- 类型：目录元数据（display_name / summary_zh / summary_en / download_count / star_count / front_category / group_name / version / published_at / security_verdict …）
- 实测：`pagination.total = 183`，8 页取全（24×7+15=183），本地 `api/catalog.json`
- 分类分布（实测计数）：`text 106 / video 29 / image 15 / engineering 13 / automation 9 / research 7 / operations 4`；分组：图像与视频 111、工具与数据 47、开发与自动化 11、研究与情报 6、效率与工作流 5、学习与知识 3
- 下载量 Top5 原文条目：

```
0 mariozhaofan--personal/director-seedance-prompt | dl 1398 | text
  将脚本、小说、参考图、序列帧、已接受的视频、音频、故事板、粗略想法或现有提示词编译为导演级电影视频提示词。
1 anisn--personal/emotion-prompt | dl 765 | text
  AI视频真人表情情绪控制提示词生成系统。三层架构（主体情绪+面部细节+核心姿态），20种情绪全覆盖，双层结构（肌肉动作→视觉结果），支持多阶段情绪转换和呼吸控制。
2 mariozhaofan--personal/viral-screenwriter | dl 752 | research
3 honghouzi--video/professional-storyboard-director | dl 580 | video
4 global/seedance | dl 573 | text
```

### 1.B 站点 Skill 正文（42 份 SKILL.md，逐条）

- 取用方式：`GET /api/skills/{namespace}/{slug}` → `item.parsed_metadata_json.body`（Markdown 全文）、`item.manifest_json`（文件清单）、`item.security_verdict`。
- 42 份全部落盘为独立 .md（本地 `api/bodies/`），下文标「全文见原文文件」的即该目录同名文件。

| # | namespace/slug | 下载 | 正文长度(字符) | 版本 | 包内文件 | 主题（summary_zh 截断） |
|---|---|---|---|---|---|---|
| 1 | `5efke4no6wd5--personal/game-scene-631` | 311 | 3752 | 20260903.124418 | 3 | 该技能用于设计、改写、生成或评析游戏环境与影视场景图像，采用灵活的6:3:1层级结构，统筹构图、光照、色彩、空间布局、资产形态与信息密度。适 |
| 2 | `5efke4no6wd5--personal/sd25-physics-prompt` | 353 | 27826 | 20260903.124412 | 1 | 本技能用于优化或改写Seedance 2.5视频提示词，重点增强物理真实感与因果连续性。它帮助用户将创意或草稿转化为清晰、可执行的提示词，涵 |
| 3 | `99job--99job/chinese-aesthetic-video-director` | 161 | 1694 | 20260921.232907 | 6 | 根据一句想法、参考图片、人物资产、已有镜头或生成失败结果，编写、续写和修复中式东方美学 AI 视频提示词。适用于中式园林、东方情绪短片、风光 |
| 4 | `anisn--personal/cinematic-scene-prompts` | 360 | 4103 | 0.9.1 | 5 | 将剧情编写或改写为跨风格AI视频分镜提示词，支持实拍与动画媒介、混合风格及首尾帧和分镜图提示词。重点处理动作证据、情绪、空间、声光与连续性， |
| 5 | `anisn--personal/emotion-prompt` | 765 | 9326 | 20260823.062103 | 1 | AI视频真人表情情绪控制提示词生成系统。三层架构（主体情绪+面部细节+核心姿态），20种情绪全覆盖，双层结构（肌肉动作→视觉结果），支持多阶 |
| 6 | `doudingjueshi--personal/generate-four-dimensional-voice-prompt` | 183 | 1360 | 20260922.143953 | 4 | 将简短场景、人物处境、对白构想或 AI 视频镜头扩写为严格四维的中文表演提示词，固定使用“场景、人物状态、发声方式、台词”四个标签，并把专业 |
| 7 | `erdong--personal/image-impact-frame` | 175 | 8145 | 1.1.2 | 9 | 该技能用于为战斗漫剧或动作场景中的冲击帧生成可直接使用的AI图像提示词，聚焦打击命中的单一瞬间。它涵盖三条核心原则、四种力量结构与五种帧型、 |
| 8 | `erdong--personal/image-portrait-3x4` | 71 | 1902 | 1.1.1 | 7 | 这是一个从零生成 3:4 竖版肖像出图提示词的工具。它锁定 3:4 比例，把骨相、五官、识别、气质四项身份定值写入并固定，画面只保留头部、颈 |
| 9 | `erdong--personal/image-swiss-poster` | 84 | 1806 | 1.1.1 | 27 | 把任意角色编译成现代瑞士主义（国际主义平面设计 / Modern Swiss Style）风格的竖版角色海报提示词——超大无衬线标题、非对称 |
| 10 | `global/roger-deakins-cinematography` | 403 | 8733 | 1.0.0 | 3 | 罗杰·迪金斯（Roger Deakins）摄影风格大师。涵盖其标志性摄影语言的完整知识体系：自然主义打光、 极简构图、阴影叙事、建筑框架、克 |
| 11 | `global/seedance` | 573 | 2654 | 20260809.100404 | 7 | 此技能用于生成视频提示词、创建Seedance提示词、撰写视频描述，或涉及Seedance、即梦平台、视频提示词、视频生成、AI视频、短剧、 |
| 12 | `honghouzi--personal/im2-clean-image-清洁图像` | 556 | 22148 | 1.0.0 | 7 | 为 IM2 / GPT Image 2 图像生成、重绘与照片修复提供材质真实感、信息密度、干净渲染、负面提示和证据保真控制；适用于画面清理、 |
| 13 | `honghouzi--personal/minimax-h3-prompting-海螺提示助手` | 279 | 19933 | 2.7.0 | 6 | 将创意需求引导为可生成的 MiniMax H3 / 海螺 H3 提示词，并针对 T2VA、I2VA、FL2VA、L2VA 与 Ref2VA  |
| 14 | `honghouzi--personal/prompt-library-提示词库管理` | 226 | 1749 | 1.0.0 | 7 | 引导收集、拆解、评分、归档和复用提示词，覆盖结构分析、技巧识别、质量矩阵、适用性判断和索引更新。 |
| 15 | `honghouzi--video/ai-video-prompt-director` | 142 | 70020 | 1.0.0 | 5 | AI视频提示词导演工具：以研究、结构、剧作、镜头、表演、动作、声音和生成约束为一体，组织完整的电影化视频提示词工作流。用于导演模式、片场模式 |
| 16 | `honghouzi--video/ai-video-prompt-preflight` | 165 | 44716 | 1.0.0 | 6 | AI视频提示词提交前检查工具：在生成前检查可执行性、内部冲突、参考图职责、资产准备、时间负载、镜头数量、连续性和模型适配问题。用于正式提交提 |
| 17 | `honghouzi--video/cinematic-music-sound-design` | 230 | 7974 | 1.0.0 | 7 | 电影配乐与声音设计工具：设计主题动机、速度、节拍、和声、配器、环境声、拟音、冲击声、静默、空间声场和声画关系。用于影片配乐、声音叙事和时间点 |
| 18 | `honghouzi--video/high-tension-shot-design` | 374 | 9641 | 1.0.0 | 12 | 高张力镜头设计工具：通过景别、机位、构图、透视、镜头运动、速度感、剪辑节拍和视觉重心增强画面张力。用于动作、悬念、冲突、海报和强视觉冲击镜头 |
| 19 | `honghouzi--video/jimeng-sd2-prompting` | 141 | 40834 | 1.0.0 | 3 | 即梦SD2提示词工具：为即梦SD2、Seedance 2.0及相关视频模型创建、改写和诊断提示词，并利用时间连接词组织自然的动作、表演和镜头 |
| 20 | `honghouzi--video/mokeaigc-v9` | 331 | 16790 | 1.0.1 | 1 | MOKEAIGC V017 规则作用域修订版：世界观构建、生物设计与视觉构图探索，默认交付世界设定和九张电影感图像提示词。 |
| 21 | `honghouzi--video/prompt-contamination-guard` | 181 | 9013 | 1.0.0 | 2 | 提示词污染防护工具：清理图像和视频提示词中的上下文残留、否定联想、纠错痕迹、默认模板、内部术语和互相冲突的控制语句。用于正式生成前获得干净、 |
| 22 | `honghouzi--video/seedance-20` | 219 | 12574 | 6.1.0 | 261 | Seedance 2.0总控工具：根据任务选择提示词、镜头、动作、角色、声音、连续性、风格、特效和故障排查模块，组织完整的Seedance视 |
| 23 | `honghouzi--video/seedance-antislop` | 140 | 3657 | 6.1.0 | 1 | Seedance反套路工具：识别并消除空泛电影感、无意义运镜、堆砌形容词、模板化节奏和廉价AI感，让提示词更具体、更有因果关系。用于提升Se |
| 24 | `honghouzi--video/seedance-camera` | 162 | 4086 | 6.1.0 | 1 | Seedance镜头工具：设计景别、机位、构图、镜头运动、焦点、轴线和镜头衔接，并限制不必要的运镜。用于Seedance镜头语言和摄影控制。 |
| 25 | `honghouzi--video/seedance-examples-zh` | 137 | 2343 | 6.1.0 | 1 | Seedance中文示例库：提供中文提示词结构、镜头、动作、角色、声音和常见场景示例。用于需要中文Seedance提示词范例与快速套用参考时 |
| 26 | `honghouzi--video/seedance-fight-director` | 517 | 13319 | 1.0.0 | 5 | Seedance打斗导演工具：为Seedance 2.0设计具备站位、距离、攻防因果、身体力学、节奏、镜头和打击反馈的动作场面。用于武打、搏 |
| 27 | `honghouzi--video/seedance-lighting` | 185 | 3427 | 6.1.0 | 1 | Seedance灯光工具：设计主光、辅光、轮廓光、环境光、色温、方向、强弱、动态变化和材质响应。用于Seedance场景气氛、时间状态和人物 |
| 28 | `honghouzi--video/seedance-motion` | 167 | 4275 | 6.1.0 | 1 | Seedance运动工具：描述角色、物体、布料、头发、镜头和环境运动的起因、路径、速度、重量、惯性与结束状态。用于提升动作清晰度和物理可信度 |
| 29 | `honghouzi--video/seedance-prompt-short` | 132 | 2347 | 6.1.0 | 1 | Seedance精简提示词工具：在有限字数内保留主体、核心动作、镜头、场景和关键限制，输出直接可用的短提示词。用于快速生成或模型更偏好简洁输 |
| 30 | `honghouzi--video/seedance-prompt` | 145 | 9798 | 6.1.0 | 1 | Seedance完整提示词工具：把创意整理为包含主体、场景、动作、镜头、光线、声音、节奏、连续性和限制条件的生成级提示词。用于复杂或高质量S |
| 31 | `honghouzi--video/seedance-recipes` | 140 | 4824 | 6.1.0 | 1 | Seedance配方库：提供常见题材、镜头、动作、访谈、产品、叙事和视觉风格的可复用组合方法。用于快速选择成熟结构并按任务调整。 |
| 32 | `honghouzi--video/seedance-troubleshoot` | 147 | 5585 | 6.1.0 | 1 | Seedance故障排查工具：诊断人物漂移、动作失真、镜头混乱、口型问题、画面污染、闪烁和生成失败，并给出最小重试方案。用于结果异常或需要定 |
| 33 | `honghouzi--video/seedance-vfx` | 411 | 5064 | 7.0.0 | 1 | Seedance视觉特效工具：编排能量、烟雾、火焰、破坏、粒子、光效和环境交互的发生阶段、运动规律、材质与镜头关系。用于Seedance特效 |
| 34 | `honghouzi--video/seedance-vocab-en` | 127 | 3005 | 6.1.0 | 1 | Seedance英语词汇库：整理英语环境下常用的镜头、动作、表演、光线、材质、声音和风格表达。用于英文提示词编写、翻译和词汇选择。 |
| 35 | `honghouzi--video/seedance-vocab-zh` | 160 | 1753 | 6.1.0 | 1 | Seedance中文词汇库：整理中文环境下常用的镜头、动作、表演、光线、材质、声音和风格表达。用于中文提示词编写、改写和专业词汇选择。 |
| 36 | `honghouzi--video/visual-style-aesthetic-direction` | 327 | 21301 | 1.0.0 | 11 | 视觉风格与审美导演工具：为摄影、电影、插画、动画、三维、平面、产品、时尚和建筑等方向建立高级视觉风格系统。用于风格探索、审美统筹和提示词视觉 |
| 37 | `mariozhaofan--personal/director-seedance-prompt` | 1398 | 16917 | 20260902.032227 | 17 | 将脚本、小说、参考图、序列帧、已接受的视频、音频、故事板、粗略想法或现有提示词编译为导演级电影视频提示词。适用于分镜、镜头提示词、视频提示词 |
| 38 | `mariozhaofan--personal/reference-lut-generator` | 80 | 2868 | 20261010.134834 | 10 | 根据参考视频或图像提取色彩风格，生成可复用的 .cube LUT、三栏对比及完整交付包，包含媒体处理与 LUT 验证工具。 |
| 39 | `q7r6a384b4fv--personal/cinematic-zhang-yimou` | 152 | 713 | 20261004.023552 | 12 | 使用张艺谋（Zhang Yimou）的构图、光线、色彩与人物关系，生成原创电影单帧或生图提示词。适用于用户指定这位导演视觉语言的电影静帧、关 |
| 40 | `q7r6a384b4fv--personal/lira-image-prompts` | 211 | 16051 | 20260827.145747 | 1 | 为 AI 图像生成与编辑编写、诊断和优化生产级提示词，覆盖角色、场景、道具和局部修复工作流。 |
| 41 | `q7r6a384b4fv--personal/seedance-2-5-prompting` | 229 | 15435 | 20261003.154046 | 7 | 为 Seedance 2.5 / Dreamina 2.5 的视频生成、编辑和延长编写提示词。当目标模型为 Seedance 2.5，或任务 |
| 42 | `q7r6a384b4fv--personal/suno-music-prompts` | 187 | 30054 | 20260827.145740 | 10 | Suno AI v5.5 音乐提示词专家（2026-03-27 规范对齐）。覆盖 Voices 个人声模型、Custom Models 自定 |

> 主题列为站点 `summary_zh` 原文截断；完整摘要见 `B-素材原文.md` 第四部分（183 条目录全表）。

#### 重点素材逐条摘录（原文，非概括）

**B-19 `prompt-library-提示词库管理`**（本任务最有价值的一条——它本身就是一个「提示词评测框架」）
URL：`https://www.mokeaigc.com/api/skills/honghouzi--personal/prompt-library-%E6%8F%90%E7%A4%BA%E8%AF%8D%E5%BA%93%E7%AE%A1%E7%90%86`
原文：
```
当用户发送提示词时，自动进行：
1. 结构拆解（6要素分析）
2. 技巧识别（8种常见技巧）
3. 质量评估（5维度评分）
4. 适用性分析（判断是否适合我）
5. 智能应用（自动融入系统设定）

### Step 2: 结构拆解 —— 6要素分析：角色定义/任务描述/知识注入/推理框架/输出格式/约束条件
### Step 4: 质量评估 —— 5维度评分
| 维度 | 分数 |
| 清晰度 | X/5 |
| 完整性 | X/5 |
| 可执行 | X/5 |
| 鲁棒性 | X/5 |
| 创新性 | X/5 |
评级：S/A/B/C/D + 适用性（高/中/低）
```
→ 与我们的评测器定位高度重合，是**唯一给出中文评级档（S/A/B/C/D）与五维评分维度**的现成框架。

**B-6 `seedance-prompt` 的 Director Formula 与压缩顺序**（原文表）
```
Use `Subject + Action + Scene + Camera + Lighting/Style + Audio + Constraints`.
| Slot | Use for | Prompt-ready pattern |
| Subject | The anchor the model must track. | `Original ceramic perfume bottle on black acrylic, label preserved exactly` |
| Action | The visible change. | `condensation beads form and slide down the glass over five seconds` |
| Scene | Only what is not already in references. | `quiet rain-lit kitchen counter, shallow depth of field` |
| Camera | One primary move with endpoint. | `slow dolly-in from medium product shot to macro label detail` |
| Light and style | Physical light plus safe visual language. | `warm practical key from frame left, cool blue rim, clean commercial realism` |
| Audio | Ambient bed, SFX, dialogue, or silence. | `Sound: low room tone, soft glass chime on final frame` |
| Stability locks | Preservation and positive state anchors. | `logo, shape, label, and cap geometry remain unchanged` |

When the prompt is too long, cut in this order: duplicate style adjectives, generic quality words,
background details visible in references, secondary camera moves, secondary actions, and speculative
emotional labels. Keep preservation constraints, action timing, and role maps.
```

**B-6 的「Liu 可粘贴提示词硬门」六段顺序**（原文，`seedance-prompt` / `jimeng-sd2-prompting` / `seedance-vfx` 三处一致）：
```text
角色/资产锁定
视觉材质总控
镜头语言总控
事件节拍
声音
正向稳定约束
```
并附带硬规则原文：`the model-ready code block is positive-only. It states only what is present, visible, audible, active, and locked in the current shot. Exclusion, absence, correction, comparison to old attempts, and previous-failure wording stay outside the copyable block.`

**B-7 `seedance-2-5-prompting` 的官方模板与 Example（原文全录）**
```
Core formula: Subject + Action or Event + Scene and Environment + Visual Style + Camera/Cut + Audio
Template:
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <visual style>.
Use <shot size, camera angle, camera movement, or cuts>.
Audio includes <dialogue, ambience, sound effects, or music>.
Example:
A ceramic artist finishes a pale blue cup in a studio at dawn, lifts it from the wheel,
and places it in the center of a wooden shelf.
Soft morning light enters through the window. The wet clay has a delicate sheen.
Begin with a medium shot of the wheel-throwing process, slowly push in toward the cup's
surface texture, then cut to a frontal view of the shelf.
Retain the low hum of the pottery wheel, the friction of clay, and subtle indoor ambience.
```
多镜头开场「锁定观感块」（原文）：
```
[LOOK — LOCKED, APPLIES TO EVERY SHOT]
<camera body / capture format>, <lens set>, <stock or sensor>, <optical format>, <T-stop>,
<depth of field>, <grain>, <highlight behaviour>, <black level>, <contrast>.
<Grade name>: <hero tone>, <secondary field>, <shadow bias>.
<Camera operation>. <Performance and audio baseline>.
```
音频/字幕分隔符表（原文）：`音乐 ()`、`音效 <>`、`台词 {}`、`字幕 【】`；分阶段结构 `[Generation Goal] / [Stage 1] Initial state / Primary event / End state / [Maintain Consistency]`。

**B-9 `seedance-antislop` 的空词六类与替换表（原文）**
```
| Filler | Ask what it means | Strong replacement pattern |
| cinematic | What camera and light make it cinematic? | `locked close-up, warm practical key, cool rim light` |
| epic | What is the scale or stake? | `wide low-angle shot, tiny figure against storm wall` |
| beautiful | What color, texture, or light behavior? | `pearl highlights on wet ceramic, soft window bounce` |
| dynamic | What moves, how fast, and where does it end? | `fast lateral track ending on the hero label` |
| professional | What production setup? | `clean commercial tabletop, controlled reflection, no clutter` |

The Six Slop Classes:
1. Empty evaluators (cinematic, epic, stunning)
2. Borrowed image-model tokens (8K, masterpiece, trending on ArtStation)
3. Tag salad (comma keyword dumps ported from image prompting)
4. Negation slop (no blur, no artifacts, no extra fingers)
5. Adjective stacking (three synonyms for one quality)
6. Feel-suffix words (电影感, 雰囲気のある, 감성적인, atmosférico, атмосферный, vibey)
```
→ 这是**天然的反例集**：每一条「差提示词特征」都可以直接当评测器的扣分项定义。

**B-10 `prompt-contamination-guard` 的污染七类（原文标题 + 关键句）**
```
Old-context residue / Correction and exclusion leakage / Default-template contamination /
Loaded-label contamination / Positive semantic over-weighting / Internal-control leakage /
Conflicting semantic anchors
"Exclusion, absence, correction… the unwanted noun remains semantically active even when the sentence rejects it."
"Internal-control leakage: 上一个 / 之前那版 / 本段 / 继续保持"
```

**B-22 `seedance-examples-zh` 中文成品示例（原文 10 条，示范 4 条）**
```
Product I2V: [Image1]为产品参考，严格保持logo、标签、瓶身形状和颜色不变。镜头缓慢推进到标签特写；左侧暖光扫过玻璃，水珠沿瓶身下滑，背景保持暗色静止。声音：轻微环境声，结尾一声清脆玻璃音。
Character drama: 原创角色A站在狭窄走廊，缓慢放下信封，目光停在紧闭的门上。镜头为稳定中近景并轻微推进。暖色顶灯微微闪烁，墙面有冷色雨光反射。声音：远处雨声，无配乐。
Action: 原创快递员在雨夜屋顶奔跑，跃过一道狭窄缝隙，落地后单膝撑住并冲向即将关闭的铁门。低机位手持跟拍，冷色屋顶灯和湿地反光。声音：急促呼吸、雨声、铁门提示音。
First/last frame: @图1为首帧，@图2为尾帧。保持同一原创角色、服装和房间布局，角色从椅子上缓慢站起，走到窗边并停在尾帧姿势。动作连续自然，不跳切，不改变脸部、衣服或房间结构。镜头固定中景，仅轻微推镜。声音：安静室内环境声。
```

**B-21 `seedance-prompt-short` 压缩优先级（原文）**
```
Preserve in this order: 1. Reference tags and their role. 2. Subject or product identity.
3. Action verb and visible endpoint. 4. One camera move. 5. Physical light source or atmosphere.
6. Audio cue or silence instruction. 7. Safety, IP, or continuity constraint.
8. Sequence state clauses…
Return one compact prompt, ideally 30-100 English words
```

**B-11 `im2-clean-image` 提示词书写顺序 + 负面卫生（原文）**
```
Build IM2 prompts in this order:
1. Subject, identity, pose, action, and setting.
2. Style or medium, if the user requested one.
3. Camera, composition, and hierarchy scaffold…
4. Light path and material layer…
5. Distance and information-density falloff…
6. Controlled-detail clean layer…
7. Negative hygiene layer…

Negative-Prompt Hygiene 核心规则：the negative slot is not a memory of old failures.
Safe default avoid block:
Avoid: dirty texture buildup, random micro-pattern noise, hidden watermark-like marks, ghost texture,
latent artifacts, muddy shadows, noisy bokeh, low-contrast residual textures, over-sharpened grime,
uniform plastic gloss, pasted-on texture, milky reflections, clipped highlights, crushed blacks,
dirty AO halos, malformed anatomy when people are present, stray text or logo unless requested.
```

**B-18 `lira-image-prompts` 的 4-D 方法论 + 十条防失败规则（原文摘录）**
```
4-D: 拆解 (DECONSTRUCT) → 诊断 (DIAGNOSE) → 开发 (DEVELOP) → 交付 (DELIVER)
规则 2：一段 80-150 字的紧凑提示词，胜过一段 400 字结构松散的提示词
规则 3：正面 > 负面 —— 干净的皮肤 → "clean dry skin"，而不是"没有痘痘 (no acne)"
规则 4：宽高比与分辨率 = 平台参数（散文内不能出现 --ar / 16:9 / 4K）
规则 5：技术光照与材质 —— "单一的头顶主光，柔和的 2:1 光比，平滑的光线衰减" 胜过 "戏剧性的电影光照"
规则 6：调色板控制 —— "60% 暖赭石色，30% 深炭灰色，10% 铁锈红色的调色板"
规则 10：编辑操作 —— 最小的 更改 (CHANGE) + 详尽的 保留 (PRESERVE EXACTLY)
```

**B-8 `sd25-physics-prompt` 的约束语句正/反例（原文）**
```
Prefer: The steel hood folds into sharp load-aligned creases and remains permanently deformed;
it does not soften or stretch like rubber.
Avoid:  zero melting, zero morphing, zero distortion, absolute lock, perfect physics, 8K, masterpiece
```

**B-17 `image-impact-frame` 编译清单（原文，11 条硬检查，可直接转成判据）**
```
[ ] Does the prompt describe an instant, not a state or a layout?
[ ] Is there no empty field, and is it stated that nothing is laid in as a filled area?
[ ] Does every value carry one duty, with no two layers fighting over the same job?
[ ] Are the line layer and the fragment layer written separately…?
[ ] If the palette is monochrome-family, are the two values far apart in value and temperature?
[ ] Does the mark module appear in the first third of the prompt?
[ ] Does every mark clause say the gaps stay open…?
[ ] Is any sentence asking for the opposite of another sentence? Re-read line by line for this specifically.
[ ] Is any anatomy word present — face, eye, skin, teeth, vein, sweat? If yes, replace with a form description.
[ ] Is the vanishing point named, and is it unique?
[ ] Is --no short and concrete, with no multi-word negatives that can contradict each other?
```

**B-1 `director-seedance-prompt` 输出合同（原文模板）**
```text
### 第01段｜建议[普通场景窄区间；打戏或精确时码写准确T秒]｜[场景功能]
【角色/场景/素材锁定】…
【基础风格】…
【运镜与时间轴】… CUT 1：[cold-start opening + visible people/set + camera/spatial relation + explicit change + movement/focus + performance/action/dialogue + sound cue + cut reason/relay + visible OUT]
【声音设计】无背景音乐；[current audible layers]
【画面限制】无字幕、无水印、无乱码文字；人物身份稳定，面部、身体和手部结构自然完整。
```
对白记号法原文：`角色A：“（这个数值……不会错。）” = internal OS`；`角色A：【贴近】“…” = action before the line`；`*内容* = spoken emphasis`。

**B-2 `emotion-prompt` 三层映射（原文，摘录「开心」与「委屈」）**
```
架构：[主体情绪] + [面部细节] + [核心姿态] → 精确表情提示词
面部细节双层结构：肌肉动作→视觉结果（前半段精确指令，后半段画面落地）

### 1. 开心
面部细节：嘴部: 颧大肌收缩→嘴角向外上方牵引，上唇展平，可露上齿6-8颗；口轮匝肌松弛→双唇自然分开
眼部: 眼轮匝肌外侧纤维收缩→外眼角辐射状细纹，眼裂缩窄呈弯月状…
眉额: 额肌完全放松→额头平滑无纹；皱眉肌无收缩→眉间距正常
核心姿态：手部: 手指自然微张或轻搭身侧… 身体: 躯干挺拔不僵硬… 视线: 注视点直接锁定对象面部，眼动灵活…
### 2. 委屈
嘴部: 降口角肌轻度收缩→嘴角向下微坠；颏肌收缩→下巴皮肤起细密皱褶，下唇被推向上微噘…
眼部: 眼轮匝肌内侧紧张→下眼睑轻微上推，眼眶微微泛红；泪腺分泌增加→下睑缘出现泪膜反光
眉额: 皱眉肌+降眉间肌轻度收缩→眉头内侧上提内收，形成浅八字眉
```
关键规则原文：`真笑 = 颧大肌 + 眼轮匝肌外侧同时收缩（杜兴标记）`；`假笑/空笑 = 只有颧大肌，眼轮匝肌不参与`。

**B-31 `global/roger-deakins-cinematography` 提示词输出格式（原文）**
```
🎬 场景标题
📽️ 影片参照：[最接近的迪金斯作品 + 场景]
**Style（风格）：** [完整英文风格提示词 — 打光、色调、氛围]
**Scene（画面）：** [完整英文画面提示词 — 构图、主体、环境]
**完整提示词：** [Style + Scene 合并]
💡 打光笔记：… 🎨 色彩笔记：…
```

**B-39 `suno-music-prompts` 输出成品（原文块，音乐类提示词形态）**
```
📎 Style of Music:
City Pop, Dream Pop, Warm, Nostalgic, Silky Vocals, 80s Japanese
📎 Instrumentation:
Synth, Electric Guitar, Bass Guitar, Electric Piano, Drums
📎 Tempo: 92 BPM   📎 Key: A Major   📎 Weirdness: 30   📎 Style Influence: 85
📎 Audio Influence: 70（使用 Voices 时）  📎 Section Steering: ON
📎 Title: 海风的记忆
📎 Lyrics:
[Intro] / [Verse 1] / [Pre-Chorus] / [Chorus] / [Interlude] / [Verse 2] / [Bridge] / [Chorus] / [Outro]
```

**B-41 `mokeaigc-v9` = MOKE 原创「世界观构建导演 V017」**（站点主打 Skill；GitHub 版 `MOKEAIGC-work V017 .md` 为 39781 字节 / 16790 字符，API 版 SKILL.md 为 40254 字节，同一文档）
核心原文规则（逐条，全文见 `B-素材原文.md`）：
```
相机预设（默认，强制打头）：Arri 65mm camera, Cooke anamorphic lenses, analog film stock
默认负面附加项：no clean digital sharpness, no CGI look, no poster composition, no centered portrait, no black bars
必须写出具体镜头焦距（如 shot on a 24mm lens / 85mm lens），不要用"广角/长焦"这类笼统词
人类皮肤细节：real human detailed natural looking skin and textures, visible pores, freckles, fine lines, small blemishes,
subtle acne and pimple marks, scars, pore level detail, skin grain, real skin tones, peach fuzz facial hair softly
catching the light, and realistic highlights on the skin,
中英双语两个版本，功能性固定串（相机打头句、皮肤细节句、负面项、MJ 参数）一律保留英文原文不翻译
避免"史诗""美丽""酷"这类空泛词，除非有具体视觉细节支撑；避免"以某在世创作者或工作室的风格"
九张概览的九个叙事方面：居民/动物/建筑/地景/日常/迁徙或运动/声音或文化/权力或张力/肖像
区分规则：例行→日常；移动→迁徙；声音/记忆/表演→声音或文化；压力/危机→权力或张力；私密反应→肖像
```
九方面输出模板原文（英文提示词行）：
```
English Prompt:
A cinematic photograph, Arri 65mm camera, Cooke anamorphic lenses, analog film stock, [完整英文视觉提示词] [默认负面附加项]
中文提示词:
A cinematic photograph, Arri 65mm camera, Cooke anamorphic lenses, analog film stock, [完整中文视觉描述（功能性固定串保留英文）] [默认负面附加项]
```
另有 §4.6 焦段速查表（18–24mm 史诗地景 / 28–35mm 环境叙事 / 40–50mm 通用 / 65–85mm 肖像 / 100–135mm 压缩 / 135mm+ 望远）与 §4.7「科幻浪漫极简」风格锚点短语原文：`vast negative space, single subject off-center, minimal composition, quiet and breathable, soft romantic light with anamorphic streak flares, low-saturation cold palette with a single warm accent, subtle sci-fi geometry in the defocused background, matte sci-fi materials and faint glowing seams, clean geometric negative space`。

### 1.C 站点公开页面文案（含一条 agent 指令提示词原文）

1. **首页 `https://www.mokeaigc.com/`** 明示：「提示词库等受保护内容需要登录；MCP 需要单独授权。」并给出三条使用路径（图像/视频模板、编剧模板、MCP 连接）。
2. **`/mcp.html` 公开的提示词库用法示意**（提示词库页虽需登录，但其模板形态在 HTML 里公开，原文）：
```
为我想讲的故事，找一个合适的模板。
图像 / 视频 / 编剧 / 游戏 / 音乐 · 作品形式
叙事短片 —— 主角 → 目标 → 反制 → 有代价的选择
【故事构思】 【时长】 【锁定事实】
检索 → 读取 → 展开创作
```
3. **`/mcp.html` 的「复制说明，发给 Codex」提示词**（一条真实的、面向 agent 的操作指令提示词，带防幻觉护栏，原文）：
```
请根据下方配置，帮我连接 MOKEAIGC MCP。先检查已有的 Codex 配置，保留其他设置，修改前让我确认；
合并 moke 配置，不要重复添加。然后运行 codex mcp login moke --scopes openid,offline_access,skill:read,prompt:read，
让我自己登录并点击 Authorize。如果你无法修改本地配置或运行命令，请告诉我手动操作步骤，不要声称已完成。
授权后，搜索一个 Skill 和一条提示词并读取内容，确认是否真的能访问。不要安装或执行 Skill，
不要输出凭据，也不要更改服务端登录设置。
```
4. **`/skill.html`（SkillHub 页）原文要点**：`MOKE SkillHub｜可安装 · 可订阅 · 经过审核`；`发现可直接交付智能体使用的 Skill，查看版本、安全状态与真实使用数据。`；精选：`MOKE ORIGINAL SKILL / V17「从一个灵感，生长出一个世界。」世界设定、生命与文明、电影感视觉。`；下载文件 `worldbuilding-moke-v17.md`（Markdown 39 KB）。
5. **Skill 安装指令模板（每个 Skill 详情 API 都返回，原文，防越权护栏值得借鉴）**：
```
请帮我把 MOKE SkillHub 中的 Skill「{ns}/{slug}」安装到当前用户的 Codex。
请执行下面的官方安装命令：npx @astron-team/skillhub@latest install {slug} --registry https://www.mokeaigc.com --scope user --agent codex
安装完成后请确认 ~/.codex/skills/{slug}/SKILL.md 已存在，并告诉我安装结果和使用方法「$slug」。
安装阶段只下载和校验文件，不要执行 Skill 包内的脚本，也不要改动其他目录。
```
6. **`/today.html`（技术与资讯，公开）** 里的方法论断言（原文，可作为"写法共识"引证）：
```
把提示词沉淀为 Skill，而不是停留在聊天记录 —— 好的 Skill 应该包含触发场景、输入格式、操作步骤、验收标准和失败恢复方式。
图像生成的审美门槛正在回到摄影和电影语言 —— 光线、焦段、景别、调色和材质描述，比单纯堆叠"高质量"更能决定结果。
视频工具的关键变量：镜头语言和可复现性 —— 一次惊艳输出不等于可生产…能否按镜号、参考图和角色设定稳定复现。
```

### 1.D GitHub `MOKEAIGC/MOKE-Vision-One`（成品提示词与词库）

仓库：`https://github.com/MOKEAIGC/MOKE-Vision-One`（React+Vite+Tauri 桌面生图/生视频应用，master）

**D-1 `components/seedance/templates.ts`（13.2 KB）——11 条完整成品视频提示词（A–K），原文全录在 `B-素材原文.md`。** 形态清单：

| ID | 名称 | 模式 | 结构特征 |
|---|---|---|---|
| A | 电影冒险（10 秒，全素材参考） | 全素材参考 | `9:16 vertical, 10s` + 三段时码 + `Audio:` 行 + `Visual control:` 行 + 独立 negative |
| B | 延展已有视频 | 全素材参考 | `Extend @video1 by 5s.` + 连续性锁定 + `0-2s (new segment)` |
| C | 角色替换 | 全素材参考 | `Replace the main performer in @video1 with… Preserve original choreography…` |
| D | IP 安全原创生物对战 | 纯文本 | `vertical 9:16, 10s, 24fps` + Creature A/B 分角色行 + 三段节拍 + 强 negative（`no existing franchise characters…`） |
| E | IP 安全科幻英雄 | 纯文本 | 角色昵称行（Alloy Sentinel / Orbit Mentor）+ 三段节拍 + `no Marvel, no Iron Man…` |
| F | 玩偶舞蹈动画 | 全素材参考 | negative 最长（含 `no deformed hands, no flicker, no blur, no face distortion`） |
| G | MV 节拍同步蒙太奇 | 全素材参考 | 以 `@audio1 beat accents` 为时间基准 |
| H | 产品展示 / 电商广告 | 全素材参考 | 360° 旋转 + 3D 爆炸图 + `Material rendering:` 行 |
| I | 含对白的短剧（15 秒） | 全素材参考 | `Dialogue (Character A, cold and firm): "…"` + `Sound:` 逐段行 |
| J | 一镜到底 + 多图航点 | 全素材参考 | 四个 `@image` 各自绑定用途 + `Single continuous camera movement throughout, no cuts, no montage` |
| K | 多段拼接长视频（30 秒） | 多段拼接 | `## 第 1 段 / 交接帧 / ## 第 2 段` + 延展指令 |

A 与 H 原文（完整，未删节）：
```
A: 9:16 vertical, 10s fantasy adventure cinematic, cel-shading blended with watercolor, cool blue-green palette with warm highlights.
0-3s: hero wakes in a dim ancient chamber; faint glowing runes pulse on wet stone walls; slow dolly out.
3-7s: hero walks to giant rune door and touches circular mechanism; energy ripples activate runes in sequence; heavy door opens into bright light; follow shot.
7-10s: reveal vast world from cliff edge with floating islands and distant glowing ruins; crane up + pullback for scale.
Audio: water-drop echoes and low temple resonance at start; layered activation tones at rune trigger; deep rumble on door opening; orchestral swell on world reveal; wind ambience to end.
Visual control: coherent lighting, physically plausible movement, stable identity.
negative: no watermark, no logo, no subtitles, no on-screen text.

H: 16:9 widescreen, 10s, 3D product showcase, studio lighting with soft gradient backdrop, cinematic product commercial tone
0-3s: product rotates 360° at medium speed, clean reflections on surface, hero key light from upper-left
3-7s: product pauses, then splits into 3 sections (top/middle/bottom) in a 3D exploded view, each part floats apart with subtle particle trails, smooth transition
7-10s: parts rapidly reassemble with satisfying snap motion, final hero shot with brand-neutral backdrop glow, slight camera push-in for impact
Material rendering: accurate surface finish, glass reflections, metallic sheen where applicable
negative: no watermark, no logo overlay, no text overlay, no price tags, no competitor branding, no distorted proportions
```

**D-2 `components/seedance/cheatSheet.ts`（7.2 KB）——镜头/画质控制词库，10 类 80 条（实测计数），中英对照 + 一句裁判说明。** 分类：景别(11)/镜头运动(13)/机位角度(6)/焦点景深(5)/转场(7)/节奏(6)/灯光(10)/色彩方案(7)/艺术风格(10)/胶片纹理(5)。样例原文：
```
{ zh: '推近', en: 'push-in', desc: '镜头向主体推近（制造紧张/聚焦）' }
{ zh: '体积光', en: 'volumetric light', desc: '可见的光线穿过大气（丁达尔效应/上帝之光）' }
{ zh: '互补对比', en: 'complementary split', desc: '两种对比色（如青橙对比）' }
{ zh: '35mm 胶片颗粒', en: '35mm film grain', desc: '有机纹理，经典电影感' }
```

**D-3 `data/filmPresetTemplates.ts`（11.8 KB）——29 条胶片风格提示词片段（`recommendedSnippet`），可直接作为"画质控制词"最小单元。** 样例原文：
```
Kodak Portra 400: 'shot on Kodak Portra 400, soft pastel tones, creamy skin tones, natural warm colors, fine film grain'
Fuji Velvia 50:   'shot on Fuji Velvia 50, ultra-saturated colors, deep rich greens and reds, high contrast, extremely fine grain, landscape film'
CineStill 800T 系: 'CineStill 800T 钨丝灯红光晕 + 雾化'（中文说明）
```

**D-4 `services/atmosphereRecommender.ts`（12.2 KB）——把胶片映射到 `{atmospheric, aerial, humidity}` 三维 0–100 参数的规则引擎**，含 56 条关键词规则，每条带 reason（如 `CineStill 800T 钨丝灯红光晕 + 雾化 → {70, 55, 85}`、`Ektar 100 超细颗粒 + 高饱和远景清晰 → {25, 75, 20}`）。这是"抽象氛围词 → 可量化参数"的少见实现，适合当评测器的"术语可量化性"参考。

**D-5 `components/seedance/SeedancePromptWindow.tsx`（54 KB）——内嵌 3 条元提示词（原文）**：
```
(1) 剧本 → 资产提取（结构化输出 JSON schema：name / description）
请从以下剧本中提取出主要的角色和场景资产，用于AI视频生成的素材映射。
返回纯 JSON 数组，每个对象包含 name（如 @image1, @scene1）和 description（描述外观特征）。
注意：只返回 JSON，不要包含 markdown 代码块标记。

(2) 剧本 → 分镜提示词（英文正式 + 中文翻译）
你是一个专业的 AI 视频提示词工程师，精通 Seedance 2.0 格式。
请根据以下剧本和参数，分析剧本长度。如果剧本较长的，请拆分为多个连贯的 ${duration}秒 视频段落。
为每段生成英文正式提示词（包含时间轴节拍），以及对应的中文翻译版本。
【剧本内容】/【素材映射】/【生成参数】…
请返回纯 JSON 格式（不要 markdown 代码块），包含 "segments" 数组，每项含 "english" 和 "chinese"。

(3) 角色描述 → 概念图/三视图
你是一位世界顶尖的影视概念设计师和AI绘画提示词专家。根据用户提供的角色描述，生成用于AI绘画的英文Prompt。
请严格以JSON格式输出：
{"character_name":"角色名","visual_analysis":"中文外貌分析","common_tags":"核心特征英文关键词",
 "concept_art_prompt":"氛围概念图Prompt(16:9, cinematic)",
 "character_sheet_prompt":"三视图Prompt(front view, side view, back view, white background, --ar 16:9)"}
```

### 1.E GitHub `MOKEAIGC/MOKEAIGC-work-V017`

- `https://github.com/MOKEAIGC/MOKEAIGC-work-V017`，文件：`MOKEAIGC-work V017 .md`（16790 字）、`MOKEAIGC-work V09 .md`（12984 字）、`README.md`、4 张流程图/作品集图。
- 与站点 CDN 的 `assets/downloads/worldbuilding-moke-v17.md`（39781 字节）内容一致（同一份 V017 正文）；与 Skill API `honghouzi--video/mokeaigc-v9` 的 SKILL.md（40254 字节）为同一文档的不同修订。
- V09 与 V017 的差异（实测比对）：V09 无「规则适用范围与优先级」表、无「世界设定交付/关系图/差异表」、无「模式 B 生物设计」、九方面为硬性 9 张；V017 把张数改为可扩展、新增交付结构与三模式路由。→ **可直接当"同一提示词/方法论文档的版本演化"对照样本。**

### 1.F 其它（bonus）

- `MOKEAIGC/.github/profile/README.md`（组织主页文案）。
- `MOKEAIGC/AIHOT`（"自己找热点、自己写日报的网站框架"，与提示词写法无关，未采）。
- 站点 CDN 静态资源路径 `https://zcdn.rytesa.cn/moke-v3/<hash>/runtime/*.js`（如 `skills.js` 暴露了 catalog 接口 `/api/skills?publicPage=skills…`，是本路采集的突破口）。

---

## ② 优秀提示词的写作模式分析

### 2.1 三种成品形态（同一批作者并存，评测器必须都能判）

| 形态 | 特征 | 代表素材 | 适用/风险 |
|---|---|---|---|
| **① 拍摄简报式（自然语言散文）** | 完整句子、一主体一动作、时间用 seconds 叙述式；无参数后缀、无关键词堆砌 | Seedance 2.5 官方 Example（陶瓷杯）、seedance-examples-zh | 被官方指南与 antislop 规则共同推荐；最抗"标签沙拉" |
| **② 分节合同式（中文小节标题 + 混合语言）** | `角色/资产锁定 / 视觉材质总控 / 镜头语言总控 / 事件节拍 / 声音 / 正向稳定约束` | Liu 六段式（jimeng-sd2 / seedance-prompt / vfx 三处一致） | 长视频/多镜头可复现性最强；坏处是"合同"本身不含内容时会显得空 |
| **③ 参数块式（标签 + 参数键值）** | `Style of Music:` / `Tempo: 92 BPM` / `--ar 16:9` / `@image1` 角色行 | Suno 提示词、Vision-One templates 的 `@image1/negative` | 音乐与图像编辑平台仍需要；但当"画质词表"使用（8K, masterpiece）即触发 slop 规则 |

**共同结构骨架（跨形态一致率最高）**：
`主体/身份锁定 → 动作与可见结果 → 场景环境 → 镜头（一个主动作 + 终点）→ 光线/材质 → 声音 → 正向稳定约束（+ 极短负面块）`

### 2.2 结构模板清单

| 模板名 | 骨架 | 出处 |
|---|---|---|
| Director Formula（7 槽） | Subject + Action + Scene + Camera + Lighting/Style + Audio + Constraints | `seedance-prompt` |
| 核心公式（6 项，非全填） | Subject + Action/Event + Scene & Environment + Visual Style + Camera/Cut + Audio | `seedance-2-5-prompting`（官方） |
| 四句模板 | `<Subject> performs <action> in <scene>.` / `The visuals feature <style>.` / `Use <shot size/angle/move/cut>.` / `Audio includes <…>.` | 同上 |
| 锁定观感块 | `[LOOK — LOCKED, APPLIES TO EVERY SHOT]` + 3 行（机身/镜头/胶片/T值/景深/颗粒/高光/黑位/对比 + Grade 三段 + 运镜与表演基线），多镜头只写一次 | 同上 |
| 分阶段（Stage） | `[Generation Goal]` → `[Stage n] Initial state / Primary event / End state` → `[Maintain Consistency]`，每段 `Continue from the previous stage:` | 同上 |
| 时间预算 | `0-3s… 3-7s… 7-12s…`；区间必须连续不重叠；时间戳是"预算"不是"剪辑点" | 同上 |
| 中文紧凑版 | `[Image1]为参考，严格保持[主体/产品/脸部/标志]不变；仅加入[动作/光线/镜头变化]。镜头：[一个动作]。声音：[音效或环境声]。` | `seedance-vocab-zh` |
| 压缩优先级 | 参考标签角色 > 主体身份 > 动作+可见终点 > 单一运镜 > 物理光源 > 声音 > 安全/IP/连续性 > 序列状态 | `seedance-prompt-short` |
| 配方骨架 | Product I2V / Drama T2V / Reference Motion / First-Last Frame / Animation 五条填空句 | `seedance-recipes` |
| 特效卡 | `source/owner → formation → path/bulk motion → contact → receiver/light response → decay/residue` | `seedance-vfx` |
| IM2 七段顺序 | 主体→风格→机位与层级→光路与材质→距离与信息密度衰减→干净细节层→负面卫生层 | `im2-clean-image` |
| 音频/台词分隔符 | 音乐 `()` / 音效 `<>` / 台词 `{}` / 字幕 `【】`；非中文台词必须先声明语言 | `seedance-2-5-prompting` |
| 双版本固定串 | 中英双语各一版，功能性固定串（相机打头句/皮肤句/负面项/MJ 参数）永远保留英文不译 | V017 世界观构建 |
| 结构化输出元提示 | "返回纯 JSON…不要包含 markdown 代码块标记" + responseSchema | Vision-One 三条元提示 |

### 2.3 控制词密度：他们的"密度纪律"

- **字数区间**：`seedance-prompt-short` 明示"理想 30–100 英文单词"；`lira` 明示"80–150 字的紧凑提示词胜过 400 字松散提示词"。V017 走反向（长模板 + 每帧段落式），但用"每段自包含 + 固定串复用"控密度，而不是靠删信息。
- **压缩删除顺序（原文顺序，可直接当扣分优先级）**：重复风格形容词 → 泛化质量词 → 参考图里已可见的背景细节 → 次要运镜 → 次要动作 → 猜测性情绪标签。**保留**：保真约束、动作时点、参考角色映射。
- **一词一职**：`image-impact-frame` 的"Does every value carry one duty, with no two layers fighting over the same job?"；V017 的"摄影/灯光两字段是从整段提示词里摘录提炼，不是新增内容"。
- **命名必带可见后果**：`Cooke S4/i primes` 单独出现 = 装饰；`Cooke S4/i primes, warm skin rendering, creamy controlled bokeh, soft flare` = 指令（seedance-2-5 原文规则）。
- **每个参考素材必须同时写"用什么"和"不用什么"**（Rule 1），否则参考图里的背景/路人会漏进画面。

### 2.4 中英混用习惯（可归纳为 4 条）

1. **平台原语保留英文，描述内容走中文**：`@Image 1/@图片1`、`--ar`、`--sref`、`@image1`、`Arri 65mm camera, Cooke anamorphic lenses, analog film stock` 一律不译（V017 §6 明确"功能性固定串一律保留英文原文不翻译"）。
2. **术语双语并列，中文后缀解释**：cheatSheet 的 `{zh:'体积光', en:'volumetric light', desc:'可见的光线穿过大气（丁达尔效应/上帝之光）'}`——英文给模型，中文给作者，desc 给验收。
3. **中文压缩换密度**：`seedance-vocab-zh` 原文 `不可译标签保留 + 短制作短语替代抽象形容词`；示例 `缓慢推镜 / 横向跟拍 / 侧逆光 / 水珠沿表面下滑 / 脚步声卡点`（四字级密度）。
4. **混合语言只能用于澄清，不得用于隐蔽**：`Use language mixing only for clarity: reference roles, dialogue, language, technical camera terms, and safe production constraints. Do not use another language to hide unsafe intent.`（`seedance-prompt` 原文）
5. **中文 prompt 的专属空词表**：`电影感 / 氛围感 / 高级感 / 大片感 / 质感` → 必须分解为 材质、光线、色彩、空气（`seedance-vocab-zh` De-Slop Rule 原文）；对应英文空词表为 `cinematic / epic / beautiful / dynamic / professional`。

### 2.5 动作 / 场景 / 画质控制词怎么用

- **动作**：写"可见变化 + 时点 + 终点"，不写情绪词。`condensation beads form and slide down the glass over five seconds`；`performance written as a visible gesture rather than an emotion word`。情绪必须绑定可拍摄线索（眼动、眉张力、嘴形、呼吸、视线、手部）——`emotion-prompt` 把它做成了 20×3 的映射表，`seedance-2-5` 给出"两到四个线索足够，不要清点整张脸"的上限。
- **场景**：只写参考里没有的信息（`Scene: Only what is not already in references`）；环境当"一种力量"（V017 §4：通过远处人影、动物路径、废墟、田垄、炊烟、脚印、船只、旗帜、侵蚀或天气体现尺度）。
- **镜头**：一个镜头一个主运动 + 明确终点；多主体时必须写明相机跟随/环绕的是哪一个、起止位置；复合运动拆成节拍而不是叠形容词。节奏词 `slow/smooth/gradual/gentle` 控速度，裸 `fast` 会抖动（seedance-2-5 "carried over" 段）。
- **画质**：不写 `8K/masterpiece/trending on ArtStation`（那是平台参数或空词），而写物理来源：`warm practical key from frame left, cool blue rim`、`Arri 65mm + anamorphic + analog film stock`、`shot on Kodak Portra 400, soft pastel tones…`、`60% 暖赭石 / 30% 深炭灰 / 10% 铁锈红`。
- **焦距**：V017 强制"每条必须写出具体焦段"（`shot on a 24mm lens`），并配速查表 → 把"焦段"升格为可检查的字段（评测器可直接正则校验）。
- **负面词**：统一口径是"负面槽不是旧失败的记忆"：只放**宽泛可复用**的失败类（artifact / 结构错误 / 风格漂移 / 水印 / 假材质 / 构图杂乱），一条紧凑行优先；被否定的名词若本不该出现，写出来反而会召唤它（`prompt-contamination-guard` 的 Correction and exclusion leakage、`im2-clean-image` 的 Negative-Prompt Hygiene）。六段式合同里更彻底：负面槽被 `正向稳定约束` 取代。

### 2.6 反面清单（可直接转成扣分判据）

- **六类 slop**：空评价词、搬运图像模型 token（8K/masterpiece）、标签沙拉、否定 slop、形容词堆叠（同义三连）、感受后缀词（电影感/雰囲気/감성적/atmosférico）。
- **七类语义污染**：旧上下文残留、纠正/排除泄漏、默认模板污染、标签负载污染（`压迫感/史诗感/动态镜头` 等靠标签代替可见证据）、正向语义过权重（同义重复导致某元素过大）、内部控制泄漏（`上一个/之前那版/本段/继续保持`、工作流注释、参考 ID 无角色）、冲突语义锚（克制 × 爆发、锁定 × 自由运动）。
- **硬失败（preflight/self-check 类原文）**：主体与主动作缺失；多镜头无锁定观感块；参考素材无角色与排除；每段多于一个主变化或无结束状态；把生成参数写进正文；`no X` 长清单互相矛盾；无支撑的能力承诺（`frame-accurate` 承诺）；空占位符未填。

### 2.7 给 req-prompt-eval 的判据映射建议（AIGC 生图/生视频判据包）

| 判据 | 建议来源规则（可引用原文措辞） |
|---|---|
| 主体/身份锁定 | `Subject/Action first`、`角色/资产锁定`、I2V 只写 `preserve [Image1] exactly` |
| 可见性（反空词） | Visibility Test：`visible to a camera, measurable by a light meter, audible in the mix, or observable as motion` |
| 镜头可执行性 | 一个主动作 + 终点；写明跟随对象与起止；具体焦段必填 |
| 时间/结构 | 区间连续不重叠；每段一个主变化 + 结束状态；`Continue from the previous stage:` |
| 参考素材职责 | 每个素材一行：用**什么** + 排除**什么**；多视图同一物体必须显式声明 |
| 声音层 | 与环境声/音效/台词/字幕分隔符；非中文台词声明语言；`无配乐` 也是合法值 |
| 保真/稳定性 | `logo, shape, label, and cap geometry remain unchanged` 类正向锁定 |
| 负面词卫生 | 宽泛可复用、单行、无旧失败专名、不与正向冲突 |
| 密度 | 30–100 词（短）/ 80–150 字（图）/ 超出则按压缩优先级删 |
| 中英混用合规 | 功能串留英文、描述走中文、混合仅为澄清 |
| 越权/幻觉 | 不得承诺模型做不到的（帧级精确、像素级一致）；不得把生产管理语句写进提示词 |
| 合规/IP | 真实人名→特征化描述；IP 名→原创替换（`MOKEAIGC/global/seedance` 的合规替换原则：保留颜色主调/装备风格/战斗能力，去掉版权元素） |

---

## ③ 可当测试用例的素材列表（12 条，形态各异）

| # | 用例 | 形态 | 为什么适合当测试用例 | 期望评测信号 |
|---|---|---|---|---|
| T1 | Vision-One `templates.ts` **A 电影冒险** | 三段时码 + Audio 行 + 独立 negative | 形态完整、可复现、有 `Visual control:` 稳定行；是"优秀基准" | 高分；不可扣"无镜头/无声音" |
| T2 | Vision-One `templates.ts` **H 产品展示** | 商品爆炸图 + 材质行 | 非叙事型（产品向）提示词，检验判据是否只对叙事友好 | 高分；材质/光路字段齐全 |
| T3 | Vision-One `templates.ts` **I 含对白短剧** | `Dialogue (Character A, cold and firm): "…"` + 逐段 `Sound:` | 含台词与情绪，检验"表演可拍摄化"判据 | 高分；情绪有可拍摄线索 |
| T4 | Seedance 2.5 官方 **陶瓷杯 Example** | 自然语言散文、无时码、无参数 | 官方推荐形态，作为"散文式满分基线"；同时检验评测器是否误扣"没有时间分段" | 高分；**不应**要求时码 |
| T5 | `seedance-2-5-prompting` 的 **锁定观感块 + Stage 模板**（未填的空模板） | 纯模板（占位符未填） | 检验"模板 vs 成品"判别：结构完美但无具体信息 → 应判为**未完成/低分** | 中低分；报"占位符未填" |
| T6 | V017 世界观构建 **九方面输出模板** | 中文双语结构 + 固定串 | 中文长结构样本，检验"中英混用是否合规（固定串留英文）"与"信息量是否被稀释" | 结构分高；混用分高 |
| T7 | `seedance-antislop` 的 **空词表本身的示例句**：`dramatic cinematic noir vibes` | 差样本（负例） | 天然负例，用于校准"空词密度"扣分曲线 | 低分；命中空评价词/感受后缀词 |
| T8 | `lira` 的反例句：`no acne` / `no people` | 否定 slop（负例） | 检验"负面词卫生"判据与"正面 > 负面"规则 | 扣分；提示改写为正表述 |
| T9 | `seedance-examples-zh` **Character drama**（中文紧凑句） | 中文 60–80 字紧凑成品 | 检验压缩密度与中文词表判据；与 T1 形成"长/短"对照 | 高分；密度在区间内 |
| T10 | Vision-One `filmPresetTemplates` 的 `Kodak Portra 400` 片段 | 单句风格串（29 条之一） | 边界样本：**只有画质词、没有主体/动作** | 低-中分；应报"缺主体/动作/镜头"但不报"空词" |
| T11 | `suno-music-prompts` 的 **Style of Music 块 + [Verse]/[Chorus] 结构** | 键值标签式 | 非视觉媒介（音乐），检验判据包的"跨模态适配"与结构标记识别 | 中-高分；不应套视觉判据 |
| T12 | `im2-clean-image` 的 **Avoid 长负面块**（原文 20+ 项） | 负面词堆叠 | 检验"负面清单是否过长/是否含旧失败专名"的边界 | 扣分（单行过长、宽泛混杂），示范"窄块"改写 |

（备选：`prompt-library-提示词库管理` 的 6 要素/5 维度框架 → 可作为**评测器自身的 rubric 对照**，而不是被测样本；`director-seedance-prompt` 的五段合同模板 → 作为"重结构"极端样本；`image-impact-frame` 的 11 条编译清单 → 转为自动化检查项。）

---

## ④ 抓取失败清单（如实记录）

| 目标 | 现象 | 判定 |
|---|---|---|
| `https://www.mokeaigc.com/cinematique.html`（**提示词库**，站点主导航） | `302 → /auth/login?returnTo=%2Fcinematique.html`；跟随重定向后落回 `https://www.mokeaigc.ai/` 首页 HTML（44448 B） | **需登录，未采集**（不建账号）。提示词库正文（生图/生视频模板）**未取得**，仅取得 `mcp.html` 上公开的用法示意与结构线索 |
| `.../cinematique.html?section=image|video|text|music|animation|game|story|voice|sound|digital-human` | 同上，全部 302 | 未采集 |
| `https://www.mokeaigc.com/film-stills/`（电影剧照） | 302 → 登录；跳转后为 `.ai` 首页 | 未采集（无附带提示词可验证） |
| `https://www.mokeaigc.com/videos.html`（视频教程） | 302 → 登录 | 未采集 |
| `https://www.mokeaigc.com/tutorial.html`（流程规范/教程） | 302 → 登录 | **未采集**——这是"教人怎么写提示词"最可能的位置，属本次最大缺口 |
| `/api/prompts`、`/api/prompts?publicPage=prompts`、`/api/library/prompts`、`/api/cinematique`、`/api/cinematique/prompts`、`/api/prompt-library`、`/api/prompts/list`、`/api/prompts/search?q=…`、`/api/film-stills`、`/api/stills` | 一律 `200 + text/html 29027 B`（SPA 回退页），非 JSON | 无此公开端点；该路由族命名未能猜中 |
| `/api/content?publicPage=prompts`、`/api/library`、`/api/prompt` | 同上 SPA 回退 | 不存在 |
| `/sitemap.xml`、`/robots.txt` | 返回 SPA 首页 HTML（非 sitemap/robots） | 无法用 sitemap 枚举受保护路由 |
| `https://www.mokeaigc.com/mcp`（MCP 服务端点） | 存在但需 OAuth 授权（`/api/session` 返回 `{"authenticated":false,"publicPages":["visual","about","all-ai","skills"]}`） | 未授权，**未采集**（不登录） |
| `skill.html` 上的「发现 Skills 0」 | 静态 HTML 中为 0，属 JS 异步占位；真正数据在 `/api/skills`（已改走 API） | 已绕过 |
| `www.mokeaigc.ai` 同路径 | 与 `.com` 同源行为（`/api/skills` 亦返回 183 条），但 `/cinematique.html`、`/film-stills/` 同样落回首页 | 无额外收获 |
| 工具限制 | `web_extract` 对本域名误判为内网地址而拒绝；浏览器内核本机损坏 → 全程改用 `terminal` + curl / Python urllib | 已记录，不影响结果 |

**未采集但可后续补的**：提示词库正文（需账号或 MCP 授权）；`tutorial.html` 流程规范；`film-stills` 剧照与其提示词；`MOKEAIGC/AIHOT` 仓库（与本主题无关）。

---

## ⑤ 附录：本地文件索引

- 站点页面：`C:/Users/A/.moke-scratch/{home,skill,today,mcp,videos,tutorial,filmstills,cine-image}.html`
- Skill 目录：`C:/Users/A/.moke-scratch/api/catalog.json`（183 条）
- Skill 正文（42 份）：`C:/Users/A/.moke-scratch/api/bodies/*.md` + `_index.json`（含每个 Skill 的 files 清单、版本、下载量）
- GitHub 原始文件：`C:/Users/A/.moke-scratch/gh/MOKE-Vision-One__*.ts|tsx|md`、`MOKEAIGC-work-V017__*.md`
- 组织/仓库元数据：`gh_org.json`、`tree_vision.json`、`tree_v017.json`
- 汇编原文：`D:/req-prompt-eval/research/B-素材原文.md`
