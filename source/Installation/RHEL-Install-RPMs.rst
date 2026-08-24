RHEL（RPM 软件包）
==================

.. contents:: 目录
   :depth: 2
   :local:

ROS 2 {DISTRO_TITLE_FULL} 的 RPM 软件包目前可用于 RHEL 9。
目标平台在 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`__ 中定义。

资源
----

* 状态页面：

  * ROS 2 {DISTRO_TITLE}（RHEL 9）：`amd64 <http://repo.ros2.org/status_page/ros_{DISTRO}_rhel.html>`__
* `Jenkins 实例 <http://build.ros2.org/>`__
* `软件仓库 <http://repo.ros2.org>`__

系统设置
--------

设置语言环境
^^^^^^^^^^^^

.. include:: _RHEL-Set-Locale.rst

启用所需软件仓库
^^^^^^^^^^^^^^^^

你需要启用 EPEL 软件仓库和 PowerTools 软件仓库：

.. code-block:: console

   $ sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E %rhel).noarch.rpm
   $ sudo env FORCE_DNF=1 crb enable

.. note:: 根据你所使用的发行版，此步骤可能略有不同。
          `请查阅 EPEL 文档 <https://docs.fedoraproject.org/en-US/epel/getting-started/>`_

接下来，下载 ``ros2-release`` 软件包并安装：

.. code-block:: console

   $ sudo dnf install curl
   $ export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
   $ sudo dnf install "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-release-${ROS_APT_SOURCE_VERSION}-1.noarch.rpm"

`ros2-release <https://github.com/ros-infrastructure/ros-apt-source/>`_ 软件包为各个 ROS 软件仓库提供密钥和仓库配置。
当该软件包的新版本发布到 ROS 软件仓库时，仓库配置会自动更新。

安装开发工具（可选）
^^^^^^^^^^^^^^^^^^^^

如果你要构建 ROS 软件包或进行其他开发工作，你还可以安装开发工具：

.. code-block:: console

   $ sudo dnf install -y \
     cmake \
     gcc-c++ \
     git \
     make \
     patch \
     python3-colcon-common-extensions \
     python3-flake8-blind-except \
     python3-flake8-class-newline \
     python3-flake8-deprecated \
     python3-mypy \
     python3-pip \
     python3-pydocstyle \
     python3-pytest \
     python3-pytest-repeat \
     python3-pytest-rerunfailures \
     python3-rosdep \
     python3-setuptools \
     python3-vcstool \
     wget

安装 ROS 2
----------

.. include:: _Dnf-Update-Admonition.rst

桌面安装（推荐）：ROS、RViz、演示、教程。

.. code-block:: console

   $ sudo dnf install ros-{DISTRO}-desktop

ROS-Base 安装（基础版）：通信库、消息软件包、命令行工具。
不含 GUI 工具。

.. code-block:: console

   $ sudo dnf install ros-{DISTRO}-ros-base

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

   如果你不使用 console，请将 ``.bash`` 替换为你的 shell。
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

   $ sudo dnf remove ros-{DISTRO}-*

要移除仓库配置，请运行

.. code-block:: console

   $ sudo dnf remove ros2-release
