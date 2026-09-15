RHEL（RPM 软件包）
==================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 {DISTRO_TITLE_FULL} 的 RPM 软件包目前可用于 RHEL 8。
目标平台在 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`__ 中定义。

资源
----

* 状态页面：

  * ROS 2 {DISTRO_TITLE}（RHEL 8）：`amd64 <http://repo.ros2.org/status_page/ros_{DISTRO}_rhel.html>`__
* `Jenkins 实例 <http://build.ros2.org/>`__
* `仓库 <http://repo.ros2.org>`__


设置 locale
-----------

.. include:: _RHEL-Set-Locale.rst

.. _rhel-install-rpms-setup-sources:

配置软件源
----------

你需要启用 EPEL 仓库和 PowerTools 仓库：

.. code-block:: console

   $ sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E %rhel).noarch.rpm
   $ sudo env FORCE_DNF=1 crb enable

.. note:: 此步骤可能因你所使用的发行版而略有不同。
          请查看 `EPEL 文档 <https://docs.fedoraproject.org/en-US/epel/getting-started/>`_

接下来，下载 ``ros2-release`` 软件包并安装它：

.. code-block:: console

   $ sudo dnf install curl
   $ export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
   $ sudo dnf install "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-release-${ROS_APT_SOURCE_VERSION}-1.noarch.rpm"

`ros2-release <https://github.com/ros-infrastructure/ros-apt-source/>`_ 软件包为各个 ROS 仓库提供密钥和仓库配置。
当该软件包的新版本发布到 ROS 仓库时，仓库配置会自动更新。

.. _rhel-install-rpms-install-ros-2-packages:

安装 ROS 2 软件包
-----------------

.. include:: _Dnf-Update-Admonition.rst

桌面版安装（推荐）：ROS、RViz、演示程序和教程。

.. code-block:: console

   $ sudo dnf install ros-{DISTRO}-desktop

ROS-Base 安装（精简版）：通信库、消息包、命令行工具。
不包含 GUI 工具。

.. code-block:: console

   $ sudo dnf install ros-{DISTRO}-ros-base

环境配置
--------

加载安装脚本
^^^^^^^^^^^^

通过加载以下文件来配置你的环境。

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash

.. note::

   如果你不使用 console，请将 ``.bash`` 替换为你所用的 shell。
   可选值包括：``setup.bash``、``setup.sh``、``setup.zsh``。

尝试一些示例
------------

如果你在上面安装了 ``ros-{DISTRO}-desktop``，可以尝试一些示例。

在一个终端中，加载安装脚本，然后运行 C++ 的 ``talker``\ ：

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp talker

在另一个终端中加载安装脚本，然后运行 Python 的 ``listener``\ ：

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 输出 ``Publishing`` 消息，而 ``listener`` 输出 ``I heard`` 这些消息。
这验证了 C++ 和 Python API 都能正常工作。
太棒了！

如果你想使用其他 RMW 实现，可以查看 :doc:`指南 <./RMW-Implementations>`。

安装后的后续步骤
----------------
继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并了解 ROS 2 的核心概念。

其他 RMW 实现（可选）
---------------------
ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
请参阅关于如何使用多个 RMW 的 :doc:`指南 <../How-To-Guides/Working-with-multiple-RMW-implementations>`。

故障排查
--------

故障排查技巧可以在 :doc:`这里 <../How-To-Guides/Installation-Troubleshooting>` 找到。

卸载
----

如果你已经通过二进制包安装了 ROS 2，之后需要卸载或切换到基于源码的安装，请运行以下命令：

.. code-block:: console

   $ sudo dnf remove ros-{DISTRO}-*

要移除仓库配置，请运行

.. code-block:: console

   $ sudo dnf remove ros2-release
