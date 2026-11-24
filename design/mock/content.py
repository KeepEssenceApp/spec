"""Sample content shared by all clients. Everything here is made up."""
from mocklib import ic, cell, life, kept, bee_chip, sbar_mini

DATE = "11月21日 周六"
UNREAD = '<span class="pill honey">未读</span>'
READ = '<span class="xs">读了</span>'

# (title, conclusion, source title, source url)
ITEMS = [
    ("持久化的 agent 运行框架：先写意图，再执行，最后写结果",
     "工具要声明自己能不能安全重放。副作用和重放契约那一节值得读。",
     "Durable harness: intent, effect, result", "github.com/example/durable-harness"),
    ("任务队列的认领和租约：三种超时设计的对比",
     "知道就行。结论是租约要短、续租要便宜。",
     "Leases in job queues", "blog.example.dev/leases"),
    ("SQLite 在高并发写入下的 WAL 行为实测",
     "值得读，尤其是 checkpoint 卡住读者的那一节。",
     "WAL under write pressure", "db.example.org/wal-notes"),
    ("视频（12 分钟）：给 Capacitor 应用加系统分享入口",
     "步骤和你现在的做法一致，可以不看。",
     "Share extension in 12 minutes", "video.example.com/watch/8f2k"),
    ("一张截屏：终端里证书链不完整的报错",
     "报错指向中间证书缺失。截屏里能看到是第二级证书没有随服务器下发。",
     "截屏 11-21 14.32", "来自 iPhone"),
    ("一张图片：手冲咖啡粉水比对照表",
     "表里给的是 1:15 到 1:17 三档，对应三种烘焙度的建议水温。",
     "图片", "来自 Mac"),
]
GROUPS = [("Agent 崩了以后怎么办", [0, 1]), ("本地优先的存储", [2, 3]), ("零碎", [4, 5])]

WEAVE = ("今天有两条都在讲同一件事：一份活做到一半断了，怎么让别人安全地接着做。"
         "运行框架那篇从「工具要声明能否重放」入手，队列那篇从「租约多久过期」入手，合起来正好是取活、认领、交回的完整设计。"
         "WAL 那篇是它的存储一侧：检查点卡住的时候，认领的超时不能比它短。")
DIG = ["「能安全重放」怎么定义？哪些工具天然做不到，做不到的该怎么办？",
       "租约过期和任务本身超时，是一个钟还是两个钟？",
       "WAL 的检查点能不能放到没人取活的时候做？"]
NIGHT = "如果只能给每份活留一个超时，你会把它定成多久？为什么？"


def item_html(i, acts=True, dislike=True, src=True):
    t, c, st, su = ITEMS[i]
    a = ""
    if acts:
        a = (f'<div class="acts"><span class="btn quiet sm">{ic("chat", 15)}深入对话</span><span class="sp"></span>'
             + ('<span class="btn ghost sm">不感兴趣</span><span class="btn ghost sm">看过了</span>' if dislike else "") + "</div>")
    s = f'<div class="src mt4">{ic("link", 13)}<em>{st} · {su}</em></div>' if src else ""
    return f'<div class="it"><div class="h3">{t}</div><p class="verdict mt4">{c}</p>{s}{a}</div>'


# blooms: (icon, title, source, state 0/1/2, days left (0 = kept, it never expires), bee)
BLOOMS = [
    ("link", "Streamable HTTP 传输说明（草案）", "spec.example.io", 0, 30, None),
    ("img", "截屏 11-21 20.58", "来自 iPhone · 快捷指令", 0, 30, None),
    ("link", "把定时任务做成幂等的七种写法", "blog.example.dev", 1, 30, "阿读"),
    ("text", "「先写意图再执行」那段摘抄", "来自 Mac · 剪贴板", 1, 7, "阿读"),
    ("link", "持久化的 agent 运行框架", "github.com/example", 2, 0, "阿读"),       # 0 days left = kept
    ("link", "SQLite 在高并发写入下的 WAL 行为实测", "db.example.org", 2, 90, "阿读"),
    ("video", "给 Capacitor 应用加系统分享入口", "video.example.com", 2, 30, "阿读"),
    ("img", "手冲咖啡粉水比对照表", "来自 Mac", 2, 3, "阿读"),
    ("file", "季度账单.pdf", "来自 iPhone · 分享", 2, 1, "阿读"),
]
STATE = {0: "等分派", 1: "等解读", 2: "已解读", 3: "值得深读", 4: "留成笔记"}


def note_thumb():
    """A note: the gold dot, the one thing that was kept."""
    return f'<span class="thumb">{cell(4, 28)}</span>'


LIFE_NOTE = "到期连同解读一起删除；用户看不见，归档副本的保留规则见数据保留说明。每日摘要里的那一条不受影响。"
KEEP_NOTE = "收藏就是把期限延到不过期：原文和解读一直留着。不用精读，也不用深入对话。随时可以改回来。"


def life_pick(days=90):
    """How long an item lives. The last choice, never, is what keeping means. days: 7 | 30 | 90 | 365 | 0 (kept)."""
    return '<span class="seg">' + "".join(f'<span class="{"on" if v == days else ""}">{t}</span>' for v, t in [(7, "7"), (30, "30"), (90, "90"), (365, "365"), (0, "收藏")]) + '</span>'


def bloom_row(b, show_bee=False):
    icn, t, s, st, d, bee = b
    tot = {7: 7, 30: 30, 90: 90, 3: 30, 1: 30}.get(d, 30)
    extra = f' · {bee_chip(bee)}' if (show_bee and bee) else ""
    return (f'<div class="li"><span class="thumb">{ic(icn, 20)}</span><div class="col sp" style="min-width:0">'
            f'<span class="ti">{t}</span><span class="src mt4"><em>{s}</em></span>'
            f'<div class="row mt4" style="gap:10px;flex-wrap:wrap">{cell(st, 16)}<span class="xs">{STATE[st]}{extra}</span><span class="sp"></span>{life(d, tot) if d else kept()}</div></div></div>')


# honey: (title, date, from, attachments)
HONEY = [
    ("一份活做到一半断了：认领、租约和重放的设计笔记", "11月20日", "出自 11月19日 每日摘要 · 第 2 条", "1 个附件"),
    ("本地优先应用的同步冲突：我们到底要不要做合并", "11月16日", "出自 11月15日 每日摘要 · 第 4 条", ""),
    ("墨水屏上的排版：行长、字重和灰阶", "11月9日", "出自 11月8日 每日摘要 · 第 1 条", "3 个附件"),
    ("给个人工具定价：免费的那一档该包含什么", "11月2日", "出自 11月1日 每日摘要 · 第 3 条", ""),
]

