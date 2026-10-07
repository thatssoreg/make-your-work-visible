"""Native HTTP-browser smoke checks for environments that permit local navigation.
Run after python build.py and playwright install chromium. Does not use a storage mock.
"""
from pathlib import Path
import json,threading,http.server,functools
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];checks=[];errors=[];external=[]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT/'public')))
threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
def check(name,ok):
 checks.append({'name':name,'passed':bool(ok)})
 if not ok:print('FAIL:',name)
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True);ctx=browser.new_context(viewport={'width':1440,'height':900},accept_downloads=True);p=ctx.new_page();p.set_default_timeout(10000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:external.append(r.url) if not r.url.startswith(origin) and not r.url.startswith('blob:') else None)
  p.goto(origin+'/index.html',wait_until='networkidle');check('Real HTTP document loads',p.locator('.slide:visible').count()==1)
  p.locator('[data-action=work-card]').first.click();p.locator('#work-start').select_option('project');p.locator('#work-title').fill('Native persistence check');p.locator('#remember').check();p.locator('#work-form button[type=submit]').click();p.reload(wait_until='networkidle');p.locator('[data-action=contents]').click();p.locator('#dialog [data-jump="6"]').click();check('Opt-in card survives real reload','Native persistence check' in p.locator('[data-scene="6"] [data-own-work]').inner_text());
  p.locator('[data-help-id=own-fluency][data-help-level=nudge]').click();check('Real help reveal works',p.locator('#help-panel-own-fluency').is_visible())
  p.locator('[data-timer-toggle=own-fluency]').click();p.wait_for_timeout(1300);check('Real clock counts down',p.locator('[data-timer=own-fluency] .timer-display').inner_text()!='3:00');p.locator('[data-timer-toggle=own-fluency]').click()
  with p.expect_download() as out:p.locator('[data-scene="6"] [data-download=workbook]').click()
  check('Real Markdown download contains chosen title','Native persistence check' in Path(out.value.path()).read_text())
  p.locator('.mainnav [data-view=guide]').click();p.locator('#guide-nav [data-guide=about]').click()
  for id in ['student-worksheet','facilitator-guide','run-sheet']:
   with p.expect_download() as out:p.locator(f'[data-pdf={id}]').click()
   check(f'{id}: embedded PDF downloads as PDF',Path(out.value.path()).read_bytes().startswith(b'%PDF'))
  p.locator('#guide-content [data-action=return]').click();check('Native return preserves prior slide',p.locator('[data-scene="6"]').is_visible())
  p.locator('[data-action=work-card]').first.click();p.on('dialog',lambda d:d.accept());p.locator('[data-action=clear-card]').click();p.reload(wait_until='networkidle');check('Native clear removes stored context','Native persistence check' not in p.locator('#main').inner_text())
  p.goto(origin+'/artifact.html',wait_until='networkidle');check('Native Artifact entry point loads twelve selections',p.locator('.portfolio-card').count()==12)
  p.locator('[data-lens=Builder]').click();check('Native collection filter works',p.locator('.portfolio-card').count()==2)
  p.locator('.artifact-tabs [data-artifact=writing]').click();p.locator('[data-kit=Researcher]').click();check('Native writing kit retains six sections',p.locator('#writing-paper tbody tr').count()==6)
  p.goto(origin+'/index.html#session/13',wait_until='networkidle');check('Direct slide hash works',p.locator('[data-scene="13"]').is_visible())
  p.locator('#main').focus();p.keyboard.press('Home');check('Native keyboard navigation works',p.locator('[data-scene="1"]').is_visible())
  p.set_viewport_size({'width':375,'height':812});check('Narrow native viewport has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth+1'))
  p.set_viewport_size({'width':1366,'height':768});
  for n in range(1,15):
   p.locator('[data-action=contents]').click();p.locator(f'#dialog [data-jump="{n}"]').click();p.wait_for_timeout(220);check(f'Native screen {n} has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth+1'))
  check('Native document has no uncaught errors',not errors);check('Native app makes no external requests',not external)
  browser.close()
finally:
 server.shutdown()
report={'environment':'Native Chromium over a temporary local HTTP server; real browser storage and reload, not a storage mock','checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'errors':errors,'external_requests':external}
(ROOT/'docs/NATIVE-TEST-RESULTS.json').write_text(json.dumps(report,indent=2));print(report['passed'],'/',report['total'],'native checks passed')
if report['passed']!=report['total']:raise SystemExit(1)
