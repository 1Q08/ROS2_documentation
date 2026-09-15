IDE 与调试 [社区贡献]
=====================

ROS 2 并非围绕某个特定的开发环境而构建，其主要关注点是在命令行中构建 / 运行。
尽管如此，集成开发环境（IDE）仍可用于开发、运行和/或调试 ROS 2 节点。

下面列出了一些 IDE 以及如何在 ROS 2 中使用它们的说明。


.. contents:: 目录
    :depth: 2
    :local:


通用
----


.. _InstalledPythonCode:

已安装的 Python 代码
^^^^^^^^^^^^^^^^^^^^

默认情况下，使用以下命令构建工作空间时：

.. code-block:: console

   $ colcon build

Python 代码会被复制到 ``build``/``install`` 目录中。
因此，当在 IDE 中把调试器附加到 ``ros2 run`` 命令时，正在运行的代码（来自 ``build``/``install``）与在 IDE 项目中打开的文件并不相同。

有两种处理方式：

* 从 ``build``/``install`` 目录打开源文件，并在那里放置断点。
* 在构建工作空间时为 colcon 加上 `--symlink-install <https://colcon.readthedocs.io/en/released/reference/verb/build.html#command-line-arguments>`__ 标志，这样会把源文件符号链接到 ``build``/``install`` 目录。


Visual Studio Code
------------------

`VSCode <https://code.visualstudio.com/>`_ 是一个多用途的免费开发环境。

VSCode 与 ROS 2 配合使用相对容易。
只需在命令行中激活你的环境，并从同一终端启动 VSCode 应用程序，然后照常使用即可。
即：

#. 按通常方式创建你的 ROS 工作空间。
#. 在终端中，同时 source ROS 2 和你的 install（如果已经构建过）。
#. 从同一命令行启动 VSCode。
   终端会被阻塞，直到该应用程序再次关闭。

.. tabs::

   .. group-tab:: Linux

      .. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash
        $ cd ~/dev_ws
        $ source ./install/setup.bash
        $ /usr/bin/code ./src/my_node/

   .. group-tab:: macOS

      .. code-block:: console

        $ . ~/ros2_install/ros2-osx/setup.bash
        $ cd ~/dev_ws
        $ . ./install/setup.bash
        $ /Applications/Visual Studio Code.app/Contents/Resources/app/bin/code ./src/my_node/

   .. group-tab:: Windows

      在 Windows 命令行界面中：

      .. code-block:: console

        $ call C:\dev\ros2\local_setup.bat
        $ cd C:\dev_ws
        $ call .\install\local_setup.bat
        $ "C:\Program Files\Microsoft VS Code\Code.exe" .\src\my_node\

      或者在 powershell 中：

      .. code-block:: console

        $ C:\dev\ros2\local_setup.ps1
        $ cd C:\dev_ws
        $ .\install\local_setup.ps1
        $ & "C:\Program Files\Microsoft VS Code\Code.exe" .\src\my_node\


VSCode 以及在 VSCode 内创建的任何终端都会正确继承父环境，并且应当能够使用 ROS 和已安装的软件包。

.. note::

   在添加软件包或进行重大更改后，你可能需要重新 source 你的 install。
   最简单的做法是关闭 VSCode，然后按上述方式重新启动它。


Python
^^^^^^

在你的工作空间中，确认使用的是正确的解释器。
source 之后，基本的 ``python`` 命令应当是正确的，但 VSCode 倾向于使用 Python 的绝对路径。
点击右下角的“Selected Python Interpreter”即可更改。

如果你的 ROS 2 Python 版本来自虚拟环境，VSCode 会在每次运行命令时尝试 source 它。
但我们已经从已 source 的环境中启动了 VSCode，因此这一步额外操作并不必要。
你可以为当前工作空间禁用该功能，方法是找到“Settings” > “Extensions” > “Python” > “Activate Environment”并取消勾选。

现在只需运行某个文件，或在 ``launch.json`` 中创建配置即可。
调试节点最简单的方式是创建类似 ``python ...`` 命令的配置，而不是 ``ros2 run/launch ...``。
``launch.json`` 的一个示例如下：

.. code-block::

   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: File",
               "type": "python",
               "request": "launch",
               "program": "my_node.py"
           },
       ]
   }


此外，你也可以在“Attach using Process Id”下创建用于附加到正在运行的进程的配置。


关于如何结合 Docker 使用 VSCode 的完整说明，请参见 :doc:`使用 VSCode 和 Docker 搭建 ROS 2<Setup-ROS-2-with-VSCode-and-Docker-Container>`。


PyCharm
-------

`PyCharm <https://www.jetbrains.com/pycharm/>`_ 是一个专门面向 Python 的 IDE。

当然，它只能有意义地用于用 Python 编写的节点。