CLASSES = [("11月21日 周六", "存入了 9 条 · 2 条值得深读", False), ("11月20日 周五", "存入了 12 条 · 3 条值得深读", True),
           ("11月19日 周四", "存入了 6 条 · 1 条值得深读", True), ("11月18日 周三", "存入了 15 条 · 4 条值得深读", True),
           ("11月16日 周一", "存入了 4 条 · 含 15 日漏归的 2 条", True), ("11月14日 周六", "存入了 8 条 · 2 条值得深读", True),
           ("11月13日 周五", "存入了 11 条 · 3 条值得深读", True)]

WAGGLE = [("新存入的「把定时任务做成幂等的七种写法」", "和 11月19日 每日摘要里讲租约的那条说的是同一个问题。"),
          ("新存入的「Streamable HTTP 传输说明」", "你 11月16日 那篇笔记「同步冲突」里引用过它的上一版。")]

RULES = ("技术文章、代码仓库交给阿读，活 30 天。\n视频只要结论，活 7 天。\n截屏和图片交给阿读，写清楚图里有什么，活 30 天。\n"
         "论文和长文活 90 天。")


# ---------------------------------------------------------------- pieces every client shares
# What a capture says when it is done. One wording on every client (rule C3).
T0 = "把定时任务做成幂等的七种写法"
SAY_OK = "已存入：{}"
SAY_DUP = "之前存入过，这个条目还在"
SAY_QUEUED = "先存在这台设备上，联网后自动上传"
SAY_FAIL = "没存上：连不上 KeepEssence，稍后再试"
SAY_ASK = "这看起来像密码、验证码或密钥，确定要存入吗？"
SAY_ASK_SUB = "还没有上传，也没有留在{}上。"

# The one notification: an item has been read. Bold line, then the title(s). The same wording on every platform.
# Nothing else is ever notified: not the digest, not items about to be cleaned up, not an assistant that did not come.
NOTE_ONE = ("解读好了 · 值得深读", T0)
NOTE_MANY = ("解读好了 6 条 · 2 条值得深读", T0 + "、持久化的 agent 运行框架")
NOTE_MISS = ("解读好了 3 条 · 1 条没取到内容", "没有值得深读的")
NOTIFY = ["都通知", "有值得深读的才通知", "不通知"]
NOTIFY_NOTE = "连着解读好的合成一条，里面只有标题和判定。只有这一种通知：每日摘要出了、条目快要到期删除、助手没来，都不发。"
ASK_NOTIFY = "解读好了通知你？"
ASK_NOTIFY_SUB = "助手来取活要等一会儿。解读好了发一句，只有标题和判定。别的事不通知。"


def notify_pick(on=0):
    return '<span class="seg">' + "".join(f'<span class="{"on" if i == on else ""}">{t}</span>' for i, t in enumerate(NOTIFY)) + '</span>'


def notify_card(here="这台 iPhone", ok=True, on=0, ask="去系统设置里打开"):
    """The only notification setting: one choice of three, plus whether this device can receive it."""
    got = '<span class="pill ok">收得到</span>' if ok else f'<span class="row g6"><span class="pill off">收不到</span><span class="lk sm">{ask}</span></span>'
    return (f'<div class="card" style="padding:2px 16px"><div style="padding:11px 0;border-bottom:1px solid var(--line)">'
            f'<div class="xs">条目解读好了</div><div class="mt8">{notify_pick(on)}</div></div>'
            f'<div class="kv"><span>{here}</span>{got}</div></div><p class="xs mt8">{NOTIFY_NOTE}</p>')

# A ripen request: state -> (label, pill class). The same five everywhere.
# Three depths, one word each. 解读: every item, the assistant, automatic. 精读: an item in the dig queue, an assistant alone,
# while it waits. 深入对话: the user takes the item to the assistant (talk, search again, run things there).
# The platform cannot see what happens at the assistant's place, so an item in the queue has no "digging now" or "finished"
# state. Its only states are about the close reading; everything else is a fact: when it was queued, whether the user went,
# whether a note came back.
RIPEN = {"wait": ("等精读", ""), "prep": ("精读中", "warn"), "ready": ("精读好了", "ok"),
         "skip": ("没做精读", "plain"), "void": ("已移出", "off")}
STEP_READ, STEP_DIG = "精读", "深入对话"
READ_SAYS = "加入深读队列。助手趁它排着先精读，不用你在场；读好了在「笔记」页最上面等你。"
DIG_SAYS = "现在就带着这一条去助手那边：聊、让它再查、做它那边能做的事。有笔记存回来就留下，没有也没关系。"


def ripen_pill(state):
    t, c = RIPEN[state]
    return f'<span class="pill {c}">{t}</span>'


def ripen_req(title, bee, state, body="", label=False):
    """One ripen request: state pill on the left, the bee on the right, the question, then what happens next."""
    lab = '<span class="xs">深入对话</span>' if label else ""
    return (f'<div class="card"><div class="row">{lab}{ripen_pill(state)}<span class="sp"></span>{bee_chip(bee)}</div>'
            f'<div class="h3 mt8">{title}</div>{body}</div>')


def bee_row(name, role, when, dot="ok", extra="", product=None):
    """One bee in the colony: name, its kind (comes on a schedule / lives in a chat), the product it runs in, what it does,
    when it last came. dot: ok | warn | bad | '' (never came). Kind and product come from BEES unless product is given."""
    prod, kind = BEES.get(name, ("", ""))
    if product:
        prod, kind = product, dict((x[0], x[1]) for x in PRODUCTS)[product]
    tag = kind_pill(kind) if kind else ""
    role = f"{prod} · {role}" if prod else role
    return (f'<div class="li" style="align-items:center"><span class="thumb">{ic("bee", 20)}</span><div class="col sp" style="min-width:0">'
            f'<span class="row g6"><b>{name}</b>{tag}</span>'
            f'<span class="xs">{role}</span></div><span class="xs row g6" style="flex:none"><span class="dot {dot}"></span>{when}</span>{extra}</div>')


def said(icon, text):
    """icon + one sentence, used inside each platform's own toast / HUD / snackbar."""
    return f'{icon}<span>{text}</span>'


# ---------------------------------------------------------------- round 4: one skeleton for every kind of bloom
SCOUT, SIPPER, RIPENER = "阿探", "阿读", "阿深"

