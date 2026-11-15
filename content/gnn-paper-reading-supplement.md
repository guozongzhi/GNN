# GNN 原理与关键论文：融合补充版逐页讲稿

32 页融合补充版。结合用户提供的 15 页入门 PPT，保留论文精读密度，不含 Demo。新增论文核验于 2026-11-15；既有部署资料沿用 2026-11-10 核查。论文数值为作者报告。原件位于 `source/papers/`，定位采用本地 PDF 的物理页序。

## 01 · GNN 原理与关键论文

内容由原始论文与既有应用核查记录整理。封面沿用 AI 生成概念插图，不表示某篇论文的结构或结果。论文原件与版本见 source/manifest.json。

参考输入：图神经网络（GNN）入门：原理、里程碑与应用.pptx；15页；SHA-256 19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。输入文件保持不变。仅采用问题组织与示意方向，事实以下列原文为准。
融合补充版共32页，新增8页；不含Demo。

## 02 · 为什么用图：关系、邻域与节点重编号

来源：MPNN https://arxiv.org/abs/1704.01212 。下图为六节点无向教学图的邻接数据可视化。颜色仅区分示例对象，橙色A为目标。相同图在后续各页保持相同节点位置。

Gilmer et al. (2017). Neural Message Passing for Quantum Chemistry. ICML.
原始记录：https://arxiv.org/abs/1704.01212
本地原件：[mpnn2017.pdf](../source/papers/mpnn2017.pdf)
定位：PDF 第 3 页，§2，式 (1)–(3)。
MPNN 把多种既有图模型统一为消息函数 M、节点更新函数 U 和整图读出 R。消息可依赖中心节点、邻居节点和边特征。对邻居求和使节点编号变化时表示同步重排；整图性质预测的 readout 必须对节点排列不变。此处省略层索引和部分上下标以便阅读，N(v) 是邻居集合。论文主要研究分子性质回归，原子是节点，化学键或距离等作为边信息。它是模型框架，不是只有一套固定网络结构。
本地原件：source/papers/zhou-survey2021.pdf
原始记录：https://arxiv.org/abs/1812.08434v6
原文定位：PDF 第1–3页，§1、图1、§2
规则网格和一般关系图均可建模为图。一般图邻居数量可变，编号不应改变实体对应的预测。以下置换公式为教学推导。
参考输入：图神经网络（GNN）入门：原理、里程碑与应用.pptx；15页；SHA-256 19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。输入文件保持不变。仅采用问题组织与示意方向，事实以下列原文为准。

## 03 · 图、表示与预测：GNN 的统一记号

来源：MPNN https://arxiv.org/abs/1704.01212 。下图为六节点无向教学图的邻接数据可视化。颜色仅区分示例对象，橙色A为目标。相同图在后续各页保持相同节点位置。

GCN: https://arxiv.org/abs/1609.02907。邻接约定A[i,j]表示j向i传播。六节点图无向，矩阵对称；此页A未加自环。特征矩阵只是教学示意，不是标签。

GCN: https://arxiv.org/abs/1609.02907。本页是六节点环图上的数值扩散。每个节点原始度2，加自环后度3，因此S=(A+I)/3。初始只有A=1，其他为0。依次显示x、Sx、S²x，W=1且无非线性，不含训练。橙色表示当前非零值。

Gilmer et al. (2017). Neural Message Passing for Quantum Chemistry. ICML.
原始记录：https://arxiv.org/abs/1704.01212
本地原件：[mpnn2017.pdf](../source/papers/mpnn2017.pdf)
定位：PDF 第 3 页，§2，式 (1)–(3)。
MPNN 把多种既有图模型统一为消息函数 M、节点更新函数 U 和整图读出 R。消息可依赖中心节点、邻居节点和边特征。对邻居求和使节点编号变化时表示同步重排；整图性质预测的 readout 必须对节点排列不变。此处省略层索引和部分上下标以便阅读，N(v) 是邻居集合。论文主要研究分子性质回归，原子是节点，化学键或距离等作为边信息。它是模型框架，不是只有一套固定网络结构。

## 04 · 从业务到模型：三类任务与各自的输出头

GCN: https://arxiv.org/abs/1609.02907。本页是六节点环图上的数值扩散。每个节点原始度2，加自环后度3，因此S=(A+I)/3。初始只有A=1，其他为0。依次显示x、Sx、S²x，W=1且无非线性，不含训练。橙色表示当前非零值。

