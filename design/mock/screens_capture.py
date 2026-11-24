"""Capture-only clients on the desktop: the browser extension and the Mac menu-bar app."""
from mocklib import ic, logo, cell, browser, macdesk
from content import T0, SAY_OK, SAY_DUP, SAY_QUEUED, SAY_FAIL, SAY_ASK, SAY_ASK_SUB

ART = ('<div class="art"><div class="w"><h1>把定时任务做成幂等的七种写法</h1><div class="by">blog.example.dev · 8 分钟读完</div>'
       '<div class="fig"></div><p>定时任务最常见的事故不是没跑，而是跑了两遍。本文从「同一份活交两遍会怎样」出发，列出七种让它不出乱子的写法。</p>'
       '<p>第一种最朴素：给每份活一个由内容算出来的标识，交回时按标识去重。{m1}第二种是租约：领活的人拿到一个会过期的凭据，过期之后别人可以接手。{m2}</p>'
       '<p>第三种把副作用和记录写进同一个事务。详见 <a>这篇关于发件箱模式的文章</a>。</p>'
       '<p>第四种是把「做了没有」问到对方那里去，而不是自己记。</p>{over}</div></div>')
TAB = dict(url="blog.example.dev/idempotent-cron", tab_title="把定时任务做成幂等的七种写法", tab_icon='<span style="width:15px;height:15px;border-radius:3px;background:#5b8def;display:inline-block"></span>')


def toast(icon, text, top=16):
    return f'<div class="ui" style="position:static;height:auto;background:none"><div class="toast" style="top:{top}px">{icon}<span>{text}</span></div></div>'


def page(over="", sel=False):
    return ART.format(over=over, m1="<mark>" if sel else "", m2="</mark>" if sel else "")


def states_page():
    rows = [(ic("check", 18), SAY_OK.format(T0), "存入好了。核心收到了才这么说。"),
            (ic("check", 18), SAY_DUP, "重复的吞掉，不新增。"),
            (ic("warn", 18), SAY_FAIL, "没存上要说原因。"),
            (ic("warn", 18), "没存上：文件太大，上限 25 MB", ""),
            (ic("key", 18), "先接入：去 KeepEssence 里允许，短码 KEEP-4827", "第一次存入。允许之后这次要存入的会自动存好。"),
            (ic("warn", 18), "这个页面不是网页，存入不了", "浏览器自己的页面。")]
    body = "".join(f'<div class="row" style="gap:18px;margin-bottom:14px"><div class="toast" style="position:static;min-width:360px">{i}<span>{t}</span></div>'
                   f'<span class="sm">{n}</span></div>' for i, t, n in rows)
    return (f'<div class="ui" style="padding:36px 44px;background:#fff"><div class="h1">页面右上角的一句话 · 全部状态</div>'
            f'<p class="sm mt4" style="margin-bottom:24px">扩展没有弹窗。每次存入完在页面右上角说一句，几秒后自己消失。</p>{body}</div>')


def options_page():
    return (f'<div class="ui" style="padding:44px 0;align-items:center;background:#FAFAF8"><div style="width:620px">'
            f'<div class="row g12">{logo("simple", 40)}<div class="h1">存入到 KeepEssence</div></div>'
            f'<p class="mt12 mut">点工具栏上的 KeepEssence 按钮，或按 ⌥⇧K：存入当前网页。在链接、图片或选中的文字上点右键：存入它。存入好了、之前存入过，或者没存上，页面右上角都会告诉你。</p>'
            f'<div class="card mt20"><div class="h3">连接</div><p class="mt4">已连接，这个浏览器叫「Chrome · Mac」。在 KeepEssence 的 助手设置 › 设备 里可以改名和撤销。</p>'
            f'<div class="row mt12"><span class="btn ghost sm">断开</span></div></div>'
            f'<div class="card mt12"><div class="lab" style="margin-top:0">这个浏览器的名字</div><div class="inp">Chrome · Mac</div>'
            f'<p class="xs mt4">显示在「设备」里。另一台电脑请用不同的名字。</p>'
            f'<div class="lab">KeepEssence 地址</div><div class="inp">https://keepessence.app</div><p class="xs mt4">自己架设的才需要改。改了地址要重新连接。</p>'
            f'<div class="row mt12"><span class="btn sm">保存</span></div></div>'
            f'<p class="xs mt16">这个扩展只在你点它的时候工作：读当前网页的地址和标题，或者你右键点的链接、图片、选中的文字，然后存入到你的 KeepEssence。不读别的内容，不收集任何数据。</p></div></div>')


