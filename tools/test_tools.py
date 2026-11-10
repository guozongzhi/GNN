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


class ProvenanceTests(unittest.TestCase):
    def test_cached_download_keeps_original_retrieval_time(self):
        previous = next(row for row in json.loads((HERE.parent / 'source/manifest.json').read_text()) if row['id'] == 'gcn2017')
        report = fetch.download(previous, previous)
        self.assertEqual(report['retrieved_at'], previous['retrieved_at'])
        self.assertEqual(report['sha256'], previous['sha256'])

    def test_corruption_is_rejected_without_overwriting_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'source/papers').mkdir(parents=True)
            row = {'id': 'test', 'pdf_url': 'https://example.invalid/test.pdf', 'sha256': '0' * 64,
                   'status': 'downloaded', 'retrieved_at': 'original timestamp'}
            (root / 'source/catalog.json').write_text(json.dumps([row]))
            manifest = root / 'source/manifest.json'
            manifest.write_text(json.dumps([row]))
            original = manifest.read_bytes()
            (root / 'source/papers/test.pdf').write_bytes(b'%PDF-corrupted')
            with patch.object(fetch, 'ROOT', root), self.assertRaises(SystemExit):
                fetch.main()
            self.assertEqual(manifest.read_bytes(), original)
            failure = json.loads((root / 'tmp/download-report.json').read_text())[0]
            self.assertIn('SHA-256 mismatch', failure['reason'])

    def test_readonly_verifier_checks_papers_and_pages(self):
        import hashlib
        verifier = load('verify_sources', 'verify-sources.py')
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'source').mkdir()
            (root / 'source/file').write_bytes(b'evidence')
            record = {'id': 'one', 'status': 'downloaded', 'file': 'source/file',
                      'bytes': 8, 'sha256': hashlib.sha256(b'evidence').hexdigest()}
            (root / 'source/manifest.json').write_text(json.dumps([record]))
            (root / 'source/web-manifest.json').write_text(json.dumps([{**record, 'file': 'file'}]))
            self.assertEqual(verifier.verify(root), (2, 0))
            (root / 'source/file').write_bytes(b'changed!')
            with self.assertRaises(ValueError):
                verifier.verify(root)


if __name__ == '__main__':
    unittest.main()
