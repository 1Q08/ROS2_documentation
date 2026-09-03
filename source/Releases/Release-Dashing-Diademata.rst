Dashing Diademata (``dashing``)
===============================

.. contents:: 目录
   :depth: 2
   :local:

*Dashing Diademata* 是 ROS 2 的第四个版本。

支持的平台
----------

Dashing Diademata 根据 `平台支持等级 <../The-ROS2-Project/Platform-Support-Tiers>` 支持以下平台：

一级平台：

* Ubuntu 18.04 (Bionic)：``amd64`` 和 ``arm64``
* Mac macOS 10.12 (Sierra)
* Windows 10 (Visual Studio 2019)

二级平台：

* Ubuntu 18.04 (Bionic)：``arm32``

三级平台：

* Debian Stretch (9)：``amd64``、``arm64`` 和 ``arm32``
* OpenEmbedded Thud (2.6) / webOS OSE：``arm32`` 和 ``x86``

目标平台：

+--------------+----------------------+----------------------+--------------------+--------------------+----------------+
| 架构         | Ubuntu Bionic        | MacOS Sierra         | Windows 10         | Debian Stretch     | OpenEmbedded / |
|              | (18.04)              | (10.12)              | (VS2019)           | (9)                | webOS OSE      |
+==============+======================+======================+====================+====================+================+
| amd64        | Tier 1 [d][a][s]     | Tier 1 [a][s]        | Tier 1 [a][s]      | Tier 3 [s]         |                |
+--------------+----------------------+----------------------+--------------------+--------------------+----------------+
| arm64        | Tier 1 [d][a][s]     |                      |                    | Tier 3 [s]         | Tier 3 [s]     |
+--------------+----------------------+----------------------+--------------------+--------------------+----------------+
| arm32        | Tier 2 [a][s]        |                      |                    | Tier 3 [s]         | Tier 3 [s]     |
+--------------+----------------------+----------------------+--------------------+--------------------+----------------+


以下指标显示了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为此平台提供 Debian 软件包。

\" \[a\] \" 二进制版本以单个归档文件的形式为每个平台提供，其中包含 Dashing ROS 2 repos 文件[^6] 中的所有软件包。

\" \[s\] \" 从源码编译。

中间件实现支持：

+--------------------------+---------------------+---------------+--------------------------+--------------------------+
| 中间件库                 | 中间件提供方        | 支持等级      | 平台                     | 架构                     |
+==========================+=====================+===============+==========================+==========================+
| rmw_fastrtps_cpp*        | eProsima Fast-RTPS  | Tier 1        | All Platforms            | All Architectures        |
+--------------------------+---------------------+---------------+--------------------------+--------------------------+
| rmw_connext_cpp          | RTI Connext         | Tier 1        | All Platforms except     | All Architectures except |
|                          |                     |               | Debian and OpenEmbedded  | arm64/arm32              |
+--------------------------+---------------------+---------------+--------------------------+--------------------------+
| rmw_cyclonedds_cpp       | Eclipse Cyclone DDS | Tier 2        | All Platforms            | All Architectures        |
+--------------------------+---------------------+---------------+--------------------------+--------------------------+
| rmw_opensplice_cpp       | ADLink OpenSplice   | Tier 2        | All Platforms except     | All Architectures        |
|                          |                     |               | Debian and OpenEmbedded  |                          |
+--------------------------+---------------------+---------------+--------------------------+--------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-RTPS  | Tier 2        | All Platforms            | All Architectures        |
+--------------------------+---------------------+---------------+--------------------------+--------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持等级。例如，二级平台上的一级中间件实现只能获得二级支持。

最低语言要求：

- C++14
- Python 3.5

依赖要求：

+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
|              | 必需支持                                            | 推荐支持                                |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| 软件包       | Ubuntu Bionic   | MacOS**         | Windows 10**    | Debian Stretch  | OpenEmbedded**        |
+==============+=================+=================+=================+=================+=======================+
| CMake        | 3.10.2          | 3.14.4          | 3.14.4          | 3.7.2           | 3.16.1 / 3.12.2***    |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| EmPY         | 3.3.2                                                                                         |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Gazebo       | 9.0.0           | 9.9.0           | N/A             | 9.8.0*          | N/A                   |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Ogre         | 1.10*                                                                 | N/A                   |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| OpenCV       | 3.2.0           | 4.1.0           | 3.4.6*          | 3.2*            | 4.1.0 / 3.2.0***      |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| OpenSSL      | 1.1.0g          | 1.0.2r          | 1.0.2r          | 1.1.0j          | 1.1.1d / 1.1.1b***    |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Poco         | 1.8.0           | 1.9.0           | 1.8.0*          | 1.8.0*          | 1.9.4                 |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Python       | 3.6.5           | 3.7.3           | 3.7.3           | 3.5.3           | 3.8.2 / 3.7.5***      |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Qt           | 5.9.5           | 5.12.3          | 5.10.0          | 5.7.1           | 5.14.1 / 5.12.5***    |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
|              |                 | **仅 Linux**                      |                                         |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| PCL          | 1.8.1           | N/A             | N/A             | 1.8.0           | 1.8.1                 |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| **RMW DDS 中间件提供方**                                                                                     |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Connext DDS  | 5.3.1                                               | N/A                                     |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Cyclone DDS  | 0.7.x (Coquette)                                                                              |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| Fast-RTPS    | 1.8.0                                                                                         |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+
| OpenSplice   | 6.9.190403OSS                                                         | N/A                   |
+--------------+-----------------+-----------------+-----------------+-----------------+-----------------------+

\" \* \" 表示这不是上游版本（可在官方操作系统仓库中获得），而是由 OSRF 或社区分发的软件包（在自定义仓库中构建和分发）。

