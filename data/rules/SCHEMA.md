# data/rules · 字段 Schema 集中定义

> 16 JSON 字段命名 / 类型 / 取值范围 / 必填性集中约定
> 用途:Phase 1 后端导入 PostgreSQL / 前端 TypeScript 类型 / 测试基线校验
> 版本:v0.1(2026-09-08 建立,基于 16 JSON 现状反向提取)
> 维护:T1 巡检 + 任意 JSON 字段变更时同步更新本文件

---

## 一、顶层通用字段(全部 16 JSON 共享)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `category` | `string` (中文分类名) | ✅ | 例:"人格心理学" / "行为信号规则库" / "飞书 Bot 意图路由表" |
| `category_id` | `string` (snake_case) | ✅ | 例:`personality_psychology` / `signal_rules` / `bot_intents` |
| `source` | `string` | ✅ | 源 markdown 绝对路径,或"手工维护 · ..." 描述 |
| `meta` | `object` | ✅ | 元信息字典,字段因文件而异(见下表) |
| `items` | `array<item>` | ✅ | 业务条目列表,长度 ≥ 1 |
| `generated_at` | `string` (ISO 8601 date) | ✅ | 最后一次生成或手工更新时间,`YYYY-MM-DD` |
| `item_count` | `integer` | ✅ | `items.length`,与服务端实际值必须一致 |

### 1.1 可选顶层字段

| 字段 | 类型 | 出现文件 | 说明 |
|------|------|----------|------|
| `fallback_used` | `boolean` | md_to_json 生成的 11 文件 | 标记本次生成是否走了 fallback 解析路径 |
| `note` | `string` | persona_frameworks | 手工维护文件的额外说明 |
| `usage_notes` | `string` | career_profiles / risk_flags | 使用注意事项,前端展示用 |
| `schema_notes` | `string` | cases | schema 变更历史备注 |
| `categories` | `string[]` (枚举) | signal_rules / risk_flags / cases / bot_intents | 业务上合法的分类值清单 |
| `roles` | `string[]` (枚举) | career_profiles | 5 岗位名清单,5 个 |

### 1.2 meta 子字段(各文件约定)

`meta` 是 16 JSON 都有的对象,字段**因文件而异**,不做强制统一。常见子字段:

| 子字段 | 类型 | 说明 |
|-------|------|------|
| `类型` | `string` | 知识库路径表达,例:"知识库 > 识人 > 人格心理学" |
| `适用角色` | `string` | 适用人群描述,例:"HR / 销售 / 管理者" |
| `适用场景` | `string` | 业务场景,例:"面试 / 谈判 / 婚恋初次" |
| `更新日期` | `string` (date) | 与 `generated_at` 同值或更早 |
| `来源` | `string` | 知识/数据出处 |
| `适用阶段` | `string` | Phase 0 / Phase 1 / ... |
| `基线条数` / `目标条数` | `string` | bot_intents 专用 |
| `边界声明` | `string` | bot_intents 专用,声明"只做分类/路由,不做诊断" |

> **schema 纪律**:`meta` 不参与业务逻辑,只做展示和审计。任意字段缺失不报错,但 `类型` / `适用角色` / `边界声明`(如适用)**应**齐全。

---

## 二、items 内字段(各文件独立,无强一致)

16 JSON 的 items 内字段集**不完全统一**。Phase 0 阶段允许差异,但 Phase 1 导入数据库前需要做 1:1 映射。

### 2.1 10 分类 + persona_frameworks · 11 文件

适用于:`personality.json` / `behavior.json` / `team_role.json` / `interview.json` / `character.json` / `leadership.json` / `communication.json` / `eq.json` / `talent.json` / `classic.json` / `persona_frameworks.json`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | `string` | ✅ | 条目标题,中文,2-30 字 |
| `content` | `string` (markdown) | ✅ | 条目正文,markdown 格式,可含表格/代码块/分隔线 |
| `tags` | `string[]` | ✅ | 标签列表,允许空数组 `[]`,每个 tag 中文 2-10 字 |

