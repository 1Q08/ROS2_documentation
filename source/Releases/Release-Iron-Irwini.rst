.. _iron-release:

Iron Irwini (``iron``)
======================

.. toctree::
   :hidden:

   Iron-Irwini-Complete-Changelog

.. contents:: 目录
   :depth: 2
   :local:

*Iron Irwini* 是 ROS 2 的第九个版本。
以下是自上一个版本以来 Iron Irwini 中的重要变更和功能的亮点。
有关自 Humble 以来的所有变更列表，请参阅 :doc:`详细变更日志 <Iron-Irwini-Complete-Changelog>`。

支持的平台
----------

Iron Irwini 根据 `平台支持等级 <../The-ROS2-Project/Platform-Support-Tiers>` 支持以下平台：

一级平台：

* Ubuntu 22.04 (Jammy)：``amd64`` 和 ``arm64``
* Windows 10 (Visual Studio 2019)：``amd64``

二级平台：

* RHEL 9：``amd64``

三级平台：

* macOS：``amd64``
* Debian Bullseye：``amd64``

目标平台：

+--------------+------------------+---------------+------------------+------------+-----------------+----------------+
| 架构         | Ubuntu Jammy     | Windows 10    | RHEL 9           | macOS      | Debian Bullseye | OpenEmbedded / |
|              | (22.04)          | (VS2019)      |                  |            | (11)            | Yocto Project  |
+==============+==================+===============+==================+============+=================+================+
| amd64        | Tier 1 [d][a][s] | Tier 1 [a][s] | Tier 2 [d][a][s] | Tier 3 [s] | Tier 3 [s]      | Tier 3 [s]     |
+--------------+------------------+---------------+------------------+------------+-----------------+----------------+
| arm64        | Tier 1 [d][a][s] |               |                  |            | Tier 3 [s]      | Tier 3 [s]     |
+--------------+------------------+---------------+------------------+------------+-----------------+----------------+
| arm32        | Tier 3 [s]       |               |                  |            | Tier 3 [s]      | Tier 3 [s]     |
+--------------+------------------+---------------+------------------+------------+-----------------+----------------+

以下指示符显示了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为此平台提供特定于发行版的（Debian、RPM 等）软件包。

\" \[a\] \" 二进制版本以每个平台单个归档文件的形式提供，包含 Iron ROS 2 repos 文件[^12] 中的所有软件包。

\" \[s\] \" 从源代码编译。

中间件实现支持：

+--------------------------+-------------------------+---------------+-----------------------------+------------------------------+
| 中间件库                 | 中间件提供方            | 支持等级      | 平台                        | 架构                         |
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

中间件实现支持取决于平台支持等级。例如，二级平台上的一个一级中间件实现只能获得二级支持。

最低语言要求：

- C++17
- Python 3.8

依赖要求：

+-------------------+-----------------------+-----------------------------------------------------------+
|                   | 必需支持              | 推荐支持                                                  |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| 软件包            | Ubuntu    | Windows   | RHEL 9  | macOS**   | Debian          | OpenEmbedded**    |
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
|                               | **仅 Linux**                                                          |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| PCL               | 1.12.1    | N/A       | 1.12.0  | N/A       | 1.11.1          | 1.10.0            |
+-------------------+-----------+-----------+---------+-----------+-----------------+-------------------+
| **RMW DDS 中间件**                                                                                    |
+-------------------+-----------------------------------------------------------------------------------+
| Cyclone DDS       | 0.9                                                                               |
+-------------------+-----------------------------------------------------------------------------------+
| Fast-DDS          | 2.8                                                                               |
+-------------------+---------------------------------------------+-------------------------------------+
| Connext DDS       | 6.0.1                                       | N/A                                 |
+-------------------+-----------------------+---------------------+-------------------------------------+
| Gurum DDS         | 2.8.x                 | N/A                                                       |
+-------------------+-----------------------+-----------------------------------------------------------+

\" \* \" 表示这不是上游版本（来自官方操作系统仓库），而是由 OSRF 或社区分发的软件包（在自定义仓库上构建和分发的软件包）。

\" \*\* \" 表示该依赖可能会经历多个版本变更，因为该依赖使用了一个会持续更新依赖且没有稳定 API 的软件包管理器。

\" \*\*\* \" webOS OSE 提供了这个不同的版本。

本文档仅记录 ROS 发行版首次发布时的版本，不会随着依赖的推进而更新。
因此这些版本是最低水位线。

依赖使用的软件包管理器：

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

此 ROS 2 版本中的新功能
-----------------------

Python 软件包的 API 文档生成
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 已经为 C++ 软件包提供了多个版本的自动 API 文档，例如 https://docs.ros.org/en/rolling/p/rclcpp/generated/index.html。
Iron 也为 Python 软件包添加了自动 API 文档，例如 https://docs.ros.org/en/rolling/p/rclpy/rclpy.html。

更多详情请参阅 https://github.com/ros-infrastructure/rosdoc2/pull/28、https://github.com/ros-infrastructure/rosdoc2/pull/49、https://github.com/ros-infrastructure/rosdoc2/pull/51 和 https://github.com/ros-infrastructure/rosdoc2/pull/52。

服务内省
^^^^^^^^

现在可以按服务逐个启用服务内省。
启用后，用户可以查看与请求服务的客户端、接受请求的服务器、发送响应的服务器以及接受响应的客户端相关联的元数据。
可选地，客户端/服务器的请求/响应内容也可以被内省。
所有信息都发布在根据服务名称生成的隐藏话题上。
因此，如果服务名为 ``/myservice``，那么信息将发布在 ``/myservice/_service_event`` 上。

请注意，此功能默认禁用；要启用它，用户必须在创建服务客户端或服务器后调用 ``configure_introspection``。
在 https://github.com/ros2/demos/tree/iron/demo_nodes_cpp/src/services（C++）和 https://github.com/ros2/demos/blob/iron/demo_nodes_py/demo_nodes_py/services/introspection.py（Python）中有展示如何操作的示例。

