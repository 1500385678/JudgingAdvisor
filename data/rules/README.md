# data/rules · 结构化规则库

> 10 分类 × 结构化 JSON · 由 `scripts/md_to_json.py` 自动生成 · 2026-08-26 起

## 文件清单

| 文件 | 分类 | 源目录 | item 数 |
|------|------|--------|---------|
| `personality.json`   | 人格心理学       | `_JudgingPeopleLib/01_人格心理学/` | 8 |
| `behavior.json`      | 行为观察         | `_JudgingPeopleLib/02_行为观察/`   | 8 |
| `team_role.json`     | 团队角色         | `_JudgingPeopleLib/03_团队角色/`   | 8 |
| `interview.json`     | 面试与评估       | `_JudgingPeopleLib/04_面试与评估/` | 7 |
| `character.json`     | 性格特征识别     | `_JudgingPeopleLib/05_性格特征识别/` | 8 |
| `leadership.json`    | 领导力评估       | `_JudgingPeopleLib/06_领导力评估/` | 7 |
| `communication.json` | 沟通风格识别     | `_JudgingPeopleLib/07_沟通风格识别/` | 6 |
| `eq.json`            | 情商评估         | `_JudgingPeopleLib/08_情商评估/`   | 7 |
| `talent.json`        | 人才选拔与配置   | `_JudgingPeopleLib/09_人才选拔与配置/` | 7 |
| `classic.json`       | 识人经典         | `_JudgingPeopleLib/10_识人经典/`   | 8 |
| `persona_frameworks.json` | 性格框架规则库 | 手工整理(MBTI 16型/大五/DISC/九型) | 5 |
| `signal_rules.json`   | 行为信号规则库  | 手工整理(真诚/撒谎/控制/焦虑/操纵/自恋/攻击/回避/压力 9 类) | 25 |
| `career_profiles.json` | 职业画像模板库  | 手工整理(销售/工程师/产品经理/HR/管理者 5 岗位) | 5 |
| `risk_flags.json`    | 风险信号规则库  | 手工整理(PUA/NPD/ASPD/煤气灯/三角操纵/情感勒索/受害者扮演/控制型伴侣 8 类) | 15 |
| `cases.json`         | 案例库          | 手工整理(面试识人/合伙谈判/婚恋首次/团队招聘/重要决策 5 场景) | 5 |
| `bot_intents.json`   | 飞书 Bot 意图路由 | 手工整理(性格/行为/职业/风险/案例/决策/自查/关系/工具/兜底 10 意图) | 10 |

> **附加工具文件**:`persona_frameworks.json` / `signal_rules.json` / `career_profiles.json` / `risk_flags.json` / `cases.json` / `bot_intents.json` 不在 `md_to_json.py` 自动生成的 10 分类内,
> 是 Phase 0 手工维护的"多框架 + 行为信号 + 职业画像 + 风险信号 + 案例 + 飞书 Bot 路由"基线,结构对齐下方 Schema。
> `signal_rules.json` 是 Phase 0 第 3 项基线版(v0.1, 20 条),2026-09-09 扩到 v0.2 共 25 条(攻击/控制/自恋/撒谎 各补 1-2 条),后续 T1 会扩到 50+。
> `career_profiles.json` 是 Phase 0 第 4 项基线版(v0.1, 5 岗位),后续 T1 会扩到 20+。
> `risk_flags.json` 是 Phase 0 第 5 项基线版(v0.1, 15 条 / 8 类),后续 T1 会扩到 50+。
> `cases.json` 是 Phase 0 第 6 项基线版(v0.1, 5 场景各 1 例),后续 T1 会扩到 20-30 条。
> `bot_intents.json` 是 Phase 0 第 7 项基线版(v0.1, 10 意图),覆盖 5 大模块 + 决策/自查/关系/工具/兜底,后续 T1 会扩到 20+ 并补 multi_intent 融合。

## JSON Schema

每个 JSON 文件结构:

```json
{
  "category":      "人格心理学",          // 中文分类名
  "category_id":   "personality_psychology",  // 英文 ID(稳定)
  "source":        "/abs/path/to/人格心理学.md",  // 源 md 路径
  "meta": {                              // md 头部元数据
    "类型": "知识库 > 识人 > 人格心理学",
    "适用角色": "HR / 管理者 / 心理咨询师",
    "更新日期": "2026-05-30",
    "来源": "人格心理学知识"
  },
  "items": [                             // 解析后的结构化条目
    {
      "title":   "一、人格基本概念",
      "content": "### 什么是人格\n\n**定义**:...完整段落...",
      "tags":    ["大五", "MBTI"]        // 自动从内容抽出的 tag
    }
  ],
  "fallback_used": false,                // 是否触发无结构兜底
  "generated_at":  "2026-08-26T03:51:12",
  "item_count":    8
}
```

## 标签词典

当前内置 18 个标签(MBTI / 大五 / DISC / 九型 / 依恋 / 微表情 / 声音 /
面试 / 团队 / 领导力 / 沟通 / 情商 / PUA / NPD / ASPD / 焦虑 / 操控 / 匹配 / 速查)。
词典维护在 `scripts/md_to_json.py` 顶部 `TAG_DICT`。

## 重新生成

```bash
cd JudgingPeopleWeb/
python3 scripts/md_to_json.py                        # 全部 10 分类
python3 scripts/md_to_json.py --only 01,02,05        # 只跑 01/02/05
python3 scripts/md_to_json.py --src ../01_人格心理学/人格心理学.md \
                               --out data/rules/personality.json
```

幂等:可重复运行,输出覆盖更新。

## 下游用途

- 性格解读页:从 `personality.json` 拉 MBTI/大五/DISC/九型条目
- 行为信号识别:从 `behavior.json` 拉微表情/声音/情绪条目
- 风险预警:用 `tags` 字段过滤 PUA/NPD/ASPD/操控/焦虑 相关条目
- 案例库:在 items 基础上挂 `outcome` 字段,扩展为 cases 表

## Schema 集中定义

> 16 JSON 字段命名 / 类型 / 取值范围 / 必填性 集中约定 → [`SCHEMA.md`](./SCHEMA.md)(v0.1, 2026-09-08 建立)
>
> 用途:Phase 1 后端导入 PostgreSQL / 前端 TypeScript 类型 / 测试基线校验
> 触发更新:任意 JSON 字段变更时,本 README + SCHEMA.md 同步改
