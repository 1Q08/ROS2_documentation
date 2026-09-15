.. _jazzy-release:

Jazzy Jalisco（``jazzy``）
==========================

.. toctree::
   :hidden:

   Jazzy-Jalisco-Complete-Changelog

.. contents:: 目录
   :depth: 2
   :local:

*Jazzy Jalisco* 是 ROS 2 的第十个发行版。
以下内容介绍了自上一个发行版以来 Jazzy Jalisco 中的重要变更和新特性。
自 Iron 以来的全部变更列表，请参阅 :doc:`完整变更日志 <Jazzy-Jalisco-Complete-Changelog>`。

支持的平台
----------

根据 `平台支持层级 <../The-ROS2-Project/Platform-Support-Tiers>`，Jazzy Jalisco 支持以下平台：

Tier 1 平台：

* Ubuntu 24.04 (Noble): ``amd64`` and ``arm64``
* Windows 10 (Visual Studio 2019): ``amd64``

Tier 2 平台：

* RHEL 9: ``amd64``

Tier 3 平台：

* macOS: ``amd64``
* Debian Bookworm: ``amd64``

目标平台：

+--------------+-----------------------+----------------------+----------------------+-----------------------+---------+-----------------------+-----------------------------+
| Architecture | Ubuntu Noble (24.04)  | Windows 10 (VS2019)  | RHEL 9               | Ubuntu Jammy (22.04)  | macOS   | Debian Bookworm (12)  | OpenEmbedded /              |
|              |                       |                      |                      |                       |         |                       | Yocto Project               |
+==============+=======================+======================+======================+=======================+=========+=======================+=============================+
| amd64        | Tier 1 [d][a][s]      | Tier 1 [a][s]        | Tier 2 [d][a][s]     | Tier 3 [s]            | Tier 3  | Tier 3 [s]            | Tier 3 [s]                  |
|              |                       |                      |                      |                       | [s]     |                       |                             |
+--------------+-----------------------+----------------------+----------------------+-----------------------+---------+-----------------------+-----------------------------+
| arm64        | Tier 1 [d][a][s]      |                      |                      |                       |         | Tier 3 [s]            | Tier 3 [s]                  |
+--------------+-----------------------+----------------------+----------------------+-----------------------+---------+-----------------------+-----------------------------+
| arm32        | Tier 3 [s]            |                      |                      |                       |         | Tier 3 [s]            | Tier 3 [s]                  |
+--------------+-----------------------+----------------------+----------------------+-----------------------+---------+-----------------------+-----------------------------+


以下指标说明了每个平台可用的交付机制。

\" \[d\] \" 将为提交到 rosdistro 的软件包提供平台特定的（Debian、RPM 等）软件包。

\" \[a\] \" 以每个平台一个压缩包的形式提供二进制发行包，其中包含 Jazzy ROS 2 repos 文件中的所有软件包[^13]。

\" \[s\] \" 从源码编译。

中间件实现支持：

+--------------------------+-------------------------+---------------+----------------------------+--------------------------------+
| Middleware Library       | Middleware Provider     | Support Level | Platforms                  | Architectures                  |
+==========================+=========================+===============+============================+================================+
| rmw_fastrtps_cpp*        | eProsima Fast-DDS       | Tier 1        | All Platforms              | All Architectures              |
+--------------------------+-------------------------+---------------+----------------------------+--------------------------------+
| rmw_cyclonedds_cpp       | Eclipse Cyclone DDS     | Tier 1        | All Platforms              | All Architectures              |
+--------------------------+-------------------------+---------------+----------------------------+--------------------------------+
| rmw_connextdds           | RTI Connext             | Tier 1        | Ubuntu, Windows, and macOS | All Architectures except arm64 |
+--------------------------+-------------------------+---------------+----------------------------+--------------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-DDS       | Tier 2        | All Platforms              | All Architectures              |
+--------------------------+-------------------------+---------------+----------------------------+--------------------------------+
| rmw_gurumdds_cpp         | GurumNetworks GurumDDS  | Tier 3        | Ubuntu and Windows         | All Architectures except arm32 |
+--------------------------+-------------------------+---------------+----------------------------+--------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持层级。例如，Tier 2 平台上的 Tier 1 中间件实现只能获得 Tier 2 级别的支持。

