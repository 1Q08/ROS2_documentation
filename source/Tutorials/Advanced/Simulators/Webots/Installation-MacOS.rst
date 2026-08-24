安装（macOS）
=============

**目标：** 安装 ``webots_ros2`` 包，并在 macOS 上运行仿真示例。

**教程级别：** 高级

**用时：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``webots_ros2`` 包提供了 ROS 2 与 Webots 之间的接口。
它包含多个子包，包括 ``webots_ros2_driver``，该子包允许你启动 Webots 并与它通信。
其他子包主要是示例，展示了使用该接口的多种可能实现。
在本教程中，你将安装该软件包，并学习如何运行其中一个示例。

前置条件
--------

建议理解初学者 :doc:`../../../../Tutorials` 中涵盖的基本 ROS 原理。
特别是 :doc:`../../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace` 和 :doc:`../../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package` 是有用的前置条件。

如下文所述，为了在虚拟机中使用 ``webots_ros2`` 包，必须在 Mac 上原生安装 Webots。
你可以遵循 `安装步骤 <https://cyberbotics.com/doc/guide/installation-procedure>`_ 或 `从源码构建 <https://github.com/cyberbotics/webots/wiki/macOS-installation/>`_。

任务
----

在 macOS 上，基于 UTM 虚拟机的方案比原生 macOS 安装能带来更好的 ROS 2 使用体验，因为它是在 Linux 环境中运行 ROS。
但是，Webots 应该原生安装在 macOS 上，它将能够与运行在虚拟机（VM）中的 ROS 节点通信。
此方案允许 Webots 使用原生 3D 硬件加速。
VM 运行所有 ROS 部分（包括 RViz），并通过 TCP 连接到主机以启动 Webots。
一个共享文件夹允许脚本将世界文件和其他资源文件从 VM 传输到运行 Webots 的 macOS。

以下步骤解释了如何创建带 ``webots_ros2`` 发布包安装的 VM 镜像。
也可以从源码安装。

1 创建 VM 镜像
^^^^^^^^^^^^^^

在你的 macOS 机器上安装 UTM。
链接可以在 `UTM 官网 <https://mac.getutm.app/>`_ 上找到。

下载 `Ubuntu 22.04 <https://cdimage.ubuntu.com/jammy/daily-live/current/>`_ 的 ``.iso`` 镜像（用于 Humble 和 Rolling）或 `Ubuntu 20.04 <https://cdimage.ubuntu.com/focal/daily-live/pending/>`_ 的 ``.iso`` 镜像（用于 Foxy）。
请务必下载与你 CPU 架构对应的镜像。

在 UTM 软件中：

* 创建一个新镜像，并选择 ``Virtualize`` 选项。
* 在 ``Boot ISO Image`` 字段中选择你已下载的 ISO 镜像。
* 将所有硬件设置保留默认值（包括禁用硬件加速）。
* 在 ``Shared Directory`` 窗口中，选择一个将被 ``webots_ros2`` 用于将所有 Webots 资源传输到主机的文件夹。
  在本示例中，选定的文件夹是 ``/Users/username/shared``。
* 将其余所有参数保留默认值。
* 启动 VM。
  注意，每次启动 VM 时你都可以选择另一个共享文件夹。
* 在 VM 首次启动期间，安装 Ubuntu 并为你的账户选择一个用户名。
  在本示例中，用户名是 ``ubuntu``。
* 一旦 Ubuntu 安装完成，关闭 VM，从 CD/DVD 字段中移除 iso 镜像，然后重新启动 VM。

2 配置 VM
^^^^^^^^^
在本节中，ROS 2 被安装在 VM 中，并配置共享文件夹。
以下说明和命令都在 VM 内部运行。

* 在已启动的 VM 中打开终端，按照 :doc:`../../../../Installation/Ubuntu-Install-Debs` 中的说明安装你需要的 ROS 2 发行版：
* 在 VM 中创建一个文件夹用作共享文件夹。
  在本示例中，VM 中的共享文件夹是 ``/home/ubuntu/shared``。

  .. code-block:: console

      $ mkdir /home/ubuntu/shared

