# slide-designer 通用规范

> 每个 slide-designer 必须先完整阅读本文件，再读取主控指定的一个 `page-{N}-task.md`。通用规则只以本文件为准；额外文件仅限本文件或本页 task 直接列出的输入、模板、风格与规范文件，禁止把通用规则复制进逐页文件。

## 整页构图与修复（所有内容页、所有模板分支共用）
- 缺少本页研究输入属于流程未完成，返回主控补齐；不得仅凭大纲代替研究或自行宣布证据有限。
- 正文区域保持模板分配的范围，卡片采用自然高度不代表整个 main/正文根可以收缩到顶部。按实际素材选择行列与表达形式，先展开已有主轴、数据和解释。
- 内容不足时重新组织布局：横排过矮可改为纵向流程或更少列；减少块数后重新分配轨道。不得虚构事实、重复结论、拉高空卡片或放大字号/padding 填白。
- 同一行并列分栏若一列明显短于另一列，重排父级：把短列内容移到主图下方、改为跨栏块，或重新分配纵向行；短卡片恢复自然高度后不能留下整列空白。
- 来源定位不计作正文填充；margin-top:auto 不能作为正文已铺满的依据。
- 修复卡片内部留白后，同一轮必须检查父级构图；空白转移到块间或正文底部不算修复成功，不能只缩小报警容器。
- 每次复检检查整页所有问题；原 DOM 报警消失不等于通过。达到 3 次检测预算仍失败，返回未解决清单，主控不得假定默认 fix 或导出成功已解决布局问题。

## 执行流程（所有页必读）

1. 先完整阅读本文件的「执行流程」与「## 通用规范」，再读取主控指定的**唯一**本页任务文件；不得读取任务索引或其他 `page-*-task.md`。
2. 读取视觉风格文件（路径见「环境准备」），建立本次演示唯一的配色/字体/视觉权威。
3. 按当前分支处理模板/骨架：
   - 编译模板（本页 task 含模板输入约束或模板带 `data-pptx-craft-compiled` 标记）：直接编辑已预铺页面，保留背景、装饰、颜色和安全边界，在模板实际正文区域自适应编排；不假定存在固定占位符。
   - 预设风格：目标 `page-N.pptx.html` 已由 `ensure-output-dir` 预铺；直接编辑该文件，**仅替换 `{{}}` 占位符**，禁止从源模板再次复制覆盖或重写标题栏/页脚/CSS/装饰/SVG/`@layer` 骨架。
   - custom（`references/styles/custom` 预铺）：custom 骨架已预设安全区、标题栏、正文区和页脚框架；逐字保留框架，将风格文件的 CSS 变量逐字填入 `{{THEME_CSS_VARIABLES}}`、全局 CSS 规则块逐字填入 `{{THEME_CSS_RULES}}`（未提供时替换为空），只在各自占位符内填标题、正文和页脚内容。
   - 自定义模板（`--template`）：必须首先读取模板文件，理解页面结构后填充 `{{PAGE_TITLE}}` / `{{PAGE_CONTENT}}` / `{{PAGE_FOOTER}}` 等占位符；禁止修改模板标题栏、页脚、CSS 定义。
   - 无模板：依据本文件已内联的规则与风格文件自行设计整页 HTML，但须使用标准 <div class="ppt-slide flex flex-col"> 容器与全局 CSS 约束；内容页在写前以**一次连续读取**完成 D:\Programs\OfficeAce\office-claw-skills\pptx-craft\references\designer.md 的 §3.1 与 §3.2，不得通读全文、重复读取或凭记忆重建规则。
