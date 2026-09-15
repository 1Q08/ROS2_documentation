.. redirect-from::

    Working-with-Eclipse-CycloneDDS

Eclipse Cyclone DDS
===================

Eclipse Cyclone DDS 是一个性能非常高且健壮的开源 DDS 实现。
Cyclone DDS 作为 Eclipse IoT 项目完全公开开发。
另请参阅：https://projects.eclipse.org/projects/iot.cyclonedds


前置条件
--------

已 :doc:`安装 rosdep <../../../Tutorials/Intermediate/Rosdep>`。

安装软件包
----------

最简单的方式是从 ROS 2 apt 仓库安装。

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-rmw-cyclonedds-cpp

从源码构建
----------

从源码构建也是另一种安装方式。

首先，在 ROS 2 工作空间的源码目录中克隆 Cyclone DDS 和 rmw_cyclonedds。
为了确定要检出的正确分支，你需要查看你的 `ROS 发行版的 ros2.repos 文件 <https://raw.githubusercontent.com/ros2/ros2/refs/heads/{DISTRO}/ros2.repos>`_ 中指定了哪些版本。

或者，你可以运行以下代码来获取 Cyclone DDS 所需的正确分支/标签：

.. code-block:: console

   $ CYCLONEDDS_BRANCH=$(curl -s https://raw.githubusercontent.com/ros2/ros2/refs/heads/{DISTRO}/ros2.repos | grep -A 3 "eclipse-cyclonedds/cyclonedds:" | grep "version:" | awk '{print $2}')

现在，克隆并检出代码：

.. code-block:: console

   $ cd ros2_ws/src
   $ git clone https://github.com/ros2/rmw_cyclonedds ros2/rmw_cyclonedds -b {DISTRO}
   $ git clone https://github.com/eclipse-cyclonedds/cyclonedds eclipse-cyclonedds/cyclonedds -b ${CYCLONEDDS_BRANCH}

然后，安装 Cyclone DDS 所需的软件包。

.. code-block:: console

   $ cd ..
   $ rosdep install --from src -i

最后，运行 colcon build。

.. code-block:: console

   $ colcon build --symlink-install

切换到 rmw_cyclonedds
---------------------

通过指定环境变量，从其他 rmw 切换到 rmw_cyclonedds。

.. code-block:: console

   $ export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

另请参阅：:doc:`使用多个 RMW 实现 <../../../How-To-Guides/Working-with-multiple-RMW-implementations>`

运行 talker 和 listener
-----------------------

现在运行 ``talker`` 和 ``listener`` 来测试 Cyclone DDS。

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp talker

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp listener
