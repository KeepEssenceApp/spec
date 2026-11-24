"""iPhone app, share extension and Shortcuts."""
from mocklib import ic, logo, cell, life, kept, bee_chip, phone, wordmark
from content import *


COLSEG = '<span class="seg"><span class="{a}">助手</span><span class="{b}">规则</span><span class="{c}">设备</span><span class="{d}">月历</span><span>账户</span></span>'


def class_card(done=False):
    return (f'<div class="card"><div class="row"><span class="xs">今晚的每日摘要</span><span class="sp"></span>'
            f'{READ if done else UNREAD}</div>'
            f'<div class="h2 mt4">每日摘要 · {DATE}</div><p class="sm mt4">存入了 9 条。2 条值得深读，其余 5 条收在后面。</p>'
            f'<div class="row mt12"><span class="btn sm">读每日摘要</span><span class="sp"></span><span class="xs">阿读 · 21:02 汇总</span></div></div>')


def waggle_card(n=2):
    rows = "".join(f'<div class="row top mt8">{ic("pin", 16, "deep")}<p class="sm" style="color:var(--ink)"><b>{a}</b>{b}</p></div>' for a, b in WAGGLE[:n])
    return f'<div class="card flat"><div class="xs">以前见过类似的</div>{rows}</div>'


def ripen_card(title="「能安全重放」怎么定义？"):
    return ripen_req(title, SIPPER, "ready",
                     f'<div class="row mt12"><span class="btn sm">{ic("chat", 15)}去深入对话</span><span class="xs">{SIPPER}读好了</span></div>', label=True)


def bees_card(ok=True):
    if ok:
        return (f'<div class="card flat"><div class="row"><span class="dot ok"></span><span class="sm" style="color:var(--ink)">3 个助手在干活</span>'
                f'<span class="sp"></span><span class="xs">阿读 4 分钟前来过</span></div>'
                f'<div class="row mt8"><span class="sm">今天存入了 9 条，2 条等分派，2 条等解读</span><span class="sp"></span>{ic("chev", 16, "faint")}</div></div>')
    return (f'<div class="card bad"><div class="row">{ic("warn", 18, "badc")}<b>没有助手在干活</b></div>'
            f'<p class="sm mt4" style="color:var(--ink)">14 个条目还没被解读，最早的一条 11月24日 到期删除。今天没有每日摘要，因为没有助手来汇总。</p>'
            f'<div class="row mt8"><span class="xs">阿读 3 天前来过</span><span class="sp"></span><span class="lk sm">看助手设置</span></div></div>')


def reading(dark=False):
    return (f'<div class="xs">{SIPPER}汇总 · 21:02 · 存入了 9 条</div><div class="h1 mt4">每日摘要 · {DATE}</div>'
            f'<p class="sm mt8" style="line-height:1.65">{SUMMARY}</p>'
            f'<div class="lab">值得深读的 · 2 条</div>{lesson_card(FLOWERS[0])}<div class="mt12">{lesson_card(FLOWERS[3])}</div>')


def reading_end(done=False):
    return (f'<div class="mt4">{lesson_card(FLOWERS[3])}</div><div class="mt16">{lesson_rest()}</div>{night(done)}'
            f'<p class="xs mt8" style="text-align:center">{"可以撤销。" if done else "只做标记。不点也不欠账。"}</p>')


def today(part=1, dark=False, reader=False):
    light = "".join(f'<div class="mt8" style="opacity:.78">{stage1(f, st)}</div>' for f, st in [
        (dict(FLOWERS[0], title="Streamable HTTP 传输说明（草案）", src="spec.example.io", at="20:51"), 1),
        ])
    if part == 1:
        return sbar_narrow() + f'<div class="lab">还没进每日摘要的 · 3 个解读，新的在前</div>{drop(FLOWERS[0])}<div class="mt12">{drop(FLOWERS[2], pts=1)}</div>'
    return (f'{drop(FLOWERS[3], pts=1)}<div class="lab">处理过的 · 2 个</div><div class="fold" style="padding:2px 14px">{drop_done(FLOWERS[5], "不感兴趣")}{drop_done(FLOWERS[4], "看过了")}</div>'
            f'<div class="lab">还在等助手的条目 · 1 条</div>{light}')


