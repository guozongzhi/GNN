# GNN 原始论文索引

原有资料核验于2026-11-10，补充论文核验于2026-11-15；逐文件获取时间见manifest.json。年份是主要发表年份；下载的 arXiv 文件不一定是出版社排版。身份核对以标题、作者与原始记录为依据；文件版本、哈希、页数见 manifest.json。

| ID / 年份 | 论文 / 作者 / 会议 | 为什么读 | 原始记录与文件 |
| --- | --- | --- | --- |
| gori2005 / 2005 | A new model for learning in graph domains；Gori, Monfardini, Scarselli；IJCNN | 早期图域学习模型；追溯起点，全文受限 | [记录](https://doi.org/10.1109/IJCNN.2005.1555942) · 全文未取得 |
| scarselli2009 / 2009 | The Graph Neural Network Model；Scarselli et al.；IEEE TNN | 递归状态与固定点，理解现代消息传递之前的GNN | [记录](https://doi.org/10.1109/TNN.2008.2005605) · [本地 PDF](papers/scarselli2009.pdf) |
| bruna2014 / 2014 | Spectral Networks and Deep Locally Connected Networks on Graphs；Bruna et al.；ICLR | 把卷积推广到图的谱域 | [记录](https://arxiv.org/abs/1312.6203) · [本地 PDF](papers/bruna2014.pdf) |
| chebnet2016 / 2016 | Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering；Defferrard, Bresson, Vandergheynst；NeurIPS | 多项式近似带来局部化与高效计算 | [记录](https://arxiv.org/abs/1606.09375) · [本地 PDF](papers/chebnet2016.pdf) |
| gcn2017 / 2017 | Semi-Supervised Classification with Graph Convolutional Networks；Kipf and Welling；ICLR | 最适合入门复现的归一化邻居聚合 | [记录](https://arxiv.org/abs/1609.02907) · [本地 PDF](papers/gcn2017.pdf) |
| mpnn2017 / 2017 | Neural Message Passing for Quantum Chemistry；Gilmer et al.；ICML | 用消息、聚合、更新统一多类模型 | [记录](https://arxiv.org/abs/1704.01212) · [本地 PDF](papers/mpnn2017.pdf) |
| graphsage2017 / 2017 | Inductive Representation Learning on Large Graphs；Hamilton, Ying, Leskovec；NeurIPS | 邻居采样与归纳学习，面向大图和新节点 | [记录](https://arxiv.org/abs/1706.02216) · [本地 PDF](papers/graphsage2017.pdf) |
| gat2018 / 2018 | Graph Attention Networks；Velickovic et al.；ICLR | 学习不同邻居的重要性 | [记录](https://arxiv.org/abs/1710.10903) · [本地 PDF](papers/gat2018.pdf) |
| rgcn2018 / 2018 | Modeling Relational Data with Graph Convolutional Networks；Schlichtkrull et al.；ESWC | 区分边类型，适配知识图谱 | [记录](https://arxiv.org/abs/1703.06103) · [本地 PDF](papers/rgcn2018.pdf) |
| pinsage2018 / 2018 | Graph Convolutional Neural Networks for Web-Scale Recommender Systems；Ying et al.；KDD | 工业推荐中的采样、训练与离线推理 | [记录](https://arxiv.org/abs/1806.01973) · [本地 PDF](papers/pinsage2018.pdf) |
| gn2018 / 2018 | Relational inductive biases, deep learning, and graph networks；Battaglia et al.；arXiv | 节点、边、全局状态与关系归纳偏置 | [记录](https://arxiv.org/abs/1806.01261) · [本地 PDF](papers/gn2018.pdf) |
| gin2019 / 2019 | How Powerful are Graph Neural Networks?；Xu et al.；ICLR | 表达能力与Weisfeiler-Lehman测试的联系 | [记录](https://arxiv.org/abs/1810.00826) · [本地 PDF](papers/gin2019.pdf) |
| oversmoothing2018 / 2018 | Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning；Li, Han, Wu；AAAI | 拉普拉斯平滑视角与过平滑 | [记录](https://arxiv.org/abs/1801.07606) · [本地 PDF](papers/oversmoothing2018.pdf) |
| lightgcn2020 / 2020 | LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation；He et al.；SIGIR | 推荐任务中简化传播层的例子 | [记录](https://arxiv.org/abs/2002.02126) · [本地 PDF](papers/lightgcn2020.pdf) |
| heterophily2020 / 2020 | Beyond Homophily in Graph Neural Networks: Current Limitations and Effective Designs；Zhu et al.；NeurIPS | 异配图挑战：相邻未必同类 | [记录](https://arxiv.org/abs/2006.11468) · [本地 PDF](papers/heterophily2020.pdf) |
| bottleneck2021 / 2021 | On the Bottleneck of Graph Neural Networks and its Practical Implications；Alon and Yahav；ICLR | 远距离信息压缩与过挤压 | [记录](https://arxiv.org/abs/2006.05205) · [本地 PDF](papers/bottleneck2021.pdf) |
| egnn2021 / 2021 | E(n) Equivariant Graph Neural Networks；Satorras, Hoogeboom, Welling；ICML | 几何变换下保持等变，适配空间结构 | [记录](https://arxiv.org/abs/2102.09844) · [本地 PDF](papers/egnn2021.pdf) |
| graphgps2022 / 2022 | Recipe for a General, Powerful, Scalable Graph Transformer；Rampasek et al.；NeurIPS | 局部消息传递、全局注意力与位置结构编码结合 | [记录](https://arxiv.org/abs/2205.12454) · [本地 PDF](papers/graphgps2022.pdf) |
| graphcast2023 / 2023 | Learning skillful medium-range global weather forecasting；Lam et al.；Science | 多尺度图上的全球天气预测 | [记录](https://arxiv.org/abs/2212.12794) · [本地 PDF](papers/graphcast2023.pdf) |
| gnome2023 / 2023 | Scaling deep learning for materials discovery；Merchant et al.；Nature | GNN筛选与DFT验证的材料发现闭环 | [记录](https://doi.org/10.1038/s41586-023-06735-9) · [本地 PDF](papers/gnome2023.pdf) |
| multibisage2022 / 2022 | MultiBiSage: A Web-Scale Recommendation System Using Multiple Bipartite Graphs at Pinterest；Gurukar et al.；KDD | 多种关系图用于推荐系统 | [记录](https://arxiv.org/abs/2205.10666) · [本地 PDF](papers/multibisage2022.pdf) |
| dcrnn2018 / 2018 | Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting；Yaguang Li, Rose Yu, Cyrus Shahabi, Yan Liu；ICLR | 有向随机游走扩散卷积与时序编码解码；交通预测 | [记录](https://arxiv.org/abs/1707.01926v3) · [本地 PDF](papers/dcrnn2018.pdf) |
| tgn2020 / 2020 | Temporal Graph Networks for Deep Learning on Dynamic Graphs；Emanuele Rossi et al.；arXiv preprint / ICML 2020 GRL+ workshop | 事件流、节点记忆与时间可见性；动态图框架 | [记录](https://arxiv.org/abs/2006.10637v3) · [本地 PDF](papers/tgn2020.pdf) |
| wu-survey2021 / 2021 | A Comprehensive Survey on Graph Neural Networks；Zonghan Wu et al.；IEEE TNNLS 32(1), 2021; online 2020 | 递归、卷积、自编码、时空四类综述；预印本始于2019 | [记录](https://arxiv.org/abs/1901.00596v4) · [本地 PDF](papers/wu-survey2021.pdf) |
| zhou-survey2021 / 2021 | Graph Neural Networks: A Review of Methods and Applications；Jie Zhou et al.；AI Open 1 (2020), 57–81; published 2021 | 设计流程与应用地图；预印本始于2018 | [记录](https://arxiv.org/abs/1812.08434v6) · [本地 PDF](papers/zhou-survey2021.pdf) |
| llm-graphs2024 / 2024 | Large Language Models on Graphs: A Comprehensive Survey；Bowen Jin, Gang Liu, Chi Han, Meng Jiang, Heng Ji, Jiawei Han；IEEE TKDE 36(12):8622–8642, 2024 | 按 Predictor / Encoder / Aligner 区分LLM角色 | [记录](https://arxiv.org/abs/2312.02783v4) · [本地 PDF](papers/llm-graphs2024.pdf) |
