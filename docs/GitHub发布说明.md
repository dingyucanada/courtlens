# CourtLens GitHub 发布说明

版本 v2.1，2026-09-22。

- 源码：https://github.com/dingyucanada/courtlens
- 在线演练：https://dingyucanada.github.io/courtlens/
- 产品与 PPT：https://github.com/dingyucanada/courtlens/releases/latest

## 两种运行形态

在线版是 GitHub Pages 静态演练，提供固定合成视频、双视角、证据定位、指标比较和分析下载。数据与规则回答由正式 Python 引擎构建为 JSON；页面不调用云模型。

完整产品在本机运行，支持用户视频、数据导入、持久项目、版本历史、人工标注与异步成片任务。SQLite 数据库和用户视频留在本机，不随代码提交。Pages 不能运行 Python 服务，因此没有把本机编辑按钮假装成公网服务。

## 维护

修改 `site/` 或分析引擎后运行 README 的测试，向 `main` 推送会触发 Pages 构建与部署。另一个 Product checks 工作流在 Linux 运行完整测试集，系统语音属于 macOS 专有能力，Linux 对此项显式跳过，不能算作跨平台语音验收。

新版演示文稿保存为 `docs/CourtLens-product-deck.pptx`，网站构建时复制为 `presentation.pptx`，下载按钮自动启用。演示图表中的合成数据不代表真实 NBA 准确率，详细来源见图表脚注、讲者备注与方法文档。

发布目录采用白名单检查，拒绝无关残留或符号链接。不要把密钥、`.env`、`workspace/`、用户视频、内部测试日志或赛事未公开数据加入仓库。GitHub Actions 使用平台提供的短期令牌，源码没有嵌入凭据。

官方机制参考：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
