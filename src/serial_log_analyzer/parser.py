"""解析串口日志行，并汇总统计。

日志行格式（可选的 tag: 前缀）：

    [00:00:01.234] INFO  boot: firmware v1.2.3
    [00:00:02.900] ERROR i2c: timeout after 3 retries
    [00:00:03.000] WARN  bus busy
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, Iterator, Optional

LEVELS = ("TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL")

LINE_RE = re.compile(
    r"^\[(?P<ts>\d{1,2}:\d{2}:\d{2}(?:\.\d{1,6})?)\]\s+"
    r"(?P<level>" + "|".join(LEVELS) + r")\s+"
    r"(?:(?P<tag>[A-Za-z0-9_.\-]+):\s+)"
    r"(?P<msg>.*)$"
)


@dataclass
class Entry:
    """一条解析成功的日志。"""

    ts: str
    level: str
    tag: Optional[str]
    msg: str

    @property
    def seconds(self) -> float:
        """把 时:分:秒[.毫秒] 换成秒，用于算时间跨度。"""
        fmt = "%H:%M:%S.%f" if "." in self.ts else "%H:%M:%S"
        t = datetime.strptime(self.ts, fmt)
        return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6


@dataclass
class Summary:
    """一次分析的汇总结果。"""

    total: int = 0
    parsed: int = 0
    unparsed: int = 0
    by_level: Counter = field(default_factory=Counter)
    top_errors: list = field(default_factory=list)
    first_ts: Optional[str] = None
    last_ts: Optional[str] = None
    duration: Optional[float] = None


def parse_line(line: str) -> Optional[Entry]:
    """解析一行；解析不出来返回 None（不抛异常，脏数据不该让工具崩）。"""
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    return Entry(ts=m["ts"], level=m["level"], tag=m["tag"], msg=m["msg"].strip())


def parse_lines(lines: Iterable[str]) -> Iterator[Optional[Entry]]:
    """逐行解析，产出 Entry 或 None。"""
    for ln in lines:
        yield parse_line(ln)


def summarize(lines: Iterable[str]) -> Summary:
    """统计行数、级别分布、时间跨度、最常见的错误。"""
    s = Summary()
    errors: Counter = Counter()
    first_s: Optional[float] = None
    last_s: Optional[float] = None

    for raw in lines:
        s.total += 1
        e = parse_line(raw)
        if e is None:
            s.unparsed += 1
            continue

        s.parsed += 1
        s.by_level[e.level] += 1
        if e.level in ("ERROR", "FATAL"):
            errors[e.msg] += 1

        if first_s is None:
            first_s = e.seconds
            s.first_ts = e.ts
        last_s = e.seconds
        s.last_ts = e.ts

    s.top_errors = errors.most_common(5)
    if first_s is not None and last_s is not None:
        s.duration = last_s - first_s
    return s
