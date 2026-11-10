"""Create a portable HTML result page from metrics (no network or JS required)."""
from html import escape
import json
from pathlib import Path


def write_report(report, out):
    out = Path(out)
    summaries = []
    for name, values in report['summary'].items():
        acc, f1 = values['accuracy'], values['macro_f1']
        spread = '单次运行，无标准差' if acc['std'] is None else f"± {100 * acc['std']:.1f} 个百分点"
        summaries.append(f"<div class='card'><span>{escape(name)}</span><b>{100 * acc['mean']:.1f}%</b>"
                         f"<small>{spread}<br>Macro-F1 {f1['mean']:.3f}</small></div>")
    runs = []
    for row in report['results']:
        stem = f"{row['name']}-{row['seed']}"
        matrix = ''.join('<tr><th>' + str(i) + '</th>' + ''.join(f'<td>{n}</td>' for n in counts) + '</tr>'
                         for i, counts in enumerate(row['confusion']))
        runs.append(f"<details><summary>{escape(stem)} · 测试 {row['accuracy']:.1%} · 第 {row['best_epoch']} 轮</summary>"
                    f"<p>验证损失 {row['val_loss']:.4f}；测试 Macro-F1 {row['macro_f1']:.4f}。行是真实类，列是预测类。</p>"
                    f"<table><thead><tr><th>真实 / 预测</th><th>0</th><th>1</th><th>2</th></tr></thead><tbody>{matrix}</tbody></table>"
                    f"<p><a href='{stem}-predictions.csv'>逐节点预测 CSV</a> · <a href='{stem}-history.csv'>训练日志 CSV</a> · "
                    f"<a href='{stem}.pt'>模型权重</a></p></details>")
    config = escape(json.dumps(report['config'], ensure_ascii=False, indent=2))
    page = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>GNN 实验报告</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#f6f7f2;color:#17302f;font:16px/1.7 system-ui,sans-serif}}
main{{max-width:1000px;margin:auto;padding:40px 24px}}h1{{font-size:38px;line-height:1.2}}a{{color:#12675e}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.card{{background:#e3eee6;padding:18px;border-radius:10px}}
.card b{{display:block;font-size:32px}}small{{font-size:12px}}img{{width:100%;height:auto}}pre{{background:#173d37;color:white;padding:20px;overflow:auto;border-radius:8px}}
details{{background:white;border:1px solid #ced9cf;border-radius:8px;margin:12px 0;padding:16px}}summary{{cursor:pointer;font-weight:600}}
td,th{{padding:6px 18px;text-align:center;border-bottom:1px solid #ced9cf}}.note{{border-left:4px solid #aa4c20;background:#fff1df;padding:14px}}
@media(max-width:600px){{main{{padding:24px 16px}}.cards{{grid-template-columns:repeat(2,1fr)}}h1{{font-size:30px}}.card b{{font-size:27px}}}}
</style></head><body><main><p>GNN / LOCAL EXPERIMENT</p><h1>关系在这次实验中有用吗？</h1>
<p>以下为当前实验目录的实际结果。数据集：合成三社区图，传导式节点分类；节点/特征 {report['nodes']}/{report['features']}。</p>
<div class="cards">{''.join(summaries)}</div><p>种子：{escape(str(report['seeds']))}。标准差为样本标准差。</p>
<p>随机性口径：{escape(report['seed_protocol'])}。训练标签用于梯度，验证损失选模型，测试集仅在选模后评分。</p>
<p class="note">合成数据用于理解机制，不代表真实业务精度。对照 MLP、仅自环、打乱图，判断模型究竟使用了什么信息。</p>
<h2>训练与表示</h2><img src="experiment.png" alt="验证损失、测试准确率与表示投影">
<p>图为第一个模型种子；一维隐藏表示的第二投影轴补零。PCA 颜色使用真实类别，仅用于展示。</p>
<h2>逐次实验与错误分析</h2>{''.join(runs)}
<p>预测 CSV 包含所有节点的划分、真实类别、预测类别和概率；分析泛化时筛选 split=test。概率未经校准。</p>
<h2>复现配置</h2><pre>{config}</pre><p>{escape(str(report['environment']))}</p>
<p><a href="results.json">完整 JSON</a> · <a href="experiment.svg">矢量图</a></p>
</main></body></html>'''
    (out / 'report.html').write_text(page, encoding='utf-8')
