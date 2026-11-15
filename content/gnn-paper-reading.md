# GNN：原理图解与论文精读讲稿

对应当前 **35页PPT**，2026-11-15更新。正文以机制、推导与反例为主，不以基准分数表组织内容，不含Demo。下文的页码均指仓库中原始PDF的物理页，从第一页起计。

## 共同记号

`x`是可观测输入属性，`h`是传播中的隐藏状态，`W / θ`是跨节点共享的可学习参数，`S`是由图和度数计算的传播算子。`h(A)`表示节点A的状态，上标表示传播层数。消息函数、聚合函数和更新函数分别记作`M / AGG / U`，图级读出记作`R`。

公式后的解释回答三个问题：信息从哪里来、经过什么操作、为什么这种操作保留了所需信息。论文的理论保证、作者实验与本讲教学推导分别说明；所有历史实验都没有在本次重新复现。

## 01 · GNN 原理与关键论文

本讲以原理解释为主。用同一张小图解释邻域消息、特征变换和训练，再逐篇说明经典论文改变了哪一步、为什么改变、又损失了什么。公式紧跟直观解释；保留必要教学反例，实验数字不作主体。所有原始PDF及哈希见source/manifest.json。用户提供的15页入门PPT原字节保留于source/reference-decks。

PPT不含Demo章节。

## 02 · GNN 学的是什么：节点属性与关系共同形成表示

先固定一张A—B—C小图。节点特征是可观测属性，例如用户行为、论文文本或原子类型；边定义允许哪些实体交流。模型要生成的隐藏表示h既含自身属性，也含与任务有关的邻域信息，最终用于节点、边或整图预测。图不是图像可视化，而是信息流的约束。节点改名不改变实体，因此共享的邻域规则应与重编号相容。节点预测随重编号同步重排，整图预测应不变。

不同输出的训练标签和损失必须分别定义，不能把标签直接塞进节点特征。后文主要用接收端Aij表示j向i传消息，DCRNN单独采用原文W的方向约定。

**原文定位**：MPNN p3 式(1)–(3)；Zhou 综述 p3–4 §3。

