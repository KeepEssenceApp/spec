"""Web app: the full reading platform, wide layout."""
from mocklib import ic, logo, bee_chip, webapp, browser, wordmark, hive
from content import *
import screens_iphone as I


def home(ok=True):
    if ok:
        left = (sbar_wide() + f'<div class="lab">今天的解读 · 新的在前</div>{drop(FLOWERS[0])}<div class="mt8">{drop(FLOWERS[3], pts=2)}</div>'
                '')
    else:
        left = (sbar_wide(False) + f'<div class="card mt12" style="padding:22px 24px"><div class="row"><span class="xs">最近的一份每日摘要</span><span class="sp"></span>{READ}</div>'
                f'<div class="h1 mt4">每日摘要 · 11月18日 周三</div><p class="mt8 mut">存入了 15 条。3 条值得深挖。这是最近的一份。</p>'
                f'<div class="row mt16"><span class="btn">读每日摘要</span></div></div>')
    if ok:
        right = (f'<div class="row top" style="margin-bottom:14px"><div class="col sp"><span class="xs">这个月的月历 · 11月</span><span class="sm mt4">存入了 148 条 · 读了 16 份每日摘要 · 留下 5 篇</span><span class="lk xs mt8">打开</span></div>{hive(MONTH, 9)}</div>'
                 f'<div class="card"><div class="row"><span class="xs">今晚的每日摘要</span><span class="sp"></span>{UNREAD}</div>'
                 f'<div class="h2 mt4">每日摘要 · {DATE}</div><p class="sm mt4">存入了 9 条。2 条值得深挖，其余 5 条收在后面。</p>'
                 f'<div class="row mt12"><span class="btn sm">读每日摘要</span><span class="sp"></span><span class="xs">阿读 · 21:02 汇总</span></div></div>'
                 f'<div class="lab">深挖队列</div>'
                 + ripen_req(DIG[0], SIPPER, "ready", f'<div class="row mt12"><span class="btn sm">{ic("chat", 15)}去深挖</span><span class="lk sm">看精读</span></div>')
                 + f'<div class="lab">处理过的 · 2 个</div><div class="fold" style="padding:2px 14px">{drop_done(FLOWERS[5], "不感兴趣")}{drop_done(FLOWERS[4], "看过了")}</div>'
                 + f'<div class="lab">还在等助手的条目 · 4 条</div><div class="card"><div class="row"><span>2 条等分派 · 2 条等解读</span><span class="sp"></span>{ic("chev", 16, "faint")}</div>'
                 f'<p class="xs mt4">最早的一条明天删除</p></div>')
    else:
        right = (f'<div class="card bad" style="padding:18px 20px"><div class="row">{ic("warn", 20, "badc")}<b style="font-size:16px">没有助手在干活</b></div>'
                 f'<p class="mt8">条目照样能存入，也照样会按时到期删除。没有助手来，就没有解读和每日摘要。</p>'
                 f'<div class="hr"></div><div class="kv"><span>还没被解读的条目</span><b>14 条</b></div>'
                 f'<div class="kv"><span>最早的一条到期删除</span><b class="badc">11月24日（3 天后）</b></div>'
                 f'<div class="kv"><span>今天为什么没有每日摘要</span><span>没有助手来汇总</span></div></div>'
                 + f'<div class="lab">每个助手上一次来</div><div class="card" style="padding:2px 16px">'
                 + bee_row("阿探", "分派助手 · 还在分派", "刚刚来过")
                 + bee_row("阿读", ALL3, "3 天前来过", "bad")
                 + bee_row("阿深", "深挖", "5 天前来过", "bad") + '</div>'
                 f'<div class="row mt12"><span class="btn quiet sm">{ic("gear", 15)}看助手设置</span></div>')
    return f'<div class="pane read" style="padding-right:14px">{left}</div><div class="pane" style="width:390px;flex:none;padding-left:14px">{right}</div>'