\" \*\* \" 滚动发行版在其生命周期内会看到这些依赖项的多次版本变更。OpenEmbedded 显示的版本是 3.1 Dunfell 版本系列提供的版本；其他受支持的版本系列提供的版本列在此处：<https://github.com/ros/meta-ros/wiki/Package-Version-Differences> 。请注意，ROS 发行版支持的 OpenEmbedded 版本系列在其支持时间范围内会发生变化，依据此处显示的 OpenEmbedded 支持策略：<https://github.com/ros/meta-ros/wiki/Policies#openembedded-release-series-support> 。不过，它始终会由至少一个稳定的 OpenEmbedded 版本系列支持。

\" \*\*\* \" webOS OSE 提供此不同版本。

本文档仅记录 ROS 发行版首次发布时的版本，并且不会随着依赖项的更新而更新。因此这些版本是一个低水位线。

依赖项的包管理器使用情况：

- Ubuntu、Debian：apt
- MacOS：Homebrew、pip
- Windows：Chocolatey、pip
- OpenEmbedded：opkg

构建系统支持：

- ament_cmake
- cmake
- setuptools

安装
----

`安装 Dashing Diademata <../../dashing/Installation.html>`__

此 ROS 2 版本中的新功能
-----------------------

我们想重点介绍的一些功能和改进：

* :doc:`组件 <../Tutorials/Intermediate/Composition>` 现在是编写节点的推荐方式。
  它们既可以独立使用，也可以在进程内组合使用，并且这两种方式都通过 ``launch`` 文件得到完整支持。
* :doc:`进程内通信 <../Tutorials/Demos/Intra-Process-Communication>` （仅 C++）已得到改进——无论是延迟还是减少拷贝方面。
* Python 客户端库已更新，以匹配大多数 C++ 等价功能，并且一些重要的错误修复和与内存使用及性能相关的改进也已落地。
* 参数现在是 ROS 1 中 ``dynamic_reconfigure`` 的完整替代品，包括范围或只读等约束。
* 通过依赖（子集）`IDL 4.2 <https://www.omg.org/spec/IDL/4.2>`__ 进行消息生成流水线，现在可以使用 ``.idl`` 文件（除了 ``.msg`` / ``.srv`` / ``.action`` 文件）。
  此更改同时支持普通字符串的可选 UTF-8 编码以及 UTF-16 编码的多字节字符串（见 `宽字符串设计文章 <https://design.ros2.org/articles/wide_strings.html>`__）。
* 与 ``actions`` 和 ``components`` 相关的命令行工具。
* 支持 Deadline、Lifespan 和 Liveliness 服务质量设置。
* MoveIt 2 `alpha 版本 <https://github.com/AcutronicRobotics/moveit2/releases/tag/moveit_2_alpha>`__。

请参阅 GitHub 上的 `Dashing 元工单 <https://github.com/ros2/ros2/issues/607>`__，其中包含更多信息以及对带有额外详细信息的具体工单的引用。


自 Crystal 版本以来的变更
-------------------------

声明参数
^^^^^^^^

从 Dashing 开始，参数的行为发生了一些变化，这也带来了一些新的 API 以及其他 API 的弃用。
有关 API 更改的更多信息，请参阅下面的 ``rclcpp`` 和 ``rclpy`` 章节。

获取和设置未声明的参数
""""""""""""""""""""""

从 Dashing 开始，参数现在需要先声明，然后才能被访问或设置。

在 Dashing 之前，你可以调用 ``get_parameter(name)``，如果它之前被设置过，就能得到一个值，否则得到类型为 ``PARAMETER_NOT_SET`` 的参数。
你也可以在任何时候调用 ``set_parameter(name, value)``，即使该参数之前未设置。

从 Dashing 开始，你需要先声明一个参数，然后才能获取或设置它。
如果你尝试获取或设置一个未声明的参数，你会得到一个抛出的异常（例如 ParameterNotDeclaredException），或者在某些情况下会以多种方式收到一个不成功的结果（更多详细信息请参阅具体函数）。

不过，通过在创建节点时使用 ``allow_undeclared_parameters`` 选项，你可以获得旧行为（大部分情况下，见下一段中的说明）。
你可能希望这样做，以便暂时避免代码更改，或满足一些不常见的用例。
例如，“全局参数服务器”或“参数黑板”可能希望允许外部节点在未先声明的情况下在其上设置新参数，因此它可以使用 ``allow_undeclared_parameters`` 选项来实现这一点。
然而，在大多数情况下，不推荐使用此选项，因为它会使参数 API 的其余部分对参数名拼写错误和“使用前设置”等逻辑错误的安全性降低。

请注意，使用 ``allow_undeclared_parameters`` 可以让你获得大部分旧行为，特别是“get”和“set”方法的行为，但它不会将所有与参数相关的行为更改还原为 ROS Crystal 中的方式。
为此，你还需要将 ``automatically_declare_parameters_from_overrides`` 选项设置为 ``true``，这在下文的 :ref:`使用 YAML 文件进行参数配置 <parameter-configuration-using-a-yaml-file>` 中有描述。

使用 ParameterDescriptor 声明参数
"""""""""""""""""""""""""""""""""

在使用参数之前声明参数的另一个好处是，它允许你同时声明一个参数描述符（ParameterDescriptor）。

现在，在声明参数时，你可以包含一个自定义的 ``ParameterDescriptor`` 以及名称和默认值。
``ParameterDescriptor`` 在 ``rcl_interfaces/msg/ParameterDescriptor`` 中定义为一个消息，包含诸如 ``description`` 之类的元数据以及 ``read_only`` 或 ``integer_range`` 之类的约束。
这些约束可用于在设置参数时拒绝无效值，和/或作为向外部工具提示给定参数的有效值。
``read_only`` 约束将阻止参数值在声明后被更改，并阻止其被取消声明。

