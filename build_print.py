#!/usr/bin/env python3
"""Generate podium-friendly PDFs from the canonical scene data.
No external fonts, network calls, or office-suite installation required.
"""
from pathlib import Path
import json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab import rl_config
rl_config.invariant = 1
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'public/downloads';OUT.mkdir(parents=True,exist_ok=True)
SCENES=json.loads((ROOT/'content/session.json').read_text())
NAVY=colors.HexColor('#232D4B');ORANGE=colors.HexColor('#E57200');INK=colors.HexColor('#282827');MUTED=colors.HexColor('#566072');LINE=colors.HexColor('#D8D6CF');TINT=colors.HexColor('#F3F0E8')
styles={
 'kicker':ParagraphStyle('k',fontName='Helvetica-Bold',fontSize=9,leading=13,textColor=NAVY,spaceAfter=8),
 'title':ParagraphStyle('t',fontName='Times-Roman',fontSize=32,leading=35,textColor=NAVY,spaceAfter=12),
 'subtitle':ParagraphStyle('st',fontName='Helvetica',fontSize=13,leading=19,textColor=MUTED,spaceAfter=16),
 'h2':ParagraphStyle('h2',fontName='Times-Roman',fontSize=24,leading=28,textColor=NAVY,spaceAfter=12),
 'h3':ParagraphStyle('h3',fontName='Helvetica-Bold',fontSize=13,leading=18,textColor=NAVY,spaceBefore=10,spaceAfter=6),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=12.5,leading=18,textColor=INK,spaceAfter=9),
 'say':ParagraphStyle('say',fontName='Times-Italic',fontSize=16,leading=21,textColor=NAVY,spaceAfter=11),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=10,leading=14,textColor=MUTED,spaceAfter=6),
 'row':ParagraphStyle('row',fontName='Helvetica',fontSize=10.5,leading=14,textColor=INK),
 'rowbold':ParagraphStyle('rowbold',fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=NAVY),
 'label':ParagraphStyle('label',fontName='Helvetica-Bold',fontSize=10,leading=14,textColor=NAVY,spaceAfter=7)
}
def P(t,style='body'):return Paragraph(t,styles[style])
def E(t):return html.escape(t).replace('→','&#8594;')
def clean(t):return t.replace('→','to').replace('–','-').replace('—','; ').replace('’',"'").replace('“','"').replace('”','"')
def line():
 t=Table([['']],colWidths=[516],rowHeights=[2]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),ORANGE)]));return t

def chrome(c,doc):
 c.saveState();w,h=letter
 c.setStrokeColor(NAVY);c.setLineWidth(1);c.line(48,h-34,w-48,h-34)
 c.setFont('Helvetica',8);c.setFillColor(MUTED);c.drawString(48,h-26,'MAKE YOUR WORK VISIBLE  /  SDS CAREER SERVICES')
 c.line(48,37,w-48,37);c.drawString(48,24,'Reggie Leonard · UVA School of Data Science · Edition 1.0.0')
 c.drawRightString(w-48,24,str(doc.page));c.restoreState()