def classes():
    more = CLASSES + [("11月12日 周四", "存入了 7 条 · 2 条值得深挖", True), ("11月11日 周三", "存入了 9 条 · 2 条值得深挖", True)]
    picks = "".join(f'<div class="pick{" on" if i == 0 else ""}"><div class="row"><b class="serif">每日摘要 · {d}</b><span class="sp"></span>{"" if r else UNREAD}</div>'
                    f'<span class="xs">{s}</span></div>' for i, (d, s, r) in enumerate(more))
    body = (f'<div class="inner"><div class="row"><span class="xs">阿读汇总 · 21:02 · 存入了 9 条</span><span class="sp"></span>'
            f'<span class="btn ghost sm">{ic("dl", 15)}导出</span></div>'
            f'<div class="h1 mt8" style="font-size:30px">每日摘要 · {DATE}</div>'
            f'<p class="sm mt8" style="line-height:1.7;font-size:14px">{SUMMARY}</p>'
            f'<div class="lab">值得深挖的 · 2 条</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start">{lesson_card(FLOWERS[0])}{lesson_card(FLOWERS[3])}</div>'
            f'<div class="mt16">{lesson_rest(False)}</div>{night()}</div>')
    return f'<div class="pane side">{picks}</div><div class="pane read">{body}</div>'


def honey():
    picks = "".join(f'<div class="pick{" on" if i == 0 else ""}"><b class="serif">{t}</b><span class="xs">{d} · {f}{(" · " + a) if a else ""}</span></div>'
                    for i, (t, d, f, a) in enumerate(HONEY))
    body = (f'<div class="inner"><div class="row"><span class="xs">笔记 · 11月20日 · {bee_chip("阿深")}</span><span class="sp"></span>'
            f'<span class="btn ghost sm">{ic("dl", 15)}下载</span></div>'
            f'<div class="h1 mt8" style="font-size:28px">{HONEY[0][0]}</div>'
            f'<p class="mt16" style="font-size:16px;line-height:1.8">一份活同时只归一个助手，靠的是认领；认领会过期，靠的是租约；过期之后别人接着做不出乱子，靠的是重放安全。三件事缺一件，另外两件都白做。</p>'
            f'<div class="h2 mt20">结论</div><p class="mt8" style="font-size:16px;line-height:1.8">一、租约定 30 分钟，比最慢的一次检查点长。<br>二、交回按内容去重，同一份交两遍只留后一次。<br>三、不能重放的工具不让助手在取活的路上调用。</p>'
            f'<div class="h2 mt20">出处</div><div class="src mt8">{ic("link", 13)}<em>Durable harness: intent, effect, result · github.com/example/durable-harness</em></div>'
            f'<div class="src mt4">{ic("link", 13)}<em>Leases in job queues · blog.example.dev/leases</em></div>'
            f'<div class="card mt20"><div class="row">{ic("img", 18, "mut")}<span>租约时序图.png</span><span class="sp"></span><span class="xs">附件 · 182 KB</span>{ic("dl", 18, "deep")}</div></div>'
            f'<p class="xs mt16">出自 11月19日 每日摘要 · 第 2 条</p></div>')
    return f'<div class="pane side" style="width:360px">{picks}</div><div class="pane read">{body}</div>'


def blooms():
    rows = "".join(bloom_row(b) for b in BLOOMS[:7])
    return (f'<div class="pane side" style="width:440px;padding:16px 20px"><div class="row"><span class="sm">未到期的条目 · 23 条</span><span class="sp"></span>'
            f'<span class="seg"><span class="on">今天</span><span>全部</span><span>收藏</span></span></div><div class="lst mt4">{rows}</div></div>'
            f'<div class="pane read"><div class="inner">{I.bloom_detail()}</div></div>')


def ripen():
    return f'<div class="pane read"><div class="inner">{I.ripen_list()}</div></div>'


