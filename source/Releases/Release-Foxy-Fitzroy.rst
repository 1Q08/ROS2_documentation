Foxy Fitzroy（``foxy``）
========================

.. contents:: 目录
   :depth: 2
   :local:

*Foxy Fitzroy* 是 ROS 2 的第六个发行版。

支持的平台
----------

Foxy Fitzroy 根据 `平台支持层级 <../The-ROS2-Project/Platform-Support-Tiers>`
，支持以下平台：

第 1 层级平台：

* Ubuntu 20.04（Focal）：``amd64`` 和 ``arm64``
* Mac macOS 10.14（Mojave）
* Windows 10（Visual Studio 2019）

第 3 层级平台：

* Ubuntu 20.04（Focal）：``arm32``
* Debian Buster（10）：``amd64``、``arm64`` 和 ``arm32``
* OpenEmbedded Thud（2.6） / webOS OSE：``arm32`` 和 ``x86``

目标平台：

+--------------+-----------------------+----------------------+--------------------+-------------------+----------------+
|     架构     |  Ubuntu Focal (20.04) | MacOS Mojave (10.14) | Windows 10 (VS2019)| Debian Buster (10)| OpenEmbedded / |
|              |                       |                      |                    |                   | webOS OSE      |
+==============+=======================+======================+====================+===================+================+
|     amd64    |  第 1 层级 [d][a][s]  |   第 1 层级 [a][s]   |  第 1 层级 [a][s]  |   第 3 层级 [s]   |                |
+--------------+-----------------------+----------------------+--------------------+-------------------+----------------+
|     arm64    |  第 1 层级 [d][a][s]  |                      |                    |   第 3 层级 [s]   |  第 3 层级 [s] |
+--------------+-----------------------+----------------------+--------------------+-------------------+----------------+
|     arm32    |     第 3 层级 [s]     |                      |                    |   第 3 层级 [s]   |  第 3 层级 [s] |
+--------------+-----------------------+----------------------+--------------------+-------------------+----------------+

以下指标说明了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为此平台提供
Debian 软件包。

\" \[a\] \" 以每个平台一个压缩包的形式提供二进制发行版，其中包含
Foxy ROS 2 repos 文件[^9]中的所有软件包。

\" \[s\] \" 从源码编译。

中间件实现支持：

+--------------------------+-----------------------+---------------+-------------------------+-----------------------------------+
|         中间件库         |      中间件供应商     |    支持层级   |           平台          |                架构               |
+==========================+=======================+===============+=========================+===================================+
|     rmw_fastrtps_cpp*    |   eProsima Fast-RTPS  |   第 1 层级   |         所有平台        |              所有架构             |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------------+
|    rmw_cyclonedds_cpp    |  Eclipse Cyclone DDS  |   第 1 层级   |         所有平台        |              所有架构             |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------------+
|      rmw_connext_cpp     |      RTI Connext      |   第 1 层级   | 所有平台，除 Debian 和  | 所有架构，除                      |
|                          |                       |               | OpenEmbedded 外         | arm64/arm32 外                    |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------------+
| rmw_fastrtps_dynamic_cpp |   eProsima Fast-RTPS  |   第 2 层级   |         所有平台        |              所有架构             |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------------+
|     rmw_gurumdds_cpp     |     GurumNetworks     |   第 3 层级   |    Ubuntu 和 Windows    |       除 arm32 外的所有架构       |
|                          |        GurumDDS       |               |                         |                                   |
+--------------------------+-----------------------+---------------+-------------------------+-----------------------------------+


\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持层级。例如，第 1 层级中间件实现运行在
第 2 层级平台上时，只能获得第 2 层级支持。

最低语言要求：

- C++14
- Python 3.7

依赖项要求：

