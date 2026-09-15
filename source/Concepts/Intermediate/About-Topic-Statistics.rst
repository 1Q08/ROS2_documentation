.. redirect-from::

    About-Topic-Statistics
    Concepts/About-Topic-Statistics

话题统计信息
============

.. contents:: 目录
   :local:

概述
----

ROS 2 提供了对任何订阅所收到消息的统计信息的集成度量。
让用户能够收集订阅统计信息，使他们可以描述系统性能，或帮助诊断当前存在的任何问题。

所提供的度量包括「收到消息的年龄」（received message age）和「收到消息的周期」（received message period）。
对每项度量，所提供的统计量包括平均值、最大值、最小值、标准差和样本数。
这些统计量是在滑动窗口中计算的。

统计信息是如何计算的
--------------------

每组统计量都是利用 `libstatistics_collector <https://github.com/ros-tooling/libstatistics_collector>`__ 包中所实现的工具，以常数时间和常数内存计算得出的。
当订阅收到一条新消息时，这就是当前度量窗口中的一个新样本。
所计算的平均值就是一个 `移动平均 <https://en.wikipedia.org/wiki/Moving_average>`__。
最大值、最小值和样本数在收到每个新样本时更新，而标准差则使用 `Welford 在线算法 <https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance#Welford's_online_algorithm>`__ 计算。

所计算的统计信息类型
--------------------

* 收到消息的周期

  * 单位：毫秒
  * 使用系统时钟来测量收到消息之间的周期

* 收到消息的年龄

  * 单位：毫秒
  * 要求消息在 header 字段中填充了时间戳，以便计算消息从发布者发出后的年龄

行为
----

默认情况下，话题统计信息度量并未启用。
通过订阅配置选项为特定节点启用该功能后，针对该特定订阅的「收到消息的年龄」与「收到消息的周期」两项度量都会被启用。

数据以 `statistics_msg/msg/MetricsMessage
<https://github.com/ros2/rcl_interfaces/blob/{REPOS_FILE_BRANCH}/statistics_msgs/msg/MetricsMessage.msg>`__ 的形式，按可配置的周期（默认 1 秒）发布到可配置的话题（默认 ``/statistics``）。
请注意，发布周期同时也用作样本收集窗口的周期。

由于「收到消息的周期」要求 header 字段中有消息时间戳，因此会发布空数据。
也就是说，如果找不到时间戳，所有统计值都为 NaN。
发布 NaN 值而不是完全不发布，避免了「无信号」问题，其用意是明确表明该项度量无法进行。

「收到消息的周期」统计量在窗口中的第一个样本不会产生度量结果。
这是因为计算该统计量需要知道上一条消息到达的时间，所以窗口中的后续样本才会产生度量结果。

与 ROS 1 的对比
---------------

与 ROS 1 的 `话题统计信息 <https://wiki.ros.org/Topics#Topic_statistics>`__ 类似，消息年龄和消息周期都会被计算，只不过是从订阅侧计算。
其他 ROS 1 指标，例如丢包数或流量，目前尚未提供。

支持情况
--------

该功能目前在 ROS 2 Foxy 中仅支持 C++（rclcpp）。
未来的工作与改进，例如 Python 支持，可以在
`此处 <https://github.com/ros2/ros2/issues/917>`__ 查看。
