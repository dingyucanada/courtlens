# CourtLens Studio · 篮球复盘与内容制作系统

![CourtLens Studio 片单制作](docs/images/studio-playlist.png)

**从比赛素材到逐回合复核、分析、片单与交付，在一个单用户工作室里完成。**

[打开 Studio](https://dingyucanada.github.io/courtlens/) · [查看证据演示](https://dingyucanada.github.io/courtlens/demo.html) · [下载完整产品](https://github.com/dingyucanada/courtlens/releases/latest) · [Studio 使用说明](docs/Studio使用手册.md)

## v3.0：网页也能实际工作

公开网页已从固定一页演示升级为可保存项目的多页面应用。包含工作总览、比赛项目、回合复核、数据分析、片单制作、报告交付和存储设置。

- **自己的素材：** 导入浏览器可播放的视频，读取时长、尺寸与 SHA-256，保存视频 Blob；导入 CSV / JSON，最多 2,000 个回合，或手工逐条标记。
- **原始证据：** 原 CourtLens JSON 导入保留逐回合原记录和指标语义；可展开查看 Gravity、Leverage、轨迹与标注，备份原样保存。高级叠加和完整数据集处理仍使用原证据工作台。
- **真实复核：** 校正出手与结果时刻、球员、战术标签、笔记和坐标；保存修订历史、恢复旧版；跨标签页冲突拒绝覆盖；视频和内容变化撤销复核。
- **分析决策：** 球员、标签、结果筛选联动 FG%、eFG%、已记录得分、未知结果与输入期望得分；仅绘制实际提供坐标的投篮图。
- **内容制作：** 片段选择、排序、入出点裁切、顺序预览；批准项目后实时录制真实无声 WebM，单次最长 180 秒。
- **交付和备份：** 下载独立可打印 HTML 报告、CSV、按片单拼接的 VTT、项目 JSON 备份。备份不包含原视频，须另行保存。

Studio 使用当前浏览器的 IndexedDB，是本机数据、单用户应用；不提供账号、云同步或多人权限。发布到 GitHub Pages 的是应用文件，用户视频不会上传。相同浏览器、相同来源地址下可继续工作；线上与 localhost、不同端口和不同浏览器的存储互相独立。首次进入不制造项目，点击「载入合成演练」可完整体验。

本机 Python/SQLite/FFmpeg 工作台仍提供独立的持久工程、人工画面标注、后台 MP4 任务和可选 macOS 配音。两种工作区不自动同步；Studio 的备份用于 Studio，不冒充旧工作台 JSON。现有 14 页路演文件来自 v2.1，v3 的实际能力与验收以本 README 和 [Studio 验收报告](docs/Studio验收报告.md) 为准。

NBA 深蓝、红、白为视觉配色，CourtLens 为独立作品。内置素材全部合成，功能验收不代表真实 NBA 预测或自动战术识别精度。正式赛方素材、规则及云模型调用仍待相应实证。

## 启动与入口

在本目录运行：

```sh
python3 tools/launch.py --port 8765
```

启动器会先构建 Studio。打开 [Studio 工作室](http://127.0.0.1:8765/studio/) 使用新版；[FFmpeg / SQLite 工作区](http://127.0.0.1:8765/projects.html) 使用原本机工作流。[复盘台](http://127.0.0.1:8765/) 保留原演练入口；请从项目页点击“打开复盘”查看自己的持久项目。随包的 `启动工作台.command` 与 `启动工作台.bat` 会尝试从已知位置选择已安装且具备 Pillow 的渲染解释器，不自动安装依赖；平台验证范围见最终报告。停止服务按 Ctrl+C。

服务只绑定 `127.0.0.1`；启动器自动复制静态资源，无需 npm 安装或前端编译。先点击项目页右上角“本机功能”查看依赖。后端使用 Python 标准库；视频持久导入需要 FFprobe，成片导出还需要 FFmpeg 及渲染解释器中的 Pillow。Python 环境和外部工具版本以最终报告为准，Pillow 要求见 [requirements-media.txt](requirements-media.txt)。

如果启动解释器没有 Pillow，但另一个已安装解释器具备渲染依赖，可以指定：

```sh
python3 server.py --port 8765 --render-python /absolute/path/to/python
```

该路径应替换为本机真实解释器路径。也可通过 `COURTLENS_RENDER_PYTHON` 配置。缺少依赖时不会静默声称导出成功；先补齐依赖并重启服务，再重试。

## 原本机工作台的使用顺序

1. **创建项目。** 选择“从视频开始”“导入回合表”或“高级数据”，填写真实来源。也可用全合成演练体验。
2. **校正回合。** 填写视频秒数、投篮球员和投篮分值。新建占位回合不是自动识别结果；未知指标留空。
3. **标注与复核。** “画面标注”可添加箭头、矩形区域与文字。人工静态标注有独立来源，不能代表自动追踪已校准。
4. **保存项目。** 每次保存形成 SQLite 历史版本。修改会撤销网页的整体复核状态；核对后勾选“已核对回合时刻与来源”再保存。
5. **导出。** 在“导出记录”创建后台任务；本机支持时可选择中文配音。完成后下载 MP4、WebVTT 与分析 JSON，配音任务另附语音记录。每个任务冻结创建时的版本，继续编辑不改变已排队输入。

默认 MP4 包含画面叠加与字幕、没有音轨。macOS 本机 `say` 可用时，可选离线中文配音；它朗读已编译的同步字幕，不调用云模型。两种模式都不保留原视频音轨。配音不可用、过密或失败时明确报错，不会把无声中间视频冒充配音成片。Windows 当前不提供此配音能力，实际平台结果见最终报告。

## 原本机工作台的保存位置与冲突

默认数据位于本目录下 `workspace/`：项目及历史存在 `workspace.sqlite3`，已导入视频位于 `media/`，导出记录和结果位于 `jobs/`。可用 `--workspace /absolute/path/to/workspace` 指定目录。它不会被静态文件服务直接暴露；浏览器通过受控项目接口读取媒体。

项目页遇到 HTTP 409 版本冲突时，旧修改不会覆盖最新版本。先“下载我的草稿”，再“载入最新版本”并比对合并；草稿不是自动合并文件，也不是已保存历史。不要以为未点击保存的浏览器编辑已写进 SQLite。恢复旧版会创建新 revision，保留原历史。

标注页另有“下载标注草稿”，用于保存当前标注数据集 JSON；它不包含视频，也不能代替保存项目或完整工作区备份。

备份应先停止服务，再复制整个工作区。只复制数据库或只有成片都不足以完整恢复项目。当前没有自动云备份、多人协作、账号认证或公网部署功能；只在可信本机环境使用。详见 [产品架构与运维](docs/产品架构与运维.md)。

## 原本机工作台的数据与能力边界

- 每个视频最大 512 MiB；服务端核对文件格式、尺寸、时长及 SHA-256。浏览器能否解码仍取决于实际编码。
- CSV 支持最多 200 个回合，时间必须已经映射成视频秒数；错误定位到 CSV 记录结束的物理行。
- xFG 使用 0–1 概率；Gravity 保留来源单位；非空 Leverage 必须显式确认“0–1 回合胜率机会差”，不能冒充球员累计分。
- 人工标注使用 `origin=manual`、`frame_reviewed=true` 与 `author_note`，不改变原 `camera_segments.calibrated`。无轨迹时不会自动追踪球员。
- 系统不从任意转播独立识别人名、恢复场外位置或复现 NBA 专有统计模型。`official` 只是提供者声明，不是软件认证。

## 可选云规划器

网页工作流不调用外部模型。独立的 `tools/cloud_director.py` 可在明确启用且具备 AWS 凭据、模型权限和数据许可后调用 Bedrock；发送选定回合的结构化证据，不发送视频。模型选择已有声明 ID，本地编译可见文字与数值。目前只有模拟提供者的协议测试，**没有完成真实云调用**。配置与运行方法见 [产品架构与运维](docs/产品架构与运维.md)。

## 文档导航

- [产品使用手册](docs/产品使用手册.md)：从新建、标注到导出的操作与故障处理。
- [数据接口与接入](docs/数据接口与接入.md)：CSV、JSON、审核和本机 API。
- [方法与指标](docs/方法与指标.md)：指标解释、人工与追踪的证据边界。
- [参赛策略与产品方案](docs/参赛策略与产品方案.md)：作品主张、强替代、现场计划与路演。
- [专业产品研究](docs/专业产品研究.md)：一手来源、可借鉴机制和数据许可边界。
- [最终验收报告](docs/最终验收报告.md)：唯一的最终计数、实测环境、失败与未验证项汇总。

研究代码与参赛准备已形成可运行产品，但正式比赛规则、允许复用范围、原始素材授权和最终提交仍须按赛方要求核对。

## 复现测试

在项目根目录执行；媒体相关检查需要 FFmpeg/FFprobe、Pillow，macOS 配音检查另需 `say`。请使用装有 Pillow 的 Python 解释器。缺失依赖的跳过不能解释为验收通过。

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/*.test.cjs
python3 tests/independent_core.py
python3 tests/independent_media.py
python3 tests/media_export_checks.py
```

日常使用不需要 Node；它只用于前端逻辑测试。随交付包的验收证据记录实际版本、结果和独立反例。

## 网站构建与 GitHub 发布

`studio/` 是 v3 的浏览器工作室，`site/` 保留证据演示，`web/` 是 Python 本机工作台。构建结果根页为 Studio，`demo.html` 为演示。GitHub Pages 提供应用静态文件；项目与视频由浏览器保存在本机，Python 服务和用户工作区不上传至 Pages。

```sh
python3 tools/build_site.py --output ../site-dist --presentation docs/CourtLens-product-deck.pptx
python3 tools/test_site.py
node --test site/logic.test.mjs studio/domain.test.mjs studio/export.test.mjs studio/ui-boundaries.test.mjs
```

构建器直接调用 `core.engine` 生成双视角分析与 42 份证据回答，并核对视频 SHA-256。输出目录只允许已知发布文件；发现无关文件或符号链接会停止，防止意外上传。静态站不调用外部模型，也不上传浏览器操作。

推送 `main` 后，GitHub Actions 先运行自动检查，再构建和部署 Pages。首次配置、范围和版本记录见 [GitHub 发布说明](docs/GitHub发布说明.md)。
