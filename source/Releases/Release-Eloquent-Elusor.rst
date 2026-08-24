Eloquent Elusor (``eloquent``)
==============================

.. contents:: 目录
   :depth: 2
   :local:

*Eloquent Elusor* 是 ROS 2 的第五个版本。

支持的平台
----------

Eloquent Elusor 根据 `平台支持等级 <../The-ROS2-Project/Platform-Support-Tiers>` 支持以下平台：

一级平台：

* Ubuntu 18.04 (Bionic)：``amd64`` 和 ``arm64``
* Mac macOS 10.14 (Mojave)
* Windows 10 (Visual Studio 2019)

二级平台：

* Ubuntu 18.04 (Bionic)：``arm32``

三级平台：

* Debian Stretch (9)：``amd64``、``arm64`` 和 ``arm32``
* OpenEmbedded Thud (2.6) / webOS OSE：``arm32`` 和 ``x86``

目标平台：

+--------------+----------------------+----------------------+----------------------+-------------------+----------------+
| 架构         | Ubuntu Bionic (18.04)| MacOS Mojave (10.14) | Windows 10 (VS2019)  | Debian Buster (10)| OpenEmbedded / |
|              |                      |                      |                      |                   | webOS OSE      |
+==============+======================+======================+======================+===================+================+
| amd64        | Tier 1 [d][a][s]     | Tier 1 [a][s]        | Tier 1 [a][s]        | Tier 3 [s]        |                |
+--------------+----------------------+----------------------+----------------------+-------------------+----------------+
| arm64        | Tier 1 [d][a][s]     |                      |                      | Tier 3 [s]        | Tier 3 [s]     |
+--------------+----------------------+----------------------+----------------------+-------------------+----------------+
| arm32        | Tier 2 [a][s]        |                      |                      | Tier 3 [s]        | Tier 3 [s]     |
+--------------+----------------------+----------------------+----------------------+-------------------+----------------+


以下指示符显示了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为此平台提供 Debian 软件包。

\" \[a\] \" 二进制版本以每个平台单个归档文件的形式提供，包含 Eloquent ROS 2 repos 文件[^7] 中的所有软件包。

\" \[s\] \" 从源代码编译。

中间件实现支持：

+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| 中间件库                 | 中间件提供方        | 支持等级      | 平台                              | 架构                              |
+==========================+=====================+===============+===================================+===================================+
| rmw_fastrtps_cpp*        | eProsima Fast-RTPS  | Tier 1        | All Platforms                     | All Architectures                 |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_connext_cpp          | RTI Connext         | Tier 1        | All Platforms except Debian and   | All Architectures except          |
|                          |                     |               | OpenEmbedded                      | arm64/arm32                       |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_cyclonedds_cpp       | Eclipse Cyclone DDS | Tier 2        | All Platforms                     | All Architectures                 |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_opensplice_cpp       | ADLINK OpenSplice   | Tier 2        | All Platforms except Debian and   | All Architectures                 |
|                          |                     |               | OpenEmbedded                      |                                   |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-RTPS  | Tier 2        | All Platforms                     | All Architectures                 |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持
等级。例如，二级平台上的一个一级中间件实现
只能获得二级支持。

最低语言要求：

- C++14
- Python 3.6

依赖要求：

+--------------+-------------------+----------------+----------------+----------------+-----------------------+
|              | 必需支持                                            | 推荐支持                               |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| 软件包       | Ubuntu Bionic     | MacOS**        | Windows 10**   | Debian Buster  | OpenEmbedded**        |
+==============+===================+================+================+================+=======================+
| CMake        | 3.10.2            | 3.14.4         | 3.14.4         | 3.13.4         | 3.16.1 / 3.12.2****   |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| EmPY         | 3.3.2                                                                                        |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Gazebo       | 9.0.0             | 9.9.0          | N/A            | 9.8.0*         | N/A                   |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Ogre         | 1.10*                                                                | N/A                   |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| OpenCV       | 3.2.0             | 4.1.0          | 3.4.6*         | 3.2.0          | 4.1.0 / 3.2.0****     |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| OpenSSL      | 1.1.0g            | 1.0.2r         | 1.0.2r         | 1.1.1c         | 1.1.1d / 1.1.1b****   |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Poco         | 1.8.0             | 1.9.0          | 1.8.0*         | 1.9.0          | 1.9.4                 |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Python       | 3.6.5             | 3.7.3          | 3.7.3          | 3.7.3          | 3.8.2 / 3.7.5****     |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Qt           | 5.9.5             | 5.12.3         | 5.10.0         | 5.11.3         | 5.14.1 / 5.12.5****   |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
|                                  | **仅 Linux**                                                             |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| PCL          | 1.8.1             | N/A            | N/A            | 1.9.1          | 1.8.1                 |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| **RMW DDS 中间件提供方**                                                                                    |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Connext DDS  | 5.3.1***                                            | N/A                                    |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Cyclone DDS  | 0.7.x (Coquette)                                                                             |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Fast-RTPS    | 1.9.0                                                                                        |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| OpenSplice   | 6.9.190705OSS                                                        | N/A                   |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+


