# ROS 2 文档本地构建指南

本文档记录如何在本地构建并预览 ROS 2 文档网站，包括环境准备、构建命令、常见问题与踩坑记录。

> **通用化说明**：本文所有命令默认在项目根目录内执行。文中出现的 `<项目目录>` 为占位符，请替换为你本地实际的项目路径（例如克隆本仓库后的目录名 `ROS2_documentation`）。

## 一、环境准备（首次或环境被清理后）

```bash
# 1. 进入项目目录（将 <项目目录> 替换为你本地实际路径）
cd <项目目录>

# 2. 创建 Python 虚拟环境（只需一次）
python3 -m venv ros2doc

# 3. 激活虚拟环境
source ros2doc/bin/activate

# 4. 安装依赖（版本锁定在 constraints.txt，保证可重现）
pip install -r requirements.txt -c constraints.txt
```

> 依赖安装时若出现 `generate-parameter-library-py`、`launch-ros` 的 `setuptools` 冲突警告，可忽略（那是系统 ROS 包引起的，不影响构建）。

验证工具链：

```bash
sphinx-build --version    # 应显示 8.2.x
sphinx-autobuild --version
```

## 二、构建与启动方式速查

| 场景 | 命令 |
|------|------|
| 一次性构建（默认 rolling） | `make html` |
| 一次性构建指定版本（如 jazzy） | `make html OPTS="-c . -W -j auto -D smv_current_version=jazzy"` |
| 实时开发服务 | `make serve` |
| 实时服务 + 指定版本 | `sphinx-autobuild --host 0.0.0.0 --port 2022 -c . -D smv_current_version=jazzy -W source build/html` |
| 多版本构建（部署用） | `make multiversion` |
| 自定义绑定地址/端口 | `make serve LIVE_HOST=127.0.0.1 LIVE_PORT=8080` |
| 指定并行构建进程数 | `make html JOBS=8` |
| 拼写检查 | `make spellcheck` |

> 各方式的详细说明与完整代码块见下「三、构建方式详解」。

## 三、构建方式详解

### 方式 1：一次性构建（生成静态 HTML）

**① 默认版本（`rolling`）：**

```bash
make html
```

**② 指定版本（如 `jazzy`）：** 覆盖 `OPTS` 变量传入版本参数即可：

```bash
make html OPTS="-c . -W -j auto -D smv_current_version=jazzy"
```

等价于直接调用 sphinx-build（把 `jazzy` 换成 `rolling` / `iron` / `humble` / … 即可）：

```bash
sphinx-build -c . -D smv_current_version=jazzy -W -j auto source build/html
```

**③ 用浏览器打开产物：**

```bash
sensible-browser build/html/index.html
NO_AT_BRIDGE=1 sensible-browser build/html/index.html   # 安静版：屏蔽 GTK 提示
```

> `Gtk-Message: Not loading module "atk-bridge"...` 说明：新版 GTK（3.22+）已把无障碍支持内置进自身，不再依赖独立的 `atk-bridge` 模块，所以每次启动 GTK 应用都会打印这行无害噪音，页面照常打开。`NO_AT_BRIDGE=1` 告诉 GTK「不需要桥接模块」从而消掉该输出，是否加随你。

### 方式 2：实时开发服务（推荐，边编辑边预览）

**① 启动默认服务：**

```bash
source ros2doc/bin/activate
make serve
```

服务启动在 `http://0.0.0.0:2022`，之后浏览器打开 `http://localhost:2022`。

**特点**：`sphinx-autobuild` 持续监视 `source/` 目录，每次保存 `.rst` 文件自动增量重建并刷新浏览器。

**② 自定义绑定地址/端口：**

```bash
make serve LIVE_HOST=127.0.0.1 LIVE_PORT=8080
```

**③ 指定版本 + 实时开发（如 `jazzy`）：** `make serve` 本身不带版本参数，用 `sphinx-autobuild` 透传 `-D` 给 `sphinx-build` 即可：

```bash
source ros2doc/bin/activate
sphinx-autobuild --host 0.0.0.0 --port 2022 -c . \
  -D smv_current_version=jazzy -W source build/html
```

这样既保留自动监视、保存即刷新的实时体验，又让页面中的 `{DISTRO}` 展开为指定版本（如上例为 `jazzy`，安装命令显示 `ros-jazzy-*`）。

> 注意：此方式下页面底部**没有**多版本切换器（那是 `sphinx-multiversion` 的 `html-page-context` 钩子在注入 `smv_metadata` 后才生成的），但对本地预览单个版本完全够用。

