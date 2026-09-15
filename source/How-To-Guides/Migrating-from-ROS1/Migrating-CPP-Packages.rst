.. redirect-from::

   Migration-Guide
   Contributing/Migration-Guide
   The-ROS2-Project/Contributing/Migration-Guide

迁移 C++ 软件包参考
===================

.. contents:: 目录
   :depth: 2
   :local:

本页介绍如何把 C++ 软件包的一部分从 ROS 1 迁移到 ROS 2。
如果这是你第一次迁移 C++ 软件包，请先阅读 :doc:`C++ 迁移示例 <Migrating-CPP-Package-Example>`。
之后，在你迁移自己的软件包时，可以把本页作为参考。

构建工具
--------

ROS 2 不使用 ``catkin_make``、``catkin_make_isolated`` 或 ``catkin build``，而是使用命令行工具 `colcon <https://design.ros2.org/articles/build_tool.html>`__ 来构建和安装一组软件包。
参见 :doc:`初学者教程 <../../Tutorials/Beginner-Client-Libraries/Colcon-Tutorial>` 开始使用 ``colcon``。

将 ``CMakeLists.txt`` 更新为使用 *ament_cmake*
----------------------------------------------

ROS 2 的 C++ 软件包使用 `CMake <https://cmake.org/>`__，以及由 `ament_cmake <https://index.ros.org/p/ament_cmake/>`__ 提供的便捷函数。
请应用以下更改，以便使用 ``ament_cmake`` 而不是 ``catkin``。


要求更新的 CMake 版本
^^^^^^^^^^^^^^^^^^^^^

ROS 2 依赖的 CMake 版本比 ROS 1 使用的新。
在 `REP 2000 <https://reps.openrobotics.org/rep-2000/>`__ 中查找你所希望支持的 ROS 发行版使用的最低 CMake 版本，并在你的 ``CMakeLists.txt`` 顶部使用该版本。
例如，`ROS Humble 建议的最低支持版本是 3.14.4 <https://reps.openrobotics.org/rep-2000/#humble-hawksbill-may-2022-may-2027>`__。

.. code-block::

   cmake_minimum_required(VERSION 3.14.4)

将构建类型设置为 ament_cmake
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从你的 ``package.xml`` 中移除对 ``catkin`` 的所有依赖

.. code-block::

   # Remove this!
   <buildtool_depend>catkin</buildtool_depend>

添加对 ``ament_cmake_ros`` 的新依赖（`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/package.xml#L25>`__）：

.. code-block:: xml

   <buildtool_depend>ament_cmake_ros</buildtool_depend>

如果你的 ``package.xml`` 目前还没有 ``<export>`` 小节，请添加一个。
将 ``<build_type>`` 设置为 ``ament_cmake`` （`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/package.xml#L43-L45>`__）

.. code-block:: xml

   <export>
      <build_type>ament_cmake</build_type>
   </export>

添加对 ``ament_package()`` 的调用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在你的 ``CMakeLists.txt`` 底部插入对 ``ament_package()`` 的调用（`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/CMakeLists.txt#L127>`__）

.. code-block:: cmake

   # Add this to the bottom of your CMakeLists.txt
   ament_package()

更新 ``find_package()`` 调用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

把 ``find_package(catkin COMPONENTS ...)`` 调用替换为单独的 ``find_package()`` 调用（`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/CMakeLists.txt#L14-L18>`_）：

例如，把下面这段：

.. code-block::

   find_package(catkin REQUIRED COMPONENTS foo bar std_msgs)
   find_package(baz REQUIRED)

改为：

.. code-block:: cmake

   find_package(ament_cmake_ros REQUIRED)
   find_package(foo REQUIRED)
   find_package(bar REQUIRED)
   find_package(std_msgs REQUIRED)
   find_package(baz REQUIRED)


使用现代 CMake 目标
^^^^^^^^^^^^^^^^^^^

优先使用针对每个目标的 CMake 函数，这样你的软件包就能导出现代 CMake 目标。

如果你的 ``CMakeLists.txt`` 使用了 ``include_directories()``，请删除这些调用。

.. code-block::

   # Delete calls to include_directories like this one!
   include_directories(include ${catkin_INCLUDE_DIRS})

为你的软件包中的每个库添加一个 ``target_include_directories()`` 调用（`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/CMakeLists.txt#L24-L26>`__）。

.. code-block:: cmake

   target_include_directories(my_library PUBLIC
      "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
      "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>")

把所有 ``target_link_libraries()`` 调用改为使用现代 CMake 目标。
例如，如果你的 ROS 1 软件包像下面这样使用旧式标准 CMake 变量。

