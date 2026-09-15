.. _kilted-release:

Kilted Kaiju（代号 ``kilted``；2025 年 5 月）
=============================================

.. toctree::
   :hidden:

   Kilted-Kaiju-Complete-Changelog

.. contents:: 目录
   :depth: 2
   :local:

*Kilted Kaiju* 是 ROS 2 的第十一个发行版。
以下内容介绍了自上一个发行版以来 Kilted Kaiju 中的重要变更和新特性。
自 Jazzy 以来的全部变更列表，请参阅 :doc:`完整变更日志 <Kilted-Kaiju-Complete-Changelog>`

支持的平台
----------

根据 `平台支持层级 <../The-ROS2-Project/Platform-Support-Tiers>`，Kilted Kaiju 支持以下平台：

Tier 1 平台：

* Ubuntu 24.04 (Noble)：``amd64`` 和 ``arm64``
* Windows 10 (Visual Studio 2019)：``amd64``

Tier 2 平台：

* RHEL 9：``amd64``

Tier 3 平台：

* macOS：``amd64``
* Debian Bookworm：``amd64``

目标平台：

+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+
| Architecture | Ubuntu Noble      | Windows 10    | RHEL 9            | macOS     | Debian Bookworm | OpenEmbedded / |
|              | (24.04)           | (VS2019)      |                   |           | (12)            | Yocto Project  |
+==============+===================+===============+===================+===========+=================+================+
| amd64        | Tier 1 [d][a][s]  | Tier 1 [a][s] | Tier 2 [d][a][s]  | Tier 3 [s]| Tier 3 [s]      | Tier 3 [s]     |
+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+
| arm64        | Tier 1 [d][a][s]  |               |                   |           | Tier 3 [s]      | Tier 3 [s]     |
+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+
| arm32        | Tier 3 [s]        |               |                   |           | Tier 3 [s]      | Tier 3 [s]     |
+--------------+-------------------+---------------+-------------------+-----------+-----------------+----------------+

以下指标说明了每个平台可用的交付机制。

\" \[d\] \" 将为提交到 rosdistro 的软件包提供平台特定的（Debian、RPM 等）软件包。

\" \[a\] \" 以每个平台一个压缩包的形式提供二进制发行包，其中包含 Jazzy ROS 2 repos 文件中的所有软件包[^14]。

\" \[s\] \" 从源码编译。

中间件实现支持：

+---------------------------+-------------------------+---------------+----------------------------+-------------------------------+
| Middleware Library        | Middleware Provider     | Support Level | Platforms                  | Architectures                 |
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

中间件实现支持取决于平台支持层级。例如，Tier 2 平台上的 Tier 1 中间件实现只能获得 Tier 2 级别的支持。

最低语言要求：

- C++17
- Python 3.9

依赖要求：

+---------------+-------------------------------+-------------------------------------------------------------+
|               | Required Support              | Recommended Support                                         |
+===============+===============+===============+==========+==========+==================+====================+
| Package       | Ubuntu Noble  | Windows 10**  | RHEL 9   | macOS**  | Debian Bookworm  | OpenEmbedded**     |
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
|                               | **Linux only**                                                              |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| PCL           | 1.14.0        | N/A           | 1.12.0   | 1.14.1   | 1.13.0           | 1.10.0             |
+---------------+---------------+---------------+----------+----------+------------------+--------------------+
| **RMW Middleware**                                                                                          |
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

\" \* \" 表示这不是上游版本（即官方操作系统仓库中提供的版本），而是由 OSRF 或社区发行的软件包（在自定义仓库上构建并分发的软件包）。

\" \*\* \" 表示该依赖可能会经历多个版本变更，因为该依赖使用的包管理器会持续更新，而没有稳定的 API。

\" \*\*\* \" webOS OSE 提供此不同版本。

本文档仅记录 ROS 发行版首次发布时的版本，不会随依赖的演进而更新。
因此这些版本是一个最低水位线。

依赖使用的包管理器：

- Ubuntu、Debian：apt、pip
- Windows：pixi/conda、pip
- macOS：Homebrew、pip
- RHEL：dnf
- OpenEmbedded：opkg

构建系统支持：

- ament_cmake
- cargo
- cmake
- setuptools

安装
----

`安装 Kilted Kaiju <../../kilted/Installation.html>`__

支持的 Gazebo 发行版
--------------------
对于 Kilted Kaiju，推荐的 Gazebo 发行版是 `Ionic <https://gazebosim.org/docs/ionic/ros_installation>`__。

此 ROS 2 发行版中的新特性
-------------------------

``ament_cmake_ros``
^^^^^^^^^^^^^^^^^^^

