IDE 与调试 [社区贡献]
=====================

ROS 2 并不围绕特定的开发环境构建，其主要重点是构建/从命令行运行。
尽管如此，集成开发环境（IDE）仍然可以用于开发、运行和/或调试 ROS 2 节点。

下面列出了一些 IDE 以及如何将它们与 ROS 2 结合使用的说明。


.. contents:: Contents
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
因此，当从 IDE 内将调试器附加到 ``ros2 run`` 命令时，正在运行的代码（来自 ``build``/``install``）与 IDE 项目中打开的文件并不相同。

有两种方法可以处理这个问题：

* 从 ``build``/``install`` 目录打开源文件，并在那里放置断点。
* 使用 colcon 的 `--symlink-install <https://colcon.readthedocs.io/en/released/reference/verb/build.html#command-line-arguments>`__ 标志构建工作空间，这会将源文件符号链接到 ``build``/``install`` 目录，而不是复制。


Visual Studio Code
------------------

`VSCode <https://code.visualstudio.com/>`_ 是一个多功能且免费的开发环境。

VSCode 与 ROS 2 配合使用相对容易。
只需在命令行中激活你的环境，并从同一个终端启动 VSCode 应用程序，然后正常使用即可。
所以：

#. 像往常一样创建你的 ROS 工作空间。
#. 在终端中，source ROS 2 和你的 install（如果它已经构建过）。
#. 从同一个命令行启动 VSCode。
   终端将被阻塞，直到应用程序再次关闭。

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


VSCode 以及 VSCode 内创建的任何终端都会正确继承父环境，并且应该可以使用 ROS 和已安装的包。

.. note::

   在添加包或进行重大更改后，你可能需要再次 source 你的 install。
   最简单的方法是关闭 VSCode 并按上述方式重新启动它。


Python
^^^^^^

在你的工作空间中，验证使用的是正确的解释器。
通过 source，基本的 ``python`` 命令应该是正确的，但 VSCode 倾向于使用 Python 的绝对路径。
在右下角点击 "Selected Python Interpreter" 进行更改。

如果你的 ROS 2 Python 版本来自虚拟环境，VSCode 会在每次运行命令时尝试 source 它。
但我们已经从一个已 source 的环境中启动了 VSCode，所以这个额外步骤是不必要的。
你可以通过找到 "Settings" > "Extensions" > "Python" > "Activate Environment" 并禁用该勾选，来为当前工作空间禁用此行为。

现在只需运行一个文件，或在 ``launch.json`` 中创建一个配置。
调试节点最简单的方法是创建一个类似 ``python ...`` 命令的配置，而不是 ``ros2 run/launch ...``。
``launch.json`` 的一个示例可以是：

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


相反，你也可以在 "Attach using Process Id" 下创建一个附加到正在运行进程的配置。


有关如何结合 Docker 使用 VSCode 的完整说明，请参见 :doc:`使用 VSCode 和 Docker 设置 ROS 2<Setup-ROS-2-with-VSCode-and-Docker-Container>`。


PyCharm
-------

`PyCharm <https://www.jetbrains.com/pycharm/>`_ 是一个专门用于 Python 的 IDE。

当然，它只能有意义地用于用 Python 编写的节点。

使用 PyCharm，你可以附加到现有进程（可能是你通过 ``ros2 run ...`` 或 ``ros2 launch ...`` 启动的），或者直接从 Python 运行节点（相当于 ``python [file.py]``）。


集成以进行代码检查
^^^^^^^^^^^^^^^^^^

你可以设置你的 PyCharm 项目，使其完全感知 ROS 2 代码，从而支持代码补全和建议。