Gilmer et al. (2017). Neural Message Passing for Quantum Chemistry. ICML.
原始记录：https://arxiv.org/abs/1704.01212
本地原件：[mpnn2017.pdf](../source/papers/mpnn2017.pdf)
定位：PDF 第 3 页，§2，式 (1)–(3)。
MPNN 把多种既有图模型统一为消息函数 M、节点更新函数 U 和整图读出 R。消息可依赖中心节点、邻居节点和边特征。对邻居求和使节点编号变化时表示同步重排；整图性质预测的 readout 必须对节点排列不变。此处省略层索引和部分上下标以便阅读，N(v) 是邻居集合。论文主要研究分子性质回归，原子是节点，化学键或距离等作为边信息。它是模型框架，不是只有一套固定网络结构。

Schlichtkrull et al. (2018). Modeling Relational Data with Graph Convolutional Networks. ESWC.
原始记录：https://arxiv.org/abs/1703.06103
本地原件：[rgcn2018.pdf](../source/papers/rgcn2018.pdf)
定位：PDF 第 2–3 页，式 (2)–(4)，图 2。
R-GCN 将邻居按关系类型分组，对每种关系使用 W_r 变换，再归一化求和并加入自身变换。知识图谱中的关系方向很重要，原文加入逆关系与自环。关系很多时，直接使用完整 W_r 会产生大量参数；basis decomposition 让 W_r=∑_b a_rb V_b，共享基矩阵，block decomposition 则使用块对角结构。实体分类使用节点输出，链路预测还需要关系解码器；原文采用 DistMult。图数据库或知识图谱应用并不自动等于使用 R-GCN。
本地原件：source/papers/zhou-survey2021.pdf
原始记录：https://arxiv.org/abs/1812.08434v6
原文定位：PDF 第3–4页 §3；第14–18页表3与§8
表中公式为简化教学实例。链路任务需定义正例、负样本及解码器，整图任务需定义readout，不可只换分类层就忽略协议。
参考输入：图神经网络（GNN）入门：原理、里程碑与应用.pptx；15页；SHA-256 19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。输入文件保持不变。仅采用问题组织与示意方向，事实以下列原文为准。

## 05 · 关键演进：从固定点到分层传播与科学应用

精选时间线。Gori2005 DOI10.1109/IJCNN.2005.1555942与Scarselli2009 DOI10.1109/TNN.2008.2005605；Bruna2014 https://arxiv.org/abs/1312.6203；ChebNet2016 https://arxiv.org/abs/1606.09375；GCN2017 https://arxiv.org/abs/1609.02907 与MPNN https://arxiv.org/abs/1704.01212；GIN2019 https://arxiv.org/abs/1810.00826；EGNN2021 https://arxiv.org/abs/2102.09844；GraphGPS2022 https://arxiv.org/abs/2205.12454；GraphCast2023 https://arxiv.org/abs/2212.12794；GNoME2023 DOI10.1038/s41586-023-06735-9。按主要发表年份，非首次预印本年份。

Scarselli et al. (2009). The Graph Neural Network Model. IEEE TNN.
原始记录：https://doi.org/10.1109/TNN.2008.2005605
本地原件：[scarselli2009.pdf](../source/papers/scarselli2009.pdf)
定位：PDF 第 3–5 页，§II-A 与固定点讨论。
每个节点有状态，状态依赖本节点、边与邻居的信息。全图状态可概括为 h=Fθ(h,x)。原文通过关于状态的压缩映射条件，保证固定点的存在、唯一性和迭代收敛。这里用 h、x 统一记号，不照搬原文的 x 状态符号。与现代固定层数前馈 GNN 相比，这一框架强调共享转移函数的迭代与收敛约束。2005 年 Gori 等论文是早期记录，本包未取得其全文；本页细节依据 Scarselli 2009。

## 06 · Bruna → ChebNet → GCN：谱卷积的局部化

Bruna et al. (2014). Spectral Networks and Deep Locally Connected Networks on Graphs. ICLR.
原始记录：https://arxiv.org/abs/1312.6203
本地原件：[bruna2014.pdf](../source/papers/bruna2014.pdf)
定位：谱卷积章节。
用图拉普拉斯 L=UΛUᵀ 的特征向量充当图傅里叶基。谱滤波写作 Ugθ(Λ)Uᵀx；基与图结构有关，显式特征分解及稠密基运算昂贵。
Defferrard, Bresson, Vandergheynst (2016). Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering. NeurIPS.
原始记录：https://arxiv.org/abs/1606.09375
本地原件：[chebnet2016.pdf](../source/papers/chebnet2016.pdf)
定位：PDF 第 2–3 页，§2.1，式 (2)–(5)，图 1。
以切比雪夫多项式参数化谱滤波，通过递推在稀疏图上计算，不必显式形成 U。最高多项式次数为 K 时，传播支持范围不超过 K 跳；本页写成 k=0…K，原论文另有 K 个系数、最高 K−1 次的记号。忽略通道等因子时复杂度随 K|E| 线性增长。原图说明原论文还有图粗化与池化；它们不是下方公式的全部内容。

