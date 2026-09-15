.. redirect-from::

  Release-Crystal-Clemmys

Crystal Clemmys（``crystal``）
==============================

.. contents:: 目录
   :depth: 2
   :local:

*Crystal Clemmys* 是 ROS 2 的第三个发行版。

支持的平台
----------

根据 `平台支持层级 <../The-ROS2-Project/Platform-Support-Tiers>`，Crystal Clemmys 支持以下平台：

第 1 层级平台：

* Ubuntu 18.04（Bionic）
* Mac macOS 10.12（Sierra）
* Windows 10

第 2 层级平台：

* Ubuntu 16.04（Xenial）

目标平台：

+--------------+-----------------------+----------------------+--------------------+-----------------------+-------------------+
|     架构     | Ubuntu Bionic (18.04) | MacOS Sierra (10.12) | Windows 10 (VS2017)| Ubuntu Xenial (16.04) | Debian Stretch (9)|
+==============+=======================+======================+====================+=======================+===================+
| amd64        |  第 1 层级 [d][a][s]  |   第 1 层级 [a][s]   |  第 1 层级 [a][s]  |     第 2 层级 [s]     |   第 3 层级 [s]   |
+--------------+-----------------------+----------------------+--------------------+-----------------------+-------------------+
| arm64        |  第 1 层级 [d][a][s]  |                      |                    |     第 2 层级 [s]     |   第 3 层级 [s]   |
+--------------+-----------------------+----------------------+--------------------+-----------------------+-------------------+

以下指示符说明了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为其提供该平台的 Debian 软件包。

\" \[a\] \" 二进制发行版按平台提供单个归档文件，其中包含 Crystal ROS 2 repos 文件中的所有软件包[^4]。

\" \[s\] \" 从源代码编译。

中间件实现支持：

+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
|         中间件库         |    中间件供应商     |   支持层级    |            平台             |              架构              |
+==========================+=====================+===============+=============================+================================+
| rmw_fastrtps_cpp*        | eProsima Fast-RTPS  |   第 1 层级   |          所有平台           |            所有架构            |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_connext_cpp          | RTI Connext         |   第 1 层级   |   除 Debian 外的所有平台    |     除 arm64 外的所有架构      |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_opensplice_cpp       | ADLINK OpenSplice   |   第 2 层级   |   除 Debian 外的所有平台    |            所有架构            |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-RTPS  |   第 2 层级   |          所有平台           |            所有架构            |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_connext_dynamic_cpp  | RTI Connext         |   第 2 层级   |   除 Debian 外的所有平台    |     除 arm64 外的所有架构      |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持层级。例如，第 2 层级平台上的第 1 层级中间件实现，只能获得第 2 层级的支持。

最低语言要求：

- C11[^5]
- C++14
- Python 3.5

依赖项要求：

+------------+----------------------------------------------------------+--------------------+
|            |                        必需的支持                        |     推荐的支持     |
+------------+---------------+----------+-------------+-----------------+--------------------+
|   软件包   | Ubuntu Bionic | MacOS**  | Windows 10* | Ubuntu Xenial[s]| Debian Stretch [s] |
+============+===============+==========+=============+=================+====================+
| CMake      | 3.10.2        | 3.13.3   | 3.13.3      | 3.5.1           | 3.7.2              |
+------------+---------------+----------+-------------+-----------------+--------------------+
| EmPY       | 3.3.2         | 3.3.2    | 3.3.2       | 3.3.2           | 3.3.2              |
+------------+---------------+----------+-------------+-----------------+--------------------+
| Gazebo     | 9.0.0         | 9.9.0    | N/A         | 9.9.0*          | 9.8.0*             |
+------------+---------------+----------+-------------+-----------------+--------------------+
| Ogre       | 1.10*                                                                         |
+------------+---------------+----------+-------------+-----------------+--------------------+
| OpenCV     | 3.2.0         | 4.0.1    | 3.4.1*      | 2.4.9           | 3.2*               |
+------------+---------------+----------+-------------+-----------------+--------------------+
| OpenSSL    | 1.1.0g        | 1.0.2q   | 1.0.2q      | 1.0.2g          | 1.1.0j             |
+------------+---------------+----------+-------------+-----------------+--------------------+
| Poco       | 1.8.0         | 1.9.0    | 1.8.0*      | 1.8.0*          | 1.8.0*             |
+------------+---------------+----------+-------------+-----------------+--------------------+
| Python     | 3.6.5         | 3.7.2    | 3.7.2       | 3.5.1           | 3.5.3              |
+------------+---------------+----------+-------------+-----------------+--------------------+
| Qt         | 5.9.5         | 5.12.0   | 5.10.0      | 5.5.1           | 5.7.1              |
+------------+---------------+----------+-------------+-----------------+--------------------+
|                            |      **仅 Linux**      |                                      |
+------------+---------------+----------+-------------+-----------------+--------------------+
| PCL        | 1.8.1         | N/A      | N/A         | 1.7.2           | 1.8.0              |
+------------+---------------+----------+-------------+-----------------+--------------------+
|                                  **RMW DDS 中间件供应商**                                  |
+------------+---------------+----------+-------------+-----------------+--------------------+
| Connext DDS| 5.3.1                                                    | N/A                |
+------------+----------------------------------------------------------+--------------------+
| Fast-RTPS  | 1.7.0                                                                         |
+------------+-------------------------------------------------------------------------------+
| OpenSplice | 6.9.181127OSS                                                                 |
+------------+-------------------------------------------------------------------------------+

