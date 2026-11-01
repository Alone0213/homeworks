import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation

path = r'F:\code\homeworks\password\12 OPSA .pptx'
prs = Presentation(path)

lines = []
lines.append(f'幻灯片数量: {len(prs.slides)}')
lines.append('=' * 60)

for i, slide in enumerate(prs.slides):
    lines.append(f'\n--- 第 {i+1} 页 ---')
    if slide.slide_layout:
        lines.append(f'布局: {slide.slide_layout.name}')
    
    img_count = 0
    for shape in slide.shapes:
        if shape.shape_type == 13:
            img_count += 1
    
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                txt = para.text.strip()
                if txt:
                    txt_clean = txt.replace('\u200b', '')
                    lines.append(f'  {txt_clean}')
        if shape.has_table:
            table = shape.table
            for row in table.rows:
                cells = [cell.text.strip().replace('\u200b', '') for cell in row.cells]
                lines.append(f'  | {" | ".join(cells)} |')
    
    if img_count > 0:
        lines.append(f'  [本页包含 {img_count} 张图片]')
    lines.append('')

result = '\n'.join(lines)
with open(r'F:\code\homeworks\password\ppt_content.txt', 'w', encoding='utf-8') as f:
    f.write(result)
print(f'OK: {len(lines)} lines written')
