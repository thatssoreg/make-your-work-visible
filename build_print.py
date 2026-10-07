#!/usr/bin/env python3
"""Generate separate facilitator PDFs and a public, unstructured student worksheet."""
from pathlib import Path
import json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab import rl_config
rl_config.invariant=1
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'docs/print';OUT.mkdir(parents=True,exist_ok=True)
PUB=ROOT/'public/downloads';PUB.mkdir(parents=True,exist_ok=True)
SCENES=json.loads((ROOT/'content/session.json').read_text())
NAVY=colors.HexColor('#232D4B');ORANGE=colors.HexColor('#E57200');INK=colors.HexColor('#282827');MUTED=colors.HexColor('#566072');LINE=colors.HexColor('#D8D6CF');SOFT=colors.HexColor('#F3F0E8')
styles={
 'kicker':ParagraphStyle('k',fontName='Helvetica-Bold',fontSize=10,leading=14,textColor=NAVY,spaceAfter=9),
 'title':ParagraphStyle('t',fontName='Times-Roman',fontSize=32,leading=36,textColor=NAVY,spaceAfter=14),
 'h2':ParagraphStyle('h',fontName='Times-Roman',fontSize=24,leading=28,textColor=NAVY,spaceAfter=12),
 'body':ParagraphStyle('b',fontName='Helvetica',fontSize=12.5,leading=18,textColor=INK,spaceAfter=9),
 'say':ParagraphStyle('s',fontName='Times-Italic',fontSize=17,leading=22,textColor=NAVY,spaceAfter=14),
 'small':ParagraphStyle('sm',fontName='Helvetica',fontSize=10.5,leading=15,textColor=MUTED,spaceAfter=9),
 'row':ParagraphStyle('r',fontName='Helvetica',fontSize=11,leading=15,textColor=INK),
 'bold':ParagraphStyle('rb',fontName='Helvetica-Bold',fontSize=10.5,leading=14,textColor=NAVY)}
def clean(s):return s.replace('→','to').replace('–','-').replace('—','; ').replace('’',"'").replace('“','"').replace('”','"')
def E(s):return html.escape(clean(str(s)))
def P(s,style='body'):return Paragraph(s,styles[style])
def chrome(c,d):
 c.saveState();c.setStrokeColor(NAVY);c.line(48,758,564,758);c.setFont('Helvetica',8);c.setFillColor(MUTED);c.drawString(48,769,'GITHUB AND PORTFOLIOS  /  SDS CAREER SERVICES');c.line(48,37,564,37);c.drawString(48,24,'Reggie Leonard · UVA School of Data Science');c.drawRightString(564,24,str(d.page));c.restoreState()
def build(path,story):SimpleDocTemplate(str(path),pagesize=letter,leftMargin=48,rightMargin=48,topMargin=51,bottomMargin=49,title='GitHub and portfolios | SDS Career Services',author='Reggie Leonard',pageCompression=1).build(story,onFirstPage=chrome,onLaterPages=chrome)
def run_content():
 story=[P('FACILITATOR ONLY','kicker'),P('GitHub and portfolios','title'),P('A practical introduction, followed by time to work and ask questions. All times below start at Reggie\'s handoff. No timing appears on student screens.','small')]
 rows=[[P('WHEN','bold'),P('SLIDE','bold'),P('WHAT TO DO','bold')]];elapsed=0
 for s in SCENES:
  end=elapsed+s['minutes'];rows.append([P(f'{elapsed:02d}-{end:02d}','bold'),P(f'{s["number"]:02d}','bold'),P(('<b>EXERCISE: </b>' if s['number']==3 else '<b>WORK + Q&amp;A: </b>' if s['number']==10 else '')+E(s['title']),'row')]);elapsed=end
 t=Table(rows,colWidths=[61,49,406],repeatRows=1);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),SOFT),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.35,LINE)]));story+=[t,Spacer(1,18),P('<b>40-minute plan:</b> The opening includes discussion and the Post-it activity. Slide 10 protects 22 minutes for work and questions, including a short shared Q&amp;A.','small'),P('<b>45-minute plan:</b> Add five minutes to slide 10. Close at minutes 43-45.','small'),P('<b>Keep beside you:</b> Three Post-it notes per person, pens, the HTML, and this run sheet. Ask, "What are you trying to learn or show?"','small')];return story
build(OUT/'run-sheet.pdf',run_content())
# Two cues per page, with no need to read a script.
story=run_content()+[PageBreak()];elapsed=0
for i in range(0,len(SCENES),2):
 for j,s in enumerate(SCENES[i:i+2]):
  end=elapsed+s['minutes'];story +=[P(f'{s["number"]:02d}  /  {E(s["kind"].upper())}  /  {elapsed:02d}-{end:02d} MIN','kicker'),P(E(s['title']),'h2'),P(E(s['say']),'say')]
  for a in s['actions']:story.append(P('[  ] '+E(a),'body'))
  if s['transition']:story.append(P('<b>Transition:</b> '+E(s['transition']),'small'))
  elapsed=end
  if j==0 and i+1<len(SCENES):
   rule=Table([['']],colWidths=[516],rowHeights=[2]);rule.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),ORANGE)]));story +=[Spacer(1,16),rule,Spacer(1,24)]
 if i+2<len(SCENES):story.append(PageBreak())
story +=[Spacer(1,20),P('When someone needs technical evaluation','h2'),P('"I can help you decide what you are trying to learn or show. Let\'s identify the course resource, faculty member, documentation, or practice environment that can help you check the technical approach."','say')]
build(OUT/'facilitator-guide.pdf',story)
def blank(h):
 t=Table([['']],colWidths=[516],rowHeights=[h]);t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.4,LINE)]));return t
ws=[P('YOUR NOTES','kicker'),P('GitHub and portfolios','title'),P('Use this page or your own notes while you work. You do not need a finished project to begin.','body')]
for heading,prompt,h in [('What would you like to work on?','An About section, project explanation, new question, existing assignment, or something else.',55),('What did you change, learn, or decide?','Record a useful revision, a choice you made, or something you want to investigate.',60),('What would help?','Write a question to ask or feedback you received.',50),('What comes next?','Name the next action and where you saved your work.',40)]:ws +=[Spacer(1,17),P(heading,'h2'),P(prompt,'small'),blank(h)]
build(PUB/'student-worksheet.pdf',ws)
# Remove facilitator files from the student build (not from the source/history).
for name in ['facilitator-guide.pdf','run-sheet.pdf']:
 p=PUB/name
 if p.exists():p.unlink()
notes='# Facilitator guide: GitHub and portfolios\n\nSDS Career Services · Reggie Leonard\n\nPrivate facilitation reference. The student interface contains no timing, mode labels, or speaker notes.\n\n';elapsed=0
for s in SCENES:
 notes+=f"## {s['number']:02d}. {s['title']}\n{s['kind']} · {elapsed}-{elapsed+s['minutes']} minutes\n\n**Say:** {s['say']}\n\n"+'\n'.join('- [ ] '+a for a in s['actions'])+f"\n\n**Transition:** {s['transition']}\n\n";elapsed+=s['minutes']
notes+='## Pacing\n\nUse 22 minutes for work and questions in the 40-minute version; use 27 in the 45-minute version. A neighbor review is optional. Invite questions throughout. There is no timed technical lab or required public post.\n'
(ROOT/'docs/FACILITATOR.md').write_text(notes)
print('Built facilitator PDFs separately from the student worksheet.')
