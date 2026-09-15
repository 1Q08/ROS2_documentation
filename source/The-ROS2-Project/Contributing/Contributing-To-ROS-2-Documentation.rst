.. redirect-from::

    Contributing/Contributing-To-ROS-2-Documentation

为 ROS 2 文档做贡献
===================

.. contents:: 目录
   :depth: 2
   :local:

非常欢迎您为本网站做出贡献。
本页介绍如何为 ROS 2 文档做贡献。
在贡献之前，请务必仔细阅读以下各节。

本网站使用 `Sphinx <https://www.sphinx-doc.org/en/master/>`_ 构建，并特别使用了 `Sphinx multiversion <https://sphinx-contrib.github.io/multiversion/main/index.html>`_。

分支结构
--------

文档的源代码位于 `ROS 2 Documentation GitHub 仓库 <https://github.com/ros2/ros2_documentation>`_ 中。
该仓库为每个 ROS 2 发行版设置了一个分支，以处理各发行版之间的差异。
如果某项更改适用于所有 ROS 2 发行版，则应将其提交到 ``rolling`` 分支（随后会视情况进行反向移植）。
如果某项更改仅针对某个特定的 ROS 2 发行版，则应将其提交到相应的分支。

源文件结构
----------

本网站的所有源文件都位于 ``source`` 子目录下。
各种 Sphinx 插件的模板位于 ``source/_templates`` 下。
根目录包含本地构建网站以进行测试所需的配置和文件。

在本地构建网站
--------------

首先创建一个 `venv <https://docs.python.org/3/library/venv.html>`__ 来构建文档：

.. code-block:: console

   $ python3 -m venv ros2doc  # create venv
   $ source ros2doc/bin/activate  # activate venv

然后安装位于 ``requirements.txt`` 文件中的依赖项：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ pip install -r requirements.txt -c constraints.txt

  .. group-tab:: macOS

    .. code-block:: console

       $ pip install -r requirements.txt -c constraints.txt

  .. group-tab:: Windows

    .. code-block:: console

      $ python -m pip install -r requirements.txt -c constraints.txt

为了让 Sphinx 能够生成图表，``dot`` 命令必须可用。

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

       $ sudo apt update ; sudo apt install graphviz

  .. group-tab:: macOS

    .. code-block:: console

      $ brew install graphviz

  .. group-tab:: Windows

      从 `Graphviz 下载页面 <https://graphviz.gitlab.io/_pages/Download/Download_windows.html>`__ 下载安装程序并进行安装。
      确保允许安装程序将其添加到 Windows 的 ``%PATH%`` 中，否则 Sphinx 将无法找到它。

为单个分支构建网站
^^^^^^^^^^^^^^^^^^

若要仅为当前分支构建网站，请在仓库的顶层输入 ``make html``。
这是测试本地更改的推荐方式。

.. code-block:: console

   $ make html

构建过程可能需要一些时间。
要查看输出，请在浏览器中打开 ``build/html/index.html``。

本地开发的实时重载
^^^^^^^^^^^^^^^^^^

在迭代文档时，不必在每次编辑后重新运行 ``make html`` 并刷新浏览器，而可以使用 `sphinx-autobuild <https://github.com/sphinx-doc/sphinx-autobuild>`__ 来监视源文件、在保存时增量重建，并通过浏览器自动重载来提供结果。

``sphinx-autobuild`` 已作为 ``requirements.txt`` 的一部分安装。
使用以下命令启动实时服务器：

.. code-block:: console

   $ make serve

然后在浏览器中打开 ``http://localhost:2022``。

``serve`` 目标默认绑定到 ``0.0.0.0:2022``，因此可以通过 devcontainer / 端口转发访问该服务器。
如有需要，可以覆盖绑定地址或端口：

.. code-block:: console

   $ make serve LIVE_HOST=127.0.0.1 LIVE_PORT=8080


检查 / 测试网站
^^^^^^^^^^^^^^^

