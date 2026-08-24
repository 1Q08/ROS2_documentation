eProsima Fast DDS
=================

eProsima Fast DDS 是一个面向实时嵌入式架构和操作系统的完整开源 DDS 实现。
另请参见：https://www.eprosima.com/index.php/products-all/eprosima-fast-dds


先决条件
--------

请先 :doc:`安装 rosdep <../../../Tutorials/Intermediate/Rosdep>`。

安装软件包
----------

最简单的方法是从 ROS 2 apt 软件仓库进行安装。

.. code-block:: console

   $ sudo apt install ros-{DISTRO}-rmw-fastrtps-cpp

从源代码构建
------------

从源代码构建是另一种安装方式。

首先，在 ROS 2 工作空间的源代码目录中克隆 Fast DDS 和 rmw_fastrtps。

.. code-block:: console

   $ cd ros2_ws/src
   $ git clone https://github.com/ros2/rmw_fastrtps ros2/rmw_fastrtps -b {REPOS_FILE_BRANCH}
   $ git clone https://github.com/eProsima/Fast-DDS eProsima/fastrtps

然后，安装 Fast DDS 所需的软件包。

.. code-block:: console

   $ cd ..
   $ rosdep install --from src -i

最后，运行 colcon build。

.. code-block:: console

   $ colcon build --symlink-install

切换到 rmw_fastrtps
-------------------

可以通过指定环境变量来选择 eProsima Fast DDS RMW：

.. code-block:: console

   $ export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

另请参见：:doc:`使用多种 RMW 实现 <../../../How-To-Guides/Working-with-multiple-RMW-implementations>`

运行 talker 和 listener
-----------------------

现在运行 ``talker`` 和 ``listener`` 来测试 Fast DDS。

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp talker

.. code-block:: console

   $ source /opt/ros/{DISTRO}/setup.bash
   $ ros2 run demo_nodes_cpp listener
