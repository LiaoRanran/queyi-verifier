# queyi-verifier（阙疑验证器 · 独立仓库）

> 本仓库由 **657 A 段（仓库拆分）** 从 [`CPP-Bible`](https://github.com/LiaoRanran/CPP-Bible) 拆出。
> 目标：把「阙疑验证器」（四态判决 / Merkle 信任根 / 账本哈希链 / 变异测试 / 证据 replay / 门禁引擎 /
> 保护器 / 前端）从书籍仓库独立成可单独克隆、单独运行、单独 CI 的仓库。

## 划分边界（657 A1）

- **搬入本仓库**：`tools/`（核心工具）、`tests/`（测试）、`web/`（前端）、技术文档（`docs/` 的
  UVK 纲领 / 判决规格 / ARCHITECTURE / 信任终止 / Rust 边界）、配置（`queyi.toml` / `pyproject.toml`）、
  `LICENSE` / `README` / `.github/`。
- **留在 CPP-Bible（数据与笔记）**：`atoms/`（卡片源）、`data/` 下的历史报告（652_gaps / 验收报告等）。
  验证器运行所需的 `data/`（变异基线、账本、Merkle 根等）与 `atoms/` 通过**可配置路径**引用 CPP-Bible。

## 独立可运行（657 A3 · 已验证）

本机实测：

```powershell
cd C:\CodeLearnling\queyi-verifier
python tools/boundary_backfill_657.py --check     # PASS
python -m pytest tests/test_boundary_backfill_657.py tests/test_core_pbt_656.py -q   # 76 passed
python tools/run_656_gate.py --fast-only           # 门禁可跑（见 tools/run_656_gate.py）
```

> **路径可配置机制（当前实现）**：`tools/` 仍按 `ROOT/<dir>` 解析；本仓库用
> `New-Item -ItemType Junction` 把 `data/` 与 `atoms/` 指到 `queyi.toml` 里声明的 CPP-Bible 路径
> （Windows `mklink /J` 等价物；Linux/macOS 用 `ln -s`）。这样**不改任何工具代码**即可独立运行。
>
> **生产化 TODO**：把 `tools/` 的路径解析改为读取 `queyi.toml` 的 `data_path`/`atoms_path`
> （或环境变量 `QUEYI_DATA`/`QUEYI_ATOMS`），去掉对 junction 的依赖——属拆分收尾，不阻塞本批验证。

## 目录

```
queyi-verifier/
├── tools/         # 验证器核心（四态判决 / Merkle / 账本 / 变异 / replay / 门禁 / 保护器 / 前端工程化）
├── tests/         # 工具链回归测试
├── web/           # 星图 / 验哈希 / 学习 MVP 前端
├── docs/          # 技术文档（UVK / 判决规格 / ARCHITECTURE / 信任终止 / Rust 边界）
├── queyi.toml     # 数据/卡片路径配置（指向 CPP-Bible）
├── pyproject.toml # ruff / mypy / pytest 配置（从 CPP-Bible 同步）
├── data/          # junction → CPP-Bible/data（不入库）
└── atoms/         # junction → CPP-Bible/atoms（不入库）
```

## 与 CPP-Bible 的关系

- CPP-Bible **保留** `atoms/`、`data/` 与书籍源；其 `tools/` 是否删除见下方「收尾状态」。
- 本仓库是验证器的**唯一演进地**；CPP-Bible 后续只消费验证器产出（边界三元组 / 信任根 / 验收报告）。

## 收尾状态（657 诚实登记）

- ✅ 新仓库脚手架 + 独立可运行验证（A2/A3）：**完成**。
- ⏳ 从 CPP-Bible **删除** `tools/`（A2 后半）：**未做**——删除会破坏 CPP-Bible 的
  在仓门禁 `run_656_gate.py`（它 import `tools/`）与本批 657 D 段全部工具，须先于删除把
  门禁迁到本仓库并验证，故列为后续动作（详见 CPP-Bible 的 `data/657_acceptance_report.md`）。
- ⏳ 双仓 **push**（A4）：**未做**——需先在 GitHub 建 `QueYi/queyi-verifier` 仓库（外部动作），
  本批不代建、不代 push（与「不代签 DCO / 不代签 VSA 凭证」同一纪律）。
