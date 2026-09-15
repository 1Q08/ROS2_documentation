.. redirect-from::

    Tutorials/Tf2/Time-Travel-With-Tf2-Cpp

.. _TimeTravelWithTf2Cpp:

时间旅行（C++）
===============

**目标：** 学习 tf2 的高级时间旅行特性。

**教程级别：** 中级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 2
   :local:

背景
----

在上一节教程中，我们讨论了 :doc:`tf2 与时间基础知识 <./Learning-About-Tf2-And-Time-Cpp>` 。
本节教程将更进一步，展示一个强大的 tf2 技巧：时间旅行。
简而言之，tf2 库的关键特性之一就是它既能在空间上变换数据，也能在时间上变换数据。

tf2 的时间旅行特性可用于多种任务，例如长时间监测机器人的位姿，或者构建一个会跟随领导者“脚步”的跟随机器人。
我们将使用该时间旅行特性来查询过去时刻的变换，并让 ``turtle2`` 跟随 ``carrot1`` 的 5 秒之前的位置。

时间旅行
--------

首先，让我们回到上一节教程 :doc:`使用时间 <./Learning-About-Tf2-And-Time-Cpp>` 结束的地方。
进入你的 ``learning_tf2_cpp`` 软件包。

现在，我们不再让第二只乌龟前往胡萝卜当前所在的位置，而是让它前往第一个胡萝卜 5 秒之前所在的位置。
将 ``turtle_tf2_listener.cpp`` 文件中的 ``lookupTransform()`` 调用修改为

.. code-block:: C++

    rclcpp::Time when = this->get_clock()->now() - rclcpp::Duration(5, 0);
    t = tf_buffer_->lookupTransform(
        toFrameRel,
        fromFrameRel,
        when,
        50ms);

现在，如果你运行这段代码，在前 5 秒内，第二只乌龟将不知道要去哪里，因为此时我们还没有胡萝卜位姿的 5 秒历史记录。
但 5 秒之后会发生什么呢？
让我们试一试：

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_fixed_frame_demo_launch.xml

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_fixed_frame_demo_launch.yaml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_fixed_frame_demo_launch.py

.. image:: images/turtlesim_delay1.png

你现在应该会注意到，你的乌龟像这张截图中所显示的那样，不受控制地四处乱转。
让我们试着理解这种行为背后的原因。

#. 在我们的代码中，我们向 tf2 提出了如下问题：“``carrot1`` 在 5 秒之前的位姿，相对于 5 秒之前的 ``turtle2`` 是什么？”。
   这意味着我们既根据第二只乌龟 5 秒之前所在的位置，也根据第一个胡萝卜 5 秒之前所在的位置来控制它。

#. 然而，我们真正想问的是：“``carrot1`` 在 5 秒之前的位姿，相对于 ``turtle2`` 的当前位置是什么？”。

``lookupTransform()`` 的高级 API
--------------------------------

为了向 tf2 提出这个特定问题，我们将使用一个高级 API，它让我们能够显式地指定何时获取指定的变换。
这可以通过使用附加参数调用 ``lookupTransform()`` 方法来实现。
现在你的代码应该如下所示：

.. code-block:: C++

    rclcpp::Time now = this->get_clock()->now();
    rclcpp::Time when = now - rclcpp::Duration(5, 0);
    t = tf_buffer_->lookupTransform(
        toFrameRel,
        now,
        fromFrameRel,
        when,
        "world",
        50ms);

``lookupTransform()`` 的高级 API 需要六个参数：

#. 目标坐标系

#. 要变换到的时间

#. 源坐标系

#. 评估源坐标系的时间

#. 不随时间变化的坐标系，本例中为 ``world`` 坐标系

#. 等待目标坐标系可用所需的时间

总而言之，tf2 会在后台执行以下操作。
在过去时刻，它计算从 ``carrot1`` 到 ``world`` 的变换。
在 ``world`` 坐标系中，tf2 从过去时间旅行到当前时刻。
而在当前时刻，tf2 计算从 ``world`` 到 ``turtle2`` 的变换。

检查结果
--------

让我们再次运行仿真，这次使用高级时间旅行 API：

.. tabs::

  .. group-tab:: XML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_fixed_frame_demo_launch.xml

  .. group-tab:: YAML

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_fixed_frame_demo_launch.yaml

  .. group-tab:: Python

    .. code-block:: console

        $ ros2 launch learning_tf2_cpp turtle_tf2_fixed_frame_demo_launch.py

.. image:: images/turtlesim_delay2.png

没错，第二只乌龟现在会前往第一个胡萝卜 5 秒之前所在的位置！

概述
----

在本教程中，你已经了解了 tf2 的高级特性之一。
你学习了 tf2 可以在时间上变换数据，并学会了如何通过 turtlesim 示例来实现这一点。
tf2 让你能够回到过去，并使用高级的 ``lookupTransform()`` API 在乌龟的旧位姿与当前位姿之间进行坐标系变换。