+--------------+------------------+------------------+------------------+------------------+-----------------------+
|              |                        必需支持                        |                 推荐支持                 |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
|    软件包    |   Ubuntu Focal   |      MacOS**     |   Windows 10**   |   Debian Buster  |     OpenEmbedded**    |
+==============+==================+==================+==================+==================+=======================+
| CMake        | 3.16.3           | 3.14.4           | 3.14.4           | 3.13.4           | 3.16.1 / 3.12.2****   |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| EmPY         | 3.3.2                                                                                             |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| Gazebo       | 11.0.0*          | 11.0.0           | N/A              | 11.0.0*          | N/A                   |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| Ignition     | Citadel*                            | N/A              | Citadel*         | N/A                   |
+--------------+-------------------------------------+------------------+------------------+-----------------------+
| Ogre         | 1.10*                                                                     | N/A                   |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| OpenCV       | 4.2.0            | 4.2.0            | 3.4.6*           | 3.2.0            | 4.1.0 / 3.2.0****     |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| OpenSSL      | 1.1.1d           | 1.1.1f           | 1.1.1f           | 1.1.1d           | 1.1.1d / 1.1.1b****   |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| Poco         | 1.9.2            | 1.9.0            | 1.8.0*           | 1.9.0            | 1.9.4                 |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| Python       | 3.8.0            | 3.8.2            | 3.8.0            | 3.7.3            | 3.8.2 / 3.7.5****     |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| Qt           | 5.12.5           | 5.12.3           | 5.10.0           | 5.11.3           | 5.14.1 / 5.12.5****   |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
|                                 |                                **仅 Linux 平台**                               |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| PCL          | 1.10.0           | N/A              | N/A              | 1.9.1            | 1.10.0                |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
|                                             **RMW DDS 中间件供应商**                                             |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| Connext DDS  | 5.3.1                                                  | N/A                                      |
+--------------+-------------------------------------+------------------+------------------------------------------+
| Cyclone DDS  | 0.7.x (Coquette)                                                                                  |
+--------------+---------------------------------------------------------------------------------------------------+
| Fast-RTPS    | 2.0.x                                                                                             |
+--------------+------------------+------------------+------------------+------------------+-----------------------+
| Gurum DDS    | 2.7.x            | N/A              | 2.7.x            | N/A                                      |
+--------------+------------------+------------------+------------------+------------------------------------------+

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

`安装 Foxy Fitzroy <../../foxy/Installation.html>`__

此 ROS 2 发行版中的新特性
-------------------------

在开发过程中，GitHub 上的 `Foxy 元工单 <https://github.com/ros2/ros2/issues/830>`__ 包含当前高层任务的最新状态，以及指向更详细具体工单的引用。

补丁版本 8 的变更（2022-09-28）
-------------------------------

Launch GroupAction 限定环境变量的作用域
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``SetEnvironmentVariable`` 操作现在会被限定在它所属的任意 ``GroupAction`` 作用域内。

例如，考虑以下 launch 文件，

.. tabs::

   .. group-tab:: Python

      .. code-block:: python

         import launch
         from launch.actions import SetEnvironmentVariable
         from launch.actions import GroupAction
         from launch_ros.actions import Node


         def generate_launch_description():
             return launch.LaunchDescription([
                 SetEnvironmentVariable(name='my_env_var', value='1'),
                 Node(package='foo', executable='foo', output='screen'),
                 GroupAction([
                     SetEnvironmentVariable(name='my_env_var', value='2'),
                 ]),
             ])

   .. group-tab:: XML

      .. code-block:: xml

         <launch>
           <set_env name="my_env_var" value="1"/>
           <node pkg="foo" exec="foo" output="screen" />
           <group>
             <set_env name="my_env_var" value="2"/>
           </group>
         </launch>

在补丁版本 8 之前，节点 ``foo`` 启动时会带有 ``my_env_var=2``，而现在它会以 ``my_env_var=1`` 启动。

要退出这一新行为，可以在 ``GroupAction`` 上设置参数 ``scoped=False``。

相关工单：


* `ros2#1244 <https://github.com/ros2/ros2/issues/1244>`_
* `launch#630 <https://github.com/ros2/launch/pull/630>`_

补丁版本 7 的变更（2022-02-08）
-------------------------------