新增 rmw_test_fixture 以支持 RMW 隔离测试
"""""""""""""""""""""""""""""""""""""""""

新增了两个软件包，提供了一种可扩展的机制，用于创建基于 RMW 的通信隔离测试夹具。
它紧密参照 rmw 和 rmw_implementation API 建模。

``rmw_test_fixture`` 软件包目前仅提供 API，RMW 提供方可以实现它，以便为待运行的测试配置其 RMW。

``rmw_test_fixture_implementation`` 软件包提供了用于发现、加载和调用相应扩展的入口点。

更多详情请参阅 https://github.com/ros2/ament_cmake_ros/pull/21。

``common_interfaces``
^^^^^^^^^^^^^^^^^^^^^

新增 nav_msgs/Goals 消息
""""""""""""""""""""""""

引入了一种新的消息类型 {interface(nav_msgs/msg/Goals)}，用于在 nav_msgs 软件包中支持导航目标数组。

更多详情请参阅 https://github.com/ros2/common_interfaces/pull/269。

``ros2cli``
^^^^^^^^^^^

动作内省
""""""""

这允许通过命令行内省动作。
使用 ``ros2cli`` 工具：``ros2 action echo <action name>``。

更多信息请参阅 https://github.com/ros2/ros2cli/pull/978。

``rclcpp``
^^^^^^^^^^

动作通用客户端
""""""""""""""

支持动作通用客户端，它用于在 rosbag2 中支持动作。

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2759。

``rclpy``
^^^^^^^^^

静态类型检查
""""""""""""

为 ``ActionClient`` 和 ``ActionServer`` 添加了静态类型提示。

更多详情请参阅 https://github.com/ros2/rclpy/pull/1349。

在 ``pub/sub/client/server/actions``、``Future/Task`` 和 ``Parameter`` 中添加对 `泛型 <https://typing.python.org/en/latest/reference/generics.html>`_ 的支持。

``Publisher``、``Subscription``、``Server``、``Task`` 和 ``Parameter`` 无需任何更新即可添加对泛型的支持。

``Client`` 则需要按如下方式更新，才能获得改进后的类型检查。

.. code-block:: python

    self._get_parameter_client: Client[GetParameters.Request,
                                       GetParameters.Response] = self.node.create_client(
                                        GetParameters, '/get_parameters',
                                        qos_profile=qos_profile, callback_group=callback_group)

``ActionClient`` 则需要按如下方式更新，才能获得改进后的类型检查。

.. code-block:: python

    ac: ActionClient[Fibonacci.Goal,
                     Fibonacci.Result,
                     Fibonacci.Feedback] = ActionClient(self.node, Fibonacci, 'fibonacci')

``Future`` 则需要按如下方式更新，才能获得改进后的类型检查。

.. code-block:: python

    log_msgs_future: Future[bool] = Future()

更多详情请参阅 https://github.com/ros2/rclpy/pull/1239、https://github.com/ros2/rclpy/pull/1275、https://github.com/ros2/rclpy/pull/1246 和 https://github.com/ros2/rclpy/pull/1254/files。

此外还对整个 ``rclpy`` 做了各种其他小的改进和修正。

可以使用封装了 `mypy <https://www.mypy-lang.org/>`_ 的 `ament_mypy <https://github.com/ament/ament_lint/tree/kilted/ament_mypy>`_ 对 Python 类型进行静态检查。

EventsExecutor
""""""""""""""

为 ``rclpy`` 支持实验性的事件执行器，它是对原始 ``rclcpp`` 事件执行器概念的移植。

更多详情请参阅 https://github.com/ros2/rclpy/pull/1391。

``Rosbag2``
^^^^^^^^^^^

Rosbag2 动作内省支持
""""""""""""""""""""

允许从 rosbag 中记录和播放动作。

更多信息请参阅 https://github.com/ros2/rosbag2/pull/1955。
设计文档 https://github.com/ros2/rosbag2/pull/1928。

``ros2 bag play`` 的进度条
""""""""""""""""""""""""""

为 ``ros2 bag play`` CLI 添加了进度条，显示包时间和时长，与 ROS 1 中的体验类似。

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1836。

新增使用 ``ros2 bag play`` CLI 重放多个包的支持
"""""""""""""""""""""""""""""""""""""""""""""""

要重放多个包，请使用新的 ``-i, --input`` CLI 选项：

.. code-block:: console

    $ ros2 bag play -i bag1 -i bag2 -i bag3 [storage_id]

更多信息请参阅 https://github.com/ros2/rosbag2/pull/1848。

新增按其发布时间戳按时间顺序重放消息的支持
""""""""""""""""""""""""""""""""""""""""""

这通过 ``ros2 bag play`` 的新 ``--message-order {received,sent}`` 选项提供。
默认行为是按消息接收顺序播放。

更多信息请参阅 https://github.com/ros2/rosbag2/pull/1876。

每次触发快照时写入新文件
""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1842。