* 要将此文件夹挂载到主机，请执行以下命令。
  如果你的共享文件夹路径不同，请不要忘记修改路径。

  .. code-block:: console

      $ sudo mount -t 9p -o trans=virtio share /home/ubuntu/shared -oversion=9p2000.L

* 要在启动 VM 时自动将此文件夹挂载到主机，请将以下行添加到 ``/etc/fstab``。
  如果你的共享文件夹路径不同，请不要忘记修改路径。

  .. code-block:: console

      share     /home/ubuntu/shared     9p      trans=virtio,version=9p2000.L,rw,_netdev,nofail 0       0

* 环境变量 ``WEBOTS_SHARED_FOLDER`` 必须始终设置，包才能在 VM 中正常工作。
  此变量向 ``webots_ros2`` 包指定用于在主机与虚拟机（VM）之间交换数据的共享文件夹位置。
  此变量应使用的值格式为 ``<主机共享文件夹>:<VM 共享文件夹>``，其中 ``<主机共享文件夹>`` 是主机上共享文件夹的路径，``<VM 共享文件夹>`` 是 VM 上同一个共享文件夹的路径。

  在本示例中：

  .. code-block:: console

    $ export WEBOTS_SHARED_FOLDER=/Users/username/shared:/home/ubuntu/shared

  你可以将此命令行添加到 ``~/.bashrc`` 文件中，以便在启动新终端时自动设置此环境变量。

3 安装 ``webots_ros2``
^^^^^^^^^^^^^^^^^^^^^^

你可以从官方发布包安装 ``webots_ros2``，也可以从 `Github <https://github.com/cyberbotics/webots_ros2>`_ 的最新源码安装。

.. tabs::

    .. group-tab:: 安装 ``webots_ros2`` 发布包

        在 VM 终端中运行以下命令。

        .. code-block:: console

            $ sudo apt-get install ros-{DISTRO}-webots-ros2

    .. group-tab:: 从源码安装 ``webots_ros2``

        安装 git。

        .. code-block:: console

            $ sudo apt-get install git

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

如前面几节所述，该包使用共享文件夹在 VM 与主机之间与 Webots 通信。
为了让 Webots 能够从 VM 的 ROS 包在主机上启动，必须运行一个本地 TCP 仿真服务器。

服务器可以在此处下载：`local_simulation_server.py <https://github.com/cyberbotics/webots-server/blob/main/local_simulation_server.py>`_。
在 ``WEBOTS_HOME`` 环境变量中指定 Webots 安装文件夹（例如 ``/Applications/Webots.app``），并在主机上的新终端（不是 VM 中）运行以下命令来启动服务器：

.. code-block:: console

        $ export WEBOTS_HOME=/Applications/Webots.app
        $ python3 local_simulation_server.py

在 VM 中打开终端，执行以下命令来启动软件包：

如果尚未加载，请先加载 ROS 2 环境。

.. code-block:: console

        $ source /opt/ros/{DISTRO}/setup.bash

如果是从源码安装的，请加载你的 ROS 2 工作空间（如果尚未加载）。

.. code-block:: console

        $ cd ~/ros2_ws
        $ source install/local_setup.bash

如果尚未在 ``~/.bashrc`` 中设置，请设置 ``WEBOTS_SHARED_FOLDER`` （详见前面几节）。
请确保根据你各自目录的位置修改路径。

.. code-block:: console

        $ export WEBOTS_SHARED_FOLDER=/Users/username/shared:/home/ubuntu/shared

使用 ROS 2 launch 命令启动演示软件包（例如 ``webots_ros2_universal_robot``）。

.. code-block:: console

        $ ros2 launch webots_ros2_universal_robot multirobot_launch.py

如果 Webots 被关闭或 ROS 2 进程被中断，本地服务器将自动等待新的软件包启动，并会清理共享文件夹以备下次运行。
