.. redirect-from::

    Tutorials/Understanding-ROS2-Nodes

.. _ROS2Nodes:

理解节点
========

**目标：** 了解节点在 ROS 2 中的作用，以及与它们交互的工具。

**教程级别：** 入门

**用时：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

1 ROS 2 图
^^^^^^^^^^

在接下来的几个教程中，你将学习一系列核心的 ROS 2 概念，它们共同构成了所谓的“ROS（2）图”。

ROS 图是一个由 ROS 2 元素组成的网络，这些元素在同一时间共同处理数据。
如果你将它们全部绘制出来并可视化，它会涵盖所有可执行程序以及它们之间的连接。

2 ROS 2 中的节点
^^^^^^^^^^^^^^^^

ROS 中的每个节点应当只负责一个单一的、模块化的用途，例如控制车轮电机或发布来自激光测距仪的传感器数据。
每个节点都可以通过话题、服务、动作或参数与其他节点收发数据。

.. image:: images/Nodes-TopicandService.gif

一个完整的机器人系统由许多协同工作的节点组成。
在 ROS 2 中，一个可执行程序（C++ 程序、Python 程序等）可以包含一个或多个节点。

前置条件
--------

:doc:`上一篇教程 <../Introducing-Turtlesim/Introducing-Turtlesim>` 向你展示了如何安装这里用到的 ``turtlesim`` 包。

和往常一样，别忘了在 :doc:`每一个你新打开的终端 <../Configuring-ROS2-Environment>` 中 source ROS 2。

任务
----

1 ros2 run
^^^^^^^^^^

命令 ``ros2 run`` 从包中启动一个可执行程序。

.. code-block:: console

  $ ros2 run <package_name> <executable_name>

要运行 turtlesim，请打开一个新终端，并输入以下命令：

.. code-block:: console

  $ ros2 run turtlesim turtlesim_node

turtlesim 窗口将会打开，正如你在 :doc:`上一篇教程 <../Introducing-Turtlesim/Introducing-Turtlesim>` 中看到的那样。

这里，包名是 ``turtlesim``，可执行程序名是 ``turtlesim_node``。

不过，我们还不知道节点名。
你可以使用 ``ros2 node list`` 找到节点名。

2 ros2 node list
^^^^^^^^^^^^^^^^

``ros2 node list`` 会显示所有正在运行的节点的名称。
当你想要与某个节点交互，或者当你运行着一个包含许多节点的系统并需要跟踪它们时，这一点尤其有用。

在 turtlesim 仍在另一个终端中运行的情况下打开一个新终端，并输入以下命令。
终端会返回节点名：

.. code-block:: console

  $ ros2 node list
  /turtlesim

再打开一个新终端，并用以下命令启动 teleop 节点：

.. code-block:: console

  $ ros2 run turtlesim turtle_teleop_key

这里，我们再次引用了 ``turtlesim`` 包，但这次我们指定的是名为 ``turtle_teleop_key`` 的可执行程序。

回到你运行 ``ros2 node list`` 的终端，再次运行它。
现在你将看到两个活动节点的名称：

.. code-block:: console

  $ ros2 node list
  /turtlesim
  /teleop_turtle

2.1 重映射
~~~~~~~~~~

`重映射（Remapping） <https://design.ros2.org/articles/ros_command_line_arguments.html#name-remapping-rules>`__ 允许你将节点的默认属性（如节点名、话题名、服务名等）重新赋值为自定义值。
在上一篇教程中，你对 ``turtle_teleop_key`` 使用了重映射，以更改 cmd_vel 话题并让 **turtle2** 成为目标。

现在，让我们重新指定 ``/turtlesim`` 节点的名称。
在一个新终端中，运行以下命令：

.. code-block:: console

  $ ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle

由于你再次对 turtlesim 调用了 ``ros2 run``，另一个 turtlesim 窗口将会打开。
然而，现在如果你回到运行 ``ros2 node list`` 的终端并再次运行它，你将看到三个节点名：

.. code-block:: console

    /my_turtle
    /turtlesim
    /teleop_turtle

3 ros2 node info
^^^^^^^^^^^^^^^^

既然你已经知道了节点的名称，你可以通过以下命令获取有关它们的更多信息：

.. code-block:: console

  $ ros2 node info <node_name>

要检查你最新的节点 ``my_turtle``，请运行以下命令：

.. code-block:: console

  $ ros2 node info /my_turtle
  /my_turtle
    Subscribers:
      /parameter_events: rcl_interfaces/msg/ParameterEvent
      /turtle1/cmd_vel: geometry_msgs/msg/Twist
    Publishers:
      /parameter_events: rcl_interfaces/msg/ParameterEvent
      /rosout: rcl_interfaces/msg/Log
      /turtle1/color_sensor: turtlesim/msg/Color
      /turtle1/pose: turtlesim/msg/Pose
    Service Servers:
      /clear: std_srvs/srv/Empty
      /kill: turtlesim/srv/Kill
      /my_turtle/describe_parameters: rcl_interfaces/srv/DescribeParameters
      /my_turtle/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
      /my_turtle/get_parameters: rcl_interfaces/srv/GetParameters
      /my_turtle/list_parameters: rcl_interfaces/srv/ListParameters
      /my_turtle/set_parameters: rcl_interfaces/srv/SetParameters
      /my_turtle/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
      /reset: std_srvs/srv/Empty
      /spawn: turtlesim/srv/Spawn
      /turtle1/set_pen: turtlesim/srv/SetPen
      /turtle1/teleport_absolute: turtlesim/srv/TeleportAbsolute
      /turtle1/teleport_relative: turtlesim/srv/TeleportRelative
    Service Clients:

    Action Servers:
      /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute
    Action Clients:

``ros2 node info`` 会返回订阅者、发布者、服务和动作的列表，
也就是与该节点交互的 ROS 图连接。

现在尝试对 ``/teleop_turtle`` 节点运行相同的命令，看看它的连接与 ``my_turtle`` 有何不同。

你将在后续的教程中了解更多关于 ROS 图连接概念（包括消息类型）的内容。

小结
----

节点是 ROS 2 的基本元素，在机器人系统中承担单一、模块化的用途。

在本教程中，你通过运行可执行程序 ``turtlesim_node`` 和 ``turtle_teleop_key``，使用了 ``turtlesim`` 包中创建的节点。

你学习了如何使用 ``ros2 node list`` 发现活动节点名，以及如何使用 ``ros2 node info`` 内省单个节点。
这些工具对于理解复杂、真实的机器人系统中的数据流至关重要。

下一步
------

既然你已经理解了 ROS 2 中的节点，你可以继续学习 :doc:`话题教程 <../Understanding-ROS2-Topics/Understanding-ROS2-Topics>`。
话题是连接节点的一种通信类型。

相关内容
--------

:doc:`../../../Concepts` 页面为节点的概念补充了更多细节。
