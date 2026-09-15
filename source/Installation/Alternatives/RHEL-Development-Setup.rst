.. redirect-from::

  Installation/RHEL-Development-Setup

.. _rhel-latest:

RHEL（源码）
============

.. contents:: 目录
   :depth: 2
   :local:


系统要求
--------
当前 {DISTRO_TITLE_FULL} 的目标 Red Hat 平台为：

- Tier 2: RHEL 8 64-bit

如 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`_ 中所定义。

系统设置
--------

设置区域设置
^^^^^^^^^^^^

.. include:: ../_RHEL-Set-Locale.rst

启用所需仓库
^^^^^^^^^^^^

rosdep 数据库中包含来自 EPEL 和 PowerTools 仓库的软件包，而这两个仓库默认未启用。
可以通过运行以下命令启用它们：

.. code-block:: console

   $ sudo dnf install 'dnf-command(config-manager)' epel-release -y
   $ sudo dnf config-manager --set-enabled powertools

.. note:: 此步骤可能因你所使用的发行版而略有不同。
          请查看 `EPEL 文档 <https://docs.fedoraproject.org/en-US/epel/#_quickstart>`_


安装开发工具和 ROS 工具
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ sudo dnf install -y \
     cmake \
     gcc-c++ \
     git \
     make \
     patch \
     python3-colcon-common-extensions \
     python3-pip \
     python3-pydocstyle \
     python3-pytest \
     python3-pytest-repeat \
     python3-pytest-rerunfailures \
     python3-rosdep \
     python3-setuptools \
     python3-vcstool

   ~ install some pip packages needed for testing and
   ~ not available as RPMs
   $ python3 -m pip install -U --user \
     flake8-blind-except==0.1.1 \
     flake8-builtins \
     flake8-class-newline \
     flake8-comprehensions \
     flake8-deprecated \
     flake8-docstrings \
     flake8-import-order==0.18.2 \
     flake8-quotes \
     mypy==0.931

.. _rhel-dev-get-ros2-code:

获取 ROS 2 代码
---------------

创建一个工作空间并克隆所有仓库：

.. code-block:: console

   $ mkdir -p ~/ros2_{DISTRO}/src
   $ cd ~/ros2_{DISTRO}
   $ vcs import --input https://raw.githubusercontent.com/ros2/ros2/{REPOS_FILE_BRANCH}/ros2.repos src

.. _rhel-development-setup-install-dependencies-using-rosdep:

使用 rosdep 安装依赖项
----------------------

.. include:: ../_Dnf-Update-Admonition.rst

.. code-block:: console

   $ sudo rosdep init
   $ rosdep update
   $ rosdep install --from-paths src --ignore-src -y --skip-keys "asio cyclonedds fastcdr fastrtps ignition-cmake2 ignition-math6 python3-babeltrace python3-mypy rti-connext-dds-6.0.1 urdfdom_headers"

安装额外 DDS 实现（可选）
-------------------------

如果你想使用除默认外的其他 DDS 或 RTPS 厂商，可以在此处找到说明：:doc:`这里 <../RMW-Implementations>`。

在工作空间中构建代码
--------------------

如果你已经用其他方式安装了 ROS 2（无论是通过 RPM 还是二进制发布版），请确保在一个未加载那些其他安装的全新环境中运行下面的命令。
同时确保你的 ``.bashrc`` 中没有 ``source /opt/ros/${ROS_DISTRO}/setup.bash``。
你可以用命令 ``printenv | grep -i ROS`` 来确认 ROS 2 没有被加载。
输出应该为空。

关于使用 ROS 工作空间的更多信息，可以在 :doc:`本教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>` 中找到。

.. code-block:: console

   $ cd ~/ros2_{DISTRO}/
   $ colcon build --symlink-install --cmake-args -DTHIRDPARTY_Asio=ON -DPython3_EXECUTABLE=/usr/bin/python3 --no-warn-unused-cli

注意：如果你在编译所有示例时遇到困难，导致无法成功完成构建，你可以像 `CATKIN_IGNORE <https://github.com/ros-infrastructure/rep/blob/master/rep-0128.rst>`__ 那样使用 ``COLCON_IGNORE`` 来忽略某个子目录树，或者将该文件夹从工作空间中移除。
举例来说：假设你想避免安装庞大的 OpenCV 库。
那么只需在 ``cam2image`` 演示目录中运行 ``touch COLCON_IGNORE``，即可将它排除在构建过程之外。

环境配置
--------

加载安装脚本
^^^^^^^^^^^^

通过加载以下文件来配置你的环境。

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/local_setup.bash

.. note::

   如果你不使用 bash，请将 ``.bash`` 替换为你所用的 shell。
   可选值包括：``setup.bash``、``setup.sh``、``setup.zsh``。

.. _rhel_talker-listener:

尝试一些示例
------------

在一个终端中，加载安装脚本，然后运行 C++ 的 ``talker``\ ：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/local_setup.bash
   $ ros2 run demo_nodes_cpp talker

在另一个终端中加载安装脚本，然后运行 Python 的 ``listener``\ ：

.. code-block:: console

   $ . ~/ros2_{DISTRO}/install/local_setup.bash
   $ ros2 run demo_nodes_py listener

你应该会看到 ``talker`` 输出 ``Publishing`` 消息，而 ``listener`` 输出 ``I heard`` 这些消息。
这验证了 C++ 和 Python API 都能正常工作。
太棒了！

安装后的后续步骤
----------------
继续学习 :doc:`教程和演示 <../../Tutorials>`，以配置你的环境、创建自己的工作空间和软件包，并了解 ROS 2 的核心概念。

其他 RMW 实现（可选）
---------------------
ROS 2 使用的默认中间件是 ``Fast DDS``，但中间件（RMW）可以在运行时替换。
请参阅关于如何使用多个 RMW 的 :doc:`指南 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

替代编译器
----------

除 gcc 之外，使用其他编译器来编译 ROS 2 也很简单。
如果你将环境变量 ``CC`` 和 ``CXX`` 分别设置为可正常工作的 C 和 C++ 编译器的可执行文件，然后重新触发 CMake 配置（通过使用 ``--force-cmake-config``，或删除你希望受影响的软件包），CMake 就会重新配置并使用不同的编译器。

Clang
^^^^^

要配置 CMake 检测并使用 Clang：

.. code-block:: console

   $ sudo dnf install clang
   $ export CC=clang
   $ export CXX=clang++
   $ colcon build --cmake-force-configure

保持最新
--------

请参阅 :doc:`../Maintaining-a-Source-Checkout`，以定期刷新你的源码安装。

故障排查
--------

故障排查技巧请参见 :ref:`这里 <linux-troubleshooting>`。

卸载
----

1. 如果你按上述方式使用 colcon 安装了工作空间，所谓“卸载”可能只需打开一个新终端，并且不加载该工作空间的 ``setup`` 文件。
   这样，你的环境就会表现得如同系统中根本没安装过 {DISTRO_TITLE} 一样。

2. 如果你还想释放空间，可以用以下命令删除整个工作空间目录：

   .. code-block:: console

     $ rm -rf ~/ros2_{DISTRO}
