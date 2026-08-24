.. redirect-from::

    Introspection-with-command-line-tools
    Tutorials/Introspection-with-command-line-tools
    Concepts/About-Command-Line-Tools

使用命令行工具进行内省
======================

.. contents:: 目录
   :local:

ROS 2 包含一套用于内省 ROS 2 系统的命令行工具。

用法
----

这些工具的主要入口点是 ``ros2`` 命令，它本身又有各种子命令，用于内省和处理节点、话题、服务等。

要查看所有可用的子命令，请运行：

.. code-block:: console

   $ ros2 --help

可用的子命令示例包括：

* ``action``：内省/交互 ROS 动作
* ``bag``：录制/回放 rosbag
* ``component``：管理组件容器
* ``daemon``：内省/配置 ROS 2 守护进程
* ``doctor``：检查 ROS 设置是否存在潜在问题
* ``interface``：显示 ROS 接口的信息
* ``launch``：运行/内省启动文件
* ``lifecycle``：内省/管理具有托管生命周期的节点
* ``multicast``：组播调试命令
* ``node``：内省 ROS 节点
* ``param``：内省/配置节点上的参数
* ``pkg``：内省 ROS 包
* ``plugin``：内省 ROS 插件
* ``run``：运行 ROS 节点
* ``security``：配置安全设置
* ``service``：内省/调用 ROS 服务
* ``test``：运行 ROS 启动测试
* ``topic``：内省/发布 ROS 话题
* ``trace``：追踪工具，用于获取 ROS 节点执行的信息（仅在 Linux 上可用）
* ``wtf``：``doctor`` 的别名

示例
----

要使用命令行工具生成典型的 talker-listener 示例，可以用 ``topic`` 子命令在话题上发布和回显消息。

在一个终端中用以下命令发布消息：

.. code-block:: console

   $ ros2 topic pub /chatter std_msgs/msg/String "data: Hello world"
   publisher: beginning loop
   publishing #1: std_msgs.msg.String(data='Hello world')

   publishing #2: std_msgs.msg.String(data='Hello world')

在另一个终端中用以下命令回显收到的消息：

.. code-block:: console

   $ ros2 topic echo /chatter
   data: Hello world

   data: Hello world

ROS 2 守护进程：后台发现服务
----------------------------

ROS 2 使用分布式发现过程让节点互相连接。
由于该过程有意不使用集中式发现机制，ROS 节点发现 ROS 图中所有其他参与者可能需要一些时间。
为了解决这个问题，ROS 2 运行一个后台守护进程，维护 ROS 图的信息，以便更快地响应查询，例如节点名称列表。

当你首次使用 ``ros2 node list``、``ros2 topic list`` 或其他内省命令时，ROS 2 守护进程会自动启动。
如果没有守护进程在运行，这些工具会在执行请求的命令之前，先在后台实例化一个新的守护进程。

守护进程使用 localhost 网络接口（127.0.0.1）进行通信，并使用 :doc:`ROS_DOMAIN_ID <../Intermediate/About-Domain-ID>` 环境变量作为端口号偏移。
这意味着如果你想控制某个特定的守护进程实例（例如使用 ``ros2 daemon stop``），必须确保你的 :doc:`ROS_DOMAIN_ID <../Intermediate/About-Domain-ID>` 与该守护进程使用的域 ID 匹配。
不同的 :doc:`ROS_DOMAIN_ID <../Intermediate/About-Domain-ID>` 值会导致在不同的端口上运行单独的守护进程实例。

你可以运行 ``ros2 daemon --help`` 查看与守护进程交互的更多选项，包括启动、停止或检查守护进程状态的命令。

在前台运行守护进程
^^^^^^^^^^^^^^^^^^

出于调试目的，在前台运行 ROS 2 守护进程可能会很有用，这样它的输出会直接打印到 stdout 和 stderr。
这可以通过 ``_ros2_daemon`` 命令实现，它是守护进程本身的入口点：

.. code-block:: console

   $ _ros2_daemon --ros-domain-id 0 --rmw-implementation rmw_fastrtps_cpp

这将在不进行守护进程化的前提下启动守护进程，使你能够实时观察所有发现活动和 XML-RPC 请求。
请将 ``--ros-domain-id`` 和 ``--rmw-implementation`` 的值替换为适合你环境的值。

.. note::

   在前台启动守护进程之前，请务必停止任何现有的守护进程实例（``ros2 daemon stop``），以避免端口冲突。

实现
----

``ros2`` 命令的源代码可在 https://github.com/ros2/ros2cli 获取。

``ros2`` 工具被实现为一个可以通过插件扩展的框架。
例如，`sros2 <https://github.com/ros2/sros2>`__ 包提供了一个 ``security`` 子命令，如果安装了 ``sros2`` 包，``ros2`` 工具会自动检测到它。