\" \* \" 表示这不是上游版本（即操作系统官方仓库中可用的版本），而是由 OSRF 或社区分发的软件包（在自定义仓库中构建并分发的软件包）。

\" \*\* \" 滚动发行版将在其生命周期内看到这些依赖的多次版本变更。OpenEmbedded 显示的版本是 3.1 Dunfell 发行版系列提供的版本；其他受支持的发行版系列提供的版本列在这里：
<https://github.com/ros/meta-ros/wiki/Package-Version-Differences>。
请注意，ROS 发行版支持哪些 OpenEmbedded 发行版系列在其支持时间框架内会发生变化，具体依据这里显示的 OpenEmbedded 支持策略：
<https://github.com/ros/meta-ros/wiki/Policies#openembedded-release-series-support>
。但是，它始终至少由一个稳定的 OpenEmbedded 发行版系列支持。

\" \*\*\* \" 预计在迁移补丁[^8] 就绪后，该版本将提升到 Connext DDS 6.0.0。

\" \*\*\*\* \" webOS OSE 提供了这个不同的版本。

本文档仅记录 ROS 发行版首次发布时的版本，不会随依赖的演进更新。
因此这些版本是一个低水位标记。

依赖使用的软件包管理器：

- Ubuntu, Debian: apt
- MacOS: Homebrew, pip
- Windows: Chocolatey, pip
- OpenEmbedded: opkg

构建系统支持：

- ament_cmake
- cmake
- setuptools

安装
----

`安装 Eloquent Elusor <../../eloquent/Installation.html>`__

此 ROS 2 版本中的新功能
-----------------------

我们想重点介绍的一些功能和改进：

* `支持基于标记的启动文件 (XML/YAML) <https://github.com/ros2/launch/pull/226>`__
* `改进的基于启动的测试 <https://github.com/ros2/ros2/issues/739#issuecomment-555743540>`__
* `在 CLI 上传递键值参数 <https://github.com/ros2/design/pull/245>`__
* `支持流日志宏 <https://github.com/ros2/rclcpp/pull/926>`__
* `按节点日志记录 <https://github.com/ros2/ros2/issues/789>`__ - 节点的所有 stdout/stderr 输出都记录在 ~/.ros 中
* `ros2doctor <https://index.ros.org/doc/ros2/Tutorials/Getting-Started-With-Ros2doctor/>`__
* `改进 source setup 文件的性能 <https://github.com/ros2/ros2/issues/764>`__
* rviz：`交互式标记 <https://github.com/ros2/rviz/pull/457>`__、`扭矩环 <https://github.com/ros2/rviz/pull/396>`__、`tf 消息过滤器 <https://github.com/ros2/rviz/pull/375>`__
* rqt：`参数插件 <https://github.com/ros-visualization/rqt_reconfigure/pull/31>`__、`tf 树插件 <https://github.com/ros-visualization/rqt_tf_tree/pull/13>`__、`机器人转向插件 <https://github.com/ros-visualization/rqt_robot_steering/pull/7>`__ （也已向后移植到 Dashing）
* `turtlesim <https://github.com/ros/ros_tutorials/pull/53>`__ （也已向后移植到 Dashing）
* RMW 实现：

  * `用于零拷贝的消息租借 API <https://github.com/ros2/design/pull/256>`__，由 `rmw_iceoryx <https://github.com/ros2/rmw_iceoryx>`__ 使用
  * `Fast RTPS 1.9.3 <https://github.com/ros2/ros2/issues/734#issuecomment-518018479>`__
  * 新的二级实现：`rmw_cyclonedds <https://github.com/ros2/rmw_cyclonedds>`__ （也已向后移植到 Dashing）

