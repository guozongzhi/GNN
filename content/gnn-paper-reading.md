# GNN：问题链演进、GCN / GAT 与 Transformer 深度精读讲稿

对应当前 **33页PPT**，核对于2026-11-16。全篇沿「痛点 / 问题 → 机制设计 → 局限暴露 → 下一代演进」的因果问题链展开，覆盖 6 大模块；不含Demo和跨论文性能排行榜。下文页码均指本地原始PDF的物理页，从文件首页起计。

## 阅读结构

| 页码 | 所属模块 | 需要回答的核心问题 |
| --- | --- | --- |
| 1–5 | 问题链与统一解剖台 | 哪些环环相扣的瓶颈推动演进，M / AGG / U 如何统一拆解各代模型？ |
| 6–13 | GCN 深读 | 如何从拉普拉斯谱滤波四步近似得到一跳传播，归一化怎样手算与训练？ |
| 14–20 | GAT 与 GATv2 深读 | 怎样按内容动态分配邻居权重，多头、静态排序限制与动态交互有何区别？ |
| 21–23 | 局部聚合判别与通信瓶颈 | Mean/Max/Sum 为何影响 1-WL 判别力，过挤压与过平滑如何不同？ |
| 24–29 | GNN 与 Transformer 深层对照 | Q/K/V 解耦、掩码开关、拓扑注入（Graphormer/GPS）与成本怎样权衡？ |
| 30–33 | 跨图复用前沿与选型决策 | 新节点与异构新图如何复用模型，如何按痛点落地选型与精读原文？ |

## 共同记号

A是邻接矩阵，I提供自身连接，D̃是A+I的度矩阵，S是GCN对称归一化传播算子。X是原始属性，H / h是隐藏表示，W / a是共享可学习参数，σ是逐通道激活。L=I−D^-1/2 A D^-1/2是对称归一化拉普拉斯，L̃=(2/λmax)L−I是缩放后的拉普拉斯，B=D^-1/2 A D^-1/2。

矩阵总式把节点放在行，因此写HW与HWQ；GAT单节点公式沿原文采用列向量，写zᵢ=Whᵢ。两种约定互为转置，不把同名矩阵直接混用。消息下标ij表示接收者i从发送者j接收；GAT的邻域Ñ(i)包含自身。

严格区分原论文的方法定义、理论保证和本稿教学推导/手算校验。近期跨图论文（GraphAny ICLR 2025、GraphPFN ICML 2026）以正式全文和官方会议记录交叉核对；未在本次独立复现论文性能。

## 01 · GNN：发展脉络、GCN与GAT、Transformer对照

本讲共33页，沿一条“痛点→机制→局限→演进”的因果问题链展开：从非规则图上的谱滤波与GCN局部归一化，到同度邻居的内容动态调权（GAT与GATv2），再到局部聚合的多重集判别盲区（GIN/1-WL）与远距过挤压瓶颈，继而引入Transformer全图直连与拓扑融合（Graphormer/GraphGPS），最后落脚跨图泛化前沿（GraphSAGE/GraphAny/GraphPFN）与工程选型决策。

正文不堆砌历史榜单分数或Demo命令；全部原始论文、来源链接与SHA-256见source/manifest.json。

## 02 · 核心问题链：五个环环相扣的瓶颈推动架构演进

与其按论文发表年份平铺直叙，不如从每代模型留下的具体瓶颈出发。痛点一：非规则图没有固定网格，谱卷积如何简化为实用的一跳传播（GCN）？痛点二：GCN 对同度邻居强制等权，如何按节点特征内容动态分配权重（GAT 与 GATv2）？痛点三：即使学会动态加权，纯局部聚合仍会在多重集上丢结构、在窄桥上发生过挤压（GIN 与 Bottleneck）。

痛点四：全局注意力打破局部路径限制，又如何补回图拓扑（Transformer、Graphormer、GraphGPS）？痛点五：新图维度与类别空间变化时，模型如何跨图复用（GraphSAGE、GraphAny、GraphPFN）？全篇围绕通信掩码、系数打分、内容变换三个正交轴展开对照。

