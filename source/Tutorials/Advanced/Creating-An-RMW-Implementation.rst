创建一个 ``rmw`` 实现
=====================

**目标：** 学习如何创建一个新的 ``rmw`` 实现，从底层中间件所需的功能到 ``rmw`` 实现的细节。

**教程级别：** 高级

**预计用时：** 30 分钟以上

.. contents:: 目录
   :local:

简介
----

ROS 2 的架构有两个主要的 :doc:`抽象层 <../../Concepts/Advanced/About-Internal-Interfaces>`。
从上到下：

#. 客户端库接口 ``rcl``，它支持面向用户的 :doc:`客户端库 <../../Concepts/Basic/About-Client-Libraries>`，例如 ``rclcpp`` 和 ``rclpy``
#. 中间件接口 ``rmw``，它抽象了 :doc:`底层中间件实现 <../../Concepts/Intermediate/About-Different-Middleware-Vendors>`，例如某个 DDS 实现、Zenoh 等

``rmw`` 的 `API 包含函数级文档 <https://docs.ros.org/en/{DISTRO}/p/rmw/generated/index.html#functions>`_，但没有关于接口特性以及它对底层中间件的期望的更高层文档。

本指南面向那些想为某个特定中间件实现 ``rmw`` 接口的开发者。
它首先介绍 ``rmw`` 接口及其工作方式。
然后介绍中间件实现必须支持的主要概念或特性。
最后介绍一些实现细节，包括如何创建实现骨架以及实现接口函数的一些技巧。

本指南旨在作为一个切入点，以启动新 ``rmw`` 实现的开发。
在合适的地方，它会链接到其他页面和源代码以获取更多细节。

.. note::

    `design.ros2.org <https://design.ros2.org/>`_ 上的 ROS 2 设计文章是历史文档，可能无法反映 ROS 2 的当前状态。
    然而，在某些情况下，它们提供了有用的上下文和信息，因此本指南或本指南链接的页面仍可能引用它们。

``rmw`` 接口
------------

``rmw`` 接口由 ``rmw`` 包通过 `C 头文件 <https://github.com/ros2/rmw/tree/{DISTRO}/rmw/include/rmw>`_ 声明。
这些头文件中声明的 C 函数的实现由 ``rmw`` 实现提供，它们是独立的包。
例如，``rmw_fastrtps_cpp`` 包为 eProsima Fast DDS 实现了该接口。

示例实现
^^^^^^^^

以下 ``rmw`` :doc:`实现 <../../Concepts/Advanced/About-Middleware-Implementations>` 可以作为参考。
请注意，存在不同的 `支持级别，它们由 REP 2000 定义 <https://reps.openrobotics.org/rep-2000/#support-tiers>`_。

#. DDS：

    #. ``rmw_fastrtps_cpp``、``rmw_fastrtps_dynamic_cpp``：`ros2/rmw_fastrtps <https://github.com/ros2/rmw_fastrtps>`_
    #. ``rmw_cyclonedds_cpp``：`ros2/rmw_cyclonedds <https://github.com/ros2/rmw_cyclonedds>`_
    #. ``rmw_connextdds``：`ros2/rmw_connextdds <https://github.com/ros2/rmw_connextdds>`_
    #. ``rmw_gurumdds_cpp``：`ros2/rmw_gurumdds <https://github.com/ros2/rmw_gurumdds>`_

    * 参见 :ref:`这个概览 <about-middleware-impls_struct_dds>`

#. ``rmw_zenoh_cpp``：`ros2/rmw_zenoh <https://github.com/ros2/rmw_zenoh>`_

    * 参见 `设计文档 <https://github.com/ros2/rmw_zenoh/blob/{DISTRO}/docs/design.md>`_

#. ``rmw_email_cpp``，一个基于电子邮件的实现：`christophebedard/rmw_email <https://github.com/christophebedard/rmw_email>`_

    * 参见 `底层电子邮件中间件的设计文档 <https://christophebedard.com/rmw_email/design/email/>`_ 和 `提供背景的博客文章 <https://christophebedard.com/ros-2-over-email/>`_

.. _rmw-impl-guide_selection-mechanism:

构建时和运行时的 ``rmw`` 实现选择机制
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

对实际 ``rmw`` 实现的依赖是通过 ``rmw_implementation` 包 <https://index.ros.org/p/rmw_implementation/#{DISTRO}>`_ 完成的。
``rmw`` 的用户（例如 ``rcl``）依赖 ``rmw`` 包来获取接口（头文件）和一些实用函数。
它们还依赖 ``rmw_implementation`` 包来获取实际实现。