作为参考，以下是撰写本文时的 ``ParameterDescriptor`` 消息链接：

https://github.com/ros2/rcl_interfaces/blob/0aba5a142878c2077d7a03977087e7d74d40ee68/rcl_interfaces/msg/ParameterDescriptor.msg#L1

.. _parameter-configuration-using-a-yaml-file:

使用 YAML 文件进行参数配置
""""""""""""""""""""""""""

从 Dashing 开始，YAML 配置文件中的参数（例如通过命令行参数 ``__params:=`` 传递给节点）仅在声明参数时用于覆盖参数的默认值。

在 Dashing 之前，你通过 YAML 文件传递的任何参数都会被隐式地设置在节点上。

从 Dashing 开始，情况不再如此，因为参数需要被声明，才能出现在节点上供外部观察者（如 ``ros2 param list``）查看。

可以通过在创建节点时使用 ``automatically_declare_parameters_from_overrides`` 选项来获得旧行为。
如果此选项设置为 ``true``，则在构造节点时自动声明输入 YAML 文件中的所有参数。
这可用于避免对现有代码进行大的更改，或服务于特定用例。
例如，“全局参数服务器”可能希望在启动时用任意参数进行播种，而这些参数它无法提前声明。
然而，大多数时候不推荐使用此选项，因为它可能导致在 YAML 文件中设置一个参数时假设节点会使用它，即使节点实际上并没有使用它。

未来我们希望有一个检查器，如果你向节点传递了它不期望的参数，它会警告你。

YAML 文件中的参数将继续在参数首次声明时影响其值。

ament_cmake
^^^^^^^^^^^

CMake 函数 ``ament_index_has_resource`` 之前返回 ``TRUE`` 或 ``FALSE``。
自 `此版本 <https://github.com/ament/ament_cmake/pull/155>`_ 起，如果找到资源，它返回前缀路径，否则返回 ``FALSE``。

如果你在 CMake 条件中像这样使用返回值：

.. code-block:: cmake

   ament_index_has_resource(var ...)
   if(${var})

你需要更新条件，以确保它将字符串值视为 ``TRUE``：

.. code-block:: cmake

   if(var)

rclcpp
^^^^^^

``Node::get_node_names()`` 的行为变更
"""""""""""""""""""""""""""""""""""""

函数 ``NodeGraph::get_node_names()``，因此也包括 ``Node::get_node_names()``，现在返回一个 ``std::vector<std::string>``，其中包含带命名空间的完全限定节点名，而不仅仅是节点名。

向节点传递选项的方式已更改
""""""""""""""""""""""""""

``rclcpp::Node()`` 构造函数的扩展参数（超出名称和命名空间的部分）已被替换为 ``rclcpp::NodeOptions`` 结构。
有关该结构及选项默认值的详细信息，请参阅 `ros2/rclcpp#622 <https://github.com/ros2/rclcpp/pull/622/files>`__。

如果你正在像这样使用 ``rclcpp::Node()`` 的任何扩展参数：

.. code-block:: cpp

  auto context = rclcpp::contexts::default_context::get_global_default_context();
  std::vector<std::string> args;
  std::vector<rclcpp::Parameter> params = { rclcpp::Parameter("use_sim_time", true) };
  auto node = std::make_shared<rclcpp::Node>("foo_node", "bar_namespace", context, args, params);

你需要更新为使用 ``NodeOptions`` 结构

.. code-block:: cpp

  std::vector<std::string> args;
  std::vector<rclcpp::Parameter> params = { rclcpp::Parameter("use_sim_time", true) };
  rclcpp::NodeOptions node_options;
  node_options.arguments(args);
  node_options.parameter_overrides(params);
  auto node = std::make_shared<rclcpp::Node>("foo_node", "bar_namespace", node_options);

创建发布器和订阅器的更改
""""""""""""""""""""""""

在 Dashing 中，创建发布器和订阅器的方式发生了一些变化：

- QoS 设置现在使用新的 ``rclcpp::QoS`` 类传递，并且 API 鼓励用户至少指定历史深度。
- 选项现在以对象形式传递，即 ``rclcpp::PublisherOptions`` 和 ``rclcpp::SubscriptionOptions``。

所有更改都是向后兼容的（无需更改代码），但一些现有的调用风格已被弃用。
鼓励用户更新到新的签名。

----

过去，在创建发布器或订阅器时，你可以不指定任何 QoS 设置（例如只为发布器提供话题名称），也可以指定一个已设置好所有设置的“qos profile”数据结构（类型为 ``rmw_qos_profile_t``）。
现在你必须使用新的 ``rclcpp::QoS`` 对象来指定你的 QoS，以及至少指定 QoS 的历史设置。
这鼓励用户在使用 ``KEEP_LAST`` 时指定历史深度，而不是默认使用一个可能合适也可能不合适的值。

在 ROS 1 中，这被称为 ``queue_size``，并且在 C++ 和 Python 中都是必需的。
我们正在更改 ROS 2 API 以恢复这一要求。

----

此外，以前在创建发布器或订阅器时可以传递的任何选项，现在已分别封装在 ``rclcpp::PublisherOptions`` 和 ``rclcpp::SubscriptionOptions`` 类中。
这使得签名更短、使用更方便，并且可以在不破坏 API 的情况下添加新的未来选项。

----

一些用于创建发布器和订阅器的签名现在已被弃用，并添加了新的签名，使你能够使用新的 ``rclcpp::QoS`` 和发布器/订阅器选项类。

以下是新的推荐 API：

