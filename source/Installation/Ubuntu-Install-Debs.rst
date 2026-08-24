.. redirect-from::

   Installation/Linux-Install-Debians
   Installation/Ubuntu-Install-Debians

Ubuntu（deb 软件包）
====================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 {DISTRO_TITLE_FULL} 的 deb 软件包目前可用于 Ubuntu Noble (24.04)。
目标平台在 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`__ 中定义。

资源
----

* 状态页面：

  * ROS 2 {DISTRO_TITLE}（Ubuntu Noble 24.04）：`amd64 <http://repo.ros2.org/status_page/ros_{DISTRO}_default.html>`__\ ，`arm64 <http://repo.ros2.org/status_page/ros_{DISTRO}_unv8.html>`__
* `Jenkins 实例 <http://build.ros2.org/>`__
* `软件仓库 <http://repo.ros2.org>`__

系统设置
--------

设置语言环境
^^^^^^^^^^^^

.. include:: _Ubuntu-Set-Locale.rst

启用所需软件仓库
^^^^^^^^^^^^^^^^

.. include:: _Apt-Repositories.rst

.. _linux-install-debs-install-ros-2-packages:

安装开发工具（可选）
^^^^^^^^^^^^^^^^^^^^

如果你要构建 ROS 软件包或进行其他开发工作，你还可以安装开发工具：

.. warning::

   在 Ubuntu 24.04 安装中，你的 apt 源可能只包含基础的 ``noble`` 套件。
   这可能会在安装 ``ros-dev-tools`` 时导致依赖冲突。

   检查 ``/etc/apt/sources.list.d/ubuntu.sources``，并确保 ``Suites:`` 行包含 ``noble-updates`` 和 ``noble-backports``：

   .. code-block:: console

      $ grep Suites /etc/apt/sources.list.d/ubuntu.sources

   如果缺少 ``noble-updates`` 或 ``noble-backports``，请编辑该文件并将该行更新为：

   .. code-block:: text

      Suites: noble noble-updates noble-backports

   然后运行：

   .. code-block:: console

      $ sudo apt clean && sudo apt update && sudo apt full-upgrade -y

.. code-block:: console

   $ sudo apt update && sudo apt install ros-dev-tools

安装 ROS 2
----------

设置好软件仓库后，更新你的 apt 软件仓库缓存。

.. code-block:: console

   $ sudo apt update

.. include:: _Apt-Upgrade-Admonition.rst

桌面安装（推荐）：ROS、RViz、演示、教程。

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-desktop

ROS-Base 安装（基础版）：通信库、消息软件包、命令行工具。
不含 GUI 工具。

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-ros-base

安装额外的 RMW 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
关于如何使用多种 RMW，请参见 :doc:`指南 <../How-To-Guides/Working-with-multiple-RMW-implementations>`。

设置环境
--------

通过 source 以下文件来设置你的环境。

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash

.. note::

   如果你不使用 bash，请将 ``.bash`` 替换为你的 shell。
   可选值为：``setup.bash``、``setup.sh``、``setup.zsh``。

尝试一些示例
------------

如果你在上一步安装了 ``ros-{DISTRO}-desktop``，可以尝试一些示例。

在一个终端中，source 设置文件，然后运行一个 C++ ``talker``\ ：

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp talker

在另一个终端中 source 设置文件，然后运行一个 Python ``listener``\ ：

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 显示它正在 ``Publishing`` 消息，而 ``listener`` 显示 ``I heard`` 那些消息。
这验证了 C++ 和 Python API 都正常工作。
太棒了！

如果你想使用其他 RMW 实现，可以查看 :doc:`指南 <./RMW-Implementations>`。

后续步骤
--------

继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并学习 ROS 2 核心概念。

故障排查
--------

故障排查技巧可参见 :doc:`此处 <../How-To-Guides/Installation-Troubleshooting>`。

卸载
----

如果你已经通过二进制包安装了 ROS 2，现在需要卸载它或切换到基于源代码的安装，请运行以下命令：

.. code-block:: console

   $ sudo apt remove '~nros-{DISTRO}-*' && sudo apt autoremove

你可能还想移除软件仓库：

.. code-block:: console

   $ sudo apt remove ros2-apt-source
   $ sudo apt update
   $ sudo apt autoremove
   $ sudo apt upgrade # Consider upgrading for packages previously shadowed.