- Gilmer et al.，Neural Message Passing for Quantum Chemistry，ICML（2017）。[原始记录](https://arxiv.org/abs/1704.01212) · [本地PDF](../source/papers/mpnn2017.pdf)

- Jie Zhou et al.，Graph Neural Networks: A Review of Methods and Applications，AI Open 1 (2020), 57–81; published 2021（2021）。[原始记录](https://arxiv.org/abs/1812.08434v6) · [本地PDF](../source/papers/zhou-survey2021.pdf)

## 03 · 一次消息传递：准备消息、汇总邻居、更新自身

一次消息传递包含三个不同函数。M把发送节点状态、接收节点状态和边属性映射为消息；AGG把数量可变的消息集合变成固定宽度向量；U把聚合消息和中心旧状态融合为新状态。求和、均值等对邻居顺序不敏感，但保留的信息不同。所有节点同步使用上一层状态，避免节点遍历顺序改变结果。接收者并非总使用完整邻居集合，GraphSAGE和PinSage会采样。

原始GCN的M可化为归一化权重乘邻居特征，GAT学习这个权重，RGCN用关系类型选择变换。这些论文的区别因此可以定位到同一条计算链。

**原文定位**：Gilmer et al. 2017，p3 式(1)–(3)。

- Gilmer et al.，Neural Message Passing for Quantum Chemistry，ICML（2017）。[原始记录](https://arxiv.org/abs/1704.01212) · [本地PDF](../source/papers/mpnn2017.pdf)

## 04 · 层数怎样扩展信息范围：沿依赖关系逐层前进

把A—B—C—D链上每个节点的初始属性看成一张独立卡片。第一层中B的状态含A、B、C的信息，A的状态含A和B。第二层A从B的上一层状态中间接接收到C的信息，所以两层的A至多依赖两跳。这个结论针对局部传播且初始特征不含全局信息；GraphGPS全局注意力会改变通信范围。感受野大不代表保留所有信息：多条路径会进入固定维向量，归一化可能衰减远处影响，聚合可能把不同多重集压成相同摘要。

训练时每一层有独立参数，不能把真实深网简单等同重复做固定平均。

**原文定位**：GCN p2 式(2)；MPNN p3 式(1)–(2)；图为教学示意。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Gilmer et al.，Neural Message Passing for Quantum Chemistry，ICML（2017）。[原始记录](https://arxiv.org/abs/1704.01212) · [本地PDF](../source/papers/mpnn2017.pdf)

## 05 · 训练怎样改变传播：标签监督的是共享规则

半监督节点分类不是给每个未标注节点传播一个现成类别。前向时全图特征通过共享W和固定图算子生成表示；只有训练标签节点对交叉熵贡献误差。以B有标签为例，B预测依赖A、B、C的特征，反向传播沿这些计算路径更新共享权重W。更新后的同一W随后用于所有节点。原始GCN中邻接和对称度归一化通常固定，不在标准任务中自动学出新边。

允许测试节点的特征和边进入计算图是传导式协议的一部分，但测试标签不能参与损失或选模。验证标签用于早停和超参数选择，最终测试只在选模后使用。

**原文定位**：Kipf & Welling 2017，p3–4 式(9)–(10)；梯度路径为教学说明。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 06 · 关键论文怎样改变同一条消息传递链

早期GNN求共享状态转移的固定点，Scarselli给压缩映射条件以确保收敛。现代分层模型使用有限次前向传播。Bruna与ChebNet研究怎样在一般图定义滤波，GCN选择低阶、共享和稳定的传播。GraphSAGE处理全邻域展开与新节点表示，GAT处理邻居权重，RGCN处理关系类型，GIN分析聚合丢失的信息。

后面的几何和时空模型还增加坐标对称或事件顺序约束。这些变化属于不同轴，不能用一个“更先进”替代具体问题。

**原文定位**：各原始论文方法章节；Gori 2005 全文未取得，仅保留索引。

- Scarselli et al.，The Graph Neural Network Model，IEEE TNN（2009）。[原始记录](https://doi.org/10.1109/TNN.2008.2005605) · [本地PDF](../source/papers/scarselli2009.pdf)

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[原始记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Hamilton, Ying, Leskovec，Inductive Representation Learning on Large Graphs，NeurIPS（2017）。[原始记录](https://arxiv.org/abs/1706.02216) · [本地PDF](../source/papers/graphsage2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[原始记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Schlichtkrull et al.，Modeling Relational Data with Graph Convolutional Networks，ESWC（2018）。[原始记录](https://arxiv.org/abs/1703.06103) · [本地PDF](../source/papers/rgcn2018.pdf)

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[原始记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

## 07 · 谱图卷积的直觉：图上的“频率”描述邻居差异

在网格里，低频意味着相邻像素变化慢。一般图没有统一左右方向，但仍可比较沿边两端的值是否相似。对组合拉普拉斯Lc=D−A，xᵀLcx等于每条无向边上wij(xi−xj)²的和，差异越小越平滑。谱方法将图信号分解到拉普拉斯特征向量上，再对各分量加权，最后重构。低特征值模态对应较低图变化率。组合拉普拉斯用于本页解释能量；后续ChebNet使用对称归一化L，平滑能量比较xi/√di与xj/√dj，不能不说明就混用。

图卷积可学低通、高通或更复杂响应；GCN的一阶绑定版本则带有平滑偏置。

**原文定位**：Bruna 2014 §3；ChebNet 2016 p3 式(1)–(4)；信号为教学构造。

- Bruna et al.，Spectral Networks and Deep Locally Connected Networks on Graphs，ICLR（2014）。[原始记录](https://arxiv.org/abs/1312.6203) · [本地PDF](../source/papers/bruna2014.pdf)

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[原始记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

## 08 · ChebNet：用连续的局部计算实现谱滤波

自由谱滤波依赖特征向量基U，一般为全局运算。ChebNet把滤波限制为拉普拉斯的低阶多项式。若L̃只包含一跳与对角连接，乘一次最多经过一条边，k次乘积只能影响至多k跳。用多项式组合不同次数，就组合不同范围的局部响应。切比雪夫递推t0=x,t1=L̃x,tk=2L̃tk−1−tk−2避免显式计算U。系数θk学习怎样组合响应，递推本身只负责有效地计算基函数。

原文K为项数，最高次数K−1；本页用r表示最高次数以免与GCN和SAGE的K混淆。局部性是代数保证，不要求训练结果一定平滑，也不等于整层只保存简单平均。

**原文定位**：Defferrard et al. 2016，p3 式(3)–(4)，p4 式(5)；路径图为教学说明。

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[原始记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

## 09 · GCN 的推导：四个选择各自解决什么问题

记B=D^-1/2 A D^-1/2。第一步把Chebyshev滤波截到一阶，单层只处理自身和一跳关系，较远信息靠堆层。第二步近似λmax为2，使缩放后的L̃近似L−I=−B。第三步绑定两个系数θ0′=−θ1′=θ，得到θ(I+B)x，自身和邻居不能再独立调权。第四步将I+B替换成对A+I重新计算度的S。

I+B的特征值可能大于1，多次相乘会放大某些模态；S与随机游走矩阵相似，在非负无向图纯传播部分谱半径为1。该设计缓解传播不稳定，但不保证含任意W与非线性的全网络永远稳定。重要的是最后一步不是数学恒等式，也不是仅把自环项补上。

**原文定位**：GCN p2–3 式(4)–(8)；最后一步为算子替换。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Defferrard, Bresson, Vandergheynst，Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering，NeurIPS（2016）。[原始记录](https://arxiv.org/abs/1606.09375) · [本地PDF](../source/papers/chebnet2016.pdf)

## 10 · GCN 归一化：消息为何同时除以两端的度

A—B—C加入自身连接后，A和C的度为2，B的度为3。B接收A消息的系数是1/√(3×2)，接收自身的系数是1/3。分解S=D̃^-1/2 Ã D̃^-1/2：右侧先按发送节点的度缩放特征，中间沿边累加，左侧再按接收节点的度缩放。这种对称处理让高连接节点的单条消息权重减小，同时保留无向算子对称性。它不同于按接收端度归一化的普通平均，S每行不一定和为1。

教学解释中的“避免高连接节点影响过大”是对系数机制的描述，不保证在所有任务都最佳。原GCN还固定自环强度，后续设计可以改变。

**原文定位**：GCN p2 式(2)、p3 式(8)；三节点权重为教学推导。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 11 · GCN 的两个轴：跨节点传播与特征通道变换

H每行是节点，每列是特征通道。左乘S在节点轴上组合邻居，不改变通道含义；右乘W在特征轴上重新组合各维特征，且所有节点使用相同W。把SHW拆开可以看清结构和学习的职责。S(HW)=(SH)W来自矩阵结合律，只在线性部分允许换序；ReLU插在两者之间通常不再相等。ReLU把负响应截断，使多层网络具有非线性，不能把多层GCN总写成S^K X乘一个矩阵。

输出头将隐藏通道转换成类别分数，softmax在类别维归一化，交叉熵仅取训练标签。标签误差更新W；S通常由固定图预计算。

**原文定位**：GCN p2 式(2)，p3–4 式(9)–(10)；线性换序为教学推导。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

## 12 · GCN 何时有效：平滑与任务信号是否一致

如果边把同类或相似语义节点连接起来，局部平滑可以减少特征噪声，使少标签节点也获得有用邻域线索。但异配图中，相邻节点可能角色相反，一味混合会抹去对任务重要的差异。反复应用S，在连通非负无向且有自环的图上，会使每通道趋向与√d̃成比例的低维子空间；不是一般不规则图上所有原始坐标值完全相等。真实深网还有W、激活、残差，所以纯扩散极限不能冒充所有训练网络的失败证明。

过挤压是另一问题：很多远处节点的信息通过小割集进入有限维状态，尚未表示趋同也可能已经丢信息。异配是数据关系，过平滑是表示演化，过挤压是通信瓶颈，三者不能混为一谈。

**原文定位**：Li et al. 2018 p3–4；Zhu et al. 2020 §3–4；反例为教学构造。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Li, Han, Wu，Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning，AAAI（2018）。[原始记录](https://arxiv.org/abs/1801.07606) · [本地PDF](../source/papers/oversmoothing2018.pdf)

- Zhu et al.，Beyond Homophily in Graph Neural Networks: Current Limitations and Effective Designs，NeurIPS（2020）。[原始记录](https://arxiv.org/abs/2006.11468) · [本地PDF](../source/papers/heterophily2020.pdf)

- Alon and Yahav，On the Bottleneck of Graph Neural Networks and its Practical Implications，ICLR（2021）。[原始记录](https://arxiv.org/abs/2006.05205) · [本地PDF](../source/papers/bottleneck2021.pdf)

## 13 · GraphSAGE：给新节点计算表示，而非另学一张查找表

GraphSAGE从xv开始，将采样邻居状态聚合成av，再与自身状态拼接，通过共享W、非线性和L2归一化生成hv。W[h∥a]可展开为Wself h+Wneigh a，保留自身与邻域的独立角色。归纳性来自共享函数，不是采样本身；新节点只要具备语义一致的特征和可访问邻域，就可使用已学参数前向计算，不必为这个新ID重新优化专用向量。

跨图时特征与标签含义仍需一致。实验新节点时间留出与PPI整图留出检验不同泛化条件，原论文不证明任意分布迁移。

**原文定位**：GraphSAGE p4 算法1，p5–6 §3.1–3.3；示意图不代表原文采样数。

- Hamilton, Ying, Leskovec，Inductive Representation Learning on Large Graphs，NeurIPS（2017）。[原始记录](https://arxiv.org/abs/1706.02216) · [本地PDF](../source/papers/graphsage2017.pdf)

## 14 · GraphSAGE：采样近似计算，损失定义学什么

确定目标节点后，先反向展开并采样各层依赖，再从最底层原始特征向上计算。采样树随层数和每层邻居数乘积增长，重叠去重会减少实际量，不能说系统总成本与图规模无关。对固定邻居向量，均匀样本均值可以无偏；递归依赖、非线性和归一化后，整个表示不保证是全邻域模型的无偏估计。训练有两条路线：监督版直接优化标签任务；无监督版把随机游走共现节点作为正上下文、按分布采节点作负上下文，以内积拉近/推远表示。

无监督表示的分类评估仍使用训练标签拟合读出，不能称整条分类流程不用标签。mean和pool保持顺序对称，LSTM单次结果仍依赖顺序，随机排列不是对称性证明。

**原文定位**：GraphSAGE p5 式(1)、§3.2，p12 算法2，p13–15 附录B–C。

- Hamilton, Ying, Leskovec，Inductive Representation Learning on Large Graphs，NeurIPS（2017）。[原始记录](https://arxiv.org/abs/1706.02216) · [本地PDF](../source/papers/graphsage2017.pdf)

## 15 · GAT：在允许的邻居中学习怎样分配权重

原始GAT先用共享W将每个节点投影为zi，再将目标和候选邻居的投影拼接，经过共享打分向量a和LeakyReLU得到逐边logit。softmax只在给定邻域含自环内归一化，得到α，最后加权求和并激活。GCN系数由结构和度数给定；GAT系数还随输入特征变化。边掩码决定能否交流，注意力决定已有通道分配多少权重；原GAT不会自动把不相连但相似的节点接成边。

注意力的归一化发生在邻居维，节点分类softmax发生在类别维，二者不同。权重是内部计算系数，单独观察α不能得出因果重要性。

**原文定位**：GAT p3–4 式(1)–(6)、图1；图为同一张链的教学示意。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[原始记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 16 · GAT 的多头：并行看不同特征，而非扩大邻域

多头使用各自W与a在同一邻域独立计算聚合，可以学习不同投影与关注模式。隐藏层拼接各头结果，扩大输出通道；最终输出层平均各头，再作任务激活。多头不会新增边，也不直接增大这一层的图感受野。更细的原式限制：将a分成左右两半，aᵀ[zi∥zj]=ci+qj。LeakyReLU严格单调，所以给定相同候选集合，同一头中候选按qj的排序不随目标i改变。

如果全部logit落在同一线性段，ci在softmax中抵消；跨分段时权重数值可改变，但排序仍不改变。这是由原式推出的教学分析，不冒充原文新实验。原论文常量注意力的同架构消融比跨论文最佳分数更接近隔离注意力机制，但只支持指定PPI设定，不支持所有图上必优。

**原文定位**：GAT p4 式(5)–(6)，p8 表3；排序限制由原式教学推导。

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[原始记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

## 17 · R-GCN：边的含义决定消息经过哪种变换

普通聚合把各邻居用同一变换处理，可能忽略关系含义。RGCN先按关系类型分组，对每类使用Wr，把消息按关系内归一化后相加，再加入W0处理自身。正关系与逆关系作为不同传播类型，方向是模型输入的一部分。图中的箭头表示消息传入中心：若事实为“人在公司任职”，公司传给人的消息使用该事实的逆关系类型。独立Wr在关系多且样本稀少时参数膨胀，基分解令各关系矩阵由共享Vb线性组合，关系只学习组合系数arb。

共享的是一组基础变换，不是把全部关系变成同一个权重。另一种块对角分解限制跨通道块交互，属于不同约束。减少参数可能帮助稀有关系，也限制矩阵空间；不保证耗时按参数比例下降。

**原文定位**：R-GCN p2 式(2)–(3)，p3 式(4)、图2；语义图为教学构造。

- Schlichtkrull et al.，Modeling Relational Data with Graph Convolutional Networks，ESWC（2018）。[原始记录](https://arxiv.org/abs/1703.06103) · [本地PDF](../source/papers/rgcn2018.pdf)

## 18 · R-GCN 的编码器与解码器：上下文和评分各管什么

编码器把已有关系事实压进实体表示，解码器再对候选三元组打分。原文使用DistMult，f(s,r,o)=esᵀdiag(r)eo。对固定实体向量和同一r，交换s和o得到同一分数，因此即使RGCN编码器利用了方向，DistMult对同一关系仍不能表达任意非对称性。父母关系的方向例子直观说明这一点。额外引入逆关系标签可以学习另一套关系参数，但不消除原关系交换端点的代数对称。

训练用腐化端点的采样负例和sigmoid损失，未观察到不一定为假。评估必须区分候选集和过滤规则，特别注意逆关系捷径。论文主评FB15k-237避免旧数据中大量逆关系泄漏问题；这与模型是否更会推理是不同维度。

**原文定位**：R-GCN p3–4 图3、式(6)–(7)，p6 表5及讨论；对称性为教学推导。

- Schlichtkrull et al.，Modeling Relational Data with Graph Convolutional Networks，ESWC（2018）。[原始记录](https://arxiv.org/abs/1703.06103) · [本地PDF](../source/papers/rgcn2018.pdf)

## 19 · GIN 的出发点：聚合可能提前丢掉什么信息

邻域是多重集，既包含有哪些特征，也包含各特征出现几次。取a和b为两种不同编码，X={a,b}，Y={a,a,b,b}，对任意逐点编码f，mean(X)=mean(Y)，因为比例相同；max对重复出现也不敏感。sum在适当编码下保留计数，有希望区分这些集合。但未经编码的原始向量直接sum不一定单射，例如标量{1,3}与{2,2}都为4，一旦相加碰撞，后面的MLP无法还原。

GIN的理论是存在合适编码f使求和单射，在可数输入和有界多重集等条件下成立，不是任意浮点向量求和都能区分。实际网络通过前层与MLP学习表示，不保证优化后达到精确单射。

**原文定位**：GIN p5–8 §4–5、图2–3；多重集例子按原文性质教学构造。

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[原始记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

## 20 · GIN 与 1-WL：每一轮怎样保留结构差别

1-WL颜色细化把中心旧颜色和邻居颜色多重集作为新颜色的依据，只要输入对不同就分配不同新颜色。共享邻域聚合GNN若收到同样旧状态与多重集，输出必相同，因此不能超越该过程可区分的结构。反向充分性要求聚合、中心组合和readout都单射，层数足够，才可保留每轮颜色差异。Lemma5在可数特征、有界多重集下构造f，使sum f(x)像不进位的计数编码。

Corollary6把中心角色也编码进来。GIN用MLP((1+ε)hv+Σhu)实现该动机；ε=0时，中心a邻居b与中心b邻居a在该局部输入上碰撞。无理数ε是理论充分构造之一，不等于任意学习出的ε必保证单射。实际GIN-0也可能泛化较好，说明表达能力、优化与泛化是不同问题。

**原文定位**：GIN p4 Lemma2 / Theorem3，p5 Lemma5 / Corollary6，p6 式(4.2)。

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[原始记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

## 21 · GIN 的边界：同样的邻域颜色可能隐藏不同整图

取六节点环C6与两个互不相连三角形2C3。所有节点初始特征同为a，且每个节点都恰有两个邻居。第一轮每个节点看到中心a与{a,a}，所以颜色一致。归纳地，任意后续轮各节点仍看到相同颜色及相同重复数，因此两图每轮的六个节点状态多重集相同。任何只依赖这些状态的排列不变readout都相同。两图显然不同：一个连通且无三角形，另一个不连通且含三角形。

达到1-WL上界的GIN也分不出这个例子，多堆层无效。这个结论假设没有额外节点ID、位置特征或高阶机制；加入新结构信息已改变模型可用输入。

**原文定位**：GIN p4 Lemma2 / Theorem3；C₆ 与 2C₃ 为本讲教学反例。

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[原始记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

## 22 · MPNN 的分子实例：键决定变换，读出组合原子

MPNN统一消息函数M、更新U与读出R，框架中可替换各部分。原文edge network根据边属性生成矩阵A(e)，消息为A(evu)hu：同一原子状态沿不同键或距离可产生不同消息。相比把原子和边分别求和，这保留谁沿哪条边发来的关联。GRU把旧状态与聚合消息融合，经过多轮后形成原子表示。门控sum或set2set把原子集合变成图表示，set2set用循环注意力按需读集合，输出不依赖节点排列。

最终预测的是分子性质，原论文QM9标签主要来自DFT计算。训练标准化目标并优化MSE，评估MAE。其部分无空间消融使用DFT partial charge，作者明确该输入在应用中不可直接取得，讲解机制时不能省掉输入可得性。

**原文定位**：MPNN p3 式(1)–(4)，p5–6 §5.1–5.3，p7–8 §8。

- Gilmer et al.，Neural Message Passing for Quantum Chemistry，ICML（2017）。[原始记录](https://arxiv.org/abs/1704.01212) · [本地PDF](../source/papers/mpnn2017.pdf)

## 23 · PinSage：先找到有用邻域，再学习相似候选的差别

PinSage在pin–board二部图上从query出发作短随机游走，按访问频率取重要邻居并归一化为权重。它不是平均全部一跳邻居；游走把更远的共现关系汇总成有限邻域。每个邻居先变换再作重要性加权，与自身拼接、变换和归一化。训练使用margin ranking hinge：正例相似度要超过负例相似度一定间隔。

随机负例往往过容易，模型已经把它排远后不再产生梯度；困难负例与正例更像，迫使表示学习细粒度差异。作者用课程方式渐增hard negatives，避免一开始过难。训练时CPU采样和取特征、GPU计算局部批次；离线MapReduce逐层生成全图embedding；线上近邻检索复用这些embedding，不是每个请求全图前向。

原文离线Hit-rate和缩放MRR有特殊候选及排名定义，不能直接当线上点击增益。

**原文定位**：PinSage p4 算法1，p5 式(1)，p6 §3.4–3.5；p8 指标定义。

- Ying et al.，Graph Convolutional Neural Networks for Web-Scale Recommender Systems，KDD（2018）。[原始记录](https://arxiv.org/abs/1806.01973) · [本地PDF](../source/papers/pinsage2018.pdf)

## 24 · LightGCN：传播 ID 嵌入，让共同交互产生相似性

LightGCN针对用户–物品隐式反馈图，输入为可训练ID向量。节点初值没有像文本或图像那样固定语义通道，作者通过NGCF消融提出去掉层间W与非线性。传播只作D^-1/2 A D^-1/2的归一化邻居求和，不额外加自环；最终组合零层到K层状态，因此原始ID信息仍可保留。在二部图上，一跳用户吸收物品状态，两跳又回到共享交互的用户，这解释高阶协同信号。

线性展开E=P(S)E0=Σαk S^k E0，表示多种路径长度的滤波组合。该式不代表每条路径权重相等，度归一化和不同长度系数仍作用。论文在ID协同过滤中的优化观察不能推广到丰富语义特征的所有图任务。

**原文定位**：LightGCN p3–4 §2.2–3.1，式(3)–(5)；路径解释为教学推导。

- He et al.，LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation，SIGIR（2020）。[原始记录](https://arxiv.org/abs/2002.02126) · [本地PDF](../source/papers/lightgcn2020.pdf)

## 25 · LightGCN 的学习：误差怎样回到初始 ID 向量

用户物品得分是最终向量内积，BPR损失最大化已交互i相对于未观测j的得分差。损失对最终嵌入产生梯度，沿线性的多跳传播回到E0，所以删掉传播W不意味着无训练。教学代数：E=P(S)E0，S与α固定时∂L/∂E0=P(S)ᵀ∂L/∂E。图上的邻居因此耦合初始向量的更新。BPR使用未观测为对比近似，不能认定用户真的不喜欢j。

层组合使浅层和深层信号共存，但均匀权重并非每任务最优；作者有单层配置更优的反例。消融中去掉非线性单独一步也非全数据提升，结论是特定ID推荐中简化有利于优化，不是复杂模块在理论上永远无用。

**原文定位**：LightGCN p4 式(5)，p5 式(15)；梯度展开为教学推导。

- He et al.，LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation，SIGIR（2020）。[原始记录](https://arxiv.org/abs/2002.02126) · [本地PDF](../source/papers/lightgcn2020.pdf)

## 26 · DCRNN：空间扩散进入循环单元，时间状态继续传递

DCRNN同时处理两个方向：路网空间上的有向扩散与观测随时间演化。原文W_ij表示i到j，出度DO=diag(W1)，入度DI=diag(Wᵀ1)，Pf=DO^-1 W，Pb=DI^-1 Wᵀ。滤波把不同扩散步数的Pf^k X和Pb^k X用可训练系数组合。它们提供上下游可用信息通道，并不是精确求解交通物理方程。

DCGRU将GRU门和候选状态中的稠密线性映射替换为扩散卷积，隐状态沿时间传递。编码器读历史，解码器递归预测未来。训练纯喂真值而推理喂预测会导致输入分布差异，scheduled sampling逐渐让训练使用自身预测；它缓解差异，但不保证长时滚动无误差。

**原文定位**：DCRNN p2–4 §2、式(2)–(4)、图2；p7–8 消融。

- Yaguang Li, Rose Yu, Cyrus Shahabi, Yan Liu，Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting，ICLR（2018）。[原始记录](https://arxiv.org/abs/1707.01926v3) · [本地PDF](../source/papers/dcrnn2018.pdf)

## 27 · TGN：事件更新记忆，预测只能使用过去

静态图把多次交互合并，容易丢失发生顺序。TGN把事件eij(t)作为基本输入，消息可由事件前双方记忆si(t−)、sj(t−)、时间间隔和事件特征形成；聚合多个消息后用GRU等更新记忆，embedding模块再结合邻居记忆与时间信息生成查询时表示。记忆是历史状态，不等于最终embedding。训练存在微妙矛盾：若当前事件更新后才预测自己会泄漏；若完全在预测后做无梯度的更新，memory模块无法直接收到这批损失梯度。

原文用raw message store保存过去事件，在下一批先由过去消息更新记忆、再预测当前批、最后缓存当前消息。整批共享相同记忆快照，批越大后部事件越看不到本批较早事件，吞吐与陈旧度需权衡。按时间切分还要检查特征、邻居和记忆是否按时点生成。

**原文定位**：TGN p3–5 §3、式(1)–(5)、图2；p7 §5。

- Emanuele Rossi et al.，Temporal Graph Networks for Deep Learning on Dynamic Graphs，arXiv preprint / ICML 2020 GRL+ workshop（2020）。[原始记录](https://arxiv.org/abs/2006.10637v3) · [本地PDF](../source/papers/tgn2020.pdf)

## 28 · EGNN：属性保持不变，坐标随整体变换一起变化

把分子或粒子系统整体平移旋转后，原子类型、距离和某些标量性质应不变；预测位置、力等向量则应随坐标系一起变换。前者叫不变，后者叫等变。EGNN把输入分成标量特征h与几何坐标x。消息网络只读取h、边属性和距离平方，因此输入整体变换时消息保持不变；坐标更新使用相对位移向量乘标量系数，所以方向自然跟着几何改变。

它不需要MLP从有限增强样本中猜出所有旋转规律。等变性只描述坐标变换下的行为约束，不保证模型满足全部守恒定律或动力学稳定性。原式E(n)还含反射，下一页展开其证明与边界。

**原文定位**：EGNN p2–3 式(3)–(6)、§3.1；示意几何为教学构造。

- Satorras, Hoogeboom, Welling，E(n) Equivariant Graph Neural Networks，ICML（2021）。[原始记录](https://arxiv.org/abs/2102.09844) · [本地PDF](../source/papers/egnn2021.pdf)

## 29 · EGNN 的等变证明：方向来自坐标，强度来自 MLP

设变换x̃i=Qxi+t，QᵀQ=I。相对位置变为Q(xi−xj)，范数平方不变，所以消息mij=φe(hi,hj,||xi−xj||²,aij)保持不变，标量φx(mij)也不变。坐标更新xi′=xi+CΣ(xi−xj)φx(mij)，变换后每个向量都左乘Q，代数整理得到x̃i′=Qxi′+t。特征更新hi′=φh(hi,Σmij)仍不变，逐层归纳即可保留性质。

Q包含反射，故若输入只有标量属性与距离、输出要求不变标量，镜像构型可能无法区分；坐标输出仍会随镜像等变，不能说整个EGNN完全不能表达手性。手性提醒来自公式推论，非原文此处做过的实验。

**原文定位**：EGNN p2 式(3)–(6)，p3 §3.1、附录A；镜像限制为教学推论。

- Satorras, Hoogeboom, Welling，E(n) Equivariant Graph Neural Networks，ICML（2021）。[原始记录](https://arxiv.org/abs/2102.09844) · [本地PDF](../source/papers/egnn2021.pdf)

## 30 · GraphGPS：局部与全局并行，结构编码补足位置

GraphGPS将节点状态在同层并行送入local MPNN和global attention，两支各自残差归一化后相加并进入MLP；边属性进入local分支，不是先MPNN再attention的串行层。局部支路沿真实边提取邻域归纳偏置，全局支路允许远节点直接交流，PE/SE把结构位置或角色加入输入。

纯attention若节点初始特征相同、没有结构信息，会把相同节点对称处理；位置结构编码用于打破这些不可分辨性，但编码选择会决定保留的信息及稳定性。标准全注意力仍为O(N²)，线性attention的线性复杂度以固定宽度并排除结构编码预处理等为条件。原文ZINC消融去global后误差持平，说明局部子结构任务不必从全局支路获益。

**原文定位**：GraphGPS p5 式(1)–(4)，p6 复杂度，p20 表B.1。

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[原始记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 31 · GraphCast：在多尺度图上学习下一步状态变化

GraphCast输入连续两时刻天气状态以及forcing/static信息，通过Grid2Mesh编码到球面多尺度网格，在mesh processor沿不同尺度边传播，再Mesh2Grid解码回经纬网。输出是去标准化后的状态残差，与最新输入状态相加形成下一帧，之后把预测帧作为下一次输入，逐步滚动。多尺度边让远处信息经过较短图路径交互，不是在百万网格上做标准全注意力。

损失是变量、层次、格点面积加权MSE：面积权重避免经纬网极区格点密集导致过计数，变量归一化避免量纲大者垄断误差，任务权重改变优化重点。多步自回归训练对完整展开序列反传，减少仅训练一步的分布差异；较长预测仍可能积累误差，MSE也可能鼓励模糊。原文部分平流层目标落后于HRES，不能说所有指标都胜。

**原文定位**：GraphCast p25–33 式(4)–(5)、式(19)、§4；主文图1。

- Lam et al.，Learning skillful medium-range global weather forecasting，Science（2023）。[原始记录](https://arxiv.org/abs/2212.12794) · [本地PDF](../source/papers/graphcast2023.pdf)

## 32 · GNoME：GNN 筛选候选，DFT 建立新的验证数据

GNoME不是让GNN直接宣告材料已被合成。结构候选通过原子节点和距离边建图，模型预测形成能等信息筛选，再对保留候选进行DFT结构弛豫与能量计算。计算结果既用于验证，也回流到训练与下一轮候选生成，形成主动学习闭环。稳定性以与竞争相组合的能量凸包比较为核心：若候选能量高于同组成的相混合最低能量，就可能分解；加入新低能结构后，旧凸包会下降，原先稳定的候选可能失去稳定性。

原论文对旧凸包和更新凸包的数量口径不同，不能合并为“发现并合成”的数量。DFT稳定还取决于近似泛函、温压条件与动力学，实验合成可行性是更后一级证据。模型预测误差和候选筛选命中率也属不同指标。

**原文定位**：GNoME p1–4 主文、图1–2，p7–8 Methods；凸包说明为教学解释。

- Merchant et al.，Scaling deep learning for materials discovery，Nature（2023）。[原始记录](https://doi.org/10.1038/s41586-023-06735-9) · [本地PDF](../source/papers/gnome2023.pdf)

## 33 · GNN 与语言模型：文本语义和图结构怎样分工

原综述将LLM角色分为Predictor、Encoder、Aligner，图场景pure/text-attributed/text-paired是另一条分类轴。Encoder可先把节点文本编码成向量，GNN再沿边传播，分别处理语义与关系；Predictor把序列化图、结构摘要或图表示交给语言模型预测；Aligner通过伪标签、蒸馏或对比损失对齐语言与图表示。

Aligner并不必然意味着两模型端到端训练。信息通路必须按实际架构画清：文本是否含目标答案，边是否来自未来事件，图信息究竟进入哪些模块。GraphRAG是一类检索组织方式，图检索本身不要求训练GNN，这一界限见仓库官方网页核查；本页以原综述角色为主，不把GraphRAG当某一种GNN。

**原文定位**：Jin et al. 2024，p4–5 §3.1–3.2，p8–10 图3–5。

- Bowen Jin, Gang Liu, Chi Han, Meng Jiang, Heng Ji, Jiawei Han，Large Language Models on Graphs: A Comprehensive Survey，IEEE TKDE 36(12):8622–8642, 2024（2024）。[原始记录](https://arxiv.org/abs/2312.02783v4) · [本地PDF](../source/papers/llm-graphs2024.pdf)

## 34 · 方法对照：先定位缺少哪种信息，再选择模型

模型选择先检查数据与任务约束。GCN适合作为浅层归一化传播基线，但关系是否支持平滑需要验证。SAGE处理依赖采样和共享新节点编码；GAT在现有边内学习特征相关权重；RGCN按关系类型区分消息；GIN研究聚合计数和单射条件；EGNN加入几何变换约束；TGN按事件历史与可见时间组织记忆；GraphGPS为局部、全局和结构编码的组合框架。

它们不是按年份递增的通用优劣排名。每次替换模块要问想保留什么信息，损失函数是否真的奖励这种信息，评估划分是否检验所声称的能力。

**原文定位**：各论文方法章节；本表为基于机制的教学归纳。

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Hamilton, Ying, Leskovec，Inductive Representation Learning on Large Graphs，NeurIPS（2017）。[原始记录](https://arxiv.org/abs/1706.02216) · [本地PDF](../source/papers/graphsage2017.pdf)

- Velickovic et al.，Graph Attention Networks，ICLR（2018）。[原始记录](https://arxiv.org/abs/1710.10903) · [本地PDF](../source/papers/gat2018.pdf)

- Schlichtkrull et al.，Modeling Relational Data with Graph Convolutional Networks，ESWC（2018）。[原始记录](https://arxiv.org/abs/1703.06103) · [本地PDF](../source/papers/rgcn2018.pdf)

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[原始记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)

- Satorras, Hoogeboom, Welling，E(n) Equivariant Graph Neural Networks，ICML（2021）。[原始记录](https://arxiv.org/abs/2102.09844) · [本地PDF](../source/papers/egnn2021.pdf)

- Rampasek et al.，Recipe for a General, Powerful, Scalable Graph Transformer，NeurIPS（2022）。[原始记录](https://arxiv.org/abs/2205.12454) · [本地PDF](../source/papers/graphgps2022.pdf)

## 35 · 原始论文的阅读路径与溯源入口

完整论文索引列26条记录，其中25份PDF已在本地保存，Gori2005全文未取得；不将索引记录冒充已读全文。manifest记录原始URL、下载时间、版本、页数、文件长度与SHA256，verify-sources只读核对完整性。Scarselli2009为学术镜像原件，其来源单独记录。arXiv版本不一定与期刊排版分页一致，本讲页码均指仓库PDF物理页。

用户提供的15页入门PPT保留原字节，作为内容组织参考，不作为独立事实或操作指令。逐页讲稿把机制、推导、作者证据及适用边界分开，实验原始表仍可按以下定位回原文阅读。本次不复现实验，作者报告与本讲构造的图例不混用。

**原文定位**：原件记录：source/catalog.json、manifest.json；完整索引：source/paper-index.md。

- Gilmer et al.，Neural Message Passing for Quantum Chemistry，ICML（2017）。[原始记录](https://arxiv.org/abs/1704.01212) · [本地PDF](../source/papers/mpnn2017.pdf)

- Kipf and Welling，Semi-Supervised Classification with Graph Convolutional Networks，ICLR（2017）。[原始记录](https://arxiv.org/abs/1609.02907) · [本地PDF](../source/papers/gcn2017.pdf)

- Xu et al.，How Powerful are Graph Neural Networks?，ICLR（2019）。[原始记录](https://arxiv.org/abs/1810.00826) · [本地PDF](../source/papers/gin2019.pdf)