\" \* \" 表示这不是上游版本（操作系统官方仓库中提供的版本），而是由 OSRF 或社区分发的软件包（在自定义仓库中构建和分发的软件包）。

\" \*\* \" 滚动发行版在其生命周期内会经历这些依赖项的多次版本变更。

\" \[s\] \" 从源代码编译，ROS 构建农场不会为这些平台生成任何二进制软件包。

本文档仅记录 ROS 发行版首次发布时的版本，不会随着依赖项的演进更新。因此这些版本是一个最低基准。

依赖项使用的软件包管理器：

- Ubuntu、Debian：apt
- MacOS：Homebrew、pip
- Windows：Chocolatey、pip

构建系统支持：

- ament_cmake
- cmake
- setuptools

此 ROS 2 发行版中的新功能
-------------------------

* C / C++ 中的动作（`服务器 <https://github.com/ros2/examples/tree/af08e6f7ac50f7808dbe6165f1adfd8e6cd3a79c/rclcpp/minimal_action_server>`__ / `客户端 <https://github.com/ros2/examples/tree/af08e6f7ac50f7808dbe6165f1adfd8e6cd3a79c/rclcpp/minimal_action_client>`__ 示例）
* `gazebo_ros_pkgs <http://gazebosim.org/tutorials?tut=ros2_overview>`__
* `image_transport <https://github.com/ros-perception/image_common/wiki/ROS2-Migration>`__
* `navigation2 <https://github.com/ros-planning/navigation2/blob/master/README.md>`__
* `rosbag2 <https://index.ros.org/r/rosbag2/github-ros2-rosbag2/#crystal>`__
* `rqt <../../Concepts/Intermediate/About-RQt>`
* 内存管理方面的改进
* 关于节点的内省信息
* 启动系统改进

  * `参数 <https://github.com/ros2/launch/pull/123>`__
  * `嵌套启动文件 <https://github.com/ros2/launch/issues/116>`__
  * `条件 <https://github.com/ros2/launch/issues/105>`__
  * `向节点传递参数 <https://github.com/ros2/launch/issues/117>`__

* 为 `基于文件的日志记录和 /rosout 发布 <https://github.com/ros2/rcl/pull/327>`__ 奠定了基础
* `Python 中的时间与时长 API <https://github.com/ros2/rclpy/issues/186>`__
* `参数可与 Python 节点配合使用 <https://github.com/ros2/rclpy/issues/202>`__


自 Bouncy 发行版以来的变更
--------------------------

自 `Bouncy Bolson <Release-Bouncy-Bolson>` 发行版以来的变更：

* geometry2 - ``tf2_ros::Buffer`` API 变更

  ``tf2_ros::Buffer`` 现在使用 ``rclcpp::Time``，其构造函数要求传入指向 ``rclcpp::Clock`` 实例的 ``shared_ptr``。
  详情请参见 https://github.com/ros2/geometry2/pull/67，示例用法如下：

  .. code-block:: c++

    #include <tf2_ros/transform_listener.h>
    #include <rclcpp/rclcpp.hpp>
    ...
    # Assuming you have a rclcpp::Node my_node
    tf2_ros::Buffer buffer(my_node.get_clock());
    tf2_ros::TransformListener tf_listener(buffer);

* 所有 ``rclcpp`` 和 ``rcutils`` 日志宏都需要分号。

  详情请参见 https://github.com/ros2/rcutils/issues/113。

* ``rcutils_get_error_string_safe()`` 和 ``rcl_get_error_string_safe()`` 已替换为 ``rcutils_get_error_string().str`` 和 ``rcl_get_error_string().str``。

  详情请参见 https://github.com/ros2/rcutils/pull/121。