Kipf and Welling (2017). Semi-Supervised Classification with Graph Convolutional Networks. ICLR.
原始记录：https://arxiv.org/abs/1609.02907
本地原件：[gcn2017.pdf](../source/papers/gcn2017.pdf)
定位：PDF 第 2–3 页，式 (2)、(6)–(8)。
GCN 从切比雪夫一阶近似出发，近似最大特征值并约束两个系数，再引入 renormalization trick。图先加自环，再按新度数做对称归一化。S 的每行不必和为 1，因此它不等于普通均值。左表为三节点链的 S；右例输入为 [1,2,0]，计算 A 的聚合值。W=1，无非线性，只用于手算说明。

## 07 · GCN：归一化、两层模型与半监督损失

Kipf and Welling (2017). Semi-Supervised Classification with Graph Convolutional Networks. ICLR.
原始记录：https://arxiv.org/abs/1609.02907
本地原件：[gcn2017.pdf](../source/papers/gcn2017.pdf)
定位：PDF 第 2–3 页，式 (2)、(6)–(8)。
GCN 从切比雪夫一阶近似出发，近似最大特征值并约束两个系数，再引入 renormalization trick。图先加自环，再按新度数做对称归一化。S 的每行不必和为 1，因此它不等于普通均值。左表为三节点链的 S；右例输入为 [1,2,0]，计算 A 的聚合值。W=1，无非线性，只用于手算说明。

Kipf and Welling (2017). Semi-Supervised Classification with Graph Convolutional Networks. ICLR.
原始记录：https://arxiv.org/abs/1609.02907
本地原件：[gcn2017.pdf](../source/papers/gcn2017.pdf)
定位：PDF 第 3–4 页，式 (9)、(10)，图 1。
两层模型 Z=softmax(S ReLU(S X W0) W1)。softmax 逐节点作用，交叉熵仅在有训练标签的节点上求和。传导式设定可以看到同图未标注节点的特征与边，不等于可以使用测试标签。原图右侧是作者在 Cora 上使用约 5% 标签得到的隐藏表示 t-SNE，可视化不等于分类准确率。GCN 算子有共享参数，不能把原文传导式评估误读为该算子在数学上绝不能用于新节点。

## 08 · GCN 手算：三节点链的一次完整向量传播

Kipf and Welling (2017). Semi-Supervised Classification with Graph Convolutional Networks. ICLR.
原始记录：https://arxiv.org/abs/1609.02907
本地原件：[gcn2017.pdf](../source/papers/gcn2017.pdf)
定位：PDF 第 2–3 页，式 (2)、(6)–(8)。
GCN 从切比雪夫一阶近似出发，近似最大特征值并约束两个系数，再引入 renormalization trick。图先加自环，再按新度数做对称归一化。S 的每行不必和为 1，因此它不等于普通均值。左表为三节点链的 S；右例输入为 [1,2,0]，计算 A 的聚合值。W=1，无非线性，只用于手算说明。

Kipf and Welling (2017). Semi-Supervised Classification with Graph Convolutional Networks. ICLR.
原始记录：https://arxiv.org/abs/1609.02907
本地原件：[gcn2017.pdf](../source/papers/gcn2017.pdf)
定位：PDF 第 3–4 页，式 (9)、(10)，图 1。
两层模型 Z=softmax(S ReLU(S X W0) W1)。softmax 逐节点作用，交叉熵仅在有训练标签的节点上求和。传导式设定可以看到同图未标注节点的特征与边，不等于可以使用测试标签。原图右侧是作者在 Cora 上使用约 5% 标签得到的隐藏表示 t-SNE，可视化不等于分类准确率。GCN 算子有共享参数，不能把原文传导式评估误读为该算子在数学上绝不能用于新节点。
参考输入：图神经网络（GNN）入门：原理、里程碑与应用.pptx；15页；SHA-256 19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。输入文件保持不变。仅采用问题组织与示意方向，事实以下列原文为准。
教学例，非论文实验。三节点链加自环后度为(2,3,2)，S22=1/3。参考PPT的0.50自环权重应修正；W=I、ReLU下，中心输出[1.2247,1.4082]。

## 09 · GCN：作者结果、随机划分与评价协议

Kipf and Welling (2017). Semi-Supervised Classification with Graph Convolutional Networks. ICLR.
原始记录：https://arxiv.org/abs/1609.02907
本地原件：[gcn2017.pdf](../source/papers/gcn2017.pdf)
定位：PDF 第 6–7 页，§5.2 与表 2。
引用网络仅使用每类 20 个训练标签，另外使用 500 个验证节点调参。默认划分 GCN 在 Citeseer/Cora/Pubmed 上分别为 70.3/81.5/79.0% Accuracy；论文还报告随机划分为 67.9±0.5、80.1±0.5、78.9±0.7%。默认 GCN 数值是 100 次随机权重初始化的均值，随机划分行来自作者另外的实验协议。不能把两行差异解释为同一组重复实验的置信区间。Planetoid* 是原文表 2 引用的相应数据集最佳变体。所有数值为作者报告的历史结果，本次没有复现。