更多信息请参阅 `REP 2012 <https://github.com/ros-infrastructure/rep/pull/360>`__ 和跟踪问题 https://github.com/ros2/ros2/issues/1285。

设置参数前后回调支持
^^^^^^^^^^^^^^^^^^^^

在许多版本中，用户可以注册一个回调，当节点上的参数被外部实体（如 ``ros2 param set``）更改时调用。
该回调可以检查更改的参数类型和值，并在其中一个不满足特定条件时拒绝整个批次。
但是，它不能修改参数列表，也不应该修改状态（因为在设置回调之后可能还有其他回调会拒绝这些参数）。

此版本添加了前置和后置回调。
回调按以下顺序调用：

* “pre”设置参数回调，可以根据任意条件修改参数列表。
* “set”参数回调，不能修改列表，只能根据参数的类型和值接受或拒绝参数（这是现有的回调）。
* “post”设置参数回调，可以根据参数进行状态更改，并且仅在前两个回调成功时才会调用。

在 https://github.com/ros2/demos/blob/iron/demo_nodes_cpp/src/parameters/set_parameters_callback.cpp（C++）和 https://github.com/ros2/demos/blob/iron/demo_nodes_py/demo_nodes_py/parameters/set_parameters_callback.py（Python）中有实际运行的示例。

更多信息请参阅 https://github.com/ros2/rclcpp/pull/1947、https://github.com/ros2/rclpy/pull/966 和 https://github.com/ros2/demos/pull/565。

改进的发现选项
^^^^^^^^^^^^^^

以前的 ROS 2 版本提供的发现选项有限。
基于 DDS 的 RMW 实现的默认行为是发现通过组播可达的任何节点。
可以通过设置环境变量 ``ROS_LOCALHOST_ONLY`` 将其限制在同一台机器上，但任何其他配置都需要直接配置中间件，通常通过中间件特定的 XML 文件和环境变量。
ROS Iron 保留了相同的默认发现行为，但弃用了 ``ROS_LOCALHOST_ONLY``，改用更细粒度的选项。

* ``ROS_AUTOMATIC_DISCOVERY_RANGE`` 控制 ROS 节点尝试发现彼此的范围。有效选项为：

  * ``SUBNET`` - 默认值，对于基于 DDS 的中间件，它将发现通过组播可达的任何节点。
  * ``LOCALHOST`` - 只尝试发现同一台机器上的其他节点。
  * ``OFF`` - 不会自动尝试发现任何其他节点，即使是同一台机器上的节点。
  * ``SYSTEM_DEFAULT`` - 不更改任何发现设置。当你已经为中间件设置了自定义设置且不希望 ROS 更改它们时，这很有用。

* ``ROS_STATIC_PEERS`` - 一个以分号（``;``）分隔的地址列表，ROS 应尝试在这些地址上发现节点。这允许用户连接到特定机器上的节点（只要它们的发现范围未设置为 ``OFF``）。

例如，你可能有几台机器人将 ``ROS_AUTOMATIC_DISCOVERY_RANGE`` 设置为 ``LOCALHOST``，这样它们就不会相互通信。
当你想将 RViz 连接到其中一台时，你可以在终端中将其地址添加到 ``ROS_STATIC_PEERS``。
现在你可以使用 ROS 2 CLI 和可视化工具与该机器人交互。

有关此功能的更多信息，请参阅 https://github.com/ros2/ros2/issues/1359。

匹配事件
^^^^^^^^

除了 QoS 事件之外，当任何发布者和订阅者建立或断开它们之间的连接时，也会生成匹配事件。
用户可以为每个发布者和订阅者提供由匹配事件触发的回调函数，并以他们认为合适的方式处理它们，类似于处理话题上收到的消息。

* 发布者：当它找到与话题匹配且 QoS 兼容的订阅者，或者已连接的订阅者断开连接时，会发生此事件。
* 订阅者：当它找到与话题匹配且 QoS 兼容的发布者，或者已连接的发布者断开连接时，会发生此事件。

更多信息请参阅跟踪问题 https://github.com/ros2/rmw/issues/330。

* 匹配事件的 C++ 演示：https://github.com/ros2/demos/blob/iron/demo_nodes_cpp/src/events/matched_event_detect.cpp
* 匹配事件的 Python 演示：https://github.com/ros2/demos/blob/iron/demo_nodes_py/demo_nodes_py/events/matched_event_detect.py

记录器的外部配置服务
^^^^^^^^^^^^^^^^^^^^

现在可以通过服务远程配置节点记录器级别。
当在节点创建期间启用 ``enable_logger_service`` 选项时，``set_logger_levels`` 和 ``get_logger_levels`` 服务将可用。

请注意，``enable_logger_service`` 选项默认禁用，因此用户需要在创建节点时启用此选项。

更多信息请参阅 https://github.com/ros2/ros2/issues/1355。

类型描述分发
^^^^^^^^^^^^

现在可以传达关于 ROS 2 消息类型的信息，以便可能具有同名但类型不同的系统可以更透明地发现它们的兼容性。
这一组能力由 REP-2011：消息类型演进 的一个子集定义，其许多部分已在 Iron 中落地。

首先，新软件包 `type_description_interfaces <https://index.ros.org/p/type_description_interfaces/github-ros2-rcl_interfaces/#iron>`__ 的引入，提供了一种传达 ROS 2 通信接口类型（msg、srv、action）描述的通用方式。

接下来，确定了对类型描述进行哈希的方法，即 ROS 接口哈希标准（RIHS）——从第一个版本 RIHS01 开始。
RIHS 哈希会在构建时为所有已编译的 ROS 类型自动计算，并烘焙到生成的代码中，以便检查。
这些哈希也会在发现期间自动传达，并包含在用于图内省查询（如 ``get_publishers_info_by_topic``）的 ``rmw_topic_endpoint_info_t`` 中。

