.. redirect-from::

   Guides/Parameters-YAML-files-migration-guide
   Tutorials/Parameters-YAML-files-migration-guide
   How-To-Guides/Parameters-YAML-files-migration-guide

迁移参数
========

.. contents:: 目录
   :depth: 2
   :local:

在 ROS 1 中，参数与一个中央服务器相关联，
该服务器允许在运行时通过网络 API 检索参数。
在 ROS 2 中，参数按节点关联，并且可以在运行时通过 ROS 服务进行配置。

* 有关系统模型的更多详细信息，请参见
  `ROS 2 参数设计文档 <https://design.ros2.org/articles/ros_parameters.html>`_。

* 参见 :doc:`ROS 2 CLI 用法 <../../Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters>`，
  以更好地理解 CLI 工具的工作方式及其与 ROS 1 工具的差异。

全局参数服务器
--------------

在 ROS 1 中，``roscore`` 就像一个全局参数黑板，
所有节点都可以在其中获取和设置参数。
由于 ROS 2 中没有中央 ``roscore``，因此该功能不再存在。
ROS 2 中推荐的方法是使用与使用它们的节点紧密关联的逐节点参数。
如果仍然需要全局黑板，可以为此创建一个专用节点。
ROS 2 在 ``ros-{DISTRO}-demo-nodes-cpp`` 包中附带了一个名为
``parameter_blackboard`` 的节点；它可以通过以下命令运行：

.. code-block:: console

   $ ros2 run demo_nodes_cpp parameter_blackboard

``parameter_blackboard`` 的代码位于
`此处 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/parameters/parameter_blackboard.cpp>`__。

迁移 YAML 参数文件
------------------

本指南介绍如何为 ROS 2 改编 ROS 1 参数文件。

YAML 文件示例
^^^^^^^^^^^^^

在 ROS 1 和 ROS 2 中，YAML 都被用来编写参数文件。
ROS 2 中的主要区别在于，必须使用节点名称来寻址参数。
除了完全限定的节点名称之外，我们还使用键 "ros__parameters"
来标记该节点参数的开始。

例如，下面是一个 ROS 1 参数文件：

.. code-block:: yaml

   lidar_name: foo
   lidar_id: 10
   ports: [11312, 11311, 21311]
   debug: true

让我们假设前两个参数用于名为 ``/lidar_ns/lidar_node_name`` 的节点，
下一个参数用于名为 ``/imu`` 的节点，
最后一个参数我们希望同时设置在两个节点上。

我们将如下构造 ROS 2 参数文件：

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

请注意使用通配符（``/**``）来指示参数 ``debug``
应该被设置在任何命名空间中的任何节点上。

功能对等
^^^^^^^^

ROS 1 参数文件的某些功能在 ROS 2 中不存在：

- 尚不支持列表中的混合类型（`相关问题 <https://github.com/ros2/rcl/issues/463>`_）
- 不支持 ``deg`` 和 ``rad`` 替换

参数原子操作
------------

将参数组从 ROS 1 迁移到 ROS 2 时，有一些重要的差异需要考虑。
在 ROS 1 中，``dynamic_reconfigure`` 以原子方式处理参数组，
这意味着重配置请求中的所有参数都在单个回调中一起处理。
在 ROS 2 中，``set_parameters`` 服务逐个处理每个参数，
这可能导致多次回调调用。
在从 ``dynamic_reconfigure`` 迁移时，为了保持原子行为，
请使用 ``set_parameters_atomically`` 服务，
它将所有参数作为单个操作进行验证和应用。
如果任何参数验证失败，则不会更新任何参数。
