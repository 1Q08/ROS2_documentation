.. redirect-from::

    About-ROS-2-Parameters
    Concepts/About-ROS-2-Parameters

参数
====

.. contents:: 目录
   :local:

概述
----

ROS 2 中的参数与单个节点相关联。
参数用于在节点启动时（以及运行时）配置节点，而无需修改代码。
参数的生命周期与节点的生命周期绑定在一起（尽管节点可以实现某种持久化机制，在重启后重新加载值）。

参数通过节点名、节点命名空间、参数名以及参数命名空间来定位。
提供参数命名空间是可选的。

每个参数都由键、值和描述符组成。
键是字符串，值可以是以下类型之一：``bool``、``int64``、``float64``、``string``、``byte[]``、``bool[]``、``int64[]``、``float64[]`` 或 ``string[]``。
默认情况下，所有描述符都是空的，但也可以包含参数描述、取值范围、类型信息以及额外约束。

有关 ROS 参数的实践教程，请参见 :doc:`../../Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters`。

参数背景
--------

声明参数
^^^^^^^^

默认情况下，一个节点需要在其整个生命周期内 *声明* 它将接受的所有参数。
这样可以确保节点启动时参数的类型和名称被明确定义，从而减少后续配置错误的机会。
请参见 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP` 或 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python` 以获取在节点中声明和使用参数的教程。

对于某些类型的节点，并非所有参数都能提前得知。
在这种情况下，可以在实例化节点时设置 ``allow_undeclared_parameters`` 为 ``true``，这允许节点在尚未声明参数时也可以读取和设置这些参数。

参数类型
^^^^^^^^

ROS 2 节点上的每个参数都有一个如概述中所述的预定义参数类型。
默认情况下，试图在运行时更改已声明参数的类型会失败。
这可以防止常见错误，例如把布尔值放入整数参数。

如果一个参数需要支持多种不同类型，并且使用该参数的代码可以处理这种情况，那么可以更改默认行为。
当参数被声明时，应使用 ``ParameterDescriptor`` 并将成员变量 ``dynamic_typing`` 设置为 ``true``。

参数回调
^^^^^^^^

ROS 2 节点可以注册两种不同类型的回调，以便在参数发生变化时得到通知。
这两种回调都是可选的。

第一种称为“设置参数”回调，可以通过节点 API 中的 ``add_on_set_parameters_callback`` 来设置。
回调接收一个不可变 ``Parameter`` 对象列表，并返回 ``rcl_interfaces/msg/SetParametersResult``。
该回调的主要目的是让用户能够检查即将发生的参数变更并显式拒绝该变更。

.. note::
   需要注意的是，“设置参数”回调不能有副作用。
   由于多个“设置参数”回调可以串联调用，因此单个回调无法知道后续回调是否会拒绝更新。
   如果某个回调对其所在类进行了修改，例如可能导致它与实际参数失去同步。
   若要在参数成功修改后获取回调，请参见下方第二种回调。

第二种回调称为“参数事件”回调，可以通过参数客户端 API 中的 ``on_parameter_event`` 来设置。
回调接收一个 ``rcl_interfaces/msg/ParameterEvent`` 对象，不返回任何内容。
当输入事件中的所有参数都已被声明、修改或删除后，会调用该回调。
该回调的主要目的是让用户能够对已成功接受的参数变化作出响应。

与参数交互
----------

ROS 2 节点可以通过节点 API 执行参数操作，如 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP` 或 :doc:`../../Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-Python` 中所述。
外部进程可以通过参数服务执行参数操作；当节点实例化时，这些参数服务会默认创建。
默认创建的服务有：

* ``/node_name/describe_parameters``：使用服务类型 ``rcl_interfaces/srv/DescribeParameters``。
  给定参数名称列表，返回与这些参数关联的描述符列表。
* ``/node_name/get_parameter_types``：使用服务类型 ``rcl_interfaces/srv/GetParameterTypes``。
  给定参数名称列表，返回与这些参数关联的参数类型列表。
* ``/node_name/get_parameters``：使用服务类型 ``rcl_interfaces/srv/GetParameters``。
  给定参数名称列表，返回与这些参数关联的参数值列表。
* ``/node_name/list_parameters``：使用服务类型 ``rcl_interfaces/srv/ListParameters``。
  给定可选参数前缀列表，返回具有该前缀的可用参数列表。
  如果前缀为空，则返回所有参数。
* ``/node_name/set_parameters``：使用服务类型 ``rcl_interfaces/srv/SetParameters``。
  给定参数名称和值列表，尝试在节点上设置这些参数。
  返回尝试设置每个参数的结果列表；其中一些可能成功，另一些可能失败。
* ``/node_name/set_parameters_atomically``：使用服务类型 ``rcl_interfaces/srv/SetParametersAtomically``。
  给定参数名称和值列表，尝试在节点上设置这些参数。
  返回一次尝试设置所有参数的单一结果；若有一个参数失败，则全部失败。

在运行节点时设置初始参数值
--------------------------

可以在运行节点时通过单个命令行参数或 YAML 文件设置初始参数值。
请参考 :ref:`NodeArgsParameters` 中的示例，以了解如何设置初始参数值。

通过 launch 方式启动节点时设置初始参数值
----------------------------------------

同样也可以通过 ROS 2 的 launch 设施在运行节点时设置初始参数值。
请参见 :doc:`本文档 <../../Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects>`，了解如何通过 launch 指定参数。

在运行时操作参数值
------------------

``ros2 param`` 命令是与已经运行节点交互参数的通用方式。
``ros2 param`` 使用上文描述的参数服务 API 来执行各种操作。
请参见 :doc:`this how-to guide <../../How-To-Guides/Using-ros2-param>`，以了解如何使用 ``ros2 param``。

从 ROS 1 迁移
-------------

:doc:`Launch 文件迁移指南 <../../How-To-Guides/Migrating-from-ROS1/Migrating-Launch-Files>` 说明了如何将 ROS 1 中的 ``param`` 与 ``rosparam`` launch 标签迁移到 ROS 2。

:doc:`迁移指南 <../../How-To-Guides/Migrating-from-ROS1/Migrating-Parameters>` 说明了如何将 ROS 1 中的参数迁移到 ROS 2。