def doc(path,story):SimpleDocTemplate(str(path),pagesize=letter,leftMargin=48,rightMargin=48,topMargin=49,bottomMargin=49,title='Make Your Work Visible | SDS Career Services',author='Reggie Leonard · SDS Career Services',pageCompression=1).build(story,onFirstPage=chrome,onLaterPages=chrome)
def run_content():
 story=[P('FACILITATOR RUN SHEET','kicker'),P('Make your work visible','title'),P('Times start at Reggie\'s handoff, after the faculty opening. Keep one student-selected project or question in use throughout.','subtitle')]
 data=[[P('TIME','rowbold'),P('SCREEN / MODE','rowbold'),P('WHAT HAPPENS','rowbold')]];minute=0
 summaries=['Name the purpose and the persistent project.','Explain fluency, legibility, and reach.','Choose a starting condition; write and circle a note.','Model the Figma task through the measurement brief.','Tables scope the CSIS task; hear one rationale.','Students write a bridge for their own work.','Compare the two explanations with the same questions.','Pairs identify missing facts, without inventing them.','Students write about their own project or plan.','Compare project, profile, and optional website.','Model an introduction; students draft two sentences.','Students work in their own tool. Walk the room.','Read first, explain a choice, then revise.','Save the work and name the next action.']
 for s,summary in zip(SCENES,summaries):
  a,b=minute,minute+s['minutes'];minute=b
  data.append([P(f'{a:02d}-{b:02d} min','rowbold'),P(f'<b>{s["number"]:02d}</b>  {E(s["kind"])}','row'),P(E(summary),'row')])
 t=Table(data,colWidths=[70,129,317],repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),TINT),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.4,LINE),('LEFTPADDING',(0,0),(-1,-1),8)]));story+=[t,Spacer(1,14),P('<b>45-minute option:</b> Independent work runs 29-40 minutes; peer review runs 40-44; close runs 44-45. Select 45 min in the HTML. Do not add more lecture.','small'),P('<b>When someone is stuck:</b> Ask what they are trying to learn or show. Offer a nudge, then an example. A paper note or local document works when accounts or Wi-Fi do not.','small')]
 return story

def cue(s,minute):
 text=[P(f'{s["number"]:02d}  /  {s["theme"].upper()}  /  {s["kind"].upper()}  /  {minute:02d}-{minute+s["minutes"]:02d} MIN','kicker'),P(E(s['title']),'h2'),P(E(s['say']),'say')]
 for a in s['actions']:text.append(P('[  ] '+E(a),'body'))
 if s['output']:text.append(P('<b>What should exist:</b> '+E(s['output']),'small'))
 text.append(P('<b>Transition:</b> '+E(s['transition']),'small'))
 return text
setup=[P('BEFORE THE SESSION','kicker'),P('Set up the room and your browser','title'),P('Bring three Post-it notes per person, pens, and this guide. The printed student worksheet is an optional alternative, not additional required paperwork.','subtitle'),P('Prepare the teaching environment','h3')]
for x in ['Open the main HTML in a full browser. Confirm that Next, a help button, a timer, and a Markdown download work on the teaching laptop.','Check the projector at the intended zoom. Use Present to hide your personal work card and starting-condition choices. Keep the speaker note closed while speaking.','Distribute the HTML file or an approved hosted link. A local file path on your laptop will not open on a student’s laptop.','Check the Figma and CSIS links, student access to the SDS board, and profile examples. Their descriptions remain in the file if the pages are unavailable.','Agree on the 15-20 minute faculty handoff. Select 40 or 45 minutes in the HTML; this changes work and peer timers.']:
 setup.append(P('[  ] '+E(x),'body'))
setup += [P('What to watch while facilitating','h3'),P('By minute five, everyone has one selected project, assignment, task, or question. The shared examples teach a move; students then return to their own note. Do not let every exercise become a new project.','body'),P('During work time, ask: “What are you trying to show or learn?” and “What is the smallest useful finish line?” A question, plan, paragraph, or revision can be read by a partner.','body'),P('When a student needs technical evaluation','h3'),P('“I can help you decide what you are trying to learn or show. Let’s identify the course resource, faculty member, documentation, or practice environment that can help you check the technical approach.”','say'),P('Timers do not synchronize across browsers. They start only when pressed, and pause when you leave the activity. Plans must remain visibly distinct from completed results.','small')]
# Nine-page guide. Pair cues, with a clear section rule and generous separation.
story=run_content()+[PageBreak()]+setup+[PageBreak()]
elapsed=0
for i in range(0,len(SCENES),2):
 for j in [i,i+1]:
  s=SCENES[j];story+=cue(s,elapsed);elapsed+=s['minutes']
  if j==i:story +=[Spacer(1,15),line(),Spacer(1,18)]
 if i+2<len(SCENES):story.append(PageBreak())