完整的 ``TypeDescription`` 数据结构以及用于生成它的原始源文本（如 ``.msg`` 文件）现在默认烘焙到消息库中，因此 ``typesupport`` 或最终用户可以使用它们。
虽然我们期望这些数据对大多数用户有价值，但一些希望最小化安装空间字节数的用户可以在构建 ROS 2 Core 时通过定义 CMake 变量 ``ROSIDL_GENERATOR_C_DISABLE_TYPE_DESCRIPTION_CODEGEN`` 来禁用此功能。

最后，定义了新服务 ``type_description_interfaces/GetTypeDescription.srv``，允许节点在遇到未知的 RIHS 类型哈希时，向发布该类型的节点请求完整定义。
在 ROS 2 节点中原生提供此功能的工作正在进行中，作为节点构造时的可选开关。
此功能尚未发布，但预计将在 2023 年年中的某个时候回移到 Iron。
与此同时，用户节点可以使用稳定的服务接口独立实现此服务。

设计提案请参阅 `REP 2011 <https://github.com/ros-infrastructure/rep/pull/358>`__。
功能集开发跟踪请参阅 `类型描述分发 <https://github.com/ros2/ros2/issues/1159>`__。

动态类型和动态消息
^^^^^^^^^^^^^^^^^^

除了上述类型描述分发功能之外，还可以在运行时构建和访问动态创建的类型（即动态类型）。
此功能在 Iron 中适用于 Fast DDS 和 ``rcl``，并提供了新的 ``rmw`` 接口，用于支持以动态消息（即根据动态类型的结构构建或遵循该结构的消息）的形式获取消息。

首先，在 `rosidl <https://index.ros.org/r/rosidl/github-ros2-rosidl/#iron>`__ 中引入了实用工具，以帮助构建和操作类型描述。

接下来，编写了 `rosidl_dynamic_typesupport <https://index.ros.org/r/rosidl_dynamic_typesupport/github-ros2-rosidl_dynamic_typesupport/#iron>`__ 软件包，它提供了一个与中间件无关的接口，用于在运行时构建动态类型和动态消息。
类型可以在运行时通过编程方式构建，也可以通过解析 ``type_description_interfaces/TypeDescription`` 消息来构建。

.. note::

   ``rosidl_dynamic_typesupport`` 库需要序列化支持库来实现中间件特定的动态类型行为。
   Fast DDS 的序列化支持库在 `rosidl_dynamic_typesupport_fastrtps <https://index.ros.org/r/rosidl_dynamic_typesupport_fastrtps/github-ros2-rosidl_dynamic_typesupport_fastrtps/#iron>`__ 中实现。
   理想情况下，更多中间件将实现支持库，从而扩展支持此功能的中间件数量。

最后，为了支持动态类型和动态消息的使用，向 `rmw <https://index.ros.org/r/rmw/github-ros2-rmw/#iron>`__ 和 `rcl <https://index.ros.org/r/rcl/github-ros2-rcl/#iron>`__ 添加了新方法，支持：

- 获取中间件特定序列化支持的能力
- 在运行时构建使用动态类型的消息类型支持的能力
- 使用动态类型获取动态消息的能力

在客户端库中使用动态类型创建订阅的工作正在进行中（参见下面的 ``rclcpp`` issue），尽管该功能何时落地或被回移尚不确定。
这将允许用户订阅仅在运行时才知道类型描述的话题。
与此同时，用户可以使用此功能集引入的新 ``rmw`` 和 ``rcl`` 功能来编写自己的订阅动态类型的订阅。

设计提案请参阅 `REP 2011 <https://github.com/ros-infrastructure/rep/pull/358>`__。
功能集开发跟踪请参阅 `动态订阅 <https://github.com/ros2/ros2/issues/1374>`__，其中 `rclcpp <https://github.com/ros2/rclcpp/pull/2176>`__ 需要完成大部分工作。

``launch``
^^^^^^^^^^

``PythonExpression`` 现在支持导入模块
"""""""""""""""""""""""""""""""""""""

现在可以让 launch 的 ``PythonExpression`` 在执行求值之前导入模块。
这对于在求值表达式时引入额外功能很有用。

更多信息请参阅 https://github.com/ros2/launch/pull/655。

``ReadyToTest`` 可以从事件处理器调用
""""""""""""""""""""""""""""""""""""

现在可以注册一个在其输出中使用 ``ReadyToTest`` 的事件处理器。
这对于在允许测试运行之前下载资源等操作很有用。

更多信息请参阅 https://github.com/ros2/launch/pull/665。

添加 ``AnySubstitution`` 和 ``AllSubstitution``
"""""""""""""""""""""""""""""""""""""""""""""""

现在可以指定在任一输入参数为真时（``AnySubstitution``），或在所有输入参数都为真时（``AllSubstitution``）进行的替换。

更多详情请参阅 https://github.com/ros2/launch/pull/649。

新增获取 launch 日志目录的替换
""""""""""""""""""""""""""""""

现在可以使用名为 ``LaunchLogDir`` 的替换来获取 launch 当前的日志目录。

更多详情请参阅 https://github.com/ros2/launch/pull/652。

``launch_ros``
^^^^^^^^^^^^^^

添加 ``LifecycleTransition`` 动作
"""""""""""""""""""""""""""""""""

现在可以通过新的 ``LifeCycleTransition`` 动作向生命周期节点发送转换信号。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/317。

添加 ``SetROSLogDir`` 动作
""""""""""""""""""""""""""

现在可以通过 ``SetROSLogDir`` 动作配置用于日志记录的目录。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/325。

为 ``ComposableNode`` 指定条件的能力
""""""""""""""""""""""""""""""""""""

现在可以指定一个必须满足的条件，以便将 ``ComposableNode`` 插入其容器中。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/311。

``launch_testing``
^^^^^^^^^^^^^^^^^^