## 10 · MPNN：消息、状态更新与图级读出的设计空间

Gilmer et al. (2017). Neural Message Passing for Quantum Chemistry. ICML.
原始记录：https://arxiv.org/abs/1704.01212
本地原件：[mpnn2017.pdf](../source/papers/mpnn2017.pdf)
定位：PDF 第 3 页，§2，式 (1)–(3)。
MPNN 把多种既有图模型统一为消息函数 M、节点更新函数 U 和整图读出 R。消息可依赖中心节点、邻居节点和边特征。对邻居求和使节点编号变化时表示同步重排；整图性质预测的 readout 必须对节点排列不变。此处省略层索引和部分上下标以便阅读，N(v) 是邻居集合。论文主要研究分子性质回归，原子是节点，化学键或距离等作为边信息。它是模型框架，不是只有一套固定网络结构。

Gilmer et al. (2017). Neural Message Passing for Quantum Chemistry. ICML.
原始记录：https://arxiv.org/abs/1704.01212
本地原件：[mpnn2017.pdf](../source/papers/mpnn2017.pdf)
定位：PDF 第 3–5 页，§2、§3 及 readout 讨论。
原论文将多个模型实例化为不同的 M、U、R，并在 QM9 上研究分子性质预测。边网络可以用边属性产生作用于邻居状态的变换；节点更新可以使用 GRU 等函数；整图读出比较求和与 set2set 等集合函数。不能用一种均值聚合代替所有 MPNN，也不能把节点读出自动当成整图预测。
Battaglia et al. (2018). Relational inductive biases, deep learning, and graph networks. arXiv.
原始记录：https://arxiv.org/abs/1806.01261
本地原件：[gn2018.pdf](../source/papers/gn2018.pdf)
定位：Graph Network block 定义。
Graph Networks 进一步显式组织边、节点与全局状态的更新。这个扩展是模型组织方式，不是 MPNN 论文已经包含的唯一标准实现。

## 11 · GraphSAGE：采样邻域与共享聚合函数

Hamilton, Ying, Leskovec (2017). Inductive Representation Learning on Large Graphs. NeurIPS.
原始记录：https://arxiv.org/abs/1706.02216
本地原件：[graphsage2017.pdf](../source/papers/graphsage2017.pdf)
定位：PDF 第 2、4–5 页，图 1，算法 1，§3.2–3.3。
GraphSAGE 学习共享的邻域聚合函数，区别于直接为每个已知节点学习独立向量。对新节点仍需要可用特征和邻接关系。每层采样固定数量邻居，控制计算展开；批量成本仍随各层采样数的乘积增长。典型更新把自身表示与聚合结果拼接后做变换，并有 L2 归一化。论文比较 mean、pooling、LSTM 聚合器；LSTM 使用随机邻居顺序，并不严格置换不变。原文既支持无监督图损失，也支持监督损失。

## 12 · GraphSAGE：新节点与新图需要不同的留出验证

Hamilton, Ying, Leskovec (2017). Inductive Representation Learning on Large Graphs. NeurIPS.
原始记录：https://arxiv.org/abs/1706.02216
本地原件：[graphsage2017.pdf](../source/papers/graphsage2017.pdf)
定位：PDF 第 7–8 页，表 1，§4.1–4.2。
柱状图选用表 1 的监督 GraphSAGE-mean 与 raw features。Citation 的 micro-F1 为 0.820 对 0.575；Reddit 为 0.950 对 0.585；PPI 为 0.598 对 0.422。Citation 按年份留出新论文，Reddit 按时间留出新帖子，PPI 留出整张图。PPI 是多标签节点分类；不能把不同数据集 micro-F1 的绝对值拿来跨任务比较难度。也不能据此把 GCN 的传播算子一概归为无法归纳。数值均为作者原表结果，本次没有复现。

## 13 · GAT：邻域注意力公式与同架构消融

Velickovic et al. (2018). Graph Attention Networks. ICLR.
原始记录：https://arxiv.org/abs/1710.10903
本地原件：[gat2018.pdf](../source/papers/gat2018.pdf)
定位：PDF 第 3–4 页，式 (1)–(6)，图 1。
GAT 首先用共享 W 变换节点特征，然后对中心与邻居的拼接计算 LeakyReLU 注意力分数。softmax 只在给定邻域内归一化，原文实验包括自环。多头注意力在隐藏层拼接，在最终层平均。注意力沿图中的边计算，并不默认所有节点两两互看；这与普通全连接 Transformer 注意力范围不同。权重可以用来查看模型如何分配信息，但不是因果解释。