使用 PyCharm，你可以附加到已有的进程（可能由你通过 ``ros2 run ...`` 或 ``ros2 launch ...`` 启动），也可以直接从 Python 运行节点（相当于 ``python [file.py]``）。


集成以进行代码检查
^^^^^^^^^^^^^^^^^^

你可以设置 PyCharm 项目，使其完全理解 ROS 2 代码，从而提供代码补全和提示。


Linux
"""""

打开终端，source ROS 并启动 PyCharm：

.. code-block:: console

   $ source /opt/ros/humble/setup.bash
   $ cd path/to/dev_ws
   $ /opt/pycharm/bin/pycharm.sh

选择正确的解释器后，一切应当都能正常工作。

.. note::

    这一点尚未验证。


Windows
"""""""

在 Windows 上，先 source ROS 再从命令行启动 PyCharm 似乎没有效果。
相反，需要调整一些设置。

#. 按通常方式创建你的 ROS 工作空间。
#. 正常启动 PyCharm。
#. 打开一个项目。
   这应当是你正在开发的 ROS 节点的根目录，例如 ``C:\dev_ws\src\my_node``。
#. 点击“Add new interpreter” > “Add local interpreter...”。
   选择一个系统解释器（或你正在使用的虚拟环境），然后选择你的 ROS Python 版本的可执行文件（通常是 ``C:\Python38\python.exe``）。

      * 如果你此时打开某个代码文件，会看到关于缺少导入的警告。
        尝试运行该文件会证实这些问题。

#. 在“Python Interpreters”窗口中，找到并选择你的 ROS 解释器。
   将名称编辑为易于识别的名称。
   更重要的是，现在点击“Show Interpreter Paths”按钮。
#. 在新窗口中，你会看到已经与该解释器关联的路径。
   点击“+”按钮并再添加两个路径（根据你的 ROS 安装情况）：

      * ``C:\dev\ros2_humble\bin``
      * ``C:\dev\ros2_humble\Lib\site-packages``

PyCharm 会重新建立索引，完成后应能正确解析你的项目，识别 ROS 2 系统软件包。
你可以浏览代码、获得补全，并按预期阅读文档说明。


如果有与你的软件包一起构建的依赖项，它们可能尚未被识别，从而导致无效的 IDE 警告和运行时错误。

可通过以下方式解决：

* 确保运行/调试配置中的 ``PATH`` 覆盖同时包含 ROS 2 的 install 和你的工作空间，例如：

  .. code-block:: console

     $ C:\dev\ros2_humble\local_setup.ps1
     $ C:\dev_ws\install\local_setup.ps1
     $ echo $ENV:Path

* 将 ``install/`` 目录中的相关文件夹添加到你的项目源码中。

  转到“Settings...”，在“Project: ” > “Project Structure”下点击“Add content root”。
  添加 ``install/Lib/*`` 下所有相关的 ``site-packages`` 文件夹。

  最后，确保你的运行/调试配置启用了“include content roots in PYTHONPATH”选项。

.. tip::

   在 colcon 构建中使用 `--merge-install <https://colcon.readthedocs.io/en/released/user/isolated-vs-merged-workspaces.html>`__ 选项可以减少依赖目录的数量，从而更容易配置 PyCharm。


附加到进程
^^^^^^^^^^

即使没有对 PyCharm 做任何配置，你也始终可以直接附加到正在运行的 Python 节点。
打开你的项目源码并像往常一样运行你的节点：

.. code-block:: console

   $ ros2 run my_node main

然后在 PyCharm 中选择“Run” > “Attach to Process...”。
可能需要一秒，但会弹出一个小窗口，列出当前正在运行的 Python 实例，包括你的节点。
可能有多个 Python 进程，因此可能需要反复尝试才能找到正确的那个。

选择某个实例后，通常的调试工具即可使用。
你可以暂停它，或在代码中创建断点并单步执行。

.. note::

   你项目中的代码可能并不是正在执行的文件，参见 :ref:`此处<InstalledPythonCode>`。


运行/调试
^^^^^^^^^

首先按集成步骤操作。

从 PyCharm 运行你的 Python 文件很可能会出现导入错误。
这是因为 PyCharm 会扩展 ``PYTHONPATH`` 环境变量，但不会改动 ``PATH``。
找不到 ``ros/bin`` 中必需的库文件。

编辑该文件的运行/调试配置，并在“Environment Variables:”下添加一个新变量。
目前不支持扩展现有的 ``PATH``，因此我们需要覆盖它。
在已 source ROS 的终端中，用以下命令输出 ``PATH`` 的内容：``echo $Env:PATH``。
复制结果。

回到 PyCharm，将其粘贴为 ``PATH``，应用更改，然后运行或调试你的节点。
现在它应当像任何 Python 项目一样工作，可以轻松添加断点和其他调试方式。

.. note::

   在 Windows 上，“Environment Variables:”下的 ``PATH`` 变量似乎必须写作“path”（全小写）才能生效。