.. code-block:: cpp

  template<
    typename MessageT,
    typename AllocatorT = std::allocator<void>,
    typename PublisherT = ::rclcpp::Publisher<MessageT, AllocatorT>>
  std::shared_ptr<PublisherT>
  create_publisher(
    const std::string & topic_name,
    const rclcpp::QoS & qos,
    const PublisherOptionsWithAllocator<AllocatorT> & options =
    PublisherOptionsWithAllocator<AllocatorT>()
  );

  template<
    typename MessageT,
    typename CallbackT,
    typename AllocatorT = std::allocator<void>,
    typename SubscriptionT = rclcpp::Subscription<
      typename rclcpp::subscription_traits::has_message_type<CallbackT>::type, AllocatorT>>
  std::shared_ptr<SubscriptionT>
  create_subscription(
    const std::string & topic_name,
    const rclcpp::QoS & qos,
    CallbackT && callback,
    const SubscriptionOptionsWithAllocator<AllocatorT> & options =
    SubscriptionOptionsWithAllocator<AllocatorT>(),
    typename rclcpp::message_memory_strategy::MessageMemoryStrategy<
      typename rclcpp::subscription_traits::has_message_type<CallbackT>::type, AllocatorT
    >::SharedPtr
    msg_mem_strat = nullptr);

以下是已弃用的 API：

.. code-block:: cpp

  template<
    typename MessageT,
    typename AllocatorT = std::allocator<void>,
    typename PublisherT = ::rclcpp::Publisher<MessageT, AllocatorT>>
  [[deprecated("use create_publisher(const std::string &, const rclcpp::QoS &, ...) instead")]]
  std::shared_ptr<PublisherT>
  create_publisher(
    const std::string & topic_name,
    size_t qos_history_depth,
    std::shared_ptr<AllocatorT> allocator);

  template<
    typename MessageT,
    typename AllocatorT = std::allocator<void>,
    typename PublisherT = ::rclcpp::Publisher<MessageT, AllocatorT>>
  [[deprecated("use create_publisher(const std::string &, const rclcpp::QoS &, ...) instead")]]
  std::shared_ptr<PublisherT>
  create_publisher(
    const std::string & topic_name,
    const rmw_qos_profile_t & qos_profile = rmw_qos_profile_default,
    std::shared_ptr<AllocatorT> allocator = nullptr);

  template<
    typename MessageT,
    typename CallbackT,
    typename Alloc = std::allocator<void>,
    typename SubscriptionT = rclcpp::Subscription<
      typename rclcpp::subscription_traits::has_message_type<CallbackT>::type, Alloc>>
  [[deprecated(
    "use create_subscription(const std::string &, const rclcpp::QoS &, CallbackT, ...) instead"
  )]]
  std::shared_ptr<SubscriptionT>
  create_subscription(
    const std::string & topic_name,
    CallbackT && callback,
    const rmw_qos_profile_t & qos_profile = rmw_qos_profile_default,
    rclcpp::callback_group::CallbackGroup::SharedPtr group = nullptr,
    bool ignore_local_publications = false,
    typename rclcpp::message_memory_strategy::MessageMemoryStrategy<
      typename rclcpp::subscription_traits::has_message_type<CallbackT>::type, Alloc>::SharedPtr
    msg_mem_strat = nullptr,
    std::shared_ptr<Alloc> allocator = nullptr);

  template<
    typename MessageT,
    typename CallbackT,
    typename Alloc = std::allocator<void>,
    typename SubscriptionT = rclcpp::Subscription<
      typename rclcpp::subscription_traits::has_message_type<CallbackT>::type, Alloc>>
  [[deprecated(
    "use create_subscription(const std::string &, const rclcpp::QoS &, CallbackT, ...) instead"
  )]]
  std::shared_ptr<SubscriptionT>
  create_subscription(
    const std::string & topic_name,
    CallbackT && callback,
    size_t qos_history_depth,
    rclcpp::callback_group::CallbackGroup::SharedPtr group = nullptr,
    bool ignore_local_publications = false,
    typename rclcpp::message_memory_strategy::MessageMemoryStrategy<
      typename rclcpp::subscription_traits::has_message_type<CallbackT>::type, Alloc>::SharedPtr
    msg_mem_strat = nullptr,
    std::shared_ptr<Alloc> allocator = nullptr);

----

QoS 传递方式的更改最有可能影响用户。

发布器的典型更改如下：

.. code-block:: diff

  - pub_ = create_publisher<std_msgs::msg::String>("chatter");
  + pub_ = create_publisher<std_msgs::msg::String>("chatter", 10);

对于订阅器：

.. code-block:: diff

  - sub_ = create_subscription<std_msgs::msg::String>("chatter", callback);
  + sub_ = create_subscription<std_msgs::msg::String>("chatter", 10, callback);

如果你不知道该使用什么深度，并且现在不在乎（可能只是在做原型），那么我们建议使用 ``10``，因为这是之前的默认值，应该能保持现有行为。

关于如何选择合适深度的更深入文档即将推出。

这是一个稍微复杂一点的更改示例，用于避免新弃用的 API：

.. code-block:: diff

  - // Creates a latched topic
  - rmw_qos_profile_t qos = rmw_qos_profile_default;
  - qos.depth = 1;
  - qos.durability = RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL;
  -
    model_xml_.data = model_xml;
    node_handle->declare_parameter("robot_description", model_xml);
    description_pub_ = node_handle->create_publisher<std_msgs::msg::String>(
  -   "robot_description", qos);
  +   "robot_description",
  +   // Transient local is similar to latching in ROS 1.
  +   rclcpp::QoS(1).transient_local());

有关更多示例和详细信息，请参阅引入 QoS 更改的 pull request（以及相关联的 pull request）：

- https://github.com/ros2/rclcpp/pull/713

  - https://github.com/ros2/demos/pull/332
  - https://github.com/ros2/robot_state_publisher/pull/19
  - 以及其他……


由于声明参数更改带来的变更
""""""""""""""""""""""""""

