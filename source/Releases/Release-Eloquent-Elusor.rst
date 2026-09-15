Eloquent Elusor（``eloquent``）
===============================

.. contents:: 目录
   :depth: 2
   :local:

*Eloquent Elusor* 是 ROS 2 的第五个发行版。

支持的平台
----------

Eloquent Elusor 根据 `平台支持层级 <../The-ROS2-Project/Platform-Support-Tiers>`，支持以下平台：

第 1 层级平台：

* Ubuntu 18.04（Bionic）：``amd64`` 和 ``arm64``
* Mac macOS 10.14（Mojave）
* Windows 10（Visual Studio 2019）

第 2 层级平台：

* Ubuntu 18.04（Bionic）：``arm32``

第 3 层级平台：

* Debian Stretch（9）：``amd64``、``arm64`` 和 ``arm32``
* OpenEmbedded Thud（2.6） / webOS OSE：``arm32`` 和 ``x86``

目标平台：

+--------------+----------------------+----------------------+----------------------+-------------------+----------------+
|     架构     | Ubuntu Bionic (18.04)| MacOS Mojave (10.14) | Windows 10 (VS2019)  | Debian Buster (10)| OpenEmbedded / |
|              |                      |                      |                      |                   | webOS OSE      |
+==============+======================+======================+======================+===================+================+
| amd64        | 第 1 层级 [d][a][s]  |   第 1 层级 [a][s]   |   第 1 层级 [a][s]   |   第 3 层级 [s]   |                |
+--------------+----------------------+----------------------+----------------------+-------------------+----------------+
| arm64        | 第 1 层级 [d][a][s]  |                      |                      |   第 3 层级 [s]   | 第 3 层级 [s]  |
+--------------+----------------------+----------------------+----------------------+-------------------+----------------+
| arm32        |   第 2 层级 [a][s]   |                      |                      |   第 3 层级 [s]   | 第 3 层级 [s]  |
+--------------+----------------------+----------------------+----------------------+-------------------+----------------+


以下指标说明了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为此平台提供
Debian 软件包。

\" \[a\] \" 以每个平台一个压缩包的形式提供二进制发行版，其中包含
Eloquent ROS 2 repos 文件[^7]中的所有软件包。

\" \[s\] \" 从源码编译。

中间件实现支持：

+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
|         中间件库         |    中间件供应商     |   支持层级    |               平台                |               架构                |
+==========================+=====================+===============+===================================+===================================+
| rmw_fastrtps_cpp*        | eProsima Fast-RTPS  |   第 1 层级   |             所有平台              |             所有架构              |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_connext_cpp          | RTI Connext         |   第 1 层级   | 除 Debian 和 OpenEmbedded         |    除 arm64/arm32 外的所有架构    |
|                          |                     |               | 外的所有平台                      |                                   |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_cyclonedds_cpp       | Eclipse Cyclone DDS |   第 2 层级   |             所有平台              |             所有架构              |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_opensplice_cpp       | ADLINK OpenSplice   |   第 2 层级   | 除 Debian 和 OpenEmbedded         |             所有架构              |
|                          |                     |               | 外的所有平台                      |                                   |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-RTPS  |   第 2 层级   |             所有平台              |             所有架构              |
+--------------------------+---------------------+---------------+-----------------------------------+-----------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持层级。例如，第 1 层级中间件实现运行在
第 2 层级平台上时，只能获得第 2 层级支持。

最低语言要求：

- C++14
- Python 3.6

依赖项要求：

+--------------+-------------------+----------------+----------------+----------------+-----------------------+
|              |                      必需支持                       |                推荐支持                |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
|    软件包    | Ubuntu Bionic     | MacOS**        | Windows 10**   | Debian Buster  | OpenEmbedded**        |
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
|                                  |                            **仅 Linux 平台**                             |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| PCL          | 1.8.1             | N/A            | N/A            | 1.9.1          | 1.8.1                 |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
|                                          **RMW DDS 中间件供应商**                                           |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Connext DDS  | 5.3.1***                                            | N/A                                    |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Cyclone DDS  | 0.7.x (Coquette)                                                                             |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| Fast-RTPS    | 1.9.0                                                                                        |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+
| OpenSplice   | 6.9.190705OSS                                                        | N/A                   |
+--------------+-------------------+----------------+----------------+----------------+-----------------------+


