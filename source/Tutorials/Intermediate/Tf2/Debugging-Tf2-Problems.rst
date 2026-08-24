.. redirect-from::

    Tutorials/Tf2/Debugging-Tf2-Problems

.. _DebuggingTf2Problems:

调试
====

**目标：** 学习如何使用系统化方法来调试 tf2 相关的问题。

**教程级别：** 中级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

本教程将带你一步步调试一个典型的 tf2 问题。
它还会使用许多 tf2 调试工具，如 ``tf2_echo``、``tf2_monitor`` 和 ``view_frames``。
本教程假设你已经完成了 :doc:`学习 tf2 <./Tf2-Main>` 教程。

调试示例
--------

1 设置并启动示例
^^^^^^^^^^^^^^^^

在本教程中，我们将设置一个存在多个问题的演示应用程序。
本教程的目标是应用一种系统化方法来发现并解决这些问题。
首先，让我们创建源文件。

转到我们在 :doc:`tf2 教程 <./Tf2-Main>` 中创建的 ``learning_tf2_cpp`` 包。
在 ``src`` 目录中复制源文件 ``turtle_tf2_listener.cpp``，并将其重命名为 ``turtle_tf2_listener_debug.cpp``。

用你喜欢的文本编辑器打开该文件，将第 65 行从

.. code-block:: C++

   std::string toFrameRel = "turtle2";

改为

.. code-block:: C++

   std::string toFrameRel = "turtle3";

并将第 73-77 行的 ``lookupTransform()`` 调用从