有关实际行为更改的详细信息，请参阅上文的 `声明参数`_。

在 ``rclcpp::Node`` 接口中有几个新的 API 调用：

- 声明参数的方法，给定名称、可选的默认值、可选的描述符，并返回实际设置的值：

  .. code-block:: c++

    const rclcpp::ParameterValue &
    rclcpp::Node::declare_parameter(
      const std::string & name,
      const rclcpp::ParameterValue & default_value = rclcpp::ParameterValue(),
      const rcl_interfaces::msg::ParameterDescriptor & parameter_descriptor =
      rcl_interfaces::msg::ParameterDescriptor());

    template<typename ParameterT>
    auto
    rclcpp::Node::declare_parameter(
      const std::string & name,
      const ParameterT & default_value,
      const rcl_interfaces::msg::ParameterDescriptor & parameter_descriptor =
      rcl_interfaces::msg::ParameterDescriptor());

    template<typename ParameterT>
    std::vector<ParameterT>
    rclcpp::Node::declare_parameters(
      const std::string & namespace_,
      const std::map<std::string, ParameterT> & parameters);

    template<typename ParameterT>
    std::vector<ParameterT>
    rclcpp::Node::declare_parameters(
      const std::string & namespace_,
      const std::map<
        std::string,
        std::pair<ParameterT, rcl_interfaces::msg::ParameterDescriptor>
      > & parameters);

- 用于取消声明参数并检查参数是否已声明的方法：

  .. code-block:: c++

    void
    rclcpp::Node::undeclare_parameter(const std::string & name);

    bool
    rclcpp::Node::has_parameter(const std::string & name) const;

- 一些以前不存在的便捷方法：

  .. code-block:: c++

    rcl_interfaces::msg::SetParametersResult
    rclcpp::Node::set_parameter(const rclcpp::Parameter & parameter);

    std::vector<rclcpp::Parameter>
    rclcpp::Node::get_parameters(const std::vector<std::string> & names) const;

    rcl_interfaces::msg::ParameterDescriptor
    rclcpp::Node::describe_parameter(const std::string & name) const;

- 一个新方法，用于设置回调，该回调在参数即将被更改时调用，让你有机会拒绝更改：

  .. code-block:: c++

    using OnParametersSetCallbackType =
      rclcpp::node_interfaces::NodeParametersInterface::OnParametersSetCallbackType;

    OnParametersSetCallbackType
    rclcpp::Node::set_on_parameters_set_callback(
      OnParametersSetCallbackType callback);

还有一些已弃用的方法：

  .. code-block:: c++

    template<typename ParameterT>
    [[deprecated("use declare_parameter() instead")]]
    void
    rclcpp::Node::set_parameter_if_not_set(
      const std::string & name,
      const ParameterT & value);

    template<typename ParameterT>
    [[deprecated("use declare_parameters() instead")]]
    void
    rclcpp::Node::set_parameters_if_not_set(
      const std::string & name,
      const std::map<std::string, ParameterT> & values);

    template<typename ParameterT>
    [[deprecated("use declare_parameter() and it's return value instead")]]
    void
    rclcpp::Node::get_parameter_or_set(
      const std::string & name,
      ParameterT & value,
      const ParameterT & alternative_value);

    template<typename CallbackT>
    [[deprecated("use set_on_parameters_set_callback() instead")]]
    void
    rclcpp::Node::register_param_change_callback(CallbackT && callback);

内存策略
""""""""

接口 ``rclcpp::memory_strategy::MemoryStrategy`` 曾在各种方法签名中使用 typedef ``WeakNodeVector``。
从 Dashing 开始，该 typedef 已更改为 ``WeakNodeList``，并且各种方法中的参数类型也随之更改。
任何自定义内存策略都需要更新以匹配修改后的接口。

相关 API 更改可以在 `ros2/rclcpp#741 <https://github.com/ros2/rclcpp/pull/741>`__ 中找到。

rclcpp_components
^^^^^^^^^^^^^^^^^

在 Dashing 中实现组合的正确方法是使用 ``rclcpp_components`` 包。

为了正确实现运行时组合，必须对节点进行以下更改：

节点必须有一个接受 ``rclcpp::NodeOptions`` 的构造函数：

.. code-block:: cpp

  class Listener: public rclcpp::Node {
    Listener(const rclcpp::NodeOptions & options)
    : Node("listener", options)
    {
    }
  };

C++ 注册宏（如果存在）需要更新为使用 ``rclcpp_components`` 的等价宏。
如果不存在，则必须在一个翻译单元中添加注册宏。

.. code-block:: cpp

  // Insert at bottom of translation unit, e.g. listener.cpp
  #include "rclcpp_components/register_node_macro.hpp"
  // Use fully-qualifed name in registration
  RCLCPP_COMPONENTS_REGISTER_NODE(composition::Listener);

CMake 注册宏（如果存在）需要更新。
如果不存在，则必须将注册宏添加到项目的 CMake 中。

.. code-block:: cmake

  add_library(listener src/listener.cpp)
  rclcpp_components_register_nodes(listener "composition::Listener")

有关组合的更多信息，请参阅 `教程 <../Tutorials/Intermediate/Writing-a-Composable-Node>`

rclpy
^^^^^

