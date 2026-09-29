#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""setup_corpus_links_665.py — 665 A1：给 queyi-verifier 补**语料联结**（不复制大目录）。

背景（本批实测）
================
`queyi-verifier` 里 `atoms`、`data` 本来就是**联结**（junction → CPP-Bible），
但 `Examples/atoms`、`evidence`、`misconceptions`、`Book`、`research`、`docs`、`goldens`
**没有** ⇒ 大量测试因为"文件不存在"直接红（全量 pytest **323 FAILED**）。

处置原则
========
* **只建联接、不复制内容**（`data` 有 3.4 GB；复制会拖死仓库，也会制造第二份真相）。
* **不删除任何已有目录**：若目标路径已存在且非空 ⇒ 跳过并打印原因，人工决定。
* 连结路径写进 `.gitignore`（它们是**机器布局**，不该被提交成 symlink 条目）。
* **`.github` 例外**：它是 CI 的真源，本批改为**真实副本**（8 个文件），不进 ignore。

用法
====
    python tools/setup_corpus_links_665.py --check    # 只报告（默认）
    python tools/setup_corpus_links_665.py --apply
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CPP = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")

#: (verifier 侧相对路径, CPP-Bible 侧相对路径)
#: 666 双仓复核增补两项：
#:   * `Examples`（整目录）：原先只联结 `Examples/atoms`，导致部分副本目录未跟踪、
#:     四条"受控目录零污染"门禁假红 + Merkle 量错目录（见 .gitignore 注释）；
#:   * `_archive/benchmarks`：D5 基准源归档（126 个 `_bench_d5_*.cpp`），
#:     613 的路径解析契约要求它们在库内可解析（缺它 ⇒ 6 条 D5 测试红）。
LINKS = [
    ("atoms", "atoms"),
    ("data", "data"),
    ("evidence", "evidence"),
    ("misconceptions", "misconceptions"),
    ("Book", "Book"),
    ("research", "research"),
    ("docs", "docs"),
    ("goldens", "goldens"),
    ("Examples", "Examples"),
    ("_archive/benchmarks", "_archive/benchmarks"),
]

IGNORE_BLOCK = """
# ── 665 A1：语料联结（junction → CPP-Bible）─────────────────────────────────
# 这些是**机器布局**：真实内容在 CPP-Bible 仓，verifier 通过联结复用同一份真相。
# 不进版本库（否则要么复制 3.4 GB，要么提交 symlink 条目，两者都更糟）。
# 重建命令：python tools/setup_corpus_links_665.py --apply
/evidence/
/misconceptions/
/Book/
/research/
/docs/
/goldens/
/Examples/atoms/
"""


def is_link(p: Path) -> bool:
    """是否为**联结/符号联接**（Windows 的 junction 不算 `is_symlink`，要单独判）。"""
    if not p.exists():
        return False
    try:
        if hasattr(os.path, "isjunction") and os.path.isjunction(p):   # py3.12+
            return True
    except OSError:
        pass
    if p.is_symlink():
        return True
    try:                                                                # FILE_ATTRIBUTE_REPARSE_POINT
        return bool(p.stat().st_file_attributes & 0x400)
    except (AttributeError, OSError):
        return False


def status() -> list[tuple[str, str]]:
    rows = []
    for rel, src in LINKS:
        p = ROOT / rel
        s = CPP / src
        if not s.exists():
            rows.append((rel, "源缺失(CPP-Bible 侧不在)"))
        elif is_link(p):
            rows.append((rel, "已是联结"))
        elif p.exists():
            rows.append((rel, "已存在（非联结，跳过）"))
        else:
            rows.append((rel, "缺 → 需建联结"))
    return rows


def make_link(rel: str, src: str) -> str:
    p = ROOT / rel
    s = CPP / src
    p.parent.mkdir(parents=True, exist_ok=True)
    # 用 mklink /J（目录联结，不需要管理员权限）；subprocess 传 list 避免 shell 解析问题
    r = subprocess.run(["cmd", "/c", "mklink", "/J", str(p), str(s)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return "ok" if r.returncode == 0 else f"fail: {(r.stdout or r.stderr).strip()[:80]}"


def ensure_ignore() -> str:
    gi = ROOT / ".gitignore"
    txt = gi.read_text(encoding="utf-8") if gi.is_file() else ""
    if "语料联结（junction" in txt:
        return "已存在"
    gi.write_text(txt.rstrip("\n") + "\n" + IGNORE_BLOCK, encoding="utf-8")
    return "已追加"


def selftest() -> int:
    ok = True
    for rel, src in LINKS:
        if not (CPP / src).exists():
            print(f"WARN 源不在：{src}")
            ok = False
    assert len({r for r, _ in LINKS}) == len(LINKS), "联结路径不得重复"
    print("setup_corpus_links_665 selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="665 A1：verifier 语料联结")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    rows = status()
    for rel, st in rows:
        print(f"  {rel:<18} {st}")
    if a.apply:
        for rel, src in LINKS:
            p = ROOT / rel
            if p.exists() or is_link(p):
                continue
            print(f"  link {rel}: {make_link(rel, src)}")
        print(f"  .gitignore: {ensure_ignore()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
