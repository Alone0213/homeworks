---
font-family:
  - Noto Sans SC
  - sans-serif
---
# 风格规范：custom

## 整体风格描述
- 受众：大三本科生，课程设计开题报告
- 视觉气质：极简学术风，重内容轻装饰，白底深字、克制用色

## 配色方案
- 主色：#2C3E50（标题与结构性文字）
- 辅色：#6B7280（次要说明、标签、页码）
- 背景色：#FFFFFF
- 文字色：#1F2937
- 强调色：#2563EB（关键术语、技术名词、少量高亮）

## 字体
- 标题字体：Noto Sans SC
- 正文字体：Noto Sans SC

## 排版与组件规范
- 页面尺寸：1280×720px
- 标题字号：32px
- 正文字号：18px
- 每页内容量：3–5 个语义单元，标题 + 简短引述 + 要点列表或单张图示
- 卡片/分隔/图表风格：无卡片阴影堆叠，仅用 1px 细线或浅灰底色区分区块；图表使用单色描边 + 透明填充，无渐变

## CSS 主题变量
```css
--color-bg: #FFFFFF;
--color-surface: #F9FAFB;
--color-text: #1F2937;
--color-muted: #6B7280;
--color-accent: #2563EB;
--font-family: "Noto Sans SC", sans-serif;
--radius-card: 8px;
--shadow-card: 0 2px 8px rgba(31, 41, 55, 0.06);
--content-density: comfortable;
```

## 全局 CSS 规则
```css
.ppt-slide {
  background-color: var(--color-bg);
}
.page-header {
  color: var(--color-text);
  font-weight: 600;
  letter-spacing: 0.02em;
}
.page-main {
  color: var(--color-text);
  line-height: 1.7;
}
.page-footer {
  color: var(--color-muted);
  font-size: 14px;
}
```

## 图表约束
- 图表字体、颜色、标签和背景必须复用上述字体栈与 CSS 主题变量
- 禁止动画和渐变填充，保证 PPTX 矢量导出

## 页脚与页码规范
- 页码：保留页码（格式如 04 / 15）
- 页脚内容：默认留空

## 设计禁忌
- 禁止使用本文件未定义的颜色或字体
- 禁止动画
- 禁止渐变填充与重阴影
- 禁止装饰性插画、emoji、大色块背景
- 禁止卡片多层嵌套与圆角过大（≤8px）
- 禁止正文使用强调色大面积着色，强调色仅用于关键词与少量高亮