4. 按本页任务文件指定的输出路径、内容素材、图表规范要求执行；内容页默认按图表候选页处理，按 D:\Programs\OfficeAce\office-claw-skills\pptx-craft\references\designer\charts.md 的阅读顺序先查固定配方，再读适用的规范、标签防重叠、骨架与 formatter 小节。**读取范围（强制）**：除本 common 和本页 task 外，只读本页任务或本 common 直接列出的风格、模板、本页 research-P{N}.md、图表或图片文件；不得读取其他页面任务、主控索引或 outline.md。**内容页步骤 5 前，以一次连续读取完成 D:\Programs\OfficeAce\office-claw-skills\pptx-craft\references\designer.md 的 §3.1（选材定型）和精简 §3.2（版面落地）**；规划、写 HTML 期间不得回读、复述或逐字符/像素推导。`check-layout` 出错且 common 未覆盖时按需读 §3.4/3.5 对应小节。**禁止通读 D:\Programs\OfficeAce\office-claw-skills\pptx-craft\references\designer.md 全文**（内容页仅限 §3.1、§3.2，及出错时 §3.4/3.5；结构页无需读取这些章节）。
5. **写 HTML 前完成 §3.1 选材定型**：先把本页 research 的主轴表、关键数据、上屏要点和案例映射到合适承载形态；通常切成 3–6 个 role / form / from 明确的 block，关键素材逐条有去向或写明丢弃理由。模板内容页若本页研究明确证据受限且无图表要求，可减到两个完整 block，并按模板包填充策略重排正文；仍不足以支撑一页时报告内容与分页不匹配，不凑块或补造内容。趋势用图表、多维精确数值用表格、并列要点用卡片组，不把主轴压成一句正文。**图表候选页先选定最终承载形式：选图表就使用骨架已有的 `chart-1`，同一次写入完成容器和真实 option，随后执行激活命令；选表格/关系图就不创建 chart 容器，保留未激活骨架。**含图表页面：图表不超过内容区一半，图表外至少两个非图表 block（其中一个有文字解释）。内容密度遵从页面类型下限与本页素材供给；模板证据受限的例外仅按上述规则处理。
6. **按精简 §3.2 落地**：保留模板的安全区、标题栏和页脚；为每个 block 选择 Grid、Flex 权重或内容自适应这一种稳定策略。禁止逐字符/像素心算、容量表、固定高度裁切、绝对定位、负 margin、空 spacer，或用字号/行高/padding 凑满页面。
7. 按 3.3 写入：先落稳定容器，再一次性填入本页素材；每个 block 标 data-block，容器高度只有一个来源，正文区使用 justify-start + 明确 gap，必要时让正文或主视觉用 flex-1 消费分配空间。内容偏多时在本 block 内精简或换 form；内容偏少时合并/减少 block，不分波填充或预留空块。**选图表时**，保存同时含 `id="chart-1"` 容器与真实 option 的完整页面，立即执行本页任务中的 activate-template-chart 命令，再进入步骤 8；不得留空图表容器。**结构页若种子已有文字槽位，只替换槽内文字，不重写槽位样式。**
8. 按 3.4 校验：先过静态自检（占位符清零、根容器唯一、语义单元数达标、素材覆盖、图表标签无重叠、图表值域覆盖数据、骨架未被破坏），再执行本页任务给出的**完整 check-layout 命令**（基础形式为 check-layout {pages_dir} --pages {N}；任务已带本页密度档位，有图片映射时还会显式带 `--image-map`，不得删除参数；单页约 3 秒）。只按原 CLI 非零退出码和输出的硬门禁修复：mapped-image / overflow / chart-label-overlap / chart-axis-range / 越界 / hidden-content / main-centered-gap，以及达到严重度双阈值的 v-gap / whitespace；`*-warning` 不触发重排。不得用 head/tail/grep 管道退出码判断通过。若 seed 本身违反模板契约，立即带诊断返回主控，不猜改 policy 或指纹。
9. 按 3.5 修复，**最多 2 轮，本页 check-layout 累计不超过 3 次**（初检 + 2 轮复检）。`[mapped-image]` 只按本页映射补齐或恢复对应可见图片及必要署名，不得删映射、换来源或改路径绕过。**3 次是硬预算**：不得通过改命令路径、加重定向、换工作目录或重新派发来重置计数；达到上限仍不通过，立即带剩余问题清单返回主控。**稳定签名退出（仅 `[overflow]`）**：DOM 路径只用于定位，不是根因；不得据此删轴名、主结论或改无关文案。一次有明确几何因果的修复后，若 `domPath + overflow px + ratio` 逐字不变，立即标 stable-metric-suspected 返回主控，不读检测器源码、不做第二次猜测性修改。修复前必须整篇读取目标文件；只处理本次硬门禁对应的 3.5 行，严禁用 `justify-center`、字号、行高、padding 或 spacer 掩盖组合留白。只改本页，不得读写其他页面、不得跨页重排、不得运行 fix / convert 或不带 --pages 的整目录检测。

