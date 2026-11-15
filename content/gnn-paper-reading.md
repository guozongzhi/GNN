# GNN：发展脉络、GCN / GAT 与 Transformer 对照讲稿

对应当前 **26页PPT**，核对于2026-11-15。主线是发展进展、GCN与GAT机制、Transformer关键对比；不含Demo和性能排行榜。下文页码均指本地原始PDF的物理页，从文件首页起计。

## 阅读结构

| 页码 | 主题 | 需要回答的问题 |
| --- | --- | --- |
| 2–6 | 发展与比较框架 | 哪些瓶颈推动GNN演进，哪些设计轴应分开比较？ |
| 7–12 | GCN深读 | 传播式怎样得来，归一化怎样作用，训练改变什么？ |
| 13–18 | GAT深读 | 系数如何生成，多头改变什么，静态排序限制是什么？ |
| 19–24 | GCN/GAT直接对照与Transformer | 掩码、打分、Q/K/V、结构编码和成本怎样不同？ |
| 25–26 | 归纳与原文路径 | 怎样把模型选择与信息需求对应起来？ |

## 共同记号

A是邻接矩阵，I提供自身连接，D̃是A+I的度矩阵，S是GCN传播算子。X是原始属性，H / h是隐藏表示，W / a是共享可学习参数，σ是逐通道激活。L=I−D^-1/2 A D^-1/2是对称归一化拉普拉斯，L̃是缩放后的拉普拉斯。

矩阵总式把节点放在行，因此写HW与HWQ；GAT单节点公式沿原文采用列向量，写zᵢ=Whᵢ。两种约定互为转置，不把同名矩阵直接混用。消息下标ij表示接收者i从发送者j接收；GAT的邻域Ñ(i)包含自身。

区分原论文的方法定义、理论保证和本稿教学推导。近期论文以正式全文和官方会议记录交叉核对；未在本次独立复现论文性能。

## 01 · GNN：发展脉络、GCN与GAT、Transformer对照

本讲只沿一条问题链展开：GNN怎样从固定的邻域传播发展为可学习注意力，又怎样与Transformer融合。主体聚焦GCN和GAT，近期跨图复用仅作进展窗口。其余模型作为历史定位或比较证据，不各自展开应用章节。历史基准分数和Demo不进入正文。原始论文、固定文件与SHA-256见source/manifest.json。

## 02 · 主线：图上的信息由谁传来，又怎样组合

本讲用通信范围和组合规则解释模型关系。GCN沿给定边传播，混合系数由图与度计算，学习特征变换；GAT通常保留同一给定邻域，额外学习依赖节点特征的混合系数；标准全注意力Transformer让允许集合内的所有位置直接交流，按Q/K匹配打分。图Transformer再把拓扑信息放进编码、偏置、掩码或局部支路。

它们不是单一的优劣序列：连接范围、打分函数、结构表达是可分开选择的设计轴。

**原文定位**：GCN §2；GAT §2；Transformer §3；GraphGPS §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 03 · 发展脉络：从图域递归到可训练的局部传播

早期GNN用共享状态函数在图上迭代到固定点。谱卷积通过拉普拉斯特征向量定义图上的滤波；ChebNet把滤波限制为低阶多项式，使计算局部化并避免显式谱基。GCN进一步选择一阶近似与重新归一化，成为简洁的节点分类基线。GAT把邻居混合系数改为可学习注意力。年份按主要发表口径：GCN预印本2016、ICLR2017；GAT预印本2017、ICLR2018。

此处是服务主线的选读路径，不声称完整起源史，也不把GAT称为GNN唯一后继。

**原文定位**：Scarselli §III；Bruna §3；ChebNet §2；GCN / GAT §2。