def reading_swipe(done=False):
    """The digest with its first item being swiped right, or just after."""
    head = (f'<div class="xs">{SIPPER}汇总 · 21:02 · 存入了 9 条</div><div class="h1 mt4">每日摘要 · {DATE}</div>'
            f'<p class="sm mt8" style="line-height:1.65">{SUMMARY}</p>')
    if not done:
        return head + f'<div class="lab">值得深读的 · 2 条</div>{swipe(lesson_card(FLOWERS[0]), "dig")}<div class="mt12">{lesson_card(FLOWERS[3])}</div>'
    return (head + f'<div class="lab">值得深读的 · 1 条</div>{lesson_card(FLOWERS[3])}'
            f'<div class="lab">处理过的 · 1 条</div><div class="fold" style="padding:2px 14px">{drop_done(FLOWERS[0], MARK_DIGQ)}</div>')


def today_swipe(done=False):
    """Today with an item being swiped left, or just after."""
    top = sbar_narrow() + f'<div class="lab">还没进每日摘要的 · 3 个解读，新的在前</div>{drop(FLOWERS[0], pts=1)}'
    if not done:
        return top + f'<div class="mt12">{swipe(drop(FLOWERS[2], pts=1), "no")}</div>'
    return top + f'<div class="lab">处理过的 · 1 个</div><div class="fold" style="padding:2px 14px">{drop_done(FLOWERS[2], "不感兴趣")}</div>'


def today_ask():
    """First time an item is waiting for an assistant: one card asks whether to notify. Shown once."""
    f = dict(FLOWERS[0], at="20:51")
    return (sbar_narrow() + f'<div class="card mt12"><b>{ASK_NOTIFY}</b><p class="sm mt4">{ASK_NOTIFY_SUB}</p>'
            f'<div class="row mt12 g6"><span class="btn sm">通知我</span><span class="btn quiet sm">不用</span></div></div>'
            f'<div class="lab">还在等助手的条目 · 1 条</div>{stage1(f, 1)}')


def colony_notify(ok=True):
    return (COLSEG.format(a="on", b="", c="", d="") + f'<div class="lab">谁做哪一步</div><div class="card" style="padding:2px 16px">'
            f'<div class="kv"><span>精读助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>缺省精读助手</span><span class="sel">{bee_chip("阿深")}{ic("down", 16, "faint")}</span></div>'
            f'</div><div class="lab">通知</div>{notify_card(ok=ok)}')


def today_empty():
    from mocklib import empty
    return sbar_narrow() + '<div class="mt20">' + empty("今天的都处理完了", "新存入的条目被解读之后会出现在这里。") + '</div>'


def dig_sheet(mode="link"):
    return f'<div class="scrim"></div><div class="sheet">{dig_pick(mode)}</div>'


def paste_sheet():
    return f'<div class="scrim"></div><div class="sheet">{paste_back()}</div>'


def other(frame):
    """Mark a frame as not KeepEssence's interface."""
    return frame.replace('class="ui ios"', 'class="ui ios other"')


ASSIST_T = "助手 · 已连接 KeepEssence"


def blooms():
    return (f'<div class="row"><span class="sm">未到期的条目 · 23 条</span><span class="sp"></span><span class="seg"><span class="on">今天</span><span>全部</span><span>收藏</span></span></div>'
            f'<div class="lst mt4">{"".join(bloom_row(b) for b in BLOOMS[:7])}</div>')


def bloom_detail(keep=False):
    return (f'<div class="row g6"><span class="thumb">{ic("link", 20)}</span><div class="col"><span class="xs">db.example.org · 今天 15:12 存入自浏览器扩展</span>'
            f'<span class="lk sm">打开原文</span></div></div>'
            f'<div class="h1 mt12" style="font-size:22px">SQLite 在高并发写入下的 WAL 行为实测</div>'
            f'<div class="lab">解读 · {bee_chip("阿读")}</div>'
            f'<p style="font-size:14.5px;line-height:1.65">作者用 8 个写线程压了三种同步级别。结论是 WAL 本身不慢，慢在检查点：有长读事务时检查点推不动，WAL 文件一直涨。'
            f'给了两个办法，一是把读事务切短，二是在空闲时主动做截断式检查点。值得读，尤其是检查点卡住读者的那一节。</p>'
            f'<div class="card flat mt12"><div class="row top">{ic("pin", 16, "deep")}<p class="sm" style="color:var(--ink)"><b>以前见过类似的</b>　和 11月19日 每日摘要里讲租约的那条有关：检查点卡住时，认领的超时不能比它短。</p></div></div>'
            f'<div class="lab">怎么处理这个条目</div><div class="card" style="padding:2px 16px">'
            f'<div class="kv"><span>交给哪个助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>活多久（天）</span>{life_pick(0 if keep else 90)}</div>'
            f'<div class="kv"><span>到期删除</span><span>{kept() if keep else life(90, 90)}</span></div></div>'
            f'<p class="xs mt8">{KEEP_NOTE if keep else LIFE_NOTE + " 想一直留着，选「收藏」。"}</p>')


