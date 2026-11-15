"""Arcange Dev animated GitHub banner: scene(t) -> SVG, frames via Chromium, GIF via Pillow.
Run: python3 build_banner.py   (needs fonttools, playwright, pillow, Inter fonts)"""
import math, os, io, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
F="/usr/share/fonts/opentype/inter/Inter-%s.otf"
_c={}
def fnt(w):
    if w not in _c:
        f=TTFont(F%w); _c[w]=(f.getGlyphSet(),f.getBestCmap(),f["head"].unitsPerEm,f["hmtx"])
    return _c[w]
def textpath(s,w,size,x,y,sp=0):
    gs,cm,upm,hm=fnt(w); k=size/upm; pen=SVGPathPen(gs); cx=x
    for ch in s:
        g=cm[ord(ch)]; gs[g].draw(TransformPen(pen,(k,0,0,-k,cx,y))); cx+=hm[g][0]*k+sp
    return pen.getCommands(), cx-sp
BLUE="#2563EB"; CYAN="#22D3EE"; T=8.0
W,H=1500,500
def clamp(x): return max(0.0,min(1.0,x))
def prog(t,a,b): return clamp((t-a)/(b-a))
def eo(p): return 1-(1-p)**3
def eio(p): return 3*p*p-2*p**3
def mix(t):
    a=(0x25,0x63,0xEB); b=(0x22,0xD3,0xEE)
    return "#%02X%02X%02X"%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))

ARC,ARC_END=textpath("ARCANGE","Bold",134,88,258,6)
SUB,_=textpath("HARDWARE & SOFTWARE DEVELOPER","Medium",26,90,346,4)
TAG,TAG_END=textpath("FROM SILICON TO SOFTWARE","SemiBold",22,90,392,6)
LABELS=["ELECTRONICS","FIRMWARE","OPERATING SYSTEMS","APPLICATIONS","INTELLIGENT SYSTEMS"]
BX=930; YS=[98,174,250,326,402]
LBL=[textpath(l,"SemiBold",28,BX+104,y-4,3)[0] for l,y in zip(LABELS,YS)]
BIN={d:textpath(d,"Medium",14,0,0,0)[0] for d in "01"}

