迁移脚本
========

ROS CLI
-------

在 ROS 1 中，有不同的独立命令用于执行各种操作，
例如 ``rosrun``、``rosparam`` 等。

在 ROS 2 中，有一个名为 ``ros2`` 的单一顶层命令，
所有操作都是它的子命令，例如 ``ros2 run``、``ros2 param`` 等。

ROS CLI 参数
------------

在 ROS 1 中，节点的参数直接提供在命令行上。

ROS 2 的参数应该用 ``--ros-args`` 限定作用域，
并在末尾加上 ``--`` （如果后面没有参数，末尾的双破折号可以省略）。

重映射名称与 ROS 1 类似，采用 ``from:=to`` 的形式，
只是它前面必须加上 ``--remap`` （或 ``-r``）标志。
例如：

.. code-block:: console

   $ ros2 run some_package some_ros_executable --ros-args -r foo:=bar

对于参数，我们使用类似的语法，使用 ``--param``\ （或 ``-p``）标志：

.. code-block:: console

   $ ros2 run some_package some_ros_executable --ros-args -p my_param:=value

请注意，这与 ROS 1 中使用前导下划线的方式不同。

要更改节点名称，请使用 ``__node``\ （ROS 1 中的等价物是 ``__name``）：

.. code-block:: console

   $ ros2 run some_package some_ros_executable --ros-args -r __node:=new_node_name

请注意 ``-r`` 标志的使用。
更改命名空间 ``__ns`` 也需要使用相同的重映射标志：

.. code-block:: console

   $ ros2 run some_package some_ros_executable --ros-args -r __ns:=/new/namespace

在 ROS 2 中，以下 ROS 1 键没有等价物：

- ``__log``\ （但可以使用 ``--log-config-file`` 提供日志记录器配置文件）
- ``__ip``
- ``__hostname``
- ``__master``

更多信息请参见 `设计文档 <https://design.ros2.org/articles/ros_command_line_arguments.html>`_。

快速参考
~~~~~~~~

+------------+-------------+----------------+
| 功能       | ROS 1       | ROS 2          |
+============+=============+================+
| 重映射     | foo:=bar    | -r foo:=bar    |
+------------+-------------+----------------+
| 参数       | _foo:=bar   | -p foo:=bar    |
+------------+-------------+----------------+
| 节点名称   | __name:=foo | -r __node:=foo |
+------------+-------------+----------------+
| 命名空间   | __ns:=foo   | -r __ns:=foo   |
+------------+-------------+----------------+
