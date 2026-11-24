"""One bloom's life: every kind of content, the same skeleton, through five stages."""
from mocklib import ic, cell, board, life, bee_chip
from content import *

STAGES = [("① 刚存入", "图标、标题、来源、时间，加状态标识：三个空心的形状。"),
          ("② 分派后", "三个形状变实心。多出：交给谁、还能活几天。"),
          ("③ 解读后：解读", "固定四行：是什么、事实、要点、判定。这时就能读、能处理，并通知一句。"),
          ("④ 进每日摘要", "值得深读的留一句话加判定；其余缩成一行。"),
          ("⑤ 到期删除", "内容和解读消失；每日摘要里那一句还在。收藏了的不走到这一步。")]
MARKS = ["刚存入，等分派", "等解读", "已解读", "值得深读，进了每日摘要", "深入对话后留成笔记"]
NOTE = {"文章": "事实行：作者、篇幅", "视频": "事实行：时长", "截屏": "事实行：图里有什么", "仓库": "事实行：语言、星数、许可",
        "帖子": "事实行：作者、平台。标题取第一句", "文字": "事实行：字数。标题取第一句", "文件": "事实行：格式、页数"}


def in_lesson(f):
    if f["v"] is None:
        return lesson_line(f, "没取到内容")
    if f["v"] == 0:
        return lesson_card(f)
    return f'<div class="fold" style="padding:2px 14px">{lesson_line(f, VERDICT[f["v"]][0])}</div>'


def wilted(f):
    left = "没有东西留下。" if f["v"] is None else ("每日摘要里还在：" + (f["what"] if f["v"] == 0 else f["title"]))
    when = {30: "12月21日", 7: "11月28日"}[f["days"]]
    return (f'<div class="gone"><div class="row g6">{ic(f["icon"], 15)}<span>{when} 到期删除，内容和解读已删除</span></div>'
            f'<p class="sm mt8">{left}</p></div>')


def row(f, name=None, note=None):
    name = name or f["kind"]
    note = note or NOTE[f["kind"]]
    return (f'<div class="rk">{name}<span>{note}</span></div><div>{stage1(f)}</div><div>{stage1(f, 1)}</div>'
            f'<div>{drop(f)}</div><div>{in_lesson(f)}</div><div>{wilted(f)}</div>')


def sheet():
    hd = '<div></div>' + "".join(f'<div class="hd"><b>{cell(i, 18) if i < 4 else ""}{t}</b>{d}</div>' for i, (t, d) in enumerate(STAGES))
    run = "".join(f'<span class="row g6">{cell(i, 20)}<span>{t}</span></span>{"<i>→</i>" if i < 4 else ""}' for i, t in enumerate(MARKS))
    rows = "".join(row(f) for f in FLOWERS) + row(FAILED, "没取到内容", "照实说，不拿残片凑")
    inner = (f'<div class="bh">一个条目的一生</div><div class="bsub">七种条目，同一副骨架。从左到右是同一个条目的五个阶段；类型的差别只有一个小图标和解读里的一行事实。'
             f'扫一眼的位置永远一样：第一行知道是什么，最后一行知道要不要管。</div><div class="markrun">{run}</div><div class="lifeg">{hd}{rows}</div>')
    return '<div class="grid" style="--cols:1">' + board("一个条目的一生 · 七种条目 × 五个阶段", "每一格都是界面上真实出现的那张卡。最后一行是没取到内容的情况。", inner, w=1950) + '</div>'