- Scarselli et al.，The Graph Neural Network Model，IEEE TNN（2009）。[正式记录](https://doi.org/10.1109/TNN.2008.2005605) · [本地PDF](../source/papers/scarselli2009.pdf)

- Bruna et al.，Spectral Networks and Deep Locally Connected Networks on Graphs，ICLR（2014）。[正式记录](https://arxiv.org/abs/1312.6203) · [本地PDF](../source/papers/bruna2014.pdf)

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[正式记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 04 · 后续进展：结构判别、远距离通信与跨图复用

GIN把邻域聚合的结构判别能力与1-WL联系起来，揭示不同聚合器丢失的信息及理论条件。远处消息通过窄图路径、固定宽度状态汇合，形成过挤压瓶颈；这与过平滑不同。Graphormer以拓扑编码和全局注意力提供另一种通信结构，GraphGPS把局部消息传递和全局注意力并行组合。另一条研究线研究跨图迁移、通用分类器和上下文学习，GraphAny与GraphPFN是后文两个代表。

这里的箭头仅指阅读顺序，各研究线并存，不表示较新架构在所有任务替代GCN或GAT。

**原文定位**：GIN §4；Alon §3；Graphormer §3；GPS §3；GraphAny / GraphPFN 方法。

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[正式记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

- Alon and Yahav，On the Bottleneck of Graph Neural Networks and its Practical Implications，ICLR（2021）。[正式记录](https://arxiv.org/abs/2006.05205) · [本地PDF](../source/papers/bottleneck2021.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

- Zhao, Zhu, Galkin, Mostafa, Bronstein, Tang，Fully-inductive Node Classification on Arbitrary Graphs，ICLR（2025）。[正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [本地PDF](../source/papers/graphany2025.pdf)

- Eremeev, Platonov, Bazhenov, Babenko, Prokhorenkova，GraphPFN: A Prior-Data Fitted Graph Foundation Model，ICML / PMLR 306（2026）。[正式记录](https://proceedings.mlr.press/v306/eremeev26a.html) · [本地PDF](../source/papers/graphpfn2026.pdf)

## 05 · 近期进展：两种跨图复用路线

GraphAny是2024预印本、ICLR2025正式论文。它用固定线性图滤波器与目标图部分标签构造解析分类器，再构造同一节点各预测通道间的置换不变距离，并做熵归一化以缓解类别维度变化，最后用学习过的注意力模块融合多个线性预测器。跨图迁移的是组合规则，解析分类器仍依赖目标图标签。GraphPFN最终发表于ICML2026、PMLR306。

它在LimiX的二维特征与样本注意力骨干上加入邻接掩码的图注意力适配器，以合成属性图先验继续预训练，目标图用有标签上下文预测查询节点。继续预训练冻结骨干而训练图适配器。无微调推理不等于无目标标签。两者并列显示不同复用机制；GraphPFN不是纯GCN，也不是抛弃图结构的普通Transformer。

模型和先验仍有适用范围，不能称为所有图任务的通用解。

**原文定位**：GraphAny p4–6；GraphPFN p3–6、p12；会议正式版本。

- Zhao, Zhu, Galkin, Mostafa, Bronstein, Tang，Fully-inductive Node Classification on Arbitrary Graphs，ICLR（2025）。[正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [本地PDF](../source/papers/graphany2025.pdf)

- Eremeev, Platonov, Bazhenov, Babenko, Prokhorenkova，GraphPFN: A Prior-Data Fitted Graph Foundation Model，ICML / PMLR 306（2026）。[正式记录](https://proceedings.mlr.press/v306/eremeev26a.html) · [本地PDF](../source/papers/graphpfn2026.pdf)

## 06 · GCN、GAT 与 Transformer 的关键区别

先看概览，再深读两种GNN。GCN固定的是由图与度得到的混合系数，不是整个网络参数。GAT参数在边间共享，但由输入特征产生的系数每次前向可不同。标准Transformer的Q/K/V均为可学习投影，注意力范围由掩码规定；本页全局范围特指标准全注意力Encoder，Decoder因果掩码和稀疏变体另当别论。

图Transformer不是单一公式，Graphormer和GPS展示两种加入结构的办法。

**原文定位**：GCN 式(2)；GAT 式(1)–(6)；Transformer 式(1)；Graphormer §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

## 07 · GCN 核心公式：传播、变换与非线性

输入H按行存节点、按列存特征，传播算子S左乘，沿节点维把邻居的信息组合起来；W右乘，对每个节点使用同一特征通道变换；激活函数逐通道引入非线性。以行向量约定写作H′=σ(SHW)。S由给定图加自环后归一化得到，在原始模型中不被标签梯度学习；W由任务损失优化。维度为H:N×d，S:N×N，W:d×d′，输出N×d′。

矩阵结合律允许线性部分S(HW)=(SH)W，但一般不能让非线性越过S或W。

**原文定位**：GCN p2 式(2)；p3 式(8)。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 08 · GCN 的来源：从谱滤波到一跳传播

谱滤波在拉普拉斯特征向量基上调整图信号的各频率分量。ChebNet以低阶多项式近似滤波器，通过局部稀疏乘法避免显式特征分解。GCN选择最高一阶，近似最大特征值为2，令L̃≈L−I=−B，B=D^-1/2 A D^-1/2；再绑定系数θ0′=−θ1′=θ，得到θ(I+B)x；最后将I+B替换为S。

最后一步是重新设计传播算子而非恒等变换。对非负无向图，S与带自环随机游走算子相似，纯传播谱半径为1；这不构成任意W、非线性和优化条件下全网稳定的保证。

**原文定位**：ChebNet p3 式(3)–(4)；GCN p2–3 式(4)–(8)。

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[正式记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 09 · GCN 归一化：自身信息与两端度数

A—B—C加自环后度为2、3、2。B接收A和C的系数分别为1/√6，自身为1/3。D̃^-1/2(A+I)D̃^-1/2可以拆为发送端缩放、沿边求和、接收端缩放。这种对称缩放让高连接节点的单条消息系数变小，保留无向算子的对称性。它不等于普通邻居均值，也不等于softmax注意力；S的行和通常不为1。

图中自环作用由公式和度数体现，不把无向边误画成新增可学习边。

**原文定位**：GCN p2 式(2)、p3 式(8)；权重为教学推导。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 10 · 两层 GCN：信息传播与分类头怎样连接

原论文节点分类模型可以写作Z=softmax(S ReLU(SXW0) W1)。第一层把输入属性混合后变成隐藏特征，第二层输出类别通道，再在每个节点的类别维做softmax。在线性部分可以先乘W再沿S传播，功能相同而成本可能不同。对一条A—B—C链，A第一层只直接接收A和B，但B的第一层包含C，因而A第二层可以间接依赖C。

传播层数是信息路径的上界，不保证远处所有细节都能保留。这里W0、W1独立，是原始模型设定，不声称所有GNN都不共享层参数。

**原文定位**：GCN p3–4 式(9)–(10)；链图为教学构造。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 11 · GCN 的训练：标签怎样改变共享的 W

原始半监督GCN前向可见同一图的节点属性和边，但交叉熵只在训练标签节点上求和。B有标签时，B的预测依赖自身和邻居特征，梯度沿预测计算图更新各层W。没有标签的邻居也可以在前向图中提供特征，但不把其测试标签放入损失或输入。S在该模型中固定，更新的是跨节点共享的权重；权重更新后全部节点使用同一规则重算。

softmax在类别维归一化，和GAT在邻居维的归一化是两个不同操作。

**原文定位**：GCN p4 式(10)及 §3；流程为教学说明。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 12 · GCN 的偏置与边界：平滑什么时候有用

归一化邻域混合带有平滑偏置。当相邻节点提供对任务有用的一致线索时，该偏置可能缓解标签少的问题；关系噪声、异配或不合适的图构造则可能混合冲突信号。异配是相邻节点标签或属性不同，不意味着任何GNN必然失败；要看是否区分自身与邻居、跳数和关系含义。过平滑描述层间混合后节点表示难区分；过挤压描述很多远处信号穿过窄路径并压进有限宽度状态，两者成因与修正方式不同。

单看层数或参数量无法判定模型是否匹配任务。

**原文定位**：GCN §2；Li §3；Zhu §3；Alon §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Li, Han, Wu，Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning，AAAI（2018）。[正式记录](https://arxiv.org/abs/1801.07606) · [本地PDF](../source/papers/oversmoothing2018.pdf)

- Zhu et al.，Beyond Homophily in Graph Neural Networks: Current Limitations and Effective Designs，NeurIPS（2020）。[正式记录](https://arxiv.org/abs/2006.11468) · [本地PDF](../source/papers/heterophily2020.pdf)

- Alon and Yahav，On the Bottleneck of Graph Neural Networks and its Practical Implications，ICLR（2021）。[正式记录](https://arxiv.org/abs/2006.05205) · [本地PDF](../source/papers/bottleneck2021.pdf)

## 13 · GAT 的动机：同样相连，信息未必同样有用

仍取同一张A—B—C链。A与C在给定图中对B同样相连且度数相同，GCN为这两条边给相同的结构系数；不过其特征变换后内容可以不同，不能说GCN完全不使用节点特征。GAT进一步从B和候选节点的投影特征计算混合系数：图不变而特征改变，系数也可变。它把“邻居带来什么内容”和“这次给它多大权重”分开计算。

原GAT只在给定邻域含自身上运算，没有自动发现所有语义相似但不相连节点。

**原文定位**：GCN 式(2)；GAT p3–4 式(1)–(4)。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 14 · GAT 完整算子：投影、打分、归一化、聚合

原始GAT使用共享线性投影zi=Whi。逐边logit为eij=LeakyReLU(aᵀ[zi∥zj])；把所有允许候选的e送入以邻居为维度的softmax，得到αij=exp(eij)/Σk∈Ñ(i) exp(eik)，最后h′i=σ(Σj∈Ñ(i) αij zj)。a是共享打分向量，拼接符号∥把接收者和发送者投影并排。

W既服务打分，也提供被加权的内容；原始单头不单独定义Transformer那样独立的Q、K、V矩阵。softmax令同一接收节点的候选系数和为1，但此性质不适用于GCN的S。

**原文定位**：GAT p3–4 式(1)–(4)；Ñ(i) 含自身。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 15 · GAT 的学习：训练的不是每条边一份参数

α是由W、a以及当前节点特征计算出的中间量，不是独立存储并直接优化的一张每边参数表。任务误差既经内容路径回到W，也经softmax、打分路径回到a和W。因此模型可以学到对任务有用的混合模式。图结构固定时，训练或输入改变会使α改变；图掩码仍限定它能给哪些邻居分配权重。注意力权重大小受归一化集合、特征投影和多头等影响，不能直接等价为节点因果贡献。

**原文定位**：GAT p3–4 式(2)–(4)；训练流程为计算图解释。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 16 · GAT 多头：并行学习不同的投影与混合

多个头在同一个给定邻域上独立使用Wk与ak计算权重和聚合。原论文隐藏层拼接各头结果，若每头宽度为d′、头数为K，则隐藏输出宽度为K d′；最终输出层则平均各头，再作任务激活以保持类别通道含义。Transformer多头通常拼接后再经输出投影WO，这与GAT原始输出层的平均不同。多头扩大了并行表示视角，不会自动新增边或增加一层图距离；各头学习不同模式也不是强制保证。

**原文定位**：GAT p4 式(5)–(6)、图1。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 17 · 原始 GAT 的限制：邻居排序为何仍受约束

把打分向量a拆为左右两段，则aᵀ[zi∥zj]=ci+qj，其中ci只依赖接收者，qj只依赖候选。LeakyReLU为严格单调函数，所以同一头对固定的两个共同候选，按qj的相对排序不随接收者i改变；softmax也保序。这叫静态注意力的排序限制。它不表示α数值完全不随接收者变化：跨LeakyReLU分段时差值和归一化数值仍会变。

一个教学需求是接收者P偏好A而接收者Q偏好C，二者的共同候选包含A与C，各自自环可保留；原始单头不能任意实现这两个共同候选的排序反转。多头或深网可增强整体表达，但不能把单头原式说成任意query-conditioned打分。

**原文定位**：GAT 式(3)；GATv2 p3–5 定义3.1–3.2、定理1。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

## 18 · GATv2：先让两端特征交互，再压成分数

原始GAT先把拼接特征线性压成一个标量，再经过单调非线性，形成ci+qj的排序限制。GATv2把非线性放在向量隐层，再用a投影成标量：eij=aᵀLeakyReLU(W[hi∥hj])，等价地可拆成源、目标两部分矩阵。这样不同接收者能改变隐层通道的激活方式，进而改变候选排序。其定理说明在足够宽度等条件下能表达动态注意力；不能把它扩张成任意训练结果、任意任务都更好。

缩放点积注意力qᵢᵀkⱼ也能依接收者改变排序，但GATv2与点积注意力函数族和约束不同，二者都不凭打分公式决定通信范围。

**原文定位**：GATv2 p4–5 式(7)及定理2；p5 §3.3。

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

## 19 · GCN 与 GAT：差别集中在混合系数的生成

这张对照表总结已经推导过的机制，不用跨论文分数排列优劣。GCN的系数固定于给定图，网络仍有W可训练；GAT用共享参数生成输入依赖的系数，softmax带来邻居竞争，仍受候选图和打分形式影响。两者基本架构都可使用共享规则处理新节点，但实际泛化需要特征、结构和训练分布支持；原论文的某种评估设定不应混同架构唯一能力。

**原文定位**：GCN 式(2)；GAT 式(1)–(6)；GATv2 §3。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

## 20 · Transformer：Q/K 匹配决定权重，V 提供内容

以行向量约定写Q=HWQ、K=HWK、V=HWV；Q表示接收者寻求的信息，K描述发送者可被怎样匹配，V是最终被组合的内容。单头注意力A=softmax(QKᵀ/√dk+mask)，输出AV。除以√dk用于控制点积随宽度增长的尺度，避免softmax过度饱和的倾向。完整Transformer block包含多头注意力、残差连接、归一化与逐位置FFN，不应只拿一个attention算子与整个GCN分类器比较。

原论文Encoder全局可见，Decoder自注意力使用因果mask，另有Encoder–Decoder交叉注意力；本讲主要对照Encoder的同集合自注意力。

**原文定位**：Transformer p3–5，图1、式(1)–(2)、§3.2.3。

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

## 21 · 关键对比一：通信范围由掩码决定

比较同一组节点时，邻接掩码限制局部GNN只沿给定边交流；全注意力Encoder允许所有节点对直接交流，图上的远距离不再等于长计算依赖路径。全局通信不自动知道原图拓扑，也不保证注意力把远处有效信息保留下来。Transformer Decoder的因果掩码按序列方向限制未来位置；稀疏、局部与线性注意力又是其他变体。

因此“GNN局部、Transformer全局”只能作为所选基础架构的对照，不能当作全部模型的定义。

**原文定位**：GAT §2；Transformer §3.2.3；Graphormer §3。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

## 22 · 关键对比二：拓扑不是节点编号或序列位置

没有结构输入的自注意力可以看见所有节点，却不知道这些节点在原图上相邻与否。Graphormer把入度和出度的可学习编码加到节点特征中，把节点对最短路径距离的编码加入注意力logit，再加入最短路径上的边特征编码。由此注意力既比较语义内容，也依赖图上的关系。任意节点编号不是图的固有位置；重编号时特征与成对结构编码应同步置换，才能保持结构含义。

单独度编码仍不能唯一识别所有图，最短路径和边编码也有适用边界。

**原文定位**：Transformer §3.5；Graphormer p4–5 式(5)–(7)。

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

## 23 · 融合进展：GraphGPS 的局部与全局并行

GraphGPS把含位置与结构编码的节点状态同时送入局部MPNN与全局attention，两支分别包含残差和归一化，再相加并经过MLP。边属性进入局部分支；融合后更新的节点状态使这类信息可在后续层进入全局分支。因此不是“先MPNN再attention”的同层串行结构。局部支路保留真实边的归纳偏置，全局支路提供远程通信，结构编码提供位置与角色线索。

原论文ZINC消融说明去全局支路未必变差，不能把融合结构当成所有任务的免费增益。

**原文定位**：GraphGPS p5 式(1)–(4)、p6 复杂度、p20 表B.1。

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 24 · 关键对比三：计算成本与建模偏置的取舍

设N个节点、E条有向消息边、隐藏宽度d，忽略常数并统一每层宽度。GCN和固定头数、总宽度相同的GAT典型计算约为O(Nd²+Ed)，后者还需逐边打分和邻域softmax。标准全注意力Transformer约为O(Nd²+N²d)，显式注意力矩阵有N²项；FFN常数、投影次序、头数、采样和硬件会影响实际成本。

内存优化可避免存完整矩阵，但不自动消除精确全注意力的成对算术。图Transformer的结构编码如最短路预处理还有额外成本，不可忽略后宣称线性。这里不是墙钟时间或精度比较。

**原文定位**：GCN §3；GAT §2；Transformer p6 表1；GPS p6。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 25 · 把演进与选择放回同一条问题链

理解架构时先确定任务需要什么信息，再定位瓶颈。可信局部关系且简单混合已足够时，GCN是清晰的基线；同一邻域内部差异明显时，GAT引入内容驱动的权重，但应检查原始静态排序限制；需要强query-dependent匹配时可比较GATv2或点积打分；依赖远距离且图结构仍有意义时，比较全局或混合图Transformer，并明确结构编码和预算。

这些是有条件的建模判断，不是未实验的性能承诺。公平比较应固定任务、信息可见性、划分、特征、预算和选模过程，区别模块与完整网络。

**原文定位**：依据各原论文方法与边界；本页为教学归纳。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 26 · 原文阅读路径：围绕 GCN、GAT 与 Transformer

按本讲主线阅读：GCN先读传播式、谱推导和分类训练；GAT先读单头和多头，再读GATv2的静态排序定理；Transformer读QKV、掩码与完整Encoder结构；Graphormer和GPS理解结构输入与局部全局融合。GraphAny、GraphPFN仅用于定位近期跨图复用路线。

全部本地原件对应source/manifest.json中的下载时间、固定来源、页数与哈希。原件和历史版本不因当前讲解缩减而删除。

**原文定位**：所有页码为本地原始 PDF 物理页；完整索引见 source/paper-index.md。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[正式记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[正式记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Brody, Alon, Yahav，How Attentive are Graph Attention Networks?，ICLR（2022）。[正式记录](https://arxiv.org/abs/2105.14491v3) · [本地PDF](../source/papers/gatv22022.pdf)

- Vaswani et al.，Attention Is All You Need，NeurIPS（2017）。[正式记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [本地PDF](../source/papers/transformer2017.pdf)

- Ying et al.，Do Transformers Really Perform Bad for Graph Representation?，NeurIPS（2021）。[正式记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [本地PDF](../source/papers/graphormer2021.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[正式记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

- Zhao, Zhu, Galkin, Mostafa, Bronstein, Tang，Fully-inductive Node Classification on Arbitrary Graphs，ICLR（2025）。[正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [本地PDF](../source/papers/graphany2025.pdf)

- Eremeev, Platonov, Bazhenov, Babenko, Prokhorenkova，GraphPFN: A Prior-Data Fitted Graph Foundation Model，ICML / PMLR 306（2026）。[正式记录](https://proceedings.mlr.press/v306/eremeev26a.html) · [本地PDF](../source/papers/graphpfn2026.pdf)