最低语言要求：

- C++17
- Python 3.8

依赖要求：

+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
|             | Required Support              | Recommended Support                                                        |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Package     | Ubuntu Noble  | Windows 10**  | RHEL 9 | Ubuntu Jammy | macOS**    | Debian Bookworm | OpenEmbedded**      |
+=============+===============+===============+========+==============+============+=================+=====================+
| CMake       | 3.28.3        | 3.22.0        | 3.20.2 | 3.22.1       | 3.20.0     | 3.25.1          | 3.22.3              |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| EmPY        | 3.3.4         | 3.3.2         | 3.3.4                                                                      |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Gazebo      | Harmonic*     | N/A           | N/A    | Harmonic*    | Harmonic*  | Harmonic*       | N/A                 |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| NumPy       | 1.26.4        | 1.18.4        | 1.20.1 | 1.21.5       | 1.18.4     | 1.24.2          | N/A                 |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Ogre        | 1.12.10                                                                              | N/A                 |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| OpenCV      | 4.6.0         | 3.4.6*        | 4.6.0  | 4.5.4        | 4.2.0      | 4.6.0           | 4.1.0 / 3.2.0***    |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| OpenSSL     | 3.0.13        | 1.1.1l        | 3.0.7  | 1.1.1l       | 1.1.1f     | 3.0.11          | 1.1.1d / 1.1.1b***  |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Python      | 3.12.3        | 3.8.3         | 3.9.16 | 3.10.4       | 3.10.8     | 3.11.2          | 3.8.2 / 3.7.5***    |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Qt          | 5.15.10       | 5.12.12       | 5.15.3 | 5.15.3       | 5.12.3     | 5.15.8          | 5.14.1 / 5.12.5***  |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
|                             | **Linux only**                                                                             |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| PCL         | 1.14.0        | N/A           | 1.12.0 | 1.12.1       | N/A        | 1.13.0          | 1.10.0              |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| **RMW DDS Middleware**                                                                                                   |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Cyclone DDS | 0.10.4                                                                                                     |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Fast-DDS    | 2.14.0                                                                                                     |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Connext DDS | 6.0.1                                                              | N/A                                   |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+
| Gurum DDS   | 4.2.0                         | N/A                                                                        |
+-------------+---------------+---------------+--------+--------------+------------+-----------------+---------------------+

\" \* \" 表示这不是上游版本（即官方操作系统仓库中提供的版本），而是由 OSRF 或社区发行的软件包（在自定义仓库上构建并分发的软件包）。

\" \*\* \" 表示该依赖可能会经历多个版本变更，因为该依赖使用的包管理器会持续更新，而没有稳定的 API。

\" \*\*\* \" webOS OSE 提供此不同版本。

本文档仅记录 ROS 发行版首次发布时的版本，不会随依赖的演进而更新。
因此这些版本是一个最低水位线。

依赖使用的包管理器：

- Ubuntu, Debian: apt, pip
- Windows: Chocolatey, pip
- macOS: Homebrew, pip
- RHEL: dnf
- OpenEmbedded: opkg

构建系统支持：

- ament_cmake
- cmake
- setuptools

安装
----

`安装 Jazzy Jalisco <../../jazzy/Installation.html>`__

ROS 2 与 Gazebo 集成方式的变更
------------------------------

从 Jazzy Jalisco 开始，我们正在简化 ROS 2 与 `Gazebo <https://gazebosim.org>`__ 的集成方式。
每个 ROS 2 发行版都会有一个推荐且受支持的 Gazebo 发行版与之搭配。
对于 Jazzy Jalisco，推荐的 Gazebo 发行版为 Harmonic。

