# contract：接口契约

[`openapi.yaml`](openapi.yaml) 是接口的唯一来源，手写的 OpenAPI 3.1。核心和各客户端都照它做；接口不在别处定。

## 里面有什么

| 部分 | 内容 |
|---|---|
| `paths` | 三组接口：攒存、读、助手。另有授权服务器（`/oauth/*`、`/.well-known/*`）、助手端点（`/mcp`）、公开的月历图（`/c/*`） |
| `x-tier` | 客户端接口需要的权限档：`save`（只存入）、`read`（读）、`manage`（管理） |
| `x-mcp-tool` | 标了它的助手接口同时是 MCP 工具，输入输出相同。`x-mcp-readonly` 是只读工具 |
| `x-error-codes` | 全部错误码 |
| `x-limits` | 全部数字：寿命、认领期限、大小上限、合并通知的等待时间等 |
| `x-shared-rules` | 各客户端共用的规则，只有这一份：像密码的内容怎么识别、存入完的那一句话（和它后面接的说明：存下来的和用户给的不一样时，`save_notes`）、判定的叫法、通知的措辞、开场话。核心经 `GET /v1/meta` 发给客户端 |

## 版本

契约的大版本号就是路径里的 `/v1`。各模块（core、web、extension、agents、ios）的大版本号和它对齐。有破坏性改动时出 `/v2`，所有模块一起升大版本；旧版本一直认，直到走完弃用步骤（规则 C4）。

## 和规格的出入

写契约时定下的，规格里没有或不一样的地方：

| 项 | 契约的做法 | 原因 |
|---|---|---|
| 登录 | `POST /v1/auth/email-codes`、`POST /v1/auth/sessions`：受邀邮箱收验证码，登录的设备是管理档 | 规格只说「登录直接得到管理档」，没写怎么登录 |
| 短码轮询 | 建短码时另给一个 `poll_secret`，轮询时带上 | 短码会显示在屏幕上，不能凭它取到凭据 |
| 接入助手 | 没有 `POST /v1/assistants`。助手只经允许页接入（`/oauth/authorize` → `/v1/oauth/requests/*`） | 规则 B8、D9：接入只有「点允许」一个动作 |
| 深挖队列 | 加了 `GET /v1/deep-read-queue` | 笔记页要列出队列 |
| 状态栏 | 加了 `GET /v1/status` | 规格把它和数量放在一起，这里分开 |
| 汇总的上下文 | `GET /v1/assistant/digests/{day}/context` | 汇总的活不是一个条目 |
| 助手查找 | `GET /v1/assistant/search`（工具 `search_digests_and_notes`） | 规格写了「助手可以在每日摘要和笔记里按文字查找」，没给接口 |
| 上传地址 | `upload_url` 指向核心自己，带签名和期限 | 效果同预签名地址；不需要另配 R2 的访问密钥 |
| 月历图 | 只有 SVG | PNG 还没做 |
| 提醒 | 没有「有活了」的接收地址 | 规则 D2 写的是「可以」，v1.0 先不做 |
| 用词 | 字段里叫 `credential`，不叫 token | 词表的「不用的词」 |

## 校验

```
npx @redocly/cli lint contract/openapi.yaml
```