默认情况下，ROS 2 允许你在运行时选择要使用的 ``rmw`` 实现。
这便于在同一台机器上比较两种实现，并且让 ROS 2 能够分发一套与多种 ``rmw`` 实现兼容的二进制文件。
:doc:`实现是在运行时选择的 <../../How-To-Guides/Working-with-multiple-RMW-implementations>`，通过 ``RMW_IMPLEMENTATION`` 环境变量；如果该变量未设置，则加载默认的 ``rmw`` 实现。

这是由 ``rmw_implementation`` 包完成的，它充当实际 ``rmw`` 实现的代理。
它的工作原理是创建占位的 ``rmw`` 函数。
当它们被调用时，它会 ``dlopen()`` 所选 ``rmw`` 实现对应的库，然后在调用它们之前，使用 ``dlsym()`` 函数在加载的共享库中查找相应的符号。

``rmw_implementation`` 包可以在构建时进行配置，以更改默认选项或禁用运行时选择。
默认实现可以在构建时通过 ``RMW_IMPLEMENTATION`` CMake 变量（例如 ``-DRMW_IMPLEMENTATION=rmw_other``）或 ``RMW_IMPLEMENTATION`` 环境变量来选择。
如果构建时只有一个实现可用，或者运行时选择被禁用（``-DRMW_IMPLEMENTATION_DISABLE_RUNTIME_SELECTION=ON``），``rmw_implementation`` 目标将只是一个针对单个实现的简单 ``INTERFACE`` 库。

由于上述代理机制和 CMake 逻辑，一个没有实现接口中所有函数的 ``rmw`` 实现只会在运行时（具体是在符号查找失败时）出错，而不是在构建时（具体是在链接时，如果运行时选择被禁用的话）出错。

特性
----

本节介绍 ``rmw`` 接口的主要特性，底层中间件必须支持或处理这些特性。
根据中间件的不同——以及它与接口所期望的特性的相似程度——``rmw`` 实现可能比较琐碎，也可能需要做更多“胶水”工作。
对于一些非关键特性或配置选项，实现可以通过 ``rmw_feature_supported()`` 或返回 ``RMW_RET_UNSUPPORTED`` 来表明不支持它们。
无论如何，``rmw`` 实现的任何特殊行为最好都应有文档说明。

主题、发布/订阅、服务
^^^^^^^^^^^^^^^^^^^^^

:doc:`主题 <../../Concepts/Basic/About-Topics>` 是发布/订阅中间件中的常见概念。
然而，ROS 2 有自己的主题名称规范，它使用 ``rmw_validate_full_topic_name()`` 进行验证。
``rmw`` 实现只需使用给定的（已解析的）主题名称。
这可能涉及改编或改写 ROS 主题名称，以适配底层中间件的主题名称规范或约束，或者编码有用的信息。
例如，对于基于 DDS 的实现，名为 ``/chatter`` 的发布/订阅主题通常会被改写为 ``rt/chatter``，使 DDS 上的 ROS 主题容易与普通 DDS 主题区分开。
参见 `该设计文档中的“ROS 2 主题和服务名称到 DDS 概念的映射”一节 <https://design.ros2.org/articles/topic_and_service_names.html#mapping-of-ros-2-topic-and-service-names-to-dds-concepts>`_。
对于 Zenoh，域 ID、解析后的主题名称、主题类型名称和主题类型哈希被 `编码到底层 Zenoh key 中 <https://github.com/ros2/rmw_zenoh/blob/{DISTRO}/docs/design.md#topic-and-service-name-mapping-to-zenoh-key-expressions>`_，以避免不同 ROS 主题名称和类型之间的通信。

