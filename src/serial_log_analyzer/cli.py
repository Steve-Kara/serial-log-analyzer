"""命令行入口：sla <日志文件|->"""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .parser import LEVELS, Summary, filter_lines, summarize

RULE = "-" * 32


def _force_utf8_output() -> None:
    """Windows 控制台默认代码页是 GBK，直接 print 中文会变乱码。

    这里把标准输出/错误流强制切成 UTF-8。注意要容错：被 pytest 之类
    捕获时 stdout 不是 TextIOWrapper，没有 reconfigure 方法。
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except (AttributeError, ValueError):
            pass


def render(s: Summary, source: str, grep: Optional[str] = None) -> str:
    """把汇总结果渲染成给人看的文本。"""
    out: List[str] = []
    header = f"串口日志汇总  {source}"
    if grep:
        header += f"   [筛选: {grep}]"
    out.append(header)
    out.append(RULE)
    out.append(f"总行数      {s.total}")
    out.append(f"已解析      {s.parsed}")
    out.append(f"无法解析    {s.unparsed}")
    if s.duration is not None:
        out.append(f"时间跨度    {s.first_ts} → {s.last_ts}  ({s.duration:.3f}s)")
    elif s.parsed == 0:
        out.append("时间跨度    （没有可解析的日志行）")

    if s.by_level:
        out.append(RULE)
        out.append("级别分布")
        for lv in LEVELS:
            if s.by_level.get(lv):
                out.append(f"  {lv:<6} {s.by_level[lv]}")

    if s.top_errors:
        out.append(RULE)
        out.append("出现最多的 ERROR")
        for msg, n in s.top_errors:
            out.append(f"  {msg}   ×{n}")

    return "\n".join(out)


def main(argv: Optional[List[str]] = None) -> int:
    _force_utf8_output()
    ap = argparse.ArgumentParser(prog="sla", description="串口日志分析器")
    ap.add_argument("path", nargs="?", default="-", help="日志文件路径；- 表示从标准输入读")
    ap.add_argument("--grep", metavar="正则", help="只统计匹配该正则的日志行（大小写不敏感）")
    ap.add_argument("--version", action="version", version=f"sla {__version__}")
    args = ap.parse_args(argv)

    if args.path == "-":
        text, source = sys.stdin.read(), "标准输入"
    else:
        try:
            with open(args.path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except FileNotFoundError:
            print(f"找不到文件：{args.path}", file=sys.stderr)
            return 2
        source = args.path

    lines = text.splitlines()
    if args.grep:
        lines = list(filter_lines(lines, args.grep))

    print(render(summarize(lines), source, args.grep))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
