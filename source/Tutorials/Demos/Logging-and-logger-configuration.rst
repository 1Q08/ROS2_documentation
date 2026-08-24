.. redirect-from::

    Logging-and-logger-configuration
    Tutorials/Logging-and-logger-configuration

日志记录
========

.. contents:: 目录
   :depth: 2
   :local:

有关可用功能的详细信息，请参阅 `日志页面 <../../Concepts/Intermediate/About-Logging>`。

在代码中使用日志语句
--------------------

基本日志
^^^^^^^^

以下代码将从 ROS 2 节点以 ``DEBUG`` 严重级别输出一条日志消息：

.. tabs::

    .. group-tab:: C++

        .. code-block:: C++

            // printf style
            RCLCPP_DEBUG(node->get_logger(), "My log message %d", 4);

            // C++ stream style
            RCLCPP_DEBUG_STREAM(node->get_logger(), "My log message " << 4);

    .. group-tab:: Python

        .. code-block:: python

            node.get_logger().debug('My log message %d' % (4))

请注意，在两种情况下都没有添加末尾换行，因为日志基础设施会自动添加一个。

仅首次记录日志
^^^^^^^^^^^^^^

以下代码将从 ROS 2 节点以 ``INFO`` 严重级别输出一条日志消息，但仅在首次命中时：

.. tabs::

    .. group-tab:: C++

        .. code-block:: C++

            // printf style
            RCLCPP_INFO_ONCE(node->get_logger(), "My log message %d", 4);

            // C++ stream style
            RCLCPP_INFO_STREAM_ONCE(node->get_logger(), "My log message " << 4);

    .. group-tab:: Python

        .. code-block:: python

            num = 4
            node.get_logger().info(f'My log message {num}', once=True)

除了首次之外都记录日志
^^^^^^^^^^^^^^^^^^^^^^

以下代码将从 ROS 2 节点以 ``WARN`` 严重级别输出一条日志消息，但不在首次命中时输出：

.. tabs::

    .. group-tab:: C++

        .. code-block:: C++

            // printf style
            RCLCPP_WARN_SKIPFIRST(node->get_logger(), "My log message %d", 4);

            // C++ stream style
            RCLCPP_WARN_STREAM_SKIPFIRST(node->get_logger(), "My log message " << 4);

    .. group-tab:: Python

        .. code-block:: python

            num = 4
            node.get_logger().warning('My log message {0}'.format(num), skip_first=True)

节流日志
^^^^^^^^

以下代码将从 ROS 2 节点以 ``ERROR`` 严重级别输出一条日志消息，但每秒不超过一次。

指定消息间隔毫秒数的 interval 参数应为整数数据类型，以便转换为 ``rcutils_duration_value_t``（一个 ``int64_t``）：

.. tabs::

    .. group-tab:: C++

        .. code-block:: C++

            // printf style
            RCLCPP_ERROR_THROTTLE(node->get_logger(), *node->get_clock(), 1000, "My log message %d", 4);

            // C++ stream style
            RCLCPP_ERROR_STREAM_THROTTLE(node->get_logger(), *node->get_clock(), 1000, "My log message " << 4);

            // For now, use the nanoseconds() method to use an existing rclcpp::Duration value, see https://github.com/ros2/rclcpp/issues/1929
            RCLCPP_ERROR_STREAM_THROTTLE(node->get_logger(), *node->get_clock(), msg_interval.nanoseconds()/1000000, "My log message " << 4);

    .. group-tab:: Python

        .. code-block:: python

            num = 4
            node.get_logger().error(f'My log message {num}', throttle_duration_sec=1)

除首次之外都节流记录日志
^^^^^^^^^^^^^^^^^^^^^^^^

以下代码将从 ROS 2 节点以 ``DEBUG`` 严重级别输出一条日志消息，每秒不超过一次，并跳过首次命中：

.. tabs::

    .. group-tab:: C++

        .. code-block:: C++

            // printf style
            RCLCPP_DEBUG_SKIPFIRST_THROTTLE(node->get_logger(), *node->get_clock(), 1000, "My log message %d", 4);

            RCLCPP_DEBUG_SKIPFIRST_THROTTLE(node->get_logger(), *node->get_clock(), 1000, "My log message " << 4);

    .. group-tab:: Python

        .. code-block:: python

            num = 4
            node.get_logger().debug(f'My log message {num}', skip_first=True, throttle_duration_sec=1.0)