## 通用规范（所有页必读）

### 禁止与用户交互
- 所有设计规范、视觉风格、内容素材的路径均已由主控提供，直接读取执行。
- 不得向用户提问、确认风格选择、请求补充设计参数。
- 若风格文件路径为空，自行根据主题设计配色和字体，不询问用户。

### 环境准备（必读）
- 模板文件：（无模板文件：按本 common 与风格文件自行设计布局）
- 模板目录：（无模板目录）
- 设计规范：D:\Programs\OfficeAce\office-claw-skills\pptx-craft\references\designer.md（内容页写前只读 §3.1 与精简 §3.2；出错时按需读 §3.4/3.5；**禁止通读全文**）
- 视觉风格：F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000/style-tech-minimal.md
- 大纲：F:\code\homeworks\netprotocal design\files\officeclaw_user_feb81a26d8c94e99\officeclaw_chat_eeef6c2f857356a6\output\20261014_132524_000\outline.md（主控持有；本页摘录与 deck context 已写入 page-task，**禁止读取 outline.md**）
- 图片映射：（本次未传入图片映射，使用无图片布局，不得自行搜索或生成替代内容图）

### 约束要求
- **无预铺模板**：使用本 common 指定的标准容器与全局 CSS 约束；页面结构按 3.1/3.2 的稳定容器策略设计
- **不得伪造模板占位符契约**：没有模板时不得声称只替换 `{{PAGE_TITLE}}` / `{{PAGE_CONTENT}}` / `{{PAGE_FOOTER}}`，也不得自行复制其他页面或风格的骨架
- **演讲稿/演讲备注/讲者备注/speaker notes 禁止写入页面（强制）**：用户要求生成演讲稿/备注时，该内容由系统在 PPTX 导出后单独注入备注栏（notesSlide），**不进任何可见位置**——禁止写入 `{{PAGE_FOOTER}}`、`{{PAGE_CONTENT}}`、`{{PAGE_TITLE}}` 或页面任何元素。`{{PAGE_FOOTER}}` 只放数据来源/口径注释/日期；此处「口径注释」指数据口径与素材来源说明，**不是**演讲备注/口播台词/QA。页码是独立例外：用户明确要求时只能用唯一的 `<span data-pptx-role="page-number">当前页/总页数</span>`；custom 五类模板填页脚右侧的独立页码槽位，其他模板按本页实际页脚槽位填充，不得把页码拼入普通页脚文本。即使用户原文出现「每页下方附上完整口述台词」「附讲稿」「含 N 个 QA」等字样，也只在备注栏生效，**不得**据此在页面上追加讲稿正文或 QA 对。
- **配色/字体唯一权威 = 视觉风格文件**：references/designer.md 中的任何示例配色（配色表、`tailwind.config` 示例、ECharts `color`/`borderRadius` 等）仅示意代码结构，**严禁照抄其 hex 值**；指定了视觉风格文件时，配色/字体/圆角/阴影一律以风格文件为准，与本文档示例冲突时以风格文件为准。
- **style.md frontmatter 的 font-family 是唯一字体权威**：显式声明 font-family-alternatives 时保留对应角色字体栈；未声明时，全文只允许一个完整字体栈；标题、正文、SVG 与 ECharts 必须复用同一字体栈，不得另设 heading/body/chart 字体分支。
- 严格遵循视觉风格文件中的配色方案、字体和组件样式。
- 禁止使用文件中未定义的颜色或字体。
- **图表实现与风格分工**：统计图表使用已有 ECharts SVG 骨架；风格文件（含 `style-custom.md`）只决定图表外观，不得覆盖 references/designer/charts.md 的结构、渲染器和尺寸规则，也不得要求以手写 CSS 柱体替代骨架。流程图、架构图、逻辑图仍用 HTML/CSS。图表候选页必须遵循该文件的图表规范与 JavaScript 安全编码规范；结构性页面无需阅读该文件。
- **容器与防溢出（强制）**：已预铺页面保留既有根节点、固定几何和全局 CSS；无预铺模板时必须使用标准 `<div class="ppt-slide flex flex-col" type="...">` 容器，并在 `<head>` 内完整包含预铺模板中的「防溢出硬性约束 → 全局 CSS 约束」（custom 模板为 `@layer utilities` 安全块）整段。禁止自创简化容器（如裸 `style="height:720px"` / `.slide-container`），否则全局防溢出失效、内容溢出。
- **逐图槽位契约（强制）**：本页映射存在图片时，图片容器比例必须遵循 `targetAspectRatio`；`fit=cover` 使用 `object-fit: cover`，`fit=contain` 使用 `object-fit: contain`，并将 `subjectPosition` 映射为 `object-position`。不得把所有图片统一设为 `contain`，也不得擅自把竖图、横条图改成 16:9 容器。