``ros2 bag info`` 命令新增 ``--sort`` CLI 选项
""""""""""""""""""""""""""""""""""""""""""""""

使用新的 ``--sort`` CLI 选项，用户可以按名称、话题类型或记录的消息数量对话题、服务和动作进行排序。

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1804。

使用 ``ros2 bag info`` 显示每个话题的大小占比
"""""""""""""""""""""""""""""""""""""""""""""

使用新的 ``--size-contribution`` 选项并结合 ``ros2 bag info -v``，用户可以查看 bag 文件中每个话题的大小占比。

更多信息请参阅 https://github.com/ros2/rosbag2/pull/1726。

为 ``ros2 bag play`` 和 ``ros2 bag record`` 添加 ``--log-level`` 选项，以允许输出调试消息
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

更多详情请参阅 https://github.com/ros2/rosbag2/pull/1625。

``rosidl_rust``
^^^^^^^^^^^^^^^

Added ``rosidl_rust``
"""""""""""""""""""""

在默认代码生成器列表中新增了一个 Rust IDL 生成器。

更多详情请参阅 https://github.com/ros2/ros2/pull/1674。

``ros2``
^^^^^^^^

Windows 改用 Pixi/Conda
"""""""""""""""""""""""

这样可以轻松管理依赖并日后更新它们。
安装过程得到了显著简化。
无需几十个安装依赖的步骤，只需几条命令。
更新依赖也变得容易得多。
依赖安装在各自独立的工作空间中，没有“全局”安装。

更多详情请参阅 https://github.com/ros2/ci/pull/802 和 https://github.com/ros2/ros2/pull/1642。
请访问 :doc:`Windows 源码安装说明 <../Installation/Alternatives/Windows-Development-Setup>` 在 Windows 上安装它。

支持 DDS 话题中的话题实例
"""""""""""""""""""""""""

话题实例是一种将同一逻辑类型的多个对象的更新复用到同一资源（即话题）上传输的方式。

更多信息请参阅 https://github.com/ros2/ros2/issues/1538。
你也可以查看相关文档：https://github.com/ros2/design/pull/340/files。

自 Jazzy 发行版以来的变更
-------------------------

``common_interfaces``
^^^^^^^^^^^^^^^^^^^^^

为像素格式新增 NV12
"""""""""""""""""""

新增了 NV12 像素格式，它是硬件加速解码器的一种常见输出格式。

更多详情请参阅 https://github.com/ros2/common_interfaces/pull/253。

``rclcpp``
^^^^^^^^^^

从属节点行为一致化
""""""""""""""""""

修复了从属节点行为不一致的问题。
从属节点是与主节点关联的次级节点，它共享相同的底层上下文和资源，同时保持独立的名称和命名空间。
该行为变更可能会影响依赖先前实现的现有应用：

1. 由从属节点创建的通用客户端现在会正确地遵循从属节点的子命名空间
2. 使用从属节点获取的参数现在会正确地使用（父）节点的 ``rclcpp::node_interfaces::NodeParametersInterface``

更多详情请参阅 https://github.com/ros2/rclcpp/pull/2822。

``rmw_connextdds_cpp``
^^^^^^^^^^^^^^^^^^^^^^

版本升级到 7.3
""""""""""""""

RTI Connext DDS 版本升级到 7.3.0。

更多详情请参阅 https://github.com/ros2/ci/pull/811。

``Connextmicro``
^^^^^^^^^^^^^^^^

弃用 Connextmicro
"""""""""""""""""

RTI Connext Micro RMW 软件包 ``rmw_connextddsmicro`` 将在 Kilted Kaiju 中停止接收更新，并在未来的 ROS 2 发行版中被移除。

更多信息请参阅 https://github.com/ros2/rmw_connextdds/pull/182。

``rosidl_dynamic_typesupport``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

移除对 float128 的支持
""""""""""""""""""""""

由于定义存在不一致，已移除对 float128 的支持。

更多详情请参阅 https://github.com/ros2/rosidl_dynamic_typesupport/issues/11。

``rmw_fastrtps_cpp``
^^^^^^^^^^^^^^^^^^^^

将软件包从 fastrtps 重命名为 fastdds
""""""""""""""""""""""""""""""""""""

``fastrtps`` 已重命名为 ``fastdds``。
rmw 实现的名称保持不变。
XML Profile ENV 字符串将会变更。

更多详情请参阅 https://github.com/ros2/ros2/pull/1641。

``ament_target_dependencies`` 已弃用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CMake 宏 ``ament_target_dependencies()`` 已被弃用，建议改为使用配合现代 CMake 目标的 ``target_link_libraries()``。
该宏仍然可用，但在构建时会像下面这样发出 CMake 弃用警告：