SETTABS = '<div class="row" style="padding:14px 28px 0;gap:6px"><span class="seg"><span class="{a}">助手和规则</span><span class="{b}">设备</span><span class="{c}">我的月历</span><span>账户</span></span></div>'


def settings_colony(notify_ok=True):
    rev = REV
    left = (f'<div class="row"><div class="h2">助手</div><span class="sp"></span><span class="btn quiet sm">{ic("plus", 15)}接入一个助手</span></div>'
            f'<div class="card mt12" style="padding:2px 16px">'
            + bee_row("阿探", "分派助手 · 我们提供，免费", "刚刚来过", "ok")
            + bee_row("阿读", ALL3, "4 分钟前来过", "ok", rev)
            + bee_row("阿深", "深挖", "2 小时前来过", "warn", rev)
            + f'</div><div class="h2 mt28">谁做哪一步</div><div class="card mt12" style="padding:4px 16px">'
            f'<div class="kv"><span>缺省解读助手 · 分派助手没指名时</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>汇总助手 · 出每日摘要</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>精读助手 · 精读队列里的条目</span><span class="sel">{bee_chip("阿读")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>缺省精读助手 · 点「去深挖」时</span><span class="sel">{bee_chip("阿深")}{ic("down", 16, "faint")}</span></div>'
            f'<div class="kv"><span>寿命档位（天）</span><span>7 · 30 · 90 · 365</span></div></div>'
            f'<p class="xs mt8">设成「无」的那一步没人做。</p>')
    right = (f'<div class="h2">规则</div><p class="sm mt4">写给分派助手的话：什么样的条目交给谁、活多久。它只看标题、来源和开头。</p>'
             f'<div class="inp area mt12" style="white-space:pre-line;min-height:120px;font-size:14.5px">{RULES}</div>'
             f'<div class="row mt12"><span class="btn sm">保存</span><span class="xs">分派助手没写的由核心补：交给缺省解读助手，活 30 天。</span></div>'
             f'<div class="h2 mt28">每日摘要</div><div class="card mt12" style="padding:4px 16px">'
             f'<div class="kv"><span>几点以后出</span><span class="sel">21:00{ic("down", 16, "faint")}</span></div>'
             f'<div class="kv"><span>时区</span><span>跟这台设备</span></div></div>'
             f'<div class="h2 mt28">通知</div><div class="mt12">{notify_card("这个浏览器", ok=notify_ok, ask="在这个浏览器里通知我")}</div>')
    return (f'<div class="col" style="flex:1;min-width:0">{SETTABS.format(a="on", b="", c="")}<div style="display:flex;flex:1;min-height:0">'
            f'<div class="pane read" style="padding-right:14px">{left}</div><div class="pane" style="width:440px;flex:none;padding-left:14px">{right}</div></div></div>')


def add_bee(product="Claude"):
    """Connect a bee: the product list on the left, the guide for the chosen one on the right."""
    return (f'<div class="col" style="flex:1;min-width:0">{SETTABS.format(a="on", b="", c="")}<div style="display:flex;flex:1;min-height:0">'
            f'<div class="pane" style="width:470px;flex:none;padding-right:14px"><div class="row"><span class="lk sm row g4">{ic("back", 15)}助手</span></div>'
            f'<div class="h2 mt8">接入一个助手</div><p class="sm mt4">选它在哪个产品里。每一种能做的事不一样。</p>'
            f'<div class="mt8">{product_list(product)}</div><p class="xs mt12">{KINDS_NOTE}</p></div>'
            f'<div class="pane read" style="padding-left:14px"><div class="card" style="padding:22px 24px;max-width:560px">{guide(product)}</div></div></div></div>')


