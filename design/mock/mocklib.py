"""Building blocks for the UX mock canvas: icons, logo symbols, device frames, page CSS and canvas JS.

Screens live in screens_*.py and call the frame functions here. build.py puts everything into index.html.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGO = HERE.parent.parent / "brand" / "logo"

# ---------------------------------------------------------------- icons (24x24, stroke = currentColor)
_I = {
    "home": '<path d="M4 11l8-7 8 7"/><path d="M6 10v9h12v-9"/>',
    "book": '<path d="M5 5h9a3 3 0 013 3v11H8a3 3 0 01-3-3z"/><path d="M5 16a3 3 0 013-3h9"/>',
    "jar": '<rect x="5" y="4" width="14" height="16"/><path d="M8.5 9h7M8.5 12.500h7M8.500 16h4"/>',
    "flower": '<rect x="5.500" y="5.500" width="13" height="13"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/>',
    "chev": '<path d="M9 6l6 6-6 6"/>',
    "back": '<path d="M15 6l-6 6 6 6"/>',
    "down": '<path d="M6 9l6 6 6-6"/>',
    "bee": '<rect x="5" y="8.500" width="14" height="10.500"/><path d="M12 8.500V5.500"/><path d="M9.500 13v1.500M14.500 13v1.500"/><path d="M10.500 4.500h3"/>',
    "clock": '<circle cx="12" cy="12" r="8"/><path d="M12 7.5V12l3 2"/>',
    "link": '<path d="M10 14a4 4 0 005.7 0l2.6-2.6a4 4 0 00-5.7-5.7L11.5 6.800"/><path d="M14 10a4 4 0 00-5.7 0l-2.6 2.6a4 4 0 005.7 5.7l1.1-1.1"/>',
    "dl": '<path d="M12 4v11M7.500 11l4.500 4.500 4.500-4.500M5 20h14"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "check": '<path d="M5 12.5l4.500 4.500L19 7.500"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "nope": '<path d="M7 14V5h9.500a2 2 0 012 1.600l1 6a2 2 0 01-2 2.400H14l.800 3.200a1.800 1.800 0 01-3.300 1.300L9 14z"/><path d="M7 5H4v9h3"/>',
    "share": '<path d="M12 15V4M8 8l4-4 4 4"/><path d="M6 12v7h12v-7"/>',
    "wifioff": '<path d="M4 4l16 16"/><path d="M8.500 15.500a5 5 0 017 0M5.500 12.300a9.500 9.500 0 014-2.400M18.500 12.300a9.500 9.500 0 00-5-2.700"/><circle cx="12" cy="19" r="1"/>',
    "img": '<rect x="4" y="5" width="16" height="14" rx="2"/><circle cx="9" cy="10" r="1.500"/><path d="M5 17l4.500-4.500 3.500 3.500 2.500-2.500L20 17"/>',
    "text": '<path d="M6 7h12M6 12h12M6 17h7"/>',
    "video": '<rect x="3.500" y="6" width="12" height="12" rx="2"/><path d="M15.500 10.500L20.500 8v8l-5-2.500"/>',
    "file": '<path d="M7 3.500h7l4 4V20.500H7z"/><path d="M14 3.500V8h4"/>',
    "chat": '<path d="M5 6h14v10H10l-4 3.500V16H5z"/>',
    "key": '<circle cx="8" cy="14" r="3.500"/><path d="M10.500 11.500L19 3M15.500 6.500l2.500 2.500"/>',
    "device": '<rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/>',
    "chart": '<path d="M5 19V9M10 19V5M15 19v-7M20 19v-11"/>',
    "warn": '<path d="M12 4l9 15.500H3z"/><path d="M12 10v4.500"/><circle cx="12" cy="17" r=".600"/>',
    "dots": '<circle cx="6" cy="12" r="1.200"/><circle cx="12" cy="12" r="1.200"/><circle cx="18" cy="12" r="1.200"/>',
    "lock": '<rect x="6" y="11" width="12" height="9" rx="2"/><path d="M8.500 11V8a3.500 3.500 0 017 0v3"/>',
    "clip": '<rect x="6" y="5" width="12" height="16" rx="2"/><path d="M9 5a3 3 0 016 0"/>',
    "crop": '<path d="M7 3v14h14M3 7h14v14"/>',
    "pin": '<path d="M12 21v-6M8 4h8l-1 6 3 3H6l3-3z"/>',
    "sun": '<circle cx="12" cy="12" r="3.500"/><path d="M12 3v2.500M12 18.500V21M3 12h2.500M18.500 12H21M5.600 5.600l1.800 1.800M16.600 16.600l1.800 1.800M5.600 18.400l1.800-1.800M16.600 7.400l1.800-1.800"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def ic(name, size=20, cls=""):
    return (f'<svg class="ic {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.700" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true">{_I[name]}</svg>')


# ---------------------------------------------------------------- logo symbols (from brand/logo, unmodified shapes)
# (file, recolour): the strokes of the mark follow the text colour of where it sits, so one symbol serves both themes.
# The dot stays gold, except in the single-colour version.
_SYMS = {
    "lg-color": ("keepessence-mark-black.svg", True),            # with the triangle and the square
    "lg-simple": ("keepessence-mark-simple-black.svg", True),    # without them, 24 to 64 px
    "lg-16": ("keepessence-favicon-16.svg", False),              # pixel version on its black tile
    "lg-mono": ("keepessence-mark-mono-black.svg", True),
    "lg-white": ("keepessence-mark-mono-black.svg", True),
    "lg-app": ("keepessence-icon.svg", False),
    "lg-word": ("keepessence-wordmark-black.svg", True),
}


def _svg(fn):
    src = (LOGO / fn).read_text().strip()
    return re.search(r'viewBox="([^"]+)"', src).group(1), re.sub(r"^<svg[^>]*>|</svg>\s*$", "", src)


def sprite():
    out = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true">']
    for sid, (fn, recolour) in _SYMS.items():
        vb, inner = _svg(fn)
        if recolour:
            inner = inner.replace("#0B0B0B", "currentColor")
        out.append(f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>')
    out.append("</svg>")
    return "".join(out)


def logo(kind="color", size=28, cls=""):
    return f'<svg class="lg {cls}" width="{size}" height="{size}"><use href="#lg-{kind}"/></svg>'


def wordmark(h=22, light=False):
    """The name in outlines. It takes the text colour of where it sits; `light` is kept for callers and not needed."""
    _, _, vw, vh = (float(v) for v in _svg(_SYMS["lg-word"][0])[0].split())
    h = round(h * 0.82)
    return f'<svg class="lg" width="{round(h * vw / vh)}" height="{h}"><use href="#lg-word"/></svg>'


# the state of one piece of content, read the way the logo reads: a pile of mixed shapes comes in, one dot is kept.
# 0 three hollow shapes (waiting to be dispatched), 1 three solid shapes (waiting to be read), 2 one black dot (read),
# 3 gold ring (worth digging, in the digest), 4 gold dot (kept as a note). Gold only from 3 on.
_PILE = ("M12 2.500L17.500 11.500H6.500z", (2.500, 13, 8.500), (17.250, 17.250, 4.250))   # triangle, square, circle


def cell(state, size=18):
    tri, (sx, sy, sw), (cx, cy, cr) = _PILE
    if state == 0:
        w = 1.700                                 # the stroke sits inside the same outline the solid pile fills
        shape = (f'<g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linejoin="miter">'
                 f'<path d="M12 4.130L15.980 10.650H8.020z"/>'      # the triangle above, inset by half a stroke
                 f'<rect x="{sx + w / 2}" y="{sy + w / 2}" width="{sw - w}" height="{sw - w}"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="{cr - w / 2}"/></g>')
    elif state == 1:
        shape = (f'<g fill="currentColor"><path d="{tri}"/><rect x="{sx}" y="{sy}" width="{sw}" height="{sw}"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="{cr}"/></g>')
    elif state == 3:
        shape = '<circle cx="12" cy="12" r="5.600" fill="none" stroke="currentColor" stroke-width="2.800"/>'
    else:
        shape = f'<circle cx="12" cy="12" r="{6.500 if state == 2 else 7}" fill="currentColor"/>'
    return f'<svg class="cell s{state}" width="{size}" height="{size}" viewBox="0 0 24 24">{shape}</svg>'


# ---------------------------------------------------------------- frames
def _fig(kind, name, note, inner, w):
    return (f'<figure class="frame f-{kind}" style="width:{w}px"><div class="dev dev-{kind}">{inner}</div>'
            f'<figcaption><b>{name}</b><span>{note}</span></figcaption></figure>')


_STATUS_IOS = ('<div class="sb"><span class="t">21:04</span><span class="isl"></span><span class="r">'
               '<svg width="18" height="12" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx=".7"/><rect x="5" y="5.500" width="3" height="6.500" rx=".7"/><rect x="10" y="3" width="3" height="9" rx=".7"/><rect x="15" y="0" width="3" height="12" rx=".7"/></svg>'
               '<svg width="16" height="12" viewBox="0 0 16 12"><path d="M8 2.400c2.300 0 4.400.900 6 2.400l1-1.100A10 10 0 008 1 10 10 0 001 3.700l1 1.100a8.600 8.600 0 016-2.400zM8 6c1.300 0 2.500.500 3.400 1.300l1-1.100A6.500 6.500 0 008 4.500 6.500 6.500 0 003.600 6.200l1 1.100A5 5 0 018 6zm0 3.200c-.700 0-1.300.300-1.800.700L8 11.800l1.800-1.900c-.500-.400-1.100-.700-1.800-.700z"/></svg>'
               '<svg width="27" height="12" viewBox="0 0 27 12"><rect x=".500" y=".500" width="22" height="11" rx="3.200" fill="none" stroke="currentColor" opacity=".45"/><rect x="2" y="2" width="17" height="8" rx="2"/><rect x="24" y="4" width="2" height="4" rx="1" opacity=".5"/></svg>'
               '</span></div>')

TABS = [("home", "home", "今天"), ("class", "book", "每日摘要"), ("honey", "jar", "笔记"), ("set", "bee", "助手设置")]


def _tabs(active, kind, reader=False, unread=True):
    """Bottom bar: Today, Lesson, Honey, Colony. A reader device has no Colony tab. The dot on Lesson means unread."""
    tabs = TABS[:3] if reader else TABS
    dot = '<i class="tdot"></i>'
    its = "".join(f'<div class="tab{" on" if k == active else ""}"><span class="ti">{ic(i, 24)}{dot if (k == "class" and unread and active != "class") else ""}</span><span>{l}</span></div>' for k, i, l in tabs)
    return f'<div class="tabs tabs-{kind}">{its}</div>'


def sbar_mini(ok=True):
    """The narrowest colony status: how many bees, and a dot. Opens into the wide one."""
    return f'<span class="sbm">{ic("bee", 15)}{"3" if ok else "0"}<span class="dot {"ok" if ok else "bad"}"></span></span>'


def phone(name, note, body, tab=None, title=None, back=None, right="", big=True, dark=False, overlay="", bare=False, pad=True, reader=False, unread=True, bg=""):
    """iPhone frame. title: nav title; back: label of the back button (makes a small centred title); overlay: html above everything."""
    if tab and not right:
        right = sbar_mini()
    nav = ""
    if title is not None:
        if back is not None:
            nav = (f'<div class="nav nav-s"><span class="bk">{ic("back", 22)}{back}</span><span class="nt">{title}</span>'
                   f'<span class="nr">{right}</span></div>')
        elif big:
            nav = f'<div class="nav nav-b"><div class="nb-top"><span></span><span class="nr">{right}</span></div><h1>{title}</h1></div>'
        else:
            nav = f'<div class="nav nav-s"><span></span><span class="nt">{title}</span><span class="nr">{right}</span></div>'
    ui = (f'<div class="ui ios{" dark" if dark else ""}{" bare" if bare else ""}">{bg}{_STATUS_IOS}{nav}'
          f'<div class="body{" pad" if pad else ""}">{body}</div>{_tabs(tab, "ios", reader, unread) if tab else ""}'
          f'<span class="hi"></span>{overlay}</div>')
    return _fig("phone", name, note, ui, 412)


def android(name, note, body, tab=None, title=None, back=False, right="", dark=False, overlay="", pad=True, bg=""):
    sb = ('<div class="sb"><span class="t">21:04</span><span class="hole"></span><span class="r">'
          '<svg width="15" height="12" viewBox="0 0 15 12"><path d="M7.500 1C4.600 1 2 2.100.200 3.900L7.500 11.500l7.300-7.600C13 2.100 10.400 1 7.500 1z"/></svg>'
          '<svg width="13" height="12" viewBox="0 0 13 12"><path d="M12.500 0v12H.500z"/></svg>'
          '<svg width="9" height="13" viewBox="0 0 9 13"><rect x="0" y="1.500" width="9" height="11.500" rx="1.500"/><rect x="2.500" y="0" width="4" height="2" rx=".5"/></svg></span></div>')
    if tab and not right:
        right = sbar_mini()
    nav = ""
    if title is not None:
        nav = f'<div class="abar">{ic("back", 24) if back else ""}<span class="at">{title}</span><span class="nr">{right}</span></div>'
    ui = (f'<div class="ui droid{" dark" if dark else ""}">{bg}{sb}{nav}<div class="body{" pad" if pad else ""}">{body}</div>'
          f'{_tabs(tab, "droid") if tab else ""}<span class="gb"></span>{overlay}</div>')
    return _fig("android", name, note, ui, 430)


def browser(name, note, page, url="keepessence.app", tab_title="KeepEssence", dark=False, w=1280, h=800, ext=None, tab_icon=None):
    """Browser window. ext: None | 'idle' | 'on' draws our toolbar button. page fills the content area."""
    extb = ""
    if ext:
        extb = f'<span class="bx{" on" if ext == "on" else ""}">{logo("simple", 20)}</span>'
    chrome = (f'<div class="bw{" dark" if dark else ""}"><div class="bt"><span class="tl"><i></i><i></i><i></i></span>'
              f'<span class="btab">{tab_icon or logo("16", 15)}<em>{tab_title}</em>{ic("x", 13)}</span>{ic("plus", 15)}</div>'
              f'<div class="bu"><span class="bnav">{ic("back", 17)}{ic("chev", 17)}</span>'
              f'<span class="burl">{ic("lock", 13)}<em>{url}</em></span><span class="bxs">{extb}{ic("dots", 18)}</span></div>'
              f'<div class="bp" style="height:{h}px">{page}</div></div>')
    return _fig("browser", name, note, chrome, w)


TDOT = '<i class="tdot"></i>'
WEBNAV = [("home", "home", "今天"), ("class", "book", "每日摘要"), ("honey", "jar", "笔记"), ("set", "bee", "助手设置")]


def webapp(name, note, active, main, title, dark=False, right="", url=None, bees_ok=True, h=800, overlay="", reader=False):
    active = {"bloom": "home", "ripen": "honey", "stats": "set"}.get(active, active)
    nav = "".join(f'<a class="{"on" if k == active else ""}">{ic(i, 18)}<span>{l}</span>{TDOT if (k == "class" and active != "class") else ""}</a>' for k, i, l in (WEBNAV[:3] if reader else WEBNAV))
    st = ('<span class="dot ok"></span>3 个助手在干活 · 阿读 4 分钟前 · 今天 9 条，4 条在等' if bees_ok else '<span class="dot bad"></span>没有助手在干活 · 14 条在等')
    page = (f'<div class="ui web{" dark" if dark else ""}"><aside><div class="brand">{logo("simple", 28)}{wordmark(19, dark)}</div>'
            f'<nav>{nav}</nav><div class="sp"></div>'
            f'<div class="me"><span class="av">我</span><span>我</span><span class="sp"></span>{ic("sun", 16)}</div></aside>'
            f'<section><header><h1>{title}</h1><span class="sp"></span>{right}<span class="beest">{st}</span></header>'
            f'<main>{main}</main></section>{overlay}</div>')
    return browser(name, note, page, url=url or "keepessence.app", dark=dark, h=h)


def macdesk(name, note, inner, w=1280, h=800, dark=False):
    bar = (f'<div class="mbar"><span class="apple"></span><b>Safari</b><span>文件</span><span>编辑</span><span>显示</span><span>历史记录</span>'
           f'<span class="sp"></span><span class="mi">{ic("wifioff", 15) if False else ""}</span>'
           f'<span class="mi us">{logo("white" if dark else "mono", 19)}</span>'
           f'<span class="mi">100%</span><span class="mi">11月21日 周六 21:04</span></div>')
    return _fig("mac", name, note, f'<div class="desk{" dark" if dark else ""}" style="height:{h}px">{bar}{inner}</div>', w)


def eink(name, note, inner, page="1 / 4"):
    return _fig("eink", name, note, f'<div class="ink">{inner}<div class="inkf"><span>每日摘要 · 11月21日</span><span>{page}</span></div></div>', 640)


def section(sid, title, desc, frames, cols):
    return (f'<section class="sec" id="sec-{sid}"><header class="sech"><h2>{title}</h2><p>{desc}</p></header>'
            f'<div class="grid" style="--cols:{cols}">{"".join(frames)}</div></section>')


# ---------------------------------------------------------------- small shared pieces
def life(days, total=30):
    cls = " soon" if days <= 3 else ""
    txt = "明天删除" if days == 1 else f"{days} 天后删除"
    return f'<span class="life{cls}"><i style="--p:{max(4, round(100 * days / total))}%"></i>{txt}</span>'


def kept():
    """A kept item: its life was extended to never. Same place and shape as the life bar."""
    return '<span class="life kept"><i style="--p:100%"></i>已收藏 · 不过期</span>'


def bee_chip(name):
    return f'<span class="bee">{ic("bee", 14)}{name}</span>'


# ---------------------------------------------------------------- round 2: boards, flows, empty states
def board(name, note, inner, w=1500):
    """A plain sheet (no device) for the style and component reference."""
    return _fig("board", name, note, f'<div class="ui sheetui">{inner}</div>', w)


def section_raw(sid, title, desc, inner):
    return f'<section class="sec" id="sec-{sid}"><header class="sech"><h2>{title}</h2><p>{desc}</p></header>{inner}</section>'


def grid(frames, cols):
    return f'<div class="grid" style="--cols:{cols}">{"".join(frames)}</div>'


def flow(title, desc, steps):
    """steps: list of (frame_html, label_of_the_arrow_that_follows). The last label is ignored."""
    out = []
    for i, (f, lab) in enumerate(steps):
        out.append(f'<div class="fstep"><span class="fnum">{i + 1}</span>{f}</div>')
        if i < len(steps) - 1:
            out.append(f'<div class="arr"><span>{lab}</span><svg width="120" height="24" viewBox="0 0 120 24"><path d="M2 12h108M98 3l14 9-14 9" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
    return f'<div class="flow"><div class="flowh"><b>{title}</b><span>{desc}</span></div><div class="flowr">{"".join(out)}</div></div>'


def hive(days, r=14, today=True, cls=""):
    """The month: one dot per day, seven to a row. days: a state per day up to today (later days are not drawn).
    0 nothing (a speck), 1 something came in (grey ring), 2 digest unread (ring), 3 digest read (solid), 4 a note was
    kept (gold). The name is historical: this used to be a honeycomb."""
    p = r * 1.9                                   # distance between days
    sw = max(.6, r * .14)
    out = []
    for d, st in enumerate(days):
        cx, cy = p / 2 + (d % 7) * p, p / 2 + (d // 7) * p
        c = f'cx="{cx:.1f}" cy="{cy:.1f}"'
        if st == 0:
            out.append(f'<circle {c} r="{max(.7, r * .15):.1f}" fill="var(--line)"/>')
        elif st == 1:
            out.append(f'<circle {c} r="{r * .5 - sw / 2:.1f}" fill="none" stroke="var(--faint)" stroke-width="{sw:.1f}"/>')
        elif st == 2:
            out.append(f'<circle {c} r="{r * .5 - sw / 2:.1f}" fill="none" stroke="var(--ink)" stroke-width="{sw:.1f}"/>')
        elif st == 3:
            out.append(f'<circle {c} r="{r * .5:.1f}" fill="var(--ink)"/>')
        else:
            out.append(f'<circle {c} r="{r * .56:.1f}" fill="var(--gold,#C5A229)"/>')
        if today and d == len(days) - 1:
            h = p * .43
            out.append(f'<rect x="{cx - h:.1f}" y="{cy - h:.1f}" width="{2 * h:.1f}" height="{2 * h:.1f}" fill="none" stroke="var(--ink)" stroke-width="1.2"/>')
    n = max(1, len(days))
    W, H = min(7, n) * p, ((n + 6) // 7) * p
    return f'<svg class="hive {cls}" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" aria-hidden="true">{"".join(out)}</svg>'


def empty(title, text, n=0, action=""):
    """Nothing to list: one sentence, no illustration. The month behind Today already shows the state."""
    return (f'<div class="empty"><div class="h2">{title}</div><p class="sm mt8">{text}</p>'
            f'{f"<div class=mt16>{action}</div>" if action else ""}</div>')


def skel(w="100%", h=14):
    return f'<i class="skel" style="width:{w};height:{h}px"></i>'


def tokens(dark=False):
    """Colour tokens read from mock.css, so the component board can never drift from what the screens use."""
    css = (HERE / "mock.css").read_text()
    block = re.search(r"\.ui\.dark\{([^}]*)\}" if dark else r"\.ui\{([^}]*)\}", css).group(1)
    t = dict(re.findall(r"--([a-z]+):(#[0-9A-Fa-f]{6})", block))
    if dark:                      # the dark theme only overrides some tokens
        t = {**tokens(False), **t}
    return t