您可以使用以下命令在本地运行文档测试（使用 `doc8 <https://github.com/PyCQA/doc8>`_）：

.. code-block:: console

   $ make test

您可以使用以下命令在本地运行 Python 文档工具测试（使用 `pytest <https://docs.pytest.org/en/stable/>`_）：

.. code-block:: console

   $ make test-tools

您可以使用以下命令在本地运行 Python 文档工具测试（使用 `pytest <https://docs.pytest.org/en/stable/>`_）：

.. code-block:: console

   make test-tools

您可以使用以下命令在本地运行文档 linter（使用 `sphinx-lint <https://github.com/sphinx-contrib/sphinx-lint>`_）：

.. code-block:: console

   $ make lint

您可以使用以下命令在本地运行文档拼写检查器（使用 `codespell <https://github.com/codespell-project/codespell>`_）：

.. code-block:: console

   $ make spellcheck

.. note::

   如果该检查检测到需要忽略的特定单词，请将其添加到 `codespell_whitelist <https://github.com/ros2/ros2_documentation/blob/{REPOS_FILE_BRANCH}/codespell_whitelist.txt>`_ 中。

要了解关于拼写检查的更多信息，请参阅 :ref:`拼写检查 <spelling-check>`

通过 GitHub CI 查看网站
^^^^^^^^^^^^^^^^^^^^^^^

对于 ROS 2 文档的小改动，您可以使用 Github Actions 中生成的产物以渲染后的 HTML 形式查看所做的更改。
"build" 操作会将整个 ROS 文档生成为一个可下载的 Zip 文件，其中包含 `docs.ros.org <https://docs.ros.org/>`_ 的所有 HTML。
该构建操作会在通过测试操作和 lint 操作后触发。

要下载并查看您的更改，首先转到您的拉取请求，在标题下点击 "Checks" 选项卡。
在检查页面的左侧，点击 "tests" 下的 "Test" 部分，再点击 "build" 对话框。
这将在右侧打开一个菜单，您可以在其中点击 "Upload document artifacts"，然后滚动到底部，在 "Artifact download URL" 标题下查看 Zip 压缩 HTML 文件的下载链接。

.. image:: ./images/github_action.png
  :width: 100%
  :alt: 在 ROS Github action 上查找渲染后的 HTML 文件的步骤

为所有分支构建网站
^^^^^^^^^^^^^^^^^^

要为所有分支构建网站，请从 ``rolling`` 分支输入 ``make multiversion``。
这有两个缺点：

#. multiversion 插件不支持增量构建，因此它总是重新构建所有内容。
   这可能会很慢。

#. 输入 ``make multiversion`` 时，它总是会检出 ``conf.py`` 文件中列出的确切分支。
   这意味着本地更改不会显示出来。

要在 multiversion 输出中显示本地更改，您必须先将更改提交到本地分支。
然后您必须编辑 `conf.py <https://github.com/ros2/ros2_documentation/blob/rolling/conf.py>`_ 文件，并将 ``smv_branch_whitelist`` 变量更改为指向您的分支。

检查失效链接
^^^^^^^^^^^^

要检查网站上的失效链接，请运行：

.. code-block:: console

   $ make linkcheck

这将检查整个网站的失效链接，并将结果输出到屏幕和 ``build/linkcheck``。

.. _spelling-check:

拼写检查
^^^^^^^^

``make spellcheck`` 命令会扫描文档文件并标记任何拼写错误。
如果检测到错误，请查看建议并根据需要更新拉取请求。

某些单词（例如技术术语或专有名词）可能会被误标记为拼写错误。
如果遇到这种情况，您可以将其添加到忽略列表中，以防止将来再次被标记。
为此，请按如下方式将其添加到 `codespell_whitelist <https://github.com/ros2/ros2_documentation/blob/{REPOS_FILE_BRANCH}/codespell_whitelist.txt>`_ 文件中：

.. code-block:: text

   empy
   jupyter
   lets
   ws

