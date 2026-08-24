.. redirect-from::

    About-Topic-Statistics
    Concepts/About-Topic-Statistics

话题统计
========

.. contents:: 目录
   :local:

概述
----

ROS 2 为任何订阅接收到的消息提供了集成的统计测量。
允许用户收集订阅统计信息，可以帮助他们评估系统性能，或辅助诊断现有的问题。

提供的测量项包括：接收消息年龄和接收消息周期。
对于每个测量项，提供的统计数据包括平均值、最大值、最小值、标准差和样本数。
这些统计量在滑动窗口中计算。

统计量的计算方式
----------------

每组统计量都借助 `libstatistics_collector <https://github.com/ros-tooling/libstatistics_collector>`__ 包中实现的工具，以恒定时间和恒定内存来计算。
当订阅收到一条新消息时，它就成为当前测量窗口中的一个新样本。
计算的平均值就是一个简单的 `移动平均 <https://en.wikipedia.org/wiki/Moving_average>`__。
最大值、最小值和样本数在每收到一个新样本时更新，而标准差则使用 `Welford 在线算法 <https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm>`__ 计算。

计算出的统计量类型
------------------

* 接收消息周期

  * 单位：毫秒
  * 使用系统时钟来测量收到的消息之间的周期

* 接收消息年龄

  * 单位：毫秒
  * 要求消息的头字段中填充了时间戳，以便计算发布者发出消息的年龄

行为
----

默认情况下，话题统计测量未启用。
通过订阅配置选项为特定节点启用此功能后，该特定订阅的接收消息年龄和接收消息周期测量都会被启用。

数据以 `statistics_msg/msg/MetricsMessage
<https://github.com/ros2/rcl_interfaces/blob/{REPOS_FILE_BRANCH}/statistics_msgs/msg/MetricsMessage.msg>`__ 的形式，以可配置的周期（默认 1 秒）发布到可配置的话题（默认 ``/statistics``）。
请注意，发布周期也用作样本采集窗口的周期。

由于接收消息周期要求消息头字段中有时间戳，因此会发布空数据。
也就是说，如果没有找到时间戳，所有统计值都是 NaN。
发布 NaN 值而不是完全不发布，可以避免“信号缺失”的问题，其目的是明确表明无法完成测量。

接收消息周期统计量在每个窗口的第一个样本不会产生测量值。
这是因为计算该统计量需要知道上一条消息到达的时间，因此窗口中的后续样本才会产生测量值。

与 ROS 1 的比较
---------------

与 ROS 1 的 `话题统计 <https://wiki.ros.org/Topics#Topic_statistics>`__ 类似，消息年龄和消息周期都会计算，只不过是在订阅侧计算。
目前不提供其他 ROS 1 指标，例如丢弃的消息数量或流量大小。

支持情况
--------

此功能目前在 ROS 2 Foxy 中仅支持 C++（rclcpp）。
未来的工作和改进（例如 Python 支持）可以
`在这里 <https://github.com/ros2/ros2/issues/917>`__ 找到。
