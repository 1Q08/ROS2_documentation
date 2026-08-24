.. _kilted-release:

Kilted Kaiju (codename 'kilted'; May, 2025)
===========================================

.. toctree::
   :hidden:

   Kilted-Kaiju-Complete-Changelog

.. contents:: 目录
   :depth: 2
   :local:

*Kilted Kaiju* 是 ROS 2 的第十一个版本。
以下是自上一个版本以来 Kilted Kaiju 中的重要变更和功能的亮点。
有关自 Jazzy 以来的所有变更列表，请参阅 :doc:`详细变更日志 <Kilted-Kaiju-Complete-Changelog>`。

支持的平台
----------

Kilted Kaiju 根据 `平台支持等级 <../The-ROS2-Project/Platform-Support-Tiers>` 支持以下平台：

一级平台：

* Ubuntu 24.04 (Noble)：``amd64`` 和 ``arm64``
* Windows 10 (Visual Studio 2019)：``amd64``

二级平台：

* RHEL 9：``amd64``

三级平台：

* macOS：``amd64``
* Debian Bookworm：``amd64``

目标平台：

+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+
| 架构         | Ubuntu Noble      | Windows 10    | RHEL 9            | macOS     | Debian Bookworm | OpenEmbedded / |
|              | (24.04)           | (VS2019)      |                   |           | (12)            | Yocto Project  |
+==============+===================+===============+===================+===========+=================+================+
| amd64        | Tier 1 [d][a][s]  | Tier 1 [a][s] | Tier 2 [d][a][s]  | Tier 3 [s]| Tier 3 [s]      | Tier 3 [s]     |
+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+
| arm64        | Tier 1 [d][a][s]  |               |                   |           | Tier 3 [s]      | Tier 3 [s]     |
+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+
| arm32        | Tier 3 [s]        |               |                   |           | Tier 3 [s]      | Tier 3 [s]     |
+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+

以下指示符显示了每个平台可用的交付机制。

\" \[d\] \" 对于提交到 rosdistro 的软件包，将为此平台提供特定于发行版的（Debian、RPM 等）软件包。

\" \[a\] \" 二进制版本以每个平台单个归档文件的形式提供，包含 Jazzy ROS 2 repos 文件[^14] 中的所有软件包。

\" \[s\] \" 从源代码编译。

中间件实现支持：

+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| 中间件库                  | 中间件提供方            | 支持等级      | 平台                       | 架构                          |
+===========================+=========================+===============+============================+===============================+
| rmw_fastrtps_cpp*         | eProsima Fast-DDS       | Tier 1        | All Platforms              | All Architectures             |
+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_connextdds            | RTI Connext             | Tier 1        | Ubuntu, Windows, and macOS | All Architectures except arm64|
+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_cyclonedds_cpp        | Eclipse Cyclone DDS     | Tier 1        | All Platforms              | All Architectures             |
+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_zenoh_cpp             | Eclipse Zenoh           | Tier 1        | All Platforms              | All Architectures             |
+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_fastrtps_dynamic_cpp  | eProsima Fast-DDS       | Tier 2        | All Platforms              | All Architectures             |
+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| rmw_gurumdds_cpp          | GurumNetworks GurumDDS  | Tier 3        | Ubuntu and Windows         | All Architectures except arm32|
+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+

\" \* \" 表示默认的 RMW 实现。

中间件实现支持取决于平台支持
等级。例如，二级平台上的一个一级中间件实现
只能获得二级支持。

最低语言要求：

- C++17
- Python 3.9

依赖要求：