### 方式 3：多版本构建（部署用）

```bash
make multiversion
```

`sphinx-multiversion` 会遍历所有分支（`rolling`、`jazzy`、`iron`、…），为每个分支单独构建，生成 `build/html/<版本>/` 目录，并自动传入 `smv_current_version=<版本>`。注意：它会**忽略本地未提交的改动**，只构建各分支已提交的内容。

### 版本构建（`{DISTRO}` 宏展开）说明

文档源码中的 `{DISTRO}`、`{DISTRO_TITLE}`、`{DISTRO_TITLE_FULL}` 是**宏占位符**，构建时被替换成具体的 ROS 发行版名（如 `rolling`、`jazzy`）。`conf.py` 中定义的默认值：

```python
macros = {
    'DISTRO': 'rolling',
    'DISTRO_TITLE': 'Rolling',
    'DISTRO_TITLE_FULL': 'Rolling Ridley',
    'REPOS_FILE_BRANCH': 'rolling',
}
```

> ⚠️ `make html` 和 `make serve` **不会读取 git 分支**，始终使用上述默认值 `rolling`。因此即使当前分支是 `jazzy`，页面中的安装命令仍会显示 `ros-rolling-*`，这是正常现象，并非翻译问题。要构建指定版本，用「方式 1」的 `OPTS` 覆盖或「方式 2」的 `sphinx-autobuild -D`。

## 四、常见问题与踩坑记录

### 坑 1：终端里 `cd` 会被简化丢失

某些终端环境下 `cd ... && make serve` 实际不会切到项目目录，导致 `make` 找不到目标。

**解决**：用 `make -C` 显式指定目录：

```bash
source <项目目录>/ros2doc/bin/activate \
  && make -C <项目目录> serve
```

### 坑 2：`Adopters` 页面构建极慢（卡在 `reading sources`）

构建时若一直卡在 `reading sources` 阶段，大概率是 `Adopters` 页面的 URL 联网检查：`plugins/adopters_schema.py` 的 `validate_adopter_urls()` 会对 `adopters.yaml` 里 60+ 个外部 URL 做探测（每个 10 秒超时 × 3 次重试 + 指数退避），网络差时能卡好几分钟。这是**警告性质**的检查，不影响文档内容，也不会让 `-W` 构建失败。

**推荐做法（临时补丁 + 完成后还原）**：在该函数开头加 `return []` 跳过联网检查，构建完成后再删掉还原。

操作步骤：

1. 编辑 `plugins/adopters_schema.py`，在 `validate_adopter_urls()` 的 docstring 之后、`warnings = []` 之前加一行：

   ```python
   def validate_adopter_urls(adopters, timeout=10):
       """..."""
       return []  # TEMP-PATCH: skip network URL checks for faster local serve; revert after build
       warnings = []
       ...
   ```

2. 保存后重启 serve / 重新构建（`plugins/` 不在 sphinx-autobuild 监视范围，改了代码需重启服务才生效）：

   ```bash
   source ros2doc/bin/activate
   make -C <项目目录> serve
   ```

   或一次性构建：

   ```bash
   make html OPTS="-c . -W -j auto -D smv_current_version=jazzy"
   ```

3. **构建完成后还原**：删掉 `return []` 那一行，保存。

4. 用 `git status` / `git diff` 确认只剩翻译改动（`README.md`、`source/**` 等），`plugins/adopters_schema.py` 不残留：

   ```bash
   git status --short
   ```

> ⚠️ 之所以要还原：直接改 `.py` 源码会污染 `git diff`，且会悄悄禁用官方/CI 的失效链接检查，不能长期留在代码里。

### 坑 3：search 索引生成阶段看似卡住

构建到最后 `genindex.html` 已生成但 `searchindex.js` 未出现时，看起来像卡死，实际是 CPU 密集计算（进程状态为 `R`，`wchan=0`）。等待即可，最终会输出：

```
build succeeded.
The HTML pages are in build/html.
[sphinx-autobuild] Serving on http://0.0.0.0:2022
```

## 五、验证服务是否正常运行

```bash
ss -ltn | grep 2022                                            # 查看端口监听
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:2022 # 应返回 200
```

## 六、构建产物结构

- `build/html/` — 生成的静态站点（HTML、静态资源、图片等）
- `build/html/index.html` — 首页
- `build/html/sitemap.xml` — 站点地图
- `build/html/searchindex.js` — 搜索索引
- `build/html/.buildinfo` — 构建元信息（用于增量构建判断）
