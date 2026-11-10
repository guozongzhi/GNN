# GNN 应用事实核查

核查日期：2026-11-10。方法：读取官方原文/论文全文，并由独立研究 Agent 交叉核验；搜索摘要仅作发现。独立 Agent 并不等于独立信源；同一公司的两篇文章明确标注为关联证据。不把历史部署推定为当前部署，不引用未经验证的收益数字。

| 主张 | 状态 | 原始证据 | 核验结论与限制 |
| --- | --- | --- | --- |
| Google Maps 使用 GNN 预测 ETA | 确认（历史）；当前架构待确认 | [DeepMind 2020](https://deepmind.google/blog/traffic-prediction-with-advanced-graph-neural-networks/)、[Google Maps 2020](https://blog.google/products-and-platforms/products/maps/google-maps-101-how-ai-helps-predict-traffic-and-determine-routes/) | 两文均描述路段图和产品应用；同一机构的相关来源，未满足独立机构对当前部署的二源确认，故仅作历史案例 |
| Pinterest PinSage 已生产部署 | 确认（历史）；当前架构待确认 | [PinSage 2018](https://arxiv.org/abs/1806.01973)、[MultiBiSage 2022](https://arxiv.org/abs/2205.10666) | 原论文及后续论文确认当时 PinSage 部署；团队相关，不能当成独立线上审计；MultiBiSage 离线对比不等于已全面上线 |
| GraphCast 当前仍由原服务提供实时预报 | 需修正 | [Google 当前模型文档](https://developers.google.com/weathernext/guides/models-wn-graph)、[Google 弃用说明](https://developers.google.com/weathernext/guides/deprecation)、[独立机构 ECMWF 2026-05-11](https://www.ecmwf.int/en/about/media-centre/aifs-blog/2026/farewell-external-ai-models) | Google 文档明确已弃用、不再产生实时预报；ECMWF 公告也停止相关外部模型运行。两家独立机构支持各自服务状态的变化；不延伸判断所有第三方部署 |
| GNoME 用 GNN 与 DFT 构成材料发现闭环 | 确认（科研及数据用途） | [Nature 原论文](https://www.nature.com/articles/s41586-023-06735-9)、[独立 Materials Project 版本记录](https://docs.materialsproject.org/changes/database-versions) | 原文描述候选筛选、DFT 再验证与主动学习；数据库记录提供独立数据纳入证据。不把计算稳定写成可合成或商业量产 |
| GNN 已为本部门无线任务带来实际收益 | 待确认 | 本学习包无本部门一手数据 | 只给建图方法的教学类比；不进入收益结论，也不从其他业务线派生 |

## 证据冲突的处理

ECMWF 的旧 [Machine Learning model data 页面](https://www.ecmwf.int/en/forecasts/datasets/machine-learning-model-data) 仍出现正在运行 GraphCast 的旧描述。较新的停运公告优先；介绍采用保守现状口径，不沿用旧页。

Google 模型文档中出现了具体弃用日期。本包正文只表述“当前文档写已弃用”，不把该单机构具体日期扩展成跨机构共同时间点。原始 HTML 快照与哈希见 `../source/web-manifest.json`；外部网页可能有与正文无关的导航、脚本及后续更新，核验时以实际正文为准。

MultiBiSage arXiv HTML 曾保留模板 DOI/ISBN，因此引用使用 arXiv 标识，不复制模板 DOI。历史首发与会议年份在论文表内区分。
