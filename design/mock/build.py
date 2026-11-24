#!/usr/bin/env python3
"""Build design/mock/index.html: one self-contained page with every client's screens on a pan/zoom canvas.

    python3 design/mock/build.py

To add a screen: add one frame call (phone / android / webapp / browser / macdesk / eink from mocklib.py)
to the list in the matching screens_*.py, then run this again.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mocklib import sprite, section, section_raw, logo  # noqa: E402
import screens_iphone, screens_android, screens_web, screens_capture, screens_eink, screens_more, screens_life  # noqa: E402

SECTIONS = [
    ("iphone", "iPhone App", "读的平台，也能存入。底部四个页签：今天、每日摘要、笔记、助手设置。进来就是今天：已经存入、还没进每日摘要的东西。", screens_iphone.screens(), 6),
    ("share", "iPhone 分享入口", "从任何 App 的分享面板存入。一个动作，继续做手上的事，完成时一句话。", screens_iphone.share_screens(), 6),
    ("shortcut", "iPhone 快捷指令", "「存入到 KeepEssence」和「截屏到 KeepEssence」，绑在轻点背面上。", screens_iphone.shortcut_screens(), 6),
    ("android", "安卓 App", "和 iPhone 同样的内容，用安卓的系统样式。", screens_android.screens(), 6),
    ("web", "网页", "读的平台的完整版。左栏和手机底栏是同样的四项、同样的顺序。没有搜索框，没有标签筛选。", screens_web.screens(), 3),
    ("ext", "浏览器扩展", "只负责存入。点工具栏按钮或右键，结果在页面右上角说一句。没有需要再点一下的弹窗。", screens_capture.ext_screens(), 3),
    ("mac", "Mac 菜单栏应用", "只负责存入。菜单栏图标加一个下拉菜单。", screens_capture.mac_screens(), 3),
    ("eink", "墨水屏", "每日摘要在黑白墨水屏上：没有图，大字，高对比。", screens_eink.screens(), 3),
]


def main():
    css = (HERE / "mock.css").read_text()
    js = (HERE / "canvas.js").read_text()
    toc = "".join(f'<button data-go="{sid}">{title}</button>' for sid, title, *_ in SECTIONS)
    RAW = [
        ("life", "一个条目的一生", "七种条目用同一副骨架，画出同一个条目从存入到到期删除的五个样子。先看这里。", screens_life.sheet()),
        ("perm", "设备权限", "一台设备能看到什么、能做什么，取决于授权时给它的那一档：只存入、读、管理。", screens_more.perms()),
        ("flows", "流程", "四条主线，按箭头从左往右看。每一屏左上角是步骤号，箭头上写的是谁做了什么。", screens_more.flows()),
        ("states", "状态", "空的、加载中、出错，以及这个产品特有的：还没有每日摘要、没有助手、条目快到期删除、精读在等。", screens_more.states()),
        ("kit", "组件与样式", "颜色、字号、间距、按钮、列表行、卡片、寿命、状态标识、空状态。各端的屏幕由这些拼成。", screens_more.components()),
    ]

    def col(ids):
        return '<div class="colw">' + "".join(section(sid, title, desc, frames, cols) for sid, title, desc, frames, cols in SECTIONS if sid in ids) + "</div>"
    raw = '<div class="colw">' + "".join(section_raw(*r) for r in RAW) + "</div>"
    body = raw + col(("iphone", "share", "shortcut", "android")) + col(("web", "ext", "mac", "eink"))
    toc = "".join(f'<button data-go="{sid}">{title}</button>' for sid, title, *_ in RAW) + toc
    n = sum(len(s[3]) for s in SECTIONS) + sum(r[3].count('<figure') for r in RAW)
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>KeepEssence UX mock</title>
<style>{css}</style>
</head>
<body>
{sprite()}
<div id="bar">
  <div class="box" id="brand">{logo("simple", 24)}<span>KeepEssence UX mock · {n} 屏</span></div>
  <div class="box" id="toc">{toc}</div>
  <div class="box" id="zoom"><button id="z-out" class="opt">−</button><span id="zl">100%</span><button id="z-in" class="opt">+</button><button id="z-100">100%</button><button id="z-fit">适应全部</button></div>
</div>
<div id="vp"><div id="world">{body}</div></div>
<div id="hint">拖动平移 · 滚轮或双指缩放 · 双击一屏放大 · 0 适应全部 · 1 原始大小</div>
<script>{js}</script>
</body>
</html>
"""
    (HERE / "index.html").write_text(html)
    print(f"index.html: {n} screens, {len(html) // 1024} KB")
    for sid, title, _d, frames, _c in SECTIONS:
        print(f"  {sid:9} {len(frames):2}  {title}")


if __name__ == "__main__":
    main()
