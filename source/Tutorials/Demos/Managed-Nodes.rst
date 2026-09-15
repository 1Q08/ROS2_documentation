.. redirect-from::

    Managed-Nodes
    Tutorials/Managed-Nodes

管理节点生命周期 - 示例
=======================

节点的受管生命周期可以让你更好地控制 ROS 系统的状态。
本示例使用一对简单的 talker/listener 受管节点，展示如何实现并使用受管生命周期。
你可以通过该示例来理解并试验以这种方式管理节点。

**领域：ROS 框构 | 内容类型：示例 | 经验：专家**

.. contents:: 目录
   :depth: 2
   :local:

概述
----

ROS 2 引入了受管节点（managed node）的概念，也称为生命周期节点（lifecycle node）。
这些节点可用于确保在节点于各生命周期状态之间转换时，资源被正确地初始化、激活、停用和清理。
一个常见的使用场景是控制硬件的节点，其中摄像头、激光雷达、电机驱动器以及其他传感器和执行器必须以受控的顺序启动、配置和关闭。

使用生命周期节点有助于确保硬件仅在其就绪时才被初始化，并在关闭或错误恢复期间被安全释放。
以下软件包使你能够实现这些受管节点：`rclcpp_lifecycle <https://index.ros.org/p/rclcpp_lifecycle/>`__ （实现库）和 `lifecycle_msgs <https://index.ros.org/p/lifecycle_msgs/>`__ （接口定义）。

前提条件
--------

有关安装 ROS 2 的详细信息，请参阅 :doc:`安装说明 <../../Installation>`。

示例
----

获取示例
^^^^^^^^

有关如何运行该示例的信息见：`lifecycle_demo_launch.py <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/lifecycle_py/launch/lifecycle_demo_launch.py>`__

说明
^^^^

有关如何运行它以及其中发生了什么，更多信息请参阅：`lifecycle README <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/lifecycle/README.rst>`__

相关内容
--------

软件包/参考：

* `rclcpp_lifecycle <https://index.ros.org/p/rclcpp_lifecycle/>`_ （实现库）：包含生命周期实现原型的软件包。
* `lifecycle_msgs <https://index.ros.org/p/lifecycle_msgs/>`_ （接口定义）：包含一些与生命周期相关的消息和服务定义的软件包。
* `lifecycle <https://docs.ros.org/en/{DISTRO}/p/lifecycle/>`_ ：包含生命周期实现演示的软件包。
