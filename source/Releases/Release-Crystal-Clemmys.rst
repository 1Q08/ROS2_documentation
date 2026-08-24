.. redirect-from::

  Release-Crystal-Clemmys

Crystal Clemmys (``crystal``)
=============================

.. contents:: 目录
   :depth: 2
   :local:

*Crystal Clemmys* 是 ROS 2 的第三个版本。

支持的平台
----------

Crystal Clemmys 根据 `平台支持等级 <../The-ROS2-Project/Platform-Support-Tiers>` 支持以下平台：

一级平台：

* Ubuntu 18.04 (Bionic)
* Mac macOS 10.12 (Sierra)
* Windows 10

二级平台：

* Ubuntu 16.04 (Xenial)

目标平台：

+--------------+-----------------------+----------------------+--------------------+-----------------------+-------------------+
| 架构         | Ubuntu Bionic (18.04) | MacOS Sierra (10.12) | Windows 10 (VS2017)| Ubuntu Xenial (16.04) | Debian Stretch (9)|
+==============+=======================+======================+====================+=======================+===================+
| amd64        | Tier 1 [d][a][s]      | Tier 1 [a][s]        | Tier 1 [a][s]      | Tier 2 [s]            | Tier 3  [s]       |
+--------------+-----------------------+----------------------+--------------------+-----------------------+-------------------+
| arm64        | Tier 1 [d][a][s]      |                      |                    | Tier 2  [s]           | Tier 3 [s]        |
+--------------+-----------------------+----------------------+--------------------+-----------------------+-------------------+

以下指示符显示了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为此平台提供 Debian 软件包。

\" \[a\] \" 二进制版本以每个平台单个归档文件的形式提供，包含 Crystal ROS 2 repos 文件[^4] 中的所有软件包。

\" \[s\] \" 从源代码编译。

中间件实现支持：

+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| 中间件库                 | 中间件提供方        | 支持等级      | 平台                        | 架构                           |
+==========================+=====================+===============+=============================+================================+
| rmw_fastrtps_cpp*        | eProsima Fast-RTPS  | Tier 1        | All Platforms               | All Architectures              |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_connext_cpp          | RTI Connext         | Tier 1        | All Platforms except Debian | All Architectures except arm64 |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_opensplice_cpp       | ADLINK OpenSplice   | Tier 2        | All Platforms except Debian | All Architectures              |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_fastrtps_dynamic_cpp | eProsima Fast-RTPS  | Tier 2        | All Platforms               | All Architectures              |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+
| rmw_connext_dynamic_cpp  | RTI Connext         | Tier 2        | All platforms except Debian | All architectures except arm64 |
+--------------------------+---------------------+---------------+-----------------------------+--------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持
等级。例如，二级平台上的一个一级中间件实现
只能获得二级支持。

最低语言要求：

- C11[^5]
- C++14
- Python 3.5

依赖要求：

+------------+----------------------------------------------------------+--------------------+
|            | 必需支持                                                 | 推荐支持           |
+------------+---------------+----------+-------------+-----------------+--------------------+
| 软件包     | Ubuntu Bionic | MacOS**  | Windows 10* | Ubuntu Xenial[s]| Debian Stretch [s] |
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
|                            | **仅 Linux**           |                                      |
+------------+---------------+----------+-------------+-----------------+--------------------+
| PCL        | 1.8.1         | N/A      | N/A         | 1.7.2           | 1.8.0              |
+------------+---------------+----------+-------------+-----------------+--------------------+
| **RMW DDS 中间件提供方**                                                                   |
+------------+---------------+----------+-------------+-----------------+--------------------+
| Connext DDS| 5.3.1                                                    | N/A                |
+------------+----------------------------------------------------------+--------------------+
| Fast-RTPS  | 1.7.0                                                                         |
+------------+-------------------------------------------------------------------------------+
| OpenSplice | 6.9.181127OSS                                                                 |
+------------+-------------------------------------------------------------------------------+

\" \* \" 表示这不是上游版本（即操作系统官方仓库中可用的版本），而是由 OSRF 或社区分发的软件包（在自定义仓库中构建并分发的软件包）。

