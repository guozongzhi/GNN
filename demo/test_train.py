import tempfile
import unittest
from pathlib import Path
import torch
from train import Network, evaluate, fit, make_graph, metrics, normalize, propagation


class DemoTests(unittest.TestCase):
    def test_normalization_by_hand_and_isolated_node(self):
        a = torch.tensor([[0., 1., 0.], [1., 0., 0.], [0., 0., 0.]])
        expected = torch.tensor([[.5, .5, 0.], [.5, .5, 0.], [0., 0., 1.]])
        torch.testing.assert_close(normalize(a), expected)

    def test_node_permutation_equivariance(self):
        data = make_graph()
        model = Network().eval()
        p = torch.randperm(len(data['y']))
        a = normalize(data['a'])
        torch.testing.assert_close(model(data['x'][p], a[p][:, p]), model(data['x'], a)[p])

    def test_split_disjoint_complete_and_reproducible(self):
        a, b = make_graph(), make_graph()
        for key in a:
            torch.testing.assert_close(a[key], b[key])
        sets = [set(a[k].tolist()) for k in ('train', 'val', 'test')]
        self.assertFalse(sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
        self.assertEqual(len(set.union(*sets)), len(a['y']))
        self.assertFalse(torch.diag(a['a']).any())

    def test_mlp_equals_gcn_with_self_loops_only(self):
        data = make_graph()
        torch.testing.assert_close(propagation(data, 'no_edges', 7), normalize(torch.zeros_like(data['a'])))
        torch.testing.assert_close(propagation(data, 'mlp', 7), propagation(data, 'no_edges', 7))

    def test_labels_outside_train_do_not_change_gradient(self):
        data = make_graph()
        model = Network(dropout=0).eval()
        prop = normalize(data['a'])
        def gradient(y):
            model.zero_grad()
            torch.nn.functional.cross_entropy(model(data['x'], prop)[data['train']], y[data['train']]).backward()
            return [p.grad.clone() for p in model.parameters()]
        changed = data['y'].clone()
        changed[data['test']] = (changed[data['test']] + 1) % 3
        changed[data['val']] = (changed[data['val']] + 1) % 3
        for x, y in zip(gradient(data['y']), gradient(changed)):
            torch.testing.assert_close(x, y)

    def test_metric_values(self):
        logits = torch.tensor([[8., 0., 0.], [0., 8., 0.], [0., 0., 8.]])
        report = metrics(logits, torch.arange(3), torch.arange(3))
        self.assertEqual(report['accuracy'], 1.)
        self.assertEqual(report['macro_f1'], 1.)

    def test_training_and_checkpoint_reload(self):
        torch.set_num_threads(1)
        data = make_graph()
        config = dict(hidden=16, layers=2, dropout=.3, lr=.01, epochs=80)
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)
            result, history, _, _ = fit(data, 'gcn', 7, config, out)
            loaded = evaluate(out / 'gcn-7.pt', out)
            self.assertEqual(result['accuracy'], loaded['accuracy'])
            self.assertEqual(result['confusion'], loaded['confusion'])
            self.assertLess(history[-1]['train_loss'], history[0]['train_loss'])
            self.assertGreater(result['accuracy'], .7)

    def test_invalid_inputs(self):
        for a in (torch.zeros(2, 3), torch.tensor([[0., -1.], [-1., 0.]]), torch.tensor([[0., 1.], [0., 0.]])):
            with self.assertRaises(ValueError):
                normalize(a)
        for options in ({'p_in': 1.1}, {'p_out': -.1}, {'noise': -1}, {'per_class': 20}):
            with self.assertRaises(ValueError):
                make_graph(**options)
        with self.assertRaises(ValueError):
            Network(layers=0)
        with self.assertRaises(ValueError):
            propagation(make_graph(), 'unknown', 7)


if __name__ == '__main__':
    unittest.main()
