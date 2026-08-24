.. redirect-from::

    About-ROS-2-Parameters
    Concepts/About-ROS-2-Parameters

参数
====

.. contents:: 目录
   :local:

概述
----

ROS 2 中的参数与各个节点相关联。
参数用于在启动时（以及运行期间）配置节点，而无需更改代码。
参数的生命周期与节点的生命周期绑定（不过节点可以实现某种持久化机制，以便在重启后重新加载值）。

参数通过节点名称、节点命名空间、参数名称和参数命名空间来寻址。
提供参数命名空间是可选的。

每个参数由一个键、一个值和一个描述符组成。
键是字符串，值是以下类型之一：``bool``、``int64``、``float64``、``string``、``byte[]``、``bool[]``、``int64[]``、``float64[]`` 或 ``string[]``。
默认情况下，所有描述符都是空的，但可以包含参数描述、取值范围、类型信息以及额外的约束。

有关 ROS 参数的动手教程，请参阅 :doc:`../../Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters`。

参数背景
--------

声明参数
^^^^^^^^

默认情况下，节点需要 *声明* 它在其生命周期内将要接受的所有参数。
这样可以在节点启动时就明确参数的类型和名称，从而降低之后配置出错的可能性。
有关在节点中声明和使用参数的教程，请参阅 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP` 或 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python`。

对于某些类型的节点，并非所有参数都能提前知道。
在这些情况下，可以在实例化节点时将 ``allow_undeclared_parameters`` 设置为 ``true``，这样即使参数尚未声明，也允许在节点上获取和设置它们。

参数类型
^^^^^^^^

ROS 2 节点上的每个参数都具有概述中提到的一种预定义参数类型。
默认情况下，在运行时尝试更改已声明参数的类型会失败。
这可以防止常见错误，例如将布尔值放入整数参数中。

如果一个参数需要支持多种不同类型，并且使用该参数的代码能够处理这种情况，则可以更改此默认行为。
在声明参数时，应使用 ``ParameterDescriptor`` 进行声明，并将其 ``dynamic_typing`` 成员变量设置为 ``true``。

参数回调
^^^^^^^^

ROS 2 节点可以注册三种不同类型的回调，以便在参数发生变化时得到通知。
这三种回调都是可选的。

第一种称为“预设置参数（pre set parameter）”回调，可以通过节点 API 调用 ``add_pre_set_parameters_callback`` 来设置。
此回调会收到一个正在更改的 ``Parameter`` 对象列表，并且不返回任何内容。
它被调用时，可以修改 ``Parameter`` 列表以更改、添加或删除条目。
例如，如果每当 ``parameter1`` 更改时 ``parameter2`` 都应更改，就可以用这个回调来实现。

第二种称为“设置参数（set parameter）”回调，可以通过节点 API 调用 ``add_on_set_parameters_callback`` 来设置。
此回调会收到一个不可变的 ``Parameter`` 对象列表，并返回一个 ``rcl_interfaces/msg/SetParametersResult``。
此回调的主要目的是让用户能够检查即将发生的参数更改，并明确拒绝该更改。

.. note::
   “设置参数”回调不应有任何副作用，这一点很重要。
   由于多个“设置参数”回调可以串联执行，单个回调无法知道后续的回调是否会拒绝更新。
   例如，如果单个回调对它所在的类进行了更改，就可能与实际参数失去同步。
   要在参数 *成功* 更改之后获得回调，请参阅下面的下一种回调类型。

第三种类型的回调称为“后置设置参数（post set parameter）”回调，可以通过节点 API 调用 ``add_post_set_parameters_callback`` 来设置。
此回调会收到一个不可变的 ``Parameter`` 对象列表，并且不返回任何内容。
此回调的主要目的是让用户能够对已成功接受的参数更改做出反应。

ROS 2 的演示中有一个使用所有这些回调的 `示例 <https://github.com/ros2/demos/blob/{DISTRO}/demo_nodes_cpp/src/parameters/set_parameters_callback.cpp>`__。

与参数交互
----------

ROS 2 节点可以通过节点 API 执行参数操作，如 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP` 或 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python` 中所述。
外部进程可以通过节点实例化时默认创建的参数服务来执行参数操作。
默认创建的服务有：

* ``/node_name/describe_parameters``：使用 ``rcl_interfaces/srv/DescribeParameters`` 服务类型。
  给定一个参数名称列表，返回与这些参数相关联的描述符列表。
* ``/node_name/get_parameter_types``：使用 ``rcl_interfaces/srv/GetParameterTypes`` 服务类型。
  给定一个参数名称列表，返回与这些参数相关联的参数类型列表。
* ``/node_name/get_parameters``：使用 ``rcl_interfaces/srv/GetParameters`` 服务类型。
  给定一个参数名称列表，返回与这些参数相关联的参数值列表。
* ``/node_name/list_parameters``：使用 ``rcl_interfaces/srv/ListParameters`` 服务类型。
  给定一个可选的参数前缀列表，返回具有该前缀的可用参数列表。
  如果前缀为空，则返回所有参数。
* ``/node_name/set_parameters``：使用 ``rcl_interfaces/srv/SetParameters`` 服务类型。
  给定一个参数名称和值的列表，尝试在节点上设置这些参数。
  返回尝试设置每个参数的结果列表；其中一些可能成功，一些可能失败。
* ``/node_name/set_parameters_atomically``：使用 ``rcl_interfaces/srv/SetParametersAtomically`` 服务类型。
  给定一个参数名称和值的列表，尝试在节点上设置这些参数。
  返回尝试设置所有参数的单一结果，因此只要有一个失败，所有参数都视为失败。

运行节点时设置初始参数值
------------------------

在运行节点时，可以通过单独的命令行参数或 YAML 文件来设置初始参数值。
有关如何设置初始参数值的示例，请参阅 :ref:`NodeArgsParameters`。

启动节点时设置初始参数值
------------------------

在通过 ROS 2 启动设施运行节点时，也可以设置初始参数值。
有关如何通过 launch 指定参数的信息，请参阅 :doc:`本文档 <../../Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects>`。

在运行时操作参数值
------------------

``ros2 param`` 命令是与已运行节点交互参数的通用方式。
``ros2 param`` 使用如上所述的参数服务 API 来执行各种操作。
有关如何使用 ``ros2 param`` 的详细信息，请参阅 :doc:`此操作指南 <../../How-To-Guides/Using-ros2-param>`。

除了命令行接口外，还可以在运行时使用 ROS 2 客户端库以编程方式操作参数。
所有客户端库都提供了在节点运行时获取、设置和响应参数变化的 API。

客户端库的支持包括：
 * **C++（rclcpp）**：请参阅 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP` 和 :doc:`../../Tutorials/Intermediate/Monitoring-For-Parameter-Changes-CPP`。
 * **Python（rclpy）**：请参阅 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python` 和 :doc:`../../Tutorials/Intermediate/Monitoring-For-Parameter-Changes-Python`。

从 ROS 1 迁移
-------------

:doc:`启动文件迁移指南 <../../How-To-Guides/Migrating-from-ROS1/Migrating-Launch-Files>` 介绍了如何将 ``param`` 和 ``rosparam`` 启动标签从 ROS 1 迁移到 ROS 2。

:doc:`迁移指南 <../../How-To-Guides/Migrating-from-ROS1/Migrating-Parameters>` 介绍了如何将参数从 ROS 1 迁移到 ROS 2。
