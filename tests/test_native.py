"""Exercise the real app, using HTTP when the environment permits it."""
from pathlib import Path
import json,threading,http.server,functools,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];PRE=ROOT/'previews';PRE.mkdir(exist_ok=True)
checks=[];errors=[];external=[];mode='Native HTTP'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT/'public')));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
def check(name,ok):
 checks.append({'name':name,'passed':bool(ok)})
 if not ok:print('FAIL',name)
def goto_slide(p,n):
 p.locator('[data-action=contents]').click();p.locator(f'#dialog [data-jump="{n}"]').click();p.wait_for_timeout(200)
def no_horizontal(p):return p.evaluate('document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1')
try:
 with sync_playwright() as pw:
  launch={'headless':True}
  if Path('/usr/bin/chromium').exists():launch['executable_path']='/usr/bin/chromium'
  b=pw.chromium.launch(**launch);ctx=b.new_context(viewport={'width':1440,'height':900},accept_downloads=True);p=ctx.new_page();p.set_default_timeout(5000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('request',lambda r:external.append(r.url) if not r.url.startswith((origin,'blob:','data:')) else None)
  try:p.goto(origin+'/index.html',wait_until='networkidle',timeout=10000)
  except Exception:
   mode='Chromium document injection (environment denied local HTTP navigation)';p.close();p=ctx.new_page();p.set_default_timeout(5000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:external.append(r.url) if not r.url.startswith((origin,'blob:','data:')) else None);p.set_content((ROOT/'public/index.html').read_text(),wait_until='load')
  check('Main entry point loads one slide',p.locator('.slide:visible').count()==1)
  check('No clocks or presenter controls are rendered',p.locator('[data-action="speaker"],[data-action="settings"],[data-timer],[data-action="work-card"]').count()==0)
  for n in range(1,12):
   goto_slide(p,n);check(f'Screen {n}: no elapsed timing text',not __import__('re').search(r'\b\d{1,2}:\d{2}\b',p.locator(f'[data-scene="{n}"]').inner_text()));check(f'Screen {n}: fits desktop width',no_horizontal(p));p.screenshot(path=str(PRE/f'slide-{n:02d}.png'))
  for n,id,values in [(4,'job',['task','bridge']),(6,'readme',['before','after']),(7,'presence',['about','github','website']),(9,'sharing',['confirmed','outreach','post'])]:
   goto_slide(p,n)
   for val in values:
    p.locator(f'[data-panel="{id}"][data-value="{val}"]').click();check(f'{id} tab {val} reveals content',len(p.locator(f'#{id}-example').inner_text())>40);check(f'{id} tab {val} active state',p.locator(f'[data-panel="{id}"][data-value="{val}"]').get_attribute('aria-pressed')=='true');p.screenshot(path=str(PRE/f'{id}-{val}.png'))
  goto_slide(p,10);p.locator('.mainnav [data-view=work]').click();check('In practice opens without diagnostic',p.locator('.route-card').count()==4)
  for group,count in [('existing',6),('showcase',2),('all',12),('starting',4)]:
   p.locator(f'#work-filters [data-work="{group}"]').click();check(f'Activity filter {group}',p.locator('.route-card').count()==count)
  p.screenshot(path=str(PRE/'in-practice.png'))
  p.locator('#work-filters [data-work=all]').click()
  for id in ['about','profile','readme','extension','case','question','bridge','practice','mission','pr','share','website']:
   p.locator(f'#route-grid [data-route="{id}"]').click();check(f'Activity {id} has steps and references',p.locator('#dialog .dialog-steps li').count()==3 and p.locator('#dialog a').count()>0);p.locator('.dialog-close').click()
  p.locator('#route-grid [data-route=readme]').click();p.locator('#dialog [data-template=readme]').click()
  with p.expect_download() as dl:p.locator('#dialog [data-save-text]').click()
  check('Markdown download contains actual outline','My approach and contribution' in Path(dl.value.path()).read_text());p.locator('.dialog-close').click()
  p.locator('.mainnav [data-view=guide]').click()
  for key in ['start','projects','explaining','github','platforms','permissions','writing','tools','sources','about']:
   p.locator(f'#guide-nav [data-guide="{key}"]').click();check(f'Guide {key} contains readable material',len(p.locator('#guide-content').inner_text())>100)
  with p.expect_download() as dl:p.locator('#guide-content [data-pdf=student-worksheet]').click()
  check('Embedded student PDF downloads',Path(dl.value.path()).read_bytes().startswith(b'%PDF'))
  with p.expect_download() as dl:p.locator('#guide-content [data-action=export-guide]').first.click()
  check('Complete Markdown guide downloads','Portfolio platforms' in Path(dl.value.path()).read_text() or 'Choose a place' in Path(dl.value.path()).read_text())
  p.locator('#guide-nav [data-guide=tools]').click();p.locator('#guide-content [data-prompt=pulse]').click();check('AI prompt is text rather than a model call',p.locator('#copy-text').input_value().strip()!='');p.locator('.dialog-close').click()
  p.locator('#guide-nav [data-guide=sources]').click();p.locator('#source-search').fill('Squarespace');check('Source search filters results',p.locator('.source-entry').count()==2)
  p.locator('#guide-content [data-action=return]').click();check('Return keeps previous slide',p.locator('[data-scene="10"]').is_visible())
  p.locator('.mainnav [data-artifact=collection]').click();check('All original portfolio selections remain',p.locator('.portfolio-card').count()==12)
  for lens,count in [('Builder',2),('Storyteller',3),('Expert',3),('Researcher',2),('Analyst',2),('All',12)]:
   p.locator(f'[data-lens="{lens}"]').click();check(f'Artifact {lens} filter',p.locator('.portfolio-card').count()==count)
  p.locator('#portfolio-search').fill('Sukhman');check('Artifact search',p.locator('.portfolio-card').count()==1);p.locator('.portfolio-card').click();check('Portfolio detail opens',p.locator('#dialog a').count()>0);p.keyboard.press('Escape');check('Escape closes dialog',not p.locator('#dialog').is_visible());p.locator('#portfolio-search').fill('')
  p.screenshot(path=str(PRE/'artifact.png'));p.locator('.artifact-tabs [data-artifact=writing]').click()
  for k in ['Builder','Analyst','Expert','Researcher','Storyteller']:
   p.locator(f'[data-kit="{k}"]').click();check(f'Writing guide {k} preserved',p.locator('#writing-paper tbody tr').count()==6)
  p.screenshot(path=str(PRE/'writing-kit.png'));p.locator('.artifact-tabs [data-artifact=readings]').click();check('All nine reading selections remain',p.locator('.reading-card').count()==9)
  p.locator('[data-action=return]').last.click();goto_slide(p,1);p.locator('#main').focus();p.keyboard.press('ArrowRight');check('Keyboard moves to next slide',p.locator('[data-scene="2"]').is_visible())
  p.locator('[data-action=read-all]').click();check('Read-all displays all 11 screens',p.locator('.slide:visible').count()==11);p.locator('[data-action=read-all]').click()
  for width,height in [(1366,768),(375,812)]:
   p.set_viewport_size({'width':width,'height':height})
   for n in range(1,12):
    goto_slide(p,n);check(f'{width}px screen {n} no horizontal overflow',no_horizontal(p))
    if width==1366:check(f'Projector screen {n} clears footer',p.evaluate("document.querySelector('.slide:not([hidden])').getBoundingClientRect().bottom <= document.querySelector('.deckfooter').getBoundingClientRect().top"))
   if width==1366:
    for sn,pid,val in [(4,'job','bridge'),(6,'readme','after'),(7,'presence','github'),(7,'presence','website'),(9,'sharing','outreach'),(9,'sharing','post')]:
     goto_slide(p,sn);p.locator(f'[data-panel="{pid}"][data-value="{val}"]').click();check(f'Projector {pid}/{val} clears footer',p.evaluate("document.querySelector('.slide:not([hidden])').getBoundingClientRect().bottom <= document.querySelector('.deckfooter').getBoundingClientRect().top"))
   for view in ['work','guide']:
    p.locator(f'.mainnav [data-view="{view}"]').click();check(f'{width}px {view} no horizontal overflow',no_horizontal(p))
   if width==375:p.screenshot(path=str(PRE/'mobile-guide.png'))
   p.locator('.mainnav [data-artifact=collection]').click();check(f'{width}px collection no horizontal overflow',no_horizontal(p));p.locator('.mainnav [data-view=session]').click()
  if mode=='Native HTTP':
   p.goto(origin+'/artifact.html',wait_until='networkidle');check('Standalone Artifact opens collection',p.locator('.portfolio-card').count()==12)
   p.goto(origin+'/index.html#session/6',wait_until='networkidle');check('Direct slide URL works',p.locator('[data-scene="6"]').is_visible());p.reload(wait_until='networkidle');check('Reload preserves slide URL',p.locator('[data-scene="6"]').is_visible())
  check('No uncaught JavaScript errors',not errors);check('No automatic external requests',not external)
  b.close()
finally:server.shutdown()
report={'environment':mode,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'errors':errors,'external_requests':external};(ROOT/'docs/NATIVE-TEST-RESULTS.json').write_text(json.dumps(report,indent=2));print(mode,report['passed'],'/',report['total']);assert report['passed']==report['total']
