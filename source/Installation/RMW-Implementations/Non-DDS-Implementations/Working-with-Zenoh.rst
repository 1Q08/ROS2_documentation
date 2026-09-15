Zenoh
=====

Zenoh 是一种开源通信协议和中间件，旨在促进在异构系统之间高效地分发数据。
它为高性能的发布/订阅和分布式查询提供了与位置无关的抽象。
另请参阅：https://zenoh.io/docs/getting-started/first-app/

前置条件
--------

已 :doc:`安装 rosdep <../../../Tutorials/Intermediate/Rosdep>`。

安装软件包
----------

RMW 实现 Zenoh 可以通过二进制包安装，推荐用于稳定的开发。

支持的 ROS 2 发行版（参见发行版分支）的二进制包可在各发行版对应的 Tier-1 平台上获取。
首先请按照此处的说明，确保你的系统已配置好以安装 ROS 2 二进制包。

然后使用以下命令安装 rmw_zenoh 二进制包

.. code-block:: bash

   sudo apt install ros-{DISTRO}-rmw-zenoh-cpp

从源码构建
----------

仅当需要最新特性时，才推荐从源码构建。

默认情况下，我们内置并编译带有 zenoh 特性子集的 ``zenoh-cpp``。
如有需要，可以覆盖 ``ZENOHC_CARGO_FLAGS`` CMake 参数以包含其他特性。
更多详情请参阅 `zenoh_cpp_vendor/CMakeLists.txt <https://github.com/ros2/rmw_zenoh/blob/{DISTRO}/zenoh_cpp_vendor/CMakeLists.txt>`__。

1. 克隆仓库

.. code-block:: bash

    mkdir ~/ws_rmw_zenoh/src -p && cd ~/ws_rmw_zenoh/src
    git clone https://github.com/ros2/rmw_zenoh.git -b {DISTRO}

1. 安装依赖项：

.. code-block:: bash

    cd ~/ws_rmw_zenoh
    rosdep install --from-paths src --ignore-src --rosdistro {DISTRO} -y

3. 使用 Colcon 构建工作空间：

.. code-block:: bash

    source /opt/ros/{DISTRO}/setup.bash
    colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release


切换到 rmw_zenoh_cpp
--------------------

通过指定环境变量，从其他 rmw 切换到 rmw_zenoh_cpp。

.. code-block:: bash

   export RMW_IMPLEMENTATION=rmw_zenoh_cpp

运行 talker 和 listener
-----------------------

现在运行 ``talker`` 和 ``listener`` 来测试 Zenoh。

启动 Zenoh 路由器

.. code-block:: bash

   # terminal 1
   source /opt/ros/{DISTRO}/setup.bash
   ros2 run rmw_zenoh_cpp rmw_zenohd

.. note:: 如果没有 Zenoh 路由器，节点将无法彼此发现，因为在节点的会话配置中默认禁用了多播发现。
    取而代之，节点会通过 Zenoh 路由器的 gossip 功能接收有关其他对等节点的发现信息。

.. code-block:: bash

   # terminal 2
   export RMW_IMPLEMENTATION=rmw_zenoh_cpp
   source /opt/ros/{DISTRO}/setup.bash
   ros2 run demo_nodes_cpp talker

.. code-block:: bash

   # terminal 3
   export RMW_IMPLEMENTATION=rmw_zenoh_cpp
   source /opt/ros/{DISTRO}/setup.bash
   ros2 run demo_nodes_cpp listener

.. note:: 在运行这些命令之前，请记得加载你的 ROS 2 安装脚本。

