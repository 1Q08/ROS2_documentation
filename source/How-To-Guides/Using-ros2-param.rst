使用 ``ros2 param`` 命令行工具
==============================

.. contents:: 目录
   :depth: 1
   :local:

ROS 2 中的参数可以通过一组服务进行获取、设置、列出和描述，
如 :doc:`概念文档 <../Concepts/Basic/About-Parameters>` 中所述。
``ros2 param`` 命令行工具是这些服务调用的封装，
它使得从命令行操作参数变得很容易。

``ros2 param list``
-------------------

此命令将列出给定节点上的所有可用参数，
如果未给定节点，则列出所有可发现节点上的参数。

获取给定节点上的所有参数：

.. code-block:: console

  $ ros2 param list /my_node

获取系统中所有节点上的所有参数
（在复杂的网络上这可能需要很长时间）：

.. code-block:: console

  $ ros2 param list

``ros2 param get``
------------------

此命令将获取特定节点上特定参数的值。

获取节点上某个参数的值：

.. code-block:: console

  $ ros2 param get /my_node use_sim_time

``ros2 param set``
------------------

此命令将设置特定节点上特定参数的值。
对于大多数参数，新值的类型必须与现有类型相同。

设置节点上某个参数的值：

.. code-block:: console

  $ ros2 param set /my_node use_sim_time false

在命令行上传入的值是 YAML 格式，它允许使用任意的 YAML 表达式。
然而，这也意味着某些表达式的解释方式可能与预期不同。
例如，如果节点 ``my_node`` 上的参数 ``my_string`` 是字符串类型，
以下命令将不起作用：

.. code-block:: console

  $ ros2 param set /my_node my_string off

这是因为 YAML 将 "off" 解释为布尔值，而 ``my_string`` 是字符串类型。
可以通过使用 YAML 中显式设置字符串的语法来绕过这一点，例如：

.. code-block:: console

  $ ros param set /my_node my_string '!!str off'

此外，YAML 支持异构列表，例如包含一个字符串、一个布尔值和一个整数。
然而，ROS 2 参数不支持异构列表，因此任何包含多种类型的 YAML 列表
都会被解释为字符串。
假设节点 ``my_node`` 上的参数 ``my_int_array`` 是整数数组类型，
以下命令将不起作用：

.. code-block:: console

  $ ros param set /my_node my_int_array '[foo,off,1]'

以下字符串类型的参数则可以正常工作：

.. code-block:: console

  $ ros param set /my_node my_string '[foo,off,1]'

``ros2 param delete``
---------------------

此命令将从特定节点移除一个参数。
然而，请注意，这只能移除动态参数（不能移除已声明的参数）。
更多信息请参见 :doc:`概念文档 <../Concepts/Basic/About-Parameters>`。

.. code-block:: console

  $ ros2 param delete /my_node my_string

``ros2 param describe``
-----------------------

此命令将提供特定节点上特定参数的文本描述：

.. code-block:: console

  $ ros2 param describe /my_node use_sim_time

``ros2 param dump``
-------------------

此命令将以 YAML 文件格式打印出特定节点上的所有参数。
此命令的输出随后可用于稍后以相同的参数重新运行节点：

.. code-block:: console

  $ ros2 param dump /my_node

``ros2 param load``
-------------------

此命令将从 YAML 文件加载参数值到特定节点。
也就是说，此命令可以在运行时重新加载由 ``ros2 param dump``
导出的值：

.. code-block:: console

  $ ros2 param load /my_node my_node.yaml
