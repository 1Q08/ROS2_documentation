等待确认
========

**目标：** 等待发布者所发送消息的确认。

**教程级别：** 高级

**时长：** 10 分钟

.. contents:: 目录
   :depth: 1
   :local:

概述
----

在发布者-订阅者架构中，消息从发布者发送给订阅者，而发布者没有任何内置机制来确认订阅者已收到消息。
该特性使发布者能够等待其所发送消息的确认。
在发布者需要在继续执行进一步操作（例如发送更多消息或执行其他操作）之前确保订阅者已收到消息的场景中，这非常有用。

RMW 支持
--------

等待确认需要 RMW 实现的支持。

.. list-table::  Wait-for-Acknowledgment 支持状态
   :widths: 25 25

   * - rmw_fastrtps
     - supported
   * - rmw_connextdds
     - supported
   * - rmw_cyclonedds
     - supported

发布者的 :ref:`QoS 可靠性策略 <about_qos_policies>` 需要为 ``RELIABLE`` 才能使用等待确认特性，否则发布者将不会等待确认。

安装演示
--------

有关安装 ROS 2 的详细信息，请参阅 :doc:`安装说明 <../../Installation>`。

如果你从软件包安装了 ROS 2，请确保已安装 ``ros-{DISTRO}-examples-rclcpp-minimal-publisher`` 和 ``ros-{DISTRO}-examples-rclcpp-minimal-subscriber``。
如果你下载了压缩包或从源码构建了 ROS 2，它们已包含在安装中。

运行演示
--------

本演示展示了如何在发布者中使用等待确认特性，以确保发布者发送的消息被所有订阅端确认。

https://github.com/ros2/examples/blob/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_publisher/member_function_with_wait_for_all_acked.cpp

发布者可以使用 ``wait_for_all_acked`` 方法，在因信号关闭之前，于指定的超时时间内等待消息确认。

我们可以通过运行 ``examples_rclcpp_minimal_publisher`` 软件包中的 ``publisher_wait_for_all_acked`` 和 ``subscriber_member_function`` 可执行文件来启动该演示（别忘了先 source 设置文件）：

在一个终端中启动订阅者：

.. code-block:: console

    $ ros2 run examples_rclcpp_minimal_subscriber subscriber_member_function
    [INFO] [1743121567.030751270] [minimal_subscriber]: I heard: 'Hello, world! 0'
    [INFO] [1743121567.530981660] [minimal_subscriber]: I heard: 'Hello, world! 1'
    [INFO] [1743121568.031032935] [minimal_subscriber]: I heard: 'Hello, world! 2'
    [INFO] [1743121568.531048458] [minimal_subscriber]: I heard: 'Hello, world! 3'
    [INFO] [1743121569.031049351] [minimal_subscriber]: I heard: 'Hello, world! 4'
    [INFO] [1743121569.530980327] [minimal_subscriber]: I heard: 'Hello, world! 5'
    [INFO] [1743121570.030825871] [minimal_subscriber]: I heard: 'Hello, world! 6'
    ...

然后在另一个终端中启动发布者：

.. code-block:: console

    $ ros2 run examples_rclcpp_minimal_publisher publisher_wait_for_all_acked
    [INFO] [1743121567.030353553] [minimal_publisher_with_wait_for_all_acked]: Publishing: 'Hello, world! 0'
    [INFO] [1743121567.530420788] [minimal_publisher_with_wait_for_all_acked]: Publishing: 'Hello, world! 1'
    [INFO] [1743121568.030461599] [minimal_publisher_with_wait_for_all_acked]: Publishing: 'Hello, world! 2'
    [INFO] [1743121568.530435646] [minimal_publisher_with_wait_for_all_acked]: Publishing: 'Hello, world! 3'
    [INFO] [1743121569.030431263] [minimal_publisher_with_wait_for_all_acked]: Publishing: 'Hello, world! 4'
    [INFO] [1743121569.530447106] [minimal_publisher_with_wait_for_all_acked]: Publishing: 'Hello, world! 5'
    [INFO] [1743121570.030353934] [minimal_publisher_with_wait_for_all_acked]: Publishing: 'Hello, world! 6'
    ^C[INFO] [1743121570.344981639] [rclcpp]: signal_handler(signum=2)
    [INFO] [1743121570.345398788] [minimal_publisher_with_wait_for_all_acked]: All subscribers acknowledge messages

当发布者被终止时（例如按下 :kbd:`Ctrl-C`），它会在关闭之前等待所有已发送消息的确认。
如果所有订阅者都确认了消息，发布者将打印一条消息，表明所有订阅者都已确认这些消息。
如果没有，它将打印一条消息，表明并非所有订阅者都在指定的超时时间内确认了消息。

相关内容
--------

- `使用 rclpy 的等待确认示例 <https://github.com/ros2/examples/blob/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function_with_wait_for_all_acked.py>`__。
