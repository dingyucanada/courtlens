# CourtLens GitHub 发布说明

版本 v3.0，2026-09-22。

- 源码：https://github.com/dingyucanada/courtlens
- Studio 工作室：https://dingyucanada.github.io/courtlens/
- 证据演示：https://dingyucanada.github.io/courtlens/demo.html
- 发布包：https://github.com/dingyucanada/courtlens/releases/latest

## 运行形态

GitHub Pages 现为可用的单用户浏览器工作室，支持项目创建、视频与 CSV/JSON 导入、复核、剪辑编排、报告与 WebM 成片。项目、版本历史和视频保存在当前浏览器 IndexedDB，数据不会自动同步到其他设备或原 Python 工作区。定期下载 JSON 备份，并另行保管原视频。

原证据演示保留于 demo.html。其固定合成视频、双视角、证据定位与分析下载由正式 Python 引擎构建为 JSON，不调用云模型，不代表真实 NBA 模型准确率。

原本机 Python 服务保留独立 SQLite 工作区与 FFmpeg 精确 MP4 成片。启动后 /studio/ 是浏览器工作室，/projects.html 是本机服务项目库；两套工作区不自动互通。公网静态网站不包含 Python 服务、账号系统或云端数据库。

## 发布和维护

修改 studio/、site/ 或分析引擎后运行 README 中的检查。推送 main 会触发 Pages 构建与部署。Product checks 工作流在 Linux 运行完整检查；系统语音属于 macOS 专有能力，Linux 对此项显式跳过。

现有 docs/CourtLens-product-deck.pptx 为 v2.1 图表版演示文稿；它与 Studio v3 新增流程的范围不同，未冒称 v3 路演稿。新版系统说明见 Studio使用手册.md，真实测试范围见 Studio验收报告.md。

浏览器成片是无音频 WebM、最多 180 秒、按播放时间录制；录制需要前台活动标签页。MediaRecorder 容器可能不包含有限时长或完整寻址索引，精确剪辑和音频交付请使用本机 FFmpeg 路线。

发布目录采用白名单检查，不包括测试页面、用户视频、工作区、密钥或临时日志。GitHub Actions 使用平台短期令牌，源码不嵌入凭据。