.. code-block:: C++

    try {
      t = tf_buffer_->lookupTransform(
        toFrameRel, fromFrameRel,
        tf2::TimePointZero);
    } catch (const tf2::TransformException & ex) {

改为

.. code-block:: C++

    try {
      t = tf_buffer_->lookupTransform(
        toFrameRel, fromFrameRel,
        this->now());
    } catch (const tf2::TransformException & ex) {

并保存对文件的更改。
为了运行这个演示，我们需要在 ``learning_tf2_cpp`` 包的 ``launch`` 子目录中创建一个名为 ``start_tf2_debug_demo_launch``、扩展名为 ``.py``、``.xml`` 或 ``.yaml`` 的启动文件：

.. tabs::

  .. group-tab:: Python

    .. literalinclude:: launch/start_tf2_debug_demo_launch.py
        :language: python

  .. group-tab:: XML

    .. literalinclude:: launch/start_tf2_debug_demo_launch.xml
        :language: xml

  .. group-tab:: YAML

    .. literalinclude:: launch/start_tf2_debug_demo_launch.yaml
        :language: yaml

不要忘记将 ``turtle_tf2_listener_debug`` 可执行文件添加到 ``CMakeLists.txt`` 中，并构建包。

现在让我们运行它，看看会发生什么：

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.xml

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.yaml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.py

现在你会看到 turtlesim 出现了。
同时，如果你在另一个终端窗口运行 ``turtle_teleop_key``，你可以使用方向键驾驶 ``turtle1`` 四处移动。

.. code-block:: console

   $ ros2 run turtlesim turtle_teleop_key
   [turtle_tf2_listener_debug-4] [INFO] [1630223454.942322623] [listener_debug]: Could not
   transform turtle3 to turtle1: "turtle3" passed to lookupTransform argument target_frame
   does not exist

你还会注意到左下角有第二只 turtle。
如果演示正常工作，这第二只 turtle 应该跟随你能用方向键控制的那只 turtle。
然而事实并非如此，因为我们必须先解决一些问题。

2 查找 tf2 请求
^^^^^^^^^^^^^^^

首先，我们需要找出我们到底要求 tf2 做什么。
因此，我们进入使用 tf2 的那部分代码。
打开 ``src/turtle_tf2_listener_debug.cpp`` 文件，查看第 65 行：

.. code-block:: C++

   std::string toFrameRel = "turtle3";

以及第 73-77 行：

.. code-block:: C++

    try {
      t = tf_buffer_->lookupTransform(
        toFrameRel, fromFrameRel,
        this->now());
    } catch (const tf2::TransformException & ex) {

这里我们向 tf2 发起实际的请求。
这三个参数直接告诉我们我们在要求 tf2 做什么：在时间 ``now`` 从帧 ``turtle3`` 变换到帧 ``turtle1``。

现在，让我们看看为什么这个对 tf2 的请求会失败。

3 检查帧
^^^^^^^^

首先，为了找出 tf2 是否知道我们 ``turtle3`` 和 ``turtle1`` 之间的变换，我们将使用 ``tf2_echo`` 工具。

.. code-block:: console

   $ ros2 run tf2_ros tf2_echo turtle3 turtle1
   [INFO] [1630223557.477636052] [tf2_echo]: Waiting for transform turtle3 ->  turtle1:
   Invalid frame ID "turtle3" passed to canTransform argument target_frame - frame does
   not exist

输出告诉我们帧 ``turtle3`` 不存在。

那么哪些帧存在呢？
如果你想要一个图形化表示，请使用 ``view_frames`` 工具。

.. code-block:: console

   $ ros2 run tf2_tools view_frames

打开生成的 ``frames.pdf`` 文件，查看以下输出：

.. image:: images/turtlesim_frames.png

所以问题显然是我们请求从帧 ``turtle3`` 变换，而该帧不存在。
要修复这个错误，只需将第 65 行的 ``turtle3`` 替换为 ``turtle2``。

现在停止正在运行的演示，构建它，然后再次运行：

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.xml
        [turtle_tf2_listener_debug-4] [INFO] [1630223704.617382464] [listener_debug]: Could not
        transform turtle2 to turtle1: Lookup would require extrapolation into the future. Requested
        time 1630223704.617054 but the latest data is at time 1630223704.616726, when looking up
        transform from frame [turtle1] to frame [turtle2]

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.yaml
        [turtle_tf2_listener_debug-4] [INFO] [1630223704.617382464] [listener_debug]: Could not
        transform turtle2 to turtle1: Lookup would require extrapolation into the future. Requested
        time 1630223704.617054 but the latest data is at time 1630223704.616726, when looking up
        transform from frame [turtle1] to frame [turtle2]

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.py
        [turtle_tf2_listener_debug-4] [INFO] [1630223704.617382464] [listener_debug]: Could not
        transform turtle2 to turtle1: Lookup would require extrapolation into the future. Requested
        time 1630223704.617054 but the latest data is at time 1630223704.616726, when looking up
        transform from frame [turtle1] to frame [turtle2]

我们立刻就遇到了下一个问题。

4 检查时间戳
^^^^^^^^^^^^

既然我们解决了帧名称问题，现在是时候看看时间戳了。
记住，我们正在尝试获取 ``turtle2`` 和 ``turtle1`` 之间在当前时间（即 ``now``）的变换。
要获取关于时间的统计信息，请用相应的帧调用 ``tf2_monitor``。

.. code-block:: console

   $ ros2 run tf2_ros tf2_monitor turtle2 turtle1
   RESULTS: for turtle2 to turtle1
   Chain is: turtle1
   Net delay     avg = 0.00287347: max = 0.0167241

   Frames:
   Frame: turtle1, published by <no authority available>, Average Delay: 0.000295833, Max Delay: 0.000755072

   All Broadcasters:
   Node: <no authority available> 125.246 Hz, Average Delay: 0.000290237 Max Delay: 0.000786781

这里的关键部分是 ``turtle2`` 到 ``turtle1`` 链的延迟。
输出显示平均延迟约为 3 毫秒。
这意味着 tf2 只能在经过 3 毫秒后才能变换 turtle 之间的数据。
因此，如果我们要求 tf2 给出 3 毫秒前而不是 ``now`` 的 turtle 间变换，tf2 有时就能给出答案。
让我们通过将第 73-77 行改为以下内容来快速测试：

.. code-block:: C++

    try {
      t = tf_buffer_->lookupTransform(
        toFrameRel, fromFrameRel,
        this->now() - rclcpp::Duration::from_seconds(0.1));
    } catch (const tf2::TransformException & ex) {

在新代码中，我们请求 100 毫秒前的 turtle 间变换。
通常使用更长的时间段，只是为了确保变换会到达。
停止演示，构建并运行：

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.xml

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.yaml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp start_tf2_debug_demo_launch.py

你应该终于看到 turtle 移动了！

.. image:: images/turtlesim_follow1.png

我们做的最后一个修复并不是你真正想做的，它只是用来确认那就是我们的问题。
真正的修复应该是这样的：

.. code-block:: C++

    try {
      t = tf_buffer_->lookupTransform(
        toFrameRel, fromFrameRel,
        tf2::TimePointZero);
    } catch (const tf2::TransformException & ex) {

或者像这样：

.. code-block:: C++

    try {
      t = tf_buffer_->lookupTransform(
        toFrameRel, fromFrameRel,
        tf2::TimePoint());
    } catch (const tf2::TransformException & ex) {

你可以在 :doc:`使用时间 <./Learning-About-Tf2-And-Time-Cpp>` 教程中了解更多关于超时的内容，并按如下方式使用它们：

.. code-block:: C++

    try {
      t = tf_buffer_->lookupTransform(
        toFrameRel, fromFrameRel,
        this->now(),
        rclcpp::Duration::from_seconds(0.05));
    } catch (const tf2::TransformException & ex) {

总结
----

在本教程中，你学习了如何使用系统化方法来调试 tf2 相关的问题。
你还学习了如何使用 tf2 调试工具，如 ``tf2_echo``、``tf2_monitor`` 和 ``view_frames`` 来帮助你调试这些 tf2 问题。
