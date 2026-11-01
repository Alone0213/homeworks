# -*- coding: utf-8 -*-
"""Reformat 12_OPSA.docx per 《软件学报》 layout standards.

Requirements:
- Title: 四号(14pt), bold, centered
- Section headers (一、二、三...): 四号(14pt) bold
- Subsection headers (1.1, 2.1...): 小四(12pt) bold  
- Body text: 宋体(SimSun), 小四(12pt)
- Line spacing: fixed 22磅(22pt)
- Abstract/Keywords: 五号(10.5pt)
- References: 小五(9pt)
- Body: 两端对齐, 首行缩进2字符
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from lxml import etree

def set_run_font(run, font_name='宋体', size_pt=12, bold=None):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    if bold is not None:
        run.font.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = etree.SubElement(rPr, qn('w:rFonts'))
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)

def set_line_spacing(para, pt=22):
    pf = para.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(pt)

def set_first_line_indent(para, chars=2, font_size_pt=12):
    pf = para.paragraph_format
    pf.first_line_indent = Pt(font_size_pt) * chars

# Read from original (the rebuild script generated it)
doc = Document('12_OPSA.docx')

for idx, p in enumerate(doc.paragraphs):
    if not p.text.strip():
        continue
    
    text = p.text
    
    is_title = (idx == 0)
    is_abstract = (idx == 1)
    is_keywords = (idx == 2)
    is_section_header = idx in {3, 7, 12, 15, 20, 24}
    is_subsection = any(text.startswith(f'{i}.') for i in range(1,6))
    is_references = (idx == 26)
    is_conclusion_body = (idx == 25)
    
    if is_title:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            set_run_font(run, '宋体', 14, bold=True)
        set_line_spacing(p, 22)
        pf = p.paragraph_format
        pf.space_before = Pt(6)
        pf.space_after = Pt(6)
        
    elif is_section_header:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            set_run_font(run, '宋体', 14, bold=True)
        set_line_spacing(p, 22)
        pf = p.paragraph_format
        pf.space_before = Pt(6)
        pf.space_after = Pt(3)
        
    elif is_subsection:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            set_run_font(run, '宋体', 12, bold=True)
        set_line_spacing(p, 22)
        pf = p.paragraph_format
        pf.space_before = Pt(3)
        pf.space_after = Pt(2)
        
    elif is_abstract or is_keywords:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in p.runs:
            set_run_font(run, '宋体', 10.5)
        set_line_spacing(p, 22)
        
    elif is_references:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            set_run_font(run, '宋体', 9)
        set_line_spacing(p, 22)
        
    elif is_conclusion_body:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in p.runs:
            set_run_font(run, '宋体', 12)
        set_line_spacing(p, 22)
        set_first_line_indent(p, 2, 12)
        
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        for run in p.runs:
            set_run_font(run, '宋体', 12)
        set_line_spacing(p, 22)
        set_first_line_indent(p, 2, 12)

# Save to temp then copy
import shutil, os
tmp = '12_OPSA_new.docx'
doc.save(tmp)

# Close the doc
doc = None

# Replace original via shell
os.system(f'copy /Y "{tmp}" "12_OPSA.docx" >nul 2>&1')
os.system(f'del "{tmp}" >nul 2>&1')

print('✅ 12_OPSA.docx reformatted successfully!')

# Verify
doc2 = Document('12_OPSA.docx')
print(f'\n--- Verification ---')
for i, p in enumerate(doc2.paragraphs):
    if not p.text.strip():
        continue
    r = p.runs[0] if p.runs else None
    if r:
        pf = p.paragraph_format
        print(f'[{i:2d}] font={r.font.name} sz={r.font.size} bold={r.font.bold} spacing={pf.line_spacing} rule={pf.line_spacing_rule} indent={pf.first_line_indent}')
