.. _iron-release:

Iron Irwini（``iron``）
=======================

.. toctree::
   :hidden:

   Iron-Irwini-Complete-Changelog

.. contents:: 目录
   :depth: 2
   :local:

*Iron Irwini* 是 ROS 2 的第九个发行版。
以下内容介绍了自上一个发行版以来 Iron Irwini 中的重要变更和新特性。
自 Humble 以来的全部变更列表，请参阅 :doc:`完整变更日志 <Iron-Irwini-Complete-Changelog>`。

支持的平台
----------

根据 `平台支持层级 <../The-ROS2-Project/Platform-Support-Tiers>`，Iron Irwini 支持以下平台：

Tier 1 平台：

* Ubuntu 22.04 (Jammy)：``amd64`` 和 ``arm64``
* Windows 10 (Visual Studio 2019)：``amd64``

Tier 2 平台：

* RHEL 9：``amd64``

Tier 3 平台：

* macOS：``amd64``
* Debian Bullseye：``amd64``

目标平台：

+--------------+------------------+---------------+------------------+------------+-----------------+----------------+
| Architecture | Ubuntu Jammy     | Windows 10    | RHEL 9           | macOS      | Debian Bullseye | OpenEmbedded / |
|              | (22.04)          | (VS2019)      |                  |            | (11)            | Yocto Project  |
+==============+==================+===============+==================+============+=================+================+
| amd64        | Tier 1 [d][a][s] | Tier 1 [a][s] | Tier 2 [d][a][s] | Tier 3 [s] | Tier 3 [s]      | Tier 3 [s]     |
+--------------+------------------+---------------+------------------+------------+-----------------+----------------+
| arm64        | Tier 1 [d][a][s] |               |                  |            | Tier 3 [s]      | Tier 3 [s]     |
+--------------+------------------+---------------+------------------+------------+-----------------+----------------+
| arm32        | Tier 3 [s]       |               |                  |            | Tier 3 [s]      | Tier 3 [s]     |
+--------------+------------------+---------------+------------------+------------+-----------------+----------------+

以下指标说明了每个平台可用的交付机制。

\" \[d\] \" 将为提交到 rosdistro 的软件包提供平台特定的（Debian、RPM 等）软件包。

\" \[a\] \" 以每个平台一个压缩包的形式提供二进制发行包，其中包含 Iron ROS 2 repos 文件中的所有软件包[^12]。

\" \[s\] \" 从源码编译。

中间件实现支持：

+--------------------------+-------------------------+---------------+-----------------------------+------------------------------+
| Middleware Library       | Middleware Provider     | Support Level | Platforms                   | Architectures                |
+==========================+=========================+===============+=============================+==============================+
| rmw_fastrtps_cpp*        | eProsima Fast-DDS       | Tier 1        | All Platforms               | All Architectures            |
+--------------------------+-------------------------+---------------+-----------------------------+------------------------------+
| rmw_cyclonedds_cpp       | Eclipse Cyclone DDS     | Tier 1        | All Platforms               | All Architectures            |
+--------------------------+-------------------------+---------------+-----------------------------+------------------------------+
| rmw_connextdds           | RTI Connext             | Tier 1        | Ubuntu, Windows, and macOS  | All Architectures except     |
|                          |                         |               |                             | arm64                        |
+--------------------------+-------------------------+---------------+-----------------------------+------------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-DDS       | Tier 2        | All Platforms               | All Architectures            |
+--------------------------+-------------------------+---------------+-----------------------------+------------------------------+
| rmw_gurumdds_cpp         | GurumNetworks GurumDDS  | Tier 3        | Ubuntu and Windows          | All Architectures except     |
|                          |                         |               |                             | arm32                        |
+--------------------------+-------------------------+---------------+-----------------------------+------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持层级。例如，Tier 2 平台上的 Tier 1 中间件实现只能获得 Tier 2 级别的支持。

最低语言要求：

- C++17
- Python 3.8

依赖要求：

+-------------------+-----------------------+-----------------------------------------------------------+
|                   | Required Support      | Recommended Support                                       |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| Package           | Ubuntu    | Windows   | RHEL 9  | macOS**   | Debian          | OpenEmbedded**    |
|                   | Jammy     | 10**      |         |           | Bullseye        |                   |
+===================+===========+===========+=========+===========+=================+===================+
| CMake             | 3.22.1    | 3.22.0    | 3.20.2  | 3.14.4    | 3.18.4          | 3.22.3 / 3.16.5***|
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| EmPY              | 3.3.4     | 3.3.2     | 3.3.4   | 3.3.2                                           |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| Gazebo Classic    | 11.x.x*   | N/A       | N/A     | 11.x.x    | 11.x.x*         | N/A               |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| Gazebo (Ignition) | Fortress* | N/A       | N/A     | Fortress* | Fortress*       | N/A               |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| NumPy             | 1.21.5    | 1.18.4    | 1.20.1  | 1.18.4    | 1.19.5          | N/A               |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| Ogre              | 1.12.1*                                                       | N/A               |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| OpenCV            | 4.5.4     | 3.4.6*    | 4.6.0   | 4.2.0     | 4.5.1           | 4.1.0 / 3.2.0***  |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| OpenSSL           | 3.0.2     | 1.1.1l    | 3.0.1   | 1.1.1f    | 1.1.1i          | 1.1.1d / 1.1.1b***|
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| Python            | 3.10.6    | 3.8.3     | 3.9.14  | 3.10.8    | 3.9.1           | 3.8.2 / 3.7.5***  |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| Qt                | 5.15.3    | 5.12.12   | 5.15.3  | 5.12.3    | 5.15.2          | 5.14.1 / 5.12.5***|
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
|                               | **Linux only**                                                        |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| PCL               | 1.12.1    | N/A       | 1.12.0  | N/A       | 1.11.1          | 1.10.0            |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| **RMW DDS Middleware**                                                                                |
+-------------------+-----------------------------------------------------------------------------------+
| Cyclone DDS       | 0.9                                                                               |
+-------------------+-----------------------------------------------------------------------------------+
| Fast-DDS          | 2.8                                                                               |
+-------------------+---------------------------------------------+-------------------------------------+
| Connext DDS       | 6.0.1                                       | N/A                                 |
+-------------------+-----------------------+---------------------+-------------------------------------+
| Gurum DDS         | 2.8.x                 | N/A                                                       |
+-------------------+-----------------------+-----------------------------------------------------------+

