"""filter_lines 的测试。

新功能先写测试，是这个项目的习惯：测试同时充当"这个函数应该怎么用"的说明。
"""

from serial_log_analyzer.parser import filter_lines

LINES = [
    "[00:00:01.234] INFO  boot: firmware v1.2.3",
    "[00:00:02.900] ERROR i2c: timeout after 3 retries",
    "[00:00:03.500] ERROR i2c: timeout after 3 retries",
    "[00:00:03.900] INFO  main: loop tick 1000",
]


def test_filter_keeps_only_matching_lines():
    kept = list(filter_lines(LINES, "i2c"))
    assert len(kept) == 2
    assert all("i2c" in ln for ln in kept)


def test_filter_is_case_insensitive():
    assert len(list(filter_lines(LINES, "ERROR"))) == 2
    assert len(list(filter_lines(LINES, "error"))) == 2


def test_filter_no_match_yields_nothing():
    assert list(filter_lines(LINES, "这个关键字不存在")) == []


def test_filter_also_matches_unparsable_lines():
    lines = ["[00:00:01.000] INFO  a: 正常一行", "这行是乱码，但里面提到了 i2c"]
    assert list(filter_lines(lines, "i2c")) == ["这行是乱码，但里面提到了 i2c"]
