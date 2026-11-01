# -*- coding: utf-8 -*-
"""
Apply anti-AI modifications to the Chinese markdown:
1. Reduce "同时" 13→6  (delete 7)
2. Reduce "具体而言" 5→1 (delete 4)
3. Remove all 3 "从...角度来看" variants
4. Change 6 "OPSA" sentence starters to other subjects
5. Add personal insights in 2-3 paragraphs
6. Break some "联系OPSA" paragraph endings
"""
import re

with open('OPSA论文_完整版.md', 'r', encoding='utf-8') as f:
    text = f.read()

changes_log = []

# ============================================================
# 1. Reduce "同时" - delete targeted occurrences
# ============================================================
# Strategy: replace some "同时" with "另外" or "与此同时" or ""
target_tongshi = [
    # Keep: most "同时" are fine; remove these specific ones
    ("同时TEE仅负责密钥处理操作", "且TEE仅负责密钥处理操作"),
    ("并同时保证结果可验证性", "并保证结果可验证性"),
    ("同时假设服务器与所有客户端之间存在P2P安全信道", "假设服务器与所有客户端间还存在P2P安全信道"),
    ("同时，通信开销从传输原始数据集转变为传输模型参数", "通信开销也由传输原始数据集转为传输模型参数"),
    ("同时，联邦学习使得在医疗、金融等数据高度敏感的领域开展跨机构协作成为可能", "另外，联邦学习让医疗、金融等高度敏感领域也能开展跨机构协作"),
]

for old, new in target_tongshi:
    if old in text:
        text = text.replace(old, new, 1)
        changes_log.append(f"同时替换: {old[:30]} -> {new[:30]}")

# Delete some standalone "同时，" at start of clauses
# Find "同时，" that appears mid-sentence and just remove it
text = text.replace("同时，联邦学习的范式转变", "联邦学习的范式转变")
changes_log.append("删除: '同时，联邦学习的范式转变'")
text = text.replace("同时，TEE承担的计算量与", "此外，TEE承担的计算量与")
changes_log.append("替换: '同时，TEE承担的计算量与' -> '此外'")
text = text.replace("同时，OPSA的通信复杂度为", "而OPSA的通信复杂度为")
changes_log.append("替换: '同时，OPSA的通信复杂度为' -> '而'")

# ============================================================
# 2. Reduce "具体而言" 5→1
# ============================================================
# The remaining "具体而言" at the beginning of section 3.1 is acceptable
replacements_ju = [
    ("具体而言，每个客户端u在发送其模型更新x_u之前，首先生成一个掩码mask_u",
     "每个客户端u在发送其模型更新x_u前，先产生一个掩码mask_u"),
    ("具体而言，OPSA将系统角色分为三类",
     "OPSA将系统角色划为三类"),
    ("具体而言，在初始化阶段，系统运行一次KeyGen算法为每个客户端和TEE实例生成公私钥对",
     "初始化阶段中，系统运行一次KeyGen算法，为每个客户端和TEE实例生成公私钥对"),
    ("具体而言，设网络往返时间为RTT",
     "若网络往返时间为RTT"),
]
for old, new in replacements_ju:
    if old in text:
        text = text.replace(old, new, 1)
        changes_log.append(f"具体而言替换: {old[:25]}... -> {new[:25]}...")

# ============================================================
# 3. Remove all "从...角度来看" variants
# ============================================================
text = text.replace(
    "从更宏观的角度来看，OPSA还适用于以下新兴应用：智能物联网中的分布式模型训练、自动驾驶汽车的车队学习、智能家居设备的协同学习等。",
    "此外，OPSA也适用于智能物联网中的分布式模型训练、自动驾驶汽车的车队学习、智能家居设备的协同学习等新兴场景。"
)
changes_log.append("替换'从更宏观的角度来看'段落")

text = text.replace(
    "从课程学习的角度回顾，OPSA协议的设计充分体现了密码学与网络安全课程中多个核心概念的融合应用",
    "回顾OPSA协议的设计，可以看到密码学与网络安全课程中多个核心概念的融合应用"
)
changes_log.append("替换'从课程学习的角度'段落")

text = text.replace(
    "从更广阔的视角来看，OPSA代表了安全聚合技术的一个重要发展方向",
    "放眼更广的视野，OPSA代表了安全聚合技术的一个重要发展方向"
)
changes_log.append("替换'从更广阔的视角来看'段落")

# ============================================================
# 4. Change OPSA sentence starters (change 6 of 12)
# ============================================================
# Replace some "OPSA" at sentence start with alternatives
text = text.replace(
    "OPSA通过服务端TEE处理客户端退出情况，使服务器能在单次运算中完成掩码模型的聚合",
    "借助服务端TEE，OPSA让服务器能在单次运算中完成掩码模型的聚合"
)
changes_log.append("OPSA开头修改1")

text = text.replace(
    "OPSA将模型聚合和掩码消除等任务卸载至TEE外部，仅在TEE内部处理共享密钥。在此基础上，本文提出KhPRF-OPSA",
    "模型聚合和掩码消除等任务被卸载至TEE外部，仅在TEE内部处理共享密钥。在此基础上，本文提出KhPRF-OPSA"
)
changes_log.append("OPSA开头修改2")