要包含 ``codespell`` 应应用的自定义更正，您可以按如下方式将其添加到 `codespell_dictionary <https://github.com/ros2/ros2_documentation/blob/{REPOS_FILE_BRANCH}/codespell_dictionary.txt>`_ 文件中：

.. code-block:: text

   amnet->ament
   colcn->colcon
   rosabg->rosbag
   rosdistroy->rosdistro

要检查字典，您可以运行 ``make check-dictionaries`` 命令。
这将检查字典中的空行以及前导/尾随空格。
如果它报告字典有问题，您可以运行 ``make sort-dictionaries`` 命令。
如果发现任何问题，该命令会自动修改字典。

从 ROS Wiki 迁移页面
--------------------

将页面从 `ROS Wiki <https://wiki.ros.org>`_ 迁移到 ROS 2 文档的第一步是确定该页面是否需要迁移。
通过在 https://docs.ros.org/en/{DISTRO} 上搜索相关术语，检查该内容或类似内容是否已经存在。
如果它已经被迁移了，那么恭喜！
您就完成了。
如果它尚未被迁移，那么请考虑它是否值得保留。
您或其他人觉得有用并经常参考的页面是很好的候选对象，前提是它们没有被其他文档所取代。
针对当前发行版不再支持的 ROS 项目和功能的页面不应被迁移。

迁移 ROS Wiki 页面的下一步是确定迁移页面的正确位置。
只有涵盖 ROS 核心概念的 ROS Wiki 页面才属于 ROS 文档，这些页面应迁移到 ROS 文档中的合理位置。
特定于软件包的文档应迁移到该软件包源代码仓库中生成的软件包级文档。
软件包级文档更新后，它将作为 `软件包级文档的一部分 <https://docs.ros.org/en/{DISTRO}/p/>`__ 可见。
如果您不确定是否迁移某个页面以及迁移到哪里，请通过 https://github.com/ros2/ros2_documentation 上的 issue 或 https://discourse.openrobotics.org/ 与我们联系。

一旦您确定某个 ROS Wiki 页面值得迁移，并在 ROS 文档中找到了合适的落点，迁移过程的下一步就是设置迁移该页面所需的转换工具。
在大多数情况下，将单个 ROS Wiki 页面迁移到 ROS 文档所需的唯一工具是 `PanDoc <https://pandoc.org/>`_ 命令行工具和一个文本编辑器。
PanDoc 受大多数现代操作系统的支持，可使用其网站上提供的安装说明进行安装。
值得注意的是，ROS Wiki 使用的是较旧的 wiki 技术（MoinMoin），因此所使用的标记语言是 `MediaWiki <https://www.mediawiki.org/wiki/Help:Formatting>`__ 格式的一种晦涩方言。
我们发现，从 ROS Wiki 迁移页面的最简单方法是使用 PanDoc 将其从 HTML 转换为 reStructuredText。


迁移 Wiki 文件
^^^^^^^^^^^^^^

#. 克隆相应的仓库。
   如果您要将页面迁移到此处托管的官方文档，则应克隆 https://github.com/ros2/ros2_documentation。

#. 为您要迁移的页面创建一个新的 Github 分支。
   我们建议使用类似 ``pagename-migration`` 的名称。

#. 使用 wget 或类似工具将相应的 ROS Wiki 页面下载为 html 文件（例如 ``wget -O urdf.html https://wiki.ros.org/urdf``）。
   或者，您可以使用网页浏览器保存该页面的 HTML。

#. 接下来，您需要删除所下载文件中多余的 HTML。
   使用浏览器的开发者模式，找到 Wiki 页面中第一个有用的 HTML 元素名称。
   在大多数情况下，可以安全地删除文件中从第三行开始、以 ``<head>`` 标签开头一直到第一个 ``<h1>`` 标签开始处的所有 HTML。
   如果存在目录，第一个有用的标签可能是 ``<h2>`` 标签。
   类似地，ROS wiki 包含一些页脚文本，它以 ``<div id="pagebottom"></div>`` 开头，结束于 ``</body></html>`` 正上方，也可以删除。

