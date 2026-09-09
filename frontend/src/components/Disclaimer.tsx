// frontend/src/components/Disclaimer.tsx
// 12-识人 JudgingAdvisor · 全站风险边界提示组件
// 哲学:辅助判断,不替决定 · 2026-09-10 P0-D 落地
import React from "react";

export interface DisclaimerProps {
  /** 提示强度,默认 standard;严格场景用 strict */
  level?: "standard" | "strict";
  /** 自定义文案(可选),不传走默认 */
  message?: string;
  /** 隐藏(测试或暗色场景) */
  hidden?: boolean;
}

const DEFAULT_TEXT_STANDARD =
  "本工具仅供辅助参考。所有分析均基于有限文本/语音/视频信号,不能替代专业判断。涉及人身安全、婚姻、雇佣等重大决策,请结合其他渠道核实后再行动。";

const DEFAULT_TEXT_STRICT =
  "以下分析为行为模式辅助参考,非心理诊断、非法律意见、非人身安全评估。识人顾问对结果准确性不承担责任。重大决策请务必咨询专业人士并经多源验证。";

/**
 * 全站统一的"辅助不替代"边界提示。
 * 任何对外输出"风险/性格/操纵/红旗"信号的页面都应在头部或结果区嵌入此组件。
 *
 * 使用:
 *   <Disclaimer />
 *   <Disclaimer level="strict" />
 */
export const Disclaimer: React.FC<DisclaimerProps> = ({
  level = "standard",
  message,
  hidden = false,
}) => {
  if (hidden) return null;
  const text = message ?? (level === "strict" ? DEFAULT_TEXT_STRICT : DEFAULT_TEXT_STANDARD);
  const isStrict = level === "strict";

  return (
    <aside
      role="alert"
      aria-live="polite"
      style={{
        padding: "12px 16px",
        borderRadius: 6,
        border: `1px solid ${isStrict ? "#d97706" : "#94a3b8"}`,
        background: isStrict ? "#fffbeb" : "#f8fafc",
        color: isStrict ? "#78350f" : "#334155",
        fontSize: 13,
        lineHeight: 1.55,
        margin: "12px 0",
      }}
    >
      <strong style={{ marginRight: 6 }}>⚠️ 边界提示</strong>
      {text}
    </aside>
  );
};

export default Disclaimer;