进程启动超时现在可配置
""""""""""""""""""""""

在此版本之前，``ReadyToTest`` 动作会恰好等待 15 秒让进程启动。
如果进程启动时间超过这个时间，它们就会失败。
现在有一个名为 ``ready_to_test_action_timeout`` 的新装饰器，允许用户配置等待进程启动的时间量。

更多信息请参阅 https://github.com/ros2/launch/pull/625。

``rclcpp``
^^^^^^^^^^

新增处理 ``Node`` 和 ``LifecycleNode`` 的新范式
"""""""""""""""""""""""""""""""""""""""""""""""

``Node`` 和 ``LifecycleNode`` 类相关，因为它们提供相同的基础方法集（尽管 ``LifecycleNode`` 还提供额外的方法）。
由于各种实现方面的考虑，它们并非派生自一个共同的基类。

这给想要接受 ``Node`` 或 ``LifecycleNode`` 的下游代码带来了一些麻烦。
一种解决方案是提供两个方法签名，一个接受 ``Node``，一个接受 ``LifecycleNode``。
另一种推荐的解决方案是提供一个接受可从两个类访问的“节点接口”指针的方法，例如：

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

这是可行的，但当需要许多节点接口时可能会变得有些笨重。
为了改善这一点，现在有一个新的 ``NodeInterfaces`` 类，可以构造它来包含这些接口，然后供其他代码使用。

在 https://github.com/ros2/rclcpp/pull/2041 中有如何使用它的示例。

引入新的执行器类型：事件执行器
""""""""""""""""""""""""""""""

来自 iRobot 的 ``EventsExecutor`` 已合并到主 ``rclcpp`` 代码库中。
这种替代执行器实现使用来自中间件实现的事件驱动回调，在 ``rclcpp`` 层触发回调。
除了基于推送的模型之外，``EventsExecutor`` 还将定时器管理移到一个单独的线程中，这可以带来更准确的结果和更低的开销，尤其是在定时器较多的情况下。

``EventsExecutor`` 拥有大量的文档和实际使用经验，使其成为纳入 ``rclcpp`` 代码库的有力候选者。
有关初始实现提案以及性能基准的信息，请参阅 https://discourse.ros.org/t/ros2-middleware-change-proposal/15863。
有关设计的更多信息，请参阅设计 PR：https://github.com/ros2/design/pull/305。

由于 API 相同，尝试 ``EventsExecutor`` 就像替换你当前的 Executor 实现（例如 ``SingleThreadedExecutor``）一样简单：

.. code-block:: C++

    #include <rclcpp/experimental/executors/events_executor/events_executor.hpp>
    using rclcpp::experimental::executors::EventsExecutor;

    EventsExecutor executor;
    executor.add_node(node);
    executor.spin();

**注意** ``EventsExecutor`` 和 ``TimersManager`` 目前位于 ``experimental`` 命名空间中。
虽然它作为独立实现已经使用了一段时间 https://github.com/irobot-ros/events-executor，但决定至少在一个版本中使用 ``experimental`` 命名空间，以便在该版本内更改 API 时留有余地。
请谨慎使用，因为它不会受到与非实验代码相同的 API/ABI 保证。

``rclpy``
^^^^^^^^^

等待另一个节点加入图的能力
""""""""""""""""""""""""""

现在可以使用如下代码等待另一个节点加入网络图：

.. code-block:: Python

  node.wait_for_node('/fully_qualified_node_name')

更多信息请参阅 https://github.com/ros2/rclpy/pull/930。

``AsyncParameterClient`` 的实现
"""""""""""""""""""""""""""""""

``rclpy`` 现在有了 ``AsyncParameterClient`` 类，使其与 ``rclcpp`` 功能对等。
此类用于在远程节点上执行参数操作，而不会阻塞调用节点。

更多信息和示例请参阅 https://github.com/ros2/rclpy/pull/959。

订阅回调现在可以选择获取消息信息
""""""""""""""""""""""""""""""""

现在可以注册一个订阅回调，其函数签名同时接受消息和消息信息，例如：

.. code-block:: Python

  def msg_info_cb(msg, msg_info):
      print('Message info:', msg_info)

  node.create_subscription(msg_type=std_msgs.msg.String, topic='/chatter', qos_profile=10, callback=msg_info_cb)

消息信息结构包含各种信息，如消息的序列号、源时间戳和接收时间戳，以及发布者的 GID。

更多信息请参阅 https://github.com/ros2/rclpy/pull/922。

隐藏消息类断言的可选参数
""""""""""""""""""""""""
所有消息类现在都包含一个新的可选参数，允许隐藏消息中每个字段类型的断言。
默认情况下，断言是隐藏的，这在运行时提供了性能改进。
为了在开发/调试目的下启用断言，你有两种选择：

1. 将环境变量 ``ROS_PYTHON_CHECK_FIELDS`` 定义为 ``'1'`` （这将影响你项目中的所有消息）：

.. code-block:: Python

  import os
  from std_msgs.msg import String

  os.environ['ROS_PYTHON_CHECK_FIELDS'] = '1'
  new_message=String()

2. 通过在构造函数中显式定义新参数，为单个消息选择特定行为：

.. code-block:: Python

  from std_msgs.msg import String

  new_message=String(check_fields=True)

更多信息请参阅 https://github.com/ros2/rosidl_python/pull/194。

``ros2param``
^^^^^^^^^^^^^

使用 ``ros2 param`` 等待节点时的超时选项
""""""""""""""""""""""""""""""""""""""""

现在可以通过向命令传递 ``--timeout``，让各种 ``ros2 param`` 命令超时。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/802。

已弃用的选项被移除
""""""""""""""""""

``dump`` 命令的 ``--output-dir`` 和 ``--print`` 选项已被移除。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/824。

``ros2topic``
^^^^^^^^^^^^^

``now`` 作为 ``builtin_interfaces.msg.Time`` 的关键字，``auto`` 用于 ``std_msgs.msg.Header``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

``ros2 topic pub`` 现在允许通过 ``now`` 关键字将 ``builtin_interfaces.msg.Time`` 消息设置为当前时间。
类似地，当传入关键字 ``auto`` 时，``std_msg.msg.Header`` 消息将自动生成。
此行为与 ROS 1 的 ``rostopic`` 一致（http://wiki.ros.org/ROS/YAMLCommandLine#Headers.2Ftimestamps）

相关 PR：`ros2/ros2cli#749 <https://github.com/ros2/ros2cli/pull/749>`_

``ros2 topic pub`` 可以配置为等待最长时间
"""""""""""""""""""""""""""""""""""""""""