创建发布器、订阅器和 QoS 配置文件的更改
"""""""""""""""""""""""""""""""""""""""

在 Dashing 之前，你可以在创建发布器或订阅器时可选地提供一个 ``QoSProfile`` 对象。
为了鼓励用户为消息队列指定历史深度，我们现在**要求**在创建发布器或订阅器时提供深度值或 ``QoSProfile`` 对象。

要创建发布器，以前你会这样写：

.. code-block:: python

  node.create_publisher(Empty, 'chatter')
  # Or using a keyword argument for QoSProfile
  node.create_publisher(Empty, 'chatter', qos_profile=qos_profile_sensor_data)

在 Dashing 中，建议使用以下 API，将深度值或 ``QoSProfile`` 对象作为第三个位置参数提供：

.. code-block:: python

  # Assume a history setting of KEEP_LAST with depth 10
  node.create_publisher(Empty, 'chatter', 10)
  # Or pass a QoSProfile object directly
  node.create_publisher(Empty, 'chatter', qos_profile_sensor_data)

对于订阅器，以前你会这样写：

.. code-block:: python

  node.create_subscription(BasicTypes, 'chatter', lambda msg: print(msg))
  # Or using a keyword argument for QoSProfile
  node.create_subscription(BasicTypes, 'chatter', lambda msg: print(msg), qos_profile=qos_profile_sensor_data)

In Dashing:

.. code-block:: python

  # Assume a history setting of KEEP_LAST with depth 10
  node.create_subscription(BasicTypes, 'chatter', lambda msg: print(msg), 10)
  # Or pass a QoSProfile object directly
  node.create_subscription(BasicTypes, 'chatter', lambda msg: print(msg), qos_profile_sensor_data)

为了缓解过渡，不使用新 API 的用户将看到弃用警告。

此外，我们还要求在构造 ``QoSProfile`` 对象时设置历史策略和/或深度。
如果提供了 ``KEEP_LAST`` 历史策略，则还需要提供深度参数。
例如，以下调用是有效的：

.. code-block:: python

  QoSProfile(history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_ALL)
  QoSProfile(history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST, depth=10)
  QoSProfile(depth=10)  # equivalent to the previous line

而以下调用会导致弃用警告：

.. code-block:: python

  QoSProfile()
  QoSProfile(reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT)
  # KEEP_LAST but no depth
  QoSProfile(history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST)

有关引入此更改的更多详细信息，请参阅相关的 issue 和 pull request：

- https://github.com/ros2/rclpy/issues/342
- https://github.com/ros2/rclpy/pull/344


由于声明参数更改带来的变更
""""""""""""""""""""""""""

有关实际行为更改的详细信息，请参阅上文的 `声明参数`_。这些更改与 ``rclcpp`` 中的更改类似。

以下是 ``rclpy.node.Node`` 接口中可用的新 API 方法：

- 声明参数，给定名称、可选的默认值（由 ``rcl_interfaces.msg.ParameterValue`` 支持）和可选的描述符，并返回实际设置的值：

  .. code-block:: python

      def declare_parameter(
          name: str,
          value: Any = None,
          descriptor: ParameterDescriptor = ParameterDescriptor()
      ) -> Parameter

      def declare_parameters(
        namespace: str,
        parameters: List[Union[
            Tuple[str],
            Tuple[str, Any],
            Tuple[str, Any, ParameterDescriptor],
        ]]
      ) -> List[Parameter]

- 取消声明之前声明的参数，并检查参数是否已事先声明：

  .. code-block:: python

      def undeclare_parameter(name: str) -> None

      def has_parameter(name: str) -> bool

- 获取和设置参数描述符：

  .. code-block:: python

      def describe_parameter(name: str) -> ParameterDescriptor

      def describe_parameters(names: List[str]) -> List[ParameterDescriptor]

      def set_descriptor(
          name: str,
          descriptor: ParameterDescriptor,
          alternative_value: Optional[ParameterValue] = None
      ) -> ParameterValue

- 用于获取可能尚未声明的参数的便捷方法：

  .. code-block:: python

      def get_parameter_or(name: str, alternative_value: Optional[Parameter] = None) -> Parameter

其他更改
""""""""

``rclpy.parameter.Parameter`` 现在可以自动推断其类型，而无需显式设置（只要它是 ``rcl_interfaces.msg.ParameterValue`` 支持的类型之一）。
例如，以下代码：

  .. code-block:: python

      p = Parameter('myparam', Parameter.Type.DOUBLE, 2.41)

等价于以下代码：

  .. code-block:: python

      p = Parameter('myparam', value=2.41)

此更改不会破坏现有 API。

rosidl
^^^^^^

在 Crystal 之前，每个消息生成器包使用 ``ament_cmake`` 扩展点 ``rosidl_generate_interfaces`` 注册自身，并接收一组 ``.msg`` / ``.srv`` / ``.action`` 文件。
从 Dashing 开始，消息生成流水线改为基于 ``.idl`` 文件。

任何消息生成器包都需要更改，并使用新的扩展点 ``rosidl_generate_idl_interfaces`` 注册自身，该扩展点只传递 ``.idl`` 文件。
常用语言 C、C++ 和 Python 的消息生成器，以及用于 introspection、Fast RTPS、Connext 和 OpenSplice 的 typesupport 包已经更新（见 `ros2/rosidl#334 <https://github.com/ros2/rosidl/pull/334/files>`__）。
调用 ``rosidl_generate_interfaces()`` 的 CMake 代码可以直接传递 ``.idl`` 文件，也可以传递 ``.msg`` / ``.srv`` / ``.action`` 文件，这些文件会在传递给每个消息生成器之前在内部转换为 ``.idl`` 文件。

``.msg`` / ``.srv`` / ``.action`` 文件的格式在未来不会继续演进。
``.msg`` / ``.srv`` / ``.action`` 文件与 ``.idl`` 文件之间的映射在 `此设计文章 <https://design.ros2.org/articles/legacy_interface_definition.html>`__ 中描述。
`第二篇设计文章 <https://design.ros2.org/articles/idl_interface_definition.html>`__ 描述了 ``.idl`` 文件支持的特性。
为了利用任何新特性，现有的接口需要被转换（例如使用命令行工具 ``msg2idl`` / ``srv2idl`` / ``action2idl``）。

为了区分同名但命名空间不同的类型，introspection 结构体现在包含一个命名空间字段，取代了包名（见 `ros2/rosidl#335 <https://github.com/ros2/rosidl/pull/355/files>`_）。

.msg 文件中 char 的映射
"""""""""""""""""""""""

