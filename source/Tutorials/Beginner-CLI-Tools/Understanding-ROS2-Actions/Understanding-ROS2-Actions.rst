.. redirect-from::

    Tutorials/Understanding-ROS2-Actions

.. _ROS2Actions:

理解动作
========

**目标：** 内省 ROS 2 中的动作。

**教程级别：** 入门

**用时：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

动作是 ROS 2 中的通信类型之一，用于长时间运行的任务。
它们由三个部分组成：目标（goal）、反馈（feedback）和结果（result）。

动作建立在话题和服务之上。
它们的功能与服务类似，区别在于动作可以被取消。
它们还提供持续的反馈，而服务只返回单个响应。

动作使用客户端-服务器模型，类似于发布者-订阅者模型（在 :doc:`话题教程 <../Understanding-ROS2-Topics/Understanding-ROS2-Topics>` 中描述）。
一个“动作客户端”节点向一个“动作服务器”节点发送目标，后者确认该目标并返回反馈流和一个结果。

.. image:: images/Action-SingleActionClient.gif

前置条件
--------

本教程建立在先前教程中介绍的概念之上，如 :doc:`节点 <../Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>` 和 :doc:`话题 <../Understanding-ROS2-Topics/Understanding-ROS2-Topics>`。

本教程使用 :doc:`turtlesim 包 <../Introducing-Turtlesim/Introducing-Turtlesim>`。

和往常一样，别忘了在 :doc:`每一个你新打开的终端 <../Configuring-ROS2-Environment>` 中 source ROS 2。

任务
----

1 准备
^^^^^^

启动两个 turtlesim 节点：``/turtlesim`` 和 ``/teleop_turtle``。

打开一个新终端并运行：

.. code-block:: console

  $ ros2 run turtlesim turtlesim_node

打开另一个终端并运行：

.. code-block:: console

  $ ros2 run turtlesim turtle_teleop_key


2 使用动作
^^^^^^^^^^

当你启动 ``/teleop_turtle`` 节点时，你会在终端中看到以下消息：

.. code-block:: console

    Use arrow keys to move the turtle.
    Use G|B|V|C|D|E|R|T keys to rotate to absolute orientations. 'F' to cancel a rotation.

让我们关注第二行，它对应于一个动作。
（第一条指令对应于 "cmd_vel" 话题，此前已在 :doc:`话题教程 <../Understanding-ROS2-Topics/Understanding-ROS2-Topics>` 中讨论过。）

注意，字母键 ``G|B|V|C|D|E|R|T`` 在美国 QWERTY 键盘上围绕 ``F`` 键形成了一个“方框”（如果你不使用 QWERTY 键盘，请查看 `此链接 <https://upload.wikimedia.org/wikipedia/commons/d/da/KB_United_States.svg>`__ 以便跟上）。
每个键在 ``F`` 周围的位置对应 turtlesim 中的那个方向。
例如，``E`` 会将乌龟的方向旋转到左上角。

注意运行 ``/turtlesim`` 节点的终端。
每当你按下这些键中的一个时，你都是在向 ``/turtlesim`` 节点中的动作服务器发送一个目标。
目标是让乌龟旋转到面向特定方向。
当乌龟完成旋转后，应该会显示一条传递目标结果的消息：

.. code-block:: console

    [INFO] [turtlesim]: Rotation goal completed successfully

``F`` 键会在执行过程中取消一个目标。

尝试按下 ``C`` 键，然后在乌龟完成旋转之前按下 ``F`` 键。
在运行 ``/turtlesim`` 节点的终端中，你会看到消息：

.. code-block:: console

  [INFO] [turtlesim]: Rotation goal canceled

不仅客户端（你在 teleop 中的输入）可以停止目标，服务器端（``/turtlesim`` 节点）也可以。
当服务器端选择停止处理一个目标时，称为“中止”（abort）该目标。

尝试按下 ``D`` 键，然后在第一次旋转完成之前按下 ``G`` 键。
在运行 ``/turtlesim`` 节点的终端中，你会看到消息：