\" \* \" 表示这不是上游版本（即官方操作系统仓库中提供的版本），而是由 OSRF 或社区发行的软件包（在自定义仓库上构建并分发的软件包）。

\" \*\* \" 表示该依赖可能会经历多个版本变更，因为该依赖使用的包管理器会持续更新，而没有稳定的 API。

\" \*\*\* \" webOS OSE 提供此不同版本。

本文档仅记录 ROS 发行版首次发布时的版本，不会随依赖的演进而更新。
因此这些版本是一个最低水位线。

依赖使用的包管理器：

- Ubuntu、Debian：apt
- Windows：Chocolatey、pip
- macOS：Homebrew、pip
- RHEL：dnf
- OpenEmbedded：opkg

构建系统支持：

- ament_cmake
- cmake
- setuptools

安装
----

`安装 Iron Irwini <../../iron/Installation.html>`__

此 ROS 2 发行版中的新特性
-------------------------

Python 软件包的 API 文档生成
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 已经多个发行版为 C++ 软件包提供自动 API 文档，例如 https://docs.ros.org/en/rolling/p/rclcpp/generated/index.html。
Iron 也同样为 Python 软件包增加了自动 API 文档，例如 https://docs.ros.org/en/rolling/p/rclpy/rclpy.html。

更多细节请参阅 https://github.com/ros-infrastructure/rosdoc2/pull/28、https://github.com/ros-infrastructure/rosdoc2/pull/49、https://github.com/ros-infrastructure/rosdoc2/pull/51 和 https://github.com/ros-infrastructure/rosdoc2/pull/52。

服务内省
^^^^^^^^

现在可以按服务启用服务内省。
启用后，用户可以查看与以下行为相关的元数据：客户端请求服务、服务端接受请求、服务端发送响应以及客户端接受响应。
此外，还可以选择内省客户端/服务端请求/响应的内容。
所有信息都发布在一个根据服务名称生成的隐藏话题上。
因此，如果服务名为 ``/myservice``，那么信息将发布在 ``/myservice/_service_event`` 上。

请注意，此功能默认禁用；要启用它，用户必须在创建服务客户端或服务端后调用 ``configure_introspection``。
https://github.com/ros2/demos/tree/iron/demo_nodes_cpp/src/services （C++）和 https://github.com/ros2/demos/blob/iron/demo_nodes_py/demo_nodes_py/services/introspection.py （Python）中有展示如何实现的示例。

更多信息请参阅 `REP 2012 <https://github.com/ros-infrastructure/rep/pull/360>`__ 以及跟踪缺陷 https://github.com/ros2/ros2/issues/1285。

设置参数前后的回调支持
^^^^^^^^^^^^^^^^^^^^^^

在过去的多个发行版中，用户可以注册一个回调，当节点上的参数被外部实体（如 ``ros2 param set``）修改时该回调会被调用。
该回调可以检查被修改的参数类型和值，并在其中某个参数不符合特定条件时拒绝整批修改。
然而，它无法修改参数列表，也不应修改状态（因为在设置回调之后可能还有其他回调会拒绝这些参数）。

此发行版新增了前置和后置回调。
回调按以下顺序调用：

* “pre”设置参数回调，可以根据任意条件修改参数列表。
* “set”设置参数回调，不能修改列表，只能根据参数的类型和值接受或拒绝参数（这是现有的回调）。
* “post”设置参数回调，可以根据参数修改状态，仅在前两个回调都成功时才会被调用。

https://github.com/ros2/demos/blob/iron/demo_nodes_cpp/src/parameters/set_parameters_callback.cpp （C++）和 https://github.com/ros2/demos/blob/iron/demo_nodes_py/demo_nodes_py/parameters/set_parameters_callback.py （Python）中有实际应用的示例。

更多信息请参阅 https://github.com/ros2/rclcpp/pull/1947、https://github.com/ros2/rclpy/pull/966 和 https://github.com/ros2/demos/pull/565。

改进的发现选项
^^^^^^^^^^^^^^

以前的 ROS 2 版本提供了有限的发现选项。
基于 DDS 的 RMW 实现的默认行为是发现可通过组播到达的任何节点。
可以通过设置环境变量 ``ROS_LOCALHOST_ONLY`` 将其限制在同一台机器上，但任何其他配置都需要直接配置中间件，通常是通过中间件特定的 XML 文件和环境变量。
ROS Iron 保留了相同的默认发现行为，但弃用了 ``ROS_LOCALHOST_ONLY``，转而采用更细粒度的选项。

* ``ROS_AUTOMATIC_DISCOVERY_RANGE`` 控制 ROS 节点尝试相互发现的范围。有效选项为：

  * ``SUBNET`` - 默认值；对于基于 DDS 的中间件，它将发现可通过组播到达的任何节点。
  * ``LOCALHOST`` - 仅尝试发现同一台机器上的其他节点。
  * ``OFF`` - 不尝试自动发现任何其他节点，即使在同一台机器上也是如此。
  * ``SYSTEM_DEFAULT`` - 不更改任何发现设置。 当你已经为中间件自定义了设置，且不希望 ROS 更改它们时，该选项很有用。

* ``ROS_STATIC_PEERS`` - 以分号（``;``）分隔的地址列表，ROS 应尝试在这些地址上发现节点。 这允许用户连接到特定机器上的节点（只要其发现范围未设置为 ``OFF``）。

例如，你可能有多台机器人将 ``ROS_AUTOMATIC_DISCOVERY_RANGE`` 设置为 ``LOCALHOST``，这样它们之间不会互相通信。
当你想要将 RViz 连接到其中一台机器人时，在其终端中将它的地址添加到 ``ROS_STATIC_PEERS``。
现在你可以使用 ROS 2 CLI 和可视化工具与该机器人交互。

有关此功能的更多信息，请参阅 https://github.com/ros2/ros2/issues/1359。

匹配事件
^^^^^^^^

除 QoS 事件之外，当任意发布者和订阅之间建立或断开连接时，也可以生成匹配事件。
用户可以为每个发布者和订阅提供回调函数，这些函数由匹配事件触发，并以自己认为合适的方式处理它们，这与处理话题上收到的消息类似。