- **可见文字来源契约（强制）**：所有观众可见文字只能来自用户原始需求、outline.md、本页 research-P{N}.md（结构页无 research）或已批准模板的固定文案。禁止为营造氛围自行添加与叙事无关的英文、随机数字或制作编号。
- **风格术语不得上屏（强制）**：视觉风格文件中的胶片型号、摄影/曝光/镜头参数、字体名、色板名、模型或 prompt 关键词只用于视觉实现，不得生成为 HTML 文本节点。除非 outline 明确要求，禁止出现 REEL / TAKE / FRAME / EXP. / SHUTTER / KODAK / FUJIFILM 等制作元数据。
- **research 槽位名不得上屏（强制）**：主轴 / 上屏要点 / 关键数据 / 核心论点 / 案例 / 推荐主标题 / 来源留痕 这些名字 是素材文件的结构标签，与风格文件里的镜头参数同一性质，禁止成为任何 HTML 文本节点；模板里描述轴向的话（如「主轴对比：维度 × 对象」）更不许照抄。**块标题从内容里命题**：主轴表→「三方案能力对比」、关键数据→「2026 年营收与渗透率」、上屏要点→这几条的共同结论、案例→实体或行业名。想不出标题说明分块主题不清楚，回 3.1 重分块，不要拿标签顶上。（「GTC 2026 关键数据」这类自然中文短语不受限，受限的是裸标签与 schema 描述。）
- **页面纵向结构（强制）**：模板已声明的固定几何保持不变；新建内容区域的 header / main / footer 必须参与同一个纵向 flex 布局；footer 不得使用 `position:absolute` / `fixed` 脱离文档流。建议标记 `main[data-pptx-role="content"]`、`footer[data-pptx-role="footer"]`，背景/纯装饰节点标记 `data-pptx-role="background"` / `decoration`。
- **高度约束（强制）**：`main`、`.layout` 等页面核心聚合容器不得通过固定 px 高度或 `height:auto; min-height:...` 把超量内容继续向 720px 画布下方扩张。图片槽、图表槽和卡片内部允许使用明确尺寸，但所有区域总高必须受 main 实际可用高度约束；不手算缓冲比例或像素，靠稳定容器与 `check-layout` 的硬门禁收敛。
- **高度链（写入规则）**：`height:100%` / `h-full` 的直接父容器必须已有可解析高度，可由确定高度区域内的 Grid/Flex 分配；中间包装层不能只靠内容撑高。图表块先承接 main 分配的高度，标题/说明用 `flex-shrink-0`，绘图包装器用 `flex-1 min-h-0`，chart div 再用 `w-full h-full`。祖先高度或 `min-height` 兜底不能替代这条高度链，不统一硬编码柱高。