Velickovic et al. (2018). Graph Attention Networks. ICLR.
原始记录：https://arxiv.org/abs/1710.10903
本地原件：[gat2018.pdf](../source/papers/gat2018.pdf)
定位：PDF 第 8–9 页，§3，表 2、3。
表 3 在 PPI 上给出相同架构的常量注意力 Const-GAT 与 GAT：micro-F1 分别为 0.934±0.006 和 0.973±0.002；均值差为 0.039，即 3.9 个百分点。原文报告 10 次运行，± 为标准差。这个消融比直接比较不同宽度、层数或邻域处理方式的架构更能隔离自适应权重的贡献，但依然只适用于作者这一实验设定。原表 2 的 Cora/Citeseer/Pubmed GAT Accuracy 为 83.0±0.7/72.5±0.7/79.0±0.3%。数值为作者原论文报告，本次未重新复现。

## 14 · R-GCN：按关系聚合与关系参数共享

Schlichtkrull et al. (2018). Modeling Relational Data with Graph Convolutional Networks. ESWC.
原始记录：https://arxiv.org/abs/1703.06103
本地原件：[rgcn2018.pdf](../source/papers/rgcn2018.pdf)
定位：PDF 第 2–3 页，式 (2)–(4)，图 2。
R-GCN 将邻居按关系类型分组，对每种关系使用 W_r 变换，再归一化求和并加入自身变换。知识图谱中的关系方向很重要，原文加入逆关系与自环。关系很多时，直接使用完整 W_r 会产生大量参数；basis decomposition 让 W_r=∑_b a_rb V_b，共享基矩阵，block decomposition 则使用块对角结构。实体分类使用节点输出，链路预测还需要关系解码器；原文采用 DistMult。图数据库或知识图谱应用并不自动等于使用 R-GCN。

## 15 · 异质、异配与动态：三个彼此独立的维度

Schlichtkrull et al. (2018). Modeling Relational Data with Graph Convolutional Networks. ESWC.
原始记录：https://arxiv.org/abs/1703.06103
本地原件：[rgcn2018.pdf](../source/papers/rgcn2018.pdf)
定位：PDF 第 2–3 页，式 (2)–(4)，图 2。
R-GCN 将邻居按关系类型分组，对每种关系使用 W_r 变换，再归一化求和并加入自身变换。知识图谱中的关系方向很重要，原文加入逆关系与自环。关系很多时，直接使用完整 W_r 会产生大量参数；basis decomposition 让 W_r=∑_b a_rb V_b，共享基矩阵，block decomposition 则使用块对角结构。实体分类使用节点输出，链路预测还需要关系解码器；原文采用 DistMult。图数据库或知识图谱应用并不自动等于使用 R-GCN。

过平滑论文：https://arxiv.org/abs/1801.07606。异配性 https://arxiv.org/abs/2006.11468 。过挤压 https://arxiv.org/abs/2006.05205。左图为六节点规则环的纯扩散x,Sx,S²x,S⁶x，W=1、无非线性，不是完整GCN训练，也不据此断言所有GNN深度增加必然失效。S为对称且行和1的规则图传播，重复扩散使数值趋同。
本地原件：[tgn2020.pdf](../source/papers/tgn2020.pdf)
原始记录：https://arxiv.org/abs/2006.10637v3
原文定位：PDF 第2–4页 §3–3.2
事件流建模、记忆和时间可见性。下表为跨论文教学比较，异质与异配不是同义词。

## 16 · GIN：重复计数、单射聚合与 1-WL 上界

Xu et al. (2019). How Powerful are Graph Neural Networks?. ICLR.
原始记录：https://arxiv.org/abs/1810.00826
本地原件：[gin2019.pdf](../source/papers/gin2019.pdf)
定位：PDF 第 5–7 页，Lemma 5、图 2、图 3。
邻域是多重集，同一类型可以出现多次。教学例令 a=[1,0]、b=[0,1]：{a,b} 与 {a,a,b,b} 的均值均为 [0.5,0.5]，max 均为 [1,1]，但求和是 [1,1] 与 [2,2]。这展示重复计数的丢失，不证明任意原始数值直接求和都是单射，例如标量集合 {1,3} 与 {2,2} 也会碰撞。原论文通过适当编码、可数特征域和有界多重集等条件讨论可区分性。原图是论文图 3 的示意，不是本地训练结果。