* publisher：当它发现一个与话题匹配且具有兼容 QoS 的订阅时，或者当已连接的订阅断开时，会发生此事件。
* subscription：当它发现一个与话题匹配且具有兼容 QoS 的发布者时，或者当已连接的发布者断开时，会发生此事件。

更多信息请参阅跟踪缺陷 https://github.com/ros2/rmw/issues/330。

* 匹配事件的 C++ 演示：https://github.com/ros2/demos/blob/iron/demo_nodes_cpp/src/events/matched_event_detect.cpp
* 匹配事件的 Python 演示：https://github.com/ros2/demos/blob/iron/demo_nodes_py/demo_nodes_py/events/matched_event_detect.py

日志记录器的外部配置服务
^^^^^^^^^^^^^^^^^^^^^^^^

现在可以通过服务远程配置节点日志记录器的级别。
在创建节点时启用 ``enable_logger_service`` 选项后，``set_logger_levels`` 和 ``get_logger_levels`` 服务将可用。

请注意，``enable_logger_service`` 选项默认禁用，因此用户需要在创建节点时启用此选项。

更多信息请参阅 https://github.com/ros2/ros2/issues/1355。

类型描述分发
^^^^^^^^^^^^

现在可以传递有关 ROS 2 消息类型的信息，这样名称相同但类型可能不同的系统可以更透明地发现彼此的兼容性。
这组能力由 REP-2011：Evolving Message Types 的一个子集定义，其中许多部分已在 Iron 中落地。

首先，引入新包 `type_description_interfaces <https://index.ros.org/p/type_description_interfaces/github-ros2-rcl_interfaces/#iron>`__ 提供了一种通用方式来传递 ROS 2 通信接口类型（msg、srv、action）的描述。

其次，确定了类型描述哈希的方法，即 ROS 接口哈希标准（RIHS）——从第一个版本 RIHS01 开始。
所有已编译的 ROS 类型在构建时都会自动计算 RIHS 哈希，并内置到生成的代码中，以便可以对其进行检查。
这些哈希也会在发现过程中自动传递，并包含在 ``rmw_topic_endpoint_info_t`` 中，用于诸如 ``get_publishers_info_by_topic`` 之类的图内省查询。

完整的 ``TypeDescription`` 数据结构以及用于生成它的原始源文本（例如 ``.msg`` 文件）现在默认内置到消息库中，因此 ``typesupport`` 或最终用户都可以使用它们。
虽然我们预期这些数据对大多数用户都有价值，但希望尽可能减小安装空间占用的一些用户可以在构建 ROS 2 Core 时通过定义 CMake 变量 ``ROSIDL_GENERATOR_C_DISABLE_TYPE_DESCRIPTION_CODEGEN`` 来禁用此功能。

最后，定义了新服务 ``type_description_interfaces/GetTypeDescription.srv``，使节点在遇到未知的 RIHS 类型哈希时，可以向声明该类型的节点请求完整定义。
目前正在开发将该特性原生集成到 ROS 2 节点中，作为节点构造时的一个可选开关。
该特性尚未发布，但预计会在 2023 年中期向后移植到 Iron。
与此同时，用户节点可以使用稳定的服务接口自行实现该服务。

设计提案请参阅 `REP 2011 <https://github.com/ros-infrastructure/rep/pull/358>`__。
该特性集的开发进展跟踪请参阅 `Type Description Distribution <https://github.com/ros2/ros2/issues/1159>`__。

动态类型与动态消息
^^^^^^^^^^^^^^^^^^

除了上述类型描述分发特性之外，还有在运行时构造和访问动态创建类型（即动态类型）的能力。
该特性在 Iron 中可用于 Fast DDS 和 ``rcl``，并新增了 ``rmw`` 接口以支持将消息作为动态消息接收（即从动态类型构建或遵循动态类型结构构建的消息）。

首先，在 `rosidl <https://index.ros.org/r/rosidl/github-ros2-rosidl/#iron>`__ 中引入了实用工具，以帮助构造和操作类型描述。

其次，编写了 `rosidl_dynamic_typesupport <https://index.ros.org/r/rosidl_dynamic_typesupport/github-ros2-rosidl_dynamic_typesupport/#iron>`__ 包，它提供了与中间件无关的接口，用于在运行时构造动态类型和动态消息。
类型可以在运行时以编程方式构造，也可以通过解析 ``type_description_interfaces/TypeDescription`` 消息来构造。

.. note::

   ``rosidl_dynamic_typesupport`` 库需要序列化支持库来实现与中间件相关的动态类型行为。
   Fast DDS 的序列化支持库已在 `rosidl_dynamic_typesupport_fastrtps <https://index.ros.org/r/rosidl_dynamic_typesupport_fastrtps/github-ros2-rosidl_dynamic_typesupport_fastrtps/#iron>`__ 中实现。
   理想情况下，会有更多中间件实现支持库，从而扩大支持该特性的中间件数量。

最后，为支持动态类型和动态消息的使用，`rmw <https://index.ros.org/r/rmw/github-ros2-rmw/#iron>`__ 和 `rcl <https://index.ros.org/r/rcl/github-ros2-rcl/#iron>`__ 中新增了以下方法：

- 获取与中间件相关的序列化支持的能力
- 在运行时构造使用动态类型的消息类型支持的能力
- 使用动态类型接收动态消息的能力

目前正在开发使用动态类型在客户端库中创建订阅的功能（请参阅下文的 ``rclcpp`` 问题），不过该特性何时落地或向后移植尚不确定。
这将允许用户订阅那些类型描述只有在运行时才知晓的话题。
与此同时，用户可以使用作为该特性集一部分引入的新 ``rmw`` 和 ``rcl`` 特性，编写自己的订阅来订阅动态类型。

设计提案请参阅 `REP 2011 <https://github.com/ros-infrastructure/rep/pull/358>`__。
该特性集的开发进展跟踪请参阅 `Dynamic Subscription <https://github.com/ros2/ros2/issues/1374>`__，其中大部分工作需要在 `rclcpp <https://github.com/ros2/rclcpp/pull/2176>`__ 中完成。

``launch``
^^^^^^^^^^