在 `ROS 1 <https://wiki.ros.org/msg#Fields>`__ 中，``char`` 已被弃用很长时间，并被映射为 ``uint8``。
在 ROS 2 中，直到 Crystal 之前，``char`` 被映射为单个字符（C / C++ 中的 ``char``，Python 中长度为 1 的 ``str``），以努力提供更自然的映射。
从 Dashing 开始，恢复了 ROS 1 的语义，``char`` 再次映射为 ``uint8``。

rosidl_generator_cpp
^^^^^^^^^^^^^^^^^^^^

为消息、服务和动作生成的 C++ 数据结构为每个字段提供了 setter 方法。
在 Crystal 之前，每个 setter 返回指向数据结构本身的指针，以支持命名参数惯用法。
从 Dashing 开始，这些 setter 改为 `返回引用 <https://github.com/ros2/rosidl/pull/353>`__，因为这似乎是更常见的签名，而且它明确了返回值不可能是 ``nullptr``。

rosidl_generator_py
^^^^^^^^^^^^^^^^^^^

在 Crystal 之前，消息中的数组（固定大小）或序列（动态大小，可选带有上限）字段在 Python 中存储为 ``list``。
从 Dashing 开始，数值类型数组/序列的 Python 类型已更改：

* 数值数组存储为 ``numpy.ndarray``\ （``dtype`` 的选择与数值类型匹配）
* 数值序列存储为 ``array.array``\ （``typename`` 的选择与数值类型匹配）

与之前一样，非数值类型的数组/序列在 Python 中仍然表示为 ``list``。

此更改带来了许多好处：

* 新的数据结构确保数组/序列中的每一项都符合数值类型的取值范围限制。
* 数值可以在内存中更高效地存储，避免为每一项产生 Python 对象的开销。
* 两种数据结构的内存布局允许在单次操作中读写数组/序列的所有项，这使得与 Python 之间的转换显著更快/更高效。

launch
^^^^^^

``launch_testing`` 包赶上了 Bouncy Bolson 中所做的 ``launch`` 包重新设计。
已经移动到 ``launch.legacy`` 子模块中的旧 Python API 因此被弃用并移除。

有关如何使用其新 API，请参阅 ``launch`` 的 `示例 <https://github.com/ros2/launch/tree/dashing/launch/examples>`__ 和 `文档 <https://github.com/ros2/launch/tree/dashing/launch/doc>`__。

有关如何使用新的 ``launch_testing`` API，请参阅 `demos tests <https://github.com/ros2/demos>`__。

rmw
^^^

自 `Crystal Clemmys <Release-Crystal-Clemmys>` 版本以来的变更：

* ``rmw`` 中的新 API，``rmw_context_t`` 的 fini 函数：

 * `rmw_context_fini <https://github.com/ros2/rmw/blob/c518842f6f82910482470b40c221c268d30691bd/rmw/include/rmw/init.h#L111-L136>`_

* 对 ``rmw`` 的修改，现在将 ``rmw_context_t`` 传递给 ``rmw_create_wait_set``：

 * `rmw_create_wait_set <https://github.com/ros2/rmw/blob/c518842f6f82910482470b40c221c268d30691bd/rmw/include/rmw/rmw.h#L522-L543>`_

* ``rmw`` 中的新 API，用于为已发布和已订阅的消息预分配空间：

 * `rmw_init_publisher_allocation <https://github.com/ros2/rmw/blob/dc7b2f49f1f961d6cf2c173adc54736451be8938/rmw/include/rmw/rmw.h#L262>`_
 * `rmw_fini_publisher_allocation <https://github.com/ros2/rmw/blob/dc7b2f49f1f961d6cf2c173adc54736451be8938/rmw/include/rmw/rmw.h#L279>`_
 * `rmw_init_subscription_allocation <https://github.com/ros2/rmw/blob/dc7b2f49f1f961d6cf2c173adc54736451be8938/rmw/include/rmw/rmw.h#L489>`_
 * `rmw_fini_subscription_allocation <https://github.com/ros2/rmw/blob/dc7b2f49f1f961d6cf2c173adc54736451be8938/rmw/include/rmw/rmw.h#L506>`_
 * `rmw_serialized_message_size <https://github.com/ros2/rmw/blob/dc7b2f49f1f961d6cf2c173adc54736451be8938/rmw/include/rmw/rmw.h#L395>`_

* 对 ``rmw`` 的修改，现在分别将 ``rmw_publisher_allocation_t`` 或 ``rmw_subscription_allocation_t`` 传递给 ``rmw_publish`` 和 ``rmw_take``。
  请注意，此参数可以是 ``NULL`` 或 ``nullptr``，从而保持现有的 Crystal 行为。

 * `rmw_publish <https://github.com/ros2/rmw/blob/dc7b2f49f1f961d6cf2c173adc54736451be8938/rmw/include/rmw/rmw.h#L310>`_
 * `rmw_take <https://github.com/ros2/rmw/blob/dc7b2f49f1f961d6cf2c173adc54736451be8938/rmw/include/rmw/rmw.h#L556>`_

* ``rmw_get_*_names_and_types*`` 函数返回的类型名应具有完全限定的命名空间。
  例如，返回的类型名应为 ``rcl_interface/msg/Parameter`` 和 ``rcl_interfaces/srv/GetParameters``，而不是 ``rcl_interfaces/Parameter`` 和 ``rcl_interfaces/GetParameters``。

actions
^^^^^^^

