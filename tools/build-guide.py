"""Render the Markdown source plus interactive teaching widgets, without network access."""
import html
import json
from pathlib import Path
import re
import markdown

ROOT = Path(__file__).resolve().parents[1]


def build():
    papers = json.loads((ROOT / 'source/manifest.json').read_text())
    source = (ROOT / 'content/gnn-introduction.md').read_text()
    timeline_ids = ['scarselli2009', 'chebnet2016', 'gcn2017', 'mpnn2017', 'graphsage2017', 'gat2018', 'gin2019', 'egnn2021', 'graphgps2022']
    by_id = {p['id']: p for p in papers}
    timeline = '<div class="timeline">' + ''.join(
        f'<div class="milestone"><span class="year">{by_id[key]["year"]}</span><b>{key}</b><p>{html.escape(by_id[key]["why_read"])}</p></div>' for key in timeline_ids) + '</div>'
    index = ['# GNN 原始论文索引', '', '原有资料核验于2026-11-10，补充论文核验于2026-11-15；逐文件获取时间见manifest.json。年份是主要发表年份；下载的 arXiv 文件不一定是出版社排版。身份核对以标题、作者与原始记录为依据；文件版本、哈希、页数见 manifest.json。', '', '| ID / 年份 | 论文 / 作者 / 会议 | 为什么读 | 原始记录与文件 |', '| --- | --- | --- | --- |']
    refs = ['<div class="table-wrap"><table class="references"><thead><tr><th>ID / 年份</th><th>原始论文与阅读目的</th><th>原始记录 / PDF</th></tr></thead><tbody>']
    for row in papers:
        key = row['id']
        if row['status'] == 'downloaded':
            local = f'<a href="../{row["file"]}">本地原始 PDF · {row["pages"]} 页</a>'
            md_local = f'[本地 PDF]({row["file"].replace("source/", "", 1)})'
        else:
            local = '全文未取得：保留原始记录'
            md_local = '全文未取得'
        refs.append(f'<tr id="ref-{key}"><td>{key}<br>{row["year"]} · {row["venue"]}</td><td><strong>{html.escape(row["title"])}</strong><br>{html.escape(row["authors"])}<br>{html.escape(row["why_read"])}</td><td><a href="{html.escape(row["url"])}">官方记录 / DOI</a><br>{local}</td></tr>')
        index.append(f'| {key} / {row["year"]} | {row["title"]}；{row["authors"]}；{row["venue"]} | {row["why_read"]} | [记录]({row["url"]}) · {md_local} |')
    refs.append('</tbody></table></div>')
    (ROOT / 'source/paper-index.md').write_text('\n'.join(index) + '\n')
    rendered = markdown.markdown(source, extensions=['tables', 'fenced_code', 'toc'])
    rendered = rendered.replace('<div id="paper-timeline"></div>', timeline)
    rendered = rendered.replace('<div id="paper-references"></div>', '\n'.join(refs))
    rendered = rendered.replace('href="fact-check.md"', 'href="../content/fact-check.md"')
    nav = ''.join(f'<a href="#{anchor}">{text}</a>' for anchor, text in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', rendered))
    template = (ROOT / 'tools/guide-template.html').read_text()
    output = template.replace('__NAV__', nav).replace('__ARTICLE__', rendered)
    (ROOT / 'outputs/gnn-guide.html').write_text(output)
    print('Built', ROOT / 'outputs/gnn-guide.html')


if __name__ == '__main__':
    build()