.. code-block:: console

  [WARN] [turtlesim]: Rotation goal received before a previous goal finished. Aborting previous goal

这个动作服务器选择中止第一个目标，因为它收到了一个新目标。
它本可以选择其他处理方式，比如拒绝新目标，或在第一个目标完成后再执行第二个目标。
不要假设每个动作服务器在收到新目标时都会选择中止当前目标。

3 ros2 node info
^^^^^^^^^^^^^^^^

要查看节点提供的动作列表（本例中为 ``/turtlesim``），请打开一个新终端并运行命令：

.. code-block:: console

  $ ros2 node info /turtlesim
  /turtlesim
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
      /reset: std_srvs/srv/Empty
      /spawn: turtlesim/srv/Spawn
      /turtle1/set_pen: turtlesim/srv/SetPen
      /turtle1/teleport_absolute: turtlesim/srv/TeleportAbsolute
      /turtle1/teleport_relative: turtlesim/srv/TeleportRelative
      /turtlesim/describe_parameters: rcl_interfaces/srv/DescribeParameters
      /turtlesim/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
      /turtlesim/get_parameters: rcl_interfaces/srv/GetParameters
      /turtlesim/list_parameters: rcl_interfaces/srv/ListParameters
      /turtlesim/set_parameters: rcl_interfaces/srv/SetParameters
      /turtlesim/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
    Service Clients:

    Action Servers:
      /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute
    Action Clients:

该命令返回 ``/turtlesim`` 的订阅者、发布者、服务、动作服务器和动作客户端列表。

注意，``/turtlesim`` 的 ``/turtle1/rotate_absolute`` 动作位于 ``Action Servers`` 之下。
这意味着 ``/turtlesim`` 响应 ``/turtle1/rotate_absolute`` 动作并提供反馈。

``/teleop_turtle`` 节点的名称 ``/turtle1/rotate_absolute`` 位于 ``Action Clients`` 之下，意味着它为那个动作名称发送目标。
要查看这一点，请运行：

.. code-block:: console

  $ ros2 node info /teleop_turtle
  /teleop_turtle
    Subscribers:
      /parameter_events: rcl_interfaces/msg/ParameterEvent
    Publishers:
      /parameter_events: rcl_interfaces/msg/ParameterEvent
      /rosout: rcl_interfaces/msg/Log
      /turtle1/cmd_vel: geometry_msgs/msg/Twist
    Service Servers:
      /teleop_turtle/describe_parameters: rcl_interfaces/srv/DescribeParameters
      /teleop_turtle/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
      /teleop_turtle/get_parameters: rcl_interfaces/srv/GetParameters
      /teleop_turtle/list_parameters: rcl_interfaces/srv/ListParameters
      /teleop_turtle/set_parameters: rcl_interfaces/srv/SetParameters
      /teleop_turtle/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
    Service Clients:

    Action Servers:

    Action Clients:
      /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute

4 ros2 action list
^^^^^^^^^^^^^^^^^^

要识别 ROS 图中的所有动作，请运行命令：

.. code-block:: console

  $ ros2 action list
  /turtle1/rotate_absolute

这是目前 ROS 图中唯一的动作。
正如你之前看到的，它控制乌龟的旋转。
通过使用 ``ros2 node info <node_name>`` 命令，你也已经知道这个动作有一个动作客户端（``/teleop_turtle`` 的一部分）和一个动作服务器（``/turtlesim`` 的一部分）。

4.1 ros2 action list -t
~~~~~~~~~~~~~~~~~~~~~~~

动作有类型，与话题和服务类似。
要查找 ``/turtle1/rotate_absolute`` 的类型，请运行命令：

.. code-block:: console

  $ ros2 action list -t
  /turtle1/rotate_absolute [turtlesim/action/RotateAbsolute]

在每个动作名称右侧的方括号中（本例中只有 ``/turtle1/rotate_absolute``）是动作类型 ``turtlesim/action/RotateAbsolute``。
当你想要从命令行或代码中执行动作时，会需要它。

5 ros2 action type
^^^^^^^^^^^^^^^^^^