def kept_list():
    """Today > all items, filtered to the kept ones."""
    rows = "".join(bloom_row((b[0], b[1], b[2], 2, 0, b[5])) for b in (BLOOMS[4], BLOOMS[5], BLOOMS[7]))
    return (f'<div class="row"><span class="sm">收藏的条目 · 3 条 · 不过期</span><span class="sp"></span><span class="seg"><span>今天</span><span>全部</span><span class="on">收藏</span></span></div>'
            f'<div class="lst mt4">{rows}</div><p class="xs mt12">收藏的条目是存入时的原样，加上助手的解读。它们不是笔记：笔记是你深入对话之后存回来的。</p>')


def honey_list(queued=False):
    new = ""
    if queued:
        new = ('<div class="newmark">' + ripen_req(DIG_T, SIPPER, "wait", f'<p class="sm mt4">刚刚排进来。等{SIPPER}下一次来取活，读好了这里会出现「看精读」。</p>') + '</div><div class="mt8"></div>')
    top = (f'<div class="lab" style="margin-top:0">深读队列 · {3 if queued else 2} 个</div>' + new + ripen_req(DIG[0], SIPPER, "ready", f'<div class="row mt12"><span class="btn sm">{ic("chat", 15)}去深入对话</span><span class="lk sm">看精读</span></div>')
           + '<div class="mt8">' + ripen_req(DIG[2], SIPPER, "wait", f'<p class="sm mt4">等{SIPPER}下一次来取活。</p>') + '</div><div class="lab">笔记 · 一直留着</div>')
    rows = "".join(f'<div class="li">{note_thumb()}<div class="col sp">'
                   f'<span class="ti">{t}</span><span class="xs mt4">{d} · {f}{(" · " + a) if a else ""}</span></div></div>' for t, d, f, a in HONEY[:3])
    return f'{top}<div class="lst">{rows}</div>'


def honey_page():
    return (f'<div class="xs">笔记 · 11月20日 · {bee_chip("阿深")}</div><div class="h1 mt4" style="font-size:23px">{HONEY[0][0]}</div>'
            f'<p class="mt12" style="font-size:15px;line-height:1.7">一份活同时只归一个助手，靠的是认领；认领会过期，靠的是租约；过期之后别人接着做不出乱子，靠的是重放安全。三件事缺一件，另外两件都白做。</p>'
            f'<div class="h3 mt16">结论</div>'
            f'<p class="mt4" style="font-size:15px;line-height:1.7">一、租约定 30 分钟，比最慢的一次检查点长。二、交回按内容去重，同一份交两遍只留后一次。三、不能重放的工具不让助手在取活的路上调用。</p>'
            f'<div class="h3 mt16">出处</div>'
            f'<div class="src mt4">{ic("link", 13)}<em>Durable harness · github.com/example/durable-harness</em></div>'
            f'<div class="src mt4">{ic("link", 13)}<em>Leases in job queues · blog.example.dev/leases</em></div>'
            f'<div class="card mt16"><div class="row">{ic("img", 18, "mut")}<span class="sp">租约时序图.png</span><span class="xs">附件 · 182 KB</span>{ic("dl", 18, "deep")}</div></div>'
            f'<p class="xs mt12">出自 11月19日 每日摘要 · 第 2 条</p>')


def ripen_list():
    return ('<div class="col g12">'
            + ripen_req(DIG[0], SIPPER, "ready", f'<p class="sm mt4">{SIPPER}读好了，等你看。7 天没动静就移出。</p><div class="row mt12"><span class="btn sm">{ic("chat", 15)}去深入对话</span><span class="lk sm">看精读</span><span class="sp"></span><span class="xs">11月21日 发起</span></div>')
            + ripen_req(DIG[1], SIPPER, "prep", f'<p class="sm mt4">{SIPPER} 6 分钟前领走了，正在读原文、查相关的。</p>')
            + ripen_req(DIG[2], SIPPER, "wait", f'<p class="sm mt4">等{SIPPER}下一次来取活。它上次来是 4 分钟前。</p><div class="row mt8"><span class="sp"></span><span class="lk sm">移出队列</span></div>')
            + ripen_req("墨水屏上的排版要不要自己调字重", RIPENER, "skip", f'<p class="sm mt4">11月20日 去过，{RIPENER}取过这一条。还没有笔记存回来。</p><div class="row mt12"><span class="btn quiet sm">{ic("chat", 15)}再去深入对话</span><span class="sp"></span><span class="lk sm">把结果贴回来</span><span class="lk sm">移出队列</span></div>')
            + '</div>')


