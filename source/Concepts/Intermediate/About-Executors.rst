.. redirect-from::

   Concepts/About-Executors

执行器
======

.. contents:: 目录
   :local:

概述
----

ROS 2 中的执行管理由执行器处理。
执行器使用底层操作系统中的一个或多个线程，按照传入消息和事件来调用订阅、定时器、服务服务器、动作服务器等回调。
显式执行器类（在 rclcpp 中为 `executor.hpp <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp/include/rclcpp/executor.hpp>`_，在 rclpy 中为 `executors.py <https://github.com/ros2/rclpy/blob/{REPOS_FILE_BRANCH}/rclpy/rclpy/executors.py>`_，在 rclc 中为 `executor.h <https://github.com/ros2/rclc/blob/master/rclc/include/rclc/executor.h>`_）相比 ROS 1 中的 spin 机制，提供了更强的执行管理控制能力，尽管基本 API 极其相似。

下面，我们重点关注 C++ 客户端库 *rclcpp*。

基本用法
--------

最简单的情况是，主线程通过调用 ``rclcpp::spin(..)`` 来处理节点收到的消息和事件，如下所示：

.. code-block:: cpp

   int main(int argc, char* argv[])
   {
      // 一些初始化。
      rclcpp::init(argc, argv);
      ...

      // 实例化一个节点。
      rclcpp::Node::SharedPtr node = ...

      // 运行执行器。
      rclcpp::spin(node);

      // 关闭并退出。
      ...
      return 0;
   }

调用 ``spin(node)`` 基本上等价于实例化并调用单线程执行器，这也是最简单的执行器：

.. code-block:: cpp

   rclcpp::executors::SingleThreadedExecutor executor;
   executor.add_node(node);
   executor.spin();

通过调用执行器实例的 ``spin()``，当前线程会开始向 rcl 和中间件层查询传入消息和其他事件，并调用相应的回调函数，直到节点关闭。
为避免影响中间件的 QoS 配置，传入消息不会先存入客户端库层的队列，而是保留在中间件中，直到回调函数取走并处理。
（这是与 ROS 1 的关键区别。）
*等待集合* 用于通知执行器中间件层上的消息是否可用，每个队列对应一个二进制标志位。
*等待集合* 也用于检测定时器是否到时。

.. image:: ../images/executors_basic_principle.png

单线程执行器也会被容器进程用于 :doc:`组件 <./About-Composition>`，也就是所有在没有显式 main 函数时创建和执行节点的场景。

.. _TypesOfExecutors:

执行器类型
----------

目前，rclcpp 提供了三种执行器类型，它们都派生自共享父类：

.. graphviz::

   digraph Flatland {

      Executor -> SingleThreadedExecutor [dir = back, arrowtail = empty];
      Executor -> MultiThreadedExecutor [dir = back, arrowtail = empty];
      Executor -> StaticSingleThreadedExecutor [dir = back, arrowtail = empty];
      Executor  [shape=polygon,sides=4];
      SingleThreadedExecutor  [shape=polygon,sides=4];
      MultiThreadedExecutor  [shape=polygon,sides=4];
      StaticSingleThreadedExecutor  [shape=polygon,sides=4];

      }

*多线程执行器* 创建可配置数量的线程，以允许并行处理多个消息或事件。
*静态单线程执行器* 优化了扫描节点结构的运行时成本，例如扫描订阅、定时器、服务服务器、动作服务器等。
它只会在添加节点时扫描一次，而其他两种执行器会定期扫描这些变化。
因此，静态单线程执行器应仅在节点在初始化时即可创建所有订阅、定时器等时使用。

所有三种执行器都可以通过为每个节点调用 ``add_node(..)`` 来服务多个节点。

.. code-block:: cpp

   rclcpp::Node::SharedPtr node1 = ...
   rclcpp::Node::SharedPtr node2 = ...
   rclcpp::Node::SharedPtr node3 = ...

   rclcpp::executors::StaticSingleThreadedExecutor executor;
   executor.add_node(node1);
   executor.add_node(node2);
   executor.add_node(node3);
   executor.spin();

在上述示例中，静态单线程执行器的一个线程同时服务三个节点。
对于多线程执行器，其并行度取决于回调组。

回调组
------

ROS 2 允许按组组织节点的回调。
在 rclcpp 中，可以使用 Node 类的 ``create_callback_group`` 函数创建这样的 *回调组*。
在 rclpy 中，则可通过特定回调组类型的构造器来做同样的事情。
回调组必须在节点整个执行期间保存下来（例如作为类成员），否则执行器将无法触发这些回调。
随后，在创建订阅、定时器等时可指定该回调组，例如通过订阅选项：

.. tabs::

   .. group-tab:: C++

      .. code-block:: cpp

        my_callback_group = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

        rclcpp::SubscriptionOptions options;
        options.callback_group = my_callback_group;

        my_subscription = create_subscription<Int32>("/topic", rclcpp::SensorDataQoS(),
                                                     callback, options);
   .. group-tab:: Python

      .. code-block:: python

        my_callback_group = MutuallyExclusiveCallbackGroup()
        my_subscription = self.create_subscription(Int32, "/topic", self.callback, qos_profile=1,
                                                   callback_group=my_callback_group)

