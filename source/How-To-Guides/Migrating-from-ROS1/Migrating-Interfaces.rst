迁移接口
========

.. contents:: 目录
   :depth: 2
   :local:

在 ROS 2 中，消息、服务和动作统称为 ``interfaces``。

接口定义
--------

消息文件必须以 ``.msg`` 结尾，并且必须放在 ``msg`` 子目录中。
服务文件必须以 ``.srv`` 结尾，并且必须放在 ``srv`` 子目录中。
动作文件必须以 ``.action`` 结尾，并且必须放在 ``action`` 子目录中。

这些文件可能需要进行更新以符合 `ROS 接口定义 <http://design.ros2.org/articles/legacy_interface_definition.html>`__。
一些基本类型已被移除，ROS 1 中作为内置类型的 ``duration`` 和 ``time`` 已被普通的消息定义取代，必须从 `builtin_interfaces <https://github.com/ros2/rcl_interfaces/tree/{REPOS_FILE_BRANCH}/builtin_interfaces>`__ 软件包中使用。
此外，有些命名约定比 ROS 1 更为严格。
更多信息请参阅 :doc:`概念文章 <../../Concepts/Basic/About-Interfaces>`。

构建接口
--------

ROS 2 中接口的构建方式与 ROS 1 有本质区别。
接口只能从包含 ``CMakeLists.txt`` 的软件包中构建。
如果你开发的是纯 Python 软件包，那么接口应当放在一个只包含接口的独立软件包中（这本来就是最佳实践）。
更多信息请参阅 :doc:`自定义接口教程 <../../Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces>`。

将接口软件包迁移到 ROS 2
^^^^^^^^^^^^^^^^^^^^^^^^

在你的 ``package.xml`` 中：

* 添加 ``<buildtool_depend>rosidl_default_generators</buildtool_depend>``。
* 添加 ``<exec_depend>rosidl_default_runtime</exec_depend>``。
* 添加 ``<member_of_group>rosidl_interface_packages</member_of_group>``
* 对每个依赖的消息软件包，添加 ``<depend>message_package</depend>``。

在你的 ``CMakeLists.txt`` 中：

* 启用 C++17

.. code-block:: cmake

   set(CMAKE_CXX_STANDARD 17)

* 添加 ``find_package(rosidl_default_generators REQUIRED)``
* 对每个依赖的消息软件包，添加 ``find_package(message_package REQUIRED)``，并把对 CMake 函数 ``generate_messages`` 的调用替换为 ``rosidl_generate_interfaces``。

这会取代 ``add_message_files`` 和 ``add_service_files`` 中罗列的所有消息和服务文件，这些内容可以删除。

