迁移接口
========

.. contents:: 目录
   :depth: 2
   :local:

在 ROS 2 中，消息、服务和动作被统称为 ``接口（interfaces）``。

接口定义
--------

消息文件必须以 ``.msg`` 结尾，并且必须位于子文件夹 ``msg`` 中。
服务文件必须以 ``.srv`` 结尾，并且必须位于子文件夹 ``srv`` 中。
动作文件必须以 ``.action`` 结尾，并且必须位于子文件夹 ``action`` 中。

这些文件可能需要更新，以符合
`ROS 接口定义 <http://design.ros2.org/articles/legacy_interface_definition.html>`__。
一些原始类型已被移除，并且在 ROS 1 中作为内置类型的
``duration`` 和 ``time`` 类型已被普通的消息定义所取代，
必须从 `builtin_interfaces <https://github.com/ros2/rcl_interfaces/tree/{REPOS_FILE_BRANCH}/builtin_interfaces>`__
包中使用。
此外，一些命名约定比 ROS 1 中更严格。
:doc:`概念文章 <../../Concepts/Basic/About-Interfaces>` 中提供了更多信息。

构建接口
--------

ROS 2 中构建接口的方式与 ROS 1 有很大不同。
接口只能从包含 ``CMakeLists.txt`` 的包中构建。
如果你正在开发一个纯 Python 包，那么接口应该放在一个
只包含接口的独立包中（无论如何这都是最佳实践）。
更多信息请参见 :doc:`自定义接口教程 <../../Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces>`。

将接口包迁移到 ROS 2
^^^^^^^^^^^^^^^^^^^^

在你的 ``package.xml`` 中：

* 添加 ``<buildtool_depend>rosidl_default_generators</buildtool_depend>``。
* 添加 ``<exec_depend>rosidl_default_runtime</exec_depend>``。
* 添加 ``<member_of_group>rosidl_interface_packages</member_of_group>``
* 对于每个依赖的消息包，添加 ``<depend>message_package</depend>``。

在你的 ``CMakeLists.txt`` 中：

* 启用 C++17

.. code-block:: cmake

   set(CMAKE_CXX_STANDARD 17)

* 添加 ``find_package(rosidl_default_generators REQUIRED)``
* 对于每个依赖的消息包，添加 ``find_package(message_package REQUIRED)``，
  并将 CMake 函数调用 ``generate_messages`` 替换为 ``rosidl_generate_interfaces``。

这将取代列出所有消息和服务文件的
``add_message_files`` 和 ``add_service_files``，它们可以被移除。

