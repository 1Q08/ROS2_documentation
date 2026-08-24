.. redirect-from::

   Installation/Windows-Development-Setup

Windows（源代码）
=================

.. contents:: 目录
   :depth: 2
   :local:

本页介绍如何在 Windows 上搭建 ROS 2 开发环境。

系统要求
--------

仅支持 Windows 10。

.. warning::

   我们建议使用干净的 Windows 环境进行构建，例如全新安装的系统、Docker 容器或虚拟机。
   这是因为现有软件（例如其他 Python 版本）可能会污染构建配置并导致编译错误。

语言支持
^^^^^^^^

请确保你的语言环境支持 ``UTF-8``。
例如，对于中文版 Windows 10 安装，你可能需要安装 `英语语言包 <https://support.microsoft.com/en-us/windows/language-packs-for-windows-a5094319-a92d-18de-5b53-1cfc697cfca8>`_。

创建 ROS 2 安装位置
-------------------

该位置将同时包含已安装的二进制软件包以及 ROS 2 安装本身。

启动一个 powershell 会话（通常是点击开始菜单，然后输入 ``powershell``）。

然后创建一个目录来存储安装内容。
由于 Windows 的路径长度限制，该路径应尽可能短。
在本文后续说明中，我们将使用 ``C:\dev``。

.. code-block:: console

   $ md C:\dev

增大 Windows 最大路径长度
-------------------------

默认情况下，Windows 的最大路径长度（MAX_PATH）被限制为 260 个字符。
ROS 2 构建将使用明显更长的路径，因此我们需要增大该限制。
使用你上面启动的 powershell 会话，运行以下命令：

.. code-block:: console

   $ New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

你可以在 `Microsoft 的文档 <https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry>`__ 中了解更多关于此限制的信息。


安装先决条件
------------

安装 MSVC
^^^^^^^^^

为了编译 ROS 2 代码，必须安装 MSVC 编译器。
目前建议使用 MSVC 2019。

继续使用之前的 powershell 会话，运行以下命令进行下载：

.. code-block:: console

   $ irm https://aka.ms/vs/16/release/vs_buildtools.exe -OutFile vs_buildtools_2019.exe

现在安装 MSVC 2019：

.. code-block:: console

   $ .\vs_buildtools_2019.exe --quiet --wait --norestart --add Microsoft.Component.MSBuild --add Microsoft.Net.Component.4.6.1.TargetingPack --add Microsoft.Net.Component.4.8.SDK --add Microsoft.VisualStudio.Component.CoreBuildTools --add Microsoft.VisualStudio.Component.Roslyn.Compiler --add Microsoft.VisualStudio.Component.TextTemplating --add Microsoft.VisualStudio.Component.VC.CLI.Support --add Microsoft.VisualStudio.Component.VC.CoreBuildTools --add Microsoft.VisualStudio.Component.VC.CoreIde --add Microsoft.VisualStudio.Component.VC.Redist.14.Latest --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows10SDK --add Microsoft.VisualStudio.Component.Windows10SDK.19041 --add Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Core --add Microsoft.VisualStudio.Workload.MSBuildTools --add Microsoft.VisualStudio.Workload.VCTools

.. note::

   MSVC 的安装可能需要很长时间，并且在安装过程中没有任何反馈。

安装 pixi
^^^^^^^^^

ROS 2 使用 `conda-forge <https://conda-forge.org/>`__ 作为软件包的后端，并使用 `pixi <https://pixi.sh/latest/>`__ 作为前端。

继续使用之前的 powershell 会话，按照 https://pixi.sh/latest/ 上的说明来安装 ``pixi``。
安装完 ``pixi`` 后，关闭 powershell 会话并重新启动它，这将确保 ``pixi`` 位于 PATH 中。

安装依赖项
^^^^^^^^^^

在现有的 powershell 会话中下载 pixi 配置文件：

.. code-block:: console

   $ cd C:\dev
   $ irm https://raw.githubusercontent.com/ros2/ros2/refs/heads/{REPOS_FILE_BRANCH}/pixi.toml -OutFile pixi.toml

安装依赖项：

.. code-block:: console

   $ pixi install

现在你应该关闭 powershell 会话，因为本文其余说明将使用 Windows 命令提示符。

构建 ROS 2
----------

启动一个新的 Windows 命令提示符，它将用于构建。

source MSVC 编译器
^^^^^^^^^^^^^^^^^^