为了便于 ROS 2 软件包使用 Gazebo 软件包，现在提供了 ``gz_*_vendor`` 软件包。
这些软件包包括：

* gz_common_vendor: https://github.com/gazebo-release/gz_common_vendor
* gz_cmake_vendor: https://github.com/gazebo-release/gz_cmake_vendor
* gz_math_vendor: https://github.com/gazebo-release/gz_math_vendor
* gz_transport_vendor: https://github.com/gazebo-release/gz_transport_vendor
* gz_sensor_vendor: https://github.com/gazebo-release/gz_sensor_vendor
* gz_sim_vendor: https://github.com/gazebo-release/gz_sim_vendor
* gz_tools_vendor: https://github.com/gazebo-release/gz_tools_vendor
* gz_utils_vendor: https://github.com/gazebo-release/gz_utils_vendor
* sdformat_vendor: https://github.com/gazebo-release/sdformat_vendor

ROS 2 软件包可以通过在 ``package.xml`` 中添加依赖来使用这些软件包中的功能，例如：

.. code::

   <depend>gz_math_vendor</depend>

然后在 ``CMakeLists.txt`` 中使用它们，例如：

.. code::

   find_package(gz_math_vendor REQUIRED)
   find_package(gz-math)

   add_executable(my_executable src/exe.cpp)
   target_link_libraries(my_executable gz-math::core)

.. note::

   在 Jazzy Jalisco 中仍然可以使用其他 Gazebo 版本。但这些版本不会经过同样充分的测试，也不会有同样好的 ROS 2 集成。更多信息请参阅 https://gazebosim.org/docs/harmonic/ros_installation。

此 ROS 2 发行版中的新特性
-------------------------

``common_interfaces``
^^^^^^^^^^^^^^^^^^^^^

新增 VelocityStamped 消息
"""""""""""""""""""""""""

新增了一条消息，包含定义速度并对其进行变换所需的全部字段。

更多详情请参阅 https://github.com/ros2/common_interfaces/pull/240。

为 Marker.msg 新增 ARROW_STRIP
""""""""""""""""""""""""""""""

为 Marker.msg 新增了新的标记类型 ``ARROW_STRIP``。

更多详情请参阅 https://github.com/ros2/common_interfaces/pull/242。

``image_transport``
^^^^^^^^^^^^^^^^^^^

支持惰性订阅者
""""""""""""""

更多详情请参阅 https://github.com/ros-perception/image_common/issues/272。

提供设置回调组的选项
""""""""""""""""""""

更多详情请参阅 https://github.com/ros-perception/image_common/issues/274。

启用允许列表
""""""""""""

新增参数，使用户能够在运行时选择性地禁用 ``image_transport`` 插件。

更多详情请参阅 https://github.com/ros-perception/image_common/issues/264。

使用自定义 QoS 发布和订阅
"""""""""""""""""""""""""

允许用户在创建 ``image_transport`` 发布者和订阅者时传入自定义的服务质量（QoS）。

更多详情请参阅 https://github.com/ros-perception/image_common/issues/288。

为 Republish 新增 rclcpp 组件
"""""""""""""""""""""""""""""

用户现在可以将 ``image_transport`` 转发节点作为 rclcpp_component 启动。

更多详情请参阅 https://github.com/ros-perception/image_common/issues/275。


``message_filters``
^^^^^^^^^^^^^^^^^^^

TypeAdapters 支持
"""""""""""""""""

允许用户在 message_filters 中使用类型适配（Type Adaptation）。

更多信息请参阅 https://github.com/ros2/message_filters/pull/96。

``rcl``
^^^^^^^

新增获取类型描述服务
""""""""""""""""""""

实现了 ``~/get_type_description`` 服务，允许外部用户获取节点提供的每种类型的描述。
每个节点都按照 `REP 2016 <https://github.com/ros-infrastructure/rep/pull/381>`__ 提供该服务。

