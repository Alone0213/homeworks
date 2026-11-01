# -*- coding: utf-8 -*-
"""
Step 1: Extract all transition words from the paper
Step 2: Remove them carefully (multi-character transitions only for safety)
Step 3: Output cleaned Chinese
"""
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('OPSA论文_完整版.md', 'r', encoding='utf-8') as f:
    text = f.read()

# =========================================================
# 1. Define comprehensive Chinese transition word list
# Only multi-character (>=3 chars) or clearly safe 2-char words
# =========================================================
transition_categories = {
    "序列/顺序": [
        '首先', '其次', '然后', '最后',
        '第一', '第二', '第三', '第四', '第五',
        '一是', '二是', '三是',
    ],
    "递进/补充": [
        '此外', '另外', '除此之外', '不仅如此',
        '不仅', '而且', '并且', '甚至', '乃至',
        '更有', '进一步',
    ],
    "转折/对比": [
        '然而', '但是', '可是', '不过',
        '相比之下', '相较之下', '相较于',
        '相反', '反之', '反过来', '另一方面',
        '虽然', '尽管', '固然',
    ],
    "因果/推论": [
        '因此', '所以', '因而', '故而', '为此', '于是',
        '正因如此', '之所以',
        '从而', '由此', '据此', '故此',
    ],
    "总结/归纳": [
        '综上所述', '总之', '总而言之', '总的来说', '总体而言',
        '归根结底', '简而言之', '简言之', '概括而言', '综上',
    ],
    "解释/说明": [
        '具体而言', '具体来说', '具体地说',
        '换言之', '换句话说', '也就是说',
        '这意味着', '举例来说',
    ],
    "强调/突出": [
        '值得注意的是', '需要指出的是', '值得强调的是',
        '特别是', '尤其是',
        '重要的是', '关键的是',
    ],
    "并列": [
        '同时', '与此同时',
        '一方面', '另一方面',
    ],
    "条件/假设": [
        '如果', '假如', '倘若', '一旦',
        '那么', '无论', '不论', '不管',
    ],
    "时间/承接": [
        '随后', '接着', '继而', '而后',
        '此前', '此后', '之后',
        '接下来', '起初', '最初',
    ],
    "视角/范围": [
        '本质上', '根本上', '实质上',
        '从更宏观的角度来看',
        '从更广阔的视角来看',
        '从课程学习的角度',
    ],
    "过渡/重申": [
        '基于此', '在此基础上',
        '如前所述', '如上所述',
        '整体而言',
    ],
    "举例/引用": [
        '例如', '比如', '譬如',
    ],
}

all_transitions = []
for cat, words in transition_categories.items():
    for w in words:
        all_transitions.append((w, cat))

# Sort by length descending to match longer phrases first
all_transitions.sort(key=lambda x: -len(x[0]))

# =========================================================
# 2. Identify all transition words in the text
# =========================================================
found_transitions = {}
for word, cat in all_transitions:
    count = len(re.findall(re.escape(word), text))
    if count > 0:
        found_transitions[word] = {'count': count, 'category': cat}

print("=" * 70)
print("【筛选出的所有转接词 (Transition Words Found)】")
print("=" * 70)

by_category = {}
for word, info in found_transitions.items():
    cat = info['category']
    if cat not in by_category:
        by_category[cat] = []
    by_category[cat].append((word, info['count']))

total_found = 0
for cat in by_category:
    print(f"\n  [{cat}]")
    for word, count in sorted(by_category[cat], key=lambda x: -x[1]):
        print(f"    「{word}」: {count}次")
        total_found += count

print(f"\n  --- 总计: {len(found_transitions)}种转接词, 共 {total_found}次出现 ---")

# =========================================================
# 3. Remove transition words from the text
# =========================================================

def remove_transitions(text, transition_words):
    """Remove transition words from text, being careful about word boundaries"""
    cleaned = text
    # Sort by length descending so longer phrases are matched first
    sorted_words = sorted(transition_words, key=lambda x: -len(x))
    
    for word in sorted_words:
        # Only remove when the word appears as a standalone transition word:
        # - to avoid removing "第一" from "第一个", we check that the word is
        #   NOT preceded by another Chinese character (would be part of word)
        # - followed by punctuation or end-of-string
        # - OR preceded by start-of-string/punctuation/whitespace
        escaped = re.escape(word[0])
        if len(word) > 1:
            rest = re.escape(word[1:])
        else:
            rest = ''
        
        # Pattern: word must be followed by punctuation/whitespace/end
        # and NOT be part of a longer word
        # Use simpler approach: match word only when followed by punctuation
        pattern = re.escape(word) + r'(?=[，。；：、！？\n\r\s]|$)'
        cleaned = re.sub(pattern, '', cleaned)
    
    # Clean up:
    # 1. Remove extra spaces
    cleaned = re.sub(r'  +', ' ', cleaned)
    # 2. Remove extra blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    # 3. Fix: "。，" -> "。" (period followed by comma)
    cleaned = re.sub(r'。[，、]', '。', cleaned)
    # 4. Fix: "：，" -> "：" 
    cleaned = re.sub(r'：[，、]', '：', cleaned)
    # 5. Fix: "，。" -> "。"
    cleaned = re.sub(r'[，、]。', '。', cleaned)
    # 6. Fix doubled punctuation
    cleaned = re.sub(r'[，、]{2,}', '，', cleaned)
    cleaned = re.sub(r'，[，、]', '，', cleaned)
    # 7. Remove leading comma at start of paragraph
    cleaned = re.sub(r'\n，', '\n', cleaned)
    # 8. Fix "？，" -> "？"
    cleaned = re.sub(r'？，', '？', cleaned)
    # 9. Fix trailing "的" that lost its object
    cleaned = re.sub(r'的[，。；：]', '。', cleaned)
    
    return cleaned

transition_words_only = [t[0] for t in all_transitions]
cleaned_text = remove_transitions(text, transition_words_only)

with open('OPSA论文_清洗版.md', 'w', encoding='utf-8') as f:
    f.write(cleaned_text)

print(f"\n\n{'=' * 70}")
print("【清洗完成】已保存至 OPSA论文_清洗版.md")
print(f"{'=' * 70}")

# =========================================================
# 4. Show sample diff
# =========================================================
print(f"\n{'=' * 70}")
print("【清洗示例对比 (前5个有变化的段落)】")
print(f"{'=' * 70}")

orig_lines = text.split('\n')
clean_lines = cleaned_text.split('\n')

changes_shown = 0
for i, (ol, cl) in enumerate(zip(orig_lines, clean_lines)):
    if ol != cl and len(ol.strip()) > 30 and changes_shown < 5:
        print(f"\n原文:  {ol.strip()}")
        print(f"清洗后: {cl.strip()}")
        print()
        changes_shown += 1

# Show transition word occurrences with context
print(f"\n{'=' * 70}")
print("【转接词上下文示例】")
print(f"{'=' * 70}")
for word, info in sorted(found_transitions.items(), key=lambda x: -x[1]['count']):
    if info['count'] >= 3:
        # Find first occurrence with context
        idx = text.find(word)
        if idx >= 0:
            start = max(0, idx - 15)
            end = min(len(text), idx + len(word) + 20)
            ctx = text[start:end].replace('\n', ' ')
            print(f"  「{word}」({info['count']}次): ...{ctx}...")