Linux
"""""

打开一个终端，source ROS 并启动 PyCharm：

.. code-block:: console

   $ source /opt/ros/humble/setup.bash
   $ cd path/to/dev_ws
   $ /opt/pycharm/bin/pycharm.sh

选择正确的解释器后，一切应该都能正常工作。

.. note::

    这是未经测试的。


Windows
"""""""

在 Windows 上，先 source ROS 然后再从命令行启动 PyCharm 似乎没有效果。
相反，需要调整一些设置。

#. 像往常一样创建你的 ROS 工作空间。
#. 正常启动 PyCharm。
#. 打开一个项目。
   这应该是你正在开发的 ROS 节点的根目录，例如 ``C:\dev_ws\src\my_node``。
#. 点击 "Add new interpreter" > "Add local interpreter..."。
   选择一个系统解释器（如果你正在使用虚拟环境，则选择虚拟环境），并选择你的 ROS Python 版本的可执行文件（通常是 ``C:\Python38\python.exe``）。

      * 如果你现在打开某个代码文件，你会看到关于缺失导入的警告。
        尝试运行该文件将确认这些问题。

#. 在 "Python Interpreters" 窗口下，找到并选择你的 ROS 解释器。
   将名称编辑为易于识别的名称。
   更重要的是，现在点击 "Show Interpreter Paths" 按钮。
#. 在新窗口中，你会看到已经与该解释器关联的路径。
   点击 "+" 按钮，并添加两个路径（根据你的 ROS 安装）：

      * ``C:\dev\ros2_humble\bin``
      * ``C:\dev\ros2_humble\Lib\site-packages``

PyCharm 将重新索引，完成后它应该能正确解释你的项目，识别出 ROS 2 系统包。
你可以按预期浏览代码、获得补全并阅读文档摘要。


如果有与你的包一起构建的依赖项，它们可能尚未被识别，并导致无效的 IDE 警告和运行时错误。

通过以下方式解决：

* 确保运行/调试配置中的 ``PATH`` 覆盖同时包含 ROS 2 安装和你的工作空间，例如：

  .. code-block:: console

     $ C:\dev\ros2_humble\local_setup.ps1
     $ C:\dev_ws\install\local_setup.ps1
     $ echo $ENV:Path

* 将 ``install/`` 目录中的相关文件夹添加到你的项目源代码中。

  转到 "Settings..."，在 "Project: " > "Project Structure" 下点击 "Add content root"。
  添加 ``install/Lib/*`` 下所有相关的 ``site-packages`` 文件夹。

  最后，确保你的运行/调试配置已启用 "include content roots in PYTHONPATH" 选项。

.. tip::

   在 colcon build 中使用 `--merge-install <https://colcon.readthedocs.io/en/released/user/isolated-vs-merged-workspaces.html>`__ 选项将限制依赖目录的数量，使 PyCharm 更易于配置。


附加到进程
^^^^^^^^^^

即使不对 PyCharm 进行任何配置，你也可以始终附加到一个正在运行的 Python 节点。
打开你的项目源代码，并像往常一样运行你的节点：

.. code-block:: console

   $ ros2 run my_node main

然后在 PyCharm 中选择 "Run" > "Attach to Process..."。
这可能需要一点时间，但应该会弹出一个窗口，列出当前正在运行的 Python 实例，包括你的节点。
可能有多个 Python 进程，因此找到正确的进程可能需要一些试错。

选择一个实例后，就可以使用常用的调试工具了。
你可以暂停它，或者在代码中创建断点并单步执行。

.. note::

   你项目中的代码可能不是正在执行的文件，请参见 :ref:`此处<InstalledPythonCode>`。


运行/调试
^^^^^^^^^

先按照集成步骤操作。

从 PyCharm 运行你的 Python 文件很可能会导致导入错误。
这是因为 PyCharm 扩展了 ``PYTHONPATH`` 环境变量，但保持 ``PATH`` 不变。
``ros/bin`` 中必要的库文件无法被找到。

编辑你的文件的运行/调试配置，并在 "Environment Variables:" 下添加一个新变量。
目前不支持扩展现有的 ``PATH``，所以我们需要覆盖它。
在一个已 source ROS 的终端中，使用 ``echo $Env:PATH`` 导出 ``PATH`` 的内容。
复制结果。

回到 PyCharm，将其粘贴为 ``PATH``，应用更改并运行或调试你的节点。
现在它应该像任何 Python 项目一样工作，可以轻松添加断点和其他调试方法。

.. note::

   在 Windows 上，"Environment Variables:" 下的 ``PATH`` 变量的大小写似乎必须是 "path"（全小写）才能正常工作。
