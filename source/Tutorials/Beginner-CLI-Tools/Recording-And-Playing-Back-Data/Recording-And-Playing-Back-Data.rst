.. redirect-from::

    Tutorials/Ros2bag/Recording-And-Playing-Back-Data

.. _ROS2Bag:

录制与回放数据
==============

**目标：** 录制发布在话题上的数据，以便随时回放和检查。

**教程级别：** 入门

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

``ros2 bag`` 是一个命令行工具，用于录制系统中发布在话题上的数据。
它会累积任意数量的话题上传递的数据，然后保存到数据库中。
之后你可以回放数据，重现测试和实验的结果。
录制话题也是分享你的工作、让他人复现的好方法。


前置条件
--------

你的常规 ROS 2 环境安装中应该已经包含 ``ros2 bag``。

如果你需要安装 ROS 2，请参阅 :doc:`安装说明 <../../../Installation>`。

本教程讨论了先前教程中介绍的概念，如 :doc:`节点 <../Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>` 和 :doc:`话题 <../Understanding-ROS2-Topics/Understanding-ROS2-Topics>`。
它还会用到 :doc:`turtlesim 包 <../Introducing-Turtlesim/Introducing-Turtlesim>`。

和往常一样，别忘了在 :doc:`每一个你新打开的终端 <../Configuring-ROS2-Environment>` 中 source ROS 2。


任务
----

1 准备
^^^^^^
你将录制 ``turtlesim`` 系统中的键盘输入，以便稍后保存和回放，所以首先启动 ``/turtlesim`` 和 ``/teleop_turtle`` 节点。

打开一个新终端并运行：

.. code-block:: console

    $ ros2 run turtlesim turtlesim_node

打开另一个终端并运行：

.. code-block:: console

    $ ros2 run turtlesim turtle_teleop_key

作为良好的习惯，让我们再创建一个新目录来存放我们的录制文件：

.. tabs::

    .. group-tab:: Linux

        .. code-block:: console

            $ mkdir bag_files
            $ cd bag_files

    .. group-tab:: macOS

        .. code-block:: console

            $ mkdir bag_files
            $ cd bag_files

    .. group-tab:: Windows

        .. code-block:: console

            $ md bag_files
            $ cd bag_files


2 选择一个话题
^^^^^^^^^^^^^^

``ros2 bag`` 只能从发布到话题的消息中录制数据。
要查看系统的话题列表，请打开一个新终端并运行命令：

.. code-block:: console

  $ ros2 topic list
  /parameter_events
  /rosout
  /turtle1/cmd_vel
  /turtle1/color_sensor
  /turtle1/pose

在话题教程中，你了解到 ``/turtle_teleop`` 节点在 ``/turtle1/cmd_vel`` 话题上发布命令，使乌龟在 turtlesim 中移动。

要查看 ``/turtle1/cmd_vel`` 正在发布的数据，请运行命令：

.. code-block:: console

    $ ros2 topic echo /turtle1/cmd_vel

一开始什么都不会显示，因为 teleop 还没有发布任何数据。
返回你运行 teleop 的终端并选中它，使其处于活动状态。
使用方向键移动乌龟，你就会看到数据发布在运行 ``ros2 topic echo`` 的终端上。

.. code-block:: console

  linear:
    x: 2.0
    y: 0.0
    z: 0.0
  angular:
    x: 0.0
    y: 0.0
    z: 0.0
    ---


3 ros2 bag record
^^^^^^^^^^^^^^^^^

3.1 录制单个话题
~~~~~~~~~~~~~~~~

要录制发布到某个话题的数据，请使用以下命令语法：

.. code-block:: console

    $ ros2 bag record <topic_name>

在你选定的话题上运行此命令之前，请打开一个新终端并进入你之前创建的 ``bag_files`` 目录，因为 rosbag 文件会保存在你运行它的目录中。

运行命令：

.. code-block:: console

    $ ros2 bag record /turtle1/cmd_vel
    [INFO] [rosbag2_storage]: Opened database 'rosbag2_2019_10_11-05_18_45'.
    [INFO] [rosbag2_transport]: Listening for topics...
    [INFO] [rosbag2_transport]: Subscribed to topic '/turtle1/cmd_vel'
    [INFO] [rosbag2_transport]: All requested topics are subscribed. Stopping discovery...

现在 ``ros2 bag`` 正在录制发布在 ``/turtle1/cmd_vel`` 话题上的数据。
返回 teleop 终端，再次移动乌龟。
移动方式并不重要，但尽量做出一个可识别的图案，以便稍后回放数据时能看到。

