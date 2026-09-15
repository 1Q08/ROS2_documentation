.. redirect-from::

   Working-with-GurumNetworks-GurumDDS

GurumNetworks GurumDDS
======================
``rmw_gurumdds`` 是使用 GurumNetworks GurumDDS 实现的 ROS 中间件接口。
有关 GurumDDS 的更多信息，请访问 `GurumNetworks 官网 <https://gurum.cc/index_eng>`_。


前置条件
--------
本指南假定你已经完成了 ROS 2 环境配置流程，方式可以是 :doc:`通过 Deb 软件包安装 ROS 2 <../../Ubuntu-Install-Debs>` 或 :doc:`在 Ubuntu 上从源码构建 ROS 2 <../../Alternatives/Ubuntu-Development-Setup>`。

版本要求（`详情参见 README <https://github.com/ros2/rmw_gurumdds>`_）：

================  ================
ROS 2 发行版       GurumDDS 版本
================  ================
rolling           ``>= 3.2.0``
lyrical           ``>= 3.2.0``
kilted            ``>= 3.2.0``
jazzy             ``>= 3.2.0``
humble            ``3.1.x``
================  ================

Ubuntu 上的 ROS 2 apt 仓库提供了 GurumDDS 的 Deb 软件包。
GurumDDS 的 Windows 二进制安装程序即将推出。

你可以从 `GurumDDS 免费试用页面 <https://gurum.cc/free_trial_eng.html>`_ 获取免费试用许可证。

获取许可证后，请将其放置在以下位置：``/etc/gurumnet``


安装
----
选项 1：从 ROS 2 apt 仓库安装（推荐）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-rmw-gurumdds-cpp

这会同时安装 ``rmw_gurumdds_cpp`` 和 ``gurumdds``。

选项 2：从源码构建
^^^^^^^^^^^^^^^^^^
1. 克隆仓库

.. code-block:: console

   $ cd ros2_ws/src
   $ git clone https://github.com/ros2/rmw_gurumdds -b {DISTRO} ros2/rmw_gurumdds

2. 安装依赖：

.. code-block:: console

   $ cd ..
   $ rosdep install --from src -i --rosdistro {DISTRO}

3. 使用 Colcon 构建工作空间：

.. code-block:: console

   $ colcon build --symlink-install


切换到 rmw_gurumdds
-------------------
通过设置环境变量，从其他 RMW 实现切换到 rmw_gurumdds：

.. code-block:: console

   $ export RMW_IMPLEMENTATION=rmw_gurumdds_cpp

有关使用多个 RMW 实现的更多信息，请参见 :doc:`使用多个 RMW 实现 <../../../How-To-Guides/Working-with-multiple-RMW-implementations>`。

测试安装
--------
运行 ``talker`` 和 ``listener`` 节点以验证你的安装：

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp talker

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp listener

如果节点之间通信成功，说明你的安装工作正常。

.. note:: 运行这些命令前，请记得加载你的 ROS 2 安装脚本。