\" \* \" 表示这不是上游版本（即可以在官方操作系统软件仓库中获取的
版本），而是由 OSRF 或社区构建并分发的软件包（构建并分发在
自定义软件仓库中的软件包）。

\" \*\* \" 滚动发行版在其生命周期内会经历这些依赖项的多次版本变更。
此处给出的 OpenEmbedded 版本来自 3.1 Dunfell 发行系列；其他受支持的
发行系列所提供的版本列在此处：
<https://github.com/ros/meta-ros/wiki/Package-Version-Differences> 。
注意，某个 ROS 发行版所支持的 OpenEmbedded 发行系列会在其支持时间
范围内发生变化，依据的是此处所示的 OpenEmbedded 支持策略：
<https://github.com/ros/meta-ros/wiki/Policies#openembedded-release-series-support>
。不过，它始终会至少由一个稳定的 OpenEmbedded 发行系列提供支持。

\" \*\*\* \" 预计在迁移补丁[^8]就绪后，将升级到 Connext DDS 6.0.0。

\" \*\*\*\* \" webOS OSE 提供了这一不同版本。

本文档仅记录某个 ROS 发行版首次发布时的版本，不会随依赖项的
发展而更新。因此这些版本是一个下限值。

依赖项使用的软件包管理器：

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

`安装 Eloquent Elusor <../../eloquent/Installation.html>`__

本发行版新增功能
----------------

我们想重点介绍以下功能与改进：

* `支持基于标记的启动文件（XML/YAML） <https://github.com/ros2/launch/pull/226>`__
* `改进基于 launch 的测试 <https://github.com/ros2/ros2/issues/739#issuecomment-555743540>`__
* `在 CLI 上传递键值参数 <https://github.com/ros2/design/pull/245>`__
* `支持流式日志宏 <https://github.com/ros2/rclcpp/pull/926>`__
* `按节点日志记录 <https://github.com/ros2/ros2/issues/789>`__ - 节点的所有 stdout/stderr 输出都会记录到 ~/.ros 中
* `ros2doctor <https://index.ros.org/doc/ros2/Tutorials/Getting-Started-With-Ros2doctor/>`__
* `改进 setup 文件的 source 性能 <https://github.com/ros2/ros2/issues/764>`__
* rviz：`交互式标记 <https://github.com/ros2/rviz/pull/457>`__、`力矩环 <https://github.com/ros2/rviz/pull/396>`__、`tf 消息过滤器 <https://github.com/ros2/rviz/pull/375>`__
* rqt：`参数插件 <https://github.com/ros-visualization/rqt_reconfigure/pull/31>`__、`tf 树插件 <https://github.com/ros-visualization/rqt_tf_tree/pull/13>`__、`机器人转向插件 <https://github.com/ros-visualization/rqt_robot_steering/pull/7>`__ （也已向后移植到 Dashing）
* `turtlesim <https://github.com/ros/ros_tutorials/pull/53>`__ （也已向后移植到 Dashing）
* RMW 实现：

  * `用于零拷贝的消息借出 API <https://github.com/ros2/design/pull/256>`__，由 `rmw_iceoryx <https://github.com/ros2/rmw_iceoryx>`__ 使用
  * `Fast RTPS 1.9.3 <https://github.com/ros2/ros2/issues/734#issuecomment-518018479>`__
  * 新增第 2 层级实现：`rmw_cyclonedds <https://github.com/ros2/rmw_cyclonedds>`__ （也已向后移植到 Dashing）

* 环境变量 `ROS_LOCALHOST_ONLY <https://github.com/ros2/ros2/issues/798>`__，用于将通信限制在本机
* MacOS Mojave 支持
* 针对 rcl 和 rclcpp 的 `跟踪插桩 <https://github.com/ros2/ros2/pull/748>`__