ADD_BEE = f'<div class="row mt12"><span class="btn quiet sm">{ic("plus", 15)}接入一个助手</span></div>'


def colony():
    return (COLSEG.format(a="on", b="", c="", d="") + f'<div class="lab">助手</div><div class="card" style="padding:2px 16px">'
            + bee_row("阿探", "分派助手 · 我们提供，免费", "刚刚来过")
            + bee_row("阿读", ALL3, "4 分钟前来过", "ok", REV)
            + bee_row("阿深", "深入对话", "2 小时前来过", "warn", REV)
            + f'</div>{ADD_BEE}'
            f'<div class="lab">谁做哪一步</div><div class="card" style="padding:2px 16px">'
            f'<div class="kv"><span>缺省解读助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>汇总助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>精读助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>缺省精读助手</span><span class="sel">{bee_chip("阿深")}{ic("down", 16, "faint")}</span></div>'
            f'</div>'
            f'<p class="xs mt12">写给分派助手的话在「规则」里；客户端和助手的权限在「设备」里。</p>')


def bee_pick():
    return f'<p class="sm">选它在哪个产品里。每一种能做的事不一样。</p><div class="mt4">{product_list()}</div><p class="xs mt12">{KINDS_NOTE}</p>'


def bee_allow(product="Claude", name=RIPENER, steps="深入对话"):
    """The allow page for a bee, opened in the browser by the assistant. No short code."""
    kind = dict((x[0], x[1]) for x in PRODUCTS)[product]
    return (f'<div class="col" style="align-items:center;padding-top:20px;text-align:center">{logo("simple", 48)}'
            f'<div class="mt12" style="width:100%">{join_allow(name, kind, "", steps=steps, warn=True, product=product)}</div></div>')


def login():
    return (f'<div class="col" style="align-items:center;padding-top:54px;text-align:center">{logo("color", 88)}'
            f'<div class="mt12">{wordmark(34)}</div></div><div class="mt16">{join_wait("iPhone · App")}</div>'
            f'<div class="mt20"><span class="btn block">打开 KeepEssence</span></div>')


def allow():
    return (f'<div class="col" style="align-items:center;padding-top:28px;text-align:center">{logo("simple", 52)}'
            f'<div class="mt12" style="width:100%">{join_allow("iPhone · App", "客户端", "", tier=2)}</div></div>')


def devices(n=None):
    return (COLSEG.format(a="", b="", c="on", d="") + f'<p class="sm mt12">每个客户端和每个助手都是一个设备。客户端可以改权限。</p>'
            f'<div class="lst mt4">{device_rows(n)}</div>')


def revoke_sheet():
    return f'<div class="scrim"></div><div class="sheet" style="padding-top:22px">{revoke_confirm()}</div>'


# ---- share extension / shortcuts: a host app behind
def host_article():
    return ('<div class="art m"><div class="w"><h1>把定时任务做成幂等的七种写法</h1><div class="by">blog.example.dev · 8 分钟读完</div>'
            '<div class="fig"></div><p>定时任务最常见的事故不是没跑，而是跑了两遍。本文从「同一份活交两遍会怎样」出发，列出七种让它不出乱子的写法。</p>'
            '<p>第一种最朴素：给每份活一个由内容算出来的标识，交回时按标识去重。</p><p>第二种是租约：领活的人拿到一个会过期的凭据……</p></div></div>')


