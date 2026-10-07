from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'public/index.html').read_text()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=1)
 page=context.new_page();errors=[];logs=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m: logs.append(m.text) if m.type=='error' else None)
 context.route('https://workshop.example/**',lambda route:route.fulfill(status=200,content_type='text/html',body=html))
 mode='mocked-https'
 try:
  page.goto('https://workshop.example/',timeout=10000)
 except Exception as e:
  print('Mocked HTTPS navigation:',str(e).splitlines()[0]);mode='document-injection';page.close();page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m: logs.append(m.text) if m.type=='error' else None);page.set_content(html,wait_until='load')
 page.wait_for_timeout(400)
 for n in range(1,15):
  page.locator('#main').focus();page.keyboard.press('Home') if n==1 else page.keyboard.press('ArrowRight')
  page.wait_for_timeout(100)
  page.screenshot(path=str(ROOT/f'previews/slide-{n:02d}.png'),full_page=True)
 page.locator('[data-artifact=collection]').first.click();page.wait_for_timeout(100);page.screenshot(path=str(ROOT/'previews/artifact.png'),full_page=True)
 page.locator('[data-artifact=writing]').first.click();page.screenshot(path=str(ROOT/'previews/writing-kit.png'),full_page=True)
 print(json.dumps({'mode':mode,'errors':errors,'console':logs,'title':page.title(),'slides':page.locator('.slide').count(),'storage':page.evaluate('(()=>{try {localStorage.setItem("test", "yes");localStorage.removeItem("test");return true;}catch{return false;}})()')},indent=2))
 browser.close()
