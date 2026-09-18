# 文档因子归档

本项目是 `microfactor` 文档挖掘因子的独立、可审计归档，不参与因子计算或调度。

当前归档固定为：

- 393 个文档因子，其中 247 个精确复现、146 个近似复现。
- 332 个已发布并完成评估的因子，其中 84 个通过、248 个拒绝。
- 61 个尚未发布、尚未评估的候选因子。
- Factorcalc/Factoreval 快照：`snapshot_e3e73aa97706fd71f27ad486`。
- Factoreval 批次：`20260917_231028_ee6693d0`。

## 目录

- `archive.toml`：全部来源分卷的总索引。
- `configs/evaluation/daily-v1.toml`：固定评估合同。
- `factors/daily/*.qha`：QHA v1 声明式公式。
- `archives/*/manifest.toml`：按逻辑来源拆分的清单。
- `archives/*/IDEA-*.md`：因子说明、来源和评估结论。
- `sources/`：60 个来源文件的原目录结构副本。
- `evaluations/factor-evaluation.csv`：固定批次的完整评估指标。

QHA v1 是 UTF-8、TOML 兼容的声明格式。它保存公式契约和当前 Python 实现指针，
但不定义新的因子执行引擎。

## 构建

从本目录执行：

```powershell
C:\Users\admin\Desktop\quant-xuck\factoreval\.venv\Scripts\python.exe tools\build_archive.py
```

生成器读取兄弟目录中的 `microfactor`、`factoreval` 和
`D:\BaiduNetdiskDownload`，并使用 `copy2` 将全部来源复制到本项目的 `sources/`，
保留原相对路径、文件名、内容和修改时间。
来源 `reference` 始终使用构建时文件的实际 SHA-256；若它与研究库存中的历史哈希不同，
对应 IDEA 会同时记录两者，保留来源漂移证据。

## 校验

```powershell
C:\Users\admin\Desktop\quant-xuck\factoreval\.venv\Scripts\python.exe tools\validate_archive.py
```

校验包括数量、TOML 结构、来源哈希、内容快照、注册元数据、评估状态，以及两次临时
构建的字节级一致性。
