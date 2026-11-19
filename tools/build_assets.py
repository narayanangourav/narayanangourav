"""Build every SVG used by README.md (spec sheet design, dark + light variants).

Usage (from repo root):  python tools/build_assets.py
Outputs: assets/sheet/*.svg (masthead + numbered sections) and assets/buttons/*.svg.
Edit the content constants below (ABOUT, CODE, FOCUS, STACK, EXTRA, COLLAB, ASK, TAG), then rerun.
Stack icon rows are embedded from tools/icons/ (skillicons.dev downloads, one file per row and theme).
assets/sheet/typing.svg is a downloaded readme-typing-svg file and is not generated here.
"""
import re
import sys
import textwrap
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent   # repo root
A = ROOT / "assets"

T = {
    "dark": dict(text="#F0F6FC", muted="#9BA3AE", subtle="#6E7681", rule="#30363D",
                 code="#151B23", accent="#3DD68C", g0="#FFFFFF", g1="#9B9B9B"),
    "light": dict(text="#1F2328", muted="#59636E", subtle="#8C959F", rule="#D1D9E0",
                  code="#F6F8FA", accent="#1A7F37", g0="#000000", g1="#666666"),
}
W, LABEL_W, COL = 880, 220, 240           # canvas, label column, content x
CW = W - COL                              # content width 640
EASE = "cubic-bezier(0.22,1,0.36,1)"
CSS = f"""
.s{{font-family:Geist,Manrope,-apple-system,BlinkMacSystemFont,'Segoe UI Variable Text','Segoe UI',system-ui,sans-serif}}
.m{{font-family:'Geist Mono',ui-monospace,SFMono-Regular,'Cascadia Mono',Consolas,monospace}}
.h1{{font-size:56px;font-weight:600;letter-spacing:-1.6px}}
.h2{{font-size:44px;font-weight:600;letter-spacing:-1.2px}}
.t1{{font-size:20px;font-weight:400}}
.t2{{font-size:18px;font-weight:500;letter-spacing:-0.2px}}
.b3{{font-size:16px;font-weight:400}}
.b1{{font-weight:600}}
.b4{{font-size:14px;font-weight:600}}
.b6{{font-size:14px;font-weight:400}}
.cap{{font-size:12px;font-weight:500;letter-spacing:1.2px}}
.code{{font-size:14px;font-weight:400;white-space:pre}}
.chip{{font-size:13px;font-weight:500}}
.in{{opacity:0;transform:translateY(16px);animation:in 700ms {EASE} forwards}}
@keyframes in{{to{{opacity:1;transform:none}}}}
@keyframes fade{{to{{opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.in{{transform:none;animation:fade 500ms {EASE} forwards}}}}
"""


def svg(h, label, body, css="", extra_ns=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg"{extra_ns} width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
            f'fill="none" role="img" aria-label="{escape(label)}">\n<style>{CSS}{css}</style>\n{body}\n</svg>\n')


def rule(y, t, x=0, w=W):
    return f'<rect x="{x}" y="{y}" width="{w}" height="1" fill="{t["rule"]}"/>'


def label(idx, name, t):
    parts = [p.strip() + ("," if i == 0 and "," in name else "") for i, p in enumerate(name.split(","))]
    spans = "".join(f'<tspan x="0" {"y=" + chr(34) + "80" + chr(34) if i == 0 else "dy=" + chr(34) + "26" + chr(34)}>{escape(p)}</tspan>' for i, p in enumerate(parts))
    return (f'<text x="0" y="52" class="m cap" fill="{t["accent"]}">{idx}</text>'
            f'<text class="s t2" fill="{t["text"]}">{spans}</text>')


def rich(s, t, base_fill):
    """**bold** -> semibold tspans."""
    out = []
    for i, part in enumerate(re.split(r"\*\*", s)):
        if not part:
            continue
        if i % 2:
            out.append(f'<tspan class="b1" fill="{t["text"]}">{escape(part)}</tspan>')
        else:
            out.append(escape(part))
    return "".join(out)


