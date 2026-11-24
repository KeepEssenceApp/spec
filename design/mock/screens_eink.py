"""The evening lesson on a black-and-white e-ink reader: no images, large type, high contrast."""
from mocklib import eink
from content import *


def card(f):
    return f'<div class="it"><b>{f["what"]}</b>{f["kind"]} · 值得深挖<div class="u">{f["title"]} · {f["src"]}</div></div>'


def screens():
    p1 = (f'<h1>每日摘要 · {DATE}</h1><div class="meta">阿读汇总 · 存入了 9 条</div><p style="margin-top:14px">{SUMMARY}</p>'
          f'<h2>值得深挖的</h2>{card(FLOWERS[0])}{card(FLOWERS[3])}')
    p2 = ('<h2 style="margin-top:0">其余的</h2>' + "".join(f'<p>· {FLOWERS[i]["title"]}　<span style="font-size:17px">{m}</span></p>' for i, m in REST)
          + '<p style="margin-top:30px;font-size:17px">深挖、不感兴趣、看过了，要到手机或电脑上点。墨水屏只读。</p>')
    p3 = (f'<h2 style="margin-top:0">睡前一问</h2><p style="font-size:25px;line-height:1.6">{NIGHT}</p>'
          f'<p style="margin-top:20px;font-size:17px">不用回答。带着它去睡。</p>'
          f'<div class="btns" style="margin-top:28px"><span class="f">读了，晚安</span><span>上一页</span></div>')
    return [
        eink("第一页", "总结几句话，然后是值得深挖的。纯文字，没有图，没有灰色的字。", p1, "1 / 3"),
        eink("其余的", "一行一条。墨水屏上不提供动作。", p2, "2 / 3"),
        eink("最后一页", "睡前一问，和唯一的动作「读了，晚安」。", p3, "3 / 3"),
    ]
