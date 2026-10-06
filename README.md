# serial-log-analyzer

[![Test](https://github.com/Steve-Kara/serial-log-analyzer/actions/workflows/test.yml/badge.svg)](https://github.com/Steve-Kara/serial-log-analyzer/actions/workflows/test.yml)

> 串口日志分析器 —— 把 STM32 串口日志变成一张能读的汇总表。
> A tiny CLI that turns messy serial logs into a readable summary.

## 它解决什么问题

调试 STM32 时串口会刷出成百上千行日志。想知道「总共多少条 ERROR」「卡了多久」「哪条报错出现最多」，
靠肉眼翻是不现实的。这个工具读一个日志文件，直接给出汇总。

## 特性

- 解析 `[时:分:秒.毫秒] 级别 标签 消息` 格式的日志行
- 按级别统计（TRACE / DEBUG / INFO / WARN / ERROR / FATAL）
- 计算时间跨度、报错最多的消息
- 容忍脏数据：无法解析的行会单独计数，不会让程序崩掉

## 安装

```bash
pip install -e ".[dev]"
```

## 用法

```bash
sla examples/sample.log
```

或者不带参数从标准输入读：

```bash
type log.txt | sla -
```

## 示例输出

```text
串口日志汇总  examples/sample.log
--------------------------------
总行数      9
已解析      8
无法解析    1
时间跨度    00:00:01.234 → 00:00:03.900  (2.666s)
--------------------------------
级别分布
  DEBUG  2
  INFO   3
  WARN   1
  ERROR  2
--------------------------------
出现最多的 ERROR
  timeout after 3 retries   ×2
```

## 日志格式

```text
[00:00:01.234] INFO  boot: firmware v1.2.3
[00:00:02.900] ERROR i2c: timeout after 3 retries
```

## 开发

```bash
pytest            # 跑测试
```

## 路线图

- [ ] 支持自定义时间戳格式（有些固件用 `tick` 而不是时钟）
- [ ] 导出 CSV / Markdown 报告
- [ ] `--grep` 过滤关键字
- [ ] 自动识别常见的 FreeRTOS / HAL 错误码
- [ ] 过滤「与主程序无关」的报错，不计入统计

## 许可

[MIT](LICENSE) © 2026 Steve-Kara
