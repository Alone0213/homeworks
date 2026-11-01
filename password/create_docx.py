# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import re

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)

def set_line_spacing(paragraph, pt_value):
    pPr = paragraph.paragraph_format
    pPr.line_spacing = Pt(pt_value)

def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'SimSun'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
    run.font.size = Pt(14)
    run.font.bold = True
    set_line_spacing(p, 22)
    p.paragraph_format.space_after = Pt(6)

def add_heading1(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'SimSun'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
    run.font.size = Pt(12)
    run.font.bold = True
    set_line_spacing(p, 22)

def add_heading2(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'SimSun'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
    run.font.size = Pt(12)
    run.font.bold = True
    set_line_spacing(p, 22)

def add_body(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'SimSun'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
    run.font.size = Pt(12)
    set_line_spacing(p, 22)
    p.paragraph_format.first_line_indent = Pt(24)

with open('OPSA论文_完整版.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

body = ''.join(lines)

# Title
for line in lines:
    if line.startswith('# ') and not line.startswith('## '):
        add_title(doc, line.replace('# ', '').strip())
        break

in_ref_section = False
section_order = ['摘要', '一、研究背景与意义', '二、理论基础与安全假设', '三、方案设计', '四、安全性分析', '五、比较分析与应用', '六、总结', '参考文献']

current_section = None
abstract_done = False

for line in lines:
    s = line.strip()
    if s == '':
        continue
    
    # Check if this is a section heading
    if s.startswith('## ') and not s.startswith('### '):
        h = s.replace('## ', '').strip()
        if h in section_order:
            current_section = h
            if h == '摘要' and not abstract_done:
                add_heading1(doc, '摘要')
                abstract_done = True
            elif h == '参考文献':
                in_ref_section = True
                add_heading1(doc, '参考文献')
            elif any(c in h for c in ['一、', '二、', '三、', '四、', '五、', '六、']):
                add_heading1(doc, h)
            continue
    
    if s.startswith('### '):
        add_heading2(doc, s.replace('### ', '').strip())
        continue
    
    # Handle body text
    if s.startswith('**摘要：**'):
        add_body(doc, s.replace('**摘要：**', '').strip())
        continue
    
    if s.startswith('**关键词：**'):
        p = doc.add_paragraph()
        run = p.add_run(s)
        run.font.name = 'SimSun'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
        run.font.size = Pt(12)
        run.font.bold = True
        set_line_spacing(p, 22)
        continue
    
    if s.startswith('# ') and not s.startswith('## '):
        continue  # Title already done
    
    if in_ref_section and re.match(r'^\[\d+\]', s):
        add_body(doc, s)
        continue
    
    if not s.startswith('#') and not s.startswith('|') and not s.startswith('---'):
        # Skip table formatting lines
        add_body(doc, s)

doc.save('OPSA论文_正式版.docx')
print('Document saved successfully!')
