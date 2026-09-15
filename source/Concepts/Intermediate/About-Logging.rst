.. redirect-from::

    Logging
    Concepts/About-Logging

日志与日志器配置
================

.. contents:: 目录
   :local:

概述
----

ROS 2 中的日志子系统旨在将日志消息发送到多种目标，包括：

* 控制台（如果连接了控制台）
* 磁盘日志文件（如果本地存储可用）
* ROS 2 网络中的 ``/rosout`` 主题

默认情况下，ROS 2 节点中的日志消息会同时输出到控制台（stderr）、磁盘日志文件，以及 ROS 2 网络中的 ``/rosout`` 主题。
这些目标可以按节点逐个启用或禁用。

本文档其余部分将介绍日志子系统背后的一些设计思路。

严重级别
--------

日志消息都带有一个严重级别：``DEBUG``、``INFO``、``WARN``、``ERROR`` 或 ``FATAL``，按升序排列。

日志器只会处理严重级别等于或高于其设置级别的日志消息。

每个节点都有一个与之关联的日志器，日志器名会自动包含节点的名称和命名空间。
如果节点名称被外部重映射为与源代码中定义不同的名称，那么日志器名称也会反映这一点。
也可以创建非节点日志器，并为其指定特定名称。

日志器名称表示层次结构。
如果名为 "abc.def" 的日志器级别未设置，它会继承其父级日志器 "abc" 的级别；如果父级级别也未设置，则使用默认日志器级别。
当日志器 "abc" 的级别发生变化时，所有其后代（例如 "abc.def"、"abc.ghi.jkl"）都会受到影响，除非它们已经显式设置了自己的级别。

API
---

以下是 ROS 2 日志基础设施的终端用户应使用的 API，按客户端库分组。

.. tabs::

  .. group-tab:: C++

    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}`` - 每当代码执行到该行时，输出给定的 printf 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_ONCE`` - 仅在第一时间输出给定的 printf 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_EXPRESSION`` - 仅在给定表达式为真时输出给定的 printf 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_FUNCTION`` - 仅在给定函数返回真时输出给定的 printf 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_SKIPFIRST`` - 除第一次外，输出给定的 printf 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_THROTTLE`` - 每隔给定速率（以整数毫秒为单位）最多输出一次给定的 printf 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_SKIPFIRST_THROTTLE`` - 除第一条外，每隔给定速率最多输出一次给定的 printf 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_STREAM`` - 每当代码执行到该行时，输出给定的 C++ stream 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_STREAM_ONCE`` - 仅在第一次执行该行时输出给定的 C++ stream 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_STREAM_EXPRESSION`` - 仅在给定表达式为真时输出给定的 C++ stream 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_STREAM_FUNCTION`` - 仅在给定函数返回真时输出给定的 C++ stream 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_STREAM_SKIPFIRST`` - 除第一次外，输出给定的 C++ stream 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_STREAM_THROTTLE`` - 每隔给定速率（以整数毫秒为单位）最多输出一次给定的 C++ stream 风格消息
    * ``RCLCPP_{DEBUG,INFO,WARN,ERROR,FATAL}_STREAM_SKIPFIRST_THROTTLE`` - 每隔给定速率最多输出一次给定的 C++ stream 风格消息，但跳过第一条

    上述每个 API 都接受一个 ``rclcpp::Logger`` 对象作为第一个参数。
    可以通过节点 API 调用 ``node->get_logger()`` 获取它（建议这样做），或者构造一个独立的 ``rclcpp::Logger`` 对象。

    * ``rcutils_logging_set_logger_level`` - 为特定日志器名称设置给定严重级别
    * ``rcutils_logging_get_logger_effective_level`` - 给定日志器名称，返回该日志器级别（可能未设置）

  .. group-tab:: Python

    * ``logger.{debug,info,warning,error,fatal}`` - 向日志基础设施输出给定的 Python 字符串。
      这些调用接受以下关键字参数来控制行为：

      * ``throttle_duration_sec`` - 如果不是 ``None``，表示节流间隔的持续时间（浮点秒）
      * ``skip_first`` - 如果为 ``True``，则除了第一次外输出消息
      * ``once`` - 如果为 ``True``，则仅在第一次输出消息

    * ``rclpy.logging.set_logger_level`` - 为特定日志器名称设置给定严重级别
    * ``rclpy.logging.get_logger_effective_level`` - 给定日志器名称，返回该日志器级别（可能未设置）