#. 通过在 HTML 和 reStructuredText 之间运行 PanDoc 转换来转换您的 html 文件。
   以下命令将 HTML 文件转换为等效的 reStructuredText 文件：``pandoc -f html -t rst urdf.html > URDF.rst``。

#. 尝试使用 ``make html`` 命令构建您的新文档。
   可能会有一些需要您解决的错误和警告。

#. **仔细地** 通读整个页面，确保内容对 ROS 2 来说是最新的。
   检查每一个链接，确保它指向 docs.ros.org 上的正确位置。
   内部文档引用必须更新为指向等效的 ROS 2 内容。
   除非绝对必要，否则您更新后的文档不应指向 ROS Wiki。
   此过程可能需要您对文档进行相当大的改动，并且您可能需要拉取多个 wiki 文件。
   您应验证文档中的每个代码示例在 ROS 2 下都能正确运行。

#. 查找并下载旧文档中可能存在的所有图片。
   最简单的方法是在浏览器中右键单击并下载所有图片。
   或者，您可以通过在 HTML 文件中搜索 ``<img src>`` 标签来查找图片。

#. 对于下载的每个图片文件，更新图片文件链接，使其指向 ROS 文档的正确图片目录。
   如果任何图片需要更新，或者可以替换为 `Mermaid <https://mermaid.js.org/intro/>`__ 图表，请进行此更改。
   请注意，目前只有核心 ROS 2 文档支持 Mermaid.js。

#. 文档完成后，使用适当的 Sphinx 命令在您的新 rst 文档顶部添加目录。
   此代码块应替换旧 ROS Wiki 中现有的任何目录。

#. 提交您的拉取请求。
   请务必指向原始 ROS Wiki 文件以供参考。

#. 您的拉取请求被接受后，请在原始 ROS Wiki 文章页面顶部添加一条说明，指向新的文档页面。

要了解此过程实际应用的真实示例，请参阅 `the ROS 2 Docs <https://github.com/ros-perception/image_pipeline/blob/rolling/image_pipeline/doc/tutorials.rst>`__ 和原始 `ROS Wiki <https://wiki.ros.org/image_pipeline>`__ 中的 ROS 2 图像处理流水线。
完整的文档页面可在 `ROS 2 package documentation for image_pipeline <https://docs.ros.org/en/rolling/p/image_pipeline/>`__ 中找到。

使用 GitHub Codespaces 构建网站
-------------------------------
首先，您需要有一个 GitHub 账户（如果没有，可以免费创建一个）。
然后，您需要前往 `ROS 2 Documentation GitHub 仓库 <https://github.com/ros2/ros2_documentation>`__。
之后，您可以在 Codespaces 中打开该仓库，只需点击仓库页面上的 "Code" 按钮，然后从下拉菜单中选择 "Open with Codespaces" 即可。

.. image:: images/codespaces.png
   :width: 100%
   :alt: 创建 Codespaces

之后，您将被重定向到您的 Codespaces 页面，在那里您可以看到 Codespaces 创建的进度。
完成后，浏览器中将打开一个 Visual Studio Code 选项卡。
您可以通过点击顶部面板中的 "Terminal" 选项卡或按 :kbd:`Ctrl-J` 来打开终端。

在这个终端中，您可以运行任何您想要的命令，例如，您可以运行以下命令来仅为此分支构建网站：

.. code-block:: console

   $ make html

最后，要查看网站，您可以点击右下角面板中的 "Go Live" 按钮，然后它将在浏览器的新选项卡中打开网站（您需要浏览到 ``build/html`` 文件夹）。

.. image:: images/live_server.png
   :width: 100%
   :alt: 实时服务器

使用 Devcontainer 构建网站
--------------------------

`ROS 2 Documentation GitHub 仓库 <https://github.com/ros2/ros2_documentation>`__ 还支持使用 Visual Studio Code 的 ``Devcontainer`` 开发环境。
这将使您能够更轻松地构建文档，而无需更改您的操作系统。