Launch 前端 set_env 行为变更
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`launch#468 <https://github.com/ros2/launch/pull/468>`_ 无意中改变了前端 launch 文件中 ``set_env`` 操作的作用域行为。
使用 ``set_env`` 操作对环境变量所做的更改不再限定在父级 ``group`` 操作的作用域内，而是全局生效。
由于该改动已被向后移植，因此它影响到本发行版。

我们认为这一改动是一次回归，并打算在下一个补丁版本以及未来的 ROS 发行版中修复该行为。
我们还计划修复 Python launch 文件中的该行为，这些文件从未正确限定设置环境变量的作用域。

相关问题：

* `ros2#1244 <https://github.com/ros2/ros2/issues/1244>`_
* `launch#597 <https://github.com/ros2/launch/issues/597>`_

修复 launch 前端解析器
^^^^^^^^^^^^^^^^^^^^^^

对 launch 前端解析器的一次重构修复了一些 `解析特殊字符的问题 <https://github.com/ros2/launch_ros/issues/214>`_。
其结果是，在解析字符串时出现了细微的行为变化。
例如，以前要把数字作为字符串传递，你必须添加额外的引号（如果使用替换，需要两组引号）：

.. code-block:: xml

   <!-- results in the string value "'3'" -->
   <param name="foo" value="''3''"/>

重构之后，上述写法会得到字符串 ``"''3''"`` （注意多出的那组引号）。
现在，用户应使用 ``type`` 属性来表明该值应被解释为字符串：

.. code-block:: xml

   <param name="foo" value="3" type="str"/>

相关拉取请求：

* `launch#530 <https://github.com/ros2/launch/pull/530>`_
* `launch_ros#265 <https://github.com/ros2/launch_ros/pull/265>`_

修复 rmw_fastrtps_dynamic_cpp 中的内存泄漏和未定义行为
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下头文件中的 API 已更改：

- ``rmw_fastrtps_dynamic_cpp/TypeSupport.hpp``
- ``rmw_fastrtps_dynamic_cpp/TypeSupport_impl.hpp``

尽管从技术上讲它们是公开可访问的，但人们不太可能直接使用它们。
因此，我们决定破坏 API 以修复内存泄漏和未定义行为。

该修复最初提交于 `rmw_fastrtps#429 <https://github.com/ros2/rmw_fastrtps/pull/429>`_，随后通过 `rmw_fastrtps#577 <https://github.com/ros2/rmw_fastrtps/pull/577>`_ 向后移植到 Foxy。

补丁版本 2 的变更（2020-08-07）
-------------------------------

static_transform_publisher 中的缺陷
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
在 Foxy 开发期间，tf2_ros 的 static_transform_publisher 程序中引入了一个缺陷。
传给 static_transform_publisher 的欧拉角顺序实现与文档不一致。
Foxy 补丁版本 2 `修复 <https://github.com/ros2/geometry2/pull/296>`_ 了这一顺序，使实现与文档（yaw、pitch、roll）一致。
对于已经开始使用 Foxy 初始发行版或补丁版本 1 的用户来说，这意味着所有使用 static_transform_publisher 的 launch 文件都必须按照新顺序交换命令行参数顺序。
对于来自 ROS 2 Dashing、ROS 2 Eloquent 或 ROS 1 的用户，无需做任何更改即可迁移到 Foxy 补丁版本 2。

自 Eloquent 发行版以来的变更
----------------------------

经典 CMake 与现代 CMake
^^^^^^^^^^^^^^^^^^^^^^^

在“经典” CMake 中，软件包在被 ``find_package()`` 时提供诸如 ``<pkgname>_INCLUDE_DIRS`` 和 ``<pkgname>_LIBRARIES`` 这样的 CMake 变量。
使用 ``ament_cmake`` 时，这通过调用 ``ament_export_include_directories`` 和 ``ament_export_libraries`` 来实现。
再结合 ``ament_export_dependencies``，``ament_cmake`` 确保递归依赖的所有包含目录和库都会被拼接并包含在这些变量中。