更多详情请参阅 https://github.com/ros2/rcl/pull/1052。

``rclcpp``
^^^^^^^^^^

服务的类型支持辅助工具
""""""""""""""""""""""

新增了用于服务的类型支持辅助工具 ``rclcpp::get_service_typesupport_handle``，用于提取服务类型支持句柄。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2209。

``rclpy``
^^^^^^^^^

ParameterEventHandler
"""""""""""""""""""""

新的 ``ParameterEventHandler`` 类允许我们通过参数事件监视并响应参数变更。

更多详情请参阅 https://github.com/ros2/rclpy/pull/1135。

``ros2cli``
^^^^^^^^^^^

新增 ``--log-file-name`` 命令行参数
"""""""""""""""""""""""""""""""""""

现在可以使用 ``--log-file-name`` 命令行参数指定日志文件名前缀。

.. code-block:: console

   $ ros2 run demo_nodes_cpp talker --ros-args --log-file-name filename

更多信息请参阅 https://github.com/ros2/ros2cli/issues/856。

为订阅选项新增 QoS
""""""""""""""""""

在 ``TopicStatisticsOptions`` 中新增了用户可设置的 QoS 参数，使统计信息可以具有与订阅本身不同的 QoS。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2323。

新增客户端和服务数量
""""""""""""""""""""

现在可以获取某个服务创建的客户端数量。

``ros2action``
^^^^^^^^^^^^^^

支持 ``type`` 子命令
""""""""""""""""""""

现在可以使用 ``type`` 子命令检查动作类型。

.. code-block:: console

   $ ros2 action type /fibonacci
   action_tutorials_interfaces/action/Fibonacci

更多信息请参阅 https://github.com/ros2/ros2cli/pull/894。

``rosbag2``
^^^^^^^^^^^

服务数据录制与回放
""""""""""""""""""

现在可以使用 ``ros2bag`` 命令行界面录制和回放服务数据。

此特性基于 `服务内省 <https://github.com/ros2/ros2/issues/1285>`__，该功能自 Iron Irwini 起可用。
`服务录制与显示 <https://github.com/ros2/rosbag2/pull/1480>`__ 增加了将服务数据录制到 bag 文件中的能力。
而 `服务回放 <https://github.com/ros2/rosbag2/pull/1481>`__ 可以从 bag 文件中回放这些服务数据。

录制所有服务数据：

.. code-block:: console

   $ ros2 bag record --all-services

录制所有服务和所有话题数据：

.. code-block:: console

   $ ros2 bag record --all

从 bag 文件回放服务数据：

.. code-block:: console

   $ ros2 bag play --publish-service-requests bag_path

更多信息请参阅 `设计文档 <https://github.com/ros2/rosbag2/blob/rolling/docs/design/rosbag2_record_replay_service.md>`__。

新增过滤模式
""""""""""""

现在可以按话题类型进行过滤。

.. code-block:: console

    $ ros2 bag record --topic_types sensor_msgs/msg/Image sensor_msgs/msg/CameraInfo

.. code-block:: console

    $ ros2 bag record --topic_types sensor_msgs/msg/Image

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1577 和 https://github.com/ros2/rosbag2/pull/1582。

Player 和 Recorder 现在作为 rclcpp 组件暴露
"""""""""""""""""""""""""""""""""""""""""""

这允许在数据录制或回放期间使用进程内通信时实现“零拷贝”。
在处理高带宽数据流时，这可以显著降低录制或回放期间的 CPU 负载，并有助于避免传输层的数据丢失。
它还提供了为 ``rosbag2_transport::Player`` 和 ``rosbag2_transport::Recorder`` 可组合节点使用 YAML 配置文件的能力。

更多详情请参阅 https://github.com/ros2/rosbag2/tree/jazzy?tab=readme-ov-file#using-with-composition。

新增禁用录制器键盘控制的选项
""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1607。

录制期间使用来自 ``message_info`` 的中间件发送和接收时间戳
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

在可用的情况下，``rosbag2`` 现在使用中间件提供的发送和接收时间戳。
这些时间戳更能反映数据实际发送和接收的时间。
请注意，目前仅 MCAP 文件（默认格式）支持将时间戳保存到 bag 中。

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1531。

为录制选项新增压缩线程优先级
""""""""""""""""""""""""""""