.. code-block::

   target_link_libraries(my_library ${catkin_LIBRARIES} ${baz_LIBRARIES})

那就把它改为使用具体的现代 CMake 目标。
如果你所依赖的软件包是 ``std_msgs`` 之类的消息软件包，请使用 ``${package_name_TARGETS}``。

.. code-block:: cmake

   target_link_libraries(my_library PUBLIC foo::foo bar::bar ${std_msgs_TARGETS} baz::baz)

根据你的库如何使用该依赖来选择 ``PUBLIC`` 或 ``PRIVATE`` （`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/CMakeLists.txt#L27-L31>`__）。

* 如果下游用户需要该依赖（例如你的库的公共 API 用到了它），请使用 ``PUBLIC``。
* 如果该依赖仅供你的库内部使用，请使用 ``PRIVATE``。

用各种 ament_cmake 调用替换 ``catkin_package()``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

假设你的 ``CMakeLists.txt`` 中有如下对 ``catkin_package`` 的调用：

.. code-block::

   catkin_package(
       INCLUDE_DIRS include
       LIBRARIES my_library
       CATKIN_DEPENDS foo bar std_msgs
       DEPENDS baz
   )

   install(TARGETS my_library
      ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
      LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
      RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
   )


替换 ``catkin_package(INCLUDE_DIRS ...)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

如果你已经使用了现代 CMake 目标和 ``target_include_directories()``，那就无需再做其他事情。
下游用户只要依赖你的现代 CMake 目标，就能获得包含目录。

替换 ``catkin_package(LIBRARIES ...)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用 ``ament_export_targets()`` 和 ``install(TARGETS ... EXPORT ...)`` 来替换 ``LIBRARIES`` 参数。

在安装 ``my_library`` 目标时使用 ``EXPORT`` 关键字（`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/CMakeLists.txt#L37-L41>`__）。

.. code-block:: cmake

   install(TARGETS my_library EXPORT export_my_package
      ARCHIVE DESTINATION lib
      LIBRARY DESTINATION lib
      RUNTIME DESTINATION bin
   )

对于库目标来说，上面是一个不错的默认写法。
如果你的软件包使用了不同的 ``CATKIN_*_DESTINATION`` 变量，请按如下方式转换：

.. list-table::
   :header-rows: 1

   * - **catkin**
     - **ament_cmake**
   * - CATKIN_GLOBAL_BIN_DESTINATION
     - bin
   * - CATKIN_GLOBAL_INCLUDE_DESTINATION
     - include
   * - CATKIN_GLOBAL_LIB_DESTINATION
     - lib
   * - CATKIN_GLOBAL_LIBEXEC_DESTINATION
     - lib
   * - CATKIN_GLOBAL_SHARE_DESTINATION
     - share
   * - CATKIN_PACKAGE_BIN_DESTINATION
     - lib/${PROJECT_NAME}
   * - CATKIN_PACKAGE_INCLUDE_DESTINATION
     - include/${PROJECT_NAME}
   * - CATKIN_PACKAGE_LIB_DESTINATION
     - lib
   * - CATKIN_PACKAGE_SHARE_DESTINATION
     - share/${PROJECT_NAME}

添加对 ``ament_export_targets()`` 的调用，名称与你给 ``EXPORT`` 关键字的名称相同（`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/CMakeLists.txt#L124-L125>`__）。

.. code-block:: cmake

   ament_export_targets(export_my_package)


替换 ``catkin_package(CATKIN_DEPENDS .. DEPENDS ..)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

你的软件包的使用者必须 ``find_package()`` 你的软件包公共 API 所使用的依赖。
在 ROS 1 中，这是通过 ``CATKIN_DEPENDS`` 和 ``DEPENDS`` 参数为下游用户完成的。
在 ROS 2 中，请使用 `ament_export_dependencies <https://github.com/ament/ament_cmake/blob/{REPOS_FILE_BRANCH}/ament_cmake_export_dependencies/cmake/ament_export_dependencies.cmake>`__ 来完成这件事。

.. code-block:: cmake

   ament_export_dependencies(
      foo
      bar
      std_msgs
      baz
   )

生成消息
^^^^^^^^

如果你的软件包同时包含 C++ 代码和 ROS 消息、服务或动作定义，请考虑把它拆分为两个软件包：

* 一个只包含 ROS 消息、服务和/或动作定义的软件包
* 一个包含 C++ 代码的软件包

向包含 ROS 消息的软件包的 ``package.xml`` 添加以下依赖：

1. 添加对 ``rosidl_default_generators`` 的 ``<buildtool_depend>`` （`示例 <https://github.com/ros2/common_interfaces/blob/d685509e9cb9f80bd320a347f2db954a73397ae7/std_msgs/package.xml#L19>`__）

   .. code-block:: xml

      <buildtool_depend>rosidl_default_generators</buildtool_depend>