def panel(name, idx, title, content_fn, label_text):
    for th, t in T.items():
        body, h = content_fn(t)
        full = rule(0, t) + label(idx, title, t) + body
        (A / "sheet").mkdir(parents=True, exist_ok=True)
        (A / "sheet" / f"{name}-{th}.svg").write_text(svg(h, label_text, full, extra_ns=' xmlns:xlink="http://www.w3.org/1999/xlink"'), encoding="utf-8")


# ------------------------------------------------------------------ masthead
def masthead():
    for th, t in T.items():
        h = 216
        body = f'''<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="520" y2="0">
<stop offset="0" stop-color="{t["g0"]}"/><stop offset="1" stop-color="{t["g1"]}"/></linearGradient></defs>
<g class="in"><circle cx="5" cy="22" r="4" fill="{t["accent"]}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>
<text x="18" y="27" class="m cap" fill="{t["muted"]}">&gt;_ SOFTWARE ENGINEER</text></g>
<g class="in" style="animation-delay:90ms"><text x="-3" y="112" class="s h1" fill="url(#g)">Narayana N Gourav</text></g>
<g class="in" style="animation-delay:180ms"><text x="0" y="156" class="s t1" fill="{t["muted"]}">Building reliable products from complex systems</text></g>
{rule(h - 1, t)}'''
        (A / "sheet").mkdir(parents=True, exist_ok=True)
        (A / "sheet" / f"masthead-{th}.svg").write_text(
            svg(h, "Narayana N Gourav, Software Engineer. Building reliable products from complex systems.", body), encoding="utf-8")


# ------------------------------------------------------------------ 01 about
ABOUT = [
    "**2+ years of engineering experience** across backend, frontend, and cloud",
    "Focused on **Python, Java, TypeScript, React.js, and SQL**",
    "Building backend systems, web applications, automation, and data workflows",
    "Hands-on with **cloud engineering on AWS and GCP**, serverless systems, and DevOps",
    "Strong believer in clean architecture, testing, and measurable improvement",
    "I solve root causes instead of applying temporary patches",
]


def about(t):
    rows = []
    y0 = 40
    for i, line in enumerate(ABOUT):
        y = y0 + i * 36
        rows.append(f'<text x="{COL}" y="{y + 17}" class="m cap" fill="{t["subtle"]}">—</text>'
                    f'<text x="{COL + 28}" y="{y + 18}" class="s b3" fill="{t["muted"]}">{rich(line, t, t["muted"])}</text>')
    h = y0 + len(ABOUT) * 36 + 28
    return "".join(rows), h


# ------------------------------------------------------------------ 02 mindset (code)
CODE = '''class Engineer:
    def __init__(self):
        self.name = "Narayana N Gourav"
        self.principles = [
            "Fix the root cause",
            "Design for reliability",
            "Automate repeatable work",
            "Keep systems maintainable",
        ]

    def solve(self, problem):
        return analyze(problem).design().test().ship()'''
KW = r"\b(class|def|return)\b"


def hl(line, t):
    out, pos = [], 0
    for m in re.finditer(r'"[^"]*"|' + KW + r"|\bself\b", line):
        out.append(escape(line[pos:m.start()]))
        tok = m.group(0)
        if tok.startswith('"'):
            out.append(f'<tspan fill="{t["muted"]}">{escape(tok)}</tspan>')
        elif tok == "self":
            out.append(f'<tspan fill="{t["subtle"]}">{tok}</tspan>')
        else:
            out.append(f'<tspan fill="{t["accent"]}">{tok}</tspan>')
        pos = m.end()
    out.append(escape(line[pos:]))
    return "".join(out)


