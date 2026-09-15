.. redirect-from::

   Installation/Windows-Development-Setup

.. _windows-latest:

Windows（源码）
===============

.. contents:: 目录
   :depth: 2
   :local:

本指南说明如何在 Windows 上搭建 ROS 2 开发环境。

系统要求
--------

仅支持 Windows 10。

语言支持
^^^^^^^^

确保你的语言环境支持 ``UTF-8``。
例如，在中文 Windows 10 安装环境中，你可能需要安装一个 `英文语言包 <https://support.microsoft.com/en-us/windows/language-packs-for-windows-a5094319-a92d-18de-5b53-1cfc697cfca8>`_。

.. include:: ../_Windows-Install-Prerequisites.rst

额外前置条件
------------

从源码构建时，你需要安装一些额外前置条件。

从 Chocolatey 安装额外前置条件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ choco install -y cppcheck curl git winflexbison3

你需要把 Git cmd 文件夹 ``C:\Program Files\Git\cmd`` 加到 PATH 中（可以通过单击 Windows 图标，输入“Environment Variables”，然后单击“Edit the system environment variables”完成。
在弹出的对话框中，单击“Environment Variables”，然后在底部窗格中单击“Path”，再单击“Edit”并加入该路径）。


安装 Python 前置条件
^^^^^^^^^^^^^^^^^^^^

安装额外 Python 依赖：

.. code-block:: bash

   $ pip install -U colcon-common-extensions coverage flake8 flake8-blind-except flake8-builtins flake8-class-newline flake8-comprehensions flake8-deprecated flake8-docstrings flake8-import-order flake8-quotes mock mypy==0.931 pep8 pydocstyle pytest pytest-mock vcstool

安装杂项前置条件
^^^^^^^^^^^^^^^^

接下来安装 xmllint：

* 从 https://www.zlatkovic.com/projects/libxml/ 下载 ``libxml2`` （及其依赖 ``iconv`` 和 ``zlib``）的 `64 位二进制归档包 <https://www.zlatkovic.com/pub/libxml/64bit/>`__
* 将所有归档包解压到例如 ``C:\xmllint``
* 将 ``C:\xmllint\bin`` 添加到 ``PATH``。

获取 ROS 2 源码
---------------

现在我们已经有了开发工具，可以获取 ROS 2 源码。

先创建一个开发目录，例如 ``C:\{DISTRO}``：

.. note::

   由于 Windows 默认的路径长度限制较短（260 个字符），所选路径必须尽可能短，这一点非常重要。
   若要允许更长的路径，请参阅 `maximum-file-path-limitation <https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry>`__。

.. code-block:: bash

   $ md \{DISTRO}\src
   $ cd \{DISTRO}

获取定义了要克隆的仓库的 ``ros2.repos`` 文件：

.. code-block:: console

   $ vcs import --input https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos src

安装额外 DDS 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^

Fast DDS 与 ROS 2 源码捆绑在一起，除非你在 ``src\eProsima`` 文件夹中放置一个 ``COLCON_IGNORE`` 文件，否则它总会被构建。

如果你想使用除默认外的其他 DDS 或 RTPS 厂商，可以在此处找到说明：:doc:`这里 <../RMW-Implementations>`。

构建 ROS 2 代码
---------------

.. _windows-dev-build-ros2:

要构建 ROS 2，你需要以管理员身份运行 Visual Studio 命令提示符（“x64 Native Tools Command Prompt for VS 2019”）。

要构建 ``\{DISTRO}`` 文件夹树：

.. code-block:: console

   $ colcon build --merge-install

.. note::

   这里我们使用 ``--merge-install``，以避免构建结束时 ``PATH`` 变量过长。
   如果你把这些说明改用于构建更小的工作空间，那么你也许可以使用默认行为，即隔离安装（每个软件包安装到不同的文件夹）。

.. note::

   如果你在做调试构建，请使用 ``python_d path\to\colcon_executable`` ``colcon``。
   关于在 Windows 上以调试构建方式运行 Python 代码的更多信息，请参阅 `调试模式的额外内容`_。

.. note::

   由于会有大量软件包被拉入工作空间，源码安装可能会花费很长时间。

配置环境
--------

启动一个命令行 shell，并加载 ROS 2 安装文件以配置工作空间：

.. code-block:: console

   $ call C:\{DISTRO}\install\local_setup.bat

这将自动为所有已构建支持的 DDS 厂商配置好环境。

如果没有其他问题，上一条命令恰好输出一次 ``The system cannot find the path specified.`` 是正常的。

测试与运行
----------

请注意，第一次运行任何可执行文件时，你都需要在 Windows 防火墙弹窗中允许其通过网络访问。

