"""Round 2: product-specific states, the four main flows, and the component / style board."""
from mocklib import kept, ic, logo, cell, life, bee_chip, phone, webapp, board, flow, grid, hive, empty, skel, wordmark, tokens
from content import *
import screens_iphone as I
import screens_web as Wb

HOME_T = "今天"
GO = '<span class="btn quiet sm">去做</span>'


def last_class(date="11月20日 周五", n="12 条，3 条值得深读"):
    return (f'<div class="card"><div class="row"><span class="xs">最近一份每日摘要</span><span class="sp"></span>{READ}</div>'
            f'<div class="h2 mt4">每日摘要 · {date}</div><p class="sm mt4">存入了 {n}。</p>'
            f'<div class="row mt12"><span class="btn quiet sm">再读一遍</span></div></div>')


# ------------------------------------------------------------------ states
HONEY_EMPTY = "在每日摘要的某一条上点「深入对话」，和助手聊出来的东西会留在这里。"


def st_no_class_yet():
    return (f'<div class="card"><div class="row">{ic("clock", 18, "deep")}<b>今晚的每日摘要还没出</b></div>'
            f'<p class="sm mt4" style="color:var(--ink)">21:00 之后，阿读来汇总的时候出。今天存入的 9 条里已经有 7 条被解读。</p></div>'
            f'<div class="mt12">{last_class()}</div><div class="mt12">{I.bees_card()}</div>')


def st_first_day():
    ways = "".join(f'<div class="kv"><span class="row" style="color:var(--ink)">{ic(i, 18, "deep")}{t}</span>{ic("chev", 16, "faint")}</div>'
                   for i, t in [("device", "装 iPhone 快捷指令"), ("img", "装浏览器扩展"), ("bee", "接入一个助手")])
    return (empty("还没有条目", "在任何地方把看到的东西存入进来。助手读完，每天晚上归成一份每日摘要。")
            + f'<div class="card mt20" style="padding:2px 16px">{ways}</div>')


def st_class_empty():
    return empty("还没有每日摘要", "有条目被解读之后，当天 21:00 以后出第一份。没有条目的日子不出。")


def st_honey_empty():
    return empty("还没有笔记", HONEY_EMPTY)


def st_loading():
    row = lambda: (f'<div class="li" style="align-items:center"><div class="col sp g6">{skel("62%", 16)}{skel("38%", 11)}</div></div>')
    return '<div class="lst">' + row() * 7 + '</div>'


def st_error():
    return (f'<div class="card bad"><div class="row">{ic("wifioff", 18, "badc")}<b>连不上 KeepEssence</b></div>'
            f'<p class="sm mt4" style="color:var(--ink)">下面是上次打开时的内容，可能不是最新的。</p>'
            f'<div class="row mt8"><span class="btn quiet sm">再试一次</span></div></div>'
            f'<div class="lab">上次打开时的内容</div><div class="lst">' + "".join(
                f'<div class="li" style="align-items:center"><div class="col sp"><span class="ti">每日摘要 · {d}</span><span class="xs mt4">{s}</span></div>{ic("chev", 16, "faint")}</div>'
                for d, s, r in CLASSES[1:6]) + '</div>')


def st_wilting():
    soon = [("img", "手冲咖啡粉水比对照表", "来自 Mac", 2, 3, "阿读"), ("file", "季度账单.pdf", "来自 iPhone · 分享", 2, 1, "阿读"),
            ("link", "一篇没来得及被读的长文", "essay.example.net", 1, 2, "阿读")]
    return (f'<div class="row"><span class="sm">未到期的条目 · 23 条</span><span class="sp"></span><span class="seg"><span>今天</span><span class="on">全部</span><span>收藏</span></span></div>'
            f'<div class="lab" style="margin-top:12px">3 天内到期删除</div><div class="lst">{"".join(bloom_row(b) for b in soon)}</div>'
            f'<div class="lab">之后</div><div class="lst">{"".join(bloom_row(b) for b in BLOOMS[4:7])}</div>')


def st_wilting_detail():
    return (f'<div class="row g6"><span class="thumb">{ic("link", 20)}</span><div class="col"><span class="xs">essay.example.net · 10月22日 存入自 iPhone 快捷指令</span>'
            f'<span class="lk sm">打开原文</span></div></div>'
            f'<div class="h1 mt12" style="font-size:22px">一篇没来得及被读的长文</div>'
            f'<div class="card bad mt12"><div class="row">{ic("clock", 18, "badc")}<b>2 天后删除，还没有被解读</b></div>'
            f'<p class="sm mt4" style="color:var(--ink)">阿读 3 天没来了。到期时没被解读也照样删除，不会进每日摘要。</p></div>'
            f'<div class="lab">怎么处理这个条目</div><div class="card" style="padding:2px 16px">'
            f'<div class="kv"><span>交给哪个助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>活多久（天）</span>{life_pick(30)}</div>'
            f'<div class="kv"><span>到期删除</span><span>{life(2, 30)}</span></div></div>'
            f'<p class="xs mt8">想留久一点就改「活多久」；想一直留着就选「收藏」。不改就让它到期删除，不用做任何事。</p>')


