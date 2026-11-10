# 用四组对照理解 GNN

## 第一步：看懂一层，而不是先看准确率

打开 `../outputs/gnn-guide.html`，选择 A 节点，执行一层传播。分别切换普通均值和 GCN 对称归一化：均值权重之和为 1；GCN 的每个权重还取决于发送节点的度数，权重之和不一定为 1。

删掉 C—E 边，观察哪些节点的一层结果改变，再观察二层结果。这里使用固定 W=1、恒等激活，仅展示传播算子。真正的训练在 Python Demo 中进行。

## 第二步：训练，并说明比较是否公平

```sh
python demo/train.py --data-seed 42 --seeds 7 17 27 --out runs/fixed-data
```

每个种子的四组模型使用同样的数据、划分、层宽、层数、初始化与优化配置。GCN 使用真实图；MLP 使用单位传播矩阵；仅自环与 MLP 等价；Shuffled 保留图结构但打乱节点对应关系。

`--data-seed` 固定三个种子的图、特征和划分。GCN/MLP 的差异可用于分析模型随机性；Shuffled 的种子同时影响置换，因此还包含置换波动。样本只有三个时，标准差仅供观察，不能支持强泛化结论。

打开 `runs/fixed-data/report.html`，先看验证损失和最优轮次，再看测试准确率。不要根据测试准确率反复挑模型参数，否则测试集也参与了调参。

## 第三步：找到错分节点

打开 `gcn-7-predictions.csv`，先筛选 `split=test`，再筛选 `correct=False`。同一个节点在 MLP 与 GCN 中的预测不同，可以帮助提出假设：邻居是否提供了信息，还是混入了噪声？这只是诊断线索，并不是因果证明。

CSV 中 p0/p1/p2 是 softmax 概率，和约为 1；高概率不意味着经过校准。行顺序对应生成图的节点索引，没有用真实标签另加输入特征。

## 第四步：制造一个失败条件

```sh
python demo/train.py --p-in .06 --p-out .06 --out runs/no-community
```

此时社区内外连边概率相同，边的生成不再依赖类别。图传播可能混合无关节点。若 GCN 低于 MLP，先解释数据与建图条件，而不是立即更换一个更复杂的网络。

额外练习：`--noise 2.5` 提高特征噪声；`--layers 8` 加深网络；`--hidden 1` 把隐藏状态压成一个数。后者的 PCA 图第二轴补零，不能解释成真正的二维结构。

## 第五步：重载模型，验证结果可复现

```sh
python demo/train.py --evaluate runs/fixed-data/gcn-7.pt --out runs/fixed-data-evaluation
```

新目录里的 `evaluation.json` 应与 `results.json` 对应行的 Accuracy、Macro-F1、loss 和 confusion 一致。checkpoint 内保存了验证选中的权重、生成数据和实际传播矩阵；重载不会重新划分数据或重新训练。

## 常见问题

| 现象 | 原因与处理 |
| --- | --- |
| GitHub 点 HTML 看到源码 | 克隆整个仓库后用浏览器打开本地文件，保留相对目录关系 |
| 输出目录非空被拒绝 | 换一个实验名；确实要替换时显式添加 `--overwrite` |
| 修改数据参数却没改变重载评估 | `--evaluate` 使用 checkpoint 内的数据与模型；参数变化应通过重新训练实现 |
| 单个种子的标准差为空 | 一个样本不能计算样本标准差；报告明确显示单次运行 |
| 无边 GCN 和 MLP 数值完全相同 | 这是预期的一致性检查 |
| 原文哈希不一致 | 检查文件是否损坏/换版，不要直接重算哈希来消除报警；原清单保留 |
| 训练达 100%，是否已经掌握真实业务 | 默认图是可控的简单合成数据；下一步需要真实数据、合适的划分和任务基线 |

## 实现定位

- `demo/train.py` 的 `make_graph`：数据与划分；`normalize`：自环和对称归一化。
- `Network.forward`：传播、线性层和非线性；`fit`：训练与验证选模。
- `evaluate`：checkpoint 重载；`demo/report.py`：实验报告。
- `tools/verify-sources.py`：无需联网的证据核验。
