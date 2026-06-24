#!/usr/bin/env python3
"""Generate the A4 'Innovation Lab — Field Notes' PDF for the emlyon × Exoflow LEX visits."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, FrameBreak, NextPageTemplate, PageBreak)
from reportlab.platypus.flowables import Flowable, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

RED=colors.HexColor('#ff0033'); INK=colors.HexColor('#343333')
INK2=colors.HexColor('#5b5a59'); LINE=colors.HexColor('#d8d3cb')
BLUE=colors.HexColor('#195edd'); PAPER=colors.HexColor('#fbfaf8')
PINK=colors.HexColor('#fff0f2')

W,H=A4
M=18*mm

ss=getSampleStyleSheet()
def st(name,**k):
    base=dict(fontName='Helvetica',fontSize=10,leading=14,textColor=INK)
    base.update(k); return ParagraphStyle(name,**base)
H1=st('H1',fontName='Helvetica-Bold',fontSize=26,leading=29,textColor=INK)
H2=st('H2',fontName='Helvetica-Bold',fontSize=15,leading=18,textColor=RED,spaceBefore=6,spaceAfter=4)
H3=st('H3',fontName='Helvetica-Bold',fontSize=11,leading=14,textColor=INK,spaceBefore=4)
BODY=st('BODY',fontSize=9.5,leading=13,textColor=INK2)
SMALL=st('SMALL',fontSize=8,leading=11,textColor=INK2)
EY=st('EY',fontName='Helvetica-Bold',fontSize=8,leading=11,textColor=RED)
WHITE=st('WHITE',fontName='Helvetica-Bold',fontSize=9.5,leading=12,textColor=colors.white)

class Lines(Flowable):
    """Ruled writing lines."""
    def __init__(self,n=4,gap=8*mm,width=None):
        Flowable.__init__(self); self.n=n; self.gap=gap; self.width=width
    def wrap(self,aw,ah):
        self.w=self.width or aw; self.h=self.n*self.gap; return self.w,self.h
    def draw(self):
        c=self.canv; c.setStrokeColor(LINE); c.setLineWidth(0.6)
        for i in range(self.n):
            y=self.h-(i+1)*self.gap
            c.line(0,y,self.w,y)

class Box(Flowable):
    """Colored rounded panel with a title; reserves note space."""
    def __init__(self,title,height,fill=PINK,border=colors.HexColor('#ffd6dd'),tcolor=RED,width=None,lines=0,sub=None):
        Flowable.__init__(self); self.title=title; self.bh=height; self.fill=fill
        self.border=border; self.tcolor=tcolor; self.width=width; self.lines=lines; self.sub=sub
    def wrap(self,aw,ah):
        self.w=self.width or aw; return self.w,self.bh
    def draw(self):
        c=self.canv; c.setFillColor(self.fill); c.setStrokeColor(self.border); c.setLineWidth(1)
        c.roundRect(0,0,self.w,self.bh,6,fill=1,stroke=1)
        c.setFillColor(self.tcolor); c.setFont('Helvetica-Bold',9)
        c.drawString(8,self.bh-13,self.title.upper())
        top=22
        if self.sub:
            c.setFillColor(INK2); c.setFont('Helvetica-Oblique',7.5)
            c.drawString(8,self.bh-22,self.sub); top=30
        if self.lines:
            c.setStrokeColor(LINE); c.setLineWidth(0.5)
            for i in range(self.lines):
                y=self.bh-top-i*7*mm
                if y>6: c.line(8,y,self.w-8,y)

def header_footer(canvas,doc):
    canvas.saveState()
    # top rule
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.8)
    canvas.line(M,H-13*mm,W-M,H-13*mm)
    canvas.setFont('Helvetica-Bold',8); canvas.setFillColor(RED)
    canvas.drawString(M,H-11.5*mm,'INNOVATION LAB · FIELD NOTES')
    canvas.setFont('Helvetica',8); canvas.setFillColor(INK2)
    canvas.drawRightString(W-M,H-11.5*mm,'emlyon Executive MBA × Exoflow · 25 June 2026')
    # footer
    canvas.line(M,15*mm,W-M,15*mm)
    canvas.setFillColor(INK2); canvas.setFont('Helvetica',7.5)
    canvas.drawString(M,11*mm,'victor@exoflow.fr · www.exoflow.fr')
    canvas.drawRightString(W-M,11*mm,'Page %d'%doc.page)
    canvas.restoreState()

def bullets(items,style=BODY):
    return [Paragraph('<font color="#ff0033">•</font>&nbsp;&nbsp;'+t,style) for t in items]

doc=BaseDocTemplate('Innovation-Lab-Field-Notes.pdf',pagesize=A4,
    leftMargin=M,rightMargin=M,topMargin=18*mm,bottomMargin=18*mm,title='Innovation Lab — Field Notes',author='Exoflow')
frame=Frame(M,18*mm,W-2*M,H-36*mm,id='main')
doc.addPageTemplates([PageTemplate(id='main',frames=[frame],onPage=header_footer)])

S=[]
def P(t,s=BODY): S.append(Paragraph(t,s))
def sp(h=4): S.append(Spacer(1,h))

# ---------- COVER ----------
S.append(Spacer(1,30*mm))
P('LEARNING EXPEDITION · LYON · THURSDAY 25 JUNE 2026',EY)
sp(4)
P('Innovation Lab',H1)
P('Field Notes',ParagraphStyle('sub',parent=H1,textColor=RED))
sp(8)
P('A working notebook for your two visits — capture what you see, score each space, '
  'and reuse it for your final graded canvas. Methods, best practices and space-organisation '
  'cues are on the next pages; the blank canvases follow.',BODY)
sp(14)
cover=[
 ['MORNING · 10:30–12:30','Orange — 131 av. Félix Faure, 69003 Lyon','Host: Julien Manivong, Solutions Engineer'],
 ['AFTERNOON · 14:00–16:00','Sanofi — 14 Bis Innovation Lab','Host: Sylvain Grivel, Head of 14 Bis · arrive 13:45'],
]
t=Table([[Paragraph('<b>'+a+'</b>',SMALL),Paragraph('<b>'+b+'</b>',H3),Paragraph(c,SMALL)] for a,b,c in cover],
        colWidths=[40*mm,70*mm,'*'])
t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),
    ('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-2),0.5,LINE)]))
S.append(t)
sp(10)
P('The 5 analysis lenses (use these on every space): aesthetic choices · functional choices · '
  'creation strategy · operating model · opportunities &amp; threats.',SMALL)
sp(6)
P('Reminder before access: bring valid photo ID and complete the Sanofi SAFE safety training '
  'before Monday 23 June.',ParagraphStyle('warn',parent=SMALL,textColor=RED,fontName='Helvetica-Bold'))
S.append(PageBreak())

# ---------- METHODS ----------
P('Methods cheat-sheet',H2)
P('The tools a healthy lab uses — grouped by what they are for. Tick the ones you spot on site.',SMALL)
sp(6)
methods=[
 ['DISCOVER','Design Thinking — Empathise·Define·Ideate·Prototype·Test','Customer Journey Map','Jobs-to-be-Done interviews','Personas & empathy maps'],
 ['IDEATE','Crazy 8s / brainwriting','Business Model Canvas (9 blocks)','Value Proposition Canvas','Three Horizons (H1/H2/H3)'],
 ['BUILD & TEST','Design Sprint (5 days)','Lean Startup — Build·Measure·Learn','Assumption / riskiest-first mapping','Pirate metrics (AARRR)'],
 ['SCALE & GOVERN','Stage-Gate funding','OKRs','Innovation Ambition Matrix (70-20-10)','Generative AI co-pilot'],
]
data=[]
for grp in methods:
    head=Paragraph('<b>'+grp[0]+'</b>',ParagraphStyle('g',parent=SMALL,textColor=BLUE,fontName='Helvetica-Bold'))
    cells=[Paragraph('☐ '+x,SMALL) for x in grp[1:]]
    data.append([head]+cells)
mt=Table(data,colWidths=[26*mm]+[ (W-2*M-26*mm)/4.0 ]*4)
mt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),
    ('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),0.4,LINE),
    ('BACKGROUND',(0,0),(0,-1),PAPER)]))
S.append(mt)
sp(10)
P('Best practices — the 5 conditions for lab survival',H2)
P('Audit questions to ask each host — note the answer next to each.',SMALL)
sp(4)
bp=[('Mandate','Is there a clear strategic mandate &amp; an executive sponsor?'),
    ('Metrics','Is success measured beyond "ideas generated"?'),
    ('Scale path','Is there a defined route from lab to the core business?'),
    ('Right to fail','Can a project be killed without career damage?'),
    ('Funding','Is funding multi-year, or hostage to the annual budget?')]
bprows=[[Paragraph('<b>'+n+'</b>',ParagraphStyle('bn',parent=SMALL,textColor=RED,fontName='Helvetica-Bold')),
         Paragraph(q,SMALL),Paragraph('',SMALL)] for n,q in bp]
bpt=Table(bprows,colWidths=[26*mm,78*mm,'*'])
bpt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),
    ('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),0.5,LINE),
    ('LINEAFTER',(1,0),(1,-1),0.5,LINE),('BACKGROUND',(0,0),(-1,-1),PINK)]))
S.append(bpt)
S.append(PageBreak())

# ---------- SPACE ORGANISATION ----------
P('Space organisation — what to look for',H2)
P('Space is behavioural infrastructure. Note how each lab uses these levers.',SMALL)
sp(6)
space=[
 ('Proximity','Are mixed teams clustered to force "collisions"? (comms drop sharply beyond ~50 m)'),
 ('Visibility','Is work on the walls — writable surfaces, pin-up zones, prototype shelves?'),
 ('Modularity','Does furniture move — casters, foldable walls, reconfigurable rooms?'),
 ('Zoning','Are loud/divergent zones separated from quiet/focus zones? Acoustics?'),
 ('Threshold','Does entering the lab feel different from the corridor? Identity &amp; ritual?'),
 ('Making','Is there a maker corner (3D print, cardboard, electronics) to lower the cost of trying?'),
]
sd=[[Paragraph('<b>'+n+'</b>',H3),Paragraph(d,SMALL),Paragraph('☐ seen',SMALL)] for n,d in space]
stb=Table(sd,colWidths=[30*mm,'*',18*mm])
stb.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),
    ('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),0.4,LINE)]))
S.append(stb)
sp(10)
P('Zoning sketch — draw the floor plate you see',H2)
P('Rough the layout: entrance, collaboration, focus, meeting, maker, demo, lounge.',SMALL)
sp(4)
S.append(Box('Sketch / plan',70*mm,fill=colors.white,border=LINE,tcolor=INK2))
S.append(PageBreak())

# ---------- CANVAS (reusable) ----------
def canvas_page(place,host):
    P('Analysis canvas — '+place,H2)
    P('Host: '+host+'    ·    Date: 25 June 2026    ·    Time: __________',SMALL)
    sp(6)
    lenses=[('Aesthetic choices','look & feel, materials, light, brand'),
            ('Functional choices','zones, flow, furniture, tech'),
            ('Creation strategy','why built, sponsor, ambition, horizons'),
            ('Operating model','team, programs, funding, metrics'),
            ('Opportunities & threats','what works, what is at risk')]
    cw=(W-2*M-6*mm)/2
    rows=[[Box(lenses[0][0],42*mm,sub=lenses[0][1],lines=4,width=cw),
           Box(lenses[1][0],42*mm,sub=lenses[1][1],lines=4,width=cw)],
          [Box(lenses[2][0],42*mm,sub=lenses[2][1],lines=4,width=cw),
           Box(lenses[3][0],42*mm,sub=lenses[3][1],lines=4,width=cw)],
          [Box(lenses[4][0],42*mm,sub=lenses[4][1],lines=4,width=cw),
           Box('Overall score   __ / 5',42*mm,fill=colors.HexColor('#eaf1fd'),
               border=colors.HexColor('#c9dcfb'),tcolor=BLUE,sub='one big takeaway from this space',lines=4,width=cw)]]
    gt=Table(rows,colWidths=[(W-2*M-6*mm)/2,(W-2*M-6*mm)/2],hAlign='LEFT')
    gt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),('LEFTPADDING',(0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(0,-1),6)]))
    S.append(gt)

canvas_page('Orange — 131 av. Félix Faure, 69003 Lyon','Julien Manivong, Solutions Engineer')
S.append(PageBreak())
canvas_page('Sanofi — 14 Bis Innovation Lab','Sylvain Grivel, Head of 14 Bis')
S.append(PageBreak())

# ---------- QUESTIONS + NOTES ----------
P('Question bank &amp; free notes',H2)
for b in bullets([
 'What is your mandate — and who is the executive sponsor?',
 'How do you measure success beyond "ideas generated"?',
 'What happens to a validated concept — who scales it?',
 'Can a project be killed without hurting a career?',
 'How does this lab coexist with R&amp;D / corporate VC / M&amp;A?',
 'Which space decisions changed how people behave?',
 'How do bottom-up ideas reach you from the rest of the org?'],SMALL):
    S.append(b)
sp(8)
P('Free notes',H3)
S.append(Lines(n=14,gap=9*mm))

doc.build(S)
print('PDF written: Innovation-Lab-Field-Notes.pdf')
