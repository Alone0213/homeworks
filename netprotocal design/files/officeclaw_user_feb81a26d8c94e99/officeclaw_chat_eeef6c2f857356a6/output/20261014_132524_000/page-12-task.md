# P12 slide-designer 任务

> 必读通用规范：F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\slide-designer-common.md。任务文件只限本文件与该通用规范；除此之外仅可读取二者直接列出的本页输入、模板、风格与规范文件。不得读取其他 `page-*-task.md` 或主控索引。

### P12  [内容页 / unknown]
- 输出文件（最高优先级，禁止违反）：F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\pages\page-12.pptx.html
- 本页大纲：标题「实验设计涵盖白板同步延迟、音视频质量与文件传输速率三类评估指标」／类型 `unknown`／研究需求 ✅
  - 内容概要：实验设计与性能评估。评估指标：(1) 白板协同：操作同步延迟、并发冲突解决时间、状态一致性收敛时间；(2) 音视频：连接建立时间、端到端延迟、丢包率、MOS评分；(3) 文件传输：传输速率、成功率、断点续传恢复时间。测试场景：2/4/8人协作、不同网络条件（WiFi/4G/弱网）、不同文件大小（1MB/100MB/1GB）
  - 数据需求：各评估指标的目标基准值、不同并发规模下的性能预期、弱网测试参数配置（仅参考）
- Deck context / 元数据（以下 page_number、total_pages、content_page_count 仅供任务定位与结构占位符；**禁止直接上屏**）：page_number=12；total_pages=15；content_page_count=13。默认禁止页码；只有 spawn prompt 中用户明确要求页码时，才可按当前风格文件规定的格式使用。
- 内容素材：本页大纲摘录（见下方「本页大纲」）+ F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\research-P12.md；**禁止读取 outline.md**（摘录已含本页所需素材，不能浏览其他页）。
- 图表规范：需要（内容页默认按图表候选页处理，必读 D:\Programs\OfficeAce\office-claw-skills\pptx-craft\references\designer\charts.md 的图表与数据可视化章节）
- 密度档位：`standard`（research 未标注证据受限）
- 内容模式：`evidence_rich`；正文可使用配额高度，但只有子元素实际消费分配空间时才使用 flex:1；短标签卡片和稀疏列表仍按内容自适应高度排版。
  - 该档位只影响留白类检测，不要求你做额外容量计算；
  - 3.4 的检测命令必须带 `--density standard`；
  - 素材充足，按标准密度契约执行。**溢出、越界、图表压字的判定与档位无关，任何情况下都不放宽。**
- 本页完整检测命令（逐字执行，不得删参）：`node "D:\Programs\OfficeAce\office-claw-skills\pptx-craft\packages\cli\dist\cli.js" check-layout "F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\pages" --pages 12 --density standard`
- 本页使用图表时，写入完成后先执行激活命令：`node "D:\Programs\OfficeAce\office-claw-skills\pptx-craft\packages\cli\dist\cli.js" activate-template-chart --file "F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\pages\page-12.pptx.html"`；无图表则跳过。
- 可用素材（`validate-research` 确定性统计，**不要自己重数**）：主轴 5×3 = **15 格** ｜ 关键数据 7 条 ｜ 上屏要点 6 条 ｜ 案例 3 条 ｜ **可上屏原子合计 31**
  - 3.1 ① 的素材清单**就是这些**，不得出现清单之外的内容；
  - 3.2 安排 block 时不得超过这份供给：某块需要的同轴槽位超过主轴的 15 格时，**必须减槽位/减并列项/合并块**——禁止编造条目、同义改写凑数，或把某个对象的数值挪到另一个对象名下。
### 本页图片映射
- 本次未传入图片映射；使用无图片布局，不得自行搜索或生成替代内容图。
- 任务：你负责生成第 12 页的 HTML 幻灯片。仅生成该页面，确保内容完整提取自本页研究素材 research-P12.md。本页所有可见文字只能来自本页大纲摘录与 research-P12.md，不得把风格描述或制作元数据当作文案。
