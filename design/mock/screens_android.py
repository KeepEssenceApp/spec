"""Android app: the most representative screens, in Android's own chrome."""
from mocklib import ic, cell, android
from content import *
import screens_iphone as I


def screens():
    host = I.host_article()
    return [
        android("今天", "和 iPhone 同样的内容：今日状态、今晚的每日摘要、今天的解读。底部导航是安卓的样式。",
                I.today(1), tab="home", title="今天", right=" ", bg=hive_bg()),
        android("每日摘要", "点页签直接是最新一份。内容和 iPhone 一致。", I.reading(), tab="class", title="每日摘要", right=ic("share", 22)),
        android("往右滑 · 加入深挖队列", "和 iPhone 一样的两个滑动：往右加入深挖队列，往左不感兴趣。", I.reading_swipe(), tab="class", title="每日摘要", right=ic("share", 22)),
        android("排入之后", "底部一条提示，带撤销。", I.reading_swipe(True), tab="class", title="每日摘要", right=ic("share", 22),
                overlay=f'<div class="snack" style="bottom:96px">{said_undo(SAY_DIGQ)}</div>'),
        android("往左滑 · 不感兴趣", "方向和意思跟 iPhone 一致。", I.today_swipe(), tab="home", title="今天", right=" ", bg=hive_bg()),
        android("解读好了 · 通知一句", "和 iPhone 一样的一句：判定在前，标题在后。连着解读好的合成一条。", host, title="blog.example.dev", back=True, pad=False,
                overlay=I.notif(*NOTE_ONE)),
        android("笔记", "深挖队列在最上面，下面是笔记。", I.honey_list(), tab="honey", title="笔记"),
        android("从别的 App 分享", "系统分享面板里选 KeepEssence 后，底部一条提示说结果，不换应用。", host, title="blog.example.dev", back=True, pad=False,
                overlay=f'<div class="snack">{said(ic("check", 18), SAY_OK.format(T0))}</div>'),
        android("没网：排着队", "先存在手机里，联网后自己上传。", host, title="blog.example.dev", back=True, pad=False,
                overlay=f'<div class="snack">{said(ic("wifioff", 18), SAY_QUEUED)}</div>'),
        android("助手设置", "第四个页签，管理档才有。", I.colony(), tab="set", title="助手设置"),
    ]