def share_sheet():
    def other(glyph):
        return f'<span style="width:56px;height:56px;border-radius:13px;display:flex;align-items:center;justify-content:center;background:var(--fill);color:var(--mut)">{ic(glyph, 26)}</span>'
    apps = "".join(f'<div class="col g4" style="align-items:center;width:64px">{inner}<span class="xs" style="color:var(--ink)">{n}</span></div>'
                   for n, inner in [("附近设备", other("device")), ("消息", other("chat")),
                                    ("KeepEssence", f'<span style="width:56px;height:56px;border-radius:13px;overflow:hidden;display:block">{logo("app", 56)}</span>'),
                                    ("记事", other("text")), ("更多", other("dots"))])
    return (f'<div class="scrim"></div><div class="sheet" style="padding-bottom:46px"><div class="row"><span class="thumb">{ic("link", 20)}</span><div class="col sp">'
            f'<b style="font-size:14px">{T0}</b><span class="xs">blog.example.dev</span></div></div>'
            f'<div class="hr"></div><div class="row" style="justify-content:space-between">{apps}</div>'
            f'<div class="hr"></div><div class="kv"><span style="color:var(--ink)">拷贝</span>{ic("clip", 18, "mut")}</div>'
            f'<div class="kv"><span style="color:var(--ink)">添加到阅读列表</span>{ic("book", 18, "mut")}</div></div>')


def hud(icon, text, top=380):
    return f'<div class="hud" style="top:{top}px">{icon}<span>{text}</span></div>'


def notif(title, text, when="现在"):
    return (f'<div class="notif"><span class="ai">{logo("app", 38)}</span><div><b>{title}</b>{text}</div><small>{when}</small></div>')


def springboard(dark=False):
    return (f'<div style="height:100%;background:linear-gradient(170deg,#dcdcd9,#9c9c98 55%,#3a3a38);"></div>')