# kind, icon, title, source, time, days, what, fact, points, verdict(0 dig / 1 know / 2 skip), waggle
FLOWERS = [
    dict(kind="文章", icon="link", title="把定时任务做成幂等的七种写法", src="blog.example.dev", at="14:20", days=30,
         what="一篇讲定时任务重复执行也不出错的长文，给了七种写法。",
         fact="作者 M. Rivera · 约 4,200 字 · 读完 12 分钟",
         pts=["核心只有一句：把「做了没有」记在和结果同一个事务里。", "七种写法里前三种够用，后四种是特例。", "反例一节讲了去重键选错的后果。"],
         v=0, wag="和 11月19日 每日摘要里讲租约的那条说的是同一个问题。"),
    dict(kind="视频", icon="video", title="给 Capacitor 应用加系统分享入口", src="video.example.com", at="13:05", days=7,
         what="一段演示：给混合应用加上系统分享入口。",
         fact="时长 12 分 08 秒 · 有字幕",
         pts=["步骤和你现在的做法一致。", "唯一新的是第 9 分钟讲的共享容器权限。"],
         v=2, wag=""),
    dict(kind="截屏", icon="img", title="截屏 11-21 14.32", src="iPhone · 快捷指令", at="14:32", days=30,
         what="终端里一条证书链不完整的报错。",
         fact="图里有：一段报错、一个域名、三级证书的名字",
         pts=["报错指向中间证书缺失。", "第二级证书没有随服务器下发。"],
         v=1, wag=""),
    dict(kind="仓库", icon="file", title="example/durable-harness", src="github.com", at="11:48", days=30,
         what="一个让 agent 运行中断后能接着跑的框架：先写意图，再执行，最后写结果。",
         fact="TypeScript · 2.1k 星 · MIT · 上周还在更新",
         pts=["工具要声明自己能不能安全重放。", "不能重放的工具，中断后停下来问人。", "还是实验性的，接口会变。"],
         v=0, wag="你 11月16日 那篇笔记「同步冲突」里引用过它的上一版。"),
    dict(kind="帖子", icon="chat", title="我们把队列的租约从 5 分钟改成 30 秒之后……", src="某社交平台", at="10:17", days=30,
         what="一位工程师讲缩短租约之后重复执行反而变多的经过。",
         fact="作者 @queue_nerd · 某社交平台 · 一串 6 条",
         pts=["租约短于任务最长耗时，就会被别人抢走重做。", "他们最后改成短租约加续租。"],
         v=1, wag=""),
    dict(kind="文字", icon="text", title="先写意图，再执行，最后写结果", src="Mac · 剪贴板", at="09:40", days=7,
         what="一句摘抄，没有出处。",
         fact="86 字 · 没有原文链接",
         pts=["说的是操作日志的三段式写法。"],
         v=1, wag=""),
    dict(kind="文件", icon="clip", title="季度账单.pdf", src="iPhone · 分享", at="08:12", days=7,
         what="一份三页的季度账单。",
         fact="PDF · 3 页 · 214 KB",
         pts=["总额和上季度持平。", "多了一项年费，12 月扣款。"],
         v=2, wag=""),
]
FAILED = dict(kind="文章", icon="link", title="example.net 上的一页", src="example.net", at="15:02", days=30,
              what="没取到内容", fact="", pts=[], v=None, wag="")
VERDICT = [("值得深读", "honey ring"), ("知道就行", "ok"), ("可以略过", "off")]


def verdict_pill(v):
    t, c = VERDICT[v]
    return f'<span class="pill {c}">{t}</span>'


def kind_tag(f):
    return f'<span class="ty">{ic(f["icon"], 14)}{f["kind"]}</span>'


def stage1(f, st=0):
    """Just foraged: kind icon, title, where from, when, and the state mark (the pile of three shapes)."""
    tail = f'<div class="row mt8" style="gap:8px">{cell(0, 16)}<span class="xs">{STATE[0]}</span></div>'
    if st:
        tail = f'<div class="row mt8" style="gap:8px;flex-wrap:wrap">{cell(1, 16)}<span class="xs">交给 {bee_chip(SIPPER)}</span><span class="sp"></span>{life(f["days"], f["days"])}</div>'
    return (f'<div class="card bl"><div class="row top" style="gap:12px"><span class="thumb">{ic(f["icon"], 20)}</span><div class="col sp" style="min-width:0">'
            f'<span class="ti">{f["title"]}</span><span class="xs mt4">{f["kind"]} · {f["src"]} · {f["at"]} 存入</span></div></div>{tail}</div>')


def acts3(sm=True):
    return (f'<div class="acts"><span class="btn quiet sm">{ic("chat", 15)}深入对话</span>'
            f'<span class="btn ghost sm">不感兴趣</span><span class="btn ghost sm">看过了</span></div>')


def drop(f, acts=True, pts=3):
    """A drop: four fixed lines (what, fact, points, verdict), then the waggle if any, then three optional actions."""
    head = (f'<div class="row">{kind_tag(f)}<span class="xs">{f["src"]} · {f["at"]}</span><span class="sp"></span>'
            f'<span class="xs row g6">{ic("link", 13)}原文</span></div>')
    if f["v"] is None:
        return (f'<div class="card drop">{head}<div class="h3 mt8 mutc">没取到内容</div>'
                f'<p class="xs mt4">{bee_chip(SIPPER)} 去读的时候页面打不开。没有要点，也没有判定。</p></div>')
    p = "".join(f"<li>{x}</li>" for x in f["pts"][:pts])
    wag = (f'<div class="wag">{ic("pin", 14, "deep")}<span>{f["wag"]}</span></div>') if f["wag"] else ""
    return (f'<div class="card drop">{head}<div class="h3 mt8">{f["what"]}</div><div class="fact">{f["fact"]}</div>'
            f'<ul class="pts">{p}</ul><div class="row mt8">{verdict_pill(f["v"])}<span class="sp"></span>{bee_chip(SIPPER)}</div>'
            f'{wag}{acts3() if acts else ""}</div>')


# Swiping an item on a phone: right keeps it (queue it for digging), left drops it (not interested). Two actions, no more.
SWIPE = {"dig": ("chat", "加入深读队列"), "no": ("nope", "不感兴趣")}
SAY_DIGQ = "已加入深读队列"
SAY_NOPE = "已标为不感兴趣"
MARK_DIGQ = "已加入深读队列"


def swipe(card, side):
    """An item card half way through a swipe. side: dig (dragged right, the action shows on the left) | no (dragged left)."""
    i, t = SWIPE[side]
    return f'<div class="swipe {side}"><span class="act">{ic(i, 22)}{t}</span>{card}</div>'