在“现代” CMake 中，软件包改为提供接口目标（通常命名为 ``<pkgname>::<pkgname>``），它本身封装了所有递归依赖。
为了导出库目标以使用现代 CMake，需要调用 ``ament_export_targets`` 并指定一个导出名称，该名称在使用 ``install(TARGETS <libA> <libB> EXPORT <export_name> ...)`` 安装库时也会用到。
导出的接口目标可通过 CMake 变量 ``<pkgname>_TARGETS`` 获取。
要让库目标能够这样导出，它们不能依赖影响全局状态的经典函数（如 ``include_directories()``），而必须使用生成器表达式在目标自身上设置包含目录（对构建环境以及安装环境都是如此），例如 ``target_include_directories(<target> PUBLIC "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>" "$<INSTALL_INTERFACE:include>")``。

当使用 ``ament_target_dependencies`` 为库目标添加依赖时，如果现代 CMake 目标可用，该函数就会使用它们。
否则，它会退回到使用经典 CMake 变量。
因此，只有当所有依赖也提供现代 CMake 目标时，你才应该导出现代 CMake 目标。
**否则，导出的接口目标会在生成的 CMake 逻辑中包含包含目录 / 库的绝对路径，从而使该软件包无法重定位。**

关于 Foxy 中软件包如何更新到现代 CMake 的示例，请参见 `ros2/ros2#904 <https://github.com/ros2/ros2/issues/904>`_。

ament_export_interfaces 被 ament_export_targets 取代
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``ament_cmake_export_interfaces`` 软件包中的 CMake 函数 ``ament_export_interfaces`` 已被弃用，取而代之的是新软件包 ``ament_cmake_export_targets`` 中的函数 ``ament_export_targets``。
更多背景信息请参见 GitHub 工单 `ament/ament_cmake#237 <https://github.com/ament/ament_cmake/issues/237>`_。

rosidl_generator_c|cpp 命名空间 / API 变更
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``rosidl_generator_c`` 和 ``rosidl_generator_cpp`` 软件包已经过重构，许多头文件和源文件被移入新软件包 ``rosidl_runtime_c`` 和 ``rosidl_runtime_cpp``。
其目的是消除对生成器软件包的运行时依赖，从而也消除对使用 Python 的代码生成工具的运行时依赖。
在移动头文件的同时，包含路径 / 命名空间也相应更新，因此在许多情况下，只需把 include 指令从生成器软件包改为运行时软件包即可。

生成的 C / C++ 代码也已重构。
以 ``__struct.h|hpp``、``__functions.h``、``__traits.hpp`` 等结尾的文件已被移入子目录 ``detail``，但大多数代码只包含以接口命名的头文件，而不带这些后缀。

一些与字符串和序列边界相关的类型也已重命名以符合命名约定，但不预期在用户代码中使用它们（即在 RMW 实现和类型支持软件包之上）

更多信息请参见 `ros2/rosidl#446（C 语言） <https://github.com/ros2/rosidl/issues/446>`_ 和 `ros2/rosidl#447（C++） <https://github.com/ros2/rosidl/issues/447>`_。

ament_add_test 的默认工作目录
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用 ``ament_add_test`` 添加的测试的默认工作目录已更改为 ``CMAKE_CURRENT_BINARY_DIR``，以匹配 CMake ``add_test`` 的行为。
要么更新测试以适配新的默认值，要么传入 ``WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}`` 以恢复之前的值。

默认控制台日志格式
^^^^^^^^^^^^^^^^^^

默认的控制台日志输出格式已更改，默认包含时间戳，参见：

- `https://github.com/ros2/rcutils/pull/190 <https://github.com/ros2/rcutils/pull/190>`_
- `https://discourse.ros.org/t/ros2-logging-format/11549 <https://discourse.ros.org/t/ros2-logging-format/11549>`_

默认控制台日志输出流
^^^^^^^^^^^^^^^^^^^^

从 Foxy 起，所有严重级别的日志消息默认都会记录到 stderr。
这可以确保日志消息立即输出，并使 ROS 2 日志系统与大多数其他日志系统保持一致。
可以在运行时通过 RCUTILS_LOGGING_USE_STDOUT 环境变量将输出流改为 stdout，但所有日志消息仍会写入同一个流。
更多详细信息请参见 `https://github.com/ros2/rcutils/pull/196 <https://github.com/ros2/rcutils/pull/196>`_。

