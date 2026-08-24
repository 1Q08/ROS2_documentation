.. redirect-from::

    Tutorials/Tf2/Learning-About-Tf2-And-Time-Cpp

.. _LearningAboutTf2AndTimeCpp:

使用时间（C++）
===============

**目标：** 学习如何使用 ``lookupTransform()`` 函数获取特定时间的变换，并等待变换在 tf2 树上可用。

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在之前的教程中，我们通过编写 :doc:`tf2 广播器 <Writing-A-Tf2-Broadcaster-Cpp>` 和 :doc:`tf2 监听器 <Writing-A-Tf2-Listener-Cpp>` 重建了 turtle 演示。
我们还学习了如何 :doc:`向变换树添加新帧 <Adding-A-Frame-Cpp>`，并了解了 tf2 如何追踪坐标帧树。
这棵树会随时间变化，tf2 会为每个变换存储一个时间快照（默认最多 10 秒）。
到目前为止，我们使用 ``lookupTransform()`` 函数来获取 tf2 树中最新可用的变换，而不知道该变换是在什么时间记录的。
本教程将教你如何获取特定时间的变换。

任务
----

1 更新监听器节点
^^^^^^^^^^^^^^^^

让我们回到 :doc:`添加帧教程 <Adding-A-Frame-Cpp>` 结束的地方。
转到 ``learning_tf2_cpp`` 包。
打开 ``turtle_tf2_listener.cpp`` 并查看 ``lookupTransform()`` 调用：

.. code-block:: C++

   try {
       t = tf_buffer_->lookupTransform(
          toFrameRel,
          fromFrameRel,
          tf2::TimePointZero);
   } catch (const tf2::TransformException & ex) {

你可以看到，我们通过调用 ``tf2::TimePointZero`` 指定了等于 0 的时间。

.. note::

    ``tf2`` 包有自己的时间类型 ``tf2::TimePoint``，它与 ``rclcpp::Time`` 不同。
    ``tf2_ros`` 包中的许多 API 会自动在 ``rclcpp::Time`` 和 ``tf2::TimePoint`` 之间转换。

    这里也可以使用 ``rclcpp::Time(0, 0, this->get_clock()->get_clock_type())``，但无论如何它都会被转换为 ``tf2::TimePointZero``。

对于 tf2，时间 0 表示缓冲区中“最新可用”的变换。
现在，把这一行改为获取当前时间 ``this->get_clock()->now()`` 的变换：

.. code-block:: C++

   rclcpp::Time now = this->get_clock()->now();
   try {
       t = tf_buffer_->lookupTransform(
           toFrameRel, fromFrameRel,
           now);
   } catch (const tf2::TransformException & ex) {

现在构建包并尝试运行启动文件。

.. code-block:: console

   $ ros2 launch learning_tf2_cpp turtle_tf2_demo_launch.xml # .py or .yaml are also acceptable
   [INFO] [1629873136.345688064] [listener]: Could not transform turtle2 to turtle1: Lookup would
   require extrapolation into the future.  Requested time 1629873136.345539 but the latest data
   is at time 1629873136.338804, when looking up transform from frame [turtle1] to frame [turtle2]

输出告诉你该帧不存在，或者数据在将来。

要理解为什么会发生这种情况，我们需要了解缓冲区是如何工作的。
首先，每个监听器都有一个缓冲区，用来存储来自不同 tf2 广播器的所有坐标变换。
其次，当广播器发出一个变换时，该变换进入缓冲区需要一些时间（通常是几毫秒）。
因此，当你在“现在”这个时间请求一个帧变换时，你应该等待几毫秒让该信息到达。

2 修复监听器节点
^^^^^^^^^^^^^^^^

tf2 提供了一个好用的工具，可以等待变换变为可用。
你可以通过在 ``lookupTransform()`` 中添加一个超时参数来使用它。
要修复这个问题，请如下修改你的代码（添加最后一个超时参数）：

.. code-block:: C++

   rclcpp::Time now = this->get_clock()->now();
   try {
       t = tf_buffer_->lookupTransform(
           toFrameRel,
           fromFrameRel,
           now,
           50ms);
   } catch (const tf2::TransformException & ex) {

``lookupTransform()`` 可以接受四个参数，其中最后一个是可选超时。
它最多会阻塞到该时长，等待超时。

3 检查结果
^^^^^^^^^^

现在你可以构建包并运行启动文件。

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

你应该会注意到 ``lookupTransform()`` 实际上会阻塞，直到两只 turtle 之间的变换变为可用（这通常需要几毫秒）。
一旦达到超时（本例中为五十毫秒），只有当变换仍然不可用时才会引发异常。

总结
----

在本教程中，你学习了如何获取特定时间戳的变换，以及在使用 ``lookupTransform()`` 函数时如何等待变换在 tf2 树上可用。
