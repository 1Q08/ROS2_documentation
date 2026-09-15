安装（Windows）
===============

**目标：** 安装 ``webots_ros2`` 包，并在 Windows 上运行仿真示例。

**教程级别：** 高级

**用时：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``webots_ros2`` 包提供了 ROS 2 与 Webots 之间的接口。
它包含多个子包，包括 ``webots_ros2_driver``，该子包允许 ROS 节点与 Webots 通信。
其他子包主要是示例，展示了使用该接口的多种可能实现。
在本教程中，你将安装该软件包，并学习如何运行其中一个示例。

前置条件
--------

建议理解初学者 :doc:`../../../../Tutorials` 中涵盖的基本 ROS 原理。
特别是 :doc:`../../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace` 和 :doc:`../../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package` 是有用的前置条件。

Webots 是使用 ``webots_ros2`` 包的前置条件。
你可以遵循 `安装步骤 <https://cyberbotics.com/doc/guide/installation-procedure>`_ 或 `从源码构建 <https://github.com/cyberbotics/webots/wiki/Windows-installation/>`_。

或者，你也可以让 ``webots_ros2`` 自动下载 Webots。
当你启动该软件包的示例且未找到 Webots 安装时，就会出现这个选项。

多个 Webots 安装
^^^^^^^^^^^^^^^^

如果你安装了多个 Webots，ROS 2 将按以下位置顺序查找 Webots：

1. 如果设置了 ``ROS2_WEBOTS_HOME`` 环境变量，ROS 2 将使用此文件夹中的 Webots，而不论其版本。
2. 如果设置了 ``WEBOTS_HOME`` 环境变量，ROS 2 将使用此文件夹中的 Webots，而不论其版本。
3. 如果上述条件均未设置/安装，ROS 2 将在默认安装路径中查找兼容版本的 Webots：``C:\Program Files\Webots``。
4. 如果找不到 Webots，``webots_ros2`` 将弹出一个窗口，提供最新兼容版本 Webots 的自动安装。

任务
----

1 安装 WSL2
^^^^^^^^^^^

在 Windows 上，WSL（适用于 Linux 的 Windows 子系统）比原生 Windows 安装能带来更好的 ROS 2 使用体验，因为它运行在 Linux 平台上。
请安装与你 ROS 发行版兼容的 Ubuntu 版本的 WSL，并按照 `微软官方教程 <https://learn.microsoft.com/en-us/windows/wsl/install>`_ 升级到 WSL2。

2 在 WSL 中安装 ROS 2
^^^^^^^^^^^^^^^^^^^^^

按照 :doc:`../../../../Installation/Ubuntu-Install-Debs`，在 Ubuntu WSL 中安装 ROS 2。

3 安装 ``webots_ros2``
^^^^^^^^^^^^^^^^^^^^^^
然后，你可以从官方发布包安装 ``webots_ros2``，也可以从 `Github <https://github.com/cyberbotics/webots_ros2>`_ 的最新源码安装。

以下命令必须在 WSL 环境中运行。

.. tabs::

    .. group-tab:: 安装 ``webots_ros2`` 发布包

        在终端中运行以下命令。

        .. code-block:: console

            $ sudo apt-get install ros-{DISTRO}-webots-ros2

    .. group-tab:: 从源码安装 ``webots_ros2``

        创建一个带 ``src`` 目录的 ROS 2 工作空间。

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

        加载此工作空间。

        .. code-block:: console

            $ source install/local_setup.bash


4 启动 ``webots_ros2_universal_robot`` 示例
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

WSL 目前不支持硬件加速。
因此，Webots 应在 Windows 上启动，而 ROS 部分在 WSL 中运行。
为此，以下命令必须在 WSL 环境中运行。

如果尚未加载，请先加载 ROS 2 环境。

.. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash

设置 ``WEBOTS_HOME`` 环境变量可以让你启动特定的 Webots 安装（例如 ``C:\Program Files\Webots``）。
使用挂载点 "/mnt" 来引用原生 Windows 上的路径。

.. code-block:: console

        $ export WEBOTS_HOME=/mnt/c/Program\ Files/Webots

如果是从源码安装的，请加载你的 ROS 2 工作空间（如果尚未加载）。

.. code-block:: console

        $ cd ~/ros2_ws
        $ source install/local_setup.bash

使用 ROS 2 launch 命令启动演示软件包（例如 ``webots_ros2_universal_robot``）。

.. code-block:: console

        $ ros2 launch webots_ros2_universal_robot multirobot_launch.py


5 RViz 排错
^^^^^^^^^^^

在较新版本的 WSL2 中，RViz 应该可以开箱即用。

你可以通过运行任何使用 RViz 的示例来检查它是否正常工作，例如：

.. code-block:: console

        $ sudo apt install ros-{DISTRO}-slam-toolbox
        $ ros2 launch webots_ros2_tiago robot_launch.py rviz:=true slam:=true

Tiago 机器人可以通过以下方式控制：

.. code-block:: console

        $ ros2 run teleop_twist_keyboard teleop_twist_keyboard

在较旧的 WSL 版本中，由于没有可用的显示器，RViz2 可能无法直接工作。
要使用 RViz，你可以升级 WSL，或启用 X11 转发。

.. tabs::
    .. group-tab:: 升级 WSL

        在 Windows shell 中：

        .. code-block:: console

            $ wsl --update

    .. group-tab:: 启用 X11 转发

        对于较旧版本的 WSL，可以按照以下步骤操作：

        1. 安装 `VcXsrv <https://sourceforge.net/projects/vcxsrv/>`_。
        2. 启动 VcXsrv。
           你可以保留大多数默认参数，但 ``Extra settings`` 页面除外，在那里你必须勾选 ``Clipboard``、``Primary Selection`` 和 ``Disable access control``，并取消勾选 ``Native opengl``。
        3. 你可以保存配置以便将来启动。
        4. 点击 ``Finish``，你将看到 X11 服务器在图标托盘中运行。
        5. 在你的 WSL 环境中，导出 ``DISPLAY`` 变量。

            .. code-block:: console

                $ export DISPLAY=$(ip route list default | awk '{print }'):0

            你可以将其添加到你的 ``.bashrc`` 中，这样它在每个未来的 WSL 环境中都会设置。

            .. code-block:: console

                $ echo "export DISPLAY=$(ip route list default | awk '{print }'):0" >> ~/.bashrc
