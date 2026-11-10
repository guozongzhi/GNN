"""A small dense GCN, matched MLP and graph ablations on a synthetic graph."""
import argparse
import copy
import csv
from datetime import datetime, timezone
import math
import json
from pathlib import Path
import platform

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from report import write_report


def make_graph(seed=7, per_class=60, p_in=0.18, p_out=0.015, noise=1.5):
    if per_class < 24:
        raise ValueError('per_class must be >=24 for nonempty train/validation/test splits')
    if not (0 <= p_in <= 1 and 0 <= p_out <= 1) or not math.isfinite(noise) or noise < 0:
        raise ValueError('edge probabilities must be in [0,1]; noise must be nonnegative')
    rng = np.random.default_rng(seed)
    y = np.repeat(np.arange(3), per_class)
    n = len(y)
    probability = np.where(y[:, None] == y[None, :], p_in, p_out)
    upper = np.triu(rng.random((n, n)) < probability, 1)
    adjacency = (upper | upper.T).astype(np.float32)
    prototypes = rng.normal(0, 0.45, (3, 16))
    x = prototypes[y] + rng.normal(0, noise, (n, 16))
    splits = {key: [] for key in ('train', 'val', 'test')}
    for c in range(3):
        indices = rng.permutation(np.where(y == c)[0])
        for key, subset in zip(splits, (indices[:8], indices[8:20], indices[20:])):
            splits[key].extend(subset.tolist())
    # Fit preprocessing only on training features, never on held-out labels/features.
    mean, std = x[splits['train']].mean(0), x[splits['train']].std(0).clip(1e-6)
    x = ((x - mean) / std).astype(np.float32)
    return {'x': torch.tensor(x), 'y': torch.tensor(y), 'a': torch.tensor(adjacency),
            **{k: torch.tensor(v, dtype=torch.long) for k, v in splits.items()}}


def normalize(a):
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError('adjacency must be square')
    if not torch.isfinite(a).all() or (a < 0).any() or not torch.allclose(a, a.T):
        raise ValueError('demo requires finite, nonnegative, undirected adjacency')
    # Input is raw adjacency without loops. Add exactly one self-loop per node.
    a = a.clone()
    a.fill_diagonal_(1)
    inverse = a.sum(1).rsqrt()
    return inverse[:, None] * a * inverse[None, :]


class Network(nn.Module):
    def __init__(self, hidden=16, layers=2, dropout=0.3):
        super().__init__()
        if layers < 1 or hidden < 1 or not 0 <= dropout < 1:
            raise ValueError('invalid layer count, hidden size or dropout')
        sizes = [16] + [hidden] * (layers - 1) + [3]
        self.weights = nn.ModuleList(nn.Linear(a, b, bias=False) for a, b in zip(sizes, sizes[1:]))
        self.dropout = dropout

    def forward(self, x, propagation):
        for i, linear in enumerate(self.weights):
            x = linear(propagation @ x)
            if i < len(self.weights) - 1:
                x = F.dropout(F.relu(x), p=self.dropout, training=self.training)
        return x

    def embedding(self, x, propagation):
        for linear in self.weights[:-1]:
            x = F.relu(linear(propagation @ x))
        return x


def propagation(data, name, seed):
    if name in ('mlp', 'no_edges'):
        return torch.eye(len(data['y']))
    a = data['a']
    if name == 'shuffled':
        generator = torch.Generator().manual_seed(seed + 12345)
        permutation = torch.randperm(len(a), generator=generator)
        # Preserve graph topology/edge count, destroy node-feature/label alignment.
        a = a[permutation][:, permutation]
    elif name != 'gcn':
        raise ValueError(f'unknown experiment {name}')
    return normalize(a)


def metrics(logits, y, indices):
    selected, target = logits[indices], y[indices]
    predicted = selected.argmax(1)
    confusion = torch.bincount(target * 3 + predicted, minlength=9).reshape(3, 3)
    tp = confusion.diag().float()
    f1 = 2 * tp / (confusion.sum(0) + confusion.sum(1)).clamp(min=1)
    return {'loss': F.cross_entropy(selected, target).item(),
            'accuracy': (predicted == target).float().mean().item(),
            'macro_f1': f1.mean().item(), 'confusion': confusion.tolist()}