+---------------+-------------------------------+-------------------------------------------------------------+
|               | 必需支持                      | 推荐支持                                                    |
+===============+===============+===============+==========+==========+==================+====================+
| 软件包        | Ubuntu Noble  | Windows 10**  | RHEL 9   | macOS**  | Debian Bookworm  | OpenEmbedded**     |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| CMake         | 3.28.3        | 3.28.3        | 3.26.5   | 3.31.1   | 3.25.1           | 3.22.3             |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| EmPY          | 3.3.4         | 3.3.4         | 3.3.4a   | 3.3.4                                            |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| Gazebo        | Ionic*        | N/A           | N/A      | Ionic*   | Ionic*           | N/A                |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| NumPy         | 1.26.4        | 1.26.4        | 1.20.1   | 2.1.3    | 1.24.2           | N/A                |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| Ogre          | 1.12.10                                                                | N/A                |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| OpenCV        | 4.6.0         | 4.9.0         | 4.6.0    | 4.10.0   | 4.6.0            | 4.1.0 / 3.2.0***   |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| OpenSSL       | 3.0.13        | 3.3.2         | 3.2.2    | 1.1.1w   | 3.0.15           | 1.1.1d / 1.1.1b*** |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| Python        | 3.12.3        | 3.12.3        | 3.9.19   | 3.13.0   | 3.11.2           | 3.8.2 / 3.7.5***   |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| Qt            | 5.15.13       | 5.15.8        | 5.15.9   | 5.15.16  | 5.15.8           | 5.14.1 / 5.12.5*** |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
|                               | **仅 Linux**                                                                |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| PCL           | 1.14.0        | N/A           | 1.12.0   | 1.14.1   | 1.13.0           | 1.10.0             |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| **RMW 中间件**                                                                                              |
+---------------------------------------------------------------------+---------------------------------------+
| Connext DDS   | 7.3.0.0                                             | N/A                                   |
+---------------+-----------------------------------------------------+---------------------------------------+
| Cyclone DDS   | 0.10.5                                                                                      |
+---------------+---------------------------------------------------------------------------------------------+
| Fast-DDS      | 2.14.4                                                                                      |
+---------------+-------------------------------+-------------------------------------------------------------+
| Gurum DDS     | 4.2.0                         | N/A                                                         |
+---------------+-------------------------------+-------------------------------------------------------------+
| Zenoh         | 1.0.4                                                                                       |
+---------------+---------------------------------------------------------------------------------------------+

\" \* \" 表示这不是上游版本（即操作系统官方仓库中可用的版本），而是由 OSRF 或社区分发的软件包（在自定义仓库中构建并分发的软件包）。

\" \*\* \" 表示该依赖可能会看到多次版本变更，因为该依赖使用的软件包管理器在没有稳定 API 的情况下持续更新该依赖。

\" \*\*\* \" webOS OSE 提供了这个不同的版本。

本文档仅记录 ROS 发行版首次发布时的版本，不会随依赖的演进更新。
因此这些版本是一个低水位标记。

依赖使用的软件包管理器：

- Ubuntu, Debian: apt, pip
- Windows: pixi/conda, pip
- macOS: Homebrew, pip
- RHEL: dnf
- OpenEmbedded: opkg

构建系统支持：

- ament_cmake
- cargo
- cmake
- setuptools

安装
----

`安装 Kilted Kaiju <../../kilted/Installation.html>`__

支持的 Gazebo 版本
------------------
对于 Kilted Kaiju，推荐的 Gazebo 版本是 `Ionic <https://gazebosim.org/docs/ionic/ros_installation>`__。

此 ROS 2 版本中的新功能
-----------------------

``ament_cmake_ros``
^^^^^^^^^^^^^^^^^^^