现在可以指定执行压缩的线程的优先级。

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1457。

新增按时间拆分已有 ros2 bag 的能力
""""""""""""""""""""""""""""""""""

在 ``StorageOptions`` 中新增了 ``start_time_ns`` 和 ``end_time_ns``，以在 ``ros2 bag convert`` 操作期间排除不在
``[start_time;end_time]`` 范围内的消息。

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1455。

直接在 bag 文件中存储序列化元数据
"""""""""""""""""""""""""""""""""

``rosbag2`` 一直将元数据存储在 bag 文件关联的 ``metadata.yaml`` 文件中。
现在元数据还存储在每一个 bag 文件中，一次在打开文件时，另一次在关闭写入的 bag 文件时。
这使得 bag 文件可以自包含，从而无需 ``metadata.yaml`` 文件即可在 rosbag2 播放器或第三方应用中使用。
如有需要，仍可使用 ``ros2 bag reindex`` 恢复 ``metadata.yaml`` 文件。

在元数据中存储 ROS_DISTRO 名称
""""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1241。

为 Python 绑定新增内省 QoS 方法
"""""""""""""""""""""""""""""""

现在可以从 Python 绑定中内省 QoS 设置。

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1648。

``rosidl``
^^^^^^^^^^

新增支持键注解的接口
""""""""""""""""""""

``key`` 注解用于指明某个数据成员是键的一部分；键可以包含零个或多个键字段，并且可应用于各种类型的结构字段。

更多详情请参阅 https://github.com/ros2/rosidl/pull/796 和 https://github.com/ros2/rosidl_typesupport_fastrtps/pull/116。

``rviz2``
^^^^^^^^^

为 TF 显示新增正则表达式过滤字段
""""""""""""""""""""""""""""""""

当 ``/tf`` 上有许多坐标系时，在 RViz 中很难正确可视化它们，尤其是在坐标系重叠时。
通常的解决方法是在 TF 显示的 Frames 字段中启用和禁用所需的坐标系。
现在可以使用正则表达式过滤坐标系。

更多详情请参阅 https://github.com/ros2/rviz/pull/1032。

将测得的订阅频率追加到话题状态
""""""""""""""""""""""""""""""

可以在话题状态部件中可视化 Hz。

更多详情请参阅 https://github.com/ros2/rviz/issues/1113。

重置功能
""""""""

可以使用新服务或键盘快捷键 ``R`` 重置时间。

更多详情请参阅 https://github.com/ros2/rviz/issues/1109 和 https://github.com/ros2/rviz/issues/1088。

新增对 point_cloud_transport 的支持
"""""""""""""""""""""""""""""""""""

可以使用 ``point_cloud_transport`` 软件包订阅点云。

更多详情请参阅 https://github.com/ros2/rviz/pull/1008。

与用于 ROS 的 RViz 功能对等
"""""""""""""""""""""""""""

可以使用 ROS 1 版本中提供的相同插件。

* DepthCloud
* AccelStamped
* TwistStamped
* WrenchStamped
* Effort

相机信息显示
""""""""""""

可以在 3D 场景中可视化 CameraInfo 消息。

更多详情请参阅 https://github.com/ros2/rviz/pull/1166。

``rcpputils``
^^^^^^^^^^^^^

新增 tl_expected
""""""""""""""""

`std::expected <https://en.cppreference.com/w/cpp/utility/expected>`__ 是 C++23 特性，ROS 2 尚未支持。
不过，可以通过向后移植的实现来使用 rcpputils 中的 ``tl::expected``。

更多详情请参阅 https://github.com/ros2/rcpputils/pull/185。