def cpu():
    pins="".join(f'<rect x="{-30+i*10}" y="-42" width="3" height="5" fill="#C9A24A"/><rect x="{-30+i*10}" y="37" width="3" height="5" fill="#C9A24A"/><rect x="-42" y="{-30+i*10}" width="5" height="3" fill="#C9A24A"/><rect x="37" y="{-30+i*10}" width="5" height="3" fill="#C9A24A"/>' for i in range(7))
    return f'''<rect x="-38" y="-38" width="76" height="76" rx="6" fill="#0F2A5C" stroke="#7E8AA0" stroke-width="1"/>{pins}
<rect x="-28" y="-28" width="56" height="56" rx="5" fill="url(#metal)" stroke="#DDE4F0" stroke-width="1"/>
<rect x="-16" y="-16" width="32" height="32" rx="2" fill="#0A1020" stroke="{CYAN}" stroke-width="1.2"/>
<path d="M-8 -8H8V8H-8Z M-16 0H-8 M8 0H16 M0 -16V-8 M0 8V16" fill="none" stroke="{BLUE}" stroke-width="1.2"/>
<path d="M-38 -38 l9 0 l-9 9Z" fill="{CYAN}"/>'''
def ram():
    chips="".join(f'<rect x="{-62+i*32}" y="-10" width="24" height="16" rx="2" fill="#0A0E18" stroke="#8C97AB" stroke-width=".8"/>' for i in range(4))
    gold="".join(f'<rect x="{-70+i*5.2:.1f}" y="12" width="3" height="5" fill="#C9A24A"/>' for i in range(27))
    return f'''<rect x="-75" y="-17" width="150" height="34" rx="3" fill="#12306B" stroke="#7E8AA0" stroke-width="1"/>{chips}{gold}
<path d="M-4 17 v-5 h8 v5" fill="#080B12"/><rect x="-75" y="-17" width="150" height="2" fill="{CYAN}" fill-opacity=".6"/>'''
def mcu():
    leads="".join(f'<rect x="{-17+i*5:.0f}" y="-30" width="2" height="7" fill="#AEB8C7"/><rect x="{-17+i*5:.0f}" y="23" width="2" height="7" fill="#AEB8C7"/><rect x="-30" y="{-17+i*5:.0f}" width="7" height="2" fill="#AEB8C7"/><rect x="23" y="{-17+i*5:.0f}" width="7" height="2" fill="#AEB8C7"/>' for i in range(8))
    return f'''{leads}<rect x="-23" y="-23" width="46" height="46" rx="3" fill="#0A0E18" stroke="#8C97AB" stroke-width="1"/>
<circle cx="-14" cy="-14" r="3" fill="none" stroke="{CYAN}" stroke-width="1.2"/><path d="M-8 4H8M-8 9H3" stroke="{BLUE}" stroke-width="1.4"/>'''
def board():
    hdr="".join(f'<rect x="{-52+i*7.5:.1f}" y="-30" width="5" height="5" fill="#C9A24A"/><rect x="{-52+i*7.5:.1f}" y="25" width="5" height="5" fill="#C9A24A"/>' for i in range(14))
    return f'''<rect x="-72" y="-32" width="144" height="64" rx="8" fill="#0F2F6B" stroke="#8C97AB" stroke-width="1"/>
<rect x="-56" y="-31" width="108" height="9" fill="#0A0E18"/><rect x="-56" y="22" width="108" height="9" fill="#0A0E18"/>{hdr}
<rect x="-80" y="-14" width="26" height="28" rx="2" fill="url(#metal)" stroke="#DDE4F0" stroke-width=".8"/>
<rect x="-6" y="-12" width="40" height="24" rx="2" fill="#0A0E18" stroke="{CYAN}" stroke-width=".9"/>
<circle cx="52" cy="0" r="5" fill="none" stroke="{CYAN}" stroke-width="1.2"/><path d="M-44 8H-20 M-44 -6H-24" stroke="{BLUE}" stroke-width="1.3"/>'''
def ssd():
    gold="".join(f'<rect x="{-58+i*4.4:.1f}" y="-7" width="2.4" height="14" fill="#C9A24A"/>' for i in range(5))
    return f'''<rect x="-62" y="-15" width="124" height="30" rx="3" fill="#12306B" stroke="#8C97AB" stroke-width="1"/>{gold}
<rect x="-34" y="-9" width="26" height="18" rx="2" fill="#0A0E18" stroke="#8C97AB" stroke-width=".8"/><rect x="0" y="-9" width="26" height="18" rx="2" fill="#0A0E18" stroke="#8C97AB" stroke-width=".8"/><rect x="34" y="-9" width="18" height="18" rx="2" fill="#0A0E18" stroke="{CYAN}" stroke-width=".8"/>
<path d="M62 -4 a4 4 0 0 0 0 8" fill="#080B12"/>'''
def fan(cx,rot):
    blades="".join(f'<path d="M0 0 L{14*math.cos(math.radians(a)):.1f} {14*math.sin(math.radians(a)):.1f}" stroke="#AEB8C7" stroke-width="3" stroke-linecap="round"/>' for a in range(0,360,60))
    return f'<g transform="translate({cx} 0) rotate({rot:.1f})"><circle r="19" fill="#0A0E18" stroke="{CYAN}" stroke-width="1.2"/>{blades}<circle r="4" fill="#DDE4F0"/></g>'
