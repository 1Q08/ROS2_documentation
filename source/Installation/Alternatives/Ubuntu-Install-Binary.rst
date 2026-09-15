.. redirect-from::

   Installation/Linux-Install-Binary

Ubuntu（二进制）
================

.. contents:: 目录
   :depth: 2
   :local:

本文说明如何在 Ubuntu Linux 上从预构建二进制包安装 ROS 2。

.. note::

    预构建二进制包不包含所有 ROS 2 软件包。
    它包含 `ROS base 变体 <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中的所有软件包，但只包含 `ROS desktop 变体 <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中的一部分软件包。
    确切的软件包列表由 `此 ros2.repos 文件 <https://github.com/ros2/ros2/blob/{REPOS_FILE_BRANCH}/ros2.repos>`_ 中列出的仓库描述。

此外还有 :doc:`deb 软件包 <../Ubuntu-Install-Debs>` 可用。

系统要求
--------

当前支持 Ubuntu Linux Jammy（22.04）64 位 x86 与 64 位 ARM。

添加 ROS 2 apt 仓库
-------------------

.. include:: ../_Apt-Repositories.rst

下载 ROS 2
----------

* 前往 `releases 页面 <https://github.com/ros2/ros2/releases>`_
* 下载适用于 Ubuntu 的最新软件包；假设它最终位于 ``~/Downloads/ros2-package-linux-x86_64.tar.bz2``。

  * 注意：可能存在多个二进制下载选项，这会导致文件名有所不同。

*
  解压它：

  .. code-block:: console

       $ mkdir -p ~/ros2_{DISTRO}
       $ cd ~/ros2_{DISTRO}
       $ tar xf ~/Downloads/ros2-package-linux-x86_64.tar.bz2

安装并初始化 rosdep
-------------------

.. code-block:: console

       $ sudo apt update
       $ sudo apt install -y python3-rosdep
       $ sudo rosdep init
       $ rosdep update

.. _linux-install-binary-install-missing-dependencies:

安装缺失的依赖项
----------------

.. include:: ../_Apt-Upgrade-Admonition.rst

请根据你下载的发行版设置你的 rosdistro。

.. code-block:: bash

       rosdep install --from-paths ~/ros2_{DISTRO}/ros2-linux/share --ignore-src -y --skip-keys "cyclonedds fastcdr fastrtps rti-connext-dds-6.0.1 urdfdom_headers"

.. include:: ../_rosdep_Linux_Mint.rst

安装开发工具（可选）
^^^^^^^^^^^^^^^^^^^^

如果你打算构建 ROS 软件包或进行其他开发工作，也可以安装开发工具：

.. code-block:: bash

       sudo apt install ros-dev-tools

安装额外 DDS 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^

如果你想使用除默认外的其他 DDS 或 RTPS 厂商，可以在此处找到说明：:doc:`这里 <../RMW-Implementations>`。

环境配置
--------

加载安装脚本
^^^^^^^^^^^^

通过加载以下文件来配置你的环境。

.. code-block:: console

   $ . ~/ros2_{DISTRO}/ros2-linux/setup.bash

.. note::

   如果你不使用 bash，请将 ``.bash`` 替换为你所用的 shell。
   可选值包括：``setup.bash``、``setup.sh``、``setup.zsh``。

尝试一些示例
------------

在一个终端中，加载安装脚本，然后运行 C++ 的 ``talker``：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/ros2-linux/setup.bash
   $ ros2 run demo_nodes_cpp talker

在另一个终端中加载安装脚本，然后运行 Python 的 ``listener``：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/ros2-linux/setup.bash
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 输出 ``Publishing`` 消息，而 ``listener`` 输出 ``I heard`` 这些消息。
这验证了 C++ 和 Python API 都能正常工作。
太棒了！

安装后的后续步骤
----------------
继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并了解 ROS 2 的核心概念。

使用 ROS 1 桥接
---------------
ROS 1 桥接可以将话题从 ROS 1 连接到 ROS 2，反之亦然。
请参阅关于如何构建和使用 ROS 1 桥接的专门 `文档 <https://github.com/ros2/ros1_bridge/blob/master/README.md>`__。

其他 RMW 实现（可选）
---------------------
ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
请参阅关于如何使用多个 RMW 的 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

故障排查
--------

故障排查技巧可以在 :doc:`这里 <../../How-To-Guides/Installation-Troubleshooting>` 找到。

卸载
----

1. 如果你按上面的说明使用 colcon 安装工作空间，那么“卸载”可能只需打开一个新终端，并且不要加载该工作空间的 ``setup`` 文件。
   这样，你的环境就会表现得如同系统中没有安装 {DISTRO_TITLE}。

2. 如果你还想释放空间，可以用以下命令删除整个工作空间目录：

   .. code-block:: console

      $ rm -rf ~/ros2_{DISTRO}
