.. redirect-from::

   Installation/Linux-Install-Binary

Ubuntu（二进制）
================

.. contents:: 目录
   :depth: 2
   :local:

本页介绍如何从预构建的二进制软件包在 Ubuntu Linux 上安装 ROS 2。

.. note::

    预构建的二进制文件不包含所有 ROS 2 软件包。
    包含 `ROS base 变体 <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中的所有软件包，但只包含 `ROS desktop 变体 <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中的一部分软件包。
    软件包的确切列表由 `这个 ros2.repos 文件 <https://github.com/ros2/ros2/blob/{REPOS_FILE_BRANCH}/ros2.repos>`_ 中列出的仓库描述。

也提供 :doc:`deb 软件包 <../Ubuntu-Install-Debs>`。

系统要求
--------

我们目前支持 Ubuntu Noble (24.04) 的 64 位 x86 和 64 位 ARM。

系统设置
--------

设置语言环境
^^^^^^^^^^^^

.. include:: ../_Ubuntu-Set-Locale.rst

启用所需软件仓库
^^^^^^^^^^^^^^^^

.. include:: ../_Apt-Repositories.rst

安装前置条件
^^^^^^^^^^^^

为了获取并解压二进制发行版，必须安装几个软件包。

.. code-block:: console

   $ sudo apt install tar bzip2 wget -y

安装开发工具（可选）
^^^^^^^^^^^^^^^^^^^^

如果你要构建 ROS 软件包或进行其他开发工作，你还可以安装开发工具：

.. code-block:: console

   $ sudo apt update && sudo apt install ros-dev-tools

安装 ROS 2
----------

* 前往 `发布页面 <https://github.com/ros2/ros2/releases>`_
* 下载适用于 Ubuntu 的最新软件包；我们假设它最终位于 ``~/Downloads/ros2-package-linux-x86_64.tar.bz2``。

  * 注意：可能有多个二进制下载选项，这可能会导致文件名不同。

*
  解压它：

  .. code-block:: console

     $ mkdir -p ~/ros2_{DISTRO}
     $ cd ~/ros2_{DISTRO}
     $ tar xf ~/Downloads/ros2-package-linux-x86_64.tar.bz2

.. _linux-install-binary-install-missing-dependencies:

使用 rosdep 安装依赖项
^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../_Apt-Upgrade-Admonition.rst

.. code-block:: console

   $ sudo apt update
   $ sudo apt install -y python3-rosdep
   $ sudo rosdep init
   $ rosdep update
   $ rosdep install --from-paths ~/ros2_{DISTRO}/ros2-linux/share --ignore-src -y --skip-keys "cyclonedds fastcdr fastrtps iceoryx_binding_c rmw_connextdds rti-connext-dds-6.0.1 urdfdom_headers"

.. include:: ../_rosdep_Linux_Mint.rst

安装额外的 RMW 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
关于如何使用多种 RMW，请参见 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

设置环境
--------

通过 source 以下文件来设置你的环境。

.. code-block:: console

   $ . ~/ros2_{DISTRO}/ros2-linux/setup.bash

.. note::

   如果你不使用 bash，请将 ``.bash`` 替换为你的 shell。
   可选值为：``setup.bash``、``setup.sh``、``setup.zsh``。

尝试一些示例
------------

在一个终端中，source 设置文件，然后运行一个 C++ ``talker``：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/ros2-linux/setup.bash
   $ ros2 run demo_nodes_cpp talker

在另一个终端中 source 设置文件，然后运行一个 Python ``listener``：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/ros2-linux/setup.bash
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 显示它正在 ``Publishing`` 消息，而 ``listener`` 显示 ``I heard`` 那些消息。
这验证了 C++ 和 Python API 都正常工作。
太棒了！

后续步骤
--------

继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并学习 ROS 2 核心概念。

故障排查
--------

故障排查技巧可参见 :doc:`此处 <../../How-To-Guides/Installation-Troubleshooting>`。

卸载
----

1. 如果你按照上述说明使用 colcon 安装了工作空间，那么"卸载"可能只是打开一个新终端并且不 source 工作空间的 ``setup`` 文件即可。
   这样，你的环境将表现得就像系统中没有安装 {DISTRO_TITLE} 一样。

2. 如果你还想释放空间，可以删除整个工作空间目录：

   .. code-block:: console

      $ rm -rf ~/ros2_{DISTRO}
