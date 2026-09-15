安装（Ubuntu）
==============

**目标：** 在 Ubuntu 上安装 ``mvsim`` 软件包并验证其可用。

**教程级别：** 高级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

`MVSim <https://mvsimulator.readthedocs.io/>`__ （MultiVehicle Simulator）是一个轻量级的开源移动机器人仿真器。
它提供基于物理的 2D 仿真与 3D 可视化，支持差速驱动和阿克曼（Ackermann）车辆、
多种传感器类型（LiDAR、相机、IMU、GPS），并可通过标准消息类型原生集成 ROS 2。

MVSim 采用 BSD 3-clause 许可证授权。

前提条件
--------

建议先了解初学者 :doc:`../../../../Tutorials` 中介绍的基本 ROS 原理。
特别是 :doc:`../../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace` 是一个很有用的前提条件。

你应当已经有一个可用的 ROS 2 安装。
如果需要，请按照 :doc:`ROS 2 安装说明 <../../../../Installation>` 操作。

任务
----

1 安装 ``mvsim``
^^^^^^^^^^^^^^^^

你既可以安装已发布的二进制软件包，也可以从源码构建。

.. tabs::

    .. group-tab:: 从 ROS 二进制软件包安装

        在终端中运行以下命令：

        .. code-block:: console

            $ sudo apt install ros-{DISTRO}-mvsim

    .. group-tab:: 从源码构建

        如果还没有 ROS 2 工作空间，先创建一个：

        .. code-block:: console

            $ mkdir -p ~/ros2_ws/src

        加载 ROS 2 环境：

        .. code-block:: console

            $ source /opt/ros/{DISTRO}/setup.bash

        克隆 MVSim 仓库：

        .. code-block:: console

            $ cd ~/ros2_ws/src
            $ git clone https://github.com/MRPT/mvsim.git --recursive

        使用 ``rosdep`` 安装依赖：

        .. code-block:: console

            $ cd ~/ros2_ws
            $ rosdep install --from-paths src --ignore-src -r -y

        构建软件包：

        .. code-block:: console

            $ colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

        加载工作空间：

        .. code-block:: console

            $ source install/setup.bash

2 验证安装
^^^^^^^^^^

检查 ``mvsim`` CLI 是否可用：

.. code-block:: console

    $ mvsim --version

你应该会在终端中看到打印出的已安装版本号。

.. warning::

   ``mvsim`` 软件包提供两个可执行文件：

   - ``mvsim``：用于单独运行仿真器的主 CLI 工具
   - ``mvsim_node``：一个 ROS 2 节点封装，用于运行仿真器并将其连接到其他 ROS 2 节点

3 启动演示
^^^^^^^^^^

要快速验证一切正常，请使用 ROS 2 启动仓库演示：

.. code-block:: console

    $ ros2 launch mvsim demo_warehouse.launch.py

你应该会看到 MVSim GUI 窗口打开，其中有一台 Jackal 机器人在仓库环境中。
使用键盘（W/A/S/D 键）来驱动机器人。

概述
----

你已经安装了 MVSim，并通过启动演示场景验证了它可以正常工作。
在下一个教程中，你将学习如何启动不同的演示场景，并通过 ROS 2 话题与它们交互。