def gpu(t):
    r=(t/T)*360*2
    return f'''<rect x="-82" y="-27" width="164" height="54" rx="6" fill="#141B2B" stroke="#8C97AB" stroke-width="1"/>
<rect x="-86" y="-27" width="6" height="54" fill="url(#metal)"/>{fan(-34,r)}{fan(30,-r)}<rect x="-82" y="-27" width="164" height="3" fill="{BLUE}"/>
<rect x="-50" y="27" width="70" height="5" fill="#C9A24A"/>'''
def bust_front():
    return '<path d="M20 300 C20 250 60 232 84 226 L84 200 L116 200 L116 226 C140 232 180 250 180 300Z"/><ellipse cx="100" cy="112" rx="50" ry="64"/>'
def bust_profile():
    return '<path d="M30 300 L30 262 C30 238 62 226 88 214 L90 186 C62 174 46 146 48 108 C50 62 88 26 134 28 C170 30 192 58 192 92 L204 122 L192 126 L194 142 C196 150 190 154 186 158 L190 168 C186 184 168 190 150 192 L150 214 C176 226 205 236 210 262 L210 300Z"/>'
ICON=[
 '<path d="M-9 0H-5 l2 -5 l3 10 l3 -10 l3 10 l2 -5 H9" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/>',
 '<rect x="-5" y="-5" width="10" height="10" fill="none" stroke="{c}" stroke-width="1.6"/><path d="M-8 -2H-5 M-8 2H-5 M5 -2H8 M5 2H8 M-2 -8V-5 M2 -8V-5 M-2 5V8 M2 5V8" stroke="{c}" stroke-width="1.4"/>',
 '<path d="M-7 -5 l5 5 l-5 5" fill="none" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/><path d="M1 6H8" stroke="{c}" stroke-width="1.8"/>',
 '<rect x="-8" y="-8" width="7" height="7" fill="none" stroke="{c}" stroke-width="1.5"/><rect x="1" y="-8" width="7" height="7" fill="none" stroke="{c}" stroke-width="1.5"/><rect x="-8" y="1" width="7" height="7" fill="none" stroke="{c}" stroke-width="1.5"/><rect x="1" y="1" width="7" height="7" fill="{c}" fill-opacity=".7" stroke="{c}" stroke-width="1.5"/>',
 '<path d="M-8 6 L0 -7 L8 6 M-8 6 H8" fill="none" stroke="{c}" stroke-width="1.3"/><circle cx="-8" cy="6" r="2.4" fill="{c}"/><circle cx="0" cy="-7" r="2.4" fill="{c}"/><circle cx="8" cy="6" r="2.4" fill="{c}"/>',
]

def scene(t, settled=False):
    t=t%T
    env=1.0 if settled else eo(prog(t,0,0.7))*(1-eio(prog(t,7.45,8.0)))
    o=[]
    o.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">Arcange Dev: Hardware &amp; Software Developer. From Silicon to Software.</title>