doc(OUT/'facilitator-guide.pdf',story)
doc(OUT/'run-sheet.pdf',run_content())
# Two-page worksheet, intended for actual handwriting rather than a cramped form.
def blank(height=40):
 t=Table([['']],colWidths=[516],rowHeights=[height]);t.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),.5,LINE)]));return t
ws=[P('STUDENT WORKSHEET · PAGE 1 OF 2','kicker'),P('Keep one piece of work in view','title'),P('Use this page, your own document, or Post-it notes. You will return to the same assignment, project, question, or job task in each section.','subtitle'),P('My selected work and its current status','h3'),blank(40),P('1. Fluency: choose a next learning move','h2')]
for q in ['What have I already done or attempted?','What do I want to understand, compare, or practice next?','What first action can I take with the time and access I have?']:
 ws +=[P(q,'body'),blank(43),Spacer(1,10)]
ws +=[Spacer(1,10),P('A bridge can be an investigation, comparison, revision, or small implementation. You do not need to reproduce the scale or private data of an employer.','small'),PageBreak(),P('STUDENT WORKSHEET · PAGE 2 OF 2','kicker'),P('Explain and review the same work','title'),P('My selected work: __________________________________________________','body'),P('2. Legibility: write your project explanation','h2'),P('What problem or question? What approach and contribution? What result, current progress, or plan, and what does it mean?','body'),blank(70),Spacer(1,15),P('3. Reach: introduce one part of the work','h2'),P('Who might have a genuine reason to discuss it? Write two opening sentences for that situation. Nothing needs to be sent today.','body'),blank(52),Spacer(1,15),P('4. Reader feedback and revision','h2'),P('I understand ... / I am still looking for ...','body'),blank(28),Spacer(1,10),P('One choice I explained without the template, and one revision I made:','body'),blank(24),Spacer(1,10),P('My next action and where I saved the actual work:','body'),blank(22)]
doc(OUT/'student-worksheet.pdf',ws)
# Markdown facilitator source derives from the same data.
fac='# Make Your Work Visible\n## Facilitator guide\n\nReggie Leonard · SDS Career Services · UVA School of Data Science\n\nThe faculty opening takes 15-20 minutes. These times begin at Reggie’s handoff. The core is 40 minutes; the longer version adds four minutes to work and one minute to peer review.\n\n'
fac+='## Before the room opens\n\nGive each learner three Post-it notes and a pen. A private note or typed equivalent works. Test Next, a timer, a help reveal, and an export on the actual teaching laptop. Keep a local copy for Wi-Fi trouble. Distribute an actual HTML file or a verified hosted URL, not a local path. Use Present to hide personal context.\n\n'
elapsed=0
for s in SCENES:
 fac+=f"## {s['number']:02d}. {s['title']}\n**{s['kind']} · {elapsed}-{elapsed+s['minutes']} minutes · {s['theme']}**\n\n**Say:** {s['say']}\n\n"+'\n'.join('- [ ] '+x for x in s['actions'])+f"\n\n**Output:** {s['output'] or 'Shared orientation or a model to inspect.'}\n\n**Transition:** {s['transition']}\n\n";elapsed+=s['minutes']
fac+='## Technical boundary\n\nHelp students scope, explain, and reflect on work. Do not certify the correctness of a technical approach. Refer implementation questions to course staff, a technical peer, official documentation, or a provider-authored resource.\n\n## Contingencies\n\nNo idea: borrow the music question or a concrete table example. No account or Wi-Fi: use a local note. No finished project: explain status and planned learning honestly. Not comfortable sharing: choose a permitted or private example and complete the reader task in writing. Over time: shorten a debrief or work period, not the closing reader test and save.\n'
(ROOT/'docs/FACILITATOR.md').write_text(fac)
print('Created three PDFs and synchronized facilitator Markdown.')