launch_ros
^^^^^^^^^^

节点名称和命名空间参数已变更
""""""""""""""""""""""""""""

与命名相关的 ``Node`` 操作参数已更改：

- ``node_name`` 已重命名为 ``name``
- ``node_namespace`` 已重命名为 ``namespace``
- ``node_executable`` 已重命名为 ``executable``
- 新增 ``exec_name``，用于命名与该节点关联的进程。
  以前，用户会使用 ``name`` 关键字参数。

旧参数已被弃用。

做出这些更改是为了让 launch 前端更符合惯用风格。
例如，不用

.. code-block:: xml

   <node pkg="demo_nodes_cpp" exec="talker" node-name="foo" />

我们现在可以写成

.. code-block:: xml

   <node pkg="demo_nodes_cpp" exec="talker" name="foo" />

此更改同样适用于 ``ComposableNodeContainer``、``ComposableNode`` 和 ``LifecycleNode``。
示例请参见 `demos 的相关更改。 <https://github.com/ros2/demos/pull/431>`_

`launch_ros 中的相关拉取请求。 <https://github.com/ros2/launch_ros/pull/122>`_

rclcpp
^^^^^^

高级订阅回调签名的变更
""""""""""""""""""""""

通过拉取请求 `https://github.com/ros2/rclcpp/pull/1047 <https://github.com/ros2/rclcpp/pull/1047>`_，同时接收消息信息和消息的回调签名已更改。
以前它使用 ``rmw`` 类型 ``rmw_message_info_t``，现在使用 ``rclcpp`` 类型 ``rclcpp::MessageInfo``。
所需的更改很直接，可在以下拉取请求中看到演示：

- `https://github.com/ros2/system_tests/pull/423/files <https://github.com/ros2/system_tests/pull/423/files>`_
- `https://github.com/ros2/rosbag2/pull/375/files <https://github.com/ros2/rosbag2/pull/375/files>`_
- `https://github.com/ros2/ros1_bridge/pull/253/files <https://github.com/ros2/ros1_bridge/pull/253/files>`_

序列化消息回调签名的变更
""""""""""""""""""""""""

拉取请求 `ros2/rclcpp#1081 <https://github.com/ros2/rclcpp/pull/1081>`_ 引入了以序列化形式获取 ROS 消息的回调的新签名。
以前使用的 C 结构体 `rcl_serialized_message_t <https://github.com/ros2/rmw/blob/foxy/rmw/include/rmw/serialized_message.h>`_ 正被 C++ 数据类型 `rclcpp::SerializedMessage <https://github.com/ros2/rclcpp/blob/foxy/rclcpp/include/rclcpp/serialized_message.hpp>`_ 取代。

``demo_nodes_cpp`` 中的示例节点，即 ``talker_serialized_message`` 以及 ``listener_serialized_message``，反映了这些更改。

节点接口 getter 签名的破坏性变更
""""""""""""""""""""""""""""""""

通过拉取请求 `ros2/rclcpp#1069 <https://github.com/ros2/rclcpp/pull/1069>`_，节点接口 getter 的签名已被修改为返回节点接口的共享所有权（即 ``std::shared_ptr``），而不是非拥有的裸指针。
依赖旧签名的下游软件包所需的更改简单直接：使用 ``std::shared_ptr::get()`` 方法。