def st_ripen_stuck():
    rq = lambda title, state, extra: ripen_req(title, SIPPER, state, extra)
    return ('<div class="col g12">'
            + rq(DIG[2], "wait", '<p class="sm mt4"><span class="badc">阿读 3 天没来了。</span>再过 4 天还没有动静，这一条移出队列。</p>'
                 f'<div class="row mt12"><span class="btn quiet sm">换一个助手</span><span class="sp"></span><span class="lk sm">移出队列</span></div>')
            + rq(DIG[1], "ready", '<p class="sm mt4">阿读读好了，等你看。还剩 2 天，没动静就移出。</p>'
                 f'<div class="row mt12"><span class="btn sm">{ic("chat", 15)}去深入对话</span><span class="lk sm">看精读</span></div>')
            + rq("墨水屏上的排版要不要自己调字重", "void", '<p class="sm mt4">7 天没有助手来领。收藏的条目已经放开，照常到期删除。</p>'
                 f'<div class="row mt8"><span class="lk sm">重新排入队列</span></div>')
            + '</div>')


def st_authorizing():
    return (f'<div class="col" style="align-items:center;padding-top:110px;text-align:center">{logo("simple", 64)}</div>'
            f'<div class="mt8">{join_wait("iPhone · App")}</div><div class="col mt16" style="align-items:center"><span class="spin"></span></div>')


def web_first_day():
    steps = [("check", "登录", "做完了", True), ("bee", "接入一个助手", "没有助手，条目只会等到到期删除。", False),
             ("device", "装一个存入的入口", "iPhone 快捷指令或浏览器扩展。", False), ("book", "等第一份每日摘要", "有条目被解读的那天晚上 21:00 以后。", False)]
    lis = "".join(f'<div class="kv"><span class="row" style="color:var(--ink)">'
                  f'<span class="thumb" style="width:34px;height:34px;{"background:var(--okbg);color:var(--ok)" if d else ""}">{ic(i, 18)}</span>'
                  f'<span class="col"><b>{t}</b><span class="xs">{s}</span></span></span>{"" if d else GO}</div>' for i, t, s, d in steps)
    return (f'<div class="pane read"><div class="inner" style="max-width:620px">{empty("还没有条目", "在任何地方把看到的东西存入进来。助手读完，每天晚上归成一份每日摘要。")}'
            f'<div class="card mt28" style="padding:6px 18px">{lis}</div></div></div>')


def web_error():
    return (f'<div class="pane side">' + "".join(f'<div class="pick">{skel("70%", 15)}<span style="height:6px"></span>{skel("40%", 10)}</div>' for _ in range(8)) + '</div>'
            f'<div class="pane read"><div class="inner"><div class="card bad"><div class="row">{ic("warn", 20, "badc")}<b style="font-size:16px">这份每日摘要没读出来</b></div>'
            f'<p class="mt8">连不上 KeepEssence。检查网络后再试一次。你的东西都还在。</p>'
            f'<div class="row mt12"><span class="btn quiet sm">再试一次</span></div></div></div></div>')


def states():
    P = phone
    phones = [
        P("今天还没有每日摘要", "21:00 之前的今天。说清楚什么时候出、由谁出，已经解读了多少。", st_no_class_yet(), tab="home", title=HOME_T),
        P("第一天：什么都还没有", "空状态不画插图，不用 logo。直接给出三件该做的事。", st_first_day(), tab="home", title=HOME_T),
        P("每日摘要 · 空", "只写一句话。没有条目的日子不出每日摘要。", st_class_empty(), tab="class", title="每日摘要"),
        P("笔记 · 空", "告诉用户笔记从哪来：只有他自己去深入对话、存回来才有。", st_honey_empty(), tab="honey", title="笔记"),
        P("加载中", "骨架屏，不转圈。", st_loading(), tab="class", title="每日摘要"),
        P("连不上", "先说事实，再给上次的内容，标明可能不是最新的。", st_error(), tab="class", title="每日摘要"),
        P("条目即将到期删除", "「全部」里把 3 天内到期删除的排在最前，用红色的寿命条。不发通知。", st_wilting(), title="还在等助手的条目", back="今天"),
        P("一条快到期删除、还没被读的条目", "没有助手来，它到期照样删除。想留就改「活多久」，不改就什么都不用做。", st_wilting_detail(), tab="home", title="", back="今天"),
        P("深读队列：没人来精读、快移出、已移出", "队列里的一条 7 天没有任何动静就移出：没有助手来精读，或者精读好了你一直没去。", st_ripen_stuck(), tab="honey", title="深读队列", back="笔记"),
        P("等着被允许", "App 显示短码，等用户在 KeepEssence 里点「允许」。只有我们自己的客户端这样；助手不用短码。", st_authorizing(), pad=True),
        P("没有助手在干活", "条目在等，最早的几天后删除，今天为什么没有每日摘要。", I.bees_card(False) + '<div class="mt12">' + last_class("11月18日 周三", "15 条，归成 5 组") + '</div>', tab="home", title=HOME_T),
        P("离线时存入的条目在排队", "联网后自己上传，传完就从这里消失。", _queue_body(), title="待上传", back="助手设置"),
    ]
    webs = [
        webapp("今天 · 第一天", "没有条目、没有助手时，今天就是一张四步的清单。做完一步划掉一步。", "home", web_first_day(), "今天", bees_ok=False),
        webapp("每日摘要 · 没读出来", "列表是骨架，正文说清楚出了什么事、东西还在不在。", "class", web_error(), "每日摘要"),
    ]
    return grid(phones, 6) + '<div style="height:84px"></div>' + grid(webs, 2)