def bee_allow_page(product="Claude", name=RIPENER, steps="深挖"):
    kind = dict((x[0], x[1]) for x in PRODUCTS)[product]
    return (f'<div class="ui" style="align-items:center;justify-content:center"><div class="col" style="align-items:center;text-align:center;width:440px">'
            f'{logo("simple", 56)}<div class="mt12" style="width:100%">{join_allow(name, kind, "", steps=steps, warn=True, product=product)}</div></div></div>')


def dig_modal():
    return f'<div class="scrim"></div><div class="modal" style="width:460px">{dig_pick("link")}</div>'


def paste_modal():
    return f'<div class="scrim"></div><div class="modal">{paste_back()}</div>'


def revoke_modal():
    return f'<div class="scrim"></div><div class="modal">{revoke_confirm()}</div>'


def settings_devices():
    ways = [("device", "iPhone 快捷指令", "安装", "轻点背面两下存入网页，三下存入截屏。第一次运行会显示一个短码，回到这里点允许。"),
            ("img", "浏览器扩展", "安装", "点工具栏按钮或右键存入。第一次存入时显示一个短码，回到这里点允许。"),
            ("device", "Mac 菜单栏应用、手机 App", "v1.x", "和上面两个一样：显示一个短码，回到这里点允许。"),
            ("bee", "一个助手", "怎么接", "助手不用短码。在「助手和规则」里点「接入一个助手」，选产品，把接入地址贴到它那边，再在允许页点允许。")]
    right = ('<div class="h2">再接入一个</div><div class="col g12 mt12">'
             + "".join(f'<div class="card"><div class="row">{ic(i, 18, "deep")}<b>{t}</b><span class="sp"></span><span class="btn quiet sm">{b}</span></div><p class="xs mt4">{d}</p></div>'
                       for i, t, b, d in ways) + '</div>')
    return (f'<div class="col" style="flex:1;min-width:0">{SETTABS.format(a="", b="on", c="")}<div style="display:flex;flex:1;min-height:0">'
            f'<div class="pane read" style="padding-right:14px"><div class="h2">设备</div><p class="sm mt4">接入的每个客户端和每个助手都是一个设备。客户端可以改权限；每个都可以改名、单独撤销，马上生效，别的设备不受影响。</p>'
            f'<div class="card mt12" style="padding:2px 16px">{device_rows()}</div></div>'
            f'<div class="pane" style="width:440px;flex:none;padding-left:14px">{right}</div></div></div>')


def stats():
    days = [("15", 46, .55), ("16", 30, .55), ("17", 0, .55), ("18", 112, .55), ("19", 44, .55), ("20", 90, .55), ("21", 68, 1)]
    bars = "".join(f'<div class="col" style="align-items:center;justify-content:flex-end;gap:6px;flex:1;height:100%"><div style="width:100%;height:{h}px;background:var(--ink);border-radius:6px 6px 0 0;opacity:{o}"></div><span class="xs">{d}</span></div>'
                   for d, h, o in days)

    def src(n, v, p):
        return f'<div class="kv"><span>{n}</span><span class="row"><i style="display:inline-block;width:{p}px;height:6px;border-radius:3px;background:var(--ink)"></i><b style="min-width:28px;text-align:right">{v}</b></span></div>'

    def num(v, l):
        return f'<div class="card"><div class="h1" style="font-size:30px">{v}</div><div class="xs">{l}</div></div>'
    return (f'<div class="pane read"><p class="sm">只有汇总的数字。条目到期删除以后，这里不再能指回它，也不能按来源去翻条目。</p>'
            f'<div class="cols mt16" style="grid-template-columns:repeat(4,1fr)">{num("54", "最近 7 天存入的条目")}{num("47", "被解读")}{num("6", "份每日摘要")}{num("31", "条到期删除了")}</div>'
            f'<div class="cols mt20" style="grid-template-columns:1.2fr 1fr"><div class="card"><div class="h3">每天存入了多少</div><div class="row" style="align-items:flex-end;height:150px;gap:14px;margin-top:14px">{bars}</div></div>'
            f'<div class="card"><div class="h3">从哪来</div><div class="mt8">{src("iPhone · 快捷指令", 23, 150)}{src("浏览器扩展", 17, 110)}{src("Mac 菜单栏应用", 9, 60)}{src("iPhone · 分享", 5, 34)}</div></div></div>'
            f'<div class="card mt20"><div class="h3">每个助手做了多少</div><div class="cols mt8" style="grid-template-columns:repeat(3,1fr)">'
            f'<div class="kv"><span>分派助手</span><b>54</b></div><div class="kv"><span>阿读 · 解读</span><b>47</b></div><div class="kv"><span>阿读 · 汇总</span><b>6</b></div></div></div></div>')


