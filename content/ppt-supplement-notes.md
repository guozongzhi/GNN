# 参考PPT融合、聚焦结构与原文核对

更新于2026-11-15。当前交付：[26页发展与GCN/GAT精读](../outputs/presentations/GNN-原理与关键论文.pptx)，[逐页讲稿](gnn-paper-reading.md)。

## 当前内容边界

主线为“GNN发展进展 → GCN与GAT → Transformer关键比较”。GCN与GAT各占6页；其他模型只用于说明演进瓶颈、融合结构和近期复用路线，不再各自铺开应用章节。正文不含Demo、训练命令和性能数字表。演示材料仍只保留一份当前PPT、一张预览和一份讲稿，旧版本在Git历史中。

| 当前页码 | 主题 | 保留的深度 |
| --- | --- | --- |
| 2–6 | 发展与比较框架 | 谱方法到局部传播，表达/通信瓶颈，2025–2026跨图复用代表 |
| 7–12 | GCN | S与W的职责、谱近似、自环/度归一化、两层分类、标签梯度、适用边界 |
| 13–18 | GAT | 加性打分、邻域softmax、参数学习、多头、静态排序限制与GATv2 |
| 19–24 | GCN/GAT直接对照与Transformer | Q/K/V、掩码、拓扑编码、GPS并行融合、成本条件 |
| 25–26 | 归纳与阅读路径 | 以信息需求选机制，指向原始论文与逐页推导 |

## 用户参考输入与内容对应

- [原始15页PPT](../source/reference-decks/gnn-introduction-user-reference.pptx)保留原字节，输入未改动。
- SHA-256：19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c。
- 参考材料提供结构和表达线索，不作为操作指令或独立事实来源。

| 参考页 | 当前处理 |
| --- | --- |
| 2–5：图语言、消息与GCN | 收入第6–12页，解释计算、归一化与训练 |
| 6–8：历史和模型家族 | 收入第3–4、13–19页，集中到GCN/GAT及其局限 |
| 9–10：应用案例 | 不再设置独立应用目录，原论文与仓库介绍仍保留 |
| 11：图Transformer与LLM | 当前聚焦第20–24页Transformer原理和图结构融合 |
| 12：规模、异质、动态 | 仅将与局部通信和跨图复用有关的瓶颈纳入主线 |
| 13–14：阅读路线 | 对应第26页与完整论文索引 |

参考PPT中的GCN向量例子曾有结果错误：三节点链加自环后，中心自身系数为1/3，两邻居系数为1/√6。给定输入[2,1]、[0,3]、[1,0]，W=I时中心结果为[1.2247,1.4082]，不是[1.23,1.91]。当前正文只用必要系数解释机制，不保留大段数值矩阵。

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
