.. redirect-from::

   Guides/Parameters-YAML-files-migration-guide
   Tutorials/Parameters-YAML-files-migration-guide
   How-To-Guides/Parameters-YAML-files-migration-guide

迁移参数
========

.. contents:: 目录
   :depth: 2
   :local:

在 ROS 1 中，参数与一个中心服务器相关联，可以通过网络 API 在运行时获取参数。
在 ROS 2 中，参数与每个节点相关联，并可通过 ROS 服务在运行时进行配置。

* 关于系统模型的更多细节，请参阅 `ROS 2 参数设计文档 <https://design.ros2.org/articles/ros_parameters.html>`_。

* 关于命令行工具的工作方式及其与 ROS 1 工具的区别，请参阅 :doc:`ROS 2 命令行用法 <../../Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters>`。

全局参数服务器
--------------

在 ROS 1 中，``roscore`` 类似于一块全局参数黑板，所有节点都可以在上面获取和设置参数。
由于 ROS 2 中不再有中心的 ``roscore``，该功能已不复存在。
ROS 2 中推荐的做法是使用与使用它们的节点紧密绑定的按节点参数。
如果仍然需要一块全局黑板，可以为此创建一个专用节点。
ROS 2 在 ``ros-{DISTRO}-demo-nodes-cpp`` 软件包中自带一个名为 ``parameter_blackboard`` 的节点，可以用以下命令运行：

.. code-block:: console

   $ ros2 run demo_nodes_cpp parameter_blackboard

``parameter_blackboard`` 的代码在 `这里 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/parameters/parameter_blackboard.cpp>`__。

迁移 YAML 参数文件
------------------

本指南介绍如何为 ROS 2 调整 ROS 1 的参数文件。

YAML 文件示例
^^^^^^^^^^^^^

ROS 1 和 ROS 2 都使用 YAML 编写参数文件。
ROS 2 中的主要区别在于必须使用节点名称来寻址参数。
除了完全限定的节点名称之外，我们还使用键 "ros__parameters" 来标示节点参数的开始。


例如，下面是一个 ROS 1 的参数文件：

.. code-block:: yaml

   lidar_name: foo
   lidar_id: 10
   ports: [11312, 11311, 21311]
   debug: true

假设前两个参数属于名为 ``/lidar_ns/lidar_node_name`` 的节点，下一个参数属于名为 ``/imu`` 的节点，而最后一个参数我们希望在两个节点上都设置。

我们构建的 ROS 2 参数文件如下：

.. code-block:: yaml

   /lidar_ns:
     lidar_node_name:
       ros__parameters:
         lidar_name: foo
         id: 10
   imu:
     ros__parameters:
       ports: [2438, 2439, 2440]
   /**:
     ros__parameters:
       debug: true

注意这里使用了通配符（``/**``），表示参数 ``debug`` 应在任意命名空间中的任意节点上设置。

功能对等性
^^^^^^^^^^

ROS 1 参数文件的一些功能在 ROS 2 中并不存在：

- 尚不支持列表中的混合类型（`相关 issue <https://github.com/ros2/rcl/issues/463>`_）
- 不支持 ``deg`` 和 ``rad`` 替换


参数原子操作
------------

在把参数组从 ROS 1 迁移到 ROS 2 时，有一些重要差异需要考虑。
在 ROS 1 中，``dynamic_reconfigure`` 以原子方式处理参数组，也就是说一次重配置请求中的所有参数会在单个回调中一起处理。
在 ROS 2 中，``set_parameters`` 服务会逐个处理每个参数，这可能导致多次回调调用。
为了在从 ``dynamic_reconfigure`` 迁移时保持原子行为，请使用 ``set_parameters_atomically`` 服务，它会把所有参数作为单个操作进行校验并应用。
如果任何参数校验失败，则不会更新任何参数。