* ``rclcpp_action::Client`` 签名的更改：

  `rclcpp_action::Client::async_send_goal <https://github.com/ros2/rclcpp/blob/ef41059a751702274667e2164182c062b47c453d/rclcpp_action/include/rclcpp_action/client.hpp#L343>`_ 的签名已更改。
  现在用户可以使用新的
  `SendGoalOptions <https://github.com/ros2/rclcpp/blob/ef41059a751702274667e2164182c062b47c453d/rclcpp_action/include/rclcpp_action/client.hpp#L276>`_ 结构体，为**目标响应**和**结果**可选地提供回调函数。
  当动作服务器接受或拒绝目标时，会调用目标响应回调；当收到目标的结果时，会调用结果回调。
  还为 `rclcpp_action::Client::async_cancel_goal <https://github.com/ros2/rclcpp/blob/ef41059a751702274667e2164182c062b47c453d/rclcpp_action/include/rclcpp_action/client.hpp#L432-L434>`_
  和 `rclcpp_action::Client::async_get_result <https://github.com/ros2/rclcpp/blob/ef41059a751702274667e2164182c062b47c453d/rclcpp_action/include/rclcpp_action/client.hpp#L399-L401>`_ 添加了可选回调。

* 目标状态转换名称的更改：

  目标状态转换的名称已重构，以反映设计文档。
  这会影响 ``rcl_action``、``rclcpp_action`` 和 ``rclpy``。
  以下是事件名称更改列表（*旧名称 -> 新名称*）：

  * GOAL_EVENT_CANCEL -> GOAL_EVENT_CANCEL_GOAL
  * GOAL_EVENT_SET_SUCCEEDED -> GOAL_EVENT_SUCCEED
  * GOAL_EVENT_SET_ABORTED -> GOAL_EVENT_ABORT
  * GOAL_EVENT_SET_CANCELED -> GOAL_EVENT_CANCELED

* ``CancelGoal.srv`` 的更改：

  ``CancelGoal`` 服务的响应消息中添加了一个 ``return_code`` 字段。
  这是为了更好地传达服务调用失败的原因。
  有关详细信息，请参阅 `pull request <https://github.com/ros2/rcl_interfaces/pull/76>`_ 及相关 issue。

rviz
^^^^

* 插件应使用完全限定的类型名，否则会记录警告。
  例如，请 `参见 <https://github.com/ros2/rviz/blob/dfceae319d49546f1e4ad39689853c18fef0001e/rviz_default_plugins/plugins_description.xml#L13>`_，使用类型 ``sensor_msgs/msg/Image`` 而不是 ``sensor_msgs/Image``。
  有关更多详细信息，请参阅 `引入此更改的 PR <https://github.com/ros2/rviz/pull/387>`_。

已知问题
--------

* `[ros2/rclcpp#715] <https://github.com/ros2/rclcpp/issues/715>`_ 在独立 ROS 2 节点和组合 ROS 2 节点之间，参数 YAML 文件的加载方式存在不一致。
  目前可用的变通方法记录在一个 `issue 评论 <https://github.com/ros2/rclcpp/issues/715#issuecomment-497392626>`_ 中
* `[ros2/rclpy#360] <https://github.com/ros2/rclpy/issues/360>`_ 在 Windows 上使用 OpenSplice 时，rclpy 节点会忽略 :kbd:`ctrl-c`。
* `[ros2/rosidl_typesupport_opensplice#30] <https://github.com/ros2/rosidl_typesupport_opensplice/issues/30>`_ 使用 OpenSplice 时，存在一个 bug，会阻止在具有相同名称的服务或动作定义中嵌套消息。
* `[ros2/rclcpp#781] <https://github.com/ros2/rclcpp/pull/781>`_ 在 Dashing 上，从 ``on_set_parameter_callback`` 内部调用 ``get_parameter``/``list_parameter`` 会导致死锁。此问题已在 Eloquent 中修复，但由于是 ABI 破坏性更改，因此未向后移植到 Dashing。
* `[ros2/rclcpp#912] <https://github.com/ros2/rclcpp/issues/912>`_ 当进程内通信发生在一个 ``std::unique_ptr`` 发布器和一个 ``std::unique_ptr`` 订阅器之间时，进程间通信会强制进行消息复制（发布的 ``std::unique_ptr`` 会在内部被提升为 ``std::shared_ptr``）。
* `[ros2/rosbag2#125] <https://github.com/ros2/rosbag2/issues/125>`_ 具有 unreliable QOS 的话题不会被记录。
* `[ros2/rclcpp#715] <https://github.com/ros2/rclcpp/issues/715>`_ 组合节点无法通过重映射接收参数。向组合节点提供参数可以使用 `[此评论] <https://github.com/ros2/rclcpp/issues/715#issuecomment-497392626>`_ 中描述的方法来完成。
* `[ros2/rclcpp#893] <https://github.com/ros2/rclcpp/issues/893>`_ 由于与 ``rclcpp::GraphListener`` 存在引用循环，``rclcpp::Context`` 不会被销毁。这会导致内存泄漏。由于存在破坏 ABI 的风险，修复尚未向后移植。

发布前的时间线
--------------

发布前的几个里程碑：

    Mon. Apr 8th (alpha)
        核心软件包的首个版本可用。
        从现在开始可以进行测试（某些功能可能尚未落地）。

    Thu. May 2nd
        核心软件包的 API 冻结

    Mon. May 6th (beta)
        核心软件包的更新版本可用。
        对最新功能进行额外测试。

    Thu. May 16th
        功能冻结。
        在此之后只应发布 bug 修复版本。
        新软件包可以独立发布。

    Mon. May 20th (release candidate)
        核心软件包的更新版本可用。

    Wed. May 29th
        冻结 rosdistro。
        rosdistro 仓库中将不再合并针对 Dashing 的 PR（在发布公告后重新开放）。