``PythonExpression`` 现支持导入模块
"""""""""""""""""""""""""""""""""""

现在可以让 launch 的 ``PythonExpression`` 在执行求值之前导入模块。
这在需要引入额外功能供求值表达式使用时非常有用。

更多信息请参阅 https://github.com/ros2/launch/pull/655。

可在事件处理程序中调用 ``ReadyToTest``
""""""""""""""""""""""""""""""""""""""

现在可以注册一个在其输出中使用 ``ReadyToTest`` 的事件处理程序。
这在允许测试运行之前下载资源等场景中很有用。

更多信息请参阅 https://github.com/ros2/launch/pull/665。

新增 ``AnySubstitution`` 和 ``AllSubstitution``
"""""""""""""""""""""""""""""""""""""""""""""""

现在可以指定一种替换：当任意输入参数为真时发生（``AnySubstitution``），或当所有输入参数都为真时发生（``AllSubstitution``）。

更多详情请参阅 https://github.com/ros2/launch/pull/649。

新增获取 launch 日志目录的替换
""""""""""""""""""""""""""""""

现在可以使用名为 ``LaunchLogDir`` 的替换来获取 launch 当前的日志目录。

更多详情请参阅 https://github.com/ros2/launch/pull/652。

``launch_ros``
^^^^^^^^^^^^^^

新增 ``LifecycleTransition`` 动作
"""""""""""""""""""""""""""""""""

现在可以通过新的 ``LifeCycleTransition`` 动作向生命周期节点发送转换信号。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/317。

新增 ``SetROSLogDir`` 动作
""""""""""""""""""""""""""

现在可以通过 ``SetROSLogDir`` 动作配置用于日志记录的目录。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/325。

可为 ``ComposableNode`` 指定条件
""""""""""""""""""""""""""""""""

现在可以指定一个必须满足的条件，只有满足该条件才会将 ``ComposableNode`` 插入其容器中。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/311。

``launch_testing``
^^^^^^^^^^^^^^^^^^

进程启动超时现在可配置
""""""""""""""""""""""

在此版本之前，``ReadyToTest`` 动作会恰好等待 15 秒让进程启动。
如果进程耗时超过该时间，就会失败。
现在新增了一个名为 ``ready_to_test_action_timeout`` 的装饰器，允许用户配置等待进程启动的时间。

更多信息请参阅 https://github.com/ros2/launch/pull/625。

``rclcpp``
^^^^^^^^^^

新增处理 ``Node`` 和 ``LifecycleNode`` 的新范式
"""""""""""""""""""""""""""""""""""""""""""""""

``Node`` 和 ``LifecycleNode`` 这两个类是相关的，因为它们都提供相同的基础方法集（不过 ``LifecycleNode`` 还提供了额外的方法）。
由于各种实现方面的考虑，它们并非派生自同一个基类。

这给希望同时接受 ``Node`` 或 ``LifecycleNode`` 的下游代码带来了一些麻烦。
一种解决方案是提供两个方法签名，一个接受 ``Node``，另一个接受 ``LifecycleNode``。
另一种推荐方案是让方法接受可从这两个类访问的“节点接口”指针，例如

.. code-block:: C++

   void do_thing(rclcpp::node_interfaces::NodeGraphInterface graph)
   {
     fprintf(stderr, "Doing a thing\n");
   }

   void do_thing(rclcpp::Node::SharedPtr node)
   {
     do_thing(node->get_node_graph_interface());
   }

   void do_thing(rclcpp::LifecycleNode::SharedPtr node)
   {
     do_thing(node->get_node_graph_interface());
   }

这样做是可行的，但在需要许多节点接口时会变得有些笨拙。
为了改善这一点，现在新增了一个 ``NodeInterfaces`` 类，可以构造它来包含这些接口，然后供其他代码使用。

有关如何使用它的示例，请参阅 https://github.com/ros2/rclcpp/pull/2041。

引入新的执行器类型：事件执行器
""""""""""""""""""""""""""""""

来自 iRobot 的 ``EventsExecutor`` 已合并到 ``rclcpp`` 主代码库中。
这种替代执行器实现使用来自中间件实现的事件驱动回调，在 ``rclcpp`` 层触发回调。
除了基于推送的模型之外，``EventsExecutor`` 还将定时器管理移到单独的线程中，这可以获得更准确的结果并降低开销，尤其是在定时器很多的情况下。

``EventsExecutor`` 拥有大量文档和实践使用经验，这使其成为纳入 ``rclcpp`` 代码库的有力候选。
有关初始实现提案以及性能基准的信息，请参阅 https://discourse.ros.org/t/ros2-middleware-change-proposal/15863。
有关设计方案的更多信息，请参阅设计 PR：https://github.com/ros2/design/pull/305。

由于 API 相同，尝试 ``EventsExecutor`` 就像替换当前的执行器实现（例如 ``SingleThreadedExecutor``）一样简单：

.. code-block:: C++

    #include <rclcpp/experimental/executors/events_executor/events_executor.hpp>
    using rclcpp::experimental::executors::EventsExecutor;

    EventsExecutor executor;
    executor.add_node(node);
    executor.spin();

**注意** ``EventsExecutor`` 和 ``TimersManager`` 目前位于 ``experimental`` 命名空间中。
虽然它作为独立实现已经使用了一段时间 https://github.com/irobot-ros/events-executor，但决定至少在某个版本中使用 ``experimental`` 命名空间，以便在该版本内灵活修改 API。
请谨慎使用，因为它不会像非实验性代码那样享有同等的 API/ABI 保证。

``rclpy``
^^^^^^^^^

能够等待另一个节点加入图
""""""""""""""""""""""""

现在可以使用如下代码等待另一个节点加入网络图：

.. code-block:: Python

  node.wait_for_node('/fully_qualified_node_name')

更多信息请参阅 https://github.com/ros2/rclpy/pull/930。

实现 ``AsyncParameterClient``
"""""""""""""""""""""""""""""

``rclpy`` 现在有了 ``AsyncParameterClient`` 类，使其功能与 ``rclcpp`` 对齐。
该类用于在远程节点上执行参数操作，而不会阻塞调用节点。

更多信息和示例请参阅 https://github.com/ros2/rclpy/pull/959。

订阅回调现在可以选择性地获取消息信息
""""""""""""""""""""""""""""""""""""

现在可以注册函数签名同时接受消息和消息信息的订阅回调，如下所示：

.. code-block:: Python

  def msg_info_cb(msg, msg_info):
      print('Message info:', msg_info)

  node.create_subscription(msg_type=std_msgs.msg.String, topic='/chatter', qos_profile=10, callback=msg_info_cb)

