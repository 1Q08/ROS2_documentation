安装（Ubuntu）
==============

**目标：** 在 Ubuntu 上安装 ``webots_ros2`` 软件包并运行仿真示例。

**教程级别：** 高级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``webots_ros2`` 软件包提供了 ROS 2 与 Webots 之间的接口。
它包含若干子软件包，其中包括 ``webots_ros2_driver``，它允许你启动 Webots 并与之通信。
这个接口在后续的大多数教程中都会用到，因此需要事先安装它。
其他子软件包主要是一些示例，展示了使用该接口的多种可能实现方式。
在本教程中，你将安装这个软件包，并学习如何运行其中一个示例。

前提条件
--------

建议先了解初学者 :doc:`../../../../Tutorials` 中介绍的基本 ROS 原理。
特别是 :doc:`../../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace` 和 :doc:`../../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package` 都是很有用的前提条件。

要使用 ``webots_ros2`` 接口，应当先安装 Webots 软件。
你可以按照 `安装步骤 <https://cyberbotics.com/doc/guide/installation-procedure>`_ 操作，或者 `从源码构建 <https://github.com/cyberbotics/webots/wiki/Linux-installation/>`_。

或者，你也可以让 ``webots_ros2`` 自动下载并安装 Webots。
当你启动该软件包的示例而未找到 Webots 安装时，就会出现这个选项。

Webots 的多个安装
^^^^^^^^^^^^^^^^^

如果你的计算机上安装了不同版本的 Webots，``webots_ros2`` 会按以下顺序在以下位置查找 Webots：

1. 如果设置了 ``ROS2_WEBOTS_HOME`` 环境变量，ROS 2 将使用该文件夹中的 Webots，而不论其版本。
2. 如果设置了 ``WEBOTS_HOME`` 环境变量，ROS 2 将使用该文件夹中的 Webots，而不论其版本。
3. 如果这些变量都没有设置，``webots_ros2`` 会在兼容版本的默认安装路径中查找 Webots：``/usr/local/webots`` 和 ``/snap/webots/current/usr/share/webots``。
4. 如果找不到 Webots，``webots_ros2`` 会弹出一个窗口，提供自动安装最新兼容版本 Webots 的选项。

任务
----

1 安装 ``webots_ros2``
^^^^^^^^^^^^^^^^^^^^^^
你既可以安装官方发布的软件包，也可以从 `Github <https://github.com/cyberbotics/webots_ros2>`_ 上的最新源码安装。

.. tabs::

    .. group-tab:: 安装 ``webots_ros2`` 发行版软件包

        在终端中运行以下命令。

        .. code-block:: console

            $ sudo apt-get install ros-{DISTRO}-webots-ros2

    .. group-tab:: 从源码安装 ``webots_ros2``

        创建一个带有 ``src`` 目录的 ROS 2 工作空间。

        .. code-block:: console

            $ mkdir -p ~/ros2_ws/src

        加载 ROS 2 环境。

        .. code-block:: console

            $ source /opt/ros/{DISTRO}/setup.bash

        从 Github 获取源码。

        .. code-block:: console

            $ cd ~/ros2_ws
            $ git clone --recurse-submodules https://github.com/cyberbotics/webots_ros2.git src/webots_ros2

        安装软件包依赖。

        .. code-block:: console

            $ sudo apt install python3-pip python3-rosdep python3-colcon-common-extensions
            $ sudo rosdep init && rosdep update
            $ rosdep install --from-paths src --ignore-src --rosdistro {DISTRO}

        使用 ``colcon`` 构建软件包。

        .. code-block:: console

            $ colcon build

        加载这个工作空间。

        .. code-block:: console

            $ source install/local_setup.bash

2 启动 ``webots_ros2_universal_robot`` 示例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下说明介绍了如何启动所提供的一个示例。

如果还没有加载 ROS 2 环境，请先加载。

.. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash

设置 ``WEBOTS_HOME`` 环境变量可以让你启动指定的 Webots 安装。

.. code-block:: console

        $ export WEBOTS_HOME=/usr/local/webots

如果是通过源码安装的，请先加载你的 ROS 2 工作空间（如果还没有加载）。

.. code-block:: console

        $ cd ~/ros2_ws
        $ source install/local_setup.bash

使用 ROS 2 launch 命令启动演示软件包（例如 ``webots_ros2_universal_robot``）。

.. code-block:: console

        $ ros2 launch webots_ros2_universal_robot multirobot_launch.py
