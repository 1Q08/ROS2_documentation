.. redirect-from::

    Tutorials/Launch-Files/Using-Event-Handlers
    Tutorials/Launch/Using-Event-Handlers

使用事件处理器
==============

**目标：** 了解 ROS 2 launch 文件中的事件处理器

**教程级别：** 中级

**时长：** 15 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

ROS 2 中的 launch 是一个用于执行和管理用户定义进程的系统。
它负责监控所启动进程的状态，并报告和响应这些进程状态的变化。
这些变化称为事件，可以通过向 launch 系统注册事件处理器来处理。
事件处理器可以针对特定事件注册，对于监控进程状态非常有用。
此外，它们还可以用来定义一组复杂的规则，从而动态地修改 launch 文件。

本教程展示了 ROS 2 launch 文件中事件处理器的用法示例。

前提条件
--------

本教程使用 :doc:`turtlesim <../../Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim>` 软件包。
本教程还假定你已经 :doc:`创建了一个新软件包 <../../Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>` ，其构建类型为 ``ament_python``，名称为 ``launch_tutorial``。

本教程扩展了 :doc:`在 launch 文件中使用替换 <./Using-Substitutions>` 教程中展示的代码。

使用事件处理器
--------------

1 事件处理器示例 launch 文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在 ``launch_tutorial`` 软件包的 ``launch`` 文件夹中创建一个名为 ``example_event_handlers.launch.py`` 的新文件。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python

在 launch 描述中定义了针对 ``OnProcessStart``、``OnProcessIO``、``OnExecutionComplete``、``OnProcessExit`` 和 ``OnShutdown`` 事件的 ``RegisterEventHandler`` 操作。

事件处理器 ``OnProcessStart`` 用于注册一个回调函数，该函数在 turtlesim 节点启动时执行。
它在 turtlesim 节点启动时会向控制台记录一条消息，并执行 ``spawn_turtle`` 操作。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 98-106

事件处理器 ``OnProcessIO`` 用于注册一个回调函数，该函数在 ``spawn_turtle`` 操作写入其标准输出时执行。
它会记录生成请求的结果。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 107-115

事件处理器 ``OnExecutionComplete`` 用于注册一个回调函数，该函数在 ``spawn_turtle`` 操作完成时执行。
它在生成操作完成时会向控制台记录一条消息，并执行 ``change_background_r`` 和 ``change_background_r_conditioned`` 操作。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 116-128

事件处理器 ``OnProcessExit`` 用于注册一个回调函数，该函数在 turtlesim 节点退出时执行。
它在 turtlesim 节点退出时会向控制台记录一条消息，并执行 ``EmitEvent`` 操作以发出 ``Shutdown`` 事件。
这意味着当 turtlesim 窗口关闭时，launch 进程将会关闭。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 129-139

最后，``OnShutdown`` 事件处理器用于注册一个回调函数，该函数在要求 launch 文件关闭时执行。
它会向控制台记录要求 launch 文件关闭的原因。
它会记录带有关闭原因的消息，例如 turtlesim 窗口关闭或用户按下 :kbd:`ctrl-c` 信号。

.. literalinclude:: launch/example_event_handlers_launch.py
    :language: python
    :lines: 140-146

构建软件包
----------

转到工作空间的根目录，并构建软件包：

.. code-block:: console

  $ colcon build

另外，记得在构建后加载工作空间。

运行示例
--------

现在你可以使用 ``ros2 launch`` 命令启动 ``example_event_handlers.launch.py`` 文件。

.. code-block:: console

    $ ros2 launch launch_tutorial example_event_handlers.launch.py turtlesim_ns:='turtlesim3' use_provided_red:='True' new_background_r:=200

这将执行以下操作：

#. 启动一个带有蓝色背景的 turtlesim 节点
#. 生成第二只海龟
#. 将颜色改为紫色
#. 如果提供的 ``background_r`` 参数为 ``200`` 且 ``use_provided_red`` 参数为 ``True``，则在两秒后将颜色改为粉色
#. 当 turtlesim 窗口关闭时关闭 launch 文件

此外，在以下情况下它还会向控制台记录消息：

#. turtlesim 节点启动时
#. 执行生成操作时
#. 执行 ``change_background_r`` 操作时
#. 执行 ``change_background_r_conditioned`` 操作时
#. turtlesim 节点退出时
#. 要求 launch 进程关闭时。

文档
----

`launch 文档 <https://github.com/ros2/launch/blob/{REPOS_FILE_BRANCH}/launch/doc/source/architecture.rst>`_ 提供了关于可用事件处理器的详细信息。

概述
----

在本教程中，你学习了如何在 launch 文件中使用事件处理器。
你了解了它们的语法以及用于定义动态修改 launch 文件的一组复杂规则的使用示例。