在开发过程中，GitHub 上的 `Eloquent meta ticket <https://github.com/ros2/ros2/issues/734>`__ 包含了正在进行的高层任务的最新状态，以及包含更多细节的具体 issue 引用。

自 Dashing 发行版以来的变更
---------------------------

geometry_msgs
^^^^^^^^^^^^^

``geometry_msgs/msg/Quaternion.msg`` 接口现在默认初始化为一个有效的四元数，其取值如下：

.. math::

    x = 0 \\
    y = 0 \\
    z = 0 \\
    w = 1

相关 pull request 详见：`https://github.com/ros2/common_interfaces/pull/74 <https://github.com/ros2/common_interfaces/pull/74>`_

静态变换的广播者和监听者现在在 ``/tf_static`` 主题上使用 QoS 持久性 ``transient_local``。
与 ROS 1 中的 latched 设置类似，静态变换只需发布一次。
新的监听者会收到所有仍然存活且此前已发布过数据的静态广播者所发布的变换。
所有发布者都必须更新为使用这一持久性设置，否则它们的消息不会被变换监听者接收。
更多详情请参见此 pull request：`https://github.com/ros2/geometry2/pull/160 <https://github.com/ros2/geometry2/pull/160>`_

rclcpp
^^^^^^

与 ``get_actual_qos()`` 的 API 破坏性变更
"""""""""""""""""""""""""""""""""""""""""

在 Dashing 中引入的 ``PublisherBase`` 和 ``SubscriptionBase`` 上的 ``get_actual_qos()`` 方法此前返回的是 rmw 类型 ``rmw_qos_profile_t``，但这使其难以在创建其他实体时复用。
因此，它被改为返回 ``rclcpp::QoS``。

如果仍然需要 rmw profile，现有代码需要使用 ``rclcpp::QoS::get_rmw_qos_profile()`` 方法。
例如：

.. code-block:: cpp

    void my_func(const rmw_qos_profile_t & rmw_qos);

    /* Previously: */
    // my_func(some_pub->get_actual_qos());
    /* Now: */
    my_func(some_pub->get_actual_qos()->get_rmw_qos_profile());

之所以直接做这种破坏性变更而不采用 tick-tock 方式，是因为这是一个新函数，预计用户很少使用它。
此外，由于只有返回类型发生变化，若要执行弃用周期，就只能新增一个名称不同的函数，而 ``get_actual_qos()`` 是最合适的名称，因此我们只能为该方法另选一个不够直观的名称。

Publisher 和 Subscription 类的 API 破坏性变更
"""""""""""""""""""""""""""""""""""""""""""""

为了简化 Publisher 和 Subscription 的构造过程，我们更改了构造函数的 API。

无法支持弃用周期，因为旧签名接受 rcl 类型，而新签名接受 ``NodeBaseInterface`` 类型，以便获取它现在所需的额外信息，而仅凭 rcl 类型无法获得这些额外信息。
如果有助益于贡献者，新签名也许可以向后移植；但由于 publisher 和 subscription 几乎总是通过工厂函数或其他更高层 API 创建，我们认为这对大多数用户不会造成问题。

更多详情请查看原始 PR，如果这带来了问题，请在那里发表评论：

`https://github.com/ros2/rclcpp/pull/867 <https://github.com/ros2/rclcpp/pull/867>`_

关于 ``add_on_set_parameters_callback`` 返回值未被使用的编译器警告
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

*自 Eloquent 补丁版本 2（2020-12-04）起*

用户应保留 ``rclcpp::Node::add_on_set_parameters_callback`` 返回的句柄，否则他们的回调可能会被注销。
我们添加了一条警告，以帮助识别返回的句柄未被使用的缺陷。

`https://github.com/ros2/rclcpp/pull/1243 <https://github.com/ros2/rclcpp/pull/1243>`_

rmw
^^^

由于新增 Publisher 和 Subscription 选项而导致的 API 破坏性变更
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

``rmw_create_publisher()`` 方法新增了一个 ``const rmw_publisher_options_t *`` 类型的参数。
这个新结构体保存了新建 publisher 的选项（typesupport、主题名和 QoS 之外的选项）。