``rcutils``
^^^^^^^^^^^

为日志格式新增人类可读的日期
""""""""""""""""""""""""""""

现在可以通过在 ``RCUTILS_CONSOLE_OUTPUT_FORMAT`` 环境变量中使用 ``{date_time_with_ms}`` 标记，在控制台日志中输出人类可读的日期格式。

更多详情请参阅 https://github.com/ros2/rcutils/pull/441。

自 Iron 发行版以来的变更
------------------------

``common_interfaces``
^^^^^^^^^^^^^^^^^^^^^

为 geometry_msgs/Polygon 和 PolygonStamped 新增 ID
""""""""""""""""""""""""""""""""""""""""""""""""""
多边形常用于表示特定对象，但当前若没有任何特定标识，则难以对其进行纠正。
此特性新增了 ID 字段以区分不同的多边形。

更多详情请参阅 https://github.com/ros2/common_interfaces/pull/232。


``geometry2``
^^^^^^^^^^^^^

移除已弃用的头文件
""""""""""""""""""

在 Humble 中，头文件：``tf2_bullet/tf2_bullet.h``、``tf2_eigen/tf2_eigen.h``、``tf2_geometry_msgs/tf2_geometry_msgs.h``、
``tf2_kdl/tf2_kdl.h``、``tf2_sensor_msgs/tf2_sensor_msgs.h`` 已被弃用，改用：``tf2_bullet/tf2_bullet.hpp``、
``tf2_eigen/tf2_eigen.hpp``、``tf2_geometry_msgs/tf2_geometry_msgs.hpp``、``tf2_kdl/tf2_kdl.hpp``、``tf2_sensor_msgs/tf2_sensor_msgs.hpp``
在 Jazzy 中，``tf2_bullet/tf2_bullet.h``、``tf2_eigen/tf2_eigen.h``、``tf2_geometry_msgs/tf2_geometry_msgs.h``、
``tf2_kdl/tf2_kdl.h``、``tf2_sensor_msgs/tf2_sensor_msgs.h`` 头文件已被完全移除。

更改了 ``wait_for_transform_async`` 和 ``wait_for_transform_full_async`` 的返回类型
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

以前，``Buffer`` 类的 ``wait_for_transform_async`` 和 ``wait_for_transform_full_async`` 返回一个包含 true 或 false 的 future
在 Jazzy 中，该 future 将包含正在等待的变换的信息。

启用 Twist 插值器
"""""""""""""""""

新增了用于查询运动坐标系在参考坐标系中速度的 API。

更多信息请参阅 https://github.com/ros2/geometry2/pull/646。

``rcl``
^^^^^^^

定时器被调用时的实际与预期调用时间
""""""""""""""""""""""""""""""""""

新增定时器 API ``rcl_timer_call_with_info``，用于在调用定时器时收集实际调用时间和预期调用时间。
这使用户可以获取定时器预期调用时间以及实际调用时间的信息。

更多详情请参阅 https://github.com/ros2/rcl/pull/1113。

改进 rcl_wait 的超时计算和虚假唤醒
""""""""""""""""""""""""""""""""""

为使用启用了时间覆盖的时钟的定时器新增了特殊处理。
对于这些定时器，我们不应计算超时，因为等待集会由关联的守卫条件唤醒。

更多详情请参阅 https://github.com/ros2/rcl/issues/1146。

``rclcpp``
^^^^^^^^^^

修复数据竞争条件
""""""""""""""""

修复了执行器中的数据竞争条件。

更多详情请参阅 https://github.com/ros2/rclcpp/issues/2500。

在执行器中使用 ``rclcpp::WaitSet``
""""""""""""""""""""""""""""""""""

通过让默认的单线程/多线程执行器在实体集合重建方面像静态单线程执行器一样工作，
来减少 ``rcl_wait_set`` 的创建和删除次数。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2142。

由于这一变更，执行器中的回调不再保持一致顺序，即使在同一实体内也是如此。