弃用 set_on_parameters_set_callback
"""""""""""""""""""""""""""""""""""

请改用 ``rclcpp::Node`` 的方法 ``add_on_set_parameters_callback`` 和 ``remove_on_set_parameters_callback`` 来添加和移除在设置参数时调用的函数。

相关拉取请求：https://github.com/ros2/rclcpp/pull/1123

发布者 getter 签名的破坏性变更
""""""""""""""""""""""""""""""

通过拉取请求 `ros2/rclcpp#1119 <https://github.com/ros2/rclcpp/pull/1119>`_，发布者句柄 getter 的签名已被修改为返回底层 rcl 结构的共享所有权（即 ``std::shared_ptr``），而不是非拥有的裸指针。
这是为了修复某些情况下的段错误所必需的。
依赖旧签名的下游软件包所需的更改简单直接：使用 ``std::shared_ptr::get()`` 方法。

rclcpp_action
^^^^^^^^^^^^^

弃用 ClientGoalHandle::async_result()
"""""""""""""""""""""""""""""""""""""

使用此 API 时，可能会遇到竞态条件而导致抛出异常。
建议改用更安全的 ``Client::async_get_result()``。

更多信息请参见 `ros2/rclcpp#1120 <https://github.com/ros2/rclcpp/pull/1120>`_ 及关联问题。

rclpy
^^^^^

支持多个参数设置回调
""""""""""""""""""""

使用 ``Node`` 的方法 ``add_on_set_parameters_callback`` 和 ``remove_on_set_parameters_callback`` 来添加和移除在设置参数时调用的函数。

方法 ``set_parameters_callback`` 已被弃用。

相关拉取请求：https://github.com/ros2/rclpy/pull/457、https://github.com/ros2/rclpy/pull/504

rmw_connext_cpp
^^^^^^^^^^^^^^^

Connext 5.1 定位器种类兼容模式
""""""""""""""""""""""""""""""

直到 ``Eloquent`` （含）为止，``rmw_connext_cpp`` 都会将 ``dds.transport.use_510_compatible_locator_kinds`` 属性设置为 ``true``。
不再强制设置此属性，``Foxy`` 与之前发行版之间的共享传输通信将停止工作。
类似于以下的日志：

.. code-block:: bash

  PRESParticipant_checkTransportInfoMatching:Warning: discovered remote participant 'RTI Administration Console' using the 'shmem' transport with class ID 16777216.
  This class ID does not match the class ID 2 of the same transport in the local participant 'talker'.
  These two participants will not communicate over the 'shmem' transport.
  Check the value of the property 'dds.transport.use_510_compatible_locator_kinds' in the local participant.
  See https://community.rti.com/kb/what-causes-error-discovered-remote-participant for additional info.

会在发生这种不兼容时出现。

如果需要兼容性，可以在外部 QoS 配置文件中设置，内容包含：

.. code-block:: xml

   <participant_qos>
      <property>
         <value>
               <element>
                  <name>
                     dds.transport.use_510_compatible_locator_kinds
                  </name>
                  <value>1</value>
               </element>
         </value>
      </property>
   </participant_qos>

请记得将 ``NDDS_QOS_PROFILES`` 环境变量设置为 QoS 配置文件的路径。
更多信息请参见 `Transport_Compatibility <https://community.rti.com/static/documentation/connext-dds/5.2.0/doc/manuals/connext_dds/html_files/RTI_ConnextDDS_CoreLibraries_ReleaseNotes/Content/ReleaseNotes/Transport_Compatibility.htm>`_ 中的 ``How to Change Transport Settings in 5.2.0 Applications for Compatibility with 5.1.0`` 一节。

rviz
^^^^

工具使用 ROS 时间戳记消息
"""""""""""""""""""""""""

'2D Pose Estimate'、'2D Nav Goal' 和 'Publish Point' 工具现在使用 ROS 时间而非系统时间为它们的消息添加时间戳，以便 ``use_sim_time`` 参数对它们生效。

相关拉取请求：https://github.com/ros2/rviz/pull/519

std_msgs
^^^^^^^^

消息的弃用
""""""""""

尽管长期以来都不被推荐，我们现已正式弃用 ``std_msgs`` 中的以下消息。
在 `example_interfaces <https://index.ros.org/p/example_interfaces>`_ 中有它们的副本

