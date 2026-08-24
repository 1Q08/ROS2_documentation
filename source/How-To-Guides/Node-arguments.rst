.. redirect-from::

    Node-arguments
    Guides/Node-arguments
    Tutorials/Node-arguments

通过命令行向节点传递 ROS 参数
=============================

.. contents:: 目录
   :depth: 2
   :local:


所有 ROS 节点都接受一组参数，这些参数允许重新配置各种属性。
示例包括配置节点的名称/命名空间、使用的话题/服务名称以及节点上的参数。
所有 ROS 特定参数都必须在 ``--ros-args`` 标志之后指定：


.. code-block:: console

   $ ros2 run my_package node_executable --ros-args ...


有关更多详细信息，请参见 `这份设计文档 <https://design.ros2.org/articles/ros_command_line_arguments.html>`__。

名称重映射
----------

节点内的名称（例如话题/服务）可以使用语法 ``-r <old name>:=<new name>`` 进行重映射。
节点本身的名称/命名空间可以使用 ``-r __node:=<new node name>`` 和 ``-r __ns:=<new node namespace>`` 进行重映射。


请注意，这些重映射是“静态”重映射，因为它们适用于节点的整个生命周期。
节点启动后的名称“动态”重映射尚不受支持。

有关重映射参数的更多详细信息，请参见 `这份设计文档 <https://design.ros2.org/articles/static_remapping.html>`__ （并非所有功能都已可用）。

示例
^^^^

以下调用将导致 ``talker`` 节点以节点名称 ``my_talker`` 启动，在名为 ``my_topic`` 的话题上发布，而不是默认的 ``chatter``。
命名空间必须以正斜杠开头，设置为 ``/demo``，这意味着话题创建在该命名空间中（``/demo/my_topic``），而不是全局的（``/my_topic``）。

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args -r __ns:=/demo -r __node:=my_talker -r chatter:=my_topic

将重映射参数传递给特定节点
~~~~~~~~~~~~~~~~~~~~~~~~~~

如果在单个进程中运行多个节点（例如使用 :doc:`组合 <../Concepts/Intermediate/About-Composition>`），可以使用节点名称作为前缀将重映射参数传递给特定节点。
例如，以下内容将把重映射参数传递给指定的节点：

.. code-block:: console

  $ ros2 run composition manual_composition --ros-args -r talker:__node:=my_talker -r listener:__node:=my_listener


以下示例既更改节点名称又重映射话题（节点和命名空间更改总是在话题重映射*之前*应用）：

.. code-block:: console

  $ ros2 run composition manual_composition --ros-args -r talker:__node:=my_talker -r my_talker:chatter:=my_topic -r listener:__node:=my_listener -r my_listener:chatter:=my_topic


日志记录器配置
--------------

每个节点的日志记录级别可以使用 ``--log-level`` 命令行参数指定。
可执行文件日志文件名前缀（包括可执行文件中的所有节点）可以使用 ``--log-file-name`` 命令行参数指定。
有关更多信息，请参见 :doc:`日志页面 <../Tutorials/Demos/Logging-and-logger-configuration>`。

参数
----

.. _NodeArgsParameters:

直接从命令行设置参数
^^^^^^^^^^^^^^^^^^^^

你可以使用以下语法直接从命令行设置参数：

.. code-block:: console

  $ ros2 run package_name executable_name --ros-args -p param_name:=param_value

例如，你可以运行：

.. code-block:: console

  $ ros2 run demo_nodes_cpp parameter_blackboard --ros-args -p some_int:=42 -p "a_string:=Hello world" -p "some_lists.some_integers:=[1, 2, 3, 4]" -p "some_lists.some_doubles:=[3.14, 2.718]"

其他节点将能够检索参数值，例如：

.. code-block:: console

  $ ros2 param list parameter_blackboard
  a_string
  qos_overrides./parameter_events.publisher.depth
  qos_overrides./parameter_events.publisher.durability
  qos_overrides./parameter_events.publisher.history
  qos_overrides./parameter_events.publisher.reliability
  some_int
  some_lists.some_doubles
  some_lists.some_integers
  use_sim_time

从 YAML 文件设置参数
^^^^^^^^^^^^^^^^^^^^

参数可以以 yaml 文件的形式从命令行设置。

`请参见此处 <https://github.com/ros2/rcl/tree/{REPOS_FILE_BRANCH}/rcl_yaml_param_parser>`__ 了解 yaml 文件语法的示例。

例如，将以下内容保存为 ``demo_params.yaml``：

.. code-block:: yaml

  parameter_blackboard:
      ros__parameters:
          some_int: 42
          a_string: "Hello world"
          some_lists:
              some_integers: [1, 2, 3, 4]
              some_doubles : [3.14, 2.718]

  /**:
    ros__parameters:
      wildcard_full: "Full wildcard for any namespaces and any node names"

  /**/parameter_blackboard:
    ros__parameters:
      wildcard_namespace: "Wildcard for a specific node name under any namespace"

  /*:
    ros__parameters:
      wildcard_nodename_root_namespace: "Wildcard for any node names, but only in root namespace"


.. note::

   通配符可以用于节点名称和命名空间。
   ``*`` 匹配由斜杠（``/``）分隔的单个标记。
   ``**`` 匹配由斜杠分隔的零个或多个标记。
   不允许部分匹配（例如 ``foo*``）。


然后在你的节点中使用 `declare_parameter <http://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/classrclcpp_1_1Node.html#_CPPv4N6rclcpp4Node17declare_parameterERKNSt6stringERKN6rclcpp14ParameterValueERKN14rcl_interfaces3msg19ParameterDescriptorEb>`__ 或 `declare_parameters <http://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/classrclcpp_1_1Node.html#_CPPv4I0EN6rclcpp4Node18declare_parametersENSt6vectorI10ParameterTEERKNSt6stringERKNSt3mapINSt6stringENSt4pairI10ParameterTN14rcl_interfaces3msg19ParameterDescriptorEEEEEb>`__ 声明参数，或者 `将节点设置为自动声明参数 <http://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/classrclcpp_1_1NodeOptions.html#_CPPv4NK6rclcpp11NodeOptions47automatically_declare_parameters_from_overridesEv>`__ （如果它们是通过命令行覆盖传入的）。

然后运行以下命令：

.. code-block:: console

  $ ros2 run demo_nodes_cpp parameter_blackboard --ros-args --params-file demo_params.yaml


其他节点将能够检索参数值，例如：

.. code-block:: console

  $ ros2 param list parameter_blackboard
  a_string
  qos_overrides./parameter_events.publisher.depth
  qos_overrides./parameter_events.publisher.durability
  qos_overrides./parameter_events.publisher.history
  qos_overrides./parameter_events.publisher.reliability
  some_int
  some_lists.some_doubles
  some_lists.some_integers
  use_sim_time
  wildcard_full
  wildcard_namespace
  wildcard_nodename_root_namespace
