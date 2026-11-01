# -*- coding: utf-8 -*-
"""Multi-dimensional AI rate analysis for OPSA_CH.docx"""
import sys, io, re, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

doc = Document('OPSA_CH.docx')
text = '\n'.join([p.text for p in doc.paragraphs])

chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
sentences = [s.strip() for s in re.split(r'[。！？；]', text) if s.strip() and len(s.strip()) > 5]
paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

print('=' * 70)
print('OPSA_CH.docx 多维AI特征分析')
print('=' * 70)

# 1. Transition word density
print('\n【1. 过渡词密度】')
trans_words = {
    '序列/顺序': ['首先','其次','最后','第一','第二','第三','一是','二是','三是'],
    '递进/补充': ['此外','另外','不仅如此','不仅','而且','并且','甚至','进一步'],
    '转折/对比': ['然而','但是','可是','不过','相比之下','相反','反之','虽然','尽管'],
    '因果/推论': ['因此','所以','因而','从而','由此','据此'],
    '总结': ['综上所述','总之','总而言之','总的来说','总体而言','简而言之','综上'],
    '解释/说明': ['具体而言','换言之','换句话说','也就是说','这意味着','举例来说'],
    '强调': ['值得注意的是','需要指出的是','特别是','尤其是'],
    '并列': ['同时','与此同时','一方面','另一方面'],
    '条件': ['如果','假如','一旦','那么','无论'],
    '承接': ['随后','接着','继而','此后','接下来'],
}
total_all = 0
for cat, words in trans_words.items():
    cat_total = 0
    for w in words:
        c = len(re.findall(w, text))
        if c > 0:
            cat_total += c
    if cat_total > 0:
        print('  %s: %d次' % (cat, cat_total))
        total_all += cat_total
print('  --- 过渡词总计: %d次 ---' % total_all)
print('  每千字密度: %.1f次/千字' % (total_all/(chinese_chars/1000)))
print('  >>> 人类学术论文平均约5-15次/千字')

# 2. Sentence starter diversity
print('\n【2. 句子开头多样性分析】')
starters_count = {}
for s in sentences:
    first5 = s.strip()[:5]
    starters_count[first5] = starters_count.get(first5, 0) + 1

repeated = {k:v for k,v in sorted(starters_count.items(), key=lambda x:-x[1]) if v >= 3}
print('  共%d个句子，%d种不同开头' % (len(sentences), len(starters_count)))
print('  高频重复开头(>=3次):')
for k,v in repeated.items():
    print('    "%s...": %d次' % (k, v))