def said_undo(text):
    """What a swipe says when it is done: one sentence and an undo."""
    return f'{ic("check", 18)}<span>{text}</span><span class="undo">撤销</span>'


def drop_done(f, mark):
    """A drop the user has dealt with: one quiet line, can be brought back."""
    return (f'<div class="li done" style="align-items:center"><span class="xs" style="flex:none">{mark}</span>'
            f'<span class="sm sp" style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{f["title"]}</span><span class="lk xs">挽回</span></div>')


def lesson_card(f):
    """In the evening lesson, worth digging: one sentence, the verdict, the three actions."""
    return (f'<div class="card"><div class="row">{kind_tag(f)}<span class="sp"></span>{verdict_pill(f["v"])}</div>'
            f'<div class="h3 mt8">{f["what"]}</div><div class="src mt4">{ic("link", 13)}<em>{f["title"]} · {f["src"]}</em></div>{acts3()}</div>')


def lesson_line(f, mark=""):
    return (f'<div class="li done" style="align-items:center">{ic(f["icon"], 15, "faint")}'
            f'<span class="sm sp" style="min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{f["title"]}</span>'
            f'<span class="xs" style="flex:none">{mark}</span><span class="lk xs" style="flex:none">挽回</span></div>')


SUMMARY = ("今天存入了 9 条。两条都在讲同一件事：一份活做到一半断了，怎么让别人安全地接着做。"
           "其余是一段你已经会的视频、一张报错截屏、一句摘抄和一份账单。")
REST = [(1, "可以略过"), (2, "知道就行"), (4, "看过了"), (5, "不感兴趣"), (6, "可以略过")]


def lesson_rest(open_=True):
    rows = "".join(lesson_line(FLOWERS[i], m) for i, m in REST) if open_ else ""
    return (f'<div class="fold"><div class="row"><span class="sm">其余的 · {len(REST)} 条</span><span class="sp"></span>'
            f'{ic("down" if open_ else "chev", 16, "faint")}</div>{rows}</div>')


def night(done=False):
    b = (f'<span class="btn quiet block">{ic("check", 18)}已标为读了 · 晚安</span>' if done
         else f'<span class="btn block">读了，晚安</span>')
    return (f'<div class="night"><div class="xs">睡前一问</div><p class="q">{NIGHT}</p>'
            f'<p class="xs">不用回答。带着它去睡。</p></div><div class="mt16">{b}</div>')


# The colony status bar, three widths. Same facts every time.
def sbar_wide(ok=True):
    if not ok:
        return (f'<div class="sbw bad"><span class="row g6"><span class="dot bad"></span><b>没有助手在干活</b></span>'
                f'<span>{bee_chip(SIPPER)} 3 天前来过</span><span>{bee_chip(RIPENER)} 5 天前来过</span><span class="sp"></span>'
                f'<span>14 条在等 · 最早的 11月24日 到期删除</span></div>')
    return (f'<div class="sbw"><span class="row g6"><span class="dot ok"></span><b>3 个助手在干活</b></span>'
            f'<span>{bee_chip(SCOUT)} 刚刚来过</span><span>{bee_chip(SIPPER)} 4 分钟前来过</span><span>{bee_chip(RIPENER)} 2 小时前来过</span>'
            f'<span class="sp"></span><span>今天存入了 9 条 · 4 条在等</span></div>')


def sbar_narrow(ok=True):
    if not ok:
        return '<div class="sbn"><span class="dot bad"></span><span>没有助手在干活 · 14 条在等</span></div>'
    return f'<div class="sbn"><span class="dot ok"></span><span>3 个助手在干活 · {SIPPER} 4 分钟前 · 今天 9 条，4 条在等</span></div>'


# ---------------------------------------------------------------- round 5: joining a client. The client shows a short code, KeepEssence allows it.
CODE = "KEEP-4827"
REV = '<span class="lk xs" style="margin-left:10px;flex:none">撤销</span>'


def code_box(code=CODE):
    return f'<div class="jcode">{code}</div>'


def join_wait(name, logo_html=""):
    """What the joining side shows (any client): its own name, the short code, where to allow it."""
    return (f'<div class="col" style="align-items:center;text-align:center">{logo_html}'
            f'<div class="h2 mt16">去 KeepEssence 里允许</div><p class="sm mt8" style="max-width:280px">在已登录的 KeepEssence 里会看到「{name} 想接入」。核对下面这个码，点「允许」。</p>'
            f'{code_box()}<p class="xs">10 分钟内有效 · 允许之后这里会自己继续</p></div>')


TIERS = [("只存入", "看不到内容"), ("读", "能读、能处理"), ("管理", "还能管助手设置和设备")]


def tier_pick(asked, chosen=None):
    """The three tiers on the allow page. asked: what the client requested (0..2). Higher than asked is not offered."""
    chosen = asked if chosen is None else chosen
    return ('<div class="tier">' + "".join(
        f'<span class="{"on" if i == chosen else ("no" if i > asked else "")}"><b>{t}</b>{d}</span>' for i, (t, d) in enumerate(TIERS)) + '</div>')


def check(t, on=True):
    return f'<span class="chk{" on" if on else ""}"><i>{ic("check", 13) if on else ""}</i>{t}</span>'