.. image:: images/record.png

按 ``Ctrl+C`` 停止录制。

数据将累积到一个新的 bag 目录中，目录名的格式为 ``rosbag2_年_月_日-时_分_秒``。
该目录将包含一个 ``metadata.yaml`` 以及按录制格式保存的 bag 文件。

3.2 录制多个话题
~~~~~~~~~~~~~~~~

你也可以录制多个话题，并更改 ``ros2 bag`` 保存文件的名称。

运行以下命令：

.. code-block:: console

  $ ros2 bag record -o subset /turtle1/cmd_vel /turtle1/pose
  [INFO] [rosbag2_storage]: Opened database 'subset'.
  [INFO] [rosbag2_transport]: Listening for topics...
  [INFO] [rosbag2_transport]: Subscribed to topic '/turtle1/cmd_vel'
  [INFO] [rosbag2_transport]: Subscribed to topic '/turtle1/pose'
  [INFO] [rosbag2_transport]: All requested topics are subscribed. Stopping discovery...

``-o`` 选项允许你为 bag 文件选择一个唯一的名称。
后面的字符串，在本例中是 ``subset``，就是文件名。

要同时录制多个话题，只需用空格分隔每个话题。
在本例中，上面的命令输出确认了两个话题都在被录制。


你可以移动乌龟，完成后按 ``Ctrl+C``。

.. note::

    你还可以给命令添加另一个选项 ``-a``，它会录制系统中的所有话题。

4 ros2 bag info
^^^^^^^^^^^^^^^

你可以通过运行以下命令查看录制的详细信息：

.. code-block:: console

    $ ros2 bag info <bag_file_name>

对 ``subset`` bag 文件运行此命令，将返回该文件的信息列表：

.. code-block:: console

    $ ros2 bag info subset
    Files:             subset.db3
    Bag size:          228.5 KiB
    Storage id:        sqlite3
    Duration:          48.47s
    Start:             Oct 11 2019 06:09:09.12 (1570799349.12)
    End                Oct 11 2019 06:09:57.60 (1570799397.60)
    Messages:          3013
    Topic information: Topic: /turtle1/cmd_vel | Type: geometry_msgs/msg/Twist | Count: 9 | Serialization Format: cdr
                       Topic: /turtle1/pose | Type: turtlesim/msg/Pose | Count: 3004 | Serialization Format: cdr

5 ros2 bag play
^^^^^^^^^^^^^^^

在回放 bag 文件之前，在运行 teleop 的终端中输入 ``Ctrl+C``。
然后确保 turtlesim 窗口可见，这样你就能看到 bag 文件的回放效果。

输入命令：

.. code-block:: console

    $ ros2 bag play subset
    [INFO] [rosbag2_storage]: Opened database 'subset'.

你的乌龟将沿着你录制时输入的相同路径移动（虽然不是 100% 完全一致；turtlesim 对系统时序的微小变化很敏感）。

.. image:: images/playback.png

由于 ``subset`` 文件录制了 ``/turtle1/pose`` 话题，只要 turtlesim 还在运行，``ros2 bag play`` 命令就不会退出，即使你当时没有移动。

这是因为只要 ``/turtlesim`` 节点处于活动状态，它就会定期在 ``/turtle1/pose`` 话题上发布数据。
你可能已经注意到，在上面的 ``ros2 bag info`` 示例结果中，``/turtle1/cmd_vel`` 话题的 ``Count`` 信息只有 9；这就是我们在录制时按下方向键的次数。

注意，``/turtle1/pose`` 的 ``Count`` 值超过了 3000；在我们录制期间，数据在该话题上发布了 3000 次。

要了解位置数据的发布频率，你可以运行命令：

.. code-block:: console

    $ ros2 topic hz /turtle1/pose

小结
----

你可以使用 ``ros2 bag`` 命令录制 ROS 2 系统中在话题上传递的数据。
无论你是要与他人分享工作，还是内省自己的实验，它都是一个值得了解的好工具。

下一步
------

你已经完成了“入门：CLI 工具”教程！
下一步是“入门：客户端库”教程，从 :doc:`../../Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace` 开始。

相关内容
--------

关于 ``ros2 bag`` 的更详细说明可以在 README `这里 <https://github.com/ros2/rosbag2>`__ 找到。
关于 QoS 兼容性与 ``ros2 bag`` 的更多信息，请参阅 :doc:`../../../How-To-Guides/Overriding-QoS-Policies-For-Recording-And-Playback`。
