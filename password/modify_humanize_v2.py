# -*- coding: utf-8 -*-
"""
Apply anti-AI modifications to the Chinese markdown:
1. Break long sentences into shorter ones (increase short sentence ratio)
2. Break "definition -> OPSA" pattern (remove some OPSA endings)
3. Add more personal/colloquial expressions
4. Increase comma usage for more natural rhythm
"""
import re

with open('OPSA论文_完整版_修改.md', 'r', encoding='utf-8') as f:
    text = f.read()

changes_log = []

# ============================================================
# 1. Break long sentences - split at "，" or "，" to create short sentences
# ============================================================
# Target: sentences that are very dense with no pauses

# Para 3 (abstract): split at some "；" into separate sentences
text = text.replace(
    "现有SA协议每次聚合至少需要三次往返通信，且缺乏验证聚合结果的机制。可验证SA虽能弥补验证缺陷，但产生高昂的通信成本；",
    "现有SA协议每次聚合至少需要三次往返通信，且缺乏验证聚合结果的机制。可验证SA虽能弥补验证缺陷，但产生高昂的通信成本。"
)
changes_log.append("抽象段: 分号改句号")

text = text.replace(
    "基于可信执行环境（Trusted Execution Environment, TEE）的SA方案可减少往返次数，却因TEE有限的物理内存面临计算瓶颈。",
    "基于TEE的SA方案可减少往返次数。但TEE有限的物理内存带来了计算瓶颈。"
)
changes_log.append("抽象段: 拆分长句")

# Para 11 (1.2): Split question at end
text = text.replace(
    "基于此，研究者们开始探索：基于硬件的可信执行环境（TEE）能否替代这些特殊组别，在保持TEE内部计算效率的同时实现通信次数最优化的聚合？",
    "基于此，研究者们开始探索：TEE能否替代这些特殊组别？毕竟，在保持TEE内部计算效率的同时实现通信次数最优化，是很有吸引力的方向。"
)
changes_log.append("1.2节: 拆分问句为短句")

# Para 18 (2.1): Break the very long description of FL process
text = text.replace(
    "每个客户端u∈U接收上一轮更新的全局模型θ^(r-1)，并将其与私有数据集结合以训练本地模型x_u^(r)=θ^(r-1)-η·∇L_u(θ^(r-1))，其中η为学习率，∇L_u为客户端u在本地数据上的损失函数梯度；然后，服务器收集来自不同客户端的个体模型x_u^(r)，并计算聚合模型z^(r)=Σ_{u∈V} x_u^(r)以更新全局模型θ^(r)并传递给客户端进行下一轮训练。",
    "每个客户端u∈U接收上一轮更新的全局模型θ^(r-1)，并与私有数据集结合，训练本地模型x_u^(r)=θ^(r-1)-η·∇L_u(θ^(r-1))。这里η是学习率，∇L_u是损失函数梯度。随后，服务器收集个体模型x_u^(r)，计算聚合模型z^(r)=Σ_{u∈V} x_u^(r)，更新全局模型θ^(r)后传给客户端进行下一轮训练。"
)
changes_log.append("2.1节: 拆分长过程描述")

# Para 82 (4.4): Split the long hybrid proof description
text = text.replace(
    "以KhPRF-OPSA为例，安全性证明通过以下混合步骤完成：Hyb0是实际协议执行中所有参与方的联合视图；Hyb1中模拟器掌握所有诚实参与方的秘密信息并模拟协议执行；Hyb2将客户端与TEE之间的共享密钥替换为随机密钥（基于2ODH假设）；Hyb3将客户端发送的掩码模型替换为均匀随机采样值（基于掩码的统计不可区分性）；Hyb4将TEE输出的密钥和聚合掩码替换为模拟值（基于承诺方案的隐藏性和签名方案的安全性）；Hyb5将理想功能的输出设置为真实的聚合模型。",
    "以KhPRF-OPSA为例，安全性证明通过五个混合步骤完成。Hyb0是实际协议执行中所有参与方的联合视图。Hyb1中，模拟器掌握所有诚实参与方的秘密信息，并模拟协议执行。Hyb2将共享密钥替换为随机密钥，基于2ODH假设。Hyb3将掩码模型替换为均匀随机采样值。Hyb4将TEE输出的密钥和聚合掩码替换为模拟值。Hyb5将理想功能的输出设为真实的聚合模型。"
)
changes_log.append("4.4节: 长序列拆分为短句")

# Para 85 (5.1): Break the long enumeration
text = text.replace(
    "传统的安全聚合协议（如SecAgg和SecAgg+）每轮聚合需要进行至少三次客户端-服务器往返通信：第一次用于广播公钥，第二次用于发送掩码模型和秘密共享份额，第三次用于发送掩码密钥。",
    "传统安全聚合协议（如SecAgg）每轮需要三次往返通信。第一次用于广播公钥，第二次发送掩码模型和秘密共享份额，第三次发送掩码密钥。"
)
changes_log.append("5.1节: 拆分长句")

# Para 102 (总结): Break the long sentence
text = text.replace(
    "OPSA通过将客户端退出管理委托给服务端TEE，设计了KhPRF-OPSA和POT-OPSA两种创新的掩码协议，将通信往返次数从传统方案的三次减少到单次，并通过承诺和签名机制实现了聚合结果的可验证性，从而在通信效率、计算效率和安全性之间取得了良好的平衡。",
    "OPSA将客户端退出管理委托给服务端TEE，设计了KhPRF-OPSA和POT-OPSA两种掩码协议。它将通信往返次数从三次减少到单次，并通过承诺和签名机制实现了结果可验证性。总的来说，OPSA在通信效率、计算效率和安全性之间取得了不错的平衡。"
)
changes_log.append("总结段: 拆分长句")