def screens():
    A = phone
    out = [
        A("今天", "缺省进来就是它：已经存入、还没进每日摘要的东西。右上角淡淡的是这个月的月历，一天一个点；今日状态叠在上面。",
          today(1), tab="home", title="今天", right=" ", bg=hive_bg()),
        A("今天 · 往下", "处理过的缩成一行，可以挽回。还没被解读的条目排在最后，样子更轻。",
          today(2), tab="home", title="今天", right=" ", bg=hive_bg()),
        A("今天 · 都处理完了", "只写一句话，不另画插图。背景里今天那个点已经是实心的。", today_empty(), tab="home", title="今天", right=" ", bg=hive_bg(MONTH[:-1] + [3])),
        A("解读好了 · 通知一句", "存入之后要等助手来取活，短则几分钟，长则几小时。解读一交回，发一句：判定在前，标题在后。点它直接打开这个解读。只说一次，没看也不再说；图标上不带数字。",
          springboard(), pad=False, bare=True, overlay=notif(*NOTE_ONE)),
        A("连着解读好的 · 合成一条", "助手一次来读了六条，只收到一条：一共几条、几条值得深读、是哪两条。没取到内容的照实写。点它打开「今天」。",
          springboard(), pad=False, bare=True, overlay=notif(*NOTE_MANY) + notif(*NOTE_MISS, "下午 3:12")),
        A("要不要通知 · 只问一次", "第一次有条目在等助手时，「今天」里多一张卡。点了「通知我」系统才弹权限提问；点「不用」就再也不问，以后想要去助手设置里开。",
          today_ask(), tab="home", title="今天", right=" ", bg=hive_bg()),
        A("这个月的月历", "点右上角的月历打开。一天一个点，五种样子；下面是四个数。没有连续天数，没有提醒。", hive_page(), tab="home", title="", back="今天"),
        A("翻到上个月", "以前的月份整月都画出来。点有每日摘要的那个点打开那天的每日摘要。", hive_page(MONTH_OCT, "10月", ("203", "24", "22", "6"), "9月", "11月"), tab="home", title="", back="今天"),
        A("月初第一天", "只有一个点。", hive_page([1], "12月", ("3", "0", "0", "0"), "11月"), tab="home", title="", back="今天"),
        A("整月都没有条目", "没有条目的日子只是一个小点。没有红色，没有「你已经几天没来」。", hive_page(MONTH_NONE, "1月", ("0", "0", "0", "0"), "12月"), tab="home", title="", back="今天"),
        A("每日摘要", "点页签直接打开最新一份；未读时页签上有个点。左上角翻以前的。四部分：总结、值得深读的、其余的、睡前一问。",
          reading(), tab="class", title="", back="以前的", right=ic("share", 20)),
        A("每日摘要 · 读到最后", "其余的折叠成一行一条，可以挽回。睡前一问不用回答。最后是「读了，晚安」。",
          reading_end(), tab="class", title="", back="以前的", right=ic("share", 20)),
        A("往右滑 · 加入深读队列", "手机上，一个条目可以左右滑，只有两个动作。往右是留：加入深读队列。不用选，也不离开这一页；助手趁它排着先精读。卡上的三个按钮还在，滑动只是快一点。",
          reading_swipe(), tab="class", title="", back="以前的", right=ic("share", 20)),
        A("排入之后", "一句话，带撤销，自己消失。这一条缩成一行，可以挽回。不跳去助手那边：助手趁它排着先精读，你有空了去「笔记」页最上面看精读、去深入对话。",
          reading_swipe(True), tab="class", title="", back="以前的", right=ic("share", 20), overlay=f'<div class="hud" style="top:640px">{said_undo(SAY_DIGQ)}</div>'),
        A("往左滑 · 不感兴趣", "往左是去：不感兴趣。「今天」的解读和每日摘要里的一条都能滑，方向和意思一样。「看过了」没有滑动，还在卡上。",
          today_swipe(), tab="home", title="今天", right=" ", bg=hive_bg()),
        A("标了之后", "和点卡上的「不感兴趣」结果一样：缩成一行，可以挽回。",
          today_swipe(True), tab="home", title="今天", right=" ", bg=hive_bg(), overlay=f'<div class="hud" style="top:640px">{said_undo(SAY_NOPE)}</div>'),
        A("笔记 · 排进来的那一条", "排进队列的条目出现在「笔记」页最上面。定时来的助手下次来取活时精读它；没等到精读也可以直接去深入对话。",
          honey_list(True), tab="honey", title="笔记"),
        A("以前的每日摘要", "按日期倒序，可以往前翻。漏了一天的会并进下一份。没有搜索。",
          '<div class="lst">' + "".join(
              f'<div class="li" style="align-items:center"><div class="col sp"><span class="ti">每日摘要 · {d}</span><span class="xs mt4">{s}</span></div>'
              f'{"" if r else UNREAD}{ic("chev", 16, "faint")}</div>' for d, s, r in CLASSES) + '</div>',
          tab="class", title="以前的每日摘要", back="最新"),
        A("点「深入对话」之后 · 现在去深入对话", "面板顶上两个选项：排入队列先精读，或者现在去深入对话。点卡上的「深入对话」缺省是现在去：列出能深入对话的助手，缺省的已选好。选的是能用链接打开的对话助手（Claude）：一个按钮直接过去。",
          reading(), tab="class", title="", back="以前的", overlay=dig_sheet("link")),
        A("现在去深入对话 · 打不开链接的", "对话助手没有链接可开（Gemini），或者它在手机 App 里：开场话放在框里，复制后贴过去。这是少数几样能复制的东西之一。",
          reading(), tab="class", title="", back="以前的", overlay=dig_sheet("copy")),
        A("点「深入对话」之后 · 排入队列，先精读", "切到左边：加入深读队列，助手趁它排着先精读，不用你在场。精读只有定时来的助手能做，对话里的选不了。和往右滑是同一件事。",
          reading(), tab="class", title="", back="以前的", overlay=dig_sheet("read")),
        other(A("深入对话 · 存成笔记", "这不是 KeepEssence 的界面，是助手自己的地方，画成中性的样子。助手从 KeepEssence 取到这一条；说「存成笔记」，它就存回来。对话不进核心。",
                assist_chat(), title=ASSIST_T, big=False, pad=False)),
        A("一份精读", "助手给队列里的一条交回来的东西：读出来的、另外查到的、可以接着问的。它跟着队列里的这一条走，不是笔记。可以带着它去深入对话，也可以看完就算了。",
          read_page(), tab="honey", title="", back="深读队列"),
        other(A("深入对话 · 在助手那边", "深入对话就是你带着这一条去助手那边：聊、让它再去查、做它那边预先配好的事（跑脚本之类）。这些 KeepEssence 都看不到，所以不管也不记，也没有「深入对话中」这种状态。有笔记存回来就留下；这一次没有，也没关系。",
                assist_chat(msgs=CHAT_DEEP), title=ASSIST_T, big=False, pad=False)),
        A("笔记", "深读队列排在最上面，每条写着精读到哪一步了。下面是笔记，按时间倒序，没有搜索，不显示寿命。", honey_list(), tab="honey", title="笔记"),
        A("笔记 · 深读队列里的各种样子", "状态只有精读的三档：等精读、精读中、精读好了。去没去深入对话不是状态，只照实写「哪天去过」「有没有笔记回来」，因为助手那边做了什么我们不知道。有笔记回来就移出队列；也可以自己移出；7 天没动静移出。",
          ripen_list(), tab="honey", title="深读队列", back="笔记"),
        A("把结果贴回来", "助手不能替你存的时候（ChatGPT 的个人套餐）：标题、一个大的粘贴框、「存成笔记」。",
          ripen_list(), tab="honey", title="深读队列", back="笔记", overlay=paste_sheet()),
        A("一篇笔记", "自己站得住：结论写全，出处只留标题和网址，记下出自哪份每日摘要。可以带附件，可以下载。",
          honey_page(), title="", back="笔记", right=ic("dl", 20)),
        A("一个条目", "原文入口、解读、以前见过类似的。只有这里能看到并改「交给哪个助手」和「活多久」。",
          bloom_detail(), tab="home", title="", back="今天"),
        A("一个条目 · 收藏", "条目是存入的，到期删除。想一直留着就在「活多久」里选「收藏」：其实就是把期限延到不过期。不用精读，也不用深入对话。",
          bloom_detail(True), tab="home", title="", back="今天"),
        A("收藏的条目", "在「今天」的全部条目里，多一个「收藏」的筛选。它们是原样留下的条目，不是笔记，所以不在「笔记」页。",
          kept_list(), tab="home", title="全部条目", back="今天"),
        A("助手设置", "第四个页签，管理档的设备才有。里面分助手、规则、设备、账户。每个助手一行：名字、是定时来的还是对话里的、在哪个产品里、干哪几步。",
          colony(), tab="set", title="助手设置"),
        A("助手设置 · 往下：通知", "只有一项，三选一，缺省是都通知。下面照实写这台设备收不收得到。对这个账户的所有设备生效。",
          colony_notify(), tab="set", title="助手设置"),
        A("通知 · 这台设备收不到", "系统里没允许就照实说，给一个去打开的入口。不弹窗，不反复问。",
          colony_notify(False), tab="set", title="助手设置"),
        A("接入一个助手 · 选产品", "助手设置里点「接入一个助手」。每一行：产品名、是哪一种助手、能做什么、一句小字。产品只写名字，不画图标。",
          bee_pick(), tab="set", title="接入一个助手", back="助手设置"),
        A("接入一个助手 · Claude", "照着做的步骤。要复制的只有接入地址：人人都一样，不是凭据。",
          guide("Claude"), tab="set", title="", back="接入一个助手"),
        A("接入一个助手 · ChatGPT", "要在电脑上接。个人套餐只能读，笔记由用户贴回来。",
          guide("ChatGPT"), tab="set", title="", back="接入一个助手"),
        A("接入一个助手 · Gemini", "限制写在步骤下面，不藏。",
          guide("Gemini"), tab="set", title="", back="接入一个助手"),
        A("接入一个助手 · Muse（待验证）", "还没验证的不编步骤，只说一句现在知道的。",
          guide("Muse"), tab="set", title="", back="接入一个助手"),
        A("接入一个助手 · 允许页", "助手在浏览器里打开 KeepEssence 的允许页：哪个产品想接入、给助手起的名字（填好了，可以改）、勾它能干哪几步、内容会被送出去的提示。没有短码。",
          bee_allow(), title="keepessence.app", big=False),
        A("登录这台设备", "App 显示一个短码，等用户在一台管理档的设备上允许。我们自己的客户端都是这个样子；助手不用短码。", login(), pad=True),
        A("助手设置 · 设备", "客户端和助手都在这里。客户端一行显示它的权限，可以改；助手显示它干哪几步。每行可以改名、撤销。", devices(6), tab="set", title="助手设置"),
        A("助手设置 · 我的月历", "给自己的月历开一个图片地址。上面是图的预览；开关、地址、换一个地址；底色、范围、带不带数字和标志。", COLSEG.format(a="", b="", c="", d="on") + '<div class="mt12">' + my_hive() + '</div>', tab="set", title="助手设置"),
        A("我的月历 · 没打开", "缺省是关的。说清楚打开后谁能看到、图里有什么。", COLSEG.format(a="", b="", c="", d="on") + '<div class="mt12">' + my_hive(False) + '</div>', tab="set", title="助手设置"),
        A("撤销一台设备", "撤销马上生效，别的设备不受影响。", devices(6), tab="set", title="助手设置", overlay=revoke_sheet()),
        A("今天 · 没有助手在干活", "不算故障，但要看得出来：多少条没被解读、最早哪天到期删除、今天为什么没有每日摘要。",
          bees_card(False) + '<div class="mt12">' + class_card(True).replace(DATE, "11月18日 周三").replace("新存入 9 条，归成 3 组：Agent 崩了以后怎么办、本地优先的存储、零碎。", "新存入 15 条，归成 5 组。") + '</div>',
          tab="home", title="今天"),
        A("今天 · 深色", "黑底白字。金只在留下来的东西上。",
          today(1), tab="home", title="今天", dark=True, right=" ", bg=hive_bg()),
        A("每日摘要 · 深色", "同一份每日摘要的深色版。", reading(), tab="class", title="", back="以前的", right=ic("share", 20), dark=True),
    ]
    return out


