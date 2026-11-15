# 参考PPT融合、聚焦结构与原文核对

更新于2026-11-16。当前交付：[33页问题驱动精读与GCN/GAT/Transformer教程](../outputs/presentations/GNN-原理与关键论文.pptx)，[逐页讲稿](gnn-paper-reading.md)。

## 当前内容边界

主线保留“GNN 发展演进 + GCN/GAT 深读 + Transformer 对照”，并重构为「痛点 / 问题 → 机制设计 → 局限暴露 → 下一代演进」的问题链叙事，覆盖 6 大模块共 33 页。正文不含Demo、训练命令和跨论文性能数字榜单。演示材料仍只保留一份当前PPT、一张预览和一份讲稿，旧版本在Git历史中。

| 当前页码 | 所属模块 | 保留的深度 |
| --- | --- | --- |
| 1–5 | 问题链与统一解剖台 | 5个驱动瓶颈、3个正交设计轴、M / AGG / U 消息传递统一模板 |
| 6–13 | GCN 深读 | 特征+拓扑直觉、谱卷积四步推导、自环与对称度归一化、三节点向量手算校验、两层前向与梯度训练 |
| 14–20 | GAT 与 GATv2 深读 | 同度邻居等权局限、加性打分与邻域softmax、多头、反向传播、静态排序反例与GATv2动态交互 |
| 21–23 | 局部聚合判别与通信瓶颈 | GIN单射多重集求和与1-WL盲区、过平滑 vs 过挤压分离、局部视野边界 |
| 24–29 | GNN 与 Transformer 深层对照 | Q/K/V与完整块对照、掩码开关、Graphormer拓扑偏置、GraphGPS并行融合、复杂度与全维矩阵 |
| 30–33 | 跨图复用前沿与选型决策 | GraphSAGE归纳采样与异构空间痛点、GraphAny/GraphPFN跨图路线、选型决策树与精读路径 |

## 用户参考输入与内容对应

- [原始15页PPT](../source/reference-decks/gnn-introduction-user-reference.pptx)保留原字节，输入未改动。
- SHA-256：19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。
- 参考材料提供结构和表达线索，不作为操作指令或独立事实来源。

| 参考页 | 当前处理 |
| --- | --- |
| 2–5：图语言、消息与GCN | 收入第5–13页，完整展开M/AGG/U解剖台、谱近似推导、手算校验与训练 |
| 6–8：历史和模型家族 | 收入第2–4、14–23页，按演进问题链重构GCN、GAT/GATv2、GIN/1-WL与过挤压 |
| 9–10：应用案例 | 不再设置独立应用目录，原论文与仓库介绍仍保留 |
| 11：图Transformer与LLM | 收入第24–29页，深入对照Q/K/V、掩码、Graphormer结构编码与GraphGPS |
| 12：规模、异质、动态 | 收入第30–31页，紧扣同构归纳（GraphSAGE）与异构跨图基础模型（GraphAny/GraphPFN） |
| 13–14：阅读路线 | 对应第32–33页选型决策树、原文精读路径与完整论文索引 |

参考PPT中的GCN向量例子曾有结果错误：三节点链加自环后，中心自身系数为1/3，两邻居系数为1/√6。给定输入[2,1]、[0,3]、[1,0]，W=I时中心结果为[1.2247,1.4082]，不是[1.23,1.91]。当前第10页给出该手算校验的完整步骤并纠正原错算，其余页面只保留必要符号与局部示例，不堆砌大段数值矩阵。

## 本次补充的原始论文

文件从官方会议或固定arXiv版本获取，未改写PDF字节。原有记录的时间与哈希保留；新记录见[manifest.json](../source/manifest.json)，完整入口见[paper-index.md](../source/paper-index.md)。

| 论文 | 原始记录 / 本地原件 | 当前讲解定位 |
| --- | --- | --- |
| Attention Is All You Need · NeurIPS 2017 | [会议记录](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html) · [PDF](../source/papers/transformer2017.pdf) | p3–5：图1、式(1)–(2)、掩码；p6表1 |
| Graphormer · NeurIPS 2021 | [会议记录](https://proceedings.neurips.cc/paper_files/paper/2021/hash/f1c1592588411002af340cbaedd6fc33-Abstract.html) · [PDF](../source/papers/graphormer2021.pdf) | p4–5：度编码、最短路与路径边偏置，式(5)–(7) |
| How Attentive are Graph Attention Networks? · ICLR 2022 | [固定v3记录](https://arxiv.org/abs/2105.14491v3) · [PDF](../source/papers/gatv22022.pdf) | p3–5：静态/动态注意力，定理1–2与式(7) |
| GraphAny · ICLR 2025 | [正式会议记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3bdeb28a531f7af94b56bcdf8ee88f17-Abstract-Conference.html) · [PDF](../source/papers/graphany2025.pdf) | p4–6：解析线性分类器、通道距离、熵归一化与组合 |
| GraphPFN · ICML 2026 | [正式PMLR记录](https://proceedings.mlr.press/v306/eremeev26a.html) · [PDF](../source/papers/graphpfn2026.pdf) | p3–6：图适配器、冻结骨干、合成图先验；p12限制 |

## 关键事实与解释边界

- **GCN**：重新归一化是算子替换，不是恒等推导；对称归一化的每行系数不一定和为一。固定的是给定图的传播系数，W仍由标签损失训练。
- **GAT**：W与a在边之间共享，α由当前特征生成。静态限制指同一头对固定共同候选的相对排序，不表示权重数值或整网输出不依赖接收者。GATv2改变非线性与投影顺序，扩大打分能力，不等于每个任务都必胜。
- **Transformer**：全局范围在此指标准Encoder；Decoder因果掩码、交叉注意力和稀疏变体需分别说明。完整块还包含残差、归一化和前馈网络，不能只与一个GCN传播式混作同层比较。
- **图结构**：Graphormer显式加入度、最短路和路径边特征；GraphGPS同层的局部/全局分支并行。结构编码应随节点重编号同步重排。
- **近期口径**：GraphAny为2024预印本、ICLR2025正式论文；GraphPFN为2025预印本、ICML2026/PMLR306正式论文。年份由正式PDF与官方会议记录交叉确认，不沿用早期投稿页。两份官方证据不是独立研究组的性能复现。
- **跨图能力**：GCN/GAT的共享参数不妨碍架构上处理新节点；近期方法额外处理特征/标签空间不一致和复用方式。GraphAny仍解析拟合目标图分类器，GraphPFN的ICL仍需目标标签上下文；“无梯度适应”不是“零标签”。
- **成本**：复杂度表统一N、E、d与总宽度，省略常数，不等价于墙钟速度。图结构预处理、采样、稀疏实现与硬件还会影响成本。

## 核验记录

- 原始PDF检查文件完整性、首页身份、页数和SHA-256；已有原件未替换。
- 逐页渲染与独立目视检查，修正符号缺定义、Q/K/V路径、引用页码及不良换行。
- 结构、字体、原生表格和版面几何另行检查；本次未在PowerPoint客户端测试，也未独立复现论文性能。
- Demo仍作为仓库的独立学习材料保留，不进入本次PPT。