- ``std_msgs/msg/Bool``
- ``std_msgs/msg/Byte``
- ``std_msgs/msg/ByteMultiArray``
- ``std_msgs/msg/Char``
- ``std_msgs/msg/Float32``
- ``std_msgs/msg/Float32MultiArray``
- ``std_msgs/msg/Float64``
- ``std_msgs/msg/Float64MultiArray``
- ``std_msgs/msg/Int16``
- ``std_msgs/msg/Int16MultiArray``
- ``std_msgs/msg/Int32``
- ``std_msgs/msg/Int32MultiArray``
- ``std_msgs/msg/Int64``
- ``std_msgs/msg/Int64MultiArray``
- ``std_msgs/msg/Int8``
- ``std_msgs/msg/Int8MultiArray``
- ``std_msgs/msg/MultiArrayDimension``
- ``std_msgs/msg/MultiArrayLayout``
- ``std_msgs/msg/String``
- ``std_msgs/msg/UInt16``
- ``std_msgs/msg/UInt16MultiArray``
- ``std_msgs/msg/UInt32``
- ``std_msgs/msg/UInt32MultiArray``
- ``std_msgs/msg/UInt64``
- ``std_msgs/msg/UInt64MultiArray``
- ``std_msgs/msg/UInt8``
- ``std_msgs/msg/UInt8MultiArray``

安全特性
^^^^^^^^

安全飞地的使用
""""""""""""""

从 Foxy 起，域参与者不再直接映射到 ROS 节点。
因此，ROS 2 安全特性（它们是针对域参与者的）也不再直接映射到 ROS 节点。
取而代之的是，Foxy 引入了安全“飞地”（enclave）的概念，其中“飞地”是一个进程或一组进程，它们将共享相同的身份和访问控制规则。

这意味着安全工件 **不再** 基于节点名称来获取，而是基于安全飞地名称来获取。
可以使用 ROS 参数 ``--enclave`` 设置节点的飞地名称，例如 ``ros2 run demo_nodes_py talker --ros-args --enclave /my_enclave``

相关设计文档：https://github.com/ros2/design/pull/274

请注意，权限文件受底层传输数据包大小的限制，因此如果生成的权限文件超过 64kB，将许多权限归组到同一个飞地下将 **不会** 生效。
相关问题 `[ros2/sros2#228] <https://github.com/ros2/sros2/issues/228>`_

环境变量的重命名
""""""""""""""""

.. list-table:: 环境变量重命名
   :widths: 25 25
   :header-rows: 1

   * - Eloquent 中的名称
     - Foxy 中的名称
   * - ROS_SECURITY_ROOT_DIRECTORY
     - ROS_SECURITY_KEYSTORE
   * - ROS_SECURITY_NODE_DIRECTORY
     - ROS_SECURITY_ENCLAVE_OVERRIDE


已知问题
--------

* `[ros2/ros2#922] <https://github.com/ros2/ros2/issues/922>`_ 对于使用 eProsima Fast-RTPS 或 ADLINK CycloneDDS 作为 RMW 实现的 ``rclcpp`` 节点，服务的性能不稳定。
  具体来说，服务客户端有时收不到来自服务端的响应。

* `[ros2/rclcpp#1212] <https://github.com/ros2/rclcpp/issues/1212>`_ 就绪的可重入 Waitable 对象可能会尝试执行多次。


发行前的时间线
--------------

发行前的几个里程碑：

    .. note::

      以下日期反映了因新冠疫情而延长的大约两周时间。

    2020 年 4 月 22 日（周三）
        ``ros_core`` [1]_ 软件包的 API 和特性冻结。
        请注意，这包括 ``rmw``，它是 ``ros_core`` 的递归依赖。
        在此之后只应发布缺陷修复版本。
        新软件包可以独立发布。

    2020 年 4 月 29 日（周一）（beta）
        ``desktop`` [2]_ 软件包的更新版本可用。
        对新特性进行测试。

    2020 年 5 月 27 日（周三）（release candidate）
        ``desktop`` [2]_ 软件包的更新版本可用。

    2020 年 6 月 3 日（周三）
        冻结 rosdistro。
        不会合并 rosdistro 仓库上针对 Foxy 的任何 PR（在发行公告后重新开放）。

.. [1] `variants <https://github.com/ros2/variants>`_ 仓库中描述的 ``ros_core`` 变体。
.. [2] `variants <https://github.com/ros2/variants>`_ 仓库中描述的 ``desktop`` 变体。