配置
----

由于 ``rclcpp`` 和 ``rclpy`` 使用相同的底层日志基础设施，因此配置选项也相同。

环境变量
^^^^^^^^

以下环境变量控制 ROS 2 日志器的部分行为。
请注意，每个环境设置都是进程级设置，适用于该进程中的所有节点。

* ``ROS_LOG_DIR`` - 控制写入日志消息到磁盘时使用的日志目录（如果启用）。
  若非空，使用该环境变量指定的目录。
  若为空，则使用 ``ROS_HOME`` 环境变量构造路径 ``$ROS_HOME/.log``。
  在所有情况下，``~`` 字符都会展开为用户的 HOME 目录。
* ``ROS_HOME`` - 控制各种 ROS 文件（包括日志与配置文件）的主目录。
  在日志上下文中，此变量用于构造日志文件目录路径。
  若非空，使用该变量的内容作为 ``ROS_HOME`` 路径。
  在所有情况下，``~`` 字符都会展开为用户的 HOME 目录。
* ``RCUTILS_LOGGING_USE_STDOUT`` - 控制消息输出到哪个流。
  若未设置或为 0，则使用 stderr。
  若为 1，则使用 stdout。
* ``RCUTILS_LOGGING_BUFFERED_STREAM`` - 控制日志流（由 ``RCUTILS_LOGGING_USE_STDOUT`` 配置）是按行缓冲还是无缓冲。
  若未设置，使用流默认方式（通常 stdout 为行缓冲，stderr 为无缓冲）。
  若为 0，则强制使用无缓冲。
  若为 1，则强制使用行缓冲。
* ``RCUTILS_COLORIZED_OUTPUT`` - 控制输出消息时是否使用颜色。
  若未设置，则基于平台和终端是否为 TTY 自动判定。
  若为 0，则强制禁用颜色输出。
  若为 1，则强制启用颜色输出。
* ``RCUTILS_CONSOLE_OUTPUT_FORMAT`` - 控制每条日志消息输出哪些字段。
  可用字段包括：

  * ``{severity}`` - 严重级别。
  * ``{name}`` - 日志器名称（可能为空）。
  * ``{message}`` - 日志消息（可能为空）。
  * ``{function_name}`` - 调用此函数的函数名（可能为空）。
  * ``{file_name}`` - 调用此函数的文件名（可能为空）。
  * ``{time}`` - 自纪元以来的秒数。
  * ``{time_as_nanoseconds}`` - 自纪元以来的纳秒数。
  * ``{line_number}`` - 调用此行的行号（可能为空）。

  若未给出格式，默认值为 ``[{severity}] [{time}] [{name}]: {message}``。


节点创建
^^^^^^^^

在初始化 ROS 2 节点时，可以通过节点选项控制部分行为。
由于这些配置是按节点选项设置的，因此即使多个节点组合在一个进程中，也可以分别设置。

* ``log_levels`` - 在特定节点中使用的组件日志级别。
  可通过如下方式设置：``ros2 run demo_nodes_cpp talker --ros-args --log-level talker:=DEBUG``
* ``external_log_config_file`` - 用于配置后端日志器的外部文件。
  如果为 NULL，则使用默认配置。
  请注意，此文件格式依赖后端日志器（当前默认后端日志器 spdlog 尚未实现）。
  可通过以下方式设置：``ros2 run demo_nodes_cpp talker --ros-args --log-config-file log-config.txt``
* ``log_stdout_disabled`` - 是否禁用将日志消息写入控制台。
  可通过以下方式设置：``ros2 run demo_nodes_cpp talker --ros-args --disable-stdout-logs``
* ``log_rosout_disabled`` - 是否禁用将日志消息写入 ``/rosout``。
  这会显著节省网络带宽，但外部观察者将无法监控日志。
  可通过以下方式设置：``ros2 run demo_nodes_cpp talker --ros-args --disable-rosout-logs``
