.. redirect-from::

   Installation/Linux-Install-Debians
   Installation/Ubuntu-Install-Debians

Ubuntu（deb 软件包）
====================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 {DISTRO_TITLE_FULL} 的 deb 软件包目前可用于 Ubuntu Jammy（22.04）。
目标平台在 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`__ 中定义。

资源
----

* 状态页面：

  * ROS 2 {DISTRO_TITLE}（Ubuntu Jammy）：`amd64 <http://repo.ros2.org/status_page/ros_{DISTRO}_default.html>`__\ 、`arm64 <http://repo.ros2.org/status_page/ros_{DISTRO}_ujv8.html>`__
* `Jenkins 实例 <http://build.ros2.org/>`__
* `仓库 <http://repo.ros2.org>`__


设置 locale
-----------

.. include:: _Ubuntu-Set-Locale.rst

.. _linux-install-debians-setup-sources:

配置软件源
----------

.. include:: _Apt-Repositories.rst

.. _linux-install-debs-install-ros-2-packages:

安装 ROS 2 软件包
-----------------

配置好仓库后，更新你的 apt 仓库缓存。

.. code-block:: console

   $ sudo apt update

.. include:: _Apt-Upgrade-Admonition.rst

.. warning::

   由于 Ubuntu 22.04 的早期更新，务必在安装 ROS 2 之前先更新 ``systemd`` 和 ``udev`` 相关的软件包。
   在未升级的全新安装系统上安装 ROS 2 的依赖项，可能会触发 **关键系统软件包被移除**。

   更多信息请参阅 `ros2/ros2#1272 <https://github.com/ros2/ros2/issues/1272>`_ 和 `Launchpad #1974196 <https://bugs.launchpad.net/ubuntu/+source/systemd/+bug/1974196>`_。

桌面版安装（推荐）：ROS、RViz、演示程序和教程。

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-desktop

ROS-Base 安装（精简版）：通信库、消息包、命令行工具。
不包含 GUI 工具。

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-ros-base

开发工具：用于构建 ROS 软件包的编译器和其他工具

.. code-block:: console

   $ sudo apt install ros-dev-tools

环境配置
--------

加载安装脚本
^^^^^^^^^^^^

通过加载以下文件来配置你的环境。

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash

.. note::

   如果你不使用 bash，请将 ``.bash`` 替换为你所用的 shell。
   可选值包括：``setup.bash``、``setup.sh``、``setup.zsh``。

尝试一些示例
------------

talker-listener
^^^^^^^^^^^^^^^

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

使用 ROS 1 桥接
---------------
ROS 1 桥接可以将话题从 ROS 1 连接到 ROS 2，反之亦然。
有关如何构建和使用 ROS 1 桥接的专门说明，请参阅 `文档 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__。

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

   $ sudo apt remove '~nros-{DISTRO}-*' && sudo apt autoremove

你可能还需要移除该仓库：

.. code-block:: console

   $ sudo apt remove ros2-apt-source
   $ sudo apt update
   $ sudo apt autoremove
   $ sudo apt upgrade # Consider upgrading for packages previously shadowed.