消息信息结构包含各种信息，例如消息的序号、发送和接收时间戳，以及发布者的 GID。

更多信息请参阅 https://github.com/ros2/rclpy/pull/922。

用于隐藏消息类断言的可选参数
""""""""""""""""""""""""""""
所有消息类现在都包含一个新的可选参数，用于隐藏消息中每种字段类型的断言。
默认情况下断言被隐藏，这可在运行时带来性能提升。
为了在开发/调试时启用断言，你有两种选择：

1. 将环境变量 ``ROS_PYTHON_CHECK_FIELDS`` 定义为 ``'1'``，这会影响项目中的所有消息：

.. code-block:: Python

  import os
  from std_msgs.msg import String

  os.environ['ROS_PYTHON_CHECK_FIELDS'] = '1'
  new_message=String()

2. 通过在构造函数中显式定义新参数，为单条消息选择特定行为：

.. code-block:: Python

  from std_msgs.msg import String

  new_message=String(check_fields=True)

更多信息请参阅 https://github.com/ros2/rosidl_python/pull/194。

``ros2param``
^^^^^^^^^^^^^

使用 ``ros2 param`` 等待节点时可设置超时
""""""""""""""""""""""""""""""""""""""""

现在，``ros2 param`` 的各种命令都可以通过传递 ``--timeout`` 来设置超时。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/802。

已废弃的选项已被移除
""""""""""""""""""""

``dump`` 命令的 ``--output-dir`` 和 ``--print`` 选项已被移除。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/824。

``ros2topic``
^^^^^^^^^^^^^

``now`` 用作 ``builtin_interfaces.msg.Time`` 的关键字，``auto`` 用作 ``std_msgs.msg.Header`` 的关键字
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

``ros2 topic pub`` 现在允许通过 ``now`` 关键字将 ``builtin_interfaces.msg.Time`` 消息设置为当前时间。
类似地，当传入关键字 ``auto`` 时，会自动生成 ``std_msg.msg.Header`` 消息。
此行为与 ROS 1 的 ``rostopic`` 一致（http://wiki.ros.org/ROS/YAMLCommandLine#Headers.2Ftimestamps）

相关 PR：`ros2/ros2cli#749 <https://github.com/ros2/ros2cli/pull/749>`_

``ros2 topic pub`` 可以配置最长等待时间
"""""""""""""""""""""""""""""""""""""""

``ros2 topic pub -w 1`` 命令在发布消息之前会等待至少该数量的订阅者。
本次发行新增了 ``--max-wait-time`` 选项，以便在没有看到订阅者时，命令只等待最长时间后退出。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/800。

``ros2 topic echo`` 可以配置最长等待时间
""""""""""""""""""""""""""""""""""""""""

``ros2 topic echo`` 命令现在接受 ``--timeout`` 选项，用于控制命令等待发布发生的最长时间。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/792。

已废弃的选项已被移除
""""""""""""""""""""

``echo`` 命令的 ``--lost-messages`` 选项已被移除。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/824。

自 Humble 发行版以来的变更
--------------------------

默认控制台日志文件刷新行为的变更
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

这特别适用于 ROS 2 中默认的基于 ``spdlog`` 的日志后端，即在 ``rcl_logging_spdlog`` 中实现的版本。
日志文件的刷新行为已改为：每次使用 "error" 级日志消息时刷新（例如每次 ``RCLCPP_ERROR()`` 调用），并且每五秒定期刷新一次。

以前，``spdlog`` 除创建用于记录到文件的 sink 外没有进行任何配置。

我们测试了该变更，并未发现 CPU 开销有明显增加，即使是在磁盘较慢的机器上（例如 SD 卡）。
不过，如果此变更给你带来了问题，可以通过设置 ``RCL_LOGGING_SPDLOG_EXPERIMENTAL_OLD_FLUSHING_BEHAVIOR=1`` 环境变量来恢复旧行为。

以后我们希望支持完整的配置文件（见：https://github.com/ros2/rcl_logging/issues/92），让你对日志的记录方式有更大的灵活性，但这目前只是计划中的工作。

  因此，当我们为 ``rcl_logging_spdlog`` 日志后端添加配置文件支持时，**此环境变量应被视为实验性的，将来可能会在不经过弃用流程的情况下被移除**。

有关该变更的更多详情，请参阅此 pull request：https://github.com/ros2/rcl_logging/pull/95

``ament_cmake_auto``
^^^^^^^^^^^^^^^^^^^^

包含依赖现在被标记为 SYSTEM
"""""""""""""""""""""""""""

使用 ``ament_auto_add_executable`` 或 ``ament_auto_add_library`` 时，依赖现在会自动以 ``SYSTEM`` 方式添加。
这意味着依赖头文件中的警告将不会被报告。

更多详情请参阅 https://github.com/ament/ament_cmake/pull/385。

``ament_cmake_nose``
^^^^^^^^^^^^^^^^^^^^

软件包已被弃用并移除
""""""""""""""""""""

Python 的 ``nose`` 软件包早已被弃用。
由于当前发布到 Humble 或 Rolling 的开源软件包都不再依赖它，本次发行弃用并移除了围绕它的 ament 封装。

更多信息请参阅 https://github.com/ament/ament_cmake/pull/415。

``ament_lint``
^^^^^^^^^^^^^^

文件可以从 linter 检查中排除
""""""""""""""""""""""""""""

现在，在调用 ``ament_lint_auto_find_test_dependencies`` 之前设置 ``AMENT_LINT_AUTO_FILE_EXCLUDE`` CMake 变量，即可将某些文件从 linter 检查中排除。

更多信息请参阅 https://github.com/ament/ament_lint/pull/386。

``camera_info_manager``
^^^^^^^^^^^^^^^^^^^^^^^

