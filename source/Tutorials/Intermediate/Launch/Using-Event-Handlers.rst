.. redirect-from::

    Tutorials/Launch-Files/Using-Event-Handlers
    Tutorials/Launch/Using-Event-Handlers

使用事件处理器
==============

**目标：** 了解 ROS 2 launch 文件中的事件处理器

**教程级别：** 中级

**时间：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

ROS 2 中的 Launch 是一个执行和管理用户定义进程的系统。
它负责监控它启动的进程的状态，并报告和响应这些进程状态的变化。
这些变化称为事件，可以通过向 launch 系统注册事件处理器来处理。
事件处理器可以针对特定事件进行注册，并且可以用于监控进程状态。
此外，它们还可以用于定义一套复杂的规则，用于动态修改 launch 文件。

本教程展示了 ROS 2 launch 文件中事件处理器的使用示例。

先决条件
--------

本教程使用 :doc:`turtlesim <../../Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim>` 包。
本教程还假设你已经 :doc:`创建了一个新包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>`，构建类型为 ``ament_python``，名为 ``launch_tutorial``。

本教程扩展了 :doc:`在 launch 文件中使用替换 <./Using-Substitutions>` 教程中展示的代码。

使用事件处理器
--------------

1 事件处理器示例 launch 文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 ``launch_tutorial`` 包的 ``launch`` 文件夹中创建一个名为 ``example_event_handlers_launch.py`` 的新文件。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python

在 launch 描述中定义了针对 ``OnProcessStart``、``OnProcessIO``、``OnExecutionComplete``、``OnProcessExit`` 和 ``OnShutdown`` 事件的 ``RegisterEventHandler`` action。

``OnProcessStart`` 事件处理器用于注册一个在 turtlesim 节点启动时执行的回调函数。
当 turtlesim 节点启动时，它向控制台记录一条消息并执行 ``spawn_turtle`` action。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 98-106

``OnProcessIO`` 事件处理器用于注册一个在 ``spawn_turtle`` action 向其标准输出写入时执行的回调函数。
它记录生成请求的结果。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 107-115

``OnExecutionComplete`` 事件处理器用于注册一个在 ``spawn_turtle`` action 完成时执行的回调函数。
当生成 action 完成时，它向控制台记录一条消息，并执行 ``change_background_r`` 和 ``change_background_r_conditioned`` action。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 116-128

``OnProcessExit`` 事件处理器用于注册一个在 turtlesim 节点退出时执行的回调函数。
当 turtlesim 节点退出时，它向控制台记录一条消息，并执行 ``EmitEvent`` action 来发出一个 ``Shutdown`` 事件。
这意味着当 turtlesim 窗口关闭时，launch 进程将会关闭。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 129-139

最后，``OnShutdown`` 事件处理器用于注册一个在 launch 文件被要求关闭时执行的回调函数。
它向控制台记录一条消息，说明为什么要求关闭 launch 文件。
它记录的消息包含关闭原因，例如关闭 turtlesim 窗口或用户按下的 :kbd:`ctrl-c` 信号。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 140-146

构建包
------

进入工作空间的根目录，并构建包：

.. code-block:: console

  $ colcon build

另外，请记住在构建后 source 工作空间。

启动示例
--------

现在你可以使用 ``ros2 launch`` 命令启动 ``example_event_handlers_launch.py`` 文件。

.. code-block:: console

    $ ros2 launch launch_tutorial example_event_handlers_launch.py turtlesim_ns:='turtlesim3' use_provided_red:='True' new_background_r:=200

这将执行以下操作：

#. 启动一个背景为蓝色的 turtlesim 节点
#. 生成第二只海龟
#. 将颜色改为紫色
#. 如果提供的 ``background_r`` 参数为 ``200`` 且 ``use_provided_red`` 参数为 ``True``，则两秒后将颜色改为粉红色
#. 当 turtlesim 窗口关闭时关闭 launch 文件

此外，在以下情况下它会向控制台记录消息：

#. turtlesim 节点启动时
#. spawn action 被执行时
#. ``change_background_r`` action 被执行时
#. ``change_background_r_conditioned`` action 被执行时
#. turtlesim 节点退出时
#. launch 进程被要求关闭时。

文档
----

`launch 文档 <https://docs.ros.org/en/{DISTRO}/p/launch/architecture.html>`_ 提供了有关可用事件处理器的详细信息。

总结
----

在本教程中，你了解了如何在 launch 文件中使用事件处理器。
你学习了它们的语法和使用示例，以定义一套复杂的规则来动态修改 launch 文件。
