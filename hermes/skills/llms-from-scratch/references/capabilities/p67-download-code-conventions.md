# 下载代码三条工程约定 (p67) — Router 能力卡

> Stage 2 RIA++ Router 卡 | 来源书: Build a Large Language Model (From Scratch) (Raschka) 第 2/5 章 | 绑定单元: p67 | 支持材料: ce13 (版本/环境), ce15
> 去向: source-router 服务; 纸面 walkthrough 验证, 阶段 4 实测前不声称"已实测"

## R — Reading (原文)

> "response = requests.get(url, timeout=30)\nresponse.raise_for_status()"

— Raschka, ch02 (ch02_01_main-chapter-code_ch02.txt @69-70; ch05 @284-285 同模式)

同节: 外层 `if not os.path.exists(file_path)` 缓存跳过。自译: 下载数据/权重的三条约定——①先查本地缓存, 已存在即跳过; ②requests 带 30 秒超时; ③非 2xx 立即 raise_for_status 抛错, 不带病写文件。

## I — Interpretation (自述)

三条约定各自堵一个真实故障: 缓存检查避免重复下载大文件; timeout 防止网络挂起把脚本吊死 (urllib 默认无超时, 书明确说 requests 更稳); raise_for_status 把 HTTP 4xx/5xx 变成异常, 避免"下载失败"被当成空文件写盘、错误延迟暴露。任何写"从 URL 拉数据/权重"的代码都应默认带齐三条, 缺失即补。

## A1 — Application Example

### 示例: 下载 the-verdict.txt (原书代码例)

- **类型与来源**: 原书 worked_example (ch02 下载数据文件的标准块)。
- **问题/输入**: URL → the-verdict.txt。
- **方法论的使用**: os.path.exists 不存在才请求 → requests.get(url, timeout=30) → raise_for_status → 写盘。
- **结果**: 文件就位供后续分词; 二次运行直接命中缓存跳过 (规则可复算)。

## A2 — Future Trigger ★

### 情境 / 语言信号

1. 写任何数据集/模型权重下载脚本、下载偶发挂起或静默失败; 关键词 "下载 / requests timeout / raise_for_status / urllib"。

### 与相邻 skill 区分

- 与 `gpt2-pretraining-pipeline` (f14 排障): 那是环境级故障 (SSL/illegal instruction); 本卡是下载代码的写法约定本身。

## E — Execution

**必需输入**: URL 列表 + 目标路径。

1. 每个文件: if not os.path.exists → 请求 (timeout=30) → raise_for_status → 写盘; 已存在跳过。
2. 失败处理: 抛错即停 (不吞异常); 书中另有备用源分支先例 (预转换 PyTorch 权重作备选)——多源场景照此加 fallback。
3. 复核: 文件大小/行数与预期一致再进入下游。

**输出契约**: 就位文件 + 来源日志; 完成标准 = 下游步骤能读且校验通过。

## B — Boundary

- 不要用于: 需要认证/限流的 API 下载 (加会话/重试策略, 三条约定不覆盖); 大文件断点续传 (需额外机制)。
- 环境边界 (ce13): 公司代理/SSL 拦截是环境问题, 代码正确也会失败, 按 f14 排障处理。
- 约定边界: timeout=30 是书中取值, 大文件可调大, 但"必须显式设 timeout"不可省。