\" \*\* \" 滚动发行版将在其生命周期内看到这些依赖的多次版本变更。

\" \[s\] \" 从源代码编译，ROS 构建农场不会为这些平台生成任何二进制软件包。

本文档仅记录 ROS 发行版首次发布时的版本，不会随依赖的演进更新。
因此这些版本是一个低水位标记。

依赖使用的软件包管理器：

- Ubuntu, Debian: apt
- MacOS: Homebrew, pip
- Windows: Chocolatey, pip

构建系统支持：

- ament_cmake
- cmake
- setuptools

此 ROS 2 版本中的新功能
-----------------------

* C / C++ 中的动作（`服务端 <https://github.com/ros2/examples/tree/af08e6f7ac50f7808dbe6165f1adfd8e6cd3a79c/rclcpp/minimal_action_server>`__ / `客户端 <https://github.com/ros2/examples/tree/af08e6f7ac50f7808dbe6165f1adfd8e6cd3a79c/rclcpp/minimal_action_client>`__ 示例）
* `gazebo_ros_pkgs <http://gazebosim.org/tutorials?tut=ros2_overview>`__
* `image_transport <https://github.com/ros-perception/image_common/wiki/ROS2-Migration>`__
* `navigation2 <https://github.com/ros-planning/navigation2/blob/master/README.md>`__
* `rosbag2 <https://index.ros.org/r/rosbag2/github-ros2-rosbag2/#crystal>`__
* `rqt <../../Concepts/Intermediate/About-RQt>`
* 内存管理的改进
* 关于节点的自省信息
* 启动系统的改进

  * `参数 <https://github.com/ros2/launch/pull/123>`__
  * `嵌套启动文件 <https://github.com/ros2/launch/issues/116>`__
  * `条件 <https://github.com/ros2/launch/issues/105>`__
  * `向节点传递参数 <https://github.com/ros2/launch/issues/117>`__

* 为 `基于文件的日志记录和 /rosout 发布 <https://github.com/ros2/rcl/pull/327>`__ 奠定了基础
* `Python 中的 Time 和 Duration API <https://github.com/ros2/rclpy/issues/186>`__
* `参数可用于 Python 节点 <https://github.com/ros2/rclpy/issues/202>`__


自 Bouncy 版本以来的变更
------------------------

自 `Bouncy Bolson <Release-Bouncy-Bolson>` 版本以来的变更：

* geometry2 - ``tf2_ros::Buffer`` API 变更

  ``tf2_ros::Buffer`` 现在使用 ``rclcpp::Time``，构造函数需要一个指向 ``rclcpp::Clock`` 实例的 ``shared_ptr``。
  详情参见 https://github.com/ros2/geometry2/pull/67，示例用法如下：

  .. code-block:: c++

    #include <tf2_ros/transform_listener.h>
    #include <rclcpp/rclcpp.hpp>
    ...
    # Assuming you have a rclcpp::Node my_node
    tf2_ros::Buffer buffer(my_node.get_clock());
    tf2_ros::TransformListener tf_listener(buffer);

* 所有 ``rclcpp`` 和 ``rcutils`` 日志宏都需要分号。

  详情参见 https://github.com/ros2/rcutils/issues/113。

* ``rcutils_get_error_string_safe()`` 和 ``rcl_get_error_string_safe()`` 已被替换为 ``rcutils_get_error_string().str`` 和 ``rcl_get_error_string().str``。

  详情参见 https://github.com/ros2/rcutils/pull/121。