在执行以下步骤之前，请参阅 :doc:`../../How-To-Guides/Setup-ROS-2-with-VSCode-and-Docker-Container` 以安装 VS Code 和 Docker。

克隆仓库并启动 VS Code：

.. code-block:: console

   $ git clone https://github.com/ros2/ros2_documentation
   $ cd ./ros2_documentation
   $ code .

要使用 ``Devcontainer``，您需要在 VS Code 中安装 "Remote Development" 扩展，可在扩展中搜索（CTRL+SHIFT+X）。

然后，使用 ``View->Command Palette...`` 或 ``Ctrl+Shift+P`` 打开命令面板。
搜索命令 ``Dev Containers: Reopen in Container`` 并执行它。
这将自动为您构建开发 docker 容器。

要构建文档，请使用 ``View->Terminal`` 或 ``Ctrl+Shift+``` 打开终端，然后在 VS Code 中选择 ``New Terminal``。
在终端中，您可以构建文档：

.. code-block:: console

   $ make html

.. image:: images/vscode_devcontainer.png
   :width: 100%
   :alt: VS Code Devcontainer

编写页面
--------

ROS 2 文档网站使用 ``reStructuredText`` 格式，这是 Sphinx 使用的默认纯文本标记语言。
本节是对 ``reStructuredText`` 概念、语法和最佳实践的简要介绍。
在格式化您的 ``reStructuredText`` 文件时，**请确保每行只写一句话，因为这会使审查和修改文件变得更加容易。**
另外，请注意文件中空白的使用！
ROS 2 文档 linter 不会接受带有尾随空白的拉取请求。
如果您的编辑器支持，我们建议您启用自动空白高亮和/或清理功能。

您可以参考 `reStructuredText 用户文档 <https://docutils.sourceforge.io/rst.html>`_ 以获取详细的技术规范。

目录
^^^^

有两种用于生成目录的指令：``.. toctree::`` 和 ``.. contents::``。
``.. toctree::`` 用于像 ``Tutorials.rst`` 这样的顶层页面，用于设置其子页面的顺序和可见性。
该指令会创建指向所列出子页面的左侧导航面板和页内导航链接。
它帮助读者理解各个文档部分的结构并在页面之间导航。

.. code-block:: rst

   .. toctree::
      :maxdepth: 1

``.. contents::`` 指令用于为特定页面生成目录。
它会解析页面中存在的所有标题，并构建页内嵌套目录。
它帮助读者了解内容的概览并在页面内导航。

``.. contents::`` 指令支持定义嵌套部分的最大深度。
使用 ``:depth: 2`` 将仅在目录中显示节和小节。

.. code-block:: rst

   .. contents:: Table of Contents
      :depth: 2
      :local:

标题
^^^^

文档中使用四种主要的标题类型。
请注意，符号的数量必须与标题的长度相匹配。

.. code-block:: rst

   Page Title Header
   =================

   Section Header
   --------------

   2 Subsection Header
   ^^^^^^^^^^^^^^^^^^^

   2.4 Subsubsection Header
   ~~~~~~~~~~~~~~~~~~~~~~~~

在教程和操作指南中，我们通常使用一位数字为小节编号，使用两位数字（以点分隔）为子小节编号。

列表
^^^^

星号 ``*`` 用于以项目符号列出无序项，井号 ``#.`` 用于列出编号项。
两者都支持嵌套定义，并会相应地渲染。

.. code-block:: rst

   * bullet point

     * bullet point nested
     * bullet point nested

   * bullet point

.. code-block:: rst

  #. first listed item
  #. second lited item

代码格式
^^^^^^^^

行内代码可以通过 ``backticks`` 进行格式化，以显示 ``highlighted`` 代码。

.. code-block:: rst

   In-text code can be formatted using ``backticks`` for showing ``highlighted`` code.

