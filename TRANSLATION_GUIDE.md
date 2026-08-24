# ROS 2 文档翻译规范（TRANSLATION GUIDE）

本文件用于指导将 ROS 2 官方文档（RST 格式）翻译为简体中文。
**核心原则：翻译语言要专业、通顺、符合中文表达习惯；同时保证 RST 语法完整、构建不报错。**

## 一、翻译范围

### 需要翻译
- 标题（注意下划线长度，见第四节）
- 正文段落
- 列表项文本
- 链接的**显示文字**（不翻译 URL）
- 图片替代文字（alt text）
- 表格单元格文本
- 指令（directive）中的说明性文字（如 `.. note::`、`.. warning::` 后的内容）

### 保留不翻译
- 代码块内容（`.. code-block::` 及缩进代码）
- 行内代码（`` `code` ``）
- 命令、路径、文件名、包名、节点名、消息名
- `:doc:` / `:ref:` / `:term:` 引用**标签**（但显示文字可翻译）
- toctree 里的文件路径
- 锚点定义 `.. _label:`（若需翻译引用文字，改用 `:ref:`中文 <label>`` 形式）
- 品牌名与专有名词：ROS、ROS 2、DDS、REP、MoveIt、Nav2、Gazebo 等

## 二、术语表（保持全文一致）

| 英文 | 中文 |
|------|------|
| workspace | 工作空间 |
| package | 包 / 软件包 |
| node | 节点 |
| topic | 话题 |
| service | 服务 |
| action | 动作 |
| launch / launch file | 启动 / 启动文件 |
| subscriber | 订阅者 |
| publisher | 发布者 |
| message (msg) | 消息 |
| overlay | 覆盖层 |
| underlay | 底层 |
| distribution | 发行版 |
| DDS | 数据分发服务（保留 DDS 缩写） |
| middleware | 中间件 |
| client library | 客户端库 |
| interface | 接口 |
| parameter | 参数 |
| graph | 图（ROS 图） |
| introspection | 内省 |
| capability | 能力（组件） |
| framework | 框架 |
| ecosystem | 生态 |

## 三、排版与语言规范

1. **中英文之间加空格**：`ROS 2 文档`、`Sphinx 的 -j auto`（中文排版习惯）。
2. **语言专业通顺**：优先意译，避免逐字直译导致的欧化句式。
   - 例：`make sure` → `确保`；`keep in mind` → `请记住`；`out of the box` → `开箱即用`。
3. **术语首次出现**可括注英文：`客户端库（client library）`。
4. 长句拆分为短句，符合中文习惯；保持原文的段落结构。
5. 保留原文的语气词与强调（如 `**不要**`），使用中文标点（。，：；（））。

## 四、RST 语法要求（构建不报错的关键）

### 1. 标题下划线长度
RST 标题下划线**必须不短于标题文字**。
中文按**显示宽度 2** 计算（每个汉字=2，ASCII 字符=1）。
例如 `开发环境准备` 宽度 = 3×2 + 2×1 = 8，下划线 `========` 至少 8 个。
可用脚本检查：`/usr/bin/python3 check_underlines.py`。

### 2. inline 标记后紧跟全角标点 → 报错
`**粗体**`、`:term:`API``、`*斜体*`、``代码``、`链接_` 后**紧跟**全角标点（。，：；（）等）
会触发 `start-string without end-string` 错误。
**修复**：在闭合标记与标点之间加空格：
- 错：`**注意**：`  →  对：`**注意** ：` 或 `**注意**：`
  > 实际规范：全角冒号等**不属于** ASCII 标点，需在 inline 闭合后加空格或改用全角括号包住。

### 3. 引用锚点（:ref: 与链接）
- `:ref:`引用文字 <label>`` —— label **不可翻译**，显示文字可翻译。
- 若锚点定义 `.. _label:` 是英文，而引用处翻译了显示文字，须用 `:ref:`中文 <英文label>`` 形式。
- 标题链接 `标题文字_` 引用时，若目标标题已翻译为中文，引用处也须用中文标题文字，并保证目标标题下划线够长。

### 4. 代码块与内容块
- `.. code-block:: <lang>` 后的代码**逐字节保留**（含缩进、空行）。
- `.. code-block:: console`、`.. code-block:: bash` 等语言标识符**不翻译**。
- `.. note::` / `.. warning::` / `.. tip::` / `.. important::` 指令名**不翻译**，只翻译其内容；内容需整体缩进对齐。

### 5. 占位符与替换
- `{DISTRO}`、`{DISTRO_TITLE}`、`{DISTRO_TITLE_FULL}` 等占位符**不翻译**。
- 全局替换（global_substitutions）如 `|packages|`、`|rolling|` **不翻译**。

## 五、翻译流程

1. **读取完整文件**（勿用摘要编辑）。
2. 翻译正文/标题/列表，保留所有 RST 语法结构。
3. 用脚本检查下划线长度与 inline 标点：
   - `/usr/bin/python3 check_underlines.py <file>`
   - `/usr/bin/python3 scan_inline.py <file>`
4. 用 `git diff` 复查，确保只改了文本、没动代码块。

## 六、构建验证

```bash
source ros2doc/bin/activate
make -C /home/nvidia/Desktop/ros2_documentation html   # 或 make serve 实时预览
```

- 构建须 `build succeeded`，无 WARNING/ERROR（除 sphinx_adopters 外部 URL 检查警告，属网络问题可忽略）。
- 实时服务：`make serve` 后访问 http://localhost:2022。

## 七、常用辅助脚本（被 git clean 清理后可重建）

- `fix_underlines.py`：按显示宽度修复中文标题下划线长度。
- `check_underlines.py`：检查所有标题下划线是否够长。
- `scan_inline.py`：扫描 inline 标记后紧跟全角标点的问题。