def _queue_body():
    items = [("link", T0, "20:51 从浏览器分享"), ("img", "截屏 11-21 20.58", "20:58 轻点背面三下"), ("text", "一段摘抄", "21:01 从别的 App 分享")]
    return (f'<div class="card tint"><div class="row">{ic("wifioff", 18, "warnc")}<b>3 样东西等着上传</b></div><p class="sm mt4" style="color:var(--ink)">现在没有网络。联网后自动上传，不用管它。</p></div>'
            f'<div class="lst mt8">' + "".join(
                f'<div class="li" style="align-items:center"><span class="thumb">{ic(i, 20)}</span><div class="col sp"><span class="ti">{t}</span><span class="xs mt4">{w} · 待上传</span></div></div>'
                for i, t, w in items) + '</div>')


# ------------------------------------------------------------------ flows
NEW = ("link", "把定时任务做成幂等的七种写法", "blog.example.dev · 刚刚存入自分享", 0, 30, None)


def blooms_with_new(state):
    b = list(NEW)
    b[3] = state
    b[5] = "阿读" if state else None
    rest = [x for x in BLOOMS if x[1] != NEW[1]][:5]
    return (f'<div class="row"><span class="sm">未到期的条目 · 24 条</span><span class="sp"></span><span class="seg"><span class="on">今天</span><span>全部</span><span>收藏</span></span></div>'
            f'<div class="lst mt4"><div class="newmark">{bloom_row(tuple(b))}</div>{"".join(bloom_row(x) for x in rest)}</div>')


def read_done():
    return I.reading_end(True)


def today_flow(st):
    f = FLOWERS[0]
    if st < 2:
        return (sbar_narrow() + f'<div class="lab">还在等助手的条目</div><div class="newmark">{stage1(f, st)}</div>'
                f'<div class="lab">今天的解读 · 新的在前</div>{drop(FLOWERS[3], pts=2)}')
    return sbar_narrow() + f'<div class="lab">今天的解读 · 新的在前</div><div class="newmark">{drop(f)}</div><div class="lab">处理过的 · 1 个</div><div class="fold" style="padding:2px 14px">{drop_done(FLOWERS[4], "看过了")}</div>'


def honey_new():
    rows = "".join(f'<div class="li">{note_thumb()}<div class="col sp">'
                   f'<span class="ti">{t}</span><span class="xs mt4">{d} · {f}{(" · " + a) if a else ""}</span></div></div>' for t, d, f, a in HONEY[:3])
    new = (f'<div class="newmark"><div class="li">{note_thumb()}<div class="col sp">'
           f'<span class="ti">{DIG_T}</span><span class="xs mt4">刚刚 · 出自 11月21日 每日摘要 · 第 1 条</span></div>'
           f'<span class="pill honey">新</span></div></div>')
    return f'<p class="sm">深入对话的产出。按时间排，一直留着。</p><div class="lst mt4">{new}{rows}</div>'


def colony_first(came=False):
    return ('<div class="lab" style="margin-top:0">助手</div><div class="card" style="padding:2px 16px">'
            + bee_row("阿探", "分派助手 · 我们提供，免费", "刚刚来过", "ok")
            + bee_row("阿读", ALL3, "刚刚来过" if came else "还没来过", "ok" if came else "", REV, product=SELF)
            + f'</div>{I.ADD_BEE}'
            f'<div class="lab">谁做哪一步</div><div class="card" style="padding:2px 16px">'
            f'<div class="kv"><span>缺省解读助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>汇总助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>精读助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>缺省精读助手</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div></div>'
            + ('' if came else f'<div class="card tint mt16"><div class="row top">{ic("clock", 18, "warnc")}<p class="sm" style="color:var(--ink)"><b>阿读已经接入，还没来过。</b>它第一次来取活时这里的点会变成实心。</p></div></div>')
            + '<div class="lab">规则 · 写给分派助手的话</div><div class="inp area faint" style="min-height:60px">还没写。不写就全部交给阿读，活 30 天。</div>')


def home_first_bee():
    return (f'<div class="card"><div class="row"><span class="dot ok"></span><b>阿读来了</b><span class="sp"></span><span class="xs">刚刚</span></div>'
            f'<p class="sm mt4" style="color:var(--ink)">它领走了 5 个条目，正在解读。今晚 21:00 以后出第一份每日摘要。</p></div>'
            f'<div class="mt12">{empty("第一份每日摘要今晚出", "在那之前不用做任何事。")}</div>')