def share_screens():
    host = host_article()
    return [
        phone("在别的 App 里点分享", "系统分享面板里选 KeepEssence。之后不再有任何需要点的东西。", host, title="blog.example.dev", big=False, overlay=share_sheet(), pad=False),
        phone("已存入", "一闪而过，约两秒半自己消失。核心收到了才说「已存入」。", host, title="blog.example.dev", big=False, pad=False,
              overlay=hud(ic("check", 20), SAY_OK.format(T0))),
        phone("没网：排着队", "不说比事实多的话。先存在手机里，联网后自己上传。", host, title="blog.example.dev", big=False, pad=False,
              overlay=hud(ic("wifioff", 20), SAY_QUEUED)),
        phone("之前存入过", "重复的吞掉，不新增。只给一句反馈。", host, title="blog.example.dev", big=False, pad=False,
              overlay=hud(ic("check", 20), SAY_DUP)),
        phone("像密码：先问", "像密码、验证码或密钥的内容，不悄悄上传，也不悄悄丢掉。", host, title="blog.example.dev", big=False, pad=False,
              overlay='<div class="scrim"></div><div class="alert"><div class="ab"><h4>这看起来像密码、验证码或密钥，确定要存入吗？</h4><p>还没有上传，也没有留在手机上。</p></div><div class="ax"><span>不存</span><span>存入</span></div></div>'),
        phone("App 里的待上传", "离线时存入的东西排在这里，联网后自己传完就消失。在 助手设置 里能看到。",
              f'<div class="card tint"><div class="row">{ic("wifioff", 18, "warnc")}<b>3 样东西等着上传</b></div><p class="sm mt4" style="color:var(--ink)">现在没有网络。联网后自动上传，不用管它。</p></div>'
              f'<div class="lst mt8">' + "".join(
                  f'<div class="li" style="align-items:center"><span class="thumb">{ic(i, 20)}</span><div class="col sp"><span class="ti">{t}</span><span class="xs mt4">{w} · 待上传</span></div></div>'
                  for i, t, w in [("link", T0, "20:51 从浏览器分享"), ("img", "截屏 11-21 20.58", "20:58 轻点背面三下"), ("text", "一段摘抄", "21:01 从别的 App 分享")]) + '</div>',
              title="待上传", back="助手设置"),
    ]