* rmw - ``rmw_init`` API 变更

  新增了两个结构体 ``rcl_context_t`` 和 ``rcl_init_options_t``，它们与 ``rmw_init`` 一起使用。
  初始化选项结构体用于将选项向下传递给中间件，是 ``rmw_init`` 的输入。
  上下文是一个句柄，作为 ``rmw_init`` 函数的输出，用于标识每个实体关联的是哪一次初始化-关闭周期；这里的“实体”是指所创建的任何东西，例如节点、守护条件等。

  这里列出这一点，是因为替代 rmw 实现的维护者需要实现这些新函数，才能让他们的 rmw 实现可在 Crystal 中工作。

  以下是发生了签名变更的函数：

  * `rmw_init <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init.h#L54-L82>`__

  此外，以下这些新函数需要由每个 rmw 实现来提供：

  * `rmw_shutdown <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init.h#L84-L109>`__
  * `rmw_init_options_init <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init_options.h#L62-L92>`__
  * `rmw_init_options_copy <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init_options.h#L94-L128>`__
  * `rmw_init_options_fini <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init_options.h#L130-L153>`__

  以下示例展示了为遵循此 API 变更，rmw 实现中至少需要修改的内容：

  * `rmw_fastrtps pr <https://github.com/ros2/rmw_fastrtps/pull/237/files>`_

* rcl - ``rcl_init`` API 变更

  与上面的 ``rmw`` 变更类似，``rcl`` 中新增了两个结构体 ``rcl_context_t`` 和 ``rcl_init_options_t``。
  初始化选项作为输入传入 ``rcl_init``，而上下文作为输出传出。
  上下文用于将所有其他 rcl 实体关联到特定的初始化-关闭周期，从而使 init 和 shutdown 不再是全局函数；更准确地说，这些函数不再使用全局状态，而是将所有状态封装在上下文类型中。

  任何客户端库实现（其底层也使用 ``rcl``）的维护者都需要做出修改才能在 Crystal 中工作。

  以下函数已被移除：

  * ``rcl_get_global_arguments``
  * ``rcl_get_instance_id``
  * ``rcl_ok``

  以下函数发生了签名变更：

  * `rcl_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init.h#L30-L82>`__
  * `rcl_shutdown <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init.h#L84-L111>`__
  * `rcl_guard_condition_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/guard_condition.h#L54-L99>`__
  * `rcl_guard_condition_init_from_rmw <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/guard_condition.h#L101-L140>`__
  * `rcl_node_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/node.h#L100-L194>`__
  * `rcl_timer_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/timer.h#L64-L159>`__

  以下是新增的函数与类型：

  * `rcl_context_t <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/context.h#L36-L136>`__
  * `rcl_get_zero_initialized_context <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/context.h#L138-L142>`__
  * `rcl_context_fini <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/context.h#L146-L171>`__
  * `rcl_context_get_init_options <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/context.h#L175-L205>`__
  * `rcl_context_get_instance_id <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/context.h#L207-L233>`__
  * `rcl_context_is_valid <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/context.h#L235-L255>`__
  * `rcl_init_options_t <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init_options.h#L32-L37>`__
  * `rcl_get_zero_initialized_init_options <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init_options.h#L39-L43>`__
  * `rcl_init_options_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init_options.h#L45-L73>`__
  * `rcl_init_options_copy <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init_options.h#L75-L105>`__
  * `rcl_init_options_fini <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init_options.h#L107-L128>`__
  * `rcl_init_options_get_rmw_init_options <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init_options.h#L130-L153>`__
  * `rcl_node_is_valid_except_context <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/node.h#L288-L299>`__
  * `rcl_publisher_get_context <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/publisher.h#L378-L404>`__
  * `rcl_publisher_is_valid_except_context <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/publisher.h#L428-L439>`__

  这些新增和变更的函数会影响你在客户端库中处理初始化和关闭的方式。
  有关示例，请查看以下 ``rclcpp`` 和 ``rclpy`` 的 PR：

  * `rclcpp <https://github.com/ros2/rclcpp/pull/587>`__
  * `rclpy <https://github.com/ros2/rclpy/pull/249>`__

  不过，你也可以继续在客户端库中只提供单一的全局初始化和关闭，并只存储一个全局上下文对象。

已知问题
--------

* Fast-RTPS 1.7.0 中的竞态条件可能导致在高负载下丢消息（`问题 <https://github.com/ros2/rmw_fastrtps/issues/258>`__）。
* 将 TRANSIENT_LOCAL QoS 配置与 rmw_fastrtps_cpp 一起使用，在消息较大时可能导致应用程序崩溃（`问题 <https://github.com/ros2/rmw_fastrtps/issues/257>`__）。
* rmw_fastrtps_cpp 与其他实现之间的跨供应商通信在 Windows 上无法正常工作（`问题 <https://github.com/ros2/rmw_fastrtps/issues/246>`__）。
* 在 macOS 和 Windows 上使用 OpenSplice（版本 < 6.9.190227）时，如果引用的字段类型其名称来自其他软件包，而当前软件包中也存在同名名称，你可能会遇到命名冲突（`问题 <https://github.com/ros2/rmw_opensplice/issues/259>`__）。
  升级到更新的 OpenSplice 版本以及至少 Crystal 的第三个补丁版本后，该问题应当得到解决。
  在 Linux 上，更新到最新的 Debian 软件包将包含最新的 OpenSplice 版本。
