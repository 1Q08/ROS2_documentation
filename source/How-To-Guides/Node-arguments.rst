.. redirect-from::

    Node-arguments
    Guides/Node-arguments
    Tutorials/Node-arguments

通过命令行向节点传递 ROS 参数
=============================

.. contents:: 目录
   :depth: 2
   :local:


所有 ROS 节点都接受一组参数，用于重新配置各种属性。
例如配置节点的名称/命名空间、使用的话题/服务名称以及节点上的参数。
所有 ROS 特有的参数都必须放在 ``--ros-args`` 标志之后指定：


.. code-block:: console

   $ ros2 run my_package node_executable --ros-args ...


更多细节请参阅 `这份设计文档 <https://design.ros2.org/articles/ros_command_line_arguments.html>`__。

名称重映射
----------

节点内的名称（例如话题/服务）可以使用 ``-r <old name>:=<new name>`` 语法重映射。
节点自身的名称/命名空间可以使用 ``-r __node:=<new node name>`` 和 ``-r __ns:=<new node namespace>`` 重映射。


请注意，这些重映射是“静态”重映射，也就是说它们在节点的整个生命周期内都生效。
目前尚不支持在节点启动后对名称进行“动态”重映射。

有关重映射参数的更多细节，请参阅 `这份设计文档 <https://design.ros2.org/articles/static_remapping.html>`__ （并非所有功能都已可用）。

示例
^^^^

下面的调用会让 ``talker`` 节点以节点名 ``my_talker`` 启动，并在名为 ``my_topic`` 的话题上发布，而不是默认的 ``chatter``。
命名空间必须以前斜杠开头，这里设为 ``/demo``，这意味着话题在该命名空间中创建（``/demo/my_topic``），而不是在全局范围内（``/my_topic``）。

.. code-block:: console

  $ ros2 run demo_nodes_cpp talker --ros-args -r __ns:=/demo -r __node:=my_talker -r chatter:=my_topic

向特定节点传递重映射参数
~~~~~~~~~~~~~~~~~~~~~~~~

如果在单个进程内运行多个节点（例如使用 :doc:`组合 <../Concepts/Intermediate/About-Composition>`），可以把节点名作为前缀，向特定节点传递重映射参数。
例如，下面会把重映射参数传递给指定的节点：

.. code-block:: console

  $ ros2 run composition manual_composition --ros-args -r talker:__node:=my_talker -r listener:__node:=my_listener


下面的示例既更改节点名又重映射话题（节点和命名空间的更改总是先于话题重映射应用）：

.. code-block:: console

  $ ros2 run composition manual_composition --ros-args -r talker:__node:=my_talker -r my_talker:chatter:=my_topic -r listener:__node:=my_listener -r my_listener:chatter:=my_topic


日志器配置
----------

请参阅 :doc:`日志页面 <../Tutorials/Demos/Logging-and-logger-configuration>` 中 ``--log-level`` 参数的用法。

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

其他节点将能够获取这些参数值，例如：

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

可以通过 yaml 文件的形式从命令行设置参数。

`参见此处 <https://github.com/ros2/rcl/tree/{REPOS_FILE_BRANCH}/rcl_yaml_param_parser>`__ 了解 yaml 文件语法的示例。

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

   通配符可用于节点名和命名空间。
   ``*`` 匹配由斜杠（``/``）分隔的单个词元。
   ``**`` 匹配零个或多个由斜杠分隔的词元。
   不允许部分匹配（例如 ``foo*``）。


然后，在节点内使用 `declare_parameter <http://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/classrclcpp_1_1Node.html#_CPPv4N6rclcpp4Node17declare_parameterERKNSt6stringERKN6rclcpp14ParameterValueERKN14rcl_interfaces3msg19ParameterDescriptorEb>`__ 声明这些参数，或使用 `declare_parameters <http://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/classrclcpp_1_1Node.html#_CPPv4I0EN6rclcpp4Node18declare_parametersENSt6vectorI10ParameterTEERKNSt6stringERKNSt3mapINSt6stringENSt4pairI10ParameterTN14rcl_interfaces3msg19ParameterDescriptorEEEEEb>`__ 声明，又或者 `设置节点自动声明参数 <http://docs.ros.org/en/{DISTRO}/p/rclcpp/generated/classrclcpp_1_1NodeOptions.html#_CPPv4NK6rclcpp11NodeOptions47automatically_declare_parameters_from_overridesEv>`__ （前提是它们是通过命令行覆盖传入的）。

然后运行以下命令：

.. code-block:: console

  $ ros2 run demo_nodes_cpp parameter_blackboard --ros-args --params-file demo_params.yaml


其他节点将能够获取这些参数值，例如：

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
