"""Browser acceptance test for any freshly generated experiment directory."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def check(folder):
    folder = Path(folder).resolve()
    report = json.loads((folder / 'results.json').read_text())
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        errors, remote = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: remote.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
        page.goto((folder / 'report.html').as_uri())
        page.wait_for_load_state('networkidle')
        assert page.locator('details').count() == len(report['results'])
        page.locator('summary').first.click()
        counts = [int(text) for text in page.locator('details').first.locator('tbody td').all_text_contents()]
        assert counts == [n for row in report['results'][0]['confusion'] for n in row]
        for link in page.locator('a').evaluate_all('(items) => items.map(a => a.getAttribute("href"))'):
            assert (folder / link).is_file(), link
        assert page.locator('img').evaluate('(img) => img.complete && img.naturalWidth > 0')
        for width, name in ((1280, 'desktop'), (390, 'mobile')):
            page.set_viewport_size({'width': width, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), name
            page.evaluate('window.scrollTo(0, 0)')
            page.screenshot(path=str(folder / f'report-{name}.png'))
        assert not errors, errors
        assert not remote, remote
        browser.close()
    print('Report controls, confusion values, local files, images, desktop/mobile and offline loading: passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    check(parser.parse_args().folder)