def mindset(t):
    lines = CODE.split("\n")
    lh, pad, y0 = 22, 24, 40
    boxh = pad * 2 + len(lines) * lh
    b = [f'<rect x="{COL + .5}" y="{y0 + .5}" width="{CW - 1}" height="{boxh - 1}" rx="8" fill="{t["code"]}" stroke="{t["rule"]}"/>',
         f'<text x="{W - 20}" y="{y0 + 26}" text-anchor="end" class="m cap" fill="{t["subtle"]}">PYTHON</text>']
    for i, ln in enumerate(lines):
        y = y0 + pad + i * lh + 15
        b.append(f'<text x="{COL + 24}" y="{y}" class="m code" xml:space="preserve" fill="{t["text"]}">{hl(ln, t)}</text>')
    return "".join(b), y0 + boxh + 40


# ------------------------------------------------------------------ 03 focus (table rows)
FOCUS = [
    ("Backend Engineering", "APIs, databases and scalable services with Django, Django REST Framework, Flask, FastAPI, Node.js and Express"),
    ("Frontend Engineering", "React.js, Next.js, TypeScript and Tailwind CSS"),
    ("API Development", "REST, RPC and gRPC services, plus WebSockets for real time features"),
    ("Cloud & DevOps", "AWS (EC2, Lambda, S3) and GCP, CI/CD with GitHub Actions and Jenkins, Docker and Kubernetes"),
    ("Automation", "Terraform infrastructure, Python and Bash scripting, scheduled jobs"),
    ("Data Engineering", "PostgreSQL, MySQL, MongoDB, BigQuery and analytics"),
    ("Code Quality", "Jest, React Testing Library, SonarQube, static analysis and clean architecture"),
    ("AI-Assisted Coding", "OpenAI Codex, Claude Code and modern developer workflows"),
]


def focus(t):
    b, y = [], 40
    vx = COL + 196
    for i, (k, v) in enumerate(FOCUS):
        if len(v) <= 60:
            lines = [v]
        else:
            mid = len(v) // 2
            cut = min((i for i, ch in enumerate(v) if ch == " "), key=lambda i: abs(i - mid))
            lines = [v[:cut], v[cut + 1:]]
        rh = 20 * len(lines) + 24
        if i:
            b.append(rule(y, t, COL, CW))
        b.append(f'<text x="{COL}" y="{y + 27}" class="s b4" fill="{t["text"]}">{escape(k)}</text>')
        for j, ln in enumerate(lines):
            b.append(f'<text x="{vx}" y="{y + 27 + j * 20}" class="s b6" fill="{t["muted"]}">{escape(ln)}</text>')
        y += rh
    return "".join(b), y + 28


# ------------------------------------------------------------------ 04 stack (embedded icons)
STACK = [("Languages", "languages"), ("Frontend and Backend", "frontend-backend"),
         ("Databases and Data", "databases"), ("Cloud and DevOps", "cloud-devops"),
         ("Development Tools", "tools")]
EXTRA = ["SQLAlchemy", "Streamlit", "BigQuery", "SonarQube", "OpenAI Codex", "Weblate",
         "gRPC", "Jest", "Testing Library", "Claude Code"]
ICON_SRC = Path(__file__).resolve().parent / "icons"   # skillicons rows, <name>-<theme>.svg