def join_allow(name, kind, can, cannot="", steps="", warn=False, tier=None, chosen=None, product=""):
    """The allow page on a manager device.
    A client: who wants in, the same short code it shows, and a tier.
    A bee (product given): which product wants in, a name for the bee (prefilled, editable), a checkbox per step. No short code."""
    w = (f'<div class="card tint mt12"><div class="row top">{ic("warn", 18, "warnc")}<p class="sm" style="color:var(--ink);text-align:left"><b>内容会被送到这个助手运行的地方。</b>'
         f'交给它的内容、解读、每日摘要和笔记都会离开 KeepEssence。</p></div></div>') if warn else ""
    foot = (f'<div class="row mt16"><span class="btn ghost sp">不允许</span><span class="btn sp">允许</span></div>'
            f'<p class="xs mt12">以后可以在 助手设置 › 设备 里改名、改权限或撤销。</p>')
    if product:
        if isinstance(steps, str):
            steps = [(t, True) for t in steps.split('、')]
        boxes = "".join(check(t, on) for t, on in steps)
        only = '<p class="xs mt8">对话里的助手只在你和它聊的时候干活，所以只有深入对话，不能精读。</p>' if kind == K_CHAT else ""
        return (f'<div class="h2">{product} 想接入</div><p class="sm mt4">是你刚才在{" " if product[0].isascii() else ""}{product} 那边发起的，才点允许。</p>'
                f'<div class="card mt12" style="text-align:left"><div class="xs">给这个助手起个名字</div>'
                f'<div class="inp row mt4"><b class="sp">{name}</b><span class="xs">可以改</span></div>'
                f'<div class="row mt12"><span class="xs">它可以干哪几步</span><span class="sp"></span>{kind_pill(kind)}</div>'
                f'<div class="row mt8" style="gap:18px;flex-wrap:wrap">{boxes}</div>{only}</div>{w}{foot}')
    rows = f'<div class="kv"><span>名称</span><b>{name}</b></div><div class="kv"><span>种类</span><span>{kind}</span></div>'
    perm = ""
    if tier is not None:
        perm = (f'<div class="xs mt12" style="text-align:left">给它的权限 · 它请求的是「{TIERS[tier][0]}」，可以调低</div>{tier_pick(tier, chosen)}')
    else:
        rows += f'<div class="kv"><span>它能做</span><span>{can}</span></div>'
    return (f'<div class="h2">「{name}」想接入</div><p class="sm mt4">和它那边显示的码一样，才点允许。</p>{code_box()}'
            f'<div class="card" style="text-align:left;padding:2px 16px">{rows}</div>{perm}{w}{foot}')


# name, icon, kind, tier or steps, last used
DEVICES = [("iPhone · App", "device", "客户端", "管理", "今天 20:51"), ("Chrome · 这台 Mac", "img", "客户端", "管理", "刚刚"),
           ("阿读", "bee", "助手 · 定时来的", "解读、汇总、精读、深入对话", "4 分钟前"), ("阿深", "bee", "助手 · 对话里的", "深入对话", "2 小时前"),
           ("墨水屏阅读器", "book", "客户端", "读", "昨天 22:10"), ("iPhone · 快捷指令", "device", "客户端", "只存入", "今天 20:58"),
           ("Chrome 扩展 · Mac", "img", "客户端", "只存入", "今天 15:12"), ("Firefox 扩展 · Mac", "img", "客户端", "只存入", "11月19日")]


def device_rows(n=None, only_mgr=False):
    out = ""
    for name, i, kind, can, when in DEVICES[:n]:
        client = kind == "客户端"
        perm = f'<span class="sel xs" style="flex:none">{can}{ic("down", 13, "faint")}</span>' if client else ""
        sub = f'{kind} · 上次使用 {when}' if client else f'{kind} · {can} · 上次使用 {when}'
        out += (f'<div class="li" style="align-items:center"><span class="thumb">{ic(i, 20)}</span><div class="col sp" style="min-width:0"><b>{name}</b>'
                f'<span class="xs">{sub}</span></div>{perm}<span class="lk xs" style="flex:none;margin-left:10px">改名</span>{REV}</div>')
    return out


def last_mgr_note():
    return (f'<div class="card tint"><div class="row top">{ic("warn", 18, "warnc")}<p class="sm" style="color:var(--ink)"><b>这是最后一台管理档的设备。</b>'
            f'它不能降档，也不能撤销。先把另一台设备提到管理档，再回来动它。</p></div></div>')


def perm_table():
    rows = [("存入东西", 1, 1, 1, 0), ("读今天、每日摘要、笔记", 0, 1, 1, 0), ("深入对话、不感兴趣、看过了、读了", 0, 1, 1, 0),
            ("看今日状态：谁在干活", 0, 1, 1, 0), ("改一个条目「交给谁」「活多久」", 0, 0, 1, 0), ("管理助手设置和规则", 0, 0, 1, 0),
            ("允许新设备接入", 0, 0, 1, 0), ("给设备改名、改权限、撤销", 0, 0, 1, 0), ("取分给它的活、交回结果", 0, 0, 0, 1)]
    body = "".join(f'<tr><td>{r[0]}</td>' + "".join(f'<td class="{"y" if v else "n"}">{"✓" if v else "—"}</td>' for v in r[1:]) + '</tr>' for r in rows)
    return f'<table class="perm"><tr><th>功能</th><th>只存入</th><th>读</th><th>管理</th><th>助手</th></tr>{body}</table>'


def revoke_confirm(name="Firefox 扩展 · Mac"):
    return (f'<div class="h2">撤销「{name}」？</div><p class="sm mt8">它马上就不能再存入了。别的设备不受影响。想再用，在它那边重新接入一次。</p>'
            f'<div class="row mt16"><span class="btn ghost sp">取消</span><span class="btn sp" style="background:var(--bad);color:#fff">撤销</span></div>')


# ---------------------------------------------------------------- round 9: joining a bee. An address to paste, then the allow page. No short code.
K_SCHED, K_CHAT = "定时来的", "对话里的"
ADDR = "keepessence.app/mcp"          # the same for everyone; not a credential
ALL3 = "解读、汇总、精读、深入对话"       # the name is historical: it used to be three steps
SELF = "自己部署的 agent"

# product, kind, what it can do, the small note
PRODUCTS = [("Claude", K_CHAT, "深入对话", "各套餐都能接；能把笔记存回来"),
            ("ChatGPT", K_CHAT, "深入对话", "在网页上接；个人套餐只能读，笔记由你贴回来"),
            ("Gemini", K_CHAT, "深入对话", "目前只限美国、英文、个人账号"),
            ("Muse", K_SCHED, ALL3, "待验证"),
            (SELF, K_SCHED, ALL3, "支持 MCP 和 OAuth 的都行")]
# which product each of our sample bees runs in
BEES = {SIPPER: ("Muse", K_SCHED), RIPENER: ("Claude", K_CHAT)}

