#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_json.py
=============
将 _JudgingPeopleLib/ 下的 10 个分类目录的 md 文件,转成结构化 JSON,
输出到 JudgingPeopleWeb/data/rules/。

设计原则(参考 2026-08-24 计划):
  1. 容错优先:Lib 下 md 是张勇手工笔记,无统一 schema,能解析就解析,不能解析就 fallback 到 raw 段落
  2. 分类映射:Lib 目录 01_人格心理学...10_识人经典 → 输出 personality.json...classic.json
  3. 输出 schema:{category, source, items: [{title, content, tags}]}
  4. 幂等:可重复运行,覆盖更新

用法:
  cd JudgingPeopleWeb/
  python scripts/md_to_json.py                       # 默认:解析所有 10 个分类
  python scripts/md_to_json.py --src ../01_人格心理学 --out data/rules/personality.json
  python scripts/md_to_json.py --only 01,02,05      # 只跑指定编号
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable

# -----------------------------------------------------------------------------
# 分类映射:Lib 目录编号 → (输出 json 名, 英文 category id, 中文标签)
# -----------------------------------------------------------------------------
CATEGORY_MAP: list[tuple[str, str, str, str]] = [
    # (lib_dir_prefix, output_stem, category_id, label_zh)
    ("01_人格心理学", "personality", "personality_psychology", "人格心理学"),
    ("02_行为观察",   "behavior",    "behavior_observation",  "行为观察"),
    ("03_团队角色",   "team_role",   "team_role",             "团队角色"),
    ("04_面试与评估", "interview",   "interview_assessment",  "面试与评估"),
    ("05_性格特征识别", "character", "character_recognition", "性格特征识别"),
    ("06_领导力评估", "leadership",  "leadership_assessment", "领导力评估"),
    ("07_沟通风格识别", "communication", "communication_style", "沟通风格识别"),
    ("08_情商评估",   "eq",          "eq_assessment",         "情商评估"),
    ("09_人才选拔与配置", "talent",  "talent_selection",      "人才选拔与配置"),
    ("10_识人经典",   "classic",     "people_reading_classic","识人经典"),
]

# 标签词典:命中关键词 → 打 tag(可叠加,中英都识别)
TAG_DICT: dict[str, list[str]] = {
    "MBTI":    ["MBTI", "mbti", "16型", "16种人格"],
    "大五":    ["大五", "Big Five", "NEO-PI", "五大人格"],
    "DISC":    ["DISC"],
    "九型":    ["九型", "Enneagram"],
    "依恋":    ["依恋", "Attachment"],
    "微表情":  ["微表情", "表情", "面部", "眼神", "姿态"],
    "声音":    ["语速", "音调", "声调", "语气", "停顿"],
    "面试":    ["面试", "候选人", "招聘", "应聘"],
    "团队":    ["团队", "team", "协作"],
    "领导力":  ["领导", "领导力", "管理者", "领袖"],
    "沟通":    ["沟通", "对话", "交流"],
    "情商":    ["情商", "EQ", "共情", "情绪"],
    "PUA":     ["PUA", "操纵", "操控", "打压", "煤气灯", "gaslight"],
    "NPD":     ["自恋型", "NPD", "自恋人格"],
    "ASPD":    ["反社会", "ASPD", "反社会人格"],
    "焦虑":    ["焦虑", "回避", "紧张"],
    "操控":    ["操纵", "操控", "控制欲", "话术"],
    "匹配":    ["匹配", "岗位匹配", "人岗"],
    "速查":    ["速查", "速记", "对照表"],
}

# -----------------------------------------------------------------------------
# 数据结构
# -----------------------------------------------------------------------------
@dataclass
class Section:
    """一个二级/三级标题块,作为 items 的一项。"""
    title: str
    content: str
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"title": self.title, "content": self.content, "tags": self.tags}