def flows():
    P = phone
    host = I.host_article()
    f1 = flow("存入", "在手机上从别的 App 分享一个条目进来。用户只做第 1 步；解读一交回就通知他一句，他在「今天」就能读、能处理，不必等每日摘要。", [
        (P("在别的 App 里点分享", "选 KeepEssence。", host, title="blog.example.dev", big=False, overlay=I.share_sheet(), pad=False), "一个动作"),
        (P("已存入", "一句话，自己消失。用户继续看文章。", host, title="blog.example.dev", big=False, pad=False, overlay=I.hud(ic("check", 20), SAY_OK.format(T0))), "核心收到"),
        (P("今天：条目出现了", "只有图标、标题、来源、时间。阿探（分派助手）还没看它。", today_flow(0), tab="home", title=HOME_T), "阿探分派"),
        (P("分派后", "同一张卡多一行：交给阿读，还能活 30 天。", today_flow(1), tab="home", title=HOME_T), "阿读来取活"),
        (P("解读好了，通知一句", "用户这时多半不在 App 里。只有判定和标题。", I.springboard(), pad=False, bare=True, overlay=I.notif(*NOTE_ONE)), "点通知"),
        (P("解读出现了", "固定四行。以前见过类似的就在解读上。这时就能读，也能点深入对话、不感兴趣、看过了。", today_flow(2), tab="home", title=HOME_T), "21:00 汇总"),
        (P("进了今晚的每日摘要", "没处理过、判定是值得深读的，进每日摘要的重点部分。", I.reading(), tab="class", title="", back="以前的", right=ic("share", 20)), ""),
    ])
    f2 = flow("读", "打开今晚的每日摘要：扫一眼总结，看值得深读的，其余的不用管，带着睡前一问去睡。", [
        (P("今天：每日摘要页签上有个点", "今晚的每日摘要出了。", I.today(1), tab="home", title=HOME_T), "点「每日摘要」"),
        (P("总结和值得深读的", "总结不抢眼。重点是这几张卡。", I.reading(), tab="class", title="", back="以前的", right=ic("share", 20)), "往下读"),
        (P("其余的、睡前一问", "其余的一行一条，可以挽回。", I.reading_end(), tab="class", title="", back="以前的", right=ic("share", 20)), "点「读了，晚安」"),
        (P("标好了", "按钮变安静。只是标记，不触发任何处理。", read_done(), tab="class", title="", back="以前的", right=ic("share", 20)), "返回"),
        (P("回到今天", "页签上的点没了。没有别的事要做。", I.today_empty(), tab="home", title=HOME_T, unread=False), ""),
    ])
    O = lambda name, note, body: I.other(P(name, note, body, title=I.ASSIST_T, big=False, pad=False))
    went = (f'<p class="sm mt4">今天 23:10 去过，{RIPENER}取过这一条。还没有笔记存回来。</p><div class="row mt12"><span class="btn quiet sm">{ic("chat", 15)}再去深入对话</span>'
            f'<span class="sp"></span><span class="lk sm">移出队列</span></div>')
    dig_ends = (f'<div class="lab" style="margin-top:0">没有笔记回来 · 它还在队列里</div>' + ripen_req(DIG_T, SIPPER, "ready", went)
                + f'<div class="lab">有笔记回来 · 进了笔记，移出队列</div><div class="newmark"><div class="li">{note_thumb()}<div class="col sp"><span class="ti">{DIG_T}</span><span class="xs mt4">刚刚 · 出自 11月21日 每日摘要 · 第 1 条</span></div></div></div>')
    f3r = flow("排入队列：先精读，再深入对话", "加入深读队列的条目，助手趁它排着先精读，不用你在场。你有空了带着精读去助手那边深入对话：聊、让它再查、做它那边的事。那边做了什么我们看不到，所以只认两件事：你去过，和有没有笔记回来。", [
        (P("往右滑：加入深读队列", "不用选，不离开这一页。", I.reading_swipe(), tab="class", title="", back="以前的", right=ic("share", 20)), "松手"),
        (P("排进去了：等精读", "在「笔记」页最上面。", I.honey_list(True), tab="honey", title="笔记"), "阿读来取活，读完交回"),
        (P("精读好了", "可以看精读，也可以直接去深入对话。", I.ripen_list(), tab="honey", title="深读队列", back="笔记"), "点「看精读」"),
        (P("一份精读", "读出来的、另外查到的、可以接着问的。不是笔记。", read_page(), tab="honey", title="", back="深读队列"), "点「去深入对话」"),
        (O("深入对话：在助手那边", "不是 KeepEssence 的界面。聊、再去查、跑它那边的脚本，我们都看不到。", assist_chat(msgs=CHAT_DEEP)), "回到 KeepEssence"),
        (P("回来之后", "没有「深入对话中」，也没有「结束」。没有笔记回来，它就还在队列里，写着你去过；有笔记回来，笔记留下，这一条移出队列。", dig_ends, tab="honey", title="笔记"), ""),
    ])
    f3 = flow("现在去深入对话（从产品发起）", "不排队、不等精读：在一条上点深入对话，选一个助手，去它那边聊，说「存成笔记」，笔记回来。对话在助手那边，不进核心。", [
        (P("在一条上点「深入对话」", "解读上和每日摘要的一条上都有。", I.reading(), title="", back="每日摘要", right=ic("share", 20)), "点深入对话"),
        (P("现在去深入对话，用谁", "面板顶上两个选项：排入队列先精读，或者现在去深入对话。缺省的那个已选好，可以换。", I.reading(), title="", back="每日摘要", overlay=I.dig_sheet("link")), "点「去 Claude 深入对话」"),
        (O("到了 Claude 那边", "不是 KeepEssence 的界面。新对话，开场话已经填好。", assist_chat(0, 0, draft=OPENING)), "按发送"),
        (O("在助手那边深入对话", "助手从 KeepEssence 取到这一条和相关的上下文。", assist_chat(0, 6)), "问够了"),
        (O("说「存成笔记」", "助手把结果存回 KeepEssence。", assist_chat(2)), "回到 KeepEssence"),
        (P("笔记出现", "最后只留这一篇。", honey_new(), tab="honey", title="笔记"), ""),
    ])
    ASK = "深入对话今天每日摘要里讲租约的那条"
    f3b = flow("深入对话（从助手那边发起）", "不用先打开 KeepEssence。在已经接入的助手里直接说要哪一条。", [
        (O(f"在助手里说「{ASK}」", "不是 KeepEssence 的界面。", assist_chat(0, 0, draft=ASK)), "按发送"),
        (O("助手从 KeepEssence 取到这一条", "它自己去找是哪一条，取回内容和相关的上下文。", assist_chat(0, 2, first=ASK)), "接着深入对话"),
        (O("聊", "", assist_chat(0, 6, first=ASK)), "说「存成笔记」"),
        (O("存成笔记", "", assist_chat(2)), "回到 KeepEssence"),
        (P("笔记出现", "和从产品发起的结果一样。", honey_new(), tab="honey", title="笔记"), ""),
    ])
    f4 = flow("第一次使用", "接入这台设备用短码：App 显示，在 KeepEssence 里点允许。接入一个助手不用短码：选产品，把接入地址贴到它那边，在允许页点允许。", [
        (P("App 显示短码", "", I.login(), pad=True), "去 KeepEssence"),
        (P("允许这台设备", "核对短码，点一次。", I.allow(), title="keepessence.app", big=False), "回到 App"),
        (P("今天：什么都还没有", "三件该做的事，先接助手。", st_first_day(), tab="home", title=HOME_T), "点「接入一个助手」"),
        (P("选产品", "要有助手读条目，得接一个定时来的。", I.bee_pick(), tab="set", title="接入一个助手", back="助手设置"), f"选「{SELF}」"),
        (P("照步骤做", "复制接入地址，贴到它那边。", guide(SELF), tab="set", title="", back="接入一个助手"), "它打开允许页"),
        (P("允许这个助手", "起名字，勾它干哪几步。提示内容会被送到助手那边。没有短码。", I.bee_allow(SELF, SIPPER, ALL3), title="keepessence.app", big=False), "点允许"),
        (P("助手设置：等它第一次来", "灰点：接入了，还没来过。", colony_first(False), tab="set", title="助手设置"), "阿读来取活"),
        (P("助手设置：来过了", "点亮了。从这一刻起条目有人读。", colony_first(True), tab="set", title="助手设置"), "回今天"),
        (P("今天：开始干活", "告诉用户第一份每日摘要什么时候出。", home_first_bee(), tab="home", title=HOME_T), ""),
    ])
    return f1 + f2 + f3r + f3 + f3b + f4