更多详情请参阅 https://github.com/ros2/rclcpp/issues/2532。

``rclcpp::get_typesupport_handle`` is deprecated
""""""""""""""""""""""""""""""""""""""""""""""""

用于提取消息类型支持句柄的 ``rclcpp::get_typesupport_handle`` 已被弃用，并将在未来的发行版中移除。
应改用 ``rclcpp::get_message_typesupport_handle``。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2209。

已弃用的 ``rclcpp/qos_event.hpp`` 头文件已被移除
""""""""""""""""""""""""""""""""""""""""""""""""

在 Iron 中，头文件 ``rclcpp/qos_event.hpp`` 已被弃用，改用 ``rclcpp/event_handler.hpp``。
在 Jazzy 中，``rclcpp/qos_event.hpp`` 头文件已被完全移除。

已弃用的订阅回调签名已被移除
""""""""""""""""""""""""""""

早在 Humble 中，形如 ``void callback(std::shared_ptr<MessageT>)`` 和 ``void callback(std::shared_ptr<MessageT>, const rclcpp::MessageInfo &)`` 的订阅签名就已被弃用。

在 Jazzy 中，这些订阅签名已被移除。
应改用 ``void callback(std::shared_ptr<const MessageT>)`` 或 ``void callback(std::shared_ptr<const MessageT>, const rclcpp MessageInfo &)``。

定时器被调用时的实际与预期调用时间
""""""""""""""""""""""""""""""""""

定时器回调新增了 ``rclcpp::TimerInfo`` 参数，用于在调用定时器时收集实际调用时间和预期调用时间。
这使用户可以获取定时器预期调用时间以及实际调用时间的信息。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2343。

``rclcpp_action``
^^^^^^^^^^^^^^^^^

取消后的回调
""""""""""""

新增了一个函数，用于在目标句柄超出作用域后停止其回调。
该函数允许我们在已锁定的上下文中释放句柄。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2281。

``rclcpp_lifecycle``
^^^^^^^^^^^^^^^^^^^^

新增节点接口 TypeDescriptionsInterface
""""""""""""""""""""""""""""""""""""""

新增节点接口 ``TypeDescriptionsInterface``，用于提供 ``GetTypeDescription`` 服务。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2224。

``rclpy``
^^^^^^^^^

``rclpy.node.Node.declare_parameter``
"""""""""""""""""""""""""""""""""""""

``rclpy.node.Node.declare_parameter`` 不允许在没有默认值的情况下对参数进行静态类型标注。

更多详情请参阅 https://github.com/ros2/rclpy/pull/1216。

为方法参数添加类型
""""""""""""""""""

新增类型检查，以改善使用静态类型检查的用户的体验。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2224、https://github.com/ros2/rclpy/issues/1240、https://github.com/ros2/rclpy/issues/1237、https://github.com/ros2/rclpy/issues/1231、https://github.com/ros2/rclpy/issues/1241 和 https://github.com/ros2/rclpy/issues/1233。

``rosbag2``
^^^^^^^^^^^

重命名 ``--exclude`` CLI 选项
"""""""""""""""""""""""""""""

``--exclude`` CLI 选项被重命名为 ``--exclude-regex``，以更好地反映其功能。

更多信息请参阅 https://github.com/ros2/rosbag2/pull/1480。

``offered_qos_profiles`` 表示方式的变更
"""""""""""""""""""""""""""""""""""""""

现在，代码中的 ``offered_qos_profiles`` 使用枚举值，元数据中的 QoS 设置以及覆盖用的 QoS 配置文件 YAML 文件中则使用人类可读的字符串值。

示例请参阅 https://github.com/ros2/rosbag2/tree/jazzy?tab=readme-ov-file#overriding-qos-profiles。

为读取和写入 bag 拆分事件消息新增节点名称
"""""""""""""""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1609。

在关闭 bag 时新增 ``BagSplitInfo`` 服务调用
"""""""""""""""""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1422。