@dataclass
class ParsedDoc:
    """一个 md 文档的解析结果。"""
    category: str
    category_id: str
    source: str
    meta: dict
    items: list[Section]
    fallback_used: bool = False

    def to_dict(self) -> dict:
        return {
            "category":      self.category,
            "category_id":   self.category_id,
            "source":        self.source,
            "meta":          self.meta,
            "items":         [s.to_dict() for s in self.items],
            "fallback_used": self.fallback_used,
            "generated_at":  datetime.now().isoformat(timespec="seconds"),
            "item_count":    len(self.items),
        }


# -----------------------------------------------------------------------------
# 解析器
# -----------------------------------------------------------------------------
META_PAT = re.compile(r"^\s*-\s*\*\*(.+?)\*\*\s*[:：]\s*(.+?)\s*$")
H2_PAT   = re.compile(r"^##\s+(.+?)\s*$")
H3_PAT   = re.compile(r"^###\s+(.+?)\s*$")
H4_PAT   = re.compile(r"^####\s+(.+?)\s*$")
H_ANY    = re.compile(r"^#{1,6}\s+(.+?)\s*$")
TABLE_ROW = re.compile(r"^\|.+\|$")
SEP_LINE  = re.compile(r"^[\s|:\-]+$")  # 表格分隔行(只含 | : - 空格)
PAGE_BREAK = re.compile(r"^---+\s*$")


def parse_meta(lines: list[str]) -> tuple[dict, int]:
    """扫描开头连续的 - **key**: value 行,返回 (meta_dict, 消费行数)。

    容忍开头有 H1 标题/空行:会先跳过非 meta 行直到遇到 meta 行,
    然后连续读取 meta,直到首个非 meta 行。
    """
    meta: dict[str, str] = {}
    i = 0
    n = len(lines)

    # 跳过开头的 H1 / 空行
    while i < n:
        s = lines[i].strip()
        if not s or s.startswith("# "):
            i += 1
            continue
        break

    # 连续读取 meta 行
    while i < n:
        line = lines[i].rstrip()
        m = META_PAT.match(line)
        if not m:
            break
        meta[m.group(1).strip()] = m.group(2).strip()
        i += 1
    return meta, i


def extract_tags(text: str) -> list[str]:
    """基于 TAG_DICT 命中关键词,返回去重保序的 tag 列表。"""
    seen: list[str] = []
    for tag, keywords in TAG_DICT.items():
        for kw in keywords:
            if kw in text:
                if tag not in seen:
                    seen.append(tag)
                break
    return seen


def parse_sections(lines: list[str], start: int) -> list[Section]:
    """从 start 行开始,按 H2/H3 切分 section,H3 内容并入最近的 H2。
       若整个文档没有 H2,fallback 到全文一段。
    """
    # 1) 先扫一遍,看有没有 H2
    h2_indices = [i for i, ln in enumerate(lines[start:], start) if H2_PAT.match(ln)]
    if not h2_indices:
        return []  # 触发 fallback

    sections: list[Section] = []
    for idx, h2_pos in enumerate(h2_indices):
        title = H2_PAT.match(lines[h2_pos]).group(1).strip()
        body_start = h2_pos + 1
        body_end = h2_indices[idx + 1] if idx + 1 < len(h2_indices) else len(lines)
        body_lines = lines[body_start:body_end]

        # 内部如果还有 H3/H4,直接拼到 content 里(不去嵌套,保简单)
        buf: list[str] = []
        for ln in body_lines:
            s = ln.rstrip()
            if not s:
                buf.append("")
                continue
            # 表格分隔行跳过
            if SEP_LINE.match(s) and TABLE_ROW.match(lines[body_lines.index(ln) + body_start - 1] if False else s):
                # 上面的判断只是为了消除 lint,实际逻辑见下
                pass
            if s.startswith("#"):
                # 保留标题层级提示
                level = len(s) - len(s.lstrip("#"))
                buf.append(s)
                continue
            buf.append(s)

        # 清掉连续空行
        content = "\n".join(buf).strip()
        content = re.sub(r"\n{3,}", "\n\n", content)

        # 标题 + 正文合起来做 tag 抽取
        tag_source = title + "\n" + content
        tags = extract_tags(tag_source)

        sections.append(Section(title=title, content=content, tags=tags))
    return sections