def shortcut_screens():
    sp = springboard()
    return [
        phone("轻点背面两下：存入到 KeepEssence", "不离开正在用的 App。传完一条通知说结果。", host_article(), title="blog.example.dev", big=False, pad=False,
              overlay=notif("KeepEssence", SAY_OK.format(T0) + "（含截屏）")),
        phone("轻点背面三下：截屏到 KeepEssence", "没有网页就只存入截屏。", sp, pad=False, bare=True,
              overlay=notif("KeepEssence", SAY_OK.format("截屏 11-21 21.04"))),
        phone("没存上 / 之前存入过", "没存上要说原因；重复的只说一句。", host_article(), title="blog.example.dev", big=False, pad=False,
              overlay=notif("KeepEssence", SAY_FAIL) + notif("KeepEssence", SAY_DUP, "2 分钟前")),
        phone("第一次运行", "照实告诉用户会被问几次、问什么。这一次只是设置，不存入任何东西。", sp, pad=False, bare=True,
              overlay='<div class="scrim"></div><div class="alert" style="width:290px"><div class="ab" style="text-align:left"><h4 style="text-align:center">KeepEssence：第一次设置</h4>'
                      '<p>接下来 iPhone 会问大约 5 次「允许…吗？」<br>每次都选「始终允许」。<br>它会把要发送的内容列出来给你看，这是 iPhone 的做法。<br>中间会显示一个短码：去 KeepEssence 里核对它，点「允许」，再回到这里。</p></div>'
                      '<div class="ax"><span style="font-weight:600">好</span></div></div>'),
    ]
