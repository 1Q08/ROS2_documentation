.. redirect-from::

  Guides/Overriding-QoS-Policies-For-Recording-And-Playback
  Tutorials/Ros2bag/Overriding-QoS-Policies-For-Recording-And-Playback

.. _ROS2Bag-QoS-Override:

rosbag2：覆盖 QoS 策略
======================

**目标：** 为录制和回放覆盖 Ros2Bag 的 QoS 配置文件设置。

.. contents:: Contents
   :depth: 2
   :local:


背景
----

随着 DDS 被引入 ROS 2，在录制和回放数据时需要考虑发布者/订阅者节点的服务质量（QoS）兼容性。
有关 QoS 如何工作的更多详细信息，请参见 :doc:`此处 <../Concepts/Intermediate/About-Quality-of-Service-Settings>`。
就本指南而言，只需要知道只有可靠性（reliability）和持久性（durability）策略会影响发布者/订阅者是否兼容并能否相互接收数据。

Ros2Bag 在录制/播放话题数据时会调整其请求/提供的 QoS 配置文件，以防止消息丢失。
在回放期间，Ros2Bag 还尝试保留话题原本提供的策略。
某些情况可能需要指定明确的 QoS 配置文件设置，以便 Ros2Bag 能够录制/播放话题。
这些 QoS 配置文件覆盖可以通过 CLI 使用 ``--qos-profile-overrides-path`` 标志来指定。

使用 QoS 覆盖
-------------

配置文件覆盖的 YAML 模式是一个话题名称字典，其中包含每个 QoS 策略的键/值对：

.. code-block:: yaml

    topic_name: str
      qos_policy_name: str
      ...
      qos_duration: object
        sec: int
        nsec: int

如果没有指定某个策略值，该值将回退到 Ros2Bag 使用的默认值。
如果你指定了一个基于时长的策略，例如 ``deadline`` 或 ``lifespan``，你需要同时指定秒和纳秒。
策略值由策略的短键确定，这些短键可以使用 ``ros2topic`` 动词（例如 ``ros2 topic pub --help``）找到。
所有值都在下面列出以供参考。

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

考虑一个话题 ``/talker`` 提供 ``transient_local`` 的持久性（Durability）策略。
ROS 2 发布者默认请求 ``volatile`` 持久性。

.. code-block:: console

    $ ros2 topic pub -r 0.1 --qos-durability transient_local /talker std_msgs/String "data: Hello World"

为了让 Ros2Bag 录制这些数据，我们希望像下面这样覆盖该特定话题的录制策略：

.. code-block:: yaml

    # durability_override.yaml
    /talker:
      durability: transient_local
      history: keep_all

并从 CLI 调用它：

.. code-block:: console

    $ ros2 bag record -a -o my_bag --qos-profile-overrides-path durability_override.yaml

如果我们想回放 bag 文件，但使用不同的可靠性（Reliability）策略，我们可以指定一个：

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