# product -> (steps, footnote). Muse has none yet: it is drawn as a "to be verified" card.
GUIDES = {
    "Claude": (["打开 Claude 的「Connectors」，点 Add → Add custom connector。",
                "名字填 KeepEssence，地址粘贴上面的接入地址。",
                "认证保持它自动检测到的选项，点 Add，再点 Connect。",
                "浏览器打开 KeepEssence 的允许页，点「允许」。"], ""),
    "ChatGPT": (["在电脑上打开 chatgpt.com/plugins，点 + → Add custom MCP server。",
                 "名字填 KeepEssence，Server URL 粘贴接入地址，认证选 OAuth。",
                 "看过风险提示后确认，点 Create as a plugin，再安装它。",
                 "浏览器打开 KeepEssence 的允许页，点「允许」。"],
                "手机上不能接。个人套餐只能读：聊完把结果贴回 KeepEssence。"),
    "Gemini": (["在电脑上打开 gemini.google.com → Settings → Connected Apps。",
                "在 Custom apps 下点 Add a custom app，粘贴接入地址，点 Next。",
                "浏览器打开 KeepEssence 的允许页，点「允许」。",
                "之后在手机和网页上都能用；对话里输入 @ 选 KeepEssence。"],
               "目前只限美国、18 岁以上、个人 Google 账号、英文，并且要开着 History。存回笔记时 Gemini 每次都会让你确认。"),
    SELF: (["在你的 agent 里添加一个 MCP 服务器，地址粘贴上面的接入地址。",
            "认证选 OAuth。",
            "浏览器打开 KeepEssence 的允许页，点「允许」。"], ""),
}
UNVERIFIED = "Muse 能连上 KeepEssence，但它能不能走允许页这一步还没验证。验证后这里会有步骤。"


def kind_pill(kind):
    """The small label that says which of the two kinds a bee is."""
    return f'<span class="pill plain">{kind}</span>'


def product_row(p, on=False):
    """One product in the 'connect a bee' list: name, kind, what it can do, a small note. Generic glyph, never a logo."""
    name, kind, can, note = p
    return (f'<div class="li prod{" on" if on else ""}" style="align-items:center"><span class="thumb">{ic("clock" if kind == K_SCHED else "chat", 20)}</span>'
            f'<div class="col sp" style="min-width:0"><span class="row g6"><b>{name}</b>{kind_pill(kind)}</span>'
            f'<span class="sm" style="color:var(--ink)">能做：{can}</span><span class="xs">{note}</span></div>{ic("chev", 16, "faint")}</div>')


def product_list(on=None):
    return ('<div class="lst">' + "".join(product_row(p, p[0] == on) for p in PRODUCTS) + '</div>')


KINDS_NOTE = "「对话里的」只在你去找它的时候干活，只能深入对话。「定时来的」自己按时来取活，解读、汇总、精读都能做，也能深入对话。"


def addr_box():
    """The one thing the user copies when connecting a bee."""
    return (f'<div class="xs">接入地址 · 人人都一样，不是密码</div>'
            f'<div class="urlrow mt4"><em>{ADDR}</em><span class="lk xs" style="flex:none;font-family:system-ui">复制</span></div>')


def step_list(steps):
    return '<ol class="steps">' + "".join(f"<li><span>{t}</span></li>" for t in steps) + '</ol>'


def guide(product):
    """The step-by-step guide for one product: what it is, the address to copy, the numbered steps, a footnote."""
    name, kind, can, note = next(p for p in PRODUCTS if p[0] == product)
    head = (f'<div class="row" style="flex-wrap:wrap"><span class="h2">接入 {name}</span>{kind_pill(kind)}</div>'
            f'<p class="sm mt4">能做：{can}</p>')
    if product not in GUIDES:
        return (f'{head}<div class="card tint mt16"><div class="row"><span class="pill warn">待验证</span></div>'
                f'<p class="sm mt8" style="color:var(--ink)">{UNVERIFIED}</p></div>')
    steps, foot = GUIDES[product]
    return (f'{head}<div class="mt16">{addr_box()}</div><div class="mt16">{step_list(steps)}</div>'
            + (f'<p class="xs mt16">{foot}</p>' if foot else "")
            + '<p class="xs mt12">点了允许，这个助手就出现在助手设置里。</p>')


# ---------------------------------------------------------------- round 9: digging. Pick a bee, then go and talk where it lives.
DIG_T = "把超时做成租约"
OPENING = f"深入对话 KeepEssence 里的这一条：{DIG_T}"
SAVED = f"已交回 KeepEssence：《{DIG_T}》"


def opening_box():
    """The opening line to paste into the assistant, when it cannot be opened by a link."""
    return f'<div class="obox"><span class="sp">{OPENING}</span><span class="lk xs" style="flex:none">复制</span></div>'


def dig_pick(mode="link"):
    """The sheet behind 「深入对话」: queue it (an assistant reads it closely meanwhile), or go and dig now; then who.
    mode: read (queue it; only a scheduled assistant can read on its own) | link (dig now, with a chat assistant we can open
    by link) | copy (dig now, with one we cannot open, or a phone app). 'sched' is the old name of read."""
    read = mode in ("read", "sched")
    prod = "Gemini" if mode == "copy" else "Claude"
    seg = (f'<span class="seg" style="display:flex"><span class="sp{" on" if read else ""}" style="text-align:center">排入队列，先{STEP_READ}</span>'
           f'<span class="sp{"" if read else " on"}" style="text-align:center">现在去{STEP_DIG}</span></span>')
    bees = [(RIPENER, prod, K_CHAT), (SIPPER, "Muse", K_SCHED)]
    if read:
        bees.reverse()

    def row(i, n, p, k):
        off = read and k == K_CHAT
        note = f"不能{STEP_READ}" if off else ("缺省" if i == 0 else "")
        return (f'<div class="pk{" on" if i == 0 else ""}{" off" if off else ""}"><i></i>{bee_chip(n)}<span class="xs sp">· {p} · {k}</span>'
                + (f'<span class="xs">{note}</span>' if note else "") + '</div>')
    rows = "".join(row(i, *b) for i, b in enumerate(bees))
    if read:
        tail = (f'<div class="mt16"><span class="btn block">加入深读队列</span></div>'
                f'<p class="xs mt8">等{SIPPER}下一次来取活。读好了可以看，再决定去不去{STEP_DIG}。</p>')
    elif mode == "link":
        tail = (f'<div class="mt16"><span class="btn block">{ic("chat", 18)}去 {prod} {STEP_DIG}</span></div>'
                f'<p class="xs mt8">会打开一场新对话，开场话已经填好，你按发送就开始。</p>')
    else:
        tail = (f'<div class="xs mt16">开场话 · 复制后贴到对话里</div><div class="mt4">{opening_box()}</div>'
                f'<div class="mt12"><span class="btn block">打开 {prod}</span></div>')
    return (f'<div class="h2">深入对话</div><p class="sm mt4">{DIG_T}</p><div class="mt12">{seg}</div>'
            f'<p class="xs mt8">{READ_SAYS if read else DIG_SAYS}</p>{rows}{tail}')