你可以使用以下命令运行测试：

.. code-block:: console

   $ colcon test --merge-install

.. note::

   仅当构建步骤也使用了 ``--merge-install`` 时，才应使用它。

之后，你可以使用以下命令获取测试结果摘要：

.. code-block:: console

   $ colcon test-result

要运行示例，先打开一个干净的新 ``cmd.exe``，并通过加载 ``local_setup.bat`` 文件来配置工作空间。
然后运行 C++ 的 ``talker``\ :

.. code-block:: console

   $ call install\local_setup.bat
   $ ros2 run demo_nodes_cpp talker

在另一个 shell 中，你可以做同样的操作，但改为运行 Python 的 ``listener``\ :

.. code-block:: console

   $ call install\local_setup.bat
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 输出 ``Publishing`` 消息，而 ``listener`` 输出 ``I heard`` 这些消息。
这验证了 C++ 和 Python API 都能正常工作。
太棒了！


.. note::

   不建议在你已经加载了 ``local_setup.bat`` 的同一个 cmd 提示符中进行构建。

安装后的后续步骤
----------------
继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并了解 ROS 2 的核心概念。

其他 RMW 实现（可选）
---------------------
ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
请参阅关于如何使用多个 RMW 的 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。


调试模式的额外内容
------------------

如果你希望能够在调试模式下运行所有测试，还需要安装一些额外的东西：


* 为了能够解压 Python 源码 tar 包，你可以使用 PeaZip：

.. code-block:: bash

   choco install -y peazip


* 你还需要 SVN，因为某些 Python 源码构建依赖是通过 SVN 检出的：

.. code-block:: bash

   choco install -y svn hg


* 安装上述软件后，你需要退出并重新启动命令提示符。
* 从 ``tgz`` 获取并解压 Python 3.8.3 源码：

  * `Python-3.8.3 <https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz>`__
  * 为使这些说明简洁，请将其解压到 ``C:\dev\Python-3.8.3``

* 现在，在 Visual Studio 命令提示符中以调试模式构建 Python 源码：

.. code-block:: bash

   cd C:\dev\Python-3.8.3\PCbuild
   get_externals.bat
   build.bat -p x64 -d


* 最后，将构建产物复制到 Python38 安装目录中，紧挨着 Release 模式的 Python 可执行文件和 DLL：

.. code-block:: bash

   cd C:\dev\Python-3.8.3\PCbuild\amd64
   copy python_d.exe C:\Python38 /Y
   copy python38_d.dll C:\Python38 /Y
   copy python3_d.dll C:\Python38 /Y
   copy python38_d.lib C:\Python38\libs /Y
   copy python3_d.lib C:\Python38\libs /Y
   copy sqlite3_d.dll C:\Python38\DLLs /Y
   for %I in (*_d.pyd) do copy %I C:\Python38\DLLs /Y


* 现在，从一个全新的命令提示符中，确认 ``python_d`` 可以正常工作：

.. code-block:: bash

   python_d -c "import _ctypes ; import coverage"

* 一旦你验证了 ``python_d`` 的运行，就需要用启用了调试的库重新安装几个依赖：

.. code-block:: bash

   python_d -m pip install --force-reinstall https://github.com/ros2/ros2/releases/download/numpy-archives/numpy-1.18.4-cp38-cp38d-win_amd64.whl
   python_d -m pip install --force-reinstall https://github.com/ros2/ros2/releases/download/lxml-archives/lxml-4.5.1-cp38-cp38d-win_amd64.whl

* 验证这些依赖的安装：

.. code-block:: bash

   python_d -c "from lxml import etree ; import numpy"

* 当你希望重新构建 release 二进制文件时，需要卸载调试变体并使用 release 变体：

.. code-block:: bash

   python -m pip uninstall numpy lxml
   python -m pip install numpy lxml

* 要创建可执行的 Python 脚本（``.exe``），应使用 python_d 来调用 colcon

.. code-block:: bash

   python_d path\to\colcon_executable build

* 太棒了，你完成了！

保持最新
--------

请参阅 :doc:`../Maintaining-a-Source-Checkout`，以定期刷新你的源码安装。

故障排查
--------

故障排查技巧可以在 :ref:`这里 <windows-troubleshooting>` 找到。

卸载
----

1. 如果你按上述方式使用 colcon 安装了工作空间，所谓“卸载”可能只需打开一个新终端，并且不加载该工作空间的 ``setup`` 文件。
   这样，你的环境就会表现得如同系统中根本没安装过 {DISTRO_TITLE} 一样。

2. 如果你还想释放空间，可以用以下命令删除整个工作空间目录：

   .. code-block:: console

      $ rmdir /s /q \ros2_{DISTRO}
