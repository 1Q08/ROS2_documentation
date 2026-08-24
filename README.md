# ROS 2 文档

本仓库包含托管在 [https://docs.ros.org/en](https://docs.ros.org/en) 上的 ROS 2 文档源文件。
本仓库中的源文件由 [Jenkins 任务](https://build.ros2.org/job/doc_ros2doc/) 每晚构建并上传到该站点。

## 为文档做贡献

我们非常欢迎对本站点的贡献。
请参阅 [贡献 ROS 2 文档](https://docs.ros.org/en/rolling/The-ROS2-Project/Contributing/Contributing-to-documentation.html) 页面了解更多信息。

## 为 ROS 2 做贡献

要为 ROS 2 源代码项目做贡献，请参阅 [ROS 2 贡献指南](https://docs.ros.org/en/rolling/The-ROS2-Project/Contributing.html)。

## 先决条件

要构建本文档，你需要安装

* make
* graphviz

配合 [venv](https://docs.python.org/3/library/venv.html)

```
# activate the venv
python3 -m venv ros2doc

# activate venv
source ros2doc/bin/activate

# install required packages
pip install -r requirements.txt -c constraints.txt

# deactivate the venv
(ros2doc) deactivate
```

### 固定版本

开发时我们目前使用 Noble (Ubuntu 24.04) 作为构建平台。
所有 Python 版本都固定在 constraints 文件中，以确保构建可重现。
要升级系统，请先验证一切正常，然后使用 `pip freeze > constraints.txt` 锁定要升级的版本。

## 构建 HTML

### 本地开发测试

要在本地测试当前代码树，请使用：

`make html`

`sensible-browser build/html/index.html`

### 实时重载本地开发

要避免手动重新构建和刷新浏览器，请使用 [`sphinx-autobuild`](https://github.com/sphinx-doc/sphinx-autobuild) 来迭代文档。
它会监视源文件，在保存时增量重建，并通过自动浏览器重载提供结果。

`sphinx-autobuild` 已作为 `requirements.txt` 的一部分安装。
使用以下命令启动实时服务器：

```
make serve
```

然后在浏览器中打开 `http://localhost:2022`。

`serve` 目标默认绑定到 `0.0.0.0:2022`（带一点 ROS 2 风格），因此服务器可通过 devcontainer / 端口转发访问。
如有需要，可覆盖绑定地址或端口：

```
make serve LIVE_HOST=127.0.0.1 LIVE_PORT=8080
```

### 拼写检查

要检查拼写，请使用：

`make spellcheck`

> [!NOTE]
> 如果检测到需要忽略的特定单词，请将其添加到 [codespell_whitelist](./codespell_whitelist.txt)。 \
> 如需包含要应用的自定义更正，请将其添加到 [codespell_dictionary](./codespell_dictionary.txt)。

### 部署测试

要测试部署到网站的多站点版本，请使用：

`make multiversion`

`sensible-browser build/html/rolling/index.html`

**注意：** 这会忽略本地工作区的改动，并从各个分支构建。

### 更快的（并行）构建

`make html` 和 `make multiversion` 默认都会并行构建 Sphinx，
每个 CPU 核心使用一个工作进程（Sphinx 的 `-j auto`）。这在 Sphinx 内部处理，
因此在 Linux、macOS 和 Windows 上效果相同 —— 请注意，普通的
`make -j` 并**没有**帮助，因为每次构建都是单次 Sphinx 调用。

若要固定工作进程数量而不是自动检测，可设置 `JOBS`：

```
make html JOBS=8
make multiversion JOBS=8
```

**注意：** 对于 `make multiversion`，`JOBS` 会在*每个*分支的构建内部并行化工作；
各分支本身仍然是一个接一个地构建。

### 面向 Windows (WSL) 用户的说明

在使用 WSL 于 Windows 上构建文档时，建议在 Linux 文件系统内（例如 `/home/<user>/` 下）克隆并使用本仓库，
而不是放在 `/mnt/c` 下。

在 `/mnt/c` 下工作可能会导致构建变慢，并出现与 Sphinx 和 ROS 工具链相关的文件系统问题。