# what the assistant hands back for a queued item: a close reading. It belongs to the queue entry, it is not a note.
READ_PTS = ["原文的主张：别给一份活定一个死的超时，改成会过期、能续的租约。",
            "它没说的：续租的那边卡住时，过期的那份交回来要被拒掉，不然会重复。",
            "和你 11月20日 那篇笔记「认领、租约和重放」说的是同一套设计的两半。"]
READ_FOUND = ["Leases in job queues · blog.example.dev/leases", "Fencing tokens, explained · db.example.org/fencing",
              "example/durable-harness 的 issue #214 · github.com"]


def read_page():
    p = "".join(f"<li>{x}</li>" for x in READ_PTS)
    f = "".join(f'<div class="src mt4">{ic("link", 13)}<em>{t}</em></div>' for t in READ_FOUND)
    q = "".join(f"<li>{x}</li>" for x in DIG)
    return (f'<div class="row">{ripen_pill("ready")}<span class="sp"></span>{bee_chip(SIPPER)}</div>'
            f'<div class="h1 mt8" style="font-size:22px">{DIG_T}</div><p class="xs mt4">{STEP_READ} · 今天 22:40 · 读了原文，另外查了 6 处</p>'
            f'<div class="lab">读出来的</div><ul class="pts">{p}</ul><div class="lab">另外查到的</div>{f}'
            f'<div class="lab">可以接着问的</div><ul class="pts">{q}</ul>'
            f'<div class="mt16"><span class="btn block">{ic("chat", 18)}去{STEP_DIG}</span></div>'
            f'<p class="xs mt8">{STEP_READ}跟着队列里的这一条走，不是笔记。去深入对话时助手会带上它；有笔记存回来才会留下。7 天没有动静，它和这一条一起移出队列。</p>')


# the conversation on the assistant's side: (mine?, text)
CHAT = [(1, OPENING),
        (0, f"我从 KeepEssence 取到了这一条：<b>{DIG_T}</b>（11月21日 每日摘要）。<br>它说的是：别给一份活定一个死的超时，改成会过期、能续的租约。<br>相关的还有你 11月20日 那篇笔记「认领、租约和重放」。从哪开始？"),
        (1, "租约定多长合适？"),
        (0, "比一次心跳长几倍就行，比如 30 秒，干活的那边每 10 秒续一次。活本身要跑多久不用管，还活着就一直续。"),
        (1, "续租的那边卡住了怎么办？"),
        (0, "租约到期，别人就能领走重做。所以交回时要带上领活时拿到的编号，过期的那一份交回来会被拒掉。"),
        (1, "存成笔记"),
        (0, SAVED)]


# digging, at the assistant's place, with the close reading in hand: it searches again and runs something of its own. 2 = what it did there.
CHAT_DEEP = [(1, f"带着{SIPPER}的精读和深入对话：{DIG_T}"),
             (0, f"我取到了这一条和{SIPPER}的精读。精读里留了三个问题，从第一个开始？"),
             (1, "先去查一下别的队列是怎么定租约的"),
             (2, "查了 14 个来源，用了 3 分钟"),
             (0, "常见的是 30 秒到 5 分钟，都配续租。租约短又不续的，重复执行反而变多。"),
             (1, "照这个把我们仓库里的超时配置扫一遍"),
             (2, "跑了它那边预先配好的脚本"),
             (0, "扫到 3 处写死的超时，都没有续租。"),
             (1, "不用存了，我知道了")]


def assist_chat(a=0, b=None, draft="", first="", msgs=None):
    """The assistant's own place, drawn as a neutral chat. a, b: which turns to show; draft: text sitting in the input box."""
    msgs = msgs or ([(1, first)] + CHAT[1:] if first else CHAT)
    bubs = "".join(f'<div class="did">{ic("check", 13)}{t}</div>' if me == 2 else f'<div class="bub{" me" if me else ""}">{t}</div>' for me, t in msgs[a:b])
    box = f'<span class="sp">{draft}</span>' if draft else '<span class="sp ph">说点什么</span>'
    return (f'<div class="achat"><div class="col g10 msgs">{bubs}</div>'
            f'<div class="composer">{box}<i>{ic("chev", 16)}</i></div></div>')


def paste_back(title="墨水屏上的排版要不要自己调字重"):
    """Giving honey back by hand, for an assistant that cannot write to KeepEssence."""
    return (f'<div class="h2">把结果贴回来</div><p class="xs mt4">ChatGPT 的个人套餐不能替你存，从对话里复制结果贴在这里。</p>'
            f'<div class="xs mt12">标题</div><div class="inp mt4">{title}</div>'
            f'<div class="xs mt12">结果</div><div class="inp area mt4" style="min-height:190px">正文字重不用动，系统给的 400 在墨水屏上够黑。要调的是小字：12 号以下一律用 500，不然笔画会断。<br><br>'
            f'行长控制在 28 到 32 个字。灰阶只留两档，说明文字不用灰，改用小一号。</div>'
            f'<div class="row mt16"><span class="btn ghost sp">取消</span><span class="btn sp">{ic("jar", 18)}存成笔记</span></div>')


# ---------------------------------------------------------------- round 7: the comb (one month, one cell per day)
from mocklib import hive  # noqa: E402

# November up to the 21st: a month in steady use
MONTH = [3, 3, 0, 3, 4, 3, 3, 3, 4, 0, 3, 3, 3, 3, 0, 4, 3, 3, 3, 4, 2]
MONTH_NEW = [0, 0, 1, 3, 0, 2]                       # just started
MONTH_BUSY = [3, 4, 3, 3, 4, 3, 3, 4, 3, 3, 3, 4, 3, 3, 4, 3, 3, 3, 4, 3, 3, 4, 3, 3, 3, 4, 3, 3, 4, 3]
MONTH_OCT = [3, 3, 3, 0, 0, 3, 4, 3, 3, 0, 3, 3, 3, 4, 3, 0, 0, 0, 3, 3, 3, 3, 4, 3, 0, 3, 3, 3, 3, 3, 4]
MONTH_NONE = [0] * 18


def hive_bg(days=None):
    return f'<div class="hivebg">{hive(MONTH if days is None else days, 11)}</div>'


def hive_legend():
    one = lambda st, t: f'<span>{hive([st], 9, today=False)}{t}</span>'
    return ('<div class="legend">' + one(0, "没有条目") + one(1, "存入了条目") + one(2, "有每日摘要，没读") + one(3, "读了") + one(4, "留下了笔记") + '</div>')


