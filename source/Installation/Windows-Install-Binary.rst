Windows（二进制）
=================

.. contents:: 目录
   :depth: 2
   :local:

本页介绍如何从预构建的二进制软件包在 Windows 上安装 ROS 2。

.. note::

    预构建的二进制文件不包含所有 ROS 2 软件包。
    包含 `ROS base 变体 <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中的所有软件包，但只包含 `ROS desktop 变体 <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中的一部分软件包。
    软件包的确切列表由 `这个 ros2.repos 文件 <https://github.com/ros2/ros2/blob/{REPOS_FILE_BRANCH}/ros2.repos>`_ 中列出的仓库描述。

系统要求
--------

仅支持 Windows 10。

.. _windows-install-binary-installing-prerequisites:

为 ROS 2 安装创建位置
----------------------

该位置将同时包含已安装的二进制软件包以及 ROS 2 安装本身。

启动一个 powershell 会话（通常通过点击开始菜单，然后输入 ``powershell``）。

然后创建一个目录来存放安装内容。
由于 Windows 的路径长度限制，该路径应尽可能短。
后续说明中我们将使用 ``C:\pixi_ws``。

.. code-block:: console

   $ md C:\pixi_ws

.. note::

    注意：ROS 2 二进制软件包目前不可重定位，此问题已记录在一个 `文档 issue <https://github.com/ros2/ros2_documentation/issues/5384>`__ 中。
    在此期间请使用 ``C:\pixi_ws``。

安装前置条件
------------

ROS 2 使用 `conda-forge <https://conda-forge.org/>`__ 作为软件包的后端，并以 `pixi <https://pixi.sh/latest/>`__ 作为前端。

.. note::

   安装 conda-forge 可能会触发 Windows Defender 将其视为威胁，但你可以安全地忽略它，只需点击"更多信息"和"仍然运行"。

安装 pixi
^^^^^^^^^

继续使用之前的 powershell 会话，并按照 https://pixi.sh/latest/ 上的说明安装 ``pixi``。
``pixi`` 安装完成后，关闭 powershell 会话并重新启动它，这样可以确保 ``pixi`` 在 PATH 上。

安装依赖项
^^^^^^^^^^

在现有的 powershell 会话中下载 pixi 配置文件：

.. code-block:: console

   $ cd C:\pixi_ws
   $ irm https://raw.githubusercontent.com/ros2/ros2/refs/heads/{REPOS_FILE_BRANCH}/pixi.toml -OutFile pixi.toml

安装依赖项：

.. code-block:: console

   $ pixi install

安装 ROS 2
----------

* 前往发布页面：https://github.com/ros2/ros2/releases
* 下载适用于 Windows 的最新软件包，例如 ``ros2-{DISTRO}-*-windows-release-amd64.zip``。

.. note::

   可能有多个二进制下载选项，这可能会导致文件名不同。

* 将 zip 文件解压到某个位置（我们假设为 ``C:\pixi_ws\ros2-windows``）。

安装额外的 RMW 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
关于如何使用多种 RMW，请参见 :doc:`指南 <../How-To-Guides/Working-with-multiple-RMW-implementations>`。

设置环境
--------

启动一个新的 Windows 命令提示符，示例中将使用它。

source pixi 环境
^^^^^^^^^^^^^^^^

source pixi 环境以设置依赖项：

.. code-block:: console

   $ cd C:\pixi_ws
   $ pixi shell

source ROS 2 环境
^^^^^^^^^^^^^^^^^

在你打开的每个命令提示符中都需要执行此操作，以设置 ROS 2 工作空间：

.. code-block:: console

   $ call C:\pixi_ws\ros2-windows\local_setup.bat

如果你的计算机上未安装 RTI Connext DDS，收到它缺失的警告是正常的。

尝试一些示例
------------

在命令提示符中，按上述方式设置 ROS 2 环境，然后运行一个 C++ ``talker``\ ：

.. code-block:: console

   $ ros2 run demo_nodes_cpp talker

启动另一个命令 shell 并运行一个 Python ``listener``\ ：

.. code-block:: console

   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 显示它正在 ``Publishing`` 消息，而 ``listener`` 显示 ``I heard`` 那些消息。
这验证了 C++ 和 Python API 都正常工作。
太棒了！

后续步骤
--------

继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并学习 ROS 2 核心概念。

故障排查
--------

故障排查技巧可参见 :ref:`此处 <windows-troubleshooting>`。

卸载
----

1. 如果你按照上述说明使用 colcon 安装了工作空间，那么"卸载"可能只是打开一个新终端并且不 source 工作空间的 ``setup`` 文件即可。
   这样，你的环境将表现得就像系统中没有安装 {DISTRO_TITLE} 一样。

2. 如果你还想释放空间，可以删除整个工作空间目录：

   .. code-block:: console

      $ rmdir /s /q C:\pixi_ws