def ext_screens():
    ask = ('<div class="ui" style="position:static;height:auto;background:none"><div class="toast" style="flex-direction:column;align-items:stretch;gap:10px;width:400px;max-width:400px">'
           f'<div class="row top">{ic("key", 18)}<span>{SAY_ASK}</span></div>'
           '<div class="row" style="justify-content:flex-end"><span class="btn ghost sm" style="color:#FFFFFF;border-color:#555555">不存</span><span class="btn sm">存入</span></div></div></div>')
    menu = ('<div class="ctx" style="left:420px;top:330px"><div>拷贝</div><div>查询「第二种是租约」</div><hr>'
            f'<div class="on">{logo("16", 15)}存入选中的文字到 KeepEssence</div><hr><div>打印…</div><div>检查</div></div>'
            '<div class="ctx" style="left:860px;top:300px;width:230px"><div class="dis">在不同对象上的那一项：</div><hr>'
            f'<div>{logo("16", 15)}存入这个网页到 KeepEssence</div><div>{logo("16", 15)}存入这个链接到 KeepEssence</div><div>{logo("16", 15)}存入这张图片到 KeepEssence</div>'
            f'<div>{logo("16", 15)}存入选中的文字到 KeepEssence</div></div>')
    return [
        browser("点工具栏按钮", "点一下（或按 ⌥⇧K）就存入当前网页。页面右上角说一句「已存入」，几秒后消失。不弹需要再点的窗口。",
                page(toast(ic("check", 18), SAY_OK.format(T0))), ext="on", **TAB),
        browser("右键菜单", "在网页、链接、图片或选中的文字上点右键，各有一项。", page(menu, sel=True), ext="idle", **TAB),
        browser("像密码：先问", "像密码、验证码或密钥的内容，先问一句。这是唯一会多点一下的情况。", page(ask), ext="on", **TAB),
        browser("第一次存入：还没连接", "页面角上显示短码，用户去 KeepEssence 里点一次「允许」，之后自动存好。没有要复制的东西。",
                page(toast(ic("key", 18), "先接入：去 KeepEssence 里允许，短码 KEEP-4827")), ext="on", **TAB),
        browser("全部状态", "扩展会说的每一句话。", states_page(), url="（示意）", tab_title="状态一览", ext="idle"),
        browser("选项页", "连接状态、这个浏览器的名字、服务器地址。平时用不到。", options_page(), url="扩展程序 · 存入到 KeepEssence · 选项", tab_title="存入到 KeepEssence", ext="idle"),
    ]


def nsmenu(connected=True, right=178):
    recent = ("" if not connected else
              '<hr><div class="h">最近</div>'
              f'<div><em>已存入 · {T0} · 刚刚</em></div>'
              '<div><em>已存入 · 截屏 · 14 分钟前</em></div>'
              '<div><em>待上传 · 季度账单.pdf</em></div>'
              '<div><em>已存入 · 一段摘抄 · 2 小时前</em></div>'
              '<div class="n">待上传 1 样</div>')
    conn = ('<div class="n">已连接：Mac 菜单栏应用</div><div>断开连接</div>' if connected else '<div class="on">连接 KeepEssence…</div><div class="n">短码 KEEP-4827 · 去 KeepEssence 里允许</div>')
    return (f'<div class="nsmenu" style="right:{right}px">'
            f'<div{" class=on" if connected else ""}>存入剪贴板<span class="k">⌃⌥K</span></div>'
            '<div>存入当前网页（Safari）<span class="k">⌃⌥P</span></div>'
            '<div>截一块屏幕并存入</div>'
            '<div class="n">把文件或图片拖到菜单栏图标上也能存入</div>'
            '<div class="n">在别的 App 里选中文字或文件，右键 › 服务 › 存入到 KeepEssence</div>'
            f'{recent}<hr><div>今天的每日摘要<span class="k">未读</span></div><div>打开 KeepEssence</div><hr>{conn}'
            '<div>KeepEssence 地址…</div><hr><div>退出 KeepEssence<span class="k">⌘Q</span></div></div>')


def safari():
    return ('<div class="safwin"><div class="bw"><div class="bu" style="height:34px"><span class="tl"><i></i><i></i><i></i></span>'
            '<span class="burl"><em>blog.example.dev/idempotent-cron</em></span></div></div>'
            '<div class="art" style="height:760px;padding-top:34px"><div class="w"><h1 style="font-size:30px">把定时任务做成幂等的七种写法</h1>'
            '<div class="by">blog.example.dev · 8 分钟读完</div><div class="fig" style="height:170px"></div>'
            '<p>定时任务最常见的事故不是没跑，而是跑了两遍。本文从「同一份活交两遍会怎样」出发，列出七种让它不出乱子的写法。</p>'
            '<p>第一种最朴素：给每份活一个由内容算出来的标识，交回时按标识去重。第二种是租约：领活的人拿到一个会过期的凭据，过期之后别人可以接手。</p>'
            '<p>第三种把副作用和记录写进同一个事务。第四种是把「做了没有」问到对方那里去，而不是自己记。</p></div></div></div>')


def mac_screens():
    note = (f'<div class="macnote"><span class="ai">{logo("app", 36)}</span><div><b>KeepEssence</b>{SAY_OK.format(T0)}</div></div>')
    dlg = (f'<div class="macdlg">{logo("color", 54)}<h4>{SAY_ASK}</h4>'
           f'<p>{SAY_ASK_SUB.format("这台 Mac ")}</p><span class="b p">存入</span><span class="b">不存</span></div>')
    return [
        macdesk("菜单栏图标和下拉菜单", "图标用单色版。菜单从上到下：三种存入的办法、最近存入的几样、今天的每日摘要、连接状态。没有任何窗口。",
                safari() + nsmenu()),
        macdesk("存入完说一句", "系统通知说结果。不抢键盘，不跑到前台。", safari() + note),
        macdesk("还没连接", "点「连接 KeepEssence…」后菜单里显示短码，去 KeepEssence 里点一次「允许」。", safari() + nsmenu(False)),
        macdesk("像密码：先问", "只有用户刚亲手点了什么，才会弹这个提问。", safari() + dlg),
        macdesk("深色菜单栏", "深色下图标用反白版。", safari() + nsmenu(), dark=True),
    ]