.. code-block::

    CMake Deprecation Warning at [...]/ament_cmake_target_dependencies/share/ament_cmake_target_dependencies/cmake/ament_target_dependencies.cmake:89 (message):
    ament_target_dependencies() is deprecated.  Use target_link_libraries()
    with modern CMake targets instead.  Try replacing this call with:

        target_link_libraries([...] PUBLIC
        [...]
        )

请尝试按警告的建议，用 ``target_link_libraries()`` 调用替换 ``ament_target_dependencies()`` 调用。

更多信息请参阅 `ament/ament_cmake#572 <https://github.com/ament/ament_cmake/pull/572>`__ 和 `ament/ament_cmake#292 <https://github.com/ament/ament_cmake/issues/292>`__。

``launch``
^^^^^^^^^^

``PathJoinSubstitution``
""""""""""""""""""""""""

``PathJoinSubstitution`` 现在支持将字符串或替换拼接为单个路径组成部分。
例如：

.. code-block:: python

    PathJoinSubstitution(['robot_description', 'urdf', [LaunchConfiguration('model'), '.xacro']])

如果 ``model`` launch 配置被设置为 ``my_model``，则得到的路径等于：

.. code-block:: python

    'robot_description/urdf/my_model.xacro'

更多信息请参阅 `ros2/launch#835 <https://github.com/ros2/launch/issues/835>`__ 和 `ros2/launch#838 <https://github.com/ros2/launch/pull/838>`__。

``rmw_zenoh_cpp``
^^^^^^^^^^^^^^^^^

``Tier 1``
""""""""""

``rmw_zenoh_cpp`` 现在被视为 Tier 1。
ROS 2 核心软件包中有许多 pull request（汇总于 `ros2/rmw_zenoh#265 <https://github.com/ros2/rmw_zenoh/issues/265>`__），例如：

  * 让该 rmw 通过所有核心测试。
  * 实现并文档化安全性
  * 使其在 Tier 1 平台上可用。
  * 添加质量声明
  * 加入 REP 2005
  * 专门的每夜 CI 任务
  * 以及其他方面

更多信息请参阅 https://github.com/ros2/rmw_zenoh/issues/265。

开发进展
--------

有关 Kilted Kaiju 开发进展，请参阅 `此项目面板 <https://github.com/orgs/ros2/projects/63>`__。

有关 Kilted Kaiju 所遵循的整体流程，请参阅 :doc:`流程说明页面 <Release-Process>`。

发行时间线
----------

    2024 年 12 月 - 平台决策
        REP 2000 更新了目标平台和主要依赖项的版本。

    2025 年 4 月 7 日（周一）- Alpha + RMW 冻结
        对 ROS Base [1]_ 软件包进行初步测试和稳定化，并冻结 RMW 提供者软件包的 API 和特性。

    2025 年 4 月 14 日（周一）- 冻结
        冻结 Rolling Ridley 中 ROS Base [1]_ 软件包的 API 和特性。
        此后只应进行缺陷修复版本发布。
        新软件包可以独立发布。

    2025 年 4 月 21 日（周一）- 分支
        从 Rolling Ridley 分支。
        ``rosdistro`` 对 ROS Base [1]_ 软件包的 Rolling PR 重新开放。
        Kilted 开发从 ``ros-rolling-*`` 软件包转向 ``ros-kilted-*`` 软件包。

    2025 年 4 月 28 日（周一）- Beta
        ROS Desktop [2]_ 软件包的更新版本可用。
        呼吁进行广泛测试。

    2025 年 5 月 1 日（周四）- 教程活动启动
        托管在 https://github.com/ros2/kilted_tutorial_party 的教程开放供社区测试。

    2025 年 5 月 12 日（周一）- 候选发行版
        构建候选发行版软件包。
        ROS Desktop [2]_ 软件包的更新版本可用。

    2025 年 5 月 19 日（周一）- 发行版冻结
        冻结所有 `ROS 2 desktop packages <https://reps.openrobotics.org/rep-2001/#kilted-kaiju-may-2025-november-2026>`__ 上的所有 Kilted 分支以及 ``rosdistro``。
        不会合并 ``rosdistro`` 仓库中针对任何 ``kilted`` 分支或针对 ``kilted/distribution.yaml`` 的 PR。

    2025 年 5 月 23 日（周五）- 正式发布
        发布公告。
        `ROS 2 desktop packages <https://reps.openrobotics.org/rep-2001/#kilted-kaiju-may-2025-november-2026>`__ 源码冻结解除，``rosdistro`` 对 Kilted PR 重新开放。

.. [1] ``ros_base`` 变体在 `REP 2001 (ros-base) <https://reps.openrobotics.org/rep-2001/#ros-base>`_ 中描述。
.. [2] ``desktop`` 变体在 `REP 2001 (desktop-variants) <https://reps.openrobotics.org/rep-2001/#desktop-variants>`_ 中描述。
