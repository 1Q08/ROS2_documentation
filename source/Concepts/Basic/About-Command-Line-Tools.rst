.. redirect-from::

    Introspection-with-command-line-tools
    Tutorials/Introspection-with-command-line-tools
    Concepts/About-Command-Line-Tools

使用命令行工具进行探查
======================

.. contents:: 目录
   :local:

ROS 2 提供了一套用于探查 ROS 2 系统的命令行工具。

用法
----

这些工具的主入口命令是 ``ros2``，它自身包含了各种子命令，用于探查和处理节点、主题、服务以及更多内容。

要查看所有可用的子命令，请运行：

.. code-block:: console

   $ ros2 --help

可用子命令示例包括：

* ``action``：探查/与 ROS action 交互
* ``bag``：记录/播放 rosbag
* ``component``：管理组件容器
* ``daemon``：探查/配置 ROS 2 守护进程
* ``doctor``：检查 ROS 设置中的潜在问题
* ``interface``：显示 ROS 接口信息
* ``launch``：运行/探查 launch 文件
* ``lifecycle``：探查/管理具有托管生命周期的节点
* ``multicast``：组播调试命令
* ``node``：探查 ROS 节点
* ``param``：探查/配置节点参数
* ``pkg``：探查 ROS 包
* ``plugin``：探查 ROS 插件
* ``run``：运行 ROS 节点
* ``security``：配置安全设置
* ``service``：探查/调用 ROS 服务
* ``test``：运行 ROS launch 测试
* ``topic``：探查/发布 ROS 主题
* ``trace``：用于获取 ROS 节点执行信息的跟踪工具（仅在 Linux 上可用）
* ``wtf``：``doctor`` 的别名

示例
----

若要使用命令行工具构建典型的 talker-listener 示例，可使用 ``topic`` 子命令在某个主题上发布并回显消息。

在一个终端中发布消息：

.. code-block:: console

   $ ros2 topic pub /chatter std_msgs/msg/String "data: Hello world"
   publisher: beginning loop
   publishing #1: std_msgs.msg.String(data='Hello world')

   publishing #2: std_msgs.msg.String(data='Hello world')

在另一个终端中接收回显消息：

.. code-block:: console

   $ ros2 topic echo /chatter
   data: Hello world

   data: Hello world

ROS 2 守护进程：后台发现服务
----------------------------

ROS 2 使用分布式发现过程让节点相互连接。
由于该过程有意不使用集中式发现机制，因此 ROS 节点发现 ROS 图中所有其他参与者可能需要一定时间。
为了解决这个问题，ROS 2 会运行一个后台守护进程，维护 ROS 图的相关信息，以便更快地响应查询，例如节点名称列表。

当首次使用类似 ``ros2 node list``、``ros2 topic list`` 或其他探查命令时，ROS 2 守护进程会自动启动。
如果没有正在运行的守护进程，这些工具会在执行请求命令前，在后台实例化一个新的守护进程。

该守护进程通过 localhost 网络接口（127.0.0.1）通信，并使用 :doc:`ROS_DOMAIN_ID <../Intermediate/About-Domain-ID>` 环境变量作为端口号偏移量。
这意味着如果你想控制特定的守护进程实例（例如使用 ``ros2 daemon stop``），必须确保你的 :doc:`ROS_DOMAIN_ID <../Intermediate/About-Domain-ID>` 与该守护进程使用的域 ID 相匹配。
不同的 :doc:`ROS_DOMAIN_ID <../Intermediate/About-Domain-ID>` 值会导致不同的守护进程实例在不同端口上运行。

你可以运行 ``ros2 daemon --help`` 查看与守护进程交互的更多选项，包括启动、停止或检查守护进程状态的命令。

在前台运行守护进程
^^^^^^^^^^^^^^^^^^

出于调试目的，前台运行 ROS 2 守护进程是有用的，这样其输出会直接打印到标准输出和标准错误。
这可以通过 ``_ros2_daemon`` 命令完成，它是守护进程自身的入口点：

.. code-block:: console

   $ _ros2_daemon --ros-domain-id 0 --rmw-implementation rmw_fastrtps_cpp

这会启动守护进程而不进行后台化，允许你实时观察所有发现活动和 XML-RPC 请求。
请将 ``--ros-domain-id`` 和 ``--rmw-implementation`` 替换为适合你当前环境的值。

.. note::

   在前台启动一个守护进程前，请确保停止任何已有的守护进程实例（``ros2 daemon stop``），以避免端口冲突。

实现
----

``ros2`` 命令的源代码可在 https://github.com/ros2/ros2cli 获取。

``ros2`` 工具已经被实现为一个可通过插件扩展的框架。
例如，`sros2 <https://github.com/ros2/sros2>`__ 包提供了一个 ``security`` 子命令；只要安装了 ``sros2`` 包，``ros2`` 工具就会自动检测该子命令。
