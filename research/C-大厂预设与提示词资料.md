# C 路调研：大厂 AIGC 预设与提示词资料

> **调研范围**：国内外主流 AIGC 图/视频厂商官方文档中的「提示词指南 + 预设词表 + 参数/负面通道」
> **素材来源**：`C:\Users\A\AppData\Local\Temp\aigc\pages\`（Playwright 抓取的 innerText 纯文本，主素材）、`C:\Users\A\AppData\Local\Temp\aigc\`（原始 html / .ipynb / 代理 403 页）
> **落盘时间**：2026-10-14
> **核对纪律**：本报告每一条均标注可回溯的素材文件。素材中确无的，一律写「素材中未见」，不做补写。
> **本轮唯一补充抓取**：阿里百炼《文生图Prompt指南》（`pages/aliyun_text-to-image-prompt.txt`，本轮新增，其余全部来自上轮既有素材）。
> **对上轮汇报的一处修正**：上轮称 Veo 指南为「六要素」，原文实际列出 **7** 个小标题（Shot framing and motion / Style / Lighting / Character descriptions / Location / Action / Dialogue），见第②节。

---

## ① 厂商 × 资料类型矩阵

> 每格 = 来源 URL + 素材文件 + 关键摘录。共 **28** 条。

### 火山方舟（字节跳动 / Doubao · Seedance · Seedream）

| # | 资料类型 | 文档 | 来源 URL | 素材文件 | 关键摘录（原词） |
|---|---|---|---|---|---|
| 1 | 视频提示词指南 | Doubao Seedance 2.0 系列提示词指南 | https://www.volcengine.com/docs/82379/2222480 | `pages/www.volcengine.com_docs_82379_2222480.txt` | 进阶公式：`精准主体 + 动作细节 + 场景环境 + 光影色调 + 镜头运镜 + 视觉风格 + 画质 + 约束条件`；「好的提示词不是单纯的"文案型形容"，而是"工程型指令"」；模型拆「空间层/时间层」 |
| 2 | 视频提示词指南 | Doubao Seedance 2.5 提示词指南 | https://docs.volcengine.com/docs/ark/seedance-2-5-prompt-guide?lang=zh | `pages/docs.volcengine.com_docs_ark_seedance-2-5-prompt-guide_lang_zh.txt` | 「把 Seedance 2.5 当作一个视觉内容生产者，用导演的思维书写 [ 结构化 Prompt ]」；含「负向控制」独立小节 |
| 3 | 视频教程 | Doubao Seedance 2.5 教程 | https://docs.volcengine.com/docs/ark/seedance-2-5?lang=zh | `pages/docs.volcengine.com_docs_ark_seedance-2-5_lang_zh.txt` | 大量成品 prompt 案例（如海边说唱 MV：镜头 1 [0:00–0:03] … 逐镜时间码 + 「无字幕、无文字叠加」） |
| 4 | 视频教程 | Doubao Seedance 2.0 系列教程 | https://docs.volcengine.com/docs/ark/seedance-2-0?lang=zh | `pages/docs.volcengine.com_docs_ark_seedance-2-0_lang_zh.txt` | 越野摩托竞技短片案例，用「1）中景跟拍…2）超近低机位…」分号编号镜头逻辑 |
| 5 | 视频教程 | 视频生成教程 | https://docs.volcengine.com/docs/ark/video-generation-tutorial?lang=zh | `pages/docs.volcengine.com_docs_ark_video-generation-tutorial_lang_zh.txt` | 「图生视频时请尽量上传高清高质量的图片」 |
| 6 | 视频提示词指南 | Seedance 1.0 系列提示词指南 | https://www.volcengine.com/docs/82379/1631633 | `pages/www.volcengine.com_docs_82379_1631633.txt` | 提示词参数：`resolution / ratio / duration / seed / camera_fixed / watermark`；旧方式内联 `--rs 720p --rt 16:9 --dur 5 --seed 11 --cf false --wm true`；「景别和视角控制」 |
| 7 | 文本提示词指南 | 提示词工程 | https://docs.volcengine.com/docs/ark/prompt-engineering?lang=zh | `pages/docs.volcengine.com_docs_ark_prompt-engineering_lang_zh.txt` | LLM 侧「结构化与可评估」；页内索引指向图片/视频提示词指南 |
| 8 | 图像生成 + 提示词建议 | Doubao Seedream 4.0-5.0 图片生成 | https://docs.volcengine.com/docs/ark/seedream-4-0-5-0?lang=zh | `pages/docs.volcengine.com_docs_ark_seedream-4-0-5-0_lang_zh.txt` | 「建议用简洁连贯的自然语言写明 **主体 + 行为 + 环境**，若对画面美学有要求，可用自然语言或短语补充 **风格、色彩、光影、构图**」；「（prompt）建议**不超过300个汉字或600个英文单词**」 |
| 9 | 图像生成 | Doubao Seedream 5.0 pro | https://docs.volcengine.com/docs/ark/seedream-5-0-pro?lang=zh | `pages/docs.volcengine.com_docs_ark_seedream-5-0-pro_lang_zh.txt` | 宽高像素区间示例 `2048x1024=2097152`，区间 `[921600, 4624220]`；`optimize_prompt_options.mode`（standard / fast） |
| 10 | 图像编辑指南 | Seedream 5.0 pro 交互编辑指南 | https://docs.volcengine.com/docs/ark/seedream-5-0-pro-editing-guide?lang=zh | `pages/docs.volcengine.com_docs_ark_seedream-5-0-pro-editing-guide_lang_zh.txt` | 坐标标注语法：`把图 1 <bbox>120 180 640 760</bbox> 区域内的左侧人物换成机器人`；归一化坐标范围 `0~999`，左上角 `0,0`，右下角 `999,999`；另支持 `<point>` |
| 11 | （失效）图像提示词指南 | Seedream 提示词指南 | https://docs.volcengine.com/docs/ark/seedream-prompt-guide?lang=zh | `pages/docs.volcengine.com_docs_ark_seedream-prompt-guide_lang_zh.txt` | **无独立指南**：该 URL 实际重定向到通用落点（内容为模型列表 + Python/Ark SDK 示例），正文无提示词方法论。素材中未见即梦/Seedream 独立提示词指南 |
| 12 | （非提示词）模型列表 | 模型列表 | https://www.volcengine.com/docs/82379/1330310 | `pages/www.volcengine.com_docs_82379_1330310.txt` | 模型卡片：Doubao Seedance 2.5「30 秒超长叙事，全模态参考扩容」、Seedream 5.0 pro「编辑更可控、生产更落地」 |
| 13 | （重定向落点） | — | https://www.volcengine.com/docs/82379/1542787 | `pages/www.volcengine.com_docs_82379_1542787.txt` | 与 #11 字节数完全一致（5548B），确认为同一落点页 |

### 阿里百炼（阿里云 · 万相 Wan）

| # | 资料类型 | 文档 | 来源 URL | 素材文件 | 关键摘录（原词） |
|---|---|---|---|---|---|
| 14 | 图像提示词指南 | 文生图Prompt指南 | https://help.aliyun.com/zh/model-studio/text-to-image-prompt | `pages/aliyun_text-to-image-prompt.txt`（本轮补抓） | 双参数：「`prompt`：正向提示词」「`negative_prompt`：反向提示词，描述不希望在图像中看到的内容」；基础公式 `主体 + 场景 + 风格`；进阶公式 `主体（主体描述）+ 场景（场景描述）+ 风格（定义风格）+ 镜头语言 + 氛围词 + 细节修饰`；「提示词词典：通过图像的**五大要素**表现图片内容，包含**景别、视角、镜头拍摄类型、风格和光线**」；`prompt_extend` 智能改写 |
| 15 | 视频提示词指南 | 视频生成Prompt指南 | https://help.aliyun.com/zh/model-studio/text-to-video-prompt | `aliyun_video.html` + `txt/aliyun_video.txt` | 基础 `主体 + 场景 + 运动`；进阶 `主体（主体描述）+ 场景（场景描述）+ 运动（运动描述）+ 美学控制 + 风格化`；图生视频 `运动 + 运镜`；声音公式、多镜头公式、参考生视频公式（详见第②③节） |

### 腾讯混元（腾讯云）

| # | 资料类型 | 文档 | 来源 URL | 素材文件 | 关键摘录（原词） |
|---|---|---|---|---|---|
| 16 | 图像提示词指南 | 混元生图 Prompt 指南 | https://cloud.tencent.com/document/product/1729/106530 | `tencent_hunyuan_img.html` → `txt/tencent_hunyuan_img.txt` | 三套模板公式（人物/风景/物品）+ 完整预置风格词表；`Revise` prompt 扩写开关；预置风格「将风格编号传入接口入参中的 Style，无需手动在 Prompt 中添加风格描述」 |
| 17 | 图像 API 文档 | 提交混元生图任务 | 素材未记录页面 URL（正文域名 `hunyuan.tencentcloudapi.com`，Action `SubmitHunyuanImageJob`） | `tencent_hunyuan_task.html`（gzip 压缩，本轮解压后得 `txt/tencent_hunyuan_task.txt`） | 参数：`Prompt`（≤1024 utf-8 字符）、`NegativePrompt`（示例值「黑色，雨」）、`Style`（风格编号，示例 `riman`）、`Resolution`、`Num`、`Clarity`、`Seed`、`LogoAdd`（默认 1，右下角「图片由 AI 生成」）、`Revise` |

### 可灵（快手 Kling）

| # | 资料类型 | 文档 | 来源 URL | 素材文件 | 关键摘录（原词） |
|---|---|---|---|---|---|
| 18 | 视频 API 文档 | 视频 3.0 Omni 图生视频 | https://klingai.com/document-api/api/video/3-0-omni/image-to-video | `pages/klingai.com_document-api_api_video_3-0-omni_image-to-video.txt` | 多镜头模板：`可通过固定格式生成多镜头视频，格式为"镜头 n, m, words; 镜头 n, m, words;"`；`n` 最多 6 分镜最少 1；`m` 各分镜时长之和 = 视频总时长；`words` 最大 512；`通过@xxx的格式来指定某个主体，如：@Zhang`；正文 ≤3072 字符、建议 ≤2500 |
| 19 | 视频 API 文档 | 视频 3.0 Turbo 图生视频 | https://klingai.com/document-api/api/video/3-0-turbo/image-to-video | `pages/klingai.com_document-api_api_video_3-0-turbo_image-to-video.txt` | 同上多镜头模板（同一段原文） |
| 20 | 视频 API 文档 | 动作控制（Motion Control） | https://klingai.com/document-api/api/video/motion-control | `pages/klingai.com_document-api_api_video_motion-control.txt` | 对参考视频的硬约束：「动作视频一镜到底，角色始终出现在画面中，避免切镜、运镜等。否则会被截取。」「建议上传1人动作视频，2人及以上会取画面占比最大的人物动作进行生成。」「动作避免过快，相对平稳的动作生成效果更佳。」「图片中人物比例尽量与参考视频中人物比例一致」 |
| 21 | 图片 API 文档 | 图片 3.0 Omni 生成 | https://klingai.com/document-api/api/image/3-0-omni/image-generation | `pages/klingai.com_document-api_api_image_3-0-omni_image-generation.txt` | 双参数：「`prompt` 正向文本提示词 不能超过 2500 个字符」「`negative_prompt` 负向文本提示词 不能超过 2500 个字符」；注：「图生图（即 image 字段不为空时）场景下，**不支持负向提示词**」 |
| 22 | 能力地图 | 视频能力地图 | https://klingai.com/document-api/guides/capability-map/video | `pages/klingai.com_document-api_guides_capability-map_video.txt` | 模型矩阵 Kling 3.0 Turbo / 3.0 / 3.0 Omni / O1 / 2.6 / 2.5 Turbo；能力项：单镜头、多镜头、音画同出、声音控制（人声）、动作控制、视频参考 |
| 23 | 能力地图 | 图片能力地图 | https://klingai.com/document-api/guides/capability-map/image | `pages/klingai.com_document-api_guides_capability-map_image.txt` | Kling Image 3.0 Omni「强化叙事感、直出2K/4K超高清图、系列组图生成」；能力项：组图生成、多图参考图、角色特征参考、人脸特征参考、风格训练、主体控制 |
| 24 | 入门概览 | 开始接入可灵 | https://klingai.com/document-api/guides/get-started/overview | `pages/klingai.com_document-api_guides_get-started_overview.txt` | 「Kling 3.0 & 3.0 Omni 支持音画同出，智能分镜，主体参考」 |

### Midjourney

| # | 资料类型 | 文档 | 来源 URL | 素材文件 | 关键摘录（原词） |
|---|---|---|---|---|---|
| 25 | 参数表 | Parameter List | https://docs.midjourney.com/docs/parameter-list | `pages/docs.midjourney.com_docs_parameter-list.txt` | 参数位置三规则：「Place Parameters at the End」「Watch the Spaces: Add a space between your prompt text and the dashes」「No Punctuation: Don't use commas, periods, or other punctuation marks in your parameters」；`--aspect/--ar`、`--no`、`--quality/--q`、`--stylize/--s`、`--sref`、`--sw`、`--raw`、`--chaos/--c`、`--weird/--w`、`--seed`、`--repeat/--r`、`--tile`、`--profile/--p`、`--iw`、`--draft`、`--hd/--sd`、`--edit`、`--video`、`--motion low/high`、`--loop`、`--end`、`--bs`、`--sv` |
| 26 | 风格参考 | Style Reference | https://docs.midjourney.com/docs/style-reference | `pages/docs.midjourney.com_docs_style-reference.txt` | Best Practices：「Focus on content, not instructions」；Bad：「the look of this image but a dog」「copy this style and make a bunny」；Good：「detailed portrait of a dog」「ballpoint pen sketch of a bunny」；`--sw` 取值 0–1000，默认 `--sw 100`；`--sref random`；Style Code 风格库 |

### OpenAI / Google DeepMind

| # | 资料类型 | 文档 | 来源 URL | 素材文件 | 关键摘录（原词） |
|---|---|---|---|---|---|
| 27 | 视频提示词指南 | Sora 2: Prompting Guide（Cookbook） | https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide | `openai_sora2.ipynb`（原始 notebook）+ `pages/openai_sora2_cookbook.md`（转出正文） | 「Treat your prompt as a creative wish list, not a contract」；「detailed prompts give you control and consistency, while lighter prompts open space for creative outcomes」；API 参数与散文分离：「You cannot request them in prose, they must be set explicitly in your API call」；`: [Prose] / Cinematography: / Actions: / Dialogue:` 四段式模板；Weak vs Strong 对照表 |
| 28 | 视频提示词指南 | How to create effective prompts with Veo 3 | https://deepmind.google/models/veo/prompt-guide/ | `veo_deepmind.html` → `txt/veo_deepmind.txt` | 「The more detail you add, the more control you'll have over the final output」；**7 个小标题**：Shot framing and motion / Style / Lighting / Character descriptions / Location / Action / Dialogue；「A woman in her twenties with wavy brown hair and light freckles」优于「a brown-haired woman」 |

---

## ② 各家控制维度切法对比表

> 「素材中未见」= 该厂商文档里没有把该维度作为独立控制项写出来（不等于模型不支持）。

| 控制维度 | 火山 Seedance 2.0/2.5（视频） | 火山 Seedream 4.0-5.0（图像） | 阿里百炼 万相（图/视频） | 腾讯混元生图 | 可灵 Kling | Midjourney | Sora 2 | Veo 3 |
|---|---|---|---|---|---|---|---|---|
| **主体** | 「将<图片/视频N>中的[主体核心特征]定义为<主体N>」，核心特征要求「2–3 个清晰、稳定的静态特征（如服饰、发型、外观、类别）」 | 含在「主体 + 行为 + 环境」 | 基础公式首项「主体」；进阶「主体（主体描述）」 | 「关键人物主体」，人物/动物类模板含「人物具体的五官/表情/行为/动作/姿态」 | `element` 主体参考「最多支持指定3个主体」；正文用 `@xxx` 指代 | 散文描述，无结构化主体定义 | 「Anchoring your subject with a few distinctive details keeps it recognizable」 | 「Character descriptions」独立维度 |
| **动作 / 运动** | 独立维度「动作细节」；要求「肢体细化 + 程度量化」、「优先低缓连续小动作」、「补充动作过渡衔接」、「情绪具象外化表达」（抽象情绪→动作表） | 「行为」 | 视频基础公式「运动」；运动描述含「幅度、速率和运动作用的效果」 | 人物模板含「行为/动作/姿态」 | 动作控制 = 外部参考视频驱动（硬约束），非文本描述 | 无独立维度 | 「Actions」独立小节 + 「one clear subject action」；动作写成节拍（beats/counts） | 「Action」独立维度 |
| **场景 / 环境** | 「场景环境」；「空间关系建议优先通过参考图表达」 | 「环境」 | 「场景」= 「背景、前景」 | 人物/物品模板含「所在场景/背景」；风景模板含「场景的详细构成」 | 素材中输入场景参考 | 散文描述 | Prose 段描述 setting | 「Location」独立维度，「Describe your scene thoroughly」 |
| **镜头 / 景别 / 运镜** | 「镜头运镜」；「直接使用标准运镜术语即可」；「一个镜头里尽量只指定 1 种运镜方式」；2.5 给词表：景别（大全景/全景/中景/近景/特写）、运镜（推/拉/摇/移/跟/环绕/俯冲/后拉/上摇/手持晃动）、机位（低角度/俯视/第一人称） | 提示词建议含「构图」 | **词典化**：视频侧「镜头」分 镜头焦段（长焦/超广角-鱼眼）、机位角度（过肩/高角度/航拍）、镜头类型（干净的单人镜头/双人镜头/群像镜头/定场镜头）；图像侧「镜头拍摄类型」分 微距/超广角/长焦/鱼眼，另有「景别」（特写/近景/中景/远景）与「视角」（平视/俯视/仰视/航拍） | 三套模板均以「镜头取景方式」收尾 | 多镜头靠 `"镜头 n, m, words;"` 格式，非词表 | 无词典，靠 `--ar` 控画幅 | Cinematography 块：`Camera shot` / `Mood` + 示例「wide establishing shot, eye level」「slowly tilting camera」 | 「Shot framing and motion」独立维度 |
| **光照** | 「光影色调」 | 「光影」 | **词典化**：视频侧「光源类型」（日光/火光/阴天光/晴天光）、「光线类型」（柔光/硬光/侧光/高对比度）、「时间段」（白天/夜晚/黎明）；图像侧「光线」（自然光/逆光/霓虹灯/氛围光） | 模板含「整体环境氛围」，风格词表内无独立光线维度 | 素材中未见独立光照维度 | 无独立维度 | Lighting + palette 块：「软窗光 + 暖灯补 + 走廊冷边光」；「Naming three to five colors helps keep the palette stable」 | 「Lighting」独立维度 |
| **风格** | 「视觉风格」；示例「赛博朋克冷蓝紫色调、复古胶片、日系清新」 | 「风格」 | 图像：「风格（定义风格）」+ 词典 13 类（3D卡通/废土风/点彩画/超现实/水彩/粘土/写实/陶瓷/3D/水墨/折纸/工笔/国风水墨）；视频：「风格化」+ 视觉风格词典（毛毡/3D卡通/像素/木偶动画/黏土/黑白动画） | **三分类预置词表**（现实类 / 动漫艺术类 / 通用艺术类，共 40+ 词，见第③节）；亦可用 `Style` 参数传编号 | 图像 API 有「风格训练」「风格迁移」能力项；正文无风格词表 | `--sref`（图片/code）+ `--sw 0–1000` 控强度 | 「Style is one of the most powerful levers」；建议开头定风格（如「1970s film」） | 「Style」独立维度；示例「cartoon? Claymation? Film noir shot on 35mm?」 |
| **画质** | **独立维度「画质」**，给固定模板（见第③节）；另「画质、风格与约束词」统称一节 | prompt「不超过300个汉字或600个英文单词」；无画质词模板 | 图像进阶公式含「细节修饰」：「光源的位置」「道具搭配」「环境细节」「高分辨率」；示例中出现 `4K`、`8K`、`32k UHD` | `Clarity` 参数（x2 / x4 超分） | 分辨率参数 720P/1080P/4K、1K/2K/4K | `--quality/--q`、`--hd/--sd` | 无画质词模板；用摄影术语（`65 mm photochemical contrast`、`fine grain`） | 无画质词模板 |
| **负面 / 约束** | **无独立参数**，写进正文：约束词模板 + 2.5「负向控制」小节（字幕、音效/bgm/对白）（见第③节） | 素材中未见负面通道 | **独立参数 `negative_prompt`**（图像）：示例 `"negative_prompt": "人物"`；视频侧素材中未见 negative_prompt 字段 | **独立参数 `NegativePrompt`**：示例值「黑色，雨」 | **独立参数 `negative_prompt`**（图片 API）；「图生图场景下不支持负向提示词」；视频侧素材中未见 negative_prompt 字段 | `--no` 参数 | 官方指南未给负面通道；仅在示例里出现「Avoid signage or corporate branding」这类正向避让句 | 官方指南未给负面通道 |
| **参数（非文本控制）** | Seedance 1.0：`resolution / ratio / duration / seed / camera_fixed / watermark`，旧式内联 `--rs --rt --dur --seed --cf --wm`；2.5：`ratio`（`adaptive`）、`duration`（`-1`）、`output_format`（mov）、`content.role`（first_frame/last_frame/reference_*） | 宽高像素区间 `[921600, 4624220]`、宽高比 `[1/16, 16]`；`optimize_prompt_options.mode` | `prompt_extend` | `Resolution` / `Num`（1–4 张）/ `Clarity` / `Seed` / `LogoAdd` / `Revise` | `settings`：`multi_shot` / `audio`（native/off）/ `resolution` / `duration`；`watermark` | 全套 `--` 参数（第①节 #25） | `model` / `size` / `seconds`（"4","8","12","16","20"）/ `characters`；「You cannot request them in prose」 | 素材中未见参数化控制说明 |
| **多镜头 / 分镜时序** | 2.0：只响应「镜头 1 / 镜头 2」序号（「模型对精确时间（如 0–3 秒）的支持不稳定」）；2.5：**响应整数秒时间戳**，支持 `[1s-4s]…[4s-8s]`、时间点、相对时间三种写法 | 组图生成：一次生成多张连贯插画（`生成一组共4张连贯插画`） | 多镜头公式 `总体描述 + 镜头序号 + 时间戳 + 分镜内容`；示例「第 1 个镜头[0-3 秒]…」；「wan2.7 模型不再支持 `shot_type`」 | 素材中未见多镜头说明 | `"镜头 n, m, words;"`（≤6 分镜，时长和=总时长） | 素材中未见 | 「Optimized Shot List (2 shots / 4 s total)」+ 时间码 `0.00–2.40` | 素材中未见（示例为单镜头） |
| **声音 / 对白** | 2.0/2.5 原生音视频联合生成；2.5「支持负向控制音频：支持更细维度的单独控制：音效、背景音乐（bgm）、对白」 | 素材中未见 | **声音公式**：人声 = 内容 + 情绪 + 语调 + 语速 + 音色 + 口音；音效 = 音源材质 + 行为 + 环境音；背景音乐 = 配乐 + 风格。关断写法：「无台词」/「No dialogue.」「无背景音乐」/「No background music.」 | 素材中未见 | `audio`（native / off）；「声音控制（人声）」列在能力地图 | 素材中未见 | `<dialogue>` 块；「Place it in a `<dialogue>` block below your prose description」 | 「Dialogue」独立维度；可给角色指定台词 |
| **素材指代语法** | `<主体N>@<图片N>`（如「张三@图片1」）、`<图片/视频N>`、`将<图片/视频N>中的[…]定义为<主体N>`；「不得直接以 Asset ID 替代<图片/视频N>」 | 多图融合，用自然语言指代 | `图 n` / `视频 n`（英文 `Image 1` / `Video 1`，「英文字母和数字之间有空格，首字母大写」）；wan2.6 用 `character1` | `ContentImage` 参考图，无文本指代语法 | `@Zhang`；「请避免不同主体名称存在包含关系，如：@Zhang 与 @ZhangSan」 | 图片 prompt / `--sref` | `characters` 数组传 ID + 「refer to the character by name in the prompt」；「no more than 2 characters per generation」 | 素材中未见 |
| **词长上限** | 视频正文：素材中未见统一字数上限（可灵除外） | **≤300 汉字 / 600 英文单词** | 素材中未见 | **≤1024 utf-8 字符**（Prompt 与 NegativePrompt 同） | 视频正文 ≤3072 字符（建议 ≤2500）；`words` ≤512；图片 prompt ≤2500 字符 | 素材中未见 | 素材中未见（建议「shorter clips」遵循更可靠） | 素材中未见 |
| **自动改写 / 扩写** | 2.5 提示词模板 + 官方 skill `npx skills@latest add … --skill sd25-pe`；Seedream 有 `optimize_prompt_options` | `optimize_prompt_options.mode`（standard / fast） | `prompt_extend`（默认 true）；建议把公式作为 system message 交给 qwen3.6-plus 生成提示词 | `Revise`（1 开 / 0 关，默认开启；「如果上传了参考图，扩写关闭不生效」） | 素材中未见 | 素材中未见 | 素材中未见 | 「you can also use Gemini to help you expand on the prompt」 |

---

## ③ 预设词表摘录（原词保留，不翻译不改写）

### 3.1 画质词

| 厂商 | 原词 |
|---|---|
| 火山 Seedance 2.0 | `高清，细节丰富，电影质感，色彩自然，光影柔和` |
| 火山 Seedance 2.0（实战案例句尾） | `全程画面高清电影纪实风，色调温暖，光影柔和；人物面部稳定不变形，动作自然流畅，无卡顿无闪烁；环境音效与 @音频 1 自然融合。` |
| 火山 Seedance 2.5（案例） | `白平衡 4000K，青橙（teal-and-amber）调色，35mm，浅景深，胶片颗粒，弥漫的海雾，黄金时刻光晕` |
| 阿里百炼（图像示例中出现） | `高清相机`、`超高清`、`8K`、`32k超高清`、`32k UHD`、`超高清晰度`、`最佳品质` |
| 腾讯混元 | 素材中未见固定画质词模板（由 `Clarity` 超分参数控制） |
| 可灵 | 素材中未见画质词模板（由 `resolution` 参数控制） |

### 3.2 约束词（正向祈使式，火山方舟 Seedance 2.0 原文「常用约束词模板」）

```
避免生成字幕：“保持无字幕”、“避免生成任何文字或字幕”
避免生成 Logo：“不要生成Logo”
避免生成水印：“不要生成水印”
```

对应 badcase 处置原文：
- 「在提示词中加入明确的约束指令：“保持无字幕”、“避免生成任何文字或字幕”。」
- 「在提示词中加入明确的约束指令：“不要生成水印”、“不要生成Logo” 。」
- 2.5 备注：「提示词中已写明“不要字幕”，生成的视频仍可能出现字幕。相较 Seedance 2.0，该问题已明显优化，但仍有概率出现。」「确保参考视频本身不含字幕，否则“无字幕”指令可能失效。」

### 3.3 负面 / 负向词

| 厂商 | 通道 | 原词 |
|---|---|---|
| 火山 Seedance 2.5「负向控制」 | 写在正文 | 字幕：「不额外加入对白字幕」「不要字幕」；音频：「无 bgm，只生成环境音和动作音」「不要任何声音」 |
| 阿里百炼 | `negative_prompt` 参数 | 示例值仅见 `"negative_prompt": "人物"`；素材中未见负面词表 |
| 腾讯混元 | `NegativePrompt` 参数 | 示例值「黑色，雨」；素材中未见负面词表 |
| 可灵 Kling | `negative_prompt` 参数（图片 API） | 素材中未见负面词表 |
| 阿里百炼（视频侧关断写法） | 写在正文 | 「无台词」/「No dialogue.」「无背景音乐」/「No background music.」；「生成单镜头」/「Generate single shot.」 |
| Midjourney | `--no` 参数 | 文档只给参数定义「Tell Midjourney what you don't want in your image using the no parameter」，无词表示例 |
| OpenAI Sora 2 / Google Veo 3 | 素材中未见负面通道 | 仅见正向避让句：`Avoid signage or corporate branding` |

### 3.4 风格词表

**（a）火山 Seedance 2.0「风格」示例（原文）**
```
赛博朋克冷蓝紫色调、复古胶片、日系清新
```

**（b）阿里百炼「文生图 Prompt 指南」风格词典（原文，13 类）**
```
3D卡通、废土风、点彩画、超现实、水彩、粘土、写实、陶瓷、3D、水墨、折纸、工笔、国风水墨
```
（对应提示词示例原句：`网球女运动员，短发，白色网球服，黑色短裤，侧身回球，3D卡通风格。` / `火星上的城市，废土风格。` / `浅水彩，咖啡馆外，明亮的白色背景，更少细节，梦幻，吉卜力工作室。` / `兰花，水墨画，留白，意境，吴冠中风格，细腻的笔触，宣纸的纹理。` / `折纸杰作，牛皮纸材质的熊猫，森林背景，中景，极简主义，背光，最佳品质。` / `国风水墨风格，一个长长黑发的男人，金色的发簪，飞舞着金色的蝴蝶……`）

**（c）阿里百炼「视频生成Prompt指南」视觉风格表（原词：该表「类型」列取值）**
```
毛毡风格、3D 卡通、像素风格、木偶动画、黏土风格、黑白动画
```
另「风格化」定义原文示例：`赛博朋克、勾线插画、废土风格`

**（d）腾讯混元生图风格词表（原文完整三分类，40+ 词）**
```
现实类：摄影风格、黑白风格。
动漫艺术类：暗黑风格、素描风格、中国风风格、国潮风格、水墨风格、水彩风格、3D 风格、像素风格、赛博朋克风格、日本动画风格、手绘日漫风格。
通用艺术类：传统剪纸风格、刺绣风格、梵高风格、莫奈风格、油画风格、玉石风格、皮影风格、毛毡风格、波普风格、粘土风格、胶片电影风格、复古风格、极简风格、粉笔风格、贴纸风格、彩铅风格、穆夏风格、巴洛克绘画风格、古典主义风格、糖果色风格、青铜风格、故障艺术风格、野兽派风格、孟菲斯风格、老旧照片风格、平面构成风格、线稿风格、版画风格、埃及壁画风格、敦煌壁画风格、简单线条风格、沙画风格。
```
另：`您可以在 混元生图风格列表 中直接选择我们预置好的风格并将风格编号传入接口入参中的 Style`，API 示例值 `riman`。

**（e）Midjourney**
无自然语言风格词表，改为 `--sref`（图片或 Style Code）+ `--sw`（0–1000）+ Style Explorer 内置风格库。

### 3.5 其他成体系的预设模板 / 公式（原词）

**火山 Seedance 2.0 基础公式（按任务分类）**
```
图片参考：参考<图片N>中的<主体N>，生成...
视频参考：参考<视频N>中的<动作/运镜/风格/音效>，生成...
音频参考：参考<音频N>中的音色，生成...
增加元素：清晰描述<元素特征> + <出现时机> + <出现位置>
修改元素：严格编辑<视频N>，将其中的<原特征>修改为<新特征>
延长视频：向前/向后延长<视频N>，生成...
轨道补全：<视频1> + <过渡画面描述> + 接 <视频2> + <过渡画面描述> +接 <视频3>
参考<图片/视频N>的[参考维度]，严格编辑<视频X>，[具体编辑内容]
```

**火山 Seedance 2.5 一句话概述公式**
```
主体 + 地点 + 事件 + 题材/风格 + 特殊运镜...
```

**阿里百炼 万相 视频公式组（原词）**
```
基础公式       提示词 = 主体 + 场景 + 运动
进阶公式       提示词 = 主体（主体描述）+ 场景（场景描述）+ 运动（运动描述）+ 美学控制 + 风格化
图生视频公式   提示词 = 运动 + 运镜
声音公式       提示词 = 主体 + 场景 + 运动 + 声音描述（人声/音效/背景音乐）
多镜头公式     提示词 = 总体描述 + 镜头序号 + 时间戳 + 分镜内容
参考生视频公式 提示词 = 参考指代 + 动作 + 场景 + 台词（可选）+ 背景音乐（可选）
wan2.6         提示词 = 主角 + 动作 + 台词 + 场景
人声 = 角色说话的内容 + 情绪 + 语调 + 语速 + 音色 + 口音
音效 = 音源材质 + 行为 + 环境音
背景音乐 = 背景音乐/配乐 + 风格
```

**阿里百炼 万相 图像公式（原词）**
```
基础公式  提示词 = 主体 + 场景 + 风格
进阶公式  提示词 = 主体（主体描述）+ 场景（场景描述）+ 风格（定义风格）+ 镜头语言 + 氛围词 + 细节修饰
```

**腾讯混元生图三套模板公式（原词）**
```
人物/动物类：风格描述 + 关键人物主体 + 人物具体的五官/表情/行为/动作/姿态等 + 人物的服饰 + 人物所在场景/背景 + 整体环境氛围 + 镜头取景方式
风景类：      风格描述 + 关键场景主体 + 场景的详细构成（列举和描述场景的各个组成部分） + 背景/整体环境氛围 + 镜头取景方式
物品类：      风格描述 + 关键物品主体 + 物品的详细构成（列举和描述物品的各个组成部分） + 物品的材质/纹理/造型等 + 物品所在场景/背景 + 镜头取景方式
```

**可灵 Kling 多镜头模板（原词）**
```
“镜头 n, m, words; 镜头 n, m, words;”，用半角符号分隔
a. n：分镜序号；最多支持6个分镜，最少支持1个分镜
b. m：分镜时长；每个分镜时长不小于1，所有分镜时长之和等于当前所生成视频总时长
c. words：分镜提示词；最大长度512
通过@xxx的格式来指定某个主体，如：@Zhang。
```

**OpenAI Sora 2 描述式模板（原词）**
```
[Prose scene description in plain language. Describe characters, costumes, scenery, weather and other details. Be as descriptive to generate a video that matches your vision.]