def login_page(dark=False):
    return (f'<div class="ui{" dark" if dark else ""}" style="align-items:center;justify-content:center"><div class="col" style="align-items:center;text-align:center;width:360px">'
            f'{logo("color", 112)}<div class="mt16">{wordmark(44, dark)}</div><p class="mut mt12">随手存入，助手替你读完，每天归成一份每日摘要。</p>'
            f'<div class="mt28" style="width:100%"><span class="btn block">用 Google 登录</span></div>'
            f'<div class="mt12" style="width:100%"><span class="btn ghost block">用邮箱验证码登录</span></div>'
            f'<p class="xs mt20">现在不开放注册。</p></div></div>')


def allow_page():
    return (f'<div class="ui" style="align-items:center;justify-content:center"><div class="col" style="align-items:center;text-align:center;width:440px">'
            f'{logo("simple", 56)}<div class="mt12" style="width:100%">{join_allow("Chrome 扩展 · Mac", "客户端", "", tier=0)}</div></div></div>')


def screens():
    W = webapp
    return [
        W("今天", "最上面是宽的今日状态。左边是今天的解读，每个四行，带三个动作，以前见过类似的就在解读上。右边是今晚的每日摘要、深挖、处理过的。", "home", home(), "今天"),
        W("解读好了 · 浏览器通知", "v1.0 只有网页，通知走浏览器。页面正开着的时候不弹，解读直接出现在「今天」里；这一屏画的是页面在后台的时候。", "home", home(), "今天",
          overlay=f'<div class="macnote" style="top:14px"><span class="ai">{logo("app", 36)}</span><div><b>{NOTE_MANY[0]}</b>{NOTE_MANY[1]}</div></div>'),
        W("每日摘要", "点「每日摘要」直接打开最新一份，左边按日期往前翻。四部分：总结、值得深挖的（重点）、其余的（折叠）、睡前一问，最后「读了，晚安」。", "class", classes(), "每日摘要"),
        W("笔记", "深挖的产出，按时间排。可以下载，可以带附件。", "honey", honey(), "笔记"),
        W("今天 · 这个月的月历", "从今天页右上的小月历点开。一天一个点；下面四个数；可以翻以前的月份。", "home",
          f'<div class="pane read"><div class="inner" style="max-width:520px;margin:0 auto">{hive_page()}</div></div>', "今天"),
        W("今天 · 点开一个条目", "条目不是单独的入口，从今天点进来。右边是详情：管理档的设备能改「交给哪个助手」和「活多久」。", "home", blooms(), "今天"),
        W("每日摘要 · 点「深挖」之后", "面板顶上两个选项：排入队列先精读，或者现在去深挖。现在去时列出能深挖的助手，缺省的那个已选好，一个按钮过去；排入队列的由定时来的助手精读。网页没有滑动，排入队列只在这里。", "class", classes(), "每日摘要", overlay=dig_modal()),
        W("笔记 · 深挖队列", "深挖不是单独的入口：队列排在笔记页最上面，这里展开看全部。状态只有精读的三档；去没去深挖只照实写。去过的那条有两个安静的出口：「把结果贴回来」和「移出队列」。", "honey", ripen(), "笔记"),
        W("笔记 · 把结果贴回来", "助手不能替你存的时候（ChatGPT 的个人套餐）：标题、一个大的粘贴框、「存成笔记」。", "honey", ripen(), "笔记", overlay=paste_modal()),
        W("助手设置", "接入了哪几个助手、每个是定时来的还是对话里的、在哪个产品里；谁做哪一步、寿命档位、写给分派助手的规则。一次性的设置。", "set", settings_colony(), "助手设置"),
        W("助手设置 · 这个浏览器还没开通知", "每个浏览器各开一次。点「在这个浏览器里通知我」，浏览器才问权限。iPhone 上要先把网页加到主屏幕。", "set", settings_colony(False), "助手设置"),
        W("助手设置 · 接入一个助手", "左边选产品：每行写它是哪一种助手、能做什么。右边是这个产品的步骤。要复制的只有接入地址。这里选的是 Claude。", "set", add_bee("Claude"), "助手设置"),
        W("接入一个助手 · ChatGPT", "要在电脑上接。个人套餐只能读，笔记由用户贴回来。", "set", add_bee("ChatGPT"), "助手设置"),
        W("接入一个助手 · Gemini", "限制写在步骤下面，不藏。", "set", add_bee("Gemini"), "助手设置"),
        W("接入一个助手 · Muse（待验证）", "还没验证的不编步骤，只说一句现在知道的。", "set", add_bee("Muse"), "助手设置"),
        W("助手设置 · 设备", "客户端和助手都在这里。客户端一行显示权限（只存入、读、管理），可以改；助手显示它干哪几步。", "set", settings_devices(), "助手设置"),
        W("助手设置 · 撤销一台设备", "撤销马上生效。", "set", settings_devices(), "助手设置", overlay=revoke_modal()),
        W("今天 · 没有助手在干活", "不算故障，但要一眼看出来：多少条没被解读、最早哪天到期删除、每个助手上次来的时间、今天为什么没有每日摘要。", "home", home(False), "今天", bees_ok=False),
        W("助手设置 · 我的月历", "左边是图的预览，改选项时跟着变；右边是开关、地址和样子。地址可以复制，可以换。", "set",
          f'<div class="col" style="flex:1;min-width:0">{SETTABS.format(a="", b="", c="on")}<div style="display:flex;flex:1;min-height:0">'
          f'<div class="pane read" style="padding-right:14px"><div class="lab" style="margin-top:0">现在的样子</div>{hive_img()}'
          f'<div class="lab">十二个月的版式</div>{hive_img(year=True)}<div class="lab">深色</div>{hive_img("dark", r=10)}</div>'
          f'<div class="pane" style="width:440px;flex:none;padding-left:14px">{my_hive(preview=False)}</div></div></div>', "助手设置"),
        W("助手设置 · 统计（可有可无，v1.x）", "只有汇总数字：存入了多少、从哪来、每个助手做了多少。不能用来翻条目。", "stats", stats(), "统计"),
        browser("登录", "不开放注册。登录后才看得到任何内容。", login_page(), url="keepessence.app/login"),
        browser("允许一台设备", "已登录的 KeepEssence 里：谁想接入、它能做什么、和它那边一样的短码。只有我们自己的客户端用短码。", allow_page(), url="keepessence.app/allow"),
        browser("允许一个助手", "助手在浏览器里打开的允许页：哪个产品想接入、给助手起的名字（可以改）、勾它能干哪几步、内容会被送出去的提示。没有短码。", bee_allow_page(), url="keepessence.app/allow"),
        W("今天 · 深色", "黑底白字。金只在留下来的东西上。", "home", home(), "今天", dark=True),
        W("每日摘要 · 深色", "同一份每日摘要的深色版。", "class", classes(), "每日摘要", dark=True),
        browser("登录 · 深色", "深色背景上字标用蜡白。", login_page(True), url="keepessence.app/login", dark=True),
    ]
