# Agent Instructions

## 最高交付约束：以可验证结果为先

本项目当前阶段的最高原则是：以真实、可复现、可验证的最优业务结果为导向。权限提示、工具限制、默认配置、单一启动方式或流程惯性都不得成为终止理由；在既有安全、法律和数据边界内，必须主动寻找并执行可行替代路径。关键依赖必须显式加载、启动时自检，缺失时必须明确失败，禁止静默降级、伪造成功、把缺失数据当作空结果，或在证据不足时继续生成结论。每次交付都必须留下本地验证证据和可恢复的 Git 记录。

This repository is the master orchestration layer for Summer's life-management
systems. Work in this repo must be direct, verifiable, and product-oriented.

## Communication

Final reports to the user must be plain, clear English or Chinese, depending on
the user's latest language. Avoid implementation jargon unless the user asks for
details.

## Work Standard

- Verify before reporting completion.
- Prefer small, testable changes.
- Keep `lifepalantir` as the master system; do not bury master navigation inside a subsystem.
- Do not copy Palantir trademarks, logos, or proprietary assets.
- Use Palantir-inspired principles: ontology, operational workflows, audit trail, permission-aware design, and action loops.
- Preserve subsystem boundaries:
  - `LifeToolSystem` = life equipment and services.
  - `TomeofSouls` = personal attributes, identity, goals, AI-agent context.
  - `Whattoeat` = daily food execution.
  - `Vancouver` = immigration and settlement.

## Verification Checklist

Before saying done, run:

```bash
python3 -m py_compile server.py
python3 server.py
```

Then verify:

- `GET /api/health` returns ok.
- `GET /api/bootstrap` returns all four subsystems.
- the homepage opens in a browser.
- creating a decision writes to SQLite and is visible after reload.

## File Rules

- Keep docs current when changing architecture.
- Keep database schema documented in `docs/database.md`.
- Keep UI rules documented in `docs/palantir-design-standard.md`.
- Keep Claude/Codex rules documented in `CLAUDE.md` and `docs/claudecode-development-standard.md`.