**原文定位**：GCN §2；GAT §2；GIN §4；Transformer §3；GraphGPS §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[正式记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 03 · 图学习的起点：节点属性与拓扑关系如何共同决定表示

全篇固定使用一张三节点链图 A—B—C 作为核心解剖对象。节点特征 X 是可观测属性，例如分子中的原子类型或引文网中的文本向量；邻接关系 A 定义了允许谁向谁传递信息。单独观察中心节点 B 的属性 x(B) 往往不足以完成预测，必须结合邻居 A 和 C 的状态。与图像网格或文本序列不同，图的节点没有天然的“上下左右”或“前后”顺序：如果把节点 A、B、C 重新编号，实体本身并没有改变。

因此图模型必须满足重编号相容性：节点级输出随编号同步置换（置换等变），整图级输出保持不变（置换不变）。不同任务的输出头和标签必须独立于节点输入特征定义，不能把待预测标签直接当作特征输入。

**原文定位**：MPNN p3 式(1)–(3)；Zhou 综述 p3–4 §3。

- Gilmer et al.，Neural Message Passing for Quantum Chemistry，ICML（2017）。[正式记录](https://arxiv.org/abs/1704.01212) · [本地PDF](../source/papers/mpnn2017.pdf)

- Jie Zhou et al.，Graph Neural Networks: A Review of Methods and Applications，AI Open 1 (2020), 57–81; published 2021（2021）。[正式记录](https://arxiv.org/abs/1812.08434v6) · [本地PDF](../source/papers/zhou-survey2021.pdf)

## 04 · 统一解剖台：一次消息传递的三个基本算子（MPNN）

Gilmer 等人在 MPNN 框架中把绝大多数空间域图神经网络统一为三个按顺序执行的算子：消息生成函数 M、邻域聚合函数 AGG、状态更新函数 U。对中心节点 B 而言，首先沿允许的边生成来自邻居 A 和 C 的消息（可选带入边特征 e）；随后用顺序无关的聚合器 AGG 将数量可变的邻居消息集合压缩为固定维度向量 m(B)；最后由更新函数 U 融合中心旧状态 h(B) 与聚合摘要 m(B) 得到新状态 h′(B)。

所有节点同步读取上一层状态，保证计算与节点遍历顺序无关。这一框架为我们提供了一把统一手术刀：GCN 固定系数简化了 M，GAT 引入注意力改写了 M，GIN 则重点剖析 AGG 与 U 的单射条件。

**原文定位**：Gilmer et al. 2017，p3 式(1)–(3)。

- Gilmer et al.，Neural Message Passing for Quantum Chemistry，ICML（2017）。[正式记录](https://arxiv.org/abs/1704.01212) · [本地PDF](../source/papers/mpnn2017.pdf)

## 05 · 演进全景：关键论文各自改动了消息传递链的哪一步

这张全景表在 MPNN 解剖台上标出六代核心工作的演进逻辑，不再孤立地罗列模型。2009 年 Scarselli 迭代状态到固定点，而 2014–2016 年谱方法探索如何在无向图上用拉普拉斯多项式定义局部滤波；2017 年 GCN 将多项式极简为一阶重归一化算子 S 与共享线性层 W，但它把邻居权重锁死在度数结构上；2018–2022 年 GAT 与 GATv2 将混合系数改为节点特征驱动的动态注意力；2019–2021 年 GIN 与 Bottleneck 揭示纯局部聚合的 1-WL 判别上界与过挤压瓶颈；2021–2022 年图 Transformer 用全局注意力搭配结构编码或并行 MPNN 打通远程通信；2025–2026 年跨图基础模型进一步探索不重训适应新图特征与类别空间。

注意这是问题链阅读秩序，较新路线并非在所有任务替代 GCN 或 GAT。

**原文定位**：Scarselli §III；ChebNet §2；GCN §2；GAT §2；GIN §4；GraphGPS §3。

- Scarselli et al.，The Graph Neural Network Model，IEEE TNN（2009）。[正式记录](https://doi.org/10.1109/TNN.2008.2005605) · [本地PDF](../source/papers/scarselli2009.pdf)

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[正式记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[正式记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 06 · 痛点一：非规则图没有固定网格，怎样定义卷积与频率？

在图像等规则网格上，卷积靠固定大小的滑动窗口收集上下左右像素。但图上的节点邻居数量不定且无左右顺序，空间卷积核无处安放。Bruna 等人与 ChebNet 从谱域破题：虽然图没有统一方向，但可以用组合拉普拉斯二次型 xᵀ(D−A)x = Σ(xᵢ−xⱼ)² 衡量信号沿边变化的快慢。

相邻节点取相近值对应“低频平滑”，沿边正负剧烈交替对应“高频振荡”。把图信号 x 投影到拉普拉斯特征向量基 U 上（Uᵀx），在频率域乘以可学滤波器 gθ(Λ)，再逆变换 U gθ(Λ)Uᵀx 回到空间域，就定义了图卷积。然而直接做特征分解复杂度高达 O(N³)、滤波器非局部且换一张图特征基 U 就失效——这直接引出了 ChebNet 的多项式近似。

**原文定位**：Bruna 2014 §3；ChebNet 2016 p3 式(1)–(2)；信号为教学构造。

- Bruna et al.，Spectral Networks and Deep Locally Connected Networks on Graphs，ICLR（2014）。[正式记录](https://arxiv.org/abs/1312.6203) · [本地PDF](../source/papers/bruna2014.pdf)

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[正式记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

## 07 · ChebNet：用拉普拉斯低阶多项式实现免分解局部滤波

为绕开特征向量分解并让滤波器严格局部化，ChebNet 用缩放拉普拉斯 L̃ = (2/λmax)L − I 的 r 阶切比雪夫多项式近似频率响应 gθ(Λ)。关键代数洞察在于：U diag(pᵣ(Λ)) Uᵀ = pᵣ(UΛUᵀ) = pᵣ(L̃)，因此完全不需要计算特征向量 U，只需利用稀疏矩阵乘法递推 t₀=x、t₁=L̃x、tₖ=2L̃tₖ₋₁−tₖ₋₂，再用可学习系数 θₖ 线性组合即可。

因为 L̃ 仅在直接相邻节点及对角线非零，乘一次 L̃ 最多沿边走一跳，r 阶多项式在结构上严格只依赖于 r 跳以内的邻域。不过 ChebNet 每层仍需维护高阶多项式参数与逐图估计 λmax——Kipf & Welling 由此发问：能否把多项式截断到一阶，靠堆叠多层来获得多跳感受野？

**原文定位**：Defferrard et al. 2016，p3–4 式(3)–(5)；L̃ = (2/λmax)L − I。

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[正式记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

## 08 · GCN 的四步推导：从一阶近似到重归一化算子替换

记对称归一化拉普拉斯 L = I − D⁻¹ᐟ²AD⁻¹ᐟ²，并记 B = D⁻¹ᐟ²AD⁻¹ᐟ²。GCN 从 ChebNet 出发连续做出四步选择：第一步截断到一阶（r=1），单层仅处理自身与一跳邻居；第二步近似最大特征值 λmax ≈ 2，使 L̃ 简化为 L − I = −B，避免逐图求特征值；第三步绑定两个滤波系数 θ₀′ = −θ₁′ = θ，将双参数压缩为单参数 θ(I+B)x，限制过拟合但也绑定了自身与邻居权重；第四步最为关键：因为 I+B 的特征值落在 [0, 2]，多层连乘易发生数值爆炸或消失，作者直接用对 A+I 重新计算度矩阵的 S = D̃⁻¹ᐟ²(A+I)D̃⁻¹ᐟ² 替换 I+B。

在非负无向图上 S 的纯传播谱半径被压回 1。注意第四步是设计替换，不是代数恒等变换。

**原文定位**：ChebNet p3 式(3)–(4)；GCN p2–3 式(4)–(8)；第四步为算子替换。

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[正式记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 09 · GCN 核心公式拆解：跨节点传播 S 与跨通道变换 W

将上一页得到的一跳算子推广到多通道特征矩阵 H ∈ ℝ^(N×d)，即得经典的 GCN 层前向公式：H′ = σ(S H W)。把矩阵乘法按职责拆成两根正交的轴：左乘 S ∈ ℝ^(N×N) 在“节点轴”上按图结构与两端度数混合每个节点的邻居特征；右乘 W ∈ ℝ^(d×d′) 在“特征通道轴”上把混合后的 d 维向量投影到新的 d′ 维语义空间，且所有节点共享同一个 W；最后逐元素施加非线性激活 σ。

在线性部分，矩阵结合律保证 S(HW) = (SH)W，即先做特征投影再传播与先传播再投影等价，但实际实现中顺序影响计算量，且一旦插入非线性 σ 则不再可交换。

**原文定位**：GCN p2 式(2)；p3 式(8)；行向量矩阵记号。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 10 · GCN 归一化与手算：自环与两端度数怎样决定权重

回到 A—B—C 三节点链图，直观手算中心节点 B 究竟收到多少信息。加上自环 I 后，A 和 C 各连 1 条外部边加自环共 d̃=2，中心 B 连 A、C 加自环共 d̃=3。根据 S = D̃⁻¹ᐟ²(A+I)D̃⁻¹ᐟ²，B 接收自己的系数为 1/√(3×3) = 1/3，接收 A 和 C 的系数各为 1/√(3×2) = 1/√6。

假设隐藏层输入为二维向量 h(A)=[2,1]、h(B)=[0,3]、h(C)=[1,0] 且取恒等变换 W=I，则传播后中心节点为 h̄(B) = [2,1]/√6 + [0,3]/3 + [1,0]/√6 = [3/√6, 1/√6 + 1] ≈ [1.2247, 1.4082]。

注意两点：第一，两端同时开方除度既保留无向算子对称性，又削弱高度数节点对所有邻居的支配；第二，B 这一行权重之和为 2/√6 + 1/3 ≈ 1.1498 ≠ 1，S 并非行随机概率矩阵。

**原文定位**：GCN p2 式(2)、p3 式(8)；向量数值为教学核验。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 11 · 两层 GCN：有限层堆叠如何扩展感受野并连接分类头

单层 GCN 只能聚集一跳直接邻居的信息，Kipf & Welling 在原论文半监督节点分类中采用两层串联模型：Z = softmax(S ReLU(SXW₀) W₁)。第一层用 W₀ 和 ReLU 把原始属性 X 映射并混合成隐藏表示；第二层用 W₁ 把隐藏通道投影到类别数维度的 logits，最后沿着每个节点自身的类别维度做 softmax 得到预测概率。

在 A—B—C 链上，第一层节点 A 只直接看到 A 和 B；但由于节点 B 在第一层已经吸收了 C 的信息，第二层 A 从 B 接收消息时便间接获得了两跳外 C 的影响。需要明确，层数仅决定信息路径的最大跳数上界，远端信号被逐层混合在固定宽度向量中，不代表无损保留；且此处类别维 softmax 与 GAT 邻居维 softmax 是两个完全不同的操作。

**原文定位**：GCN p3–4 式(9)–(10)；链图为教学构造。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 12 · GCN 的半监督训练：少量标签如何更新全图共享的 W

在只有极少数节点有标注的图上，GCN 如何训练？原始 GCN 采用传导式（Transductive）半监督协议：前向传播时，全图所有节点的属性 X 和边结构 S 都参与计算，但交叉熵损失只对训练集已标注节点 YL 求和。假设 A—B—C 中只有 B 有标签，由于 B 的预测 logits 混合了 A、B、C 的特征，反向传播时梯度会沿着 S 的计算图同时更新共享参数 W₀ 和 W₁；更新后的 W 会立刻改善全图所有节点的下一次前向表示。

请严守数据边界：未标注测试节点提供特征和结构是传导式设定的一部分，但测试节点的标签绝不能进入前向特征或损失函数。

**原文定位**：GCN p4 式(10) 及 §3；梯度路径为计算图说明。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 13 · GCN 的结构偏置与边界：平滑何时有效，又有哪些痛点

到此我们看清了 GCN 的机制与代价。重归一化算子 S 隐含了局部低通平滑偏置：当图具有同配性（相邻节点倾向同属一类且特征携带一致线索）时，邻域加权混合能有效降噪并弥补少标签困境。然而这一简洁机制也集中暴露了四大痛点：痛点 A，同度邻居强制等权，无法区分重要邻居与噪声邻居；痛点 B，异配图中邻居往往是异类，强制混合会冲淡节点自身判别特征；痛点 C，堆叠过深引发过平滑，节点表示逐渐塌缩向与 √d̃ 成比例的低维子空间；痛点 D，试图靠堆层获取远距信息时，指数膨胀的邻域被强行压过窄路径，触发过挤压瓶颈。

痛点 A 直接引出模块三的 GAT，痛点 C/D 则将在模块四与五展开解剖。

**原文定位**：GCN §2；Li 2018 §3；Zhu 2020 §3；Alon 2021 §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Li, Han, Wu，Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning，AAAI（2018）。[正式记录](https://arxiv.org/abs/1801.07606) · [本地PDF](../source/papers/oversmoothing2018.pdf)

- Zhu et al.，Beyond Homophily in Graph Neural Networks: Current Limitations and Effective Designs，NeurIPS（2020）。[正式记录](https://arxiv.org/abs/2006.11468) · [本地PDF](../source/papers/heterophily2020.pdf)

- Alon and Yahav，On the Bottleneck of Graph Neural Networks and its Practical Implications，ICLR（2021）。[正式记录](https://arxiv.org/abs/2006.05205) · [本地PDF](../source/papers/bottleneck2021.pdf)

## 14 · 痛点二：同样相连且度数相同，邻居价值一定相同吗？

再看同一张 A—B—C 链图。假设 A 是与中心 B 高度相关的同质节点，而 C 是一条噪声边或无关属性节点。由于 A 和 C 在图拓扑上位置完全对称（度数均为 2），GCN 给 A→B 与 C→B 分配的结构系数完全相同（都是 1/√6），尽管 A 和 C 经过 W 变换后发送的内容向量不同，GCN 却无法根据内容相关性调高 A 的混合比例、压低 C 的干扰。

2018 年 Veličković 等人提出图注意力网络（GAT），核心突破在于把“邻居提供什么内容 Whⱼ”与“这次给它多大权重 αᵢⱼ”拆开计算：固定同一张图邻域掩码，但混合系数改为由接收者与候选邻居的投影特征实时算出，从而实现内容驱动的邻居选择。

**原文定位**：GCN 式(2)；GAT p3–4 式(1)–(4)。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 15 · GAT 单头完整算子：投影、拼接打分、归一化与聚合

拆解原始 GAT 单头的四步精确计算（沿原文列向量记号）。第一步：用共享线性矩阵 W 将所有节点投影为 zᵢ = Whᵢ。第二步：对给定边 (i, j)（j ∈ Ñ(i)，包含 i 自身），将接收者投影 zᵢ 与候选发送者投影 zⱼ 拼接，与共享打分向量 a ∈ ℝ^(2d′) 做内积并经过 LeakyReLU，得到未归一化边分数 eᵢⱼ。

第三步：仅在节点 i 的允许邻域 Ñ(i) 内对 eᵢⱼ 做 softmax，得到和为 1 的注意力系数 αᵢⱼ。第四步：用 αᵢⱼ 对邻居投影向量 zⱼ 加权求和并施加激活 σ，输出新特征 h′ᵢ。务必注意两个关键细节：第一，同一个 W 既参与打分又提供被聚合的内容，不像 Transformer 拆成独立 Q/K/V；第二，这里的 softmax 沿“邻居维度”归一化，而分类输出头的 softmax 沿“类别维度”归一化。

**原文定位**：GAT p3–4 式(1)–(4)；Ñ(i) 为节点 i 含自身的邻域。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 16 · GAT 的参数学习：训练共享打分规则，而非每条边存参数

初学者常误以为 GAT 为图上的每条边单独学习了一个标量参数 αᵢⱼ。事实恰好相反：αᵢⱼ 根本不是可训练参数，而是每次前向传播时由共享参数 W、a 和当前节点特征实时算出的中间量。因此 GAT 的参数量完全不随图边数增长。观察反向传播路径：任务损失梯度 ∂L/∂h′ᵢ 分成两条支路回传——一条直接经由 αᵢⱼ 加权项更新变换矩阵 W（内容路径）；另一条穿过 softmax 与 LeakyReLU 激活更新打分向量 a 并再次调整 W（打分路径）。

这正是 GAT 能够归纳泛化到未见图的原因：它学到的是“给定任意两个特征向量如何打分”的通用规则。同时要保持因果谨慎：注意力系数 αᵢⱼ 受特征尺度、softmax 分母候选数与多头冗余影响，不能直接等同于节点因果重要性。

**原文定位**：GAT p3–4 式(2)–(4)；计算图与梯度反传分析。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 17 · GAT 多头机制：并行子空间、隐藏层拼接与输出层平均

单组 (W, a) 往往只能捕捉一种相似性模式，且邻域 softmax 在训练初期容易产生方差。GAT 引入 K 个独立的注意力头，在同一给定邻域 Ñ(i) 上各自使用专属参数 (W⁽ᵏ⁾, a⁽ᵏ⁾) 并行打分、归一化与聚合。原论文对隐藏层与最终输出层采取不同的组合策略：隐藏层将 K 个头的输出拼接（concat），若每头维度为 d′，输出宽度扩展为 K·d′，保留多视角特征子空间；而最终输出层将 K 个头的输出取算术平均后再做激活，以保持维度与任务类别数一致。

请注意与 Transformer 的区别：Transformer 多头拼接后还会再乘一次输出投影矩阵 W_O；此外，多头只在同一跳邻域内增加并行观察视角，既不会创造新边，也不能替代堆叠多层来扩大感受野。

**原文定位**：GAT p4 式(5)–(6)、图 1。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 18 · 原始 GAT 的深层局限：为何单头只有“静态排序”？

虽然 GAT 实现了特征相关的注意力，Brody 等人在 2022 年揭示了原始打分公式的一个隐蔽缺陷：把打分向量 a 拆成对应接收者与发送者的左右两半 [a_L ∥ a_R]，由于线性变换可拆开，aᵀ[Whᵢ ∥ Whⱼ] 恒等于 cᵢ + qⱼ，其中 cᵢ = a_LᵀWhᵢ 仅依赖接收者 i，而 qⱼ = a_RᵀWhⱼ 仅依赖候选者 j。

再看外部的 LeakyReLU 与 softmax：二者都是严格单调递增函数！这就意味着，无论接收者 i 的特征怎么变，它能给共同候选集加上的仅仅是一个与 j 无关的常数偏移 cᵢ，绝对无法改变任意两个共同候选 A、C 按 qⱼ 排出的先后顺序！设想接收者 P 需要优先关注 A、而接收者 Q 需要优先关注 C，原始 GAT 单头永远无法同时满足这两个排序需求。

严谨地讲，“静态”限制的是相对排序，若跨越 LeakyReLU 分段点，具体注意力数值 α 仍可随 cᵢ 略微变化。

**原文定位**：GAT 式(3)；GATv2 p3–5 定义 3.1–3.2、定理 1。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

## 19 · GATv2：先向量非线性交互再打分，解锁动态注意力

既然原始 GAT 静态受限是因为“先线性压成标量，再施加单调非线性”，Brody 等人提出的 GATv2 解法极为直接：把非线性激活和投影向量 a 的顺序对调！写为 eᵢⱼ = aᵀ LeakyReLU(W[hᵢ ∥ hⱼ])，等价地拆成 W_L hᵢ + W_R hⱼ。先让接收者与候选特征在多维向量隐层相遇，穿过逐通道的 LeakyReLU 门控，再由 a 投影成标量。

此时不同的接收者 hᵢ 可以改变隐层各个通道是否激活（落在正斜率还是负斜率区间），从而实质性地反转候选排序，达到任意动态注意力的理论表达力。对比 Transformer 的缩放点积 qᵢᵀkⱼ：点积通过接收者查询向量 Q 与候选键向量 K 的方向匹配改变排序，也是动态注意力。注意，理论表达力增强不等于任何数据集都必胜，且两者依然受给定邻接掩码约束。

**原文定位**：GATv2 p4–5 式(7)、定理 2、§3.3。

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

## 20 · 阶段小结：GCN、原始 GAT 与 GATv2 的机制对照

在进入下一大问题之前，先对这三种一跳局部传播算子做机制收口。三者的核心演化集中在混合系数的生成与排序能力：GCN 完全由图拓扑和两端度数决定混合系数，学习职责全部交给 W；原始 GAT 用共享投影 W 与标量打分 a 生成输入相关的权重，通过邻居维 softmax 产生竞争，但在单头内存在静态排序限制；GATv2 调换非线性顺序实现了动态排序。

然而请看表格最后一行：三者都共享同一个根本前提——消息只能沿着预先给定的局部边一步步传播。一旦任务需要精准识别邻域结构计数，或者依赖多跳之外的远端信息，这一局部范式自身就会暴露瓶颈。由此引出模块四的痛点三。

**原文定位**：GCN 式(2)；GAT 式(1)–(6)；GATv2 §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

## 21 · 痛点三（上）：局部聚合何时把不同邻域压成同一表示？（GIN）

局部聚合到底能分辨多精细的图结构？Xu 等人在 2019 年 GIN 论文中指出：节点邻域在数学上是一个“多重集（Multiset）”，不仅包含有哪些特征，还包含每种特征出现了几次。对比两个邻域多重集 X={a, b} 与 Y={a, a, b, b}：Mean 聚合算出相同平均值 (a+b)/2，丢失了邻居总数与规模；Max 聚合算出相同逐通道最大值 max(a,b)，丢失了重复出现次数。

只有 Sum 聚合在配备合适单射编码 f 后能够区分它们。据此，GIN 将聚合与更新统一写为 h′ᵥ = MLP((1+ε)hᵥ + ∑ᵤ hᵤ)，把整层变成可数输入空间上的单射多重集函数，从而在理论上达到与经典 1-WL（Weisfeiler-Lehman）图同构测试等价的结构判别上界。

注意理论单射需满足可数特征与足够宽 MLP 等条件，不代表任意浮点训练都无碰撞。

**原文定位**：GIN p4–6 Lemma 2 / Theorem 3、式(4.2)、图 2–3；多重集为教学构造。

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[正式记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

## 22 · 局部聚合的结构盲区：1-WL 上界与 C₆ vs 2C₃ 反例

即便把聚合器做到完美单射（如理论上的 GIN），局部消息传递仍然存在一道绕不开的天花板：1-WL 判别上界。看右侧这组直观反例：左边是一张连通的六节点单环 C₆，右边是两个互不相连的三节点环 2C₃。两张图拓扑性质截然不同（是否有三角形、是否连通），但假设所有节点初始特征同为 a。

在第一轮，两张图中每一个节点看到的中心与邻居多重集完全相同——都是中心 a 配邻居 {a, a}！归纳下去，无论迭代多少轮，两张图上的 6 个节点都会始终保持完全相同的状态多重集，因此任何只看这些状态做排列不变读出的局部 GNN（包括 GCN、GAT、GIN）都绝对无法分辨二者。要打破这一盲区，必须引入额外子图/环计数特征、位置编码或非局部交互。

**原文定位**：GIN p4 Lemma 2 / Theorem 3；C₆ 与 2C₃ 为教学反例。

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[正式记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

## 23 · 痛点三（下）：远距离信息为何传不过来？（过挤压与过平滑）

除了 1-WL 结构盲区，纯局部消息传递在需要捕捉远距离依赖时面临另一堵高墙——深层退化。这里必须严格区分两个常被混用的概念：过平滑（Over-smoothing）与过挤压（Over-squashing）。过平滑源于拉普拉斯平滑的反复迭代，过多层传播使同一连通分量内不同节点的特征越来越相似、丢失局部辨识度；而 Alon & Yahav 2021 指出的过挤压是图拓扑决定的通信容量瓶颈：当目标节点 T 需要接收 r 跳外指数级增长的源节点群 S₁, S₂, S₃… 的信息时，所有消息被迫穿过图上少数几条“窄桥边”并被压缩进有限维度的状态向量，即使网络并未过平滑也会发生严重的信息丢失。

由此引出模块五的破局问题：能否绕开多跳窄路径，让全图节点在一层内直接交互？

**原文定位**：Li et al. 2018 §3；Alon & Yahav 2021 p2–4 §3。

- Li, Han, Wu，Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning，AAAI（2018）。[正式记录](https://arxiv.org/abs/1801.07606) · [本地PDF](../source/papers/oversmoothing2018.pdf)

- Alon and Yahav，On the Bottleneck of Graph Neural Networks and its Practical Implications，ICLR（2021）。[正式记录](https://arxiv.org/abs/2006.05205) · [本地PDF](../source/papers/bottleneck2021.pdf)

## 24 · 痛点四：如何实现全图直连，并解耦查询、匹配与内容？

为打破局部逐跳通信的窄桥限制，我们把视线转向 Vaswani 等人 2017 年的标准 Transformer Encoder。与 GAT 用单一投影矩阵 W 既算打分又提供内容不同，Transformer 将节点矩阵 H 分别通过三套独立可学习投影映射为查询 Q = H W_Q、键 K = H W_K、内容值 V = H W_V。

注意力权重由缩放点积加掩码再经 softmax 生成：A = softmax(QKᵀ/√dₖ + mask)，其中除以 √dₖ 用于防止维度较大时点积方差过大导致 softmax 饱和梯度消失；最终加权聚合独立的内容向量 A V。更重要的是，完整的 Transformer Block 绝不只是一层注意力，还包含多头并行、残差连接（Add）、层归一化（Norm）以及逐位置前馈网络（FFN）。

对照时不能拿一个完整 Transformer Block 去单挑一层简陋的 SHW 传播式。

**原文定位**：Transformer p3–5：图 1、式(1)–(2)、§3.2.3。

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

## 25 · 关键对照一（通信范围）：邻接掩码、全局与因果掩码

放在同一组节点 {A, B, C, D} 上对比：GCN 与原始 GAT 相当于在所有节点对之间施加了稀疏的“图邻接掩码”——只有存在边的地方允许通信，因此 A 到 C 的消息必须穿过中间节点逐跳传播。标准 Transformer Encoder 去掉邻接限制（全零掩码），让任意节点对在单层之内直接交互，彻底消除了多跳图路径上的过挤压瓶颈。

但请注意两项重要边界：第一，通信掩码是一个完全正交的独立开关——如果给 Transformer 加上原图邻接掩码（非邻居填 −∞），它就变成了用 QK 点积打分的局部 GAT；而 Transformer Decoder 则是用下三角因果掩码屏蔽未来位置；第二，全连接可见不等于模型自动懂得原图结构，没有边信息时，全局注意力根本分不清谁本来相连。

**原文定位**：GAT §2；Transformer §3.2.3；Graphormer §3。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

## 26 · 关键对照二（结构表达）：全局注意力如何注入图拓扑？

序列 Transformer 依靠位置编码知道词序，而在图上，任意给定的节点编号 1…N 根本不是拓扑位置——如果只把节点特征送进全注意力，整张图就退化成了一个无序集合，完全丢失连边结构！Ying 等人 2021 年提出的 Graphormer 展示了如何把拓扑信息系统地注入 Transformer：第一，中心性编码（Centrality Encoding）将节点入度与出度的可学习嵌入向量直接加到初始输入特征中，弥补自注意力对节点连接规模的无感；第二，空间编码（Spatial Encoding）按任意两节点间最短路径跳数查表得到标量偏置，加到 QKᵀ 注意力 logit 上，让模型感知节点间的图距离；第三，边编码（Edge Encoding）沿最短路径上的边特征计算加权偏置，使路径上的键或关系语义直接参与成对打分。

务必记住：节点重编号时，所有特征与成对距离/边偏置矩阵必须同步置换。

**原文定位**：Transformer §3.5；Graphormer p4–5 式(5)–(7)。

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

## 27 · 架构融合：GraphGPS 如何让局部 MPNN 与全局并行

除了像 Graphormer 那样把拓扑全写成成对偏置，2022 年 Rampášek 等人提出的 GraphGPS 给出了另一条极其有效的模块化融合路线：位置结构编码 + 局部/全局同层并行。在每一层中，已经注入位置编码（PE）与结构编码（SE）的节点特征状态，同时进入两条并行支路：上方是局部 MPNN 支路，严格沿着真实边及边属性提取强局部归纳偏置；下方是全局 Attention 支路（可选全连接或线性注意力），让所有节点直接通信以消除过挤压；两支路各自经过残差连接与归一化后直接相加，再送入共享的 FFN/MLP 模块更新状态。

请注意两点事实边界：第一，同层是“并行相加”，而非先 MPNN 再 Attention 的串行；第二，原文在 ZINC 分子数据集上的消融显示去掉全局支路后误差几乎持平，证明全局注意力不是所有局部子结构任务的免费增益。

**原文定位**：GraphGPS p5 式(1)–(4)、p6 复杂度、p20 表 B.1。

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 28 · 关键对照三（计算成本）：复杂度与结构偏置的取舍

在统一设定 N 个节点、E 条有向消息边、每层总隐藏宽度为 d 并固定头数的前提下，我们来核对四类架构的真实成本账单。GCN 与原始 GAT / GATv2 的主计算量均为 O(Nd² + Ed)：特征线性投影耗时 O(Nd²)，沿边传播/打分耗时 O(Ed)；对于边数远小于 N² 的稀疏大图，这几乎呈节点线性扩展。

标准全注意力（如 Graphormer）的主计算量为 O(Nd² + N²d)，因为任意节点对都要计算内积，显存与算术随 N² 急剧攀升；哪怕使用 FlashAttention 等分块内存优化免存完整 N×N 矩阵，精确全注意力的 O(N²d) 算术次数依然存在。此外，千万不能忽略图 Transformer 的预处理开销：全图最短路或拉普拉斯特征分解本身可达 O(N³) 或高额稀疏开销，不能撇开预处理宣称图 Transformer 达到纯线性成本。

**原文定位**：GCN §3；GAT §2；Transformer p6 表 1；GraphGPS p6。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 29 · 全维对比矩阵：GCN、GAT、GATv2 与图 Transformer

在结束架构原理深读之际，这张六行总表把 GCN、原始 GAT、GATv2、标准 Transformer Encoder 以及图 Transformer（Graphormer / GraphGPS）放在同一把尺子下横向对齐。可以看到：从 GCN 到 GAT 再到 GATv2，通信范围始终锁定在给定的一跳局部边内，演进发生在“打分公式”与“排序动态性”；从 GATv2 到标准 Transformer，放开了通信掩码并解耦了独立的 Q、K、V 与 FFN 块，却付出了丢掉图拓扑感知和平方级成对运算的代价；而图 Transformer 则重新把度编码、最短路偏置或并行 MPNN 支路请回网络。

记住：它们分别在三个正交轴上做出不同权衡，而非简单的线性淘汰关系。

**原文定位**：GCN 式(2)；GAT 式(1)–(6)；GATv2 式(7)；Transformer 式(1)；Graphormer §3；GraphGPS §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 30 · 痛点五：从单图传导到跨图泛化——新节点与新图复用

前面讨论的 GCN 训练都在同一张固定大图上运行。如果遇到两个现实工程痛点怎么办？第一个痛点是“大图显存爆炸与新节点不断涌入”：2017 年 GraphSAGE 给出第一代归纳学习方案——不再为全图做满邻域展开，而是从目标节点出发反向定长采样邻居，把邻居聚合成向量再与自身状态拼接，通过共享权重 W[hᵥ ∥ AGG({hᵤ})] 生成表示。

只要新节点或新图的特征维度、通道语义与类别空间与训练图一致，训练好的共享函数就可以直接前向计算新节点表示，无需重训。然而这引出了第二个更深层的跨图痛点（2025–2026 研究前沿）：如果目标新图来自完全不同的领域，特征维度 d₁ ≠ d₂、类别数 C₁ ≠ C₂、特征列排列也毫无对应，固定形状的 W₀ 和分类头立刻失效，该怎么复用模型？

**原文定位**：GraphSAGE p4–6 算法 1、式(1)；GraphAny p1–3 §1–2。

- Hamilton, Ying, Leskovec，Inductive Representation Learning on Large Graphs，NeurIPS（2017）。[正式记录](https://arxiv.org/abs/1706.02216) · [本地PDF](../source/papers/graphsage2017.pdf)

- Zhao, Zhu, Galkin, Mostafa, Bronstein, Tang，Fully-inductive Node Classification on Arbitrary Graphs，ICLR（2025）。[正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [本地PDF](../source/papers/graphany2025.pdf)

## 31 · 2025–2026 跨图复用前沿：GraphAny 与 GraphPFN

针对异构特征与不同类别数的跨图节点分类，2025–2026 年出现了两条机制截然不同的正式发表路线。第一条是 GraphAny（2024 预印本、ICLR 2025 正式论文）：它不迁就特定特征维度，而是先用目标图本身的部分已标注节点与多组固定线性图滤波器现场解出几个闭式解析预测器；随后构造同一节点各预测通道间对特征和类别坐标置换不变的距离，并配合熵归一化缓解类别数变化，最后由预训练好的跨图注意力模块融合各线性预测器。

第二条是 GraphPFN（2025 预印本、ICML 2026 / PMLR 306）：它冻结 LimiX 二维特征-样本注意力骨干，专门加入邻接掩码图注意力适配器，在大量合成属性图（SCM 先验）上继续预训练；测试时把目标图的已标注节点作为上下文输入，单次前向做上下文学习（ICL）预测查询节点。

两条路线虽无需目标图梯度微调，但“免微调”绝不等于“零目标图标签”！

**原文定位**：GraphAny (ICLR 2025) p4–6；GraphPFN (ICML 2026 / PMLR 306) p3–6、p12。

- Zhao, Zhu, Galkin, Mostafa, Bronstein, Tang，Fully-inductive Node Classification on Arbitrary Graphs，ICLR（2025）。[正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [本地PDF](../source/papers/graphany2025.pdf)

- Eremeev, Platonov, Bazhenov, Babenko, Prokhorenkova，GraphPFN: A Prior-Data Fitted Graph Foundation Model，ICML / PMLR 306（2026）。[正式记录](https://proceedings.mlr.press/v306/eremeev26a.html) · [本地PDF](../source/papers/graphpfn2026.pdf)

## 32 · 架构选型决策树：按「痛点 → 机制 → 前提」落地

把全篇五条问题链落回工程选型：选择任何图模型之前，不要迷信年份越新越好，而应先诊断任务面临的核心痛点。如果图具有高同配性且标签稀少，2–3 层 GCN 是最简洁可靠的基线，但务必先用“仅自环 MLP”与“打乱图”做对照，确认图关系确实有效；如果同一邻域内邻居质量参差不齐，使用 GAT 或具备动态排序能力的 GATv2，同时核验样本量是否足以防过拟合；如果需要精确计数或区分多重集结构（如分子图分类），选择 GIN 并排查是否存在 1-WL 盲区（如环计数缺失）；如果任务依赖跨过窄桥的长程交互，考虑 Graphormer 或 GraphGPS 并核算 O(N²) 算力与预处理预算；如果面临工业级大图或同构新节点流，选用 GraphSAGE 采样；如果必须在异构未知空间快速适应，评估 GraphAny 或 GraphPFN。

公平实验比较必须固定划分、特征、预算与选模协议。

**原文定位**：依据各原论文方法与边界的教学归纳；公平对比需固定划分与预算。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[正式记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

- Hamilton, Ying, Leskovec，Inductive Representation Learning on Large Graphs，NeurIPS（2017）。[正式记录](https://arxiv.org/abs/1706.02216) · [本地PDF](../source/papers/graphsage2017.pdf)

- Zhao, Zhu, Galkin, Mostafa, Bronstein, Tang，Fully-inductive Node Classification on Arbitrary Graphs，ICLR（2025）。[正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [本地PDF](../source/papers/graphany2025.pdf)

- Eremeev, Platonov, Bazhenov, Babenko, Prokhorenkova，GraphPFN: A Prior-Data Fitted Graph Foundation Model，ICML / PMLR 306（2026）。[正式记录](https://proceedings.mlr.press/v306/eremeev26a.html) · [本地PDF](../source/papers/graphpfn2026.pdf)

## 33 · 原文精读路径与本地溯源索引

最后留下一份按问题链编排的原文精读指南。第 1 站先读 MPNN（p3 式(1)–(3)）建立 M/AGG/U 统一坐标；第 2 站读 ChebNet（p3 式(3)–(4)）接 GCN（p2–4 式(2)、式(4)–(10)）理清四步近似与训练；第 3 站读 GAT（p3–4 式(1)–(6)）接 GATv2（p3–5 定理 1–2 与式(7)）彻底搞懂静态与动态排序；第 4 站读 GIN（p4–6 定理 3 与式(4.2)）接 Alon 2021（p2–4 §3）把握 1-WL 上界与过挤压；第 5 站读 Transformer（p3–5 图 1/式(1)）、Graphormer（p4–5 式(5)–(7)）与 GraphGPS（p5 式(1)–(4)）；第 6 站读 GraphSAGE（p4 算法 1）接 GraphAny / GraphPFN 定位跨图复用边界。

本仓库已存档 30 份原始 PDF 与 6 份网页快照，完整来源时间与 SHA-256 见 source/manifest.json。

**原文定位**：所有页码均为本地原始 PDF 物理页；完整 31 篇索引见 source/paper-index.md。

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[正式记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[正式记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

- Hamilton, Ying, Leskovec，Inductive Representation Learning on Large Graphs，NeurIPS（2017）。[正式记录](https://arxiv.org/abs/1706.02216) · [本地PDF](../source/papers/graphsage2017.pdf)

- Zhao, Zhu, Galkin, Mostafa, Bronstein, Tang，Fully-inductive Node Classification on Arbitrary Graphs，ICLR（2025）。[正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [本地PDF](../source/papers/graphany2025.pdf)

- Eremeev, Platonov, Bazhenov, Babenko, Prokhorenkova，GraphPFN: A Prior-Data Fitted Graph Foundation Model，ICML / PMLR 306（2026）。[正式记录](https://proceedings.mlr.press/v306/eremeev26a.html) · [本地PDF](../source/papers/graphpfn2026.pdf)