``rmw_create_subscription()`` 方法移除了一个参数 ``bool ignore_local_publications``，并用 ``const rmw_subscription_options_t *`` 类型的新选项取代了它。
``ignore_local_publications`` 选项被移入新的 ``rmw_subscription_options_t`` 类型中。

在这两种情况下，新参数都是指针，且绝不能为 null，因此 rmw 实现应检查以确保选项不为 null。
此外，还应将这些选项复制到对应的 rmw 结构体中。

更多详情请参见此 pull request 以及相关的 pull request：

`https://github.com/ros2/rmw/pull/187 <https://github.com/ros2/rmw/pull/187>`_

ros2cli
^^^^^^^

ros2msg 和 ros2srv 已弃用
"""""""""""""""""""""""""

CLI 工具 ``ros2msg`` 和 ``ros2srv`` 已弃用。
它们已被 ``ros2interface`` 工具取代，该工具还支持 action 和 IDL 接口。
你可以运行 ``ros2 interface --help`` 查看用法。

ros2node
""""""""

ros2node info 中新增了服务客户端。
作为该变更的一部分，Python 函数 ``ros2node.api.get_service_info``
已被重命名为 ``ros2node.api.get_service_server_info``。

rviz
^^^^

重命名 “2D Nav Goal” 工具
"""""""""""""""""""""""""

该工具被重命名为 “2D Goal Pose”，且默认主题从 ``/move_base_simple/goal`` 改为 ``/goal_pose``。

相关 pull request 如下：

`https://github.com/ros2/rviz/pull/455 <https://github.com/ros2/rviz/pull/455>`_

TF2 Buffer
^^^^^^^^^^

现在必须为 TF2 buffer 提供计时器接口。

如果未提供计时器接口，将抛出异常。

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

为了应对日益复杂的接口以及如今扩展后的配置选项集合，ROS CLI 语法已发生变化。
例如，使用 Dashing 语法的命令行如下：

.. code-block:: console

    $ ros2 run some_package some_node foo:=bar __params:=/path/to/params.yaml __log_level:=WARN --user-flag

使用 Eloquent（及之后版本）语法的写法为：

.. code-block:: console

    $ ros2 run some_package some_node --ros-args --remap foo:=bar --params-file /path/to/params.yaml --log-level WARN -- --user-flag

这种显式语法带来了新功能，例如单参数赋值 ``--param name:=value``。
更多参考与理由，请查阅 `ROS 命令行参数设计文档 <https://design.ros2.org/articles/ros_command_line_arguments.html>`__。

.. warning::

   旧语法已被弃用，并将在下一个发行版中移除。

已知问题
--------

* `[ros2/rosidl#402] <https://github.com/ros2/rosidl/issues/402>`_ ``find_package(PCL)`` 会干扰 ROS 接口生成。
  变通方法：在 ``rosidl_generate_interfaces()`` *之后* 调用 ``find_package(PCL)``。
* `[ros2/rclcpp#893] <https://github.com/ros2/rclcpp/issues/893>`_ ``rclcpp::Context`` 由于与 ``rclcpp::GraphListener`` 之间存在引用循环而不会被析构。这会导致内存泄漏。由于存在破坏 ABI 的风险，该修复尚未向后移植。

发行前的时间线
--------------

以下是发行前的一些里程碑：

    周一 9 月 30 日（alpha）
        核心软件包的首次发行版可供使用。
        从现在起可以开始测试（部分功能可能尚未合入）。

    周五 10 月 18 日
        核心软件包的 API 与功能冻结
        此后只应发布缺陷修复版本。
        新软件包可以独立发布。

    周四 10 月 24 日（beta）
        核心软件包的更新版本可供使用。
        对最新功能进行额外测试。

    周三 11 月 13 日（release candidate）
        核心软件包的更新版本可供使用。

    周二 11 月 19 日
        冻结 rosdistro。
        rosdistro 仓库中针对 Eloquent 的 PR 将不会被合并（发行公告后重新开放）。