def fit(data, name, seed, config, out):
    torch.manual_seed(seed)
    model = Network(config['hidden'], config['layers'], config['dropout'])
    prop = propagation(data, name, seed)
    optimizer = torch.optim.Adam(model.parameters(), lr=config['lr'], weight_decay=5e-4)
    history, best_loss, best_epoch, best_state = [], float('inf'), 0, None
    for epoch in range(1, config['epochs'] + 1):
        model.train()
        optimizer.zero_grad()
        logits = model(data['x'], prop)
        loss = F.cross_entropy(logits[data['train']], data['y'][data['train']])
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            logits = model(data['x'], prop)
            train = metrics(logits, data['y'], data['train'])
            val = metrics(logits, data['y'], data['val'])
        history.append(dict(epoch=epoch, train_loss=train['loss'], val_loss=val['loss'],
                            train_accuracy=train['accuracy'], val_accuracy=val['accuracy']))
        if val['loss'] < best_loss:
            best_loss, best_epoch = val['loss'], epoch
            best_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        logits = model(data['x'], prop)
        embedding = model.embedding(data['x'], prop)
        result = metrics(logits, data['y'], data['test'])
    result.update(name=name, seed=seed, data_seed=config.get('data_seed', seed),
                  best_epoch=best_epoch, val_loss=best_loss)
    checkpoint = {'state_dict': best_state, 'config': config, 'name': name, 'seed': seed,
                  'data': data, 'propagation': prop, 'metrics': result}
    torch.save(checkpoint, out / f'{name}-{seed}.pt')
    with (out / f'{name}-{seed}-history.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(history[0]))
        writer.writeheader()
        writer.writerows(history)
    split = [''] * len(data['y'])
    for partition in ('train', 'val', 'test'):
        for node in data[partition].tolist():
            split[node] = partition
    probabilities = logits.softmax(1)
    with (out / f'{name}-{seed}-predictions.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['node', 'split', 'true_label', 'prediction', 'correct', 'p0', 'p1', 'p2'])
        for node, scores in enumerate(probabilities.tolist()):
            prediction = int(logits[node].argmax())
            target = int(data['y'][node])
            writer.writerow([node, split[node], target, prediction, prediction == target, *scores])
    return result, history, logits, embedding


def plot_run(data, records, out, layers=2):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
    colors = {'gcn': '#0d796f', 'mlp': '#b65a22', 'no_edges': '#777b8b', 'shuffled': '#8b5cb7'}
    for name, (_, history, _, _) in records.items():
        axes[0, 0].plot([v['epoch'] for v in history], [v['val_loss'] for v in history], color=colors[name], label=name)
    axes[0, 0].set(title='Validation loss (checkpoint selection)', xlabel='Epoch', ylabel='Cross entropy')
    axes[0, 0].legend()
    names = list(records)
    axes[0, 1].bar(names, [records[n][0]['accuracy'] for n in names], color=[colors[n] for n in names])
    axes[0, 1].set(title='Held-out test accuracy (one seed)', ylim=(0, 1.05))
    for ax, values, title in ((axes[1, 0], data['x'].numpy(), 'Input features: PCA'),
                              (axes[1, 1], records['gcn'][3].numpy(), 'GCN hidden state: PCA' if layers > 1 else 'GCN input (no hidden layer): PCA')):
        centered = values - values.mean(0)
        u, s, _ = np.linalg.svd(centered, full_matrices=False)
        xy = u[:, :2] * s[:2]
        if xy.shape[1] == 1:
            xy = np.column_stack((xy[:, 0], np.zeros(len(xy))))
        for c in range(3):
            mask = data['y'].numpy() == c
            ax.scatter(xy[mask, 0], xy[mask, 1], s=22, label=f'Class {c}', alpha=0.8)
        ax.set(title=title, xlabel='PC1', ylabel='PC2')
        ax.legend(fontsize=8)
    fig.savefig(out / 'experiment.png', dpi=180)
    fig.savefig(out / 'experiment.svg')
    plt.close(fig)


def evaluate(path, out):
    checkpoint = torch.load(path, map_location='cpu', weights_only=True)
    config, data = checkpoint['config'], checkpoint['data']
    model = Network(config['hidden'], config['layers'], config['dropout'])
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    with torch.no_grad():
        logits = model(data['x'], checkpoint['propagation'])
    report = metrics(logits, data['y'], data['test'])
    out.mkdir(parents=True, exist_ok=True)
    (out / 'evaluation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, help='New experiment directory; defaults to runs/<UTC timestamp>')
    parser.add_argument('--overwrite', action='store_true', help='Allow replacing files in an existing output directory')
    parser.add_argument('--data-seed', type=int, help='Fix graph, features and split across model seeds')
    parser.add_argument('--seeds', type=int, nargs='+', default=[7, 17, 27])
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--layers', type=int, choices=range(1, 9), default=2)
    parser.add_argument('--hidden', type=int, default=16)
    parser.add_argument('--dropout', type=float, default=0.3)
    parser.add_argument('--lr', type=float, default=0.01)
    parser.add_argument('--p-in', type=float, default=0.18)
    parser.add_argument('--p-out', type=float, default=0.015)
    parser.add_argument('--noise', type=float, default=1.5)
    parser.add_argument('--evaluate', type=Path, help='Evaluate a trusted local .pt checkpoint without training')
    args = parser.parse_args(argv)
    if args.epochs <= 0 or args.hidden <= 0 or args.lr <= 0 or not 0 <= args.dropout < 1:
        parser.error('epochs, hidden and lr must be positive; dropout must be in [0,1)')
    if not all(math.isfinite(getattr(args, k)) for k in ('lr', 'dropout', 'noise', 'p_in', 'p_out')):
        parser.error('numeric parameters must be finite')
    if not (0 <= args.p_in <= 1 and 0 <= args.p_out <= 1) or args.noise < 0:
        parser.error('edge probabilities must be in [0,1]; noise must be nonnegative')
    if len(args.seeds) != len(set(args.seeds)) or any(s < 0 or s >= 2**32 for s in args.seeds):
        parser.error('seeds must be distinct integers in [0, 2**32)')
    if args.data_seed is not None and not 0 <= args.data_seed < 2**32:
        parser.error('data-seed must be in [0, 2**32)')
    if args.out is None:
        args.out = Path(__file__).resolve().parents[1] / 'runs' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    if args.out.exists() and not args.out.is_dir():
        parser.error(f'output path is not a directory: {args.out}')
    if args.out.exists() and any(args.out.iterdir()) and not args.overwrite:
        parser.error(f'output directory is not empty: {args.out}; choose another path or use --overwrite')
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)
    if args.evaluate:
        evaluate(args.evaluate, args.out)
        return
    args.out.mkdir(parents=True, exist_ok=True)
    config = {k: getattr(args, k) for k in ('epochs', 'layers', 'hidden', 'dropout', 'lr', 'p_in', 'p_out', 'noise')}
    results, first_records = [], {}
    for seed in args.seeds:
        data_seed = seed if args.data_seed is None else args.data_seed
        config['data_seed'] = data_seed
        data = make_graph(data_seed, p_in=args.p_in, p_out=args.p_out, noise=args.noise)
        for name in ('gcn', 'mlp', 'no_edges', 'shuffled'):
            record = fit(data, name, seed, config, args.out)
            results.append(record[0])
            if seed == args.seeds[0]:
                first_records[name] = record
            print(f"{name:9} seed={seed} test={record[0]['accuracy']:.3f} macroF1={record[0]['macro_f1']:.3f}")
    plot_run(make_graph(args.seeds[0] if args.data_seed is None else args.data_seed, p_in=args.p_in, p_out=args.p_out, noise=args.noise), first_records, args.out, args.layers)
    summary = {name: {metric: {'mean': float(np.mean(values)), 'std': float(np.std(values, ddof=1)) if len(values) > 1 else None}
                      for metric in ('accuracy', 'macro_f1')
                      for values in [[row[metric] for row in results if row['name'] == name]]}
               for name in first_records}
    report = {'dataset': 'synthetic 3-block graph; transductive node classification',
              'nodes': 180, 'features': 16, 'split_sizes': {'train': 24, 'val': 36, 'test': 120},
              'config': {**config, 'data_seed': args.data_seed}, 'seeds': args.seeds, 'results': results, 'summary': summary,
              'seed_protocol': 'fixed graph/features/split; vary model and shuffle seeds' if args.data_seed is not None else 'vary graph/features/split/model seeds together',
              'environment': {'python': platform.python_version(), 'torch': torch.__version__, 'numpy': np.__version__, 'device': 'cpu'}}
    (args.out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    (args.out / 'results.js').write_text('window.GNN_RESULTS = ' + json.dumps(report) + ';\n')
    write_report(report, args.out)
    print(f'Open report: {args.out.resolve() / "report.html"}')


if __name__ == '__main__':
    main()
