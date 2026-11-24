# KeepEssence spec

KeepEssence 的产品规格、接口契约和 UX mock。所有平台照这里做；冲突时以这里为准。
Product spec, API contract and UX mocks for KeepEssence. Every platform builds against this repo.

| 路径 | 内容 |
|---|---|
| [`product/`](product/README.md) | 产品规格。干活前先读这里，按 README 里的顺序读 |
| [`contract/`](contract/README.md) | 接口契约，手写的 OpenAPI 3.1，接口的唯一来源 |
| [`product/acceptance.md`](product/acceptance.md) | v1.0 内测的验收标准 |
| [`design/tokens.css`](design/tokens.css)、[`design/terms.md`](design/terms.md) | 各客户端共用的颜色、圆角、字号，和界面用词的中英对照 |
| [`design/mock/`](design/mock/README.md) | 各客户端的 UX mock，浏览器打开 `index.html` 看 |

## 其他仓库

| 仓库 | 内容 |
|---|---|
| [core](https://github.com/KeepEssenceApp/core) | 核心（服务器） |
| [web](https://github.com/KeepEssenceApp/web) | 网页客户端 |
| [extension](https://github.com/KeepEssenceApp/extension) | 浏览器扩展 |
| [agents](https://github.com/KeepEssenceApp/agents) | 助手接入 |
| [site](https://github.com/KeepEssenceApp/site) | 官网 |

## 怎么改规格

- 改产品行为、规则、术语：在这里提 issue 或 PR。
- 改接口：只在 `contract/` 改，合并后 core 和各客户端再跟。
- 文中的「open #N」指维护者内部的待定事项清单，不在本仓库；每条都有缺省做法写在规格里。
- 文中提到的 `brand/`（品牌资料）和数据保留说明暂未公开。

贡献方式见 [贡献指南](https://github.com/KeepEssenceApp/.github/blob/main/CONTRIBUTING.md)。许可证：[AGPL-3.0](LICENSE)。
