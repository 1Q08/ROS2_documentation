等待确认
========

**目标：** 等待发布者发送的消息得到确认。

**教程级别：** 高级

**时间：** 10 分钟

.. contents:: 目录
   :depth: 1
   :local:

概述
----

在发布者-订阅者架构中，消息从发布者发送到订阅者，而发布者没有任何内置机制来确认订阅者已经收到了消息。
此功能使发布者能够等待其发送的消息得到确认。
这在发布者需要确保订阅者已收到消息后才能继续后续操作（例如发送更多消息或执行其他操作）的场景中非常有用。

RMW 支持
--------

等待确认需要 RMW 实现的支持。

.. list-table::  等待确认支持状态
   :widths: 25 25

   * - rmw_fastrtps
     - 支持
   * - rmw_connextdds
     - 支持
   * - rmw_cyclonedds
     - 支持

发布者的 :ref:`QoS 可靠性策略 <about_qos_policies>` 需要为 ``RELIABLE`` 才能使用等待确认功能，否则发布者不会等待确认。

安装演示
--------

有关安装 ROS 2 的详细信息，请参阅 :doc:`安装说明 <../../Installation>`。

如果你是通过软件包安装的 ROS 2，请确保已安装 ``ros-{DISTRO}-examples-rclcpp-minimal-publisher`` 和 ``ros-{DISTRO}-examples-rclcpp-minimal-subscriber``。
如果你下载了归档文件或从源代码构建了 ROS 2，它将已经是安装的一部分。

运行演示
--------

本演示展示如何在发布者中使用等待确认功能，以确保发布者发送的消息被所有订阅者确认。

https://github.com/ros2/examples/blob/{REPOS_FILE_BRANCH}/rclcpp/topics/minimal_publisher/member_function_with_wait_for_all_acked.cpp

发布者可以使用 ``wait_for_all_acked`` 方法，在指定的超时时间内等待消息确认，然后再因信号而关闭。

我们可以通过运行 ``examples_rclcpp_minimal_publisher`` 软件包中的 ``publisher_wait_for_all_acked`` 和 ``subscriber_member_function`` 可执行文件来启动演示（别忘了先 source 安装文件）：

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

当发布者被终止（例如按下 :kbd:`Ctrl-C`）时，它将在关闭前等待所有已发送消息的确认。
如果所有订阅者都确认了这些消息，发布者将打印一条消息，表示所有订阅者均已确认这些消息。
如果没有，它将打印一条消息，表示在指定的超时时间内并非所有订阅者都确认了这些消息。

相关内容
--------

- `使用 rclpy 的等待确认示例 <https://github.com/ros2/examples/blob/{REPOS_FILE_BRANCH}/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function_with_wait_for_all_acked.py>`__。