def hive_page(days=None, title="11月", nums=("148", "17", "16", "5"), prev="10月", nxt="", note=""):
    days = MONTH if days is None else days
    n = "".join(f'<div><b>{v}</b><span>{l}</span></div>' for v, l in zip(nums, ["存入了（条）", "每日摘要（份）", "读了（份）", "笔记（篇）"]))
    nav = (f'<div class="row"><span class="lk sm">{ic("back", 15)}{prev}</span><span class="sp"></span><span class="h2">{title}</span><span class="sp"></span>'
           f'<span class="{"lk" if nxt else "xs"} sm">{nxt or "　　"}</span></div>')
    return (f'{nav}<div class="col mt16" style="align-items:center">{hive(days, 23, today=not nxt)}</div><div class="hivenums">{n}</div>'
            f'<div class="mt16">{hive_legend()}</div><p class="xs mt12">{note or "一天一个点。点一下打开那天的每日摘要；那天没有每日摘要就点不动。"}</p>')


# ---------------------------------------------------------------- round 8: the comb as an image with an address
from mocklib import logo  # noqa: E402

HIVE_URL = "keepessence.app/comb/k7Qm2xRv9TdL.svg"
YEAR = [("12", MONTH_OCT[:31]), ("1", MONTH_NONE + [0] * 13), ("2", MONTH_NEW + [0, 3, 3, 0, 3, 4, 3, 0, 0, 3, 3, 3, 0, 3, 3, 4, 3, 0, 3, 3, 3, 0]),
        ("3", MONTH_OCT), ("4", MONTH_BUSY), ("5", MONTH_OCT[::-1]), ("6", MONTH_BUSY), ("7", MONTH_OCT), ("8", MONTH_BUSY[::-1]),
        ("9", MONTH_OCT[::-1]), ("10", MONTH_OCT), ("11", MONTH)]


def hive_img(theme="light", year=False, nums=True, mark=True, r=13):
    """The picture the address returns: cells only, optionally the counts and a small mark. No titles, no names."""
    if year:
        pic = '<div class="yr">' + "".join(f'<div>{hive(d, 2.6, today=False)}<span>{m}月</span></div>' for m, d in YEAR) + '</div>'
        n = "近十二个月 · 存入了 1,640 条 · 读了 201 份每日摘要 · 留下 52 篇"
    else:
        pic = hive(MONTH, r)
        n = "11月 · 存入了 148 条 · 读了 16 份每日摘要 · 留下 5 篇"
    num = f'<span class="hn">{n}</span>' if nums else ""
    mk = ('<span class="mk">' + logo("simple", 16) + '</span>') if mark else ""
    return f'<div class="himg {theme}">{pic}{num}{mk}</div>'


def my_hive(on=True, preview=True):
    if not on:
        return (f'<div class="col" style="align-items:center;opacity:.5">{hive_img(nums=False, mark=False)}</div>'
                f'<div class="card mt16"><div class="row"><div class="col sp"><b>图片地址</b><span class="xs">关着。打开后任何拿到地址的人都能看到这张图。</span></div><span class="tog"></span></div></div>'
                f'<p class="xs mt12">图里只有圆点和数字，没有你存的任何内容，也没有你的名字。可以贴到个人主页、文档、桌面小组件里，它会自己更新。</p>')
    seg = lambda items, k: '<span class="seg">' + "".join(f'<span class="{"on" if i == k else ""}">{t}</span>' for i, t in enumerate(items)) + '</span>'
    top = f'<div class="col" style="align-items:center;margin-bottom:14px">{hive_img(r=11)}</div>' if preview else ""
    return (f'{top}<div class="card" style="padding:4px 16px"><div class="kv"><span style="color:var(--ink)"><b>图片地址</b></span><span class="tog on"></span></div>'
            f'<div style="padding:10px 0"><div class="urlrow"><em>{HIVE_URL}</em><span class="lk xs" style="flex:none;font-family:system-ui">复制</span></div>'
            f'<div class="row mt8"><span class="lk xs">换一个地址</span><span class="xs">旧的立刻失效</span><span class="sp"></span><span class="xs">也有 .png</span></div></div></div>'
            f'<div class="card mt12" style="padding:2px 16px"><div class="kv"><span>底色</span>{seg(["浅色", "深色", "透明"], 0)}</div>'
            f'<div class="kv"><span>范围</span>{seg(["这个月", "十二个月"], 0)}</div>'
            f'<div class="kv"><span>带数字</span><span class="tog on"></span></div><div class="kv"><span>带标志</span><span class="tog on"></span></div></div>'
            f'<p class="xs mt8">图里没有你存的内容和名字。不登录就能看，会自己更新。</p>')


def embeds():
    bar = '<div class="bar"><i></i><i></i><i></i></div>'
    ln = lambda w: f'<div class="ln" style="width:{w}%"></div>'
    home = (f'<div class="emb" style="width:420px">{bar}<div class="pad"><div class="row" style="display:flex;gap:14px;align-items:center">'
            f'<span style="width:54px;height:54px;border-radius:50%;background:#e7e4dd;display:block;flex:none"></span><div style="flex:1">{ln(40)}{ln(64)}</div></div>'
            f'<div style="margin-top:16px;display:flex;justify-content:center">{hive_img(r=11)}</div>{ln(90)}{ln(72)}</div></div>')
    doc = (f'<div class="emb" style="width:420px">{bar}<div class="pad"><div style="font:600 18px/1.3 Georgia,serif">这个月读了什么</div>{ln(92)}{ln(80)}'
           f'<div style="margin:14px 0;display:flex;justify-content:center">{hive_img("clear", nums=False, mark=False, r=11)}</div>{ln(88)}{ln(55)}</div></div>')
    widget = (f'<div style="width:420px;height:300px;border-radius:14px;background:linear-gradient(135deg,#3b4a5a,#1e2630);display:flex;align-items:center;justify-content:center;gap:18px">'
              f'<div style="border-radius:22px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.4)">{hive_img("dark", nums=False, r=10)}</div>'
              f'<div style="width:120px;height:120px;border-radius:22px;background:rgba(255,255,255,.14)"></div></div>')
    cap = lambda t, d: f'<div style="margin-top:10px"><b style="font-size:14px">{t}</b><div class="xs">{d}</div></div>'
    return (f'<div>{home}{cap("个人主页", "浅色，带数字和标志")}</div><div>{doc}{cap("文档里", "透明底，不带数字")}</div>'
            f'<div>{widget}{cap("桌面小组件", "深色")}</div><div style="width:520px">{hive_img(year=True)}{cap("十二个月的版式", "十二个小月历排成一排")}</div>')