命令 ``ros2 topic pub -w 1`` 将在发布消息之前至少等待该数量的订阅者。
此版本添加了 ``--max-wait-time`` 选项，这样如果没有看到订阅者，命令在退出前最多只会等待一段最长时间。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/800。

``ros2 topic echo`` 可以配置为等待最长时间
""""""""""""""""""""""""""""""""""""""""""

命令 ``ros2 topic echo`` 现在接受 ``--timeout`` 选项，它控制命令等待发布发生的最长时间。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/792。

已弃用的选项被移除
""""""""""""""""""

``echo`` 命令的 ``--lost-messages`` 选项已被移除。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/824。

自 Humble 版本以来的变更
------------------------

默认控制台日志文件刷新行为的变化
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

这特别适用于 ROS 2 中默认的基于 ``spdlog`` 的日志后端，在 ``rcl_logging_spdlog`` 中实现。
日志文件刷新已更改为每次使用“error”日志消息时（例如每次 ``RCLCPP_ERROR()`` 调用）刷新一次，并且每隔五秒定期刷新一次。

以前，``spdlog`` 除了创建用于将日志记录到文件的 sink 之外，未做任何配置。

我们测试了该变更，发现 CPU 开销并不显著，即使在磁盘速度较慢的机器上（例如 SD 卡）也是如此。
但是，如果此变更给你带来了问题，你可以通过设置 ``RCL_LOGGING_SPDLOG_EXPERIMENTAL_OLD_FLUSHING_BEHAVIOR=1`` 环境变量来恢复旧行为。

稍后我们希望支持完整的配置文件（参见：https://github.com/ros2/rcl_logging/issues/92），让你在日志记录方式上有更大的灵活性，但这目前只是计划中的工作。

  因此，**此环境变量应被视为实验性的，并且在未来为 ``rcl_logging_spdlog`` 日志后端添加配置文件支持时，可能会在没有弃用期的情况下被移除**。

有关此变更的更多详情，请参阅此拉取请求：https://github.com/ros2/rcl_logging/pull/95

``ament_cmake_auto``
^^^^^^^^^^^^^^^^^^^^

包含的依赖现在标记为 SYSTEM
"""""""""""""""""""""""""""

当使用 ``ament_auto_add_executable`` 或 ``ament_auto_add_library`` 时，依赖现在会自动添加为 ``SYSTEM``。
这意味着依赖项头文件中的警告将不会被报告。

更多详情请参阅 https://github.com/ament/ament_cmake/pull/385。

``ament_cmake_nose``
^^^^^^^^^^^^^^^^^^^^

软件包已被弃用并移除
""""""""""""""""""""

Python 的 ``nose`` 软件包早已被弃用。
由于当前发布到 Humble 或 Rolling 的开源软件包都不依赖它，此版本弃用并移除了围绕它的 ament 封装。

更多信息请参阅 https://github.com/ament/ament_cmake/pull/415。

``ament_lint``
^^^^^^^^^^^^^^

可以将文件排除在 linter 检查之外
""""""""""""""""""""""""""""""""

现在可以通过在调用 ``ament_lint_auto_find_test_dependencies`` 之前设置 ``AMENT_LINT_AUTO_FILE_EXCLUDE`` CMake 变量，将某些文件排除在 linter 检查之外。

更多信息请参阅 https://github.com/ament/ament_lint/pull/386。

``camera_info_manager``
^^^^^^^^^^^^^^^^^^^^^^^

生命周期节点支持
""""""""""""""""

``camera_info_manager`` 现在除了支持常规 ROS 2 节点外，还支持生命周期节点。

更多信息请参阅 https://github.com/ros-perception/image_common/pull/190。

``launch``
^^^^^^^^^^

``LaunchConfigurationEquals`` 和 ``LaunchConfigurationNotEquals`` 已弃用
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

``LaunchConfigurationEquals`` 和 ``LaunchConfigurationNotEquals`` 条件已弃用，将在未来的版本中移除。
应改用更通用的 ``Equals`` 和 ``NotEquals`` 替换。

更多详情请参阅 https://github.com/ros2/launch/pull/649。

``launch_ros``
^^^^^^^^^^^^^^

将名称中使用 ``Ros`` 的类重命名为 ``ROS``，以符合 PEP8
""""""""""""""""""""""""""""""""""""""""""""""""""""""

已更改的类：

* ``launch_ros.actions.RosTimer`` -> ``launch_ros.actions.ROSTimer``
* ``launch_ros.actions.PushRosNamespace`` -> ``launch.actions.PushROSNamespace``

旧的类名仍然存在，但将被弃用。

更多信息请参阅 https://github.com/ros2/launch_ros/pull/326。

``launch_xml``
^^^^^^^^^^^^^^

向 XML 前端暴露 ``emulate_tty``
"""""""""""""""""""""""""""""""

几个版本以来，launch Python 代码已经可以使用伪终端来模拟 TTY（从而做一些诸如打印颜色之类的事情）。
现在可以通过向可执行命令传递 ``emulate_tty`` 参数，在 XML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/669。

向 XML 前端暴露 ``sigterm_timeout`` 和 ``sigkill_timeout``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

几个版本以来，已经可以在 ``launch`` Python 代码中配置 SIGTERM 和 SIGKILL 信号的最大超时值。
现在可以通过向可执行命令传递 ``sigterm_timeout`` 或 ``sigkill_timeout`` 参数，在 XML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/667。

``launch_yaml``
^^^^^^^^^^^^^^^

