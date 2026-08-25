# ROS 2 文档（简体中文汉化版）

本项目是 [ROS 2 官方文档](https://docs.ros.org/en) 的**简体中文汉化版本**：将 300+ 个 RST 源文件翻译为中文，并通过 GitHub Actions + GitHub Pages 自动构建、发布为静态网站。

## 🌐 在线站点

🔗 **https://1Q08.github.io/ROS2_documentation/**

本站由 GitHub Actions 在每次推送到 `main` 分支时自动构建（Sphinx → 静态 HTML）并部署到 GitHub Pages。构建工作流见 [`.github/workflows/pages.yml`](./.github/workflows/pages.yml)。

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| [README_gf.md](./README_gf.md) | 项目完整介绍：官方 README 汉化版（环境准备、构建方法、贡献指南） |
| [TRANSLATION_GUIDE.md](./TRANSLATION_GUIDE.md) | 翻译指南：术语表、翻译规范、常见注意事项 |
| [BUILD.md](./BUILD.md) | 本地构建指南：环境准备、构建与启动方式、常见踩坑记录 |

## 🛠 技术栈

- **Sphinx** + **sphinx-rtd-theme**：静态文档生成
- **GitHub Actions**：自动构建与部署
- **GitHub Pages**：静态站点托管

## 🚀 快速构建（本地）

```bash
python3 -m venv ros2doc
source ros2doc/bin/activate
pip install -r requirements.txt -c constraints.txt
make html
sensible-browser build/html/index.html
```

详细构建步骤见 [BUILD.md](./BUILD.md)。