* 用于将通信限制在 localhost 的环境变量 `ROS_LOCALHOST_ONLY <https://github.com/ros2/ros2/issues/798>`__
* MacOS Mojave 支持
* 针对 rcl 和 rclcpp 的 `跟踪插桩 <https://github.com/ros2/ros2/pull/748>`__


在开发期间，GitHub 上的 `Eloquent 元工单 <https://github.com/ros2/ros2/issues/734>`__ 包含了正在进行的顶层任务的最新状态，以及引用具有更多细节的具体工单。

自 Dashing 版本以来的变更
-------------------------

geometry_msgs
^^^^^^^^^^^^^

``geometry_msgs/msg/Quaternion.msg`` 接口现在默认初始化为一个有效的四元数，其值如下：

.. math::

    x = 0 \\
    y = 0 \\
    z = 0 \\
    w = 1

以下是获取更多细节的拉取请求：`https://github.com/ros2/common_interfaces/pull/74 <https://github.com/ros2/common_interfaces/pull/74>`_

静态变换广播器和监听器现在在 ``/tf_static`` 话题上使用 QoS 持久性 ``transient_local``。
与 ROS 1 中的 latched 设置类似，静态变换只需要发布一次。
新的监听器将接收来自所有存活且之前已发布过的静态广播器的变换。
所有发布者都必须更新以使用此持久性设置，否则变换监听器将不会收到它们的消息。
有关更多细节，请参见此拉取请求：`https://github.com/ros2/geometry2/pull/160 <https://github.com/ros2/geometry2/pull/160>`_

rclcpp
^^^^^^

``get_actual_qos()`` 的 API 破坏
""""""""""""""""""""""""""""""""

``get_actual_qos()`` 方法在 Dashing 中引入，它在 ``PublisherBase`` 和 ``SubscriptionBase`` 上之前返回一个 rmw 类型 ``rmw_qos_profile_t``，但这使得它在创建其他实体时难以复用。
因此它被更新为改为返回 ``rclcpp::QoS``。

如果仍然需要 rmw 配置文件，现有代码将需要使用 ``rclcpp::QoS::get_rmw_qos_profile()`` 方法。
例如：

.. code-block:: cpp

    void my_func(const rmw_qos_profile_t & rmw_qos);

    /* Previously: */
    // my_func(some_pub->get_actual_qos());
    /* Now: */
    my_func(some_pub->get_actual_qos()->get_rmw_qos_profile());

直接破坏这一点而不是做 tick-tock 的理由是，它是一个新函数，预计用户很少使用。
此外，由于只有返回类型在变化，添加一个具有不同名称的新函数将是进行弃用周期的唯一方式，而 ``get_actual_qos()`` 是最合适的名称，所以我们将被迫为该方法选择一个不太明显的名称。

Publisher 和 Subscription 类的 API 破坏
"""""""""""""""""""""""""""""""""""""""

为了简化 Publisher 和 Subscription 的构造，构造函数的 API 被更改了。

支持弃用周期是不可能的，因为旧签名接受一个 rcl 类型，而新签名接受 ``NodeBaseInterface`` 类型，以便它能够获得现在所需的额外信息，而且没有办法仅从 rcl 类型获得所需的额外信息。
如果这能帮助贡献者，新签名可能会被向后移植，但由于发布者和订阅者几乎总是使用工厂函数或其他更高级的 API 创建，我们不认为这对大多数用户来说是个问题。

有关更多细节，请参阅原始 pr，如果这导致了问题，请在那里评论：

`https://github.com/ros2/rclcpp/pull/867 <https://github.com/ros2/rclcpp/pull/867>`_

关于 ``add_on_set_parameters_callback`` 未使用结果的编译器警告
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

*自 Eloquent 补丁版本 2 (2020-12-04) 起*

用户应保留 ``rclcpp::Node::add_on_set_parameters_callback`` 返回的句柄，否则他们的回调可能会被注销。
已添加一条警告，以帮助识别未使用返回句柄的 bug。

`https://github.com/ros2/rclcpp/pull/1243 <https://github.com/ros2/rclcpp/pull/1243>`_

rmw
^^^

由于新增 Publisher 和 Subscription 选项导致的 API 破坏
""""""""""""""""""""""""""""""""""""""""""""""""""""""

``rmw_create_publisher()`` 方法新增了一个类型为 ``const rmw_publisher_options_t *`` 的参数。
这个新结构体保存新发布者的选项（除了 typesupport、话题名和 QoS 之外）。

``rmw_create_subscription()`` 方法移除了一个参数 ``bool ignore_local_publications``，并被类型为 ``const rmw_subscription_options_t *`` 的新选项所取代。
``ignore_local_publications`` 选项被移入了新的 ``rmw_subscription_options_t`` 类型。

在这两种情况下，新参数都是指针，绝不能为 null，因此 rmw 实现应检查以确保选项不为 null。
此外，选项应被复制到相应的 rmw 结构中。

有关更多细节，请参见此拉取请求以及相关的拉取请求：

`https://github.com/ros2/rmw/pull/187 <https://github.com/ros2/rmw/pull/187>`_

ros2cli
^^^^^^^

ros2msg 和 ros2srv 已弃用
"""""""""""""""""""""""""

CLI 工具 ``ros2msg`` 和 ``ros2srv`` 已弃用。
它们已被工具 ``ros2interface`` 取代，该工具还支持 action 和 IDL 接口。
你可以运行 ``ros2 interface --help`` 查看用法。

ros2node
""""""""

服务客户端已添加到 ros2node info 中。
作为该变更的一部分，Python 函数 ``ros2node.api.get_service_info``
已重命名为 ``ros2node.api.get_service_server_info``。

rviz
^^^^

重命名了 '2D Nav Goal' 工具
"""""""""""""""""""""""""""

