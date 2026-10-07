"""Validate the simplified student's experience and preserved content."""
from pathlib import Path
import json,re,hashlib
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];html=(ROOT/'public/index.html').read_text();soup=BeautifulSoup(html,'html.parser');data=json.loads(soup.select_one('#workshop-data').string);results=[]
def check(name,ok):
 results.append({'name':name,'passed':bool(ok)})
 if not ok:print('FAIL:',name)
check('Eleven slides, all accounted for',len(soup.select('.slide'))==11)
check('Student session data excludes facilitator fields',all(set(s)=={'number','title','theme'} for s in data['session']))
check('No clock widgets or routing controls',not soup.select('[data-timer],[data-help],[data-own-work],[data-start-options],[data-action="work-card"],[data-action="speaker"],[data-action="settings"]'))
check('No elapsed times in any slide',not any(re.search(r'\b\d{1,2}:\d{2}\b|\b\d+\s*(?:min|minutes|seconds)\b',s.get_text()) for s in soup.select('.slide')))
check('No facilitator printables in student payload',set(data['printables'])=={'student-worksheet'})
check('No facilitator PDFs in public downloads',not (ROOT/'public/downloads/facilitator-guide.pdf').exists() and not (ROOT/'public/downloads/run-sheet.pdf').exists())
check('No forced starting states in resources',not any(k in data['resources'] for k in ['starts','help','state_nudges','model']))
check('SDS Career Services branding', 'SDS Career Services' in html and 'Career Connections' not in html)
check('No music-brief dependency', 'measurement-brief' not in html and 'music-recommendations-brief' not in html)
check('All 12 original Artifact selections retained',len(data['resources']['portfolios'])==12)
check('All 5 writing guides retained',len(data['resources']['writing_guides'])==5)
check('All 9 reading selections retained',len(data['resources']['readings'])==9)
check('Original 6-part writing structures retained',all(len(g['rows'])==6 for g in data['resources']['writing_guides']))
check('New project-selection and website guides present',all(k in data['guides'] for k in ['projects','platforms']))
ids={s['id'] for s in data['sources']}; routes=data['resources']['routes']
check('All activity reference IDs resolve',all(set(r['refs'])<=ids for r in routes))
check('All activity prompts and outlines resolve',all(r['prompt'] in data['resources']['prompts'] and r['template'] in data['resources']['templates'] for r in routes))
check('All static source links resolve',all(a['data-source-link'] in ids for a in soup.select('[data-source-link]')))
check('No automatic external runtime dependencies',not soup.select('script[src],link[href],iframe'))
check('No network or storage API usage',not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket|localStorage|sessionStorage)\b',(ROOT/'src/app.js').read_text()))
check('No script execution from external data',not re.search(r'\beval\s*\(|\bnew Function\b',(ROOT/'src/app.js').read_text()))
check('CSP blocks external connections',"connect-src 'none'" in html)
check('Student paths separate from facilitator notes',not any(k in data for k in ['speakerNotes','timers','measurement']))
check('Core facilitation plan is 40 minutes',sum(s['minutes'] for s in json.loads((ROOT/'content/session.json').read_text()))==40)
check('Work and questions retain 22 minutes',json.loads((ROOT/'content/session.json').read_text())[9]['minutes']==22)
check('No em dash in slide copy',all('—' not in (ROOT/'content'/s['file']).read_text() for s in json.loads((ROOT/'content/session.json').read_text())))
check('GitHub and website options remain distinct','profile README' in data['guides']['platforms']['markdown'] and 'GitHub Pages' in data['guides']['platforms']['markdown'])
check('Templates do not promise hiring outcomes','100% guaranteed' not in html)
check('Public artifacts have manifest checksums',all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==v for k,v in json.loads((ROOT/'docs/BUILD-MANIFEST.json').read_text())['files'].items()))
report={'checks':results,'passed':sum(x['passed'] for x in results),'total':len(results)};(ROOT/'docs/BUILD-TEST-RESULTS.json').write_text(json.dumps(report,indent=2));print(report['passed'],'/',report['total'],'build checks')
assert report['passed']==report['total']