解决了 rosbag2 中与处理 SIGINT 和 SIGTERM 信号相关的多个问题
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1557、https://github.com/ros2/rosbag2/pull/1301 和
https://github.com/ros2/rosbag2/pull/1464。

将存储返回的 ``topic_id`` 新增到 ``TopicMetadata`` 中
"""""""""""""""""""""""""""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1538。

为 CompressionOptions 和 CompressionMode 结构新增 Python 绑定
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1425。

提升 ``SqliteStorage::get_bagfile_size()`` 的性能
"""""""""""""""""""""""""""""""""""""""""""""""""

这可以最大限度地降低使用 SQLite3 存储插件录制时在 bag 拆分过程中丢失消息的概率。

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1516。

``rqt_bag``
^^^^^^^^^^^

提升性能并更新 rosbag API
"""""""""""""""""""""""""

rosbag2 API 和 Ubuntu Noble 库版本中有一些破坏性变更，因此需要对 ``rqt_bag`` 进行一些修改。

更多详情请参阅 https://github.com/ros-visualization/rqt_bag/pull/156。

开发进展
--------

关于 Jazzy Jalisco 的开发进展，请参阅 `此项目看板 <https://github.com/orgs/ros2/projects/52>`__。

关于 Jazzy Jalisco 所遵循的整体流程，请参阅 :doc:`流程说明页面 <Release-Process>`。

已知问题
--------

待补充。

发行时间线
----------

    2023 年 11 月 - 平台决策
        REP 2000 更新了目标平台和主要依赖项的版本。

    2024 年 1 月前 - Rolling 平台切换
        构建农场更新为 Jazzy Jalisco 的新平台版本和依赖项版本。

    2024 年 4 月 8 日（周一）- Alpha + RMW 冻结
        对 ROS Base [1]_ 软件包进行初步测试和稳定化，并对 RMW 提供者软件包进行 API 和特性冻结。

    2024 年 4 月 15 日（周一）- 冻结
        对 Rolling Ridley 中的 ROS Base [1]_ 软件包进行 API 和特性冻结。
        此后只应发布缺陷修复版本。
        新软件包可以独立发布。

    2024 年 4 月 22 日（周一）- 分支
        从 Rolling Ridley 分支。
        ``rosdistro`` 重新开放接受针对 ROS Base [1]_ 软件包的 Rolling PR。
        Jazzy 的开发从 ``ros-rolling-*`` 软件包转向 ``ros-jazzy-*`` 软件包。

    2024 年 4 月 29 日（周一）- Beta
        提供更新后的 ROS Desktop [2]_ 软件包发行版。
        呼吁进行广泛测试。

    2024 年 5 月 1 日（周三）- 启动教程派对
        托管在 https://github.com/osrf/ros2_test_cases 的教程向社区开放测试。

    2024 年 5 月 13 日（周一）- 候选发行版
        构建候选发行版软件包。
        提供更新后的 ROS Desktop [2]_ 软件包发行版。

    2024 年 5 月 20 日（周一）- 发行版冻结
        冻结所有 `ROS 2 桌面软件包 <https://reps.openrobotics.org/rep-2001/#jazzy-jalisco-may-2024-may-2029>`__ 上的所有 Jazzy 分支以及 ``rosdistro``。
        不会合并任何针对 ``jazzy`` 分支或 ``rosdistro`` 仓库中 ``jazzy/distribution.yaml`` 的拉取请求。

    2024 年 5 月 23 日（周四）- 正式发布
        发布公告。
        `ROS 2 桌面软件包 <https://reps.openrobotics.org/rep-2001/#jazzy-jalisco-may-2024-may-2029>`__ 的源码冻结解除，并且 ``rosdistro`` 重新开放接受 Jazzy 拉取请求。

.. [1] ``ros_base`` 变体在 `REP 2001 (ros-base) <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中描述。
.. [2] ``desktop`` 变体在 `REP 2001 (desktop-variants) <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中描述。