如果你想检查动作的动作类型，请运行命令：

.. code-block:: console

  $ ros2 action type /turtle1/rotate_absolute
  turtlesim/action/RotateAbsolute

6 ros2 action info
^^^^^^^^^^^^^^^^^^

你可以使用以下命令进一步内省 ``/turtle1/rotate_absolute`` 动作：

.. code-block:: console

  $ ros2 action info /turtle1/rotate_absolute
  Action: /turtle1/rotate_absolute
  Action clients: 1
      /teleop_turtle
  Action servers: 1
      /turtlesim

这告诉了我们之前对每个节点运行 ``ros2 node info`` 时了解到的内容：
``/teleop_turtle`` 节点有一个动作客户端，``/turtlesim`` 节点有一个用于 ``/turtle1/rotate_absolute`` 动作的动作服务器。

7 ros2 interface show
^^^^^^^^^^^^^^^^^^^^^

在你自己发送或执行动作目标之前，你还需要的一项信息是动作类型的结构。

回想一下，你在运行命令 ``ros2 action list -t`` 时识别出了 ``/turtle1/rotate_absolute`` 的类型。
在你的终端中输入以下带动作类型的命令：

.. code-block:: console

  $ ros2 interface show turtlesim/action/RotateAbsolute

它将返回：

.. code-block:: text

  # The desired heading in radians
  float32 theta
  ---
  # The angular displacement in radians to the starting position
  float32 delta
  ---
  # The remaining rotation in radians
  float32 remaining

该消息中第一个 ``---`` 之上的部分是目标请求的结构（数据类型和名称）。
下一部分是结果的结构。
最后一部分是反馈的结构。

8 ros2 action send_goal
^^^^^^^^^^^^^^^^^^^^^^^

现在让我们使用以下语法从命令行发送一个动作目标：

.. code-block:: console

  $ ros2 action send_goal <action_name> <action_type> <values>

``<values>`` 需要采用 YAML 格式。

留意 turtlesim 窗口，并在你的终端中输入以下命令：

.. code-block:: console

  $ ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}"
  Waiting for an action server to become available...
  Sending goal:
     theta: 1.57

  Goal accepted with ID: f8db8f44410849eaa93d3feb747dd444

  Result:
    delta: -1.568000316619873

  Goal finished with status: SUCCEEDED


你应该会看到乌龟在旋转。


所有目标都有一个唯一的 ID，显示在返回消息中。
你还可以看到结果，一个名为 ``delta`` 的字段，它是到起始位置的位移。

要查看该目标的反馈，请向 ``ros2 action send_goal`` 命令添加 ``--feedback``：

.. code-block:: console

  $ ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: -1.57}" --feedback
  Sending goal:
     theta: -1.57

  Goal accepted with ID: e6092c831f994afda92f0086f220da27

  Feedback:
    remaining: -3.1268222332000732

  Feedback:
    remaining: -3.1108222007751465

  …

  Result:
    delta: 3.1200008392333984

  Goal finished with status: SUCCEEDED

你将继续收到反馈（剩余的弧度数），直到目标完成。

小结
----

动作类似于服务，允许你执行长时间运行的任务、提供定期反馈，并且可以被取消。

机器人系统很可能会将动作用于导航。
一个动作目标可以告诉机器人行进到某个位置。
当机器人导航到该位置时，它可以沿途发送更新（即反馈），然后在到达目的地后发送最终结果消息。

Turtlesim 有一个动作服务器，动作客户端可以向它发送目标来旋转乌龟。
在本教程中，你内省了那个动作 ``/turtle1/rotate_absolute``，以便更好地理解动作是什么以及它们如何工作。

下一步
------

现在你已经涵盖了所有核心 ROS 2 概念。
本系列的最后几个教程将向你介绍一些工具和技术，让使用 ROS 2 更加容易，从 :doc:`../Using-Rqt-Console/Using-Rqt-Console` 开始。

相关内容
--------

你可以 `在这里 <https://design.ros2.org/articles/actions.html>`__ 阅读更多关于 ROS 2 动作背后设计决策的内容。