Cinematography:
Camera shot: [framing and angle, e.g. wide establishing shot, eye level]
Mood: [overall tone, e.g. cinematic and tense, playful and suspenseful, luxurious anticipation]

Actions:
- [Action 1: a clear, specific beat or gesture]
- [Action 2: another distinct beat within the clip]
- [Action 3: another action or dialogue line]

Dialogue:
[If the shot has dialogue, add short natural lines here or as part of the actions list. Keep them brief so they match the clip length.]
```

**Sora 2 超详尽分镜块字段名（原词）**
```
Format & Look / Lenses & Filtration / Grade / Palette / Lighting & Atmosphere / Location & Framing / Wardrobe / Props / Extras / Sound / Optimized Shot List / Camera Notes (Why It Reads) / Finishing
```

**Google Veo 3 七维提示要素（原词小标题 + 定义）**
```
Shot framing and motion — How do you want to frame your output and how should the camera move during the shot?
Style — Describe what you are creating. Is it a cartoon? Claymation? Film noir shot on 35mm?
Lighting — How is the scene lit? Is it warm lighting that's even across the frame? Or is there a spotlight in one area of your shot?
Character descriptions — Add more detail to characters' appearances.
Location — Describe your scene thoroughly. Is it a jazz club? Or a smoky jazz club at night?
Action — What are your characters doing?
Dialogue — Veo 3 can generate dialogue.
```

---

## ④ 各家共识与分歧

### 4.1 共识（≥4 家同时出现）

1. **主体 + 场景 + 动作/运动 是最小骨架**。火山（精准主体/场景环境/动作细节）、阿里（主体+场景+运动）、腾讯（关键主体+场景/背景+行为动作）、Sora（subject/setting/action）、Veo（Character/Location/Action）五家一致。区别只在顺序与是否显式成式。
2. **一律推「结构化公式」而非自由文案**。火山称「工程型指令」/「用导演的思维书写结构化 Prompt」；阿里称「结构化提示词公式」；腾讯给三套模板；Sora 给 `Cinematography / Actions / Dialogue` 段落式；Veo 给 7 维清单。
3. **「基础档 / 进阶档」两档写法**。火山（基础公式 / 进阶公式）、阿里（基础公式 / 进阶公式，图像与视频各一套）、腾讯（原始 Prompt / 优化后 Prompt 对比）、Sora（shorter prompts vs going ultra-detailed）四家显式分档。
4. **镜头语言被当作独立可点名维度**。火山给运镜术语表；阿里给景别/视角/镜头类型/机位角度词典；Sora 给 Cinematography 块与 framing 示例；Veo 给 Shot framing and motion 维度。**这是图/视频两侧最普遍被「词典化」的维度**。
5. **都提供「自动改写/扩写」兜底**。阿里 `prompt_extend`、腾讯 `Revise`、火山 Seedream `optimize_prompt_options` 与 Seedance 2.5 官方 skill、Veo「用 Gemini 扩写」。Midjourney 与可灵素材中未见此类开关。
6. **多镜头/分镜叙事成为新标配**。火山（镜头 1/2/3 或时间戳）、阿里（镜头序号 + 时间戳）、可灵（`镜头 n, m, words;`）、Sora（Optimized Shot List + 时间码）四家都给出结构。
7. **素材指代必须显式、唯一、无包含关系**。火山（`<主体N>@<图片N>`，「避免冗余，避免语义冲突」）、阿里（`图n`/`视频n`，「图和视频分开计数」）、可灵（`@Zhang`，「请避免不同主体名称存在包含关系」）、Sora（Character ID + prompt 中按名字引用）四家都把「指代消歧」写成硬规则。
8. **多素材不等于更好**。火山：「不建议用满素材上限，过多素材会导致模型难以判断特征优先级」；Sora：「We recommend no more than 2 characters per generation」；可灵：「最多支持指定3个主体」。

### 4.2 分歧

1. **负面控制放在哪一层，四派各不同。**
   - 独立 API 参数：阿里 `negative_prompt`、腾讯 `NegativePrompt`、可灵 `negative_prompt`（图片 API）
   - 写进正文自然语言：火山 Seedance（无独立参数，「不要字幕」「无 bgm，只生成环境音和动作音」）
   - 斜杠参数：Midjourney `--no`
   - 完全不提供：Sora 2、Veo 3 官方指南素材中未见负面通道
   > 有意思的是：**给出负面参数的三家都没给负面词表**（示例值分别是「人物」「黑色，雨」），而唯一给出成体系约束词模板的火山反而没有负面参数。
2. **「参数 vs 散文」的边界松紧不同。**
   - 最严：Sora 2 —「You cannot request them in prose, they must be set explicitly in your API call」（分辨率、时长、角色引用一律走 API）
   - 最松：火山 Seedance 1.0 支持把参数写进提示词尾部（`--rs 720p --rt 16:9 --dur 5`），同时推荐 request body 直传
   - 中间：可灵全 JSON 化（prompt/settings 分离）；Midjourney 全 `--` 内联
3. **时间控制的粒度互斥。**
   - Seedance 2.0 **不响应时间戳、只响应镜头序号**，且文档明确警告「模型对精确时间（如 0–3 秒）的支持不稳定」；Seedance 2.5 才改为**响应整数秒时间戳**（文档「与 Seedance 2.0 的差异点」写明）
   - 阿里万相多镜头**要求写时间戳**（`第 1 个镜头[0-3 秒]`）
   - Sora 用 Shot List 时间码（`0.00–2.40`），但建议「concise shots」、宁可拼两个 4s 片段
   同一件事，三家给出的结论相反（能写 / 必须写 / 别写太长）。
4. **风格控制：预置编号派 vs 自然语言派。**
   - 预置编号/码库：腾讯（`Style` 传编号，示例 `riman`）、Midjourney（`--sref` Style Code）
   - 自然语言词表：火山（赛博朋克冷蓝紫色调、复古胶片、日系清新）、阿里（13 类风格词典）
   - 参照图：可灵（风格训练/风格迁移能力项）
5. **词长上限口径差异极大**：火山 Seedream ≤300 汉字/600 英文单词；腾讯 ≤1024 utf-8 字符；可灵视频 ≤3072（建议 ≤2500）、图片 ≤2500；阿里、Midjourney、Sora、Veo 素材中未见数字上限。
6. **对「参考素材的复用程度」态度相反。**
   - 火山 2.5：「当参考素材本身已足够精准时，建议只做『指代』、减少画面复述」
   - Sora 2 / Veo 3：主张尽可能详尽描述，`detailed prompts give you control and consistency`
   同一条素材，中国厂商教「少写」，美国厂商教「多写」。
7. **效果稳定性的诚实度不同。** 火山会在文档里明写 badcase 与概率（「提示词中已写明"不要字幕"，生成的视频仍可能出现字幕…但仍有概率出现」）；其余各家素材中未见同等颗粒度的失败率披露。

---

## ⑤ 抓不到的清单（如实）

> 共 **14** 项。分为「站点不可达」「需登录/JS 渲染」「文档不存在」「通道被封」四类。

| # | 目标 | 登记位置 | 实际结果 |
|---|---|---|---|
| 1 | Runway — Gen-4 Video Prompting Guide | `urls1.json` / `urls4.json`：`https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide` | Playwright 三次重试全部 `Page.goto: Timeout 45000ms exceeded`（`.txt.err`）；Cloudflare 挑战页 `runway_gen4.html` 标题为「Just a moment...」；代理 `.md` 文件返回 `403 Forbidden` |
| 2 | Runway — Introduction to Prompting | `urls1.json` / `urls4.json`：`…/47313698911891-Introduction-to-Prompting` | 同上，三次重试 Timeout；`runway_intro.html` = 「Just a moment...」 |
| 3 | Runway — Gen-3 Alpha Prompting Guide | `urls1.json`：`…/30586818553107-Gen-3-Alpha-Prompting-Guide` | `net::ERR_CONNECTION_CLOSED` |
| 4 | Runway Gen-4 文档 archive.org 镜像 | `urls3.json` / `urls4.json`：`web.archive.org/web/2026…` 与 `web/2026id_/…` | 两次均为 `net::ERR_CONNECTION_CLOSED`（`fetch4.log` 三次重试后 `FAILED`） |
| 5 | Luma Dream Machine — prompt-guide | `urls1.json` / `urls3.json`：`https://lumalabs.ai/prompt-guide` | `net::ERR_CONNECTION_CLOSED`；降级抓到的 `luma.html` 是 Notion 外壳页（`<title>Notion</title>`），innerText 仅 8 字节，正文需 JS 渲染 |
| 6 | Luma prompt-guide archive.org 镜像 | `urls3.json` / `urls4.json`：`web.archive.org/web/2026id_/…` | 三次重试 `net::ERR_CONNECTION_CLOSED`，`FAILED` |
| 7 | Pika 官方提示词文档 | — | **本轮全部 6 个 urls*.json 中均无 Pika 条目**，即从未进入抓取队列；素材中未见 |
| 8 | MiniMax 官方平台文档（视频 / 图片生成） | `urls6.json`：`https://platform.minimaxi.com/document/video_generation`、`…/image_generation` | urls 已登记但 `pages/` 下**无对应 .txt / .err 落盘**——需登录的 SPA，未取得正文 |
| 9 | MiniMax 视频提示词写作指南（MiniMax-H3） | `urls3.json` / `urls5.json`：`https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md` | `net::ERR_CONNECTION_CLOSED` |
| 10 | 即梦 / Seedream 独立提示词指南 | `urls3.json`：`https://docs.volcengine.com/docs/ark/seedream-prompt-guide?lang=zh` | **该文档不存在**：URL 重定向到通用落点页（`www.volcengine.com_docs_82379_1542787.txt`，5548B，内容为模型列表 + SDK 示例）；素材中未见任何独立 Seedream 提示词指南正文 |
| 11 | Google — Veo 3.1 官方提示词指南（Cloud Blog） | `urls3.json` / `urls4.json`：`https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1` | 三次重试 `net::ERR_CONNECTION_CLOSED`，`FAILED` |
| 12 | 可灵控制台 `app.klingai.com/global/` | `urls3.json` | `net::ERR_CONNECTION_CLOSED`（该页为控制台入口，非文档正文，不影响本次结论） |
| 13 | 第三方代理补抓通道（jina.ai / corsproxy.io / codetabs.com） | `mj_param.md`、`mj_sref.md`、`runway_gen4.md`、`vol_sd10.md`、`vol_sd20.md`、`openai_sora2.html`、`p1.html`、`p2.html`、`p3.html` | 全部失败：文本型代理返回 `<title>403</title>403 Forbidden`；`openai_sora2.html` 返回 `Forbidden`；`p1.html` = `Oops... Request Timeout.`；`p2.html` = codetabs.com `522: Connection timed out`；`p3.html` = corsproxy `{"success":false,"status":403,"error":"keyless_legacy_url"}` |
| 14 | 腾讯混元生图风格列表（编号 → 风格名对照表） | 混元生图 Prompt 指南正文引用「混元生图风格列表」，API 文档引用「请在混元生图风格列表中…选择期望的风格，传入风格编号」 | **该对照页未被抓取**，素材中只有 `Style` 参数的一个示例值 `riman`；完整编号表缺失 |

**旁注（非失败，但需说明处理）**：
- `openai_sora2.html`（HTML 版）失败，但同页 `.ipynb`（`openai_sora2.ipynb`、`openai_sora2b.ipynb`）成功取得，并已转出 `pages/openai_sora2_cookbook.md`（25 KB，正文完整），Sora 2 内容不受影响。
- `tencent_hunyuan_task.html` 为 gzip 压缩体（magic `1f 8b 08`），上轮未能解析；本轮已解压并转出 `txt/tencent_hunyuan_task.txt`，故第①节 #17 可用。
- DeepMind Veo 页 `deepmind.google/models/veo/prompt-guide/` 在 `urls1/urls3/urls4.json` 中三次尝试均 `ERR_CONNECTION_CLOSED`，但上轮另有一份成功的 `veo_deepmind.html`（208 KB，标题「How to create effective prompts with Veo 3」），Veo 内容以该份为准。
