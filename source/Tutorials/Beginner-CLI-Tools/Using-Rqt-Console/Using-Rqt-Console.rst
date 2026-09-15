.. redirect-from::

    Tutorials/Rqt-Console/Using-Rqt-Console

.. _rqt_console:

使用 ``rqt_console`` 查看日志
=============================

**目标：** 了解 ``rqt_console``，这是一个用于查看日志消息的工具。

**教程级别：** 初级

**时长：** 5 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``rqt_console`` 是一个用于查看 ROS 2 中日志消息的 GUI 工具。
通常，日志消息会显示在终端中。
借助 ``rqt_console``，你可以随着时间收集这些消息，更近距离、更有条理地查看它们，对它们进行过滤、保存，甚至重新加载已保存的文件以便在其他时间查看。

节点会通过多种方式使用日志来输出有关事件和状态的消息。
它们的内容通常是面向用户的信息性内容。

前提条件
--------

你需要安装 :doc:`rqt_console 和 turtlesim <../Introducing-Turtlesim/Introducing-Turtlesim>`。

和往常一样，别忘了在你打开的 :doc:`每个新终端 <../Configuring-ROS2-Environment>` 中加载 ROS 2 环境。


任务
----

1 设置
^^^^^^

在新终端中使用以下命令启动 ``rqt_console``：

.. code-block:: console

    $ ros2 run rqt_console rqt_console

``rqt_console`` 窗口将会打开：

.. image:: images/console.png

控制台的第一部分用于显示来自系统的日志消息。

中间部分可以按排除严重级别的方式来过滤消息。
你还可以使用右侧的加号按钮添加更多排除过滤器。

底部部分用于高亮显示包含你所输入字符串的消息。
你也可以向这一部分添加更多过滤器。

现在在新终端中使用以下命令启动 ``turtlesim``：

.. code-block:: console

    $ ros2 run turtlesim turtlesim_node

2 rqt_console 上的消息
^^^^^^^^^^^^^^^^^^^^^^

为了产生供 ``rqt_console`` 显示的日志消息，我们让海龟撞到墙上。
在新终端中，输入下面的 ``ros2 topic pub`` 命令（在 :doc:`话题教程 <../Understanding-ROS2-Topics/Understanding-ROS2-Topics>` 中有详细介绍）：

.. code-block:: console

    $ ros2 topic pub -r 1 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}"

由于上面的命令以稳定的频率发布该话题，海龟会不断地撞到墙上。
在 ``rqt_console`` 中，你会看到带有 ``Warn`` 严重级别的同一条消息一遍又一遍地显示，如下所示：

.. image:: images/warn.png

在运行 ``ros2 topic pub`` 命令的终端中按 ``Ctrl+C``，让海龟停止撞墙。

3 日志记录器级别
^^^^^^^^^^^^^^^^

ROS 2 的日志记录器级别按严重程度排序：

 1. Fatal
 2. Error
 3. Warn
 4. Info
 5. Debug

对于每个级别表示什么并没有确切的标准，但可以安全地认为：

* ``Fatal`` 消息表示系统将要终止运行，以尽量避免受到损害。
* ``Error`` 消息表示存在重大问题，虽然不一定会损害系统，但会妨碍系统正常运行。
* ``Warn`` 消息表示出现了意外活动或不理想的结果，这可能代表更深层的问题，但不会直接损害功能。
* ``Info`` 消息表示事件和状态更新，可用于目视确认系统正在按预期运行。
* ``Debug`` 消息详细记录了系统执行的整个逐步过程。

默认级别是 ``Info``。
你只会看到默认严重级别以及更严重级别的消息。

通常只有 ``Debug`` 消息会被隐藏，因为它是唯一比 ``Info`` 严重程度更低的级别。
例如，如果你把默认级别设为 ``Warn``，那么你只会看到严重级别为 ``Warn``、``Error`` 和 ``Fatal`` 的消息。

3.1 设置默认日志记录器级别
~~~~~~~~~~~~~~~~~~~~~~~~~~

你可以在首次运行 ``/turtlesim`` 节点时通过重映射设置默认日志记录器级别。
在终端中输入以下命令：

.. code-block:: console

    $ ros2 run turtlesim turtlesim_node --ros-args --log-level WARN

现在你不会再看到上次启动 ``turtlesim`` 时控制台中出现的那些初始 ``Info`` 级别消息。
这是因为 ``Info`` 消息的优先级低于新的默认严重级别 ``Warn``。

概述
----

如果你需要仔细检查系统中的日志消息，``rqt_console`` 会非常有帮助。
你可能出于各种各样的原因想要检查日志消息，通常是为了找出哪里出了问题，以及导致该问题的一系列事件。

后续步骤
--------

下一个教程将教你如何使用 :doc:`ROS 2 Launch <../Launching-Multiple-Nodes/Launching-Multiple-Nodes>` 一次启动多个节点。