页面内的代码块需要使用 ``.. code-block::`` `指令 <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block>`_ 来捕获。
``.. code-block::`` 支持对 ``C++`` 、``YAML`` 、``console`` 、``bash`` 等语法的代码高亮。
指令内部的代码需要缩进。

.. code-block:: rst

   .. code-block:: C++

      int main(int argc, char** argv)
      {
         rclcpp::init(argc, argv);
         rclcpp::spin(std::make_shared<ParametersClass>());
         rclcpp::shutdown();
         return 0;
      }

代码块：``bash`` 与 ``console``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``bash`` 和 ``console`` 很相似，但它们服务于两个不同的用途。
选择正确的一个很重要，这样可以确保内容格式正确，并且复制按钮能复制正确的内容。
下面是对两者的说明；您可以跳到本节末尾查看用例列表和相应的示例。

``bash`` 用于脚本，例如脚本文件中的 bash 命令。
示例结果：

.. code-block:: bash

   export ROS_DOMAIN_ID=42
   ros2 run turtlesim turtlesim_node

``console`` 用于需要在终端中运行的命令，可选地包含它们的输出。
这样可以清楚地表明给定的命令需要在终端中运行。
它还允许使用 ``$`` 或 ``#`` 等提示符将命令行与输出行分开。
命令行会格式化为 bash 命令，而输出行则格式化为普通文本。
提示符不可选中，点击右上角的复制按钮会 *仅* 复制命令，而不会复制输出或提示符。
这意味着，如果使用 ``console`` 代码块时没有任何 ``$``，复制按钮将不会复制任何行。
示例结果：

.. code-block:: console

   $ export ROS_DOMAIN_ID=42
   $ ros2 run turtlesim turtlesim_node --ros-args --remap "__node:=my_turtle"
   [INFO] [1742150439.022947971] [my_turtle]: Starting turtlesim with node name /my_turtle
   [INFO] [1742150439.026043867] [my_turtle]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]

将上面的内容与 ``bash`` ``code-block`` 进行比较：

.. code-block:: bash

   $ export ROS_DOMAIN_ID=42
   $ ros2 run turtlesim turtlesim_node --ros-args --remap "__node:=my_turtle"
   [INFO] [1742150439.022947971] [my_turtle]: Starting turtlesim with node name /my_turtle
   [INFO] [1742150439.026043867] [my_turtle]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]

为了简化代码块，如果代码块不包含任何输出行，那么对于需要在终端中运行的命令，``bash`` 仍然可以不使用 ``$`` 来使用。
为了帮助您在 ``bash`` 和 ``console`` 之间进行选择，请参阅以下用例列表和相应的示例：

#. 需要复制到脚本文件中的命令

   * 使用不带 ``$`` 的 ``.. code-block:: bash`` ：

      .. code-block:: bash

         export ROS_DOMAIN_ID=42
         ros2 run turtlesim turtlesim_node

#. 需要在终端中运行的命令：

   * 强烈建议在所有命令行上使用带有 ``$`` 的 ``.. code-block:: console``，以保持一致性并提高清晰度。
     如果有需要显示的输出，请将其包含在同一个代码块中：

      .. code-block:: console

         $ source /opt/ros/{DISTRO}/setup.bash
         $ ros2 run turtlesim turtlesim_node
         [INFO] [1743878028.269334696] [turtlesim]: Starting turtlesim with node name /turtlesim
         [INFO] [1743878028.275096618] [turtlesim]: Spawning turtle [turtle1] at x=[5.544445], y=[5.544445], theta=[0.000000]

      .. note::

         如果某些输出行以 ``#`` 开头，那么将命令与其输出分开至关重要，因为 ``#`` 符号用于表示命令。
         因此，请将输出放在单独的 ``.. code-block:: text`` 中。

图片
^^^^

可以使用 ``.. image::`` 指令插入图片。

.. code-block:: rst

   .. image:: images/turtlesim_follow1.png

在这种情况下，图片文件（``turtlesim_follow1.png`` ）位于使用该图片的 ``.rst`` 文件相对的 ``images/`` 目录中。

