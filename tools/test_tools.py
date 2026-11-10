import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

HERE = Path(__file__).resolve().parent


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fetch = load('fetch_papers', 'fetch-papers.py')
builder = load('build_guide', 'build-guide.py')


class ToolTests(unittest.TestCase):
    def test_restricted_record_is_explicit(self):
        report = fetch.download({'id': 'restricted', 'pdf_url': None})
        self.assertEqual(report['status'], 'unavailable')
        self.assertIn('reason', report)

    def test_network_failure_is_reported(self):
        with patch('urllib.request.urlopen', side_effect=urllib.error.URLError('test failure')):
            report = fetch.download({'id': 'missing', 'pdf_url': 'https://example.invalid/paper.pdf'})
        self.assertEqual(report['status'], 'failed')
        self.assertIn('test failure', report['reason'])

    def test_html_is_rejected_as_pdf(self):
        from io import BytesIO
        response = BytesIO(b'<html>not a PDF</html>')
        response.url = 'https://example.invalid/error'
        with patch('urllib.request.urlopen', return_value=response):
            report = fetch.download({'id': 'html-error', 'pdf_url': 'https://example.invalid/paper.pdf'})
        self.assertEqual(report['status'], 'failed')
        self.assertIn('not a PDF', report['reason'])

    def test_cached_pdf_identity_and_hash(self):
        report = fetch.download({'id': 'gcn2017', 'pdf_url': 'https://arxiv.org/pdf/1609.02907'})
        self.assertEqual(report['status'], 'downloaded')
        self.assertTrue(report['cache_reused'])
        self.assertEqual(len(report['sha256']), 64)
        self.assertIn('Kipf', report['first_page_excerpt'])

    def test_build_and_missing_input(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ('source', 'content', 'tools', 'outputs'):
                (root / name).mkdir()
            for file in ('source/manifest.json', 'content/gnn-introduction.md', 'tools/guide-template.html'):
                (root / file).write_bytes((HERE.parent / file).read_bytes())
            with patch.object(builder, 'ROOT', root):
                builder.build()
                output = (root / 'outputs/gnn-guide.html').read_text()
                self.assertNotIn('__ARTICLE__', output)
                self.assertIn('../source/papers/gcn2017.pdf', output)
                self.assertIn('全文未取得', output)
                (root / 'source/manifest.json').unlink()
                with self.assertRaises(FileNotFoundError):
                    builder.build()


if __name__ == '__main__':
    unittest.main()