Xu et al. (2019). How Powerful are Graph Neural Networks?. ICLR.
原始记录：https://arxiv.org/abs/1810.00826
本地原件：[gin2019.pdf](../source/papers/gin2019.pdf)
定位：PDF 第 4–6 页，Theorem 3、Corollary 6、式 (4.1)–(4.2)。
典型 GIN 更新为 MLP((1+ε)h_v+∑_u h_u)。ε 可以学习或固定；中心节点与邻居在组合中有区别。图级输出可将各层的 sum readout 拼接。原文在可数输入特征等假设下，若聚合与 readout 足够可区分且层数足够，能达到 1-WL 的结构判别能力。1-WL 迭代聚合邻居颜色并为不同多重集重新着色；它不能区分所有非同构图，因此 GIN 也不能。表达力理论说明可表示的区别，不保证有限宽度、实际训练或任意任务精度。

## 17 · PinSage：大规模推荐中的采样、批次与推理

Ying et al. (2018). Graph Convolutional Neural Networks for Web-Scale Recommender Systems. KDD.
原始记录：https://arxiv.org/abs/1806.01973
本地原件：[pinsage2018.pdf](../source/papers/pinsage2018.pdf)
定位：PDF 第 1–4 页，图 1，§3。
Pinterest 的 PinSage 使用 pin–board 二部图及内容特征，在短随机游走形成的邻域上聚合。访问频率提供重要性权重，CPU 生产者准备邻域与特征，GPU 消费 mini-batch，离线 MapReduce 推理生成大规模嵌入。原论文报告在 30 亿节点、180 亿边图上的生产应用，这些是 2018 年论文的历史规模，不代表当前线上架构。困难负样本和课程式训练属于论文的重要工程设计。此页原图示例的局部计算图并不是完整生产图。

## 18 · LightGCN：协同过滤中的结构简化及其边界

He et al. (2020). LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation. SIGIR.
原始记录：https://arxiv.org/abs/2002.02126
本地原件：[lightgcn2020.pdf](../source/papers/lightgcn2020.pdf)
定位：PDF 第 2–4 页，表 1，图 2，式 (3)–(8)。
LightGCN 针对用户–物品协同过滤，输入是可训练的 ID embeddings。传播中去掉特征变换、非线性和显式自环，只保留对称归一化邻居求和；把第 0…K 层表示加权组合，再以内积评分并用推荐目标训练。没有每层 W 不等于没有可学习参数：第 0 层嵌入仍需要学习。论文在相同数据划分与评价协议下通过 NGCF 消融提出简化，不能推广为所有有丰富特征的图任务都应该删非线性。

## 19 · TGN：从静态邻接转向带时间戳的事件流

本地原件：[tgn2020.pdf](../source/papers/tgn2020.pdf)
原始记录：https://arxiv.org/abs/2006.10637v3
原文定位：PDF 第2–5页 §3、图1–2；第7页 §5、表2
Rossi et al., 2020，arXiv:2006.10637v3。本文为预印本与ICML2020 GRL+工作坊工作，不标为ICML主会论文。事件流、节点记忆、消息、聚合、记忆更新、embedding模块；上一批消息更新记忆后预测当前批，随后缓存当前原始消息以避免泄漏。70/15/15 chronological split，10次运行均值。

## 20 · 局部消息传递的三种限制及诊断区别

过平滑论文：https://arxiv.org/abs/1801.07606。异配性 https://arxiv.org/abs/2006.11468 。过挤压 https://arxiv.org/abs/2006.05205。左图为六节点规则环的纯扩散x,Sx,S²x,S⁶x，W=1、无非线性，不是完整GCN训练，也不据此断言所有GNN深度增加必然失效。S为对称且行和1的规则图传播，重复扩散使数值趋同。

## 21 · EGNN：用距离与相对位置保证几何等变

Satorras, Hoogeboom, Welling (2021). E(n) Equivariant Graph Neural Networks. ICML.
原始记录：https://arxiv.org/abs/2102.09844
本地原件：[egnn2021.pdf](../source/papers/egnn2021.pdf)
定位：PDF 第 2–3 页，式 (3)–(6)，§3.1。
EGNN 的消息使用平方距离 ||x_i−x_j||²，与标量节点特征及边属性一起输入 φ_e。坐标更新由相对位置向量的标量加权和组成，保证平移、旋转和反射等变；标量特征保持不变。下方公式省略层索引和常数 C。能量等标量预测通常需要不变性，坐标或向量预测需要等变性，两者不能混淆。原文标准 E(n) 结构包含反射对称性，不能自动解决依赖手性的目标；全连接构图也可能带来二次规模成本。原文研究 N-body、图自编码与 QM9 等任务。

## 22 · GraphGPS：位置编码、局部消息与全局交互

