.. redirect-from::

  Guides/Overriding-QoS-Policies-For-Recording-And-Playback
  Tutorials/Ros2bag/Overriding-QoS-Policies-For-Recording-And-Playback

.. _ROS2Bag-QoS-Override:

rosbag2：覆盖 QoS 策略
======================

**目标：** 覆盖 Ros2Bag 用于录制和回放的 QoS 配置文件设置。

.. contents:: 目录
   :depth: 2
   :local:


背景
----

随着 DDS 被引入 ROS 2，在录制和回放数据时需要考虑发布者/订阅者节点的服务质量（QoS）兼容性。
有关 QoS 工作原理的更多细节可以在 :doc:`此处 <../Concepts/Intermediate/About-Quality-of-Service-Settings>` 找到。
就本指南而言，只需知道只有可靠性（reliability）和持久性（durability）策略会影响发布者/订阅者是否兼容以及能否从彼此接收数据就够了。

Ros2Bag 在录制/回放某个话题的数据时会调整其请求/提供的 QoS 配置文件，以防止消息丢失。
在回放期间，Ros2bag 还会尝试保留该话题最初提供的策略。
某些情况下可能需要指定明确的 QoS 配置文件设置，以便 Ros2Bag 能够录制/回放话题。
这些 QoS 配置文件覆盖项可以通过 CLI 使用 ``--qos-profile-overrides-path`` 标志来指定。

使用 QoS 覆盖
-------------

配置文件覆盖项的 YAML 模式是一个以话题名称为键、每个 QoS 策略为键/值对的字典：

.. code-block:: yaml

    topic_name: str
      qos_policy_name: str
      ...
      qos_duration: object
        sec: int
        nsec: int

如果未指定某个策略的值，该值将回退为 Ros2Bag 使用的默认值。
如果你指定基于时长（Duration）的策略，例如 ``deadline`` 或 ``lifespan``，则需要同时指定秒和纳秒。
策略值由该策略的短键决定，可以使用 ``ros2topic`` 动词（例如 ``ros2 topic pub --help``）来查找。
所有值都在下面列出，以供参考。

.. code-block:: yaml

    history: [keep_all, keep_last]
    depth: int
    reliability: [system_default, reliable, best_effort, unknown]
    durability: [system_default, transient_local, volatile, unknown]
    deadline:
      sec: int
      nsec: int
    lifespan:
      sec: int
      nsec: int
    liveliness: [system_default, automatic, manual_by_topic, unknown]
    liveliness_lease_duration:
      sec: int
      nsec: int
    avoid_ros_namespace_conventions: [true, false]

示例
----

考虑一个提供 ``transient_local`` 持久性策略的话题 ``/talker``。
ROS 2 发布者默认请求 ``volatile`` 持久性。

.. code-block:: console

    $ ros2 topic pub -r 0.1 --qos-durability transient_local /talker std_msgs/String "data: Hello World"

为了让 Ros2Bag 能够录制该数据，我们需要为该特定话题覆盖录制策略，如下所示：

.. code-block:: yaml

    # durability_override.yaml
    /talker:
      durability: transient_local
      history: keep_all

并从 CLI 调用它：

.. code-block:: console

    $ ros2 bag record -a -o my_bag --qos-profile-overrides-path durability_override.yaml

如果我们想回放该 bag 文件，但使用不同的可靠性策略，可以这样指定；

.. code-block:: yaml

    # reliability_override.yaml
    /talker:
      reliability: best_effort
      history: keep_all

并从 CLI 调用它：

.. code-block:: console

    $ ros2 bag play --qos-profile-overrides-path reliability_override.yaml my_bag

我们可以使用 ``ros2 topic`` 查看结果

.. code-block:: console

    $ ros2 topic echo --qos-reliability best_effort /talker std_msgs/String