* ``log_ext_lib_disabled`` - 是否完全禁用外部日志器。
  这有时会更快，但意味着日志将不会写入磁盘。
  可通过以下方式设置：``ros2 run demo_nodes_cpp talker --ros-args --disable-external-lib-logs``

日志子系统设计
--------------

下图展示了日志子系统的五个主要组成部分以及它们之间的交互方式。

.. figure:: ../images/ros2_logging_architecture.png
   :alt: ROS 2 logging architecture
   :width: 550px
   :align: center

rcutils
^^^^^^^

``rcutils`` 具有日志实现，可以按照某种格式（见上文 ``配置``）格式化日志消息，并将这些日志消息输出到控制台。
``rcutils`` 实现了完整的日志解决方案，但允许高层组件以依赖注入模型插入日志基础设施。
当我们谈论下面的 ``rcl`` 层时，这一点会更加明显。

请注意，这是一个 *进程级* 日志实现，因此在此层配置任何内容都会影响整个进程，而不只是单个节点。

rcl_logging_spdlog
^^^^^^^^^^^^^^^^^^

``rcl_logging_spdlog`` 实现了 ``rcl_logging_interface`` API，因此为 ``rcl`` 层提供外部日志服务。
特别地，``rcl_logging_spdlog`` 实现会将格式化后的日志消息写入磁盘日志文件，使用 ``spdlog`` 库，默认路径通常位于 ``~/.ros/log`` （这可以配置；见上文 ``配置``）。

rcl
^^^

``rcl`` 中的日志子系统使用 ``rcutils`` 和 ``rcl_logging_spdlog`` 来提供 ROS 2 日志服务的主要部分。
当日志消息传入时，``rcl`` 决定把日志消息发送到哪里。
日志消息可以有 3 个主要投递位置；一个节点可以启用其任意组合：

* 通过 ``rcutils`` 层发送到控制台
* 通过 ``rcl_logging_spdlog`` 层写入磁盘
* 通过 RMW 层发送到 ROS 2 网络中的 ``/rosout`` 主题

rclcpp
^^^^^^

这是 ROS 2 的主要 C++ API，位于 ``rcl`` API 之上。
在日志上下文中，``rclcpp`` 提供 ``RCLCPP_`` 日志宏；请参见上文 ``API`` 中的完整列表。
当某个 ``RCLCPP_`` 宏执行时，会检查节点当前严重级别与宏严重级别的比较关系。
若宏严重级别大于等于节点严重级别，消息会被格式化并输出到所有当前配置的目标位置。
注意 ``rclcpp`` 在日志调用时使用全局互斥锁，因此同一进程中的所有日志调用都变成单线程方式。


rclpy
^^^^^

这是 ROS 2 的主要 Python API，位于 ``rcl`` API 之上。
在日志上下文中，``rclpy`` 提供 ``logger.debug`` 风格函数；请参见上文 ``API`` 中的完整列表。
当某个 ``logger.debug`` 函数执行时，会检查节点当前严重级别与宏严重级别的比较关系。
如果宏严重级别大于等于节点严重级别，消息会格式化并输出到所有当前配置的目标位置。


日志使用
--------

.. tabs::

  .. group-tab:: C++

    * 参考 `rclcpp logging demo <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/logging_demo>`_ 获取简单示例。
    * 参考 :doc:`logging demo <../../Tutorials/Demos/Logging-and-logger-configuration>` 获取用法示例。
    * 参考 `rclcpp documentation <https://docs.ros2.org/latest/api/rclcpp/logging_8hpp.html>`__ 获取功能详尽列表。

  .. group-tab:: Python

    * 参考 `rclpy examples <https://github.com/ros2/examples/blob/{REPOS_FILE_BRANCH}/rclpy/services/minimal_client/examples_rclpy_minimal_client/client.py>`__，获取节点日志器的用法示例。
    * 参考 `rclpy tests <https://github.com/ros2/rclpy/blob/{REPOS_FILE_BRANCH}/rclpy/test/test_logging.py>`__，获取关键字参数用法示例（例如 ``skip_first``、``once``）。
