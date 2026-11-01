# -*- coding: utf-8 -*-
"""
Convert the English Markdown paper to a properly formatted DOCX document.
"""
import re
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# Read the English markdown
with open('OPSA论文_英文版.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Split into lines
lines = text.split('\n')

doc = Document()

# Set page margins (similar to A4 with standard margins)
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)

# Default font
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.line_spacing = Pt(22)
style.paragraph_format.space_after = Pt(0)
style.paragraph_format.space_before = Pt(0)

def add_title(doc, text):
    """Add the main title - centered, bold, 14pt"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    p.paragraph_format.line_spacing = Pt(24)
    p.paragraph_format.space_after = Pt(12)
    return p

def add_heading1(doc, text):
    """Add a section heading (##) - bold, 13pt"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    p.paragraph_format.line_spacing = Pt(24)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_heading2(doc, text):
    """Add a subsection heading (###) - bold, 12pt"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    p.paragraph_format.line_spacing = Pt(22)
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    return p

def add_body(doc, text):
    """Add a body paragraph - justified, 12pt, first line indent"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    p.paragraph_format.line_spacing = Pt(22)
    p.paragraph_format.first_line_indent = Cm(0.75)
    p.paragraph_format.space_after = Pt(2)
    return p

def add_body_no_indent(doc, text):
    """Add body text without first-line indent"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    p.paragraph_format.line_spacing = Pt(22)
    p.paragraph_format.space_after = Pt(2)
    return p

def add_bold_label_paragraph(doc, label, text):
    """Add a paragraph with a bold label followed by normal text"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run_label = p.add_run(label)
    run_label.font.name = 'Times New Roman'
    run_label.font.size = Pt(12)
    run_label.font.bold = True
    run_text = p.add_run(text)
    run_text.font.name = 'Times New Roman'
    run_text.font.size = Pt(12)
    p.paragraph_format.line_spacing = Pt(22)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_formatted_line(doc, line):
    """Handle a line that might have bold markers (**)"""
    parts = re.split(r'(\*\*.*?\*\*)', line)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.font.bold = True
        else:
            run = p.add_run(part)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
    p.paragraph_format.line_spacing = Pt(18)
    return p

def add_table_from_markdown(doc, lines, start_idx):
    """Convert markdown table to DOCX table"""
    table_lines = []
    i = start_idx
    while i < len(lines) and (lines[i].startswith('|') or lines[i].strip() == ''):
        if lines[i].startswith('|'):
            table_lines.append(lines[i])
        i += 1
    
    if len(table_lines) < 2:
        return i
    
    # Parse header
    header = [c.strip() for c in table_lines[0].split('|')[1:-1]]
    # Skip separator line (index 1)
    # Parse data rows
    data = []
    for line in table_lines[2:]:
        row = [c.strip() for c in line.split('|')[1:-1]]
        if row:
            data.append(row)
    
    if not data:
        return i
    
    rows = len(data) + 1  # +1 for header
    cols = len(header)
    
    table = doc.add_table(rows=rows, cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Style the table
    table.style = 'Table Grid'
    
    # Set header
    for j, h in enumerate(header):
        cell = table.rows[0].cells[j]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.bold = True
        # Shade header
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="D9E2F3"/>')
        cell._tc.get_or_add_tcPr().append(shading)
    
    # Set data rows
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.rows[i+1].cells[j]
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
    
    # Add spacing after table
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    return i

def add_code_block(doc, line):
    """Add a code/math line"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(line)
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    p.paragraph_format.line_spacing = Pt(18)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    return p

# ==========================================
# Process the markdown and build the DOCX
# ==========================================

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Skip empty lines
    if stripped == '':
        i += 1
        continue
    
    # Main title (#)
    if line.startswith('# ') and not line.startswith('## '):
        add_title(doc, stripped[2:])
        i += 1
        continue
    
    # Abstract and keywords
    if stripped.startswith('**Abstract:**'):
        text_content = stripped[len('**Abstract:**'):].strip()
        add_bold_label_paragraph(doc, 'Abstract: ', text_content)
        i += 1
        continue
    
    if stripped.startswith('**Keywords:**'):
        text_content = stripped[len('**Keywords:**'):].strip()
        add_bold_label_paragraph(doc, 'Keywords: ', text_content)
        i += 1
        continue
    
    # Section heading (##)
    if line.startswith('## ') and not line.startswith('### '):
        add_heading1(doc, stripped[3:])
        i += 1
        continue
    
    # Subsection heading (###)
    if line.startswith('### '):
        add_heading2(doc, stripped[4:])
        i += 1
        continue
    
    # Table
    if stripped.startswith('|') and i + 1 < len(lines) and lines[i+1].strip().startswith('|'):
        i = add_table_from_markdown(doc, lines, i)
        continue
    
    # Table caption
    if stripped.startswith('**Table '):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(stripped.strip('*'))
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.italic = True
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        i += 1
        continue
    
    # Math/code lines (containing formulas)
    if '=' in stripped and re.search(r'[θΣη∇μβ]', stripped):
        add_code_block(doc, stripped)
        i += 1
        continue
    
    # References section - handle reference lines
    if stripped.startswith('[') and re.match(r'\[\d+\]', stripped):
        # Check if next line is also a reference or empty
        add_body_no_indent(doc, stripped)
        i += 1
        continue
    
    # Regular body text - handle bold markers inside
    if '**' in stripped:
        add_formatted_line(doc, stripped)
    else:
        add_body(doc, stripped)
    
    i += 1

# Save
output_path = 'OPSA论文_英文版.docx'
doc.save(output_path)
print(f'Document saved to {output_path}')
print(f'Total paragraphs: {len(doc.paragraphs)}')
print(f'Total tables: {len(doc.tables)}')
