"""parser 模块的测试。

测试的意义：它把"我以为它能用"变成"我证明它能用"。
第 5 课我们会让 GitHub 每次提交都自动跑这些测试。
"""

from serial_log_analyzer.parser import Entry, parse_line, summarize


def test_parse_basic_line():
    e = parse_line("[00:00:01.234] INFO  boot: firmware v1.2.3")
    assert isinstance(e, Entry)
    assert e.ts == "00:00:01.234"
    assert e.level == "INFO"
    assert e.tag == "boot"
    assert e.msg == "firmware v1.2.3"


def test_parse_line_without_tag():
    e = parse_line("[00:00:03.000] WARN  bus busy")
    assert e is not None
    assert e.tag is None
    assert e.msg == "bus busy"


def test_garbage_line_returns_none():
    assert parse_line("乱码：固件重启，这行没有时间戳") is None
    assert parse_line("") is None


def test_summarize_counts_levels():
    lines = [
        "[00:00:01.000] INFO  a: one",
        "[00:00:02.000] ERROR b: bad",
        "[00:00:03.000] ERROR b: bad",
        "garbage",
    ]
    s = summarize(lines)
    assert s.total == 4
    assert s.parsed == 3
    assert s.unparsed == 1
    assert s.by_level["INFO"] == 1
    assert s.by_level["ERROR"] == 2
    assert s.top_errors == [("bad", 2)]


def test_summarize_duration():
    s = summarize(["[00:00:01.500] INFO  x: a", "[00:00:03.000] INFO  x: b"])
    assert s.first_ts == "00:00:01.500"
    assert s.last_ts == "00:00:03.000"
    assert round(s.duration, 3) == 1.5


def test_summarize_empty_input():
    s = summarize([])
    assert s.total == 0
    assert s.parsed == 0
    assert s.duration is None