# ------------------------------------------------------------------ component / style board
def perms():
    import screens_web as W
    P = phone
    sheet = lambda inner: f'<div class="scrim"></div><div class="sheet" style="text-align:center;padding-top:22px">{inner}</div>'
    pick = (f'<div class="h2" style="text-align:left">「墨水屏阅读器」的权限</div>{tier_pick(2, 1)}'
            f'<p class="xs mt12" style="text-align:left">改了马上生效。调到「只存入」后它就看不到任何内容了。</p>'
            f'<div class="row mt16"><span class="btn ghost sp">取消</span><span class="btn sp">好</span></div>')
    frames = [
        P("管理档的手机", "四个页签。今日状态可以点进助手设置。", I.today(1), tab="home", title="今天", right=" ", bg=hive_bg()),
        P("读档的手机", "同一页，只有三个页签：没有「助手设置」。今日状态只读。没有权限的入口不显示，不是显示了点不动。", I.today(1), tab="home", title="今天", right=" ", reader=True, bg=hive_bg()),
        P("读档 · 一个条目", "能看原文、解读、以前见过类似的；「交给谁」「活多久」不出现。", I.bloom_detail().split('<div class="lab">怎么处理这个条目</div>')[0], tab="home", title="", back="今天", reader=True),
        P("允许一个客户端：选权限", "缺省选中它请求的那一档。可以调低；比它请求的高的那一档不给选。", I.colony(), tab="set", title="助手设置",
          overlay=sheet(join_allow("墨水屏阅读器", "客户端", "", tier=1))),
        P("允许时调低", "它请求管理，只给读。", I.colony(), tab="set", title="助手设置", overlay=sheet(join_allow("iPad · App", "客户端", "", tier=2, chosen=1))),
        P("允许一个助手：选它干哪几步", "助手不用三档，也不用短码。定时来的助手四步都能做，这里去掉了深入对话。对话里的助手只有深入对话一项。",
          I.bee_allow("Muse", SIPPER, [("解读", True), ("汇总", True), ("精读", True), ("深入对话", False)]), title="keepessence.app", big=False),
        P("在设备里改权限", "点一行里的权限就能改，马上生效。", I.devices(6), tab="set", title="助手设置", overlay=sheet(pick)),
        P("最后一台管理档设备", "至少留一台管理档：最后一台不能降档，也不能撤销。", I.COLSEG.format(a="", b="", c="on", d="") + '<div class="mt12">' + last_mgr_note() + f'</div><div class="lst mt4">{device_rows(4)}</div>', tab="set", title="助手设置"),
        webapp("读档的网页", "左栏只有今天、每日摘要、笔记。和手机的三个页签一样。", "home", W.home(), "今天", reader=True),
    ]
    return grid(frames, 5)


