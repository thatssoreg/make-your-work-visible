#!/usr/bin/env python3
"""Build two network-free HTML entry points and synchronized text materials.

Python 3.10+, markdown-it-py. No runtime package installation or server is needed.
Canonical inputs are in src/ and content/. The original imported app is not executed.
"""
from pathlib import Path
import json, hashlib, base64, html, re, subprocess, sys
from markdown_it import MarkdownIt
ROOT=Path(__file__).resolve().parent
CONTENT=ROOT/'content'; PUBLIC=ROOT/'public'; DOCS=ROOT/'docs'
for p in [PUBLIC,DOCS]:p.mkdir(exist_ok=True)
subprocess.run([sys.executable,str(ROOT/'build_print.py')],check=True)
md=MarkdownIt('commonmark',{'html':True}).enable('table')
session=json.loads((CONTENT/'session.json').read_text())
resources=json.loads((CONTENT/'resources.json').read_text())
sources=json.loads((CONTENT/'sources.json').read_text())
guide_keys=['start','explaining','github','permissions','writing','tools','sources','about']
guides={k:{'markdown':(CONTENT/f'guide-{k}.md').read_text(),'html':md.render((CONTENT/f'guide-{k}.md').read_text())} for k in guide_keys}
field='# Make Your Work Visible\n## Student field guide\n\nReggie Leonard · SDS Career Services · UVA School of Data Science\n\nEdition 1.0.0 · October 6, 2026\n\n'
for k,g in guides.items():field+=g['markdown']+'\n\n'
field+='## Work options\n\n'
for r in resources['routes']:
 field+=f"### {r['title']}\n\n{r['why']}\n\n**Where:** {r['where']}\n\n"+'\n'.join(f'{i+1}. {x}' for i,x in enumerate(r['steps']))+f"\n\n**Finish line:** {r['done']}\n\n**Fallback:** {r['fallback']}\n\n"
field+='## Full coaching prompts\n\n'
for k,t in resources['prompts'].items():field+=f'### {k.title()}\n\n{t}\n\n'
field+='## Artifact: twelve original portfolio selections\n\n'
for p in resources['portfolios']:field+=f"### {p['name']} · {p['lens']}\n\n{p['stage']}. {p['summary']}\n\n{p['pattern']}\n\n{p['url']}\n\n{p['note']}\n\n"
field+='## Artifact: writing outlines\n\n'
for g in resources['writing_guides']:field+=f"### {g['lens']}: {g['title']}\n\n{g['description']}\n\n"+'\n'.join(f"- **{r['section']}:** {r['include']} {r['reason']}" for r in g['rows'])+'\n\n'
field+='## Source register\n\n'
for s in sources:field+=f"### {s['title']}\n{s['publisher']} · {s['checked']}\n\n{s['url']}\n\n{s['note']}\n\n"
# Remove interface-only controls from the portable text version.
field=re.sub(r'<(?:button|label|div)\b[^>]*>.*?</(?:button|label|div)>','',field,flags=re.S)
field=re.sub(r'\n{4,}','\n\n\n',field)
(DOCS/'STUDENT-FIELD-GUIDE.md').write_text(field)
slides=[]; outline='# Make Your Work Visible\n## Canonical live sequence\n\nSDS Career Services · 40-minute core; 45-minute option adds four minutes to work and one to peer review.\n\n';notes='# One-line speaker notes\n\nSDS Career Services · Reggie Leonard\n\n';elapsed=0
for s in session:
 text=(CONTENT/s['file']).read_text();rendered=md.render(text)
 slides.append(f'<section class="slide" data-scene="{s["number"]}" aria-label="{html.escape(s["title"],quote=True)}"'+(' hidden' if s['number']!=1 else '')+f'><div class="scene-context"></div>{rendered}</section>')
 timing=f'{elapsed}:00–{elapsed+s["minutes"]}:00';elapsed+=s['minutes']
 outline+=f"## {s['number']:02d}. {s['title']}\n**{s['theme']} · {s['kind']} · {timing}**\n\n**Say:** {s['say']}\n\n"+'\n'.join('- '+x for x in s['actions'])+f"\n\n**Output:** {s['output'] or 'Shared orientation or a modeled example.'}\n\n**Transition:** {s['transition']}\n\n"+text+'\n\n'
 notes+=f"**{s['number']:02d} · {timing} · {s['kind']}**  \n{s['say']}\n\n"
(CONTENT/'SESSION.md').write_text(outline);(DOCS/'SPEAKER-NOTES.md').write_text(notes)
for name,text in resources['templates'].items():(CONTENT/f'{name}-template.md').write_text(text)
for name,text in resources['prompts'].items():(CONTENT/f'{name}-prompt.md').write_text(text)
(CONTENT/'ARTIFACT-COLLECTION.md').write_text('# Artifact collection\n\n'+ '\n\n'.join(f"## {p['name']} · {p['lens']}\n\n{p['stage']}\n\n{p['summary']}\n\n{p['pattern']}\n\n{p['url']}\n\n{p['note']}" for p in resources['portfolios']))
printables={f.stem:{'name':f.name,'base64':base64.b64encode(f.read_bytes()).decode()} for f in (PUBLIC/'downloads').glob('*.pdf')}
data=dict(printables=printables,session=session,resources=resources,sources=sources,guides=guides,fieldMarkdown=field,measurement=(CONTENT/'measurement-brief.md').read_text())
serialized=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
script=(ROOT/'src/app.js').read_text();style=(ROOT/'src/style.css').read_text();template=(ROOT/'src/index.template.html').read_text()
sha=base64.b64encode(hashlib.sha256(script.encode()).digest()).decode()
csp=f"default-src 'none'; script-src 'sha256-{sha}'; style-src 'unsafe-inline'; img-src data: blob:; font-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
base=template.replace('__STYLE__',style).replace('__SCRIPT__',script).replace('__DATA__',serialized).replace('__SLIDES__','\n'.join(slides)).replace('__CSP__',csp)
for filename,title,default in [('index.html','Make Your Work Visible | SDS Career Services','session'),('artifact.html','Artifact | SDS Career Services','artifact')]:
 result=base.replace('__TITLE__',title).replace('__DEFAULT__',default)
 (PUBLIC/filename).write_text(result)
(PUBLIC/'.nojekyll').write_text('')
(ROOT/'index.html').write_text((PUBLIC/'index.html').read_text())
(ROOT/'artifact.html').write_text((PUBLIC/'artifact.html').read_text())
manifest={'version':resources['version'],'built_from':'src + content','files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [PUBLIC/'index.html',PUBLIC/'artifact.html',DOCS/'STUDENT-FIELD-GUIDE.md',DOCS/'SPEAKER-NOTES.md']}}
(DOCS/'BUILD-MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print('Built',len(session),'scenes,',len(resources['portfolios']),'portfolio selections,',len(sources),'sources.', 'Core timing:',elapsed,'minutes.')
print('HTML:',(PUBLIC/'index.html').stat().st_size,'bytes')
