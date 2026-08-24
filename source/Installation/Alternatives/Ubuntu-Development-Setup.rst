.. redirect-from::

   Installation/Linux-Development-Setup
   Installation/Ubuntu-Development-Setup

Ubuntu（源代码）
================

.. contents:: 目录
   :depth: 2
   :local:


系统要求
--------
{DISTRO_TITLE_FULL} 当前基于 Debian 的目标平台为：

- 一级：Ubuntu Linux - Noble (24.04) 64 位
- 三级：Ubuntu Linux - Jammy (22.04) 64 位
- 三级：Debian Linux - Bookworm (12) 64 位

如 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`_ 中所定义。

系统设置
--------

设置语言环境
^^^^^^^^^^^^

.. include:: ../_Ubuntu-Set-Locale.rst

启用所需软件仓库
^^^^^^^^^^^^^^^^

.. include:: ../_Apt-Repositories.rst

安装开发工具
^^^^^^^^^^^^

.. code-block:: console

   $ sudo apt update && sudo apt install -y \
     python3-flake8-blind-except \
     python3-flake8-class-newline \
     python3-flake8-deprecated \
     python3-mypy \
     python3-pip \
     python3-pytest \
     python3-pytest-cov \
     python3-pytest-mock \
     python3-pytest-repeat \
     python3-pytest-rerunfailures \
     python3-pytest-runner \
     python3-pytest-timeout \
     ros-dev-tools

构建 ROS 2
----------

获取 ROS 2 代码
^^^^^^^^^^^^^^^

创建工作空间并克隆所有仓库：

.. code-block:: console

   $ mkdir -p ~/ros2_{DISTRO}/src
   $ cd ~/ros2_{DISTRO}
   $ vcs import --input https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos src

.. _linux-development-setup-install-dependencies-using-rosdep:

使用 rosdep 安装依赖项
^^^^^^^^^^^^^^^^^^^^^^

.. include:: ../_Apt-Upgrade-Admonition.rst

.. code-block:: console

   $ sudo rosdep init
   $ rosdep update
   $ rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers"

.. include:: ../_rosdep_Linux_Mint.rst

安装额外的 RMW 实现（可选）
^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在构建时或运行时替换。
关于如何使用多种 RMW，请参见 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

安装 colcon mixins
^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ colcon mixin add default https://github.com/colcon/colcon-mixin-repository/raw/master/index.yaml
   $ colcon mixin update default

构建工作空间中的代码
^^^^^^^^^^^^^^^^^^^^

如果你已经通过其他方式安装了 ROS 2（无论是通过 deb 还是二进制发行版），请确保在一个没有 source 这些其他安装的全新环境中运行以下命令。
还要确保你的 ``.bashrc`` 中没有 ``source /opt/ros/${ROS_DISTRO}/setup.bash``。
你可以使用命令 ``printenv | grep -i ROS`` 来确认 ROS 2 没有被 source。
输出应为空。

关于使用 ROS 工作空间的更多信息，请参见 :doc:`本教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>`。

.. code-block:: console

   $ cd ~/ros2_{DISTRO}/
   $ colcon build --symlink-install --mixin release

.. note::

   如果你在编译所有示例时遇到问题，并且这阻碍了你完成成功构建，你可以使用 ``--packages-skip`` colcon 标志来忽略导致问题的软件包。
   例如，如果你不想安装庞大的 OpenCV 库，可以使用以下命令跳过构建依赖它的软件包：

   .. code-block:: console

      $ colcon build --symlink-install --packages-skip image_tools intra_process_demo

设置环境
--------

通过 source 以下文件来设置你的环境。

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/local_setup.bash

.. note::

   如果你不使用 bash，请将 ``.bash`` 替换为你的 shell。
   可选值为：``setup.bash``、``setup.sh``、``setup.zsh``。

.. _talker-listener:

尝试一些示例
------------

在一个终端中，source 设置文件，然后运行一个 C++ ``talker``\ ：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/local_setup.bash
   $ ros2 run demo_nodes_cpp talker

在另一个终端中 source 设置文件，然后运行一个 Python ``listener``\ ：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/local_setup.bash
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 显示它正在 ``Publishing`` 消息，而 ``listener`` 显示 ``I heard`` 那些消息。
这验证了 C++ 和 Python API 都正常工作。
太棒了！

后续步骤
--------

继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并学习 ROS 2 核心概念。

替代编译器
----------

使用 gcc 以外的其他编译器来编译 ROS 2 是很容易的。
如果你分别将环境变量 ``CC`` 和 ``CXX`` 设置为可用的 C 和 C++ 编译器的可执行文件，并重新触发 CMake 配置（通过使用 ``--cmake-force-configure`` 或删除你希望受影响的软件包），CMake 将重新配置并使用不同的编译器。

Clang
^^^^^

要配置 CMake 以检测并使用 Clang：

.. code-block:: console

   $ sudo apt install clang
   $ export CC=clang
   $ export CXX=clang++
   $ colcon build --cmake-force-configure

保持最新
--------

参见 :doc:`../Maintaining-a-Source-Checkout` 以定期刷新你的源代码安装。

故障排查
--------

故障排查技巧可参见 :ref:`此处 <linux-troubleshooting>`。

卸载
----

1. 如果你按照上述说明使用 colcon 安装了工作空间，那么"卸载"可能只是打开一个新终端并且不 source 工作空间的 ``setup`` 文件即可。
   这样，你的环境将表现得就像系统中没有安装 {DISTRO_TITLE} 一样。

2. 如果你还想释放空间，可以删除整个工作空间目录：

   .. code-block:: console

      $ rm -rf ~/ros2_{DISTRO}
