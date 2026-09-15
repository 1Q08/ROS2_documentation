在 Ubuntu 22.04 上配合上游 ROS 使用 ``ros1_bridge``
===================================================

.. contents:: 目录
   :depth: 1
   :local:

Ubuntu 22.04 Jammy Jellyfish 上的 ROS 2 Humble（以及 Rolling）发行版标志着首个在没有官方 ROS 1 发行版的平台上发布的 ROS 2 版本。
虽然 ROS 1 Noetic 将在其 `长期支持窗口 <https://reps.openrobotics.org/rep-0003/#noetic-ninjemys-may-2020---may-2025>`__ 期间继续获得支持，但它仅面向 Ubuntu 20.04。
另一种选择是 Debian 和 Ubuntu 中的 `上游 ROS 1 软件包变体 <https://packages.ubuntu.com/jammy/ros-desktop>`__，它们并非由 ROS 维护者作为官方发行版维护。

本指南概述了当前在 Ubuntu 22.04 Jammy Jellyfish 上将 ROS 2 发行版与这些上游软件包进行桥接的机制。
这为仍然依赖 ROS 1、但希望迁移到较新的 ROS 2 和 Ubuntu 发行版的用户提供了一条迁移路径。

通过 deb 软件包安装 ROS 2
-------------------------

在 Ubuntu Jammy 上，:doc:`通过 deb 软件包安装 ROS 2 <../Installation/Ubuntu-Install-Debs>` 目前无法正常工作。
Ubuntu 仓库中可用的 ``catkin-pkg-modules`` 版本与 ROS 2 软件包仓库中的版本冲突。

如果 ROS 2 apt 仓库存在于可用的 apt 仓库中（``/etc/apt/sources.list.d``），则任何 ROS 1 软件包都无法安装。
错误信息将是：

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

要解决此问题，请从 ``sources.list`` 中移除 packages.ros.org。
如果你之前遵循的是 ROS 2 安装指南，只需删除 ``/etc/apt/sources.list.d/ros2.list``

目前，为了支持 ``ros1_bridge``，请按照下面的说明从源代码构建 ROS 2。

从源代码安装 ROS 2
------------------

在 Ubuntu Jammy 上，:doc:`从源代码安装 ROS 2 <../Installation/Alternatives/Ubuntu-Development-Setup>` 是唯一可行的 ROS 2 配置。

下面是源代码构建说明中必要步骤的摘要。
主要的差异在于，由于软件包冲突，我们跳过了使用 ROS 2 apt 仓库。

安装开发工具和 ROS 工具
^^^^^^^^^^^^^^^^^^^^^^^

由于我们不使用 ROS 2 apt 仓库，``colcon`` 必须通过 ``pip`` 安装。

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

   # Install colcon from PyPI, rather than apt packages
   python3 -m pip install -U colcon-common-extensions vcstool

接下来，请继续按照 :doc:`源代码安装指南 <../Installation/Alternatives/Ubuntu-Development-Setup>` 构建 ROS 2。

从 Ubuntu 软件包安装 ROS 1
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ sudo apt update && sudo apt install -y ros-core-dev


构建 ``ros1_bridge``
^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    $ mkdir -p ~/ros1_bridge/src # Create a workspace for the ros1_bridge
    $ cd ~/ros1_bridge/src
    $ git clone https://github.com/ros2/ros1_bridge
    $ cd ~/ros1_bridge
    $. ~/ros2_humble/install/local_setup.bash # Source the ROS 2 workspace
    $ colcon build # Build

构建完整个 ``ros1_bridge`` 后，`ros1_bridge 示例 <https://github.com/ros2/ros1_bridge#example-1-run-the-bridge-and-the-example-talker-and-listener>`__ 的其余部分应该能在你的新安装上正常工作