向 YAML 前端暴露 ``emulate_tty``
""""""""""""""""""""""""""""""""

几个版本以来，launch Python 代码已经可以使用伪终端来模拟 TTY（从而做一些诸如打印颜色之类的事情）。
现在可以通过向可执行命令传递 ``emulate_tty`` 参数，在 YAML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/669。

向 YAML 前端暴露 ``sigterm_timeout`` 和 ``sigkill_timeout``
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

几个版本以来，已经可以在 ``launch`` Python 代码中配置 SIGTERM 和 SIGKILL 信号的最大超时值。
现在可以通过向可执行命令传递 ``sigterm_timeout`` 或 ``sigkill_timeout`` 参数，在 YAML 前端中使用该功能。

更多信息请参阅 https://github.com/ros2/launch/pull/667。

``message_filters``
^^^^^^^^^^^^^^^^^^^

新的近似时间策略
""""""""""""""""

添加了一个更简单的近似时间策略，名为 ``ApproximateEpsilonTime``。
此时间策略的工作方式类似于 ``ExactTime``，但允许时间戳处于 epsilon 容差范围内。
更多信息请参阅 https://github.com/ros2/message_filters/pull/84。

新的上采样时间策略
""""""""""""""""""

添加了一个新的时间策略，名为 ``LatestTime``。
它可以通过零阶保持上采样，按速率同步最多 9 条消息。
更多信息请参阅 https://github.com/ros2/message_filters/pull/73。

``rcl_yaml_param_parser``
^^^^^^^^^^^^^^^^^^^^^^^^^

参数文件中支持 YAML ``!!str`` 语法
""""""""""""""""""""""""""""""""""

现在可以使用 YAML ``!!str`` 语法强制 ROS 参数文件解析器将字段解释为字符串。
更多信息请参阅 https://github.com/ros2/rcl/pull/999。

``rclcpp``
^^^^^^^^^^

多线程执行器的默认线程数已更改
""""""""""""""""""""""""""""""

如果用户没有另行指定，多线程执行器的默认线程数将设置为机器上的 CPU 数量。
如果底层操作系统不支持获取此信息，则将其设置为 2。

更多信息请参阅 https://github.com/ros2/rclcpp/pull/2032。

当指定深度为 0 的 KEEP_LAST QoS 时现在会打印警告
""""""""""""""""""""""""""""""""""""""""""""""""

指定深度为 0 的 KEEP_LAST QoS 是一种无意义的配置，因为实体将无法发送或接收任何数据。
如果指定了这种组合，``rclcpp`` 现在会打印一条警告，但仍会继续运行，并让底层中间件选择一个合理的值（通常是深度为 1）。

更多信息请参阅 https://github.com/ros2/rclcpp/pull/2048。

已弃用的 ``RCLCPP_SCOPE_EXIT`` 宏已被移除
"""""""""""""""""""""""""""""""""""""""""

在 Humble 中，宏 ``RCLCPP_SCOPE_EXIT`` 已被弃用，取而代之的是 ``RCPPUTILS_SCOPE_EXIT``。
在 Iron 中，``RCLCPP_SCOPE_EXIT`` 宏已被完全移除。

``rclpy``
^^^^^^^^^

多线程执行器的默认线程数已更改
""""""""""""""""""""""""""""""

如果用户没有另行指定，多线程执行器的默认线程数将设置为机器上的 CPU 数量。
如果底层操作系统不支持获取此信息，则将其设置为 2。

更多信息请参阅 https://github.com/ros2/rclpy/pull/1031。

当指定深度为 0 的 KEEP_LAST QoS 时现在会打印警告
""""""""""""""""""""""""""""""""""""""""""""""""

指定深度为 0 的 KEEP_LAST QoS 是一种无意义的配置，因为实体将无法发送或接收任何数据。
如果指定了这种组合，``rclpy`` 现在会打印一条警告，但仍会继续运行，并让底层中间件选择一个合理的值（通常是深度为 1）。

更多信息请参阅 https://github.com/ros2/rclpy/pull/1048。

Time 和 Duration 与其他类型比较时不再抛出异常
"""""""""""""""""""""""""""""""""""""""""""""

现在可以将 ``rclpy.time.Time`` 和 ``rclpy.duration.Duration`` 与其他类型进行比较，而不会引发异常。
如果类型不可比较，比较将返回 ``False``。
请注意，这是相对于以往版本的行为变更。

.. code-block:: Python

  print(None in [rclpy.time.Time(), rclpy.duration.Duration()])  # Prints "False" instead of raising TypeError

更多信息请参阅 https://github.com/ros2/rclpy/pull/1007。

``rcutils``
^^^^^^^^^^^

提升消息日志的性能
""""""""""""""""""

输出日志消息所使用的代码（当 ``RCUTILS_LOG_*`` 或 ``RCLCPP_*`` 被调用时）已进行了优化，以减少开销。
这些日志消息现在应该更加高效，但仍不应以高速率调用。
更多信息请参阅 https://github.com/ros2/rcutils/pull/381、https://github.com/ros2/rcutils/pull/372、https://github.com/ros2/rcutils/pull/369 和 https://github.com/ros2/rcutils/pull/367。