添加 rmw_test_fixture 以支持 RMW 隔离测试
"""""""""""""""""""""""""""""""""""""""""

引入了两个新软件包，它们提供了一种可扩展的机制，用于为基于 RMW 的通信隔离创建测试夹具。
它的设计紧密参照了 rmw 和 rmw_implementation API。

``rmw_test_fixture`` 软件包目前只提供 API，RMW 提供方可以实现该 API，以配置其 RMW 用于运行测试。

``rmw_test_fixture_implementation`` 软件包提供了发现、加载和调用适当扩展的入口点。

有关更多细节，请参见 https://github.com/ros2/ament_cmake_ros/pull/21。

``common_interfaces``
^^^^^^^^^^^^^^^^^^^^^

新的 nav_msgs/Goals 消息
""""""""""""""""""""""""

引入了一种新的消息类型 {interface(nav_msgs/msg/Goals)}，用于在 nav_msgs 软件包中支持导航目标数组。

有关更多细节，请参见 https://github.com/ros2/common_interfaces/pull/269。

``ros2cli``
^^^^^^^^^^^

动作自省
""""""""

这允许使用命令行自省动作。
使用 ``ros2cli`` 工具：``ros2 action echo <action name>``。

有关更多信息，请参见 https://github.com/ros2/ros2cli/pull/978。

``rclcpp``
^^^^^^^^^^

动作泛型客户端
""""""""""""""

支持动作泛型客户端，这用于支持 rosbag2 中的动作。

有关更多细节，请参见 https://github.com/ros2/rclcpp/pull/2759。

``rclpy``
^^^^^^^^^

静态类型检查
""""""""""""

为 ``ActionClient`` 和 ``ActionServer`` 添加了静态类型提示。

有关更多细节，请参见 https://github.com/ros2/rclpy/pull/1349。

为 ``pub/sub/client/server/actions``、``Future/Task`` 和 ``Parameter`` 添加了 `泛型 <https://typing.python.org/en/latest/reference/generics.html>`_ 支持。

``Publisher``、``Subscription``、``Server``、``Task`` 和 ``Parameter`` 应该无需更新即可添加泛型支持。

``Client`` 需要更新为类似以下内容，以获得改进的类型检查。

.. code-block:: python

    self._get_parameter_client: Client[GetParameters.Request,
                                       GetParameters.Response] = self.node.create_client(
                                        GetParameters, '/get_parameters',
                                        qos_profile=qos_profile, callback_group=callback_group)

``ActionClient`` 需要更新为类似以下内容，以获得改进的类型检查。

.. code-block:: python

    ac: ActionClient[Fibonacci.Goal,
                     Fibonacci.Result,
                     Fibonacci.Feedback] = ActionClient(self.node, Fibonacci, 'fibonacci')

``Future`` 需要更新为类似以下内容，以获得改进的类型检查。

.. code-block:: python

    log_msgs_future: Future[bool] = Future()

有关更多细节，请参见 https://github.com/ros2/rclpy/pull/1239、https://github.com/ros2/rclpy/pull/1275、https://github.com/ros2/rclpy/pull/1246 和 https://github.com/ros2/rclpy/pull/1254/files。

在整个 ``rclpy`` 中还进行了各种其他小的改进和修正。

Python 类型可以使用 `ament_mypy <https://github.com/ament/ament_lint/tree/kilted/ament_mypy>`_ 进行静态检查，它封装了 `mypy <https://www.mypy-lang.org/>`_。

EventsExecutor
""""""""""""""

为 ``rclpy`` 支持一个实验性的事件执行器，它是原始 ``rclcpp`` 事件执行器概念的移植。

有关更多细节，请参见 https://github.com/ros2/rclpy/pull/1391。

``Rosbag2``
^^^^^^^^^^^

动作自省的 Rosbag2 支持
"""""""""""""""""""""""

允许从 rosbag 录制和播放动作。

有关更多信息，请参见 https://github.com/ros2/rosbag2/pull/1955。
设计文档 https://github.com/ros2/rosbag2/pull/1928。

``ros2 bag play`` 的进度条
""""""""""""""""""""""""""

为 ``ros2 bag play`` CLI 添加了进度条，显示 bag 时间和时长，类似于 ROS 1 中所见。

有关更多细节，请参见 https://github.com/ros2/rosbag2/pull/1836。

添加了使用 ``ros2 bag play`` CLI 重放多个 bag 的支持
""""""""""""""""""""""""""""""""""""""""""""""""""""

要重放多个 bag，请使用新的 ``-i, --input`` CLI 选项：

.. code-block:: console

    $ ros2 bag play -i bag1 -i bag2 -i bag3 [storage_id]

有关更多信息，请参见 https://github.com/ros2/rosbag2/pull/1848。

添加了基于消息发布时间戳按时间顺序重放消息的支持
""""""""""""""""""""""""""""""""""""""""""""""""

这通过 ``ros2 bag play`` 的新的 ``--message-order {received,sent}`` 选项暴露。
默认行为是按接收顺序播放消息。

有关更多信息，请参见 https://github.com/ros2/rosbag2/pull/1876。

使快照写入在每次触发时写入一个新文件
""""""""""""""""""""""""""""""""""""

有关更多细节，请参见 https://github.com/ros2/rosbag2/pull/1842。

``ros2 bag info`` 命令中的新 ``--sort`` CLI 选项
""""""""""""""""""""""""""""""""""""""""""""""""

有了新的 ``--sort`` CLI 选项，用户将能够按名称、话题类型或已录制消息数量对话题、服务和动作进行排序。

有关更多细节，请参见 https://github.com/ros2/rosbag2/pull/1804。

使用 ``ros2 bag info`` 显示每个话题的大小占比
"""""""""""""""""""""""""""""""""""""""""""""

有了新的 ``--size-contribution`` 选项以及 ``ros2 bag info -v``，用户将能够看到 bag 文件中每个话题的大小占比。

有关更多信息，请参见 https://github.com/ros2/rosbag2/pull/1726。

为 ``ros2 bag play`` 和 ``ros2 bag record`` 添加了 ``--log-level`` 选项，以允许打印调试消息
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

