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
| `signal_rules.json`   | 行为信号规则库  | 手工整理(真诚/撒谎/控制/焦虑/操纵/自恋/攻击/回避/压力 9 类) | 30 |
| `career_profiles.json` | 职业画像模板库  | 手工整理(销售/工程师/产品经理/HR/管理者/运营/设计师/财务 8 岗位) | 8 |
| `risk_flags.json`    | 风险信号规则库  | 手工整理(PUA/NPD/ASPD/煤气灯/三角操纵/情感勒索/受害者扮演/控制型伴侣 8 类) | 25 |
| `cases.json`         | 案例库          | 手工整理(面试识人/合伙谈判/婚恋首次/团队招聘/重要决策/销售识客 6 场景) | 8 |
| `bot_intents.json`   | 飞书 Bot 意图路由 | 手工整理(性格/行为/职业/风险/案例/决策/自查/关系/工具/兜底 10 意图) | 10 |

> **附加工具文件**:`persona_frameworks.json` / `signal_rules.json` / `career_profiles.json` / `risk_flags.json` / `cases.json` / `bot_intents.json` 不在 `md_to_json.py` 自动生成的 10 分类内,
> 是 Phase 0 手工维护的"多框架 + 行为信号 + 职业画像 + 风险信号 + 案例 + 飞书 Bot 路由"基线,结构对齐下方 Schema。
> `signal_rules.json` 是 Phase 0 第 3 项基线版(v0.1, 20 条),2026-09-09 扩到 v0.2 共 25 条(攻击/控制/自恋/撒谎 各补 1-2 条),2026-09-11 扩到 v0.3 共 30 条(焦虑 +2 / 操纵_PUA +1 / 回避 +1 / 压力 +1, sig_026-sig_030, severity 全部对齐 SCHEMA 1-3 档),**2026-09-12 升 v0.3.1 · 收敛 6 条历史信号 severity(sev=4-5 → 1-3 · sig_007/008 控制 · sig_011/012 操纵_PUA · sig_013/014 自恋_NPD)· 全部 30 条对齐 SCHEMA 1-3 档 · 9 类分布更均衡**;后续 T1 会扩到 50+(v0.5)。
> `career_profiles.json` 是 Phase 0 第 4 项基线版(v0.1, 5 岗位),**2026-09-16 升 v0.2 · 5 → 8 岗位 · 补 3 类高价值缺口:运营(career_006)/ 设计师(career_007)/ 财务(career_008) · 字段结构与 career_001-005 完全对齐 · 8 岗位覆盖业务前端/技术研发/业务中台/职能支持/组织领导/创意职能 6 大角色类别**;后续 T1 会扩到 20+(v0.5 目标)。
> `risk_flags.json` 是 Phase 0 第 5 项基线版(v0.1, 15 条 / 8 类),**2026-09-14 升 v0.2 · 15 → 20 条 · 补 5 类高价值缺口:PUA 甜蜜陷阱(risk_016)/ NPD 镜像投射(risk_017)/ ASPD 责任转嫁(risk_018)/ 煤气灯现实否认(risk_019)/ 控制型伴侣经济控制(risk_020)**;**2026-09-15 升 v0.2 · 第二步 20 → 25 条 · 补 5 类高价值缺口:三角操纵 挑拨关系对比(risk_021)/ 情感勒索 牺牲叙事(risk_022)/ 受害者扮演 反向指控(risk_023)/ 控制型伴侣 认知隔离(risk_024)/ 煤气灯 情绪定义篡改(risk_025)· 8 类分布更均衡(煤气灯 3→4 / 控制型伴侣 2→3 / 三角操纵 1→2 / 情感勒索 1→2 / 受害者扮演 1→2)· Phase 0.5 v0.2 第二步已闭环**;后续 T1 会扩到 50+(v0.5 目标 W2)。
> `cases.json` 是 Phase 0 第 6 项基线版(v0.1, 5 场景各 1 例);**2026-09-17 升 v0.2 第一步 · 5 → 6 例 · 新增第 6 场景"销售识客" (case_006 · B2B 客户决策人热情买单 + 关键决策权模糊模式) · 6 大场景分布(面试识人/合伙谈判/婚恋首次/团队招聘/重要决策/销售识客)**;**2026-09-18 升 v0.2 第二步 · 6 → 7 例 · '面试识人'场景补第 2 例 (case_007 · 头部公司光环 + 跳槽频率异常 · 1.2 年一换 + 全部外部归因 · 6 大场景中第 1 个进入 2 例场景)**;**2026-09-19 升 v0.2 第三步 · 7 → 8 例 · '合伙谈判'场景补第 2 例 (case_008 · 技术大牛 + 产出拖延循环 · CTO 合伙人 8 个月未达 demo · '理论深 + 落地弱'经典模式 · 与 case_002 口头豪爽型对照) · 6 大场景中第 2 个进入 2 例 · 累计 5/6 场景已达 2 例(面试识人/合伙谈判/团队招聘待续)**;后续 T1 会扩到 20-30 条(v0.2 目标 10 例 / W4 · v0.5 目标 20-30 例)。
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