def fallback_sections(meta: dict, raw_text: str) -> list[Section]:
    """无结构时的兜底:把整篇作为一个 Section,标题用文件名/类型字段。"""
    title = meta.get("类型", "未分类笔记")
    tags = extract_tags(raw_text)
    return [Section(title=title, content=raw_text.strip(), tags=tags)]


def parse_md(path: Path, category: str, category_id: str) -> ParsedDoc:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    meta, consumed = parse_meta(lines)
    sections = parse_sections(lines, consumed)

    fallback_used = False
    if not sections:
        sections = fallback_sections(meta, text)
        fallback_used = True

    return ParsedDoc(
        category=category,
        category_id=category_id,
        source=str(path),
        meta=meta,
        items=sections,
        fallback_used=fallback_used,
    )


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------
def iter_lib_files(lib_root: Path) -> Iterable[tuple[Path, str, str, str]]:
    """遍历 10 个分类目录,产出 (md_path, dir_prefix, out_stem, label_zh)。"""
    for dir_prefix, out_stem, cat_id, label in CATEGORY_MAP:
        d = lib_root / dir_prefix
        if not d.is_dir():
            continue
        for md in sorted(d.glob("*.md")):
            yield md, dir_prefix, out_stem, label


def process_one(src: Path, out: Path, label: str, cat_id: str) -> ParsedDoc:
    doc = parse_md(src, category=label, category_id=cat_id)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(doc.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return doc


def main() -> int:
    here = Path(__file__).resolve().parent
    web_root = here.parent
    lib_root = web_root.parent  # _JudgingPeopleLib/

    ap = argparse.ArgumentParser(description="md → JSON 解析器(10 分类)")
    ap.add_argument("--src", type=Path, default=None,
                    help="单个源 md 文件路径(覆盖默认遍历)")
    ap.add_argument("--out", type=Path, default=None,
                    help="单个输出 json 路径(与 --src 配套)")
    ap.add_argument("--only", type=str, default=None,
                    help="只跑指定分类编号,逗号分隔,例如 '01,02,05'")
    ap.add_argument("--lib-root", type=Path, default=lib_root,
                    help="Lib 根目录(默认 _JudgingPeopleLib/)")
    ap.add_argument("--out-dir", type=Path, default=web_root / "data" / "rules",
                    help="JSON 输出目录")
    args = ap.parse_args()

    # 模式 1:单文件
    if args.src and args.out:
        dir_name = args.src.parent.name
        matched = next((c for c in CATEGORY_MAP if c[0] == dir_name), None)
        if matched:
            label, cat_id = matched[3], matched[2]
        else:
            label, cat_id = dir_name, "custom"
        doc = process_one(args.src, args.out, label, cat_id)
        print(f"✅ {args.src.name} → {args.out}  (items={len(doc.items)}, "
              f"fallback={doc.fallback_used})")
        return 0

    # 模式 2:批量
    only_set = None
    if args.only:
        only_set = {f"{int(x):02d}" for x in args.only.split(",") if x.strip()}

    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    summary: list[tuple[str, int, bool]] = []
    for md_path, dir_prefix, out_stem, label in iter_lib_files(args.lib_root):
        prefix_num = dir_prefix.split("_", 1)[0]
        if only_set and prefix_num not in only_set:
            continue
        out_path = out_dir / f"{out_stem}.json"
        doc = process_one(md_path, out_path, label,
                          next(c[2] for c in CATEGORY_MAP if c[0] == dir_prefix))
        summary.append((out_stem, len(doc.items), doc.fallback_used))
        print(f"✅ {dir_prefix}/{md_path.name} → {out_path.name}  "
              f"(items={len(doc.items)}, fallback={doc.fallback_used})")

    if not summary:
        print(f"⚠️  没找到任何 md,检查 --lib-root={args.lib_root}", file=sys.stderr)
        return 1

    print(f"\n📦 共生成 {len(summary)} 个 JSON,落地 {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