Rampasek et al. (2022). Recipe for a General, Powerful, Scalable Graph Transformer. NeurIPS.
原始记录：https://arxiv.org/abs/2205.12454
本地原件：[graphgps2022.pdf](../source/papers/graphgps2022.pdf)
定位：PDF 第 2–5 页，图 1，§3.1–3.3。
GPS 蓝图结合位置/结构编码、局部 MPNN 与全局注意力。局部模块处理邻接和边信息，全局模块提供非局部交互，PE/SE 为 Transformer 提供图位置与结构信号。图 1 的 GPS layer 可组合 GINE、GatedGCN、PNA 与 Transformer、Performer、BigBird 等。普通全注意力是 O(N²)，采用合适的线性注意力模块才对应线性规模的论述，且编码计算等预处理代价需要另算。不能把 GraphGPS 当成只有一个固定结构、任何配置都线性、或无条件突破全部图表达力限制。

## 23 · GNN × LLM：按语言模型的角色拆解接口

本地原件：source/papers/llm-graphs2024.pdf
原始记录：https://arxiv.org/abs/2312.02783v4
原文定位：PDF 第4–5页 §3.2、图2；第7–10页 §5、图3–5
Jin et al., TKDE 2024。准确分类为LLM as Predictor / Encoder / Aligner；场景分类为pure / text-attributed / text-paired graphs。Aligner包含预测对齐和潜在空间对齐。GraphRAG边界为本页分析：图检索本身不要求训练GNN。
参考输入：图神经网络（GNN）入门：原理、里程碑与应用.pptx；15页；SHA-256 19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。输入文件保持不变。仅采用问题组织与示意方向，事实以下列原文为准。

## 24 · 核心论文对照：改变了哪个计算环节

教学比较依据 GCN 式 (2)、GraphSAGE 算法 1、GAT 式 (1)–(6)、GIN 式 (4.1)、R-GCN 式 (2) 和 GraphGPS 图 1。原始 PDF 均位于 source/papers/。该表比较设计选择，不是准确率、计算量或年代的统一排名。每个条目省略了任务头、训练损失与具体实现。

## 25 · DCRNN：把路网传播与时间递推结合起来

本地原件：[dcrnn2018.pdf](../source/papers/dcrnn2018.pdf)
原始记录：https://arxiv.org/abs/1707.01926v3
原文定位：PDF 第2–4页 §2、式(2)–(4)、图2；第5页 §4、表1；第7页 §4.3
Li, Yu, Shahabi & Liu, ICLR2018，1707.01926v3。双向随机游走（方向转移矩阵）与DCGRU；encoder-decoder以及scheduled sampling。节点为路网传感器，图按距离构造。METR-LA 207、PEMS-BAY 325节点，5分钟窗口；70%训练、10%验证、20%测试。表格仅摘取METR-LA，MAE为mph；作者结果。

## 26 · GraphCast：多尺度球面图与 90.3% 的评价口径

Lam et al. (2023). Learning skillful medium-range global weather forecasting. Science.
原始记录：https://arxiv.org/abs/2212.12794
本地原件：[graphcast2023.pdf](../source/papers/graphcast2023.pdf)
定位：PDF 第 2–4 页，表 1，图 1。
输入为当前与 6 小时前两个天气状态，预测 6 小时后的状态，再自回归滚动到更远时刻。Encoder 将经纬度网格局部区域映射到球面 multi-mesh，Processor 在多分辨率边的并集上传播，Decoder 把表示映回规则网格。multi-mesh 包含最细尺度的 40,962 个节点与多个尺度的边，兼顾局部与远程交互。本页图 1 的原图包含模型各阶段，不能将其误读为某个实时服务的当前架构。

Lam et al. (2023). Learning skillful medium-range global weather forecasting. Science.
原始记录：https://arxiv.org/abs/2212.12794
本地原件：[graphcast2023.pdf](../source/papers/graphcast2023.pdf)
定位：PDF 第 2、4–6 页，Verification methods 与 Forecast verification results。
原论文报告在 1,380 个验证目标中的 90.3% 优于 HRES；89.9% 的目标达到作者显著性条件。目标由变量、气压层和预报提前量组合，不是分类样本，90.3% 也不是预测准确率或误差下降幅度。开发使用 1979–2017 ERA5，再在 2018 年以后的留出数据评估；评价指标包括 RMSE 与 ACC。论文注意对齐 ERA5 和 HRES 的数据同化窗口，并为 HRES 构造独立 ground truth；有长时效比较的初始化安排。单个 TPU v4 上一分钟内生成 10 天预报的结果是推理成本，不包括约四周、32 TPU 的训练。此页只展示作者原文研究结论，不声称当前线上产品性能。

## 27 · GNoME：图网络预测、DFT 验证与主动学习