有关更多细节，请参见 https://github.com/ros2/rosbag2/pull/1625。

``rosidl_rust``
^^^^^^^^^^^^^^^

添加了 ``rosidl_rust``
""""""""""""""""""""""

一个 Rust idl 生成器被添加到了默认代码生成器列表中。

有关更多细节，请参见 https://github.com/ros2/ros2/pull/1674。

``ros2``
^^^^^^^^

Windows 切换到使用 Pixi/Conda
"""""""""""""""""""""""""""""

这使得可以轻松管理依赖，并在未来更新它们。
安装过程被显著简化。
安装依赖不再是几十个步骤，而只是几条命令。
更新依赖也容易得多。
依赖安装在各个工作区中，没有“全局”安装。

有关更多细节，请参见 https://github.com/ros2/ci/pull/802 和 https://github.com/ros2/ros2/pull/1642。
访问 :doc:`Windows 源码安装说明 <../Installation/Alternatives/Windows-Development-Setup>` 以在 Windows 上安装它。

支持 DDS 话题中的话题实例
"""""""""""""""""""""""""

话题实例是一种在相同资源（即话题）上复用同一逻辑类型的多个对象更新传输的方式。

有关更多信息，请参见 https://github.com/ros2/ros2/issues/1538。
你还可以查看文档：https://github.com/ros2/design/pull/340/files。

自 Jazzy 版本以来的变更
-----------------------

``common_interfaces``
^^^^^^^^^^^^^^^^^^^^^

将 NV12 添加到像素格式
""""""""""""""""""""""

将 NV12 添加到像素格式，这是硬件加速解码器的常见输出格式。

有关更多细节，请参见 https://github.com/ros2/common_interfaces/pull/253。

``rclcpp``
^^^^^^^^^^

Subordinate 节点的一致行为
""""""""""""""""""""""""""

修复了 subordinate 节点不一致的行为。
Subordinate 节点是与主节点关联的次级节点，它与主节点共享相同的底层上下文和资源，同时保持独立的名称和命名空间。
行为修改可能会影响依赖先前实现的现有应用程序：

1. 从 subordinate 节点创建的泛型客户端现在正确地遵循 subordinate 节点的子命名空间
2. 使用 subordinate 节点获取的参数现在正确地使用（父）节点的 ``rclcpp::node_interfaces::NodeParametersInterface``

有关更多细节，请参见 https://github.com/ros2/rclcpp/pull/2822。

``rmw_connextdds_cpp``
^^^^^^^^^^^^^^^^^^^^^^

版本升级到 7.3
""""""""""""""

RTI Connext DDS 版本升级到 7.3.0。

有关更多细节，请参见 https://github.com/ros2/ci/pull/811。

``Connextmicro``
^^^^^^^^^^^^^^^^

弃用 Connextmicro
"""""""""""""""""

RTI Connext Micro RMW 软件包 ``rmw_connextddsmicro`` 将在 Kilted Kaiju 中停止接收更新，并在未来的 ROS 2 版本中被移除。

有关更多信息，请参见 https://github.com/ros2/rmw_connextdds/pull/182。

``rosidl_dynamic_typesupport``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

移除对 float128 的支持
""""""""""""""""""""""

移除了对 float128 的支持，因为其定义存在不一致。

有关更多细节，请参见 https://github.com/ros2/rosidl_dynamic_typesupport/issues/11。

``rmw_fastrtps_cpp``
^^^^^^^^^^^^^^^^^^^^

将软件包从 fastrtps 重命名为 fastdds
""""""""""""""""""""""""""""""""""""

``fastrtps`` 已重命名为 ``fastdds``。
rmw 实现的名称保持不变。
XML Profile 环境变量字符串将发生变化。

有关更多细节，请参见 https://github.com/ros2/ros2/pull/1641。

ament_target_dependencies 已弃用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CMake 宏 ``ament_target_dependencies()`` 已弃用，取而代之的是使用现代 CMake 目标的 ``target_link_libraries()``。
该宏仍然有效，但会在构建时发出类似如下的 CMake 弃用警告：

.. code-block::

    CMake Deprecation Warning at [...]/ament_cmake_target_dependencies/share/ament_cmake_target_dependencies/cmake/ament_target_dependencies.cmake:89 (message):
    ament_target_dependencies() is deprecated.  Use target_link_libraries()
    with modern CMake targets instead.  Try replacing this call with:

        target_link_libraries([...] PUBLIC
        [...]
        )

请尝试将 ``ament_target_dependencies()`` 调用替换为警告所建议的 ``target_link_libraries()`` 调用。

有关更多信息，请参见 `ament/ament_cmake#572 <https://github.com/ament/ament_cmake/pull/572>`__ 和 `ament/ament_cmake#292 <https://github.com/ament/ament_cmake/issues/292>`__。

``launch``
^^^^^^^^^^

``PathJoinSubstitution``
""""""""""""""""""""""""

``PathJoinSubstitution`` 现在支持将字符串或替换拼接为单个路径组件。
例如：

.. code-block:: python

    PathJoinSubstitution(['robot_description', 'urdf', [LaunchConfiguration('model'), '.xacro']])

如果 ``model`` 启动配置被设置为 ``my_model``，这将得到一个等于以下内容的路径：

.. code-block:: python

    'robot_description/urdf/my_model.xacro'

有关更多信息，请参见 `ros2/launch#835 <https://github.com/ros2/launch/issues/835>`__ 和 `ros2/launch#838 <https://github.com/ros2/launch/pull/838>`__。

``rmw_zenoh_cpp``
^^^^^^^^^^^^^^^^^

``Tier 1``
""""""""""