def components():
    def sw(name, hexv, use, dark=False):
        return f'<div class="sw"><i style="background:{hexv}"></i><b>{name}</b><span class="spec">{hexv}</span><span class="xs">{use}</span></div>'

    L, D = tokens(), tokens(True)
    colors = (sw("金", L["gold"], "只给留下来的：笔记、值得深读、没读的每日摘要") + sw("黑", L["ink"], "正文、按钮底、链接、图标")
              + sw("纸", L["bg"], "页面底") + sw("卡", L["card"], "卡片底") + sw("线", L["line"], "分隔线")
              + sw("填", L["fill"], "安静的底") + sw("次", L["mut"], "次要文字") + sw("淡", L["faint"], "说明文字，最浅的字")
              + sw("坏", L["bad"], "唯一的功能色：即将到期删除、没有助手、出错"))
    dcolors = (sw("夜", D["bg"], "页面底") + sw("夜卡", D["card"], "卡片底") + sw("夜填", D["fill"], "安静的底") + sw("夜线", D["line"], "分隔线")
               + sw("夜字", D["ink"], "正文") + sw("夜次", D["mut"], "次要文字") + sw("夜淡", D["faint"], "说明文字")
               + sw("金", D["gold"], "只给留下来的；深色里可以当字") + sw("坏", D["bad"], ""))
    type_ = "".join(f'<div class="row" style="gap:20px;align-items:baseline;padding:7px 0;border-bottom:1px solid var(--line)"><span class="spec" style="width:150px">{spec}</span><span style="{css}">{txt}</span></div>'
                    for spec, css, txt in [
                        ("大标题 32 / 700", "font:700 32px/1.15 var(--head)", "每日摘要"),
                        ("标题 26 / 600", "font:600 26px/1.25 var(--head)", "每日摘要 · 11月21日 周六"),
                        ("小标题 20 / 600", "font:600 20px/1.3 var(--head)", "Agent 崩了以后怎么办"),
                        ("一条的标题 17 / 600", "font:600 17px/1.35 var(--head)", "任务队列的认领和租约"),
                        ("正文 15", "font-size:15px", "知道就行。结论是租约要短、续租要便宜。"),
                        ("次要 13", "font-size:13px;color:var(--mut)", "存入了 9 条，2 条值得深读"),
                        ("说明 12", "font-size:12px;color:var(--faint)", "阿读 · 21:02 汇总")])
    space = "".join(f'<div class="col g4" style="align-items:center"><i style="display:block;width:{n}px;height:{n}px;background:var(--ink)"></i><span class="spec">{n}</span></div>' for n in (4, 8, 12, 16, 20, 28))
    radius = "".join(f'<div class="col g4" style="align-items:center"><i style="display:block;width:64px;height:44px;background:var(--fill);border:1px solid var(--line);border-radius:{r}px"></i><span class="spec">{r} {u}</span></div>'
                     for r, u in [(0, "图标、标记"), (4, "标签"), (6, "按钮、卡片、输入框"), (10, "底部面板")])
    buttons = (f'<span class="btn">{ic("check", 18)}读了</span><span class="btn sm">读每日摘要</span><span class="btn quiet sm">{ic("chat", 15)}深入对话</span>'
               f'<span class="btn ghost">取消</span><span class="btn ghost sm">{ic("dl", 15)}导出</span><span class="lk sm">撤销</span><span class="mini">{ic("nope", 15)}不感兴趣</span>')
    marks = (f'<div class="col g6"><div class="row">{cell(0)}<span>等分派</span></div><div class="row">{cell(1)}<span>等解读</span></div><div class="row">{cell(2)}<span>已解读</span></div><div class="row">{cell(3)}<span>值得深读</span></div><div class="row">{cell(4)}<span>留成笔记</span></div></div>'
             f'<div class="col g6">{life(30, 30)}{life(12, 30)}{life(3, 30)}{life(1, 30)}{kept()}</div>'
             f'<div class="col g6">{"".join(ripen_pill(k) for k in RIPEN)}</div>'
             f'<div class="col g6"><span class="row"><span class="dot ok"></span>助手来过</span><span class="row"><span class="dot warn"></span>有一阵没来</span><span class="row"><span class="dot bad"></span>很久没来</span><span class="row"><span class="dot"></span>还没来过</span></div>'
             f'<div class="col g6">{UNREAD}{READ}{bee_chip("阿读")}</div>')
    row_ = bloom_row(BLOOMS[5])
    card_ = I.class_card()
    req_ = ripen_req(DIG[1], "阿读", "prep", '<p class="sm mt4">阿读 6 分钟前领走了，正在读原文、查相关的。</p>')
    says = "".join(f'<div class="hud" style="position:static;margin:0">{i}<span>{t}</span></div>' for i, t in
                   [(ic("check", 20), SAY_OK.format("一个条目的标题")), (ic("check", 20), SAY_DUP), (ic("wifioff", 20), SAY_QUEUED), (ic("warn", 20), SAY_FAIL)])
    notice = (f'<div class="card tint" style="width:330px"><div class="row top">{ic("warn", 18, "warnc")}<p class="sm" style="color:var(--ink)"><b>提醒。</b>需要用户知道，但不要他马上做什么。</p></div></div>'
              f'<div class="card bad" style="width:330px"><div class="row">{ic("warn", 18, "badc")}<b>没有助手在干活</b></div><p class="sm mt4" style="color:var(--ink)">只用于会丢东西的事。</p></div>'
              f'<div class="card flat" style="width:330px"><div class="xs">以前见过类似的</div><p class="sm mt4" style="color:var(--ink)">安静的信息，不要求任何动作。</p></div>')
    hives = (f'<div class="col g10" style="width:100%">{hive_legend()}</div>'
             + "".join(f'<div class="col" style="align-items:center;gap:8px">{hive(d, 13)}<span class="xs">{t}</span></div>' for d, t in
                       [(MONTH_NEW, "刚开始用"), (MONTH, "用了半个多月"), (MONTH_BUSY, "用得很勤"), (MONTH_NONE, "整月没有条目")])
             + f'<div class="card" style="width:330px;position:relative;overflow:hidden;height:150px"><div style="position:absolute;right:-6px;top:8px;opacity:.55">{hive(MONTH, 11)}</div>'
               f'<div class="h1" style="position:relative">今天</div><div class="mt8" style="position:relative">{sbar_narrow()}</div><p class="xs mt12" style="position:relative">作背景：只在「今天」页，偏右上，淡，今日状态叠在上面</p></div>'
             + f'<div class="card" style="width:400px">{hive_page()}</div>')
    logos = (f'<div class="col g6" style="align-items:center">{logo("color", 72)}<span class="xs">标准版 ≥ 64</span></div>'
             f'<div class="col g6" style="align-items:center">{logo("simple", 40)}<span class="xs">简化版 24–64</span></div>'
             f'<div class="col g6" style="align-items:center">{logo("16", 20)}<span class="xs">16 像素版</span></div>'
             f'<div class="col g6" style="align-items:center">{logo("mono", 40)}<span class="xs">单色（菜单栏）</span></div>'
             f'<div class="col g6" style="align-items:center"><span style="width:64px;height:64px;border-radius:14px;overflow:hidden;display:block">{logo("app", 64)}</span><span class="xs">App 图标</span></div>'
             f'<div class="col g6" style="align-items:center">{wordmark(34)}<span class="xs">字标 Inter 700</span></div>')
    dark = (f'<div class="darkbox"><div class="ui dark" style="height:auto;background:none;flex-direction:row;gap:16px;align-items:center;flex-wrap:wrap">'
            f'<span class="btn sm">读每日摘要</span><span class="btn quiet sm">{ic("chat", 15)}深入对话</span><span class="lk sm">撤销</span>'
            f'<span class="pill ok">精读好了</span><span class="pill warn">精读中</span>{life(12, 30)}{life(2, 30)}{cell(0)}{cell(1)}{cell(2)}{cell(3)}{cell(4)}{bee_chip("阿读")}'
            f'{verdict_pill(0)}{verdict_pill(1)}{verdict_pill(2)}{UNREAD}<span class="sm">金只在留下来的东西上</span></div></div>')

    def blk(t, inner, cls="wrap"):
        return f'<div class="blk"><div class="t">{t}</div><div class="{cls}">{inner}</div></div>'
    left = (f'<div class="bh">颜色、字、间距</div><div class="bsub">黑、白、灰，加一个金。金只给留下来的东西：不做按钮底，不在浅底上写字。所有的字和它的底至少 4.5:1。</div>'
            + blk("颜色 · 浅色", colors) + blk("颜色 · 深色", dcolors) + blk("字号层级 · 标题和正文都用无衬线，靠粗细和大小分层", type_, "")
            + blk("间距 · 4 的倍数", space) + blk("圆角 · 小，或者没有", radius) + blk("LOGO · 直接取自 brand/logo，不改形状和颜色", logos))
    right = (f'<div class="bh">组件</div><div class="bsub">各端的屏幕都由这些拼成。主要动作只有「读了」和「深入对话」，其余都是安静的。</div>'
             + blk("按钮 · 主要动作黑底白字，深色里反过来", buttons) + blk("状态标识 · 条目的状态（照 logo：一堆形状进来，留下一个金点）、寿命、深读队列里一条的状态（只有精读的三档，加没做精读和已移出）、助手的状态", marks)
             + blk("列表行 · 条目", f'<div style="width:400px">{row_}</div>')
             + blk("列表行 · 助手：名字、哪一种（定时来的 / 对话里的）、在哪个产品里、做什么、上次什么时候来", f'<div class="card" style="width:400px;padding:2px 16px">{bee_row("阿读", ALL3, "4 分钟前来过")}{bee_row("阿深", "深入对话", "2 小时前来过", "warn")}</div>')
             + blk("接入一个助手 · 产品的一行：名字、哪一种、能做什么、一句小字。产品只写名字，不画图标", f'<div style="width:400px">{product_row(PRODUCTS[0])}{product_row(PRODUCTS[3], True)}</div>')
             + blk("接入一个助手 · 步骤：接入地址（唯一要复制的）加编号的几步；还没验证的只写一句", f'<div class="card" style="width:400px">{guide("Claude")}</div><div class="card" style="width:340px">{guide("Muse")}</div>')
             + blk("允许页 · 助手：没有短码。名字可以改，勾它干哪几步；对话里的只有深入对话", f'<div class="card" style="width:360px;text-align:center">{join_allow(RIPENER, K_CHAT, "", steps="深入对话", warn=True, product="Claude")}</div><div class="card" style="width:360px;text-align:center">{join_allow(SIPPER, K_SCHED, "", steps=ALL3, warn=True, product="Muse")}</div>')
             + blk("深入对话的面板 · 两个选项：排入队列先精读（只有定时来的助手能精读）；现在去深入对话（能用链接打开的、要贴开场话的）", "".join(f'<div class="card" style="width:340px">{dig_pick(m)}</div>' for m in ("read", "link", "copy")))
             + blk("一份精读 · 助手给队列里的一条交回来的东西。跟着这一条走，不是笔记", f'<div class="card" style="width:360px">{read_page()}</div>')
             + blk("开场话的框 · 带复制", f'<div style="width:340px">{opening_box()}</div>')
             + blk("把结果贴回来 · 助手不能替你存的时候", f'<div class="card" style="width:360px">{paste_back()}</div>')
             + blk("今日状态 · 常驻，三种宽度，说的是同一件事", f'<div style="width:760px">{sbar_wide()}</div><div style="width:330px" class="card">{sbar_narrow()}</div><div>{sbar_mini()}　{sbar_mini(False)}</div><div style="width:760px">{sbar_wide(False)}</div>')
             + blk("条目和解读 · 每种条目同一副骨架：刚存入、分派后、解读、处理过的", f'<div style="width:330px">{stage1(FLOWERS[0])}<div class="mt12">{stage1(FLOWERS[0], 1)}</div></div><div style="width:340px">{drop(FLOWERS[0])}</div><div style="width:340px">{drop(FAILED)}<div class="fold mt12" style="padding:2px 14px">{drop_done(FLOWERS[5], "不感兴趣")}{drop_done(FLOWERS[4], "看过了")}</div></div>')
             + blk("左右滑 · 只在手机上，只有两个：往右加入深读队列，往左不感兴趣。做完说一句，带撤销", f'<div style="width:340px">{swipe(lesson_card(FLOWERS[3]), "dig")}</div><div style="width:340px">{swipe(lesson_card(FLOWERS[3]), "no")}</div>'
                   f'<div class="col g6"><div class="hud" style="position:static;margin:0">{said_undo(SAY_DIGQ)}</div><div class="hud" style="position:static;margin:0">{said_undo(SAY_NOPE)}</div></div>')
             + blk("判定 · 三选一。状态和判定都是一个圆点加字，没有底、没有框：有底有框的只有能按的东西", f'{verdict_pill(0)}{verdict_pill(1)}{verdict_pill(2)}')
             + blk("每日摘要的四部分 · 值得深读的卡、其余的、睡前一问", f'<div style="width:340px">{lesson_card(FLOWERS[3])}</div><div style="width:340px">{lesson_rest()}</div><div style="width:340px">{night()}</div>')
             + blk("谁能看到什么、能做什么 · 客户端三档，助手另算", f'<div style="width:760px">{perm_table()}</div>')
             + blk("允许页上选权限 · 客户端：请求的那一档缺省选中，更高的不给选", f'<div style="width:340px">{tier_pick(1)}</div><div style="width:340px">{tier_pick(2, 1)}</div>')
             + blk("卡片 · 每日摘要、深读队列里的一条", f'<div style="width:360px">{card_}</div><div style="width:360px">{req_}</div>')
             + blk("存入完的一句话 · 各端外观跟系统走，措辞只有这四句", says)
             + blk("提示的三个轻重", notice) + blk("月历 · 一个月，一天一个点。五种圆点；四种典型的月份；作背景；点开后的大图", hives) + blk("月历的图片 · 浅色、深色、透明底；这个月和十二个月。图里只有圆点和数字", f'{hive_img()}{hive_img("dark")}{hive_img("clear", mark=False)}{hive_img(year=True)}') + blk("贴在别处的样子 · 个人主页、文档、桌面小组件。图会自己更新", embeds()) + blk("没有东西可列时 · 只写一句话，不画插图", f'<div class="card" style="width:330px">{empty("还没有笔记", HONEY_EMPTY)}</div>') + blk("深色", dark, ""))
    return grid([board("颜色、字、间距、logo", "来自 brand/visual.md。色值直接读自样式表。", left, 1180),
                 board("组件", "按钮、状态标识、列表行、卡片、存入完的一句话、提示、空状态。", right, 1180)], 2)
