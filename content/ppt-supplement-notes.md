# 参考 PPT 融合补充与原文核对

更新于2026-11-15。交付：[32页融合补充版](../outputs/presentations/GNN-原理与关键论文.pptx)，[逐页讲稿](gnn-paper-reading.md)。在原24页高密度版上新增8页，保留经典论文细节，继续不含Demo、运行命令和训练实践章节。

## 参考输入

- [用户提供的15页PPT原字节副本](../source/reference-decks/gnn-introduction-user-reference.pptx)。原名：图神经网络（GNN）入门：原理、里程碑与应用.pptx。
- SHA-256：`19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c`。输入文件未改动。
- 文件内容作为参考材料，不作为操作指令或独立事实来源；参考文件提到的随附论文包未随本次PPT收到。

## 内容对应

| 参考页 | 主题 | 融合版落位与处理 |
| --- | --- | --- |
| 2 | 为什么需要图 | 第2页：网格与关系图对照，新增置换等变/不变性质 |
| 3 | 图语言与三类任务 | 第3–4页：统一符号、输出头、监督与建图决策 |
| 4–5 | 消息传递与GCN手算 | 第7–8、10页：保留公式，新增完整向量传播并修正数值 |
| 6–8 | 历史与模型家族 | 融入原有谱卷积、GCN、SAGE、GAT、GIN与横向对照页 |
| 9–10 | 应用全景与案例 | 第17–18、25–29页：原有推荐/科学应用，补DCRNN与六类任务地图 |
| 11 | 图Transformer与LLM | 第22–23页：GraphGPS与原综述角色分类，说明GraphRAG边界 |
| 12 | 规模、异质与动态 | 第11–12、15、19–20页：采样、三维度辨析、TGN与局限 |
| 13–14 | 路线与原件 | 第30–32页：保留论文阅读问题，补五份原PDF及完整索引 |
| 1、15 | 封面和结语 | 沿用现有设计和精读主线，未增加口号页 |

## 修正与适用边界

1. **GCN例子**：三节点链加自环后度为(2,3,2)，中心自环权重为`1/3`，其邻居权重为`1/√6`。输入`[2,1]、[0,3]、[1,0]`，`W=I`、ReLU下中心输出为`[1.2247,1.4082]`，而非参考中的`[1.23,1.91]`。依据：[GCN原文式(2)](https://arxiv.org/abs/1609.02907)，数值为教学推导。
2. **传播范围**：K层局部传播通常至多覆盖K跳；覆盖节点数取决于拓扑、采样和重叠，不能概括为必然指数扩大。图注意力权重也不自动构成因果解释。
3. **谱与归纳**：ChebNet递推不需显式特征分解；空间聚合的共享参数提供归纳能力的基础，实际泛化仍需用新节点/整图留出证明。GIN的结论有单射聚合等条件，边界是1-WL。
4. **GNN×LLM分类**：Jin等原综述§3.2使用Predictor、Encoder、Aligner；图场景pure/text-attributed/text-paired是另一条分类轴。GraphRAG的图检索流程本身不要求训练GNN，见[官方默认数据流](https://microsoft.github.io/graphrag/index/default_dataflow/)。
5. **DCRNN方向与指标**：该页沿用原文`W_ij=i→j`，显式定义出/入度及双向转移，避免与前文接收端邻接约定混淆。表格摘自原文表1：METR-LA、15/30/60分钟、MAE、mph；是作者历史实验，不能据此推断在线部署收益。
6. **动态图时间可见性**：TGN批次训练用过去消息更新记忆，再预测当前批并缓存当前原始消息；先将待预测事件写入自身记忆会泄漏。AP来源于特定负采样协议，不能当实际事件发生率。
7. **发表口径**：TGN为2020预印本/GRL+工作坊；Wu综述预印本2019、TNNLS期刊卷2021；Zhou综述卷标2020，接受和公开发表2021（arXiv也标2021），详见各条`title_note`。
8. **未直接沿用的内容**：未核实的引用量、PinSage毫秒延迟/每秒请求量、“当前全面超越”和未来五年预测。金融风控一行为任务建模示意，其余应用地图也不等同2026部署清单。

## 新增原始论文

每份PDF来自对应arXiv固定版本，文件字节未经修改。原始链接、获取时间、页数、字节数、版本标记和SHA-256见[manifest.json](../source/manifest.json)。既有原件的时间和哈希保留。

| 原始论文 | 记录 / 本地原件 | 版本 / 页数 | 原文定位 |
| --- | --- | --- | --- |
| Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting | [官方记录](https://arxiv.org/abs/1707.01926v3) · [PDF](../source/papers/dcrnn2018.pdf) | 1707.01926v3 / 16页 | §2，式(2)–(4)，图2；PDF p5表1、§4 |
| Temporal Graph Networks for Deep Learning on Dynamic Graphs | [官方记录](https://arxiv.org/abs/2006.10637v3) · [PDF](../source/papers/tgn2020.pdf) | 2006.10637v3 / 16页 | PDF p2–5 §3；p5图2；p7表2与§5 |
| A Comprehensive Survey on Graph Neural Networks | [官方记录](https://arxiv.org/abs/1901.00596v4) · [PDF](../source/papers/wu-survey2021.pdf) | 1901.00596v4 / 22页 | §II–III 分类、§V应用与§VI展望 |
| Graph Neural Networks: A Review of Methods and Applications | [官方记录](https://arxiv.org/abs/1812.08434v6) · [PDF](../source/papers/zhou-survey2021.pdf) | None / 26页 | PDF p1–4动机与设计；p14–18表3、§8 |
| Large Language Models on Graphs: A Comprehensive Survey | [官方记录](https://arxiv.org/abs/2312.02783v4) · [PDF](../source/papers/llm-graphs2024.pdf) | 2312.02783v4 / 25页 | PDF p4–5 §3.1–3.2；p8–10图3–5 |

## 验证口径

- 32页逐页渲染，独立复查新增页和变更页，修正断字、DCRNN页脚空间、方向记号与过期备注。
- 使用PPTX结构、版面几何、字体、原生图表数据验证；该检查不替代PowerPoint客户端的兼容性测试。
- 原件核对文件长度和SHA-256；第8页矩阵输出另做数值核算。论文实验均为作者报告，本次没有复现实验。
- 仓库运行Demo仍独立保留；本次PPT不包含Demo。