``rmw_zenoh_cpp`` 现在被视为 Tier 1。
在 ROS 2 核心软件包中有许多 PR（在 `ros2/rmw_zenoh#265 <https://github.com/ros2/rmw_zenoh/issues/265>`__ 中总结），例如：

  * 使 rmw 通过所有核心测试。
  * 实现并记录安全性
  * 使其在 Tier 1 平台上工作。
  * 添加了质量声明
  * 添加到 REP 2005
  * 一个专用的 nightly CI 任务
  * 以及其他

有关更多信息，请参见 https://github.com/ros2/rmw_zenoh/issues/265。

开发进展
--------

有关 Kilted Kaiju 的开发进展，请参见 `此项目看板 <https://github.com/orgs/ros2/projects/63>`__。

有关 Kilted Kaiju 所遵循的总体流程，请参见 :doc:`流程说明页面 <Release-Process>`。

发布时间线
----------

    2024 年 12 月 - 平台决策
        REP 2000 更新了目标平台和主要依赖版本。

    2025 年 4 月 7 日（周一）- Alpha + RMW 冻结
        ROS Base [1]_ 软件包的初步测试与稳定，以及 RMW 提供方软件包的 API 和功能冻结。

    2025 年 4 月 14 日（周一）- 冻结
        Rolling Ridley 中 ROS Base [1]_ 软件包的 API 和功能冻结。
        此后只应发布缺陷修复版本。
        新软件包可以独立发布。

    2025 年 4 月 21 日（周一）- 分支
        从 Rolling Ridley 分支。
        ``rosdistro`` 重新对 ROS Base [1]_ 软件包的 Rolling PR 开放。
        Kilted 开发从 ``ros-rolling-*`` 软件包转移到 ``ros-kilted-*`` 软件包。

    2025 年 4 月 28 日（周一）- Beta
        ROS Desktop [2]_ 软件包的更新版本可用。
        呼吁进行一般性测试。

    2025 年 5 月 1 日（周四）- Tutorial Party 启动
        托管在 https://github.com/ros2/kilted_tutorial_party 的教程开放社区测试。

    2025 年 5 月 12 日（周一）- 候选版本
        候选版本软件包已构建。
        ROS Desktop [2]_ 软件包的更新版本可用。

    2025 年 5 月 19 日（周一）- 发行版冻结
        冻结所有 `ROS 2 桌面软件包 <https://reps.openrobotics.org/rep-2001/#kilted-kaiju-may-2025-november-2026>`__ 和 ``rosdistro`` 上的所有 Kilted 分支。
        任何 ``kilted`` 分支或 ``rosdistro`` 仓库中针对 ``kilted/distribution.yaml`` 的 pull request 都不会被合并。

    2025 年 5 月 23 日（周五）- 正式发布
        发布公告。
        `ROS 2 桌面软件包 <https://reps.openrobotics.org/rep-2001/#kilted-kaiju-may-2025-november-2026>`__ 源码冻结解除，``rosdistro`` 重新对 Kilted pull request 开放。

.. [1] ``ros_base`` 变体在 `REP 2001 (ros-base) <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中有描述。
.. [2] ``desktop`` 变体在 `REP 2001 (desktop-variants) <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中有描述。