def embed_icons(path, x, y, h, prefix):
    s = path.read_text(encoding="utf-8").strip()
    m = re.match(r"<svg([^>]*)>", s)
    vb = re.search(r'viewBox="([^"]+)"', m.group(1)).group(1)
    vw, vh = map(float, vb.split()[2:])
    inner = s[m.end():s.rfind("</svg>")]
    inner = re.sub(r'id="([^"]+)"', lambda k: f'id="{prefix}{k.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda k: f'url(#{prefix}{k.group(1)})', inner)
    inner = re.sub(r'href="#([^"]+)"', lambda k: f'href="#{prefix}{k.group(1)}"', inner)
    w = vw * h / vh
    return f'<svg x="{x}" y="{y}" width="{w:.1f}" height="{h}" viewBox="{vb}">{inner}</svg>'


def chips(items, x0, y0, maxw, t):
    b, x, y = [], x0, y0
    for it in items:
        w = len(it) * 7.4 + 24
        if x + w > x0 + maxw:
            x, y = x0, y + 36
        b.append(f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1:.1f}" height="27" rx="6" fill="{t["code"]}" stroke="{t["rule"]}"/>'
                 f'<text x="{x + w / 2:.1f}" y="{y + 18.5}" text-anchor="middle" class="m chip" fill="{t["muted"]}">{escape(it)}</text>')
        x += w + 8
    return "".join(b), y + 28


def stack_for(th):
    def fn(t):
        b, y = [], 40
        vx = COL + 196
        for i, (k, f) in enumerate(STACK):
            if i:
                b.append(rule(y, t, COL, CW))
            b.append(f'<text x="{COL}" y="{y + 31}" class="s b4" fill="{t["text"]}">{escape(k)}</text>')
            b.append(embed_icons(ICON_SRC / f"{f}-{th}.svg", vx, y + 10, 32, f"r{i}_"))
            y += 52
        b.append(rule(y, t, COL, CW))
        b.append(f'<text class="s b4" fill="{t["text"]}"><tspan x="{COL}" y="{y + 31}">Additional</tspan><tspan x="{COL}" dy="20">Engineering Tools</tspan></text>')
        c, endy = chips(EXTRA, vx, y + 14, CW - 196, t)
        b.append(c)
        return "".join(b), endy + 40
    return fn


# ------------------------------------------------------------------ 05 collaborate
COLLAB = ["Full-stack applications using Python, Java, React, Next.js, and TypeScript",
          "REST, RPC, and gRPC API development",
          "PostgreSQL and database-focused systems",
          "Cloud-native and serverless applications on AWS and GCP",
          "CI/CD pipelines, infrastructure as code, and engineering automation",
          "Data analytics and internal engineering platforms",
          "Open-source tools that improve developer productivity"]


def collab(t):
    b = [f'<text x="{COL}" y="58" class="s b3" fill="{t["text"]}">I am open to collaborating on:</text>']
    y = 76
    for i, line in enumerate(COLLAB):
        b.append(f'<text x="{COL}" y="{y + 18}" class="m cap" fill="{t["subtle"]}">{i + 1:02d}</text>'
                 f'<text x="{COL + 36}" y="{y + 18}" class="s b3" fill="{t["muted"]}">{escape(line)}</text>')
        y += 34
    return "".join(b), y + 28


# ------------------------------------------------------------------ 06 ask me about
ASK = ["Python", "Java", "TypeScript", "React.js", "Next.js", "Django", "Flask", "FastAPI", "PostgreSQL",
       "SQLAlchemy", "REST APIs", "gRPC", "Streamlit", "AWS", "GCP", "Terraform", "Docker", "Kubernetes",
       "CI/CD", "SonarQube"]


def ask(t):
    c, endy = chips(ASK, COL, 40, CW, t)
    return c, endy + 40


# ------------------------------------------------------------------ closing
TAG = [["Build", "clearly."], ["Automate", "carefully."], ["Ship", "reliably."]]


def closing():
    for th, t in T.items():
        h = 344
        css = f"""
.w{{fill:{t["text"]};animation:lit 9s {EASE} infinite both}}
@keyframes lit{{0%{{fill:{t["subtle"]}}}7%{{fill:{t["text"]}}}80%{{fill:{t["text"]}}}90%{{fill:{t["subtle"]}}}100%{{fill:{t["subtle"]}}}}}
@media (prefers-reduced-motion:reduce){{.w{{fill:{t["text"]};animation:none}}}}"""
        b = [rule(0, t), f'<text x="0" y="52" class="m cap" fill="{t["accent"]}">07</text>',
             f'<text x="0" y="80" class="s t2" fill="{t["text"]}">Thanks for stopping by</text>']
        k = 0
        for li, line in enumerate(TAG):
            spans = []
            for wi, w in enumerate(line):
                spans.append(("" if not wi else " ") + f'<tspan class="w" style="animation-delay:{400 + k * 260}ms">{w}</tspan>')
                k += 1
            b.append(f'<text x="{COL - 2}" y="{84 + li * 48}" class="s h2">{"".join(spans)}</text>')
        b.append(f'<text x="{COL}" y="{h - 72}" class="s b3" fill="{t["muted"]}">Got a tough challenge? Let&#8217;s dig in. The links up top reach me fastest.</text>')
        b.append(rule(h - 1, t))
        (A / "sheet" / f"closing-{th}.svg").write_text(
            svg(h, "Thanks for stopping by. Build clearly. Automate carefully. Ship reliably. Got a tough challenge? Let's dig in. The links up top reach me fastest.", "".join(b), css),
            encoding="utf-8")


masthead()
panel("about", "01", "About Me", about, "About Me. " + " ".join(s.replace("**", "") + "." for s in ABOUT))
panel("mindset", "02", "Engineering Mindset", mindset, "Engineering Mindset. " + CODE.replace("\n", " "))
panel("focus", "03", "Current Focus", focus, "Current Focus. " + " ".join(f"{k}: {v}." for k, v in FOCUS))
for th in T:
    body, h = stack_for(th)(T[th])
    full = rule(0, T[th]) + label("04", "Technology Stack", T[th]) + body
    (A / "sheet" / f"stack-{th}.svg").write_text(svg(h, "Technology Stack. Languages: Python, Java, TypeScript, JavaScript, Node.js. Frontend and Backend: React, Next.js, Tailwind CSS, Django, Flask, FastAPI, Express, HTML, CSS. Databases and Data: PostgreSQL, MongoDB, MySQL, SQLite, Firebase, Supabase. Cloud and DevOps: AWS, Google Cloud, Cloudflare, Terraform, Docker, Kubernetes, Jenkins, GitHub Actions, Linux, Bash. Development Tools: Git, GitHub, VS Code, IntelliJ IDEA, Postman, Maven, Gradle. Additional Engineering Tools: " + ", ".join(EXTRA) + ".", full, extra_ns=' xmlns:xlink="http://www.w3.org/1999/xlink"'), encoding="utf-8")
panel("collaborate", "05", "Building Better, Together", collab, "Building Better, Together. I am open to collaborating on: " + "; ".join(COLLAB) + ".")
panel("ask", "06", "Ask Me About", ask, "Ask Me About: " + ", ".join(ASK) + ".")
closing()

# ------------------------------------------------------------------ buttons (links live in README.md)
ARROW = "M200,64V168a8,8,0,0,1-16,0V83.31L69.66,197.66a8,8,0,0,1-11.32-11.32L172.69,72H88a8,8,0,0,1,0-16H192A8,8,0,0,1,200,64Z"
BUTTONS = [("portfolio", "Explore portfolio", 182, True), ("linkedin", "LinkedIn", 114, False), ("email", "Email me", 118, False)]
BTN = {"dark": dict(bg="#1F1F1F", fg="#FFFFFF", stroke="#313131", pbg="#FFFFFF", pfg="#000000"),
       "light": dict(bg="#F5F5F5", fg="#000000", stroke="#D9D9D9", pbg="#000000", pfg="#FFFFFF")}


def buttons():
    (A / "buttons").mkdir(parents=True, exist_ok=True)
    for th, c in BTN.items():
        for key, text, w, primary in BUTTONS:
            bg, fg, st = (c["pbg"], c["pfg"], c["pbg"]) if primary else (c["bg"], c["fg"], c["stroke"])
            ix = w - 28
            body = (f'<rect x=".5" y=".5" width="{w - 1}" height="39" rx="8" fill="{bg}" stroke="{st}"/>'
                    f'<text x="{(12 + ix - 8) / 2}" y="25.5" text-anchor="middle" class="s" style="font-size:16px;font-weight:600" fill="{fg}">{text}</text>'
                    f'<g transform="translate({ix} 12) scale(.0625)"><path d="{ARROW}" fill="{fg}"/></g>')
            out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="40" viewBox="0 0 {w} 40" fill="none" role="img" aria-label="{text}">'
                   f'<style>{CSS}</style>{body}</svg>\n')
            (A / "buttons" / f"{key}-{th}.svg").write_text(out, encoding="utf-8")


buttons()
print("ok")
