.. redirect-from::

    Tutorials/Tf2/Learning-About-Tf2-And-Time-Cpp

.. _LearningAboutTf2AndTimeCpp:

使用时间（C++）
===============

**目标：** 学习如何使用 ``lookupTransform()`` 函数在特定时间获取变换，并等待变换在 tf2 树上可用。

**教程级别：** 中级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在之前的教程中，我们通过编写 :doc:`tf2 广播器 <Writing-A-Tf2-Broadcaster-Cpp>` 和 :doc:`tf2 监听器 <Writing-A-Tf2-Listener-Cpp>` 重新实现了海龟演示。
我们还学习了如何 :doc:`向变换树添加新坐标系 <Adding-A-Frame-Cpp>`，以及 tf2 如何跟踪坐标系构成的树。
这棵树会随时间变化，tf2 会为每个变换存储一份时间快照（默认最多保存 10 秒）。
到目前为止，我们使用 ``lookupTransform()`` 函数来访问该 tf2 树中最新可用的变换，而不必知道该变换是在什么时间记录的。
本教程将教你如何在特定时间获取变换。

任务
----

1 更新监听器节点
^^^^^^^^^^^^^^^^

让我们回到 :doc:`添加坐标系教程 <Adding-A-Frame-Cpp>` 结束的地方。
进入 ``learning_tf2_cpp`` 软件包。
打开 ``turtle_tf2_listener.cpp``，看看 ``lookupTransform()`` 的调用：

.. code-block:: C++

   t = tf_buffer_->lookupTransform(
      toFrameRel,
      fromFrameRel,
      tf2::TimePointZero);

可以看到，我们通过调用 ``tf2::TimePointZero`` 将时间指定为 0。

.. note::

    ``tf2`` 软件包有自己的时间类型 ``tf2::TimePoint``，它不同于 ``rclcpp::Time``。
    ``tf2_ros`` 软件包中的许多 API 会自动在 ``rclcpp::Time`` 和 ``tf2::TimePoint`` 之间进行转换。

    这里本可以使用 ``rclcpp::Time(0, 0, this->get_clock()->get_clock_type())``，但无论如何它都会被转换为 ``tf2::TimePointZero``。

对于 tf2 来说，时间 0 表示缓冲区中“最新可用”的变换。
现在，把这行改为在当前时间 ``this->get_clock()->now()`` 获取变换：

.. code-block:: C++

   rclcpp::Time now = this->get_clock()->now();
   t = tf_buffer_->lookupTransform(
      toFrameRel,
      fromFrameRel,
      now);

现在试着运行该 launch 文件。

.. code-block:: console

   $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.xml # .py or .yaml are also acceptable
   [INFO] [1629873136.345688064] [listener]: Could not transform turtle2 to turtle1: Lookup would
   require extrapolation into the future.  Requested time 1629873136.345539 but the latest data
   is at time 1629873136.338804, when looking up transform from frame [turtle1] to frame [turtle2]

输出表明该坐标系不存在，或者数据来自未来。

要理解为什么会发生这种情况，我们需要了解缓冲区是如何工作的。
首先，每个监听器都有一个缓冲区，用于存储来自各个 tf2 广播器的所有坐标变换。
其次，当广播器发出一个变换时，该变换需要一些时间才能进入缓冲区（通常为几毫秒）。
因此，当你在“现在”这一时刻请求坐标系变换时，应当等待几毫秒让该信息到达。

2 修复监听器节点
^^^^^^^^^^^^^^^^

tf2 提供了一个很好的工具，它会等待直到某个变换可用。
你只需为 ``lookupTransform()`` 添加一个超时参数即可使用它。
要修复这个问题，请按下所示修改你的代码（添加最后一个超时参数）：

.. code-block:: C++

   rclcpp::Time now = this->get_clock()->now();
   t = tf_buffer_->lookupTransform(
      toFrameRel,
      fromFrameRel,
      now,
      50ms);

``lookupTransform()`` 可以接受四个参数，其中最后一个是可选的超时时间。
它最多会阻塞该时长，等待超时。

3 检查结果
^^^^^^^^^^

现在你可以运行该 launch 文件了。

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.xml

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.yaml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.py

你应该会注意到，``lookupTransform()`` 实际上会阻塞，直到两只海龟之间的变换可用（通常只需要几毫秒）。
一旦达到超时时间（这里为五十毫秒），只有在变换仍然不可用时才会抛出异常。

概述
----

在本教程中，你学习了如何获取特定时间戳的变换，以及在使用 ``lookupTransform()`` 函数时如何等待变换在 tf2 树上变为可用。
