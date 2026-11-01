# P4 slide-designer 任务

> 必读通用规范：F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\slide-designer-common.md。任务文件只限本文件与该通用规范；除此之外仅可读取二者直接列出的本页输入、模板、风格与规范文件。不得读取其他 `page-*-task.md` 或主控索引。

### P4  [内容页 / unknown]
- 输出文件（最高优先级，禁止违反）：F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\pages\page-4.pptx.html
- 本页大纲：标题「面向跨地域小组学习与远程评审场景，构建零配置开箱即用平台」／类型 `unknown`／研究需求 ✅
  - 内容概要：需求分析与场景定位。目标场景：跨地域的小组学习、线上科研讨论、远程代码/架构评审。核心目标：构建一个**零配置、开箱即用**的Web协作平台。实现"白板+语音+文件"三大功能的深度集成，提供沉浸式的协作体验
  - 数据需求：目标用户群体规模、典型协作场景频率、功能需求优先级排序（仅参考）
- Deck context / 元数据（以下 page_number、total_pages、content_page_count 仅供任务定位与结构占位符；**禁止直接上屏**）：page_number=4；total_pages=15；content_page_count=13。默认禁止页码；只有 spawn prompt 中用户明确要求页码时，才可按当前风格文件规定的格式使用。
- 内容素材：本页大纲摘录（见下方「本页大纲」）+ F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\research-P4.md；**禁止读取 outline.md**（摘录已含本页所需素材，不能浏览其他页）。
- 图表规范：需要（内容页默认按图表候选页处理，必读 D:\Programs\OfficeAce\office-claw-skills\pptx-craft\references\designer\charts.md 的图表与数据可视化章节）
- 密度档位：`lean`（research 写有证据受限标注（数据有限，基于…））
- 内容模式：`evidence_limited`；正文根内的卡片和条目优先采用内容自适应高度：卡片/列表/网格不得无条件使用 flex:1 填满空轨道，使用 h-fit、align-items:start 或 flex-shrink:0；只有主视觉或图表在确有内容消费时使用 flex:1。
  - 该档位只影响留白类检测，不要求你做额外容量计算；
  - 3.4 的检测命令必须带 `--density lean`；
  - 本页素材偏少，留白门槛已放宽：不要为凑跨度硬编内容、拉大字号或插空容器；宁可减少块数、收窄轨道，也不要注水。**溢出、越界、图表压字的判定与档位无关，任何情况下都不放宽。**
- 本页完整检测命令（逐字执行，不得删参）：`node "D:\Programs\OfficeAce\office-claw-skills\pptx-craft\packages\cli\dist\cli.js" check-layout "F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\pages" --pages 4 --density lean`
- 本页使用图表时，写入完成后先执行激活命令：`node "D:\Programs\OfficeAce\office-claw-skills\pptx-craft\packages\cli\dist\cli.js" activate-template-chart --file "F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\pages\page-4.pptx.html"`；无图表则跳过。
- 可用素材（`validate-research` 确定性统计，**不要自己重数**）：主轴 4×3 = **12 格** ｜ 关键数据 8 条 ｜ 上屏要点 6 条 ｜ 案例 3 条 ｜ **可上屏原子合计 29**
  - 3.1 ① 的素材清单**就是这些**，不得出现清单之外的内容；
  - 3.2 安排 block 时不得超过这份供给：某块需要的同轴槽位超过主轴的 12 格时，**必须减槽位/减并列项/合并块**——禁止编造条目、同义改写凑数，或把某个对象的数值挪到另一个对象名下。
### 本页图片映射
- 本次未传入图片映射；使用无图片布局，不得自行搜索或生成替代内容图。
- 任务：你负责生成第 4 页的 HTML 幻灯片。仅生成该页面，确保内容完整提取自本页研究素材 research-P4.md。本页所有可见文字只能来自本页大纲摘录与 research-P4.md，不得把风格描述或制作元数据当作文案。
