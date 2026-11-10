# GNN 学习包

一套从原始论文、可视化原理到实际训练/评估的独立培训材料。核查日期：**2026-11-10**。独立维护 GNN 学习材料与可复现实验。

仓库：[guozongzhi/GNN](https://github.com/guozongzhi/GNN)（私有）。

```sh
git clone https://github.com/guozongzhi/GNN.git
cd GNN
```

## 先打开这里

- **[可交互介绍](outputs/gnn-guide.html)**：离线双击打开；点击节点，切换归一化/自环/边，逐层观察消息传播；内含论文脉络、应用证据与实际训练结果。
- [介绍母稿](content/gnn-introduction.md)、[论文索引](source/paper-index.md)、[应用事实核查](content/fact-check.md)。
- [实验图](outputs/experiment.png)、[完整指标与混淆矩阵](outputs/results.json)。

浏览器页是原理说明和已完成实验的查看器；**重新训练在本地 Python 执行**。页面不连接外部服务，不收集数据。

## 直接运行

本机工作区已准备好 Python 3.12 的 `.venv`；新克隆请先按下一节建立环境，再执行：

```sh
# 从仓库根目录运行
.venv/bin/python demo/train.py --out outputs
.venv/bin/python demo/train.py \
  --evaluate outputs/gcn-7.pt --out outputs/re-evaluation
```

换机器时建立环境（首次安装需要联网；训练无需联网/账号/GPU）：

```sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r demo/requirements-lock.txt
# 无 uv 时：python3.12 -m venv .venv，再用环境的 python -m pip install -r ...
```

经过验证的直接依赖为 PyTorch 2.6.0、NumPy 2.2.6、Matplotlib 3.10.1；锁文件保留本次解析的间接依赖。CPU 上使用稠密矩阵，是小图教学代码；不用于大图压力测试。

## 实验设计

180 节点 / 3 类 / 16 维特征。每类训练 8、验证 12、测试 40 个节点。任务是**同一图上的传导式半监督节点分类**。只有训练标签进入损失；验证集选择 checkpoint；测试集用于选模后报告。特征标准化只在训练节点拟合。

四个实验：GCN、同宽 MLP、仅自环 GCN、打乱图与节点对应关系的 GCN。无边 GCN 在本实现中与 MLP 完全等价，是一致性检查。默认运行 7/17/27 三个种子，每个种子同时改变数据/划分/初始化。默认是人为构造的同配图，结果不代表真实基准或业务精度。

训练输出：每种模型与种子的权重 `.pt`、逐轮 CSV、验证选模轮次、测试 Accuracy/Macro-F1/混淆矩阵、PCA 可视化与结果汇总。`--evaluate` 重载权重、数据与传播矩阵，不重新训练。只读取自己生成或可信的 checkpoint。

建议依次尝试：

```sh
# 图不再带有社区线索
.venv/bin/python demo/train.py --p-in .06 --p-out .06 --out outputs/no-community
# 更深网络
.venv/bin/python demo/train.py --layers 8 --out outputs/deep
# 更强特征噪声
.venv/bin/python demo/train.py --noise 2.5 --out outputs/noisy
```

自定义输出目录有自己的 results.json / results.js / 图 / 权重；主阅读页展示默认 outputs 下结果。重训默认目录后刷新阅读页即可更新动态指标与图片。

## 原始材料与边界

`source/catalog.json` 是结构化阅读索引；`source/papers/` 保存未经改写的原始论文文件，`manifest.json` 记录下载来源 URL、下载时间、版本标记、页数、字节与 SHA-256。下载的 arXiv 文件属于作者公开版本，不保证与出版社排版相同。Scarselli 2009 从学术镜像获取，另保留 DOI 及作者机构记录链接；Gori 2005 未取得开放全文，明确保留缺口。

`source/pages/` 保存能够下载的官方网页 HTML 原件，可能包含页面脚本；建议通过介绍和核查表阅读相应结论。`web-manifest.json` 记录网页获取失败的条目，不冒称全部网页均已离线。论文版权归原权利人；公开再分发前请核对各篇许可。

应用口径区分历史部署、当前文档和科研验证。特别是：GraphCast 是重要科研里程碑，但当前 Google 文档与 ECMWF 新公告说明对应实时服务已停止/弃用；不能把历史论文写成现役服务清单。

## 构建、验证与文件职责

```sh
# 额外的文档工具依赖；训练本身不需要
uv pip install --python .venv/bin/python -r tools/requirements.txt
.venv/bin/python tools/fetch-papers.py
.venv/bin/python tools/build-guide.py
.venv/bin/python -m unittest discover -s demo -p 'test_*.py'
.venv/bin/python -m unittest discover -s tools -p 'test_*.py'
git diff --check
```

下载工具复用已有 PDF 并重新校验内容；清单保留文件原下载时间。不自动追踪更新版本。若需更新，先另存旧文件与旧清单再移走目标 PDF 重跑。

| 目录 | 内容 |
| --- | --- |
| `source/` | 论文、官方网页、书目信息、溯源清单 |
| `content/` | 原创介绍母稿与事实核查 |
| `demo/` | 训练/评估代码、依赖和测试 |
| `tools/` | 资料下载、阅读页构建与模板 |
| `outputs/` | 生成阅读页、实验图表、日志、权重与验收记录 |

当前不含 Cora 等真实数据集的论文级复现，也不含真实业务收益评估。下一步可在保持同一训练/验证/测试边界的前提下接入真实数据，再考虑 PyTorch Geometric 的稀疏实现。

可选的浏览器验收使用 Playwright（不属于训练依赖）：

```sh
uv pip install --python .venv/bin/python playwright==1.51.0
.venv/bin/python -m playwright install chromium
.venv/bin/python tools/check-browser.py
```