* rmw - ``rmw_init`` API 变更

  有两个新的结构体 ``rcl_context_t`` 和 ``rcl_init_options_t``，它们与 ``rmw_init`` 一起使用。
  init options 结构体用于将选项传递给中间件，并且是 ``rmw_init`` 的输入。
  context 是一个句柄，它是 ``rmw_init`` 函数的输出，用于标识每个实体关联的是哪个 init-shutdown 周期，其中 "实体" 是创建的任何东西，如节点、守卫条件等。

  这里列出这一点是因为替代 rmw 实现的维护者需要实现这些新函数，才能让他们的 rmw 实现在 Crystal 中工作。

  这是签名发生变化的函数：

  * `rmw_init <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init.h#L54-L82>`__

  此外，还有这些每个 rmw 实现都需要实现的新函数：

  * `rmw_shutdown <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init.h#L84-L109>`__
  * `rmw_init_options_init <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init_options.h#L62-L92>`__
  * `rmw_init_options_copy <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init_options.h#L94-L128>`__
  * `rmw_init_options_fini <https://github.com/ros2/rmw/blob/b7234243588a70fce105ea20b073f5ef6c1b685c/rmw/include/rmw/init_options.h#L130-L153>`__

  以下是一个 rmw 实现为遵循此 API 变更而最少需要修改的内容示例：

  * `rmw_fastrtps pr <https://github.com/ros2/rmw_fastrtps/pull/237/files>`_

* rcl - ``rcl_init`` API 变更

  与上面的 ``rmw`` 变更类似，``rcl`` 中有两个新结构体，称为 ``rcl_context_t`` 和 ``rcl_init_options_t``。
  init options 作为输入传入 ``rcl_init``，context 作为输出传入。
  context 用于将所有其他 rcl 实体关联到特定的 init-shutdown 周期，这实际上使 init 和 shutdown 不再是全局函数，或者更确切地说，这些函数不再使用全局状态，而是将所有状态封装在 context 类型中。

  任何客户端库实现的维护者（底层也使用 ``rcl``）都需要做出更改才能与 Crystal 一起工作。

  这些函数已被移除：

  * ``rcl_get_global_arguments``
  * ``rcl_get_instance_id``
  * ``rcl_ok``

  这些函数的签名发生了变化：

  * `rcl_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init.h#L30-L82>`__
  * `rcl_shutdown <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/init.h#L84-L111>`__
  * `rcl_guard_condition_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/guard_condition.h#L54-L99>`__
  * `rcl_guard_condition_init_from_rmw <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/guard_condition.h#L101-L140>`__
  * `rcl_node_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/node.h#L100-L194>`__
  * `rcl_timer_init <https://github.com/ros2/rcl/blob/657d9e84c73e4268176efd163e96fda73c1a76d9/rcl/include/rcl/timer.h#L64-L159>`__

  这些是新的函数和类型：

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

  这些新增和变更的函数将影响你在客户端库中处理 init 和 shutdown 的方式。
  相关示例，请查看以下 ``rclcpp`` 和 ``rclpy`` 的 PR：

  * `rclcpp <https://github.com/ros2/rclcpp/pull/587>`__
  * `rclpy <https://github.com/ros2/rclpy/pull/249>`__

  但是，你可以继续在客户端库中提供单一的全局 init 和 shutdown，只需存储一个全局 context 对象即可。

已知问题
--------

* Fast-RTPS 1.7.0 中的一个竞态条件可能导致消息在压力下丢失（`Issue <https://github.com/ros2/rmw_fastrtps/issues/258>`__）。
* 将 TRANSIENT_LOCAL QoS 设置与 rmw_fastrtps_cpp 一起使用可能会使应用程序在消息较大时崩溃（`Issue <https://github.com/ros2/rmw_fastrtps/issues/257>`__）。
* rmw_fastrtps_cpp 与其他实现之间的跨厂商通信在 Windows 上无法工作（`Issue <https://github.com/ros2/rmw_fastrtps/issues/246>`__）。
* 在 macOS 和 Windows 上使用 OpenSplice（版本 < 6.9.190227）时，如果其他软件包中的字段类型名称也存在于当前软件包中，引用这些名称时可能会遇到命名冲突（`Issue <https://github.com/ros2/rmw_opensplice/issues/259>`__）。
  通过更新到更新的 OpenSplice 版本以及至少 Crystal 的第三个补丁版本，应该可以解决这个问题。
  在 Linux 上，更新到最新的 Debian 软件包将包含最新的 OpenSplice 版本。