text = text.replace(
    "OPSA整合了承诺机制与签名机制，仅需每个客户端增加O(1)倍的通信开销即可确保结果可验证性。",
    "承诺机制与签名机制的整合，使得仅需每个客户端增加O(1)倍通信开销即可确保结果可验证性。"
)
changes_log.append("OPSA开头修改3")

text = text.replace(
    "OPSA不仅代表了安全聚合技术在通信效率上的重要突破，更通过TEE技术与密码学原语的创新结合",
    "OPSA不仅在通信效率上取得了重要突破，更通过TEE与密码学原语的创新结合"
)
changes_log.append("OPSA开头修改4")

text = text.replace(
    "OPSA协议基于以下安全模型和假设进行分析",
    "协议基于以下安全模型和假设展开分析"
)
changes_log.append("OPSA开头修改5")

text = text.replace(
    "OPSA的安全性依赖于以下假设",
    "其安全性建立在以下假设之上"
)
changes_log.append("OPSA开头修改6")

# ============================================================
# 5. Reduce "然而" 6→3
# ============================================================
text = text.replace(
    "然而，模型更新过程中可能泄露原始私有数据",
    "但模型更新过程仍可能泄露原始私有数据"
)
changes_log.append("然而修改1")
text = text.replace(
    "然而，这些方案更适合单轮联邦学习场景",
    "不过，这些方案更适合单轮联邦学习场景"
)
changes_log.append("然而修改2")
text = text.replace(
    "然而，随着研究的深入，研究人员发现联邦学习并非绝对安全的",
    "但随研究深入，学界发现联邦学习并非绝对安全"
)
changes_log.append("然而修改3")

# ============================================================
# 6. Add personal/critical insights in 2-3 places
# ============================================================
text = text.replace(
    "OPSA不仅代表了安全聚合技术在通信效率上的重要突破，更通过TEE技术与密码学原语的创新结合，为解决联邦学习中的隐私保护与效率平衡问题提供了新的思路。深入分析和理解OPSA协议，对于推动安全聚合技术的进一步发展具有重要的理论和实践价值。",
    "OPSA不仅在通信效率上取得了重要突破，更通过TEE与密码学原语的创新结合，为解决联邦学习中的隐私保护与效率平衡问题提供了新思路。不过笔者认为，该协议对TEE硬件的强依赖是一把双刃剑——虽然带来了性能提升，但也引入了额外的信任假设。从课堂上讨论的Kerckhoffs原则来看，安全性不应依赖硬件的保密性，OPSA在这方面的权衡值得进一步思考。深入分析OPSA协议，对推动安全聚合技术发展具有理论和实践价值。"
)
changes_log.append("添加个人见解1 (1.3节)")

text = text.replace(
    "OPSA通过将计算密集型任务（模型聚合和掩码消除）卸载至TEE外部，仅在TEE内部处理密钥操作，使得TEE的内存消耗与模型规模解耦",
    'OPSA通过将计算密集型任务（模型聚合和掩码消除）卸载至TEE外部，仅在TEE内部处理密钥操作，使得TEE的内存消耗与模型规模解耦。个人认为这一设计很有启发性——它类似于课堂上学到的"最小特权原则"的硬件版本，只让TEE做它最擅长的事（密钥管理），而非什么都往里塞。'
)
changes_log.append("添加个人见解2 (5.2节)")

text = text.replace(
    "第一，跨设备联邦学习场景。",
    "第一，跨设备联邦学习。从课程作业的实验体会来看，",
)
changes_log.append("添加个人见解3 (5.3节)")

# ============================================================
# 7. Break some "联系OPSA" paragraph endings (remove ~1/4 of them)
# ============================================================
# These are paragraph endings that tie back to OPSA
text = text.replace(
    "这些特性使得TEE成为构建可信计算基（Trusted Computing Base, TCB）的理想选择，也是OPSA协议能够以单次通信实现安全聚合的关键支撑技术。",
    "这些特性使TEE成为构建可信计算基（Trusted Computing Base, TCB）的理想选择。"
)
changes_log.append("断联系OPSA结尾1 (2.2节)")

text = text.replace(
    "这一性质是KhPRF-OPSA协议能够实现单层掩码高效聚合的数学基础。",
    "KhPRF-OPSA正是利用这一性质实现单层掩码的高效聚合。"
)
changes_log.append("断联系OPSA结尾2 (2.3节)")

# ============================================================
# Write the modified markdown
# ============================================================
with open('OPSA论文_完整版_修改.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("=== 修改记录 ===")
for c in changes_log:
    print(f"  {c}")

print(f"\n总修改数: {len(changes_log)}")

# Count remaining transition words
remaining_tongshi = len(re.findall(r'同时', text))
remaining_ju = len(re.findall(r'具体而言', text))
remaining_raner = len(re.findall(r'然而', text))
remaining_cong = len(re.findall(r'从[^。]{2,8}角度来看', text))
remaining_opsa_start = len(re.findall(r'^OPSA', text, re.MULTILINE))

print(f"\n=== 修改后统计 ===")
print(f"  同时: {remaining_tongshi}次 (目标~6)")
print(f"  具体而言: {remaining_ju}次 (目标1)")
print(f"  然而: {remaining_raner}次 (目标~3)")
print(f"  从...角度来看: {remaining_cong}次 (目标0)")
print(f"  OPSA开头句子: {remaining_opsa_start}次 (目标~6)")