生命周期节点支持
""""""""""""""""

``camera_info_manager`` 现在除普通 ROS 2 节点外，还支持生命周期节点。

更多信息请参阅 https://github.com/ros-perception/image_common/pull/190。

``launch``
^^^^^^^^^^

``LaunchConfigurationEquals`` 和 ``LaunchConfigurationNotEquals`` 已被弃用
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

``LaunchConfigurationEquals`` 和 ``LaunchConfigurationNotEquals`` 条件已被弃用，并将在未来的发行版中移除。
而应改用更通用的 ``Equals`` 和 ``NotEquals`` 替换。

更多详情请参阅 https://github.com/ros2/launch/pull/649。

``launch_ros``
^^^^^^^^^^^^^^

将名称中使用 ``Ros`` 的类重命名为使用 ``ROS``，以符合 PEP8
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

发生更改的类：

* ``launch_ros.actions.RosTimer`` -> ``launch_ros.actions.ROSTimer``
* ``launch_ros.actions.PushRosNamespace`` -> ``launch.actions.PushROSNamespace``

旧的类名仍然保留，但将被弃用。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/326。

``launch_xml``
^^^^^^^^^^^^^^

向 XML 前端暴露 ``emulate_tty``
"""""""""""""""""""""""""""""""

多个发行版以来，``launch`` 的 Python 代码已经可以使用伪终端来模拟 TTY（从而可以执行打印颜色之类的操作）。
现在通过向可执行命令传递 ``emulate_tty`` 参数，即可在 XML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/669。

向 XML 前端暴露 ``sigterm_timeout`` 和 ``sigkill_timeout``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

多个发行版以来，已经可以在 ``launch`` 的 Python 代码中配置 SIGTERM 和 SIGKILL 信号的最大超时值。
现在通过向可执行命令传递 ``sigterm_timeout`` 或 ``sigkill_timeout`` 参数，即可在 XML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/667。

``launch_yaml``
^^^^^^^^^^^^^^^

向 YAML 前端暴露 ``emulate_tty``
""""""""""""""""""""""""""""""""

多个发行版以来，``launch`` 的 Python 代码已经可以使用伪终端来模拟 TTY（从而可以执行打印颜色之类的操作）。
现在通过向可执行命令传递 ``emulate_tty`` 参数，即可在 YAML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/669。

向 YAML 前端暴露 ``sigterm_timeout`` 和 ``sigkill_timeout``
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

多个发行版以来，已经可以在 ``launch`` 的 Python 代码中配置 SIGTERM 和 SIGKILL 信号的最大超时值。
现在通过向可执行命令传递 ``sigterm_timeout`` 或 ``sigkill_timeout`` 参数，即可在 YAML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/667。

``message_filters``
^^^^^^^^^^^^^^^^^^^

新的近似时间策略
""""""""""""""""

新增一个更简单的近似时间策略，称为 ``ApproximateEpsilonTime``。
该时间策略的工作方式类似于 ``ExactTime``，但允许时间戳处于一个 epsilon 容差范围内。
更多信息请参阅 https://github.com/ros2/message_filters/pull/84。

新的上采样时间策略
""""""""""""""""""

新增一个时间策略，称为 ``LatestTime``。
它能够通过零阶保持（zero-order-hold）方式上采样，按各消息的速率同步最多 9 条消息。
更多信息请参阅 https://github.com/ros2/message_filters/pull/73。

``rcl_yaml_param_parser``
^^^^^^^^^^^^^^^^^^^^^^^^^

支持参数文件中的 YAML ``!!str`` 语法
""""""""""""""""""""""""""""""""""""

现在可以使用 YAML ``!!str`` 语法强制 ROS 参数文件解析器将某个字段解释为字符串。
更多信息请参阅 https://github.com/ros2/rcl/pull/999。

``rclcpp``
^^^^^^^^^^

多线程执行器的默认线程数已更改
""""""""""""""""""""""""""""""

如果用户没有另行指定，多线程执行器的默认线程数将设置为机器上的 CPU 数量。
如果底层操作系统不支持获取此信息，则设置为 2。

更多信息请参阅 https://github.com/ros2/rclcpp/pull/2032。

当 QoS 指定为 KEEP_LAST 且深度为 0 时会打印警告
"""""""""""""""""""""""""""""""""""""""""""""""

将 QoS 指定为 KEEP_LAST 且深度为 0 是一种不合理的配置，因为该实体将无法发送或接收任何数据。
``rclcpp`` 现在会在指定此组合时打印警告，但仍会继续执行，让底层中间件选择一个合理的值（通常深度为 1）。

更多信息请参阅 https://github.com/ros2/rclcpp/pull/2048。

已弃用的 ``RCLCPP_SCOPE_EXIT`` 宏已被移除
"""""""""""""""""""""""""""""""""""""""""

在 Humble 中，宏 ``RCLCPP_SCOPE_EXIT`` 已被弃用，改用 ``RCPPUTILS_SCOPE_EXIT``。
在 Iron 中，``RCLCPP_SCOPE_EXIT`` 宏已被完全移除。

``rclpy``
^^^^^^^^^

多线程执行器的默认线程数已更改
""""""""""""""""""""""""""""""

如果用户没有另行指定，多线程执行器的默认线程数将设置为机器上的 CPU 数量。
如果底层操作系统不支持获取此信息，则设置为 2。

更多信息请参阅 https://github.com/ros2/rclpy/pull/1031。

当 QoS 指定为 KEEP_LAST 且深度为 0 时会打印警告
"""""""""""""""""""""""""""""""""""""""""""""""

将 QoS 指定为 KEEP_LAST 且深度为 0 是一种不合理的配置，因为该实体将无法发送或接收任何数据。
``rclpy`` 现在会在指定此组合时打印警告，但仍会继续执行，让底层中间件选择一个合理的值（通常深度为 1）。

更多信息请参阅 https://github.com/ros2/rclpy/pull/1048。

Time 与 Duration 与其他类型比较时不再抛出异常
"""""""""""""""""""""""""""""""""""""""""""""

现在可以将 ``rclpy.time.Time`` 和 ``rclpy.duration.Duration`` 与其他类型比较而不会抛出异常。
如果类型不可比较，则比较返回 ``False``。
请注意，这是相对之前发行版的行为变更。

.. code-block:: Python

  print(None in [rclpy.time.Time(), rclpy.duration.Duration()])  # Prints "False" instead of raising TypeError

更多信息请参阅 https://github.com/ros2/rclpy/pull/1007。

``rcutils``
^^^^^^^^^^^

提升消息日志的性能
""""""""""""""""""

用于在 ``RCUTILS_LOG_*`` 或 ``RCLCPP_*`` 时输出日志消息的代码经过了优化以减少开销。
这些日志消息现在应该更高效，但仍不应以高频率调用。
更多信息请参阅 https://github.com/ros2/rcutils/pull/381、https://github.com/ros2/rcutils/pull/372、https://github.com/ros2/rcutils/pull/369 和 https://github.com/ros2/rcutils/pull/367。