该工具被重命名为 '2D Goal Pose'，默认话题从 ``/move_base_simple/goal`` 更改为 ``/goal_pose``。

以下是相关的拉取请求：

`https://github.com/ros2/rviz/pull/455 <https://github.com/ros2/rviz/pull/455>`_

TF2 缓冲区
^^^^^^^^^^

TF2 缓冲区现在必须给定一个定时器接口。

如果没有给定定时器接口，将抛出异常。

例如：

.. code-block:: cpp

    tf = std::make_shared<tf2_ros::Buffer>(get_clock());
    // The next two lines are new in Eloquent
    auto timer_interface = std::make_shared<tf2_ros::CreateTimerROS>(
      this->get_node_base_interface(),
      this->get_node_timers_interface());
    tf->setCreateTimerInterface(timer_interface);
    // Pass the Buffer to the TransformListener as before
    transform_listener = std::make_shared<tf2_ros::TransformListener>(*tf);

rcl
^^^

ROS 命令行参数变更
""""""""""""""""""

为了应对日益复杂的接口以及现在扩展的配置选项集，ROS CLI 语法已更改。
例如，使用 Dashing 语法的命令行如下：

.. code-block:: console

    $ ros2 run some_package some_node foo:=bar __params:=/path/to/params.yaml __log_level:=WARN --user-flag

使用 Eloquent（及之后版本）语法写成：

.. code-block:: console

    $ ros2 run some_package some_node --ros-args --remap foo:=bar --params-file /path/to/params.yaml --log-level WARN -- --user-flag

这种明确的语法提供了新功能，例如单参数赋值 ``--param name:=value``。
有关更多参考和理由，请查看 `ROS 命令行参数设计文档 <https://design.ros2.org/articles/ros_command_line_arguments.html>`__。

.. warning::

   旧语法已被弃用，并将在下一个版本中移除。

已知问题
--------

* `[ros2/rosidl#402] <https://github.com/ros2/rosidl/issues/402>`_ ``find_package(PCL)`` 会干扰 ROS 接口生成。
  解决方法：在 ``rosidl_generate_interfaces()`` *之后* 调用 ``find_package(PCL)``。
* `[ros2/rclcpp#893] <https://github.com/ros2/rclcpp/issues/893>`_ 由于与 ``rclcpp::GraphListener`` 存在引用循环，``rclcpp::Context`` 没有被销毁。这会导致内存泄漏。由于有破坏 ABI 的风险，修复尚未向后移植。

发布前的时间线
--------------

发布前的几个里程碑：

    9 月 30 日周一 (alpha)
        核心软件包的首个版本可用。
        从现在开始可以进行测试（某些功能可能尚未落地）。

    10 月 18 日周五
        核心软件包的 API 和功能冻结
        在此之后只应发布错误修复版本。
        新软件包可以独立发布。

    10 月 24 日周四 (beta)
        核心软件包的更新版本可用。
        对最新功能进行额外测试。

    11 月 13 日周三 (release candidate)
        核心软件包的更新版本可用。

    11 月 19 日周二
        冻结 rosdistro。
        rosdistro 仓库上针对 Eloquent 的 PR 将不会被合并（在发布公告后重新开放）。
