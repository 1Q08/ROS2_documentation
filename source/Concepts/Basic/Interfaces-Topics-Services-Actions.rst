.. redirect-from::

  How-To-Guides/Topics-Services-Actions

.. _interfaces-topics-services-actions:

接口（主题、服务、动作）
========================

ROS 中的接口定义了节点如何交换数据。
本文介绍 ROS 接口的不同类型以及它们之间的差异。
借助这些信息，您将能够为自己的用途选择合适的接口。

**领域：ROS-framework | 内容类型：concept | 经验等级：beginner**

.. contents:: 目录
   :depth: 2
   :local:

.. toctree::
   :hidden:

   About-Interfaces
   About-Topics
   About-Services
   About-Actions

概述
----

ROS 节点通常通过以下三种接口进行通信：

* 主题：用于连续数据流。
* 服务：用于同步请求/响应交互（很快完成的短任务）。
* 动作：用于带反馈的长时间任务（可能需要一段时间才能完成）。

为保证通信一致性，每种接口都使用 ``.msg``、``.srv`` 或 ``.action`` 文件中提供的定义。

:doc:`了解有关节点的更多信息 <About-Nodes>`

主题
----

主题接口适用于连续数据流，例如传感器数据流或机器人状态。
主题定义存储在 ``.msg`` 文件中。
主题实现发布/订阅模式。
一个节点向主题发布数据，其他节点订阅以接收该数据。
这种接口类型具有以下主要特征：

* 异步、单向通信
* 多个发布者和订阅者可以共享同一个主题

.. mermaid::

   flowchart LR
    P[Publisher node] -->|Publishes messages| T[Topic]
    T -->|Delivers messages| S1[Subscriber node]
    T -->|Delivers messages| S2[Subscriber node]

主题键可以识别某个主题上的各个发布者，因此节点和工具可以区分消息来自哪里。
每个主题键都让多个发布者共享同一主题时，跟踪数据源更容易。

主题统计
--------
主题统计是内置度量，用于帮助您理解订阅接收消息时消息的行为。
启用后，它会自动跟踪两件事：

:消息年龄：消息到达时基于时间戳计算它有多老。
:消息周期：连续进入消息的时间间隔。

对于消息年龄和消息周期，ROS 会使用移动窗口在每次新消息到来时计算平均值、最小值、最大值、标准差以及采样数量。
这些计算在常量时间和内存中完成，使用专用工具。
当您为某个订阅启用主题统计时，ROS 会以固定间隔在一个统计主题上发布收集到的 ``MetricsMessage``。
这让您可以清楚了解时序模式、延迟和不规则性，更容易评估系统性能或诊断与消息流相关的问题。

.. tip::

   默认间隔为 1 秒。
   默认统计主题为 ``/statistics``。

:doc:`了解如何启用主题统计 </Tutorials/Advanced/Topic-Statistics-Tutorial/Topic-Statistics-Tutorial>`

服务
----

服务接口适用于同步请求/响应交互，例如想向某个特定机器人发送查询并获取其配置时。
服务定义存储在 ``.srv`` 文件中。
服务实现请求/响应模式。
客户端发送请求，服务器回复响应。
这种接口类型具有以下主要特征：

* 同步通信
* 非常适合需要确认或根据请求返回结果的短期操作

.. mermaid::

   sequenceDiagram
    participant Service client
    participant Service server
    Service client->>Service server: Request
    Service server-->>Service client: Response

动作
----

动作接口适用于带反馈的长时间任务，例如将机器人移动到指定位置，或要求机器人执行复杂运动。
动作定义存储在 ``.action`` 文件中。
动作允许客户端发送目标、在执行期间接收反馈、必要时取消，并在可用时返回结果。
这种接口类型具有以下主要特征：

* 异步，带反馈和结果
* 适用于需要较长运行时间的操作

.. mermaid::

   sequenceDiagram
    participant Action client
    participant Action server
    Client->>Action Server: Sends a goal
    Action server-->>Action client: Provides feedback (periodic)
    Action server-->>Action client: Sends a result

ROS 接口之间的关键差异
----------------------

三种接口都能在节点之间进行通信，但每种接口都有不同目的。
下表总结了 ROS 接口类型之间的差异：

+--------------+----------------------+-----------------------+-----------------+--------------------+---------------+
|              | Pattern              | Direction             | Provided result | Typical use case   | Cancellation  |
+==============+======================+=======================+=================+====================+===============+
| **Topics**   | Publish/Subscribe    | One-way               | No              | Continuous data    | Not supported |
+--------------+----------------------+-----------------------+-----------------+--------------------+---------------+
| **Services** | Request/Response     | Two-way               | Yes             | Quick queries      | Not supported |
+--------------+----------------------+-----------------------+-----------------+--------------------+---------------+
| **Actions**  | Goal/Feedback/Result | Two-way with feedback | Yes             | Long-running tasks | Supported     |
+--------------+----------------------+-----------------------+-----------------+--------------------+---------------+