Merchant et al. (2023). Scaling deep learning for materials discovery. Nature.
原始记录：https://doi.org/10.1038/s41586-023-06735-9
本地原件：[gnome2023.pdf](../source/papers/gnome2023.pdf)
定位：PDF 第 1–2 页，图 1a，Overview of generation and filtration。
GNoME 包含基于结构与基于成分两条候选生成/筛选路径。图网络估计能量或稳定性，DFT 计算验证候选，并将新结果回流到下一轮主动学习。论文称超过 220 万结构相对旧数据的凸包更稳定；考虑新候选相互竞争后的更新凸包包含 381,000 个新条目。这两种数量的参照不同，不能混为全部新增材料都在最终凸包上。计算稳定性是特定能量判据，不等于给出合成路线、实验可合成或商业可用。图为原论文图 1a，而非 AI 生成示意。

## 28 · 应用证据：部署论文、官方披露与科研结论

本页沿用 content/fact-check.md 中核查至 2026-11-10 的应用资料，没有将论文年份当成当前线上状态。Pinterest：PinSage https://arxiv.org/abs/1806.01973；MultiBiSage https://arxiv.org/abs/2205.10666。Google Maps：https://deepmind.google/blog/traffic-prediction-with-advanced-graph-neural-networks/ 与 https://blog.google/products-and-platforms/products/maps/google-maps-101-how-ai-helps-predict-traffic-and-determine-routes/ 为同机构相关证据。GraphCast https://arxiv.org/abs/2212.12794；GNoME https://doi.org/10.1038/s41586-023-06735-9。WeatherNext Graph 原服务弃用事实另见 source/pages/weathernext-deprecation.html 和原始官方链接 https://developers.google.com/weathernext/guides/deprecation；本页不扩展为所有后继天气产品停用。

## 29 · 应用任务地图：实体、关系、目标与验证方式

本页沿用 content/fact-check.md 中核查至 2026-11-10 的应用资料，没有将论文年份当成当前线上状态。Pinterest：PinSage https://arxiv.org/abs/1806.01973；MultiBiSage https://arxiv.org/abs/2205.10666。Google Maps：https://deepmind.google/blog/traffic-prediction-with-advanced-graph-neural-networks/ 与 https://blog.google/products-and-platforms/products/maps/google-maps-101-how-ai-helps-predict-traffic-and-determine-routes/ 为同机构相关证据。GraphCast https://arxiv.org/abs/2212.12794；GNoME https://doi.org/10.1038/s41586-023-06735-9。WeatherNext Graph 原服务弃用事实另见 source/pages/weathernext-deprecation.html 和原始官方链接 https://developers.google.com/weathernext/guides/deprecation；本页不扩展为所有后继天气产品停用。
本地原件：source/papers/zhou-survey2021.pdf
原始记录：https://arxiv.org/abs/1812.08434v6
原文定位：PDF 第14–18页 表3、§8.1–8.2
推荐、化学、交通、知识图谱、视觉等应用归纳。金融风控一行为本文构造的业务建模示意，不作为已部署案例；同样不能将PointNet++一概称为GNN。
本地原件：source/papers/llm-graphs2024.pdf
原始记录：https://arxiv.org/abs/2312.02783v4
原文定位：PDF 第18–19页 §7
图与文本融合的应用方向。
参考输入：图神经网络（GNN）入门：原理、里程碑与应用.pptx；15页；SHA-256 19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。输入文件保持不变。仅采用问题组织与示意方向，事实以下列原文为准。

## 30 · 精读顺序与每篇论文必须回答的问题

阅读建议依据各论文的原始方法和评估章节；它是教学组织方式，不是作者提出的统一标准。建议先精读 GCN 式 (2)、(9)，再用 MPNN 式 (1)–(3) 对齐术语，继而读 GraphSAGE 算法 1、GAT 图 1 与表 3、GIN 的聚合反例和条件。专题按任务选择 PinSage/LightGCN、R-GCN、EGNN、GraphGPS、GraphCast/GNoME。每篇论文的图构造、标签或监督来源、数据划分、指标和消融都应一起读取。

## 31 · 原始资料：版本、定位与证据强度

原始文件：source/papers/；26条catalog记录、25份已取得PDF。Gori2005全文未取得；Scarselli2009来自学术镜像。版本、字节、页数、SHA-256和获取时间见source/manifest.json；source/paper-index.md提供原始记录和本地链接。旧资料核验于2026-11-10，新增5篇核验于2026-11-15。用户提供PPT原件位于source/reference-decks/，内容对应及修正见content/ppt-supplement-notes.md。此页为原生资料索引表。

## 32 · 参考论文索引

共26条论文索引和25份本地PDF。题名、作者、发表口径、原始URL、文件身份及缺口分别见source/catalog.json、source/paper-index.md和source/manifest.json。新增DCRNN、TGN、Wu/Zhou综述与Jin综述。Wu综述预印本2019、期刊2021；Zhou综述卷标2020但接受与发表2021；TGN标工作坊/预印本，不作ICML主会。
