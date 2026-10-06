# 变更日志

本文件记录项目的所有重要变更。格式参考
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

## [0.1.1] - 2026-10-06

### 新增

- `--grep` 参数：按正则筛选日志行后再统计，正则大小写不敏感（[#1](https://github.com/Steve-Kara/serial-log-analyzer/pull/1)）
- 新增 `filter_lines()` 函数，连同 4 个单元测试

### 修复

- Windows 控制台（GBK 代码页）下中文输出乱码：标准输出显式重设为 UTF-8
- 仓库加入 GitHub Actions：Ubuntu / Windows × Python 3.9 / 3.12 四个组合自动跑测试

## [0.1.0] - 2026-10-06

### 新增

- 项目骨架：README / LICENSE / pyproject.toml / .gitignore
- 解析 `[时:分:秒.毫秒] 级别 标签 消息` 格式的日志行，脏数据不致命
- 汇总：总行数 / 已解析 / 级别分布 / 时间跨度 / 最常见的 ERROR
- CLI 入口 `sla`，支持文件参数与标准输入管道
- 6 个单元测试
