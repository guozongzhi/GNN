# 参考 PPT 融合补充与原文核对

更新于2026-11-15。当前交付：[35页原理图解与论文精读](../outputs/presentations/GNN-原理与关键论文.pptx)，[逐页讲稿](gnn-paper-reading.md)。按“数字过多、原理不清晰”的反馈重写主线：用统一小图解释消息、聚合、更新、训练与各论文改动，移除正文基准分数表。推导条件、原文定位和证据边界保留在讲稿，继续不含Demo、运行命令和训练实践章节。

## 参考输入

- [用户提供的15页PPT原字节副本](../source/reference-decks/gnn-introduction-user-reference.pptx)。原名：图神经网络（GNN）入门：原理、里程碑与应用.pptx。
- SHA-256：`19d99aa481093b45ebdd662ae19ce41e18467ed38e9a29acf74feba9fa61042c`。输入文件未改动。
- 文件内容作为参考材料，不作为操作指令或独立事实来源；参考文件提到的随附论文包未随本次PPT收到。

## 内容对应

| 参考页 | 主题 | 当前35页的对应处理 |
| --- | --- | --- |
| 2 | 为什么需要图 | 第2页的属性与关系，第7页的图信号直觉 |
| 3 | 图语言与任务 | 第2–5页的状态、消息与学习目标，图级读出见第22页 |
| 4–5 | 消息传递与GCN手算 | 第3–5、9–11页：先计算路径，再解释近似、度归一化与特征轴 |
| 6–8 | 历史与模型家族 | 第6–21页：改变哪一步、为何设计、反例与理论边界 |
| 9–10 | 应用与案例 | 第22–25、31–32页：分子、推荐、天气与材料的机制 |
| 11 | 图Transformer与LLM | 第30、33页：GPS并行分支和语言模型角色 |
| 12 | 规模、异质与动态 | 第13–18、26–29页：采样、类型、时间记忆与几何约束 |
| 13–14 | 阅读路线与原件 | 第34–35页与完整论文索引 |
| 1、15 | 封面和结语 | 保留视觉风格，结尾改为机制对照与原件入口 |

## 修正与适用边界

1. **GCN例子**：三节点链加自环后度为(2,3,2)，中心自环权重为`1/3`，其邻居权重为`1/√6`。输入`[2,1]、[0,3]、[1,0]`，`W=I`、ReLU下中心输出为`[1.2247,1.4082]`，而非参考中的`[1.23,1.91]`。依据：[GCN原文式(2)](https://arxiv.org/abs/1609.02907)，数值为教学推导。
2. **传播范围**：K层局部传播通常至多覆盖K跳；覆盖节点数取决于拓扑、采样和重叠，不能概括为必然指数扩大。图注意力权重也不自动构成因果解释。
3. **谱与归纳**：ChebNet递推不需显式特征分解；空间聚合的共享参数提供归纳能力的基础，实际泛化仍需用新节点/整图留出证明。GIN的结论有单射聚合等条件，边界是1-WL。
4. **GNN×LLM分类**：Jin等原综述§3.2使用Predictor、Encoder、Aligner；图场景pure/text-attributed/text-paired是另一条分类轴。GraphRAG的图检索流程本身不要求训练GNN，见[官方默认数据流](https://microsoft.github.io/graphrag/index/default_dataflow/)。
5. **DCRNN方向与指标**：该页沿用原文`W_ij=i→j`，显式定义出/入度及双向转移，避免与前文接收端邻接约定混淆。当前正文改用空间扩散与时间状态的两条流程解释机制，不再展示原文结果数字表。原文表1是作者历史实验，不能据此推断在线部署收益。
6. **动态图时间可见性**：TGN批次训练用过去消息更新记忆，再预测当前批并缓存当前原始消息；先将待预测事件写入自身记忆会泄漏。AP来源于特定负采样协议，不能当实际事件发生率。
7. **发表口径**：TGN为2020预印本/GRL+工作坊；Wu综述预印本2019、TNNLS期刊卷2021；Zhou综述卷标2020，接受和公开发表2021（arXiv也标2021），详见各条`title_note`。
8. **未直接沿用的内容**：未核实的引用量、PinSage毫秒延迟/每秒请求量、“当前全面超越”和未来五年预测。应用章节解释论文中的任务与机制，不等同2026部署清单。

## 新增原始论文

每份PDF来自对应arXiv固定版本，文件字节未经修改。原始链接、获取时间、页数、字节数、版本标记和SHA-256见[manifest.json](../source/manifest.json)。既有原件的时间和哈希保留。

| 原始论文 | 记录 / 本地原件 | 版本 / 页数 | 原文定位 |
| --- | --- | --- | --- |
| Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting | [官方记录](https://arxiv.org/abs/1707.01926v3) · [PDF](../source/papers/dcrnn2018.pdf) | 1707.01926v3 / 16页 | §2，式(2)–(4)，图2；PDF p5表1、§4 |
| Temporal Graph Networks for Deep Learning on Dynamic Graphs | [官方记录](https://arxiv.org/abs/2006.10637v3) · [PDF](../source/papers/tgn2020.pdf) | 2006.10637v3 / 16页 | PDF p2–5 §3；p5图2；p7表2与§5 |
| A Comprehensive Survey on Graph Neural Networks | [官方记录](https://arxiv.org/abs/1901.00596v4) · [PDF](../source/papers/wu-survey2021.pdf) | 1901.00596v4 / 22页 | §II–III 分类、§V应用与§VI展望 |
| Graph Neural Networks: A Review of Methods and Applications | [官方记录](https://arxiv.org/abs/1812.08434v6) · [PDF](../source/papers/zhou-survey2021.pdf) | 固定下载链接1812.08434v6；PDF内未检出版本标记 / 26页 | PDF p1–4动机与设计；p14–18表3、§8 |
| Large Language Models on Graphs: A Comprehensive Survey | [官方记录](https://arxiv.org/abs/2312.02783v4) · [PDF](../source/papers/llm-graphs2024.pdf) | 2312.02783v4 / 25页 | PDF p4–5 §3.1–3.2；p8–10图3–5 |

## 验证口径

- 35页逐页渲染与独立目视复查，修正流程箭头方向、下标显示、断字、标签和连线遮挡。
- 使用PPTX结构、版面几何与字体检查，关系图和流程图使用原生可编辑对象；该检查不替代PowerPoint客户端兼容性测试。
- 原件核对文件长度和SHA-256；当前页10的度归一化、页21的1-WL反例、页28的刚性变换图例作独立计算核对。原先向量手算的纠错记录保留在上文，正文不再堆放数值矩阵。
- 仓库运行Demo仍独立保留；本次PPT不包含Demo。
