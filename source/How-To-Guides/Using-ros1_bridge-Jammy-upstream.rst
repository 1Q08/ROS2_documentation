在 Ubuntu 22.04 上将 ``ros1_bridge`` 与上游 ROS 一起使用
========================================================

.. contents:: 目录
   :depth: 1
   :local:

ROS 2 Humble（和 Rolling）在 Ubuntu 22.04 Jammy Jellyfish 上的发布，
标志着 ROS 2 首次在一个没有官方 ROS 1 发行版的平台上发布。
虽然 ROS 1 Noetic 在其 `长期支持窗口 <https://reps.openrobotics.org/rep-0003/#noetic-ninjemys-may-2020---may-2025>`__ 期间将继续得到支持，
但它只针对 Ubuntu 20.04。
另外，Debian 和 Ubuntu 中还有 `ROS 1 包的上游变体 <https://packages.ubuntu.com/jammy/ros-desktop>`__，
它们并非由 ROS 维护者作为官方发行版维护。

本指南概述了在 Ubuntu 22.04 Jammy Jellyfish 上将这些上游包与
ROS 2 发行版桥接的当前机制。
这为仍然依赖 ROS 1、但希望迁移到更新的 ROS 2 和 Ubuntu 发行版的用户
提供了一条迁移路径。

通过 deb 包安装 ROS 2
---------------------

目前在 Ubuntu Jammy 上，:doc:`通过 deb 包安装 ROS 2 <../Installation/Ubuntu-Install-Debs>` 尚不可行。
Ubuntu 仓库中可用的 ``catkin-pkg-modules`` 版本与 ROS 2 包仓库中的版本冲突。

如果 ROS 2 apt 仓库位于可用的 apt 仓库（``/etc/apt/sources.list.d``）中，
则无法安装任何 ROS 1 包。
错误将是：

.. code-block:: console

  $ apt install ros-core-dev
  Reading package lists... Done
  Building dependency tree... Done
  Reading state information... Done
  Some packages could not be installed. This may mean that you have
  requested an impossible situation or if you are using the unstable
  distribution that some required packages have not yet been created
  or been moved out of Incoming.
  The following information may help to resolve the situation:

  The following packages have unmet dependencies:
   ros-core-dev : Depends: catkin but it is not installable
  E: Unable to correct problems, you have held broken packages.

要纠正这一点，请从你的 ``sources.list`` 中移除 packages.ros.org。
如果你一直在按照 ROS 2 安装指南操作，只需移除 ``/etc/apt/sources.list.d/ros2.list`` 即可。

目前，要支持 ``ros1_bridge``，请按照下面的说明从源码构建 ROS 2。

从源码安装 ROS 2
----------------

在 Ubuntu Jammy 上，:doc:`从源码安装 ROS 2 <../Installation/Alternatives/Ubuntu-Development-Setup>` 是唯一可行的配置。

下面是从源码构建说明中必要指令的摘要。
重要的区别在于，由于包冲突，我们跳过使用 ROS 2 apt 仓库。

安装开发工具和 ROS 工具
^^^^^^^^^^^^^^^^^^^^^^^

由于我们不使用 ROS 2 apt 仓库，因此必须通过 ``pip`` 安装 ``colcon``。

.. code-block:: console

   $ sudo apt update && sudo apt install -y \
     build-essential \
     cmake \
     git \
     python3-flake8 \
     python3-flake8-blind-except \
     python3-flake8-builtins \
     python3-flake8-class-newline \
     python3-flake8-comprehensions \
     python3-flake8-deprecated \
     python3-flake8-docstrings \
     python3-flake8-import-order \
     python3-flake8-quotes \
     python3-pip \
     python3-pytest \
     python3-pytest-cov \
     python3-pytest-repeat \
     python3-pytest-rerunfailures \
     python3-rosdep \
     python3-setuptools \
     wget

   # 从 PyPI 安装 colcon，而不是通过 apt 包安装
   python3 -m pip install -U colcon-common-extensions vcstool

从这里开始，继续按照 :doc:`源码安装指南 <../Installation/Alternatives/Ubuntu-Development-Setup>` 构建 ROS 2。

从 Ubuntu 包安装 ROS 1
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ sudo apt update && sudo apt install -y ros-core-dev


构建 ``ros1_bridge``
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    $ mkdir -p ~/ros1_bridge/src # 为 ros1_bridge 创建工作空间
    $ cd ~/ros1_bridge/src
    $ git clone https://github.com/ros2/ros1_bridge
    $ cd ~/ros1_bridge
    $. ~/ros2_humble/install/local_setup.bash # Source ROS 2 工作空间
    $ colcon build # 构建

构建完所有 ``ros1_bridge`` 之后，剩余的 `ros1_bridge 示例 <https://github.com/ros2/ros1_bridge#example-1-run-the-bridge-and-the-example-talker-and-listener>`__
应该能够与你的新安装一起正常工作。