日志演示
--------

在这个 `演示 <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/logging_demo>`_ 中，展示了不同类型的日志调用，并在本地和外部配置了不同日志记录器的严重级别。

使用以下命令启动演示：

.. code-block:: console

   $ ros2 run logging_demo logging_demo_main

随着时间的推移，你会看到来自各种不同属性的日志调用的输出。
一开始，你只会看到严重级别为 ``INFO`` 及以上（``WARN``、``ERROR``、``FATAL``）的日志调用的输出。
请注意，第一条消息只会被记录一次，尽管每次迭代都会到达该行，因为这是用于该消息的日志调用的一种属性。

日志目录配置
------------

日志目录可以通过两个环境变量配置：``ROS_LOG_DIR`` 和 ``ROS_HOME``。
逻辑如下：

* 如果 ``ROS_LOG_DIR`` 已设置且不为空，则使用 ``$ROS_LOG_DIR``。
* 否则，使用 ``$ROS_HOME/log``；如果 ``ROS_HOME`` 未设置或为空，则使用 ``~/.ros`` 作为 ``ROS_HOME``。

例如，要将日志目录设置为 ``~/my_logs``：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export ROS_LOG_DIR=~/my_logs
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: macOS

    .. code-block:: console

      $ export ROS_LOG_DIR=~/my_logs
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: Windows

    .. code-block:: console

      $ set "ROS_LOG_DIR=~/my_logs"
      $ ros2 run logging_demo logging_demo_main

然后你可以在 ``~/my_logs/`` 下找到日志。

或者，你可以设置 ``ROS_HOME``，日志目录将相对于它（``$ROS_HOME/log``）。
``ROS_HOME`` 旨在供任何需要基目录的事物使用。
请注意，``ROS_LOG_DIR`` 必须未设置或为空。
例如，将 ``ROS_HOME`` 设置为 ``~/my_ros_home``：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export ROS_HOME=~/my_ros_home
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: macOS

    .. code-block:: console

      $ export ROS_HOME=~/my_ros_home
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: Windows

    .. code-block:: console

      $ set "ROS_HOME=~/my_ros_home"
      $ ros2 run logging_demo logging_demo_main

然后你可以在 ``~/my_ros_home/log/`` 下找到日志。

日志级别配置：程序化
--------------------

经过 10 次迭代后，日志记录器的级别将被设置为 ``DEBUG``，这将导致额外的消息被记录。

其中一些调试消息会导致额外的函数/表达式被求值，这些之前因为 ``DEBUG`` 日志调用未启用而被跳过。
有关所使用调用的进一步说明，请参阅演示的 `源代码 <https://github.com/ros2/demos/blob/{REPOS_FILE_BRANCH}/logging_demo/src/logger_usage_component.cpp>`__，有关受支持日志调用的完整列表，请参阅 rclcpp 日志文档。

日志级别配置：外部
------------------

ROS 2 节点提供服务，可以在运行时从外部配置日志级别。
这些服务默认是禁用的。
以下代码展示了如何在创建节点时启用日志服务。

.. tabs::

  .. group-tab:: C++

    .. code-block:: C++

        // Create a node with logger service enabled
        auto node = std::make_shared<rclcpp::Node>("NodeWithLoggerService", rclcpp::NodeOptions().enable_logger_service(true));

  .. group-tab:: Python

    .. code-block:: python

        # Create a node with logger service enabled
        node = Node('NodeWithLoggerService', enable_logger_service=True)

如果你运行上述配置的节点之一，执行 ``ros2 service list`` 时你会发现 2 个服务：

.. code-block:: console

    $ ros2 service list
    ...
    /NodeWithLoggerService/get_logger_levels
    /NodeWithLoggerService/set_logger_levels
    ...

* get_logger_levels

    使用此服务获取指定日志记录器名称的日志级别。

    运行 ``ros2 service call`` 获取 ``NodeWithLoggerService`` 和 ``rcl`` 的日志级别。

    .. code-block:: console

        $ ros2 service call /NodeWithLoggerService/get_logger_levels rcl_interfaces/srv/GetLoggerLevels '{names: ["NodeWithLoggerService", "rcl"]}'

        requester: making request: rcl_interfaces.srv.GetLoggerLevels_Request(names=['NodeWithLoggerService', 'rcl'])

        response:
        rcl_interfaces.srv.GetLoggerLevels_Response(levels=[rcl_interfaces.msg.LoggerLevel(name='NodeWithLoggerService', level=0), rcl_interfaces.msg.LoggerLevel(name='rcl', level=0)])