已弃用的 ``rcutils/get_env.h`` 头文件已被移除
"""""""""""""""""""""""""""""""""""""""""""""

在 Humble 中，头文件 ``rcutils/get_env.h`` 已被弃用，改用 ``rcutils/env.h``。
在 Iron 中，``rcutils/get_env.h`` 头文件已被完全移除。

``rmw``
^^^^^^^

将 GID 存储更改为 16 字节
"""""""""""""""""""""""""

RMW 层中的 GID 旨在作为 ROS 图中写入者的全局唯一标识符。
以前，由于旧 RMW 实现中的一个 bug，它被错误地设置为 24 字节。
但这个定义应由 ``rmw`` 软件包给出，所有实现都应遵循。
因此，本次发行将其定义为 16 字节（DDS 标准），并更改所有实现以使用该定义。

更多信息请参阅 https://github.com/ros2/rmw/pull/345 以及（已关闭但仍相关的）https://github.com/ros2/rmw/pull/328。

``rmw_dds_common``
^^^^^^^^^^^^^^^^^^

将 GID 存储更改为 16 字节
"""""""""""""""""""""""""

配合 ``rmw`` 层的变更，将发送 GID 信息的消息也改为 16 字节。

更多信息请参阅 https://github.com/ros2/rmw_dds_common/pull/68。

``ros2topic``
^^^^^^^^^^^^^

``ros2 topic hz/bw/pub`` 现在遵循 ``use_sim_time``
""""""""""""""""""""""""""""""""""""""""""""""""""

在仿真环境下运行时，ROS 2 生态通常从仿真器发布的 ``/clock`` 话题获取时间（而不是使用系统时钟）。
通常通过在节点上设置 ``use_sim_time`` 参数来告知 ROS 2 节点这一变更。
``ros2 topic`` 的 ``hz``、``bw`` 和 ``pub`` 命令所创建的节点现在会遵循该参数，并适时使用仿真时间。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/754。

``rosbag2``
^^^^^^^^^^^

将默认 bag 文件类型更改为 ``mcap``
""""""""""""""""""""""""""""""""""

在此发行版之前，rosbag2 默认将数据记录到 sqlite3 数据库中。
在测试中发现，在许多情况下其性能不足，并且缺少一些对离线处理有用的特性。

为满足这些需求，开发了一种名为 ``mcap`` 的新 bag 格式（受到原 ROS 1 bag 文件格式的影响）。
这种 bag 文件格式具备 sqlite3 文件格式所缺失的许多特性，而且性能也更好。

本次发行改用 ``mcap`` 作为写入新 bag 的默认文件格式。
旧的 ``sqlite3`` 文件格式仍然可用，用户如有需要仍可选择其进行写入。
本次发行还允许回放 ``sqlite3`` 文件格式或 ``mcap`` 文件格式的数据。

更多信息请参阅 https://github.com/ros2/rosbag2/pull/1160。

使用 SQLite3 插件在 bag 文件中存储消息定义
""""""""""""""""""""""""""""""""""""""""""

现在我们支持将消息定义以与保存到 ``mcap`` 文件相同的格式保存到 ``sqlite3`` 数据库文件中。
这为第三方工具提供了机会，使其能够反序列化 rosbag2 文件，而无需在解码由 ``sqlite3`` 插件记录的 bag 文件的机器上拥有所有原始 .msg 文件的正确版本。

更多信息请参阅 https://github.com/ros2/rosbag2/issues/782 和 https://github.com/ros2/rosbag2/pull/1293。


新的回放与录制控制
""""""""""""""""""

新增了多个 pull request，以增强用户对 bag 回放的控制。
pull request `960 <https://github.com/ros2/rosbag2/pull/960>`_ 增加了按指定秒数播放 bag 的能力。
而 pull request `1005 <https://github.com/ros2/rosbag2/pull/1005>`_ 允许播放 bag 直到指定的时间戳。
另一个 pull request `1007 <https://github.com/ros2/rosbag2/pull/1007>`_ 增加了通过服务调用
远程停止回放的能力。
如果播放器处于暂停模式，Stop 将解除暂停；如果回放正在进行，则停止回放并强制退出 play() 方法。

通过服务调用管理录制
""""""""""""""""""""

新增了一些用于从远程节点控制录制过程的选项。
pull request `1131 <https://github.com/ros2/rosbag2/pull/1131>`_ 增加了通过服务调用暂停和
恢复录制的能力。
另一个 pull request `1115 <https://github.com/ros2/rosbag2/pull/1115>`_ 增加了在录制过程中通过发送服务调用
分割 bag 的能力。

在回放时通过正则表达式过滤话题
""""""""""""""""""""""""""""""

用户有时需要只回放已记录 bag 中的部分话题，以下两个 pull request
增加了该能力。
pull request `1034 <https://github.com/ros2/rosbag2/pull/1034>`_ 新增了 ``--topics-regex`` 选项，
可通过正则表达式过滤话题。
``--topics-regex`` 选项接受以空格分隔的多个正则表达式。
而 pull request `1046 <https://github.com/ros2/rosbag2/pull/1046>`_ 增加了通过在新增的 ``--exclude``
（以及 ``-x``）选项中提供正则表达式来排除某些
特定话题不被回放的能力。

允许插件注册自己的 CLI 动词参数
"""""""""""""""""""""""""""""""

pull request `1209 <https://github.com/ros2/rosbag2/pull/1209>`_ 增加了 ``rosbag2`` 插件注册可选 Python entrypoint、以提供插件特定 CLI 参数值的能力。
因此，``ros2 bag record`` 动词的命令行选项 ``--storage-preset-profile`` 会
根据底层存储插件的不同而具有不同的有效选项。

其他变更
""""""""

pull request `1038 <https://github.com/ros2/rosbag2/pull/1038>`_ 增加了在 metadata.yaml 文件的 'custom' 字段中记录
任意键/值对的能力。
当用户需要保存录制时的某些硬件特定 id 或坐标时，这很有用。
而 pull request `1180 <https://github.com/ros2/rosbag2/pull/1180>`_ 增加了一个选项，可通过新增的命令行选项
``--node-name`` 更改录制器的底层节点名称。
该选项可用于创建包含多个 rosbag2 录制器实例的远程分布式录制。
它提供了向专门的 rosbag2 录制器实例发送服务调用以管理录制过程的能力。