2. 添加对 ``rosidl_default_runtime`` 的 ``<exec_depend>`` （`示例 <https://github.com/ros2/common_interfaces/blob/d685509e9cb9f80bd320a347f2db954a73397ae7/std_msgs/package.xml#L22>`__）

   .. code-block:: xml

      <exec_depend>rosidl_default_runtime</exec_depend>

3. 添加一个组名为 ``rosidl_interface_packages`` 的 ``<member_of_group>`` 标签（`示例 <https://github.com/ros2/common_interfaces/blob/d685509e9cb9f80bd320a347f2db954a73397ae7/std_msgs/package.xml#L26>`__）

   .. code-block:: xml

      <member_of_group>rosidl_interface_packages</member_of_group>

在你的 ``CMakeLists.txt`` 中，把 ``add_message_files``、``add_service_files`` 和 ``generate_messages`` 的调用替换为 `rosidl_generate_interfaces <https://github.com/ros2/rosidl/blob/{REPOS_FILE_BRANCH}/rosidl_cmake/cmake/rosidl_generate_interfaces.cmake>`__。
由于 `这个 bug <https://github.com/ros2/rosidl_typesupport/issues/120>`__，第一个参数必须是 ``${PROJECT_NAME}``。

例如，如果你的 ROS 1 软件包如下所示：

.. code-block::

   add_message_files(DIRECTORY msg FILES FooBar.msg Baz.msg)
   add_service_files(DIRECTORY srv FILES Ping.srv)

   add_action_files(DIRECTORY action FILES DoPong.action)
   generate_messages(
      DEPENDENCIES actionlib_msgs std_msgs geometry_msgs
   )

那么把它改为这样（`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2_msgs/CMakeLists.txt#L18-L25>`__）

.. code-block:: cmake

       rosidl_generate_interfaces(${PROJECT_NAME}
         "msg/FooBar.msg"
         "msg/Baz.msg"
         "srv/Ping.srv"
         "action/DoPong.action"
         DEPENDENCIES actionlib_msgs std_msgs geometry_msgs
       )

删除对 devel 空间的引用
^^^^^^^^^^^^^^^^^^^^^^^

删除对 *devel 空间* 的所有引用，例如 ``CATKIN_DEVEL_PREFIX``。
ROS 2 中没有与 *devel 空间* 等价的概念。


单元测试
^^^^^^^^

如果你的软件包使用了 `gtest <https://github.com/google/googletest>`__，那么：

* 把 ``CATKIN_ENABLE_TESTING`` 替换为 ``BUILD_TESTING``。
* 把 ``catkin_add_gtest`` 替换为 ``ament_add_gtest``。
* 为 ``ament_cmake_gtest`` 添加 ``find_package()``，而不是 ``GTest``

例如，如果你的 ROS 1 软件包像下面这样添加测试：

.. code-block::

      if (CATKIN_ENABLE_TESTING)
        find_package(GTest REQUIRED)
        include_directories(${GTEST_INCLUDE_DIRS})
        catkin_add_gtest(my_test src/test/some_test.cpp)
        target_link_libraries(my_test
          # ...
          ${GTEST_LIBRARIES})
      endif()

那么把它改为这样：

.. code-block:: CMake

      if (BUILD_TESTING)
        find_package(ament_cmake_gtest REQUIRED)
        ament_add_gtest(my_test src/test/test_something.cpp)
        target_link_libraries(my_test
          #...
         )
      endif()

向你的 ``package.xml`` 添加 ``<test_depend>ament_cmake_gtest</test_depend>`` （`示例 <https://github.com/ros2/geometry2/blob/d85102217f692746abea8546c8e41f0abc95c8b8/tf2/package.xml#L35>`__）。

.. code-block:: xml

   <test_depend>ament_cmake_gtest</test_depend>

代码检查工具
^^^^^^^^^^^^

ROS 2 的代码 :doc:`风格指南 <../../The-ROS2-Project/Contributing/Developer-Guide>` 与 ROS 1 不同。

如果你选择遵循 ROS 2 的风格指南，可以通过在 ``if(BUILD_TESTING)`` 代码块中添加以下几行来开启自动代码检查测试：

.. code-block:: cmake

   if(BUILD_TESTING)
      find_package(ament_lint_auto REQUIRED)
      ament_lint_auto_find_test_dependencies()
      # ...
   endif()

向你的 ``package.xml`` 添加以下依赖：

.. code-block:: xml

   <test_depend>ament_lint_auto</test_depend>
   <test_depend>ament_lint_common</test_depend>