* set_logger_levels

    使用此服务设置指定日志记录器名称的日志级别。

    运行 ``ros2 service call`` 设置 ``NodeWithLoggerService`` 和 ``rcl`` 的日志级别。

    .. code-block:: console

        $ ros2 service call /NodeWithLoggerService/set_logger_levels rcl_interfaces/srv/SetLoggerLevels '{levels: [{name: "NodeWithLoggerService", level: 20}, {name: "rcl", level: 10}]}'

        requester: making request: rcl_interfaces.srv.SetLoggerLevels_Request(levels=[rcl_interfaces.msg.LoggerLevel(name='NodeWithLoggerService', level=20), rcl_interfaces.msg.LoggerLevel(name='rcl', level=10)])

        response:
        rcl_interfaces.srv.SetLoggerLevels_Response(results=[rcl_interfaces.msg.SetLoggerLevelsResult(successful=True, reason=''), rcl_interfaces.msg.SetLoggerLevelsResult(successful=True, reason='')])


还有演示代码，展示如何通过日志服务设置或获取日志级别。

  * rclcpp: `demo code <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/demo_nodes_cpp/src/logging/use_logger_service.cpp>`__

      .. code-block:: console

          $ ros2 run demo_nodes_cpp use_logger_service

  * rclpy: `demo code <https://github.com/ros2/demos/tree/{REPOS_FILE_BRANCH}/demo_nodes_py/demo_nodes_py/logging/use_logger_service.py>`__

      .. code-block:: console

          $ ros2 run demo_nodes_py use_logger_service

.. warning::

    目前有一个限制，即 ``get_logger_levels`` 和 ``set_logger_levels`` 服务不是线程安全的。
    这意味着你需要确保同一时间只有一个线程在调用这些服务。
    详情请见 https://github.com/ros2/rcutils/issues/397

使用日志配置组件
^^^^^^^^^^^^^^^^

响应日志配置请求的服务器已开发为组件，以便可以将其添加到现有的基于组合的系统中。
例如，如果你正在使用 `容器来运行你的节点 <../Intermediate/Composition>`，为了能够配置你的日志记录器，你只需要请求它额外将 ``logging_demo::LoggerConfig`` 组件加载到容器中。

例如，如果你想调试 ``composition::Talker`` 演示，你可以像往常一样启动 talker：

Shell 1:

.. code-block:: console

   $ ros2 run rclcpp_components component_container

Shell 2:

.. code-block:: console

   $ ros2 component load /ComponentManager composition composition::Talker

然后，当你想启用调试日志时，用以下命令加载 ``LoggerConfig`` 组件：

Shell 2

.. code-block:: console

   $ ros2 component load /ComponentManager logging_demo logging_demo::LoggerConfig

最后，通过寻址空名称的日志记录器，将所有未设置的日志记录器配置为 debug 严重级别。
请注意，已专门配置为使用特定严重级别的日志记录器不会受此调用影响。

Shell 2:

.. code-block:: console

   $ ros2 service call /config_logger logging_demo/srv/ConfigLogger "{logger_name: '', level: DEBUG}"

你应该会看到进程中所有之前未设置的日志记录器开始出现调试输出，包括来自 ROS 2 核心的输出。

日志级别配置：命令行
--------------------

从 Bouncy ROS 2 发行版开始，尚未显式设置严重级别的日志记录器，可以从命令行配置其严重级别。
重新启动演示并包含以下命令行参数：


.. code-block:: console

   $ ros2 run logging_demo logging_demo_main --ros-args --log-level debug

这将任何未设置日志记录器的默认严重级别配置为 debug 严重级别。
你应该会看到来自演示本身和 ROS 2 核心的日志记录器的调试输出。

可以在命令行配置单个日志记录器的严重级别。
重新启动演示并包含以下命令行参数：

.. code-block:: console

   $ ros2 run logging_demo logging_demo_main --ros-args --log-level logger_usage_demo:=debug


控制台输出格式
^^^^^^^^^^^^^^