``rosidl_python``
^^^^^^^^^^^^^^^^^

``__slots__`` 属性内容的更改
""""""""""""""""""""""""""""

到目前为止，Python 消息类的 ``__slots__`` 属性一直被用作包含消息字段名的成员。
在 Iron 中，该属性不再仅包含消息结构中的字段名，而是包含所有类成员的字段名。
因此，用户不应依赖该属性来获取字段名信息，而应使用 ``get_field_and_field_types()`` 方法来获取。

更多信息请参阅 https://github.com/ros2/rosidl_python/pull/194。

``rviz``
^^^^^^^^

地图显示现在可以以二值形式显示
""""""""""""""""""""""""""""""

RViz 地图显示现在可以以二值形式显示地图，并带有一个可设置的阈值。
在某些情况下，这对于检查地图，或与具有可设置阈值的规划器配合使用很有用。

更多信息请参阅 https://github.com/ros2/rviz/pull/846。

相机显示插件遵循 CameraInfo 消息中的 ROI
""""""""""""""""""""""""""""""""""""""""

CameraDisplay 插件现在会遵循 CameraInfo 消息中的感兴趣区域（ROI）设置（如果提供了的话）。
这考虑了相机驱动为降低带宽而对图像进行裁剪的情况。

更多信息请参阅 https://github.com/ros2/rviz/pull/864。

来自 SOLIDWORKS 的二进制 STL 文件可以正常工作
"""""""""""""""""""""""""""""""""""""""""""""

对 STL 加载器进行了更改，使其能够接受来自 SOLIDWORKS 的、文件名中包含 "solid" 字样的二进制 STL 文件。
这在技术上违反了 STL 规范，但这种情况足够常见，因此添加了特殊处理来应对这些文件。

更多信息请参阅 https://github.com/ros2/rviz/pull/917。

``tracetools``
^^^^^^^^^^^^^^

Linux 上现在默认包含跟踪插桩
""""""""""""""""""""""""""""

ROS 2 核心已经具有跟踪插桩有一段时间了。
然而，它默认在编译时被排除在外。
要获得插桩，必须在从源码重新构建 ROS 2 之前手动安装 LTTng 跟踪器。
在 Iron 中，默认包含跟踪插桩和跟踪点；因此 LTTng 跟踪器现在成为 ROS 2 的依赖项。

请注意，这仅适用于 Linux。

更多信息请参阅 https://github.com/ros2/ros2_tracing/pull/31 和 https://github.com/ros2/ros2/issues/1177。
参见 :doc:`这份有关移除插桩（或使用 Humble 及更早版本添加插桩）的操作指南 <../How-To-Guides/Building-ROS-2-with-Tracing-Instrumentation>`。

新增了针对 ``rclcpp`` 进程内通信的跟踪点
""""""""""""""""""""""""""""""""""""""""

新增了跟踪点以支持 ``rclcpp`` 进程内通信。
这样可以评估进程内通信中消息发布与回调开始之间的时间。

更多信息请参阅 https://github.com/ros2/ros2_tracing/pull/30 和 https://github.com/ros2/rclcpp/pull/2091。

已知问题
--------

* ``rmw_connextdds`` 无法与 Windows 二进制发行包配合使用。
  RTI 不再分发 ``RTI ConnextDDS 6.0.1``，而打包任务此前使用它来生成 Windows 的二进制文件。
  现在他们分发的是 ``RTI ConnextDDS 6.1.0``，它与生成的二进制文件在 ABI 上不兼容。
  解决方案是在 Windows 上依赖 ROS 2 和 ``rmw_connextdds`` 的源码构建。

* Windows 上的 ``sros2`` 要求用户将 ``cryptography`` Python 模块降级到 ``cryptography==38.0.4``，如 `此处 <https://github.com/ros2/sros2/issues/285>`_ 所述。

* ``ros1_bridge`` 无法与来自 `上游 Ubuntu <https://packages.ubuntu.com/jammy/ros-core-dev>`_ 的 ROS Noetic 软件包配合使用。建议的变通方法是先从源码构建 ROS Noetic，然后用它来构建 ``ros1_bridge``。

发行时间线
----------

    2022 年 11 月 - 平台决策
        REP 2000 更新了目标平台和主要依赖项的版本。

    2023 年 1 月前 - Rolling 平台切换
        构建农场更新为 Iron Irwini 的新平台版本和依赖项版本（如有必要）。

    2023 年 4 月 10 日（周一）- Alpha + RMW 冻结
        对 ROS Base [1]_ 软件包进行初步测试和稳定化，并冻结 RMW 提供者软件包的 API 和特性。

    2023 年 4 月 17 日（周一）- 冻结
        冻结 Rolling Ridley 中 ROS Base [1]_ 软件包的 API 和特性。
        此后只应进行缺陷修复版本发布。
        新软件包可以独立发布。

    2023 年 4 月 24 日（周一）- 分支
        从 Rolling Ridley 分支。
        ``rosdistro`` 对 ROS Base [1]_ 软件包的 Rolling PR 重新开放。
        Iron 开发从 ``ros-rolling-*`` 软件包转向 ``ros-iron-*`` 软件包。

    2023 年 5 月 1 日（周一）- Beta
        ROS Desktop [2]_ 软件包的更新版本可用。
        呼吁进行广泛测试。

    2023 年 5 月 15 日（周一）- 候选发行版
        构建候选发行版软件包。
        ROS Desktop [2]_ 软件包的更新版本可用。

    2023 年 5 月 18 日（周四）- 发行版冻结
        冻结 rosdistro。
        不会合并 ``rosdistro`` 仓库中针对 Iron 的 PR（在发行公告后重新开放）。

    2023 年 5 月 23 日（周二）- 正式发布
        发布公告。
        ``rosdistro`` 对 Iron 的 PR 重新开放。

.. [1] ``ros_base`` 变体在 `REP 2001 (ros-base) <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中描述。
.. [2] ``desktop`` 变体在 `REP 2001 (desktop-variants) <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中描述。

开发进度
--------

有关 Iron Irwini 开发和发行的进展，请参阅 `跟踪用的 GitHub issue <https://github.com/ros2/ros2/issues/1298>`__。

有关 Iron Irwini 所遵循的整体流程，请参阅 :doc:`流程说明页面 <Release-Process>`。