至于 :doc:`服务 <../../Concepts/Basic/About-Services>`，它们并不总是由底层中间件原生支持。
对于基于 DDS 的实现，它们只是构建在发布/订阅之上：1 个请求主题和 1 个响应主题。
[#fn_dds_rpc]_
另一方面，Zenoh 通过 `queryables <https://github.com/ros2/rmw_zenoh/blob/{DISTRO}/docs/design.md#service-servers>`_ 原生支持服务，因此 ``rmw_zenoh_cpp`` 使用它们来实现服务。

请注意，虽然服务是 ``rmw`` 接口的一部分，但 :doc:`action <../../Concepts/Basic/About-Actions>` 不是。
它们是一个 ``rcl`` 概念，在 ``rcl_action`` 包中基于服务和发布/订阅实现。

节点
^^^^

:doc:`节点 <../../Concepts/Basic/About-Nodes>` 主要是 ROS 的概念。
DDS 和 Zenoh 都没有相应的概念，因此它们在 ``rmw`` 实现中主要是一个逻辑概念。
在创建发布/订阅对象时，如果需要，主题名称会由 ``rcl`` 在传给 ``rmw`` 之前用节点的命名空间/名称解析。
实现只需确保在 :ref:`内省数据 <rmw-impl-guide_introspection>` 中包含节点。

.. _rmw-impl-guide_waitsets:

等待集和等待
^^^^^^^^^^^^

:doc:`执行器 <../../Concepts/Intermediate/About-Executors>` 负责在收到新消息时触发用户提供的回调。
执行器是在客户端库层（``rclcpp``、``rclpy``）实现的，但它们依赖底层中间件使用轮询机制等待新消息。
这是通过等待集完成的，它允许以标准方式同时等待不同的实体，例如订阅、服务客户端和服务服务器。
`rmw_wait() 函数 <https://docs.ros.org/en/{DISTRO}/p/rmw/generated/function_rmw_8h_1a5f480dd59075e80288fb596b2951be2b.html>`_ 被调用时传入要等待的实体列表，以及一个实现特定的等待集对象。
它把所有实体添加到等待集中，并要求它一直等待，直到至少有一个实体有新数据可用或超时。
然后执行器检查实体列表，看哪些实体有新数据可用，并触发相应的回调。

这里的关键机制是检查某个实体是否就绪的能力，例如检查订阅是否有新消息。
然后等待只需连续地逐个检查实体，直到有一个就绪或等待超时。

看看 ``rmw_email_cpp`` 是如何 `实现等待集和等待 <https://github.com/christophebedard/rmw_email/blob/72742241d55f306d1dddcaf5dd6a5d6c2d402433/rmw_email_cpp/src/rmw_wait.cpp#L133>`_ 的，并深入到中间件 ``email``，因为它相当简单。

取数据
^^^^^^

一旦 :ref:`执行器完成等待 <rmw-impl-guide_waitsets>` 并且有新的消息、请求或响应，它就会从中间件取出数据并触发相应的回调。
例如，``rmw_take()`` 被调用时传入一个订阅和一个指向相应消息类型实例的类型擦除指针，以写入数据。

``rmw_email_cpp`` 从底层电子邮件中间件的订阅对象中取出新消息（YAML 字符串），并通过写入提供的消息将其转换为 ROS 消息。

元数据：GID、时间戳、序列号
^^^^^^^^^^^^^^^^^^^^^^^^^^^

除了实际用户指定的数据外，消息发布、服务请求、服务响应等还带有与之关联的元数据：

* GID：全局唯一 ID，用于标识一个实体（例如发布者、订阅者、客户端、服务器）

    * 实体的 GID 在一个 ROS 域内应当是唯一的，并且在本地和远程报告时应当相同。
      例如，正在发布的消息的发布者 GID 应当与订阅收到该消息时在另一端报告的发布者 GID 相同。
      [#fn_gid_remote_matching]_

* 源时间戳和接收时间戳：分别为发布和订阅的接收时间戳

* 发布序列号和接收序列号

这意味着服务请求元数据包含发出请求的客户端的 GID 和请求序列号。
服务响应元数据也包含它所响应的请求的客户端 GID 和序列号。

这些元数据以结构体的形式提供：对于订阅消息通过 ``rmw_take_with_info()``，对于服务请求/响应通过 ``rmw_take_{request,response}()``，它们由客户端库包装并提供给用户回调。

这些元数据的一部分可能由底层中间件原生支持并提供，而另一部分可能必须由 ``rmw`` 实现包含并随应用数据一起传输。
例如，DDS 通过 DDS 样本信息原生支持发布/订阅的所有这些元数据，但客户端请求元数据需要由 ``rmw`` 实现包装在服务响应数据旁边。
``email`` 原生支持所有这些元数据，它们包含在标准电子邮件头中（即不在电子邮件正文中）。

.. _rmw-impl-guide_typesupport:

类型支持
^^^^^^^^

为了弥合 ROS 2 :doc:`接口 <../../Concepts/Basic/About-Interfaces>`\ （特别是 :doc:`自定义接口 <../Beginner-Client-Libraries/Custom-ROS2-Interfaces>`\ ）与底层中间件之间的差距，需要一些胶水代码。
这被称为 :ref:`类型支持 <Type Specific Interfaces>`。
当发布一个 {interface(std_msgs/msg/String)} 类型的消息时，``rmw_publish()`` 只获得一个指向消息的 ``void *``，它可能指向 C++ 实例、C 实例等等。
该指针将根据创建发布者时提供的类型支持信息进行解释。

首先，会为每个接口类型与面向用户语言的组合生成代码，这与底层中间件无关。
例如，对于 {interface(std_msgs/msg/String)} 消息类型，会生成以下数据结构：

#. C++：``std_msgs/msg/string.hpp`` 头文件，包含由 ``rosidl_generator_cpp`` 包生成的 ``std_msgs::msg::String`` 类
#. C：``std_msgs/msg/string.h`` 头文件，包含由 ``rosidl_generator_c`` 包生成的 ``std_msgs__msg__String`` 结构体
#. Python：``std_msgs`` 模块，包含由 ``rosidl_generator_py`` 包生成的 ``std_msgs.msg.String`` 类（它只是 C 结构体的一个包装）
#. （依此类推，例如对于 Rust）

其次，为了让底层中间件能够发送和接收消息，它需要知道如何解释面向用户的数据结构。
这是 ``rmw`` 实现中最关键的部分之一。
有两种选择：:ref:`静态类型支持 <internal-interfaces_static-type-support>` 和 :ref:`动态类型支持 <internal-interfaces_dynamic-type-support>`。
静态类型支持涉及为每个接口生成中间件特定的代码。
例如，``rosidl_typesupport_fastrtps_cpp`` 生成代码，使用 `Fast CDR <https://github.com/eProsima/Fast-CDR>`_ 将每个接口类型的 C++ 类序列化/反序列化为 CDR，供 ``rmw_fastrtps_cpp`` 传给 Fast DDS。
[#fn_ts_fastrtps]_
``rmw_connextdds`` 甚至 ``rmw_zenoh_cpp`` 都使用 CDR 进行序列化，因此它们也使用这个类型支持包。
另一方面，动态类型支持涉及生成一小段与中间件无关的代码，提供关于每个接口类型的通用信息。
[#fn_ts_dynamic]_

这些信息可以在运行时由任何 ``rmw`` 实现用来解释指向数据的类型擦除指针：字段的名称和类型、根据字段类型读写字段的函数、获取数组字段大小的函数等。
对于 C++，这是 ``rosidl_typesupport_introspection_cpp``，例如它被 ``rmw_fastrtps_dynamic_cpp`` 使用（因此称为“动态”部分）。

动态类型支持在运行时通常比静态类型支持慢，因为它必须遍历每个消息字段，弄清楚它的类型，然后处理它，例如序列化它。
静态类型支持则由于它为每个接口类型生成了代码，因此确切知道如何处理消息。
这就是大多数 ``rmw`` 实现使用静态类型支持的原因。
然而，动态类型支持不需要生成中间件特定的代码。
在静态和动态类型支持之间做出选择，是与 ``rmw`` 实现本身正交的一个决定。

``rmw_email_cpp`` 使用动态类型支持在消息和 YAML 字符串之间进行转换，以便通过电子邮件发送。
它获取类型支持内省信息，并将它与消息一起传给一个外部/实验性包 `dynmsg <https://github.com/osrf/dynamic_message_introspection/>`_，由它负责在消息与 YAML 之间转换。
然后 YAML 对象通过底层中间件以 YAML 格式字符串的形式通过电子邮件发送。
当中间件收到新消息时，YAML 字符串会被转换为消息。

域 ID
^^^^^

:doc:`域 ID <../../Concepts/Intermediate/About-Domain-ID>` 是一种在同一物理网络上划分独立逻辑网络的方式。
它是 DDS 的原生特性，但不是 Zenoh 的。
DDS 通过将域 ID 用作网络端口偏移来实现这一点，而 Zenoh 通过将域 ID 作为与每个 ROS 2 主题对应的内部 Zenoh key 的第一个组成部分来实现。

服务质量（QoS）
^^^^^^^^^^^^^^^

ROS 2 中的 :doc:`服务质量设置 <../../Concepts/Intermediate/About-Quality-of-Service-Settings>` 在很大程度上源自 DDS。
像历史、深度和持久性这样的基本 QoS 策略与 ROS 1 相同，但更高级的策略则直接来自 DDS。
实现可以简单地忽略某些设置。
例如，``rmw_zenoh_cpp`` 没有实现 deadline 和 lifespan QoS 策略。

QoS 的一个重要方面是，两个配置文件（例如发布者的配置文件和订阅者的配置文件）可能不兼容，这意味着它们无法通信。
由实现来决定两个 QoS 配置文件是否兼容：``rmw_qos_profile_check_compatible()``。
基于 DDS 的实现依赖 ``rmw_dds_common::qos_profile_check_compatible()``，因为 :ref:`QoS 配置文件兼容性 <about-qos_compatibilities>` 在 DDS 中是标准的。
在 Zenoh 中，`QoS 设置本质上永远不会不兼容 <https://github.com/ros2/rmw_zenoh/blob/{DISTRO}/docs/design.md#quality-of-service>`_。

为了支持通用的“默认”行为，QoS 策略包含一个 ``*_SYSTEM_DEFAULT`` 设置（例如 ``rmw_qos_reliability_policy_t`` 的 ``RMW_QOS_POLICY_RELIABILITY_SYSTEM_DEFAULT``），它将取值留给中间件实现。
然后 ``rmw_*_get_actual_qos()`` 函数获取实现实际使用的 QoS 配置文件。

.. _rmw-impl-guide_introspection:

ROS 图内省
^^^^^^^^^^

节点能够获取其他节点、主题等的列表。
例如，这也允许发布者知道其主题是否存在任何订阅。
同样的机制被用于通过 ROS 2 CLI 来 :doc:`列出节点 <../Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes>`、:doc:`主题 <../Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics>` 等：``ros2 node list``、``ros2 topic list`` 等。

这是由许多 ``rmw`` 函数支持的：``rmw_get_node_names()``、``rmw_get_topic_names_and_types()``、``rmw_publisher_count_matched_subscriptions()`` 以及更多。
虽然接口没有指定实现方式，但 ``rmw`` 实现通常维护一个 ROS 图的缓存。
当它们创建新实体（例如节点、发布者、订阅、服务、客户端）时，它们会在内部图缓存中记录它，并通过中间件特定的机制通知其他参与者，以便它们可以将其添加到自己的缓存中。
图缓存属于 ``rmw`` 上下文，因此它在调用 ``rmw_init()`` 时被初始化。
这个上下文间接属于 ``rclcpp`` 上下文（例如由 ``rclcpp::init()`` 初始化），因此通常每个进程只有一个图缓存。

由于基于 DDS 的 ``rmw`` 实现在这方面非常相似，它们在 ``rmw_dds_common` 包 <https://github.com/ros2/rmw_dds_common>`__ 中共享一个公共的图缓存实现。
它使用一个内部主题（通常是 ``ros_discovery_info``）来共享关于新实体的信息。
``rmw_zenoh_cpp`` `创建一个 Zenoh 活跃性令牌 <https://github.com/ros2/rmw_zenoh/blob/{DISTRO}/docs/design.md#graph-cache>`_，其中包含实体类型和信息，并与其他参与者共享它。

事件
^^^^

用户可以为发布者和订阅提供回调，由中间件在特定事件（``rmw_event_type_t``）上触发（但由客户端库执行），例如 :ref:`与服务质量相关的事件 <about-qos_qos-events>` 和 :ref:`发布-订阅匹配事件 <about-qos_matched-events>`。
其中一些事件可以在图缓存发生相关变化时触发。

安全
^^^^

:doc:`安全 <../../Concepts/Intermediate/About-Security>` 在 ``rmw`` 接口中没有被很好地指定；其中大部分由 :doc:`SROS2 <../Advanced/Security/Introducing-ros2-security>` 指定。
该接口仅作为上下文初始化选项 ``rmw_init_options_t`` 的一部分定义了几个安全选项：

#. ``rmw_security_options_t``，它包含一个安全策略（enforce/permissive）以及一个指向包含安全工件（即 keystore）的目录的路径。
   这些由 ``rcl`` 根据环境变量 ``ROS_SECURITY_ENABLE`` 和 ``ROS_SECURITY_STRATEGY`` 以及 ``ROS_SECURITY_KEYSTORE`` 设置。
#. 从 keystore 中为给定进程使用的安全 enclave 的名称。
   例如，在使用 ``ros2 run`` 运行节点时，通过 ``--enclave`` 选项设置。

然而，在实践中，:doc:`keystore <./Security/The-Keystore>` 目录及其安全 enclave 的结构是基于 DDS Security 规范的。
因此，使用 ``sros2`` 包 :doc:`生成的安全工件 <./Security/Introducing-ros2-security>` 只能由基于 DDS 的 ``rmw`` 实现直接使用。
对于 ``rmw_zenoh_cpp``，可以使用 ``zenoh_security_tools`` 包从 ``sros2`` 生成的工件 `生成 Zenoh 特定的安全配置文件 <https://github.com/ros2/rmw_zenoh/tree/{DISTRO}/zenoh_security_tools>`_，并通过 ``ZENOH_SESSION_CONFIG_URI`` 环境变量提供，绕过 ``ROS_SECURITY_*`` 环境变量。

实现
----

实现骨架
^^^^^^^^

本节介绍为新实现包创建基本文件和目录的具体步骤，包括 ``package.xml`` 和 ``CMakeLists.txt`` 中的特殊处理。

从 :doc:`包创建教程 <../../Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package>` 开始，创建一个空包。
然后进行以下更改：

#. ``package.xml``

    #. 定义包/实现名称

        包名同时也是 ``rmw`` 实现的名称。
        它将用于通过 ``RMW_IMPLEMENTATION`` 环境变量或 CMake 选项来 :ref:`选择实现 <rmw-impl-guide_selection-mechanism>`。
        名称通常以 ``rmw_`` 开头，后面接底层中间件的名称。
        然后，ROS 2 生态系统中的大多数 :doc:`实现 <../../Concepts/Intermediate/About-Different-Middleware-Vendors>` 会附加一个后缀（例如 ``_cpp``）来表示该实现是用 C++ 编写的。
        然而，这并不是必须的。
        示例：``rmw_fastrtps_cpp``、``rmw_cyclonedds_cpp``、``rmw_connextdds``、``rmw_zenoh_cpp`` 和 ``rmw_email_cpp``。

        .. code-block:: xml

            <!-- TODO replace with the actual implementation name -->
            <name>rmw_IMPLEMENTATION_NAME_cpp</name>

    #. 声明对 ``rmw`` 的依赖

        因为该包将实现 ``rmw`` 包中声明的接口，并依赖一些实用函数。

        .. code-block:: xml

            <depend>rmw</depend>

    #. 声明对所需类型支持包的依赖

        详情参见 :ref:`类型支持一节 <rmw-impl-guide_typesupport>`。

        .. code-block:: xml

            <!-- keep or add what is necessary -->
            <depend>rosidl_typesupport_fastrtps_c</depend>
            <depend>rosidl_typesupport_fastrtps_cpp</depend>
            <depend>rosidl_typesupport_introspection_c</depend>
            <depend>rosidl_typesupport_introspection_cpp</depend>

    #. 声明加入 ``rmw_implementation_packages`` 组

        这允许 ``rmw_implementation`` 包 `依赖该实现 <https://github.com/ros2/rmw_implementation/blob/4dd5d571a5bfa1a67183acf271dfa442932c7572/rmw_implementation/package.xml#L38>`_，使其能与其他实现一起构建，因为没有其他包显式依赖任何 ``rmw`` 实现。
        这样，如果被选中，它就可以被找到并使用。

        .. code-block:: xml

            <member_of_group>rmw_implementation_packages</member_of_group>

#. ``CMakeLists.txt``

    #. 创建库目标

        该库必须是共享库。
        它应当依赖 ``rmw`` 来获取头文件和实用函数，以及所需的类型支持包。
        它还将依赖底层中间件。

        .. code-block:: cmake

            add_library(${PROJECT_NAME} SHARED
              src/file.cpp
              # ...
            )
            target_link_libraries(${PROJECT_NAME} PUBLIC
              rmw::rmw
            )
            target_link_libraries(${PROJECT_NAME} PRIVATE
              rosidl_typesupport_fastrtps_c::rosidl_typesupport_fastrtps_c
              rosidl_typesupport_fastrtps_cpp::rosidl_typesupport_fastrtps_cpp
              rosidl_typesupport_introspection_c::rosidl_typesupport_introspection_c
              rosidl_typesupport_introspection_cpp::rosidl_typesupport_introspection_cpp
              # TODO add any implementation-specific dependencies, e.g., underlying middleware
            )

    #. 配置实现库目标

        在实践中，这只是默认隐藏符号，以隐藏内部符号，即非 ``rmw`` 接口符号。
        如果实现是用 C 编写的（不常见），请指定 ``LANGUAGE "C"``。

        .. code-block:: cmake

            configure_rmw_library(${PROJECT_NAME})

    #. 注册 ``rmw`` 实现

        这会在 :ref:`ament 索引 <ament-cmake-doc_adding-resources>` 中注册该实现，以便在构建时（``get_available_rmw_implementations()``、``get_rmw_typesupport()``）或运行时（``ament_index_cpp::get_resources("rmw_typesupport")``）找到它。
        它还会注册该实现支持的语言和类型支持包列表。
        例如，如果该实现只对 C 和 C++ 消息使用类型支持内省（即动态而非静态）：

        .. code-block:: cmake

            register_rmw_implementation(
              "c:rosidl_typesupport_introspection_c"
              "cpp:rosidl_typesupport_introspection_cpp"
            )

        .. 例如，Python 客户端库 ``rclpy`` 使用 C 类型支持，并使用 ``get_rmw_typesupport()`` 检查 C 类型支持是否可用，因此 ``rmw`` 实现必须支持它。

    #. 安装并导出目标

        .. code-block:: cmake

            install(
              TARGETS ${PROJECT_NAME}
              EXPORT ${PROJECT_NAME}
              ARCHIVE DESTINATION lib
              LIBRARY DESTINATION lib
              RUNTIME DESTINATION bin
            )

            ament_export_targets(${PROJECT_NAME})
            # ament_export_libraries(${PROJECT_NAME})  # Old-style CMake

            # ...

接口函数的实现
^^^^^^^^^^^^^^

第一步是定义 ``rmw`` 头文件中声明的 C 接口函数。
从简单地返回 ``RMW_RET_OK`` 的空函数开始，然后按它们在运行时可能被调用的顺序逐个实现它们。
例如：``rmw_init()``、``rmw_create_node()``、``rmw_create_publisher()``、``rmw_create_subscription()`` 等等。
这将允许逐步构建和运行/测试实现。

大多数 ``rmw`` 函数必须按照函数文档的定义执行输入验证。
有各种实用宏可以简化这一点，例如 ``RMW_CHECK_ARGUMENT_FOR_NULL()`` 和 ``RMW_CHECK_TYPE_IDENTIFIERS_MATCH()``。

``rmw`` 结构体通常包含一个类型擦除指针（有时是不透明指针），用于存放 ``rmw`` 实现特定的数据。
例如，``rmw_publisher_t`` 有一个 ``void * data``。
实现可以把任何想要的东西放在那里，例如一个指向内部对象的指针，该对象包装了底层中间件的发布者对象以及任何相关信息（如类型支持）。
这个数据/对象可以在稍后 ``rmw_publish()`` 使用相应的 ``rmw_publisher_t`` 被调用时获取并使用。
为了确保不同的 ``rmw`` 实现不会尝试解释这个数据，``rmw_publisher_t`` 在其 ``implementation_identifier`` 字段中包含实现的名称。

类型支持
^^^^^^^^

类型支持结构体可能令人困惑。
下面是一个关于发布者/订阅的消息类型支持的示例。

发布者通过 ``rmw_create_publisher()`` 创建，该函数接受一个类型支持信息的句柄：``const rosidl_message_type_support_t *``。
这是与语言相关的基础类型支持：``rosidl_typesupport_c`` / ``rosidl_typesupport_cpp``。
据此，我们可以根据可用的类型支持获取具体的类型支持句柄，例如 ``rosidl_typesupport_fastrtps_c`` / ``rosidl_typesupport_fastrtps_cpp`` 和 ``rosidl_typesupport_introspection_c`` / ``rosidl_typesupport_introspection_cpp``。
令人困惑的部分是，这些句柄的类型也是 ``const rosidl_message_type_support_t *``！
然而，具体的类型支持句柄才是包含实际有用信息的句柄。
参见 `这个示例函数 <https://github.com/christophebedard/rmw_email/blob/f5e622bab24edaad8e0da054c7dbc698c6fb809c/rmw_email_cpp/src/type_support.cpp#L29-L62>`__，它给定一个基础类型支持句柄（``rosidl_typesupport_{c,cpp}``），提取出具体的 C 或 C++ 动态消息类型支持句柄（``rosidl_typesupport_introspection_{c,cpp}``）。
由 ``rclcpp`` 创建的发布者将使用 C++ 类型支持，而由 ``rclpy`` 创建的发布者将使用 C 类型支持，因为 Python 消息会被转换为 C 消息。
``/rosout`` 发布者由 ``rcl`` 管理，它是用 C 编写的，因此它使用 C 类型支持。

然后，使用具体类型支持句柄的类型擦除指针 ``const void * data``，我们获取类型支持特定的信息。
例如，对于 C++ 动态类型支持，这将是一个 ``const rosidl_typesupport_introspection_cpp::MessageMembers *``，它包含消息每个字段的信息。
参见 `这个示例函数 <https://github.com/christophebedard/rmw_email/blob/f5e622bab24edaad8e0da054c7dbc698c6fb809c/rmw_email_cpp/src/conversion.cpp#L116-L153>`__，它从具体类型支持句柄中提取与语言相关的类型支持信息。
这些信息用于读取类型擦除的消息指针，将消息转换为 YAML 对象，然后再转换为字符串，供底层中间件发布。

服务类型支持类似，但 ``rosidl_service_type_support_t`` 分别指向请求和响应消息类型的类型支持信息。

测试
----

``rmw`` 包包含一些测试，但它们主要针对实用函数（例如获取零初始化结构体）以及非实现特定的函数，例如主题/节点名称/命名空间验证。

至于测试新的 ``rmw`` 实现，``test_rmw_implementation`` 包 `包含接口的测试 <https://github.com/ros2/rmw_implementation/tree/{DISTRO}/test_rmw_implementation/test>`_。
首先定义测试可执行文件，然后一个 CMake 函数通过设置 ``RMW_IMPLEMENTATION`` 环境变量，为给定的 ``rmw`` 实现创建测试目标。
``rmw_implementation_cmake`` 的 ``call_for_each_rmw_implementation()`` 被调用，并向它提供这个 CMake 函数，该函数会针对每个可用实现被调用。
参见 `CMakeLists.txt 文件 <https://github.com/ros2/rmw_implementation/blob/{DISTRO}/test_rmw_implementation/CMakeLists.txt>`__。
许多其他包，包括仅用于测试的 ``test_rclcpp`` 包，也 `使用这个机制 <https://github.com/ros2/system_tests/blob/{DISTRO}/test_rclcpp/CMakeLists.txt>`__ 来针对所有可用的 ``rmw`` 实现运行测试，否则测试只会用默认实现运行。
包也可以使用 ``get_available_rmw_implementations()`` 来获取可用实现的实际列表。

一些测试有实现特定的代码，这是出于各种原因，例如不支持接口子集。
这些测试可以使用 ``rmw`` 的 ``rmw_get_implementation_identifier()`` `函数 <https://docs.ros.org/en/{DISTRO}/p/rmw/generated/function_rmw_8h_1aeb8a815b9be5eb3f38ab28363ef63920.html>`__ 来实现。

中间件和 ``rmw`` 实现特定的配置
-------------------------------

``rmw`` 接口允许通过 ``rmw_publisher_options_t`` / ``rmw_subscription_options_t`` 中的类型擦除字段 ``rmw_specific_publisher_payload`` / ``rmw_specific_subscription_payload`` 为发布者和订阅提供任意的实现特定配置负载。
例如，用户通过 ``rclcpp`` 中的 ``RMWImplementationSpecificPublisherPayload`` / ``RMWImplementationSpecificSubscriptionPayload`` 来设置它。
这是一个高级的、不可移植的特性，目前没有任何（tier 1）实现使用它。

为了获得更多灵活性，一些实现使用环境变量：``RMW_FASTRTPS_*``、``RMW_CONNEXT_*`` 等。
底层中间件也可能通过环境变量进行配置：``FASTDDS_*``、``ZENOH_*``、``CYCLONEDDS_*``、``EMAIL_*`` 等。
例如，如果使用了相应的中间件，``CYCLONEDDS_URI``、``FASTRTPS_DEFAULT_PROFILES_FILE`` 和 ``ZENOH_SESSION_CONFIG_URI`` 环境变量可以用于提供完整配置文件的路径。

脚注
----

.. [#fn_dds_rpc]
    现在确实有一个 DDS RPC 规范，但 `在 ROS 2 最初设计时，它尚未定稿，也没有被 DDS 供应商实现 <https://design.ros2.org/articles/ros_on_dds.html#services-and-actions>`_。
    由于 ``rmw`` 接口在官方上也是 DDS 无关的，服务由 ``rmw`` 实现决定，这解释了为什么 :ref:`跨 DDS 供应商的通信无法保证 <different-middleware-vendors-cross-vendor-communication>`，即使发布/订阅通常可以正常工作。

.. [#fn_gid_remote_matching]
    在实践中，情况并不总是如此，因此这个要求有所放宽。
    参见 `ros2/rmw_cyclonedds#377 <https://github.com/ros2/rmw_cyclonedds/issues/377>`_。

.. [#fn_ts_fastrtps]
    例如，为 {interface(std_msgs/msg/Header)} 生成的 C++ 消息 Fast CDR 序列化/反序列化代码位于 ``build/`` 目录下的 ``std_msgs/rosidl_typesupport_fastrtps_cpp/std_msgs/msg/detail/dds_fastrtps/header__type_support.cpp``。

.. [#fn_ts_dynamic]
    例如，为 {interface(std_msgs/msg/Header)} 生成的 C++ 消息内省代码位于 ``build/`` 目录下的 ``std_msgs/rosidl_typesupport_introspection_cpp/std_msgs/msg/detail/header__type_support.cpp``。