所有未指明回调组的订阅、定时器等都会被分配到 *默认回调组*。
在 rclcpp 中，可通过 ``NodeBaseInterface::get_default_callback_group()`` 查询默认回调组，
在 rclpy 中可通过 ``Node.default_callback_group`` 查询。

回调组有两种类型，类型必须在实例化时指定：

* *互斥：* 同一组的回调不能并行执行。
* *可重入：* 同一组的回调可以并行执行。

不同回调组中的回调通常都可以并行执行。
多线程执行器使用线程池，按这些条件处理尽可能多的回调并行执行。
有关高效使用回调组的技巧，请参阅 :doc:`使用回调组 <../../How-To-Guides/Using-callback-groups>`。

rclcpp 中的执行器基类还有 ``add_callback_group(..)`` 函数，允许将回调组分发到不同的执行器。
通过使用操作系统调度器配置底层线程，可以给特定回调优先级，让例如控制循环的订阅与定时器优先于节点中的其他订阅和标准服务。
`examples_rclcpp_cbg_executor 包 <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclcpp/executors/cbg_executor>`_ 提供了该机制的示例。

调度语义
--------

如果回调的处理时间短于消息和事件发生的周期，执行器基本上按 FIFO 顺序处理它们。
然而，如果某些回调的处理时间更长，消息和事件会在栈的底层队列中排队。
等待集合机制对这些队列只报告很少的信息给执行器。
具体而言，它只报告某一主题是否存在消息。
执行器据此以轮询方式处理消息（包括服务与动作），但并非 FIFO 顺序。
下图可视化说明这一调度语义。

.. image:: ../images/executors_scheduling_semantics.png

这种语义最早由 `Casini 等人在 ECRTS 2019 的论文 <https://drops.dagstuhl.de/opus/volltexte/2019/10743/pdf/LIPIcs-ECRTS-2019-6.pdf>`_ 描述。
（注：该论文还解释了计时器事件优先于所有其他消息。
`这种优先级在 Eloquent 中已被移除。 <https://github.com/ros2/rclcpp/pull/841>`_）


展望
----

虽然 rclcpp 的三种执行器适用于大多数应用，但也有一些问题使它们不适用于实时应用，这些应用需要定义良好的执行时间、确定性以及对执行顺序的自定义控制。
下面总结一些问题：

1. 调度语义复杂且混合。
   理想情况下，您希望有明确的调度语义以便进行正式时序分析。
2. 回调可能受优先级反转影响。
   高优先级回调可能会被低优先级回调阻塞。
3. 对回调执行顺序没有显式控制。
4. 对特定主题触发没有内置控制。

此外，执行器在 CPU 和内存上的开销相当可观。
静态单线程执行器可显著降低此类开销，但对某些应用来说仍可能不够。

这些问题部分已由以下发展得到解决：

* `rclcpp WaitSet <https://github.com/ros2/rclcpp/blob/{REPOS_FILE_BRANCH}/rclcpp/include/rclcpp/wait_set.hpp>`_：rclcpp 的 ``WaitSet`` 类允许直接等待订阅、定时器、服务服务器、动作服务器等，而不是使用执行器。
  它可用于实现确定性的、用户定义的处理序列，甚至可同时处理不同订阅消息。
  `examples_rclcpp_wait_set 包 <https://github.com/ros2/examples/tree/{REPOS_FILE_BRANCH}/rclcpp/wait_set>`_ 提供了数个此类用户级等待集合机制的示例。
* `rclc Executor <https://github.com/ros2/rclc/blob/master/rclc/include/rclc/executor.h>`_：来自 C 客户端库 *rclc* 的该执行器，专为 micro-ROS 开发，提供对回调执行顺序的细粒度控制，并允许通过自定义触发条件激活回调。
  此外，它还实现了逻辑执行时间（LET）语义。

更多信息
--------

* Michael Pöhnl 等人：`"ROS 2 Executor: How to make it efficient, real-time and deterministic?" <https://www.apex.ai/roscon-21>`_。
  ROS World 2021 研讨会。
  虚拟活动。
  2021 年 10 月 19 日。
* Ralph Lange：`"Advanced Execution Management with ROS 2" <https://www.youtube.com/watch?v=Sz-nllmtcc8&t=109s>`_。
  ROS Industrial Conference。
  虚拟活动。
  2020 年 12 月 16 日。
* Daniel Casini、Tobias Blass、Ingo Lütkebohle 和 Björn Brandenburg：`"Response-Time Analysis of ROS 2 Processing Chains under Reservation-Based Scheduling" <https://drops.dagstuhl.de/opus/volltexte/2019/10743/pdf/LIPIcs-ECRTS-2019-6.pdf>`_，Proceedings of 31st ECRTS 2019，德国斯图加特，2019 年 7 月。