已弃用的 ``rcutils/get_env.h`` 头文件已被移除
"""""""""""""""""""""""""""""""""""""""""""""

在 Humble 中，头文件 ``rcutils/get_env.h`` 已被弃用，取而代之的是 ``rcutils/env.h``。
在 Iron 中，``rcutils/get_env.h`` 头文件已被完全移除。

``rmw``
^^^^^^^

将 GID 存储更改为 16 字节
"""""""""""""""""""""""""

RMW 层中的 GID 旨在成为 ROS 图中写入者的全局唯一标识符。
此前，由于一个旧的 RMW 实现中的错误，它被错误地设置为 24 字节。
但 ``rmw`` 软件包应该对此进行定义，并且所有实现都应遵循该定义。
因此，本版本将其定义为 16 字节（DDS 标准），并更改了所有实现以使用该定义。

更多信息请参阅 https://github.com/ros2/rmw/pull/345 和（已关闭但相关的）https://github.com/ros2/rmw/pull/328。

``rmw_dds_common``
^^^^^^^^^^^^^^^^^^

将 GID 存储更改为 16 字节
"""""""""""""""""""""""""

随着 ``rmw`` 层中的变更，发送 GID 信息的消息也更改为 16 字节。

更多信息请参阅 https://github.com/ros2/rmw_dds_common/pull/68。

``ros2topic``
^^^^^^^^^^^^^

``ros2 topic hz/bw/pub`` 现在遵循 ``use_sim_time``
""""""""""""""""""""""""""""""""""""""""""""""""""

在仿真环境下运行时，ROS 2 生态通常从模拟器发布的 ``/clock`` 话题获取时间（而不是使用系统时钟）。
ROS 2 节点通常通过在节点上设置 ``use_sim_time`` 参数来获知这一变化。
由 ``ros2 topic`` 命令 ``hz``、``bw`` 和 ``pub`` 创建的节点现在会遵循该参数，并酌情使用仿真时间。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/754。

``rosbag2``
^^^^^^^^^^^

将默认 bag 文件类型更改为 ``mcap``
""""""""""""""""""""""""""""""""""

在此版本之前，rosbag2 默认会将数据记录到 sqlite3 数据库中。
在测试过程中，发现在许多情况下这不够高效，并且缺少某些离线处理所需的理想特性。

为了满足这些需求，开发了一种新的 bag 格式（受原始 ROS 1 bag 文件格式的影响），名为 ``mcap``。
这种 bag 文件格式具有 sqlite3 文件格式所缺失的许多特性，并且也应该更加高效。

本版本将 ``mcap`` 切换为写入新 bag 的默认文件格式。
旧的 ``sqlite3`` 文件格式仍然可用，用户可以在需要时选择用它来写入。
本版本还允许从 ``sqlite3`` 文件格式或 ``mcap`` 文件格式回放数据。

更多信息请参阅 https://github.com/ros2/rosbag2/pull/1160。

使用 SQLite3 插件在 bag 文件中存储消息定义
""""""""""""""""""""""""""""""""""""""""""

现在，我们支持以与保存到 ``mcap`` 文件相同的格式，将消息定义保存到 ``sqlite3`` 数据库文件中。
这为第三方工具提供了机会，使其无需在解码使用 ``sqlite3`` 插件录制的 bag 文件的机器上
拥有所有原始 .msg 文件的正确版本，即可反序列化 rosbag2 文件。

更多信息请参阅 https://github.com/ros2/rosbag2/issues/782 和 https://github.com/ros2/rosbag2/pull/1293。


新的回放和录制控制
""""""""""""""""""

已添加多个拉取请求以增强用户对 bag 回放的控制。
拉取请求 `960 <https://github.com/ros2/rosbag2/pull/960>`_ 增加了播放 bag 指定秒数的能力。
拉取请求 `1005 <https://github.com/ros2/rosbag2/pull/1005>`_ 允许播放 bag 直到指定的时间戳。
另一个拉取请求 `1007 <https://github.com/ros2/rosbag2/pull/1007>`_ 增加了通过服务调用远程停止回放的能力。
如果播放器处于暂停模式，停止操作会取消暂停，停止回放，并在回放进行中时强制退出 play() 方法。

通过服务调用管理录制
""""""""""""""""""""

现在有了从远程节点控制录制过程的新选项。
拉取请求 `1131 <https://github.com/ros2/rosbag2/pull/1131>`_ 增加了通过服务调用暂停和恢复录制的能力。
另一个拉取请求 `1115 <https://github.com/ros2/rosbag2/pull/1115>`_ 增加了在录制过程中通过发送服务调用分割 bag 的能力。

在回放期间通过正则表达式过滤话题
""""""""""""""""""""""""""""""""

用户有时只需要从录制的 bag 中回放一部分话题，以下两个拉取请求增加了这种能力。
拉取请求 `1034 <https://github.com/ros2/rosbag2/pull/1034>`_ 增加了一个新选项
``--topics-regex``，允许通过正则表达式过滤话题。
``--topics-regex`` 选项接受多个由空格分隔的正则表达式。
拉取请求 `1046 <https://github.com/ros2/rosbag2/pull/1046>`_ 增加了通过在新的 ``--exclude``
（和 ``-x``）选项中提供正则表达式来排除某些特定话题不被回放的能力。

允许插件注册自己的 CLI 动词参数
"""""""""""""""""""""""""""""""

拉取请求 `1209 <https://github.com/ros2/rosbag2/pull/1209>`_ 增加了 ``rosbag2`` 插件注册可选 Python 入口点以提供插件特定 CLI 参数值的能力。
因此，``ros2 bag record`` 动词的命令行选项 ``--storage-preset-profile`` 将根据底层存储插件拥有不同的有效选项。

其他变更
""""""""

拉取请求 `1038 <https://github.com/ros2/rosbag2/pull/1038>`_ 增加了在 metadata.yaml 文件的 'custom' 字段中记录任意键/值对的能力。
当用户需要保存一些硬件特定的 ID 或录制所在位置的坐标时，这很有用。
拉取请求 `1180 <https://github.com/ros2/rosbag2/pull/1180>`_ 增加了一个选项，通过提供新的命令行 ``--node-name`` 选项来更改录制器的底层节点名称。
此选项可用于使用多个 rosbag2 录制器实例创建远程分布式录制。
它提供了向专用 rosbag2 录制器实例发送服务调用以管理录制过程的能力。

``rosidl_python``
^^^^^^^^^^^^^^^^^

