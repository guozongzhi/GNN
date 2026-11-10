from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
 errors=[]; remote=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:remote.append(r.url) if r.url.startswith(('https://','http://')) else None)
 page.goto((root/'outputs/gnn-guide.html').as_uri())
 page.wait_for_load_state('networkidle')
 assert page.locator('.node').count()==6
 assert page.locator('#node-output').inner_text()=='1.0000'
 page.get_by_role('button',name='下一层',exact=False).click()
 assert abs(float(page.locator('#node-output').inner_text())-1/3)<1e-4
 page.locator('#normalization').select_option('mean')
 page.get_by_role('button',name='重置',exact=True).click()
 page.locator('#normalization').select_option('mean')
 page.get_by_role('button',name='下一层',exact=False).click()
 page.get_by_role('button',name='选择节点 E',exact=True).click()
 assert abs(float(page.locator('#node-output').inner_text())-1/3)<1e-4
 page.locator('#bridge').uncheck()
 assert abs(float(page.locator('#node-output').inner_text())-1/2)<1e-4
 page.locator('#self').uncheck()
 assert float(page.locator('#node-output').inner_text())==0
 page.locator('#depth').fill('8')
 assert '第 8 层' in page.locator('#layer-label').inner_text()
 page.get_by_role('button',name='重置',exact=True).click()
 assert page.locator('#depth').input_value()=='0'
 assert page.locator('#confusion-select option').count()==12
 page.locator('#confusion-select').select_option('1')
 assert page.locator('#confusion-matrix tbody tr').count()==3
 checks.append('Six-node propagation, normalization, self-loops, edge ablation, depth, reset, confusion selector: passed')
 missing=[]
 for href in page.locator('a').evaluate_all('(items)=>items.map(a=>a.getAttribute("href"))'):
  if href and not href.startswith(('http:','https:','#')):
   target=root/'outputs'/href
   if not target.exists():missing.append(href)
 assert not missing,missing
 for anchor in page.locator('.sidebar a').evaluate_all('(items)=>items.map(a=>a.getAttribute("href").slice(1))'):
  assert page.locator('[id="'+anchor+'"]').count()==1,anchor
 checks.append('All local links and table-of-contents anchors exist: passed')
 page.evaluate("document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0,0)")
 page.wait_for_function('scrollY === 0')
 page.screenshot(path=str(root/'outputs/guide-desktop.png'))
 page.locator('#interactive-lab').screenshot(path=str(root/'outputs/message-passing.png'))
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'desktop overflow'
 page.set_viewport_size({'width':390,'height':844})
 page.evaluate('window.scrollTo(0,0)')
 page.screenshot(path=str(root/'outputs/guide-mobile.png'))
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'mobile overflow'
 page.locator('#interactive-lab').screenshot(path=str(root/'outputs/message-passing-mobile.png'))
 checks.append('Desktop 1440px and mobile 390px: no page-level horizontal overflow')
 assert not errors,errors
 assert not remote,remote
 checks.append('No JavaScript errors; no external network requests')
 browser.close()
(root/'outputs/browser-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print('\n'.join(checks))