top3_values = sorted(starters_count.values(), reverse=True)[:3]
top3_total = sum(top3_values)
print('  前3种开头占总句子: %d/%d = %d%%' % (top3_total, len(sentences), top3_total*100//len(sentences)))
print('  >>> 人类写作前3种开头通常占比<15%')

# 3. Paragraph structural pattern
print('\n【3. 段落结构模式化程度】')
opsa_ending = 0
for p in doc.paragraphs:
    t = p.text.strip()
    if len(t) > 50 and 'OPSA' in t[-60:]:
        opsa_ending += 1
print('  以OPSA收尾的长段落: %d段' % opsa_ending)

subsec_count = 0
for p in doc.paragraphs:
    t = p.text.strip()
    if re.match(r'^\d+\.\d+\s', t):
        subsec_count += 1
print('  子章节数: %d个' % subsec_count)

pattern_paras = 0
for p in doc.paragraphs:
    t = p.text.strip()
    if len(t) > 100:
        has_def = any(kw in t for kw in ['是','指','定义为','即','表示','指一种'])
        has_opsa = 'OPSA' in t
        if has_def and has_opsa:
            pattern_paras += 1
print('  含"定义+OPSA"模式的段落: %d段' % pattern_paras)
print('  >>> AI写作常在每个段落都回归到中心主题')

# 4. Sentence length uniformity
print('\n【4. 句长均匀度（缺乏起伏）】')
sent_lens = [len(s) for s in sentences if len(s) < 500]
if sent_lens:
    avg = sum(sent_lens)/len(sent_lens)
    variance = sum((l-avg)**2 for l in sent_lens)/len(sent_lens)
    std = math.sqrt(variance)
    short = sum(1 for l in sent_lens if l < 30)
    medium = sum(1 for l in sent_lens if 30 <= l < 80)
    long = sum(1 for l in sent_lens if l >= 80)
    print('  平均句长: %d字' % avg)
    print('  标准差: %d' % std)
    print('  变异系数(CV): %.2f' % (std/avg))
    print('  短句(<30字): %d句 (%d%%)' % (short, short*100//len(sent_lens)))
    print('  中句(30-80字): %d句 (%d%%)' % (medium, medium*100//len(sent_lens)))
    print('  长句(>=80字): %d句 (%d%%)' % (long, long*100//len(sent_lens)))
    print('  >>> 人类写作短句占比通常>20%，有自然起伏')

# 5. Content originality
print('\n【5. 内容原创性与批判性】')
personal = 0
for p in doc.paragraphs:
    t = p.text
    for kw in ['笔者认为','个人认为','在我看来','我注意到','我的理解','本课程','课堂上','课程作业']:
        if kw in t:
            personal += 1
            break
print('  个人观点/课程关联段落: %d段 (%.1f%%)' % (personal, personal*100/len(paragraphs)))

critical = 0
for p in doc.paragraphs:
    t = p.text
    if 'OPSA' in t:
        for kw in ['不足','局限','缺点','问题','挑战','争议','值得商榷','有待改进','弱点','瓶颈','依赖','假设']:
            if kw in t:
                critical += 1
                break
print('  对OPSA的批判性(含假设/局限)段落: %d段' % critical)
print('  >>> 人类论文通常有10-20%的批判性内容')

# 6. Citation pattern
print('\n【6. 引用模式】')
refs = re.findall(r'\[\d+\]', text)
ref_positions = [i for i,p in enumerate(doc.paragraphs) if re.findall(r'\[\d+\]', p.text)]
print('  总引用次数: %d' % len(refs))
print('  含引用的段落: %d段' % len(ref_positions))

# 7. Punctuation
print('\n【7. 标点符号使用】')
print('  逗号: %d次' % text.count('，'))
print('  句号: %d次' % text.count('。'))
print('  分号: %d次' % text.count('；'))
print('  冒号: %d次' % text.count('：'))
print('  感叹号: %d次' % text.count('！'))
print('  问号: %d次' % text.count('？'))
ratio = text.count('。') / max(text.count('，'), 1)
print('  句号/逗号比: %.2f (人类通常1:3到1:5)' % ratio)

# 8. Language style uniformity
print('\n【8. 语言风格一致性】')
informal = 0
for p in doc.paragraphs:
    for kw in ['说白了','简单说','就是说','其实','说白了','真的','确实','显然']:
        if kw in p.text:
            informal += 1
            break
print('  口语化表达: %d处 (越少越像AI)' % informal)
print('  >>> AI文本几乎无口语化表达')

# ==================== SUMMARY ====================
print('\n' + '=' * 70)
print('【综合AI率评分矩阵】')
print('=' * 70)

scores = {}
# 1
density = total_all/(chinese_chars/1000)
if density > 20: scores['过渡词密集度'] = 9
elif density > 12: scores['过渡词密集度'] = 7
else: scores['过渡词密集度'] = 5

# 2
if top3_total/len(sentences) > 0.15: scores['句子开头重复'] = 8
else: scores['句子开头重复'] = 5

# 3
if pattern_paras > subsec_count * 0.5: scores['段落结构模式化'] = 8
else: scores['段落结构模式化'] = 6

# 4
cv = std/avg if avg > 0 else 0
if cv < 0.3: scores['句长变化不足(低起伏)'] = 8
elif cv < 0.5: scores['句长变化不足(低起伏)'] = 6
else: scores['句长变化不足(低起伏)'] = 4

# 5
if personal < 3: scores['缺乏原创性'] = 8
else: scores['缺乏原创性'] = 5

# 6
if informal < 2: scores['风格过于统一(缺变化)'] = 8
else: scores['风格过于统一(缺变化)'] = 5

for k, v in scores.items():
    bar = '█' * v + '░' * (10-v)
    print('  %s: %d/10 %s' % (k, v, bar))
avg_score = sum(scores.values()) / len(scores)
print('\n  综合评分: %.1f/10' % avg_score)
if avg_score >= 7:
    print('  评估: 高AI概率 (约70-85%)')
elif avg_score >= 5:
    print('  评估: 中等AI概率 (约50-70%)')
else:
    print('  评估: 较低AI概率 (<50%)')

print('\n' + '=' * 70)
print('【改进建议优先级】')
print('=' * 70)
suggestions = [
    ('最高优先', [
        '1. 减少"同时"等过渡词密度 (当前%.1f次/千字，目标<12)' % density,
        '2. 增加短句比例 (当前%d%%，目标>20%%)' % (short*100//len(sent_lens)),
        '3. 增加句子开头多样性 (当前前3种占%d%%，目标<15%%)' % (top3_total*100//len(sentences)),
    ]),
    ('高优先', [
        '4. 增加对OPSA的批判性分析 (当前仅%d段含批判性内容)' % critical,
        '5. 打散段落模式，减少"定义→OPSA"的固定套路',
    ]),
    ('中优先', [
        '6. 增加口语化或个人化表达 (当前%d处)' % informal,
        '7. 调整标点使用, 丰富句式变化',
    ]),
]
for level, items in suggestions:
    print('  [%s]' % level)
    for item in items:
        print('    %s' % item)