### 2.2 signal_rules(行为信号规则库)

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `id` | `string` | ✅ | 格式 `sig_NNN`,从 `sig_001` 起递增,全局唯一 |
| `category` | `string` (枚举) | ✅ | 必须在 `顶层.categories` 9 项内:真诚 / 撒谎 / 控制 / 焦虑 / 操纵_PUA / 自恋_NPD / 攻击 / 回避 / 压力 |
| `pattern` | `string` | ✅ | 信号模式描述,中文,1-100 字 |
| `weight` | `float` | ✅ | 0 ≤ weight ≤ 1,2 位小数,正向 / 负向信号统一为正向权重 |
| `severity` | `integer` | ✅ | 1-3 三档,1=轻 / 2=中 / 3=重 |
| `context` | `string` (枚举) | ✅ | 适用上下文,常见值 `text` / `behavior` / `voice` / `multi` |
| `description` | `string` | ✅ | 信号解读说明,中文,20-200 字 |
| `advice` | `string` | ✅ | 处置建议,中文,20-200 字 |

### 2.3 career_profiles(职业画像模板库)

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `id` | `string` | ✅ | 格式 `cp_NNN`,从 `cp_001` 起递增,全局唯一 |
| `role` | `string` (枚举) | ✅ | 必须在 `顶层.roles` 5 项内:销售 / 工程师 / 产品经理 / HR / 管理者 |
| `role_category` | `string` | ✅ | 角色大类,例:"业务 / 技术 / 产品 / 人力 / 管理" |
| `key_traits` | `string[]` | ✅ | 关键特质,2-8 项,每项 2-10 字 |
| `red_flags` | `string[]` | ✅ | 红旗信号,2-6 项 |
| `interview_questions` | `string[]` | ✅ | 推荐面试问题,3-8 项,每项 5-50 字 |
| `fit_signals` | `string[]` | ✅ | 适配信号,2-6 项 |
| `description` | `string` | ✅ | 角色描述,50-200 字 |
| `advice` | `string` | ✅ | 评估/面试建议,30-200 字 |

### 2.4 risk_flags(风险信号规则库)

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `id` | `string` | ✅ | 格式 `rf_NNN`,从 `rf_001` 起递增,全局唯一 |
| `type` | `string` (枚举) | ✅ | 必须在 `顶层.categories` 8 项内:PUA / NPD / ASPD / 煤气灯 / 三角操纵 / 情感勒索 / 受害者扮演 / 控制型伴侣 |
| `name` | `string` | ✅ | 风险名称,中文,4-20 字 |
| `signals` | `string[]` | ✅ | 信号清单,3-10 项,每项 4-30 字 |
| `severity` | `integer` | ✅ | 1-3 三档,1=轻 / 2=中 / 3=重 |
| `frequency` | `string` (枚举) | ✅ | 出现频率,常见值 `偶尔` / `反复` / `持续` / `高频` |
| `context` | `string` | ✅ | 适用场景,例:"亲密关系" / "职场 PUA" / "谈判" |
| `description` | `string` | ✅ | 风险描述,30-200 字 |
| `advice` | `string` | ✅ | 应对建议,30-200 字 |
| `verify_action` | `string` | ✅ | 验证/进一步动作建议,20-150 字 |

### 2.5 cases(案例库)

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `id` | `string` | ✅ | 格式 `case_NNN`,从 `case_001` 起递增,全局唯一 |
| `scenario` | `string` (枚举) | ✅ | 必须在 `顶层.categories` 5 项内:面试识人 / 合伙谈判 / 婚恋首次 / 团队招聘 / 重要决策 |
| `title` | `string` | ✅ | 案例标题,5-30 字 |
| `background` | `string` | ✅ | 背景描述,50-300 字 |
| `behavior_signals` | `string[]` | ✅ | 行为信号清单,3-8 项 |
| `persona_profile` | `object` | ✅ | 人物画像,含 MBTI / 大五 / DISC / 九型 子字段(自由结构) |
| `red_flags` | `string[]` | ✅ | 红旗信号,2-6 项 |
| `outcome` | `string` | ✅ | 案例结果,30-200 字 |
| `tags` | `string[]` | ✅ | 标签,3-8 项 |
| `advice` | `string` | ✅ | 处置建议,30-200 字 |
| `verify_action` | `string` | ✅ | 验证动作建议,20-150 字 |
| `source` | `string` | ✅ | 案例来源,例:"脱敏自 2024 Q3 合伙谈判咨询" |