但是，所有图片文件最终都会位于相对于文档根目录的 ``_images/`` 目录中。
因此，当使用 ``:target:`` 为图片文件添加超链接时，请使用先向上到根目录、再向下到 ``_images/`` 目录的相对链接。

.. code-block:: rst

   .. image:: images/turtlesim_follow1.png
      :target: ../../_images/turtlesim_follow1.png

图表、图形和示意图
^^^^^^^^^^^^^^^^^^

ROS 2 文档现在支持使用 `Mermaid 图表 <https://mermaid.js.org/intro/>`__ 编写的图表、图形和示意图。
我们更希望在图表、图形和示意图中使用 Mermaid，而不是静态图片文件，因为这使我们能够随着项目的发展以编程方式更新和编辑这些资源。
关于 Mermaid 图形语言语法的完整文档，可在其官方网站上找到：`Mermaid 图形语言语法参考 <https://mermaid.js.org/intro/syntax-reference.html>`__ 。

参考与链接
^^^^^^^^^^

外部链接
~~~~~~~~

创建指向外部网页链接的语法如下所示。

.. code-block:: rst

   `ROS Docs <https://docs.ros.org>`_

上面的链接将显示为 `ROS Docs <https://docs.ros.org>`_ 。
注意最后一个单引号后面的下划线。

内部链接
~~~~~~~~

``:doc:`` 指令用于创建指向其他页面的文内链接。

.. code-block:: rst

   :doc:`Quality of Service <../Tutorials/Quality-of-Service>`

请注意使用的是文件的相对路径。

``ref`` 指令用于创建指向页面特定部分的链接。
这些链接可以是当前页面或不同页面中的标题、图片或代码段。

需要在所需对象之前紧邻定义显式目标。
在下面的示例中，目标被定义为 ``_talker-listener``，位于标题 ``Try some examples`` 的前一行。

.. code-block:: rst

   .. _talker-listener:

   Try some examples
   -----------------

现在就可以创建从文档中任何页面到该标题的链接了。

.. code-block:: rst

   :ref:`talker-listener demo <talker-listener>`

此链接将通过 HTML 锚点链接 ``#talker-listener`` 将读者导航到目标页面。

宏
~~

可以使用宏来简化针对多个发行版编写文档的工作。

通过将宏名称包含在花括号中来使用宏。
例如，在为 ``rolling`` 分支上的 Rolling 生成文档时：

.. list-table::
   :header-rows: 1

   * - 宏
     - 示例
     - 结果（针对 {DISTRO_TITLE}）
   * - \{DISTRO\}
     - ros-\{DISTRO\}-pkg
     - ros-{DISTRO}-pkg
   * - \{DISTRO_TITLE\}
     - ROS 2 \{DISTRO_TITLE\}
     - ROS 2 {DISTRO_TITLE}
   * - \{DISTRO_TITLE_FULL\}
     - ROS 2 \{DISTRO_TITLE_FULL\}
     - ROS 2 {DISTRO_TITLE_FULL}
   * - \{REPOS_FILE_BRANCH\}
     - git checkout \{REPOS_FILE_BRANCH\}
     - git checkout {REPOS_FILE_BRANCH}
   * - \{interface_link(std_msgs/msg/String)\}
     - See: \{interface_link(std_msgs/msg/String)\}.
     - See: {interface_link(std_msgs/msg/String)}.
   * - \{interface(std_msgs/msg/String)\}
     - Publish a \{interface(std_msgs/msg/String)\}.
     - Publish a {interface(std_msgs/msg/String)}.
   * - \{package_link(rclcpp)\}
     - See: \{package_link(rclcpp)\}.
     - See: {package_link(rclcpp)}.
   * - \{package(rclcpp)\}
     - Use \{package(rclcpp)\}.
     - Use {package(rclcpp)}.

同一个文件可以在多个分支（即多个发行版）上使用，而生成的内容将是特定于发行版的。
