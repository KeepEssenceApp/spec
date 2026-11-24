# contract：接口契约

状态：还没写。

这里放手写的 OpenAPI 3.1，是接口的唯一来源。对外三组接口都在同一份契约里：攒存、读、助手（REST 与 MCP 工具一一对应）。各平台的类型和 MCP 工具清单从它生成。

写之前先读：

- [`product/techspec.md`](../product/techspec.md) §3：客户端的接口清单。
- [`product/architecture.md`](../product/architecture.md) §4：助手的接口清单。
- [`product/platforms.md`](../product/platforms.md)「核心」一节：对契约的要求。

规则：

- 攒存的契约只有两样：授权、保存。定下后不再改动。
- 改契约时在持续集成里自动比对新旧版本，并重放已发布客户端的请求样本。