<desc id="d">Banner with the name Arcange, floating hardware components, and five technology areas: electronics, firmware, operating systems, applications and intelligent systems.</desc>''')
    sx=-300+(1500+600)*prog(t,2.1,3.3); sx2=-300+(1500+600)*prog(t,5.4,6.6)
    sweep=lambda i,x:f'<linearGradient id="sw{i}" gradientUnits="userSpaceOnUse" x1="{x-140:.0f}" y1="0" x2="{x+140:.0f}" y2="0"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset=".45" stop-color="{CYAN}" stop-opacity=".95"/><stop offset=".55" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>'
    gx=(t/T)*25
    gcx=0.82+0.04*math.sin(2*math.pi*t/T); gcy=0.45+0.05*math.cos(2*math.pi*t/T)
    arcw=820 if settled else max(0.01,820*eio(prog(t,0.5,1.5)))
    tagw=(TAG_END-80) if settled else (TAG_END-80)*prog(t,1.9,3.0)
    o.append(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#03050A"/><stop offset=".6" stop-color="#070B16"/><stop offset="1" stop-color="#0A1226"/></linearGradient>
<radialGradient id="glow" cx="{gcx:.3f}" cy="{gcy:.3f}" r=".5"><stop offset="0" stop-color="{BLUE}" stop-opacity=".24"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="glow2" cx=".12" cy=".95" r=".45"><stop offset="0" stop-color="{CYAN}" stop-opacity=".09"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<linearGradient id="acc" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D8DFEA"/><stop offset=".5" stop-color="#8E99AD"/><stop offset="1" stop-color="#5E6A80"/></linearGradient>
<linearGradient id="bus" gradientUnits="userSpaceOnUse" x1="0" y1="98" x2="0" y2="402"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="bustfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity=".55"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<pattern id="gs" width="25" height="25" patternUnits="userSpaceOnUse" patternTransform="translate({gx:.2f} 0)"><path d="M25 0H0V25" fill="none" stroke="#5B7CFA" stroke-opacity=".05" stroke-width="1"/></pattern>
<pattern id="gl" width="100" height="100" patternUnits="userSpaceOnUse" patternTransform="translate({gx*4:.2f} 0)"><path d="M100 0H0V100" fill="none" stroke="#5B7CFA" stroke-opacity=".11" stroke-width="1"/></pattern>
<radialGradient id="fade" cx=".5" cy=".5" r=".65"><stop offset=".35" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
{sweep(1,sx)}{sweep(2,sx2)}
<clipPath id="arcclip"><rect x="60" y="100" width="{arcw:.1f}" height="200"/></clipPath>
<clipPath id="tagclip"><rect x="80" y="360" width="{tagw:.1f}" height="50"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="#05070D"/>
<g opacity="{env:.3f}">
<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#glow)"/><rect width="{W}" height="{H}" fill="url(#glow2)"/>
<g mask="url(#m)"><rect width="{W}" height="{H}" fill="url(#gs)"/><rect width="{W}" height="{H}" fill="url(#gl)"/></g>''')
    for (x,y,dx,dy) in ((36,36,1,1),(1464,36,-1,1),(36,464,1,-1),(1464,464,-1,-1)):
        o.append(f'<path d="M{x} {y+22*dy}V{y}H{x+22*dx}" fill="none" stroke="#9AA4B2" stroke-opacity=".35" stroke-width="1.5"/>')
    traces=[("M60 130H200L230 100H520",0.0),("M600 36H760L790 66H840",0.25),("M60 440H220L250 470H540",0.5),("M600 470H720L750 440H840",0.75)]
    for d,ph in traces:
        o.append(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-opacity=".28" stroke-width="1.2"/>')
        if not settled:
            o.append(f'<path d="{d}" pathLength="100" fill="none" stroke="{CYAN}" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="6 94" stroke-dashoffset="{-(((t/T)+ph)%1)*100:.2f}" opacity=".85"/>')
    ba=0.17 if settled else eo(prog(t,2.6,3.8))*0.17
    for fn,x,y,sc in ((bust_profile,1010,150,1.05),(bust_front,1250,150,1.05)):
        drift=3*math.sin(2*math.pi*t/T+x)
        o.append(f'<g transform="translate({x} {y+drift:.1f}) scale({sc})" opacity="{ba:.3f}" fill="url(#bustfill)" stroke="{CYAN}" stroke-width="1.2" stroke-opacity=".9">{fn()}</g>')
    for i in range(14):
        x0=(i*97+40)%1480; sp=1+(i%3)
        y=(H+20-((t/T)*H*sp+i*53)%(H+40))
        if 80<x0<860 and 140<y<420: continue
        b="01"[(i*7+int(t*2))%2] if i%2 else "01"[i%2]
        o.append(f'<g transform="translate({x0} {y:.1f})" opacity=".35"><path d="{BIN[b]}" fill="{CYAN}"/></g>')
    for i in range(20):
        x0=(i*131+17)%1500; sp=1+(i%2)
        y=(H-((t/T)*H*sp+i*71)%H)
        o.append(f'<circle cx="{x0}" cy="{y:.1f}" r="{1+(i%3)*0.5}" fill="#9CC3FF" opacity="{0.25+0.15*(i%3)}"/>')
    comps=[(cpu,170,78,0.72,-300,0,6,1.5,0.0,1),(ram,400,58,0.72,0,-120,-4,1.7,1.3,1),(mcu,625,66,0.72,300,-100,8,1.9,2.2,2),
           (board,190,452,0.62,-300,40,-3,1.6,0.7,1),(ssd,420,458,0.78,0,120,3,1.8,2.9,1),(gpu,650,452,0.62,300,100,-4,2.0,4.0,1),
           (mcu,790,210,0.6,200,0,-10,2.2,1.1,2),(cpu,800,330,0.5,200,60,12,2.3,3.1,1)]
    for fn,x,y,sc,dx,dy,tilt,st,ph,k in comps:
        p=1 if settled else eo(prog(t,st,st+1.3))
        a=2*math.pi*(t/T)*k+ph
        fy=4*math.sin(a); rot=tilt+3*math.sin(a+1); sxs=0.9+0.1*math.cos(a)
        body=fn(t) if fn is gpu else fn()
        o.append(f'<g transform="translate({x+dx*(1-p):.1f} {y+dy*(1-p)+fy:.1f}) rotate({rot:.2f}) scale({sc*sxs:.3f} {sc})" opacity="{0.9*p:.3f}">{body}</g>')
    ap=1 if settled else eio(prog(t,0.5,1.5)); slide=14*(1-ap)
    o.append(f'<g clip-path="url(#arcclip)"><g transform="translate(0 {slide:.1f})"><path d="{ARC}" fill="#FFFFFF"/>')
    if not settled: o.append(f'<path d="{ARC}" fill="url(#sw1)"/><path d="{ARC}" fill="url(#sw2)"/>')
    o.append('</g></g>')
    if not settled and 0.5<t<1.5: o.append(f'<rect x="{60+820*ap:.1f}" y="140" width="2" height="130" fill="{CYAN}" opacity=".9"/>')
    rw=640 if settled else 640*eio(prog(t,1.0,1.9))
    o.append(f'<rect x="90" y="292" width="{rw:.1f}" height="3" rx="1.5" fill="url(#acc)"/>')
    tp=1 if settled else eo(prog(t,1.2,2.0))
    o.append(f'<g transform="translate({-60*(1-tp):.1f} 0)" opacity="{tp:.3f}"><path d="{SUB}" fill="#D5DDEB"/></g>')
    o.append(f'<g clip-path="url(#tagclip)"><path d="{TAG}" fill="{CYAN}"/></g>')
    tg=prog(t,1.9,3.0)
    if not settled and (0<tg<1 or (tg>=1 and int(t*3)%2==0 and t<7.4)):
        o.append(f'<rect x="{80+(TAG_END-80)*tg+3:.1f}" y="374" width="10" height="20" fill="{CYAN}"/>')
    o.append('<line x1="850" y1="70" x2="850" y2="430" stroke="#9AA4B2" stroke-opacity=".18" stroke-dasharray="2 7"/>')
    busp=1 if settled else eio(prog(t,3.0,4.6))
    o.append(f'<line x1="{BX}" y1="{YS[0]}" x2="{BX}" y2="{YS[0]+(YS[-1]-YS[0])*busp:.1f}" stroke="url(#bus)" stroke-width="2"/>')
    act=-1 if (t<5.0 or t>7.3) else int((t-5.0)/0.46)%5
    if settled: act=-1
    for i,(y,lp) in enumerate(zip(YS,LBL)):
        c=mix(i/4); st=3.0+i*0.35
        p=1 if settled else eo(prog(t,st,st+0.9))
        on=(i==act); col=CYAN if on else "#FFFFFF"
        o.append(f'<g transform="translate({280*(1-p):.1f} 0)" opacity="{p:.3f}">')
        o.append(f'<path d="M{BX} {y}H{BX+38}l12 -12H{BX+62}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>')
        o.append(f'<circle cx="{BX}" cy="{y}" r="{11 if on else 9}" fill="{CYAN if on else "#05070D"}" fill-opacity="{.25 if on else 1}" stroke="{c}" stroke-width="2.5"/><circle cx="{BX}" cy="{y}" r="3.5" fill="{c}"/>')
        o.append(f'<g transform="translate({BX+80} {y-14})">{ICON[i].format(c=CYAN if on else c)}</g>')
        o.append(f'<path d="{lp}" fill="{col}"/>')
        o.append(f'<path d="M{BX+104} {y+14}H1440" stroke="{c}" stroke-opacity="{.9 if on else .45}" stroke-width="{2 if on else 1.2}"/><rect x="1436" y="{y+11}" width="6" height="6" fill="{c}"/>')
        o.append('</g>')
    if not settled and 4.6<t<7.4:
        py=YS[0]+(YS[-1]-YS[0])*(((t-4.6)/1.4)%1)
        o.append(f'<circle cx="{BX}" cy="{py:.1f}" r="4.5" fill="#FFFFFF"/><circle cx="{BX}" cy="{py:.1f}" r="9" fill="{CYAN}" opacity=".3"/>')
    o.append('</g></svg>')
    return "\n".join(o)

def main():
    from playwright.sync_api import sync_playwright
    from PIL import Image
    FPS=int(os.environ.get("FPS","10")); N=int(T*FPS)
    frames=[]
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={"width":W,"height":H})
        for i in range(N):
            pg.set_content(f'<body style="margin:0;background:#000">{scene(i/FPS)}</body>')
            frames.append(Image.open(io.BytesIO(pg.screenshot(clip={"x":0,"y":0,"width":W,"height":H}))).convert("RGB"))
        svg=scene(6.0,settled=True)
        open(f"{OUT}/assets/arcange-github-banner.svg","w").write(svg)
        pg.set_content(f'<body style="margin:0;background:#000">{svg}</body>'); pg.screenshot(path=f"{OUT}/assets/arcange-github-banner.png",clip={"x":0,"y":0,"width":W,"height":H})
        pg2=b.new_page(viewport={"width":W,"height":H},device_scale_factor=2)
        pg2.set_content(f'<body style="margin:0;background:#000">{svg}</body>'); pg2.screenshot(path=f"{OUT}/arcange-banner-preview-3000x1000.png",clip={"x":0,"y":0,"width":W,"height":H})
        b.close()
    keys=[0.4,1.2,2.4,3.6,5.2,6.4]
    sb=Image.new("RGB",(1500,750),"#000")
    for j,k in enumerate(keys):
        sb.paste(frames[int(k*FPS)].resize((750,250),Image.LANCZOS),((j%2)*750,(j//2)*250))
    sb.save(f"{OUT}/arcange-banner-storyboard.png")
    cols=int(os.environ.get("COLORS","64"))
    sample=Image.new("RGB",(W,H*4+300))
    for j,k in enumerate((int(N*.25),int(N*.45),int(N*.65),int(N*.85))): sample.paste(frames[k],(0,j*H))
    # weight brand colours so palette reduction keeps the cyan/blue/white accents vivid
    from PIL import ImageDraw
    d=ImageDraw.Draw(sample)
    for n,c in enumerate(("#22D3EE","#2563EB","#FFFFFF","#D5DDEB","#9CC3FF","#C9A24A")):
        d.rectangle([n*250,H*4,n*250+249,H*4+299],fill=c)
    pal=sample.quantize(colors=cols,method=Image.MEDIANCUT,dither=Image.NONE)
    q=[f.quantize(palette=pal,dither=Image.NONE) for f in frames]
    q[0].save(f"{OUT}/assets/arcange-github-banner.gif",save_all=True,append_images=q[1:],duration=int(1000/FPS),loop=0,optimize=True,disposal=1)
    print("frames",N,"gif MB",round(os.path.getsize(f"{OUT}/assets/arcange-github-banner.gif")/1e6,2))
if __name__=="__main__": main()