修改 ``__slots__`` 属性的内容
"""""""""""""""""""""""""""""

到目前为止，Python 消息类中的 ``__slots__`` 属性一直被用作包含消息字段名的成员。
在 Iron 中，此属性不再只包含消息结构中的字段名，而是包含所有类成员的字段名。
因此，用户不应依赖此属性来获取字段名信息，而应使用 ``get_field_and_field_types()`` 方法获取。

更多信息请参阅 https://github.com/ros2/rosidl_python/pull/194。

``rviz``
^^^^^^^^

地图显示现在可以以二进制形式显示
""""""""""""""""""""""""""""""""

RViz 地图显示现在可以以二进制形式显示地图，并带有可设置的阈值。
这在某些情况下很有用，例如检查地图，或与具有可设置阈值的规划器结合使用。

更多信息请参阅 https://github.com/ros2/rviz/pull/846。

相机显示插件遵循 CameraInfo 消息中的 ROI
""""""""""""""""""""""""""""""""""""""""

如果提供了 CameraInfo 消息中的感兴趣区域（ROI）设置，CameraDisplay 插件现在会遵循这些设置。
这考虑到了图像被相机驱动程序裁剪以减少带宽的情况。

更多信息请参阅 https://github.com/ros2/rviz/pull/864。

来自 SOLIDWORKS 的二进制 STL 文件可以正常使用
"""""""""""""""""""""""""""""""""""""""""""""

对 STL 加载器进行了一项更改，使其接受 SOLIDWORKS 中带有单词 "solid" 的二进制 STL 文件。
这在技术上违反了 STL 规范，但由于这种情况足够常见，因此添加了一个特殊情况来处理这些文件。

更多信息请参阅 https://github.com/ros2/rviz/pull/917。

``tracetools``
^^^^^^^^^^^^^^

Linux 上现在默认包含跟踪插桩
""""""""""""""""""""""""""""

ROS 2 核心已经有一段时间支持跟踪插桩了。
但是，它默认是被编译排除的。
要获得插桩，必须在从源代码重新构建 ROS 2 之前手动安装 LTTng 跟踪器。
在 Iron 中，跟踪插桩和跟踪点默认包含在内；因此 LTTng 跟踪器现在成为 ROS 2 的依赖。

请注意，这仅适用于 Linux。

更多信息请参阅 https://github.com/ros2/ros2_tracing/pull/31 和 https://github.com/ros2/ros2/issues/1177。
请参阅 :doc:`此操作指南，了解如何移除插桩（或为 Humble 及更早版本添加插桩）<../How-To-Guides/Building-ROS-2-with-Tracing>`。

新增了 ``rclcpp`` 进程内通信的跟踪点
""""""""""""""""""""""""""""""""""""

新增了跟踪点以支持 ``rclcpp`` 进程内通信。
这使得可以评估进程内通信中消息发布到回调开始之间的时间。

更多信息请参阅 https://github.com/ros2/ros2_tracing/pull/30 和 https://github.com/ros2/rclcpp/pull/2091。

已知问题
--------

* ``rmw_connextdds`` 无法与 Windows 二进制发布包配合使用。
  RTI 不再分发用于打包任务为 Windows 创建二进制文件的 ``RTI ConnextDDS 6.0.1``。
  相反，他们现在分发 ``RTI ConnextDDS 6.1.0``，它与生成的二进制文件 ABI 不兼容。
  解决方案是依赖在 Windows 上从源代码构建 ROS 2 和 ``rmw_connextdds``。

* Windows 上的 ``sros2`` 要求用户将 ``cryptography`` Python 模块降级到 ``cryptography==38.0.4``，如 `此处 <https://github.com/ros2/sros2/issues/285>`_ 所述。

* ``ros1_bridge`` 无法与来自 `上游 Ubuntu <https://packages.ubuntu.com/jammy/ros-core-dev>`_ 的 ROS Noetic 软件包配合使用。建议的解决办法是从源代码构建 ROS Noetic，然后使用它构建 ``ros1_bridge``。

发布计划
--------

    2022 年 11 月 - 平台决策
        更新 REP 2000，确定目标平台和主要依赖版本。

    到 2023 年 1 月 - Rolling 平台迁移
        构建农场更新为 Iron Irwini 的新平台版本和依赖版本（如有必要）。

    2023 年 4 月 10 日（周一）- Alpha + RMW 冻结
        ROS Base [1]_ 软件包的初步测试和稳定，以及 RMW 提供方软件包的 API 和功能冻结。

    2023 年 4 月 17 日（周一）- 冻结
        Rolling Ridley 中 ROS Base [1]_ 软件包的 API 和功能冻结。
        此后只应发布错误修复版本。
        新软件包可以独立发布。

    2023 年 4 月 24 日（周一）- 分支
        从 Rolling Ridley 分支。
        ``rosdistro`` 重新对 ROS Base [1]_ 软件包的 Rolling PR 开放。
        Iron 开发从 ``ros-rolling-*`` 软件包转向 ``ros-iron-*`` 软件包。

    2023 年 5 月 1 日（周一）- Beta
        ROS Desktop [2]_ 软件包的更新版本可用。
        呼吁进行普遍测试。

    2023 年 5 月 15 日（周一）- 候选发布版
        构建候选发布版软件包。
        ROS Desktop [2]_ 软件包的更新版本可用。

    2023 年 5 月 18 日（周四）- 发行版冻结
        冻结 rosdistro。
        ``rosdistro`` 仓库上针对 Iron 的 PR 将不会被合并（在发布公告后重新开放）。

    2023 年 5 月 23 日（周二）- 正式发布
        发布公告。
        ``rosdistro`` 重新对 Iron PR 开放。

.. [1] ``ros_base`` 变体在 `REP 2001 (ros-base) <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中有描述。
.. [2] ``desktop`` 变体在 `REP 2001 (desktop-variants) <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中有描述。

开发进展
--------

有关 Iron Irwini 开发和发布的进展，请参阅 `GitHub 跟踪问题 <https://github.com/ros2/ros2/issues/1298>`__。

有关 Iron Irwini 所遵循的总体流程，请参阅 :doc:`流程描述页面 <Release-Process>`。