更新源代码
----------

消息、服务和动作
^^^^^^^^^^^^^^^^

ROS 2 的消息、服务和动作的命名空间会在软件包名之后使用一个子命名空间（分别为 ``msg``、``srv`` 或 ``action``）。
因此包含语句形如：``#include <my_interfaces/msg/my_message.hpp>``。
对应的 C++ 类型名称则是：``my_interfaces::msg::MyMessage``。

共享指针类型以 typedef 的形式提供在消息结构体中：``my_interfaces::msg::MyMessage::SharedPtr`` 以及 ``my_interfaces::msg::MyMessage::ConstSharedPtr``。

更多细节请参见关于 `生成的 C++ 接口 <https://design.ros2.org/articles/generated_interfaces_cpp.html>`__ 的文章。

迁移时 include 需要做如下更改：


* 在软件包名和消息数据类型之间插入子文件夹 ``msg``
* 把被包含的文件名从驼峰式改为下划线分隔
* 从 ``*.h`` 改为 ``*.hpp``

.. code-block:: cpp

   // ROS 1 style is in comments, ROS 2 follows, uncommented.
   // # include <geometry_msgs/PointStamped.h>
   #include <geometry_msgs/msg/point_stamped.hpp>

   // geometry_msgs::PointStamped point_stamped;
   geometry_msgs::msg::PointStamped point_stamped;

迁移还要求在所有实例中插入 ``msg`` 命名空间。

服务对象的使用
^^^^^^^^^^^^^^

ROS 2 中的服务回调没有布尔返回值。
发生失败时建议抛出异常，而不是返回 false。

.. code-block:: cpp

   // ROS 1 style is in comments, ROS 2 follows, uncommented.
   // #include "nav_msgs/GetMap.h"
   #include "nav_msgs/srv/get_map.hpp"

   // bool service_callback(
   //   nav_msgs::GetMap::Request & request,
   //   nav_msgs::GetMap::Response & response)
   void service_callback(
     const std::shared_ptr<nav_msgs::srv::GetMap::Request> request,
     std::shared_ptr<nav_msgs::srv::GetMap::Response> response)
   {
     // ...
     // return true;  // or false for failure
   }

ros::Time 的用法
^^^^^^^^^^^^^^^^

对于 ``ros::Time`` 的用法：

* 把所有 ``ros::Time`` 实例替换为 ``rclcpp::Time``

* 如果你的消息或代码使用了 std_msgs::Time：

  * 把所有 std_msgs::Time 实例转换为 builtin_interfaces::msg::Time

  * 把所有 ``#include "std_msgs/time.h`` 转换为 ``#include "builtin_interfaces/msg/time.hpp"``

  * 把所有使用 std_msgs::Time 字段 ``nsec`` 的实例转换为使用 builtin_interfaces::msg::Time 字段 ``nanosec``

ros::Rate 的用法
^^^^^^^^^^^^^^^^

有一个等价的类型 ``rclcpp::Rate``，它基本上可以直接替代 ``ros::Rate``。


Boost
^^^^^

Boost 以前提供的许多功能已经被集成到 C++ 标准库中。
因此我们希望利用这些新的核心特性，并尽可能避免对 boost 的依赖。

共享指针
~~~~~~~~

要把共享指针从 boost 切换到标准 C++，请替换以下实例：


* ``#include <boost/shared_ptr.hpp>`` 替换为 ``#include <memory>``
* ``boost::shared_ptr`` 替换为 ``std::shared_ptr``

可能还有诸如 ``weak_ptr`` 之类的变体，你也需要一并转换。

此外，推荐使用 ``using`` 而不是 ``typedef``。
``using`` 在模板逻辑中能更好地工作。
详情参见 `这里 <https://stackoverflow.com/questions/10747810/what-is-the-difference-between-typedef-and-using-in-c11>`__

线程/互斥锁
~~~~~~~~~~~

ROS 代码库中常用的另一部分 boost 内容是 ``boost::thread`` 中的互斥锁。


* 把 ``boost::mutex::scoped_lock`` 替换为 ``std::unique_lock<std::mutex>``
* 把 ``boost::mutex`` 替换为 ``std::mutex``
* 把 ``#include <boost/thread/mutex.hpp>`` 替换为 ``#include <mutex>``

无序映射
~~~~~~~~

替换：


* ``#include <boost/unordered_map.hpp>`` 替换为 ``#include <unordered_map>``
* ``boost::unordered_map`` 替换为 ``std::unordered_map``

function
~~~~~~~~

替换：


* ``#include <boost/function.hpp>``  替换为 ``#include <functional>``
* ``boost::function`` 替换为 ``std::function``