如果你想要更详细或更简洁的格式，可以使用 ``RCUTILS_CONSOLE_OUTPUT_FORMAT`` 环境变量。
例如，为了额外获取日志调用的时间戳和位置，停止演示并设置环境变量后重新启动它：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export RCUTILS_CONSOLE_OUTPUT_FORMAT="[{severity} {time}] [{name}]: {message} ({function_name}() at {file_name}:{line_number})"
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: macOS

    .. code-block:: console

      $ export RCUTILS_CONSOLE_OUTPUT_FORMAT="[{severity} {time}] [{name}]: {message} ({function_name}() at {file_name}:{line_number})"
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: Windows

    .. code-block:: console

      $ set "RCUTILS_CONSOLE_OUTPUT_FORMAT=[{severity} {time}] [{name}]: {message} ({function_name}() at {file_name}:{line_number})"
      $ ros2 run logging_demo logging_demo_main

你应该会看到每条消息额外打印出以秒为单位的时间戳、函数名、文件名和行号。

有关配置控制台日志记录器格式的更多信息，请参阅 :ref:`日志记录器控制台配置 <logging-configuration-environment-variables>`

控制台输出着色
^^^^^^^^^^^^^^

默认情况下，当输出目标是终端时，输出会被着色。
如果你想强制启用或禁用它，可以使用 ``RCUTILS_COLORIZED_OUTPUT`` 环境变量。
例如：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export RCUTILS_COLORIZED_OUTPUT=0  # 1 for forcing it
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: macOS

    .. code-block:: console

      $ export RCUTILS_COLORIZED_OUTPUT=0  # 1 for forcing it
      $ ros2 run logging_demo logging_demo_main

  .. group-tab:: Windows

    .. code-block:: console

      $ set "RCUTILS_COLORIZED_OUTPUT=0" :: 1 for forcing it
      $ ros2 run logging_demo logging_demo_main

你应该会看到 debug、warn、error 和 fatal 日志现在不着色了。

.. note::

   在 Linux 和 MacOS 中，强制着色输出意味着如果你将输出重定向到文件，文件中会出现 ansi 转义颜色代码。
   在 Windows 中，着色方法依赖于控制台 API。
   如果被强制，你会得到一条新的警告，说明着色失败。
   默认行为已经检查输出是否为控制台，因此不建议强制着色。

.. note::

   如果你通过 ``ros2 launch`` 启动多个节点，没有任何节点会附加活动终端（除非你设置 ``emulate_tty=True``）。
   这意味着要让 ``ros2 launch`` 获得着色输出，你需要显式设置 ``RCUTILS_COLORIZED_OUTPUT=1``。

控制台输出的默认流
^^^^^^^^^^^^^^^^^^

在 Foxy 及更高版本中，所有调试级别的输出默认都到 stderr。
可以通过将 ``RCUTILS_LOGGING_USE_STDOUT`` 环境变量设置为 ``1`` 来强制所有输出到 stdout。
例如：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export RCUTILS_LOGGING_USE_STDOUT=1

  .. group-tab:: macOS

    .. code-block:: console

      $ export RCUTILS_LOGGING_USE_STDOUT=1

  .. group-tab:: Windows

    .. code-block:: console

      $ set "RCUTILS_LOGGING_USE_STDOUT=1"


行缓冲控制台输出
^^^^^^^^^^^^^^^^


默认情况下，所有日志输出都是无缓冲的。
你可以通过将 ``RCUTILS_LOGGING_BUFFERED_STREAM`` 环境变量设置为 1 来强制它缓冲。
例如：

.. tabs::

  .. group-tab:: Linux

    .. code-block:: console

      $ export RCUTILS_LOGGING_BUFFERED_STREAM=1

  .. group-tab:: macOS

    .. code-block:: console

      $ export RCUTILS_LOGGING_BUFFERED_STREAM=1

  .. group-tab:: Windows

    .. code-block:: console

      $ set "RCUTILS_LOGGING_BUFFERED_STREAM=1"

然后运行：

.. code-block:: console

    $ ros2 run logging_demo logging_demo_main

设置日志文件名前缀
------------------

默认情况下，日志文件名基于可执行文件名，后跟进程 ID 和文件创建时的系统时间戳。
你可以使用 ``--log-file-name`` 命令行参数将日志文件名前缀改为你选择的前缀：

.. code-block:: console

   $ ros2 run demo_nodes_cpp talker --ros-args --log-file-name filename

这将日志文件名前缀配置为 ``filename``，而不是可执行文件名（本例中为 ``talker``）。