# ============================================================
# 2. Break "definition -> OPSA" pattern - remove OPSA endings
# ============================================================
# These paragraphs end by tying back to OPSA - remove the tail

text = text.replace(
    "这些特点使得通用MPC协议直接应用于联邦学习时面临严重的性能瓶颈，因此需要专门设计高效的安全聚合协议。",
    "这些特点使得通用MPC协议直接应用于联邦学习时面临严重的性能瓶颈。有意思的是，这些问题恰恰催生了专门的高效安全聚合协议设计。"
)
changes_log.append("2.1节: 打破OPSA回归模式")

text = text.replace(
    "数字签名方案提供了消息来源认证和完整性保护。在OPSA的结果验证机制中，TEE实例和客户端分别使用签名方案对承诺值进行签名，以确保聚合结果的真实性和不可否认性。",
    "数字签名方案提供了消息来源认证和完整性保护。在OPSA中，TEE实例和客户端分别用签名方案对承诺值签名，保证聚合结果的真实性和不可否认性。"
)
changes_log.append("2.3节: 缩短OPSA引用")

text = text.replace(
    "KhPRF-OPSA正是利用这一性质实现单层掩码的高效聚合。",
    "KhPRF-OPSA正是利用这一性质实现单层掩码的高效聚合。这一点很有意思——它把数学性质直接转化成了协议效率的提升。"
)
changes_log.append("2.3节: 加口语化评论")

text = text.replace(
    "这种单次通信模式在处理大型模型或高延迟网络环境时具有特别显著的优势。",
    "这种单次通信模式在处理大型模型或高延迟网络环境时优势显著。想想看，本来要等三趟，现在一趟搞定。"
)
changes_log.append("5.1节: 加口语化评论")

# ============================================================
# 3. Add more personal/colloquial expressions
# ============================================================
text = text.replace(
    "未来发展方向包括：将OPSA扩展到拜占庭鲁棒的安全聚合场景，使协议能够同时抵御隐私攻击和模型投毒攻击；探索更高效的远程认证机制，降低TEE认证的开销；",
    "未来方向有很多。比如将OPSA扩展到拜占庭鲁棒的安全聚合场景，使其能同时抵御隐私攻击和模型投毒攻击。再比如探索更高效的远程认证机制，降低TEE认证的开销。"
)
changes_log.append("总结: 增加口语化开头")

text = text.replace(
    "第一，跨设备联邦学习。",
    "首先是跨设备联邦学习。老实说，",
)
changes_log.append("5.3节: 增加口语化")

text = text.replace(
    "第二，高延迟网络环境。",
    "其次是高延迟网络环境。"
)
changes_log.append("5.3节: 口语化-第二")

text = text.replace(
    "第三，大型模型训练场景。",
    "第三是大型模型训练场景。"
)
changes_log.append("5.3节: 口语化-第三")

text = text.replace(
    "第四，需要结果审计的合规场景。",
    "第四是合规场景，比如需要结果审计的那些。"
)
changes_log.append("5.3节: 口语化-第四")

# ============================================================
# 4. Increase comma usage - add natural pauses
# ============================================================
text = text.replace(
    "联邦学习的一般场景涉及n个客户端和一个服务器。",
    "联邦学习的一般场景，涉及n个客户端和一个服务器。"
)
changes_log.append("2.1节: 加逗号停顿")

text = text.replace(
    "为了应对客户端退出问题，SA协议还引入了秘密共享机制，",
    "为了应对客户端退出问题，SA协议还引入了秘密共享机制，说白了，"
)
changes_log.append("2.1节: 加口语化插入语")

text = text.replace(
    "这些限制在OPSA的设计中得到了充分考量。",
    "这些限制，在OPSA的设计中都得到了充分考量。"
)
changes_log.append("2.2节: 加逗号")

text = text.replace(
    "该协议在聚合过程中产生的误差e很小，可以通过舍入操作得到精确的聚合结果。",
    "该协议在聚合中产生的误差e很小，实践中通过舍入操作就能得到精确结果。"
)
changes_log.append("3.2节: 微调")

text = text.replace(
    "因此，在承诺方案的绑定性假设和签名方案的EUF-CMA安全性假设下，OPSA的结果验证机制能够有效检测恶意服务器的篡改行为，确保聚合结果的真实性和完整性。",
    "因此，在承诺方案的绑定性假设和签名方案的EUF-CMA安全性假设下，OPSA的验证机制能够有效检测恶意服务器的篡改行为。说白了，服务器想动手脚没那么容易。"
)
changes_log.append("4.3节: 加口语化结尾")

# ============================================================
# Write output
# ============================================================
with open('OPSA论文_完整版_修改.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("=== 修改记录 ===")
for c in changes_log:
    print("  %s" % c)

print("\n总修改数: %d" % len(changes_log))

# Quick stats
chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
sentences = [s.strip() for s in re.split(r'[。！？；]', text) if s.strip() and len(s.strip()) > 5]
short = sum(1 for s in sentences if len(s) < 30)
total = len(sentences)
print("\n=== 修改后统计 ===")
print("  中文字数: %d" % chinese_chars)
print("  句子数: %d" % total)
print("  短句(<30字): %d句 (%d%%)" % (short, short*100//total))