在你将用于编译 ROS 2 的命令提示符中，这是必需的；但在运行 ROS 2 时，它 *不* 是必需的：

.. code-block:: console

  $ call "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Auxiliary\Build\vcvarsall.bat" x86_amd64

source pixi 环境
^^^^^^^^^^^^^^^^

在你打开的每个命令提示符中，都必须执行此操作以设置依赖项的路径：

.. code-block:: console

   $ cd C:\dev
   $ pixi shell

获取 ROS 2 代码
^^^^^^^^^^^^^^^

现在我们已经有了开发工具，可以获取 ROS 2 源代码了。

设置一个开发文件夹，例如 ``C:\dev\{DISTRO}``：

.. code-block:: console

   $ md C:\dev\{DISTRO}\src
   $ cd C:\dev\{DISTRO}

获取 ``ros2.repos`` 文件，该文件定义了要克隆的仓库：

.. code-block:: console

   $ vcs import --input https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos src

安装额外的 RMW 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在构建时或运行时替换。
关于如何使用多种 RMW，请参见 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

构建工作空间中的代码
^^^^^^^^^^^^^^^^^^^^

.. _windows-dev-build-ros2:

要构建 ``\{DISTRO}`` 文件夹树：

.. code-block:: console

   $ colcon build --merge-install

.. note::

   我们在这里使用 ``--merge-install``，以避免构建结束时 ``PATH`` 变量过长。
   如果你调整这些说明来构建更小的工作空间，那么你可能可以使用默认行为，即隔离安装，也就是将每个软件包安装到不同的文件夹。

.. note::

   由于大量软件包被拉取到工作空间中，源代码安装可能需要很长时间。

设置环境
--------

启动一个新的 Windows 命令提示符，它将用于示例。

source pixi 环境
^^^^^^^^^^^^^^^^

在你打开的每个命令提示符中，都必须执行此操作以设置依赖项的路径：

.. code-block:: console

   $ cd C:\dev
   $ pixi shell

source ROS 2 环境
^^^^^^^^^^^^^^^^^

在你打开的每个命令提示符中，都必须执行此操作以设置 ROS 2 工作空间：

.. code-block:: console

   $ call C:\dev\{DISTRO}\install\local_setup.bat

这将自动为已构建支持的任何 DDS 供应商设置环境。

如果一切正常，上一条命令输出一次 ``The system cannot find the path specified.`` 是正常现象。

尝试一些示例
------------

请注意，第一次运行任何可执行文件时，你必须通过 Windows 防火墙弹窗允许网络访问。

你可以使用以下命令运行测试：

.. code-block:: console

   $ colcon test --merge-install

.. note::

   只有当构建步骤中也使用了 ``--merge-install`` 时，才应使用它。

之后，你可以使用以下命令获取测试摘要：

.. code-block:: console

   $ colcon test-result

要运行示例，首先打开一个干净的新 ``cmd.exe``，并通过 source ``local_setup.bat`` 文件来设置工作空间。
然后，运行一个 C++ ``talker``\ ：

.. code-block:: console

   $ call install\local_setup.bat
   $ ros2 run demo_nodes_cpp talker

在另一个单独的命令提示符中，你可以执行相同的操作，但改为运行一个 Python ``listener``\ ：

.. code-block:: console

   $ call install\local_setup.bat
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 显示它正在 ``Publishing`` 消息，而 ``listener`` 显示 ``I heard`` 那些消息。
这验证了 C++ 和 Python API 都正常工作。
太棒了！

.. note::

   不建议在已经 source 了 ``local_setup.bat`` 的同一个 cmd 提示符中进行构建。

后续步骤
--------

继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并学习 ROS 2 核心概念。

保持最新
--------

参见 :doc:`../Maintaining-a-Source-Checkout` 以定期刷新你的源代码安装。

故障排查
--------

故障排查技巧可参见 :ref:`此处 <windows-troubleshooting>`。

卸载
----

1. 如果你按照上述说明使用 colcon 安装了工作空间，那么"卸载"可能只是打开一个新终端并且不 source 工作空间的 ``setup`` 文件即可。
   这样，你的环境将表现得就像系统中没有安装 {DISTRO_TITLE} 一样。

2. 如果你还想释放空间，可以删除整个工作空间目录：

   .. code-block:: console

      $ rmdir /s /q C:\dev\{DISTRO}
