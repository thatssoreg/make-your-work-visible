"""UI contract tests on the exact standalone HTML.
This environment blocks file/HTTP navigation. Tests inject the document into Chromium.
Storage restoration is separately tested with a labeled in-memory test double.
"""
from pathlib import Path
import json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'public/index.html').read_text()
REPORT={'environment':'Chromium, document injection; native file/HTTP navigation blocked by browser policy','checks':[],'page_errors':[],'console_errors':[],'requests':[]}
def check(name,condition,detail=''):
 REPORT['checks'].append({'name':name,'passed':bool(condition),'detail':detail})
 print(('PASS' if condition else 'FAIL')+':',name,detail,flush=True)
def attach(page):
 page.on('pageerror',lambda e:REPORT['page_errors'].append(str(e)))
 page.on('console',lambda m:REPORT['console_errors'].append(m.text) if m.type=='error' else None)
 page.on('request',lambda r:REPORT['requests'].append(r.url))
def goto(page,n):
 page.locator('[data-action=contents]').click();page.locator(f'#dialog [data-jump="{n}"]').click()
def newpage(context,store=None,viewport=None,clock=False):
 p=context.new_page();p.set_default_timeout(5000);attach(p)
 if clock:p.clock.install()
 if viewport:p.set_viewport_size(viewport)
 if store is not None:p.evaluate('(s)=>{const data={...s};Object.defineProperty(window,"localStorage",{configurable:true,value:{getItem:k=>data[k]??null,setItem:(k,v)=>{data[k]=String(v)},removeItem:k=>{delete data[k]}}});window.__storage_test_double=data;}',store)
 p.set_content(HTML,wait_until='load');p.wait_for_timeout(250);return p
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 ctx=browser.new_context(viewport={'width':1440,'height':900},accept_downloads=True)
 p=newpage(ctx,clock=True)
 check('Updated office name is visible','SDS Career Services' in p.locator('.brandtext').inner_text())
 check('Opening is the only default slide',p.locator('.slide:visible').count()==1 and p.locator('[data-scene="1"]').is_visible())
 check('No old office name in displayed source','Career Connections' not in HTML)
 check('Fourteen screens follow the canonical session',p.locator('.slide').count()==14)
 p.locator('#main').focus();p.keyboard.press('ArrowRight');check('Arrow key moves one slide',p.locator('[data-scene="2"]').is_visible());p.keyboard.press('End');check('End reaches the close',p.locator('[data-scene="14"]').is_visible());p.keyboard.press('Home')
 for state in ['project','assignment','job','curiosity','new']:
  goto(p,3);p.locator(f'[data-scene="3"] [data-start="{state}"]').click()
  p.locator('[data-action=work-card]').first.click();p.locator('#work-title').fill('My selected '+state);p.locator('#work-status').select_option('planned');p.locator('#work-form button[type=submit]').click()
  for n in [6,9,11,12]:
   goto(p,n);check(f'{state}: same title at screen {n}','My selected '+state in p.locator(f'[data-scene="{n}"] [data-own-work]').inner_text())
  p.locator('.mainnav [data-view=work]').click();check(f'{state}: router initially limits choices',p.locator('#route-grid .route-card').count()==3)
  p.locator('#all-routes').click();check(f'{state}: all ten remain accessible',p.locator('#route-grid .route-card').count()==10)
  p.locator('#work-view [data-action=return]').click()
 goto(p,6)
 check('New exercise defaults to task only',not p.locator('#help-panel-own-fluency').is_visible())
 p.locator('[data-help-id=own-fluency][data-help-level=nudge]').click();check('State-tailored nudge is available','music' in p.locator('#help-panel-own-fluency').inner_text().lower())
 p.locator('[data-help-id=own-fluency][data-help-level=example]').click();check('Worked example uses other material','class' in p.locator('#help-panel-own-fluency').inner_text().lower())
 p.locator('[data-help-id=own-fluency][data-help-level=task]').click();check('Support can be removed without reset',not p.locator('#help-panel-own-fluency').is_visible() and 'My selected new' in p.locator('[data-scene="6"] [data-own-work]').inner_text())
 for id,n in [('object',3),('shared-fluency',5),('own-fluency',6),('shared-legibility',8),('own-legibility',9),('reach',11),('work',12)]:
  goto(p,n);p.locator(f'[data-help-id="{id}"][data-help-level=nudge]').click();check(f'{id}: nudge opens',p.locator(f'#help-panel-{id}').is_visible());p.locator(f'[data-help-id="{id}"][data-help-level=example]').click();check(f'{id}: example opens',len(p.locator(f'#help-panel-{id}').inner_text())>80);p.locator(f'[data-help-id="{id}"][data-help-level=task]').click()
 goto(p,4)
 for i in range(4):p.locator(f'[data-model="{i}"]').click();check(f'Model step {i+1} has a concrete explanation',len(p.locator('#model-panel').inner_text())>100)
 p.locator('#model-panel [data-download=measurement-brief]').click();check('Example links to actual planning artifact','No usage data' in p.locator('#copy-text').input_value());p.keyboard.press('Escape')
 goto(p,7);before=p.locator('#readme-criteria h3').all_text_contents();p.locator('[data-readme=after]').click();after=p.locator('#readme-criteria h3').all_text_contents();check('Before and after use identical criteria',before==after);check('Improved README does not invent an experiment','not collected usage data' in p.locator('#readme-text').inner_text())
 goto(p,13);check('Peer test removes help controls',p.locator('[data-scene="13"] [data-help]').count()==0);check('Peer test asks for independent explanation','without reading' in p.locator('[data-scene="13"]').inner_text())
 goto(p,9);p.locator('[data-template=readme]').first.click();p.keyboard.press('Escape');check('Dialog Escape restores triggering control',p.evaluate('document.activeElement.dataset.template')=='readme')
 p.locator('[data-action=present]').click();check('Presenter mode hides private context',not p.locator('[data-scene="9"] [data-own-work]').is_visible());p.locator('[data-action=present]').click()
 for guide in ['start','explaining','github','permissions','writing','tools','sources','about']:
  p.locator('.mainnav [data-view=guide]').click();p.locator(f'#guide-nav [data-guide={guide}]').click();check(f'Guide {guide} has a return path',p.locator('#guide-content [data-action=return]').is_visible());p.locator('#guide-content [data-action=return]').click();check(f'Guide {guide} returns to the same slide',p.locator('[data-scene="9"]').is_visible())
 p.locator('.mainnav [data-view=guide]').click();p.locator('#guide-nav [data-guide=about]').click()
 for pdf in ['student-worksheet','facilitator-guide','run-sheet']:
  with p.expect_download() as dl:p.locator(f'[data-pdf={pdf}]').click()
  check(f'{pdf}: embedded PDF download is valid',Path(dl.value.path()).read_bytes().startswith(b'%PDF'))
 p.locator('.mainnav [data-artifact=collection]').click();check('All twelve original portfolios present',p.locator('.portfolio-card').count()==12)
 for lens,amount in [('Builder',2),('Storyteller',3),('Expert',3),('Researcher',2),('Analyst',2)]:
  p.locator(f'[data-lens={lens}]').click();check(f'Artifact {lens} filter',p.locator('.portfolio-card').count()==amount)
 p.locator('[data-lens=All]').click();p.locator('#portfolio-search').fill('zzzzNOTFOUND');check('Artifact empty search has explanation',p.locator('.no-results').is_visible());p.locator('#portfolio-search').fill('Sukhman');check('Artifact search finds named portfolio',p.locator('.portfolio-card').count()==1);p.locator('.portfolio-card').click();check('Portfolio details include evidence boundaries','accuracy' in p.locator('#dialog-body').inner_text().lower());p.locator('[data-kit-link=Builder]').click();check('Collection connects to corresponding writing guide',p.locator('#writing-paper h2').inner_text()=='Explain how the system works')
 for lens in ['Builder','Analyst','Expert','Researcher','Storyteller']:
  p.locator(f'[data-kit={lens}]').click();check(f'{lens}: original six-part guide preserved',p.locator('#writing-paper tbody tr').count()==6);p.locator(f'[data-kit-template={lens}]').click();text=p.locator('#copy-text').input_value();check(f'{lens}: template contains placeholders, not invented results','[Your project' in text and '50GB' not in text and '99%' not in text);p.keyboard.press('Escape')
 p.locator('.artifact-tabs [data-artifact=readings]').click();check('Nine original readings retained',p.locator('.reading-card').count()==9);check('Unverified original link is labeled','could not be rechecked' in p.locator('#artifact-content').inner_text())
 p.locator('.mainnav [data-view=work]').click();p.locator('#all-routes').click() if p.locator('#route-grid .route-card').count()<10 else None
 routes=p.locator('#route-grid [data-route]').evaluate_all('(els)=>els.map(e=>e.dataset.route)')
 for id in routes:
  p.locator(f'#route-grid [data-route={id}]').click();check(f'Route {id}: specific steps, output, fallback',p.locator('#dialog-body li').count()==3 and 'fallback' in p.locator('#dialog-body').inner_text().lower());p.locator('#dialog-body [data-template]').click();check(f'Route {id}: outline is real text',len(p.locator('#copy-text').input_value())>80);p.keyboard.press('Escape')
 # Copy fallback with native clipboard unavailable in opaque origin.
 p.locator(f'#route-grid [data-route=readme]').click();p.locator('#dialog-body [data-template]').click();p.locator('[data-action=copy-text]').click();p.wait_for_timeout(150);check('Clipboard denial offers manual fallback','unavailable' in p.locator('#copy-status').inner_text().lower());
 with p.expect_download() as dl:p.locator('[data-save-text]').click()
 check('Markdown outline downloads',dl.value.suggested_filename.endswith('.md'));p.keyboard.press('Escape')
 goto(p,6)
 with p.expect_download() as dl:p.locator('[data-scene="6"] [data-download=workbook]').click()
 saved=Path(dl.value.path()).read_text();check('Worksheet export keeps selected title','My selected new' in saved);check('Worksheet says it cannot save other tools','does not contain your work from other tools' in saved)
 # Test timers using controlled browser clock; the application itself uses actual deadlines.
 for id,n in [('inventory',3),('shared-fluency',5),('own-fluency',6),('shared-legibility',8),('own-legibility',9),('reach',11),('work',12),('peer',13)]:
  goto(p,n);initial=p.locator(f'[data-timer={id}] .timer-display').inner_text();p.locator(f'[data-timer-toggle={id}]').click();p.clock.fast_forward(2100);later=p.locator(f'[data-timer={id}] .timer-display').inner_text();check(f'{id}: timer runs',initial!=later);p.locator(f'[data-timer-toggle={id}]').click();p.clock.fast_forward(2000);check(f'{id}: timer pauses',p.locator(f'[data-timer={id}] .timer-display').inner_text()==later);p.locator(f'[data-timer-reset={id}]').click();check(f'{id}: timer resets',p.locator(f'[data-timer={id}] .timer-display').inner_text()==initial)
 goto(p,12);p.locator('[data-timer-toggle=work]').click();p.clock.fast_forward(1100);remain=p.locator('[data-timer=work] .timer-display').inner_text();goto(p,13);p.clock.fast_forward(2000);goto(p,12);check('Leaving a slide pauses its timer',p.locator('[data-timer=work] .timer-display').inner_text()==remain)
 p.locator('[data-action=settings]').click();p.locator('[data-duration="45"]').click();check('45-minute plan sets eleven-minute work',p.locator('[data-timer=work] .timer-display').inner_text()=='11:00');goto(p,13);check('45-minute plan sets four-minute peer review',p.locator('[data-timer=peer] .timer-display').inner_text()=='4:00');check('45-minute plan preserves closing slot','40:00–44:00' in p.locator('[data-scene="13"] .scene-context').inner_text());p.locator('[data-timer-toggle=peer]').click();p.clock.fast_forward(241000);check('Timer finishes once and shows revision/close',p.locator('[data-timer=peer] .timer-display').inner_text()=='0:00' and 'Save the revision' in p.locator('#peer-phase').inner_text());p.locator('[data-timer-reset=peer]').click()
 # Native opaque-origin storage failure is an expected fallback, not a pass for native persistence.
 p.locator('[data-action=work-card]').first.click();p.locator('#remember').check();p.locator('#work-form button[type=submit]').click();p.locator('[data-action=work-card]').first.click();check('Unavailable native storage falls back to nonpersistent card',not p.locator('#remember').is_checked());p.keyboard.press('Escape')
 p.close()
 # Labeled storage test double validates restoration, clear behavior, and malformed-data handling.
 q=newpage(ctx,store={});q.locator('[data-action=work-card]').first.click();q.locator('#work-start').select_option('project');q.locator('#work-title').fill('Persistent example');q.locator('#remember').check();q.locator('#work-form button[type=submit]').click();stored=q.evaluate('window.__storage_test_double');check('Opt-in writes the small card only (test double)','Persistent example' in stored.get('sds-work-visible-v1','') and len(stored.get('sds-work-visible-v1',''))<400);q.close()
 q=newpage(ctx,store=stored);goto(q,6);check('Saved work restores across new page (test double)','Persistent example' in q.locator('[data-scene="6"] [data-own-work]').inner_text());q.locator('[data-action=work-card]').first.click();q.on('dialog',lambda d:d.accept());q.locator('[data-action=clear-card]').click();check('Clear removes persisted card (test double)','sds-work-visible-v1' not in q.evaluate('window.__storage_test_double'))
 # Import validation and XSS resistance.
 q.locator('[data-action=work-card]').first.click()
 with q.expect_file_chooser() as chooser:q.locator('[data-action=import-card]').click()
 chooser.value.set_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"schema":999}'})
 q.wait_for_timeout(100);check('Invalid schema is rejected','not a supported' in q.locator('#notification').inner_text())
 payload={'schema':1,'work':{'start':'project','title':'<img src=x onerror="window.attack=true">','status':'planned'}}
 with q.expect_file_chooser() as chooser:q.locator('[data-action=import-card]').click()
 chooser.value.set_files({'name':'safe-card.json','mimeType':'application/json','buffer':json.dumps(payload).encode()});q.wait_for_timeout(100);q.keyboard.press('Escape');goto(q,9);check('Imported title is escaped as text','<img' in q.locator('[data-scene="9"] [data-own-work]').inner_text() and q.locator('[data-own-work] img').count()==0 and q.evaluate('window.attack===undefined'))
 # Editing an unsaved form and exporting does not silently replace the active card.
 q.locator('[data-action=work-card]').first.click();q.locator('#work-title').fill('Unsaved form title')
 with q.expect_download() as dl:q.locator('[data-action=export-card]').click()
 check('JSON export contains edited form values','Unsaved form title' in Path(dl.value.path()).read_text());q.keyboard.press('Escape');check('Export does not silently commit form changes','<img' in q.locator('[data-scene="9"] [data-own-work]').inner_text())
 q.close()
 # Responsive/document layout checks and screenshot inspection inputs.
 layout=[]
 for width,height in [(375,812),(768,1024),(1366,768),(1440,900),(1920,1080)]:
  q=newpage(ctx,viewport={'width':width,'height':height})
  for n in range(1,15):
   goto(q,n);q.wait_for_timeout(230)
   dims=q.evaluate('({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,sh:document.documentElement.scrollHeight})')
   check(f'{width}px: screen {n} has no horizontal overflow',dims['sw']<=dims['cw']+1)
   layout.append({'width':width,'height':height,'slide':n,'page_height':dims['sh']})
   if width==1440:q.screenshot(path=str(ROOT/f'previews/slide-{n:02d}.png'),full_page=True)
   if width==375 and n in [1,3,6,9,13]:q.screenshot(path=str(ROOT/f'previews/mobile-{n:02d}.png'),full_page=True)
  q.locator('.mainnav [data-artifact=collection]').click();q.wait_for_timeout(250);check(f'{width}px: Artifact has no page overflow',q.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth+1'))
  if width==1440:q.screenshot(path=str(ROOT/'previews/artifact.png'),full_page=True)
  q.locator('.artifact-tabs [data-artifact=writing]').click();check(f'{width}px: writing tables scroll within page',q.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth+1'))
  if width==1440:q.screenshot(path=str(ROOT/'previews/writing-kit.png'),full_page=True)
  q.close()
 REPORT['layout']=layout
 check('Task-only desktop screens fit within viewport',all(x['page_height']<=x['height']+1 for x in layout if x['width']>=1000))
 # Standalone Artifact defaults correctly; no Gemini bootstrap or CDN request required.
 q=ctx.new_page();attach(q);q.set_content((ROOT/'public/artifact.html').read_text(),wait_until='load');check('Standalone Artifact opens the collection',q.locator('#artifact-view').is_visible() and q.locator('.portfolio-card').count()==12);q.close()
 browser.close()
check('No uncaught runtime errors',not REPORT['page_errors'],str(REPORT['page_errors']))
check('No console errors in tested interactions',not REPORT['console_errors'],str(REPORT['console_errors']))
check('No automatic network requests',not REPORT['requests'],str(REPORT['requests']))
REPORT['passed']=sum(c['passed'] for c in REPORT['checks']);REPORT['total']=len(REPORT['checks'])
(ROOT/'docs/UI-TEST-RESULTS.json').write_text(json.dumps(REPORT,indent=2))
print('RESULT',REPORT['passed'],'/',REPORT['total']);print('Layout over viewport (task-only):',[(x['width'],x['slide'],x['page_height']-x['height']) for x in REPORT['layout'] if x['width']>=1000 and x['page_height']>x['height']+1])
if REPORT['passed']!=REPORT['total']:raise SystemExit(1)