### 2.6 bot_intents(飞书 Bot 意图路由表)

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `id` | `string` | ✅ | 格式 `intent_NNN`,从 `intent_001` 起递增,全局唯一 |
| `intent` | `string` (枚举) | ✅ | 必须在 `顶层.categories` 10 项内:问性格_Persona / 问行为_Signal / 问职业_Career / 问风险_Risk / 问案例_Case / 问决策_Decide / 自查_SelfAssessment / 聊关系_Relationship / 工具调用_ToolUse / 默认兜底_Default |
| `name` | `string` | ✅ | 意图中文名,4-20 字 |
| `trigger_keywords` | `string[]` | ✅ | 触发关键词,3-10 项,每项 4-30 字 |
| `example_queries` | `string[]` | ✅ | 示例问句,2-5 项,每项 5-50 字 |
| `module` | `string` (枚举) | ✅ | 路由模块,5 大模块:性格 / 行为 / 职业 / 风险 / 决策 |
| `route` | `string` | ✅ | 路由目标,Phase 0 阶段为文件名 / handler 路径 |
| `handler` | `string` | ✅ | 处理函数引用,Phase 1 阶段绑定 Python 函数 |
| `response_template` | `string` | ⭕ Phase 1 必填 | 回复模板,1-3 句,Phase 1 webhook handler 启动后必填 |

---

## 三、ID 命名约定(全局)

| 文件 | 格式 | 起点 | 示例 |
|------|------|------|------|
| signal_rules | `sig_NNN` | 001 | `sig_001` |
| career_profiles | `cp_NNN` | 001 | `cp_001` |
| risk_flags | `rf_NNN` | 001 | `rf_001` |
| cases | `case_NNN` | 001 | `case_001` |
| bot_intents | `intent_NNN` | 001 | `intent_001` |

> 10 分类 + persona_frameworks 的 11 文件**无 id 字段**(用 `title` + `tags` 标识条目),Phase 1 导入数据库时由后端按 `category_id + 行号` 自动生成主键。

---

## 四、Phase 1 导入检查清单(供后端工程师)

- [ ] 16 JSON 顶层字段全部存在(category / category_id / source / meta / items / generated_at / item_count)
- [ ] `item_count` 与 `items.length` 一致
- [ ] `meta` 至少含 `类型` / `适用角色` / `更新日期` 3 项
- [ ] 4 个有 `categories` 枚举的文件(signal_rules / risk_flags / cases / bot_intents)其 `items[*].category` / `type` / `scenario` / `intent` 全部在 `categories` 列表内
- [ ] signal_rules `weight` 全部 ∈ [0, 1] 且为 float
- [ ] risk_flags / signal_rules `severity` 全部 ∈ {1, 2, 3}
- [ ] 5 个带 id 的文件 ID 命名格式正确 + 无重复
- [ ] cases `source` 字段全部是"脱敏自 ..."形式,**不含真实姓名/公司/联系方式**
- [ ] bot_intents `module` 全部在 5 大模块内
- [ ] bot_intents `response_template` 字段在 Phase 1 webhook handler 上线后必填

---

## 五、版本与变更

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1 | 2026-09-08 | 初版,基于 16 JSON 现状反向提取(0906 bot_intents 入库后 1 周内的 1 次结构盘点) |

## 六、关联文档

- `data/rules/README.md`:16 JSON 文件清单 + Schema 概览
- `scripts/md_to_json.py`:10 分类 JSON 的生成脚本(Phase 0 已闭环)
- `项目开发计划.md` Phase 1 第 1 项:Web App 骨架(Phase 1 启动后将消费本 Schema)
- `识人顾问开发架构与计划.md` · 第 4 节"数据资产盘点":16 JSON 业务定位
